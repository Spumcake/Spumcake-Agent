# Keyframe plan: {{title}}

From the shot list approved on {{shot_list_date}}. {{shot_count}} shots, {{keyframe_count}} keyframes, at {{aspect_ratio}}.

## Keyframe look

One look for every keyframe of the film. Quote these lines in every keyframe's prompt.

- Line: clean, closed, unbroken outlines, with no sketch lines, hatching, or loose strokes; {{line}}.
- Colour: each region of a subject filled with one flat colour, from its colour model or its base sheet; {{palette}}. No shading, gradients, highlights, rim light, or cast shadows.
- Light: even, neutral light, the same in every keyframe. No mood lighting.
- Shapes and proportion: {{shapes}}.
- Place: only the layout the shot needs, in the same clean line and flat, muted colours: the floor or ground line, the horizon, the walls and openings in frame, and the furniture and props the action uses or that say where the shot is. No texture, set dressing, distant detail, sky effects, or atmosphere.
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
