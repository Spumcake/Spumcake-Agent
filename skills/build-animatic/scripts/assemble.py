#!/usr/bin/env python3
"""Assemble an animatic: frames held on the timing reference's times, over the sound bed with the voice clips laid on their cues.

Usage: python3 assemble.py <assembly.json> <out.mp4>

The assembly is written and filed by write-assembly.py, never by hand.

assembly.json:
{
  "length": 8.0, "fps": 24, "size": [1536, 864],
  "frames": [{"image": "path.png", "in": 0.0, "out": 3.0}, ...],
  "bed": {"audio": "bed.wav", "gain_db": 0},
  "clips": [{"audio": "take.wav", "from": 0.05, "to": 0.65, "at": 4.2, "gain_db": 0}, ...]
}
Frames must run on from 0 to length without a gap. Needs ffmpeg. Writes only the video; project-library runs this
as a build (request.py build), which files the video into prompts/resources/.
"""
import json, subprocess, sys, tempfile, os

spec = json.load(open(sys.argv[1])); out = sys.argv[2]
L, fps = spec["length"], spec.get("fps", 24); W, H = spec.get("size", [1536, 864])
frames = spec["frames"]
t = 0.0
for f in frames:
    assert abs(f["in"] - t) < 1e-6, f"gap or overlap at {f['in']}"
    t = f["out"]
assert abs(t - L) < 1e-6, f"frames end at {t}, not {L}"

tmp = tempfile.mkdtemp()
# audio: bed plus each clip trimmed and delayed to its cue
inputs, filters, labels = ["-i", spec["bed"]["audio"]], [f"[0:a]volume={spec['bed'].get('gain_db',0)}dB,atrim=0:{L}[bed]"], ["[bed]"]
for i, c in enumerate(spec.get("clips", []), 1):
    inputs += ["-i", c["audio"]]
    d = int(round(c["at"] * 1000))
    filters.append(f"[{i}:a]atrim={c['from']}:{c['to']},asetpts=PTS-STARTPTS,volume={c.get('gain_db',0)}dB,adelay={d}|{d}[c{i}]")
    labels.append(f"[c{i}]")
filters.append("".join(labels) + f"amix=inputs={len(labels)}:normalize=0:duration=first,atrim=0:{L}[mix]")
mix = os.path.join(tmp, "mix.wav")
subprocess.run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", ";".join(filters), "-map", "[mix]", "-ar", "48000", mix], check=True)

# video: each frame held for its length. Every frame is first made plain RGB, a transparent one laid on white, since
# the concat stops early at a frame whose pixel format differs from the first's (an RGBA board among RGB keyframes)
plain = []
for i, f in enumerate(frames):
    p = os.path.join(tmp, f"f{i:05d}.png")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", f["image"], "-filter_complex",
                    "[0]split[a][b];[a]drawbox=c=white@1:t=fill[w];[w][b]overlay=format=auto,format=rgb24", "-frames:v", "1", p], check=True)
    plain.append(p)
lst = os.path.join(tmp, "frames.txt")
with open(lst, "w") as fh:
    for f, p in zip(frames, plain):
        fh.write(f"file '{p}'\nduration {f['out'] - f['in']:.3f}\n")
    fh.write(f"file '{plain[-1]}'\n")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-i", mix,
                "-vf", f"scale={W}:{H}:force_original_aspect_ratio=decrease,pad={W}:{H}:(ow-iw)/2:(oh-ih)/2:white,fps={fps},format=yuv420p",
                "-c:v", "libx264", "-crf", "18", "-c:a", "aac", "-b:a", "192k", "-t", str(L), "-shortest", out], check=True)
print("wrote", out, "and the mix", mix)
