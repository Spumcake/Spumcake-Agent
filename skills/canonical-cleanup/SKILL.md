---
name: canonical-cleanup
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
- **The execution skill** that implements `canonical-cleanup` in this setup runs the edit; when none does, the setup's renderer. It says what a request costs and where its output lands.

All come from the setup, as the [prompt roles](../../docs/prompt-roles.md) describe. If one is missing, say which and stop.

## What it needs

From the caller:

- the generated image;
- its canonical prompt: the text-to-image prompt the image descends from, as sent, however many image edits came after it;
- its pre-vis, when it was made from one, and the place's other views;
- a folder for the review, the fix plan, the prompts, and the images.

The fixes are the agent's own work, made without asking the user. Cleanup is part of every step that makes an image: once the user has approved a step, run its cleanup edits as part of it, without asking again, and report what was found, what was fixed, the prompts, the images sent, and the cost afterwards. Ask only when a fix would change something the user chose, or would cost more than the step itself.

## 1. The review

Run `review-continuity` on the image, sending its canonical prompt and its pre-vis with its references, as that skill's checks for a generated image's own sources say. Its findings are the work list; this skill adds none of its own.

## 1a. Trace each finding

Work out where each finding comes from. It is your job to trace it, not the user's. Compare the image with every input it was made from: when the input already has the fault, such as a pre-vis that holds twelve stools where the prompt asks for minimal elements, it is a fix for the pre-vis; when the generation added or changed it, such as a menu board the pre-vis does not have, it is a fix for the generation. Then:

- **not in the pre-vis:** a fix for the generation: remove it;
- **not in the pre-vis but needed:** do not remove it; a fix for the pre-vis: add it, with its shape, size, and place taken from the image, and to the pre-vis key. No new image is made for it;
- **malformed:** do not repaint it in place; record it, and let the square-on view of its wall, made from the pre-vis, show what it is;
- **texture on a form pass:** a fix for the generation: remove it, leaving each surface one plain colour.

Decide every fix yourself, from the canonical prompt: how much fewer, where, which way. Fill [the fix plan](templates/fix-plan.md).

## 2. Fixes for the pre-vis

When there is any fix for the pre-vis, return to the pre-vis first: change it, render the camera again, and show it. Then recreate the place's primary canonical location from the corrected pre-vis, by the same step that first made it, since every other image of the place is based on it. Review the new primary canonical location from step 1, then remake the images based on it. Fixes for the generation wait for that new image, since it may no longer need them.

## 3. Fixes for the generation

Fill [the cleanup template](templates/cleanup.md) and send the generated image alone. The prompt says what the image is, then lists each correction. Text fixes are for removing things, which works; counts and positions, such as the number of booths or the wall a door is on, do not change reliably by text, so fix them in the pre-vis and remake the image from it. Never inpaint: repainting a masked area changed little but surface materials and cost time and money. It describes nothing else, because the image carries it. Make two candidates.

## 4. Check

Run `review-continuity` on each candidate again, against the same canonical prompt and references, and check that nothing else changed. Say plainly when a candidate shows no visible change. Show both with the review and the fix plan. When an item is still wrong, fix it again once, and report what is still wrong after that. When the user prefers what the generation did over the pre-vis, change the pre-vis to match the image instead, so every later image of the place agrees with it.

## Hand back

- the continuity review, and the fix plan, with each fix filed for the pre-vis or the generation, and what was done;
- the corrected pre-vis, when it was changed, with every new and needed object added to it and its key;
- the malformed objects, each with the wall whose square-on view will show it;
- the cleaned image the user chooses, which replaces the generated one for everything after it;
- every prompt and image sent.
