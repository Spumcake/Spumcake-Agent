# Keyframe plan: {{title}}

From the shot list approved on {{shot_list_date}}. {{shot_count}} shots, {{keyframe_count}} keyframes, at {{aspect_ratio}}.

## Keyframe look

One look for every keyframe of the film, carried by the layout drawings and the animatic sheets, never quoted in a prompt: partially completed digital line art, no fills, no shading, and no colour; grey only for a shadow the scene casts that the shot needs; the place as only what the characters touch, outlined in light grey, with no walls, floor, ceiling, or grid; never arrows, text, captions, shot numbers, borders, or anyone the shot does not name.

## Layout drawings

One per camera, made before its keyframes: {{camera}}: {{layout_drawing}}, keeping {{kept}}.

## Keyframes

One row per keyframe, in the shot list's order. Every shot has a start keyframe, named by its number. Every shot with a camera move also has an end frame, named by its number and `-end`.

| Keyframe | Shot | Moment | Source | Camera and layout drawing | Characters, with placement, level-of-detail figure, and expression panel | References, in order | Left out to fit | Take approved | Approved on |
|---|---|---|---|---|---|---|---|---|---|
| `{{shot}}` | {{shot}} | start | {{shot_list_board_or_sketch}} | {{camera}}, {{layout_drawing}} | {{characters}} | {{references}} | {{left_out}} | {{take}} | {{date}} |
| `{{shot}}-end` | {{shot}} | end of the {{camera_move}} | {{shot_list_board_or_sketch}} | {{end_camera}}, {{end_layout_drawing}} | {{end_characters}} | {{references}}, then the approved `{{shot}}` | {{left_out}} | {{take}} | {{date}} |

## Accepted differences

Each difference the review found that the user accepted, by keyframe: {{accepted}}

## Changes

Each revision, with the keyframes it touched and the later work it put out of date: {{changes}}
