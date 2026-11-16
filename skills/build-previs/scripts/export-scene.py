#!/usr/bin/env python3
"""Export a place's pre-vis builder as its scene file: one glTF 2.0 binary (.glb) holding every object the builder
makes, named as the builder names it, its cameras, its front door's swing, and its looks as data. No model, no
render: it reads the builder, and changes nothing.

Usage:
  export-scene.py <builder.py | git:<commit>:<path>> <out.glb> [--canon <pipeline/NNN/canon.sql>]
                  [--reference <camera>=<file>[@grey|coded|simple]]...
                                            --reference names a render this builder made from that camera, the
                                            camera's reference_file; only renders this builder made are named, since
                                            another builder's geometry differs. canon names each camera's published
                                            pre-vis artifact either way. @look says which look the render was drawn
                                            in, as the command that made it did (--simple: simple; a labelled render:
                                            coded); without it, from the file's name: "simple" or "labelled", or grey
  export-scene.py --missing                 the builders in prompts/resources/ that have no scene file yet

Run it inside the project, and file what it makes with request.py build, so its record names the builder:
  request.py build "python3 <this> <builder> <tmp>/scene.glb --canon pipeline/002/canon.sql" <tmp>/scene.glb \\
      --name <place>-scene-<builder time> --from <builder>

How it reads a builder, so nothing is rendered and nothing is written but the scene file:
- the builder's source runs, in a Python process of its own, only up to its render marker,
  "# ---------- render ----------", which makes its objects, KINDS, and set_door;
- from the rest of the source, only the top-level function definitions and the CAMERAS, LIGHT, SIMPLE, and SIMPLE_KEEP
  assignments run, found by parsing the source, never retyped; every loop, if-block, and save is skipped;
- each object's label is its group, from the builder's own `key = ...` rule, taken the same way from its contents
  loop, or from render() in a builder that has none;
- the shading constants and edge colours are read from the source's own lines.
The door's swing is sampled from the builder's own set_door, at 24 frames a second over 192 frames, stepped, at
round(75·(1−(1−u)³), 1) degrees, u = clamp((t − 3.0)/0.8, 0, 1), as Last order's canon gives it: opening at 3.0 s, at
the bell, easing open over 0.8 s, to 75 degrees outward. A builder without set_door gets a door that does not move.
"""
import ast, json, math, os, re, struct, subprocess, sys

MARKER = "# ---------- render ----------"
KEEP_NAMES = ("CAMERAS", "LIGHT", "SIMPLE", "SIMPLE_KEEP")
FPS, FRAMES, OPENS_AT, OPENS_OVER, OPEN_ANGLE = 24, 192, 3.0, 0.8, 75.0


def project_root():
    p = os.path.abspath(".")
    while p != "/":
        if os.path.isdir(os.path.join(p, "library")) and os.path.isdir(os.path.join(p, "requests")): return p
        p = os.path.dirname(p)
    sys.exit("not inside a project: no folder above holds both library/ and requests/")


def read_source(root, name):
    if name.startswith("git:"):
        _, commit, path = name.split(":", 2)
        r = subprocess.run(["git", "show", "%s:%s" % (commit, path)], cwd=root, capture_output=True, text=True)
        if r.returncode: sys.exit("no %s at %s" % (path, commit))
        return r.stdout
    return open(name if os.path.isabs(name) else os.path.join(root, name)).read()


def pieces(src):
    """The builder's source up to its render marker, and, from the rest, its definitions and its grouping rule."""
    if MARKER not in src: sys.exit("the builder has no render marker, %r: it cannot be read without running it" % MARKER)
    head, rest = src.split(MARKER, 1)
    tree = ast.parse(rest)
    defs = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            defs.append(ast.get_source_segment(rest, node))
        elif isinstance(node, ast.Assign) and all(isinstance(t, ast.Name) and t.id in KEEP_NAMES for t in node.targets):
            defs.append(ast.get_source_segment(rest, node))
    # the grouping: `first = ...` and `key = ...` in the loop over the objects, its variable named oname or name
    rules = []
    for loop in ast.walk(ast.parse(src)):
        if isinstance(loop, ast.For) and isinstance(loop.target, ast.Tuple) and len(loop.target.elts) == 4:
            var = loop.target.elts[1].id if isinstance(loop.target.elts[1], ast.Name) else None
            body = [s for s in loop.body if isinstance(s, ast.Assign) and isinstance(s.targets[0], ast.Name)
                    and s.targets[0].id in ("first", "key")]
            if var and any(s.targets[0].id == "key" for s in body):
                rules.append((var, [ast.get_source_segment(src, s) for s in body]))
    rule = next((r for r in rules if r[0] == "oname"), rules[0] if rules else None)
    # the groups the builder leaves unlabelled: `if key in (...): continue` where it labels its images
    skipped = []
    for node in ast.walk(ast.parse(src)):
        if (isinstance(node, ast.If) and isinstance(node.test, ast.Compare) and isinstance(node.test.left, ast.Name)
                and node.test.left.id == "key" and isinstance(node.test.ops[0], ast.In)
                and any(isinstance(s, ast.Continue) for s in node.body)):
            skipped = list(ast.literal_eval(node.test.comparators[0]))
    # the words the published images show for each group: the builder's label map, {key: words}.get(key, key)
    words = {}
    for node in ast.walk(ast.parse(src)):
        if (isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) and node.targets[0].id == "label"
                and isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Attribute)
                and node.value.func.attr == "get" and isinstance(node.value.func.value, ast.Dict)):
            words = ast.literal_eval(node.value.func.value)
    shade = re.search(r"([0-9.]+)\s*\+\s*([0-9.]+)\s*\*\s*abs\(dot\(n,\s*LIGHT\)\)", src)
    edge = re.search(r"cols\[edge\]\s*=\s*(.+)", src)
    # the edge colour of the grey and colour-coded looks: the line's last colour, after any "if SIMPLE else"
    tuples = re.findall(r"\((\d+),\s*(\d+),\s*(\d+)\)", edge.group(1)) if edge else []
    simple_edge = int(tuples[0][0]) if len(tuples) > 1 and "SIMPLE" in edge.group(1) else None
    bg = re.search(r"cols\s*=\s*np\.full\(\(IH,\s*IW,\s*3\),\s*(\d+)", src)   # the image the faces are drawn onto
    return head, "\n\n".join(defs), rule, {"shading": [float(shade.group(1)), float(shade.group(2))] if shade else None,
                                         "edge": int(tuples[-1][0]) if tuples else None, "simple_edge": simple_edge,
                                         "background": int(bg.group(1)) if bg else None, "unlabelled": skipped,
                                         "words": words}


DRIVER = r'''
import sys, json, math, os
ns = {"__name__": "previs", "__file__": "builder.py"}
head, defs, rule = json.load(sys.stdin)
sys.argv = ["builder.py", os.environ["SCENE_TMP"]]
exec(compile(head, "builder.py", "exec"), ns)
exec(compile(defs, "builder.py", "exec"), ns)
objs = ns["objs"]
def label(name):
    if not rule: return None
    var, stmts = rule
    local = {var: name}
    for s in stmts: exec(s, ns, local)
    return local.get("key")
keep = ns.get("SIMPLE_KEEP")
out = {"size": [ns.get("IW"), ns.get("IH")], "kinds": {k: [list(v[0]), v[1]] for k, v in ns["KINDS"].items()},
       "light": list(ns["LIGHT"]) if "LIGHT" in ns else None,
       "cameras": [[c[0], list(c[1]), list(c[2]), c[3]] for c in ns.get("CAMERAS", [])],
       "objects": [{"id": o[0], "name": o[1], "kind": o[2], "polys": [[list(p) for p in poly] for poly in o[3]],
                    "label": label(o[1])} for o in objs],
       "simple_keep": [o[1] for o in objs if keep(o[1], o[2])] if keep else None}
if "set_door" in ns and "DOOR_LEAF" in ns:
    leaf = list(range(ns["DOOR_LEAF"], ns["DOOR_LEAF"] + len(ns["DOOR_CLOSED"])))
    closed = [list(objs[i][3][0][0]) for i in leaf]
    ns["set_door"](90.0)
    turned = [list(objs[i][3][0][0]) for i in leaf]
    ns["set_door"](0.0)
    # the hinge: the centre the closed points turn about, from one point and its quarter turn
    (x0, y0), (x1, y1) = closed[0][:2], turned[0][:2]
    cx, cy = (x0 + x1 - (y1 - y0)) / 2.0, (y0 + y1 + (x1 - x0)) / 2.0
    out["door"] = {"leaf": [objs[i][1] for i in leaf], "hinge": [cx, cy], "frames": [
        round(75.0 * (1 - (1 - min(max((i / 24.0 - 3.0) / 0.8, 0.0), 1.0)) ** 3), 1) for i in range(192)]}
print(json.dumps(out))
'''


def read_builder(root, name):
    head, defs, rule, consts = pieces(read_source(root, name))
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:   # the builder's OUT points here; nothing is written to it
        r = subprocess.run([sys.executable, "-I", "-c", DRIVER], input=json.dumps([head, defs, rule]), capture_output=True,
                           text=True, cwd=tmp, env=dict(os.environ, SCENE_TMP=tmp), timeout=300)
        if r.returncode: sys.exit("reading the builder failed:\n" + r.stderr[-2000:])
        if os.listdir(tmp): sys.exit("refused: the builder wrote files before its render marker: " + ", ".join(os.listdir(tmp)))
    d = json.loads(r.stdout)
    d["constants"] = consts
    return d


# ---- glTF ---------------------------------------------------------------------------------------

def norm(v):
    l = math.sqrt(sum(x * x for x in v)) or 1.0
    return [x / l for x in v]


def cross(a, b):
    return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]


def quat_from_basis(x, y, z):
    """A rotation quaternion (x, y, z, w) from the columns of a rotation matrix."""
    m00, m01, m02 = x[0], y[0], z[0]
    m10, m11, m12 = x[1], y[1], z[1]
    m20, m21, m22 = x[2], y[2], z[2]
    tr = m00 + m11 + m22
    if tr > 0:
        s = math.sqrt(tr + 1.0) * 2; return [(m21 - m12) / s, (m02 - m20) / s, (m10 - m01) / s, 0.25 * s]
    if m00 > m11 and m00 > m22:
        s = math.sqrt(1.0 + m00 - m11 - m22) * 2; return [0.25 * s, (m01 + m10) / s, (m02 + m20) / s, (m21 - m12) / s]
    if m11 > m22:
        s = math.sqrt(1.0 + m11 - m00 - m22) * 2; return [(m01 + m10) / s, 0.25 * s, (m12 + m21) / s, (m02 - m20) / s]
    s = math.sqrt(1.0 + m22 - m00 - m11) * 2; return [(m02 + m20) / s, (m12 + m21) / s, 0.25 * s, (m10 - m01) / s]


class Glb:
    def __init__(self):
        self.bin = bytearray(); self.views = []; self.accessors = []

    def add(self, fmt, values, comp, typ, count, target=None, minmax=None):
        while len(self.bin) % 4: self.bin.append(0)
        off = len(self.bin); data = struct.pack("<%d%s" % (len(values), fmt), *values); self.bin += data
        view = {"buffer": 0, "byteOffset": off, "byteLength": len(data)}
        if target: view["target"] = target
        self.views.append(view)
        acc = {"bufferView": len(self.views) - 1, "componentType": comp, "count": count, "type": typ}
        if minmax: acc["min"], acc["max"] = minmax
        self.accessors.append(acc)
        return len(self.accessors) - 1


def scene_of(d, name, sha, canon_refs, made=None):
    made = made or {}
    g = Glb()
    nodes, meshes, materials, matidx = [], [], [], {}
    for k, (rgb, grey) in d["kinds"].items():
        matidx[k] = len(materials)
        materials.append({"name": k, "pbrMetallicRoughness": {"baseColorFactor": [grey / 255.0] * 3 + [1.0],
                          "metallicFactor": 0.0, "roughnessFactor": 1.0}, "extras": {"kind": k, "coded": rgb, "grey": grey}})
    door = d.get("door")
    leaf = set(door["leaf"]) if door else set()
    hx, hy = door["hinge"] if door else (0.0, 0.0)
    children, leaf_nodes = [], []
    for o in d["objects"]:
        pos, nor = [], []
        sub = (hx, hy, 0.0) if o["name"] in leaf else (0.0, 0.0, 0.0)
        for poly in o["polys"]:
            if len(poly) < 3: continue
            n = norm(cross([poly[1][i] - poly[0][i] for i in range(3)], [poly[2][i] - poly[0][i] for i in range(3)]))
            for i in range(1, len(poly) - 1):   # a fan: every builder face is flat and convex
                for p in (poly[0], poly[i], poly[i + 1]):
                    pos += [p[0] - sub[0], p[1] - sub[1], p[2] - sub[2]]; nor += n
        if not pos: continue
        cnt = len(pos) // 3
        mn = [min(pos[i::3]) for i in range(3)]; mx = [max(pos[i::3]) for i in range(3)]
        pa = g.add("f", pos, 5126, "VEC3", cnt, 34962, (mn, mx)); na = g.add("f", nor, 5126, "VEC3", cnt, 34962)
        meshes.append({"name": o["name"], "primitives": [{"attributes": {"POSITION": pa, "NORMAL": na}, "material": matidx[o["kind"]]}]})
        nodes.append({"name": o["name"], "mesh": len(meshes) - 1,
                      "extras": {"kind": o["kind"], "label": o["label"],
                                 "label_text": d["constants"]["words"].get(o["label"], o["label"]) if o["label"] else None,
                                 "named": bool(o["label"]) and o["label"] not in d["constants"]["unlabelled"],
                                 "builder_id": o["id"]}})
        (leaf_nodes if o["name"] in leaf else children).append(len(nodes) - 1)
    animations = []
    if door:
        nodes.append({"name": "front door hinge", "translation": [hx, hy, 0.0], "children": leaf_nodes,
                      "extras": {"hinge": [hx, hy], "opens": "outward", "angles": "degrees, sampled from the builder's set_door"}})
        hinge = len(nodes) - 1; children.append(hinge)
        times = [i / float(FPS) for i in range(FRAMES)]
        rots = []
        for a in door["frames"]:
            r = math.radians(a); rots += [0.0, 0.0, math.sin(r / 2), math.cos(r / 2)]
        ta = g.add("f", times, 5126, "SCALAR", FRAMES, None, ([0.0], [times[-1]]))
        ra = g.add("f", rots, 5126, "VEC4", FRAMES)
        animations.append({"name": "door swing", "samplers": [{"input": ta, "output": ra, "interpolation": "STEP"}],
                           "channels": [{"sampler": 0, "target": {"node": hinge, "path": "rotation"}}],
                           "extras": {"fps": FPS, "frames": FRAMES, "opens_at": OPENS_AT, "opens_over": OPENS_OVER,
                                      "angle": OPEN_ANGLE, "rule": "round(75*(1-(1-u)^3), 1), u = clamp((t-3.0)/0.8, 0, 1)"}})
    cameras = []
    iw, ih = d["size"]
    for cname, cam, target, hfov in d["cameras"]:
        f = norm([target[i] - cam[i] for i in range(3)]); r = norm(cross(f, [0, 0, 1])); u = cross(r, f)
        yfov = 2 * math.atan(math.tan(math.radians(hfov) / 2) * ih / iw)
        cameras.append({"name": cname, "type": "perspective", "perspective": {"aspectRatio": iw / ih, "yfov": yfov, "znear": 0.05, "zfar": 200.0}})
        ref = canon_refs.get(cname)
        nodes.append({"name": cname, "camera": len(cameras) - 1, "translation": cam, "rotation": quat_from_basis(r, u, [-x for x in f]),
                      "extras": {"position": cam, "target": target, "hfov": hfov, "image_size": [iw, ih],
                                 "canon": ref[0] if ref else None, "reference_file": (made.get(cname) or (None, None))[0],
                                 "reference_look": (made.get(cname) or (None, None))[1]}})
        children.append(len(nodes) - 1)
    c = d["constants"]
    looks = {"background": c["background"],
             "grey": {k: v[1] for k, v in d["kinds"].items()}, "coded": {k: v[0] for k, v in d["kinds"].items()},
             "shading": {"ambient": c["shading"][0], "diffuse": c["shading"][1], "light": d["light"]} if c["shading"] else None,
             "edges": dict({"rule": "a 1-pixel edge where the object under the pixel changes", "grey": c["edge"], "coded": c["edge"]},
                           **({"simple": c["simple_edge"]} if c["simple_edge"] is not None and d["simple_keep"] is not None else {})),
             "simple": ({"kept": d["simple_keep"], "face": 255, "night": 40, "edge": 170} if d["simple_keep"] is not None
                        else None)}
    root = {"name": "z up to y up", "rotation": [-math.sqrt(0.5), 0.0, 0.0, math.sqrt(0.5)], "children": children,
            "extras": {"source_up": "z"}}
    nodes.append(root)
    gl = {"asset": {"version": "2.0", "generator": "Spumcake-Skills build-previs export-scene.py"},
          "scene": 0, "scenes": [{"name": name, "nodes": [len(nodes) - 1],
                                  "extras": {"builder": name, "builder_sha256": sha, "looks": looks, "image_size": [iw, ih],
                                             "door": ("swings, see the animation \"door swing\"" if door
                                                      else "this builder has no set_door, so the door does not move")}}],
          "nodes": nodes, "meshes": meshes, "materials": materials, "cameras": cameras,
          "buffers": [{"byteLength": len(g.bin)}], "bufferViews": g.views, "accessors": g.accessors}
    if animations: gl["animations"] = animations
    js = json.dumps(gl, separators=(",", ":")).encode()
    js += b" " * (-len(js) % 4)
    bn = bytes(g.bin) + b"\0" * (-len(g.bin) % 4)
    return (struct.pack("<III", 0x46546C67, 2, 12 + 8 + len(js) + 8 + len(bn)) + struct.pack("<II", len(js), 0x4E4F534A) + js
            + struct.pack("<II", len(bn), 0x004E4942) + bn)


def canon_references(root, canon):
    """For each camera, the published pre-vis render named for it in the pipeline's table, if any."""
    if not canon: return {}
    import sqlite3
    db = sqlite3.connect(":memory:"); db.executescript(open(os.path.join(root, canon)).read())
    refs = {}
    for aid, f in db.execute("SELECT id, file FROM artifact WHERE published IS NOT NULL AND file LIKE '%previs-%-grey.png'"):
        m = re.search(r"previs-(.+)-grey\.png$", f)
        if m: refs.setdefault(m.group(1), (aid, f))
    return refs


def missing(root):
    res = os.path.join(root, "prompts", "resources")
    lines = [json.loads(l) for l in open(os.path.join(res, "records.jsonl")) if l.strip()] \
        if os.path.exists(os.path.join(res, "records.jsonl")) else []
    done = {i["file"] for l in lines if l.get("file", "").endswith(".glb") for i in l.get("inputs", [])}
    for f in sorted(os.listdir(res)):
        if "build-previs" in f and f.endswith(".py") and "prompts/resources/" + f not in done:
            print("prompts/resources/" + f)


if __name__ == "__main__":
    a = sys.argv[1:]
    root = project_root()
    if a and a[0] == "--missing": missing(root); sys.exit()
    if len(a) < 2: print(__doc__); sys.exit(1)
    canon = a[a.index("--canon") + 1] if "--canon" in a else None
    import hashlib
    src = read_source(root, a[0])
    d = read_builder(root, a[0])
    made = {}
    for i, x in enumerate(a):
        if x == "--reference":
            cam, f = a[i + 1].split("=", 1)
            f, _, look = f.partition("@")
            if not os.path.exists(os.path.join(root, f)): sys.exit("no such render: " + f)
            look = look or ("simple" if "simple" in f else "coded" if "labelled" in f else "grey")
            if look not in ("grey", "coded", "simple"): sys.exit("a reference's look is grey, coded, or simple: " + look)
            made[cam] = (f, look)
    out = scene_of(d, a[0], hashlib.sha256(src.encode()).hexdigest(), canon_references(root, canon), made)
    open(a[1], "wb").write(out)
    print("%s: %d objects, %d cameras%s" % (a[1], len(d["objects"]), len(d["cameras"]), ", the door swings" if d.get("door") else ""))
