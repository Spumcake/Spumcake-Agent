---
name: project-pipeline
description: Publish and keep a project's canon - pipeline/<n>/canon.sql, the table of every published canonical element, artifact, fact, and what each image shows, with what each was made from and each chain's steps as templates that name canon; and the chain pages written from it - publish only what the user approved, list everything a change touches, and start and run again a new pipeline when a change contradicts canon. Use when the user approves a result, when a request needs canon, when the user asks what a change would affect, and when a brief change starts a new pipeline. Not for running a single request (project-requests) or for the brief (project-brief).
---

# The pipeline

The pipeline is what is canon. Each published result, each canonical fact, and each step that makes them is in one table, so a fact has one home and a change says exactly what it reaches. Only this skill writes `pipeline/`, always through [`scripts/pipeline.py`](../../scripts/pipeline.py).

## What it holds

`pipeline/<n>/` holds `canon.sql` and one page per chain, `<nn>-<chain>.html`. What canon points at is in `library/`, when a model made it, or in `prompts/resources/`, when the agent or a builder did, such as a floor plan or a pre-vis render; a chain's builders are resources too. The table holds:

- **elements:** each canonical place, character, prop, look, story, or sound, and parts of them, such as a door;
- **artifacts:** each published result, named `<element>: <role>`, such as `the diner: primary canonical location`, with its file in `library/` or `prompts/resources/`, its request, when it was published, and what it was made from, each source with its role;
- **facts:** each element's canonical facts, `<element>: <fact>`, such as `the front door: side in the far-end frame`, each with the artifact that settles it;
- **contents:** what each published image shows: its camera, and each named thing in its frame, where it is, its state, and, for a character, its mark and what it looks at;
- **chains and steps:** each chain, in order, and each step in it, approved or still waiting: its skill, its endpoint, its prompt as a template, its references by artifact, the request that last ran it, and the artifact it published.

## Templates name canon

A step's prompt names each canonical value as `{{<element>: <fact>}}` and each reference by its artifact, never by a file name or a copied value: "Otis looks back at the front door, on the {{the front door: side in the far-end frame}} of the frame". `pipeline.py fill` fills it from the pipeline's own table, so a step run in a new pipeline reads that pipeline's canon. A value a prompt needs that the table does not hold is added as a fact first, with the artifact that settles it, never typed into the prompt.

## Publishing

Publish only what the user approved, right after their yes:

1. `pipeline.py publish <n> "<element>: <role>" --file library/<file> --request <id> --chain <chain> --from "<source artifact>" <role>...`
2. The facts the result settles, with `pipeline.py fact`, and for an image, what it shows, with `pipeline.py content`, each thing by its canonical name; a door is "the front door", never "the door" where a place has several.
3. The step that made it, with `pipeline.py step`, its template naming canon.
4. `pipeline.py render <n>`, which writes the chain pages again from the table.

A result the user has not approved is never published; its step is recorded as waiting.

## What a change touches

`pipeline.py touches <n> --fact "<element>: <fact>"` or `--artifact "<element>: <role>"` lists every published artifact and step the change reaches: the artifact that settles the fact, every image that shows the element, everything made from those, and every step whose template or references use any of them. Show the user the list before anything is made again.

## A new pipeline

When a brief change contradicts published canon, `project-brief` starts the next brief, and this skill:

1. `pipeline.py new <next>`: the folder starts as a copy of the one before.
2. Sets the changed facts in the new table.
3. `pipeline.py touches` the change, and shows the user the steps to run again, with their cost.
4. `pipeline.py rerun <next> --fact ... --next` runs the first touched step, filled from the new table, as a request; after the user approves and it is published, the next. With `--stand-in`, the whole chain runs as a dry run that spends nothing.

The earlier pipeline is never changed.
