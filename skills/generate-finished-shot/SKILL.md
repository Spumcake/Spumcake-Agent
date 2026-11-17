---
name: generate-finished-shot
description: Finish an approved final shot for delivery - retime it to a higher frame rate and upscale it to the delivery size, each with a video model that enhances without inventing new content, each its own request after the user's yes to its plan and cost, each checked frame by frame against the take it was made from - then hand the finished picture to the mix and the delivery. Use when the user asks to retime, interpolate, or upscale a finished shot, or for a 60 fps, 4K, or delivery version of it. Not for rendering the final look itself (the setup's final-animation skill), the mix (build-animatic), or delivery (project-output).
---

# Finished shot

As the user decided on 2026-11-17, finishing belongs to Spumcake-Skills, and to no one model. A finished shot is an approved final shot made ready to deliver: retimed to the frame rate the film is shown at, and upscaled to the size it is delivered at, with nothing in it changed but its smoothness and its detail. The finished mix is laid back over it after, and it is delivered from there.

A good finished shot holds every frame of the take it was made from: the same drawing, the same faces, the same timing, the same frame, only smoother and sharper. A failed one invents what the take did not hold, such as a new mouth shape between two frames, a smeared hand on a fast move, a texture on a flat wall, or a face that is no longer the character's; or it crops, stretches, or shifts the frame; or it changes the shot's length.

Last order's retime and upscale reports, of 2026-11-15, name `create-final-animation`, the setup's final-animation skill that did this work before it moved here. They are this skill's work; `project-requests`' `models.json` names their models.

## The models and the route

Two requests, one after the other, each from a video model that enhances a video without inventing new content, such as Topaz on fal:

- **The retime:** a frame-interpolation model makes new frames between the take's own, to the target frame rate, at the same length: Topaz Interpolate Video (`topaz/interpolate/video`), its model Apollo, as Last order used it, 24 to 60 fps.
- **The upscale:** a precision upscaling model enlarges the retimed take by the factor that takes it to the delivery width, keeping its whole frame: Topaz Upscale Video Precision (`topaz/upscale/video/precision`), its model Gaia CG for computer graphics, as Last order used it, 1344 to 3840 wide, a factor of 3840 ÷ 1344 = 2.857142857.

The models this skill can use are in its [`models.json`](models.json); the model's workflow skill gives its fields, settings, and limits. The retime comes first, since the upscale then works on every frame the film shows and is the dearer request. Each is its own request, on the user's yes to its plan; this skill builds them and hands them back, and [project-requests](../project-requests/SKILL.md) runs each with `scripts/request.py`, which sends it exactly as built.

What each costs comes from the setup, and nothing is paid before the user's yes. Show each request's cost apart, and the two together, before asking: a 4K upscale of a 60 fps shot costs several times its retime, and Last order's user, shown only the total, asked for the retime alone first.

## What it needs

Each input by its canonical name, from the pipeline's table:

- the approved final shot, `<shot>: final shot`, the take to finish;
- the film's frame rate and delivery size, as facts, such as `<film>: frame rate` and `<film>: delivery size`, or the user's choice of them, settled as facts before the plan.

A take with motion blur in it is finished only after saying so: interpolation and upscaling turn blur into artifacts, as they did on Last order's fast moves. The final render has none, as the user set on 2026-11-15, and blur is added after finishing, in post.

## Making it

1. **Plan the retime.** The take as the video, the target frame rate, the length kept (no slow motion), H.264 out, and the model's interpolation model, chosen by its workflow skill for the footage. Show the plan and its cost, with the upscale's cost after it, and ask.
2. **Check the retime** before the upscale, frame by frame, since an agent cannot judge motion by watching: its length and frame rate against the plan; then frame strips of the fastest moves, such as a head turn or a door's swing, against the take's frames at the same times, for a new shape, a smear, or a doubled edge between frames. Show the strips with the take.
3. **Plan the upscale** of the approved retime: the factor to the delivery width, its frame kept whole, H.264 out, and the model's precision model, chosen for the footage, such as Gaia CG for computer graphics. Show the plan and its cost, and ask.
4. **Check the upscale:** its size, frame rate, and length against the plan; then before-and-after crops, at the same frame, of a face, a hand, a line, and a flat surface, for anything the take did not hold. Show the crops with the retime.
5. A take that fails is made again, as its own request, with one change, such as another interpolation or precision model.

Each approved step's take is published by `project-pipeline` as the shot's finished picture, such as `<shot>: final shot, 60 fps` and `<shot>: final shot, 60 fps, 4K`, each made from the take before it (`--from`), so a change to the final shot reaches them.

## Hand back

Hand back to `project-requests`:

- the retime request, then the upscale request: each the video endpoint, the take before it as its one input, by its canonical artifact, as `structure`, the source video it follows, in the field its workflow skill names, such as `video_url`, and the settings above; no prompt;

and, for the user to approve:

- each take, with its measured length, frame rate, and size, and the frame strips or crops it was checked by.

Then, once the finished picture is approved, the mix: [build-animatic](../build-animatic/SKILL.md)'s `mix.py` lays the finished sound over it, with the picture copied untouched, and [project-output](../project-output/SKILL.md) delivers the mixed film when the user calls it finished.
