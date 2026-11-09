# Dataset plan: {{name}}

The gallery a subject's LoRA is trained on. Every image is drawn from the approved reference sheets, so identity stays fixed while framing, view, outfit or variant, expression or detail, and background vary. For a subject that is not a character or creature, replace the expression rows with close-ups of the details that make it recognisable, and the actions with the ways it is used or moves. Fill the matrix, then write one prompt file per row with the entry template below, filled as the skill's "Filling the templates" says.

## The matrix

Use the first matrix for a character or a creature, and the second for any other subject.


About 36 images, one row each. Five framings:

| Framing | Rows | What is in frame | Mix |
|---|---|---|---|
| **full-body standing** | 6 | head to feet, relaxed stance | front, three-quarter, side, back in the default outfit; front and back in each other outfit |
| **full-body action** | 6 | head to feet, doing something | everyday actions that suit the character: walking, sitting, crouching, using the prop; at least one per other outfit |
| **upper-body** | 10 | waist or thigh up | varied poses, gestures, and expressions; two with the camera above, two below; two without removable headwear in the default outfit |
| **portrait** | 6 | head and shoulders | front, three-quarter, side, back, across outfits |
| **expression** | 8 | face close-up, head and neck | the core expressions (neutral, happy, angry, sad, surprised), the signature expression, and two more that suit the character, spread over front, three-quarter, and side |

For any other subject, about 36 images in four framings:

| Framing | Rows | What is in frame | Mix |
|---|---|---|---|
| **whole, at rest** | 10 | the whole subject | front, three-quarter, side, back, above, and below, in the default form; front and back in each other variant |
| **whole, in use or in motion** | 8 | the whole subject, doing what it does | the ways it is used, moves, or is handled, in settings that suit it; at least one per other variant |
| **medium** | 8 | the larger part of the subject | varied angles, two with the camera above, two below |
| **detail** | 10 | a close-up of one part | the details that make it recognisable, each from more than one angle |

- **Views and angles**: every outfit is seen from more than one side. The back view appears only in full-body and portrait rows; an expression has no back view.
- **Poses**: no more than a third of the rows are plain standing. A dataset of only standing poses trains a stiff LoRA.
- **Headwear and accessories**: anything removable appears off at least twice in the default outfit, so the LoRA does not tie its absence to another outfit.
- **Props**: in two to four rows, held or used naturally. Most rows have none.
- **Backgrounds**: about a third plain white or light grey; the rest simple, uncluttered settings that suit the character, never the same twice in a row. A dataset that is all white teaches the LoRA to draw only white backgrounds.
- **Not in the dataset**: the reference sheets themselves; several views on one image confuse training.
- **Content**: clothing and poses stay ordinary and everyday. A character who reads as a minor is never drawn in sexual or suggestive ways, in any row or caption.

| id | framing | view | outfit | expression | prop | background |
|---|---|---|---|---|---|---|
| `fb-front-{{outfit}}` | full-body | front | | | | |

## Entry prompt

One file per row, named for its id (for example `fb-front-hoodie.md`), generated with the base sheet as the first reference image, the outfit sheet when the row's outfit is not the default, and the prop sheet when the row has that prop.

```markdown
---
aspect_ratio: "{{2:3 for full-body, 3:2 for wide action, 3:4 for upper-body and portrait, 1:1 for expression}}"
quality: high
---
## Prompt

A single illustration of {{name}}, exactly as drawn on the attached reference sheets: same {{identity_features}}, proportions, colours, and art style ({{art_style}}).

- Framing: {{framing description}}.
- View: {{view}}, {{pose}}.
- {{Form_word}}: {{outfit or variant description from the brief}}.{{expression_line}}
- Prop: {{prop, or "none"}}.
- Background: {{background}}.

One subject only. No text, labels, borders, or panels. The subject fills the frame as the framing says.
```

## Kept images

The user's choice for each row, once the gallery is cleaned up: `original`, `cleanup`, or `dropped`. Only kept rows go into the subject's dataset.

| id | keep |
|---|---|
| `fb-front-{{outfit}}` | |
