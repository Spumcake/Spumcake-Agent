---
name: project-pipeline
description: Publish and keep a project's canon in its one living pipeline - pipeline/<n>/canon.sql, the table of every published canonical element, artifact, fact, and what each image shows, with what each was made from and each chain's steps as templates that name canon; its run log; and the chain pages written from it - publish only what the user approved, in place, list what is out of date and what a change reaches, and make it again as takes, keep it, or revert. Use when the user approves a result, when a request needs canon, when the user asks what a change would affect or what is out of date, and when canon changes. Not for running a single request (project-requests) or for the brief (project-brief).
---

# The pipeline

The pipeline is what is canon. Each published result, each canonical fact, and each step that makes them is in one table, so a fact has one home and a change says exactly what it reaches. Only this skill writes `pipeline/`, always through [`scripts/pipeline.py`](../../scripts/pipeline.py).

## What it holds

`pipeline/<n>/` holds `canon.sql`, its run log `runs.jsonl`, and one page per chain, `<nn>-<chain>.html`. A project has one living pipeline, the highest-numbered; a change never starts another (the user, 2026-11-16). What canon points at is in `library/`, when a model made it, or in `prompts/resources/`, when the agent or a builder did, such as a floor plan or a pre-vis render; a chain's builders are resources too. The table holds:

- **elements:** each canonical place, character, prop, look, story, or sound, and parts of them, such as a door;
- **artifacts:** each published result, named `<element>: <role>`, such as `the diner: primary canonical location`, with its file in `library/` or `prompts/resources/`, its request, when it was published, and what it was made from, each source with its role;
- **facts:** each element's canonical facts, `<element>: <fact>`, such as `the front door: side in the far-end frame`, each with the artifact that settles it;
- **contents:** what each published image shows: its camera, and each named thing in its frame, where it is, its state, and, for a character, its mark and what it looks at;
- **chains and steps:** each chain, in order, and each step in it, approved or still waiting: its skill, its endpoint, its prompt as a template, its references by artifact, the request that last ran it, and the artifact it published.

## Templates name canon

A step's prompt names each canonical value as `{{<element>: <fact>}}` and each reference by its artifact, never by a file name or a copied value: "Otis looks back at the front door, on the {{the front door: side in the far-end frame}} of the frame". `pipeline.py fill` fills it from the pipeline's own table, so a step always reads canon as it is now. A value a prompt needs that the table does not hold is added as a fact first, with the artifact that settles it, never typed into the prompt.

## Publishing

Publish only what the user approved, right after their yes:

1. `pipeline.py publish <n> "<element>: <role>" --file library/<file> --request <id> --chain <chain> --from "<source artifact>" <role>...`, in place: the file it replaces stays where it is, and the run log names it. It refuses a take whose inputs or step changed since it was made, and names which; publish the inputs' takes with it (`--with "<artifact>=<request id>"`), or make it again. A file made without a model needs its record to hold each source (`request.py resource` or `build --from`). An edit of a published artifact, such as a second pass over a published image, names the artifact itself as what it edited: it is not recorded as made from itself, the run log keeps which version it was made from as `edited_from`, and it may be made from any version of the artifact that was published, never from one that was not.
2. The facts the result settles, with `pipeline.py fact`, and for an image, what it shows, with `pipeline.py content`, each thing by its canonical name; a door is "the front door", never "the door" where a place has several.
3. The step that made it, with `pipeline.py step`, its template naming canon.
4. `pipeline.py render <n>`, which writes the chain pages again from the table.
5. Offer a commit of what the publish wrote, by path, and make it on the user's yes, so git holds the history.

A result the user has not approved is never published; its step is recorded as waiting.

The user's yes may be an action rather than a word, where the setup they work in says so. For example, putting a result into a step of a chain is the yes to publish it as that step's artifact. Saving an edit of the artifact in use, or a fix of it, is the yes to publish it as the artifact's next version. Whichever it is, the publish is the same command, with the same record. A setup that takes the yes this way publishes the moment the user acts, and an agent working in the same project reads that canon as its own.

A result made again because it was out of date is published with `--fixes`, so its run-log event names the version it fixes. It must be a take of the artifact's own step. Another take put into use is published without it, so the two read differently.

Several steps may share one place in a chain, given the same `--order`. They are alternatives made side by side, each with its own artifact, prompt, and references, such as several takes of one frame kept in use together. Each is made, published, made again, and goes out of date on its own: editing one step's template outlines only its own artifact. A second alternative is a new step at the same order, named for it, such as `"<step>, 2"`, with its own artifact, such as `"<element>: <role>, 2"`.

A keyframe step is named `keyframe, <moment>`, and the moment's staging floor plan is published as `<moment>: staging floor plan`. `pipeline.py fill` refuses a keyframe step until that plan is approved and published, so no frame of a moment is ever made without its staging.

## What a change touches, and what is out of date

`pipeline.py touches <n> --fact "<element>: <fact>"` or `--artifact "<element>: <role>"` lists every published artifact and step the change would reach: the artifact that settles the fact, every image that shows the element, everything made from those, and every step whose template or references use any of them. Show the user the list before anything is changed or made again.

`pipeline.py touches <n> --json`, with no change named, lists everything out of date now, with why: an input published again, a step edited, or a fact changed since it was made. It also lists what has no record to compare, as unverified. Read it before every step, and tell the user what it lists.

## Changing canon

Canon changes in place, as [projects.md](../../docs/projects.md) describes:

1. Change it: publish the new version, or set the new fact, on the user's yes. The run log keeps what it replaced.
2. `pipeline.py touches <n> --json` lists what is now out of date. Show it, with what making each again would cost.
3. For each, as the user chooses:
   - **make it again:** `pipeline.py rerun <n>` makes a take of the first step out of date and stops; once the user approves it and it is published, run it again for the step below. With `--stand-in`, a take is a dry run that spends nothing;
   - **keep it:** `pipeline.py keep <n> "<artifact>"... --reason "<why it still holds>"`, which records what it was accepted against, so the next change flags it again;
   - **revert:** publish the earlier file, or set the earlier value, from `pipeline.py history`.

A new project starts with pipeline `001`, which `request.py init` makes. `pipeline.py new` starts another pipeline only when the user asks to try a whole alternative direction; earlier pipelines, such as Last order's `001`, stay as they were made.
