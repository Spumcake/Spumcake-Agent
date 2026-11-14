---
name: project-requests
description: Run what the user asks for as requests - split the message into requests, name each, order them by what each needs from another, choose each request's skill by its category, run each as one cycle through scripts/request.py, which sends it exactly as built, files its outputs into library/, and writes its report in requests/, then tell the user exactly what the report says and wait for their approval. Use for every request that can make a canonical outcome in a project laid out as docs/projects.md describes, and whenever the user asks what made a file, what was sent, or which references were used. Not for publishing (project-pipeline), the brief (project-brief), or delivering a finished film (project-output).
---

# The request cycle

Every request in a project runs through this skill, and only this skill writes `requests/`. A request is one call to a generative model's endpoint with one prompt: one cycle, one report. What the agent writes or draws itself, and what a builder makes, is not a request: `project-library` files it into `prompts/resources/` when it is canon or is sent to a model, and it is not kept otherwise. The skill a request uses builds its prompt and references and returns them; it saves nothing and records nothing. This skill runs it with [`scripts/request.py`](../../scripts/request.py), so the report holds exactly what was sent, and then says what the report says.

A good cycle leaves a report that answers, without anyone's memory, what was asked, why, what was sent where, what canon it read, and what came back. A failed one has an output with no report, a prompt retyped into the report instead of the one sent, a reference left out, or a summary of the request in place of the request.

## 1. Read the project

Before planning, read:

- the brief, `brief/<latest>-<project>.html`: what the film should be;
- the pipeline's canon: `pipeline.py sql <n> "SELECT id, file FROM artifact"`, the facts, and each chain's steps;
- the requests already made: `request.py list`.

## 2. Split, name, and order

Split the user's message into requests. One message can hold several: "make the keyframes for the bell and the line" is two. For each:

- **its name:** a few words, lowercase, that say what it makes, such as `keyframe-the-line`; `request.py id <name>` gives the ID it will get;
- **its category and skill:** choose the category by what the request must produce, then the skill in it by its description, from [the categories](../../docs/skill-categories.md):
  - a document → `write`;
  - material found outside → `research`;
  - an image or a sound from a model → `generate`;
  - a result made by a script → `build`;
  - a report of differences → `review`;
  - a repair of an existing result → `fix`;
  - one finished thing that needs several of these → `make`, which plans its own requests, each run here as its own cycle;
- **what it needs:** the canon it reads, and any request whose output it takes as a reference.

Order the requests so each runs after everything it needs. Show the user the plan: each request's name, skill, endpoint, and what it needs, with the number of paid calls and their estimated cost. Nothing that costs money runs before the user's yes to that plan.

## 3. Run each request

For each request, in order:

1. **Build.** Have its skill build the prompt and references. When the request is a step of a pipeline's chain, start from `pipeline.py fill <n> <chain> <step>`, which fills the step's template from the canon and lists the canon it read; never copy a canonical value or a file name by hand. A reference is a file in `library/` or `sources/`, given with its role in the request, such as "image 1, the layout of the shot".
2. **Write the spec** as `request.py`'s usage gives it, with what was asked and why in the user's terms.
3. **Run it:** `request.py run <spec.json>`. Its outputs land in `library/`, or `sources/` for research, and its report in `requests/`. Never save, copy, rename, or move an output any other way.
4. **Show it.** When results are easier to judge side by side, make a comparison or a chart and embed it in the report with `request.py attach <id> <file> --as comparison`; it is kept nowhere else.
5. **Review it.** For an image, a clip, or a sound, run `review-continuity` on it as its own request, against the canon the request read.
6. **Tell the user** what `request.py tell <id>` prints, word for word, then the review's findings. Add nothing to it and leave nothing out: it is the endpoint, the references in order, the canon read, the prompt as sent, the outputs, the cost, and the report's path.

## 4. The user's approval

The user approves, rejects, or asks for changes. An approved result goes to `project-pipeline` to be published as canon; nothing is canon before that. A rejected result stays in the library, as every output does, and is never used again as an input. A change is a new request, with its own name and report.

## Answering about a file

When the user asks what made a file, what prompt was sent, or which references were used, answer from `request.py show <file>`, never from memory. When a file has no report, say so.
