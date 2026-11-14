#!/usr/bin/env python3
"""Records: the paper trail of every file a film is made of. See docs/records.md.

Usage:
  records.py write <file> --kind K [--made-by JSON] [--prompt P] [--from FILE ROLE]... [--camera C] [--place P]
                          [--floor-plan F] [--contents JSON] [--notes TEXT]
  records.py adopt <file>... [--moved OLD NEW]... [--kind K] [--copies]
                                       write records from older ones (a run's .json, a v001 folder's sources.json,
                                       a .source.txt, an animatic's assembly .json), or, with --copies, a file in a set from
                                       the file with the same bytes (never for a builder's renders); --moved follows folders that have moved since
  records.py copy <src> <dst>          copy a file with a record of its source
  records.py move <src> <dst>          move a file and its record, and rewrite every record that points at it
  records.py trace <file> [--out PREFIX] its whole paper trail, as a list and, with --out, a map (needs graphviz)
  records.py children <file>           what was made from it
  records.py find [--kind K] [--camera C] [--contains NAME]
  records.py check [<file>...]         problems in the records of these files and everything they trace back to;
                                       with no files, every record in the project
The project's root is the nearest folder above the file holding .git, or the current folder.
"""
import json, os, sys, shutil, subprocess, datetime, hashlib

MEDIA = (".png", ".jpg", ".jpeg", ".webp", ".wav", ".mp3", ".mp4", ".mov", ".flac", ".aif", ".aiff")
VERSION = 1


def root_of(path):
    p = os.path.abspath(path if os.path.isdir(path) else os.path.dirname(path) or ".")
    while p != "/":
        if os.path.exists(os.path.join(p, ".git")):
            return p
        p = os.path.dirname(p)
    return os.getcwd()


def rel(path, root):
    return os.path.relpath(os.path.abspath(path), root)


def record_path(file):
    return os.path.splitext(file)[0] + ".record.json"


def read(file):
    rp = record_path(file)
    return json.load(open(rp)) if os.path.exists(rp) else None


def write(file, kind, made_by=None, prompt=None, made_from=None, camera=None, place=None, floor_plan=None,
          contents=None, source=None, notes=None, date=None, root=None):
    root = root or root_of(file)
    r = {"record": VERSION, "file": rel(file, root), "kind": kind,
         "date": date or datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}
    if made_by: r["made_by"] = made_by
    if prompt: r["prompt"] = rel(prompt, root) if os.path.isabs(prompt) else prompt
    if made_from:
        r["made_from"] = [{"file": rel(m["file"], root) if os.path.isabs(m["file"]) else m["file"], "role": m.get("role", "")}
                          for m in made_from]
    for k, v in (("camera", camera), ("place", place), ("floor_plan", floor_plan), ("contents", contents),
                 ("source", source), ("notes", notes)):
        if v is not None: r[k] = v
    json.dump(r, open(record_path(file), "w"), indent=1)
    return r


def all_records(root):
    for d, dirs, files in os.walk(root):
        dirs[:] = [x for x in dirs if not x.startswith(".")]
        for f in files:
            if f.endswith(".record.json"):
                p = os.path.join(d, f)
                try:
                    yield p, json.load(open(p))
                except Exception:
                    yield p, None


def copy(src, dst):
    root = root_of(dst)
    shutil.copy2(src, dst)
    s = read(src) or {}
    write(dst, "copy", made_from=[{"file": src, "role": "copied from"}], camera=s.get("camera"), place=s.get("place"),
          floor_plan=s.get("floor_plan"), contents=s.get("contents"), root=root)


def move(src, dst):
    root = root_of(src)
    old, new = rel(src, root), rel(dst, root)
    shutil.move(src, dst)
    if os.path.exists(record_path(src)):
        shutil.move(record_path(src), record_path(dst))
        r = json.load(open(record_path(dst))); r["file"] = new; json.dump(r, open(record_path(dst), "w"), indent=1)
    n = 0
    for p, r in all_records(root):
        if not r: continue
        changed = False
        for m in r.get("made_from", []):
            if m["file"] == old: m["file"] = new; changed = True
        if r.get("prompt") == old: r["prompt"] = new; changed = True
        if changed: json.dump(r, open(p, "w"), indent=1); n += 1
    print(f"moved {old} -> {new}; {n} records rewritten")


def walk(file, root, seen=None, edges=None):
    seen = seen if seen is not None else {}; edges = edges if edges is not None else []
    key = rel(file, root)
    if key in seen: return seen, edges
    r = read(os.path.join(root, key))
    seen[key] = r
    for m in (r or {}).get("made_from", []):
        edges.append((m["file"], key, m.get("role", "")))
        walk(os.path.join(root, m["file"]), root, seen, edges)
    return seen, edges


def problems(key, r, root):
    out = []
    path = os.path.join(root, key)
    if r is None:
        if key.lower().endswith(MEDIA): out.append("no record")
        return out
    if not os.path.exists(path): out.append("the file it describes is missing")
    for m in r.get("made_from", []):
        if not os.path.exists(os.path.join(root, m["file"])): out.append(f"points at a missing file: {m['file']}")
    if r.get("kind") == "copy" and not r.get("made_from"): out.append("a copy with no source")
    if r.get("prompt") and not os.path.exists(os.path.join(root, r["prompt"])): out.append(f"its prompt is missing: {r['prompt']}")
    if key.lower().endswith((".png", ".jpg", ".jpeg", ".webp")) and r.get("kind") not in ("research photo",) and not r.get("contents"):
        out.append("no contents")
    return out


def trace(file, out=None):
    root = root_of(file)
    seen, edges = walk(file, root)
    for k, r in seen.items():
        p = problems(k, r, root)
        print(("  " if not p else "! ") + k + (f"  ({r['kind']})" if r else "") + ("  - " + "; ".join(p) if p else ""))
    if out:
        with open(out + ".dot", "w") as f:
            f.write('digraph G { rankdir=LR; node [shape=box, fontname="DejaVu Sans", fontsize=10]; edge [fontname="DejaVu Sans", fontsize=8];\n')
            for k, r in seen.items():
                p = problems(k, r, root)
                col = "#d9ead3" if not p else "#fce5cd" if p == ["no contents"] else "#f4c7c3"
                lab = "/".join(k.split("/")[-2:]) + ("\\n" + r["kind"] if r else "\\nno record")
                f.write(f'"{k}" [label="{lab}", style=filled, fillcolor="{col}"];\n')
            for a, b, role in edges:
                f.write(f'"{a}" -> "{b}" [label="{role[:40]}"];\n')
            f.write("}\n")
        subprocess.run(["dot", "-Tpng", "-Gdpi=90", out + ".dot", "-o", out + ".png"], check=True)
        print("map:", out + ".png")
    return seen


def children(file):
    root = root_of(file); key = rel(file, root)
    for p, r in all_records(root):
        if r and any(m["file"] == key for m in r.get("made_from", [])):
            print(r["file"], "-", next(m["role"] for m in r["made_from"] if m["file"] == key))


def find(root, kind=None, camera=None, contains=None):
    for p, r in all_records(root):
        if not r: continue
        if kind and r.get("kind") != kind: continue
        if camera and r.get("camera") != camera: continue
        if contains and not any(c.get("name") == contains for c in r.get("contents", [])): continue
        print(r["file"])


def check(files, root):
    bad = 0
    keys = {}
    if files:
        for f in files:
            seen, _ = walk(f, root); keys.update(seen)
    else:
        for p, r in all_records(root):
            if r: keys[r["file"]] = r
    for k, r in sorted(keys.items()):
        for pr in problems(k, r, root):
            print(f"{k}: {pr}"); bad += 1
    print(f"{len(keys)} files checked, {bad} problems")
    return bad


KINDS = {"animatic keyframe": "keyframe", "animatic layout drawing": "layout drawing"}
_texts = {}


def prompt_file(text, root):
    """The project's prompt file whose text is exactly this prompt."""
    if not _texts:
        for d, dirs, files in os.walk(root):
            dirs[:] = [x for x in dirs if not x.startswith(".") and x != "renders"]
            for f in files:
                if f.endswith((".txt", ".md")):
                    p = os.path.join(d, f)
                    try: _texts.setdefault(open(p).read().strip(), rel(p, root))
                    except Exception: pass
    return _texts.get(text.strip())


def resolve(path, root, moved):
    """A path from an old record, relative to the root, following folders that have moved since."""
    p = rel(path, root) if os.path.isabs(path) else path
    if not os.path.exists(os.path.join(root, p)):
        for old, new in moved:
            if p.startswith(old) and os.path.exists(os.path.join(root, new + p[len(old):])): return new + p[len(old):]
    return p


def same_bytes(file, root):
    h = hashlib.md5(open(file, "rb").read()).hexdigest(); size = os.path.getsize(file)
    for d, dirs, files in os.walk(root):
        dirs[:] = [x for x in dirs if not x.startswith(".")]
        for f in files:
            q = os.path.join(d, f)
            if q != os.path.abspath(file) and f.endswith(os.path.splitext(file)[1]) and os.path.getsize(q) == size \
                    and hashlib.md5(open(q, "rb").read()).hexdigest() == h:
                return q


def adopt(file, moved=(), kind=None, copies=False):
    """Write a record for a file from whatever older record it has, keeping the older one."""
    root = root_of(file); file = os.path.abspath(file); stem = os.path.splitext(file)[0]
    old = read(file) or {}
    keep = {k: old[k] for k in ("camera", "place", "floor_plan", "contents", "notes") if k in old}
    keep["date"] = datetime.datetime.fromtimestamp(os.path.getmtime(file), datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    R = lambda p: resolve(p, root, moved)
    j, d = stem + ".json", os.path.dirname(file)
    if file.endswith(".mp4"):
        n = os.path.basename(stem).rsplit("-", 1)[-1]
        spec = os.path.join(d, "assembly-%s.json" % n)
        if not os.path.exists(spec) and n == "1": spec = os.path.join(d, "assembly.json")
        s = json.load(open(spec))
        mf = [{"file": R(f["image"]), "role": "frame, %s to %s s" % (f["in"], f["out"])} for f in s["frames"]]
        mf.append({"file": R(s["bed"]["audio"]), "role": "sound bed, at %s dB" % s["bed"].get("gain_db", 0)})
        mf += [{"file": R(c["audio"]), "role": "clip %s to %s s, laid at %s s, at %s dB" % (c["from"], c["to"], c["at"], c.get("gain_db", 0))}
               for c in s.get("clips", [])]
        return write(file, kind or "video", {"tool": "build-animatic/scripts/assemble.py", "settings":
                     {k: s[k] for k in ("length", "fps", "size") if k in s}, "cost": "nothing; local"},
                     rel(spec, root), mf, root=root, **keep)
    if os.path.exists(stem + ".source.txt"):
        t = dict(l.split(": ", 1) for l in open(stem + ".source.txt").read().splitlines() if ": " in l)
        return write(file, "research photo", source={"address": t.get("Image"), "page": t.get("Source page"), "use": t.get("Use")},
                     root=root, **keep)
    if os.path.exists(os.path.join(d, "sources.json")) and os.path.basename(file).startswith("image."):
        s = json.load(open(os.path.join(d, "sources.json")))
        q = json.load(open(os.path.join(d, "request.json"))) if os.path.exists(os.path.join(d, "request.json")) else {}
        mb = {"service": "OpenRouter", "model": q.get("model"), "settings": {k: q[k] for k in ("aspect_ratio", "quality", "seed", "n") if k in q},
              "cost": "see response.json"}
        pr = R(s["prompt"]) if s.get("prompt") and os.path.exists(os.path.join(root, R(s["prompt"]))) else rel(os.path.join(d, "prompt.md"), root)
        mf = [{"file": R(p), "role": "image %d sent" % (i + 1)} for i, p in enumerate(s.get("references", []))]
        return write(file, kind or "image", mb, pr, mf, root=root, **keep)
    if os.path.exists(j):
        r = json.load(open(j))
        if "endpoint" in r and "input" in r:
            inp = r["input"]
            mb = {"service": "fal", "endpoint": r["endpoint"], "settings": {k: v for k, v in inp.items() if k not in ("prompt", "audio_urls")},
                  "seconds": r.get("response", {}).get("audio", {}).get("duration")}
            mf = [{"file": R(u), "role": "@Audio%d" % (i + 1)} for i, u in enumerate(inp.get("audio_urls", []))]
            return write(file, kind or "sound", mb, prompt_file(inp["prompt"], root), mf, root=root, **keep)
        q = r.get("request", {})
        mb = {"service": "OpenAI", **q, "usage": r.get("usage"), "cost": "not returned"} if q else r.get("made_by")
        if r.get("made_from"):
            mf = [{"file": R(m.get("file") or m.get("path")), "role": m.get("role", "")} for m in r["made_from"]]
        else:
            sent = r.get("images_sent") or ([r["image_sent"]] if r.get("image_sent") else [])
            mf = [{"file": R(p), "role": "image %d" % (i + 1)} for i, p in enumerate(sent)]
        for k in ("camera", "place", "floor_plan", "contents", "notes"):
            if k in r and k not in keep: keep[k] = r[k]
        pr = prompt_file(r["prompt"], root) if isinstance(r.get("prompt"), str) else None
        if r.get("prompt") and not pr: keep["notes"] = (keep.get("notes", "") + " Its prompt is in " + rel(j, root) + ".").strip()
        return write(file, KINDS.get(r.get("kind"), r.get("kind")) or kind or "image", mb, pr, mf, root=root, **keep)
    src = same_bytes(file, root) if copies else None
    if src:
        s = read(src) or {}
        for k in ("camera", "place", "floor_plan", "contents"):
            if k in s and k not in keep: keep[k] = s[k]
        return write(file, "copy", made_from=[{"file": src, "role": "copied from"}], root=root,
                     notes="Its source was found by its bytes; it was copied without a record.", **keep)
    return None


def main(a):
    if not a or a[0] in ("-h", "--help"): print(__doc__); return
    cmd, rest = a[0], a[1:]
    def opt(name, n=1):
        if name in rest:
            i = rest.index(name); v = rest[i + 1:i + 1 + n]; del rest[i:i + 1 + n]; return v if n > 1 else v[0]
    if cmd == "write":
        made_from = []
        while "--from" in rest:
            f, role = opt("--from", 2); made_from.append({"file": f, "role": role})
        kind = opt("--kind"); mb = opt("--made-by"); pr = opt("--prompt"); cam = opt("--camera"); pl = opt("--place")
        fp = opt("--floor-plan"); ct = opt("--contents"); nt = opt("--notes")
        write(rest[0], kind, json.loads(mb) if mb else None, pr, made_from, cam, pl, fp, json.loads(ct) if ct else None, notes=nt)
    elif cmd == "adopt":
        moved = []
        while "--moved" in rest: moved.append(tuple(opt("--moved", 2)))
        k = opt("--kind"); cp = "--copies" in rest
        if cp: rest.remove("--copies")
        for f in rest: print(("adopted " if adopt(f, moved, k, cp) else "no older record: ") + f)
    elif cmd == "copy": copy(rest[0], rest[1])
    elif cmd == "move": move(rest[0], rest[1])
    elif cmd == "trace": out = opt("--out"); trace(rest[0], out)
    elif cmd == "children": children(rest[0])
    elif cmd == "find":
        k = opt("--kind"); c = opt("--camera"); n = opt("--contains"); find(root_of("."), k, c, n)
    elif cmd == "check":
        sys.exit(1 if check(rest, root_of(rest[0] if rest else ".")) else 0)
    else: print(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
