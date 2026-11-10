---
name: create-subject-reference
description: Build a recurring subject's full reference - a brief, reference sheets (a base turnaround, one per outfit or variant, one per detailed prop or part), and the reference gallery a dataset is chosen from - with an image-edit model, then hand the user the images to choose from. A subject is anything that must look the same every time it appears, such as a character, a creature, a prop, or a vehicle. Use when the user asks to design or make a character or other recurring subject, an outfit or prop sheet, or its reference gallery or dataset images. Not for cleaning, captioning, or training.
---

# Subject reference

A subject's reference is everything that fixes what it looks like: its brief, its reference sheets, and its reference gallery. A subject is anything that must look the same every time it appears: a character, a creature, a prop, or a vehicle. This skill makes the reference and stops at the user's choice. It hands the kept images and the brief back to the caller.

Some parts apply only to a character, such as outfits and expressions. For another subject, use what fits, such as its variants and the details that make it recognisable, and leave out the rest.

## The model

Every image here comes from an **image-edit model**: one that takes the reference sheets as input images and keeps them. Never use a text-to-image model, even with a LoRA. It cannot hold a subject from sheets, so the reference would not stay consistent.

## Find the specifics

The **execution skill** that implements `create-subject-reference` in this setup, or else the setup's renderer, says:

- which image-edit model runs;
- how a request is sent with its reference images;
- what it costs;
- where its output lands.

When that model has a workflow skill, read it for how to prompt it. Both come from the setup, as the [prompt roles](../../docs/prompt-roles.md) describe.

The caller gives:

- the user's request and input images;
- the concept's style guide, when it has one: its written rules and its style sheet;
- an artifact folder, for prompts and images, each saved flat beside its prompt;
- a work folder, for everything else: the brief, the dataset plan, and the model's records.

Each step waits for the user's yes before the next. Every paid request waits for a yes to its plan: the number of requests and an estimate.

Every image of a character who reads as a minor stays ordinary and everyday. Nothing is ever sexual or suggestive, in any step, prompt, or caption.

## Filling the templates

The templates are written for any subject. Fill their subject words from the brief's kind of subject, so no prompt asks for a face, a pose, or an outfit the subject does not have:

- **For a character or a creature:** `{{identity_features}}` is "face, hair, eyes, skin, and markings" as it has them; `{{stance}}` is "full body, standing in a neutral relaxed pose, arms slightly away from the body"; `{{form_word}}` is "outfit"; `{{default_expression}}` and `{{expression_line}}` give its expression; `{{personality}}` gives its personality.
- **For any other subject,** such as a prop or a vehicle: `{{identity_features}}` is the shape, parts, and markings that make it recognisable; `{{stance}}` is "at rest on a level surface"; `{{form_word}}` is "variant"; the expression and personality placeholders are left empty.
- A detail sheet's `{{relation}}` says how the detail belongs to the subject, such as "the prop {{name}} carries" or "a part of {{name}}".

## 1. Brief

Fill [the brief template](templates/subject-brief.md) from the user's request and input images, and name the input images it is drawn from. When the concept has a style guide, its written rules are the brief's art style, quoted, not reworded. The brief includes:

- a **Trigger word**;
- **Fixed tags**, in the prompting style of the family a LoRA of the subject will be for.

Show the brief to the user; their corrections win.

## 2. Reference sheets

Each sheet is a separate 3:2 page with a header and one job, so no sheet is crowded.

- **Base sheet:** the subject in its default form, as a four-view turnaround: front, three-quarter, side, and back.
  - Fill [the base template](templates/reference-base.md), and send it with the input images as references, then the concept's style sheet when there is one, so the subject is drawn in the concept's look.
  - If the user supplies a base sheet, use theirs.
- **Outfit or variant sheet,** one per other outfit, or other version of the subject: the same turnaround and layout, with only that changed.
  - Fill [the outfit template](templates/reference-outfit.md).
  - Send it with the base sheet first, and the input image that shows the outfit or variant second.
- **Prop or detail sheet,** for a prop, a recurring object, or a part of the subject that needs detail to stay consistent: views of it alone, labelled close-ups, and one small in-use panel for scale.
  - Fill [the prop template](templates/reference-prop.md).
  - Send it with the input images that show it, and the base sheet.

**A-pose views,** for a character, once its primary canonical image is approved: the cleanest working map of the character, as a 3D model would show it. Make them in order, each step from the user's choice in the one before:

1. **The front A-pose, as a textured viewport view:** fill [the A-pose template](templates/a-pose.md) and send the primary canonical image alone. It asks for the character as a 3D model in a viewport's material preview, under neutral light: the mood and lighting are already held by the primary canonical image, so the A-pose starts neutral and is itself the texture view. An A-pose is symmetrical: upright with no lean, the head facing straight ahead, the arms at the same angle on both sides. It needs to be a good working map of the character, not a pose fit for rigging. Reject any view that turns the head, tilts the body, or poses the arms unevenly.
2. **The other views:** fill [the A-pose view template](templates/a-pose-view.md) for the back, the left side, and the right side, each sent with the approved front alone.
3. **Without outer layers:** when an outer layer, such as an apron or a coat, hides what is under it, fill [the layer template](templates/a-pose-layer.md) for the front without it, sent with the approved front alone, then its back and sides from that, as in step 2.
4. **The form passes:** convert every view with `create-concept-art`'s grey form and coloured form passes; the texture pass is not needed, since each view already is one. The form passes are the ones agents use most: with no texture, the character's contours and silhouette are clearest. For the coloured form, choose one flat colour per part, such as skin, shirt, apron, trousers, and shoes, and name them in every view's prompt, so the colours agree across views.

Keep each view whole, at one scale, on a plain background, cut away afterwards to a transparent one. These views feed the height chart and every later image of the character.

Expressions, head angles, poses, and gestures belong in the gallery, not on a sheet.

Make one sheet per request. Inspect each for drift from the base sheet, wrong colours, and broken anatomy or structure, and report honestly. A new version is a new paid request, and needs the user's yes.

When a later set of images of the subject asks for one new sheet, make only that sheet, from the existing base sheet.

## 3. Reference gallery

Fill [the dataset template](templates/dataset.md): a matrix of framings, views, outfits or variants, expressions or details, props, and backgrounds. Then write one prompt per row.

Send each row with:

- the base sheet first;
- the row's outfit or variant sheet, when it is not the default;
- the prop or detail sheet, when the row has it;
- the concept's style sheet last, when there is one.

Run a few rows first, and compare them with the sheets and the input images before asking to run the rest.

Image-edit models leave grain in flat digital art. Say so when the gallery is done, so the caller can have it cleaned up before the user chooses. Never offer a redraw by a text-to-image model: one took a character's gallery off model.

## 4. The user's choice

Show the user the gallery, and any cleaned-up versions beside it, and point them to the full-size files. The user chooses which images to keep and which version of each; never choose yourself. Record each choice in the dataset plan's Kept images section.

Hand back to the caller:

- the kept images, each named by its row id;
- the brief;
- the top sheets: base, each outfit or variant, and each prop or detail.
