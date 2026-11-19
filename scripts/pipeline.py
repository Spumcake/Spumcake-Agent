#!/usr/bin/env python3
"""A project's living pipeline: pipeline/<n>/canon.sql, its run log pipeline/<n>/runs.jsonl, its chain pages, what
is out of date, and what a change touches. See docs/projects.md.

A project has one living pipeline, the highest-numbered: a change never starts a new one. Canon changes in place, under
each artifact's stable name; history is the run log and canon.sql's git history; out of date is worked out from the
records that made each artifact, never stored.

Usage:
  pipeline.py new <n>                         start pipeline <n>: empty, or, only when the user asks to try a whole
                                              alternative direction, as a copy of the one before it
  pipeline.py sql <n> "<query>" [--read-only] [--as-of <time>]
                                              query the table; --read-only refuses a write; --as-of reads canon as it
                                              stood at a time, from canon.sql's git history
  pipeline.py history <n> [<name>] [--json]   the run log's events, and canon.sql's commits, for one name or all;
                                              for an artifact with --json, its versions newest first: each file, when
                                              it was published, its note, its request, what it was made from with
                                              each source's role, and whether it is canon now
  pipeline.py mark <n> "<label>"              name a moment in the run log, such as "final look settled"
  pipeline.py element <n> <name> --kind K     add a canonical element: a place, character, prop, look, story, sound
  pipeline.py publish <n> "<element>: <role>" --file <file> [--request <id>] --chain <chain>
                     [--from "<element>: <role>" ROLE]... [--with "<element>: <role>=<request id>"]... [--note TEXT]
                     [--waiting] [--fixes]
                                              publish an approved result as canon, in place: the file it replaces stays
                                              where it is, and the run log names it. A take is refused when an input it
                                              was made from is no longer what is published, or its step was edited
                                              since; --with publishes it together with the inputs it was made from.
                                              With --waiting, record a result that waits for the user, not canon
                                              With --fixes, a take of the artifact's own step made again because it
                                              was out of date: its run-log event names the version it fixes
  pipeline.py fact <n> "<element>: <fact>" <value> --artifact "<element>: <role>"
                                              set a canonical fact and the artifact that settles it
  pipeline.py content <n> "<element>: <role>" <json | @file>
                                              what a published image shows: [{"name", "camera", "where", "frame_box",
                                              "state", "mark", "looks_at"}], each thing by its canonical name
  pipeline.py chain <n> <name> --order NN [--title TEXT]
  pipeline.py step <n> <chain> <step> [--order N] [--skill S] [--endpoint JSON] [--template TEXT|@file]
                     [--refs JSON|@file] [--script TEXT] [--request <id>] [--artifact "<element>: <role>"] [--deliver]
                     [--show]
                                              a partial update: what is not given keeps its value, and "" clears it;
                                              --show prints the step as JSON; a ref or script naming work/ is refused
                                              record a step: its prompt as a template naming canon, {{<element>: <fact>}},
                                              its references by canonical artifact, the request that last ran it, and
                                              the artifact it published, if approved
  pipeline.py fill <n> <chain> <step> [--name NAME]
                                              a request spec for the step, filled from this pipeline's table
  pipeline.py touches <n> [--fact "<element>: <fact>" | --artifact "<element>: <role>"] [--json]
                                              with a change named, every published artifact and step it reaches; with
                                              none, everything out of date now, and what is unverified
  pipeline.py keep <n> "<element>: <role>"... --reason TEXT
                                              accept each artifact as it is against its changed inputs; a later change
                                              to any of them flags it again
  pipeline.py rerun <n> [--fact F | --artifact A | --step <chain> <step>] [--stand-in] [--plan | --expect <hash>]
                    [--json]                  make a take of the first step out of date, or the first a change reaches,
                                              or of the step named, out of date or not, filled from the table, and
                                              stop: publishing it comes first. --plan prints, offline, what it would
                                              send or run, with its hash; --expect refuses to run anything but that
                                              plan. The take's files end the output, one "take: <file>" line each, and
                                              "report: <file>" for a request, or "pending: <id>" for one still running;
                                              with --json, one JSON line instead, {chain, step, files, report,
                                              pending, stand_in}
  pipeline.py render <n>                      write the chain pages from the table
  pipeline.py deliver <n> <file>              file a finished deliverable into output/, its record inside cut to the
                                              disclosure and the request's ID
"""
import sys, os, re, json, sqlite3, shutil, html, subprocess, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import request as rq

SCHEMA = """
CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT);
CREATE TABLE IF NOT EXISTS element (name TEXT PRIMARY KEY, kind TEXT, note TEXT);
CREATE TABLE IF NOT EXISTS artifact (id TEXT PRIMARY KEY, element TEXT, role TEXT, file TEXT, request TEXT,
  chain TEXT, published TEXT, note TEXT);
CREATE TABLE IF NOT EXISTS made_from (artifact TEXT, source TEXT, role TEXT);
CREATE TABLE IF NOT EXISTS fact (element TEXT, name TEXT, value TEXT, artifact TEXT, PRIMARY KEY (element, name));
CREATE TABLE IF NOT EXISTS content (artifact TEXT, name TEXT, camera TEXT, "where" TEXT, frame_box TEXT, state TEXT,
  mark TEXT, looks_at TEXT);
CREATE TABLE IF NOT EXISTS chain (name TEXT PRIMARY KEY, ord INTEGER, title TEXT);
CREATE TABLE IF NOT EXISTS step (chain TEXT, ord INTEGER, name TEXT, skill TEXT, endpoint TEXT, template TEXT,
  refs TEXT, script TEXT, request TEXT, artifact TEXT, deliver INTEGER DEFAULT 0, PRIMARY KEY (chain, name));
"""
PLACE = re.compile(r"\{\{([^{}:]+):\s*([^{}]+?)\}\}")


def folder(root, n):
    return os.path.join(root, "pipeline", "%03d" % int(n))


def load(root, n):
    db = sqlite3.connect(":memory:")
    p = os.path.join(folder(root, n), "canon.sql")
    if not os.path.exists(p): sys.exit("no pipeline %03d: start it with new" % int(n))
    db.executescript(open(p).read())
    db.executescript(SCHEMA)
    return db


CANON_FORMAT = 1


def canon_format(db):
    r = db.execute("SELECT value FROM meta WHERE key='format'").fetchone()
    return int(r[0]) if r else 1


def save(root, n, db):
    if canon_format(db) > CANON_FORMAT: sys.exit("refused: canon.sql is format %d, newer than this checkout's %d" % (canon_format(db), CANON_FORMAT))
    db.execute("INSERT OR IGNORE INTO meta VALUES ('format', ?)", (str(CANON_FORMAT),))
    lines = [l for l in db.iterdump() if not l.startswith(("BEGIN", "COMMIT"))]
    open(os.path.join(folder(root, n), "canon.sql"), "w").write("\n".join(lines) + "\n")


def now():
    return rq.now().strftime("%Y-%m-%dT%H:%M:%SZ")


def split(name):
    if ":" not in name: sys.exit('name it as "<element>: <name>": ' + name)
    e, f = name.split(":", 1)
    return e.strip(), f.strip()


def chain_slug(db, chain):
    r = db.execute("SELECT ord FROM chain WHERE name=?", (chain,)).fetchone()
    return "%02d-%s" % (r[0] if r else 0, rq.slug(chain))


# ---- what made each artifact, and what is out of date ------------------------------------------

def events(root, n):
    p = os.path.join(folder(root, n), "runs.jsonl")
    return [json.loads(l) for l in open(p) if l.strip()] if os.path.exists(p) else []


def making(root, db, art):
    """The record that made a published artifact: its request's report, or its records.jsonl line."""
    f, req, pub = db.execute("SELECT file, request, published FROM artifact WHERE id=?", (art,)).fetchone()
    if req:
        try:
            d = rq.read_data(rq.find_report(root, req))
            return {"kind": "report", "data": d, "at": d.get("started") or pub}
        except SystemExit:
            pass
    lines = [l for l in rq.resource_records(root) if l["file"] == f]
    if lines: return {"kind": "record", "data": lines[-1], "at": lines[-1]["at"]}
    return None


def file_sha(root, f):
    return rq.sha(os.path.join(root, f)) if f and os.path.exists(os.path.join(root, f)) else None


def plan_fields(spec):
    ep = spec.get("endpoint") or {}
    return {"model": ep.get("model"), "settings": ep.get("settings") or {}, "prompt": spec.get("prompt") or "",
            "references": [r.get("file") for r in spec.get("references", [])]}


def plan_hash(spec):
    import hashlib
    return hashlib.sha256(json.dumps(plan_fields(spec), sort_keys=True).encode()).hexdigest()


def plan_differs(filled, data):
    """What a step filled now would send differently from what its report says was sent, on the plan's fields only."""
    f, sent, out = plan_fields(filled), data.get("sent") or {}, []
    if (data.get("prompt") or "") != f["prompt"]: out.append("the prompt")
    if [r.get("file") for r in data.get("references", [])] != f["references"]: out.append("the references")
    if sent.get("service") == "stand-in": return out   # a dry run sends no model or settings to compare
    if f["model"] and sent.get("model") and sent["model"] != f["model"]: out.append("the model")
    for k, v in f["settings"].items():
        if k in ("kind", "outputs"): continue
        if (sent.get("settings") or {}).get(k) != v: out.append("the setting " + k)
    return out


def fact_value_at(evs, e, f, when, now_value):
    """A fact's value at a time: the value the first later change replaced, or its value now."""
    for ev in evs:
        if ev.get("event") == "fact" and ev.get("fact") == "%s: %s" % (e, f) and ev["at"] > (when or ""):
            return ev.get("replaced")
    return now_value


def relevant_facts(db, art):
    rows = db.execute("SELECT element, name, value FROM fact WHERE artifact=?", (art,)).fetchall()
    shown = [r[0] for r in db.execute("SELECT DISTINCT name FROM content WHERE artifact=?", (art,))]
    for e in shown: rows += db.execute("SELECT element, name, value FROM fact WHERE element=?", (e,)).fetchall()
    return {"%s: %s" % (e, f): v for e, f, v in rows}


def step_of(db, art):
    return db.execute("SELECT chain, name FROM step WHERE artifact=?", (art,)).fetchone()


def baseline(root, n, db, art, evs):
    """What an artifact was accepted against: its latest keep, or the record that made it."""
    keeps = [e for e in evs if e.get("event") == "keep" and e.get("artifact") == art]
    if keeps: return {"from": "keep", **keeps[-1]}
    m = making(root, db, art)
    if not m: return None
    if m["kind"] == "report":
        d = m["data"]
        inputs = {r["canon"]: {"sha256": r.get("sha256"), "file": r.get("file")} for r in d.get("references", [])
                  if r.get("canon") and r["canon"] != art}   # an edit of an earlier version is not made from itself
        facts = {k: fact_value_at(evs, *k.split(": ", 1), m["at"], v) for k, v in relevant_facts(db, art).items()}
        return {"from": "report", "request": d["id"], "inputs": inputs, "report": d, "facts": facts}
    line = m["data"]
    return {"from": "record", "record_inputs": {i["sha256"] for i in line.get("inputs", [])},
            "facts": {k: fact_value_at(evs, *k.split(": ", 1), m["at"], v) for k, v in relevant_facts(db, art).items()}}


def current_inputs(root, db, art):
    srcs = [s for (s,) in db.execute("SELECT source FROM made_from WHERE artifact=?", (art,)) if s != art]
    out = {}
    for s in srcs:
        r = db.execute("SELECT file FROM artifact WHERE id=?", (s,)).fetchone()
        if r: out[s] = {"file": r[0], "sha256": file_sha(root, r[0])}
    return out


def out_of_date(root, n):
    """Everything out of date now, from canon.sql, the run log, and the records that made each artifact: an input
    published since, a step edited since, or a fact changed since. What has no record to compare is unverified."""
    db = load(root, n)
    evs = events(root, n)
    stale, unverified = {}, {}
    for (art,) in db.execute("SELECT id FROM artifact WHERE published IS NOT NULL"):
        b = baseline(root, n, db, art, evs)
        if not b: unverified[art] = "no record of what made it"; continue
        why, unknown = [], False
        now_in = current_inputs(root, db, art)
        if b["from"] in ("report", "keep"):
            for canon, rec in b.get("inputs", {}).items():
                cur = now_in.get(canon) or {}
                cf = db.execute("SELECT file FROM artifact WHERE id=?", (canon,)).fetchone()
                cur = {"file": cf[0], "sha256": file_sha(root, cf[0])} if cf else cur
                if rec.get("sha256") and cur.get("sha256"):
                    if rec["sha256"] != cur["sha256"]: why.append("%s was published again" % canon)
                elif rec.get("file") and cur.get("file"):
                    if rec["file"] != cur["file"]: why.append("%s was published again (by path)" % canon)
                else: unknown = True
        else:
            for s, cur in now_in.items():
                if cur.get("sha256") and cur["sha256"] not in b["record_inputs"]:
                    why.append("%s is not what it was made from" % s)
        st = step_of(db, art)
        if st:
            try:
                filled = fill(root, n, st[0], st[1])
                if b["from"] == "report":
                    d = plan_differs(filled, b["report"])
                    if d: why.append("its step was edited: " + ", ".join(d))
                elif b["from"] == "keep" and b.get("plan") and b["plan"] != plan_hash(filled):
                    why.append("its step was edited since it was kept")
            except SystemExit:
                unknown = True
        cur_facts = relevant_facts(db, art)
        for k, was in (b.get("facts") or {}).items():
            if k in cur_facts and cur_facts[k] != was: why.append("the fact %s changed" % k)
        if why: stale[art] = why
        elif unknown: unverified[art] = "its record holds no sha256 for an input"
    for art in list(stale):
        reached, _ = touches(root, n, artifact=art)
        for a in reached:
            if a != art and a not in stale: stale[a] = ["made from %s, which is out of date" % art]
            unverified.pop(a, None) if a in stale else None
    return stale, unverified


# ---- commands ----------------------------------------------------------------------------------

def new(root, n):
    d = folder(root, n)
    if os.path.exists(d): sys.exit("pipeline %03d exists" % int(n))
    before = sorted(x for x in os.listdir(os.path.join(root, "pipeline")) if x.isdigit() and int(x) < int(n)) \
        if os.path.isdir(os.path.join(root, "pipeline")) else []
    if before:
        shutil.copytree(folder(root, before[-1]), d, ignore=shutil.ignore_patterns("*.html"))
        print("pipeline %03d starts as a copy of %s" % (int(n), before[-1]))
    else:
        os.makedirs(d)
        db = sqlite3.connect(":memory:"); db.executescript(SCHEMA); save(root, n, db)
        print("pipeline %03d starts empty" % int(n))


def fill(root, n, chain, step, name=None):
    db = load(root, n)
    r = db.execute("SELECT skill, endpoint, template, refs, script, ord FROM step WHERE chain=? AND name=?",
                   (chain, step)).fetchone()
    if not r: sys.exit("no step %s in chain %s" % (step, chain))
    skill, endpoint, template, refs, script, _ = r
    if skill == "generate-keyframe" and step.startswith("keyframe, "):
        # A moment's staging floor plan comes first: no frame of a moment is made until its plan is approved.
        moment = step[len("keyframe, "):]
        plan = db.execute("SELECT published FROM artifact WHERE id=?", ("%s: staging floor plan" % moment,)).fetchone()
        if not plan or not plan[0]:
            sys.exit("no approved staging floor plan for %s: draw it with build-previs, have the user approve it, "
                     "and publish it as \"%s: staging floor plan\" before any keyframe of the moment" % (moment, moment))
    read, missing = [], []

    def value(m):
        e, f = m.group(1).strip(), m.group(2).strip()
        v = db.execute("SELECT value FROM fact WHERE element=? AND name=?", (e, f)).fetchone()
        if not v: missing.append("%s: %s" % (e, f)); return m.group(0)
        if not any(r["name"] == "%s: %s" % (e, f) for r in read):
            read.append({"name": "%s: %s" % (e, f), "value": v[0], "read_at": now(),
                         "from": "pipeline/%03d/canon.sql" % int(n)})
        return v[0]

    prompt = PLACE.sub(value, template or "")
    command = PLACE.sub(value, script) if script else None
    references = []
    for ref in json.loads(refs or "[]"):
        if ref.get("file"):
            references.append({"file": ref["file"], "role": ref.get("role", ""), "canon": None,
                               "note": "a fixed input, not canon", **({"field": ref["field"]} if ref.get("field") else {})})
            continue
        a = db.execute("SELECT file FROM artifact WHERE id=?", (ref["artifact"],)).fetchone()
        if not a: missing.append(ref["artifact"]); continue
        references.append({"file": a[0], "role": ref.get("role", ""), "canon": ref["artifact"],
                           **({"field": ref["field"]} if ref.get("field") else {})})
        read.append({"name": ref["artifact"], "value": a[0], "read_at": now(), "from": "pipeline/%03d/canon.sql" % int(n)})
    if missing: sys.exit("not in pipeline %03d's canon: %s" % (int(n), "; ".join(missing)))
    spec = {"name": name or "%s-p%03d" % (rq.slug(step), int(n)), "skill": skill, "pipeline": "%03d" % int(n),
            "chain": chain, "step": step, "endpoint": json.loads(endpoint or "{}"), "prompt": prompt,
            "references": references, "canon": read}
    if command:
        out = json.loads(endpoint or "{}").get("outputs", [])
        spec["scripts"] = [{"command": command}]
        spec["outputs"] = out
    return spec


def touches(root, n, fact=None, artifact=None):
    db = load(root, n)
    arts, steps = set(), set()
    if fact:
        e, f = split(fact)
        r = db.execute("SELECT artifact FROM fact WHERE element=? AND name=?", (e, f)).fetchone()
        if not r: sys.exit("no such fact in pipeline %03d: %s" % (int(n), fact))
        if r[0]: arts.add(r[0])
        for c, s, t in db.execute("SELECT chain, name, template FROM step"):
            if any((m.group(1).strip(), m.group(2).strip()) == (e, f) for m in PLACE.finditer(t or "")):
                steps.add((c, s))
        for (a,) in db.execute("SELECT DISTINCT artifact FROM content WHERE name=?", (e,)): arts.add(a)
    if artifact: arts.add(artifact)
    changed = {split(fact)[0]} if fact else {split(artifact)[0]} if artifact else set()
    element = dict(db.execute("SELECT id, element FROM artifact").fetchall())
    kind = dict(db.execute("SELECT name, kind FROM element").fetchall())
    shows = collections.defaultdict(set)
    for a, nm in db.execute("SELECT artifact, name FROM content"): shows[a].add(nm)

    def reaches(src, dst):
        # a change carries into another element's results only where they show what changed, or are the film's own shots
        return (element.get(dst) == element.get(src) or kind.get(element.get(dst)) in ("film", "moment")
                or bool(shows[dst] & changed))

    while True:
        size = len(arts) + len(steps)
        for a, s in db.execute("SELECT artifact, source FROM made_from").fetchall():
            if s != a and s in arts and reaches(s, a): arts.add(a)
        for c, s, refs, a in db.execute("SELECT chain, name, refs, artifact FROM step").fetchall():
            if a and a in arts: steps.add((c, s))
            elif not a and any(r.get("artifact") in arts for r in json.loads(refs or "[]")): steps.add((c, s))
            if (c, s) in steps and a: arts.add(a)
        if len(arts) + len(steps) == size: break
    order = {c: o for c, o in db.execute("SELECT name, ord FROM chain")}
    sord = {(c, s): o for c, s, o in db.execute("SELECT chain, name, ord FROM step")}
    return (sorted(arts), sorted(steps, key=lambda cs: (order.get(cs[0], 99), sord.get(cs, 99))))


def versions(root, n, art):
    """An artifact's versions, newest first, worked out from the run log and canon.sql's git history: each file, when
    it was published, its note and request, what it was made from with each source's role (None when no record says),
    and whether it is canon now. The same file published twice is one version, at its latest publish."""
    db = load(root, n)
    now_row = db.execute("SELECT file, published FROM artifact WHERE id=?", (art,)).fetchone()
    seen = {}
    def add(f, at, note, req, source, made_from):
        if not f: return
        v = seen.get(f)
        if not v or (at or "") > (v["published"] or ""):
            seen[f] = {"file": f, "published": at, "note": note, "request": req, "from": source, "made_from": made_from,
                       "edited_from": None, "fixes": None}
        elif v["made_from"] is None and made_from is not None and (at or "") == (v["published"] or ""):
            v["made_from"] = made_from   # the same publish, its roles from canon.sql when the run log lacks them
    for ev in events(root, n):   # the run log: every publish since it began
        if ev.get("event") == "publish" and ev.get("artifact") == art:
            add(ev.get("file"), ev.get("at"), ev.get("note"), ev.get("request"), "the run log", ev.get("sources"))
            seen[ev["file"]].update({k: ev.get(k) for k in ("edited_from", "fixes")})
    rel = os.path.relpath(os.path.join(folder(root, n), "canon.sql"), root)   # older: canon.sql as each commit held it
    log = rq.keyless(["git", "log", "--format=%H", "--", rel], cwd=root, capture_output=True, text=True).stdout.split()
    for c in log:
        src = rq.keyless(["git", "show", "%s:./%s" % (c, rel)], cwd=root, capture_output=True, text=True)   # ./: from root
        if src.returncode: continue
        old = sqlite3.connect(":memory:")
        try:
            old.executescript(src.stdout)
            row = old.execute("SELECT file, published, note, request FROM artifact WHERE id=?", (art,)).fetchone()
            srcs = [{"source": a, "role": r} for a, r in old.execute("SELECT source, role FROM made_from WHERE artifact=?", (art,))]
        except sqlite3.Error:
            continue
        if row and row[1]: add(row[0], row[1], row[2], row[3], "canon.sql at %s" % c[:7], srcs)
    order = {f: i for i, f in enumerate(seen)}   # the order they were last added in, the run log's, for a tie
    out = sorted(seen.values(), key=lambda v: (v["published"] or "", order[v["file"]]), reverse=True)
    for v in out: v["canon_now"] = bool(now_row and now_row[1] and now_row[0] == v["file"])
    if not out and not now_row: sys.exit("no artifact %s in pipeline %03d" % (art, int(n)))
    return out


def published_versions(root, n, art):
    """Every file the artifact was ever published as, by sha256: what an edit of it may be made from."""
    try:
        return {file_sha(root, v["file"]): v["file"] for v in versions(root, n, art)
                if os.path.exists(os.path.join(root, v["file"]))}
    except SystemExit:
        return {}


def edited_from(root, n, art, o):
    """The published version of art this take was made from, when it is an edit of the artifact itself."""
    shas = []
    if o.get("request"):
        d = rq.read_data(rq.find_report(root, o["request"]))
        shas = [r.get("sha256") for r in d.get("references", []) if r.get("canon") == art]
    elif any(s == art for s, _ in o.get("from", [])):
        lines = [l for l in rq.resource_records(root) if l["file"] == o["file"]]
        shas = [i["sha256"] for i in lines[-1].get("inputs", [])] if lines else []
    vs = published_versions(root, n, art) if shas else {}
    return next((vs[h] for h in shas if h in vs), None), bool(shas)


def check_fix(root, n, db, art, o, old):
    """--fixes: the take is the artifact made again from its own step, standing in for a published version."""
    if not (old and old[1]): sys.exit("refused --fixes: %s has no published version to fix" % art)
    st = step_of(db, art)
    if not st: sys.exit("refused --fixes: no step makes %s" % art)
    if o.get("request"):
        d = rq.read_data(rq.find_report(root, o["request"]))
        made = (d.get("chain"), d.get("step"))
    else:   # a script step's take: the run that filed it
        runs = [e for e in events(root, n) if e.get("event") == "run" and o["file"] in (e.get("files") or [])]
        made = (runs[-1]["chain"], runs[-1]["step"]) if runs else (None, None)
    if tuple(made) != tuple(st):
        sys.exit("refused --fixes: the take was not made from %s's step, %s / %s" % (art, st[0], st[1]))


def check_take(root, n, db, art, o):
    """Refuse to publish a take whose inputs are no longer what is published, whose step was edited since, or, for a
    file made without a model, whose record does not hold each source it is said to be made from."""
    withs = dict(w.split("=", 1) for w in o.get("with", []))
    problems = []
    if o.get("request"):
        d = rq.read_data(rq.find_report(root, o["request"]))
        for r in d.get("references", []):
            c = r.get("canon")
            if not c or not r.get("sha256"): continue
            if c == art:   # an edit of the artifact itself: made from any version of it that was published
                if r["sha256"] not in published_versions(root, n, art):
                    problems.append("it was made from a version of %s that was never published" % art)
                continue
            if c in withs:
                wd = rq.read_data(rq.find_report(root, withs[c]))
                if file_sha(root, wd["outputs"][0]) != r["sha256"]:
                    problems.append("%s: the take was not made from %s's take %s" % (c, c, withs[c]))
                continue
            cur = db.execute("SELECT file FROM artifact WHERE id=? AND published IS NOT NULL", (c,)).fetchone()
            if cur and file_sha(root, cur[0]) != r["sha256"]:
                problems.append("%s has been published again since this take was made" % c)
        st = step_of(db, art)
        if st:
            try:
                filled = fill(root, n, st[0], st[1])
                for r in filled.get("references", []):   # an input published with this take counts as its take
                    if r.get("canon") in withs:
                        r["file"] = rq.read_data(rq.find_report(root, withs[r["canon"]]))["outputs"][0]
                diff = plan_differs(filled, d)
                if diff: problems.append("its step was edited since this take was made: " + ", ".join(diff))
            except SystemExit:
                pass
    elif o["from"]:
        lines = [l for l in rq.resource_records(root) if l["file"] == o["file"]]
        held = {i["sha256"] for i in lines[-1].get("inputs", [])} if lines else set()
        for s, _ in o["from"]:
            if s == art:   # an edit of the artifact itself: made from any version of it that was published
                if lines and not held & set(published_versions(root, n, art)):
                    problems.append("it was made from a version of %s that was never published" % art)
                continue
            cur = db.execute("SELECT file FROM artifact WHERE id=?", (s,)).fetchone()
            h = file_sha(root, cur[0]) if cur else None
            if not lines: problems.append("%s has no record of what made it: file it with request.py resource or build --from" % o["file"])
            elif h and h not in held: problems.append("its record does not hold %s as it is published now" % s)
    if problems: sys.exit("refused to publish %s:\n  " % art + "\n  ".join(dict.fromkeys(problems)))


def step_plan(root, n, chain, step):
    """What a rerun of one step would send or run, offline, with its hash, as request.py plan works it out."""
    spec = fill(root, n, chain, step)
    kind = spec["endpoint"].get("kind")
    if kind in ("script", "agent"):
        refs = [r["file"] for r in spec.get("references", []) if r.get("file")]
        plan = {"plan": rq.SPEC_FORMAT, "chain": chain, "step": step, "kind": kind,
                "script": spec["scripts"][0]["command"] if spec.get("scripts") else None,
                "inputs": [{"file": f, "sha256": file_sha(root, f)} for f in refs], "outputs": spec.get("outputs", []),
                "estimate": "nothing: a script runs on this computer"}
        plan["hash"] = rq.plan_hash({k: v for k, v in plan.items()})
        return plan, spec
    return rq.plan_of(spec, root), spec


def rerun(root, n, fact=None, artifact=None, stand=False, plan_only=False, as_json=False, expect=None, named=None):
    """Make a take of the first step out of date, of the first step a change reaches, or of the step named, and stop.
    A take changes no canon: the user approves it, publish puts it in, and the next rerun then makes the step below."""
    if named:
        if not load(root, n).execute("SELECT 1 FROM step WHERE chain=? AND name=?", named).fetchone():
            sys.exit("no step %s in chain %s" % (named[1], named[0]))
        steps = [tuple(named)]
    elif fact or artifact:
        _, steps = touches(root, n, fact=fact, artifact=artifact)
    else:
        stale, _ = out_of_date(root, n)
        db = load(root, n)
        order = {c: o for c, o in db.execute("SELECT name, ord FROM chain")}
        steps = sorted({(c, s) for c, s, a in db.execute("SELECT chain, name, artifact FROM step") if a in stale},
                       key=lambda cs: (order.get(cs[0], 99), db.execute(
                           "SELECT ord FROM step WHERE chain=? AND name=?", cs).fetchone()[0]))
    if not steps: print("nothing to run again"); return
    chain, step = steps[0]
    plan, spec = step_plan(root, n, chain, step)
    if plan_only:
        if as_json: print(json.dumps(plan, indent=1, ensure_ascii=False))
        else:
            print("%s step: %s / %s" % ("The" if named else "Next", chain, step))
            if plan.get("script"): print("Runs: " + plan["script"])
            else: print("Sends to: %s, %s" % (plan["endpoint"]["kind"], plan["endpoint"]["model"]))
            print("Estimate: " + plan["estimate"]); print("Plan hash: " + plan["hash"])
        return
    if expect and plan["hash"] != expect:
        sys.exit("refused: the next step's plan is not the one approved (%s, now %s): plan it again" % (expect[:12], plan["hash"][:12]))
    kind = spec["endpoint"].get("kind")
    db = load(root, n)
    art, skill = db.execute("SELECT artifact, skill FROM step WHERE chain=? AND name=?", (chain, step)).fetchone()
    if kind in ("script", "agent"):
        if not stand and (kind == "agent" or not spec.get("scripts")):
            sys.exit("%s is the agent's own work, not a request: make it again with %s, then publish it" % (step, skill))
        refs = [r["file"] for r in spec.get("references", []) if r.get("file")]
        if stand:
            tmp = os.path.join(root, ".stand-in"); os.makedirs(tmp, exist_ok=True)
            try:
                made = rq.stand_in(spec, tmp)[0]
                filed = rq.resource(made, spec["name"], inputs=refs, command="stand-in", root=root)
            finally:
                shutil.rmtree(tmp, ignore_errors=True)
        else:
            filed = rq.build(spec["scripts"][0]["command"], spec.get("outputs", []), spec["name"], inputs=refs, root=root)
        rq.run_log(root, n, {"event": "run", "chain": chain, "step": step, "files": filed, "stand_in": stand})
        print("%s: a take, %s" % (step, ", ".join(filed)))
        report = pending = None
    else:
        import tempfile
        spec["asked"] = "Make a take of %s%s in pipeline %03d" % (step, "" if named else ", out of date,", int(n))
        spec["why"] = ("It reaches %s" % (fact or artifact)) if (fact or artifact) else (
            "The user asked for a take of this step" if named else "It is out of date: " + "; ".join(
            out_of_date(root, n)[0].get(art, ["its inputs changed"])))
        base = "%s-%s" % (rq.stamp(), rq.slug(spec["name"])); spec["id"], k = base, 2   # named here, so its report is known
        while os.path.exists(rq.report_path(root, spec["id"])) or os.path.exists(rq.pending_path(root, spec["id"])):
            spec["id"] = "%s-%d" % (base, k); k += 1   # a second take in the same minute
        with tempfile.NamedTemporaryFile("w", suffix=".json", dir=root, delete=False) as f:
            json.dump(spec, f); spec_file = f.name
        sys.stdout.flush()
        try:   # request.py's output goes straight through, live, so a stopped rerun loses none of it
            out = subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), "request.py"), "run", spec_file]
                                 + (["--stand-in"] if stand else []) + (["--expect", expect] if expect else []), cwd=root)
        finally:
            os.unlink(spec_file)
        if out.returncode: sys.exit("%s: request.py stopped (exit %d); its output is above" % (step, out.returncode))
        report, pending = os.path.relpath(rq.report_path(root, spec["id"]), root), None
        if os.path.exists(os.path.join(root, report)):
            print("%s: a take, %s" % (step, report))
            filed = rq.read_data(os.path.join(root, report)).get("outputs", [])
        else:   # a queued request still running: request.py collect files it
            report, pending, filed = None, spec["id"], []
            print("%s: a take on its way, %s; request.py collect %s files it" % (step, pending, pending))
    if art:
        reached, _ = touches(root, n, artifact=art)
        print("publishing it as %s would reach: %s" % (art, ", ".join(a for a in reached if a != art) or "nothing else"))
    print("stopped after one step: publish it first, then run again for the step below")
    if as_json:   # last, on one line, for a setup to read
        print(json.dumps({"chain": chain, "step": step, "files": filed, "report": report,
                          "pending": pending, "stand_in": stand}, ensure_ascii=False))
    else:
        for f in filed: print("take: " + f)
        if report: print("report: " + report)
        if pending: print("pending: " + pending)


def deliver(root, n, f):
    ext = os.path.splitext(f)[1]
    dst = os.path.join(root, "output", "%s-%03d-%s%s" % (rq.stamp(), int(n), os.path.basename(root), ext))
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if os.path.exists(dst): sys.exit("refusing to overwrite " + dst)
    rid = os.path.splitext(os.path.basename(f))[0]
    rq.strip_record(os.path.join(root, f), dst, re.sub(r"-\d+$", "", rid))
    print(os.path.relpath(dst, root))


def render(root, n):
    db = load(root, n)
    esc = html.escape
    d = folder(root, n)
    for old in os.listdir(d):
        if old.endswith(".html"): os.remove(os.path.join(d, old))
    chains = db.execute("SELECT name, ord, title FROM chain ORDER BY ord").fetchall()
    where = {a: chain_slug(db, c) for a, c in db.execute("SELECT id, chain FROM artifact")}
    for name, ord_, title in chains:
        page = os.path.join(d, chain_slug(db, name) + ".html")
        rel = lambda f: os.path.relpath(os.path.join(root, f), d)
        parts = ["<!doctype html><html lang='en'><head><meta charset='utf-8'>",
                 "<meta name='viewport' content='width=device-width,initial-scale=1'>",
                 "<title>%s</title><style>%s .ph{color:var(--accent);font-weight:600}</style></head><body>" % (
                     esc(name), rq.STYLE),
                 "<h1>%s</h1><p class='meta'>pipeline %03d · chain %02d%s</p>" % (
                     esc(name), int(n), ord_, (" · " + esc(title)) if title else "")]
        for (sname, sord, skill, endpoint, template, refs, script, request, art, dlv) in db.execute(
                "SELECT name, ord, skill, endpoint, template, refs, script, request, artifact, deliver FROM step "
                "WHERE chain=? ORDER BY ord", (name,)):
            pub = db.execute("SELECT published FROM artifact WHERE id=?", (art,)).fetchone() if art else None
            status = "published" if pub and pub[0] else "waiting for the user"
            parts.append("<h2>%d. %s</h2><p class='meta'>%s · %s%s</p>" % (
                sord, esc(sname), esc(skill or ""), status, " · delivered to output/" if dlv else ""))
            if art:
                a = db.execute("SELECT file, published, note FROM artifact WHERE id=?", (art,)).fetchone()
                if a:
                    parts.append("<figure>%s<figcaption><b>%s</b> · %s%s</figcaption></figure>" % (
                        rq.media_tag(a[0], rel(a[0]), os.path.join(root, a[0])), esc(art), ("published " + esc(a[1])) if a[1] else "waiting for the user",
                        (" · " + esc(a[2])) if a[2] else ""))
                    srcs = db.execute("SELECT source, role FROM made_from WHERE artifact=?", (art,)).fetchall()
                    if srcs:
                        parts.append("<p>Made from: %s</p>" % "; ".join(
                            "%s (%s)%s" % (esc(s), esc(r or ""), (" in <a href='%s.html'>%s</a>" % (where[s], where[s]))
                                           if where.get(s) and where[s] != chain_slug(db, name) else "") for s, r in srcs))
                    facts = db.execute("SELECT element, name, value FROM fact WHERE artifact=?", (art,)).fetchall()
                    if facts:
                        parts.append("<table><tr><th>Fact it settles</th><th>Value</th></tr>%s</table>" % "".join(
                            "<tr><td>%s: %s</td><td>%s</td></tr>" % (esc(e), esc(f), esc(v)) for e, f, v in facts))
                    cont = db.execute('SELECT name, camera, "where", state, looks_at FROM content WHERE artifact=?',
                                      (art,)).fetchall()
                    if cont:
                        parts.append("<table><tr><th>In frame</th><th>Camera</th><th>Where</th><th>State</th>"
                                     "<th>Looks at</th></tr>%s</table>" % "".join(
                                         "<tr>%s</tr>" % "".join("<td>%s</td>" % esc(x or "") for x in c) for c in cont))
            if request:
                rp = rq.report_path(root, request)
                parts.append("<p>Last run: <a href='%s'>%s</a></p>" % (esc(os.path.relpath(rp, d)), esc(request)))
            parts.append("<p>Endpoint: <code>%s</code></p>" % esc(endpoint or ""))
            if template:
                t = esc(template)
                t = re.sub(r"\{\{([^{}]+)\}\}", lambda m: "<span class='ph'>{{%s}}</span>" % m.group(1), t)
                parts.append("<p>Prompt template, naming canon:</p><pre>%s</pre>" % t)
            if script: parts.append("<p>Script:</p><pre>%s</pre>" % esc(script))
            rs = json.loads(refs or "[]")
            if rs:
                parts.append("<div class='grid'>")
                for i, r in enumerate(rs, 1):
                    f = (r["file"],) if r.get("file") else db.execute("SELECT file FROM artifact WHERE id=?", (r["artifact"],)).fetchone()
                    other = where.get(r.get("artifact"))
                    tag = rq.media_tag(f[0], rel(f[0]), os.path.join(root, f[0])) if f else "not in canon"
                    parts.append("<figure>%s<figcaption>%d. %s<br>%s%s</figcaption></figure>" % (
                        tag, i, esc(r.get("role", "")), esc(r.get("artifact") or "a fixed input, not canon"),
                        (" · <a href='%s.html'>%s</a>" % (other, other)) if other and other != chain_slug(db, name) else ""))
                parts.append("</div>")
        parts.append("</body></html>")
        open(page, "w").write("\n".join(parts))
        print(os.path.relpath(page, root))


def opts(a):
    o, rest, i = {"from": []}, [], 0
    while i < len(a):
        if a[i].startswith("--"):
            k = a[i][2:].replace("-", "_")
            if k in ("stand_in", "next", "deliver", "waiting", "read_only", "json", "show", "plan", "fixes"): o[k] = True; i += 1
            elif k == "with": o.setdefault("with", []).append(a[i + 1]); i += 2
            elif k == "from": o["from"].append((a[i + 1], a[i + 2])); i += 3
            elif k == "step": o["step"] = (a[i + 1], a[i + 2]); i += 3
            else: o[k] = a[i + 1]; i += 2
        else: rest.append(a[i]); i += 1
    return o, rest


def text(v):
    return open(v[1:]).read() if v and v.startswith("@") else v


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"): print(__doc__); sys.exit()
    cmd = sys.argv[1]
    o, rest = opts(sys.argv[2:])
    if o.get("setup"):   # the setup file, for this command and every request it runs (docs/setup.md)
        os.environ["SKILLS_SETUP"] = os.path.abspath(o["setup"]); rq._setup["path"] = os.environ["SKILLS_SETUP"]
    root = rq.project_root()
    n = rest[0] if rest else None
    reads = cmd in ("fill", "touches", "history", "render") or (cmd == "sql" and (o.get("read_only") or o.get("as_of") or
            (len(rest) > 1 and rest[1].lstrip().upper().startswith(("SELECT", "WITH", "PRAGMA"))))) \
        or (cmd == "step" and o.get("show")) or (cmd == "rerun" and o.get("plan"))
    rq.guard(root, write=not reads)
    if cmd == "new": new(root, n)
    elif cmd == "sql":
        q = rest[1]
        writes = not q.lstrip().upper().startswith(("SELECT", "WITH", "PRAGMA"))
        if o.get("read_only") and writes: sys.exit("refused: --read-only, and this query writes")
        if o.get("as_of"):
            rel = os.path.relpath(os.path.join(folder(root, n), "canon.sql"), root)
            c = rq.keyless(["git", "log", "-1", "--before=" + o["as_of"], "--format=%H", "--", rel], cwd=root,
                               capture_output=True, text=True).stdout.strip()
            if not c: sys.exit("canon.sql has no commit before " + o["as_of"])
            db = sqlite3.connect(":memory:")
            db.executescript(rq.keyless(["git", "show", "%s:./%s" % (c, rel)], cwd=root, capture_output=True, text=True).stdout)
            for row in db.execute(q): print(" | ".join("" if x is None else str(x) for x in row))
        else:
            db = load(root, n)
            for row in db.execute(q): print(" | ".join("" if x is None else str(x) for x in row))
            if writes: save(root, n, db)
    elif cmd == "element":
        db = load(root, n); db.execute("INSERT OR REPLACE INTO element VALUES (?,?,?)", (rest[1], o.get("kind"), o.get("note")))
        save(root, n, db)
    elif cmd == "publish":
        db = load(root, n); e, role = split(rest[1])
        if not os.path.exists(os.path.join(root, o["file"])): sys.exit("not found: " + o["file"])
        if not o.get("waiting"): check_take(root, n, db, rest[1], o)
        edited, is_edit = edited_from(root, n, rest[1], o)
        old = db.execute("SELECT file, published FROM artifact WHERE id=?", (rest[1],)).fetchone()
        if o.get("fixes"): check_fix(root, n, db, rest[1], o, old)
        for w in o.get("with", []):
            wa, wr = w.split("=", 1)
            wd = rq.read_data(rq.find_report(root, wr))
            wold = db.execute("SELECT file FROM artifact WHERE id=?", (wa,)).fetchone()
            db.execute("UPDATE artifact SET file=?, request=?, published=? WHERE id=?", (wd["outputs"][0], wr, now(), wa))
            rq.run_log(root, n, {"event": "publish", "artifact": wa, "file": wd["outputs"][0], "request": wr,
                                 "replaced": wold[0] if wold else None, "with": rest[1]})
        db.execute("INSERT OR REPLACE INTO artifact VALUES (?,?,?,?,?,?,?,?)",
                   (rest[1], e, role, o["file"], o.get("request"), o.get("chain"),
                    None if o.get("waiting") else (o.get("published") or now()), o.get("note")))
        db.execute("DELETE FROM made_from WHERE artifact=?", (rest[1],))
        for s, r in o["from"]:
            if s != rest[1]: db.execute("INSERT INTO made_from VALUES (?,?,?)", (rest[1], s, r))   # never from itself
        save(root, n, db)
        rq.run_log(root, n, {"event": "waiting" if o.get("waiting") else "publish", "artifact": rest[1], "file": o["file"],
                             "request": o.get("request"), "replaced": old[0] if old and old[1] else None,
                             "made_from": [s for s, _ in o["from"] if s != rest[1]], "note": o.get("note"),
                             "sources": [{"source": s, "role": r} for s, r in o["from"] if s != rest[1]],   # for a revert
                             **({"edited_from": edited} if is_edit else {}),   # the version of itself it was made from
                             **({"fixes": old[0]} if o.get("fixes") else {})})   # made again because it was out of date
    elif cmd == "fact":
        db = load(root, n); e, f = split(rest[1])
        old = db.execute("SELECT value FROM fact WHERE element=? AND name=?", (e, f)).fetchone()
        db.execute("INSERT OR REPLACE INTO fact VALUES (?,?,?,?)", (e, f, rest[2], o.get("artifact")))
        save(root, n, db)
        rq.run_log(root, n, {"event": "fact", "fact": rest[1], "value": rest[2], "replaced": old[0] if old else None,
                             "artifact": o.get("artifact")})
    elif cmd == "content":
        db = load(root, n); rows = json.loads(text(rest[2]))
        db.execute("DELETE FROM content WHERE artifact=?", (rest[1],))
        for c in rows:
            db.execute("INSERT INTO content VALUES (?,?,?,?,?,?,?,?)", (rest[1], c.get("name"), c.get("camera"), c.get("where"),
                       json.dumps(c["frame_box"]) if c.get("frame_box") else None, c.get("state"), c.get("mark"), c.get("looks_at")))
        save(root, n, db)
    elif cmd == "chain":
        db = load(root, n); db.execute("INSERT OR REPLACE INTO chain VALUES (?,?,?)", (rest[1], int(o["order"]), o.get("title")))
        save(root, n, db)
    elif cmd == "step":
        db = load(root, n)
        cols = ["chain", "ord", "name", "skill", "endpoint", "template", "refs", "script", "request", "artifact", "deliver"]
        old = db.execute("SELECT * FROM step WHERE chain=? AND name=?", (rest[1], rest[2])).fetchone()
        if o.get("show") or o.get("json"):
            if not old: sys.exit("no step %s in chain %s" % (rest[2], rest[1]))
            print(json.dumps(dict(zip(cols, old)), indent=1, ensure_ascii=False)); sys.exit()
        # a partial update: what is not given keeps its value; an empty value clears it
        cur = dict(zip(cols, old)) if old else {c: None for c in cols}
        given = {"ord": o.get("order"), "skill": o.get("skill"), "endpoint": o.get("endpoint"), "template": text(o.get("template")),
                 "refs": text(o.get("refs")), "script": o.get("script"), "request": o.get("request"), "artifact": o.get("artifact")}
        for k, v in given.items():
            if v is not None: cur[k] = (int(v) if k == "ord" else (v or None))
        if o.get("deliver"): cur["deliver"] = 1
        if cur["ord"] is None: sys.exit("a new step needs --order")
        for r in json.loads(cur["refs"] or "[]"):   # a setup's workspace files are never an input (the user, 2026-11-16)
            if (r.get("file") or "").startswith("work/"): sys.exit("refused: %s is in work/, which is never an input; file it first" % r["file"])
        if cur["script"] and re.search(r"(^|[\s'\"=/])work/", cur["script"]): sys.exit("refused: the script names work/, which is never an input")
        new_row = (rest[1], cur["ord"], rest[2], cur["skill"], cur["endpoint"], cur["template"], cur["refs"], cur["script"],
                   cur["request"], cur["artifact"], cur["deliver"] or 0)
        db.execute("INSERT OR REPLACE INTO step VALUES (?,?,?,?,?,?,?,?,?,?,?)", new_row)
        save(root, n, db)
        if not old or tuple(old) != new_row:
            rq.run_log(root, n, {"event": "step", "chain": rest[1], "step": rest[2],
                                 "replaced": dict(zip(cols, old)) if old else None})
    elif cmd == "fill": print(json.dumps(fill(root, n, rest[1], rest[2], o.get("name")), indent=1))
    elif cmd == "touches":
        if o.get("fact") or o.get("artifact"):
            arts, steps = touches(root, n, o.get("fact"), o.get("artifact"))
            if o.get("json"): print(json.dumps({"artifacts": arts, "steps": [list(s) for s in steps]}, indent=1))
            else:
                print("Published artifacts:"); [print("  " + a) for a in arts]
                print("Steps, in order:"); [print("  %s / %s" % s) for s in steps]
        else:
            stale, unverified = out_of_date(root, n)
            if o.get("json"):
                print(json.dumps({"out_of_date": [{"artifact": a, "why": w} for a, w in sorted(stale.items())],
                                  "unverified": [{"artifact": a, "why": w} for a, w in sorted(unverified.items())]}, indent=1))
            else:
                print("Out of date:"); [print("  %s: %s" % (a, "; ".join(w))) for a, w in sorted(stale.items())]
                print("Unverified:"); [print("  %s: %s" % (a, w)) for a, w in sorted(unverified.items())]
    elif cmd == "keep":
        if not o.get("reason"): sys.exit("keep needs --reason: why each still holds")
        db = load(root, n); evs = events(root, n)
        for art in rest[1:]:
            if not db.execute("SELECT 1 FROM artifact WHERE id=? AND published IS NOT NULL", (art,)).fetchone():
                sys.exit("not published: " + art)
            st = step_of(db, art)
            try: ph = plan_hash(fill(root, n, st[0], st[1])) if st else None
            except SystemExit: ph = None
            rq.run_log(root, n, {"event": "keep", "artifact": art, "reason": o["reason"],
                                 "inputs": current_inputs(root, db, art), "plan": ph, "facts": relevant_facts(db, art)})
            print("kept: " + art)
    elif cmd == "rerun":
        rerun(root, n, o.get("fact"), o.get("artifact"), o.get("stand_in", False), o.get("plan") is True, o.get("json", False), o.get("expect"),
              o.get("step"))
    elif cmd == "history" and o.get("json") and len(rest) > 1:
        print(json.dumps(versions(root, n, rest[1]), indent=1, ensure_ascii=False))
    elif cmd == "history":
        name = rest[1] if len(rest) > 1 else None
        for ev in events(root, n):
            if not name or name in json.dumps(ev, ensure_ascii=False):
                print("%s  %s  %s" % (ev["at"], ev.get("event"), json.dumps({k: v for k, v in ev.items() if k not in ("at", "event")}, ensure_ascii=False)[:240]))
        rel = os.path.relpath(os.path.join(folder(root, n), "canon.sql"), root)
        print(rq.keyless(["git", "log", "--format=%ci  commit %h  %s", "--", rel], cwd=root, capture_output=True, text=True).stdout.rstrip())
    elif cmd == "mark":
        rq.run_log(root, n, {"event": "mark", "label": rest[1]}); print("marked: " + rest[1])
    elif cmd == "render": render(root, n)
    elif cmd == "deliver": deliver(root, n, rest[1])
    else: print(__doc__)
