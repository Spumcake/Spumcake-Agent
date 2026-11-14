---
name: project-library
description: Keep a project's library/, prompts/, and sources/ - everything a model endpoint returned, flat, named by the request that made it, only ever added to; every prompt sent, named by its request; shared material no model made, such as canonical documents, pre-vis renders, and builders; and what research found outside, named by its research request, with each research's report and each source's address and allowed use - and check that nothing in them was changed, moved, or removed, and that every file has its report. Use when filing research, when checking a project, before every commit, and when the user asks where a file is or what the library holds. Not for running requests (project-requests) or publishing canon (project-pipeline).
---

# The library, the resources, and the sources

The library is the master record of everything a model endpoint returned for a project, in the order made. Because nothing in it ever moves, every report and every pipeline can point at its files forever. Only [`scripts/request.py`](../../scripts/request.py) adds to it, as each request runs; this skill keeps it whole.

## What goes where

- **`library/`:** everything a model endpoint returned: images, sounds, videos, and a language model's answers. Named `<request id>.<ext>`, or `<request id>-<n>.<ext>` when the request made several. Rejected results stay: they are part of the record.
- **`prompts/`:** every prompt sent, as `<request id>.txt`, written by `request.py run` as it sends it.
- **`prompts/resources/`:** shared material no model made, kept because it is canon or because a request sends it: canonical documents the agent wrote, such as a floor plan or a style guide; a builder and what it renders, such as a place's pre-vis; an input the agent drew, such as a mask. Named `<time>-<name>.<ext>`, filed with `request.py resource`, or `request.py build` for a builder's output. What the agent makes that is neither canon nor sent to a model, such as a contact sheet, is not kept: a comparison or a chart is embedded in the report of the request it shows.
- **`sources/`:** what research found outside the project, such as photographs and film frames, named `<request id>-<what it is>.<ext>`, with the research's report, `<request id>.html`, which gives each source's address, its page, and the use allowed.
- **Not kept:** anything else the agent made that is neither canon nor sent to a model.

## The rules

- Never change, rename, move, or delete a file in `library/`, `prompts/`, or `sources/`. A better version is a new request with a new file.
- Never add a file by hand. A library file comes only from a request, which reports what made it; a resource only through `request.py resource` or `request.py build`.
- Never nest folders in any of them. A file's name says what made it and when.
- Everything in them is committed to git.

## Filing research

Research runs as a request with the endpoint kind `research`: the spec lists the files found and, for each, its address, page, and allowed use. `request.py run` files them into `sources/` and writes the research's report there.

## The check

Run `request.py check` before every commit and whenever the user asks. It lists every report that points at a missing file, every file in `library/` or `sources/` with no report, every output whose bytes changed since its request made it, and every change git shows in `library/`, `prompts/`, or `sources/` other than an addition. It must come back with no problems; each problem is taken to the user, never fixed by editing the library.

## Answering where a file is

`request.py show <file>` gives the request that made a file. `request.py list --skill <skill>` lists a skill's requests. `ls library` lists everything, in the order made.
