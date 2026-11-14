---
name: generate-canonical-image
description: Make an element's canonical images - a place's primary canonical location painted from its grey pre-vis shot and research photographs, a character's primary canonical image as one neutral front view, a chosen image seen from a new pre-vis camera, and the grey form, coloured form, and texture passes of each canonical image - as image-edit requests whose prompts name canon. Use when make-canonical reaches one of these steps. Not for planning the sequence (make-canonical), A-pose views and prop sheets (generate-subject-reference), or concept art.
---

# Canonical images

A canonical image is one every other image of an element is based on. These are the prompt rules for each kind `make-canonical` asks for, in the order it asks.

A good canonical image shows only what its pre-vis and research hold, at low detail, under neutral light, and names every piece by its key's name. A failed one adds what the mock-up does not hold, carries a mood or a time of day into a neutral pass, or lets a person into an empty place.

## What it needs

- the element and its kind, by its canonical name;
- for a place: its grey pre-vis shot (`<place>: pre-vis <camera>`), its key's names, and its research photographs (`<place>: research`);
- for a character: its research photographs (`<character>: research`) and the place's texture view (`<place>: texture pass`);
- for a new camera: the chosen image, the pre-vis shot it was made from, and the new camera's pre-vis shot;
- for a neutral pass: the canonical image alone, and the element's part colours (`<element>: part colours`).

## The images

The concept context template is `generate-concept-design`'s.

**The primary canonical location.** The first image of a place made from its pre-vis is its primary canonical location: the image every other image of the place is based on. It shows the place only. When the concept is of a place, made from its pre-vis, send the pre-vis shot in grey, as `build-previs` renders it for the model. Say what it is for: a mock-up for positioning only, telling where things are, not the design, shape, colour, or style of anything. Send the research photographs of the place's elements with the pre-vis, and say what they are: photographs of real places that show what the mock-up's shapes are. Name the mock-up's shapes from its key, since grey shapes do not say what they are. Add "Do not add anything that is not in the mock-up." Leave out every mention of people or characters, including the context template's lines about characters, figures, and skin: an empty place needs none, and naming them invites them. Ask for low detail, since the place becomes a background for animation: change the context template's "medium detail" to "low detail" and add that detail is low and minimal, broad simple shapes with only the detail an animation background needs. The premise and purpose stay short, as the context template needs.

**The primary canonical character.** A character's primary canonical image is one front view, the whole figure, in a neutral pose on a plain background, under neutral light. Fill the concept context template without its "rule of thirds" and its line on characters as geometric masses, with the purpose "concept character design", one view only. Send several research photographs of the archetype and its clothing, then the place's texture view, so the character is drawn in the place's design style; say what each image is, and only what no image gives: the build, the face, and anything the story names about the character. State every wanted trait positively, such as "a bare, balding head with no cap", since a negative cannot remove what the archetype brings with it. Reject a candidate that adds turnarounds, close-ups, or lettering.

**A new camera on a chosen image.** When the user wants a chosen image, such as the primary canonical location, seen from another angle, render the new camera on the same grey pre-vis the image was made from, close enough to the original camera that the place is recognisable, and show it to the user first. Fill [the new camera template](templates/new-camera.md) and send three images, in this order: the pre-vis shot the chosen image was made from, the chosen image, and the new pre-vis shot. The prompt says what each image is and how it was made, and asks for the generated image from the new perspective; nothing else.

**Neutral passes.** The first canonical image of an element is painted with texture, mood, and light, and that is right. Afterwards, every canonical image of it, its primary canonical image and each of its views, is made three more times without the mood, to draw out more of what it holds, so form, surfaces, and light can be decided apart:

- **Grey form:** fill [the grey form template](templates/neutral-form-grey.md): the element as a 3D scene seen in a viewport with solid shading, every surface plain matte grey, lit flat and evenly. It fixes shapes and nothing else.
- **Coloured form:** fill [the coloured form template](templates/neutral-form-colour.md): the same, with each object in its own plain, flat colour, as a viewport's object colours show them, so each object can be told apart; each object takes one uniform colour, even where its real look has a stripe or a pattern, so it separates from what it touches. Choose the colours once for the whole element and name them in `{{part_colours}}` in every view's prompt, such as ", the counter blue, the stools red, the floor beige,", so the colours agree across views; otherwise they drift.
- **Texture:** fill [the texture template](templates/neutral-texture.md): the same in a viewport's material preview, with its colours and surface textures under neutral, even light. It is the surface reference, edited before any mood, such as making surfaces less glossy.

In each, `{{what_stays}}` says what must not change: for a place, "the same objects, shapes, and camera"; for a character, "the same character in the same symmetrical A-pose, seen straight from the front" (or the view it shows). For a character, only the grey and coloured form passes are made: its A-pose views are already textured viewport views. Send the canonical image alone. Make two candidates of each, and keep the ones with no mood and no time of day. Texture that shows through a form pass, such as lettering or a pattern on a floor or a wall, is removed in canonical cleanup. Mood and lighting are then given to each element on its own, in a later pass, and the elements are combined into one concept image only after that.

## Hand back

To `project-requests`, one `generate` request per image or pass: the image-edit endpoint, the prompt as a template naming canon, such as `{{<element>: part colours}}`, and the references by canonical artifact, each with its role, in the order to send them; with two candidates where a pass asks for two.
