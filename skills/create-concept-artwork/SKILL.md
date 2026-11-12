---
name: create-concept-artwork
description: Make the film's concept artwork from its concept art references - a character's study placed into a place's concept painting, at its true size, painted with the painting's brush size and lit by the painting's own light, doing what the beat asks - to visualise the film's mood and look design. The artwork is the look reference for the images made as first frames for video. Use once the concept art references of the characters and places a moment needs exist. Not for the references themselves (create-concept-reference) or for keyframes (create-keyframe).
---

# Concept artwork

Concept artwork shows what a moment of the film will look and feel like: the place in its mood, the character in it, doing what the beat asks. It is made only from concept art references, never from canonical images directly, so its look and the canon it holds are the ones every later image of the film takes. It is then the look reference for the keyframes, the first frames video is generated from.

Good concept artwork keeps the place's painting and light exactly, and puts the character into it as if painted at the same time: the same brush size, the same light, at the right size against the room. A failed one adds detail of its own, changes the painting's light, makes the character small, or paints the character more finely than everything around them.

## The models and the route

As `create-concept-reference` says: an image-edit model that takes the prompt exactly as written, such as OpenAI's image edit with gpt-image-2.6-sunburst, at high quality and the film's aspect ratio. The execution skill that implements `create-concept-artwork` in this setup renders it.

## What it needs

- the place's concept art reference, the painting of the view the moment uses, in the moment's mood;
- each character's concept art reference, their study;
- the beat, and what the visual identity brief asks of the moment;
- a folder for the prompts and the images.

## What concept artwork is for

As the user set on 2026-11-11, concept artwork is experiment, not coverage:

- **One image for one action.** A scene's action is shown once, at the moment that says it best. Several images of the same action, the character in another pose or with the mouth open then closed, are animatic work, made later by a different method, and are not concept artwork.
- **The master shot first, then its coverage.** The master shot is the one image that captures the action best, made with the concept staging template from the character's study and the place's painting. Every other angle of the same action is coverage, made from the master shot, never staged again from the study: send the master shot first and the place's painting from the new angle second, filled from [the coverage template](templates/coverage.md), which carries the character and their action into the new angle. Staging each angle afresh lost the action every time (2026-11-11).
- **Coverage turns the character with the camera.** Told only to keep the same pose, the model pasted the character as the master shot's frame drew them, body still square to the lens, though the camera had moved round them; their direction in the room alone did not turn them, and a part-by-part description of the new pose turned the head past what a neck can do (2026-11-11). Say it as movements, as a director would: where the person or thing the action is towards sits in the new frame, which way the body faces against it, and the head as a small turn from the body, in the character's own left and right, such as "He turns his head slightly over his right shoulder towards the door." Fill [the coverage template](templates/coverage.md) with them.
- **Not into the camera.** A character speaking to someone off frame speaks towards where that person is, never towards the camera, unless the purpose is to break the fourth wall: looking or speaking into the lens reads as addressing the audience (the user, 2026-11-11).
- **Experiment with the camera.** The variations are different angles of that one action, each from a different one of the place's views, to find whether the shot reads better from another view than the one first planned. List every view the place has before choosing, and use each view once in a round; a later round returns to a view only when an image's purpose says why. The user rejected two rounds that kept reusing the same two views (2026-11-11).
- **Close on what matters.** When the action turns on one canonical object, such as a door, a bell, or a light, one of the angles is a close-up on it, so it reads; a mood that grows colder at a door is shown close on the door, not across the room.
- **A new angle needs its place first.** When no concept art reference of the place exists from the angle to test, such as a close-up, render the angle as a pre-vis camera, then make the place's painting from it with `make-canonical`'s new camera template: the nearest painted view's pre-vis shot, that painted view, and the new pre-vis shot, in that order. Then stage the character into it, or leave the character out of frame when the angle tests holding on the object.
- **Fewer is better.** Make only the images that test a real choice, and say what each one tests.
- **The limit of coverage by image edit.** As the user concluded on 2026-11-11, after six rounds on one action: an image-edit model does not hold a character's pose, or a place's objects, across a change of camera with the adherence coverage needs. It pasted the pose as drawn, or turned the body only as far as the pose's contact with objects allowed. Coverage that must keep continuity needs 3D models of the place and its props, or drawn references of the character in the pose; until then, the master shot is the concept artwork, and coverage is an experiment, kept only when it holds.

## The purpose of each image

Before choosing an angle or writing a prompt, write each image's purpose, a short paragraph, from [the purpose template](templates/purpose.md):

- **its name,** for the idea it tests, such as "the visitor's eye";
- **what it tests:** the one question about the shot it answers, such as whether the line plays strongest with the audience where the visitor stands;
- **what it depicts:** the action, and exactly what the character does: where they stand, which way their body faces, where their eyes look, and what their hands do;
- **why:** what in the beat, the visual identity brief, or the audio identity brief makes this the right test.

The angle is chosen for the purpose, and the prompt's `{{where_and_what}}` says what the purpose says the character does, opinionated and exact: the direction of the body and the eyes, never left to the model. A character with no direction looks somewhere different in every image (2026-11-11). Keep the action's blocking the same in every angle, so the angles differ only in where the camera stands. Show the purpose beside each result.

## Making it

To place a character into a place's concept painting, fill [the concept staging template](templates/concept-staging.md) and send the place's concept painting first, then each character's chosen study, each named in `{{references_list}}` as what it is, such as "The second attached image is the finished concept painting of the character.". `{{where_and_what}}` says only where and what, from the beats; `{{scale}}` gives each character's size against the objects nearest them in the view, such as "He is a big man: the counter top reaches his waist, the lit lamp hangs just above his head, and his shoulders are wider than two stools side by side.", since a model left to choose makes a character small. `{{light_on_them}}` names the place's light as its painting shows it, and where it falls on the character's own body and what falls into shadow, such as "the lamp above him lights the top of his head, his shoulders, his forearms, and the counter in front of him; his brow shades his eyes, and his lower body and the side away from the lamp fall into the room's dim charcoal-blue shadow": naming the light alone left the character evenly lit under it (2026-11-11). A character's study is more detailed than the place's painting, so the template asks for the painting's brush size on the character too, never the study's detail; it names no stroke length, which a model exaggerates. It also asks for the study's flat shading, each part in one or two flat areas with a clean edge between lit and shadow: asked only for the brush size, the model modelled his muscles and wrinkles, against the flatter shading of his study (the user, 2026-11-11); `{{their_parts}}` names the parts, such as "his head, his arms, his shirt, and his apron". Placing a character with a short instruction alone lets the model add detail of its own and change the painting's light (the user's test, 2026-11-11); the template forbids both.

Name a hand by the character's own side and by where it sits in the frame, such as "the mint towel under his right hand, the hand on the left of the frame": a character facing the camera has their right hand on the frame's left, and a model left to choose swaps them (2026-11-11).

Say a face's expression and how strongly, in the brief's terms: "his mouth open on a word" was painted as shouting, against a line the audio brief asks to be low and flat (2026-11-11); write such as "speaking quietly, his mouth barely open, his face tired and calm".

Make two candidates, and keep the one that best holds the beat and the visual identity brief, with the reason. To test a change of wording, make one call, for the one image that failed, and nothing else: every call costs money, and rerunning what already worked, or the same prompt twice, tells nothing new (the user, 2026-11-11). Show each with its prompt and every image sent, beside the references it was made from.

## Hand back

- the concept artwork kept, with its prompt and the images sent;
- the film map, updated; the artwork is the look reference `create-keyframe` takes for the moment's first frames.
