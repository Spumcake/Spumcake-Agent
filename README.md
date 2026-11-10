# Spumcake Agent

An agnostic, open-source collection of pre-made skills for animated filmmaking from [Spumcake](https://spumcake.tv), an AI-native entertainment and technology company. Spumcake Studio imports them when it is installed, and any agent with access to its own execution stack can use them. The skills are about creative tasks, not about any one product: how Spumcake Studio or the platform works is described in their own documents, never here.

Skills for general AI animated filmmaking, with the user directing every step: planning a story from beat sheet to shot list, setting a concept's style and colour, designing and referencing its subjects and places, and boarding and timing its shots. Each skill plans its task and creates the prompts destined for the models that make its results; the setup it runs in renders them.

[docs/overview.md](docs/overview.md) says what Spumcake Agent is and where it is going. [docs/prompt-roles.md](docs/prompt-roles.md) describes the roles a prompt is filled by, and what a setup provides to run it.

## Skills

The order the skills run in is in [the pipeline](docs/pipeline.md).

| Skill | Does |
|---|---|
| [write-beat-sheet-prompt](skills/write-beat-sheet-prompt/SKILL.md) | plans a story's beat sheet and builds the prompt a language model writes it from |
| [write-script-prompt](skills/write-script-prompt/SKILL.md) | plans a script from the approved beats and builds the prompt a language model writes it from |
| [write-shot-list-prompt](skills/write-shot-list-prompt/SKILL.md) | plans a timed shot list from the script and builds the prompt a language model writes it from |
| [create-style-guide](skills/create-style-guide/SKILL.md) | builds a concept's style rules, and the prompts for style frames to choose from and a style sheet |
| [create-concept-art](skills/create-concept-art/SKILL.md) | explores a design with text-to-image candidates, makes a place's or character's primary canonical image, new views, neutral passes, mood references, the concept art, and staging |
| [create-colour-script](skills/create-colour-script/SKILL.md) | plans the colour and light of each beat, then a keyframe for each, in story order |
| [research-references](skills/research-references/SKILL.md) | researches real places and character archetypes on the web, into a sourced reference board, and a film's mood into a mood brief |
| [create-previs](skills/create-previs/SKILL.md) | builds a place's simple 3D mock-up, each piece a recognisable shape from the research with a key naming it, and renders its shot and its views |
| [canonical-cleanup](skills/canonical-cleanup/SKILL.md) | audits a generated image against its canonical prompt and the pre-vis, traces each fault to the pre-vis or the generation, and fixes it, across every view |
| [write-breakdown-prompt](skills/write-breakdown-prompt/SKILL.md) | plans a film's breakdown of every recurring character, place, and prop, and builds the prompt a language model writes it from |
| [make-canonical](skills/make-canonical/SKILL.md) | makes one recurring place, character, or prop canonical, step by step, from a story check through its neutral views |
| [create-subject-reference](skills/create-subject-reference/SKILL.md) | builds a recurring subject's brief, reference sheets, and gallery; a character's A-pose views; a small prop's sheet |
| [create-subject-dataset](skills/create-subject-dataset/SKILL.md) | makes a themed dataset of images of an existing subject |
| [create-model-sheet](skills/create-model-sheet/SKILL.md) | makes a subject's expression sheet, pose sheet, mouth chart, and colour model |
| [create-line-up](skills/create-line-up/SKILL.md) | sets several subjects side by side at true relative scale, as a line-up or a height chart |
| [create-keyframe](skills/create-keyframe/SKILL.md) | makes an on-model keyframe for each shot of an approved shot list, for the animatic |
| [create-background](skills/create-background/SKILL.md) | makes the background plates for each shot or camera setup, with no characters |
| [review-continuity](skills/review-continuity/SKILL.md) | reviews an image, clip, lip-sync, final shot, or sound against its references and the shots around it, and reports every difference |
| [create-board](skills/create-board/SKILL.md) | draws a rough layout frame for each shot of an approved shot list, or from the user's sketch |
| [create-animatic](skills/create-animatic/SKILL.md) | times the boards to the shot list as an editable timing sheet, and checks it against the lines |

Every skill keeps the user in charge. Nothing renders, downloads, or spends money before they approve that plan, and they choose what to keep.

## Licence

Spumcake Agent is licensed under the [Apache License 2.0](LICENSE).
