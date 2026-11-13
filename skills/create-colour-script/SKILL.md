---
name: create-colour-script
description: Make a film's colour script - the written colour and light logic of every beat or sequence, drafted by a language model from a prompt this skill builds, then one small keyframe per beat painted in that logic with an image-edit model sent the concept's style sheet, or a text-to-image model when there is none, laid out in story order so the arc of colour and light across the whole film can be judged at a glance - from the approved beat sheet or shot list and the concept's style guide. Use when the user asks for a colour script, a colour plan, colour keys for a film, or the mood or lighting arc of a story. Not for a concept's overall look, a place's or a character's mood reference, or the boards.
---

# Colour script

A colour script plans the mood of a whole film in colour and light, before anything is boarded or shot. It is a row of small keyframes, one per beat or sequence, in story order, so the user can see at a glance where the film is warm or cold, bright or dark, calm or tense, and where it turns. Every later image of a beat, a board, a background plate, or a shot, takes its colour and light from its line here.

It has two halves that must agree: the **colour logic**, a line per beat that a prompt can quote, saying what colours and light the beat has and why; and the **keyframes**, which show it. A good colour script has an arc you can read from across the room: neighbouring beats differ where the story turns and hold where it holds, and every colour comes from the style guide's palette or is marked as a departure. A failed one has every keyframe in the same palette, keyframes so detailed the colour is lost, or keyframes that ignore their own logic.

## The models

- **The colour logic** comes from a language model, run on a prompt this skill builds. The language model may be the agent itself, when the setup says so.
- **The keyframes** come from an **image-edit model**, sent the concept's style sheet as a reference, so every keyframe is in the concept's look. Only when the concept has no style sheet, use a **text-to-image model**. A keyframe is small and simple: big shapes of colour and light, not a finished illustration.

## Find the specifics

- **The workflow skill** of the image model the request names, or that the user chooses, says which way of running it takes text alone and which takes references, how many references it takes, and the sizes it makes. **Its prompt skill** gives its syntax and limits.
- **The execution skill** that implements `create-colour-script` in this setup renders it; when none does, the setup's renderer. It says what a request costs and where its output lands, and runs the language model too.

All come from the setup, as the [prompt roles](../../docs/prompt-roles.md) describe. If one is missing, say which and stop. When the request names no model and more than one fits, ask.

## What it needs

From the caller:

- the approved beat sheet, or the approved shot list; with neither, one is planned and approved first;
- the concept's style guide, when it has one: its written rules and its style sheet;
- the film's aspect ratio, from the shot list or the style guide; 16:9 when neither says;
- each place's primary canonical location and its views, with their neutral passes, and each character's A-pose views or another subject's reference sheet, when the user wants a keyframe to show them recognisably;
- a folder for the prompts, the colour script, and the keyframes, each keyframe saved beside its prompt.

Each step waits for the user's yes before the next. Every paid request waits for a yes to its plan: the model, the number of requests, and the cost. A first run on a new model is a short test before the rest.

Characters who read as minors, and recognisable real people, are shown only as the [prompt roles](../../docs/prompt-roles.md) say.

## Keyframe prompts

A keyframe prompt says what the picture is for, then the moment, then its colour and light, which carry the most weight. Write it in this order, for any model:

1. **What the image is:** "a colour key for one beat of an animated film: a small, simple painting of one moment, made to show its colour and light, not its detail".
2. **The moment:** where it is and what happens, by the beat sheet's or shot list's names. Characters are simple figures or silhouettes, described by what they look like or by role, never by a real person's name.
3. **The composition:** one simple arrangement of a few big shapes and values, as the shot list frames it when there is one.
4. **The colour and light:** the beat's line of colour logic, quoted: the dominant colours, the accent, the light's source, direction, and quality, the time of day, and the contrast.
5. **The look:** the style guide's shapes and texture, quoted, painted loosely. Detail is left out so the colour reads.
6. **The references,** when there are any, in the order sent: a character's front A-pose view, or another subject's reference sheet, first, for its shape and colours only; the grey form pass of the place's primary canonical location, or of its view nearest the composition, next, for its layout; the style sheet last, for its line, colour, and light. Say that the beat's own colour and light win over the colours of every reference.
7. **What to leave out:** text, labels, borders, faces in detail, and fine texture, as a plain sentence.

Keep the colour-and-light part in the same form in every keyframe, and change only its words, so the differences the user sees are the logic's differences. Keep each part short, as `write-image-prompt` says. Leave out what the model ignores, as its prompt skill says.

Put each part into its field in the model's syntax, as its prompt skill says: the words in `prompt`, what to avoid in `negative` when the model takes it, and the images, in order, in `references`, by the [prompt roles](../../docs/prompt-roles.md). Write each prompt with the setup's prompt writer.

## 1. Plan

From the beat sheet or the shot list, list its beats or sequences in story order, by their numbers and names. Propose one keyframe per beat, or per sequence when the film is long or the beats are many; most colour scripts have between eight and thirty. The user agrees the list, and every keyframe keeps its beat's number from then on.

## 2. The colour logic

Build the prompt from [the colour logic template](templates/colour-logic-request.md): the beat sheet or shot list, the style guide's colour and light rules quoted, and [the colour script template](templates/colour-script.md) as the exact form of its answer. Plan it, and run it on the user's yes when it costs anything. Send it as the [prompt roles](../../docs/prompt-roles.md) say.

Check the answer before showing it:

- every planned beat is there, once, in order, by its number and name;
- every beat has its dominant colours, its accent, its light, its contrast, its feeling, and how it changes from the beat before;
- every colour is from the style guide's palette, or is marked *departure* with its reason;
- the arc is stated in a few lines: where the film starts, where it turns, and where it ends.

When a check fails, correct the prompt as the [prompt roles](../../docs/prompt-roles.md) say. Show the colour logic to the user; their corrections win, and a correction they write is made in the colour script directly.

## 3. The keyframes

Fill [the keyframe template](templates/keyframe.md) once per beat, quoting its line of colour logic.

- Send the style sheet last, and before it any A-pose view, reference sheet, or grey form pass of a place the user wants the keyframe to show, within the number of references the model takes.
- Fill `{{style_rules}}` with the style guide's shapes and texture, quoted, or the look the user described when there is no style guide.
- Fill `{{references_line}}` with what each attached image is, in order, ending "The beat's own colour and light, above, win over the colours of every attached image." With nothing attached, it is empty.
- Plan the keyframes. Render three first, the opening, the biggest turn, and the ending, so the user can judge the range before the rest; then the rest on the user's yes.
- Report each output's path, named by its order and beat number, such as `03-beat-3`, so they sort in story order.
- Inspect each against its line of colour logic, and report honestly where it drifted, such as a cold beat that came out warm.

## 4. Lay it out

Fill the Keyframes section of the colour script: every keyframe in story order, each with its number, name, and line of colour logic beneath it. Show it to the user as one row, in order, so the arc can be judged as a whole.

Never redraw the keyframes into one image with a model: it would change them. The user judges the arc and asks for changes beat by beat. A change to one beat's logic remakes only that beat's keyframe, as a new paid request on the user's yes; every other keyframe stays as it was.

## 5. Hand back

Record which keyframes the user approved, and the date, in the colour script.

Hand back to the caller:

- the colour script: the arc, the colour logic per beat, and the keyframes in story order;
- the prompts that made them.

Every later image of a beat in colour, a place's lighting or a shot, quotes that beat's line of colour logic; boards stay grey and take none of it. Each may be sent its keyframe as a reference for colour and light only.
