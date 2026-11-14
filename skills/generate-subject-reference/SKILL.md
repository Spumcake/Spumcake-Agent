---
name: generate-subject-reference
description: Build a recurring subject's full reference - a brief; its base reference, which for a character is its A-pose set (the front A-pose as a textured viewport view from the approved primary canonical image, then the back and both sides, then the same without outer layers, then grey and coloured form passes, with one more A-pose set per other outfit), and for any other subject, such as a prop, a creature, or a vehicle, a four-view reference sheet and one per variant; a sheet per detailed prop or part, or one sheet for a small prop; and the reference gallery a dataset is chosen from - with an image-edit model, then hand the user the images to choose from. A subject is anything that must look the same every time it appears. Use when the user asks to make a character's A-poses or another recurring subject's reference, an outfit or prop sheet, or its reference gallery or dataset images. Not for the primary canonical image, cleaning, captioning, or training.
---

# Subject reference

A subject's reference is everything that fixes what it looks like: its brief, its base reference, its other sheets, and its reference gallery. A subject is anything that must look the same every time it appears: a character, a creature, a prop, or a vehicle. This skill builds the requests that make the reference, and stops at the user's choice. It hands the requests and the brief back to `project-requests`.

A subject's **base reference** is what every later image of it is sent first:

- **for a character,** its **A-pose set:** the character as a 3D model in a symmetrical A-pose, seen from the front, the back, and both sides, made from its approved primary canonical image;
- **for any other subject,** such as a prop, a creature, or a vehicle, its **reference sheet:** a four-view turnaround.

Some parts apply only to a character, such as outfits and expressions. For another subject, use what fits, such as its variants and the details that make it recognisable, and leave out the rest.

## The model

Every image here comes from an **image-edit model**: one that takes reference images as input and keeps them. Never use a text-to-image model, even with a LoRA. It cannot hold a subject from its references, so the reference would not stay consistent.

## Find the specifics

- **The workflow skill** of the image-edit model the request names, or that the user chooses, says how many references it takes and the sizes it makes; read it, and **its prompt skill**, for how to prompt it. Both come from the setup, as the [prompt roles](../../docs/prompt-roles.md) describe.
- **Running it** is [project-requests](../project-requests/SKILL.md)': this skill builds each request and hands it back, and `project-requests` runs it with `scripts/request.py`, which sends it exactly as built. What a request costs comes from the setup.

## What it needs

Each input by its canonical name, from the pipeline's table:

- the user's request and input images, such as the subject's settled concept design, `<subject>: concept design`, or research photographs;
- for a character, its approved primary canonical image, after canonical cleanup, `<character>: primary canonical image`;
- the concept's style guide, when it has one: its written rules, `<look>: style guide`, and its style sheet, `<look>: style sheet`.

Each step waits for the user's yes before the next. Every paid request waits for a yes to its plan: the number of requests and an estimate.

Characters who read as minors are kept as the [prompt roles](../../docs/prompt-roles.md) say.

## Filling the templates

The templates are written for any subject. Fill their subject words from the brief's kind of subject, so no prompt asks for a face, a pose, or an outfit the subject does not have:

- **For a character:** `{{character}}` is its name; `{{them}}` and `{{their}}` are its pronouns; `{{identity_features}}` is "face, hair, eyes, skin, and markings" as it has them; `{{expression_line}}` gives a gallery row's expression, as a new line, such as `- Expression: surprised.`.
- **For a creature:** `{{identity_features}}` is the same; `{{stance}}` is "standing in a neutral relaxed pose"; `{{form_word}}` is "outfit"; `{{expression_line}}` gives a gallery row's expression.
- **For any other subject,** such as a prop or a vehicle: `{{identity_features}}` is the shape, parts, and markings that make it recognisable; `{{stance}}` is "at rest on a level surface"; `{{form_word}}` is "variant"; `{{expression_line}}` is empty.
- Every canonical value a slot holds, such as the character's name, a part's flat colour, or a prop's name, is written in the step's template as `{{<element>: <fact>}}`, filled from the pipeline's table, never typed in by hand.
- `{{references_list}}` names each attached image in the order sent, as a sentence saying what it is and how it was made, such as "The first attached image is a generated concept design of a brass bell, made for an animated film. The second is a photograph of a real brass bell."
- `{{style_source}}` is "the last attached image, the concept's style sheet" when one is sent; otherwise "the first attached image".
- A detail sheet's `{{subject_image}}` names the attached image of the subject, such as "the third attached image, the front A-pose of Mira", and its `{{relation}}` says how the detail belongs to the subject, such as "the prop {{name}} carries" or "a part of {{name}}".
- In the outfit A-pose template, `{{outfit_image}}` says what the second image is and how it was made, such as "The second attached image is a photograph of a real waiter's jacket.", and `{{outfit}}` is "the outfit from the second image". When no image shows the outfit, `{{outfit_image}}` is empty and `{{outfit}}` describes it in words, from the brief.

What a prompt sent with images says is in the [prompt roles](../../docs/prompt-roles.md).

## 1. Brief

Fill [the brief template](templates/subject-brief.md) from the user's request and input images, and name the input images it is drawn from. When the concept has a style guide, its written rules are the brief's art style, quoted, not reworded. The brief includes:

- a **Trigger word**;
- **Fixed tags**, in the prompting style of the family a LoRA of the subject will be for.

Show the brief to the user; their corrections win. The brief is for the user and for captions. Its descriptions of the look are not copied into a prompt that sends images showing that look.

## 2. Base reference

### A character: the A-pose set

Once the character's primary canonical image is approved, make its A-pose set: the cleanest working map of the character, as a 3D model would show it. Make the views in order, each step from the user's choice in the one before:

1. **The front A-pose, as a textured viewport view:** fill [the A-pose template](templates/a-pose.md) and send the primary canonical image alone. It asks for the character as a 3D model in a viewport's material preview, under neutral light: the mood and lighting are already held by the primary canonical image, so the A-pose starts neutral and is itself the texture view. An A-pose is symmetrical: upright with no lean, the head facing straight ahead, the arms at the same angle on both sides. It needs to be a good working map of the character, not a pose fit for rigging. Reject any view that turns the head, tilts the body, or poses the arms unevenly.
2. **The other views:** fill [the A-pose view template](templates/a-pose-view.md) for the back, the left side, and the right side, each sent with the approved front alone.
3. **Without outer layers:** when an outer layer, such as an apron or a coat, hides what is under it, fill [the layer template](templates/a-pose-layer.md) for the front without it, sent with the approved front alone, then its back and sides from that, as in step 2.
4. **The form passes:** convert every view with `generate-canonical-image`'s grey form and coloured form passes; the texture pass is not needed, since each view already is one. The form passes are the ones agents use most: with no texture, the character's contours and silhouette are clearest. For the coloured form, choose one flat colour per part, such as skin, shirt, apron, trousers, and shoes, and name them in every view's prompt, so the colours agree across views.

Keep each view whole, at one scale, on a plain background, cut away afterwards to a transparent one. The A-pose set is the character's base reference: every later image of the character is sent its textured front A-pose first, and its other views as the image needs them. It feeds the height chart and every model sheet, line-up, board, and shot.

### Any other subject: the reference sheet

A prop, a creature, or a vehicle gets a reference sheet: a 3:2 page of the subject in its default form, as a four-view turnaround, front, three-quarter, side, and back, with no text on it.

- Fill [the base template](templates/reference-base.md), and send it with the input images as references, then the concept's style sheet when there is one, so the subject is drawn in the concept's look.
- If the user supplies a reference sheet, use theirs.

A small prop that belongs to a character takes the small prop sheet below instead.

## 3. Outfits, variants, and props

Each sheet or view has one job, so none is crowded.

- **A character's other outfit:** an extra A-pose set in that outfit.
  - Fill [the outfit A-pose template](templates/a-pose-outfit.md) for the front: the same A-pose and view, with only the outfit changed. Send the approved front A-pose first, then the input image that shows the outfit.
  - Then make its back and sides from that front, its views without outer layers when it has them, and its form passes, as in the A-pose set. In the coloured form, parts the outfits share keep their colours.
- **Another subject's variant sheet,** one per other version of the subject: the same turnaround and layout, with only that changed.
  - Fill [the variant template](templates/reference-outfit.md).
  - Send it with the reference sheet first, and the input image that shows the variant second.
- **Prop or detail sheet,** for a prop, a recurring object, or a part of the subject that needs detail to stay consistent: views of it alone, close-ups, and one small in-use panel for scale.
  - Fill [the prop template](templates/reference-prop.md).
  - Send it with the input images that show it, then the subject's base reference: for a character, its textured front A-pose.
- **Small prop sheet.** A small prop with few details, such as a rag, a mug, or a bell, needs no set of sheets: one sheet, from [the small prop template](templates/small-prop.md), with a map of the prop alone, such as laid out flat and folded, and small panels of its character's forearm and hand using it in each way the story or the character would, showing only the arm and hand, never the whole character; send the character's coloured form front A-pose first, for the arm, hand, colours, and style, then the prop's research photographs. Make the sheet itself as a coloured, non-textured viewport view, each part in its own plain, flat colour, and the prop in one uniform colour even where it has a stripe or a pattern, so it separates clearly from the hand and everything it touches, in the character's own animated style, with the hands plainly the character's own: a textured version adds nothing the character's views do not already show.

Expressions, head angles, poses, and gestures belong in the gallery, not on a sheet.

Make one sheet or view per request. Inspect each for drift from the base reference, wrong colours, broken anatomy or structure, and any text the model drew, and report honestly. A new version is a new paid request, and needs the user's yes.

When a later set of images of the subject asks for one new sheet or outfit, make only that, from the existing base reference.

## 4. Reference gallery

Fill [the dataset template](templates/dataset.md): a matrix of framings, views, outfits or variants, expressions or details, props, and backgrounds. Then write one prompt per row.

Send each row with:

- for a character, its textured front A-pose in the row's outfit first, then the A-pose view nearest the row's view, when that is not the front;
- for any other subject, its reference sheet first, then the row's variant sheet, when it is not the default;
- the prop or detail sheet, when the row has it;
- the concept's style sheet last, when there is one.

Run a few rows first, and compare them with the base reference and the input images before asking to run the rest.

Image-edit models leave grain in flat digital art. Say so when the gallery is done, so a cleanup can be requested before the user chooses. Never offer a redraw by a text-to-image model: one took a character's gallery off model.

## 5. The user's choice

The user chooses which images to approve and which version of each, original or cleaned up; never choose yourself. Write each choice in the dataset plan's Approved images section. Each approved image, view, and sheet is published by `project-pipeline`, by its canonical name, such as `Mira: A-pose front apron texture`, `Mira: A-pose back apron grey form`, or `the bell: reference sheet`, and each gallery image by its row id. A rejected image is never used as an input again.

## Hand back

Hand back to `project-requests`, one request per sheet, view, or gallery row, in the order above, each step after the user's choice in the one before:

- the request: the image-edit endpoint; the prompt as a template naming canon, `{{<element>: <fact>}}`; and the references by canonical artifact, each with its role, in the order to send them, as each step gives;

and, for the user to approve:

- the brief;
- each view of the base reference, for a character in each outfit, by its outfit, its side, and its pass; for any other subject, its reference sheet and each variant sheet;
- each prop or detail sheet, and each small prop sheet;
- the dataset plan, the first few gallery rows before the rest, and the gallery to choose from.
