---
name: create-style-guide
description: Make a concept's style guide - the written rules of its look (shapes, line, proportion, colour, light, texture, and what to avoid), drafted by a language model from a prompt this skill builds, and the images that show them (style frames to choose from, then a style sheet) - from the user's words and, when they have them, their own artwork. Use when the user asks for a style guide, a visual identity guide, an art direction, or "the look" of a show, a short, or any concept; it comes before subjects, locations, or boards are designed, since they all follow it. Not for one subject's reference or a colour script.
---

# Style guide

A style guide fixes how everything in a concept looks, so every later image, from a subject's sheet to a board to a shot, can be made and judged against it. It has two halves that must agree: the **written rules**, which a prompt can quote and the user can check against; and the **images**, which show what the words cannot. This skill plans both and builds every prompt they need, and stops at the user's choices. The images it keeps become the concept's style references.

## The models

- **The written rules** come from a language model, run on a prompt this skill builds.
- **Style frames** come from an image model. When the user gives their own artwork, use an **image-edit model** with that artwork as references, so the style is theirs; the user's own art is the strongest source of a look, and is never replaced by a model's guess. With no artwork, use a **text-to-image model**.
- **The style sheet** always comes from an **image-edit model**, sent with the chosen style frame, or with the user's artwork when it settled the look. Never make the sheet from text alone: it would drift from what the user chose.

## Find the specifics

- **The workflow skill** of each model the request names, or that the user chooses, says which way of running it takes text alone and which takes references, how many references it takes, and the sizes it makes. **Its prompt skill** gives its syntax and limits.
- **The execution skill** that implements `create-style-guide` in this setup runs the prompts; when none does, the setup's renderer. It says what a request costs and where its output lands. The language model may be the agent itself, when the setup says so.

All come from the setup, as the [prompt roles](../../docs/prompt-roles.md) describe. If one is missing, say which and stop.

The caller gives the user's request, the concept's brief when there is one, the user's artwork when there is any, and a folder for the guide, its prompts, and its images, each saved beside its prompt.

Each step waits for the user's yes before the next. Every paid request waits for a yes to its plan: the model, the number of requests, and the cost.

Every image of a character who reads as a minor stays ordinary and everyday. Nothing is sexual or suggestive, in any step or prompt.

## Image prompts

Every image prompt here says what the picture is for, then what is in it, then how it looks. With reference images, it also says what each reference is for, because the model cannot guess which parts to keep. Write it in this order, for any model:

1. **What the image is:** one line naming the kind of image and its use, such as "a style frame for an animated production" or "a style sheet". The kind sets the model's expectations for layout and finish.
2. **The subject:** who or what, doing what, where. Describe characters by what they look like or by role ("the girl in the red cap"), never by a real person's name.
3. **The layout,** when the image is a page: its shape, its panels in reading order, what each panel holds, and its labels. Say the labels' exact words in quotes, and keep them few and short; models misspell long text.
4. **The look:** shapes and proportion, line, colour, light and shadow, and texture, in concrete terms an image can be checked against, such as "thick, even outer lines; flat colour; one soft shadow tone". Quote the written rules here rather than rewording them.
5. **The references,** when there are any: what each one is, in the order they are sent, and what to keep from it, such as "the first attached image is the chosen style frame: match its line and colour exactly". Say what must not change, and that the model must not switch to another rendering style.
6. **What to leave out:** text, logos, borders, extra figures, or anything the request rules out. Say it plainly, as a sentence; a model reads "no text" better than a list of banned words.

Keep each part to a sentence or a few short lines. Long prompts make models drop parts, and a page with many panels needs each panel to be short. Leave out what the model ignores, as its prompt skill says.

Text to image has nothing to hold it to a look but the words, so the look carries all of it. An edit with references holds the style from the images, so the references carry most of it, and the look only says what they do not show. When the request has artwork, never write a frame as text to image instead: it would drift from the artwork.

Put each part into its field in the model's syntax, as its prompt skill says, and name the references, in order, as the job's inputs, by the [prompt roles](../../docs/prompt-roles.md). Write each prompt with the setup's prompt writer, naming the prompt skill the workflow skill gives.

## 1. The written rules

Build the prompt for the rules from [the rules prompt template](templates/rules-prompt.md): the user's request, the brief, a description of each piece of artwork, or the artwork itself when the language model takes images, and [the style guide template](templates/style-guide.md) as the exact form of its answer. Plan it, and run it on the user's yes when it costs anything.

Check the answer before showing it: every section of the template is filled; each rule names the artwork it is drawn from, or is marked *proposed*; and each rule is concrete enough to check an image against, such as "thick, even outer lines; thin inner lines; no hatching" rather than "bold lines". When it is not, build a corrected prompt that says what was wrong, and run it again.

Show the rules to the user; their corrections win. A correction the user writes is made in the rules directly.

## 2. Style frames

Unless the user's artwork already settles the look, make three to four **style frames**: one image each, of the same small scene, in a different reading of the rules, so the user can choose a direction by eye.

- Fill [the style frame template](templates/style-frame.md) once per direction; only the direction's lines change between them.
- Send the user's artwork as references when there is any.
- Plan the frames, render them on the user's yes, and report each output's path.
- Inspect each frame against the written rules, and report where it breaks them.

The user chooses one direction, or asks for a mix; never choose for them. Update the written rules to match what they chose.

## 3. The style sheet

Make one **style sheet** from the chosen frame and the final rules: a single page that shows the look's parts side by side, for every later prompt to be sent with.

- Fill [the style sheet template](templates/style-sheet.md).
- Send the chosen style frame first, then the user's artwork. When the artwork settled the look and no frame was made, send the artwork alone.
- Inspect it against the rules and the chosen frame: line weight, shapes, palette, and light. A new version is a new paid request, and needs the user's yes.

## 4. Hand back

Record the style references in the guide's Style references section: each file, and what the user chose it for.

Hand back to the caller:

- the written rules, final;
- the chosen style frame and the style sheet, as the concept's style references;
- the user's own artwork it was drawn from.

Every later task in the concept, a subject's reference, a location, a board, or a shot, is prompted with the written rules and sent with the style sheet.
