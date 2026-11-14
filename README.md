# Spumcake Agent

An agnostic, open-source collection of pre-made skills for animated filmmaking from [Spumcake](https://spumcake.tv), an AI-native entertainment and technology company. Spumcake Studio imports them when it is installed, and any agent with access to its own execution stack can use them. The skills are about creative tasks, not about any one product: how Spumcake Studio or the platform works is described in their own documents, never here.

Skills for general AI animated filmmaking, with the user directing every step: planning a story from beat sheet to shot list, setting a concept's style and colour, designing and referencing its subjects and places, and boarding and timing its shots. Each skill plans its task and creates the prompts destined for the models that make its results; the setup it runs in renders them.

[docs/overview.md](docs/overview.md) says what Spumcake Agent is and where it is going. [docs/prompt-roles.md](docs/prompt-roles.md) describes the roles a prompt is filled by, and what a setup provides to run it. [docs/records.md](docs/records.md) describes the record every file keeps, its paper trail and contents, written with [scripts/records.py](scripts/records.py); [scripts/generate.py](scripts/generate.py) sends a prompt to an image or audio model exactly as written and writes the result's record.

## Skills

Each skill belongs to one category, the first word of its name, which says what it produces and the parts every skill in it has, as [docs/skill-categories.md](docs/skill-categories.md) describes. The order the skills run in is in [the pipeline](docs/pipeline.md).

| Category | Skill | Does |
|---|---|---|
| build | [build-animatic](skills/build-animatic/SKILL.md) | times the boards to the shot list as an editable timing sheet, and checks it against the lines |
| | [build-line-up](skills/build-line-up/SKILL.md) | sets several subjects side by side at true relative scale, as a line-up or a height chart |
| | [build-previs](skills/build-previs/SKILL.md) | builds a place's simple 3D mock-up, each piece a recognisable shape from the research with a key naming it, and renders its shot and its views |
| fix | [fix-canonical-image](skills/fix-canonical-image/SKILL.md) | fixes a generated image from its continuity review: traces each finding to the pre-vis or the generation, and fixes it there, across every view |
| generate | [generate-background](skills/generate-background/SKILL.md) | makes the background plates for each shot or camera setup, with no characters |
| | [generate-board](skills/generate-board/SKILL.md) | draws a rough layout frame for each shot of an approved shot list, or from the user's sketch |
| | [generate-concept-artwork](skills/generate-concept-artwork/SKILL.md) | makes concept artwork from concept art references: a character staged into a place's painting, the look reference for first frames |
| | [generate-concept-design](skills/generate-concept-design/SKILL.md) | explores what a subject or place could look like, with a brief, directions, text-to-image candidates, and refinements, before it is canonical |
| | [generate-concept-reference](skills/generate-concept-reference/SKILL.md) | turns a canonical reference into its concept art reference: a character's study, a place's view in each mood |
| | [generate-detail-sheet](skills/generate-detail-sheet/SKILL.md) | makes a character's or prop's level-of-detail sheet: the subject at four distances, painted for concept artwork or in line for the animatic, fewer strokes the further it is |
| | [generate-keyframe](skills/generate-keyframe/SKILL.md) | makes each camera's animatic layout drawing, then an on-model keyframe in line for each shot of an approved shot list, for the animatic |
| | [generate-model-sheet](skills/generate-model-sheet/SKILL.md) | makes a subject's expression sheet, pose sheet, mouth chart, and colour model, and a character's animatic expression sheet, acting sheet, and turnaround |
| | [generate-sound](skills/generate-sound/SKILL.md) | makes a scene's sound effects and music as one bed with no voices |
| | [generate-subject-dataset](skills/generate-subject-dataset/SKILL.md) | makes a themed dataset of images of an existing subject |
| | [generate-subject-reference](skills/generate-subject-reference/SKILL.md) | builds a recurring subject's brief, reference sheets, and gallery; a character's A-pose views; a small prop's sheet |
| | [generate-voice](skills/generate-voice/SKILL.md) | makes each line as a voice-only take from its voice brief |
| make | [make-canonical](skills/make-canonical/SKILL.md) | makes one recurring place, character, or prop canonical, step by step, from a story check through its neutral views, including its canonical images and their neutral passes |
| | [make-colour-script](skills/make-colour-script/SKILL.md) | plans the colour and light of each beat, then a keyframe for each, in story order |
| | [make-style-guide](skills/make-style-guide/SKILL.md) | builds a concept's style rules, and the prompts for style frames to choose from and a style sheet |
| prompt | [prompt-image](skills/prompt-image/SKILL.md) | writes the words of any image prompt as visual, image-generator phrases, not prose |
| research | [research-references](skills/research-references/SKILL.md) | researches real places and character archetypes on the web, into a sourced reference board, and a film's mood into a mood brief, with frames from CG animated features read for their light |
| review | [review-consistency](skills/review-consistency/SKILL.md) | checks a film's written artifacts for drift: one home for every fact, the rest pointing to it |
| | [review-continuity](skills/review-continuity/SKILL.md) | reviews an image, clip, lip-sync, final shot, or sound against its references and the shots around it, and reports every difference |
| write | [write-audio-identity-brief](skills/write-audio-identity-brief/SKILL.md) | drafts from the brief and the visual identity brief what a film's sound is for, before any other research |
| | [write-beat-sheet-prompt](skills/write-beat-sheet-prompt/SKILL.md) | plans a story's beat sheet and builds the prompt a language model writes it from |
| | [write-breakdown-prompt](skills/write-breakdown-prompt/SKILL.md) | plans a film's breakdown of every recurring character, place, and prop, and builds the prompt a language model writes it from |
| | [write-script-prompt](skills/write-script-prompt/SKILL.md) | plans a script from the approved beats and builds the prompt a language model writes it from |
| | [write-shot-list-prompt](skills/write-shot-list-prompt/SKILL.md) | plans a timed shot list from the script and builds the prompt a language model writes it from |
| | [write-sound-design-brief](skills/write-sound-design-brief/SKILL.md) | drafts every sound of a film cue by cue on its length, a spotting list, which sound generation and the audio cut are made from |
| | [write-timing-reference](skills/write-timing-reference/SKILL.md) | works out every moment, sound cue, line, and animatic frame on one timeline before anything is made |
| | [write-visual-identity-brief](skills/write-visual-identity-brief/SKILL.md) | drafts what a film should feel and look like, what its colours must achieve, and candidate palettes, from the brief, the mood brief, and the visual identity research |
| | [write-voice-brief](skills/write-voice-brief/SKILL.md) | drafts one speaking character's voice and the delivery of each of their lines, the description voice generation is sent |

Every skill keeps the user in charge. Nothing renders, downloads, or spends money before they approve that plan, and they choose what to keep.

## Licence

Spumcake Agent is licensed under the [Apache License 2.0](LICENSE).
