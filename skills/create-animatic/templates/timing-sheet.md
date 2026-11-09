# Animatic timing sheet: {{title}}

From the shot list approved on {{shot_list_date}} and its approved board. {{shot_count}} shots, {{total_seconds}} seconds in all ({{total_timecode}}), against a length of {{length}}, at {{frame_rate}} frames a second. Timecode is hours:minutes:seconds:frames; each out is the next shot's in.

## Sheet

| Shot | Board | In | Out | Length | Camera move | Transition | Lines |
|---|---|---|---|---|---|---|---|
| {{shot}} | `{{board_file}}` | {{in}} | {{out}} | {{seconds}}s | {{camera_move}} | {{transition}} | {{cue}} {{speaker}}, {{on_or_off_screen}}: "{{line}}" |

## Cue list

Temp-audio cues, one per spoken line, in order. A cue starts half a second into its shot, or half a second after the cue before it in the same shot, and takes about two and a half words a second.

| Cue | Shot | Speaker | Line | Words | Starts | Takes |
|---|---|---|---|---|---|---|
| {{cue}} | {{shot}} | {{speaker}}, {{on_or_off_screen}} | "{{line}}" | {{words}} | {{cue_in}} | {{cue_seconds}}s |

## Counted

- Shots without a board: {{missing_boards}}
- Shots whose lines need more than their length: {{tight_shots}}
- Lengths that differ from the approved shot list: {{changed_lengths}}

## Changes

Each revision, with the shots it touched: {{changes}}

## Approved

{{approved}}
