---
name: prompt-image
description: Write the words of any image prompt - concept art, a mood, a view, a cleanup - as image-generator prompting, not prose - plain visual descriptors of what is seen, where light comes from and falls, colours, materials, edges, and detail level, with what each attached image is, and nothing a picture cannot show. Use every time an image prompt is written or filled in, before it is shown to the user. Not for choosing references, models, or settings.
---

# Image prompt

An image model draws what words point at. A prompt works when every phrase names something visible: a light, a colour, a surface, a shape, a level of detail. It fails when it reads like a story: the model cannot draw a feeling, a sound, a time of night as a sentence, or a mood described as an idea, so those words either do nothing or are read wrongly.

Use this skill every time an image prompt is written, and check the prompt against it before it is shown to the user.

## How to write it

- **Visual descriptors, not story.** Labelled phrases, or one dense sentence of visual descriptors such as "chunky geometric forms, sweeping brushwork, and muted yet saturated warm–cool colours"; never a sentence that tells a story or a feeling.
- **Short labelled phrases, not sentences, for lists of settings.** Write `Dusk atmosphere: muted blue-gray light through windows, dim cool white interior lamps, soft shadows.`, not `Dusk at closing time: the last cool blue light outside the windows, the lamps just switched on.`
- **Only what can be seen.** Light: its colour, where it comes from, where it falls, how hard its edges are. Colour: named hues and how saturated. Surfaces: matte, glossy, painted, rough. Shape and edges: simplified, blocky, soft. Detail: what is kept, what is dropped. Composition: what is in the foreground, what is centred, what is empty.
- **Turn a feeling into what shows it.** Not `lonely`, but `one small pool of cool white light on the counter, the rest of the room in shadow, every stool empty`. Not `tense`, but `the dark front door the darkest shape in the frame`.
- **Be literal about anything odd.** Vague phrases such as `something slightly wrong` are read as supernatural or as distortions. Name the exact thing, or leave it out.
- **Say what each attached image is** and how it was made, in one plain sentence each, as the [prompt roles](../../docs/prompt-roles.md) say, and describe nothing the images already show.
- **Group by kind:** what to make; the time and light; the colours; the paint or surface; the detail level; what to keep from the image.
- **Name the detail level concretely:** `large flat shapes, no small objects, labels as blank shapes, no fine texture`, not only `minimal`.
- **A few labelled lines in all,** about a hundred words at most beyond the fixed template text. Long prompts make models drop parts.

## What never goes in

- Sounds, smells, and silence: `quiet`, `still`, `humming`.
- Story and backstory: `after a long shift`, `waiting for someone to walk in`, `the place someone could come in from`.
- Abstract qualities with no visual form: `ordinary`, `wrong`, `uneasy`, `nostalgic`, unless followed by what shows them.
- Novel prose: similes, metaphors, and sentences with clauses.
- Text you do not want drawn: capitals, labels, and names, unless the image is meant to carry those words.

## Check before showing

Read each phrase and ask: could a painter put this on the canvas? Cut every phrase that fails, or rewrite it as what shows it.
