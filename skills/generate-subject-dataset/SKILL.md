---
name: generate-subject-dataset
description: Make a dataset of images of an existing recurring subject - a set of images on one theme, such as a day at the beach, scenes from a story, or the variety a LoRA is trained on - from the subject's base reference (a character's A-pose views, or another subject's reference sheets) with an image-edit model, first having an A-pose made for any new outfit of a character, or a sheet for any new variant, prop, or recurring object the theme needs. A subject is anything that must look the same every time it appears, such as a character, a creature, a prop, or a vehicle. Use when the user asks for a gallery, set, series, or dataset of images of a subject that already has a reference. Not for building the subject's reference itself.
---

# Subject dataset

A dataset starts from a subject that already exists, and a theme. The subject's look comes from its published reference. If the subject has no reference yet, it needs one first, from `generate-subject-reference`, approved by the user.

Every image comes from an image-edit model that takes the subject's references as input. Never build a dataset with a text-to-image model: it cannot hold the subject from its references.

## Find the specifics

- **The workflow skill** of the image-edit model the request names, or that the user chooses, says how many references it takes and the sizes it makes; **its prompt skill** gives its syntax and limits. Both come from the setup, as the [prompt roles](../../docs/prompt-roles.md) describe.
- **Running it** is [project-requests](../project-requests/SKILL.md)': this skill builds each request and hands it back, and `project-requests` runs it with `scripts/request.py`, which sends it exactly as built. What a request costs comes from the setup.

Each step waits for the user's yes, and every paid request waits for a yes to its plan.

## What it needs

Each input by its canonical name, from the pipeline's table:

- the subject's base reference: for a character, its A-pose set, such as `<character>: A-pose front <outfit>`; for any other subject, its reference sheet, `<subject>: reference sheet`;
- its other sheets, such as `<subject>: detail sheet <prop>` or `<subject>: variant sheet <variant>`;
- its brief, `<subject>: brief`, when there is one;
- the concept's style sheet, `<look>: style sheet`, and its written rules, `<look>: style guide`, when it has one;
- the theme, from the user.

Characters who read as minors are kept as the [prompt roles](../../docs/prompt-roles.md) say.

## Filling the templates

The templates are written for any subject. Fill their subject words from the brief's kind of subject, so no prompt asks for a face, a pose, or an outfit the subject does not have:

- **For a character or a creature:** `{{identity_features}}` is "face, hair, eyes, skin, and markings" as it has them; `{{form_word}}` is "outfit"; `{{expression_line}}` gives a row's expression, as a new line, such as `- Expression: surprised.`. For a character, `{{character}}` is its name, and `{{them}}` and `{{their}}` its pronouns.
- **For any other subject,** such as a prop or a vehicle: `{{identity_features}}` is the shape, parts, and markings that make it recognisable; `{{form_word}}` is "variant"; `{{expression_line}}` is empty.
- Every canonical value a slot holds, such as the subject's name or a prop's, is written in the step's template as `{{<element>: <fact>}}`, filled from the pipeline's table, never typed in by hand.
- `{{references_list}}` names each attached image in the order sent, as a sentence saying what it is and how it was made, such as "The first attached image is a generated character model of Mira in a symmetrical A-pose, seen straight from the front, a textured viewport capture made for an animated film. The second is the same model seen from the back. The third is the concept's style sheet."
- `{{subject_source}}` is "the first attached image" for a character, or "the attached reference sheets" for another subject.
- `{{style_line}}` is "drawn in the style of the concept's style sheet, the last attached image" when one is sent; otherwise "drawn in this style:" and the brief's art style. `{{style_source}}` is "the last attached image, the concept's style sheet" when one is sent; otherwise "the first attached image".
- `{{form_line}}`, for another subject's row in a variant, is a new line, `- {{Form_word}}: as the second attached image shows.`; otherwise it is empty.
- `{{prop_line}}` names the prop by the image that shows it, such as "the mug from the third attached image, held in both hands", or "none".
- A detail sheet's `{{subject_image}}` names the attached image of the subject, such as "the third attached image, the front A-pose of Mira", and its `{{relation}}` says how the detail belongs to the subject, such as "the prop {{name}} carries" or "a part of {{name}}".
- In the outfit A-pose template, `{{outfit_image}}` says what the second image is and how it was made, and `{{outfit}}` is "the outfit from the second image". When no image shows the outfit, `{{outfit_image}}` is empty and `{{outfit}}` describes it in words.

What a prompt sent with images says is in the [prompt roles](../../docs/prompt-roles.md).

## 1. Plan

Write the dataset plan: the theme in a sentence or two, then one row per image.

| id | scene | outfit or variant | props and objects | expression or detail | background | aspect |
|---|---|---|---|---|---|---|

Each id is short, lowercase, and hyphenated. Show the plan; the user's corrections win.

## 2. New reference

List everything the plan needs that the reference does not show:

- a new outfit or variant;
- a new prop;
- a recurring object that must look the same in more than one image.

For each one, make it from the base reference:

- **a character's new outfit:** fill [the outfit A-pose template](templates/a-pose-outfit.md), sent with the character's textured front A-pose first and the image that shows the outfit second: the same A-pose and view, with only the outfit changed. When rows show the outfit from another side, make those A-pose views from the approved new front, as `generate-subject-reference` makes them;
- **another subject's new variant:** fill [the variant template](templates/reference-outfit.md), sent with the reference sheet first and the image that shows it second;
- **a new prop or object:** fill [the detail template](templates/reference-prop.md), sent with the images that show it, then the subject's base reference: for a character, its textured front A-pose.

Build each request and hand it back; `project-requests` runs it on the user's yes. The dataset waits until its new references are approved and published by `project-pipeline`. They belong to the dataset; they are not added to the subject's own reference.

Something that appears once, and need not match anything, can stay in the prompt alone.

## 3. Prompts

Write one prompt per row from [the entry template](templates/entry.md), with the row's scene and the theme. When the concept has a style guide, send its style sheet last, after the subject's references; quote its written rules only for what the style sheet does not show. Say what each attached image is, then only what no image gives: the scene, framing, view, pose, expression, which prop, and background. Never describe the subject's look, outfit, or props in words. Keep the one-subject line unless the user's plan puts others in the scene.

Attach, in this order:

1. for a character, its textured front A-pose in the row's outfit, then the A-pose view nearest the row's view when that is not the front; for any other subject, its reference sheet, then the row's variant sheet when it is not the default;
2. a sheet for each prop or object in the row;
3. the style sheet, last, when there is one.

## 4. Generate

Generate a few rows first, and compare them with the references before asking to run the rest. Inspect every image for drift from the reference, wrong colours, and broken anatomy or structure, and report honestly. A new version is a new paid request, and needs the user's yes.

When the dataset is flat digital art, say a cleanup may help.

## 5. The user's choice

The user chooses which images to approve and which version of each; never choose yourself. The approved images are published by `project-pipeline`; the rest are never used as inputs again.

## Hand back

Hand back to `project-requests`, in order, the new references first, then a few rows, then the rest:

- for each new outfit, variant, prop, or object, and for each row, the request: the image-edit endpoint; the prompt as a template naming canon, `{{<element>: <fact>}}`; and the references by canonical artifact, each with its role, in the order to send them, as step 3 gives;

and, for the user to approve:

- the dataset plan;
- each new reference, before the rows that use it;
- the first few rows, before the rest are run;
- the images of the dataset, and any cleaned-up versions, to choose from.
