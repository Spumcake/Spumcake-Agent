---
name: create-location-reference
description: Build a recurring place's full reference, so a camera can move through it and keep it - a brief, an establishing sheet, a plan of its layout from above with numbered camera positions, a view from each position, a sheet of the props that belong to it, and lighting keys that show the same place under each recurring mood or time of day - with an image-edit model sent the user's art or chosen concept art, the approved views, and the concept's style sheet, using text to image only for a first exploration when there is no art at all. Use when the user asks for a location, a set, an environment or background reference, views of a place from several angles, a floor plan of a set, its set dressing, or its lighting keys. Not for a character's or a handled prop's own reference, or the colour and mood of a whole film.
---

# Location reference

A location's reference is everything that fixes what a place looks like, so a camera can move through it, shot after shot, and find the same room: the same door on the same wall, the same table under the same window, the same light at the same hour. It has a brief, an establishing sheet, a plan of the layout from above, a view from every camera position the film needs, a sheet of the props that belong to the place, and lighting keys for each recurring mood or time of day.

A good reference agrees with itself: every view puts each thing where the plan puts it, and every lighting key changes only the light. A failed one moves a window between views, adds a doorway the plan does not have, or redraws the room when only the evening light was asked for.

## The models

- **Everything** comes from an **image-edit model**, sent the place's art and its approved images as references, so each new image is held to what is already fixed.
- **Only a first exploration,** when there is no art of the place at all, comes from a **text-to-image model**: two or three establishing views for the user to choose from. Everything after is made from the chosen one. When the concept has a style sheet, the exploration is an image edit sent the style sheet alone.

## Find the specifics

- **The workflow skill** of the model the request names, or that the user chooses, says which way of running it takes text alone and which takes references, how many references it takes, and the sizes it makes. **Its prompt skill** gives its syntax and limits.
- **The execution skill** that implements `create-location-reference` in this setup renders it; when none does, the setup's renderer. It says what a request costs and where its output lands.

All come from the setup, as the [prompt roles](../../docs/prompt-roles.md) describe. If one is missing, say which and stop. When the request names no model and more than one fits, ask.

## What it needs

From the caller:

- the user's request, and the place's name as the script uses it;
- the scenes set there, from the approved script or shot list, when there is one: what happens, who enters and leaves where, and what the camera sees;
- the user's art of the place, or its chosen concept art, when there is any;
- the concept's style guide, when it has one: its written rules and its style sheet;
- the colour script's lines for the moods set there, when there is one;
- the film's aspect ratio, from the shot list or the style guide; 16:9 when neither says;
- a folder for the brief, the prompts, and the images, each image saved beside its prompt.

Each step waits for the user's yes before the next. Every paid request waits for a yes to its plan: the model, the number of requests, and the cost. A first run on a new model is one image, as a test, before the rest.

Every image of a character who reads as a minor stays ordinary and everyday. Nothing is sexual or suggestive, in any step or prompt.

Use only art and photographs the user has the right to use this way. Show a recognisable real person only when the user confirms that the person agreed to this use, or a guardian did for a child; never to deceive anyone.

## Location prompts

A place drifts between images unless each prompt pins where the camera is and what it sees there. Write every prompt in this order, for any model:

1. **What the image is:** "a LOCATION SHEET", "a plan", "a view", "a PROPS SHEET", or "a LIGHTING KEY" of the place, for an animated production, and what it is for.
2. **The references,** in the order sent, and what each fixes: "The first attached image is the establishing sheet of the Kitchen: its layout, architecture, materials, and colours are fixed." The style sheet last, for line, colour, and light only.
3. **The camera,** for a view or a lighting key: its numbered position from the plan, where it stands, which way it faces, how high, and how wide.
4. **What is seen,** left to right and near to far, by the brief's names, so the layout holds.
5. **The light:** for a sheet, a plan, or a view, the place's plain, even base light, so its shapes read and a lighting key can change it later; for a lighting key, the mood's light, quoting the colour script's line when there is one.
6. **The look:** the style guide's written rules for environments, quoted.
7. **What to leave out:** characters, unless the user wants a figure for scale, and text, except a sheet's own labels, as a plain sentence.

Keep each part short; a view with many things in it names only what the camera sees. Say what must not change, every time. Leave out what the model ignores, as its prompt skill says.

Put each part into its field in the model's syntax, as its prompt skill says: the words in `prompt`, what to avoid in `negative` when the model takes it, and the images, in order, in `references`, by the [prompt roles](../../docs/prompt-roles.md). Write each prompt with the setup's prompt writer.

`{{references_list}}` in every template names each attached image on its own line, in the order sent, with what it fixes. `{{style_rules}}` is the style guide's written rules for environments, quoted, or the look the brief describes when there is no style guide. `{{base_light}}` is the brief's base light. On the establishing sheet, `{{scale_line}}` and `{{scale_exception}}` are "One plain grey standing figure, {{height}} tall, near {{where}}, for scale." and ", except the grey figure for scale" when the user wants a figure for scale; otherwise both are empty. On a lighting key, `{{colour_script_line}}` is "The colour script's line for this mood: " and that line, quoted, when there is one; otherwise it is empty.

## 1. The brief

Fill [the location brief template](templates/location-brief.md) from the request, the art, and the scenes set there: the layout in words, its scale, its materials, its palette, the props that belong to it, the camera positions the shots need, and the recurring moods or times of day.

Show the brief to the user; their corrections win.

## 2. The establishing sheet

Fill [the establishing sheet template](templates/establishing-sheet.md): one page with the place's main view, its palette, and its materials.

- Send the user's art or the chosen concept art first, then the style sheet last.
- With no art at all, make two or three first explorations instead, from the same template, by text to image, or sent the style sheet alone; the user chooses one, and its sheet is then made from it.
- Plan it, render it on the user's yes, and report its path. Inspect it against the brief and the art, and report honestly where it differs.

The establishing sheet is the place's base sheet: it is sent first with everything after it.

## 3. The plan

Fill [the plan template](templates/location-plan.md): the place from directly above, with its walls, openings, and fixed furniture, its areas labelled, and each camera position numbered with an arrow for the way it faces.

Send the establishing sheet first, the art next, and no style sheet: a plan is a diagram. Models get a plan's geometry wrong more often than a view's. Show it to the user, and ask them to correct it: when they draw or describe a corrected plan, theirs is the plan, and is used as given. Once approved, the plan is the truth of the layout, and the camera positions keep their numbers.

## 4. The views

Make one view per camera position on the plan, from [the view template](templates/location-view.md), in the film's aspect ratio.

- Send the establishing sheet first, the plan second, an approved view that shares the most of this one's area third, and the style sheet last, within the number of references the model takes.
- Name each view by its position, such as `kitchen-view-3`.
- Make the first view, show it, and make the rest on the user's yes.
- Inspect each against the plan: every door, window, and piece of furniture where the plan puts it, and nothing the plan does not have. Report honestly what moved.

## 5. The props

When the place has props that recur in its shots and must match, fill [the props template](templates/location-props.md): each prop alone, labelled, at one consistent scale, with a small panel of where it sits in the place. Send the establishing sheet first, the views that show the props next, and the style sheet last.

A prop a character handles, or one that matters to the story on its own, is a subject with its own reference; say so, and leave it off this sheet.

## 6. The lighting keys

For each recurring mood or time of day in the brief, make a lighting key of the establishing view and of the views the shots use most, from [the lighting key template](templates/lighting-key.md).

- Send the base view it relights first, the establishing sheet second, and the style sheet last.
- Quote the colour script's line for that mood when there is one; otherwise the brief's.
- Make one key first, show it, and make the rest on the user's yes.
- Inspect each against its base view: the camera, the layout, and every object unchanged; only the light, its colour, and its shadows different. Report honestly what else changed.

Name each by its view and mood, such as `kitchen-view-3-night`.

## 7. Hand back

Record in the brief's Kept images section which images the user chose to keep as the place's references, and the date.

Hand back to the caller:

- the brief;
- the establishing sheet, the approved plan, and the views, each named by its camera position;
- the props sheet, when there is one;
- the lighting keys, each named by its view and mood.

Every later image set in the place, a board or a shot, is sent the view nearest its camera, the establishing sheet, and, for its mood, the matching lighting key, with the subjects' base sheets before them and the style sheet last, within the number of references the model takes.
