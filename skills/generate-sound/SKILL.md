---
name: generate-sound
description: Make a scene's sound effects and music together as one take with no voices - its room, every effect, and the music, each at its time on the timing reference - from a model that generates a whole scene from words, so the voices made apart can be laid over it. Use once the sound design brief and the timing reference exist. Not the voices (generate-voice), the briefs, or the mix (build-animatic).
---

# Sound and music

As the user set on 2026-11-13, a scene's sound effects and music are made together, in one take, with no voices; the dialogue is made apart and laid over them. Made together, the room, the effects, and the music sit in one space; made with the voice, the voice suffered and could not be placed; made one by one, a room tone alone sounded wrong, music alone was rejected, and library sounds did not fit.

A good take runs the scene's whole length as one continuous bed, with each event's sound at its time, clear of what is around it, and the music doing what the audio identity brief asks. A failed one carries a voice or a breath, drops to silence where the brief has none, adds a sound the canon has no source for, misses an event, or puts a cue late or under louder sound.

## The models and the route

A text-to-audio model that makes sound effects and music in one pass from words, with a timeline in its prompt, such as Seed Audio 1.0 on fal (`bytedance/seed-audio-1.0`), the user's choice on 2026-11-13, at the film's sample rate in wav. The model's workflow and prompt skills give its specifics and limits. This skill builds the request and hands it back; [project-requests](../project-requests/SKILL.md) runs it with `scripts/request.py`, which sends it exactly as built. What a request costs comes from the setup, and nothing is paid before the user's yes.

## What it needs

Each input by its canonical name, from the pipeline's table:

- the sound design brief, `<film>: sound design brief`, for each sound and the music, and its events table, for every event the scene's sound must carry, on screen or off;
- the audio identity brief, `<film>: audio identity brief`, for what the music does and its never list;
- the timing reference, `<film>: timing reference`, for each cue's time, as facts such as `<cue>: start`.

## Making it

Fill [the sound prompt template](templates/sound-prompt.md): what the scene is and that it has no voices, then the timeline in seconds, each cue at the timing reference's time, as the sound design brief describes it, then what must not be heard. Where a line or a voice sound will be laid over it, the timeline says only that no new sound comes, so the bed leaves room. Every cue's time is written in the step's template as `{{<cue>: start}}` and `{{<cue>: end}}`, filled from the pipeline's table, never typed in by hand. Before sending, check the timeline against the events table: every event has its line, and the never list names no sound an event makes. A bell over a door with "no door creak" on the never list is the failure this check is for: Last order's bed (2026-11-12) had both. Send nothing else.

Make one take. Measure it before showing it, since an agent cannot listen; say so, and let the user judge the sound:

- its length, and from its loudness over time whether it runs continuously;
- each cue's onset, from a jump in loudness, overall or in the cue's band (a high-pass for a bell or a click), against the cue's time: a cue more than 0.1 s from its time, or less than about 6 dB above the half second before it, fails the take. Last order's bed put the bell, timed at 3.0 s, at about 3.45 s and only faintly above the room, and nothing caught it; the final shot's model, which times its picture by the sound's events, then had no bell to time the door by.

A take that fails is made again, as its own request, with one change, or the cue is laid in from a sound made apart, at its exact time, in the mix.

## Hand back

Hand back to `project-requests`:

- the request: the text-to-audio endpoint, at the film's sample rate in wav; the prompt as a template naming canon, `{{<element>: <fact>}}`; and no references;

and, for the user to approve:

- the take, with its measured length and each cue's measured onset against its time; once approved, `project-pipeline` publishes it as the scene's bed, `<scene>: sound bed`, which the mix lays the voices over, made from the sound design brief, the beat sheet or script, and the place's floor plan (`--from`), so a change to the story or to an event's place or time reaches the bed, as it reaches the frames. A rejected take is never used as an input again.
