#!/usr/bin/env python3
"""Render a place from its scene file with the released spumcake-render program, and write what is in the frame.
No model, no cost: the same scene, camera, look, size, and time make the same picture.

Usage:
  render-scene.py <scene.glb> <out.png> --camera <name> --look grey|coded|simple [--size <w>x<h>] [--time <seconds>]

It writes:
- <out.png>, the picture spumcake-render makes, with its record inside it, as `request.py record` reads it;
- <out.png>.record.json, the same record: the camera, what made it (spumcake-render's version, the scene file and
  its sha256, the settings), and `contents`, each group of objects in the frame, by the scene's own label, with its
  box as fractions of the frame and whether it lies left, centre, or right.

The size is the camera's own image size unless --size gives one; --time is seconds into the scene's animation, such
as the front door's swing. Run it inside the project through request.py build, naming the scene file as its input:
  request.py build "python3 <render-scene.py> <scene.glb> <out.png> --camera <c> --look grey" <out.png> \\
      <out.png>.record.json --name <place>-<camera>-<look> --from <scene.glb>

It needs spumcake-render at the release docs/setup.md names, and a graphics device; it stops before writing
anything, saying which is missing, when either is.
"""
import sys, os, json, struct, argparse, subprocess, tempfile, hashlib, datetime, shutil

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "scripts"))
import request as rq

PROGRAM = "spumcake-render"
RELEASE = (0, 1, 0)          # the release docs/setup.md names; an older program is refused
NO_DEVICE = 3                # spumcake-render's exit code when it finds no graphics device, agreed with its makers
SETUP = "docs/setup.md's Prerequisites"


def scene_json(path):
    """The glTF JSON chunk of a .glb: the nodes with their names and extras, and the scene's extras."""
    b = open(path, "rb").read()
    if b[:4] != b"glTF": sys.exit("not a glTF binary: " + path)
    n, kind = struct.unpack("<II", b[12:20])
    if kind != 0x4E4F534A: sys.exit("no JSON chunk in " + path)
    return json.loads(b[20:20 + n])


def version():
    exe = shutil.which(PROGRAM)
    if not exe: sys.exit("%s is not installed: install it as %s says, then run %s --version" % (PROGRAM, SETUP, PROGRAM))
    out = subprocess.run([exe, "--version"], capture_output=True, text=True).stdout.strip()   # "spumcake-render 0.1.0"
    try:
        v = tuple(int(x) for x in out.split()[-1].split("."))
    except (ValueError, IndexError):
        sys.exit("%s --version printed %r, not a version: install the release %s names" % (PROGRAM, out, SETUP))
    if v < RELEASE:
        sys.exit("%s is %s, older than the release %s names (%s): install it again as it says"
                 % (PROGRAM, out, SETUP, ".".join(map(str, RELEASE))))
    return exe, out


def contents(objects, names, labels, w, h):
    """Each group in the frame, as the pre-vis builders recorded it (Last order's 2026-11-14_19-56 builder, lines 303
    to 314): a group of under 40 pixels is left out, its box is rounded to 3 places, and its box's centre puts it left
    below 0.36 and right above 0.64. A group is the scene's own label for its objects, and nothing else."""
    import numpy as np
    group_of = {}
    for i, name in names.items():
        if name is not None: group_of[int(i)] = labels.get(name, name)
    out = []
    for g in sorted(set(group_of.values())):
        mask = np.isin(objects, [i for i, x in group_of.items() if x == g])
        if mask.sum() < 40: continue
        yy, xx = np.nonzero(mask)
        x0, x1, y0, y1 = xx.min() / w, xx.max() / w, yy.min() / h, yy.max() / h
        cx = (x0 + x1) / 2
        out.append({"name": g, "frame_box": [round(x0, 3), round(y0, 3), round(x1, 3), round(y1, 3)],
                    "where": ("left" if cx < 0.36 else "right" if cx > 0.64 else "centre") + " of the frame"})
    return sorted(out, key=lambda c: c["frame_box"][0])


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0], formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("scene"); p.add_argument("out")
    p.add_argument("--camera", required=True); p.add_argument("--look", required=True, choices=("grey", "coded", "simple"))
    p.add_argument("--size"); p.add_argument("--time", type=float, default=0.0)
    o = p.parse_args()
    from PIL import Image
    import numpy as np
    j = scene_json(o.scene)
    cams = {n["name"]: n.get("extras") or {} for n in j["nodes"] if "camera" in n}
    if o.camera not in cams: sys.exit("no camera %s in %s: it has %s" % (o.camera, o.scene, ", ".join(sorted(cams))))
    if o.size:
        try: w, h = (int(x) for x in o.size.lower().split("x"))
        except ValueError: sys.exit("give the size as <width>x<height>: " + o.size)
    else:
        w, h = cams[o.camera].get("image_size") or (j.get("scenes") or [{}])[0].get("extras", {}).get("image_size") or (None, None)
        if not w: sys.exit("the scene gives camera %s no image size: give --size" % o.camera)
    labels = {n["name"]: (n.get("extras") or {}).get("label") or n["name"] for n in j["nodes"] if (n.get("extras") or {}).get("kind")}
    exe, ver = version()
    with tempfile.TemporaryDirectory() as d:
        pic, objs = os.path.join(d, "picture.png"), os.path.join(d, "objects.png")
        cmd = [exe, "render", o.scene, "--camera", o.camera, "--look", o.look, "--size", "%dx%d" % (w, h),
               "--time", "%g" % o.time, "--out", pic, "--objects", objs]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode == NO_DEVICE:
            sys.exit("%s found no graphics device: install Mesa's lavapipe and set SPUMCAKE_RENDER_ADAPTER=software, as %s "
                     "says (%s)" % (PROGRAM, SETUP, r.stderr.strip()))
        if r.returncode: sys.exit("%s failed (exit %d): %s" % (PROGRAM, r.returncode, r.stderr.strip()))
        objects = np.array(Image.open(objs)).astype(np.int64)
        names = json.load(open(objs + ".json"))
        record = {"record": 1, "file": o.out, "kind": "pre-vis render",
                  "date": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                  "made_by": {"tool": ver, "scene": {"file": o.scene, "sha256": hashlib.sha256(open(o.scene, "rb").read()).hexdigest()},
                              "settings": {"camera": o.camera, "look": o.look, "size": [w, h], "time": o.time},
                              "cost": "nothing; local"},
                  "camera": o.camera, "contents": contents(objects, names, labels, w, h)}
        rq.embed_record(pic, record, disclosure=False)
        os.makedirs(os.path.dirname(os.path.abspath(o.out)), exist_ok=True)
        shutil.copyfile(pic, o.out)
    with open(o.out + ".record.json", "w") as fh: json.dump(record, fh, indent=1, ensure_ascii=False); fh.write("\n")
    print(o.out)


if __name__ == "__main__":
    main()
