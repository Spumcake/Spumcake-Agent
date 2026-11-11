# Continuity review: {{result_name}}

{{result_kind}}, from "{{title}}". Reviewed against {{reference_count}} references, on {{sample_count}} samples. {{finding_count}} findings: {{blocking_count}} block approval, {{note_count}} are notes.

## What was looked at

The samples of the result, in the order sent, each by its frame, time, or word.

- {{sample, such as "frame 0, 0:00.00, the first frame" or "0:02.40, the word 'lantern'"}}

## Findings

One per difference, in the order they appear in the result. A difference that lasts is reported once, at its first sample, with the span it lasts.

### {{n}}. {{what, in a few words}}

- **What:** {{what differs, in a sentence}}
- **Where:** {{the frame, time, or word, and the region, such as "frames 24 to 36, 0:01.00 to 0:01.50, Mira's left hand"}}
- **Against:** {{the reference, by its file or name and the part of it, such as "Mira's colour list, the jacket row", "the shot list, shot 3-2, framing", or the canonical prompt's line, quoted}}
- **Should be:** {{what the reference fixes, in its own words or values}}
- **Serious:** {{blocks approval, or note}}
- **Kind:** {{for a generated image: ruled out by the prompt, wrong against the prompt, not in the pre-vis, not in the pre-vis but needed, malformed, texture on a form pass, or across the views; otherwise leave out}}
- **Evidence:** {{what the result shows, and what the reference shows or says, side by side; and what makes you unsure, when you are}}
- **The user's decision:** —

## Checked and clear

Every check asked for that found no difference, each with the reference it was checked against.

- {{check}}, against {{reference}}: no difference found.

## Could not check

Every check asked for that the samples or the references could not show, and why.

- {{check}}: {{why}}

## Decided

{{left empty by the review; the user's decision on every finding, and the date}}
