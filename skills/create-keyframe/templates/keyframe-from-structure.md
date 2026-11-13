---
aspect_ratio: "{{aspect_ratio}}"
quality: high
---
## Prompt

The structure image is {{structure_kind}}. Redraw it as {{moment}}, keeping its composition exactly: every figure in the same place, at the same size, in the same pose, facing the same way, with the same framing. Leave out its arrows, grey tones, and storyboard marks. {{character_images}} Draw each figure as those images draw them: {{who_is_who}} {{expression}} Add nothing else.

## Filling it

- `{{structure_kind}}`: "the shot's rough storyboard frame" or "the user's own sketch of the shot".
- `{{moment}}`: "the first moment of the shot", or, for an end frame, "the last moment of the shot, after the camera's move".
- `{{character_images}}`: the references, numbered in the order sent, as [the keyframe template](keyframe.md) names them.
- `{{who_is_who}}`: which figure in the structure image is which character, by its place in the frame: "the figure behind the counter is Otis."
- `{{expression}}`: each character's expression panel, by its label.

Only what each image is and what no image shows: the composition is the structure image's, and the look, the characters, and the place are the references'.
