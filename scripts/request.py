#!/usr/bin/env python3
"""Run one request as one cycle: send it exactly as its skill built it, file what comes back, and write its report.
See docs/projects.md.

Usage:
  request.py plan <spec.json> [--json]  what run would send, offline: the endpoint and its settings, the prompt, every
                                      reference in order with its role and path, the canon read, and the estimate,
                                      unknown and never zero; with the plan's hash, which run --expect checks
  request.py run <spec.json> [--stand-in] [--key-file F] [--expect <hash>]
                                      send the request to its model endpoint, file what comes back into library/,
                                      the prompt as sent into prompts/<id>.txt, and write requests/<id>.html;
                                      a research request files into sources/
  request.py collect <id>             finish a fal request that was accepted and paid for but not yet collected, such
                                      as one still running after an hour or one whose connection failed: its pending
                                      record, requests/<id>.pending.json, holds the addresses fal returned for it
  request.py cancel <id>              ask fal to cancel a pending request, at the address fal returned for it
  request.py close <id> --lost "<why>" close a pending request whose result is lost: its report says so and records the
                                      cost as likely spent; check stops listing it. A synchronous request keeps its raw
                                      reply beside its pending record before anything else, so collect can still file it
                                      after a full disk or a crash
  request.py attach <id> <file> --as comparison|chart [--caption TEXT]
                                      embed an image the agent made to show the results in the request's report
  request.py resource <file>... --name NAME [--from <file>]...
                                      file shared material no model made, such as a canonical document, a pre-vis
                                      render, or a builder, into prompts/resources/ as <time>-<name>.<ext>, with a
                                      line in prompts/resources/records.jsonl naming each input it was made from
  request.py build "<command>" <output>... --name NAME [--from <file> | --from git:<commit>:<path>]...
                                      run a builder, and file each file it makes into prompts/resources/, recorded
                                      with its command and inputs
  request.py record <file>            the record written inside an image or a video when it was filed
  request.py note <id> [--asked TEXT] [--why TEXT] [--notes TEXT]
                                      set the agent's own words in the report
  request.py show <id | file>         the full record of the request, resource, or build that made a file, as JSON
  request.py tell <id>                what the agent says when the request is done, word for word
  request.py list [--skill S] [--pipeline P]
  request.py check                    every pending request is listed, every report's files exist, every library file has its report, nothing in
                                      library/, sources/, prompts/, or agent/ was changed or removed since it was committed
  request.py id <name>                the ID a request named <name> would get now
  request.py version                  the formats this checkout writes, and its Spumcake-Skills commit

The commands that spend are request.py run and pipeline.py rerun, each without --stand-in. collect and cancel never
start a new paid request. A command that writes refuses a project holding records from a Spumcake-Skills commit this
checkout does not have; a command that reads warns.

A spec is JSON:
  {"name": "keyframe-the-line", "skill": "generate-keyframe", "asked": "...", "why": "...",
   "pipeline": "001", "chain": "the line", "step": "keyframe", "depends_on": ["<request id>"],
   "endpoint": {"kind": "openai-image-edit" | "openai-image" | "openrouter-image" | "openai-text" | "openrouter-text"
                        | "fal" | "research",
                "model": "...", "settings": {...}},
   "prompt": "the text exactly as sent",
   "references": [{"file": "library/<file>", "role": "image 1, the layout of the shot"}],
   "canon": [{"name": "the front door: side in the far-end frame", "value": "left", "read_at": "<time>",
              "from": "pipeline/001/canon.sql"}],
   "outputs": ["<file to file>", ...]          for research: the files found
   "sources": [{"file": "...", "address": "...", "page": "...", "use": "..."}]   for research}
A request is one call to a model endpoint. What the agent or a builder makes is not a request: it goes into
prompts/resources/ when it is canon or is sent to a model, and into agent/ otherwise: nothing made for a project
is thrown away or left in a scratch folder. A setup's workspace files go in work/, which no skill reads or writes.
Every image or video a request files carries its record inside it (request.py record), and the report keeps the
sha256 of the file as the endpoint returned it and as filed. Names use local time.
The agent writes the spec; everything else in the report comes from what this script sent and received.
"""
import sys, os, re, json, base64, hashlib, html, shutil, subprocess, urllib.request, mimetypes, wave, datetime, struct, zlib, tempfile

MEDIA_IMAGE = (".png", ".jpg", ".jpeg", ".webp", ".gif")
MEDIA_AUDIO = (".wav", ".mp3", ".flac", ".aif", ".aiff")
MEDIA_VIDEO = (".mp4", ".mov", ".webm")
# Where keys and prices come from: the setup, a setup-v1 JSON file named by --setup or SKILLS_SETUP, or found at
# ~/.config/spumcake-skills/setup.json; docs/setup.md describes the keys request.py reads. The folder below is the
# last fallback for one computer, kept until that computer's setup names its keys; it prints a warning when used.
LEGACY_CRED = "/mnt/Hot/.{}/credentials"
_setup = {}


def setup():
    """The setup file's values, read once: --setup, then SKILLS_SETUP, then ~/.config/spumcake-skills/setup.json."""
    if "values" in _setup: return _setup["values"]
    p = _setup.get("path") or os.environ.get("SKILLS_SETUP") or os.path.expanduser("~/.config/spumcake-skills/setup.json")
    vals = {}
    if p and os.path.exists(p):
        vals = json.load(open(p))
        if vals.get("format") not in ("setup-v1", None): sys.exit("the setup file %s is %s, not setup-v1" % (p, vals.get("format")))
        base = os.path.dirname(os.path.abspath(p))   # a relative path in it is relative to the file
        for k, v in list(vals.items()):
            if isinstance(v, str) and (k == "env_file" or k.endswith("_key") or k == "credentials_dir") and not os.path.isabs(v):
                vals[k] = os.path.join(base, v)
        vals["_path"] = p
    _setup["values"] = vals
    return vals


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


LFS = b"version https://git-lfs.github.com/spec/v1"


def sha(path):
    """A file's sha256; for a Git LFS pointer, the sha256 of the file it stands for, which is its oid, so a clone
    without LFS content checks and plans the same."""
    if os.path.getsize(path) < 1024:
        head = open(path, "rb").read()
        if head.startswith(LFS):
            m = re.search(rb"oid sha256:([0-9a-f]{64})", head)
            if m: return m.group(1).decode()
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()


SKILLS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RECORD_FORMAT = 1
XMP = ('<?xpacket begin="" id="W5M0MpCehiHzreSzNTczkc9d"?><x:xmpmeta xmlns:x="adobe:ns:meta/"><rdf:RDF '
       'xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"><rdf:Description rdf:about="" '
       'xmlns:Iptc4xmpExt="http://iptc.org/std/Iptc4xmpExt/2008-02-29/"><Iptc4xmpExt:DigitalSourceType>'
       'http://cv.iptc.org/newscodes/digitalsourcetype/trainedAlgorithmicMedia</Iptc4xmpExt:DigitalSourceType>'
       '</rdf:Description></rdf:RDF></x:xmpmeta><?xpacket end="r"?>')


SPEC_FORMAT = 1      # the spec a skill or a setup writes for run and plan
REPORT_FORMAT = 2    # the report's embedded JSON, "record"
TELL_FORMAT = 1      # tell's text


def plan_of(spec, root):
    """Exactly what run would send for a spec, worked out offline, with its hash. The hash leaves out what changes
    without changing what is sent: the request's ID and name, what was asked and why, when canon was read, and
    absolute paths."""
    ep = spec.get("endpoint") or {}
    refs = []
    for i, r in enumerate(spec.get("references", [])):
        f = r.get("file")
        p = os.path.join(root, f) if f else None
        refs.append({"order": i + 1, "role": r.get("role"), "field": r.get("field"), "canon": r.get("canon"), "file": f,
                     "path": os.path.abspath(p) if p else None, "sha256": sha(p) if p and os.path.exists(p) else None})
    plan = {"plan": SPEC_FORMAT, "skill": spec.get("skill"), "pipeline": spec.get("pipeline"), "chain": spec.get("chain"),
            "step": spec.get("step"), "endpoint": {"kind": ep.get("kind"), "model": ep.get("model"), "settings": ep.get("settings") or {}},
            "prompt": spec.get("prompt"), "references": refs,
            "canon": [{"name": c.get("name"), "value": c.get("value")} for c in spec.get("canon", [])],
            "scripts": [s.get("command") for s in spec.get("scripts", [])], "requests": 1,
            "estimate": estimate(spec)}
    if ep.get("kind") == "research":   # what research files is what is approved: each file, by its sha256, and its source
        files = []
        for f in spec.get("outputs", []):
            pth = f if os.path.isabs(f) else os.path.join(root, f)
            files.append({"file": os.path.basename(f), "sha256": sha(pth) if os.path.exists(pth) else None})
        plan["outputs"] = files
        plan["sources"] = spec.get("sources", [])
    plan["hash"] = plan_hash(plan)
    return plan


def plan_hash(plan):
    keep = {k: v for k, v in plan.items() if k not in ("hash", "estimate")}
    keep["references"] = [{k: v for k, v in r.items() if k != "path"} for r in keep.get("references", [])]
    return hashlib.sha256(json.dumps(keep, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def money(x):
    """A price with enough places that a small one never reads as zero: $0.64, $0.0012, $0.000034."""
    x = float(x)
    if x == 0: return "$0"
    if x >= 0.01: return "$%.2f" % x
    places = 2
    while round(x, places) == 0 or abs(round(x, places) - x) / x > 0.05: places += 1
    return "$%.*f" % (places, x)


def estimate(spec):
    """An estimate from the price the setup gives for the service and model, or the endpoint's own, or unknown:
    never zero."""
    ep = dict(spec.get("endpoint") or {})
    s = ep.get("settings") or {}
    if ep.get("kind") == "research": return "nothing: research is filed, not sent"
    service = (ep.get("kind") or "").split("-")[0]   # fal, openai, openrouter
    price = ((setup().get("prices") or {}).get(service) or {}).get(ep.get("model") or "")
    if isinstance(price, dict):
        if price.get("per_minute"): ep.setdefault("price_per_minute", price["per_minute"])
        if price.get("per_request"): ep.setdefault("price_per_request", price["per_request"])
    if ep.get("price_per_minute") and s.get("duration"):
        return "about %s, %s s at $%s a minute" % (money(float(s["duration"]) / 60 * float(ep["price_per_minute"])), s["duration"], ep["price_per_minute"])
    if ep.get("price_per_request"):
        return "about %s a request" % money(ep["price_per_request"])
    return "unknown: no price for this endpoint"


def plan_cmd(spec_file, as_json=False):
    spec = json.load(open(spec_file))
    root = project_root(os.path.dirname(os.path.abspath(spec_file)) if spec.get("project") is None else spec["project"])
    guard(root, write=False)
    if spec.get("spec", 1) > SPEC_FORMAT: sys.exit("this spec is format %s, newer than this checkout's %d" % (spec["spec"], SPEC_FORMAT))
    p = plan_of(spec, root)
    if as_json: print(json.dumps(p, indent=1, ensure_ascii=False)); return
    ep = p["endpoint"]
    print("Sends to: %s, %s, %s" % (ep["kind"], ep["model"] or "its default model", json.dumps(ep["settings"])))
    print("References, in the order sent:" if p["references"] else "References: none")
    for r in p["references"]: print("  %d. %s, %s%s" % (r["order"], r["path"], r["role"] or "", (" (%s)" % r["field"]) if r["field"] else ""))
    if p["canon"]:
        print("Canon read:"); [print("  %s = %s" % (c["name"], c["value"])) for c in p["canon"]]
    if p["scripts"]: print("Runs: " + "; ".join(p["scripts"]))
    print("Estimate: " + p["estimate"])
    print("Prompt:\n" + (p["prompt"] or "(none)"))
    print("Plan hash: " + p["hash"])


_newer = {}


def newer_records(root):
    """The Spumcake-Skills commits this project's records name that this checkout does not have."""
    if root in _newer: return _newer[root]
    seen = set()
    pat = re.compile(r'"skills_commit":\s*"([0-9a-f]{7,40})')
    for d in ("requests", "sources"):
        dd = os.path.join(root, d)
        for f in os.listdir(dd) if os.path.isdir(dd) else []:
            if f.endswith((".html", ".json")): seen.update(pat.findall(open(os.path.join(dd, f), errors="ignore").read()))
    logs = [os.path.join(root, "prompts", "resources", "records.jsonl")]
    pdir = os.path.join(root, "pipeline")
    logs += [os.path.join(pdir, n, "runs.jsonl") for n in (os.listdir(pdir) if os.path.isdir(pdir) else [])]
    for l in logs:
        if os.path.exists(l): seen.update(pat.findall(open(l, errors="ignore").read()))
    head = keyless(["git", "-C", SKILLS_DIR, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    missing = set()
    for c in seen:
        if head.startswith(c): continue
        r = keyless(["git", "-C", SKILLS_DIR, "merge-base", "--is-ancestor", c, "HEAD"], capture_output=True)
        if r.returncode: missing.add(c)
    _newer[root] = sorted(missing)
    return _newer[root]


def guard(root, write=True):
    """Refuse to write, or warn when reading, in a project holding records from a Skills commit this checkout lacks."""
    m = newer_records(root)
    if not m: return
    msg = ("this project holds records from Spumcake-Skills %s, which this checkout does not have (newer, or unknown: "
           "fetch Spumcake-Skills)" % ", ".join(m))
    if write: sys.exit("refused: " + msg)
    print("warning: " + msg, file=sys.stderr)


def skills_commit():
    """The Spumcake-Skills commit these scripts run from, "+dirty" when it has uncommitted changes, or "unknown"."""
    try:
        h = keyless(["git", "-C", SKILLS_DIR, "rev-parse", "--short=12", "HEAD"], capture_output=True, text=True, timeout=10)
        if h.returncode: return "unknown"
        d = keyless(["git", "-C", SKILLS_DIR, "status", "--porcelain", "--", "scripts", "skills", "docs"],
                           capture_output=True, text=True, timeout=10).stdout.strip()
        return h.stdout.strip() + ("+dirty" if d else "")
    except Exception:
        return "unknown"


def _png_chunks(b):
    i, out = 8, []
    while i + 8 <= len(b):
        n = struct.unpack(">I", b[i:i + 4])[0]
        out.append((b[i + 4:i + 8], b[i + 8:i + 8 + n])); i += 12 + n
    return out


def _png_chunk(typ, body):
    return struct.pack(">I", len(body)) + typ + body + struct.pack(">I", zlib.crc32(typ + body) & 0xffffffff)


def _itxt(keyword, text):
    return keyword + b"\0\0\0\0\0" + text.encode("utf-8")


def embed_record(path, record):
    """Write a request's record inside the image or video it made, so the file says where it came from wherever it
    goes: a PNG gets it as an iTXt chunk, spumcake:record, with the IPTC "made by a trained model" disclosure in its
    XMP; an MP4 or MOV gets it as its comment, its streams copied, not encoded again. Other formats keep their record
    in the report only. Returns whether it was written."""
    ext = os.path.splitext(path)[1].lower()
    data = json.dumps(record, separators=(",", ":"), ensure_ascii=False)
    if ext == ".png":
        b = open(path, "rb").read()
        if b[:8] != b"\x89PNG\r\n\x1a\n": return False
        out = [b[:8]]
        for typ, body in _png_chunks(b):
            if typ == b"iTXt" and body.split(b"\0", 1)[0] in (b"spumcake:record", b"XML:com.adobe.xmp"): continue
            if typ == b"IEND":
                out.append(_png_chunk(b"iTXt", _itxt(b"spumcake:record", data)))
                out.append(_png_chunk(b"iTXt", _itxt(b"XML:com.adobe.xmp", XMP)))
            out.append(_png_chunk(typ, body))
        open(path, "wb").write(b"".join(out))
        return True
    if ext in (".mp4", ".mov", ".m4v"):
        tmp = path + ".record" + ext
        r = keyless(["ffmpeg", "-v", "error", "-y", "-i", path, "-map", "0", "-c", "copy", "-map_metadata", "0",
                            "-metadata", "comment=" + data, tmp], capture_output=True)
        if r.returncode or not os.path.exists(tmp): return False
        os.replace(tmp, path)
        return True
    return False


def read_record(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".png":
        for typ, body in _png_chunks(open(path, "rb").read()):
            if typ == b"iTXt" and body.startswith(b"spumcake:record\0"):
                return json.loads(body.split(b"\0", 5)[5].decode("utf-8"))
        return None
    if ext in (".mp4", ".mov", ".m4v"):
        r = keyless(["ffprobe", "-v", "error", "-show_entries", "format_tags=comment", "-of", "json", path],
                           capture_output=True, text=True)
        c = (json.loads(r.stdout or "{}").get("format", {}).get("tags", {}) or {}).get("comment")
        try: return json.loads(c) if c else None
        except ValueError: return None
    return None


def strip_record(src, dst, rid):
    """Copy a file for delivery or sharing with only the disclosure and the request's ID inside it, never its prompt
    or inputs, since a file's metadata travels wherever the file is shared."""
    small = {"spumcake_record": RECORD_FORMAT, "request": rid, "made_by": "a trained model"}
    shutil.copyfile(src, dst)
    if read_record(dst) is not None or os.path.splitext(dst)[1].lower() in (".png", ".mp4", ".mov", ".m4v"):
        embed_record(dst, small)


def record_line(root, f, inputs=(), command=None, name=None):
    """Append one line to prompts/resources/records.jsonl for a file filed without a model: what it is, its sha256,
    each input it was made from with its sha256, and the command that made it."""
    def rel(x):
        a = os.path.abspath(x if os.path.isabs(x) else os.path.join(root, x))
        return os.path.relpath(a, root) if a.startswith(os.path.abspath(root) + os.sep) else "outside the project: " + os.path.basename(a)
    entries = [git_source(root, i) if i.startswith("git:") else
               {"file": rel(i), "sha256": sha(i if os.path.isabs(i) else os.path.join(root, i))} for i in inputs]
    line = {"at": now().strftime("%Y-%m-%dT%H:%M:%SZ"), "file": rel(f), "sha256": sha(os.path.join(root, f)), "name": name,
            "inputs": [e for e in entries if not e["file"].startswith("work/")],
            "command": command, "skills_commit": skills_commit()}
    workspace = [e for e in entries if e["file"].startswith("work/")]
    if workspace: line["workspace"] = workspace   # where it was exported from: provenance only, never an input
    with open(os.path.join(root, "prompts", "resources", "records.jsonl"), "a") as fh:
        fh.write(json.dumps(line, ensure_ascii=False) + "\n")


def git_source(root, name):
    """A source that exists only in the project's git history, named git:<commit>:<path>, with the path from the
    repository's root: its commit, path, and sha256, read with git show, never checked out."""
    try:
        _, commit, path = name.split(":", 2)
    except ValueError:
        sys.exit("name a source in git history as git:<commit>:<path>: " + name)
    full = keyless(["git", "rev-parse", "--verify", commit + "^{commit}"], cwd=root, capture_output=True, text=True)
    if full.returncode: sys.exit("no such commit in this project's git history: " + commit)
    blob = keyless(["git", "show", "%s:%s" % (full.stdout.strip(), path)], cwd=root, capture_output=True)
    if blob.returncode: sys.exit("no %s at %s" % (path, commit))
    return {"file": name, "commit": full.stdout.strip(), "path": path, "sha256": hashlib.sha256(blob.stdout).hexdigest()}


def resource_records(root):
    p = os.path.join(root, "prompts", "resources", "records.jsonl")
    return [json.loads(l) for l in open(p) if l.strip()] if os.path.exists(p) else []


def run_log(root, pipeline, event):
    """Append an event to the pipeline's run log, pipeline/<n>/runs.jsonl, when the pipeline exists."""
    d = os.path.join(root, "pipeline", "%03d" % int(pipeline))
    if not os.path.isdir(d): return
    event = dict({"at": now().strftime("%Y-%m-%dT%H:%M:%SZ")}, **event, skills_commit=skills_commit())
    with open(os.path.join(d, "runs.jsonl"), "a") as fh:
        fh.write(json.dumps(event, ensure_ascii=False) + "\n")


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
    """A service's key: the environment variable first; then --key-file; then the setup's env_file, its
    <service>_key file, or its credentials_dir/.<service>/credentials; then, with a warning, the legacy folder."""
    if os.environ.get(env): return os.environ[env]
    s = setup()
    tried = []
    for f, how in ((key_file, "--key-file"), (s.get("env_file"), "the setup's env_file"),
                   (s.get(service.replace("-", "_") + "_key") or s.get(service.split("-")[0] + "_key"), "the setup's %s_key" % service),
                   (os.path.join(s["credentials_dir"], "." + service, "credentials") if s.get("credentials_dir") else None, "credentials_dir")):
        if not f or not os.path.exists(f): continue
        text = open(f).read()
        m = re.search(r"^\s*%s\s*=\s*['\"]?([^'\"\s]+)" % env, text, re.M) if how == "the setup's env_file" else re.search(pattern, text)
        if m: return m.group(1) if how == "the setup's env_file" else m.group(0)
        tried.append(how)
    legacy = LEGACY_CRED.format(service)
    if os.path.exists(legacy):
        m = re.search(pattern, open(legacy).read())
        if m:
            print("warning: the %s key came from %s, which is not in the setup; name it in the setup file (docs/setup.md)"
                  % (service, os.path.dirname(legacy)), file=sys.stderr)
            return m.group(0)
    sys.exit("no %s key: set %s, or name it in the setup file (docs/setup.md)%s" % (service, env, ("; tried " + ", ".join(tried)) if tried else ""))


# ---- filing ------------------------------------------------------------------------------------

def file_into(root, folder, rid, sources, suffixes=None):
    """Copy each source into folder as <rid>.<ext>, or <rid>-<n>.<ext> when there are several. Never overwrite."""
    out = []
    os.makedirs(os.path.join(root, folder), exist_ok=True)   # a new project may not have the folder yet
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
        cmd = ["curl", "-s", url, "-H", "@-", "-F", "model=" + model]
        for r in spec["references"]: cmd += ["-F", "image[]=@" + os.path.join(root, r["file"])]
        cmd += ["--form-string", "prompt=" + spec["prompt"]]
        for name, value in settings.items(): cmd += ["-F", "%s=%s" % (name, value)]
    else:
        body = dict(model=model, prompt=spec["prompt"], **settings)
        cmd = ["curl", "-s", url, "-H", "@-", "-H", "Content-Type: application/json",
               "-d", json.dumps(body)]
    sent = {"service": "OpenAI", "url": url, "model": model, "settings": settings,
            "references_sent_as": "image[] in the order listed" if edit else "none"}
    # the key goes in on stdin, as a header, never on the command line, where any user's ps shows it
    raw = keyless(cmd, input=("Authorization: Bearer %s\n" % k).encode(), capture_output=True, timeout=900).stdout
    keep(raw, sent)   # the paid reply is on disk before anything else is done with it
    paths, result = decode("openai-image", raw, tmp, ep)
    return paths, sent, result


def decode(kind, raw, tmp, ep):
    """Turn a synchronous endpoint's raw reply into files and a result: the same whether it has just arrived or is
    read back from a kept reply by collect."""
    r = json.loads(raw)
    if kind in ("openai-image", "openai-image-edit"):
        if "error" in r: sys.exit("the endpoint refused: " + json.dumps(r["error"])[:600])
        paths = []
        for i, d in enumerate(r["data"]):
            p = os.path.join(tmp, "out-%d.png" % i)
            open(p, "wb").write(base64.b64decode(d["b64_json"]))
            paths.append(p)
        return paths, {"usage": r.get("usage"), "cost": token_cost("openai", ep.get("model", "gpt-image-2.6-sunburst"), r.get("usage"))}
    if kind == "openrouter-image":
        items = r.get("data") or []
        if len(items) != 1 or not items[0].get("b64_json"):
            sys.exit("OpenRouter returned no image: " + json.dumps({k2: v for k2, v in r.items() if k2 != "data"})[:400])
        data = base64.b64decode(items[0]["b64_json"])
        ext = ".png" if data.startswith(b"\x89PNG") else ".jpg" if data.startswith(b"\xff\xd8\xff") else ".webp" if data[8:12] == b"WEBP" else ".bin"
        path = os.path.join(tmp, "out" + ext); open(path, "wb").write(data)
        return [path], {"usage": r.get("usage"), "cost": _billed(r.get("usage"))}
    answer = ((r.get("choices") or [{}])[0].get("message") or {}).get("content")
    if not answer: sys.exit("the model returned no answer: " + json.dumps({k2: v for k2, v in r.items() if k2 != "choices"})[:400])
    path = os.path.join(tmp, "answer" + (ep.get("ext") or ".md")); open(path, "w").write(answer)
    return [path], {"usage": r.get("usage"),
                    "cost": _billed(r.get("usage")) if kind == "openrouter-text" else "unknown: not returned by the endpoint"}


_keep = {}


def keep(raw, sent):
    """Write a synchronous endpoint's raw reply beside its pending record before anything else, so a full disk or a
    crash loses a file write, never a paid result; when the project's disk refuses it, into the system's temporary
    folder instead, and the pending record says where. collect files it later without paying again."""
    root, rid = _keep["root"], _keep["rid"]
    places = [os.path.join(root, "requests", rid + ".reply"), os.path.join(tempfile.gettempdir(), "spumcake-" + rid + ".reply")]
    for p in places:
        try:
            with open(p, "wb") as fh: fh.write(raw); fh.flush(); os.fsync(fh.fileno())
            _keep["file"] = p
            break
        except OSError as e:
            print("could not keep the reply at %s: %s" % (p, e), file=sys.stderr)
    try:
        pp = pending_path(root, rid)
        pend = json.load(open(pp)); pend.update(sent=sent, reply_file=_keep.get("file")); json.dump(pend, open(pp, "w"), indent=1)
    except OSError as e:
        print("could not note the reply in the pending record: %s; it is at %s" % (e, _keep.get("file")), file=sys.stderr)


def token_cost(service, model, usage):
    """A cost worked out from the token usage an endpoint returned and the setup's per-token prices for its model,
    marked as computed, never a bill; unknown when either is missing, never zero."""
    if not usage: return "unknown: not returned by the endpoint"
    per = (((setup().get("prices") or {}).get(service) or {}).get(model) or {}).get("per_million_tokens")
    total = usage.get("total_tokens") or ((usage.get("input_tokens") or 0) + (usage.get("output_tokens") or 0))
    if not per: return "unknown: %s tokens used; no token prices for %s in the setup" % (total, model)
    d = usage.get("input_tokens_details") or {}
    text_in = d.get("text_tokens", usage.get("input_tokens", 0) if "image_tokens" not in d else 0)
    image_in = d.get("image_tokens", 0)
    out = usage.get("output_tokens", 0)
    cost = (text_in * per.get("input_text", 0) + image_in * per.get("input_image", 0) + out * per.get("output_image", per.get("output", 0))) / 1e6
    missing = [k for k, n in (("input_text", text_in), ("input_image", image_in), ("output_image", out)) if n and k not in per and not (k == "output_image" and "output" in per)]
    if missing: return "unknown: no %s price for %s in the setup" % (", ".join(missing), model)
    return "about %s, computed from the token usage and the setup's prices, not a bill" % money(cost)


def _billed(usage):
    c = (usage or {}).get("cost")
    return ("%s, as billed by OpenRouter" % money(c)) if c not in (None, "") else "unknown: not returned by the endpoint"


OPENROUTER = "https://openrouter.ai/api/v1/"


def openrouter_image(spec, root, tmp, key_file):
    """OpenRouter's image endpoint, one image a request, its references sent as data URIs in input_references, in the
    order listed. A paid request is never retried."""
    ep = spec["endpoint"]
    settings = {"quality": "high"}
    settings.update(ep.get("settings", {}))
    body = dict(settings, model=ep["model"], prompt=spec["prompt"], n=1)
    refs = []
    for r in spec.get("references", []):
        f = os.path.join(root, r["file"])
        mime = mimetypes.guess_type(f)[0]
        if mime not in ("image/png", "image/jpeg", "image/webp"): sys.exit("a reference must be PNG, JPEG, or WebP: " + r["file"])
        refs.append({"type": "image_url", "image_url": {"url": "data:%s;base64,%s" % (mime, base64.b64encode(open(f, "rb").read()).decode())}})
    if refs: body["input_references"] = refs
    k = key("openrouter", "OPENROUTER_API_KEY", r"sk-or-[A-Za-z0-9_\-]+", key_file)
    req = urllib.request.Request(OPENROUTER + "images", json.dumps(body).encode(),
                                 {"Authorization": "Bearer " + k, "Content-Type": "application/json"})
    sent = {"service": "OpenRouter", "url": OPENROUTER + "images", "model": ep["model"], "settings": settings,
            "references_sent_as": "data URIs in input_references, in the order listed"}
    raw = urllib.request.urlopen(req, timeout=ep.get("timeout", 600)).read()
    keep(raw, sent)   # the paid reply is on disk before anything else is done with it
    paths, result = decode("openrouter-image", raw, tmp, ep)
    sent["response_id"] = json.loads(raw).get("id")
    return paths, sent, result


def language_model(spec, root, tmp, key_file, service):
    """A language model's answer, through OpenAI or OpenRouter: one chat completion, its answer filed as text. A
    reference is sent as text when it is a text file, or as an image when it is a picture."""
    ep = spec["endpoint"]
    content = [{"type": "text", "text": spec["prompt"]}]
    for r in spec.get("references", []):
        f = os.path.join(root, r["file"]); mime = mimetypes.guess_type(f)[0] or ""
        if mime.startswith("image/"):
            content.append({"type": "image_url", "image_url": {"url": "data:%s;base64,%s" % (mime, base64.b64encode(open(f, "rb").read()).decode())}})
        else:
            content.append({"type": "text", "text": "%s:\n%s" % (r.get("role") or r["file"], open(f, errors="replace").read())})
    messages = ([{"role": "system", "content": ep["system"]}] if ep.get("system") else []) + [{"role": "user", "content": content}]
    body = dict(ep.get("settings", {}), model=ep["model"], messages=messages)
    if service == "openrouter":
        url, k = OPENROUTER + "chat/completions", key("openrouter", "OPENROUTER_API_KEY", r"sk-or-[A-Za-z0-9_\-]+", key_file)
    else:
        url, k = "https://api.openai.com/v1/chat/completions", key("openai", "OPENAI_API_KEY", r"sk-[A-Za-z0-9_\-]+", key_file)
    req = urllib.request.Request(url, json.dumps(body).encode(), {"Authorization": "Bearer " + k, "Content-Type": "application/json"})
    sent = {"service": "OpenRouter" if service == "openrouter" else "OpenAI", "url": url, "model": ep["model"],
            "settings": ep.get("settings", {}),
            "references_sent_as": "in the user message after the prompt, in the order listed: text files as text, pictures as images"}
    raw = urllib.request.urlopen(req, timeout=ep.get("timeout", 600)).read()
    keep(raw, sent)   # the paid reply is on disk before anything else is done with it
    paths, result = decode(service + "-text", raw, tmp, ep)
    sent["response_id"] = json.loads(raw).get("id")
    return paths, sent, result


def fal_upload(path, fal_key):
    """Upload one input file to fal's storage through fal's official Python client, as the user set on 2026-11-08,
    and return its address."""
    try:
        import fal_client
    except ImportError:
        sys.exit("fal's official Python client is not installed: install it with  pip install fal-client  and run again")
    return fal_client.SyncClient(key=fal_key).upload_file(path)


def fal(spec, root, tmp, key_file):
    ep = spec["endpoint"]
    body = {"prompt": spec["prompt"]} if spec.get("prompt") else {}  # an endpoint with no prompt, such as frame interpolation
    body.update(ep.get("settings", {}))
    fal_key = key("fal-ai", "FAL_KEY", r"[A-Za-z0-9_\-]+:[A-Za-z0-9_\-]+", key_file)
    uploaded = {}
    for r in spec.get("references", []):
        field = r.get("field") or ep.get("reference_field")
        if not field:  # never guess where a file goes: an audio file sent as an image is silently ignored
            sys.exit("no field for %s: say which of the endpoint's fields it goes in" % r["file"])
        f = os.path.join(root, r["file"])
        url = uploaded.get(f) or fal_upload(f, fal_key)  # fal refuses large files sent inline; its storage takes them
        uploaded[f] = url
        if field.endswith("_urls"): body.setdefault(field, []).append(url)
        else: body[field] = url  # a single-file field, such as image_url or end_image_url
    # fal's queue: submit, then collect. Once fal accepts a request it is paid for, so from that moment the request
    # is never lost: its pending record keeps the addresses fal returned, and `request.py collect` finishes it later
    # when waiting runs out or the connection fails. The status, result, and cancel addresses are always the ones fal
    # returned on submit, never built from the model's name.
    q = fal_call(fal_key, "https://queue.fal.run/" + ep["model"], body, retries=0)
    print("fal request " + q["request_id"], file=sys.stderr, flush=True)
    sent = {"service": "fal", "url": "https://queue.fal.run/" + ep["model"], "model": ep["model"], "request_id": q["request_id"],
            "status_url": q.get("status_url"), "response_url": q.get("response_url"), "cancel_url": q.get("cancel_url"),
            "settings": {k: v for k, v in body.items() if k != "prompt" and not str(v).startswith(("['data:", "data:"))},
            "references_sent_as": "files uploaded to fal's storage with fal's official client, each address in its reference's field, in the order listed"}
    return sent


def fal_call(fal_key, url, data=None, method=None, retries=6):
    """One call to fal's queue, tried again after a network failure, up to retries times with a growing wait."""
    import time, urllib.error
    head = {"Authorization": "Key " + fal_key, "Content-Type": "application/json"}
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, json.dumps(data).encode() if data is not None else None, head,
                                         method=method or ("POST" if data is not None else "GET"))
            return json.load(urllib.request.urlopen(req, timeout=300))
        except urllib.error.HTTPError as e:
            if e.code < 500 or attempt == retries: raise
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError):
            if attempt == retries: raise
        time.sleep(min(5 * 2 ** attempt, 120))


def fal_collect(sent, ep, tmp, key_file, wait_minutes=60):
    """Wait for a submitted fal request, fetch its result, and download its outputs. Returns None, leaving the request
    pending, when the wait runs out or the network keeps failing; raises when fal says the request failed."""
    import time, urllib.error
    fal_key = key("fal-ai", "FAL_KEY", r"[A-Za-z0-9_\-]+:[A-Za-z0-9_\-]+", key_file)
    deadline = time.time() + wait_minutes * 60
    try:
        while True:
            s = fal_call(fal_key, sent["status_url"])
            if s.get("status") == "COMPLETED": break
            if s.get("status") not in ("IN_QUEUE", "IN_PROGRESS"): raise RuntimeError("fal: " + json.dumps(s)[:600])
            if time.time() > deadline: return None
            time.sleep(5)
        r = fal_call(fal_key, sent["response_url"])
        urls = []
        for field in ("audio", "image", "video"):
            v = r.get(field)
            if isinstance(v, dict) and v.get("url"): urls.append(v["url"])
        for field in ("images", "audios", "videos"):
            urls += [v["url"] for v in r.get(field) or [] if isinstance(v, dict) and v.get("url")]
        paths = []
        for i, u in enumerate(urls):
            ext = os.path.splitext(u.split("?")[0])[1] or ".bin"
            pth = os.path.join(tmp, "out-%d%s" % (i, ext))
            for attempt in range(7):
                try:
                    urllib.request.urlretrieve(u, pth); break
                except (urllib.error.URLError, TimeoutError, ConnectionError, OSError):
                    if attempt == 6: raise
                    time.sleep(min(5 * 2 ** attempt, 120))
            paths.append(pth)
    except (urllib.error.URLError, TimeoutError, ConnectionError, OSError) as e:
        if isinstance(e, urllib.error.HTTPError) and e.code < 500: raise
        print("fal: the connection kept failing (%s)" % e, file=sys.stderr)
        return None
    seconds = (r.get("audio") or {}).get("duration") if isinstance(r.get("audio"), dict) else None
    cost = "unknown: not returned by the endpoint"
    if ep.get("price_per_minute") and seconds:
        cost = "about %s, from the price, not a bill" % money(seconds / 60 * float(ep["price_per_minute"]))
    return paths, {"seconds": seconds, "cost": cost}


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

def run(spec_file, stand=False, key_file=None, expect=None):
    spec = json.load(open(spec_file))
    root = project_root(os.path.dirname(os.path.abspath(spec_file)) if spec.get("project") is None else spec["project"])
    guard(root)
    if spec.get("spec", 1) > SPEC_FORMAT: sys.exit("this spec is format %s, newer than this checkout's %d" % (spec["spec"], SPEC_FORMAT))
    if expect:   # the approval is bound to what spends: the plan is worked out again, and must be the one approved
        got = plan_of(spec, root)["hash"]
        if got != expect: sys.exit("refused: what this would send is not the plan approved (%s, now %s): plan it again" % (expect[:12], got[:12]))
    started = now()
    rid = spec.get("id") or "%s-%s" % (stamp(started), slug(spec["name"]))
    kind = spec["endpoint"]["kind"]
    research = kind == "research"
    rpath = report_path(root, rid, research)
    if os.path.exists(rpath): sys.exit(rid + " already has a report: give the request another name")
    if os.path.exists(pending_path(root, rid)): sys.exit(rid + " is pending: finish it with request.py collect " + rid)
    refs = []
    for r in spec.get("references", []):
        f = r.get("file")
        if (f or "").startswith("work/"): sys.exit("refused: %s is in work/, which is never an input; file it first" % f)
        if f and not os.path.exists(os.path.join(root, f)): sys.exit("reference not found: " + f)
        refs.append(dict(r, sha256=sha(os.path.join(root, f))) if f else r)
    if kind == "fal" and not stand:
        tmp = os.path.join(root, ".request-" + rid)
        os.makedirs(tmp, exist_ok=True)
        try:
            sent = fal(spec, root, tmp, key_file)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
        pending = {"id": rid, "spec": spec, "refs": refs, "started": started.strftime("%Y-%m-%dT%H:%M:%SZ"), "sent": sent}
        os.makedirs(os.path.join(root, "requests"), exist_ok=True)
        json.dump(pending, open(pending_path(root, rid), "w"), indent=1)
        return collect(rid, key_file, root=root)
    tmp = os.path.join(root, ".request-" + rid)
    os.makedirs(tmp, exist_ok=True)
    pp = pending_path(root, rid)
    if not stand and kind != "research":   # sent and possibly paid for from here: if this process ends, check says so
        os.makedirs(os.path.join(root, "requests"), exist_ok=True)
        json.dump({"id": rid, "spec": spec, "refs": refs, "started": started.strftime("%Y-%m-%dT%H:%M:%SZ"),
                   "in_flight": True, "kind": kind}, open(pp, "w"), indent=1)
    _keep.clear(); _keep.update(root=root, rid=rid)
    try:
        if stand: paths, sent, result = stand_in(spec, tmp)
        elif kind == "openai-image-edit": paths, sent, result = openai_image(spec, root, tmp, True, key_file)
        elif kind == "openai-image": paths, sent, result = openai_image(spec, root, tmp, False, key_file)
        elif kind == "openrouter-image": paths, sent, result = openrouter_image(spec, root, tmp, key_file)
        elif kind == "openrouter-text": paths, sent, result = language_model(spec, root, tmp, key_file, "openrouter")
        elif kind == "openai-text": paths, sent, result = language_model(spec, root, tmp, key_file, "openai")
        elif kind == "research":
            paths = [os.path.join(root, f) if not os.path.isabs(f) else f for f in spec.get("outputs", [])]
            sent = {"service": "research"}
            result = {"cost": spec["endpoint"].get("cost", "not recorded")}
        elif kind in ("script", "agent"):
            sys.exit("not a request: what the agent or a builder makes goes into prompts/resources/ (request.py resource or build)")
        else: sys.exit("unknown endpoint kind: " + kind)
        finish(root, spec, rid, started, refs, paths, sent, result, stand)
        if os.path.exists(pp): os.remove(pp)
        if _keep.get("file") and os.path.exists(_keep["file"]): os.remove(_keep["file"])   # filed: the kept reply is done
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def pending_path(root, rid):
    return os.path.join(root, "requests", rid + ".pending.json")


def collect(rid, key_file=None, root=None):
    """Finish a fal request that fal accepted: wait for it, file what it made, and write its report. When the wait runs
    out or the network keeps failing, the request stays pending, to be collected again later, never sent again."""
    root = root or project_root()
    pp = pending_path(root, rid)
    if not os.path.exists(pp): sys.exit("no pending request " + rid)
    pend = json.load(open(pp))
    if pend.get("in_flight"):   # a synchronous request: finish it from its kept reply, never by sending it again
        rf = pend.get("reply_file") or next((f for f in (os.path.join(root, "requests", rid + ".reply"),
                                             os.path.join(tempfile.gettempdir(), "spumcake-" + rid + ".reply")) if os.path.exists(f)), None)
        if not rf or not os.path.exists(rf):
            sys.exit("%s has no kept reply, so its result is lost: close it with  request.py close %s --lost \"<why>\"" % (rid, rid))
        tmp = os.path.join(root, ".request-" + rid); os.makedirs(tmp, exist_ok=True)
        try:
            paths, result = decode(pend["kind"], open(rf, "rb").read(), tmp, pend["spec"]["endpoint"])
            sent = pend.get("sent") or {"service": pend["kind"], "note": "what was sent is in the spec"}
            started = datetime.datetime.strptime(pend["started"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc)
            finish(root, pend["spec"], rid, started, pend["refs"], paths, sent, dict(result, collected_from="the kept reply"), False)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
        os.remove(pp); os.remove(rf)
        return
    spec, sent = pend["spec"], pend["sent"]
    tmp = os.path.join(root, ".request-" + rid)
    os.makedirs(tmp, exist_ok=True)
    try:
        try:
            got = fal_collect(sent, spec["endpoint"], tmp, key_file)
        except RuntimeError as e:
            pend["failed"] = str(e); json.dump(pend, open(pp, "w"), indent=1)
            sys.exit("%s; the request failed at fal, and its pending record, %s, says so" % (e, os.path.relpath(pp, root)))
        if got is None:
            sys.exit("fal request %s is not finished yet, and is still paid for: collect it later with\n"
                     "  request.py collect %s\nor cancel it with request.py cancel %s" % (sent["request_id"], rid, rid))
        paths, result = got
        started = datetime.datetime.strptime(pend["started"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc)
        finish(root, spec, rid, started, pend["refs"], paths, sent, result, False)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    os.remove(pp)


def close(rid, why):
    """Close a request whose result is lost, such as a synchronous reply that never reached the disk: its report says
    so, records the cost as likely spent, and files nothing; check stops listing it."""
    root = project_root()
    pp = pending_path(root, rid)
    if not os.path.exists(pp): sys.exit("no pending request " + rid)
    pend = json.load(open(pp)); spec = pend["spec"]
    started = datetime.datetime.strptime(pend["started"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc)
    sent = pend.get("sent") or {"service": pend.get("kind"), "note": "sent; what was sent is in the spec"}
    est = estimate(spec)
    result = {"cost": "likely spent, never filed: " + (est if not est.startswith("unknown") else "amount unknown"), "lost": why}
    spec = dict(spec, notes=((spec.get("notes") or "") + " Lost: " + why).strip())
    finish(root, spec, rid, started, pend["refs"], [], sent, result, False)
    os.remove(pp)


def cancel(rid, key_file=None):
    root = project_root()
    pp = pending_path(root, rid)
    if not os.path.exists(pp): sys.exit("no pending request " + rid)
    pend = json.load(open(pp))
    url = pend["sent"].get("cancel_url")
    if not url: sys.exit("fal returned no cancel address for " + rid)
    fal_key = key("fal-ai", "FAL_KEY", r"[A-Za-z0-9_\-]+:[A-Za-z0-9_\-]+", key_file)
    r = fal_call(fal_key, url, method="PUT")
    pend["cancelled"] = r; json.dump(pend, open(pp, "w"), indent=1)
    print("fal: " + json.dumps(r)[:300])


def finish(root, spec, rid, started, refs, paths, sent, result, stand):
    research = spec["endpoint"]["kind"] == "research"
    rpath = report_path(root, rid, research)
    endpoint_sha, recorded = {}, []
    if not research:
        for i, pth in enumerate(paths):
            endpoint_sha[i] = sha(pth)
            rec = {"spumcake_record": RECORD_FORMAT, "request": rid, "skill": spec.get("skill"), "made_by": "a trained model",
                   "service": sent.get("service"), "model": sent.get("model") or spec["endpoint"].get("model"),
                   "settings": {k: v for k, v in (sent.get("settings") or {}).items() if not k.endswith(("_url", "_urls"))},
                   "prompt": spec.get("prompt"), "asked": spec.get("asked"), "why": spec.get("why"),
                   "pipeline": spec.get("pipeline"), "chain": spec.get("chain"), "step": spec.get("step"),
                   "inputs": [{"order": n + 1, "role": r.get("role"), "canon": r.get("canon"), "file": r.get("file"),
                               "sha256": r.get("sha256")} for n, r in enumerate(refs)],
                   "helpers": [{"name": c.get("name"), "value": c.get("value")} for c in spec.get("canon", [])],
                   "endpoint_sha256": endpoint_sha[i], "skills_commit": skills_commit()}
            if spec.get("setup"): rec["setup"] = spec["setup"]
            if embed_record(pth, rec): recorded.append(i)
    if research:
        names = ["-" + slug(os.path.splitext(os.path.basename(p))[0]) for p in paths]
        outputs = file_into(root, "sources", rid, paths, names)
    else:
        outputs = file_into(root, "library", rid, paths)
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
            "shown": [], "result": result, "notes": spec.get("notes"), "stand_in": bool(stand),
            "tell_format": TELL_FORMAT, "spec": spec.get("spec", SPEC_FORMAT),
            "endpoint_sha256": {outputs[i]: h for i, h in endpoint_sha.items() if i < len(outputs)},
            "record_inside": [outputs[i] for i in recorded if i < len(outputs)], "skills_commit": skills_commit(),
            **({"setup": spec["setup"]} if spec.get("setup") else {})}
    render(root, data, rpath)
    if spec.get("pipeline"):
        run_log(root, spec["pipeline"], {"event": "request", "request": rid, "chain": spec.get("chain"), "step": spec.get("step"),
                                         "outputs": outputs, "stand_in": bool(stand)})
    print(os.path.relpath(rpath, root))
    # What the user is told, word for word: printed with every request, so it is never left out of the reply.
    print("\n--- tell the user, word for word ---", file=sys.stderr)
    _tell_to(root, rpath, sys.stderr)


def attach(rid, f, as_, caption=None):
    root = project_root()
    path = find_report(root, rid)
    data = read_data(path)
    uri = "data:%s;base64,%s" % (mimetypes.guess_type(f)[0] or "image/png", base64.b64encode(open(f, "rb").read()).decode())
    data["shown"].append({"embedded": uri, "as": as_, "caption": caption})
    render(root, data, path)
    print("embedded in " + os.path.relpath(path, root))


def resource(fs, name, date=None, inputs=(), command=None, root=None):
    root = root or project_root()
    os.makedirs(os.path.join(root, "prompts", "resources"), exist_ok=True)
    for i in inputs:
        if i.startswith("git:"): git_source(root, i); continue
        if not os.path.exists(i if os.path.isabs(i) else os.path.join(root, i)): sys.exit("input not found: " + i)
    base = rid = "%s-%s" % (stamp(date), slug(name))
    def taken(r):   # any of the names file_into would give
        return any(os.path.exists(os.path.join(root, "prompts", "resources", r + (("-%d" % (i + 1)) if len(fs) > 1 else "")
                                               + os.path.splitext(f)[1].lower())) for i, f in enumerate(fs))
    k = 2
    while taken(rid):   # a second filing in the same minute, such as a step run twice: the next free name
        rid, k = "%s-%d" % (base, k), k + 1
    filed = file_into(root, "prompts/resources", rid, fs)
    for f in filed:
        record_line(root, f, inputs, command, name)
        print(f)
    return filed


KEY_VARS = ("OPENAI_API_KEY", "OPENROUTER_API_KEY", "FAL_KEY", "FAL_KEY_ID", "FAL_KEY_SECRET")


def keyless_env():
    """The environment without a key: the variables key() reads, and any named like a secret. A builder needs none."""
    secret = re.compile(r"(KEY|KEY_ID|SECRET|TOKEN|PASSWORD|CREDENTIALS)$", re.I)
    return {k: v for k, v in os.environ.items() if k not in KEY_VARS and not secret.search(k)}


def keyless(args, **kw):
    """subprocess.run with no key in the environment. git, ffmpeg, ffprobe, and curl need none, and git in a project
    runs that project's hooks and config commands, such as core.fsmonitor."""
    return subprocess.run(args, env=keyless_env(), **kw)


def build(command, outputs, name, inputs=(), root=None):
    root = root or project_root()
    for o in outputs:   # a folder git never holds, such as .build/ in a fresh clone, is made for the builder
        os.makedirs(os.path.dirname(os.path.join(root, o)) or root, exist_ok=True)
    sys.stdout.flush()
    p = subprocess.run(command, shell=True, cwd=root, stdout=sys.stderr, timeout=3600,   # live, onto stderr, so stdout
                       env=keyless_env())   # the builder is the project's code, not Skills': it gets no key
    if p.returncode: sys.exit("the builder failed (exit %d); its output is above" % p.returncode)   # stays the filed paths
    missing = [o for o in outputs if not os.path.exists(os.path.join(root, o))]
    if missing: sys.exit("the builder made no " + ", ".join(missing))
    return resource([os.path.join(root, o) for o in outputs], name, inputs=inputs, command=command, root=root)


def note(rid, **kw):
    root = project_root()
    path = find_report(root, rid)
    data = read_data(path)
    for k, v in kw.items():
        if v is not None: data[k] = v
    render(root, data, path)


def show(what):
    root = project_root()
    guard(root, write=False)
    base = os.path.basename(what)
    for p, d in all_reports(root):
        made = d.get("outputs", [])
        if d["id"] == base or any(os.path.basename(f) == base for f in made):
            print(json.dumps(d, indent=1)); return
    lines = [l for l in resource_records(root) if os.path.basename(l["file"]) == base]
    if lines:
        print(json.dumps(lines[-1] if len(lines) == 1 else lines, indent=1)); return
    sys.exit("no report or record made " + what)


def record(f):
    r = read_record(f)
    if r is None: sys.exit("no record inside " + f)
    print(json.dumps(r, indent=1, ensure_ascii=False))


def tell(rid):
    root = project_root()
    _tell_to(root, find_report(root, rid), sys.stdout)


def _tell_to(root, path, out):
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
    print("\n".join(lines), file=out)


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
    guard(root, write=False)
    problems, owned = [], set()
    for p, d in all_reports(root):
        for r in d.get("references", []):
            if (r.get("file") or "").startswith("work/"):
                problems.append("%s: sent a file in work/, which is never an input: %s" % (d["id"], r["file"]))
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
    logs = ("agent/index.md", "prompts/resources/records.jsonl")
    g = keyless(["git", "status", "--porcelain", "--", "library", "sources", "prompts", "agent"]
                       + [":!" + l for l in logs], cwd=root, capture_output=True, text=True)
    for line in g.stdout.splitlines():
        code, path = line[:2], line[3:]
        if set(code) & set("MDR"): problems.append("changed or removed in a folder that only grows: " + path)
    for l in logs:   # these are only added to: a change may add lines, never remove one
        d = keyless(["git", "diff", "HEAD", "--numstat", "--", l], cwd=root, capture_output=True, text=True).stdout.split()
        if len(d) >= 2 and d[1] not in ("0", "-"): problems.append("lines removed from a log that only grows: " + l)
    for f in sorted(os.listdir(os.path.join(root, "requests"))) if os.path.isdir(os.path.join(root, "requests")) else []:
        if f.endswith(".pending.json"):
            pend = json.load(open(os.path.join(root, "requests", f)))
            if pend.get("in_flight"):
                problems.append("in flight: %s, a %s request sent at %s and not filed: if the process that sent it ended, "
                                "it may have been paid for and its result lost" % (pend["id"], pend.get("kind"), pend.get("started")))
                continue
            state = "failed at fal" if pend.get("failed") else "cancelled" if pend.get("cancelled") else "paid for, not collected"
            problems.append("pending: %s, %s; request.py collect %s" % (pend["id"], state, pend["id"]))
    for x in problems: print(x)
    print("%d reports checked, %d problems" % (sum(1 for _ in all_reports(root)), len(problems)))
    sys.exit(1 if problems else 0)


def opts(a):
    o, rest, i = {}, [], 0
    while i < len(a):
        if a[i].startswith("--"):
            k = a[i][2:].replace("-", "_")
            if k in ("stand_in", "json"): o[k] = True; i += 1
            elif k == "from": o.setdefault("from", []).append(a[i + 1]); i += 2
            else: o[k] = a[i + 1]; i += 2
        else: rest.append(a[i]); i += 1
    return o, rest


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"): print(__doc__); sys.exit()
    cmd = sys.argv[1]
    o, rest = opts(sys.argv[2:])
    if o.get("setup"): _setup["path"] = o["setup"]
    if cmd == "run": run(rest[0], o.get("stand_in", False), o.get("key_file"), o.get("expect"))
    elif cmd == "plan": plan_cmd(rest[0], "json" in o)
    elif cmd == "version":
        print(json.dumps({"skills_commit": skills_commit(), "spec": SPEC_FORMAT, "report": REPORT_FORMAT, "tell": TELL_FORMAT,
                          "record_inside": RECORD_FORMAT, "canon": 1}, indent=1))
    elif cmd == "collect": collect(rest[0], o.get("key_file"))
    elif cmd == "cancel": cancel(rest[0], o.get("key_file"))
    elif cmd == "close":
        if not o.get("lost"): sys.exit('close needs --lost "<why the result is lost>"')
        close(rest[0], o["lost"])
    elif cmd == "attach": attach(rest[0], rest[1], o["as"], o.get("caption"))
    elif cmd == "note": note(rest[0], asked=o.get("asked"), why=o.get("why"), notes=o.get("notes"))
    elif cmd == "show": show(rest[0])
    elif cmd == "tell": tell(rest[0])
    elif cmd == "resource": resource(rest, o["name"], inputs=o.get("from", []))
    elif cmd == "build": build(rest[0], rest[1:], o["name"], inputs=o.get("from", []))
    elif cmd == "record": record(rest[0])
    elif cmd == "list": listing(o.get("skill"), o.get("pipeline"))
    elif cmd == "check": check()
    elif cmd == "id": print("%s-%s" % (stamp(), slug(rest[0])))
    else: print(__doc__)
