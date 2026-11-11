---
name: write-script-prompt
description: Plan a film's script from its approved beat sheet and build the prompt a language model runs to write it - the beats, the characters, places, and props to name, the screenplay form, and the rule that every spoken line is the line that will be voiced - then check the script that comes back and take it to the user for correction. Use when the user asks for a script, a screenplay, dialogue, or a draft of a short, an episode, or a pilot. Not a beat sheet or a shot list.
---

# Script prompt

A script turns the beats into scenes: where each happens, what is seen, and what is said. Every later stage reads it: the shot list breaks its scenes into shots, the voices speak its lines, and lip-sync matches them. So a spoken line in the script is the line that will be voiced, word for word.

This skill does not write the script. It plans it, builds the prompt that a language model runs to write it, checks what comes back, and stops at the user's approval.

A good script follows the approved beats, in order, and every scene serves at least one of them. What is seen is written as action the camera can show, not as thoughts. Lines are short and sound like the character. It runs about one page a minute.

## Find the specifics

The setup provides the language model that runs the prompt, and the renderer that sends it and says what it costs; see the [prompt roles](../../docs/prompt-roles.md). The language model may be the agent itself, when the setup says so. If either is missing, say which and stop.

## What it needs

From the caller:

- an approved beat sheet; with none, one is planned and approved first;
- the brief, for the characters and their voices;
- the concept's style guide, when there is one, for tone and for how places look;
- a folder for the prompt, the answer, and the script.

Characters who read as minors are kept as the [prompt roles](../../docs/prompt-roles.md) say.

## 1. Plan

From the beat sheet and the brief, list what the script must name, so every later stage finds it by the same name:

- each character who appears, speaking or not;
- each place;
- each prop or object that recurs or matters to the story.

Set its length: about one page a minute of the film.

## 2. Build the prompt

Fill [the script prompt template](templates/script-prompt.md) with the approved beat sheet, the brief, the lists above, the length, the style guide's tone, and [the script template](templates/script.md) as the exact form of the answer. The template carries the screenplay form and the rules for spoken lines. Save the prompt beside the answer it will produce.

## 3. Run it

Plan the run: the model, and the cost when it bills. Run it on the user's yes when it costs anything, with the setup's renderer. Send it as the [prompt roles](../../docs/prompt-roles.md) say.

## 4. Check the answer

Before showing it, check that:

- it lists every character, place, and prop from the plan, and uses those names exactly everywhere;
- every scene is numbered, has a heading with its place, `INT.` or `EXT.`, and `DAY` or `NIGHT`, and names the beats it serves;
- every approved beat is served, in order, and the ending is the beat sheet's;
- every spoken line has its speaker, `(O.S.)` or `(V.O.)` where the speaker is not seen, and no ellipses or emoji;
- anything the beats do not have is marked *proposed*;
- it runs about the planned length.

When a check fails, correct the prompt as the [prompt roles](../../docs/prompt-roles.md) say.

## 5. The user's review

Show the script with its running length and any proposed additions. The user's corrections win. A correction the user writes is made in the script directly; a larger change is a new prompt. Revise until they approve it, and mark it approved with the date. Once a shot list is made from it, a change to a spoken line is a new version of the script, since voices and lip-sync follow it.

Once approved, a scene keeps its number, since the shot list and the boards are numbered by it. When the beat sheet changes later, build a revision prompt from [the same template](templates/script-prompt.md). Its revision part says: "Revise the approved script below for this change: <the change>. Change only the scenes it touches. Keep every other scene and every unaffected line word for word, and every scene's number; a new scene between 3 and 4 is 3A, and a cut scene's number is not used again." Then the approved script. For a first draft, the revision part is empty. Check that every other scene and line came back word for word, and list what changed.

## 6. Hand back

Hand back the approved script, and the prompts that made it.
