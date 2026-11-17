#!/usr/bin/env python3
"""Write an animatic's assembly, the file assemble.py reads, from its frames, sounds, and times, and file it in
prompts/resources/ with its record. No model, no cost. Whoever times the animatic, an agent or a setup such as
Spumcake Studio, writes the assembly only through this script, so its format is Skills' alone.

Usage:
  write-assembly.py --length <s> --fps <n> --size <w>x<h>
                    --frame <image> <in> <out> ...          each held frame, in order, from 0 to the length, no gap
                    --bed <audio> [<gain_db>]               the sound bed, under everything
                    [--clip <audio> <from> <to> <at> [<gain_db>]] ...
                                                            a sound trimmed to <from>..<to> in its file, laid at <at>
                    [--name <name>] [--from <file>]... [--dry-run] [--json]

Times are in seconds; a gain is in dB, 0 when left out. Paths are the project's, from its root, as the assembly holds
them; a file in work/ is refused, since work/ is never an input. --name names the filed file, animatic-assembly when
left out. --from adds an input the assembly was made from besides its frames and sounds, such as the timing
reference. --dry-run prints the assembly and files nothing; --json prints {"path", "sha256"} of what it filed.

It writes {length, fps, size, frames: [{image, in, out}], bed: {audio, gain_db}, clips: [{audio, from, to, at,
gain_db}]}, as Last order's 2026-11-14_16-07-animatic-assembly.json holds it, and files it with request.py's resource,
whose records.jsonl line names every frame and sound with its sha256, and this command. Run it inside the project.
"""
import sys, os, json, math, shlex, argparse, tempfile, contextlib, io

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "scripts"))
import request as rq


def number(text, what):
    try:
        x = float(text)
    except ValueError:
        sys.exit("%s is not a number: %s" % (what, text))
    if not math.isfinite(x): sys.exit("%s is not a number: %s" % (what, text))
    return x


def gain(text, what):
    g = number(text, what)
    return int(g) if g == int(g) else g   # 0, not 0.0, as Last order's file holds it


def project_file(root, path, what):
    a = os.path.abspath(path if os.path.isabs(path) else os.path.join(root, path))
    if not a.startswith(os.path.abspath(root) + os.sep): sys.exit("%s is outside the project: %s" % (what, path))
    rel = os.path.relpath(a, root)
    if rel.startswith("work/"): sys.exit("refused: %s is in work/, which is never an input; file it first" % rel)
    if not os.path.exists(a): sys.exit("no such file, for %s: %s" % (what, rel))
    return rel


def assembly(o, root):
    L = number(o.length, "the length")
    if L <= 0: sys.exit("the length must be above 0")
    fps = number(o.fps, "the frame rate")
    if fps <= 0 or fps != int(fps): sys.exit("the frame rate must be a whole number above 0")
    try:
        W, H = (int(x) for x in o.size.lower().split("x"))
    except ValueError:
        sys.exit("give the size as <width>x<height>, such as 1536x864: " + o.size)
    if W <= 0 or H <= 0: sys.exit("the size must be above 0")

    if not o.frame: sys.exit("an assembly needs at least one --frame")
    frames, t = [], 0.0
    for f in o.frame:
        if len(f) != 3: sys.exit("--frame takes <image> <in> <out>: " + " ".join(f))
        a, b = number(f[1], "a frame's in"), number(f[2], "a frame's out")
        if abs(a - t) > 1e-6: sys.exit("frames must run on from 0 with no gap: one starts at %g, after %g" % (a, t))
        if b <= a: sys.exit("a frame must end after it starts: %g to %g" % (a, b))
        frames.append({"image": project_file(root, f[0], "the frame"), "in": a, "out": b}); t = b
    if abs(t - L) > 1e-6: sys.exit("the frames end at %g, not at the length, %g" % (t, L))

    if not o.bed or len(o.bed) > 2: sys.exit("--bed takes <audio> [<gain_db>]")
    bed = {"audio": project_file(root, o.bed[0], "the bed"), "gain_db": gain(o.bed[1], "the bed's gain") if len(o.bed) > 1 else 0}

    clips = []
    for c in o.clip or []:
        if len(c) not in (4, 5): sys.exit("--clip takes <audio> <from> <to> <at> [<gain_db>]: " + " ".join(c))
        a, b, at = number(c[1], "a clip's from"), number(c[2], "a clip's to"), number(c[3], "a clip's at")
        if a < 0 or b <= a: sys.exit("a clip's from must be 0 or more and its to after it: %g to %g" % (a, b))
        if at < 0 or at >= L: sys.exit("a clip must be laid inside the film, 0 to %g: at %g" % (L, at))
        clips.append({"audio": project_file(root, c[0], "the clip"), "from": a, "to": b, "at": at,
                      "gain_db": gain(c[4], "a clip's gain") if len(c) > 4 else 0})
    return {"length": L, "fps": int(fps), "size": [W, H], "frames": frames, "bed": bed, "clips": clips}


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0], formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--length", required=True); p.add_argument("--fps", required=True); p.add_argument("--size", required=True)
    p.add_argument("--frame", nargs="+", action="append"); p.add_argument("--bed", nargs="+", required=True)
    p.add_argument("--clip", nargs="+", action="append"); p.add_argument("--name", default="animatic-assembly")
    p.add_argument("--from", dest="sources", action="append", default=[])
    p.add_argument("--dry-run", action="store_true"); p.add_argument("--json", action="store_true")
    o = p.parse_args()
    root = rq.project_root()
    a = assembly(o, root)
    text = json.dumps(a, indent=1, ensure_ascii=False)
    if o.dry_run:
        print(text); return
    rq.guard(root, write=True)
    inputs = []
    for x in [f["image"] for f in a["frames"]] + [a["bed"]["audio"]] + [c["audio"] for c in a["clips"]] + o.sources:
        x = x if x.startswith("git:") else project_file(root, x, "an input")
        if x not in inputs: inputs.append(x)
    command = shlex.join(["python3", os.path.abspath(__file__)] + sys.argv[1:])
    with tempfile.TemporaryDirectory() as d:
        tmp = os.path.join(d, "assembly.json")
        with open(tmp, "w") as fh: fh.write(text)
        with contextlib.redirect_stdout(io.StringIO()):
            filed = rq.resource([tmp], o.name, inputs=inputs, command=command, root=root)
    if o.json: print(json.dumps({"path": filed[0], "sha256": rq.sha(os.path.join(root, filed[0]))}))
    else: print(filed[0])


if __name__ == "__main__":
    main()
