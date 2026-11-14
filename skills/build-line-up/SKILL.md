---
name: build-line-up
description: Make a line-up or a height chart of several subjects - each standing side by side on one ground line at its true relative scale, exactly as its own base reference shows it (a character's front A-pose, or another subject's reference sheet), with names, and for a height chart a labelled grid of heights - composited from the characters' A-pose fronts, with no model, so nothing is redrawn and the same inputs make the same chart again; or, only when a subject has no A-pose front, the image-edit request that makes it, sent every subject's base reference and the concept's style sheet, split into groups that share one anchor subject when there are more subjects than the model takes references, so every shot with several of them keeps their sizes. Use when the user asks for a line-up, a cast line-up, a height chart, a size comparison, or the scale of several characters, creatures, props, or vehicles against each other. Not for one subject's own sheets, or a scene of several subjects together.
---

# Line-up

A line-up puts several subjects side by side at their true relative scale, so every board and shot with more than one of them keeps their sizes: who comes up to whose shoulder, how a creature towers over a child, how a car sits beside its driver. A height chart is the same line-up on a grid of labelled heights, so the scale can be read as numbers as well as by eye. A subject is anything that must look the same every time it appears: a character, a creature, a prop, or a vehicle.

A good line-up shows every subject exactly as its base reference shows it, feet on one ground line, in the same view, with heights that match the approved numbers and its own grid. A failed one makes everyone about the same height, redraws a subject off model, or draws a grid its own subjects do not stand against.

## How it is made

A line-up is **composited**, with no model, whenever every subject has a front view on a transparent background: each is scaled to its height and stood on one ground line, and nothing is redrawn, so nothing drifts off model, and the same inputs make the same chart again. It costs nothing.

Only when a subject has no such view does the line-up need an **image-edit model** that takes the subjects' base references as input images and keeps them. Never use a text-to-image model: it cannot hold one subject from its references, let alone several. The number of references a model takes limits how many subjects one request can hold; step 3 says what to do when there are more.

## Find the specifics

- **The workflow skill** of the model the request names, or that the user chooses, says how many references it takes, the sizes and widest shape it makes, and how well it draws short labels. **Its prompt skill** gives its syntax and limits.
- **The cost** of a generated line-up comes from the setup, and waits for the user's yes before anything is paid.

This skill builds each request and hands it back; [project-requests](../project-requests/SKILL.md) runs it with `scripts/request.py`, which sends it exactly as built. The specifics come from the setup, as the [prompt roles](../../docs/prompt-roles.md) describe. If one is missing, say which and stop. When the request names no model and more than one fits, ask.

## What it needs

Each input by its canonical name, from the pipeline's table:

- two or more subjects, each with its base reference, in the outfit or variant the line-up shows: a character's front A-pose on a transparent background (`<character>: front A-pose`), in each pass the chart needs, such as the grey and the textured; any other subject's reference sheet, or its variant sheet (`<subject>: reference sheet`); a subject with none needs its reference first;
- each subject's height (`<subject>: height`), from its brief or the user, in one unit for all of them, such as centimetres, or heads of one named subject;
- the order the user wants them in, when they have one;
- the concept's style guide, when it has one: its written rules and its style sheet (`<concept>: style sheet`).

Each step waits for the user's yes before the next. Every paid request waits for a yes to its plan: the model, the number of requests, and the cost. A first run on a new model is one request, as a test, before the rest.

Characters who read as minors, and recognisable real people, are shown only as the [prompt roles](../../docs/prompt-roles.md) say.

## 1. Plan

Fill [the line-up plan template](templates/line-up-plan.md): each subject by the script's name, its base reference by its canonical name, its outfit or variant, its height in the one unit, and its place in the order. The order is the user's; with none, it runs tallest to shortest. Choose an **anchor**: the subject every height is compared to, usually the main character.

Show the plan to the user; their corrections win. Once approved, the heights are published by `project-pipeline` as each subject's facts, and stay fixed: every later shot with these subjects is held to them.

## 2. Composite it

When every subject has a front view on a transparent background, the line-up or height chart is composited. Its steps, which the composite's command carries out:

1. Scale each subject's front view so its height matches the plan, from `{{<subject>: height}}`, never typed in by hand.
2. Stand every one on one ground line, in the planned order, evenly spaced, not overlapping.
3. Write each name beneath its subject, by its canonical name.
4. On a height chart, draw the labelled grid of heights behind them: a line every `{{step}}`, as the templates' filling below gives it, numbered in the one unit, the bottom line the ground line, labelled "0".

Make one chart for each kind of view the subjects have, such as the grey and the textured. The command is a `script` request: each subject's front view by its canonical artifact, with its role, such as "subject 2, Tom, 120 cm", in the planned order; and the file it makes, one image per chart. A script written for it belongs to the pipeline, as `project-pipeline` keeps it, so the chain can run it again.

Check the result against the plan: each subject unchanged from its front view, every foot on the ground line, and each height on its grid line.

## 3. When a subject has no front view

Only then is the line-up generated. Tell the user which subjects have no front view, and that a generated line-up redraws every subject.

### Fit the references

Count the references one request needs: one per subject, a character's front A-pose in the outfit the line-up shows, or any other subject's reference sheet or variant sheet, and the style sheet last. When they fit what the model takes, the line-up is one request.

When there are more, tell the user, and propose groups:

- Split the subjects into groups that each fit, with one place kept for the style sheet.
- Put the anchor in every group, at its same height, so the groups line up against each other.
- Keep neighbours in the order together, so each group is a stretch of the full line-up.
- Make each group a line-up of its own, and show the groups side by side, in order, as the full line-up.

When the groups' own images fit what the model takes, the user may ask for one combined line-up made from them, sent in order, with every subject named. It redraws subjects a second time, so inspect it hard against each base reference; when it drifts, the groups stand as the line-up.

Never drop a subject's base reference to make room and describe the subject in words instead: it would come back off model. When a model takes too few references for even the anchor and one other, say so, and ask the user to choose a model that takes more.

### Line-up prompts

With several references, the model cannot guess which image is which subject, or how big each should be. A line-up prompt says both before anything else. Write it in this order, for any model:

1. **What the image is:** "a line-up" or "a height chart" for an animated production: its subjects side by side at true relative scale, the source of truth for their sizes.
2. **The references,** one line each, in the order sent, saying what each is and how it was made: "The first attached image is a generated character model of Mira in a symmetrical A-pose, seen straight from the front, a textured viewport capture." The style sheet last, for line, colour, and light only. Never describe in words what the references show.
3. **The order and placement:** left to right, each by name, all in the same view, standing on one ground line, evenly spaced, not overlapping.
4. **The heights:** each subject's height as a number and as a landmark against the anchor, such as "Tom: 120 cm, the top of his head level with Mira's shoulder". Models follow a landmark better than a number; give both.
5. **The labels:** each name beneath its subject; on a height chart, the grid's lines and their numbers, in the one unit. Keep labels to a word or a number.
6. **What stays the same:** each subject exactly as its own image shows it, in its proportions, colours, and style.
7. **What to leave out:** scenery, props not in a subject's image, extra figures, and notes, as a plain sentence.

Keep each subject's line short and in the same form. Leave out what the model ignores, as its prompt skill says.

Put each part into its field in the model's syntax, as its prompt skill says: the words in `prompt`, what to avoid in `negative` when the model takes it, and the subjects' images, in order, in `references`, by the [prompt roles](../../docs/prompt-roles.md).

### Filling the templates

- `{{references_list}}` names each attached image on its own line, in the order sent, saying what it is and how it was made, such as "1. A generated character model of Mira in a symmetrical A-pose, seen straight from the front, a textured viewport capture." or "2. The reference sheet of the cart, a generated turnaround." When the style sheet is sent, its line is last: "The concept's style sheet: match its line, colour, and light, not its subjects."
- `{{subjects}}` is one line per subject, left to right, from the plan: its name, the attached image that shows it, its height, and its landmark against the anchor. Its look and outfit are in its image, never in words. Each height is written as its fact, `{{<subject>: height}}`, filled from canon, never typed in by hand.
- `{{identity_features}}` is "faces, shapes, and markings" when the line-up mixes kinds of subject; "faces, hair, and markings" when all are characters or creatures; and "shapes, parts, and markings" when none are.
- `{{stance}}` is "characters and creatures standing in a neutral relaxed pose, everything else at rest on the ground", trimmed to the kinds present.
- `{{aspect_ratio}}` is "16:9" for up to five subjects, and the widest shape the model makes for more.
- On a height chart, `{{step}}` is a round number of the plan's unit that gives eight to fifteen lines up to just above the tallest subject, and `{{grid_labels}}` lists every line's number in order, such as "0, 20, 40, ... 200".

### Make it

Fill [the line-up template](templates/line-up.md), or [the height chart template](templates/height-chart.md), once per request. Plan the requests, with their count and cost; each runs as its own cycle on the user's yes.

Inspect each result against the plan: each subject against its base reference, every foot on the ground line, and each height against its landmark and, on a chart, its grid. Report honestly what is off, such as "Tom reads at Mira's chin, not her shoulder". Do not correct it by eye: a new version is a new paid request, and needs the user's yes.

## 4. The user's approval

The user approves the line-up or height chart, or its groups in order. The approved result is published by `project-pipeline`; a rejected one is never used as an input again.

Every later image with several of these subjects, a board or a shot, quotes their heights as landmarks from the published facts, and may be sent the line-up after the subjects' own base references.

## Hand back

Hand back to [project-requests](../project-requests/SKILL.md):

- **the composite,** when every subject has a front view: its command, a `script` request, with each subject's front view by its canonical artifact and its role, in the planned order, and the files it makes, one chart per kind of view;
- or, when a subject has none, **the image-edit requests:** for each, the endpoint kind, the prompt as a template naming canon, `{{<subject>: height}}`, and the references by canonical artifact, each with its role, in the order to send them, one request per group;
- the plan, with the heights and the anchor, as the facts it settles, `<subject>: height`, for the user to approve.
