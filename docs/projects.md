# Projects

A project, such as one film, is a folder that says what it holds through its folders and file names alone. No README or map is needed to read it, and no document holds a path that can go stale: files are named once, in the order they were made, and never moved.

```text
<project>/
  requests/   one report per request, <request id>.html
  library/    every output ever made, flat, <request id>.<ext>; only added to
  sources/    what research found outside, <request id>-<name>.<ext>, and each research's report, <request id>.html
  brief/      the intent, one page per pipeline, <pipeline>-<project>.html
  pipeline/   one folder per pipeline, 001/: its published canon, canon.sql; a page per chain, <nn>-<chain>.html;
              and the scripts its chains run again
  output/     finished deliverables, flat, <timestamp>-<pipeline>-<project>.<ext>
```

Each folder is owned by one skill, which alone writes there: `requests/` by [project-requests](../skills/project-requests/SKILL.md), `library/` and `sources/` by [project-library](../skills/project-library/SKILL.md), `brief/` by [project-brief](../skills/project-brief/SKILL.md), `pipeline/` by [project-pipeline](../skills/project-pipeline/SKILL.md), and `output/` by [project-output](../skills/project-output/SKILL.md). Every other skill returns its result to `project-requests` and writes nothing itself. Everything in a project is versioned in git, the library included.

## Names

- **A request ID** is the request's start time in UTC and a short name: `2026-11-14_13-30-keyframe-the-line`. It sorts in the order requests were made.
- **A library file** is its request's ID, with `-1`, `-2` when the request made several, and `-comparison` or `-chart` for what the agent made to show the results: `2026-11-14_13-30-keyframe-the-line-2.png`.
- **A source** is its research request's ID and what it is: `2026-11-09_14-07-diner-research-1939-route-40-diner.jpg`.
- **An output** is its time, its pipeline, and the project: `2026-11-14_13-30-001-last-order.mp4`.
- No folder holds a single file.

## Requests

A request is anything the user asks for that can result in a canonical outcome: one call to one endpoint, with one prompt, as one cycle. A user's message can hold several; `project-requests` names each, orders them by what each needs from another, and runs them in that order. A `make` skill is not a request: it plans the requests its steps need, and each runs as its own cycle.

[`scripts/request.py`](../scripts/request.py) is the one runner. It sends the request exactly as its skill built it, files every output into `library/`, and writes the report from what it sent and received: the endpoint and its settings; every reference in the order sent, with its role; the prompt as sent; the canon read, and when; the scripts run; the cost; and the outputs. The agent adds only its own words, what was asked and why, and the comparisons and charts it makes to show the results. The same data sits in the report as JSON, so `request.py show <file>` answers what made any file. A file that was only ever an input, such as a prompt, is kept in its report, not in the library.

## Publishing

A result becomes canon only when the user approves it and `project-pipeline` publishes it into the pipeline's table. Nothing else is canon. The table, `canon.sql`, is text that [`scripts/pipeline.py`](../scripts/pipeline.py) loads into SQLite. It holds:

- each canonical element, such as a place, a character, a prop, or a part of one, such as a door;
- each published artifact, named `<element>: <role>`, such as `the diner: primary canonical location`: its library file, the request that made it, when it was published, and what it was made from;
- each element's canonical facts, `<element>: <fact>`, such as `the front door: side in the far-end frame`, each with the artifact that settles it;
- what each published image shows: its camera, and each named thing in its frame, where it is, its state, and, for a character, its mark and what it looks at;
- each chain's steps, approved or still waiting: the skill, the endpoint, the prompt as a template that names canon, `{{<element>: <fact>}}`, never a file or a copied value, the references by artifact, and the request that last ran it.

A chain is a run of dependent requests that ends in published canon, such as a place from its research to its views. Its page, written from the table, shows each step, what it was made from, and how it relates to the chains before it.

## Pipelines

Pipelines are numbered from `001`. A pipeline's brief is updated in place while a change adds to its canon or refines what is not yet published. A change that contradicts published canon starts the next pipeline: its brief is copied with the change, its folder starts as a copy of the one before, and `pipeline.py touches` lists every published artifact and step the change reaches through what each was made from. Only those steps run again, their templates filled from the new pipeline's table, until the chain ends in a new output.

## The audit

`project-brief` compares the brief with the pipeline's canon. What the brief asks for that canon does not show, or shows differently, becomes a request.
