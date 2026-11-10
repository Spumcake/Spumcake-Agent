# Dataset plan: {{name}}

The gallery a subject's LoRA is trained on. Every image is drawn from the approved base reference, a character's A-pose views or another subject's reference sheets, so identity stays fixed while framing, view, outfit or variant, expression or detail, and background vary. For a subject that is not a character or creature, replace the expression rows with close-ups of the details that make it recognisable, and the actions with the ways it is used or moves. Fill the matrix, then write one prompt file per row with the entry template below, filled as the skill's "Filling the templates" says.

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
- **Not in the dataset**: the reference sheets and A-pose views themselves: they are references, not illustrations, and several views on one image confuse training.
- **Content**: clothing and poses stay ordinary and everyday. A character who reads as a minor is never drawn in sexual or suggestive ways, in any row or caption.

| id | framing | view | outfit | expression | prop | background |
|---|---|---|---|---|---|---|
| `fb-front-{{outfit}}` | full-body | front | | | | |

## Entry prompt

One file per row, named for its id (for example `fb-front-hoodie.md`). A character's row is sent its textured front A-pose in the row's outfit first, then the A-pose view nearest the row's view when that is not the front; another subject's row is sent its reference sheet first, then the variant sheet when the row's variant is not the default. Then the prop sheet when the row has that prop, and the style sheet last.

The prompt says what each attached image is and how it was made, then only what no image gives: the framing, the view and pose, the expression, which prop, and the background. It never describes the subject's look, outfit, or prop in words.

- `{{references_list}}` names each attached image in the order sent, such as "The first attached image is a generated character model of Mira in a symmetrical A-pose, seen straight from the front, a textured viewport capture made for an animated film. The second is the same model seen from the back. The third is the concept's style sheet."
- `{{subject_source}}` is "the first attached image" for a character, or "the attached reference sheets" for another subject.
- `{{style_line}}`: "drawn in the style of the concept's style sheet, the last attached image" when one is sent; otherwise "drawn in this style: {{art_style}}", the brief's art style.
- `{{form_line}}`: for another subject's variant row, a new line, `- {{Form_word}}: as the second attached image shows.`; otherwise empty.
- `{{prop_line}}`: the prop from its sheet, such as "the mug from the third attached image, held in both hands", or "none".

```markdown
---
aspect_ratio: "{{2:3 for full-body, 3:2 for wide action, 3:4 for upper-body and portrait, 1:1 for expression}}"
quality: high
---
## Prompt

{{references_list}} I need a single illustration of {{name}}, with the same {{identity_features}}, proportions, and colours as {{subject_source}}, {{style_line}}.

- Framing: {{framing description}}.
- View: {{view}}, {{pose}}.{{form_line}}{{expression_line}}
- Prop: {{prop_line}}.
- Background: {{background}}.

One subject only. No text, labels, borders, or panels. The subject fills the frame as the framing says.
```

## Kept images

The user's choice for each row, once the gallery is cleaned up: `original`, `cleanup`, or `dropped`. Only kept rows go into the subject's dataset.

| id | keep |
|---|---|
| `fb-front-{{outfit}}` | |
