---
name: project-library
description: Keep a project's library/ and sources/ - every output ever made, flat, named by the request that made it, only ever added to; and what research found outside, named by its research request, with each research's report and each source's address and allowed use - and check that nothing in them was changed, moved, or removed, and that every file has its report. Use when filing research, when checking a project, before every commit, and when the user asks where a file is or what the library holds. Not for running requests (project-requests) or publishing canon (project-pipeline).
---

# The library and the sources

The library is the master record of every creative artifact a project ever made, in the order made. Because nothing in it ever moves, every report and every pipeline can point at its files forever. Only [`scripts/request.py`](../../scripts/request.py) adds to it, as each request runs; this skill keeps it whole.

## What goes where

- **`library/`:** every file that was ever an output of a request: renders, sounds, videos, documents a request wrote, and the comparisons and charts made to show results. Named `<request id>.<ext>`, or `<request id>-<n>.<ext>` when the request made several, and `<request id>-comparison.<ext>` or `-chart` for what was made to show them. Rejected results stay: they are part of the record.
- **`sources/`:** what research found outside the project, such as photographs and film frames, named `<request id>-<what it is>.<ext>`, with the research's report, `<request id>.html`, which gives each source's address, its page, and the use allowed.
- **Not kept:** a file that was only ever an input, such as a prompt. Its text or image is in the report of the request that used it.

## The rules

- Never change, rename, move, or delete a file in `library/` or `sources/`. A better version is a new request with a new file.
- Never add a file by hand. A file with no request has no report, and so no record of what made it.
- Never nest folders in either. A file's name says what made it and when.
- Everything in both is committed to git.

## Filing research

Research runs as a request with the endpoint kind `research`: the spec lists the files found and, for each, its address, page, and allowed use. `request.py run` files them into `sources/` and writes the research's report there.

## The check

Run `request.py check` before every commit and whenever the user asks. It lists every report that points at a missing file, every file in `library/` or `sources/` with no report, every output whose bytes changed since its request made it, and every change git shows in either folder other than an addition. It must come back with no problems; each problem is taken to the user, never fixed by editing the library.

## Answering where a file is

`request.py show <file>` gives the request that made a file. `request.py list --skill <skill>` lists a skill's requests. `ls library` lists everything, in the order made.
