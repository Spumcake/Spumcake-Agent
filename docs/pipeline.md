# The pipeline

The order the skills run in to make one animated film, and what each step is made from. Each step is made only from the latest approved results of the steps before it; a rejected round is never an input to anything.

The user gives a brief; the agent turns it into finished results, making every choice the brief leaves open itself, from the brief, and saying why, and the user edits any result they want changed. No step waits for the user to choose. The point of the pipeline is the intermediate steps: every canonical element of a film, its places, characters, props, look, and sound, is made, shown, and open to the user's changes before any video is generated, so the user's intent survives to the final render.

## 1. Concept and intent

1. **The concept:** the user's brief: premise, characters, length, genre, and tone.
2. **The mood brief** (`research-references`), from the brief; the agent chooses the direction that serves it best.
3. **Visual identity research** (`research-references`), from the brief and the chosen mood; the agent keeps the frames that fit.
4. **The visual identity brief** (`write-visual-identity-brief`), from the brief, the mood brief, and the visual identity research.
5. **The audio identity brief** (`write-audio-identity-brief`), from the brief and the visual identity brief.

No other research begins until the identity briefs are written. Every later research question, for the canonical elements and for the mood, comes from them, so what is searched for serves what the film is meant to be.

## 2. Story

1. **Beat sheet** (`write-beat-sheet-prompt`), from the concept and the identity briefs.
2. **Script** (`write-script-prompt`), from the beat sheet.
3. **Shot list** (`write-shot-list-prompt`), from the script.

The look's style guide (`create-style-guide`) is made alongside the story, from the visual identity brief.

## 3. Breakdown

Every recurring character, place, and prop the script needs, what each must be in general, and the shots it appears in (`write-breakdown-prompt`). Concept candidates from the concept context template (`create-concept-art`) may explore what an element could look like before it is made canonical.

## 4. Canonical elements

Each recurring element is made canonical, one at a time, before any concept art with characters. A place's primary canonical location is its canonical angle: every later step that returns to the place starts from it and its passes.

Each through `make-canonical`, which holds each one's steps:

- **A place,** from its research (`research-references`) and its pre-vis (`create-previs`).
- **A character,** from its research and the place's texture view.
- **A small prop,** from its character's coloured A-pose and its photographs.
- **Several characters** (`create-line-up`): a height chart composited from their A-pose fronts, not generated.

## 5. Concept art

1. **The character study** (`create-concept-art`), from the main character's coloured form front A-pose; it becomes the style reference.
2. **The places, restyled to match** the character study (`create-concept-art`), each from its canonical angle's texture pass, then tried in each mood from the visual identity brief.
3. **The concept art** (`create-concept-art`), from the character study and the restyled places.

## 6. Staging and the shots

1. **Staging** (`create-concept-art`): the canonical characters and props placed into the place's view each shot uses.
2. **The animatic:** keyframes (`create-keyframe`), timed (`create-animatic`), with voices made first, as the audio identity brief describes them.
3. **Line-art animation,** lip-synced to the voices.
4. **Final animation,** over background plates (`create-background`), and the cut.

Consistency is checked (`check-canonical-consistency`) at the end of every step that writes or changes a brief, a story document, the style guide, a prompt, or the film map: every fact has one home, and the rest point to it.

Continuity is reviewed (`review-continuity`) at the end of every step that makes an image, a clip, or a sound, before the user approves it.

## The film map

Every film keeps one map of its canonical artifacts, started with the concept and updated at the end of every step: each artifact the film needs, from the briefs and the research through the pre-vis, the canonical renders, the concept art's references and the concept art itself, to the keyframes, the animatic, the voices, and the cut; its status, as [the film map template](film-map-template.md) names them; and the full path of the one version that counts. Rejected rounds are not listed, only that they were rejected. The agent reads the map before every step, to know what the step is made from and what is still missing, and the user reads it to find any file. Fill [the film map template](film-map-template.md).
