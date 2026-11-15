# The pipeline

The order the skills run in to make one animated film, and what each step is made from. Each step is made only from the canon the steps before it published; a rejected result is never an input to anything. Every step runs as requests through `project-requests`, in a project laid out as [projects.md](projects.md) describes.

The user gives a brief; the agent turns it into finished results, making every choice the brief leaves open itself, from the brief, and saying why, and the user edits any result they want changed. No step waits for the user to choose. The point of the pipeline is the intermediate steps: every canonical element of a film, its places, characters, props, look, and sound, is made, shown, and open to the user's changes before any video is generated, so the user's intent survives to the final render.

## 1. Concept and intent

1. **The concept:** the user's brief: premise, characters, length, genre, and tone.
1. **The final look** (`make-style-guide`), right after the brief and before anything else is made: how the finished film looks, chosen by the user by eye from test frames. When the user gives no look, it is a feature 3D animated film look, as the canonical references' viewport shading already shows things. Every canonical reference, and every final frame, is made toward it.
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

The style guide's rules beyond the final look (`make-style-guide`) are filled in alongside the story, from the visual identity brief.

**Working looks are never the final look.** Concept art is painted loosely so colour, light, and shape can be judged without detail; the animatic and the line-art animation are line art so staging and acting can be judged without light or shading. Neither is a style for the finished film, and neither is ever sent as one.

## 3. Breakdown

Every recurring character, place, and prop the script needs, what each must be in general, and the shots it appears in (`write-breakdown-prompt`).

## 4. Concept art and hand-drawn designs, before canon

As the user set on 2026-11-15, after Last order, the film's places, props, and staging are found in concept art, and its characters are designed by hand, before anything is made canonical. Last order made its canon first, from a grey mock-up, and its CG character first, from photographs; its better-staged concept art and its more appealing drawings came after, when the canon was already fixed.

1. **Concept ideation** (`generate-concept-artwork`'s concept ideation template, from text alone, staged planimetrically): the film's moments, painted, until the user approves their staging, places, and props. The canonical places and props are derived from the approved paintings.
2. **Hand-drawn character designs** (`generate-concept-design`'s hand-drawn route, or the user's own drawings): each character's forms, proportions, and appeal, front and in the poses the story needs. The CG character is built from the approved drawings, keeping their forms.

## 5. Canonical elements

Each recurring element is made canonical, one at a time, from its approved concept art or drawings, before any concept art reference or staging uses it. A place's primary canonical location is its canonical angle: every later step that returns to the place starts from it and its passes.

Each through `make-canonical`, which holds each one's steps:

- **A place,** from its approved concept art, its research (`research-references`), and its pre-vis (`build-previs`), built to the concept art's staging, ending in its floor plan (`write-staging-plan`): where everything is and what each thing is called, which every later step that places or directs a character reads first.
- **A character,** from its approved hand-drawn designs, its research, and the place's texture view; the CG character keeps the drawings' forms.

**One camera per view.** A canonical view of a place is made from its camera's pre-vis render as structure, and approved only when the pre-vis's edges, laid over it, line up. Every later image from that camera, the layouts, the plates, and the final frames, then shares one camera. Last order's canonical far-end view was an image model's guess at the pre-vis camera, drawn lower and wider; its animatic followed the pre-vis and its final render the view, and the two never lined up.
- **A small prop,** from its character's coloured A-pose and its photographs.
- **Several characters** (`build-line-up`): a height chart composited from their A-pose fronts, not generated.

## 6. Concept art from canon

Canonical reference, then concept art reference, then concept artwork, so concept artwork and the images for video rest on the same canon. The concept ideation that came before the canon (section 4) is not canon itself; the canon was derived from it.

1. **Concept art references** (`generate-concept-reference`): each canonical element repainted in the concept look: a character's front study from its A-pose and its props' sheets; each view of a place in each mood, from its texture pass and the visual identity brief.
2. **Level-of-detail sheets** (`generate-detail-sheet`): each character and prop to be staged, painted at four distances with one brush size, so concept artwork paints it with the detail its distance allows.
3. **Concept artwork** (`generate-concept-artwork`): characters' studies placed into a place's painting, for a moment of the film; it visualises the mood and look design, and is the look reference for the first frames.

## 7. Staging and the shots

1. **The animatic,** in the order the user set on 2026-11-13:
   1. **Timing** (`write-timing-reference`): every moment, sound cue, line, and frame on one timeline, before anything is made; the sound and the frames are both made to it.
   2. **Audio:** the voices (`generate-voice`), voice only, and the sound effects and music together as one bed with no voices (`generate-sound`), made apart and laid together in the mix.
   3. **Frames:** each character's animatic sheets (`generate-model-sheet`, `generate-detail-sheet`); each moment's staging floor plan (`build-previs`), approved before any frame of the moment; each camera's layout drawing; then the keyframes the timing reference lists (`generate-keyframe`), in partially completed line art with no shading.
   4. **Assembly** (`build-animatic`): the frames held on their times over the mixed audio, rendered as one video. Staging into the canonical views, with the concept artwork as the look reference, makes the first frames for video (`generate-keyframe`'s staging).
2. **Line-art animation,** lip-synced to the voices.
3. **Final animation,** over background plates (`generate-background`), and the cut.
   Its first and last frames are made in two steps. First the plate (`generate-background`): the place's canonical view from the shot's camera, in its neutral viewport shading, lit the way the concept artwork lights the place, in the final look, with no one in it; one plate for each state of the place the shot needs, such as a door closed and a door open. Then the staging (`generate-keyframe`): the canonical characters, from their own canonical images, never a concept study or the animation's sheets, placed into the plate where the shot's line-art frame puts them, lit by the plate's light as the concept artwork lights them. The final shot is made from those frames, the line-art shot's motion, and the characters' canonical references.
   **The characters' pose references** (`generate-canonical-image`), before the final render: each character's canonical CG image at each of the animatic's key poses and expressions, made from their CG canon and approved; they are the character's references in every final request, with the turnaround views. Last order sent two standing front views, and nothing of Otis in any pose from the shot.
   **No motion blur** in any CG render: blur is added in post, after any retime or upscale. Last order's blur, rendered in, broke into artifacts under frame interpolation and upscaling.

Consistency is checked (`review-consistency`) at the end of every step that writes or changes a section of the brief, a story document, the style guide, or a step's template: every fact has one home, and the rest point to it.

Continuity is reviewed (`review-continuity`) at the end of every step that makes an image, a clip, or a sound, before the user approves it.

## The brief and the pipeline

The identity briefs, the voices, the sound design, and the timing are sections of one brief page, which `project-brief` keeps. What is canon is the pipeline's table, which `project-pipeline` keeps: every published result, every canonical fact, what each published image shows, and each step as a template that names canon. The agent reads the table before every step, to know what the step is made from, and compares it with the brief to know what is still missing. Both are described in [projects.md](projects.md).
