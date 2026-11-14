---
name: write-breakdown-prompt
description: Plan a film's breakdown from its approved script and shot list, and build the prompt a language model runs to write it - every recurring character, place, and prop, what each must be in general, what the story names about it, such as a light that buzzes or a bell over a door, and the shots it appears in - then check the breakdown that comes back and take it to the user for correction. Use when the user asks for a breakdown, a list of what a film needs, or what must be designed before concept art. Not a script, a shot list, or a design.
---

# Breakdown prompt

A breakdown lists everything a film must have made before its shots can be drawn: each recurring character, place, and prop, what each must be, and the shots it appears in. Every canonical element is made from it, one at a time, and the story check that starts each one reads it. What the breakdown leaves out is costly to add later, once a place's or a character's canonical images are approved.

This skill does not write the breakdown. It plans it, builds the prompt that a language model runs to write it, checks what comes back, and stops at the user's approval. The approved breakdown stays a library document, published as canon, `<film>: breakdown`, by `project-pipeline`.

A good breakdown names every element the script and shot list name, by the same names, and nothing they do not. For each, it says what the story needs it to be and do, not how it looks: "a pendant lamp above the counter that buzzes and flickers", not its colour. It lists every prop a character handles and every light, door, or sound source the beats name. A failed one leaves out the bell the story turns on.

## Find the specifics

The setup provides the language model that runs the prompt, its limits, and what a run costs; see the [prompt roles](../../docs/prompt-roles.md). The language model may be the agent itself, when the setup says so. If it is missing, say so and stop. This skill builds the request and hands it back; `project-requests` runs it with `scripts/request.py`, which sends it exactly as built.

## What it needs

- the script (`<film>: script`) and the shot list (`<film>: shot list`), published; with none, they are planned and approved first;
- the beat sheet (`<film>: beat sheet`) and the brief, the brief page's first section;
- the style guide (`<look>: style guide`), when it is published, for anything it requires in a place, such as a kind of light.

## 1. Plan

From the script and shot list, list the names the breakdown must cover: each character, each place, each prop. A character who is never seen, such as a voice off screen, is listed with what is heard of them, and marked as never designed.

Give each recurring element one name, and each door, window, or opening the story uses its own name, such as "the front door", never "the door": the pipeline's table keeps these names as elements, the place's floor plan uses them, and every later document and prompt names them as canon.

## 2. Build the prompt

Fill [the breakdown prompt template](templates/breakdown-prompt.md) with the script, the shot list, the beat sheet, the brief, the style guide's requirements, the lists above, and [the breakdown template](templates/breakdown.md) as the exact form of the answer. The documents go in as their published artifacts, `<film>: script`, `<film>: shot list`, and `<film>: beat sheet`, and a canonical value, such as the length, as `{{<film>: length}}`, never typed in by hand.

## 3. Hand it to be run

Hand the prompt back as the request: the model, and the cost from the setup when it bills. `project-requests` runs it on the user's yes when it costs anything, sent alone as the [prompt roles](../../docs/prompt-roles.md) say, and its report holds the answer.

## 4. Check the answer

Before handing it back, check that:

- every character, place, and prop the script and shot list name is there, by the same name, and nothing else is;
- each has what it must be, what the story names about it, and every shot it appears in, by shot number;
- each place lists every element the story needs in it: the props used there, each light the story names, each door, window, or sound source that matters;
- each character lists the props they carry or handle, and what the story names about their body, dress, or manner;
- each prop is marked small, with few details, or large;
- anything the script does not have is marked *proposed*.

When a check fails, correct the prompt as the [prompt roles](../../docs/prompt-roles.md) say.

## 5. The user's review

Give the breakdown back. The user's corrections win; a correction to the story goes back to the script, not into the breakdown. The approved breakdown is published by `project-pipeline`; a rejected one is never used as an input again.

Each element is then made canonical in turn, a place first when characters are staged in it, and its story check reads this breakdown.

## Hand back

- the prompt, as a template naming canon, and the language model's answer: the breakdown, with the checks it passed;
- the facts it settles, by `<element>: <fact>`, for `project-pipeline` to publish: each character, place, prop, and named door, window, light, or sound source, as an element of the pipeline's table, and each prop's size, such as `<prop>: size`, small or large.
