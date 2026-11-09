---
name: create-background
description: Make the background plates for a film's final look - one per shot, or one per camera setup shared by every shot taken from it, each showing the place alone with no characters, drawn from the place's views, plan, and props, lit by its lighting key for the shot's mood and the colour script's line for its beat, in the style guide's finished look, framed to match the shot's approved keyframe with the same camera angle, height, and horizon, made wide or tall enough for a camera move, and kept identical across the shots of one setup so the cuts match - with an image-edit model sent the lighting key, the keyframe for its framing only, and the place's references, tested on a few setups first, then each plate taken to the user to approve, for the characters to be composited over later. Use when the user asks for backgrounds, background plates, BGs, a shot's set without its characters, or the backdrop a shot's characters go over. Not for a place's reference views or lighting keys, the keyframes, or a character's layer.
---

# Background plates

A background plate is the place a shot happens in, drawn in the film's final look with nobody in it. The characters are animated on their own, and composited over the plate later, so the plate has to be exactly the stage the keyframe set: the same camera, the same horizon, the same floor where their feet will land, lit as the shot's mood and beat call for. Shots taken from the same camera setup share one plate, so when the film cuts back to that angle, the room has not changed.

A good plate lines up with its keyframe: lay one over the other, and the horizon, the floor line, the walls, the doors, and the furniture fall in the same places, with clear room where each character stands. Every object is where the place's plan and views put it, and the light is the lighting key's. A plate for a camera move covers the whole move, with no seam. A plate has failed when the horizon or the angle differs from the keyframe, so the characters would float or slide; when a character, or a character's shadow or reflection, is in it; when a door, a window, or a prop has moved, appeared, or vanished; when its light is not the lighting key's; when two plates of one setup differ; or when a move runs off its edge.

## The model

Every plate comes from an **image-edit model** that takes the place's lighting key, the shot's keyframe, and the place's references as references. Never use a text-to-image model: it cannot hold a place from its views, and the plates would not match each other.

The keyframe is sent for its framing only: its camera, angle, and horizon, and where things stand. Never send it as `structure`: a model that follows a structure image traces its edges, and would draw the characters' outlines into the plate.

## Find the specifics

- **The workflow skill** of the model the request names, or that the user chooses, says how many references it takes, the sizes and the widest and tallest shapes it makes, and whether it extends an image past its edges. When the request names no model and more than one fits, ask.
- **Its prompt skill** gives its syntax and limits.
- **The execution skill** that implements `create-background` in this setup renders it; when none does, the setup's renderer. It says what a request costs and where its output lands.

All come from the setup, as the [prompt roles](../../docs/prompt-roles.md) describe. If one is missing, say which and stop.

## What it needs

From the caller:

- an approved shot list, with each shot's number, framing, angle, camera move, and place;
- the approved keyframes: one per shot, named by its shot number, and an end frame, named by the number and `-end`, for each camera move; with none, the keyframes are made and approved first;
- each place's references: its establishing sheet, its plan with its numbered camera positions, its views, its props sheet when it has one, and its lighting keys, each named by its view and mood;
- the colour script, with its line of colour logic for each beat, and which beat each shot falls in;
- the concept's style guide: its written rules and its style sheet;
- the film's aspect ratio;
- a folder for the background plan, the prompts, and the plates, each plate saved beside its prompt.

Each step waits for the user's yes before the next. Every paid request waits for a yes to its plan: the model, the number of requests, and the cost. A first run on a model new to this film is a short test of a few setups.

Every image of a character who reads as a minor stays ordinary and everyday. Nothing is sexual or suggestive, in any step or prompt. Use only art and photographs the user has the right to use this way.

## Setups

A **camera setup** is one camera position, at one framing and angle, in one place. Every shot taken from the same setup, such as `3-1`, `3-3`, and `3-5` cutting back to the same wide shot, uses the same plate: one file, made once, never made again for each shot. That is what keeps plates of one setup identical.

- A setup is named by its first shot's number, such as `bg-3-1`, and the plan lists every shot that uses it.
- When a later shot of a setup is in another mood or beat, such as the lights going out, its plate is made from the setup's approved plate, changing only the light, and named by the setup and the mood, such as `bg-3-1-dark`. Nothing else in it may change.
- A shot whose framing or angle differs from every other is a setup of its own, even in the same place.
- A camera move is a setup of its own, with one plate that covers the whole move.

## Plates for a camera move

The plate is as big as the move: the frame, and as far as the camera travels.

- A pan or a truck sideways needs a plate wider than the frame; a tilt or a crane, taller. The start keyframe's framing sits at one end of the plate, and the end frame's at the other.
- A push in or a pull out keeps the shape of the frame: the plate is the wider framing, at the largest size the model makes, so the tighter framing still holds its detail.
- When the move needs a plate wider or taller than the model makes, make the start framing first. Then extend it a side at a time, each request sent the plate so far as its first reference, until it covers the move. Say in each prompt that nothing already drawn changes and no seam shows.
- Record in the plan where the start and end framings sit on the plate, such as "start: the left 16:9 of the plate; end: the right 16:9".

## What passes in front

Characters are composited over the plate, so anything in the place that passes in front of a character, such as a table edge, a doorframe, or a branch, would end up behind them. Keep it in the plate, and list it in the plan for each setup, so the compositing knows it is to be layered in front. Leave clear room wherever a character stands, sits, or walks, with the floor, the seat, or the ground they touch drawn whole.

## Plate prompts

Every plate's prompt says what the picture is, which reference is which, where the camera is, what it sees, then its light and look. Write it in this order, for any model:

1. **What the image is:** "a BACKGROUND PLATE for one shot of an animated film: the place alone, with no characters, in the film's final look, for characters to be composited over".
2. **The references,** one line each, in the order sent, and what each fixes: "The first attached image is the lighting key of the Kitchen from camera position 3, at night: the place, its materials, and its light are fixed." The keyframe line always says it is for framing only, and that its characters are not drawn.
3. **The camera,** matching the keyframe exactly: its position on the plan, its framing, its angle and height, and where the horizon and the floor line sit in the frame, such as "the horizon a third of the way up, the floor meeting the back wall just below the window". For a move, the plate's shape and where each framing sits on it.
4. **What is seen,** left to right and near to far, by the place's names, exactly where the plan and the views put it, including what the characters hide in the keyframe, drawn whole.
5. **The light:** the lighting key's light, and the colour script's line for the shot's beat, quoted.
6. **The look:** the style guide's written rules for environments, line, colour, light, and texture, quoted. A plate is finished, not flat: this is the final look.
7. **What to leave out:** characters, their shadows and reflections, figures of any kind, text, labels, and borders. Say it plainly, as a sentence.

Keep each part short; a plate with many things in it names only what the camera sees. Say what must not change, every time. Leave out what the model ignores, as its prompt skill says.

### The order the references are sent in

1. The lighting key of the view nearest the shot's camera, in the shot's mood; with no key for that mood, the view itself, and say so in the plan.
2. The shot's approved keyframe, for its framing only; for a move, the start keyframe, then its end frame.
3. The place's establishing sheet.
4. The place's plan, when the plate shows what the view does not, such as what the characters hide or what lies past the view's edge.
5. The place's props sheet, when the shot shows its props.
6. The approved plate that set the plates' finish, once there is one.
7. The style sheet, last.

A plate in another mood is sent the setup's approved plate first, and an extension the plate so far first, since the first image is the one the model keeps most closely; the rest follow in the order above, without the finish plate.

When the model takes fewer, leave out the props sheet first, then the plan, then the approved finish plate, and say which, for which plate, and ask the user before planning it. Never drop the lighting key or view, the keyframe, or the style sheet.

### When the lighting key and the colour script disagree

The lighting key fixes how the place is lit; the colour script's line fixes the beat's colour and mood. When they disagree, such as a warm key in a beat the colour script makes cold, say so, and ask the user which one the plate follows. Never blend them without saying.

### Filling the templates

- Put each part into its field in the model's syntax, as its prompt skill says: the words in `prompt`, what to avoid in `negative` when the model takes it, and the images, in order, in `references`, by the [prompt roles](../../docs/prompt-roles.md). Write each prompt with the setup's prompt writer, naming the prompt skill the workflow skill gives.
- `{{references_list}}` names each attached image on its own line, in the order sent, with what it fixes.
- `{{style_rules}}` is the style guide's written rules for environments, line, colour, light, and texture, quoted.
- `{{colour_script_line}}` is the colour script's line for the shot's beat, quoted.
- `{{in_front}}` is what passes in front of the characters, from the plan, or "nothing".
- On a wide plate, `{{wide_or_tall}}` is "WIDE" for a pan or a truck and "TALL" for a tilt or a crane; `{{horizon_change}}` is empty, or, for a tilt or a crane, says where the horizon sits at the start and at the end. `{{extension_line}}` is empty for a first request; for an extension, it is "The first attached image is the plate so far: keep everything in it exactly, and extend it {{direction}} by {{amount}}, with no seam where the new part meets it."

## 1. Plan the plates

Fill [the background plan template](templates/background-plan.md):

- **One row per setup,** in the shot list's order, named by its first shot: the shots that use it, its place, its camera position on the plan, its framing and angle, its camera move, its mood and the lighting key for it, its beat and the colour script's line, its plate's shape and size, what passes in front, and its references in order.
- **A row for each mood** a setup is seen in beyond its first, made from the setup's plate.

Use the names the script, the shot list, and the place's references use. Show the plan to the user; their corrections win. Once approved, the setups keep their names.

## 2. A short test

Choose two or three setups that differ, such as a still wide shot, a camera move, and a setup seen in two moods.

- Fill [the plate template](templates/background-plate.md) for a still setup, [the wide plate template](templates/background-wide-plate.md) for a camera move, and [the relight template](templates/background-relight.md) for a setup in another mood.
- Plan them, render them on the user's yes, and report each output's path.
- Review each, as step 4 says, and report every difference honestly.

The user chooses the plate whose finish sets the plates' finish, or asks for another take; never choose for them. From now on, that approved plate is sent with every plate of another setup.

## 3. The rest of the plates

Make the rest a scene at a time, in shot order.

- A setup's first plate comes before its plates in other moods.
- Make each setup's plate once. Every shot of the setup uses that same file.
- For a move wider than the model makes, make the start framing, show it, then extend it on the user's yes.
- A new take is a new paid request, and needs the user's yes.

## 4. Review each plate

Before showing a plate, compare it with what it must agree with, and list every difference:

- with its keyframe, laid over it: the horizon, the floor line, the angle, and each wall, opening, and piece of furniture in the same place; and clear room where each character stands;
- with the place's plan, views, and props: everything where they put it, and nothing they do not have;
- with the lighting key and the colour script's line: the light's direction, colour, and shadows;
- with the style guide's rules and the approved finish plate: the line, colour, and texture;
- with nothing: no character, shadow, reflection, or figure of any kind;
- a plate in another mood, with the setup's plate: only the light changed;
- a wide plate: both framings fit on it, and no seam shows.

Report it honestly, such as "the horizon sits higher than in the keyframe, so Mira would float" or "the window moved to the left wall". Never score a plate, and never fix one on your own: the user decides, and a fix is a new take.

## 5. The user's approval

The user approves each plate, or asks for another take; never choose for them. Record the take the user approved for each setup in the plan, with the date.

## 6. Revisions

A setup keeps its name once approved, since its shots are composited over it by that name.

- A new take of a plate keeps its name. The take the user approves replaces it, and every shot of the setup uses the new one; the earlier take is kept beside it.
- When a keyframe's framing changes, redo the plate of its setup, and say which other shots of the setup it changes too. When a shot moves to another setup, the plan says so.
- When a place's references, a lighting key, or a colour script line changes, redo only the plates it touches, and list what changed.

## Hand back

Hand back to the caller:

- the approved plates, each named by its setup, and by its mood when it has more than one;
- the background plan: which shots use each plate, where a move's framings sit on its plate, what passes in front of the characters in each, the references each was made from, and the take the user approved, with the date;
- the approved plate that set the plates' finish;
- the differences the user accepted at review, by plate;
- the prompts that made the plates, each beside its plate.
