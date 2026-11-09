---
name: create-model-sheet
description: Make the model sheets that come after a subject's turnaround - an expression sheet, a pose sheet, a mouth chart of the shapes lip-sync is drawn from, each labelled by its sound, and a colour model with every colour called out on the subject by name and value - one sheet per request, from the subject's reference sheets with an image-edit model, the base sheet sent first and the concept's style sheet last. Use when the user asks for an expression sheet, a pose or action sheet, a mouth chart or mouth shapes, a colour model or colour callouts, for a character or other subject that already has its reference sheets. Not for the turnaround itself, several subjects side by side, or a gallery of images of the subject.
---

# Model sheet

A model sheet keeps a subject on model in the ways its turnaround does not: how its face moves, how its body moves, how its mouth makes each sound, and exactly what colour each part is. Each sheet is one page with one job, drawn from the subject's reference sheets so it never drifts from them, and each becomes a reference of its own: the expression and pose sheets for boards and shots, the mouth chart for lip-sync, and the colour model for colouring.

A good sheet shows the same subject in every panel, exactly as on its base sheet, with only the sheet's one thing changing, and labels that read correctly. A failed sheet changes the face or the proportions from panel to panel, shows mouth shapes that cannot be told apart, or calls out colours that are not on the subject.

There is one template per sheet:

- an **expression sheet:** the subject's faces;
- a **pose sheet:** its body in the actions and attitudes the film needs;
- a **mouth chart:** the mouth shapes lip-sync is drawn from, each labelled by the sounds it makes;
- a **colour model:** the subject in its base views, with each colour called out by name and value.

## The model

Every sheet comes from an **image-edit model** that takes the reference sheets as input images and keeps them. Never use a text-to-image model: it cannot hold a subject from sheets.

## Find the specifics

- **The workflow skill** of the model the request names, or that the user chooses, says how many references it takes, the sizes it makes, and how well it draws short labels. **Its prompt skill** gives its syntax and limits.
- **The execution skill** that implements `create-model-sheet` in this setup renders it; when none does, the setup's renderer. It says what a request costs and where its output lands.

All come from the setup, as the [prompt roles](../../docs/prompt-roles.md) describe. If one is missing, say which and stop. When the request names no model and more than one fits, ask.

## What it needs

From the caller:

- the subject's reference sheets: its base sheet, and the outfit or variant sheet when the model sheet is for another outfit or variant; with none, the subject needs its reference first;
- the subject's brief, when there is one: its personality, signature expression, palette, and fixed traits;
- the concept's style guide, when it has one: its written rules and its style sheet;
- the approved script or shot list, when there is one, for the expressions and poses the film needs;
- for a mouth chart, the mouth shapes the user's lip-sync work reads, when it has its own set;
- for a colour model, the colour values the user has, when they have them;
- a folder for the plans, the prompts, and the sheets, each sheet saved beside its prompt.

Each step waits for the user's yes before the next. Every paid request waits for a yes to its plan: the model, the number of requests, and the cost. A first run on a new model is one sheet, as a test, before the rest.

Every image of a character who reads as a minor stays ordinary and everyday. Nothing is sexual or suggestive, in any step or prompt.

Show a recognisable real person only when the user confirms that the person agreed to this use, or a guardian did for a child; never to deceive anyone.

## Sheet prompts

A sheet prompt says which sheet it is, what each reference holds, then the panels, then what changes in them and what never does. Write it in this order, for any model:

1. **What the image is:** the sheet's name and use, such as "an EXPRESSION SHEET for Mira: the single source of truth for her faces".
2. **The references,** in the order sent: "The first attached image is her base reference sheet: keep her face, proportions, colours, and art style exactly." The outfit sheet next, when it is used, and the style sheet last.
3. **The layout:** a grid, its number of panels, in reading order, and each panel's label in quotes. Keep labels to a word or two; models misspell long text.
4. **What changes,** panel by panel, and only that: the face, the pose, or the mouth. A colour model changes nothing; it adds callouts.
5. **What stays the same** in every panel: the scale, the view, the identity, the colours, and the line.
6. **What to leave out:** backgrounds, props not on the sheet, extra figures, and notes, as a plain sentence.

Keep each panel's line short. More than twelve panels on a page crowds it: split the list over two sheets. Leave out what the model ignores, as its prompt skill says.

Put each part into its field in the model's syntax, as its prompt skill says: the words in `prompt`, what to avoid in `negative` when the model takes it, and the sheets, in order, in `references`, by the [prompt roles](../../docs/prompt-roles.md). Write each prompt with the setup's prompt writer.

## Filling the templates

The templates are written for any subject. Fill their subject words from the brief's kind of subject:

- **For a character or a creature:** `{{identity_features}}` is "face, hair, eyes, skin, and markings" as it has them; `{{form_word}}` is "outfit".
- **For any other subject,** such as a prop or a vehicle: `{{identity_features}}` is its shape, parts, and markings; `{{form_word}}` is "variant". It has no expression sheet or mouth chart unless it has a face, and its pose sheet shows its states and positions, such as doors open or wheels turned.
- `{{style_sheet_line}}` is " The last attached image is the concept's style sheet: match its line, colour, and light." when one is sent; otherwise it is empty.
- `{{outfit_line}}` is " The second attached image is its {{form_word}} sheet: draw it in that {{form_word}}." when one is sent; otherwise it is empty. `{{outfit_sheet}}`, `{{form_note}}`, and `{{form_header}}` name that {{form_word}} in the plan, the colour list, and the header, such as ", the raincoat sheet", ": raincoat", and ", RAINCOAT", or are empty.
- `{{expressions}}`, `{{poses}}`, and `{{mouth_shapes}}` are one line per panel, in order, from the sheet plan: its label in quotes, then a few words, such as `"MBP": lips pressed together`.
- `{{personality}}` is the brief's personality; for a subject without one, what its poses must show, such as "its weight and age".
- `{{callouts}}` is one line per row of the colour list, such as `HAIR: "RUST #B5512C"`.

## 1. Choose the sheets

Fill [the sheet plan template](templates/sheet-plan.md): which sheets the subject needs, and what each holds.

- **Expressions:** the core set, neutral, happy, sad, angry, surprised, and afraid; the brief's signature expression; and the ones the script calls for. Each is named in a word or two.
- **Poses:** six to eight, from the actions the script and shot list give the subject, and the attitudes its personality calls for. Each is named in a few words, such as "running, looking back".
- **Mouth shapes:** the set the user's lip-sync work reads, exactly, when it has one. Otherwise these nine, each labelled as shown:
  - `REST`: closed and relaxed, for silence;
  - `MBP`: lips pressed together, for m, b, and p;
  - `AI`: wide open, jaw dropped, for a and i;
  - `E`: open and stretched wide, teeth showing, for e;
  - `O`: round and open, for o;
  - `U`: small and pushed forward, for u, w, and oo;
  - `FV`: upper teeth on the lower lip, for f and v;
  - `L`: open, tongue tip behind the upper teeth, for l and th;
  - `ETC`: teeth together, lips a little apart, for c, d, g, k, n, r, s, t, y, and z.
- **Colours:** fill [the colour list template](templates/colour-list.md), one row per region of the subject, from the brief's palette and the style guide's palette. Values the user gives are used exactly; any other value is proposed from the base sheet and marked *proposed*.

Show the plan to the user; their corrections win. Once approved, labels and values stay fixed: the work that reads them later finds them by these names.

## 2. Make each sheet

Fill the sheet's template:

- [the expression template](templates/expression-sheet.md);
- [the pose template](templates/pose-sheet.md);
- [the mouth chart template](templates/mouth-chart.md), one sheet per view, front first, and a three-quarter sheet when shots need it;
- [the colour model template](templates/colour-model.md).

Send the base sheet first, then the outfit or variant sheet when the sheet is for one, then the style sheet last.

Make one sheet per request. Plan it, render it on the user's yes, and report its path. Inspect it for drift from the base sheet, wrong colours, broken anatomy or structure, panels that look alike, and labels that came out wrong, and report honestly. On a colour model, check every label against the colour list: the list is the record of the values, and an image that misprints one is reported, not trusted. A new version is a new paid request, and needs the user's yes.

## 3. Hand back

Record in the sheet plan's Kept sheets section which version of each sheet the user chose to keep, and the date.

Hand back to the caller:

- each kept sheet, named for what it is, such as `mira-expressions` or `mira-mouth-chart-front`;
- the sheet plan: the expressions, the poses, and the mouth shapes and their sounds; and the colour list with its values;
- which sheets the user chose to keep as references for the subject.

Later images of the subject are sent its base sheet first and the kept sheet that fits second: the expression or pose sheet for a board or a shot, the mouth chart for lip-sync, and the colour model, with its list quoted, for colouring.
