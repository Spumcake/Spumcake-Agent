# Spumcake Agent

An agnostic, open-source collection of pre-made skills from [Spumcake](https://spumcake.tv), an AI-native entertainment and technology company. Spumcake Studio imports them when it is installed, and any agent with access to its own execution stack can use them. The skills are about creative tasks, not about any one product: how Spumcake Studio or the platform works is described in their own documents, never here.

General skills for an agent that makes generative media with a person directing it: rendering a prompt, writing one, cleaning up or redrawing artwork, building a character's reference, and captioning, training, and testing a character LoRA.

A general skill says how to go about a task, with any model and in any setup. It finds the specifics in two other kinds of skill:

- a **workflow skill**, which says what is true of one model family;
- an **execution skill**, which says how a step runs with one tool in a given setup.

[docs/skill-layers.md](docs/skill-layers.md) describes the layers and the setup file. [docs/workflow-manifest.md](docs/workflow-manifest.md) describes a model family's workflow repository.

## Skills

| Skill | Does |
|---|---|
| [run-prompt](skills/run-prompt/SKILL.md) | renders a written prompt, again, elsewhere, reproduced, or as a follow-up pass |
| [write-prompt](skills/write-prompt/SKILL.md) | writes a prompt's fields, with an optional model pass |
| [find-missing-models](skills/find-missing-models/SKILL.md) | lists the models a server lacks, and downloads only approved files |
| [design-workflow](skills/design-workflow/SKILL.md) | adds a model family's graph, look, prompt skill, and workflow skill |
| [clean-artwork](skills/clean-artwork/SKILL.md) | denoises flat digital art without redrawing it |
| [refine-artwork](skills/refine-artwork/SKILL.md) | redraws artwork lightly in a model's look |
| [create-character-reference](skills/create-character-reference/SKILL.md) | builds a character's brief, reference sheets, and gallery with an image-edit model |
| [create-character-gallery](skills/create-character-gallery/SKILL.md) | makes a themed gallery of an existing character |
| [caption-lora-dataset](skills/caption-lora-dataset/SKILL.md) | captions a character's dataset as the prompts that would make each image |
| [train-lora](skills/train-lora/SKILL.md) | trains a character LoRA with a model family's recipe |
| [test-lora](skills/test-lora/SKILL.md) | tests a character LoRA for breadth across every look |
| [create-character-lora](skills/create-character-lora/SKILL.md) | sequences the steps above into a tested character LoRA |
| [image-to-video](skills/image-to-video/SKILL.md) | animates a first frame, optionally to a last frame, with sound |
| [image-to-video-prompt-guide](skills/image-to-video-prompt-guide/SKILL.md) | writes a video prompt: action, pace, camera, ending, and sound |

Every skill keeps the person in charge. Nothing renders, trains, downloads, or spends money before they approve that plan, and they choose what to keep.
