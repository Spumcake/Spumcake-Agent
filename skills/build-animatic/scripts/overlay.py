#!/usr/bin/env python3
"""Lay a shot's animatic over its final render, to show how closely the render keeps to it: the line-art
animation's lines in one colour, and the pre-vis's edges, the place and anything moving in it such as a door, in
another. No model.

Usage: python3 overlay.py <render.mp4> <line-art.mp4> <out.mp4> [--previs <pre-vis.mp4>]
                          [--line-colour 255,255,255] [--previs-colour 0,220,255]

Each input is scaled to the render's size. The render's sound is kept. Needs ffmpeg.
"""
import json, os, shutil, subprocess, sys, tempfile
from PIL import Image, ImageChops, ImageFilter

a = sys.argv[1:]
render, line_art, out = a[0], a[1], a[2]
opt = {a[i][2:]: a[i + 1] for i in range(3, len(a) - 1) if a[i].startswith("--")}
previs = opt.get("previs")
line_col = tuple(int(x) for x in opt.get("line-colour", "255,255,255").split(","))
pre_col = tuple(int(x) for x in opt.get("previs-colour", "0,220,255").split(","))


def frames(video, d, size=None):
    os.makedirs(d)
    vf = ["-vf", "scale=%d:%d" % size] if size else []
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", video] + vf + [os.path.join(d, "%05d.png")], check=True)
    return sorted(os.listdir(d))


tmp = tempfile.mkdtemp()
rf = frames(render, os.path.join(tmp, "r"))
size = Image.open(os.path.join(tmp, "r", rf[0])).size
lf = frames(line_art, os.path.join(tmp, "l"), size)
pf = frames(previs, os.path.join(tmp, "p"), size) if previs else []
os.makedirs(os.path.join(tmp, "o"))
for i, f in enumerate(rf):
    img = Image.open(os.path.join(tmp, "r", f)).convert("RGB")
    if pf:
        g = Image.open(os.path.join(tmp, "p", pf[min(i, len(pf) - 1)])).convert("L")
        edges = g.filter(ImageFilter.FIND_EDGES).point(lambda v: 255 if v > 18 else 0)
        img = Image.composite(Image.blend(img, Image.new("RGB", size, pre_col), 0.85), img, edges)
    lines = Image.open(os.path.join(tmp, "l", lf[min(i, len(lf) - 1)])).convert("L").point(lambda v: 255 if v < 128 else 0)
    img = Image.composite(Image.new("RGB", size, line_col), img, lines)
    img.save(os.path.join(tmp, "o", f))
fps = json.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=r_frame_rate",
                                 "-of", "json", render], capture_output=True, text=True, check=True).stdout)["streams"][0]["r_frame_rate"]
subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", fps, "-i", os.path.join(tmp, "o", "%05d.png"), "-i", render,
                "-map", "0:v", "-map", "1:a?", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-c:a", "aac",
                "-shortest", out], check=True)
shutil.rmtree(tmp)
print(out)
