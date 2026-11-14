---
name: generate-voice
description: Make each speaking character's lines and voice sounds from their voice brief - one take of voice only, no sound effects and no music, per line or per run of lines, from a model that takes the voice and the delivery as words - then measure each take and place it on the timing reference. Use once a character's voice brief and the timing reference exist. Not the voice brief (write-voice-brief), the sound effects and music (generate-sound), or the mix (build-animatic).
---

# Voices

As the user set on 2026-11-13, dialogue is made apart from the sound and the music: one take of voice only, which the mix lays over the separately made sound. A voice generated inside a whole scene came out worse and could not be moved; a voice alone could be placed on its cue.

A good take sounds like the voice brief, says every word of the line as written, with the delivery it gives, and nothing else. A failed one rushes or garbles the line, changes the words, or carries room sound or music.

## The models and the route

A text-to-speech or text-to-audio model that takes the voice and the delivery as words in its prompt, such as Seed Audio 1.0 on fal (`bytedance/seed-audio-1.0`), the user's choice on 2026-11-13, at the film's sample rate in wav. The model's workflow and prompt skills give its specifics and limits. This skill builds the request and hands it back; [project-requests](../project-requests/SKILL.md) runs it with `scripts/request.py`, which sends it exactly as built. What a request costs comes from the setup, and nothing is paid before the user's yes.

## What it needs

Each input by its canonical name, from the pipeline's table:

- the character's voice brief, `<character>: voice brief`;
- the timing reference, `<film>: timing reference`, for each line's time and room, as facts such as `<line>: start`;
- the script's lines, each word for word, as facts such as `<line>: text`.

## Making it

Fill [the voice prompt template](templates/voice-prompt.md) from the voice brief: the voice in its own words, then the delivery, then the line word for word, and the non-verbal sounds before or after it in the order the timing reference gives. The line's words are written in the step's template as `{{<line>: text}}`, filled from the pipeline's table, never typed in by hand. Send nothing else: no reference audio, no other take, unless the user asks, since the user keeps requests as simple as possible, and a take sent as a reference was stitched in rather than matched (2026-11-13).

Make one take per line or run of lines, at the film's sample rate, in wav. Measure it before showing it: its length, and from its loudness over time where each breath, word, and pause falls, since an agent cannot listen; say so, and let the user judge the sound.

## Hand back

Hand back to `project-requests`, one request per line or run of lines, in the timing reference's order:

- the request: the text-to-speech or text-to-audio endpoint, at the film's sample rate in wav; the prompt as a template naming canon, `{{<element>: <fact>}}`; and no references, unless the user asks for one;

and, for the user to approve:

- each take, with where each line and voice sound starts and ends inside it; once approved, `project-pipeline` publishes it, such as `<line>: voice take`, and its measured length as a fact, `<line>: length`, which replaces the timing reference's estimate. A rejected take is never used as an input again.
