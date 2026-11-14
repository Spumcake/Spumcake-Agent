---
name: write-staging-plan
description: Write a place's staging plan, its floor plan from its pre-vis layout's numbers - every wall, every door and opening named for what it is and where it leads, every fixture, every camera with what lies left, centre, and right in its frame, and each character's marks - as the place's one home for where everything is and what each thing is called, and hand back each of those as a canonical fact, so every prompt that places or directs a character takes them from the pipeline's table. Use once a place's pre-vis views are approved, and again when the layout changes or the timing reference adds marks. Not for building or rendering the mock-up (build-previs).
---

# The floor plan

A floor plan says where everything in a place is and what each thing is called, once. Every skill that places or directs a character reads it first, and every prompt calls each thing by its name here. When positions live only in a builder's code, they are described in words step by step, and the words drift: several doors each called "the door", a character's place re-invented in every prompt, and his looks aimed at different doors from frame to frame.

A good floor plan names every door for what it is and where it leads, so no prompt ever needs to say "the door"; gives each camera's frame in room terms, what is left, centre, and right; and states each fact once, so each becomes one fact in the pipeline's table. A failed one leaves a door unnamed, describes a frame without saying which side a named thing is on, or holds a position the layout's numbers do not.

## What it needs

- the place's layout and key (`<place>: pre-vis layout`), with every number;
- each camera's position, direction, and lens (`<place>: pre-vis cameras`), and the approved renders from each, with what is in each frame;
- the timing reference's blocking (`<film>: timing reference`), once it exists, for each character's marks.

## 1. Write it

Fill [the floor plan template](templates/floor-plan.md) from the layout's numbers, never from an image: the room and its grid, each wall and what it holds, each door and opening with the wall it is on, where along it, where it leads, which way it opens, and who uses it in the story; each fixture; each camera, and what lies on the left, in the middle, and on the right of its frame; and each character's marks, in room terms, never frame terms. Name each door by what it is, "the front door", "the kitchen door", "the restroom door", and say for any door a story uses which one it is.

## 2. Draw it

Draw the plan from above, from the same numbers, every wall, door, fixture, and camera labelled by its name, as a build with the place's builder.

## 3. Check it

Every number in the plan is in the layout; every named thing in the key has its name in the plan; every door has a name that no other door shares; and each camera's left, centre, and right agree with its render's frame. Show the user any disagreement.

## Hand back

To `project-library`, which files it into `prompts/resources/` as canon; it is the agent's own writing, not a request:

- the floor plan, as a draft document, and the build for its drawing;
- each fact it settles, by `<element>: <fact>`, for `project-pipeline` to publish with the plan as the artifact that settles it: for each door, `<door>: wall`, `<door>: leads to`, and `<door>: opens`; for each camera and each named thing in its frame, `<thing>: side in the <camera> frame`, as left, centre, right, or behind the camera; and for each character's mark, `<character>, <moment>: mark`, `: faces`, and `: looks at`.
