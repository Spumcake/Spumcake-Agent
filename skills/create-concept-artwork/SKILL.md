---
name: create-concept-artwork
description: Make the film's concept artwork from its concept art references - a character's study placed into a place's concept painting, at its true size, painted with the painting's brush size, shaded simply but painted, and lit by one named light with its shadows, rim, and the place's depth, doing what the beat asks - to visualise the film's mood and look design. The artwork is the look reference for the images made as first frames for video. Use once the concept art references of the characters and places a moment needs exist. Not for the references themselves (create-concept-reference) or for keyframes (create-keyframe).
---

# Concept artwork

Concept artwork shows what a moment of the film will look and feel like: the place in its mood, the character in it, doing what the beat asks. It is made only from concept art references, never from canonical images directly, so its look and the canon it holds are the ones every later image of the film takes. It is then the look reference for the keyframes, the first frames video is generated from.

Good concept artwork keeps the place's painting and objects exactly, relights it with one light the moment chooses, and puts the character into it as if painted at the same time: the same brush size, lit by the same light, with the shadows that light casts, at the right size against the room. A failed one adds detail of its own, makes the character small, paints the character more finely or more cleanly than everything around them, or lights them from nowhere.

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

To place a character into a place's concept painting, fill [the concept staging template](templates/concept-staging.md) and send the place's concept painting first, then each character's chosen study. Its "Filling it" section gives every slot with Last order's approved example.

### What every concept artwork prompt carries

As the user set on 2026-11-12, every concept artwork request carries all of these, each found by a round that failed without it. The template holds them; never leave one out.

1. **Each image named as what it is,** in order: the empty place's painting first, then each study.
2. **Where and what, exactly:** where the character stands, which way the body faces, and where the eyes look, never left to the model; a character with no direction looked somewhere different in every image (2026-11-11).
3. **Never into the camera:** the eyes on what they look at, "not at the camera"; a character speaking off frame speaks towards whom they speak to.
4. **Hands by two names:** the character's side and the frame's, such as "his right hand, the hand on the left of the frame"; the model swaps them otherwise (2026-11-11).
5. **The expression and its strength,** such as "speaking quietly, his mouth barely open, his face tired and calm"; "his mouth open on a word" was painted as shouting (2026-11-11).
6. **Size against the nearest objects;** a model left to choose makes a character small (2026-11-11).
7. **The painting's brush size on the character,** never the study's detail, and no stroke length, which a model exaggerates (2026-11-11).
8. **Shaded simply, but painted:** each part in one or two large, simple areas, no modelling of muscles, wrinkles, or folds, and "painted, not cel-shaded", the edge between light and shadow a brushed edge, "neither a smooth gradient nor a hard, clean line". Asked only for brush size, the model modelled his muscles; asked for no gradient, he came out too clean, almost cel-shaded (the user, 2026-11-11 and 2026-11-12).
9. **One light, named, the others off:** the light the moment needs, such as the lamp above the character, which the image's purpose decides.
10. **Values follow depth, not the frame:** the plane of focus at the character's distance keeps its value across the whole width; the foreground falls into deep shadow; the background is only very slightly darker, its details readable; "it is not a vignette". Darkening by areas of the frame, or around a focal point, read as a bad vignette; a dark background made the place dull (the user, 2026-11-12).
11. **An ambient light on the place, not the character:** it lifts the place so everything away from the character shows its colour and texture, while the character's shadows stay deep. Without it, the place away from the character was boring; asked to brighten the middle ground, the model spread the lamp's spotlight instead (the user, 2026-11-12).
12. **Every shadow follows the light,** "without the light or the place getting any brighter": each object lighter towards the light and casting its shadow away from it, named object by object, the character's own shadow included. Naming the light alone left its direction unread (the user, 2026-11-12).
13. **A fourth, faint light when the place has one,** such as moonlight through windows, much weaker than the main light and not reaching the character.
14. **Rim light on the character,** "not a soft light over" them: thin bright edges only along the outline that faces the light, each a brushed stroke, and everything inside the edges in shadow, dark but readable; "light comes from no other direction". Soft light flattened him; a rim from a light behind him with no direction rule lit edges the light could not reach (the user, 2026-11-12).
15. **Nothing else changes and nothing is added:** the painting and its objects stay as they are; a short instruction alone let the model add detail and change the light (the user's test, 2026-11-11).

Make two candidates, and keep the one that best holds the beat and the visual identity brief, with the reason. To test a change of wording, make one call, for the one image that failed, and nothing else: every call costs money, and rerunning what already worked, or the same prompt twice, tells nothing new (the user, 2026-11-11). Show each with its prompt and every image sent, beside the references it was made from.

## Hand back

- the concept artwork kept, with its prompt and the images sent;
- the film map, updated; the artwork is the look reference `create-keyframe` takes for the moment's first frames.
