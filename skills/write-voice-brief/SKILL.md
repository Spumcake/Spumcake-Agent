---
name: write-voice-brief
description: Draft one speaking character's voice brief - what their voice sounds like, how the story's pressure shows in it, and how each of their lines and non-verbal sounds is delivered - from the audio identity brief and the beat sheet or script, as a finished draft the user edits and approves, and the one description a voice model or a casting call is given. Use for each speaking character once the audio identity brief is written, before any voice is made. Not the audio identity brief (write-audio-identity-brief), the sounds (write-sound-design-brief), or a voice.
---

# Voice brief

A voice brief is everything that makes one character's voice that character's, written so it can be heard in the head and checked against a take: "a low, rough baritone with air in it; 'friend' a fraction too careful" can be judged; "gravelly and mysterious" cannot. It is what voice generation is sent, and what a casting call reads.

A good brief describes the voice by its qualities, gives every line its delivery, and says what the character feels and hides in each. A failed one names a famous voice and stops, or describes the character instead of the voice.

This skill makes no sound. It drafts one character's part of the brief page's voices section as a finished draft and hands it back; `project-brief` places it in the page once the user approves. It does not interview the user.

## What it needs

- the audio identity: the brief page's section, for what the voice is for;
- the beat sheet (`<film>: beat sheet`) or the script (`<film>: script`), for the character's lines and the moments around them;
- the character's published images, such as `<character>: A-pose front`, and its facts, such as `<character>: apparent age`, from the pipeline's table; or, before any is published, the brief's words about them, for their apparent age and build, which the voice must fit.

## 1. Decide

From the sources, and from what the story needs where they are silent, marking each decision *proposed*:

- **Sounds like:** apparent age, pitch, timbre, texture, pace, and accent or region, each specifically.
- **Under the story's pressure:** how tiredness, fear, or whatever the story asks shows in the voice.
- **Touchstones:** performers or recordings for qualities only, each with the exact quality, such as "the gravel in the low register"; a generated voice imitates no real person, as the [prompt roles](../../docs/prompt-roles.md) say.
- **Each line,** in the script's words, quoted: its pace, volume, breath, what the character feels, what they hide, and what the line must make the audience feel.
- **Each non-verbal sound** the beats call for, such as a breath, a sigh, or a laugh: how it sounds and how long.
- **Never:** what the voice must never be.

## 2. Write the part

Fill [the voice brief template](templates/voice-brief.md), one part per character, named for them. Its last section, the description for a voice model, is the two or three sentences generation is sent; everything in it is in the sections above. `review-consistency` checks the draft against the rest of the brief page, as its own request, before the user approves it.

## Hand back

- the draft of the character's part of the brief page's voices section, for the user's approval and for `project-brief` to place;
- the facts it settles, by `<element>: <fact>`, for `project-pipeline` to publish: `<character>: voice description`, the description for a voice model, which `generate-voice` sends as `{{<character>: voice description}}`;
- its lines and non-verbal sounds, one per line, each to be recorded or generated as its own take.
