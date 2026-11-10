---
name: refine-concept-art
description: Make a recurring place canonical, one step at a time, so every later image of it holds together - research, then a pre-vis, then the primary canonical location painted from it, then canonical cleanup, then the views of the place - each step made only from the latest approved result of the one before. Use when the film's breakdown names a recurring place, before any character or prop is staged in it, and whenever a place's images stop agreeing with each other. Not for exploring a film's look, or for a character or a prop.
---

# Refine concept art

A film's places must hold together from shot to shot: the same door on the same wall, the same counter with the same stools, from every camera. An image model alone cannot keep that. This skill takes a place through the steps that do, in order, and hands on a place that is canonical: a primary canonical location every other image of it is based on, and views of it from every side the film needs.

A good result reads as that kind of place in every view, holds every element the research found, and shows the same place from each camera. A failed one invents what the research does not show, drifts between views, or was built on a result that was never approved.

## The rules of the sequence

- One step at a time. Each step is made only from the latest approved results of the steps before it; a rejected round is never an input to anything.
- When a step fails, the skill that made it is fixed, and the step is run again. A lesson goes into the skill, not around it.
- No characters until the place is canonical. They are staged into its views afterwards.
- Every paid request waits for the user's yes to its plan, and every result is shown with the whole prompt, every image sent, and their full paths, as the [prompt roles](../../docs/prompt-roles.md) say.

## What it needs

From the caller:

- the place, by the name the script uses, and what the film's breakdown says it must hold and which shots it is in;
- the period and setting of the film;
- the film's style guide, when there is one;
- the project's folder, where each step keeps its own.

## 1. Research

Run `research-references` for the place: its layout and usual sizes, how such a place is best shot, and a photograph, in the film's period, of every element it holds. An element without a photograph is not yet researched. The user approves the board and the photographs.

## 2. Pre-vis

Run `create-previs` from the approved research: the layout, the mock-up with its key, and one good shot. The user approves the shot.

## 3. The primary canonical location

Run `create-concept-art` for the primary canonical location: the grey shot, the research photographs of the place's elements, the names from the key, and the concept context template for the place. The user chooses one.

## 4. Canonical cleanup

Run `canonical-cleanup` on the chosen image, against its canonical prompt and the pre-vis. Fixes for the pre-vis go back to step 2, and the primary canonical location is made again from the corrected shot. The user approves the cleaned image as the primary canonical location.

## 5. The views of the place

Run `create-previs` for the views: a camera square-on to each wall, and each shot the concept art needs. Make each view from the primary canonical location with `create-concept-art`'s new camera template. Then run `canonical-cleanup` across the views, fixing only major inconsistencies. The user chooses each view.

## Hand back

- the approved research board and its photographs;
- the pre-vis: its layout, key, good shot, and views;
- the primary canonical location, and each view of the place, named by its camera;
- every audit, prompt, and image sent, and what the user chose at each step.

The place is then ready for its characters and props to be staged into the views its shots use.
