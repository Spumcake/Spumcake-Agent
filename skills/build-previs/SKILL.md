---
name: build-previs
description: Mock up a place in simple 3D - its layout worked out from its research, each piece a recognisable shape built from its research photograph, with a key naming each piece - and render it in grey from the cameras the place needs - one good shot to paint the primary canonical location from, a view square-on to each wall, each shot the concept art needs, and any new camera the user asks for. Use once a recurring place's research is done, before any image of the place is made, and again whenever the place's images show the mock-up needs changing. Not for placing characters, designing the place's look, or choosing a scene's cameras from the story.
---

# Pre-vis

A pre-vis mocks up a place: built simply in 3D, each piece at a believable position and size, and shaped so it reads as what it is. An image model sent its shot sees where everything is and what it is, and paints its own picture of the place, guessing as little as possible. Every image of the place starts from one of its shots.

A good pre-vis reads as that kind of place from every camera: each piece is a shape that says what it is, sits where such a place puts it, and was built from a photograph in the research. A failed one hands the model a box that could be anything, holds a piece no photograph shows, or picks a camera from which nobody can tell what the place is.

Keep to the place. No characters and no lighting: those come later, from the story.

As the user set on 2026-11-15, after Last order, a pre-vis is built to the approved concept art's staging, not only to the research: its layout puts each piece where the art puts it, and its one good shot takes the art's camera, square-on to the scene with a long lens where the art is staged planimetrically. Last order's pre-vis came first, before any concept art, and its deep, diagonal staging fixed the canon; the planimetric concept art painted later read better, and came too late.

Each camera's render is the structure every image from that camera is made from: a canonical view, a layout, a plate, a final frame. One camera stays one camera, checked by laying its render's edges over each image made from it.

## The builder

The mock-up is built by a script, from the layout's numbers, never by an image model, which cannot keep measurements. The script belongs to the place: it is a shared resource in `prompts/resources/`, so the chain can run it again whenever the layout changes. Until the place has a scene file, the builder renders itself. Each run is a build, not a request: `project-library` runs it with `request.py build`, which files every render into `prompts/resources/`; for each render, the script also writes what is in its frame, as JSON: the camera, and each named piece by its key's name, with its box in the frame and whether it lies left, centre, or right.

## The scene file

A place's scene file is its geometry, in a form any 3D tool reads: one glTF 2.0 binary (`.glb`) per builder version, holding every object the builder makes, named as the builder names it and grouped as it groups them, its cameras with their exact positions, targets, and fields of view, the front door hinged with its swing as an animation, and the builder's looks as data. Once a place has one, it is the place's only geometry: every render, view, and plan is made from it, and a setup's 3D view shows it. As the user set on 2026-11-16, with Studio 0.15's scene contract.

[scripts/export-scene.py](scripts/export-scene.py) makes it from a builder, and changes nothing: it runs the builder's source only up to its render marker, in a process of its own, takes the rest of what it needs by parsing the source, never by retyping it, and renders nothing. A builder may come from git history, as `git:<commit>:<path>`. File what it makes with `request.py build "python3 <export-scene.py> <builder> <out.glb> --canon pipeline/<n>/canon.sql" <out.glb> --name <place>-scene-<builder time> --from <builder>`, so its record names the builder, and `request.py show` traces the scene file to it. Name each render this builder made with `--reference <camera>=<file>`, so a camera links only a render of its own geometry; the camera's published canon artifact is named either way. `export-scene.py --missing` lists the builders that have no scene file yet.

## Rendering from the scene file

Once a place has a scene file, every new render comes from it, and a builder is never run again for new work. [scripts/render-scene.py](scripts/render-scene.py) renders it with `spumcake-render`, a program this skill needs, as the [setup's prerequisites](../../docs/setup.md) list:

```text
request.py build "python3 <build-previs>/scripts/render-scene.py <scene.glb> <out.png> --camera <camera> --look grey|coded|simple [--size <w>x<h>] [--time <seconds>]" <out.png> <out.png>.record.json --name <place>-<camera>-<look> --from <scene.glb>
```

It files the picture and its in-frame record, in the form the builders wrote, with every group of objects by the scene's own label, its box, and whether it lies left, centre, or right. The record is inside the picture too, naming the program's version and the scene file it was made from. The size is the camera's own unless `--size` gives one; `--time` places the scene's animation, such as the front door part-way through its swing. A render from a camera matches the builder's published render from it within the scene contract's bounds. When the program is missing, older than the release the prerequisites name, or finds no graphics device, the script says which and renders nothing.

## What it needs

From the caller:

- the place's research (`<place>: research`): its layout, the parts in order with their usual sizes, and a photograph of each element the place holds;
- what the place must hold and which shots it is in, from the film's breakdown (`<film>: breakdown`), when there is one;
- the film's aspect ratio (`<film>: aspect ratio`); 16:9 when nothing says.

## 1. The layout

Work out the place's layout from its research: the room's size, each wall's doors and windows, each door named for what it is and where it leads, such as "the front door" or "the restroom door", with which way it opens, and each element's position and size in metres, on one grid, where that kind of place puts it. Hold everything the place must hold, and nothing it does not need. Draw it from above, labelled, and show it. The user's corrections win. Keep the numbers: the mock-up is built from them.

## 2. Build the mock-up

Build every wall with its openings, every fixture, and every light fitting from the layout's numbers. Give each a simple shape that reads as what it is, taken from its photograph in the research: a stool as a round seat on a post, a lamp as a shade on a cord, a booth as a bench, a back, and a table. A box that could be anything is a guess handed to the image model. Compare the finished mock-up against the research photographs, element by element, and add what the place holds but the mock-up lacks. Keep a key that names each element and the photograph it was built from.

Render two versions of every shot. For the user, colour-code each kind of thing, so the parts are told apart at a glance: the walls and the floor in two plain neutral tones, and each common kind of thing in its own flat colour, such as seating in one colour, counters in another, tables in a third, working equipment in a fourth, windows and doors dark, and light fittings in yellow; label each piece by its name in the key. For the image model, render the same shot in plain greys, so the mock-up's colours do not carry into the painting. Shade each colour lighter on top and darker on the sides turned away. Check the mock-up against the layout: every number used, nothing added.

## 3. One good shot

Place one camera where the approved concept art shows the place, or, for a place no concept art shows, where the research says this kind of place is best shown, so the shot shows as much of the place as reads clearly. Render it at the film's aspect ratio. Show it with the camera's position marked on the layout, and its reason in a sentence. The user approves it, or asks for the camera moved. The primary canonical location is painted from this shot.

## 4. The views of the place

Once the place's primary canonical location is approved, place a camera square-on to each wall, facing it straight, framed so every object along that wall reads clearly. Place no other camera unless the user asks for it and approves it: the one good shot stays the place's canonical angle. Render each in grey and show them all, marked on the layout, with how each camera sits relative to the original one. Each becomes a view of the place, made from the primary canonical location.

## 5. A new camera, when asked

When the user wants an approved image of the place seen from another angle, place a further camera on the same mock-up, near enough to the original camera that the place is still recognisable from it, and render it in grey. Show it beside the original shot, both marked on the layout, with how far it moved and turned from the original. The user approves it, or asks for it moved.

## 6. Changes from the place's images

When the place's images show the mock-up needs changing, such as an object the place needs that the mock-up lacks, or something the user prefers where an image put it, change the layout and the mock-up to match, add it to the key, and render every camera again, so every later image of the place agrees.

When a place goes into production, its neutral views carry enough to rebuild each object as a 3D model, with a 3D generative model or modelling by hand, and place them in a better pre-vis; then every later view keeps the place exactly. Simple shapes are enough until then.

## 7. The floor plan

Once the views are approved, the place's floor plan is written from the layout's numbers with `write-staging-plan`: the one home for where everything is and what each thing is called.

## 8. A staging floor plan for each moment

Before any frame of a moment is made, draw its staging floor plan with [scripts/staging-floor-plan.py](scripts/staging-floor-plan.py): the place from above, from the builder's exported geometry (`<builder> <folder> --geometry`); the shot's camera and the edges of its frame, labelled left and right as the camera sees them; and each character's mark, the way their body faces, and their look, drawn to the named thing they look at, which is shown in red. Every position and look comes from the canonical facts, `<character>: mark position`, `<character>: faces`, and `<character>, <moment>: looks at` and `: head turn`, written into the step's command as `{{<element>: <fact>}}`, so a changed fact redraws the plan. The caption names no file. The user approves it, and `project-pipeline` publishes it as `<moment>: staging floor plan`; no keyframe of the moment is made before that.

## Hand back

To `project-library`, as a build:

- the builder's command, and the files it makes: the layout drawing from above, with every camera marked; the key, each element named with the photograph it was built from; each shot and view, in plain greys for the model and colour-coded and labelled for the user; and, for each render, what is in its frame;
- each camera's position, height, direction, and lens, with its reason or its move from the original camera, for the user's approval;
- the layout's numbers, which `write-staging-plan` writes the floor plan from;
- for each moment, its staging floor plan, for the user's approval before any frame of the moment.
