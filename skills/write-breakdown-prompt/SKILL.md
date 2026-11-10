---
name: write-breakdown-prompt
description: Plan a film's breakdown from its approved script and shot list, and build the prompt a language model runs to write it - every recurring character, place, and prop, what each must be in general, what the story names about it, such as a light that buzzes or a bell over a door, and the shots it appears in - then check the breakdown that comes back and take it to the user for correction. Use when the user asks for a breakdown, a list of what a film needs, or what must be designed before concept art. Not a script, a shot list, or a design.
---

# Breakdown prompt

A breakdown lists everything a film must have made before its shots can be drawn: each recurring character, place, and prop, what each must be, and the shots it appears in. Every canonical element is made from it, one at a time, and the story check that starts each one reads it. What the breakdown leaves out is costly to add later, once a place's or a character's canonical images are approved.

This skill does not write the breakdown. It plans it, builds the prompt that a language model runs to write it, checks what comes back, and stops at the user's approval.

A good breakdown names every element the script and shot list name, by the same names, and nothing they do not. For each, it says what the story needs it to be and do, not how it looks: "a pendant lamp above the counter that buzzes and flickers", not its colour. It lists every prop a character handles and every light, door, or sound source the beats name. A failed one leaves out the bell the story turns on.

## Find the specifics

The setup provides the language model that runs the prompt, and the renderer that sends it and says what it costs; see the [prompt roles](../../docs/prompt-roles.md). The language model may be the agent itself, when the setup says so. If either is missing, say which and stop.

## What it needs

From the caller:

- the approved script and shot list; with none, they are planned and approved first;
- the approved beat sheet and the brief;
- the concept's style guide, when there is one, for anything it requires in a place, such as a kind of light;
- a folder for the prompt, the answer, and the breakdown.

## 1. Plan

From the script and shot list, list the names the breakdown must cover: each character, each place, each prop. A character who is never seen, such as a voice off screen, is listed with what is heard of them, and marked as never designed.

## 2. Build the prompt

Fill [the breakdown prompt template](templates/breakdown-prompt.md) with the script, the shot list, the beat sheet, the brief, the style guide's requirements, the lists above, and [the breakdown template](templates/breakdown.md) as the exact form of the answer. Save the prompt beside the answer it will produce.

## 3. Run it

Plan the run: the model, and the cost when it bills. Run it on the user's yes when it costs anything, with the setup's renderer. Send only the saved prompt, as a fresh request. When the agent itself is the language model, it answers the saved prompt alone, as if it had seen nothing else of the conversation.

## 4. Check the answer

Before showing it, check that:

- every character, place, and prop the script and shot list name is there, by the same name, and nothing else is;
- each has what it must be, what the story names about it, and every shot it appears in, by shot number;
- each place lists every element the story needs in it: the props used there, each light the story names, each door, window, or sound source that matters;
- each character lists the props they carry or handle, and what the story names about their body, dress, or manner;
- each prop is marked small, with few details, or large;
- anything the script does not have is marked *proposed*.

When a check fails, build a corrected prompt that says what was wrong, and run it again.

## 5. The user's review

Show the breakdown. The user's corrections win; a correction to the story goes back to the script, not into the breakdown. Record the approval and its date in the breakdown.

## Hand back

- the approved breakdown;
- the prompt and the answer it was made from.

Each element is then made canonical in turn, a place first when characters are staged in it, and its story check reads this breakdown.
