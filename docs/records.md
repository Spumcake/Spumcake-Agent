# Records

Every file a film is made of keeps a **record**: a small file beside it that says what it is, what made it, what it was made from, and what it shows. Records are the paper trail from any image, sound, or video back to the geometry, the research, and the prompts it came from, and they are the context an agent reads before it writes the next prompt: which camera an image is from, which named things are in its frame and where, and in what state. They are the agent's, never sent to a model. As the user set on 2026-11-13, every new file gets its record when it is made, in one format, so the records stay clean and useful.

## The record

A record sits beside its file, named for it: `layout-far-end-5.png` keeps `layout-far-end-5.record.json`. It is JSON:

- **`record`:** the format's version, `1`.
- **`file`:** the file's path from the film's root, the folder that holds its film map, `film-map.md`; every other path in a record starts there too.
- **`kind`:** what it is: `pre-vis render`, `research photo`, `concept design`, `canonical image`, `prop sheet`, `concept art`, `model sheet`, `layout drawing`, `keyframe`, `voice take`, `sound bed`, `video`, or `copy`.
- **`date`:** when the file was made, in UTC.
- **`made_by`:** the tool or model, its endpoint, its settings, and its cost when known.
- **`prompt`:** the path of the prompt file it was made from, never the prompt's text; for a video, its assembly file.
- **`made_from`:** each source file, as `{"file", "role"}`, the role saying what the source was in the request, such as "image 1, the layout of the shot". A copy has one source, with the role `copied from`.
- **`camera`**, **`place`**, and **`floor_plan`**, for an image of a place: the floor plan's camera name, the place, and the floor plan's path.
- **`contents`:** each named thing in the frame, by its floor-plan or canonical name, as `{"name", "where", "frame_box", "state"}`; a character also with `"mark"` and `"looks_at"`. A pre-vis render's contents come from the geometry; an image made from others inherits its sources' contents, changed only where the request changed them, and adds what it put in.
- **`source`:** for a research photo, its address, its page, and the use allowed.
- **`notes`:** anything else worth knowing, such as a known error.

Status, whether a file is approved, waiting, or rejected, is not in the record: its one home is the film map.

## The tool

[`scripts/records.py`](../scripts/records.py) is the only way records are written and files are copied or moved:

- `write` makes a record. [`scripts/generate.py`](../scripts/generate.py), which sends a prompt to an image or audio model exactly as written, calls it for every result; so do the pre-vis builder and the animatic's [assembly script](../skills/build-animatic/scripts/assemble.py). Any other renderer must too. An image made from others takes image 1's camera and contents unless the request changed what is in the frame, when the new contents are given.
- `copy` and `move` copy or move a file with its record; a copy records its source, and a move rewrites every record that points at the old path.
- `trace <file>` draws and lists the file's whole paper trail.
- `children <file>` lists what was made from a file, so a change to it says what must be made again.
- `find` finds files by what their records say, such as every image from a camera that shows a named thing.
- `check` lists files with no record, records that point at missing files, copies with no source, and images with no contents.
- `adopt` turns an older record into this one, keeping the older file: a run's `.json`, a numbered folder's `sources.json`, a research photo's `.source.txt`, or an animatic's assembly file; `--moved` follows folders that have moved since. With `--copies`, it finds an unrecorded copy's source by its bytes; only for a file copied into a set, never for a builder's render, which a later render can match.

## Keeping them clean

- Every step that makes a file writes its record before it shows the result; a result with no record is not shown.
- A file is copied into a set or moved to a new folder only with the tool.
- `check` runs before any result is shown to the user (`review-continuity`) and before every commit, over everything the film map lists and everything those trace back to; it must come back clean.
- Before writing a prompt, read the records of the images to be sent: they say what each shows and what each thing is called.
- A record goes where its file goes: into version control with it, or out of it with it.
- A record is never written by hand from memory; where an older file has none, it is rebuilt from what made it, such as running the builder again and checking that the render matches byte for byte.
