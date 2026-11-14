#!/usr/bin/env python3
"""A pipeline's published canon: pipeline/<n>/canon.sql, its chain pages, and what a change touches. See docs/projects.md.

Usage:
  pipeline.py new <n>                         start pipeline <n> as a copy of the one before it, or empty
  pipeline.py sql <n> "<query>"               query the table
  pipeline.py element <n> <name> --kind K     add a canonical element: a place, character, prop, look, story, sound
  pipeline.py publish <n> "<element>: <role>" --file library/<file> --request <id> --chain <chain>
                     [--from "<element>: <role>" ROLE]... [--note TEXT] [--waiting]
                                              publish an approved result as canon; with --waiting, record a result
                                              that waits for the user, which is not canon
  pipeline.py fact <n> "<element>: <fact>" <value> --artifact "<element>: <role>"
                                              set a canonical fact and the artifact that settles it
  pipeline.py content <n> "<element>: <role>" <json | @file>
                                              what a published image shows: [{"name", "camera", "where", "frame_box",
                                              "state", "mark", "looks_at"}], each thing by its canonical name
  pipeline.py chain <n> <name> --order NN [--title TEXT]
  pipeline.py step <n> <chain> <step> --order N --skill S --endpoint JSON --template TEXT|@file
                     [--refs JSON|@file] [--script TEXT] [--request <id>] [--artifact "<element>: <role>"] [--deliver]
                                              record a step: its prompt as a template naming canon, {{<element>: <fact>}},
                                              its references by canonical artifact, the request that last ran it, and
                                              the artifact it published, if approved
  pipeline.py fill <n> <chain> <step> [--name NAME]
                                              a request spec for the step, filled from this pipeline's table
  pipeline.py touches <n> (--fact "<element>: <fact>" | --artifact "<element>: <role>")
                                              every published artifact and every step a change touches, in order
  pipeline.py rerun <n> --fact "<element>: <fact>" [--stand-in] [--next]
                                              run again, in order, each step the change touches, filled from <n>'s table;
                                              --next runs only the first, for the user's approval before the rest
  pipeline.py render <n>                      write the chain pages from the table
  pipeline.py deliver <n> <library file>      file a finished deliverable into output/
"""
import sys, os, re, json, sqlite3, shutil, html, subprocess, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import request as rq

SCHEMA = """
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


def save(root, n, db):
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
    read, missing = [], []

    def value(m):
        e, f = m.group(1).strip(), m.group(2).strip()
        v = db.execute("SELECT value FROM fact WHERE element=? AND name=?", (e, f)).fetchone()
        if not v: missing.append("%s: %s" % (e, f)); return m.group(0)
        read.append({"name": "%s: %s" % (e, f), "value": v[0], "read_at": now(),
                     "from": "pipeline/%03d/canon.sql" % int(n)})
        return v[0]

    prompt = PLACE.sub(value, template or "")
    command = PLACE.sub(value, script) if script else None
    references = []
    for ref in json.loads(refs or "[]"):
        if ref.get("file"):
            references.append({"file": ref["file"], "role": ref.get("role", ""), "canon": None,
                               "note": "a fixed input, not canon"})
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
            if s in arts and reaches(s, a): arts.add(a)
        for c, s, refs, a in db.execute("SELECT chain, name, refs, artifact FROM step").fetchall():
            if a and a in arts: steps.add((c, s))
            elif not a and any(r.get("artifact") in arts for r in json.loads(refs or "[]")): steps.add((c, s))
            if (c, s) in steps and a: arts.add(a)
        if len(arts) + len(steps) == size: break
    order = {c: o for c, o in db.execute("SELECT name, ord FROM chain")}
    sord = {(c, s): o for c, s, o in db.execute("SELECT chain, name, ord FROM step")}
    return (sorted(arts), sorted(steps, key=lambda cs: (order.get(cs[0], 99), sord.get(cs, 99))))


def rerun(root, n, fact, stand=False, only_next=False):
    _, steps = touches(root, n, fact=fact)
    if not steps: print("nothing to run again"); return
    import tempfile
    for chain, step in steps:
        spec = fill(root, n, chain, step)
        kind = spec["endpoint"].get("kind")
        if kind in ("script", "agent"):
            db = load(root, n)
            art, skill = db.execute("SELECT artifact, skill FROM step WHERE chain=? AND name=?", (chain, step)).fetchone()
            if not stand and (kind == "agent" or not spec.get("scripts")):
                sys.exit("%s is the agent's own work, not a request: make it again with %s, publish it, then run again"
                         % (step, skill))
            tmp = os.path.join(root, ".stand-in")
            os.makedirs(tmp, exist_ok=True)
            try:
                if stand:
                    made = rq.stand_in(spec, tmp)[0]
                else:
                    cmd = spec["scripts"][0]["command"]
                    p = subprocess.run(cmd, shell=True, cwd=root, capture_output=True, text=True)
                    if p.returncode: sys.exit(p.stdout + p.stderr)
                    made = [os.path.join(root, o) for o in spec.get("outputs", [])]
                os.makedirs(os.path.join(root, "prompts", "resources"), exist_ok=True)
                filed = rq.file_into(root, "prompts/resources", "%s-%s" % (rq.stamp(), rq.slug(spec["name"])), made)
            finally:
                shutil.rmtree(tmp, ignore_errors=True)
            print("%s: %s" % (step, ", ".join(filed)))
            if art:
                db.execute("UPDATE artifact SET file=?, request=NULL, published=?, note=? WHERE id=?",
                           (filed[0], now() if stand else None, "stand-in, a dry run" if stand else "waiting for the user", art))
                save(root, n, db)
            if only_next: print("stopped after one step, for the user's approval"); return
            continue
        spec["asked"] = "Run %s again in pipeline %03d" % (step, int(n))
        spec["why"] = "The brief changed %s; this step uses it, directly or through what it is made from." % fact
        with tempfile.NamedTemporaryFile("w", suffix=".json", dir=root, delete=False) as f:
            json.dump(spec, f); spec_file = f.name
        try:
            out = subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), "request.py"), "run", spec_file]
                                 + (["--stand-in"] if stand else []), cwd=root, capture_output=True, text=True)
        finally:
            os.unlink(spec_file)
        if out.returncode: sys.exit(out.stdout + out.stderr)
        report = out.stdout.strip()
        data = rq.read_data(os.path.join(root, report))
        print("%s: %s" % (step, report))
        db = load(root, n)
        a = db.execute("SELECT artifact, deliver FROM step WHERE chain=? AND name=?", (chain, step)).fetchone()
        db.execute("UPDATE step SET request=? WHERE chain=? AND name=?", (data["id"], chain, step))
        if stand and a and a[0]:
            db.execute("UPDATE artifact SET file=?, request=?, published=?, note=? WHERE id=?",
                       (data["outputs"][0], data["id"], now(), "stand-in, a dry run", a[0]))
        save(root, n, db)
        if stand and a and a[1]: deliver(root, n, data["outputs"][0])
        if only_next: print("stopped after one step, for the user's approval"); return


def deliver(root, n, f):
    ext = os.path.splitext(f)[1]
    dst = os.path.join(root, "output", "%s-%03d-%s%s" % (rq.stamp(), int(n), os.path.basename(root), ext))
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if os.path.exists(dst): sys.exit("refusing to overwrite " + dst)
    shutil.copyfile(os.path.join(root, f), dst)
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
            if k in ("stand_in", "next", "deliver", "waiting"): o[k] = True; i += 1
            elif k == "from": o["from"].append((a[i + 1], a[i + 2])); i += 3
            else: o[k] = a[i + 1]; i += 2
        else: rest.append(a[i]); i += 1
    return o, rest


def text(v):
    return open(v[1:]).read() if v and v.startswith("@") else v


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"): print(__doc__); sys.exit()
    cmd = sys.argv[1]
    o, rest = opts(sys.argv[2:])
    root = rq.project_root()
    n = rest[0] if rest else None
    if cmd == "new": new(root, n)
    elif cmd == "sql":
        db = load(root, n)
        for row in db.execute(rest[1]): print(" | ".join("" if x is None else str(x) for x in row))
        if not rest[1].lstrip().upper().startswith("SELECT"): save(root, n, db)
    elif cmd == "element":
        db = load(root, n); db.execute("INSERT OR REPLACE INTO element VALUES (?,?,?)", (rest[1], o.get("kind"), o.get("note")))
        save(root, n, db)
    elif cmd == "publish":
        db = load(root, n); e, role = split(rest[1])
        if not os.path.exists(os.path.join(root, o["file"])): sys.exit("not found: " + o["file"])
        db.execute("INSERT OR REPLACE INTO artifact VALUES (?,?,?,?,?,?,?,?)",
                   (rest[1], e, role, o["file"], o.get("request"), o.get("chain"),
                    None if o.get("waiting") else (o.get("published") or now()), o.get("note")))
        db.execute("DELETE FROM made_from WHERE artifact=?", (rest[1],))
        for s, r in o["from"]: db.execute("INSERT INTO made_from VALUES (?,?,?)", (rest[1], s, r))
        save(root, n, db)
    elif cmd == "fact":
        db = load(root, n); e, f = split(rest[1])
        db.execute("INSERT OR REPLACE INTO fact VALUES (?,?,?,?)", (e, f, rest[2], o.get("artifact")))
        save(root, n, db)
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
        db.execute("INSERT OR REPLACE INTO step VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                   (rest[1], int(o["order"]), rest[2], o.get("skill"), o.get("endpoint"), text(o.get("template")),
                    text(o.get("refs")), o.get("script"), o.get("request"), o.get("artifact"), 1 if o.get("deliver") else 0))
        save(root, n, db)
    elif cmd == "fill": print(json.dumps(fill(root, n, rest[1], rest[2], o.get("name")), indent=1))
    elif cmd == "touches":
        arts, steps = touches(root, n, o.get("fact"), o.get("artifact"))
        print("Published artifacts:"); [print("  " + a) for a in arts]
        print("Steps, in order:"); [print("  %s / %s" % s) for s in steps]
    elif cmd == "rerun": rerun(root, n, o["fact"], o.get("stand_in", False), o.get("next", False))
    elif cmd == "render": render(root, n)
    elif cmd == "deliver": deliver(root, n, rest[1])
    else: print(__doc__)
