---
name: refine-concept-art
description: Refine chosen concept art of a place into a believable one - a floor plan designed by a language model from what the place is, not from the concept's layout, drawn exactly; an exact perspective layout of the empty place from a chosen camera; the layout repainted in the concept's style; then the characters added in - so the concept's mood survives in a space that makes sense. Use when the user has chosen concept art whose mood works but whose space does not hold together, before a location's references are made. Not for exploring concepts, or for a subject's reference.
---

# Refine concept art

Concept art finds a mood: its colour, light, brushwork, and feeling. Its space cannot be trusted. An image model puts a sink in front of the door, or a counter where no one could walk. Everything later in a film, from the location's references to every keyframe, needs a place that holds together. This skill keeps the concept's mood and rebuilds its space from a believable plan.

A good refined concept looks like the concept in mood and paint, and makes sense as a place: a person could walk through it, every door and window leads somewhere, every light has a source, and every fixture is where that kind of place would put it. A failed one either drifts from the concept's mood, or keeps a layout the plan does not allow.

The concept's own layout is never copied. It is evidence of mood only.

## The models

- **The floor plan** comes from a language model, run on a prompt this skill builds.
- **The plan diagram and the layout** are drawn exactly from the plan, not generated: a top-down diagram, and a simple grey perspective view of the empty place from the camera. An image model cannot keep a plan's measurements.
- **The painted location** comes from an **image-edit model**: the layout as structure, the chosen concept art as a reference for its style.
- **The character pass** comes from the same kind of model: the painted location, with the characters' designs or references.

## Find the specifics

- **The workflow skill** of each image model the request names, or that the user chooses, says which way of running it takes structure and references, how many references it takes, and how to prompt it. **Its prompt skill** gives its syntax and limits.
- **The execution skill** that implements `refine-concept-art` in this setup runs the prompts and draws the plan and layout; when none does, the setup's renderer runs the prompts and the agent draws the plan and layout itself. The language model may be the agent itself, when the setup says so.

All come from the setup, as the [prompt roles](../../docs/prompt-roles.md) describe. If one is missing, say which and stop.

## What it needs

From the caller:

- the chosen concept art: one or more images whose mood the user wants kept;
- the premise and the brief: what the place is, and what happens there;
- the characters who appear, with their designs or reference sheets when they have them;
- the camera the concept is seen from, or the shot it is for;
- a folder for the plan, the drawings, the prompts, and the images.

Each step waits for the user's yes before the next. Every paid request waits for a yes to its plan: the model, the number of requests, and the cost. Every result is shown with the exact prompt sent.

Every image of a character who reads as a minor stays ordinary and everyday. Nothing is sexual or suggestive, in any step or prompt.

## 1. The floor plan

Build the prompt from [the floor plan prompt template](templates/floor-plan-prompt.md): what the place is, from the premise and the brief, and what must happen in it; [the floor plan template](templates/floor-plan.md) as the exact form of its answer. Send only the saved prompt, as a fresh request. Do not send the concept art; its layout is not evidence.

Check the answer before showing it:
- every wall, opening, fixture, and light has a position and a size in metres, on one grid;
- every door and window leads somewhere it names;
- the place works as that kind of place: people can walk between its parts, its working areas sit where its work is done, and its fixtures sit where that kind of place puts them;
- every light has a fixture and says what it lights;
- the action in the brief can happen where the plan puts it.

When a check fails, build a corrected prompt that says what was wrong, and run it again. Show the plan; the user's corrections win.

## 2. The plan diagram

Draw the approved plan exactly, top down, from its numbers: walls, openings, fixtures, lights, and a scale bar, each labelled. Draw the camera as a point with its direction and field of view. Show it to the user; a correction goes into the written plan, and the diagram is drawn again.

## 3. The layout

Place the camera from the concept or the shot: where it stands, its height, the direction it faces, and its lens. Draw the empty place exactly from the plan as seen by that camera: simple grey shapes for floor, walls, openings, and fixtures, each at its true position and height, with the horizon at the camera's height. No characters, texture, or light. This is what the painted location must follow.

Show the layout beside the concept. When the user wants the concept's framing, move the camera on the plan, not the walls.

## 4. The painted location

Fill [the painted location template](templates/painted-location.md): the layout as **structure**, and the chosen concept art as **references** for its style only. Make several candidates. Keep the prompt short: what the image is, that the layout's walls, openings, and fixtures stay exactly where they are, and that the concept's paint, colour, and light are kept, but not its layout. No characters.

Check each candidate against the layout and the plan: every wall, opening, and fixture where the plan puts it, nothing added that the plan does not have, and every light from a source the plan names. Report what moved. The user picks one.

## 5. The character pass

Fill [the character pass template](templates/character-pass.md): the chosen painted location as **structure**, then each character's design or base sheet as **references**, in order. Say where each character stands on the plan, what they do, and their pose and mood from the concept. Make several candidates.

Check each against the painted location: nothing in the place moved, each character at the plan's position and at a believable scale for that spot, and the light on them from the place's sources. The user picks one.

## Hand back

- the approved floor plan, written, and its diagram;
- the camera on the plan, and the layout drawn from it;
- the chosen painted location, empty, as the starting point for the location's references;
- the chosen refined concept, with the characters;
- every prompt sent, and what the user chose.
