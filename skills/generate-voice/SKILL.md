---
name: generate-voice
description: Make each speaking character's lines and voice sounds from their voice brief - one take of voice only, no sound effects and no music, per line or per run of lines, from a model that takes the voice and the delivery as words - then measure each take and place it on the timing reference. Use once a character's voice brief and the timing reference exist. Not the voice brief (write-voice-brief), the sound effects and music (generate-sound), or the mix (build-animatic).
---

# Voices

As the user set on 2026-11-13, dialogue is made apart from the sound and the music: one take of voice only, which the mix lays over the separately made sound. A voice generated inside a whole scene came out worse and could not be moved; a voice alone could be placed on its cue.

A good take sounds like the voice brief, says every word of the line as written, with the delivery it gives, and nothing else. A failed one rushes or garbles the line, changes the words, or carries room sound or music.

## The models and the route

A text-to-speech or text-to-audio model that takes the voice and the delivery as words in its prompt, such as Seed Audio 1.0 on fal (`bytedance/seed-audio-1.0`), the user's choice on 2026-11-13, at the film's sample rate in wav. The execution skill that implements `generate-voice` in this setup renders it. Whatever renders it writes the result's [record](../../docs/records.md); [`scripts/generate.py`](../../scripts/generate.py) renders it so.

## What it needs

- the character's voice brief;
- the timing reference, for each line's time and room;
- a folder for the prompts and the takes.

## Making it

Fill [the voice prompt template](templates/voice-prompt.md) from the voice brief: the voice in its own words, then the delivery, then the line word for word, and the non-verbal sounds before or after it in the order the timing reference gives. Send nothing else: no reference audio, no other take, unless the user asks, since the user keeps requests as simple as possible, and a take sent as a reference was stitched in rather than matched (2026-11-13).

Make one take per line or run of lines, at the film's sample rate, in wav. Measure it before showing it: its length, and from its loudness over time where each breath, word, and pause falls, since an agent cannot listen; say so, and let the user judge the sound. Show each take with its prompt, its settings, and its cost.

## Hand back

- each kept take, with where each line and voice sound starts and ends inside it;
- the lengths, for the timing reference, which replace its estimates.
