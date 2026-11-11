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

## Making it

To place a character into a place's concept painting, fill [the concept staging template](templates/concept-staging.md) and send the place's concept painting first, then each character's chosen study, each named in `{{references_list}}` as what it is, such as "The second attached image is the finished concept painting of the character.". `{{where_and_what}}` says only where and what, from the beats; `{{scale}}` gives each character's size against the objects nearest them in the view, such as "He is a big man: the counter top reaches his waist, the lit lamp hangs just above his head, and his shoulders are wider than two stools side by side.", since a model left to choose makes a character small. `{{light_on_them}}` names the place's light as its painting shows it, and where it falls on the character's own body and what falls into shadow, such as "the lamp above him lights the top of his head, his shoulders, his forearms, and the counter in front of him; his brow shades his eyes, and his lower body and the side away from the lamp fall into the room's dim charcoal-blue shadow": naming the light alone left the character evenly lit under it (2026-11-11). A character's study is more detailed than the place's painting, so the template asks for the painting's brush size on the character too, never the study's detail; it names no stroke length, which a model exaggerates. Placing a character with a short instruction alone lets the model add detail of its own and change the painting's light (the user's test, 2026-11-11); the template forbids both.

Make two candidates. Show each with its prompt and every image sent, beside the references it was made from.

## Hand back

- the concept artwork kept, with its prompt and the images sent;
- the film map, updated; the artwork is the look reference `create-keyframe` takes for the moment's first frames.
