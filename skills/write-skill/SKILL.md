---
name: write-skill
description: Write a new skill for Spumcake Agent, or rewrite an old one, with every part its category requires - its category and name, its front matter, what a good and a failed result are, what it needs by canonical name, its method, and its hand-back to project-requests - from docs/skill-categories.md, so every skill in a category covers its ground the same way. Use when the user asks for a new skill, or for a skill to be rewritten, split, or moved to another category. Not for changing a category itself, which the user decides.
---

# Writing a skill

A skill is a method for one kind of work, written so any agent carries it out the same way. Every skill in a category has the same parts, which [skill-categories.md](../../docs/skill-categories.md) gives; a skill written without them drifts from its neighbours, and its results come back in a shape `project-requests` cannot file or report.

A good skill does one category's work, says what a good and a failed result are, takes everything it needs by canonical name, and hands back exactly what its category returns. A failed one saves files itself, names a folder or a path, carries the work of two categories, or tells the agent what to say when it is done, which is `project-requests`' job.

## 1. Choose the category

From what the skill must produce, as the categories list it. When the work produces two kinds of thing, such as a document and the images made from it, write one skill for each and a `make` skill that plans them. Tell the user the category and why.

## 2. Name it

The category's word, then what it makes: `generate-keyframe`, `write-floor-plan`. Lowercase, joined by hyphens, British spelling. A `write` skill that builds a prompt for a language model ends in `-prompt`. Check the name against every skill's name in `skills/`. A new name waits for the user's yes before the skill is written.

## 3. Write it

Write `skills/<name>/SKILL.md` with, in this order:

1. **Front matter:** `name`, and a `description` saying what it makes, when to use it, and what it is not for, in one paragraph.
2. **What it is for:** a few sentences, then what a good result is and what a failed one is.
3. **What it needs:** each input by its canonical name, `<element>: <role>` for an artifact and `<element>: <fact>` for a fact, never a path or a folder.
4. **Its method:** numbered steps, with the user's yes before anything that costs money, a short test before a batch, and the category's own parts: a `generate` skill's prompt rules and templates; a `review` skill's checks and findings template; a `write` skill's sections; a `build` skill's script; a `make` skill's requests, in order.
5. **Hand back:** exactly what the category returns, as skill-categories.md gives it.

Put each template the skill fills in its own `templates/` folder, one per task. A `build` skill's script goes in its own `scripts/` folder; a script that belongs to one project goes in that project's pipeline instead.

Leave out: any folder, path, or file name of a project; saving, copying, or moving a file; a record or a map; what to tell the user when it is done; a model's name, price, or key, which the setup provides.

## 4. Check it

- Every part of step 3 is there, in order.
- `grep` the skill for `save`, `folder`, `renders/`, `record`, `film map`, and any path: each is a defect.
- Its hand-back matches its category.
- Add it to its category's row in skill-categories.md, to the README's table, and to the place it runs in [the pipeline](../../docs/pipeline.md).

## Hand back

The skill's folder, with its name and category, and the lines added to skill-categories.md, the README, and the pipeline, for the user to approve.
