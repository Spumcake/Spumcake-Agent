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
- Every paid request waits for the user's yes to its plan, and every result is shown with the whole prompt, every image sent, and their full paths, as the [prompt roles](../../docs/prompt-roles.md) say.

## What it needs

From the caller:

- the element, by the name the script uses, and its entry in the approved breakdown (`write-breakdown-prompt`);
- the period and setting of the film;
- the film's style guide, when there is one;
- for a character, the canonical place they are first seen in, when there is one, for its texture view;
- for a small prop, its character's canonical A-pose set;
- the project's folder, where each step keeps its own.

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
3. **The primary canonical location:** make it as below: the grey shot, the research photographs, the names from the key, and the concept context template for the place. The user chooses one.
4. **Canonical cleanup:** run `fix-canonical-image` on the chosen image, against its canonical prompt and the pre-vis. Fixes for the pre-vis go back to step 2, and the image is made again from the corrected shot. The user approves the cleaned image.
5. **The views:** run `build-previs` for a camera square-on to each wall, and any other camera the user asks for and approves, and make each view from the primary canonical location with the new camera template below. Run `fix-canonical-image` across the views, fixing only major inconsistencies. The user chooses each view.
6. **The neutral passes:** make the grey form, coloured form, and texture passes below on the primary canonical location and each view, then `fix-canonical-image` on the form passes. Surface changes, such as less gloss, are made on the texture passes; mood and light come in the concept art phase.

## A character

2. **The primary canonical character:** make it as below: one front view, from several research photographs and the place's texture view, so the character is drawn in the place's design style. The user chooses one.
3. **Canonical cleanup:** run `fix-canonical-image` against its canonical prompt; the story check's list is its inventory.
4. **The A-pose views:** run `generate-subject-reference`'s A-pose views: the front as a textured viewport view, then the back and both sides from it, then the same without outer layers, such as an apron, then their grey and coloured form passes, with one fixed colour per part.
5. **The props they carry:** make each small prop the story check lists, as below. With several characters, composite their height chart with `build-line-up`.

## A prop

2. **A small prop,** with few details, such as a rag, a mug, or a bell: run `generate-subject-reference`'s small prop sheet, one coloured, non-textured sheet of the prop alone and in its character's hand, from the character's coloured A-pose and the prop's photographs.
3. **A large prop,** such as a vehicle or a piece of furniture a character uses: make it as a character is made, with a primary canonical image, cleanup, and views from the front, back, and both sides, then their form passes.

As the user judged on 2026-11-11, an element's views drift from each other, and image edits cannot make them agree: cleaning several canonical images against each other was tried on a diner and failed. Views are made once and not cleaned against each other; keeping every view of an element consistent needs the element built as a full 3D model, when the setup has a way to make one.

## The canonical images

These make the images the steps above name. The concept context template is `generate-concept-design`'s.

**The primary canonical location.** The first image of a place made from its pre-vis is its primary canonical location: the image every other image of the place is based on. It shows the place only. When the concept is of a place, made from its pre-vis, send the pre-vis shot in grey, as `build-previs` renders it for the model. Say what it is for: a mock-up for positioning only, telling where things are, not the design, shape, colour, or style of anything. Send the research photographs of the place's elements with the pre-vis, and say what they are: photographs of real places that show what the mock-up's shapes are. Name the mock-up's shapes from its key, since grey shapes do not say what they are. Add "Do not add anything that is not in the mock-up." Leave out every mention of people or characters, including the context template's lines about characters, figures, and skin: an empty place needs none, and naming them invites them. Ask for low detail, since the place becomes a background for animation: change the context template's "medium detail" to "low detail" and add that detail is low and minimal, broad simple shapes with only the detail an animation background needs. The premise and purpose stay short, as the context template needs.

**The primary canonical character.** A character's primary canonical image is one front view, the whole figure, in a neutral pose on a plain background, under neutral light. Fill the concept context template without its "rule of thirds" and its line on characters as geometric masses, with the purpose "concept character design", one view only. Send several research photographs of the archetype and its clothing, then the place's texture view, so the character is drawn in the place's design style; say what each image is, and only what no image gives: the build, the face, and anything the story names about the character. State every wanted trait positively, such as "a bare, balding head with no cap", since a negative cannot remove what the archetype brings with it. Reject a candidate that adds turnarounds, close-ups, or lettering.

**A new camera on a chosen image.** When the user wants a chosen image, such as the primary canonical location, seen from another angle, render the new camera on the same grey pre-vis the image was made from, close enough to the original camera that the place is recognisable, and show it to the user first. Fill [the new camera template](templates/new-camera.md) and send three images, in this order: the pre-vis shot the chosen image was made from, the chosen image, and the new pre-vis shot. The prompt says what each image is and how it was made, and asks for the generated image from the new perspective; nothing else.

**Neutral passes.** The first canonical image of an element is painted with texture, mood, and light, and that is right. Afterwards, every canonical image of it, its primary canonical image and each of its views, is made three more times without the mood, to draw out more of what it holds, so form, surfaces, and light can be decided apart:

- **Grey form:** fill [the grey form template](templates/neutral-form-grey.md): the element as a 3D scene seen in a viewport with solid shading, every surface plain matte grey, lit flat and evenly. It fixes shapes and nothing else.
- **Coloured form:** fill [the coloured form template](templates/neutral-form-colour.md): the same, with each object in its own plain, flat colour, as a viewport's object colours show them, so each object can be told apart; each object takes one uniform colour, even where its real look has a stripe or a pattern, so it separates from what it touches. Choose the colours once for the whole element and name them in `{{part_colours}}` in every view's prompt, such as ", the counter blue, the stools red, the floor beige,", so the colours agree across views; otherwise they drift.
- **Texture:** fill [the texture template](templates/neutral-texture.md): the same in a viewport's material preview, with its colours and surface textures under neutral, even light. It is the surface reference, edited before any mood, such as making surfaces less glossy.

In each, `{{what_stays}}` says what must not change: for a place, "the same objects, shapes, and camera"; for a character, "the same character in the same symmetrical A-pose, seen straight from the front" (or the view it shows). For a character, only the grey and coloured form passes are made: its A-pose views are already textured viewport views. Send the canonical image alone. Make two candidates of each, and keep the ones with no mood and no time of day. Texture that shows through a form pass, such as lettering or a pattern on a floor or a wall, is removed in canonical cleanup. Mood and lighting are then given to each element on its own, in a later pass, and the elements are combined into one concept image only after that.

## Hand back

- the story check's list, with each item's place in the canonical images;
- the approved research board and its photographs;
- for a place, the pre-vis, its layout, key, good shot, and views, and the primary canonical location, its canonical angle, and each view with its grey form, coloured form, and texture passes; name the canonical angle's files plainly, so every later step finds them;
- for a character, the primary canonical image and the A-pose set with its form passes;
- for a prop, its sheet or its views;
- every continuity review, fix plan, prompt, and image sent, and what the user chose at each step.

The element is then ready for its concept art reference (`generate-concept-reference`), and for keyframes.
