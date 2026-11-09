---
name: create-keyframe
description: Make the on-model keyframes for an approved shot list - one generated image per shot, named by its shot number, with an end frame for each camera move, showing the shot's characters exactly as their reference, model, and expression or pose sheets draw them, at the line-up's heights, placed in the shot list's framing, angle, action, and staging in the place as its views show it, and drawn in the style guide's line and palette as clean line with flat colour and no background detail beyond the layout the shot needs - with an image-edit model sent the sheets, the line-up, the place's view, and the style sheet in a fixed order, or from the shot's rough board or the user's sketch sent as structure so its composition stays, tested on a few shots first, then each keyframe taken to the user to approve. Use when the user asks for keyframes, on-model frames, the frames an animatic is made of, or the frames a shot's line art and animation start from. Not for rough grey layout frames, background plates, a character's own sheets, or the colour keys of a whole film.
---

# Keyframes

The keyframes are the animatic's pictures: one clean, on-model frame for each shot of an approved shot list, held for the shot's length when the animatic is assembled. They are what the rest of the film is drawn from. The line-art stage redraws each keyframe as character outlines, and animates the shot from it, and from its end frame when it has one. So a keyframe is drawn to be redrawn: every character exactly as designed, in the right place, in clean line and flat colour, with nothing a tracer would have to guess at.

A good keyframe shows the shot list's framing and angle, the shot's characters on model, at the line-up's heights, where the staging puts them, facing the right way, doing what the action says at the shot's first moment, in the place as its view lays it out. Every keyframe of the film shares one keyframe look. A keyframe has failed when a character's face, hair, proportions, outfit, or colours drift from their sheets; when heights disagree with the line-up; when who is who is swapped, or someone is missing or added; when the framing, angle, or screen direction differs from the shot; when shading, lighting, texture, or a detailed background creeps in; when its look changes from keyframe to keyframe; or, from a board or a sketch, when the composition moved.

## The models

- **From the shot list,** use an **image-edit model** that takes the subjects' sheets, the line-up, and the place's view as references. Never use a text-to-image model: it cannot hold a character from sheets, and an off-model keyframe carries its errors into every stage after it. A subject in the shot with no reference sheets needs its reference first; say so and stop for that shot.
- **From the shot's rough board or the user's sketch,** use an image-edit model that takes it as **structure** as well as the sheets as references, so the composition stays and only the drawing changes. Never send a board or a sketch as a reference alone: the model would redraw the layout.

## Find the specifics

- **The workflow skill** of the model the request names, or that the user chooses, says which way of running it takes references and which takes a structure image, how many references it takes, how closely it follows a structure image and how that is set, and the sizes it makes. When the request names no model and more than one fits, ask.
- **Its prompt skill** gives its syntax and limits.
- **The execution skill** that implements `create-keyframe` in this setup renders it; when none does, the setup's renderer. It says what a request costs and where its output lands.

All come from the setup, as the [prompt roles](../../docs/prompt-roles.md) describe. If one is missing, say which and stop.

## What it needs

From the caller:

- an approved shot list; with none, one is planned and approved first;
- the concept's style guide: its written rules and its style sheet; with none, the keyframe look's line and palette are agreed with the user first, in words;
- each subject's reference sheets: its base sheet, and the outfit, variant, or detail sheet a shot needs;
- each character's model sheets: its colour model, and its expression and pose sheets, with their panel labels;
- the line-up, with its heights and anchor, when a shot has several subjects;
- each place's references: its views, each named by its camera position, its plan, and its props sheet, when it has one;
- the shot's rough board, when there is one, or the user's sketch, each named by the shot it is for;
- the film's aspect ratio;
- a folder for the keyframe plan, the prompts, and the keyframes, each keyframe saved beside its prompt.

Each step waits for the user's yes before the next. Every paid request waits for a yes to its plan: the model, the number of requests, and the cost. A first run on a model new to this film is a short test of a few shots.

Every image of a character who reads as a minor stays ordinary and everyday. Nothing is sexual or suggestive, in any step or prompt. Draw a recognisable real person only when the user confirms that the person agreed to this use, or a guardian did for a child; never to deceive anyone.

## The keyframe look

A keyframe is not the final look. The final look's light, shading, texture, and finished background come later, from the lighting keys and the background plates. So every keyframe follows the same rule, and the rule never changes between keyframes:

- **Clean line:** closed, unbroken outlines at the style guide's line weights, with no sketch lines, hatching, or loose strokes.
- **Flat colour:** each region of a subject filled with one flat colour, its colour from the subject's colour model, or its base sheet when it has no colour model; no shading, gradients, highlights, rim light, or cast shadows.
- **Plain light:** even, neutral light. The shot's mood is not painted in; the colour script and the lighting keys carry it later.
- **Only the layout the shot needs:** the place drawn simply, in the same line and in flat, muted colours from its view: the floor or ground line, the horizon, the walls and openings in frame, and the furniture and props the action uses or that say where the shot is. No texture, set dressing, distant detail, sky effects, or atmosphere.
- **Never:** arrows, text, captions, shot numbers, borders, or anyone the shot does not name.

Quote these lines in every keyframe's prompt, as the plan fills them.

## Keyframe prompts

Every keyframe's prompt says what the picture is, which reference is which, what the camera sees, who is where, then how it is drawn. With several references, the model cannot guess which image is which character, so the references come early. Write it in this order, for any model:

1. **What the image is:** "an on-model keyframe for one shot of an animated film", one frame at the film's aspect ratio, of the shot's first moment, or, for an end frame, its last.
2. **The references,** one line each, in the order sent, and what each fixes: "The first attached image is the base reference sheet of Mira: her face, hair, proportions, outfit, and colours are fixed." A view fixes the place's layout only, not its detail or light; the approved keyframe fixes the keyframe look; the style sheet, last, fixes line, shapes, and palette, not its light or texture.
3. **The framing and angle,** from the shot list, in camera words: "a wide shot at eye level", "a close-up from slightly below". Say what fills the frame, and where the horizon or floor line sits, such as "the horizon a third of the way up".
4. **The staging:** each character by the shot list's name and by what they look like ("Mira, the girl in the red cap"), where they are in frame (left, right, centre, foreground, background), which way they face, what they are doing at this moment, and their expression or pose by its sheet's label, such as "her SURPRISED face". Props by the script's names, in whose hands or where.
5. **The heights,** when several subjects share the frame: each against the line-up's anchor, as a landmark, such as "Tom's head reaches Mira's shoulder". Models follow a landmark better than a number.
6. **The place,** by the script's name, from its view nearest the camera, and only the layout the shot needs, named left to right and near to far.
7. **The keyframe look:** the plan's look lines, quoted, not reworded.
8. **What to leave out:** shading, lighting, texture, background detail, arrows, text, shot numbers, borders, and anyone not named. Say it plainly, as a sentence. The shot number is the file's name, never in the picture.

Keep each part to a sentence or a few short lines; long prompts make models drop parts. A keyframe has one moment. Leave out what the model ignores, as its prompt skill says.

### The order the references are sent in

1. Each subject's base sheet, in the order the prompt names them, main character first.
2. Then the outfit, variant, or detail sheet each needs, and the colour model, expression sheet, or pose sheet the shot's action calls for, in the same order.
3. The line-up, when several subjects share the frame.
4. The place's view nearest the camera; then its plan or props sheet only when the shot needs what the view does not show.
5. For an end frame, the shot's approved start keyframe; otherwise the approved keyframe that set the keyframe look, once there is one.
6. The style sheet, last.

A board or a sketch is not in this list: it goes as `structure`.

### When the references do not fit

Count the references each keyframe needs before planning it. When the model takes fewer, leave out, in this order, and only as far as needed:

1. the plan and the props sheet;
2. the line-up, when the heights are quoted as landmarks in the prompt;
3. the approved look keyframe, when the style sheet is sent;
4. an expression or pose sheet, when the expression is described in words instead.

Say which would be left out, for which keyframe, and ask the user before planning it. Never drop the base sheet of a character in frame, or the style sheet, and describe it in words instead: the character would come back off model. When the base sheets alone do not fit, say so, and ask the user to choose a model that takes more references, or to restage the shot with fewer characters in frame.

### Filling the templates

- Put each part into its field in the model's syntax, as its prompt skill says, and name the inputs by the [prompt roles](../../docs/prompt-roles.md): the sheets, the line-up, the view, and the keyframes as `references`, in the order above, and the board or the sketch as `structure`. Write each prompt with the setup's prompt writer, naming the prompt skill the workflow skill gives.
- `{{references_list}}` names each attached image on its own line, in the order sent, with what it fixes.
- `{{keyframe_look}}` is the plan's look lines, quoted.
- `{{identity_features}}` is "faces, hair, eyes, and markings" when the shot's subjects are characters or creatures; add "shapes, parts, and markings" when a prop or a vehicle is a subject in it.
- `{{staging}}` is one line per subject, in the order the references name them.
- `{{heights}}` is the line-up's landmarks for the subjects in frame; for one subject alone, it is "not needed: one subject".
- `{{layout}}` names only what the shot needs from the place's view, left to right and near to far, by the script's names.
- From a board or a sketch, the prompt says what the structure image is first, and the references after it, since the structure sets the composition. `{{structure_kind}}` is "the shot's rough storyboard frame" or "the user's own sketch of the shot"; `{{moment}}` is "the first moment of the shot", or, for an end frame, "the last moment of the shot, after the camera's move". An end frame from a board or a sketch is also sent its approved start keyframe, as the order above says.

## 1. Plan the keyframes

Fill [the keyframe plan template](templates/keyframe-plan.md):

- **The keyframe look:** its lines, from the template's fixed rule and the style guide's line, shapes, and palette, quoted. It is one look for the whole film, and it never changes between keyframes.
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

The user chooses the keyframe whose look sets the keyframe look, or asks for another take; never choose for them. Update the look lines only where the user asks. From now on, that approved keyframe is sent with every keyframe as the film's keyframe look.

## 3. The rest of the keyframes

Make the rest a scene at a time, in shot order.

- A start keyframe comes before its end frame. Send the end frame with its approved start keyframe, so the place, the characters, and the look stay, and only the camera's move, and the action it covers, has happened.
- From a board or a sketch, keep every figure's place, size, pose, and facing, and the framing and horizon, exactly as drawn. Drop the board's arrows and grey tones; they are marks, not the picture. If the model takes a strength for its structure, set it so the composition does not move, as its workflow skill says. Where a board or a sketch leaves something unclear, ask; do not invent it.
- Where a board and the shot list disagree, such as a different framing, say so, and ask the user which one the keyframe follows.
- A new take is a new paid request, and needs the user's yes.

## 4. Review each keyframe

Before showing a keyframe, compare it with what it must agree with, and list every difference:

- each character with their sheets: face, hair, eyes, proportions, outfit, colours, and props; and the expression or pose with its sheet's panel;
- the heights with the line-up;
- the framing, angle, staging, and facing with the shot list, and with the keyframes of the shots before and after it: who is on which side, and which way they face across the cut;
- the place with its view and plan: what is where, and nothing it does not have;
- the look with the keyframe look's lines: no shading, light, texture, or background detail crept in;
- an end frame with its start keyframe: the same place and characters, moved only as the camera and the action move them.

Report it honestly, such as "Tom's jacket came out blue, not green" or "Mira faces right; in 3-1 she faced left". Never score a keyframe, and never fix one on your own: the user decides, and a fix is a new take.

## 5. The user's approval

The user approves each keyframe, or asks for another take; never choose for them. Record the take the user approved for each keyframe in the plan, with the date. A keyframe is ready for the animatic only once it is approved; the animatic waits for every keyframe of the shots it holds.

## 6. Revisions

A shot keeps its number once approved, and so does its keyframe, since the animatic, the line art, and the shots after it are named by it.

- A new take of a keyframe keeps the shot's number. The take the user approves replaces it; the earlier take is kept beside it.
- A shot the shot list adds, such as `3-2A`, gets a keyframe of that number. A shot it cuts loses its keyframe, and its number is not used again.
- When the shot list, a subject's sheets, or a place's views change, redo only the keyframes they touch, list what changed, and say which later work made from those keyframes is now out of date.

## Hand back

Hand back to the caller:

- the approved keyframes: each named by its shot number, with its end frame, named by the number and `-end`, when it has one, in the shot list's order;
- the keyframe plan, with the keyframe look, each keyframe's references, anything left out to fit, and the take the user approved for each, with the date;
- the approved keyframe that set the keyframe look, as the film's keyframe reference;
- the differences the user accepted at review, by keyframe;
- the prompts that made the keyframes, each beside its keyframe.
