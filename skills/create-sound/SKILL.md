---
name: create-sound
description: Make a scene's sound effects and music together as one take with no voices - its room, every effect, and the music, each at its time on the timing reference - from a model that generates a whole scene from words, so the voices made apart can be laid over it. Use once the sound design brief and the timing reference exist. Not the voices (create-voice), the briefs, or the mix (create-animatic).
---

# Sound and music

As the user set on 2026-11-13, a scene's sound effects and music are made together, in one take, with no voices; the dialogue is made apart and laid over them. Made together, the room, the effects, and the music sit in one space; made with the voice, the voice suffered and could not be placed; made one by one, a room tone alone sounded wrong, music alone was rejected, and library sounds did not fit.

A good take runs the scene's whole length as one continuous bed, with each effect near its time and the music doing what the audio identity brief asks. A failed one carries a voice or a breath, drops to silence where the brief has none, or adds a sound the canon has no source for.

## The models and the route

A text-to-audio model that makes sound effects and music in one pass from words, with a timeline in its prompt, such as Seed Audio 1.0 on fal (`bytedance/seed-audio-1.0`), the user's choice on 2026-11-13, at the film's sample rate in wav. The execution skill that implements `create-sound` in this setup renders it. Whatever renders it writes the result's [record](../../docs/records.md); [`scripts/generate.py`](../../scripts/generate.py) renders it so.

## What it needs

- the sound design brief, for each sound and the music;
- the timing reference, for each cue's time;
- a folder for the prompt and the takes.

## Making it

Fill [the sound prompt template](templates/sound-prompt.md): what the scene is and that it has no voices, then the timeline in seconds, each cue at the timing reference's time, as the sound design brief describes it, then what must not be heard. Where a line or a voice sound will be laid over it, the timeline says only that no new sound comes, so the bed leaves room. Send nothing else.

Make one take. Measure it before showing it: its length, and from its loudness over time whether it runs continuously and where its effects fall, since an agent cannot listen; say so, and let the user judge the sound. Show it with its prompt, its settings, and its cost.

## Hand back

- the kept take, the scene's bed, which the mix lays the voices over.
