---
name: create-board
description: Make the boards for an approved shot list - one rough layout frame per shot, named by its shot number, in the show's board style (loose line, grey tones, arrows for camera and motion), drawn from the shot's framing, angle, camera, action, characters, and place with an image-edit model sent the characters' A-pose views, other subjects' reference sheets, the place's references, and the style sheet, or redrawn from the user's own sketch into the board style without changing its composition - with a start frame for each camera move and an end frame when it matters, then take them to the user to choose. Use when the user asks for boards, a storyboard, layout frames, or thumbnails for a shot list, a scene, or one shot. Not for timing the boards, finished frames, or a single finished drawing of a character.
---

# Boards

The boards draw one rough frame for each shot of an approved shot list, so the user can see the film's staging before anything is finished: what the camera sees, who is where, which way they face, and how the camera and the characters move. The animatic times these frames to the shot list's lengths, and later shots start from them, so a board is made to be read, not admired.

A good frame is readable at a glance. It has the framing and angle the shot list gives, the shot's characters at their right size, in the right place, facing the right way, and arrows that show the camera's move and the characters' motion. Every frame of the board shares one board style. A frame has failed when it shows a different framing or angle than the shot, puts the wrong characters in it, or swaps who is who; when it is polished, coloured, or detailed like a finished frame; when its look changes from frame to frame; or, from the user's sketch, when the composition moved.

## The models

- **From the shot list,** use an **image-edit model** that takes the subjects' base references, the place's references, and the style sheet as references. A text-to-image model cannot hold who is who from references. Use one only when nothing in the shot has a reference yet and the user agrees, and say that the frame may not match the designs later.
- **From the user's sketch,** use a model that takes the sketch as **structure** and the subjects' A-pose views and sheets as references, so the sketch's composition stays and only its finish changes. Never send the sketch as a reference alone: the model would redraw the layout.

## Find the specifics

- **The workflow skill** of the model the request names, or that the user chooses, says which way of running it takes references and which takes a structure image, how many references it takes, how closely it follows a structure image, and the sizes it makes. When the request names no model and more than one fits, ask.
- **Its prompt skill** gives its syntax and limits.
- **The execution skill** that implements `create-board` in this setup renders it; when none does, the setup's renderer. It says what a request costs and where its output lands.

All come from the setup, as the [prompt roles](../../docs/prompt-roles.md) describe. If one is missing, say which and stop.

## What it needs

From the caller:

- an approved shot list; with none, one is planned and approved first;
- the concept's style guide, when it has one: its written rules and its style sheet;
- each subject's base reference: for a character, its textured A-pose views in the outfit the shot needs, the front first; for any other subject, its reference sheet, or the variant sheet the shot needs; and the detail sheet a shot needs, and the expression or pose sheet when the shot's action needs one;
- the line-up, with its heights, when a shot has several subjects;
- each place's references, when it has them;
- the user's sketches, when there are any, each named by the shot it is for;
- the film's aspect ratio;
- a folder for the board plan, the prompts, and the frames, each frame saved beside its prompt.

Each step waits for the user's yes before the next. Every paid request waits for a yes to its plan: the model, the number of requests, and the cost. A first run on a model new to this board is a short test of two or three frames.

Every image of a character who reads as a minor stays ordinary and everyday. Nothing is sexual or suggestive, in any step or prompt. Draw a recognisable real person only when the user confirms that the person agreed to this use, or a guardian did for a child; never to deceive anyone.

## Board prompts

Every frame's prompt says what the picture is, then what the camera sees, then who is where, then how it is drawn. Write it in this order, for any model:

1. **What the image is:** "a rough storyboard frame for one shot of an animated film", one panel at the film's aspect ratio. The kind tells the model to stay rough.
2. **The framing and angle,** from the shot list, in camera words: "a wide shot at eye level", "a close-up from slightly below". Say what fills the frame and where the horizon or floor line sits.
3. **The staging:** each character by the shot list's name and by the attached image that shows them ("Mira, the character in the first image"), never by what they look like, where they are in frame (left, right, centre, foreground, background), which way they face, and what they are doing at the moment the frame shows. Then the place, by the script's name, and in a few words only when no reference of the place is sent. In the templates, `{{place_description}}` is a comma and those few words, or empty when the place's references are sent. From the user's sketch, the prompt never describes what the sketch shows: it says only who is who, and the framing, angle, and arrows. When several subjects share the frame, quote their heights from the line-up, such as "Mira's head reaches Tom's shoulder".
4. **The arrows:** the camera's move, drawn on the frame, such as an inner rectangle with corner arrows for a push in, or a broad arrow along the edge for a pan; and a thin arrow along each character's path when they move. A still shot has no camera arrow. Say the arrows are drawn as storyboard marks, not as objects in the scene.
5. **The board style:** the plan's board style lines, quoted, not reworded.
6. **The references,** in the order they are sent, what each is and how it was made, and what to keep from each: identity and proportions from each character's A-pose views and each other subject's sheets, but not their colour or finish; the layout of the place; line and tones from the approved board frame; shapes and proportion from the style sheet, but not its colour. Say the model must draw in the board style, not in the references' finish.
7. **What to leave out:** colour, finished rendering, fine detail, and any text, captions, panel numbers, or borders. The shot number is the file's name, never in the picture. Say it plainly, as a sentence.

Keep each part to a sentence or a few short lines; long prompts make models drop parts. A frame has one moment: the start of the shot, or, for an end frame, the end of its move. Leave out what the model ignores, as its prompt skill says.

Send the references in this order: each subject's base reference, in the order the prompt names them, a character's front A-pose first, then its A-pose view nearest the way it faces when that is not the front; then any detail, expression, or pose sheet the shot needs; then the line-up, when several subjects share the frame; then the place's references; then the approved board frame, once there is one; then the style sheet, last. When the model takes fewer references than the shot has, say which would be left out and ask the user; never drop the front A-pose of a character in frame without saying so.

Put each part into its field in the model's syntax, as its prompt skill says, and name the inputs by the [prompt roles](../../docs/prompt-roles.md): the A-pose views, sheets, and frames as `references`, and the user's sketch, when there is one, as `structure`. Write each prompt with the setup's prompt writer, naming the prompt skill the workflow skill gives.

## 1. Plan the board

Fill [the board plan template](templates/board-plan.md):

- **The board style:** its lines, from the template's defaults and the style guide's shapes and proportion. It is one look for the whole board, and it never changes between frames.
- **One row per shot,** in the shot list's order, by its number, such as `3-1`.
- **Its frames:** every shot has a start frame, named by its number. A camera move gets an end frame, named by its number and `-end`, such as `3-1-end`, when the move changes what the frame shows: a push in or pull out that changes the framing, or a pan, tilt, truck, or track that reveals something new. A small move needs only its arrow.
- **Its source:** the shot list, or the user's sketch for that shot.
- **Its references,** in the order above.

Use the names the script and the shot list use for every character, prop, place, and shot. Show the plan to the user; their corrections win.

## 2. Test frames

Choose two or three shots that differ, such as a wide shot that shows a place, a close-up of a character, and a shot with a camera move.

- Fill [the frame template](templates/board-frame.md) for a shot from the shot list, [the end frame template](templates/board-end-frame.md) for an end frame, and [the sketch template](templates/board-from-sketch.md) for a shot from the user's sketch.
- Plan them, render them on the user's yes, and report each output's path.
- Inspect each frame against its shot: its framing and angle, who is in frame and where, which way they face, its arrows, and the board style. Report honestly where it drifted.

The user chooses the frame whose look sets the board style, or asks for another take; never choose for them. Update the board style lines to match. From now on, that approved frame is sent with every frame as the board's look.

## 3. The rest of the board

Make the rest a scene at a time, in shot order.

- A start frame comes before its end frame. Send the end frame with its approved start frame first, so the place and the characters stay, and only the camera's move has happened.
- From the user's sketch, keep every figure's place, size, pose, and the framing exactly as drawn. If the model takes a strength for its structure, set it so the composition does not move, as its workflow skill says. Where a sketch leaves something unclear, ask; do not invent it.
- Inspect each frame as in the test, and report drift honestly. A new take is a new paid request, and needs the user's yes.

The user chooses which take of each frame is the board, and records it in the plan; never choose for them.

## 4. Revisions

A shot keeps its number once approved, and so does its frame, since the animatic and the shots after it are named by it.

- A new take of a frame keeps the shot's number. The take the user chooses replaces the board's frame; the earlier take is kept beside it.
- A shot the shot list adds, such as `3-2A`, gets a frame of that number. A shot it cuts loses its frame from the board, and its number is not used again.
- When the shot list changes, redo only the frames of the shots it touches, and list what changed.

## Hand back

Hand back to the caller:

- the approved board: each frame named by its shot number, with its end frame when it has one, in the shot list's order;
- the board plan, with the board style and the take the user chose for each frame;
- the approved frame that set the board style, as the board's style reference;
- the prompts that made the frames, each beside its frame.
