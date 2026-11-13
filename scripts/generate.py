#!/usr/bin/env python3
"""Send a prompt to a model exactly as written, save the result, and write its record (docs/records.md).

Usage:
  generate.py image-edit --prompt FILE --out PNG --kind K --image FILE ROLE [--image FILE ROLE]...
                         [--model M] [--size WxH] [--quality Q] [--key-file F] [record options]
  generate.py image      --prompt FILE --out PNG --kind K [--model M] [--size WxH] [--quality Q] [--key-file F] [record options]
  generate.py audio      --prompt FILE --out WAV --kind K [--endpoint E] [--param NAME VALUE]... [--audio FILE ROLE]...
                         [--price-per-minute USD] [--key-file F] [record options]

Record options: --camera C --place P --floor-plan F --contents JSON|@FILE --notes TEXT.
An image made from others inherits image 1's camera, place, floor plan, and contents unless they are given;
give --contents whenever the request changed what is in the frame.
image-edit and image use OpenAI's image API (key from OPENAI_API_KEY or --key-file);
audio uses fal (key from FAL_KEY or --key-file), Seed Audio 1.0 by default.
"""
import sys, os, re, json, base64, subprocess, urllib.request, mimetypes, wave
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import records


def args(a):
    o = {"image": [], "audio": [], "param": []}
    i = 0
    while i < len(a):
        k = a[i][2:].replace("-", "_")
        if k in ("image", "audio", "param"): o[k].append((a[i + 1], a[i + 2])); i += 3
        else: o[k] = a[i + 1]; i += 2
    return o


def key(o, env, pattern):
    if os.environ.get(env): return os.environ[env]
    m = re.search(pattern, open(o["key_file"]).read())
    if not m: sys.exit("no key found in " + o["key_file"])
    return m.group(0)


def contents_of(o, first_image):
    c = o.get("contents")
    if c: return json.load(open(c[1:])) if c.startswith("@") else json.loads(c)
    src = records.read(first_image) if first_image else None
    return (src or {}).get("contents")


def save_record(o, made_by, made_from):
    first = made_from[0]["file"] if made_from else None
    src = (records.read(first) if first else None) or {}
    notes = o.get("notes")
    if made_from and not o.get("contents") and src.get("contents"):
        notes = ((notes + " ") if notes else "") + "Contents inherited from image 1."
    records.write(o["out"], o["kind"], made_by=made_by, prompt=os.path.abspath(o["prompt"]),
                  made_from=[{"file": os.path.abspath(m["file"]), "role": m["role"]} for m in made_from],
                  camera=o.get("camera") or src.get("camera"), place=o.get("place") or src.get("place"),
                  floor_plan=o.get("floor_plan") or src.get("floor_plan"), contents=contents_of(o, first), notes=notes)


def openai_image(o, edit):
    model, size, quality = o.get("model", "gpt-image-2.6-sunburst"), o.get("size", "1536x864"), o.get("quality", "high")
    endpoint = "images/edits" if edit else "images/generations"
    prompt = open(o["prompt"]).read().strip()
    k = key(o, "OPENAI_API_KEY", r"sk-[A-Za-z0-9_\-]+")
    if edit:
        cmd = ["curl", "-s", "https://api.openai.com/v1/" + endpoint, "-H", "Authorization: Bearer " + k, "-F", "model=" + model]
        for f, _ in o["image"]: cmd += ["-F", "image[]=@" + f]
        cmd += ["--form-string", "prompt=" + prompt, "-F", "size=" + size, "-F", "quality=" + quality, "-F", "n=1"]
    else:
        body = json.dumps({"model": model, "prompt": prompt, "size": size, "quality": quality, "n": 1})
        cmd = ["curl", "-s", "https://api.openai.com/v1/" + endpoint, "-H", "Authorization: Bearer " + k,
               "-H", "Content-Type: application/json", "-d", body]
    r = json.loads(subprocess.run(cmd, capture_output=True, text=True, timeout=900).stdout)
    if "error" in r: sys.exit("ERROR " + json.dumps(r["error"])[:600])
    open(o["out"], "wb").write(base64.b64decode(r["data"][0]["b64_json"]))
    made_by = {"service": "OpenAI", "endpoint": endpoint, "model": model, "size": size, "quality": quality, "n": 1,
               "usage": r.get("usage"), "cost": "not returned"}
    save_record(o, made_by, [{"file": f, "role": role} for f, role in o["image"]])
    print(json.dumps(r.get("usage")))


def fal_audio(o):
    endpoint = o.get("endpoint", "bytedance/seed-audio-1.0")
    body = {"prompt": open(o["prompt"]).read().strip()}
    for name, value in o["param"]:
        try: body[name] = json.loads(value)
        except ValueError: body[name] = value
    if o["audio"]:
        body["audio_urls"] = ["data:%s;base64,%s" % (mimetypes.guess_type(f)[0] or "audio/wav",
                                                     base64.b64encode(open(f, "rb").read()).decode()) for f, _ in o["audio"]]
    req = urllib.request.Request("https://fal.run/" + endpoint, json.dumps(body).encode(),
                                 {"Authorization": "Key " + key(o, "FAL_KEY", r"[A-Za-z0-9\-]+:[A-Za-z0-9]+"),
                                  "Content-Type": "application/json"})
    r = json.load(urllib.request.urlopen(req, timeout=900))
    urllib.request.urlretrieve(r["audio"]["url"], o["out"])
    seconds = r["audio"].get("duration")
    if seconds is None and o["out"].endswith(".wav"):
        with wave.open(o["out"]) as w: seconds = w.getnframes() / w.getframerate()
    settings = {k: v for k, v in body.items() if k not in ("prompt", "audio_urls")}
    made_by = {"service": "fal", "endpoint": endpoint, "settings": settings, "seconds": seconds,
               "cost": ("about $%.3f, from the price, not a bill" % (seconds / 60 * float(o["price_per_minute"])))
               if o.get("price_per_minute") and seconds else "not returned"}
    save_record(o, made_by, [{"file": f, "role": role} for f, role in o["audio"]])
    print(json.dumps({"seconds": seconds, "cost": made_by["cost"]}))


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"): print(__doc__); sys.exit()
    cmd, o = sys.argv[1], args(sys.argv[2:])
    for need in ("prompt", "out", "kind"):
        if need not in o: sys.exit("--" + need + " is required: no result without its record")
    if cmd == "image-edit": openai_image(o, True)
    elif cmd == "image": openai_image(o, False)
    elif cmd == "audio": fal_audio(o)
    else: print(__doc__)
