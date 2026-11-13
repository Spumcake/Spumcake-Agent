---
aspect_ratio: "{{aspect_ratio}}"
quality: high
---
## Prompt

Image 1 is the layout of the shot. {{character_images}} Draw {{who}} into image 1, as {{their_images}} draw {{them}}. {{placement}} {{size}} {{expression}} {{direction}} {{changes}} Add nothing else to image 1.

## Filling it

Every sentence is either what an image is or something no image shows; nothing an image already shows is described, as `docs/prompt-roles.md` says. The images are the shot's animatic layout drawing first, then each character's animatic expression sheet, acting sheet, turnaround, and level-of-detail sheet, in that order. Example, Otis saying the line (2026-11-12):

- `{{character_images}}`: "Images 2 to 5 are Otis's expression sheet, acting sheet, turnaround, and level-of-detail sheet."
- `{{who}}`, `{{their_images}}`, `{{them}}`: "Otis", "images 2 to 5", "him".
- `{{placement}}`: where the character is against each thing they touch: "He stands behind the counter, halfway along it, leaning on both hands on its top; the counter hides him from the waist down."
- `{{size}}`: the level-of-detail sheet's figure: "His size and detail are those of the third figure in image 5."
- `{{expression}}`: the expression sheet's panel, by its label: "His expression is the panel \"the line\" in image 2."
- `{{direction}}`: left empty. Where the character looks is the expression panel's, drawn for this shot in `create-model-sheet`; when no panel looks the way the shot needs, make that panel first. Text that contradicts a panel loses to the drawing (2026-11-12).
- `{{changes}}`: only what differs from the sheets: "The towel is under his right hand on the counter, not at his apron."

As the user set on 2026-11-12, a keyframe prompt is this short. An earlier template restated the keyframe look, the characters, and the place on top of the images that show them, and named images that were not sent; at about 900 words it contradicted its own references, and the model drew walls and a horizon the layout had left out.
