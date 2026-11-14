---
name: write-shot-list-prompt
description: Plan an approved script's shot list and build the prompt a language model runs to write it - every shot numbered by scene, with its length in seconds, framing, angle, one camera move, the action, the lines it covers marked on or off screen, its characters, props, and place - then check that it covers every line once and adds up to the film's length, and take it to the user for correction. Use when the user asks for a shot list, a shot breakdown, or coverage of a scene. Not a script or the boards.
---

# Shot list prompt

A shot list says how the script will be filmed: every shot, in order, with how long it lasts and what the camera does. The boards draw one frame for each shot, and the animatic times those boards to the lengths here, so the shot list sets the film's rhythm before anything is drawn.

This skill does not write the shot list. It plans it, builds the prompt that a language model runs to write it, checks what comes back, and stops at the user's approval. The approved shot list stays a library document, published as canon, `<film>: shot list`, by `project-pipeline`.

A good shot list covers every moment of the script, and every spoken line falls in exactly one shot. Each shot has one job and one camera move, since a short generated clip holds one move well and several badly. Its lengths add up to the film's length.

## Find the specifics

The setup provides the language model that runs the prompt, its limits, and what a run costs; see the [prompt roles](../../docs/prompt-roles.md). The language model may be the agent itself, when the setup says so. If it is missing, say so and stop. This skill builds the request and hands it back; `project-requests` runs it with `scripts/request.py`, which sends it exactly as built.

## What it needs

- the script (`<film>: script`), published; with none, one is planned and approved first;
- the film's length (`<film>: length`);
- the style guide (`<look>: style guide`), when it is published, for how the camera behaves, such as still and composed or loose and handheld.

Characters who read as minors are kept as the [prompt roles](../../docs/prompt-roles.md) say.

## 1. Plan

From the script, note its scenes and their numbers, its spoken lines, and the names it lists for characters, props, and places. Estimate each scene's share of the length, timing a spoken line at about two and a half words a second, plus a short pause before and after.

## 2. Build the prompt

Fill [the shot list prompt template](templates/shot-list-prompt.md) with the approved script, the length, the style guide's camera, and [the shot list template](templates/shot-list.md) as the exact form of the answer. The template carries the rules every shot follows. The script goes in as the published `<film>: script`, and the length as `{{<film>: length}}`, never typed in by hand.

## 3. Hand it to be run

Hand the prompt back as the request: the model, and the cost from the setup when it bills. `project-requests` runs it on the user's yes when it costs anything, sent alone as the [prompt roles](../../docs/prompt-roles.md) say, and its report holds the answer.

## 4. Check the answer

Before handing it back, check that:

- every shot is numbered by its scene, such as `3-1`, and has a length in whole seconds, a framing, an angle, one camera move or still, an action, its lines, and its characters, props, and place by the script's names;
- every action and every spoken line of the script is in a shot, once, quoted word for word, and marked *on screen* or *off screen*;
- each scene opens on a shot that shows where it is, unless the style guide or the script says otherwise;
- every change of framing, angle, or camera position, and every camera move, has its reason written in the shot's action, from the script or the user; a change with no reason is a failed check, since a camera change must be deliberate;
- the lengths add up to the film's length, within a few seconds; and a shot longer than 10 seconds says why.

When a check fails, correct the prompt as the [prompt roles](../../docs/prompt-roles.md) say. When it runs over or short, say where, and what you would cut or hold.

## 5. The user's review

Give the shot list back with its total length and the shots you were least sure of. The user's corrections win. A correction the user writes is a new request, the corrected shot list written by the agent; a larger change is a new prompt. Revise until they approve it. The approved shot list is published by `project-pipeline`; a rejected one is never used as an input again.

Once approved, a shot keeps its number, since its board and clip are named by it. When the script changes later, build a revision prompt from [the same template](templates/shot-list-prompt.md). Its revision part says: "Revise the approved shot list below for this change to the script: <the change>. Change only the shots it touches. Keep every other shot as it was, and every shot's number; a new shot between 3-2 and 3-3 is 3-2A, and a cut shot's number is not used again." Then the approved shot list. For a first draft, the revision part is empty. Check that every other shot came back unchanged, and list what changed.

## Hand back

- the prompt, as a template naming canon, and the language model's answer: the shot list, with the checks it passed and, when it runs over or short, where and what to cut or hold;
- for a revision, what changed, shot by shot;
- the facts it settles, by `<element>: <fact>`, for `project-pipeline` to publish: each shot's length, framing, angle, and camera move, such as `<shot>: framing` and `<shot>: camera move`, so the steps that make its board and clip name them as `{{<shot>: camera move}}`.
