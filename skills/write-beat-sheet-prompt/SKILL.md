---
name: write-beat-sheet-prompt
description: Plan a story's beat sheet and build the prompt a language model runs to write it - the brief, the length, the number of beats, the rules every beat follows, and the exact form of the answer - then check the beat sheet that comes back and take it to the user for correction. Use when the user asks for a beat sheet, a story outline, or the structure of a short, an episode, or a pilot. Not a script or a shot list.
---

# Beat sheet prompt

A beat is one turn in the story: something happens, and afterwards things are different for someone. A beat sheet lists a story's beats in order, so its shape can be judged and changed before anything is written in full. It is the cheapest place to fix a story, and everything after it, the script, the shot list, and the boards, is built from it.

This skill does not write the beat sheet. It plans it, builds the prompt that a language model runs to write it, checks what comes back, and stops at the user's approval. The approved beat sheet stays a library document, published as canon, `<film>: beat sheet`, by `project-pipeline`.

A good beat sheet can be read in a minute. Every beat changes something; a beat where nothing turns is cut or merged. The beats add up to the film's length, and the ending pays off what the opening sets up.

## Find the specifics

The setup provides the language model that runs the prompt, its limits, and what a run costs; see the [prompt roles](../../docs/prompt-roles.md). The language model may be the agent itself, when the setup says so. If it is missing, say so and stop. This skill builds the request and hands it back; `project-requests` runs it with `scripts/request.py`, which sends it exactly as built.

## What it needs

- the brief: the brief page's first section, with the premise, the main characters, the length, the genre and tone, and who it is for;
- the style guide (`<look>: style guide`), when it is published, for its tone.

Ask for the length and the ending's direction when the brief leaves them open; never let the model invent the ending of someone's story. Everything else the brief leaves open, the model proposes, marked *proposed*.

Characters who read as minors are kept as the [prompt roles](../../docs/prompt-roles.md) say.

## 1. Plan

Choose the number of beats from the length:

- under 1 minute: 2 or 3 beats;
- 1 to 2 minutes: 4 to 6 beats;
- 2 to 5 minutes: 6 to 10;
- 5 to 12 minutes: 10 to 15;
- longer: about one beat a minute, grouped into acts.

## 2. Build the prompt

Fill [the beat sheet prompt template](templates/beat-sheet-prompt.md) with the brief, the length, the number of beats, the ending's direction, the style guide's tone, and [the beat sheet template](templates/beat-sheet.md) as the exact form of the answer. The template carries the rules every beat follows. The brief and the tone are filled from the brief page and the style guide as they stand; a canonical value the pipeline's table already holds, such as the length, is written as `{{<element>: <fact>}}`, such as `{{<film>: length}}`, never typed in by hand.

## 3. Hand it to be run

Hand the prompt back as the request: the model, and the cost from the setup when it bills. `project-requests` runs it on the user's yes when it costs anything, sent alone as the [prompt roles](../../docs/prompt-roles.md) say, and its report holds the answer.

## 4. Check the answer

Before handing it back, check that:

- it has the planned number of beats, numbered, in the template's form;
- every beat says what happens, whose beat it is, its turn, and when it starts, and the times add up to the length;
- the beats are events, not shots or lines;
- the ending follows the direction the user gave, and anything the brief left open is marked *proposed*.

When a check fails, correct the prompt as the [prompt roles](../../docs/prompt-roles.md) say.

## 5. The user's review

Give the beat sheet back with one sentence on its shape: where it turns, and where the ending is set up. The user's corrections win. A correction the user writes is a new request, the corrected beat sheet written by the agent; a larger change is a new prompt. Revise until they approve it. The approved beat sheet is published by `project-pipeline`; a rejected one is never used as an input again.

Once approved, a beat keeps its number, since the script names the beats it serves. A beat added between 3 and 4 is 3A; a cut beat's number is not used again. When the brief changes later, build a revision prompt from [the same template](templates/beat-sheet-prompt.md). Its revision part says: "Revise the approved beat sheet below for this change: <the change>. Change only the beats it touches. Keep every other beat word for word, and every beat's number; a new beat between 3 and 4 is 3A, and a cut beat's number is not used again." Then the approved beat sheet. For a first draft, the revision part is empty. Check that every other beat came back word for word, and list what changed.

## Hand back

- the prompt, as a template naming canon, and the language model's answer: the beat sheet, with the checks it passed;
- for a revision, what changed, beat by beat;
- the facts it settles, by `<element>: <fact>`, for `project-pipeline` to publish: `<film>: beat count` and `<film>: ending`, and `<film>: length` when the table does not hold it yet.
