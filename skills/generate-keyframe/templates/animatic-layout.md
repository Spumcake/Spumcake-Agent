---
aspect_ratio: "16:9"
quality: high
---
## Prompt

The attached image is a grey pre-vis render of {{place}} from one camera. Redraw it as an animatic layout drawing, the reference every animatic frame from this camera follows: partially completed digital line art in light grey, clean single lines with only here and there a construction stroke, with no fills, no shading, and no tones, on a plain white page. Keep the camera, the perspective, and each kept form exactly where the render puts them. Keep only what the characters touch or look at: {{kept}}, each as a simple outline. Leave out everything else, the walls, the floor, and the ceiling too: {{left_out}}. The kept forms float on the white page, with no room around them, no grid, no characters, and no text.

## Filling it

One layout drawing per camera, made from that camera's pre-vis render before any keyframe from it, and sent first to every keyframe from it, so every animatic frame agrees on how the place is drawn (the user, 2026-11-12).

- `{{kept}}`: only what the shot's characters touch or look at: "the counter and the front door". A door a character speaks to is kept: a layout without it left Otis looking at nothing, and his looks pointed at different doors from frame to frame (the user, 2026-11-13).
- `{{left_out}}`: everything else in the render, named, so the model drops it: "the window, the booth, the stools, the pendant lamps, the napkin dispensers, the sugar jars, the register, and everything on the table".

**A form that changes during the shot,** such as a door that opens, gets one layout drawing per state, each made from the first by an image edit that changes only that form: "Image 1 is the layout of the shot. Change only the front door: it stands half open, swung outward, away from the room, and the doorway is empty. Keep everything else exactly as it is." Each frame is sent the layout of its state (the user, 2026-11-13).

How the user narrowed it, on 2026-11-12: a first layout kept the major forms on a dense wall grid; a sparse grid buried them less; keeping only what the story uses, the door and the counter, still read as a padded room, a box of walls; what holds is only what the characters touch, with no walls, floor, or grid at all; and, on 2026-11-13, what they look at.
