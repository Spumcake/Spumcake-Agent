---
name: review-consistency
description: Check that everything said about a film agrees with what is canonical - every fact has one home, the brief page's sections for intent, the pipeline's table for facts, published artifacts, and what each image shows, each canonical element's published images for how it looks - and find each statement in a brief section, a story document, a style guide, or a prompt template that contradicts its home or is repeated outside it, each canonical value a template types instead of naming it, each thing the story needs that no canonical image holds, two canonical images of one element that disagree, and each step built on a result that was never published or was replaced; then report each with what it should be. Use at the end of every step that writes a document or a prompt, and whenever the user asks. Not for judging a new image or clip, which review-continuity checks, and never for fixing what it finds.
---

# Canonical consistency

A film's facts drift when they are written down twice, or written down differently from what was made: one copy changes, the other does not, and a later step builds on the wrong one. A mood that retells the story can contradict the brief the moment the brief changes; a style guide that restates a palette keeps the old palette after the visual identity moves on. This skill finds every fact outside its one home, and every statement that disagrees with it, and reports them. It never fixes, scores, or decides.

A consistent film reads like a set of documents each doing one job: the brief says what happens, the mood says only how it feels, the identity sections say what the picture and the sound must do, and each later artifact names where it takes its facts from. An inconsistent one tells the story in five places, in five slightly different ways. A good report lists every such difference, where it is, which home it breaks, and what it should be; a failed one fixes things, misses a typed value in a template, or judges which version is better.

## The homes

Each fact lives in one place, the one whose job it is:

- **the brief page,** one home per section, for intent:
  - **the brief:** the premise, the characters, the setting, the time of day, the length, every spoken line, and what the user fixed about tone;
  - **the mood:** genre and tone, references, and how light, colour, and camera feel; never the story, the setting, or the sound;
  - **the visual identity:** what the picture must do: the feeling at each moment, the eye, the tension, what it must never be, the colour's intent, and the palette candidates;
  - **the audio identity:** what the sound is for: the feeling at each moment, silence, the turn, music, and what it must never sound like;
  - **the voices:** each character's voice, and the delivery of each of their lines and non-verbal sounds;
  - **the sound design:** every sound, cue by cue: its time, length, place, level, and what it does, the room tone, silence, and the mix;
  - **the timing:** every moment, cue, line, and frame on one timeline, and each frame's blocking;
- **the pipeline's table,** for everything canonical:
  - **each fact,** `<element>: <fact>`, with the artifact that settles it;
  - **each published artifact,** `<element>: <role>`, the home of what it settles: the beat sheet, script, and shot list (`<film>: beat sheet`, `<film>: script`, `<film>: shot list`) for what happens, in what order, in which shot; the breakdown (`<film>: breakdown`) for which characters, places, and props recur; the style guide (`<look>: style guide`) for the look's rules; each place's floor plan (`<place>: floor plan`) for where everything is, what each thing is called, each camera, and each character's marks, so a statement that calls a thing by another name, or says "the door" where the place has several, is a finding;
  - **what each published image shows:** its camera, and each named thing in its frame, where it is, its state, and what it looks at;
  - **what exists and its status:** published or not; nothing else is canon;
- **each canonical element's published images:** how that element looks: its objects, their shapes, colours, materials, and number, as its primary canonical image, its views, and its passes show them, or a character's A-pose views, or a prop's sheet. The images outrank any description of them: a document or a template that describes a canonical element differently is wrong, not the image.

When the setup has its own homes for some facts, use them, and name them in the report.

## What may repeat

A prompt as sent restates what the model needs, since a model cannot follow a pointer. Its template does not: a step's template names each canonical value as `{{<element>: <fact>}}`, filled from the pipeline's table, and each reference by its artifact. A statement in a prompt template that types a canonical value, such as a name, a side of the frame, or a colour, instead of `{{<element>: <fact>}}`, is a finding, even when the value agrees. Everything else points: "the visitor stays unseen (the brief)", not the brief's sentence copied.

## What it needs

- the result under review: a brief section's draft, a story document, a style guide, or a step's prompt template, by its request or its canonical name;
- the brief page, every section;
- the pipeline's table, read with `pipeline.py`: the facts, the published artifacts and what each was made from, what each published image shows, and each chain's steps with their templates and references;
- each canonical element's published images, such as `<place>: primary canonical location` and `<character>: A-pose front`.

## 1. Gather

Read the result under review in full, and every brief section and published document it touches. From the pipeline's table, list the published artifacts and facts it names or should name, each step's template and references, and what each published image shows. Look at each canonical image the result describes, and compare it with what the table says it shows; write down, for this check only, anything it shows that words could state and the table does not: each object, its colour and material, how many there are, and anything the story needs.

## 2. Check

For every fact the result states, find its home, and sort it:

- **at home:** stated where it belongs;
- **repeated:** stated outside its home, in a document that is not a prompt; even when it agrees, it is drift waiting to happen;
- **contradicted:** stated outside its home differently from the home, or two homes disagree;
- **out of scope:** stated in a section or document whose job excludes it, such as story in the mood or sound in the visual identity;
- **built on an unpublished or replaced result:** made from a result the pipeline's table does not hold as published, or from one a later publish replaced, as what each artifact was made from shows; a rejected result is never an input;
- **typed canon:** a template that types a canonical value instead of `{{<element>: <fact>}}`, or names a reference by a file instead of its artifact;
- **prompt mismatch:** a template restating a fact differently from its home, or with no source for it, such as a template that calls a counter "red" when its canonical image shows it cream with a red stripe;
- **missing from the canon:** something the brief or the beat sheet needs on screen, such as a bell or a light it names, that no canonical image holds;
- **two canons disagree:** two published images of the same element that show it differently, such as a prop's sheet and the character who carries it, or an image and what the table says it shows.

Also report a fact the table holds twice, under two names or settled by two artifacts: one should be the fact, the other a pointer to it.

## 3. Report

Fill [the report template](templates/consistency-report.md): each finding with the fact, where it is stated, the home it breaks, what it should be, and whether it blocks approval. Contradictions and two canons that disagree come first, each with the canonical image named beside the statement that contradicts it: only the user decides when two canons disagree, or when a home itself may be wrong. Say what each finding should be, never make it so: a repeated or out-of-scope statement becomes a pointer to its home; a typed value becomes its `{{<element>: <fact>}}`, added to the table first if it is not there; a missing element goes to `make-canonical`; a result built on a replaced one is listed by `pipeline.py touches` for the steps to run again. A prompt already sent stays as its report holds it; the finding is against its template, for the next run.

## Hand back

The findings, in [the report template](templates/consistency-report.md), each with where it is, which canon it breaks, what it should be, and whether it blocks approval; or that there are none.
