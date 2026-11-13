---
name: create-concept-reference
description: Turn one canonical reference into its concept art reference - a character's canonical front A-pose, with the canonical sheets of the props it carries, into one front character study in the film's concept look; a place's canonical view, its texture pass, into a painting in the concept look and a chosen mood, with the place's own colours and the mood's light - so concept artwork and the references for video rest on the same canon. Use once an element is canonical and the film's visual identity brief is written. Not for exploring designs (explore-concept), making canonical images (make-canonical), or composing concept artwork (create-concept-artwork).
---

# Concept art reference

The film's process for concept art is canonical reference, then concept art reference, then concept artwork. This skill makes the middle step: one canonical element, repainted in the film's concept look, so every piece of concept artwork takes its characters and places from references that hold the canon, and the images made for video later take the same canon.

A good concept art reference keeps everything that makes the element itself, its layout and objects or its build, face, clothes, and props, and changes only how it is painted and lit. A failed one repaints the element's colours, adds or loses objects, or keeps the canonical image's detail and calls it a painting.

## The models and the route

An **image-edit model** that takes the prompt exactly as written, with no reasoning model rewriting it, such as OpenAI's image edit endpoint with gpt-image-2.6-sunburst, at high quality and the film's aspect ratio. The execution skill that implements `create-concept-reference` in this setup renders it; when none does, the setup's renderer. Whatever renders it writes the result's [record](../../docs/records.md); [`scripts/generate.py`](../../scripts/generate.py) renders it so. It comes from the setup, as the [prompt roles](../../docs/prompt-roles.md) describe; if it is missing, say which and stop.

## What it needs

- the element's canonical images: a character's front A-pose and the sheets of the props it carries, or a place's views with their texture passes;
- the visual identity brief, with its palette candidates and its research's readings (`write-visual-identity-brief`, `research-references`);
- the film map, for which version of each counts;
- a folder for the prompts and the images.

**Concept art prompts are short.** A few lines: what to make, how it is painted, and the mood. A long prompt full of instructions overloads the model, which then copies details instead of interpreting; a block of lighting instructions makes it render every form. The light's opinion comes from the light palette and one sentence saying where light falls and what falls into shadow, never from instructions about how to render forms.

## A character

**The character study:** the main character in the film's concept style, alone, one front view only, since several painted views of one character drift apart. Fill [the character study template](templates/character-study.md), the place mood template's painting words with the character in place of the place: `{{other_images}}` names each further image sent, such as "; the second attached image is the canonical sheet of the towel he carries"; `{{keeps}}` says what the character keeps and what a further image corrects, such as "He keeps his own build, face, and colors, with the towel from the second image tucked at his apron in place of the one in the first."; `{{parts}}` lists the character's parts, each with its own colour, from the canonical images; `{{pronoun}}` is the character's. Send the canonical front A-pose first, then any prop's canonical sheet the character carries, so the study takes each prop's one canon. The template asks for the character's simplification part by part, the silhouette, the face, the hands, and the clothes, since asking for a reinterpretation alone left the character barely changed (2026-11-11). Soft, even light on a plain background: the study is the reference later concept art lights for its own moment. Make two candidates; it is the style reference for every later image of the character.

## A place

**Place moods.** To try a place in a mood, fill [the place mood template](templates/place-mood.md) and send the place's canonical angle's texture pass alone to an image edit model that takes the prompt exactly as written, with no reasoning model rewriting it, such as OpenAI's image edit endpoint with gpt-image-2.6-sunburst, at high quality and the film's aspect ratio. The template grew from the user's prompt that gave the best concept painting of the diner, then was tuned against the user's reference of feature-animation concept art, a painterly gouache look with stylized shapes, dry-brush texture, layered colour, and controlled light (2026-11-11). Only its slots change, and only with what sets the mood, each from the visual identity brief and the readings of its research, and written with `write-image-prompt`:

- `{{place}}`: the kind of place, such as "diner".
- `{{time}}`: a few words, such as "at dusk".
- `{{colour_character}}`: one word or two for the colour, such as "muted"; loud, saturated colour was rejected.
- `{{world_palette}}`: the place's own colours, named from its canonical texture pass, such as "cream, diner red, warm wood brown, charcoal, steel grey, and red-and-cream tile"; the same in every mood, so no mood repaints the place.
- `{{light_palette}}`: the colours of the light and the shadow only, from the visual identity brief's palette candidates and the readings of its research, such as "cool white lamplight, cold blue moonlight, and deep blue shadow"; this is where the mood's colour opinion goes.
- `{{light_and_shadow}}`: one sentence saying where the light falls, what shape it makes, and what falls into shadow, from the readings, such as "Most of the room sinks into deep blue shadow; a single pool of cool white lamplight falls on the counter and the nearest stools, and cold moonlight lays pale window shapes across the floor." Naming light sources alone left the room evenly lit; describing the shadow is what made the light shape the picture (2026-11-11).
- `{{objects}}`: every object the view holds, from the pre-vis key, each with its own colour and one simple form word, such as "A cream tiled counter with a red stripe and a black base, blocky dispensers, cake dome, receding red stools, dark tiled floor, three pendant lights with only the nearest glowing, wood-panelled walls, menu board, wooden back door with a grey glass panel, red booths, and dark blue moonlit windows". Besides the light palette and the shadow sentence, the mood enters only through the objects that carry light: the windows, by what is outside them ("dark blue moonlit windows"), the lamps, by which are on and their colour ("three pendant lights with only the nearest glowing", "cool white pendant lights"), and the floor, by the light on it ("sunlit tiled floor"). Name a menu or a sign without its words.

Send the canonical angle as it is: never blurred, shrunk, or softened to reduce detail, which the user rejected (2026-11-11). Words that were tested in the template and taken out, and stay out: "impasto oil" and "visible paint ridges", which made every model paint thick oil; "digital painting", which confused the model; any length of brush stroke, long or short, since the model exaggerates either; "grain"; "volumetric haze" and "atmospheric depth", which filled the room with fog; and "volumetric light beams", which looked wrong. Add nothing else to the template. A block of lighting lines (key, secondary, rim light, lifted shadows, wide midtones) made the model render every form in detail, and words that describe execution are already in the template. Each further element is added only after a test shows it keeps the template's simplicity. The concept artwork's light rules (`create-concept-artwork`: one light, values by depth, ambient light, shadows that follow the light) failed that test here on 2026-11-12: added to the place mood prompt, they made the painting more rendered, brighter, and flatter. They belong where a finished painting is relit, as in the concept staging template, never where the painting is first made.

Fill every slot from the visual identity brief and the readings of its research; a light or a colour no reading supports is a guess, and is left out. Show the user the inspiration, not only the prompt: a sheet of the reference frames each prompt drew from, beside its results, each frame labelled with what was taken from it and why, and which were left out and why. Name each light by its kind: direct sun, overcast sky, moonlight, fluorescent, neon, tungsten, a screen. Artificial light takes the colour `write-visual-identity-brief` gives it. A reasoning model with an image tool, such as OpenAI's Responses API, rewrites a short prompt into a fuller one itself, and its rewrite can be read back and learned from.

## Hand back

- each concept art reference, with its prompt, the images sent, and the inspiration sheet;
- the film map and the style guide's style references, updated with the references kept.
