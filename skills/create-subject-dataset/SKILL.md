---
name: create-subject-dataset
description: Make a dataset of images of an existing recurring subject - a set of images on one theme, such as a day at the beach, scenes from a story, or the variety a LoRA is trained on - from the subject's reference sheets with an image-edit model, first having a sheet made for any new outfit, prop, or recurring object the theme needs. A subject is anything that must look the same every time it appears, such as a character, a creature, a prop, or a vehicle. Use when the user asks for a gallery, set, series, or dataset of images of a subject that already has a reference. Not for building the subject's reference itself.
---

# Subject dataset

A dataset starts from a subject that already exists, and a theme. The subject's look comes from its reference: its sheets, and its brief when there is one, in the folder the caller names. If the subject has no reference yet, it needs one first: a brief and reference sheets, approved by the user.

Every image comes from an image-edit model that takes the reference sheets as input. Never build a dataset with a text-to-image model: it cannot hold the subject from sheets.

## Find the specifics

The **execution skill** that implements `create-subject-dataset` in this setup, or else the setup's renderer, says:

- which image-edit model runs;
- how to send a request with its references;
- what it costs.

It comes from the setup, as the [prompt roles](../../docs/prompt-roles.md) describe.

The caller gives an artifact folder, for prompts and images saved flat, and a work folder, for everything else. Each step waits for the user's yes, and every paid request waits for a yes to its plan.

Every image of a character who reads as a minor stays ordinary and everyday. Nothing is sexual or suggestive, in any image, theme, or prompt.

## Filling the templates

The templates are written for any subject. Fill their subject words from the brief's kind of subject, so no prompt asks for a face, a pose, or an outfit the subject does not have:

- **For a character or a creature:** `{{identity_features}}` is "face, hair, eyes, skin, and markings" as it has them; `{{stance}}` is "full body, standing in a neutral relaxed pose, arms slightly away from the body"; `{{form_word}}` is "outfit"; `{{default_expression}}` and `{{expression_line}}` give its expression; `{{personality}}` gives its personality.
- **For any other subject,** such as a prop or a vehicle: `{{identity_features}}` is the shape, parts, and markings that make it recognisable; `{{stance}}` is "at rest on a level surface"; `{{form_word}}` is "variant"; the expression and personality placeholders are left empty.
- A detail sheet's `{{relation}}` says how the detail belongs to the subject, such as "the prop {{name}} carries" or "a part of {{name}}".

## 1. Plan

Write `dataset.md` in the work folder: the theme in a sentence or two, then one row per image.

| id | scene | outfit or variant | props and objects | expression or detail | background | aspect |
|---|---|---|---|---|---|---|

Each id is short, lowercase, and hyphenated. Show the plan; the user's corrections win.

## 2. New reference

List everything the plan needs that the reference does not show:

- a new outfit or variant;
- a new prop;
- a recurring object that must look the same in more than one image.

For each one, make one sheet from the base sheet: fill [the outfit or variant template](templates/reference-outfit.md), sent with the base sheet first and the image that shows it second; or [the detail template](templates/reference-prop.md), sent with the images that show it and the base sheet. Plan it, render it on the user's yes, and show it to the user. The dataset waits until its new sheets are approved. The new sheets belong to the dataset, and are handed back with it; they are not added to the subject's own reference.

Something that appears once, and need not match anything, can stay in the prompt alone.

## 3. Prompts

Write one prompt per row from [the entry template](templates/entry.md), with the row's scene and the theme. When the concept has a style guide, quote its written rules for the look, and send its style sheet last, after the subject's sheets. Keep the one-subject line unless the user's plan puts others in the scene.

Attach, in this order:

1. the base sheet;
2. the row's outfit or variant sheet, when it is not the default;
3. a sheet for each prop or object in the row.

## 4. Generate

Generate a few rows first, and compare them with the sheets before asking to run the rest. Inspect every image for drift from the reference, wrong colours, and broken anatomy or structure, and report honestly. A new version is a new paid request, and needs the user's yes.

When the dataset is flat digital art, say a cleanup may help.

## 5. The user's choice

Show the user the dataset, and any cleaned-up versions, and point them to the full-size files. The user chooses which images to keep and which version of each; never choose yourself. Hand the kept images and the dataset's new sheets back to the caller.
