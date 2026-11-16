---
name: project-output
description: File a project's finished deliverables into output/ - flat, named <timestamp>-<pipeline>-<project>.<ext>, such as 2026-11-14_13-30-001-last-order.mp4 - only when the user calls a result finished, from its published file in the library. Use when the user says a film, a cut, or another deliverable is finished. Not for work in progress, which stays in the library.
---

# Output

`output/` holds only what is finished, so it is the folder a viewer opens. Only this skill writes it.

## Delivering

When the user calls a result finished:

1. The result must be published canon in the pipeline it belongs to; if it is not, publish it first with `project-pipeline`.
2. `pipeline.py deliver <n> <file>` copies it to `output/<timestamp>-<pipeline>-<project>.<ext>`: the user's local time as `YYYY-MM-DD_HH-MM`, the pipeline's number, and the project's folder name. The record inside the copy is cut to the disclosure and the request's ID, since a delivered file is shared, and its metadata goes wherever it does; the full record stays in the library's file.
3. Tell the user the file's name.

## The rules

- Nothing unfinished goes in `output/`: no drafts, tests, or contact sheets.
- No folders inside it: the name says when, from which pipeline, and of which project.
- A delivered file is never changed. A new cut is a new file with its own time.
- `output/` is committed to git with the rest of the project.
