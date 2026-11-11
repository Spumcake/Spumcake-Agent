---
name: check-canonical-consistency
description: Check that everything said about a film agrees with what is canonical - every fact has one home, the brief for the story, the identity briefs for intent, each canonical element's approved images for how it looks - and find each statement in a brief, a style guide, a prompt, or the film map that contradicts its home or is repeated outside it, each thing the story needs that no canonical image holds, two canonical images of one element that disagree, and each step built on a superseded version; then fix them by pointing to the home. Use at the end of every step that writes a document or a prompt, and whenever the user asks. Not for judging a new image or clip, which review-continuity checks.
---

# Canonical consistency

A film's facts drift when they are written down twice, or written down differently from what was made: one copy changes, the other does not, and a later step builds on the wrong one. A mood brief that retells the story can contradict the brief the moment the brief changes; a style guide that restates a palette keeps the old palette after the identity brief moves on. This skill keeps one home for every fact and makes every other artifact point to it.

A consistent film reads like a set of documents each doing one job: the brief says what happens, the mood brief says only how it feels, the identity briefs say what the picture and the sound must do, and each later artifact names where it takes its facts from. An inconsistent one tells the story in five places, in five slightly different ways.

## The homes

Each fact lives in one artifact, the one whose job it is:

- **the brief:** the premise, the characters, the setting, the time of day, the length, every spoken line, and what the user fixed about tone;
- **the mood brief:** the mood only: genre and tone, references, and how light, colour, and camera feel; never the story, the setting, or the sound;
- **the visual identity brief:** what the picture must do: the feeling at each moment, the eye, the tension, what it must never be, the colour's intent, and the palette candidates;
- **the audio identity brief:** everything heard: sound design, music, voice direction, and the voices;
- **the beat sheet, script, and shot list:** what happens, in what order, in which shot;
- **the style guide:** the look's rules;
- **the breakdown:** which characters, places, and props recur;
- **each canonical element's approved images:** how that element looks: its objects, their shapes, colours, materials, and number, as its primary canonical image, its views, and its passes show them, or a character's A-pose views, or a prop's sheet. The images outrank any description of them: a document or a prompt that describes a canonical element differently is wrong, not the image;
- **the film map:** what exists, its status, and where it is.

When the setup has its own homes for some facts, use them, and write them in the film map.

## What may repeat

A prompt must restate what it sends to a model, since a model cannot follow a pointer: a prompt may repeat established facts, as long as each matches its home and the prompt's sources say where it came from. Everything else points: "the visitor stays unseen (the brief)", not the brief's sentence copied.

## 1. Gather

From the film map, list every artifact of the film that is approved or waiting, with its path: the documents, the prompts that made or will make its images, and each canonical element's approved images. Read each document and prompt in full. Look at each canonical image, and write down, for this check only, what it shows that words could state: each object, its colour and material, how many there are, and anything the story needs.

## 2. Check

For every fact each artifact states, find its home, and sort it:

- **at home:** stated where it belongs;
- **repeated:** stated outside its home, in a document that is not a prompt; even when it agrees, it is drift waiting to happen;
- **contradicted:** stated outside its home differently from the home, or two homes disagree;
- **out of scope:** stated in an artifact whose job excludes it, such as story in a mood brief or sound in a visual brief;
- **built on a superseded version:** an artifact made from a version the film map marks rejected or replaced;
- **prompt mismatch:** a prompt restating a fact differently from its home, or with no source for it, such as a prompt that calls a counter "red" when its canonical image shows it cream with a red stripe;
- **missing from the canon:** something the brief or the beat sheet needs on screen, such as a bell or a light it names, that no canonical image holds;
- **two canons disagree:** two approved images of the same element that show it differently, such as a prop's sheet and the character who carries it.

Also report two copies of the same file in two places: one becomes the file, the other a pointer, and the film map names the one that counts.

## 3. Report

Fill [the report template](templates/consistency-report.md): each finding with the fact, where it is stated, its home, and the fix. Show the user every contradiction first, with the canonical image beside the statement that contradicts it: only the user decides when two canons disagree, or when a home itself may be wrong.

## 4. Fix

Fix each repeated or out-of-scope statement by deleting it or replacing it with a pointer to its home. Fix a statement that contradicts a canonical image to match the image. Fix two disagreeing canons, or a missing one, only as the user decides; a missing element goes back to `make-canonical`. Mark each artifact built on a superseded version in the film map as needing to be made again. Do not touch a prompt that has already been sent: record the mismatch beside it, and fix the prompt's template or source for the next run. Then check again until the report is empty.

## Hand back

- the report, with every finding and its fix;
- the artifacts fixed, each with what changed;
- the film map, updated.
