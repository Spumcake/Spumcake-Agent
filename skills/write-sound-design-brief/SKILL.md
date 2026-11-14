---
name: write-sound-design-brief
description: Draft a film's sound design brief - every sound, cue by cue, as film sound teams list them in a spotting list: what it is, where it comes from, when it starts and how long it lasts, how loud and how close it is, and what it does, over the room tone that lies under them, with where silence falls - from the audio identity brief, the beat sheet or script, and the voice briefs, as a finished draft the user edits and approves. Use once the audio identity brief and the voice briefs are written, before any sound is made or the audio cut is assembled. Not the audio identity brief (write-audio-identity-brief), a voice brief (write-voice-brief), or a sound.
---

# Sound design brief

The sound design brief is the film's sound, cue by cue, laid on the film's length: what film sound teams call a spotting list. Every sound effect is made from it, and the audio cut, the voices and the sounds on one timeline before any picture, is assembled from it. Its times are where the animatic's frames will later be placed.

A good brief can be laid on a timeline as it stands: each cue has a time, a length, a place, and a level, and says what it does for the scene. A failed one names sounds without when, where, or how loud, or adds sounds the audio identity brief does not need.

This skill makes no sound. It drafts the brief page's sound design section as a finished draft and hands it back; `project-brief` places it in the page once the user approves. It does not interview the user.

## What it needs

- the audio identity: the brief page's section, for what each sound is for;
- the beat sheet (`<film>: beat sheet`) or the script (`<film>: script`), for what happens and when, and the film's length;
- the place's floor plan (`<place>: floor plan`) and its published views (`<place>: view <wall>`), and what each view shows, from the pipeline's table with `pipeline.py`, for what can make a sound;
- the voices: the brief page's section, for where each line and non-verbal sound falls, so the cues leave room for them;
- the timing: the brief page's section (`write-timing-reference`), once it exists, whose cue times this section takes rather than setting its own.

## 1. Decide

From the sources, and from what the scene needs where they are silent, marking each decision *proposed*:

- **The length,** from the beat sheet or the script.
- **The sources:** every sound comes from something the canonical place holds, as its floor plan and published views show it, or from what the beat sheet or script names, on screen or off. A sound with no source there is not added: report it as missing from the canon, for `review-consistency`. A refrigerator heard in a diner that has none once carried from a first draft into the brief, with a cue of its own.
- **The room tone:** the layers heard when nothing happens, each with its level and closeness, running the whole length unless a cue changes it.
- **Each cue,** in order: its time and length, in seconds; what it is and where it comes from in the room; how loud and how close; and what it does. The voices' lines and sounds are cues too, by name, so the timeline is whole; how they sound stays in the voices section.
- **Silence:** where everything but the room tone stops, and for how long.
- **The mix:** what is loudest, what sits under what, and what must never be covered.

## 2. Write the section

Fill [the sound design brief template](templates/sound-design-brief.md). Times are in seconds from the start, such as "4.0 to 5.6". The last section lists each sound to find or make, one line each, which is what sound generation is sent. `review-consistency` checks the draft against the rest of the brief page, as its own request, before the user approves it.

## Hand back

- the draft of the brief page's sound design section, for the user's approval and for `project-brief` to place;
- the facts it settles, by `<element>: <fact>`, for `project-pipeline` to publish: each sound to find or make as `<sound>: description`, which `generate-sound` sends as `{{<sound>: description}}`;
- the sounds to find or make, each to be made as its own take;
- the cue times, for the audio cut and for timing the animatic.
