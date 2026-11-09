# Background plan: {{title}}

From the shot list approved on {{shot_list_date}} and its approved keyframes. {{setup_count}} setups, {{plate_count}} plates, at {{aspect_ratio}}.

Finish reference: {{finish_plate}}, chosen by the user, sent with every plate of another setup once approved.

## Plates

One row per setup, in the shot list's order, named by its first shot. A setup seen in another mood has a row of its own, named by the setup and the mood, made from the setup's plate. Every shot of a setup uses its plate.

| Plate | Shots that use it | Place | Camera position | Framing and angle | Horizon and floor line | Camera move | Plate shape and size | Where the framings sit | Mood and lighting key | Beat and colour script line | What passes in front | References, in order | Left out to fit | Take approved | Approved on |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `bg-{{shot}}` | {{shots}} | {{place}} | {{position}} | {{framing}}, {{angle}} | {{horizon}} | {{camera}} | {{plate_shape}} | {{framings}} | {{mood}}, `{{lighting_key}}` | {{beat}}: {{colour_script_line}} | {{in_front}} | {{references}} | {{left_out}} | {{take}} | {{date}} |
| `bg-{{shot}}-{{mood}}` | {{shots}} | {{place}} | {{position}} | as `bg-{{shot}}` | as `bg-{{shot}}` | as `bg-{{shot}}` | as `bg-{{shot}}` | as `bg-{{shot}}` | {{mood}}, `{{lighting_key}}` | {{beat}}: {{colour_script_line}} | as `bg-{{shot}}` | the approved `bg-{{shot}}`, then {{references}} | {{left_out}} | {{take}} | {{date}} |

## Accepted differences

Each difference the review found that the user accepted, by plate: {{accepted}}

## Changes

Each revision, with the plates it touched and the shots that use them: {{changes}}
