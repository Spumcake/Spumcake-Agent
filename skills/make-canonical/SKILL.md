---
name: make-canonical
description: Make one recurring element of a film canonical - a place, a character, or a prop - one step at a time, so every later image of it holds together - a story check against the breakdown, research, then for a place a pre-vis, its primary canonical location, canonical cleanup, its views, and their neutral passes; for a character its primary canonical image, canonical cleanup, and its A-pose views with their form passes; for a prop its sheet - each step made only from the latest approved result of the one before. Use when the breakdown names a recurring element, before any concept art or staging uses it, and whenever an element's images stop agreeing with each other. Not for exploring a film's look, or its mood.
---

# Make canonical

A film's places, characters, and props must hold together from shot to shot: the same door on the same wall, the same face and apron, the same rag, from every camera. An image model alone cannot keep that. This skill takes one element through the steps that do, in order, and hands on an element that is canonical: one image every other image of it is based on, and views of it from every side the film needs, made neutral so mood and light can be decided later.

A good result reads as that kind of thing in every view, holds everything the story needs of it, and shows the same thing from each camera. A failed one invents what the research does not show, drifts between views, leaves out what the story turns on, or was built on a result that was never approved.

## The rules of the sequence

- **The canonical angle:** A place's primary canonical location, seen from the pre-vis's one good shot, is its canonical angle. Every later step that returns to the place, its mood reference, its concept art, and any other image of it, starts from the canonical angle and its passes, never from another view. A new angle is made only when the user asks for it and approves its camera, and never becomes the place's reference.

- One element at a time, one step at a time. Each step is made only from the latest approved results of the steps before it; a rejected round is never an input to anything.
- When a step fails, the skill that made it is fixed, and the step is run again. A lesson goes into the skill, not around it.
- A place is made canonical before any character is staged in it. No characters appear in a place's images.
- Each step is one or more requests, which `project-requests` runs, one cycle each: every paid request waits for the user's yes to its plan, and every result is shown as its report holds it, with the whole prompt and every image sent. An approved result is published by `project-pipeline` before the next step uses it.

## What it needs

From the caller:

- the element, by the name the script uses, and its entry in the approved breakdown (`<film>: breakdown`);
- the period and setting of the film, from the brief (`<film>: brief`);
- the film's style guide (`<film>: style guide`), when there is one;
- for a character, the canonical place they are first seen in, when there is one, for its texture view (`<place>: texture pass`);
- for a small prop, its character's canonical A-pose set (`<character>: A-pose <view>`).

## 0. The story check

Before anything is researched, list everything the story needs of the element, from its breakdown entry, the beat sheet, and the style guide:

- **a place:** each prop a character uses there, each light the story names, each door, window, or sound source that matters, such as a buzzing light or a bell over a door;
- **a character:** what the story names about their body, dress, and manner, and every prop they carry or handle;
- **a prop:** what it does in the story, and who handles it.

Every item goes into the research, the pre-vis and its key, and the primary canonical image's prompt. Check the list again before the primary canonical image is approved: an item missing then is costly to add later.

## 1. Research

Run `research-references` for the element: a photograph of every item the story check lists, in the film's period, found with short, plain searches. For a place, also its layout, usual sizes, and how it is best shot. For a character, several real people of the archetype, and their clothing and carried things. The user approves the board and the photographs.

## A place

2. **Pre-vis:** run `build-previs` from the approved research: the layout, the mock-up with its key, and one good shot. The user approves the shot.
3. **The primary canonical location:** `generate-canonical-image`'s primary canonical location: the grey shot, the research photographs, the names from the key, and the concept context template for the place. The user chooses one.
4. **Canonical cleanup:** run `fix-canonical-image` on the chosen image, against its canonical prompt and the pre-vis. Fixes for the pre-vis go back to step 2, and the image is made again from the corrected shot. The user approves the cleaned image.
5. **The views:** run `build-previs` for a camera square-on to each wall, and any other camera the user asks for and approves, and make each view from the primary canonical location with `generate-canonical-image`'s new camera. Run `fix-canonical-image` across the views, fixing only major inconsistencies. The user chooses each view.
6. **The neutral passes:** `generate-canonical-image`'s grey form, coloured form, and texture passes on the primary canonical location and each view, then `fix-canonical-image` on the form passes. Surface changes, such as less gloss, are made on the texture passes; mood and light come in the concept art phase.
7. **The floor plan:** run `write-floor-plan` from the pre-vis layout's numbers once the views are approved. Its facts, every door named and each camera's left, centre, and right, are published with it, and every later prompt that places or directs a character takes them from the pipeline's table.

## A character

2. **The primary canonical character:** `generate-canonical-image`'s primary canonical character: one front view, from several research photographs and the place's texture view, so the character is drawn in the place's design style. The user chooses one.
3. **Canonical cleanup:** run `fix-canonical-image` against its canonical prompt; the story check's list is its inventory.
4. **The A-pose views:** run `generate-subject-reference`'s A-pose views: the front as a textured viewport view, then the back and both sides from it, then the same without outer layers, such as an apron, then their grey and coloured form passes, with one fixed colour per part.
5. **The props they carry:** each small prop the story check lists, as a prop is, below. With several characters, composite their height chart with `build-line-up`.

## A prop

2. **A small prop,** with few details, such as a rag, a mug, or a bell: run `generate-subject-reference`'s small prop sheet, one coloured, non-textured sheet of the prop alone and in its character's hand, from the character's coloured A-pose and the prop's photographs.
3. **A large prop,** such as a vehicle or a piece of furniture a character uses: plan it as a character is, with a primary canonical image, cleanup, and views from the front, back, and both sides, then their form passes.

As the user judged on 2026-11-11, an element's views drift from each other, and image edits cannot make them agree: cleaning several canonical images against each other was tried on a diner and failed. Views are made once and not cleaned against each other; keeping every view of an element consistent needs the element built as a full 3D model, when the setup has a way to make one.

## Hand back

To `project-requests`, the plan, one request after another, each with its skill, what it reads from canon by name, and the user's approval before the next:

- the story check's list, with each item's place in the steps;
- for a place: research, pre-vis and its good shot, the primary canonical location, its cleanup, the views, the neutral passes, and the floor plan;
- for a character: research, the primary canonical character, its cleanup, the A-pose set with its form passes, and the props they carry;
- for a prop: its sheet, or its primary canonical image, cleanup, views, and form passes;
- for each approved result, what `project-pipeline` publishes: its artifact name, such as `<place>: primary canonical location` or `<place>: view <wall>`, what it was made from, the facts it settles, and, for an image, what it shows.

The element is then ready for its concept art reference (`generate-concept-reference`), and for keyframes.
