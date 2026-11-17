#!/usr/bin/env python3
"""Mix a take with its sound layers into the film, H.264 with AAC, and file it in prompts/resources/ with request.py
build, whose record names the take and every sound heard. No model, no cost. Whoever mixes, an agent or a setup such
as Spumcake Studio, writes a mix only through this script, so the same inputs make the same bytes.

Usage:
  mix.py --take <video> [--take-sound <gain_db>]
         [--sound <audio> <gain_db> <start> [muted]] ...
         --name <artifact> [--from <file>]... [--dry-run] [--json]

--take is the picture. Its own sound is left out, as Last order's mixes left H3's out, unless --take-sound gives its
gain. Each --sound is a layer: its file, its gain in dB, and where it starts in the take, in seconds; it plays from
its own start, and a sound running past the take's end is cut there. A layer ending in "muted" is recorded in the
command but left out of the mix and of the inputs. Paths are the project's, from its root; a file in work/ or outside
the project is refused, and so is a sound starting outside the take. --name names the filed film, as the artifact it
will be published as; --from adds an input besides the take and the sounds. --dry-run prints the mix as JSON and files
nothing; --json prints {"path", "sha256"} of what it filed. Run it inside the project.

The picture is copied untouched when it is already H.264 in yuv420p, as Last order's was; anything else is encoded
with libx264, CRF 16. The sound is 48 kHz stereo AAC at 256 kb/s, as long as the take. The output carries no
timestamps or encoder versions, so the same inputs and the same ffmpeg make the same bytes.

  mix.py --write <out.mp4> ...    the same arguments: only write the film, as request.py build runs it
"""
import sys, os, json, math, shlex, argparse, subprocess

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "scripts"))
import request as rq

RATE = 48000


def number(text, what):
    try:
        x = float(text)
    except ValueError:
        sys.exit("%s is not a number: %s" % (what, text))
    if not math.isfinite(x): sys.exit("%s is not a number: %s" % (what, text))
    return x


def project_file(root, path, what):
    a = os.path.abspath(path if os.path.isabs(path) else os.path.join(root, path))
    if not a.startswith(os.path.abspath(root) + os.sep): sys.exit("%s is outside the project: %s" % (what, path))
    rel = os.path.relpath(a, root)
    if rel.startswith("work/"): sys.exit("refused: %s is in work/, which is never an input; file it first" % rel)
    if not os.path.exists(a): sys.exit("no such file, for %s: %s" % (what, rel))
    return rel


def probe(root, path):
    r = rq.keyless(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type,codec_name,pix_fmt",
                    "-of", "json", path], cwd=root, capture_output=True, text=True)
    if r.returncode: sys.exit("ffprobe cannot read %s: %s" % (path, r.stderr.strip()))
    d = json.loads(r.stdout)
    return float(d["format"]["duration"]), d.get("streams", [])


def the_mix(o, root):
    take = project_file(root, o.take, "the take")
    length, streams = probe(root, take)
    video = [s for s in streams if s["codec_type"] == "video"]
    if not video: sys.exit("the take has no picture: " + take)
    take_sound = None
    if o.take_sound is not None:
        if not any(s["codec_type"] == "audio" for s in streams): sys.exit("the take has no sound for --take-sound: " + take)
        take_sound = number(o.take_sound, "the take's gain")
    sounds = []
    for s in o.sound or []:
        if len(s) not in (3, 4) or (len(s) == 4 and s[3] != "muted"):
            sys.exit("--sound takes <audio> <gain_db> <start> [muted]: " + " ".join(s))
        g, at = number(s[1], "a sound's gain"), number(s[2], "a sound's start")
        if at < 0 or at >= length: sys.exit("a sound must start inside the take, 0 to %.3f s: %s starts at %g" % (length, s[0], at))
        f = project_file(root, s[0], "a sound")
        if not any(x["codec_type"] == "audio" for x in probe(root, f)[1]): sys.exit("no sound in " + f)
        sounds.append({"audio": f, "gain_db": g, "start": at, "muted": len(s) == 4})
    copy = video[0].get("codec_name") == "h264" and video[0].get("pix_fmt") == "yuv420p"
    return {"take": take, "length": length, "take_sound": take_sound, "picture": "copied" if copy else "encoded",
            "sounds": sounds}


def write(m, out, root):
    heard = [s for s in m["sounds"] if not s["muted"]]
    inputs, chains, labels = ["-i", m["take"]], [], []
    if m["take_sound"] is not None:
        chains.append("[0:a]aformat=sample_rates=%d:channel_layouts=stereo,volume=%gdB[t]" % (RATE, m["take_sound"]))
        labels.append("[t]")
    for i, s in enumerate(heard, 1):
        inputs += ["-i", s["audio"]]
        chains.append("[%d:a]aformat=sample_rates=%d:channel_layouts=stereo,volume=%gdB,adelay=%dS:all=1[s%d]"
                      % (i, RATE, s["gain_db"], round(s["start"] * RATE), i))
        labels.append("[s%d]" % i)
    if not labels:   # every layer muted: the film still has a sound track, silent
        inputs += ["-f", "lavfi", "-i", "anullsrc=r=%d:cl=stereo" % RATE]
        labels.append("[%d:a]" % (inputs.count("-i") - 1))
    chains.append("%samix=inputs=%d:normalize=0:duration=longest,apad,atrim=0:%.6f[mix]" % ("".join(labels), len(labels), m["length"]))
    picture = ["-c:v", "copy"] if m["picture"] == "copied" else ["-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p"]
    cmd = (["ffmpeg", "-v", "error", "-y"] + inputs + ["-filter_complex", ";".join(chains), "-map", "0:v:0", "-map", "[mix]"]
           + picture + ["-c:a", "aac", "-b:a", "256k", "-ar", str(RATE), "-t", "%.6f" % m["length"], "-map_metadata", "-1",
                        "-fflags", "+bitexact", "-flags:v", "+bitexact", "-flags:a", "+bitexact", out])
    r = rq.keyless(cmd, cwd=root)
    if r.returncode: sys.exit("ffmpeg failed (exit %d)" % r.returncode)


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0], formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--take", required=True); p.add_argument("--take-sound")
    p.add_argument("--sound", nargs="+", action="append")
    p.add_argument("--name"); p.add_argument("--from", dest="sources", action="append", default=[])
    p.add_argument("--dry-run", action="store_true"); p.add_argument("--json", action="store_true")
    p.add_argument("--write", help=argparse.SUPPRESS)
    o = p.parse_args()
    root = rq.project_root()
    m = the_mix(o, root)
    if o.write:
        write(m, o.write, root); return
    if o.dry_run:
        print(json.dumps(m, indent=1, ensure_ascii=False)); return
    if not o.name: sys.exit("--name names the mixed film, as the artifact it will be published as")
    rq.guard(root, write=True)
    inputs = []
    for x in [m["take"]] + [s["audio"] for s in m["sounds"] if not s["muted"]] + o.sources:
        x = x if x.startswith("git:") else project_file(root, x, "an input")
        if x not in inputs: inputs.append(x)
    out = os.path.join(".build", "mix-%s.mp4" % rq.slug(o.name))
    args = [a for a in sys.argv[1:] if a not in ("--json",)]
    keep, skip = [], 0   # the command request.py build runs and records: these layers, writing to out, never filing again
    for i, a in enumerate(args):
        if skip: skip -= 1; continue
        if a in ("--name", "--from"): skip = 1; continue
        keep.append(a)
    command = shlex.join(["python3", os.path.abspath(__file__)] + keep + ["--write", out])
    import io, contextlib
    with contextlib.redirect_stdout(io.StringIO()):
        filed = rq.build(command, [out], o.name, inputs=inputs, root=root)
    os.remove(os.path.join(root, out))   # filed: the copy in prompts/resources/ is the film
    if o.json: print(json.dumps({"path": filed[0], "sha256": rq.sha(os.path.join(root, filed[0]))}))
    else: print(filed[0])


if __name__ == "__main__":
    main()
