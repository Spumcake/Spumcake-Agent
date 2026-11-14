---
name: write-timing-reference
description: Work out a film's timing before anything is made - every moment on one timeline in seconds, every sound cue and line with its time, and every animatic frame with its in and out, its character, expression panel, and action - from the beat sheet or script and the audio and voice briefs, as the timing reference the sound, the voices, the frames, and the assembled animatic are all made to. Use once the beat sheet or script and the briefs exist, before any voice, sound, or keyframe is made. Not the sound design brief's descriptions (write-sound-design-brief), the frames (generate-keyframe), or the assembly (build-animatic).
---

# Timing reference

The film's audio and its animatic frames are made to one timing worked out first: when each thing happens, when each sound starts, and when each frame appears. The sound is generated to it, the voices are placed on it, the frames are chosen from it, and the animatic is assembled on it, so they agree without being fitted afterwards. In animation this plan is a bar sheet; here it is called the timing reference, as the user named it.

A good timing reference can be played in the head and laid on a timeline as it stands: every moment has an in and an out, every sound and line a time, and every frame the moment it shows, with nothing overlapping and nothing missing. A failed one times the sound and the frames separately, leaves a line without room to be said, or holds a frame that shows no change.

This skill makes nothing but the document. It drafts the brief page's timing section as a finished draft and hands it back; `project-brief` places it in the page once the user approves.

## What it needs

- the beat sheet (`<film>: beat sheet`) or the script (`<film>: script`), and the shot list (`<film>: shot list`) when it is published, for what happens, in what order, and the film's length;
- the audio identity: the brief page's section, for what each moment's sound is for;
- the voices: the brief page's section, for each line's delivery and its estimated length;
- the character's animatic sheets (`<character>: animatic sheet`), when they are published, and their panels' labels, as the pipeline's table gives what each shows, so each frame names a panel that is there;
- each place's floor plan (`<place>: floor plan`, from `build-previs`) and its facts, from the pipeline's table, for every mark, facing, and look.

## 1. Decide

From the sources, and from what the film needs where they are silent, marking each decision *proposed*:

- **The moments:** the beats, split where something visibly changes, each with its in and out in seconds, running on from zero without a gap, adding up to the film's length.
- **The sound cues:** each sound effect and music event, at its time, as the sound design brief names it.
- **The lines and voice sounds:** each, by speaker, word for word, at its time; its length from the voice brief's estimate until a take is recorded, then the take's measured length. A line is never squeezed; the moment around it grows.
- **The frames:** one per moment that changes what is seen, each with its in and out, the shot or camera, each character in it with their expression panel and acting drawing by label, and what they do. A frame changes only when the picture must; a held frame is the animatic's rhythm.
- **The blocking:** for each frame, each character's mark on the floor plan, the way they face, and what they look at, against the plan's named objects, in room terms; and the state of anything that changes, such as a door that opens. The marks are handed back as facts, beside the floor plan's own. Frame terms, left or right, are worked out from the plan for the frame's camera, and given to the frame's expression panel, so the panel is drawn for that camera.

## 2. Write it

Fill [the timing reference template](templates/timing-reference.md). Times are in seconds from the start, to one decimal place, such as "4.8 to 6.3". The sound design takes its cue times from it, the voices are placed by it, the keyframes are made from its frame list, and the animatic is assembled on it. `review-consistency` checks the draft against the rest of the brief page, as its own request, before the user approves it.

## Hand back

- the draft of the brief page's timing section, for the user's approval and for `project-brief` to place;
- the facts it settles, by `<element>: <fact>`, for `project-pipeline` to publish: each frame's in and out, such as `<frame>: in`, and each character's blocking in each frame, such as `<character>: mark in <frame>`, `<character>: faces in <frame>`, `<character>: looks at in <frame>`, and `<character>: side of frame in <frame>`, so the steps that make the frames name them as `{{<element>: <fact>}}`;
- its frame list, for `generate-keyframe`;
- its cue and line times, for `write-sound-design-brief`, `generate-sound`, `generate-voice`, and `build-animatic`.
