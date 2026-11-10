---
name: canonical-cleanup
description: Audit a generated image against its canonical prompt - the text-to-image prompt the image descends from - list what the image has that the prompt rules out, and what the prompt asked for that came out wrong, and fix them itself: the pre-vis first when the fault is in it, then the generation. Use after any image is generated from a request, before it is approved or used to make anything else. Not for judging style, adding what was never asked for, or checking one image against another's continuity.
---

# Canonical cleanup

An image model gives back more and less than it was asked for. Some of that is welcome: a diner needs a world outside its windows, and the ordinary things a diner has; a requested thing may come back in a style the model chose. What is not welcome is what the canonical prompt, the text-to-image prompt the image descends from, rules out, such as a crowd of elements where it asked for minimal ones, and what it asked for that came back wrong. This skill finds those, and fixes them the same way every time.

A good cleanup fixes every finding and changes nothing else. A failed one leaves an item wrong, changes something that was right, or "fixes" what the canonical prompt never asked for.

## The models

- **The audit** is the agent's own comparison, or a vision-capable language model's when the setup gives one.
- **The fix** comes from an **image-edit model**.

## Find the specifics

- **The workflow skill** of the image model the request names, or that the user chooses, says how many images it takes and how to run it. **Its prompt skill** gives its syntax.
- **The execution skill** that implements `canonical-cleanup` in this setup runs the edit; when none does, the setup's renderer. It says what a request costs and where its output lands.

All come from the setup, as the [prompt roles](../../docs/prompt-roles.md) describe. If one is missing, say which and stop.

## What it needs

From the caller:

- the generated image;
- its canonical prompt: the text-to-image prompt the image descends from, as sent, however many image edits came after it;
- a folder for the audit, the prompt, and the images.

The audit and the fixes are the agent's own work, made without asking the user. Every paid request still waits for the user's yes to its plan: the model, the number of requests, and the cost.

## 1. The audit

Read the canonical prompt line by line. For each line, check the image: what it has that the line rules out, such as many elements where the prompt asks for minimal ones, or hard reflections where it asks for soft diffuse light; and what the line asks for that came out wrong. Quote the line with each finding.

Then work out where each finding comes from. It is your job to trace it, not the user's. Compare the image with every input it was made from, such as the pre-vis: when the input already has the fault, such as a pre-vis that holds twelve stools and four booths where the prompt asks for minimal elements, or a pre-vis camera that centres the view where the prompt asks for the rule of thirds, it is a fix for the pre-vis. When the input does not have it and the generation added or changed it, such as a menu board the pre-vis does not have, or hard reflections, it is a fix for the generation. File every finding under one of the two, with its reason. Fill [the audit template](templates/audit.md).

The canonical prompt is the only measure. What it does not say, such as a number of stools, is not a finding.

When the image was made from a pre-vis, the pre-vis is also its inventory. Anything in the image that the pre-vis does not represent is a fix for the generation: remove it. The only exception is the world seen through the windows, which the place needs to exist somewhere.

Then look at every visible object, one by one:

- **Malformed:** an object that does not read clearly as any one thing, or a thing formed wrongly, such as a partition that could be a door, a window, or a cabinet. Do not repaint it in place. Record it, and let the square-on views of its wall, made from the pre-vis, show what it is.
- **New and needed:** an object the pre-vis does not hold that clearly reads as a thing, and that the place needs, such as a door the place must have. Do not remove it. File it as a fix for the pre-vis: add it to the pre-vis, with its shape, size, and place taken from the image, and to the pre-vis key, so every later image of the place has its geometry. No new image is made for it.

On a form pass, a viewport view of the element with no textures, texture that shows through is a fix for the generation: lettering, and patterns on floors, walls, or upholstery, which are surfaces rather than objects. Remove them with the cleanup template, leaving each surface one plain colour.

These are not findings:

- the world seen through the windows;
- a style the model chose for something that was asked for;
- a thing asked for that is right.

Decide every fix yourself, from the canonical prompt: how much fewer, where, which way. Do not ask the user to choose. Show the audit with the fixes you made.

## 1b. Across the views

When a place has several views made from its primary canonical location, compare them with each other as well: the same objects, in the same places, the same kind. Address only major inconsistencies, such as an object that appears twice, goes missing, or changes kind between views, like a second clock, or a plain door that gains a round window. Small ones stay; removing every one needs better pre-vis assets than simple shapes. Fix each major one in this order, cheapest first:

1. choose the candidate that already has it right;
2. remove an object the generation added, with [the cleanup template](templates/cleanup.md);
3. when the images agree with each other against the pre-vis, change the pre-vis to match them.

## 2. Fixes for the pre-vis

When there is any fix for the pre-vis, return to the pre-vis first: change it, render the camera again, and show it. Then recreate the place's primary canonical location from the corrected pre-vis, by the same step that first made it, since every other image of the place is based on it. Audit the new primary canonical location from step 1, then remake the images based on it. Fixes for the generation wait for that new image, since it may no longer need them.

## 3. Fixes for the generation

Fill [the cleanup template](templates/cleanup.md) and send the generated image alone. The prompt says what the image is, then lists each correction: what to remove, or what is wrong and what it should be, as the canonical prompt asks. It describes nothing else, because the image carries it. Make two candidates.

## 4. Check

Audit each candidate against the same canonical prompt, as in step 1, and check that nothing else changed. Say plainly when a candidate shows no visible change. Show both with the audit. When an item is still wrong, fix it again once, and report what is still wrong after that. When the user prefers what the generation did over the pre-vis, change the pre-vis to match the image instead, so every later image of the place agrees with it.

## Hand back

- the audit, with each fix filed for the pre-vis or the generation, and what was done;
- the corrected pre-vis, when it was changed, with every new and needed object added to it and its key;
- the malformed objects, each with the wall whose square-on view will show it;
- the major inconsistencies across the views, and how each was fixed;
- the cleaned image the user chooses, which replaces the generated one for everything after it;
- every prompt and image sent.
