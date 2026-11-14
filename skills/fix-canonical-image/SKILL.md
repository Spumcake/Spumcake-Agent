---
name: fix-canonical-image
description: Fix a generated image from its continuity review - run `review-continuity` on it, which finds what the image has that its canonical prompt or its pre-vis rules out and what came out wrong, then trace each finding to the pre-vis or the generation and fix it there: the pre-vis first, then the generation, by removals only. Run after any image is generated from a request, as part of that step, before it is approved or used to make anything else. Not for finding faults itself, which the continuity review does, nor for judging style or adding what was never asked for.
---

# Canonical cleanup

An image model gives back more and less than it was asked for. Some of that is welcome: a diner needs a world outside its windows, and a requested thing may come back in a style the model chose. What is not welcome is what its canonical prompt or its pre-vis rules out, and what came back wrong. Finding those is the continuity review's job (`review-continuity`); this skill takes its findings and fixes them the same way every time.

A good cleanup fixes every finding and changes nothing else. A failed one leaves an item wrong, changes something that was right, or "fixes" what the canonical prompt never asked for.

## The models

- **The findings** come from `review-continuity`.
- **The fix** comes from an **image-edit model**.

## Find the specifics

- **The workflow skill** of the image model the request names, or that the user chooses, says how many images it takes and how to run it. **Its prompt skill** gives its syntax.
- **The setup** says what a request costs.

All come from the setup, as the [prompt roles](../../docs/prompt-roles.md) describe. If one is missing, say which and stop. This skill builds one request per fix and hands them back; `project-requests` runs each with `scripts/request.py`, which sends it exactly as built.

## What it needs

- the generated image, by the request that made it;
- its canonical prompt: the text-to-image prompt the image descends from, as sent, however many image edits came after it, from that request's report with `request.py show`;
- its pre-vis, when it was made from one, such as `<place>: pre-vis <camera>`, and the place's other views (`<place>: view <wall>`), by canonical name from the pipeline's table, with what each shows.

The fixes are the agent's own work, made without asking the user. Cleanup is part of every step that makes an image: once the user has approved a step, its fixes run as part of it, each as its own request, without asking again. Ask only when a fix would change something the user chose, or would cost more than the step itself.

## 1. The review

Run `review-continuity` on the image, sending its canonical prompt and its pre-vis with its references, as that skill's checks for a generated image's own sources say. Its findings are the work list; this skill adds none of its own.

## 1a. Trace each finding

Work out where each finding comes from. It is your job to trace it, not the user's. Compare the image with every input it was made from: when the input already has the fault, such as a pre-vis that holds twelve stools where the prompt asks for minimal elements, it is a fix for the pre-vis; when the generation added or changed it, such as a menu board the pre-vis does not have, it is a fix for the generation. Then:

- **not in the pre-vis:** a fix for the generation: remove it;
- **not in the pre-vis but needed:** do not remove it; a fix for the pre-vis: add it, with its shape, size, and place taken from the image, and to the pre-vis's key. No new image is made for it;
- **malformed:** do not repaint it in place; list it, and let the square-on view of its wall, made from the pre-vis, show what it is;
- **texture on a form pass:** a fix for the generation: remove it, leaving each surface one plain colour.

Decide every fix yourself, from the canonical prompt: how much fewer, where, which way. Fill [the fix plan](templates/fix-plan.md).

## 2. Fixes for the pre-vis

When there is any fix for the pre-vis, return to the pre-vis first: one `build-previs` request with the change, which renders the camera again. Once it is approved and published, `pipeline.py touches --artifact "<place>: pre-vis <camera>"` lists every step built on it, starting with the place's primary canonical location, since every other image of the place is based on it; each runs again as its own request, by the same step that first made it. Review the new primary canonical location from step 1, then remake the images based on it. Fixes for the generation wait for that new image, since it may no longer need them.

## 3. Fixes for the generation

Fill [the cleanup template](templates/cleanup.md) as one image-edit request, with the generated image as its one reference, image 1, the image to correct. The prompt says what the image is, then lists each correction. Text fixes are for removing things, which works; counts and positions, such as the number of booths or the wall a door is on, do not change reliably by text, so fix them in the pre-vis and remake the image from it. Never inpaint: repainting a masked area changed little but surface materials and cost time and money. It describes nothing else, because the image carries it. The request asks for two candidates.

## 4. Check

`review-continuity` reviews each candidate again, as its own request, against the same canonical prompt and references; check that nothing else changed. Say plainly when a candidate shows no visible change. When an item is still wrong, fix it again once, and list what is still wrong after that. The user chooses between the candidates; the chosen one is published by `project-pipeline` in place of the generated one, and the other is never used as an input again. When the user prefers what the generation did over the pre-vis, the fix is a `build-previs` request that changes the pre-vis to match the image instead, so every later image of the place agrees with it.

## Hand back

One request per fix, at the source of its error, in the order to run them, with the fix plan that traces each:

- **for the pre-vis:** one `build-previs` request with every change to the pre-vis and its key, each new and needed object added and each unwanted one removed; then the steps `pipeline.py touches` lists, each to run again as its own request;
- **for the generation:** one image-edit request: the endpoint kind, image edit; the prompt from [the cleanup template](templates/cleanup.md), its corrections all removals; and its one reference, the generated image, image 1, the image to correct; two candidates;
- the malformed objects, each with the wall whose square-on view will show it.
