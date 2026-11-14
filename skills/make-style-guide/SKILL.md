---
name: make-style-guide
description: Plan a concept's style guide as requests - the written rules of its look (shapes, line, proportion, colour, light, texture, and what to avoid), drafted by a language model from a prompt this skill builds, then the images that show them (style frames to choose from, then a style sheet) - from the user's words and, when they have them, their own artwork, each request run by project-requests as its own cycle, with the user's approval between them. Use when the user asks for a style guide, a visual identity guide, an art direction, or "the look" of a show, a short, or any concept; it comes before subjects, locations, or boards are designed, since they all follow it. Not for one subject's reference or a colour script.
---

# Style guide

A style guide fixes how everything in a concept looks, so every later image, from a subject's sheet to a board to a shot, can be made and judged against it. It has two halves that must agree: the **written rules**, which a prompt can quote and the user can check against; and the **images**, which show what the words cannot. This skill plans both as requests, says what each request needs and how its prompt is built, and runs none of them: [project-requests](../project-requests/SKILL.md) runs each as its own cycle, and the user approves each before the next is built. The images the user approves become the concept's style references.

A good style guide has rules concrete enough to check a picture against, each drawn from the user's artwork or marked *proposed*, and a style sheet that matches the chosen frame and the rules in line, shape, palette, and light. A failed one has rules too vague to check, such as "bold lines", a sheet made from text alone that drifts from what the user chose, or a look that replaces the user's own artwork with a model's guess.

## The models

- **The written rules** come from a language model, run on a prompt this skill builds. The language model may be the agent itself, when the setup says so.
- **Style frames** come from an image model. When the user gives their own artwork, use an **image-edit model** with that artwork as references, so the style is theirs; the user's own art is the strongest source of a look, and is never replaced by a model's guess. With no artwork, use a **text-to-image model**.
- **The style sheet** always comes from an **image-edit model**, sent with the chosen style frame, or with the user's artwork when it settled the look. Never make the sheet from text alone: it would drift from what the user chose.

## Find the specifics

- **The workflow skill** of each model the request names, or that the user chooses, says which way of running it takes text alone and which takes references, how many references it takes, and the sizes it makes. **Its prompt skill** gives its syntax and limits.
- **The cost** of each request comes from the setup, and waits for the user's yes before anything is paid.

Each request is built here and run by `project-requests` with `scripts/request.py`, which sends it exactly as built. The specifics come from the setup, as the [prompt roles](../../docs/prompt-roles.md) describe. If one is missing, say which and stop.

## What it needs

Each input by its canonical name, from the pipeline's table:

- the user's request, in their words;
- the concept's brief, when there is one (`<concept>: visual identity brief`);
- the user's own artwork, when there is any, each piece once published (`<concept>: artwork <n>`).

Each request waits for the user's yes to the plan before it runs, and each paid request for a yes to its model, its number of calls, and its cost. Each request is built only from the latest approved results of the requests before it.

Characters who read as minors are kept as the [prompt roles](../../docs/prompt-roles.md) say.

## Image prompts

These rules are for the style sheet, which must hold exactly to the chosen frame. Style frames use the concept context template instead, as request 2 says.

Every image prompt here says what the picture is for, then what is in it, then how it looks. With reference images, it also says what each reference is for, because the model cannot guess which parts to keep. Write it in this order, for any model:

1. **What the image is:** one line naming the kind of image and its use, such as "a style frame for an animated production" or "a style sheet". The kind sets the model's expectations for layout and finish.
2. **The subject:** who or what, doing what, where. Describe characters by what they look like or by role ("the girl in the red cap"), never by a real person's name.
3. **The layout,** when the image is a page: its shape, its panels in reading order, what each panel holds, and its labels. Say the labels' exact words in quotes, and keep them few and short; models misspell long text.
4. **The look:** shapes and proportion, line, colour, light and shadow, and texture, in concrete terms an image can be checked against, such as "thick, even outer lines; flat colour; one soft shadow tone". Quote the written rules here rather than rewording them: each is written as its fact, `{{<concept>: palette}}`, filled from canon, never typed in by hand.
5. **The references,** when there are any: what each one is, in the order they are sent, and what to keep from it, such as "the first attached image is the chosen style frame: match its line and colour exactly". Say what must not change, and that the model must not switch to another rendering style.
6. **What to leave out:** text, logos, borders, extra figures, or anything the request rules out. Say it plainly, as a sentence; a model reads "no text" better than a list of banned words.

Keep each part to a sentence or a few short lines, as `prompt-image` says; a page with many panels needs each panel to be short. Leave out what the model ignores, as its prompt skill says.

Text to image has nothing to hold it to a look but the words, so the look carries all of it. An edit with references holds the style from the images, so the references carry most of it, and the look only says what they do not show. When the request has artwork, never write a frame as text to image instead: it would drift from the artwork.

Put each part into its field in the model's syntax, as its prompt skill says, and name the references, in order, as the request's inputs, by the [prompt roles](../../docs/prompt-roles.md).

## The plan

Show the user the plan before anything runs: each request below, in order, with its category, its endpoint, what it needs, and its estimated cost, and where they approve between them. Leave out request 2 when the user's artwork already settles the look.

### Request 1: the written rules (write)

A language-model request, built from [the rules prompt template](templates/rules-prompt.md): the user's request, the brief, a description of each piece of artwork, or the artwork itself as references when the language model takes images, and [the style guide template](templates/style-guide.md) as the exact form of its answer.

Check the answer before showing it: every section of the template is filled; each rule names the artwork it is drawn from, or is marked *proposed*; and each rule is concrete enough to check an image against, such as "thick, even outer lines; thin inner lines; no hatching" rather than "bold lines". When it is not, build a corrected prompt as the [prompt roles](../../docs/prompt-roles.md) say, as a new request.

**The user approves.** Their corrections win; a correction the user writes is made in the rules directly. The approved rules are published by `project-pipeline` as `<concept>: style guide`, with the facts they settle, one per section of the template: `<concept>: look in one sentence`, `<concept>: shapes`, `<concept>: proportions`, `<concept>: silhouettes`, `<concept>: outer lines`, `<concept>: inner lines`, `<concept>: lines never`, `<concept>: palette`, `<concept>: colour fill`, `<concept>: colour and mood`, `<concept>: lighting`, `<concept>: shadows`, `<concept>: texture`, `<concept>: environments`, and `<concept>: never`.

### Request 2: style frames (generate)

Unless the user's artwork already settles the look, the style frames: concept illustrations of one small moment of the concept, to find its mood, not replicas of the final picture.

**Style frames are made as `generate-concept-design` makes its candidates:** from its concept context template, word for word, with only a premise and a purpose added. **Text gives context only where no image does,** as the [prompt roles](../../docs/prompt-roles.md) say.

- Fill [the style frame template](templates/style-frame.md): the premise from the brief, in a few words, and the purpose "16:9 concept illustration".
- With the user's artwork, an image-edit request, sent each piece by its canonical artifact, with its role; with none, a text-to-image request.
- Plan the candidates, with their count and cost. The candidates are shown together with the exact prompt sent.
- Report honestly what each candidate does with the premise; never judge the look for the user.

**The user chooses** a frame, asks for a mix, or asks for more candidates, each a new request; never choose for them. The chosen frame is published by `project-pipeline` as `<concept>: style frame`; the frames not chosen are never used as inputs again.

### Request 3: the rules revised (write)

When the chosen frame differs from the approved rules, a language-model request like request 1, sent the chosen frame and the approved rules, to bring the rules to what the user chose. **The user approves**, and the revised rules and their facts are published again by `project-pipeline`. When the frame and the rules already agree, this request is left out.

### Request 4: the style sheet (generate)

An image-edit request: one **style sheet** from the chosen frame and the final rules, a single page that shows the look's parts side by side, for every later prompt to be sent with.

- Fill [the style sheet template](templates/style-sheet.md). Each look placeholder is written as the fact it quotes, such as `{{palette}}` as `{{<concept>: palette}}`, filled from canon.
- Send `<concept>: style frame` first, then each piece of the user's artwork, each with its role. When the artwork settled the look and no frame was made, send the artwork alone.
- Inspect it against the rules and the chosen frame: line weight, shapes, palette, and light. A new version is a new paid request, and needs the user's yes.

**The user approves.** The style sheet is published by `project-pipeline` as `<concept>: style sheet`, made from the style frame and the rules. A rejected sheet is never used as an input again.

Every later task in the concept, a subject's reference, a location, a board, or a shot, is sent `<concept>: style sheet`; its prompt quotes a written rule, as its fact, only where no image it sends already shows it.

## Hand back

Hand back to [project-requests](../project-requests/SKILL.md) the plan, in order:

1. **the written rules,** a write request: the language model's endpoint, the prompt from the rules prompt template, the artwork by canonical artifact, and the facts the answer settles; then the user's approval;
2. **the style frames,** a generate request in the manner of `generate-concept-design`, unless the user's artwork settles the look: the endpoint kind, the prompt from the style frame template, and the artwork by canonical artifact with its role; then the user's choice;
3. **the rules revised,** a write request, only when the chosen frame differs from the rules; then the user's approval;
4. **the style sheet,** a generate request: the image-edit endpoint, the prompt from the style sheet template naming canon, `{{<concept>: <fact>}}`, and `<concept>: style frame`, then the artwork, each with its role; then the user's approval.

Each request is built when the approvals before it are in, from what was published.
