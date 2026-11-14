# Spumcake Agent — overview

Spumcake Agent is an open-source, versatile repository of skills from [Spumcake](https://spumcake.tv), an AI-native entertainment and technology company. It is for general AI animated filmmaking: its skills say how to plan the creative tasks of making an animated film, from a brief to a final render, and how to create the prompts that go to the models that make each result, with the user directing every step. Spumcake Studio imports them when it is installed, Spumcake's platform uses them, and so can any agent with access to its own execution stack. Spumcake's work stays human-directed: each production moves through stages the user can see and change, so their intent survives to the final render. These skills are how an agent carries out each of those stages, the same way in any product.

## Where it is going

Every fundamental task of making an animated film gets the skills that plan it and create its prompts here: the story, from a beat sheet to a script and a shot list; visual development, from a style guide to model sheets, line-ups, and location references; continuity, from canonical references to LoRA datasets; boards and the animatic; animation tests; voices and sound; and production, from a sketch made on model to line art, colouring, lip-sync, compositing, and upscaling. Each task is tested on its own, so it is known to work. Then a first production brief is carried out from start to finish as a benchmark that performs every task.

A user will be able to ask an agent for a style guide for their show, choose a direction from its style frames, and have every later character sheet, board, and shot made in that look. They will be able to turn a beat sheet into a script, the script into a timed shot list, and the shot list into an animatic, changing one beat and seeing only what it touches change after it.

## What is always true

- **Filmmaking skills that create prompts.** A skill belongs here when it plans a stage of making a film, from pre-production or one of the fundamental tasks a production is built from, and creates the prompts destined for the models that process them and return outputs, with any model. Skills fundamental to running models or workflows in particular, such as rendering a prompt, cleaning up images, or training a LoRA, live with whatever runs them. A skill that only makes sense for one model, one tool, or one project lives with that model, tool, or project.
- **Running a model is the setup's.** A skill here says how to go about a task: the method, what a good result looks like, what the user approves, and when to stop and ask. It names no model, service, server, key, price, or command, and has no scripts, except a build skill's, which makes its result without a model. The setup it runs in provides the model's own documentation, a prompt writer, and a renderer, as [prompt-roles.md](prompt-roles.md) describes.
- **Skills are sorted by category.** A skill's name starts with its category's word, and every skill in a category has the same parts, as [skill-categories.md](skill-categories.md) describes.
- **A skill is a method.** Tasks that share a method, differing only in what the result shows, are one skill with one template per task.
- **A skill holds its own prompt rules,** and builds every prompt its task needs: for a language model, an image model, or a video model.
- **Prompts are filled by role,** such as `prompt`, `references`, and `structure`, as [prompt-roles.md](prompt-roles.md) defines them, so one prompt fits any model that takes those roles.
- **The user is in charge.** Nothing renders, trains, downloads, or spends money before the user's yes to that plan. The user chooses every keeper and judges every result; a skill never scores a picture or a sound.
- **Each result feeds what follows.** A style guide's rules and sheet go with every later image of its concept; a script's lines are the lines that are voiced and lip-synced; a shot list's lengths time the animatic. Numbers and names stay fixed once the user approves them, so a small change carries forward without remaking the rest.
- **Every image of a character who reads as a minor stays ordinary and everyday.** Nothing is sexual or suggestive, in any step, prompt, or caption.
- **It documents no product.** How Spumcake Studio or the platform works is in their own documents, never here.

## What it will never be

- Not documentation of any product, and not tied to one model, service, or setup.
- Not a tool, and not a home for running models: it runs nothing itself. Rendering, cleanup, training, and the skills a tool needs live with whatever runs them.
- Not a judge of taste: it never scores or chooses results for the user.

## Words we use

- **The user:** whoever uses a skill.
- **Task:** one thing a film needs made, such as a mouth chart or a lip-sync test; each is one template in one skill.
- **Workflow, prompt, and execution skills:** what a setup provides, as [prompt-roles.md](prompt-roles.md) describes.
- **Setup:** one place the skills run, such as Spumcake Studio or an agent with its own execution stack.
- **Role:** the named part of a prompt a skill fills, such as `references`.
- **Concept:** the show, short, or other work a style guide and its references belong to.
