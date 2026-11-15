#!/usr/bin/env python3
"""Lay a line-art shot over its place: each frame of the shot, an outline drawing on white, over the layout
drawing its moment uses, with the character made solid so the place does not show through them. No model.

Usage: python3 composite.py <composite.json> <out.mp4>

composite.json:
{
  "shot": "line-art shot.mp4",
  "backgrounds": [{"image": "layout.png", "in": 0.0, "out": 3.0}, ...],  or {"video": "place.mp4", ...}, whose frame
                       at each moment is used, such as a pre-vis render of a door opening
  "white": 215,        what counts as the page: brighter than this, 0 to 255
  "close": 5           how far a line is thickened to close small gaps before the page is found, in pixels
}
The page is every near-white pixel joined to the frame's edge; everything else, the lines and what they enclose,
is the character. The backgrounds must run on from 0 to the shot's length without a gap. Keeps the shot's sound.
Needs ffmpeg.
"""
import json, os, subprocess, sys, tempfile
from PIL import Image, ImageChops, ImageDraw, ImageFilter

spec = json.load(open(sys.argv[1])); out = sys.argv[2]
shot = spec["shot"]
probe = json.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                   "stream=width,height,r_frame_rate", "-of", "json", shot],
                                  capture_output=True, text=True, check=True).stdout)["streams"][0]
W, H = probe["width"], probe["height"]
num, den = (int(x) for x in probe["r_frame_rate"].split("/"))
fps = num / den
bgs = spec["backgrounds"]
t = 0.0
for b in bgs:
    assert abs(b["in"] - t) < 1e-6, "gap or overlap at %s" % b["in"]
    t = b["out"]
white, close = spec.get("white", 215), spec.get("close", 5)
cache = {}


def background(time):
    for b in bgs:
        if b["in"] <= time < b["out"] or b is bgs[-1]:
            if b.get("video"):
                if b["video"] not in cache:
                    d = tempfile.mkdtemp()
                    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", b["video"], os.path.join(d, "b%05d.png")], check=True)
                    r = json.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                                   "stream=r_frame_rate", "-of", "json", b["video"]],
                                                  capture_output=True, text=True, check=True).stdout)["streams"][0]["r_frame_rate"]
                    n, m = (int(x) for x in r.split("/"))
                    cache[b["video"]] = (d, sorted(os.listdir(d)), n / m)
                d, names, vfps = cache[b["video"]]
                i = min(int(round((time - b["in"]) * vfps)), len(names) - 1)
                return Image.open(os.path.join(d, names[i])).convert("RGB").resize((W, H), Image.LANCZOS)
            if b["image"] not in cache:
                cache[b["image"]] = Image.open(b["image"]).convert("RGB").resize((W, H), Image.LANCZOS)
            return cache[b["image"]]


def matte(frame):
    """The character: everything but the page, where the page is near-white joined to the frame's edge.
    Found at half size by growing the page in from the edge through near-white, then scaled back up."""
    import numpy as np
    small = frame.convert("L").resize((W // 2, H // 2), Image.BILINEAR)
    ink = Image.fromarray(np.uint8(np.array(small) < white) * 255)
    if close > 1: ink = ink.filter(ImageFilter.MaxFilter(max(3, close // 2 * 2 + 1)))
    free = np.array(ink) == 0
    page = np.zeros_like(free)
    page[0, :], page[-1, :], page[:, 0], page[:, -1] = free[0, :], free[-1, :], free[:, 0], free[:, -1]
    while True:
        grown = page.copy()
        for _ in range(8):
            g = grown.copy()
            g[1:, :] |= grown[:-1, :]; g[:-1, :] |= grown[1:, :]; g[:, 1:] |= grown[:, :-1]; g[:, :-1] |= grown[:, 1:]
            grown = g & free
        if (grown == page).all(): break
        page = grown
    m = Image.fromarray(np.uint8(~page) * 255)
    if close > 1: m = m.filter(ImageFilter.MinFilter(max(3, close // 2 * 2 + 1)))
    return m.resize((W, H), Image.BILINEAR).filter(ImageFilter.GaussianBlur(1))


tmp = tempfile.mkdtemp()
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", shot, os.path.join(tmp, "f%05d.png")], check=True)
frames = sorted(f for f in os.listdir(tmp) if f.startswith("f"))
for i, f in enumerate(frames):
    fr = Image.open(os.path.join(tmp, f)).convert("RGB")
    bg = background(i / fps)
    m = matte(fr)
    solid = Image.composite(fr, bg, m)              # the character, opaque, over the place
    Image.composite(solid, ImageChops.multiply(bg, fr), m).save(os.path.join(tmp, "c" + f[1:]))
subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", "%g" % fps, "-i", os.path.join(tmp, "c%05d.png"),
                "-i", shot, "-map", "0:v", "-map", "1:a?", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18",
                "-c:a", "aac", "-shortest", out], check=True)
import shutil
shutil.rmtree(tmp)
for v in cache.values():
    if isinstance(v, tuple): shutil.rmtree(v[0])
print(out)
