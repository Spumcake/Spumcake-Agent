# The pipeline

The order the skills run in to make one animated film, and what each step is made from. Each step is made only from the canon the steps before it published; a rejected result is never an input to anything. Every step runs as requests through `project-requests`, in a project laid out as [projects.md](projects.md) describes.

The user gives a brief; the agent turns it into finished results, making every choice the brief leaves open itself, from the brief, and saying why, and the user edits any result they want changed. No step waits for the user to choose. The point of the pipeline is the intermediate steps: every canonical element of a film, its places, characters, props, look, and sound, is made, shown, and open to the user's changes before any video is generated, so the user's intent survives to the final render.

## 1. Concept and intent

1. **The concept:** the user's brief: premise, characters, length, genre, and tone.
2. **The mood brief** (`write-mood-brief`), from the brief; the agent chooses the direction that serves it best.
3. **Visual identity research** (`research-references`), from the brief and the chosen mood; the agent keeps the frames that fit.
4. **The visual identity brief** (`write-visual-identity-brief`), from the brief, the mood brief, and the visual identity research.
5. **The audio identity brief** (`write-audio-identity-brief`), from the brief and the visual identity brief: what the sound is for.
6. **A voice brief per speaking character** (`write-voice-brief`), from the audio identity brief and the beat sheet or script: what each voice sounds like and how each line is delivered.
7. **The sound design brief** (`write-sound-design-brief`), from the audio identity brief, the beat sheet or script, and the voice briefs: every sound, cue by cue, timed on the film's length.

The voice and sound design briefs are written once the beat sheet exists, and redone when the script changes a line or a moment.

No other research begins until the identity briefs are written. Every later research question, for the canonical elements and for the mood, comes from them, so what is searched for serves what the film is meant to be.

## 2. Story

1. **Beat sheet** (`write-beat-sheet-prompt`), from the concept and the identity briefs.
2. **Script** (`write-script-prompt`), from the beat sheet.
3. **Shot list** (`write-shot-list-prompt`), from the script.

The look's style guide (`make-style-guide`) is made alongside the story, from the visual identity brief.

## 3. Breakdown

Every recurring character, place, and prop the script needs, what each must be in general, and the shots it appears in (`write-breakdown-prompt`). Concept candidates from the concept context template (`generate-concept-design`) may explore what an element could look like before it is made canonical.

## 4. Canonical elements

Each recurring element is made canonical, one at a time, before any concept art with characters. A place's primary canonical location is its canonical angle: every later step that returns to the place starts from it and its passes.

Each through `make-canonical`, which holds each one's steps:

- **A place,** from its research (`research-references`) and its pre-vis (`build-previs`), ending in its floor plan (`write-staging-plan`): where everything is and what each thing is called, which every later step that places or directs a character reads first.
- **A character,** from its research and the place's texture view.
- **A small prop,** from its character's coloured A-pose and its photographs.
- **Several characters** (`build-line-up`): a height chart composited from their A-pose fronts, not generated.

## 5. Concept art

Canonical reference, then concept art reference, then concept artwork, so concept artwork and the images for video rest on the same canon. Before any canon exists, concept artwork can also be made from text alone, for ideation (`generate-concept-artwork`'s concept ideation template, staged planimetrically); it is not canon.

1. **Concept art references** (`generate-concept-reference`): each canonical element repainted in the concept look: a character's front study from its A-pose and its props' sheets; each view of a place in each mood, from its texture pass and the visual identity brief.
2. **Level-of-detail sheets** (`generate-detail-sheet`): each character and prop to be staged, painted at four distances with one brush size, so concept artwork paints it with the detail its distance allows.
3. **Concept artwork** (`generate-concept-artwork`): characters' studies placed into a place's painting, for a moment of the film; it visualises the mood and look design, and is the look reference for the first frames.

## 6. Staging and the shots

1. **The animatic,** in the order the user set on 2026-11-13:
   1. **Timing** (`write-timing-reference`): every moment, sound cue, line, and frame on one timeline, before anything is made; the sound and the frames are both made to it.
   2. **Audio:** the voices (`generate-voice`), voice only, and the sound effects and music together as one bed with no voices (`generate-sound`), made apart and laid together in the mix.
   3. **Frames:** each character's animatic sheets (`generate-model-sheet`, `generate-detail-sheet`); each moment's staging floor plan (`build-previs`), approved before any frame of the moment; each camera's layout drawing; then the keyframes the timing reference lists (`generate-keyframe`), in partially completed line art with no shading.
   4. **Assembly** (`build-animatic`): the frames held on their times over the mixed audio, rendered as one video. Staging into the canonical views, with the concept artwork as the look reference, makes the first frames for video (`generate-keyframe`'s staging).
2. **Line-art animation,** lip-synced to the voices.
3. **Final animation,** over background plates (`generate-background`), and the cut.

Consistency is checked (`review-consistency`) at the end of every step that writes or changes a section of the brief, a story document, the style guide, or a step's template: every fact has one home, and the rest point to it.

Continuity is reviewed (`review-continuity`) at the end of every step that makes an image, a clip, or a sound, before the user approves it.

## The brief and the pipeline

The identity briefs, the voices, the sound design, and the timing are sections of one brief page, which `project-brief` keeps. What is canon is the pipeline's table, which `project-pipeline` keeps: every published result, every canonical fact, what each published image shows, and each step as a template that names canon. The agent reads the table before every step, to know what the step is made from, and compares it with the brief to know what is still missing. Both are described in [projects.md](projects.md).
