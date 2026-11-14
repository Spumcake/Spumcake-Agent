---
name: make-colour-script
description: Plan a film's colour script as requests - the written colour and light logic of every beat or sequence, drafted by a language model from a prompt this skill builds, then one small keyframe per beat painted in that logic with an image-edit model sent the concept's style sheet, or a text-to-image model when there is none, shown in story order so the arc of colour and light across the whole film can be judged at a glance - from the approved beat sheet or shot list and the concept's style guide, each request run by project-requests as its own cycle, with the user's approval between them. Use when the user asks for a colour script, a colour plan, colour keys for a film, or the mood or lighting arc of a story. Not for a concept's overall look, a place's or a character's mood reference, or the boards.
---

# Colour script

A colour script plans the mood of a whole film in colour and light, before anything is boarded or shot. It is a row of small keyframes, one per beat or sequence, in story order, so the user can see at a glance where the film is warm or cold, bright or dark, calm or tense, and where it turns. Every later image of a beat, a board, a background plate, or a shot, takes its colour and light from its line here.

It has two halves that must agree: the **colour logic**, a line per beat that a prompt can quote, saying what colours and light the beat has and why; and the **keyframes**, which show it. This skill plans both as requests, says what each request needs and how its prompt is built, and runs none of them: [project-requests](../project-requests/SKILL.md) runs each as its own cycle, and the user approves each before the next is built.

A good colour script has an arc you can read from across the room: neighbouring beats differ where the story turns and hold where it holds, and every colour comes from the style guide's palette or is marked as a departure. A failed one has every keyframe in the same palette, keyframes so detailed the colour is lost, or keyframes that ignore their own logic.

## The models

- **The colour logic** comes from a language model, run on a prompt this skill builds. The language model may be the agent itself, when the setup says so.
- **The keyframes** come from an **image-edit model**, sent the concept's style sheet as a reference, so every keyframe is in the concept's look. Only when the concept has no style sheet, use a **text-to-image model**. A keyframe is small and simple: big shapes of colour and light, not a finished illustration.

## Find the specifics

- **The workflow skill** of each model the request names, or that the user chooses, says which way of running it takes text alone and which takes references, how many references it takes, and the sizes it makes. **Its prompt skill** gives its syntax and limits.
- **The cost** of each request comes from the setup, and waits for the user's yes before anything is paid.

Each request is built here and run by `project-requests` with `scripts/request.py`, which sends it exactly as built. The specifics come from the setup, as the [prompt roles](../../docs/prompt-roles.md) describe. If one is missing, say which and stop. When the request names no model and more than one fits, ask.

## What it needs

Each input by its canonical name, from the pipeline's table:

- the approved beat sheet (`<film>: beat sheet`), or the approved shot list (`<film>: shot list`); with neither, one is planned and approved first;
- the concept's style guide, when it has one: its written rules, as their facts (`<concept>: palette`, `<concept>: lighting`, `<concept>: shadows`, `<concept>: shapes`, `<concept>: texture`), and its style sheet (`<concept>: style sheet`);
- the film's aspect ratio (`<film>: aspect ratio`), from the shot list or the style guide; 16:9 when neither says;
- when the user wants a keyframe to show them recognisably: each place's primary canonical location and its views, with their grey form passes (`<place>: primary canonical location`, `<place>: view <wall>`), and each character's front A-pose (`<character>: front A-pose`) or another subject's reference sheet (`<subject>: reference sheet`).

Each request waits for the user's yes to the plan before it runs, and each paid request for a yes to its model, its number of calls, and its cost. A first run on a new model is a short test before the rest. Each request is built only from the latest approved results of the requests before it.

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

Keep the colour-and-light part in the same form in every keyframe, and change only its words, so the differences the user sees are the logic's differences. Keep each part short, as `prompt-image` says. Leave out what the model ignores, as its prompt skill says.

Put each part into its field in the model's syntax, as its prompt skill says: the words in `prompt`, what to avoid in `negative` when the model takes it, and the images, in order, in `references`, by the [prompt roles](../../docs/prompt-roles.md).

Every canonical value a keyframe prompt quotes is written as its fact in the step's template, never typed in by hand: the beat's line as `{{beat <number>: dominant colours}}`, `{{beat <number>: accent}}`, `{{beat <number>: light}}`, `{{beat <number>: contrast}}`, and `{{beat <number>: feeling}}`; the look as `{{<concept>: shapes}}` and `{{<concept>: texture}}`; and the shape as `{{<film>: aspect ratio}}`.

## The plan

### The beats

From the beat sheet or the shot list, list its beats or sequences in story order, by their numbers and names. Propose one keyframe per beat, or per sequence when the film is long or the beats are many; most colour scripts have between eight and thirty. The user agrees the list, and every keyframe keeps its beat's number from then on.

Then show the user the plan: each request below, in order, with its category, its endpoint, what it needs, and its estimated cost, and where they approve between them.

### Request 1: the colour logic (write)

A language-model request, built from [the colour logic template](templates/colour-logic-request.md): the beat sheet or shot list, the style guide's colour and light rules quoted as their facts, and [the colour script template](templates/colour-script.md) as the exact form of its answer. Send it as the [prompt roles](../../docs/prompt-roles.md) say.

Check the answer before showing it:

- every planned beat is there, once, in order, by its number and name;
- every beat has its dominant colours, its accent, its light, its contrast, its feeling, and how it changes from the beat before;
- every colour is from the style guide's palette, or is marked *departure* with its reason;
- the arc is stated in a few lines: where the film starts, where it turns, and where it ends.

When a check fails, build a corrected prompt as the [prompt roles](../../docs/prompt-roles.md) say, as a new request.

**The user approves.** Their corrections win, and a correction they write is made in the colour script directly. The approved colour script is published by `project-pipeline` as `<film>: colour script`, with the facts it settles: `<film>: colour arc`, and for each beat, `beat <number>: dominant colours`, `beat <number>: accent`, `beat <number>: light`, `beat <number>: contrast`, `beat <number>: feeling`, and `beat <number>: change from the beat before`.

### Requests 2 to 4: three keyframes first (generate)

One request per keyframe, each filled from [the keyframe template](templates/keyframe.md), quoting its beat's line of colour logic as its facts. The first three are the opening, the biggest turn, and the ending, so the user can judge the range before the rest.

- Send the style sheet last, and before it any A-pose view, reference sheet, or grey form pass of a place the user wants the keyframe to show, each by its canonical artifact with its role, within the number of references the model takes.
- Fill `{{style_rules}}` with the style guide's shapes and texture, quoted as their facts, or the look the user described when there is no style guide.
- Fill `{{references_line}}` with what each attached image is, in order, ending "The beat's own colour and light, above, win over the colours of every attached image." With nothing attached, it is empty.
- Inspect each against its line of colour logic, and report honestly where it drifted, such as a cold beat that came out warm.

**The user approves** each keyframe, or asks for it again as a new request. Each approved keyframe is published by `project-pipeline` as `beat <number>: colour key`, made from the colour script and its references; a rejected one is never used as an input again.

### Requests 5 onwards: the rest of the keyframes (generate)

On the user's yes to the range, one request per remaining beat, in story order, built as the first three. **The user approves** each, and each approved keyframe is published as `beat <number>: colour key`.

### The row

Once every keyframe is published, show them as one row, in story order, each with its number, name, and line of colour logic beneath it, so the arc can be judged as a whole. The row is a comparison of the published keyframes, which `project-requests` adds to the last keyframe's report; it is not a new image.

Never redraw the keyframes into one image with a model: it would change them. The user judges the arc and asks for changes beat by beat. A change to one beat's logic is a new colour logic request for that beat, then a new keyframe request for that beat only, each on the user's yes; every other keyframe stays as it was.

Every later image of a beat in colour, a place's lighting or a shot, quotes that beat's line of colour logic as its facts; boards stay grey and take none of it. Each may be sent `beat <number>: colour key` as a reference for colour and light only.

## Hand back

Hand back to [project-requests](../project-requests/SKILL.md) the plan, in order:

1. **the colour logic,** a write request: the language model's endpoint, the prompt from the colour logic template, and the facts the answer settles; then the user's approval;
2. **three keyframes,** the opening, the biggest turn, and the ending, each a generate request: the endpoint kind, the prompt from the keyframe template naming canon, `{{beat <number>: <fact>}}`, and the references by canonical artifact, each with its role, in the order to send them, `<concept>: style sheet` last; then the user's approval of each, and their yes to the range;
3. **the rest of the keyframes,** one generate request per beat, in story order, built the same way; then the user's approval of each.

Each request is built when the approvals before it are in, from what was published.
