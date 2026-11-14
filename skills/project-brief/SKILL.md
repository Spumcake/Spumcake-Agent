---
name: project-brief
description: Keep a project's brief - one HTML page per pipeline, brief/<pipeline>-<project>.html, holding all of its intent: the brief itself, the mood, the visual and audio identity, the voices, and the sound design, each section drafted by its write- skill - update it in place as intent grows, start the next pipeline's brief when a change contradicts published canon, and compare the brief with the pipeline's canon to list what still needs a request. Use when the user gives or changes a brief, when a write- skill drafts an identity section, and before planning requests. Not for running requests (project-requests) or publishing canon (project-pipeline).
---

# The brief

The brief says what the film should be. It is one page per pipeline, kept current, so there is one place to read intent and nothing to reconcile between several briefs. Only this skill writes `brief/`.

## The page

`brief/<pipeline>-<project>.html`, such as `brief/001-last-order.html`, holds these sections, in this order:

1. **The brief:** the premise, the characters, the setting, the time of day, the length, and every spoken line, in the user's words.
2. **The mood:** genre and tone, and how light, colour, and camera feel (`write-mood-brief`).
3. **The visual identity:** what the picture must do, moment by moment, its colour's intent, and what it must never be (`write-visual-identity-brief`).
4. **The audio identity:** what the sound is for (`write-audio-identity-brief`).
5. **The voices:** one part per speaking character (`write-voice-brief`).
6. **The sound design:** every sound, cue by cue (`write-sound-design-brief`).
7. **The timing:** every moment, cue, line, and frame on one timeline (`write-timing-reference`).

Each section's skill drafts it as a request, so its draft is in the library with its report; this skill places the approved draft in the page and links its request. The page holds intent only: never a file path, an approval, or a status, which belong to the pipeline. Write it as plain, readable HTML with the project's own style, and keep it to what each section's skill says belongs there.

## Updating it

- A change that adds to the brief, or refines something not yet published, is made in place. Git keeps the page's history.
- A change that contradicts published canon, such as moving a door the canonical floor plan places, starts the next pipeline: copy the page to `brief/<next>-<project>.html` with the change, and have `project-pipeline` start the next pipeline. The earlier page stays as it was.

## The audit

Compare the brief with the pipeline's canon, section by section: each thing the brief asks for, and whether a published artifact or fact shows it. List:

- what the brief asks for that no published artifact shows yet;
- what canon shows differently from the brief, with the artifact or fact and the brief's words;
- what canon holds that the brief never asked for.

Each item is a proposed request, taken to the user; nothing changes without their yes.
