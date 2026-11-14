#!/usr/bin/env python3
"""Draw one moment's staging floor plan from above: the place from its pre-vis geometry, the shot's camera with the edges
of its frame, and each character's mark, which way they face, and what they look at. It is drawn before any frame
of the moment is made, so the frame is checked against it.

Usage:
  staging-floor-plan.py --geometry <place geometry.json> --camera <camera> --moment <moment> --out <png>
                  [--title TEXT]
                  [--character NAME --at "x, y" --faces <thing> --looks-at <thing> [--note TEXT]]...

A <thing> is a camera's name, an object's name in the geometry, such as "the front door", or "down: <what>"
for a look at something below the eye, such as "down: the counter top". The geometry is what the place's
pre-vis builder exports: {"room": {"width", "depth", "walls": {name: side}}, "objects": [{"name", "kind",
"footprint": [[x, y], ...]}], "cameras": [{"name", "position", "target", "hfov"}], "colours": {kind: [r, g, b]}}.
"""
import sys, json, math
from PIL import Image, ImageDraw, ImageFont

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def args(a):
    o, chars, i = {}, [], 0
    while i < len(a):
        k = a[i][2:]
        if k == "character": chars.append({"name": a[i + 1]}); i += 2; continue
        if chars and k in ("at", "faces", "looks-at", "note"): chars[-1][k] = a[i + 1]; i += 2; continue
        o[k] = a[i + 1]; i += 2
    return o, chars


def bare(s):
    s = s.strip().lower()
    return s[4:] if s.startswith("the ") else s


def main():
    o, chars = args(sys.argv[1:])
    g = json.load(open(o["geometry"]))
    W, D = g["room"]["width"], g["room"]["depth"]
    S, M, FOOT = 90, 120, 150
    img = Image.new("RGB", (int(W * S + 2 * M), int(D * S + 2 * M + FOOT)), "white")
    d = ImageDraw.Draw(img)
    f, fb, fs = ImageFont.truetype(FONT, 14), ImageFont.truetype(BOLD, 16), ImageFont.truetype(FONT, 13)
    P = lambda x, y: (M + x * S, M + (D - y) * S)
    objects = {bare(ob["name"]): ob for ob in g["objects"]}
    cams = {bare(c["name"]): c for c in g["cameras"]}

    def centre(name):
        n = bare(name)
        if n in cams: return tuple(cams[n]["position"][:2])
        n = n.replace(" camera", "")
        if n in cams: return tuple(cams[n]["position"][:2])
        if n not in objects: sys.exit("not in the geometry: " + name)
        pts = objects[n]["footprint"]
        return (sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts))

    # the room and what is in it
    d.rectangle([P(0, D), P(W, 0)], outline="black", width=3)
    targets = {bare(c.get("looks-at", "")) for c in chars}
    for ob in g["objects"]:
        if ob["kind"] in ("floor", "ceiling", "wall") or len(ob["footprint"]) < 3: continue
        col = tuple(g.get("colours", {}).get(ob["kind"], [200, 200, 200]))
        light = tuple(int(c + (255 - c) * 0.45) for c in col)
        fill = (205, 30, 30) if bare(ob["name"]) in targets else light if ob["kind"] != "door" else (40, 40, 48)
        d.polygon([P(*p) for p in ob["footprint"]], fill=fill, outline=(120, 120, 120))
        if ob["kind"] == "door":  # a door is thin from above: draw it as a thick bar so it reads
            xs, ys = [p[0] for p in ob["footprint"]], [p[1] for p in ob["footprint"]]
            d.rectangle([P(min(xs), max(ys)), P(max(xs), min(ys))], outline=fill, width=7)
    for ob in g["objects"]:
        if ob["kind"] == "door" and not any(w in ob["name"] for w in ("frame", "glass", "bar")):
            x, y = centre(ob["name"])
            tx, ty = P(x, y)
            tx = min(max(tx, M + 4), M + W * S - 140)
            ty = min(max(ty - 22, M + 4), M + D * S - 22)
            d.text((tx, ty), ob["name"], fill=(205, 30, 30) if bare(ob["name"]) in targets else (20, 20, 20), font=fb)
    for name, side in g["room"].get("walls", {}).items():
        pos = {"top": (M + W * S / 2 - 40, M - 26), "bottom": (M + W * S / 2 - 40, M + D * S + 6),
               "left": (8, M + D * S / 2), "right": (M + W * S + 8, M + D * S / 2)}[side]
        d.text(pos, name, fill=(90, 90, 90), font=fs)

    # the shot's camera and the edges of its frame
    cam = cams[bare(o["camera"])]
    cx, cy = cam["position"][:2]
    ang = math.atan2(cam["target"][1] - cy, cam["target"][0] - cx)
    half = math.radians(cam["hfov"] / 2)
    purple = (140, 60, 170)
    for sgn, label in ((1, "frame left"), (-1, "frame right")):
        a = ang + sgn * half
        L = 30.0
        for wall in ((0 - cx) / math.cos(a) if math.cos(a) < 0 else (W - cx) / math.cos(a) if math.cos(a) > 0 else L,
                     (0 - cy) / math.sin(a) if math.sin(a) < 0 else (D - cy) / math.sin(a) if math.sin(a) > 0 else L):
            L = min(L, wall)
        ex, ey = cx + L * math.cos(a), cy + L * math.sin(a)
        d.line([P(cx, cy), P(ex, ey)], fill=purple, width=2)
        mx, my = P(cx + 0.55 * L * math.cos(a), cy + 0.55 * L * math.sin(a))
        d.text((mx + 4, my - 16 * (sgn > 0) + 2), label, fill=purple, font=fs)
    px, py = P(cx, cy)
    d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=purple)
    d.text((px + 10, py + 4), "%s camera (the shot)" % cam["name"], fill=purple, font=fb)

    # each character: mark, facing, look
    red, ink = (205, 30, 30), (20, 20, 20)
    lines = []
    for c in chars:
        x, y = (float(v) for v in c["at"].split(","))
        mx, my = P(x, y)
        if c.get("faces"):
            fx, fy = centre(c["faces"])
            fa = math.atan2(fy - y, fx - x)
            d.line([(mx, my), P(x + 0.75 * math.cos(fa), y + 0.75 * math.sin(fa))], fill=ink, width=4)
            hx, hy = P(x + 0.75 * math.cos(fa), y + 0.75 * math.sin(fa))
            d.polygon([(hx, hy), P(x + 0.55 * math.cos(fa + 0.25), y + 0.55 * math.sin(fa + 0.25)),
                       P(x + 0.55 * math.cos(fa - 0.25), y + 0.55 * math.sin(fa - 0.25))], fill=ink)
        look = c.get("looks-at", "")
        if look and not look.lower().startswith("down"):
            lx, ly = centre(look)
            n = 40
            for i in range(0, n, 2):
                a0, a1 = i / n, (i + 1) / n
                d.line([P(x + (lx - x) * a0, y + (ly - y) * a0), P(x + (lx - x) * a1, y + (ly - y) * a1)], fill=red, width=3)
        d.ellipse([mx - 12, my - 12, mx + 12, my + 12], fill=ink)
        d.text((mx + 15, my - 26), c["name"], fill=ink, font=fb)
        lines.append("%s: at %s; faces %s; looks %s%s." % (
            c["name"], c["at"], c.get("faces", "not set"),
            look if look.lower().startswith("down") else "at " + (look or "not set"),
            ("; " + c["note"]) if c.get("note") else ""))

    # the key, with no file paths
    y0 = M + D * S + 40
    d.text((M, y0), o.get("title") or "%s: staging floor plan" % o["moment"], fill=ink, font=fb)
    for i, t in enumerate(lines + ["Black arrow: which way the body faces. Red dashes: the look. "
                                   "Purple: the shot's camera and the edges of its frame, left and right as the camera sees them."]):
        d.text((M, y0 + 24 + 20 * i), t, fill=ink, font=f)
    img.save(o["out"])


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"): print(__doc__); sys.exit()
    main()
