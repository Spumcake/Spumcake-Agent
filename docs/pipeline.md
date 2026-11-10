# The pipeline

The order the skills run in to make one animated film, and what each step is made from. Each step is made only from the latest approved results of the steps before it; a rejected round is never an input to anything.

## 1. Story

1. **Beat sheet** (`write-beat-sheet-prompt`), from the user's brief.
2. **Script** (`write-script-prompt`), from the beat sheet.
3. **Shot list** (`write-shot-list-prompt`), from the script.

The look's style guide (`create-style-guide`) is made alongside the story.

## 2. Breakdown

Every recurring character, place, and prop the script needs, what each must be in general, and the shots it appears in (`write-breakdown-prompt`). Concept candidates from the concept context template (`create-concept-art`) may explore what an element could look like before it is made canonical.

## 3. Canonical elements

Each recurring element is made canonical, one at a time, before any concept art with characters.

Each through `make-canonical`:

- **A place:** the story check, research (`research-references`), the pre-vis (`create-previs`), the primary canonical location, canonical cleanup (`canonical-cleanup`), its views, and their grey form, coloured form, and texture passes.
- **A character:** research, the primary canonical character, canonical cleanup, then A-pose views made as textured viewport views, the front first, then the back and both sides, then the same without outer layers, then their grey and coloured form passes.
- **A small prop:** one coloured, non-textured sheet of the prop alone and in its character's hand.
- **Several characters** (`create-line-up`): a height chart composited from their A-pose fronts, not generated.

## 4. Concept art

1. **The mood brief** (`research-references`, mood investigation): genre, literary, film, and animation references, directors, painting, time of day, light, palette, camera, and presentation, in two or three directions; the user chooses.
2. **Mood references,** each place and character on its own, from its neutral references (`create-concept-art`).
3. **The concept art,** combining them (`create-concept-art`).

## 5. Staging and the shots

1. **Staging** (`create-concept-art`): the canonical characters and props placed into the place's view each shot uses.
2. **The animatic:** keyframes (`create-keyframe`), timed (`create-animatic`), with voices made first.
3. **Line-art animation,** lip-synced to the voices.
4. **Final animation,** over background plates (`create-background`), and the cut.

Continuity is reviewed (`review-continuity`) at the end of every step that makes an image, a clip, or a sound, before the user approves it.
