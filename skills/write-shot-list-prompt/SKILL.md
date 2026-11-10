---
name: write-shot-list-prompt
description: Plan an approved script's shot list and build the prompt a language model runs to write it - every shot numbered by scene, with its length in seconds, framing, angle, one camera move, the action, the lines it covers marked on or off screen, its characters, props, and place - then check that it covers every line once and adds up to the film's length, and take it to the user for correction. Use when the user asks for a shot list, a shot breakdown, or coverage of a scene. Not a script or the boards.
---

# Shot list prompt

A shot list says how the script will be filmed: every shot, in order, with how long it lasts and what the camera does. The boards draw one frame for each shot, and the animatic times those boards to the lengths here, so the shot list sets the film's rhythm before anything is drawn.

This skill does not write the shot list. It plans it, builds the prompt that a language model runs to write it, checks what comes back, and stops at the user's approval.

A good shot list covers every moment of the script, and every spoken line falls in exactly one shot. Each shot has one job and one camera move, since a short generated clip holds one move well and several badly. Its lengths add up to the film's length.

## Find the specifics

The setup provides the language model that runs the prompt, and the renderer that sends it and says what it costs; see the [prompt roles](../../docs/prompt-roles.md). The language model may be the agent itself, when the setup says so. If either is missing, say which and stop.

## What it needs

From the caller:

- an approved script; with none, one is planned and approved first;
- the film's length;
- the concept's style guide, when there is one, for how the camera behaves, such as still and composed or loose and handheld;
- a folder for the prompt, the answer, and the shot list.

Every character who reads as a minor stays in ordinary, everyday situations. Nothing about them is sexual or suggestive, in any shot.

## 1. Plan

From the script, note its scenes and their numbers, its spoken lines, and the names it lists for characters, props, and places. Estimate each scene's share of the length, timing a spoken line at about two and a half words a second, plus a short pause before and after.

## 2. Build the prompt

Fill [the shot list prompt template](templates/shot-list-prompt.md) with the approved script, the length, the style guide's camera, and [the shot list template](templates/shot-list.md) as the exact form of the answer. The template carries the rules every shot follows. Save the prompt beside the answer it will produce.

## 3. Run it

Plan the run: the model, and the cost when it bills. Run it on the user's yes when it costs anything, with the setup's renderer. Send only the saved prompt, as a fresh request, so the answer depends on nothing but the prompt. When the agent itself is the language model, it answers the saved prompt alone, as if it had seen nothing else of the conversation.

## 4. Check the answer

Before showing it, check that:

- every shot is numbered by its scene, such as `3-1`, and has a length in whole seconds, a framing, an angle, one camera move or still, an action, its lines, and its characters, props, and place by the script's names;
- every action and every spoken line of the script is in a shot, once, quoted word for word, and marked *on screen* or *off screen*;
- each scene opens on a shot that shows where it is, unless the style guide or the script says otherwise;
- every change of framing, angle, or camera position, and every camera move, has its reason written in the shot's action, from the script or the user; a change with no reason is a failed check, since a camera change must be deliberate;
- the lengths add up to the film's length, within a few seconds; and a shot longer than 10 seconds says why.

When a check fails, build a corrected prompt that says what was wrong, and run it again. When it runs over or short, say where, and what you would cut or hold.

## 5. The user's review

Show the shot list with its total length and the shots you were least sure of. The user's corrections win. A correction the user writes is made in the shot list directly; a larger change is a new prompt. Revise until they approve it, and mark it approved with the date.

Once approved, a shot keeps its number, since its board and clip are named by it. When the script changes later, build a revision prompt from [the same template](templates/shot-list-prompt.md). Its revision part says: "Revise the approved shot list below for this change to the script: <the change>. Change only the shots it touches. Keep every other shot as it was, and every shot's number; a new shot between 3-2 and 3-3 is 3-2A, and a cut shot's number is not used again." Then the approved shot list. For a first draft, the revision part is empty. Check that every other shot came back unchanged, and list what changed.

## 6. Hand back

Hand back the approved shot list, and the prompts that made it.
