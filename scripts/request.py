#!/usr/bin/env python3
"""Run one request as one cycle: send it exactly as its skill built it, file what comes back, and write its report.
See docs/projects.md.

Usage:
  request.py run <spec.json> [--stand-in] [--key-file F]
                                      send the request to its model endpoint, file what comes back into library/,
                                      the prompt as sent into prompts/<id>.txt, and write requests/<id>.html;
                                      a research request files into sources/
  request.py attach <id> <file> --as comparison|chart [--caption TEXT]
                                      embed an image the agent made to show the results in the request's report
  request.py resource <file>... --name NAME
                                      file shared material no model made, such as a canonical document, a pre-vis
                                      render, or a builder, into prompts/resources/ as <time>-<name>.<ext>
  request.py build "<command>" <output>... --name NAME
                                      run a builder, and file each file it makes into prompts/resources/
  request.py note <id> [--asked TEXT] [--why TEXT] [--notes TEXT]
                                      set the agent's own words in the report
  request.py show <id | library file> the full record of the request that made a file, as JSON
  request.py tell <id>                what the agent says when the request is done, word for word
  request.py list [--skill S] [--pipeline P]
  request.py check                    every report's files exist, every library file has its report, nothing in
                                      library/ or sources/ was changed or removed since it was committed
  request.py id <name>                the ID a request named <name> would get now

A spec is JSON:
  {"name": "keyframe-the-line", "skill": "generate-keyframe", "asked": "...", "why": "...",
   "pipeline": "001", "chain": "the line", "step": "keyframe", "depends_on": ["<request id>"],
   "endpoint": {"kind": "openai-image-edit" | "openai-image" | "fal" | "research",
                "model": "...", "settings": {...}},
   "prompt": "the text exactly as sent",
   "references": [{"file": "library/<file>", "role": "image 1, the layout of the shot"}],
   "canon": [{"name": "the front door: side in the far-end frame", "value": "left", "read_at": "<time>",
              "from": "pipeline/001/canon.sql"}],
   "outputs": ["<file to file>", ...]          for research: the files found
   "sources": [{"file": "...", "address": "...", "page": "...", "use": "..."}]   for research}
A request is one call to a model endpoint. What the agent or a builder makes is not a request: it goes into
prompts/resources/ when it is canon or is sent to a model, and is not kept otherwise. Names use local time.
The agent writes the spec; everything else in the report comes from what this script sent and received.
"""
import sys, os, re, json, base64, hashlib, html, shutil, subprocess, urllib.request, mimetypes, wave, datetime, struct, zlib

MEDIA_IMAGE = (".png", ".jpg", ".jpeg", ".webp", ".gif")
MEDIA_AUDIO = (".wav", ".mp3", ".flac", ".aif", ".aiff")
MEDIA_VIDEO = (".mp4", ".mov", ".webm")
CRED = "/mnt/Hot/.{}/credentials"


# ---- the project -------------------------------------------------------------------------------

def project_root(start="."):
    p = os.path.abspath(start)
    while p != "/":
        if os.path.isdir(os.path.join(p, "library")) and os.path.isdir(os.path.join(p, "requests")):
            return p
        p = os.path.dirname(p)
    sys.exit("not inside a project: no folder above holds both library/ and requests/")


def now():
    return datetime.datetime.now(datetime.timezone.utc)


def stamp(t=None):
    """A name's time: the user's local time, as the machine's clock gives it, so names read as the user's day."""
    return (t or now()).astimezone().strftime("%Y-%m-%d_%H-%M")


def slug(name):
    s = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    if not s: sys.exit("a request needs a name")
    return s


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()


def report_path(root, rid, research=False):
    return os.path.join(root, "sources" if research else "requests", rid + ".html")


def find_report(root, rid):
    for folder in ("requests", "sources"):
        p = os.path.join(root, folder, rid + ".html")
        if os.path.exists(p): return p
    sys.exit("no report for " + rid)


def read_data(path):
    m = re.search(r'<script type="application/json" id="request">(.*?)</script>', open(path).read(), re.S)
    if not m: sys.exit(path + " holds no request data")
    return json.loads(m.group(1).replace("<\\/", "</"))


def key(service, env, pattern, key_file=None):
    if os.environ.get(env): return os.environ[env]
    f = key_file or CRED.format(service)
    m = re.search(pattern, open(f).read())
    if not m: sys.exit("no key found in " + f)
    return m.group(0)


# ---- filing ------------------------------------------------------------------------------------

def file_into(root, folder, rid, sources, suffixes=None):
    """Copy each source into folder as <rid>.<ext>, or <rid>-<n>.<ext> when there are several. Never overwrite."""
    out = []
    for i, src in enumerate(sources):
        ext = os.path.splitext(src)[1].lower()
        tail = suffixes[i] if suffixes else (("-%d" % (i + 1)) if len(sources) > 1 else "")
        dst = os.path.join(root, folder, rid + tail + ext)
        if os.path.exists(dst): sys.exit("refusing to overwrite " + os.path.relpath(dst, root) + ": the library only grows")
        shutil.copyfile(src, dst)
        out.append(os.path.relpath(dst, root))
    return out


# ---- endpoints ---------------------------------------------------------------------------------

def stand_in(spec, tmp):
    """A stand-in endpoint for dry runs: returns one plain file of the kind asked, and spends nothing."""
    ext = spec.get("stand_in_ext") or (".wav" if spec["endpoint"].get("returns") == "audio" else ".png")
    path = os.path.join(tmp, "stand-in" + ext)
    if ext == ".wav":
        with wave.open(path, "w") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(8000); w.writeframes(b"\0\0" * 8000)
    else:
        raw = b"".join(b"\0" + b"\x80\x80\x80" * 16 for _ in range(9))
        chunk = lambda t, d: struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xffffffff)
        open(path, "wb").write(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", 16, 9, 8, 2, 0, 0, 0))
                               + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b""))
    sent = {"service": "stand-in", "note": "a dry run: nothing was sent to a model"}
    return [path], sent, {"cost": "nothing; stand-in"}


def openai_image(spec, root, tmp, edit, key_file):
    ep = spec["endpoint"]
    model = ep.get("model", "gpt-image-2.6-sunburst")
    settings = {"size": "1536x864", "quality": "high", "n": 1}
    settings.update(ep.get("settings", {}))
    url = "https://api.openai.com/v1/images/" + ("edits" if edit else "generations")
    k = key("openai", "OPENAI_API_KEY", r"sk-[A-Za-z0-9_\-]+", key_file)
    if edit:
        cmd = ["curl", "-s", url, "-H", "Authorization: Bearer " + k, "-F", "model=" + model]
        for r in spec["references"]: cmd += ["-F", "image[]=@" + os.path.join(root, r["file"])]
        cmd += ["--form-string", "prompt=" + spec["prompt"]]
        for name, value in settings.items(): cmd += ["-F", "%s=%s" % (name, value)]
    else:
        body = dict(model=model, prompt=spec["prompt"], **settings)
        cmd = ["curl", "-s", url, "-H", "Authorization: Bearer " + k, "-H", "Content-Type: application/json",
               "-d", json.dumps(body)]
    r = json.loads(subprocess.run(cmd, capture_output=True, text=True, timeout=900).stdout)
    if "error" in r: sys.exit("the endpoint refused: " + json.dumps(r["error"])[:600])
    paths = []
    for i, d in enumerate(r["data"]):
        p = os.path.join(tmp, "out-%d.png" % i)
        open(p, "wb").write(base64.b64decode(d["b64_json"]))
        paths.append(p)
    sent = {"service": "OpenAI", "url": url, "model": model, "settings": settings,
            "references_sent_as": "image[] in the order listed" if edit else "none"}
    return paths, sent, {"usage": r.get("usage"), "cost": "not returned by the endpoint"}


def fal(spec, root, tmp, key_file):
    ep = spec["endpoint"]
    body = {"prompt": spec["prompt"]}
    body.update(ep.get("settings", {}))
    for r in spec.get("references", []):
        field = r.get("field") or ep.get("reference_field", "image_urls")
        f = os.path.join(root, r["file"])
        body.setdefault(field, []).append("data:%s;base64,%s" % (
            mimetypes.guess_type(f)[0] or "application/octet-stream", base64.b64encode(open(f, "rb").read()).decode()))
    req = urllib.request.Request("https://fal.run/" + ep["model"], json.dumps(body).encode(),
                                 {"Authorization": "Key " + key("fal", "FAL_KEY", r"[A-Za-z0-9\-]+:[A-Za-z0-9]+", key_file),
                                  "Content-Type": "application/json"})
    r = json.load(urllib.request.urlopen(req, timeout=900))
    urls = []
    for field in ("audio", "image", "video"):
        v = r.get(field)
        if isinstance(v, dict) and v.get("url"): urls.append(v["url"])
    for field in ("images", "audios", "videos"):
        urls += [v["url"] for v in r.get(field) or [] if isinstance(v, dict) and v.get("url")]
    paths = []
    for i, u in enumerate(urls):
        ext = os.path.splitext(u.split("?")[0])[1] or ".bin"
        p = os.path.join(tmp, "out-%d%s" % (i, ext))
        urllib.request.urlretrieve(u, p)
        paths.append(p)
    seconds = (r.get("audio") or {}).get("duration") if isinstance(r.get("audio"), dict) else None
    cost = "not returned by the endpoint"
    if ep.get("price_per_minute") and seconds:
        cost = "about $%.3f, from the price, not a bill" % (seconds / 60 * float(ep["price_per_minute"]))
    sent = {"service": "fal", "url": "https://fal.run/" + ep["model"], "model": ep["model"],
            "settings": {k: v for k, v in body.items() if k != "prompt" and not str(v).startswith("['data:")},
            "references_sent_as": "data URIs, in the order listed, in each reference's field"}
    return paths, sent, {"seconds": seconds, "cost": cost}


# ---- the report --------------------------------------------------------------------------------

STYLE = """
:root{--bg:#fbfaf7;--fg:#1d1c1a;--muted:#6b675f;--line:#e2ded5;--card:#fff;--accent:#8a4b2a}
@media (prefers-color-scheme:dark){:root{--bg:#161514;--fg:#ece9e2;--muted:#a19b90;--line:#34312c;--card:#1f1d1b;--accent:#e0a37e}}
body{background:var(--bg);color:var(--fg);font:15px/1.55 system-ui,sans-serif;margin:0 auto;max-width:1100px;padding:24px 16px}
h1{font-size:22px;margin:0 0 4px}h2{font-size:15px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);
border-top:1px solid var(--line);padding-top:16px;margin-top:28px}
.meta{color:var(--muted)}pre{background:var(--card);border:1px solid var(--line);padding:12px;white-space:pre-wrap;
word-wrap:break-word;border-radius:6px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:12px}
figure{margin:0;background:var(--card);border:1px solid var(--line);border-radius:6px;padding:8px}
figure img,figure video{width:100%;border-radius:4px}figcaption{font-size:13px;color:var(--muted);margin-top:6px}
table{border-collapse:collapse;width:100%;display:block;overflow-x:auto}td,th{border-bottom:1px solid var(--line);padding:6px 8px;text-align:left;vertical-align:top}
a{color:var(--accent)}
"""


_previews = {}


def preview(path, width=480):
    """A small JPEG of an image, as a data URI, so a page shows it even where it cannot load neighbouring files."""
    if path in _previews: return _previews[path]
    try:
        from PIL import Image
        import io
        im = Image.open(path)
        im.thumbnail((width, width * 4))
        if im.mode not in ("RGB", "L"):
            bg = Image.new("RGB", im.size, (255, 255, 255))
            bg.paste(im.convert("RGBA"), mask=im.convert("RGBA").split()[-1]); im = bg
        buf = io.BytesIO(); im.save(buf, "JPEG", quality=78)
        uri = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
    except Exception:
        uri = None
    _previews[path] = uri
    return uri


def media_tag(src, embed=None, local=None):
    e = os.path.splitext(src)[1].lower()
    s = html.escape(embed or src)
    if e in MEDIA_IMAGE:
        small = preview(local) if local and not (embed or "").startswith("data:") and os.path.exists(local) else None
        if small: return '<a href="%s"><img src="%s" alt=""></a>' % (s, small)
        return '<img src="%s" alt="">' % s
    if e in MEDIA_AUDIO: return '<audio controls src="%s"></audio>' % s
    if e in MEDIA_VIDEO: return '<video controls src="%s"></video>' % s
    return '<a href="%s">%s</a>' % (s, html.escape(os.path.basename(src)))


def link(root, report, f):
    return os.path.relpath(os.path.join(root, f), os.path.dirname(report))


def render(root, data, path):
    esc = html.escape
    ep = data.get("sent", {})
    parts = ["<!doctype html><html lang='en'><head><meta charset='utf-8'>",
             "<meta name='viewport' content='width=device-width,initial-scale=1'>",
             "<title>%s</title><style>%s</style></head><body>" % (esc(data["id"]), STYLE),
             "<h1>%s</h1>" % esc(data["id"]),
             "<p class='meta'>%s · %s · started %s%s</p>" % (
                 esc(data.get("skill") or "no skill named"), esc(ep.get("service", "")), esc(data["started"]),
                 (" · pipeline %s" % esc(data["pipeline"])) if data.get("pipeline") else "")]
    parts.append("<h2>What was asked</h2><p>%s</p>" % esc(data.get("asked") or "not recorded"))
    parts.append("<h2>Why</h2><p>%s</p>" % esc(data.get("why") or "not recorded"))
    if data.get("written_afterwards"):
        parts.append("<p class='meta'>%s</p>" % esc(data["written_afterwards"]))
    parts.append("<h2>Endpoint</h2><pre>%s</pre>" % esc(json.dumps(ep, indent=1)))
    parts.append("<h2>Prompt, as sent</h2><pre>%s</pre>" % esc(data.get("prompt") or "none"))
    if data.get("references"):
        parts.append("<h2>References, in the order sent</h2><div class='grid'>")
        for i, r in enumerate(data["references"], 1):
            src = r.get("embedded") or link(root, path, r["file"])
            parts.append("<figure>%s<figcaption>%d. %s<br>%s</figcaption></figure>" % (
                media_tag(r.get("file") or "x.png", src, os.path.join(root, r["file"]) if r.get("file") else None), i, esc(r.get("role", "")), esc(r.get("file") or "kept only here")))
        parts.append("</div>")
    if data.get("canon"):
        parts.append("<h2>Canon read</h2><table><tr><th>Name</th><th>Value</th><th>Read</th><th>From</th></tr>")
        for c in data["canon"]:
            parts.append("<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % tuple(
                esc(str(c.get(k, ""))) for k in ("name", "value", "read_at", "from")))
        parts.append("</table>")
    if data.get("scripts"):
        parts.append("<h2>Scripts</h2><pre>%s</pre>" % esc(json.dumps(data["scripts"], indent=1)))
    if data.get("sources"):
        parts.append("<h2>Sources</h2><table><tr><th>File</th><th>Address</th><th>Use allowed</th></tr>")
        for s in data["sources"]:
            parts.append("<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (
                esc(s.get("file", "")), esc(s.get("address", "")), esc(s.get("use", ""))))
        parts.append("</table>")
    parts.append("<h2>Outputs</h2><div class='grid'>")
    for f in data.get("outputs", []):
        parts.append("<figure>%s<figcaption>%s</figcaption></figure>" % (media_tag(f, link(root, path, f), os.path.join(root, f)), esc(f)))
    parts.append("</div>" if data.get("outputs") else "<p>none</p></div>")
    if data.get("shown"):
        parts.append("<h2>Comparisons and charts</h2><div class='grid'>")
        for s in data["shown"]:
            src = s.get("embedded") or link(root, path, s["file"])
            parts.append("<figure>%s<figcaption>%s</figcaption></figure>" % (
                media_tag(s.get("file") or "x.png", src), esc(s.get("caption") or s.get("as") or "")))
        parts.append("</div>")
    parts.append("<h2>Result</h2><pre>%s</pre>" % esc(json.dumps(data.get("result", {}), indent=1)))
    if data.get("depends_on"):
        parts.append("<h2>Made after</h2><p>%s</p>" % ", ".join(
            "<a href='%s.html'>%s</a>" % (esc(d), esc(d)) for d in data["depends_on"]))
    if data.get("notes"): parts.append("<h2>Notes</h2><p>%s</p>" % esc(data["notes"]))
    blob = json.dumps(data, indent=1).replace("</", "<\\/")
    parts.append('<script type="application/json" id="request">%s</script></body></html>' % blob)
    open(path, "w").write("\n".join(parts))


# ---- commands ----------------------------------------------------------------------------------

def run(spec_file, stand=False, key_file=None):
    spec = json.load(open(spec_file))
    root = project_root(os.path.dirname(os.path.abspath(spec_file)) if spec.get("project") is None else spec["project"])
    started = now()
    rid = spec.get("id") or "%s-%s" % (stamp(started), slug(spec["name"]))
    kind = spec["endpoint"]["kind"]
    research = kind == "research"
    rpath = report_path(root, rid, research)
    if os.path.exists(rpath): sys.exit(rid + " already has a report: give the request another name")
    refs = []
    for r in spec.get("references", []):
        f = r.get("file")
        if f and not os.path.exists(os.path.join(root, f)): sys.exit("reference not found: " + f)
        refs.append(dict(r, sha256=sha(os.path.join(root, f))) if f else r)
    tmp = os.path.join(root, ".request-" + rid)
    os.makedirs(tmp, exist_ok=True)
    try:
        if stand: paths, sent, result = stand_in(spec, tmp)
        elif kind == "openai-image-edit": paths, sent, result = openai_image(spec, root, tmp, True, key_file)
        elif kind == "openai-image": paths, sent, result = openai_image(spec, root, tmp, False, key_file)
        elif kind == "fal": paths, sent, result = fal(spec, root, tmp, key_file)
        elif kind == "research":
            paths = [os.path.join(root, f) if not os.path.isabs(f) else f for f in spec.get("outputs", [])]
            sent = {"service": "research"}
            result = {"cost": spec["endpoint"].get("cost", "not recorded")}
        elif kind in ("script", "agent"):
            sys.exit("not a request: what the agent or a builder makes goes into prompts/resources/ (request.py resource or build)")
        else: sys.exit("unknown endpoint kind: " + kind)
        if research:
            names = ["-" + slug(os.path.splitext(os.path.basename(p))[0]) for p in paths]
            outputs = file_into(root, "sources", rid, paths, names)
        else:
            outputs = file_into(root, "library", rid, paths)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    if not research and spec.get("prompt"):
        os.makedirs(os.path.join(root, "prompts"), exist_ok=True)
        pp = os.path.join(root, "prompts", rid + ".txt")
        if os.path.exists(pp): sys.exit("refusing to overwrite " + os.path.relpath(pp, root))
        open(pp, "w").write(spec["prompt"])
    srcs = spec.get("sources", [])
    if research:
        by_name = {os.path.basename(s["file"]): s for s in srcs}
        srcs = [dict(by_name.get(os.path.basename(p), {}), file=o) for p, o in zip(paths, outputs)]
    data = {"record": 2, "id": rid, "name": spec["name"], "skill": spec.get("skill"), "pipeline": spec.get("pipeline"),
            "chain": spec.get("chain"), "step": spec.get("step"), "started": started.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "finished": now().strftime("%Y-%m-%dT%H:%M:%SZ"), "asked": spec.get("asked"), "why": spec.get("why"),
            "depends_on": spec.get("depends_on", []), "sent": sent, "prompt": spec.get("prompt"),
            "references": refs, "canon": spec.get("canon", []), "scripts": spec.get("scripts", []),
            "sources": srcs, "outputs": outputs, "output_sha256": {o: sha(os.path.join(root, o)) for o in outputs},
            "shown": [], "result": result, "notes": spec.get("notes"), "stand_in": bool(stand)}
    render(root, data, rpath)
    print(os.path.relpath(rpath, root))


def attach(rid, f, as_, caption=None):
    root = project_root()
    path = find_report(root, rid)
    data = read_data(path)
    uri = "data:%s;base64,%s" % (mimetypes.guess_type(f)[0] or "image/png", base64.b64encode(open(f, "rb").read()).decode())
    data["shown"].append({"embedded": uri, "as": as_, "caption": caption})
    render(root, data, path)
    print("embedded in " + os.path.relpath(path, root))


def resource(fs, name, date=None):
    root = project_root()
    os.makedirs(os.path.join(root, "prompts", "resources"), exist_ok=True)
    rid = "%s-%s" % (stamp(date), slug(name))
    for f in file_into(root, "prompts/resources", rid, fs): print(f)


def build(command, outputs, name):
    root = project_root()
    p = subprocess.run(command, shell=True, cwd=root, capture_output=True, text=True, timeout=3600)
    if p.returncode: sys.exit("the builder failed:\n" + (p.stdout + p.stderr)[-2000:])
    missing = [o for o in outputs if not os.path.exists(os.path.join(root, o))]
    if missing: sys.exit("the builder made no " + ", ".join(missing))
    resource([os.path.join(root, o) for o in outputs], name)


def note(rid, **kw):
    root = project_root()
    path = find_report(root, rid)
    data = read_data(path)
    for k, v in kw.items():
        if v is not None: data[k] = v
    render(root, data, path)


def show(what):
    root = project_root()
    base = os.path.basename(what)
    for p, d in all_reports(root):
        made = d.get("outputs", [])
        if d["id"] == base or any(os.path.basename(f) == base for f in made):
            print(json.dumps(d, indent=1)); return
    sys.exit("no report names " + what)


def tell(rid):
    root = project_root()
    path = find_report(root, rid)
    d = read_data(path)
    sent = d.get("sent", {})
    lines = ["**%s** (%s)" % (d["id"], d.get("skill") or "no skill named"),
             "- Asked: %s" % (d.get("asked") or "not recorded"),
             "- Why: %s" % (d.get("why") or "not recorded"),
             "- Sent to: %s%s%s" % (sent.get("service", "not recorded"), (", " + sent["model"]) if sent.get("model") else "",
                                    (", " + json.dumps(sent["settings"])) if sent.get("settings") else "")]
    lines.append("- References, in the order sent:" if d.get("references") else "- References: none")
    for i, r in enumerate(d.get("references", []), 1):
        lines.append("  %d. %s, %s" % (i, r.get("file") or "kept in the report", r.get("role", "")))
    if d.get("canon"):
        lines.append("- Canon read:")
        for c in d["canon"]: lines.append("  - %s = %s (%s, %s)" % (c["name"], c["value"], c.get("from", ""), c.get("read_at", "")))
    if d.get("scripts"): lines.append("- Scripts: " + "; ".join(s.get("command") or s.get("file", "") for s in d["scripts"]))
    lines.append("- Outputs: " + (", ".join(d.get("outputs", [])) or "none"))
    for s in d.get("shown", []): lines.append("- Shown in the report: %s" % (s.get("caption") or s.get("as")))
    lines.append("- Cost: %s" % (d.get("result", {}).get("cost") or "not recorded"))
    lines.append("- Report: " + os.path.relpath(path, root))
    lines.append("- Prompt, as sent:")
    lines.append("```text\n%s\n```" % (d.get("prompt") or "none"))
    print("\n".join(lines))


def all_reports(root):
    for folder in ("requests", "sources"):
        d = os.path.join(root, folder)
        for f in sorted(os.listdir(d)) if os.path.isdir(d) else []:
            if f.endswith(".html"):
                try: yield os.path.join(d, f), read_data(os.path.join(d, f))
                except SystemExit: pass


def listing(skill=None, pipeline=None):
    for p, d in all_reports(project_root()):
        if skill and d.get("skill") != skill: continue
        if pipeline and d.get("pipeline") != pipeline: continue
        print(d["id"], d.get("skill") or "", " ".join(d.get("outputs", [])))


def check():
    root = project_root()
    problems, owned = [], set()
    for p, d in all_reports(root):
        for r in d.get("references", []):
            if r.get("file") and not os.path.exists(os.path.join(root, r["file"])):
                problems.append("%s: reference missing: %s" % (d["id"], r["file"]))
        for o in d.get("outputs", []):
            owned.add(o)
            if not os.path.exists(os.path.join(root, o)): problems.append("%s: output missing: %s" % (d["id"], o))
        for o, h in (d.get("output_sha256") or {}).items():
            if os.path.exists(os.path.join(root, o)) and sha(os.path.join(root, o)) != h:
                problems.append("%s: output changed since it was made: %s" % (d["id"], o))
    for folder in ("library", "sources"):
        for f in sorted(os.listdir(os.path.join(root, folder))) if os.path.isdir(os.path.join(root, folder)) else []:
            rel = folder + "/" + f
            if f.endswith(".html") and folder == "sources": continue
            if rel not in owned: problems.append("no report made " + rel)
    g = subprocess.run(["git", "status", "--porcelain", "--", "library", "sources", "prompts"], cwd=root, capture_output=True, text=True)
    for line in g.stdout.splitlines():
        if set(line[:2]) & set("MDR"): problems.append("changed or removed in a folder that only grows: " + line[3:])
    for x in problems: print(x)
    print("%d reports checked, %d problems" % (sum(1 for _ in all_reports(root)), len(problems)))
    sys.exit(1 if problems else 0)


def opts(a):
    o, rest, i = {}, [], 0
    while i < len(a):
        if a[i].startswith("--"):
            k = a[i][2:].replace("-", "_")
            if k == "stand_in": o[k] = True; i += 1
            else: o[k] = a[i + 1]; i += 2
        else: rest.append(a[i]); i += 1
    return o, rest


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"): print(__doc__); sys.exit()
    cmd = sys.argv[1]
    o, rest = opts(sys.argv[2:])
    if cmd == "run": run(rest[0], o.get("stand_in", False), o.get("key_file"))
    elif cmd == "attach": attach(rest[0], rest[1], o["as"], o.get("caption"))
    elif cmd == "note": note(rest[0], asked=o.get("asked"), why=o.get("why"), notes=o.get("notes"))
    elif cmd == "show": show(rest[0])
    elif cmd == "tell": tell(rest[0])
    elif cmd == "resource": resource(rest, o["name"])
    elif cmd == "build": build(rest[0], rest[1:], o["name"])
    elif cmd == "list": listing(o.get("skill"), o.get("pipeline"))
    elif cmd == "check": check()
    elif cmd == "id": print("%s-%s" % (stamp(), slug(rest[0])))
    else: print(__doc__)
