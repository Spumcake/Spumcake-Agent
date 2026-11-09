# Board plan: {{title}}

From the shot list approved on {{shot_list_date}}. {{shot_count}} shots, {{frame_count}} frames, at {{aspect_ratio}}.

## Board style

One look for every frame of the board. Quote these lines in every frame's prompt.

- Line: loose, sketchy pencil line, a little uneven, with construction lines left in; {{line}}.
- Tones: three flat grey tones on white, light, middle, and dark, laid in quickly to separate the figures from the place and to show where the light comes from; {{tones}}.
- Shapes and proportion: {{shapes}}, simplified to read at a glance.
- Detail: only what the shot needs to read: faces as simple shapes with clear eye direction; hands as simple shapes; the place blocked in, its main shapes only.
- Arrows: camera moves as broad, outlined arrows, or an inner rectangle with corner arrows for a push in or pull out; characters' motion as thin, curved arrows along their path; all in a dark grey, drawn on top of the picture as storyboard marks.
- Never: colour, finished rendering, fine texture, text, captions, panel numbers, or borders; {{never}}.

Style reference: {{board_style_frame}}, chosen by the user, sent with every frame once approved.

## Frames

One row per frame, in the shot list's order. Every shot has a start frame, named by its number. An end frame, named by the number and `-end`, is for a camera move that changes what the frame shows.

| Frame | Shot | Moment | Source | Framing and angle | Camera | Characters and props | Place | References, in order | Take kept |
|---|---|---|---|---|---|---|---|---|---|
| `{{shot}}` | {{shot}} | start | {{shot_list_or_sketch}} | {{framing}}, {{angle}} | {{camera}} | {{characters_and_props}} | {{place}} | {{references}} | {{take}} |
| `{{shot}}-end` | {{shot}} | end of the {{camera}} | shot list | {{end_framing}} | {{camera}} | {{characters_and_props}} | {{place}} | the approved `{{shot}}`, then {{references}} | {{take}} |

## Changes

Each revision, with the shots it touched: {{changes}}
