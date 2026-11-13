# Keyframe plan: {{title}}

From the shot list approved on {{shot_list_date}}. {{shot_count}} shots, {{keyframe_count}} keyframes, at {{aspect_ratio}}.

## Keyframe look

One look for every keyframe of the film. Quote these lines in every keyframe's prompt.

- Line: partially completed digital line art that keeps every character on model: the main forms in clean, confident, single lines in dark grey-black, the weight varying a little, and only here and there a light construction stroke still showing, as if the inking is half done.
- Tone: no fills, no shading, and no grey tones; no colour anywhere. Grey only for a shadow the scene casts that the shot needs, as one flat, light grey shape.
- Light: none drawn, except that shadow. No mood lighting.
- Shapes and proportion: {{shapes}}.
- Place: faint, light-grey construction lines, like a perspective grid, for the layout the shot needs: the floor or ground line, the horizon, the walls and openings in frame. Props only when the action uses them. No set dressing, texture, distant detail, sky effects, or atmosphere.
- Never: arrows, text, captions, shot numbers, borders, or anyone the shot does not name; {{never}}.

Look reference: {{look_keyframe}}, chosen by the user, sent with every keyframe once approved.

## Keyframes

One row per keyframe, in the shot list's order. Every shot has a start keyframe, named by its number. Every shot with a camera move also has an end frame, named by its number and `-end`.

| Keyframe | Shot | Moment | Source | Framing and angle | Camera | Characters, with expression or pose | Props | Place and view | References, in order | Left out to fit | Take approved | Approved on |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `{{shot}}` | {{shot}} | start | {{shot_list_board_or_sketch}} | {{framing}}, {{angle}} | {{camera}} | {{characters}} | {{props}} | {{place}}, {{view}} | {{references}} | {{left_out}} | {{take}} | {{date}} |
| `{{shot}}-end` | {{shot}} | end of the {{camera}} | {{shot_list_board_or_sketch}} | {{end_framing}}, {{end_angle}} | {{camera}} | {{end_characters}} | {{props}} | {{place}}, {{end_view}} | {{references}}, then the approved `{{shot}}` | {{left_out}} | {{take}} | {{date}} |

## Accepted differences

Each difference the review found that the user accepted, by keyframe: {{accepted}}

## Changes

Each revision, with the keyframes it touched and the later work it put out of date: {{changes}}
