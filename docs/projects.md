# Projects

A project, such as one film, is a folder that says what it holds through its folders and file names alone. No README or map is needed to read it, and no document holds a path that can go stale: files are named once, in the order they were made, and never moved.

```text
<project>/
  requests/   one report per request to a model endpoint, <request id>.html
  library/    everything a model endpoint ever returned, flat, <request id>.<ext>; only added to
  prompts/    every prompt sent, flat, <request id>.txt; only added to
    resources/  shared material no model made, flat, <time>-<name>.<ext>: canonical documents, pre-vis renders,
                builders, and anything else a request sends; only added to
  sources/    what research found outside, <request id>-<name>.<ext>, and each research's report, <request id>.html
  brief/      the intent, one page per pipeline, <pipeline>-<project>.html
  pipeline/   the living pipeline, 001/: its published canon, canon.sql, its run log, runs.jsonl, only added to,
              and a page per chain, <nn>-<chain>.html
  output/     finished deliverables, flat, <timestamp>-<pipeline>-<project>.<ext>
  agent/      everything else the agent makes for the project, flat, <time>-<name>.<ext>: checks, comparisons,
              frame strips, overlays, specs, test builds, scripts, and screenshots the user pastes; only added to
  work/       a setup's workspace files, such as a storyboard's layered, editable work: overwritten on save and
              committed, written by no skill, and never an input to a step or a request
```

A setup may also keep its own state, such as open tabs, cameras, and its own history of the project, in a dot-folder of its own at the project's root, which may be committed with the project, and which no skill reads or writes and `request.py check` ignores. Everything a later step needs is in the project's own folders, never only in a setup's folder or in a conversation, so a project moves between setups, an agent's harness included, and each picks up where the other left off.

**Starting a project.** `request.py init [<folder>]` starts one, in the current folder when none is named: every folder above, each empty one holding a `.gitkeep` so a clone keeps it; `agent/index.md`; pipeline `001`; and a `.gitignore` for Skills' own scratch, `.build/` and `.stand-in/`. It runs `git init` when the folder is in no repository, and joins the one it is in otherwise, as spumcake-benchmarks holds its projects. It refuses a folder that holds a project or is inside one. An agent's harness and a setup start a project the same way, and a setup adds its own dot-folder after; nothing else makes the layout.

Each folder is owned by one skill, which alone writes there: `requests/` by [project-requests](../skills/project-requests/SKILL.md), `library/`, `prompts/`, `sources/`, and `agent/` by [project-library](../skills/project-library/SKILL.md), `brief/` by [project-brief](../skills/project-brief/SKILL.md), `pipeline/` by [project-pipeline](../skills/project-pipeline/SKILL.md), and `output/` by [project-output](../skills/project-output/SKILL.md). Every other skill returns its result to `project-requests` and writes nothing itself. `work/` is the setup's, and no skill writes it; anything in it that a step needs is exported as a plain file and filed first. Everything in a project is versioned in git, the library included.

## Names

- **A request ID** is the request's start time, in the user's local time, and a short name: `2026-11-14_13-30-keyframe-the-line`. It sorts in the order requests were made.
- **A library file** is its request's ID, with `-1`, `-2` when the request made several: `2026-11-14_13-30-keyframe-the-line-2.png`.
- **A prompt** is its request's ID: `2026-11-14_13-30-keyframe-the-line.txt`.
- **A resource** is the time it was filed and what it is: `2026-11-13_19-02-floor-plan.md`, `2026-11-11_22-20-previs-far-end-wall-grey.png`.
- **A source** is its research request's ID and what it is: `2026-11-09_14-07-diner-research-1939-route-40-diner.jpg`.
- **An output** is its local time, its pipeline, and the project: `2026-11-14_13-30-001-last-order.mp4`.
- **A scene file** is a place's geometry, a glTF 2.0 binary filed as a resource, named for its place and the builder it was made from: `2026-11-16_11-59-diner-scene-2026-11-14-19-56.glb`. Once a place has one, it is the place's only geometry ([build-previs](../skills/build-previs/SKILL.md)).
- **An agent file** is the local time it was made and what it is: `2026-11-14_21-12-door-21-08-fine.png`. `agent/index.md` says what each is. Nothing made for a project is thrown away or left in a scratch folder: the agent writes these files here from the start (the user, 2026-11-14).
- No folder holds a single file.

## Requests

A request is one call to a generative model's endpoint, such as an image, a sound, or a language model's answer, with one prompt, as one cycle. What the agent writes or draws itself, and what a builder makes, is not a request: it is kept in `prompts/resources/` when it is canon or is sent to a model, and in `agent/` otherwise. A resource or a build is filed with the inputs it was made from (`request.py resource` or `build --from`), and `prompts/resources/records.jsonl`, only added to, holds one line for each: its sha256, each input with its sha256, the command, and the Skills commit, which `request.py show` reads. Nothing made for a project is thrown away or left in a scratch folder (the user, 2026-11-14). A user's message can hold several; `project-requests` names each, orders them by what each needs from another, and runs them in that order. A `make` skill is not a request: it plans the requests its steps need, and each runs as its own cycle.

[`scripts/request.py`](../scripts/request.py) is the one runner. It sends the request exactly as its skill built it, files every output into `library/`, writes the prompt as sent into `prompts/<request id>.txt`, and writes the report from what it sent and received: the endpoint and its settings; every reference in the order sent, with its role; the prompt as sent; the canon read, and when; the scripts run; the cost; and the outputs. The agent adds only its own words, what was asked and why, and the comparisons and charts it makes to show the results, which are embedded in the report and kept nowhere else. The same data sits in the report as JSON, so `request.py show <file>` answers what made any file. Any other input a request sends, such as a pre-vis render, is a resource in `prompts/resources/`.

**The record inside the file.** As the user set on 2026-11-16, every image or video a request files carries its record inside it, so the file says where it came from wherever it goes: a PNG as an iTXt chunk, `spumcake:record`, with the standard IPTC "made by a trained model" disclosure in its XMP; an MP4 or MOV as its comment, its streams copied, never encoded again. The record is one JSON object with a format version: the request's ID, the skill, the service, the model, the settings, the prompt as sent, what was asked and why, each input with its role, order, canonical name, and sha256, the canon read, the sha256 of the file as the endpoint returned it, and the Skills commit, with an optional object a setup fills. It never holds a key, an absolute path, an email address, or an input itself. Whether a file is canon, and its version, are never in it: they change, and the file never does. The report keeps both sha256s, the endpoint's and the filed file's. `request.py record <file>` prints it. A file delivered to `output/` carries only the disclosure and the request's ID, since a delivered file is shared.

## Publishing

A result becomes canon only when the user approves it and `project-pipeline` publishes it into the pipeline's table. Nothing else is canon. A result made but not published is a **take**: running a step again makes a take, never a change to canon, and the agent puts a take into the chain only after saying what it would reach, with the user's yes. The table, `canon.sql`, is text that [`scripts/pipeline.py`](../scripts/pipeline.py) loads into SQLite. It holds:

- each canonical element, such as a place, a character, a prop, or a part of one, such as a door;
- each published artifact, named `<element>: <role>`, such as `the diner: primary canonical location`: its file in `library/` or `prompts/resources/`, the request that made it, when it was published, and what it was made from;
- each element's canonical facts, `<element>: <fact>`, such as `the front door: side in the far-end frame`, each with the artifact that settles it;
- what each published image shows: its camera, and each named thing in its frame, where it is, its state, and, for a character, its mark and what it looks at;
- each chain's steps, approved or still waiting: the skill, the endpoint, the prompt as a template that names canon, `{{<element>: <fact>}}`, never a file or a copied value, the references by artifact, and the request that last ran it.

A chain is a run of dependent requests that ends in published canon, such as a place from its research to its views. Its page, written from the table, shows each step, what it was made from, and how it relates to the chains before it.

## One living pipeline

As the user set on 2026-11-16, a project has one living pipeline, and a change never starts a new one, which would only add bloat and more to keep track of. A project that already holds several, such as Last order's `001` and `002`, keeps the earlier ones as they were made; the highest-numbered is the living one. `pipeline.py new` copies the living pipeline only when the user asks to try a whole alternative direction.

**Canon changes in place.** Publishing a new version of an artifact points its stable name, such as `the diner: floor plan`, at the new file; the file it replaces stays where it is, since nothing in `library/` or `prompts/resources/` is ever removed. Reverting is publishing the earlier file again, or setting the earlier value.

**History is worked out, not kept twice.** The run log, `pipeline/<n>/runs.jsonl`, only added to, has one line per event, with its time: each request a step made, each run of a step, each publish with the file it replaced and each source it was made from with its role, so going back to an older file can put back the sources it was made from, each fact set with the value it replaced, each step edited with its earlier definition, each keep, and each named mark, such as "final look settled". `canon.sql`'s git history covers anything older. `pipeline.py history` lists both, and `pipeline.py sql --as-of <time>` reads canon as it stood at a time. Git holds only what is committed, so after a publish the agent offers a commit of what it wrote, by path, and makes it on the user's yes; the run log keeps whatever falls between commits.

**Out of date is computed, never stored.** For each published artifact, `pipeline.py` reads the record that made it, its report or its line in `records.jsonl`, and compares:
- each input it was made from, by sha256, with what is published now; where a report holds no sha256, by path, since a published file is never overwritten;
- what its step would send if filled now, on the prompt, the model, the settings, and the references, with what its report says was sent;
- each fact it settles, and each fact of an element it shows, as it was when the artifact was made, from the run log, with its value now.

`pipeline.py touches <n> --json` with no change named lists everything out of date this way, with why, and everything with no record to compare as "unverified", never as current. A setup and an agent read the same answer from the same project. With a change named, `touches` lists what that change would reach.

**Each flagged artifact has three answers:**
- make it again: `pipeline.py rerun` makes a take of the first step out of date, upstream first, and stops, so the step below is made from the newly published upstream;
- keep it: `pipeline.py keep`, with a reason, records the inputs, the filled step, and the facts it was accepted against, so a later change to any of them flags it again;
- revert the change that flagged it.

**Publishing a take checks it.** `publish` refuses a take whose inputs are no longer what is published, or whose step was edited since it was made, and names which; `--with` publishes it together with the takes of the inputs it was made from, each checked against the sha256 the take recorded. A file made without a model is published only when its record holds each source it is said to be made from.

## The audit

`project-brief` compares the brief with the pipeline's canon. What the brief asks for that canon does not show, or shows differently, becomes a request.
