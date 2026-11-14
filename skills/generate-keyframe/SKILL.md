---
name: generate-keyframe
description: Make the on-model keyframes for an approved shot list - one generated image per shot, named by its shot number, with an end frame for each camera move, drawn in partially completed digital line art with no shading and no colour, keeping the focus on the action - with an image-edit model sent the shot's animatic layout drawing first, then each character's animatic expression sheet, acting sheet, turnaround, and level-of-detail sheet, with a short prompt that says only what each image is and what no image shows, or from the shot's rough board or the user's sketch sent as structure so its composition stays, tested on a few shots first, then each keyframe taken to the user to approve. Use when the user asks for keyframes, on-model frames, the frames an animatic is made of, or the frames a shot's line art and animation start from. Not for rough layout frames, background plates, a character's own sheets, or the colour keys of a whole film.
---

# Keyframes

The keyframes are the animatic's pictures: one rough, on-model sketch for each shot of an approved shot list, held for the shot's length when the animatic is assembled. They are what the rest of the film is drawn from. The line-art stage redraws each keyframe as character outlines, and animates the shot from it, and from its end frame when it has one. So a keyframe is drawn to be redrawn: every character exactly as designed, in the right place, in clean line with no shading, with nothing a tracer would have to guess at.

A good keyframe shows the shot list's framing and angle, the shot's characters on model, at the size their level-of-detail sheet sets, where the staging puts them against what they touch, facing the right way, doing what the action says at the shot's first moment, in the place as its layout drawing draws it. Every keyframe of the film shares one keyframe look. A keyframe has failed when a character's face, hair, proportions, or outfit drift from their animatic sheets; when sizes disagree with their level-of-detail sheets; when who is who is swapped, or someone is missing or added; when the framing, angle, or screen direction differs from the shot; when shading, lighting, texture, or anything the layout drawing leaves out creeps in; when its look changes from keyframe to keyframe; or, from a board or a sketch, when the composition moved.

## The models

- **From the shot list,** use an **image-edit model** that takes the shot's layout drawing and each character's animatic sheets as references. Never use a text-to-image model: it cannot hold a character from its references, and an off-model keyframe carries its errors into every stage after it. A character in the shot with no animatic sheets needs them first (`generate-model-sheet`, `generate-detail-sheet`); say so and stop for that shot.
- **From the shot's rough board or the user's sketch,** use an image-edit model that takes it as **structure** as well as the animatic sheets as references, so the composition stays and only the drawing changes. Never send a board or a sketch as a reference alone: the model would redraw the layout.

## Find the specifics

- **The workflow skill** of the model the request names, or that the user chooses, says which way of running it takes references and which takes a structure image, how many references it takes, how closely it follows a structure image and how that is set, and the sizes it makes. When the request names no model and more than one fits, ask.
- **Its prompt skill** gives its syntax and limits.
- **The execution skill** that implements `generate-keyframe` in this setup renders it; when none does, the setup's renderer. It says what a request costs and where its output lands.

All come from the setup, as the [prompt roles](../../docs/prompt-roles.md) describe. If one is missing, say which and stop.

## What it needs

From the caller:

- an approved shot list; with none, one is planned and approved first;
- for each camera, its pre-vis render, from which its animatic layout drawing is made;
- each place's floor plan (`build-previs`) and the timing reference's blocking, for where each character stands, faces, and looks, by the plan's names;
- each character's animatic expression sheet, acting sheet, and turnaround (`generate-model-sheet`), and board-style level-of-detail sheet (`generate-detail-sheet`), with their panel labels; the expression sheet holds a panel for each look a shot needs, drawn as that shot needs it;
- the line-up, when several characters share a frame;
- the shot's rough board, when there is one, or the user's sketch, each named by the shot it is for;
- the film's aspect ratio;
- a folder for the keyframe plan, the prompts, and the keyframes, each keyframe saved beside its prompt.

Each step waits for the user's yes before the next. Every paid request waits for a yes to its plan: the model, the number of requests, and the cost. A first run on a model new to this film is a short test of a few shots.

Characters who read as minors, and recognisable real people, are shown only as the [prompt roles](../../docs/prompt-roles.md) say.

## The keyframe look

A keyframe is not the final look. The final look's light, shading, texture, and finished background come later, from the places' mood references and the background plates. So every keyframe follows the same rule, and the rule never changes between keyframes:

- **Partially completed digital line art:** the main forms drawn with clean, confident, single lines in dark grey-black that keep every character on model, the line's weight varying a little, and only here and there a light construction stroke still showing, as if the inking is half done (the user, 2026-11-12: looser sketch lines were too sketchy). An animatic stays focused on the action.
- **No shading by default:** no fills, no shading, and no grey tones on the characters or the place; no colour anywhere. Grey appears only when the shot needs a shadow the scene casts on them, such as a character standing in a doorway's shadow, as one flat, light grey shape (the user, 2026-11-12: these models shade by habit, and shading is never the default).
- **Only what the characters touch or look at:** the place is only the forms the characters touch or look at, outlined in light grey, floating on the white page, as the shot's layout drawing draws them: no walls, floor, ceiling, or grid. Decisions about props and background elements are not made in the animatic.
- **Never:** arrows, text, captions, shot numbers, borders, or anyone the shot does not name.

These rules are what the layout drawing and the animatic sheets show; a keyframe prompt that sends them does not restate them, as `docs/prompt-roles.md` says.

**The layout drawing.** Before any keyframe from a camera, make that camera's animatic layout drawing from its pre-vis render with [the animatic layout template](templates/animatic-layout.md): only what the characters touch or look at, outlined, with no walls, floor, ceiling, or grid. It is sent first to every keyframe from that camera, so every animatic frame draws the place the same way (the user, 2026-11-12; the template records how it was narrowed).

**The characters' sheets.** A character's references are their animatic expression sheet, acting sheet, and turnaround (`generate-model-sheet`) and their board-style level-of-detail sheet (`generate-detail-sheet`). Their size in the frame is a figure of the level-of-detail sheet, never a landmark in words: landmarks left Otis too big, and the sheet's figure brought him to scale (the user, 2026-11-12). Their look is an expression panel drawn for the shot; when no panel looks the way the shot needs, make that panel first, since text that contradicts a panel loses to the drawing.

## Keyframe prompts

Fill [the keyframe template](templates/keyframe.md). The prompt is short: what each image is, in the order sent, then only what no image shows: where each character is against what they touch, which level-of-detail figure sets their size, which expression panel they wear, and anything that differs from the sheets, such as a prop in a hand. Nothing an image already shows is described: not the look, the character, or the place. An earlier template of about 900 words restated them on top of the images and contradicted its own references (the user, 2026-11-12).

### The order the references are sent in

1. The shot's layout drawing; for an end frame, the shot's approved start keyframe after it.
2. For each character, main character first: the animatic expression sheet, acting sheet, turnaround, and level-of-detail sheet.
3. The line-up, when several characters share the frame.

A board or a sketch is not in this list: it goes as `structure`.

### When the references do not fit

Count the references each keyframe needs before planning it. When the model takes fewer, leave out, in this order, and only as far as needed: the turnaround, when the shot's angle is near the expression sheet's; then the acting sheet, when the shot's pose is the expression panel's. Never leave out the layout drawing, a character's expression sheet, or their level-of-detail sheet, and never describe them in words instead. Say which would be left out, for which keyframe, and ask the user before planning it.

### Filling the templates

- Put each part into its field in the model's syntax, as its prompt skill says, and name the inputs by the [prompt roles](../../docs/prompt-roles.md): the layout drawing, the sheets, and the keyframes as `references`, in the order above, and the board or the sketch as `structure`.
- The keyframe template's "Filling it" gives every slot with Otis saying the line as its example.
- **Read the records first.** Before writing the prompt, read the record of each image to be sent: the layout drawing's says which named objects are in the frame, where, and in what state; the floor plan and the blocking say which of them the character stands at and looks at. Write the prompt from that mapping. The keyframe's [record](../../docs/records.md) is written with the result: its sources with their roles, the layout's contents, and each character with their mark and what they look at, given to the renderer as its contents.
- **What a character looks at is named as it appears in the image,** never by a document's name the model cannot see, and never by the character's own left or right. The floor plan decides which object it is; the prompt points at it as drawn: "he turns his head away from the camera, back towards the door in image 1, the door that has just opened behind him, and looks at it". "The front door" is a name the model has never seen, and "over his right shoulder", meaning his own right, the frame's left, was read as the frame's right: four keyframes sent him staring away from the door that had just opened (the user, 2026-11-13). When the object is behind the character in this camera, the prompt says the head turns away from the camera; eyes alone cannot look behind a face turned to the lens.
- `{{placement}}` comes from the timing reference's blocking, read against the floor plan, and names each object by its floor-plan name. For each thing a character touches, it says where they are against it: which side, how far along it, what it hides of them, and where their hands land. With the place reduced to what is touched, "behind the counter on the right" left the model to put him anywhere (the user, 2026-11-12).
- From a board or a sketch, fill [the structure template](templates/keyframe-from-structure.md); for an end frame, [the end frame template](templates/keyframe-end-frame.md). Both follow the same rule: what each image is, and only what no image shows.

## 1. Plan the keyframes

Fill [the keyframe plan template](templates/keyframe-plan.md):

- **The keyframe look:** the fixed rule above, one look for the whole film, recorded in the plan; it is carried by the layout drawings and the animatic sheets, never quoted in a prompt.
- **One row per keyframe,** in the shot list's order. Every shot has a start keyframe, named by its number, such as `3-1`. Every shot with a camera move also has an end frame, named by its number and `-end`, such as `3-1-end`: the last moment, once the move is done. A still shot has none.
- **Its source:** the shot list, the shot's rough board, or the user's sketch.
- **Its characters and props,** with the expression or pose label each takes, and **its place,** with the view nearest its camera.
- **Its references,** in the order above, and anything left out to fit.

Use the names the script and the shot list use for every character, prop, place, and shot. Show the plan to the user; their corrections win.

## 2. A short test

Choose two or three shots that differ, such as a wide shot that shows a place, a close-up with a strong expression, and a shot with several characters and a camera move.

- Fill [the keyframe template](templates/keyframe.md) for a shot from the shot list, [the end frame template](templates/keyframe-end-frame.md) for an end frame, and [the structure template](templates/keyframe-from-structure.md) for a shot from its board or the user's sketch.
- Plan them, render them on the user's yes, and report each output's path.
- Review each against everything it must agree with, as step 4 says, and report every difference honestly.

The user approves each test keyframe, or asks for another take; never choose for them. A fix to the look goes into the sheets or the layout drawing, never into a prompt.

## 3. The rest of the keyframes

Make the rest a scene at a time, in shot order.

- A start keyframe comes before its end frame. Send the end frame with its approved start keyframe, so the place, the characters, and the look stay, and only the camera's move, and the action it covers, has happened.
- From a board or a sketch, keep every figure's place, size, pose, and facing, and the framing and horizon, exactly as drawn. Drop the board's arrows and grey tones; they are marks, not the picture. If the model takes a strength for its structure, set it so the composition does not move, as its workflow skill says. Where a board or a sketch leaves something unclear, ask; do not invent it.
- Where a board and the shot list disagree, such as a different framing, say so, and ask the user which one the keyframe follows.
- A new take is a new paid request, and needs the user's yes.

## 4. Review each keyframe

Before showing a keyframe, compare it with what it must agree with, and list every difference:

- each character with their animatic sheets: face, hair, eyes, proportions, outfit, and props, in line, with no shading; the expression with its panel; and the size with the level-of-detail figure named;
- the heights with the line-up, when several characters share the frame;
- the framing, angle, staging, and facing with the shot list, and with the keyframes of the shots before and after it: who is on which side, and which way they face across the cut;
- the place with its layout drawing: what is where, and nothing it leaves out;
- each character's mark, facing, and look with the blocking and the floor plan: standing where the plan puts them, and looking at the named object the blocking gives, such as the front door, from this camera;
- the look with the keyframe look's lines: no colour, texture, or background or prop detail crept in, and no shading crept in, beyond a shadow the staging names;
- an end frame with its start keyframe: the same place and characters, moved only as the camera and the action move them.

Report it honestly, such as "Tom's jacket came out blue, not green" or "Mira faces right; in 3-1 she faced left". Never score a keyframe, and never fix one on your own: the user decides, and a fix is a new take.

## 5. The user's approval

The user approves each keyframe, or asks for another take; never choose for them. Record the take the user approved for each keyframe in the plan, with the date. A keyframe is ready for the animatic only once it is approved; the animatic waits for every keyframe of the shots it holds.

## 6. Revisions

A shot keeps its number once approved, and so does its keyframe, since the animatic, the line art, and the shots after it are named by it.

- A new take of a keyframe keeps the shot's number. The take the user approves replaces it; the earlier take is kept beside it.
- A shot the shot list adds, such as `3-2A`, gets a keyframe of that number. A shot it cuts loses its keyframe, and its number is not used again.
- When the shot list, a character's animatic sheets, or a layout drawing change, redo only the keyframes they touch, list what changed, and say which later work made from those keyframes is now out of date.

## Staging

**Staging into a canonical view.** A keyframe's characters and props are placed into the canonical view of the place its shot uses, so the first frames for video hold the same canon the concept artwork does; the moment's concept artwork is sent as the look reference. Fill [the staging template](templates/staging.md): the view first, then each canonical character's A-pose views or prop's sheet, in order, each named in `{{references_list}}` as a sentence saying what it is and how it was made. Say only what no attached image gives: who goes where in the view, and what they are doing, from the shot list. Make several candidates, and run canonical cleanup on the one the user chooses.

## Hand back

Hand back to the caller:

- the approved keyframes: each named by its shot number, with its end frame, named by the number and `-end`, when it has one, in the shot list's order;
- the keyframe plan, with each keyframe's references, anything left out to fit, and the take the user approved for each, with the date;
- the differences the user accepted at review, by keyframe;
- the prompts that made the keyframes, each beside its keyframe.
