---
name: write-beat-sheet-prompt
description: Plan a story's beat sheet and build the prompt a language model runs to write it - the brief, the length, the number of beats, the rules every beat follows, and the exact form of the answer - then check the beat sheet that comes back and take it to the user for correction. Use when the user asks for a beat sheet, a story outline, or the structure of a short, an episode, or a pilot. Not a script or a shot list.
---

# Beat sheet prompt

A beat is one turn in the story: something happens, and afterwards things are different for someone. A beat sheet lists a story's beats in order, so its shape can be judged and changed before anything is written in full. It is the cheapest place to fix a story, and everything after it, the script, the shot list, and the boards, is built from it.

This skill does not write the beat sheet. It plans it, builds the prompt that a language model runs to write it, checks what comes back, and stops at the user's approval.

A good beat sheet can be read in a minute. Every beat changes something; a beat where nothing turns is cut or merged. The beats add up to the film's length, and the ending pays off what the opening sets up.

## Find the specifics

The setup provides the language model that runs the prompt, and the renderer that sends it and says what it costs; see the [prompt roles](../../docs/prompt-roles.md). The language model may be the agent itself, when the setup says so. If either is missing, say which and stop.

## What it needs

From the caller:

- the brief: the premise, the main characters, the length, the genre and tone, and who it is for;
- the concept's style guide, when there is one, for its tone;
- a folder for the prompt, the answer, and the beat sheet.

Ask for the length and the ending's direction when the brief leaves them open; never let the model invent the ending of someone's story. Everything else the brief leaves open, the model proposes, marked *proposed*.

Every character who reads as a minor stays in ordinary, everyday situations. Nothing about them is sexual or suggestive, in any beat.

## 1. Plan

Choose the number of beats from the length:

- under 2 minutes: 4 to 6 beats;
- 2 to 5 minutes: 6 to 10;
- 5 to 12 minutes: 10 to 15;
- longer: about one beat a minute, grouped into acts.

## 2. Build the prompt

Fill [the beat sheet prompt template](templates/beat-sheet-prompt.md) with the brief, the length, the number of beats, the ending's direction, the style guide's tone, and [the beat sheet template](templates/beat-sheet.md) as the exact form of the answer. The template carries the rules every beat follows. Save the prompt beside the answer it will produce.

## 3. Run it

Plan the run: the model, and the cost when it bills. Run it on the user's yes when it costs anything, with the setup's renderer. Send only the saved prompt, as a fresh request, so the answer depends on nothing but the prompt. When the agent itself is the language model, it answers the saved prompt alone, as if it had seen nothing else of the conversation.

## 4. Check the answer

Before showing it, check that:

- it has the planned number of beats, numbered, in the template's form;
- every beat says what happens, whose beat it is, its turn, and when it starts, and the times add up to the length;
- the beats are events, not shots or lines;
- the ending follows the direction the user gave, and anything the brief left open is marked *proposed*.

When a check fails, build a corrected prompt that says what was wrong, and run it again.

## 5. The user's review

Show the beat sheet with one sentence on its shape: where it turns, and where the ending is set up. The user's corrections win. A correction the user writes is made in the beat sheet directly; a larger change is a new prompt. Revise until they approve it, and mark it approved with the date.

Once approved, a beat keeps its number, since the script names the beats it serves. A beat added between 3 and 4 is 3A; a cut beat's number is not used again. When the brief changes later, build a revision prompt from [the same template](templates/beat-sheet-prompt.md). Its revision part says: "Revise the approved beat sheet below for this change: <the change>. Change only the beats it touches. Keep every other beat word for word, and every beat's number; a new beat between 3 and 4 is 3A, and a cut beat's number is not used again." Then the approved beat sheet. For a first draft, the revision part is empty. Check that every other beat came back word for word, and list what changed.

## 6. Hand back

Hand back the approved beat sheet, and the prompts that made it.
