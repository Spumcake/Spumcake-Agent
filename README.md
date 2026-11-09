# Spumcake Agent

An agnostic, open-source collection of pre-made skills for animated filmmaking from [Spumcake](https://spumcake.tv), an AI-native entertainment and technology company. Spumcake Studio imports them when it is installed, and any agent with access to its own execution stack can use them. The skills are about creative tasks, not about any one product: how Spumcake Studio or the platform works is described in their own documents, never here.

Skills for general AI animated filmmaking, with the user directing every step: planning a story from beat sheet to shot list, setting a concept's style, and building a recurring subject's reference and dataset. Each skill plans its task and creates the prompts destined for the models that make its results; the setup it runs in renders them.

[docs/overview.md](docs/overview.md) says what Spumcake Agent is and where it is going. [docs/prompt-roles.md](docs/prompt-roles.md) describes the roles a prompt is filled by, and what a setup provides to run it.

## Skills

| Skill | Does |
|---|---|
| [write-beat-sheet-prompt](skills/write-beat-sheet-prompt/SKILL.md) | plans a story's beat sheet and builds the prompt a language model writes it from |
| [write-script-prompt](skills/write-script-prompt/SKILL.md) | plans a script from the approved beats and builds the prompt a language model writes it from |
| [write-shot-list-prompt](skills/write-shot-list-prompt/SKILL.md) | plans a timed shot list from the script and builds the prompt a language model writes it from |
| [create-style-guide](skills/create-style-guide/SKILL.md) | builds a concept's style rules, and the prompts for style frames to choose from and a style sheet |
| [create-subject-reference](skills/create-subject-reference/SKILL.md) | builds a recurring subject's brief, reference sheets, and gallery with an image-edit model |
| [create-subject-dataset](skills/create-subject-dataset/SKILL.md) | makes a themed dataset of images of an existing subject |

Every skill keeps the user in charge. Nothing renders, downloads, or spends money before they approve that plan, and they choose what to keep.

## Licence

Spumcake Agent is licensed under the [Apache License 2.0](LICENSE).
