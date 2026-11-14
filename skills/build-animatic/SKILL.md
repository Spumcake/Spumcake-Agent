---
name: build-animatic
description: Build an animatic from an approved shot list and its approved keyframes, or rough boards for shots that have no keyframe yet - each board held for its shot's length, in order, with its camera move and the transition into it marked and the script's lines cued at their recorded lengths - written as a plain, editable timing sheet (shot, board, in, out, length, camera move, transition, lines) that any editor or timeline can play, and, where the setup offers a language model, the prompt it runs to check each shot's timing against its lines; then the assembly script's command, which holds each frame on its times over the sound bed and the voices, for project-requests to run. Use when the user asks for an animatic, a story reel, a timed board, or to time the boards to the shot list. Not for drawing the boards or writing the shot list.
---

# Animatic

An animatic is made of each shot's on-model keyframe, generated and approved; a rough board stands in for a shot whose keyframe is not made yet. Below, "board" means the shot's keyframe, or its rough board when it has none. The clip assembled from them is not generated.

An animatic is the board played in time: each frame held for as long as its shot lasts, in order, with the camera's moves, the transitions, and the lines where they fall. It is the first time the user sees the film's rhythm, and the camera tests and the shots that follow are cut to it. This skill lays it out as a timing sheet, a plain list that any editor or timeline can lay out and play, and that the user can change by hand, then builds the request that assembles it into one clip the user can watch, which the camera tests, restyling, and sound are cut to.

A good animatic holds every shot of the approved shot list once, in order, for exactly its length, on its approved board. Its ins and outs run on without a gap or an overlap, and it adds up to the film's length. Every spoken line of the script is cued once, word for word, in the shot that covers it, with room to be said. A failed one drops or repeats a shot, holds a board for a length the shot list does not give, cues a line in the wrong shot, or squeezes a line into a shot too short to say it, however smoothly it plays.

## The model

The timing sheet is not generated: it is laid out from the shot list and the boards, and its sums are counted, not guessed. The clip is assembled by [the assembly script](scripts/assemble.py), with no model. A **language model** checks the sheet: whether each shot gives its lines time to be said, and where the pauses fall. It runs on a prompt this skill builds. The language model may be the agent itself, when the setup says so.

## Find the specifics

- **The workflow skill** of the language model the request names, or that the user chooses, says how it runs and what it takes; **its prompt skill** gives its syntax and limits.
- **The cost** of the check comes from the setup, and waits for the user's yes before anything is paid. The assembly costs nothing.

This skill builds each request and hands it back; [project-requests](../project-requests/SKILL.md) runs it with `scripts/request.py`, which sends it exactly as built. The specifics come from the setup, as the [prompt roles](../../docs/prompt-roles.md) describe. If one is missing, say which and stop. When the setup offers no language model for the check, say so, and give the user the counted checks of step 2 alone.

## What it needs

Each input by its canonical name, from the pipeline's table:

- the approved timing reference (`<film>: timing reference`, from `write-timing-reference`): each frame's in and out, and each cue's and line's time; the frames and the audio are made to it, and the animatic is assembled on it;
- the approved shot list (`<film>: shot list`), with each shot's number, length, camera, and lines; with none, one is planned and approved first;
- the approved board for it: one frame per shot (`<shot>: keyframe`, or `<shot>: rough board`), and an end frame (`<shot>: end keyframe`) for each camera move that has one; with none, the board is made and approved first;
- the approved script (`<film>: script`), for its lines and any transitions it writes, such as a fade in;
- the approved voice take of every spoken line (`<line>: voice take`, from `generate-voice`), with where its line starts and ends inside it (`<line>: start in take`, `<line>: end in take`), since voices are made before the animatic, so it is timed to the real lines; a line with no take yet is marked *estimated*;
- the approved sound bed (`<film>: sound bed`, from `generate-sound`): the scene's sound effects and music, with no voices;
- the film's length, frame rate, and size (`<film>: length`, `<film>: frame rate`, `<film>: size`).

Each step waits for the user's yes before the next. A check that costs anything waits for a yes to its plan: the model, the number of requests, and the cost.

Characters who read as minors are kept as the [prompt roles](../../docs/prompt-roles.md) say.

## The timing sheet

Fill [the timing sheet template](templates/timing-sheet.md). It has one row per shot, in the shot list's order:

- **Shot:** its number, as the shot list gives it, such as `3-1` or `3-2A`.
- **Board:** its approved frame, by its canonical name; for a camera move with an end frame, both, start first.
- **In and out:** timecode at the film's frame rate, hours, minutes, seconds, and frames. The first shot is in at zero. Each shot's in is the last one's out, and its out is its in plus its length.
- **Length:** the shot list's length, in seconds.
- **Camera move:** the shot list's move, said as a move on the board, such as "push in from the full frame to the inner rectangle", "pan right to the end frame", or "still". A move between a start and an end frame goes from one to the other across the shot.
- **Transition:** how the shot begins: a cut, unless the script writes another, such as a fade in, a dissolve, or a fade to black, or the user asks for one. A dissolve or a fade has its length in frames, centred on the cut, so no shot's in or out moves.
- **Lines:** each spoken line it covers, by speaker, marked on or off screen, quoted word for word from the script, with its cue number.

Below the rows, the **cue list** gives each line: its number, its shot, its speaker, the line word for word, its take, where it starts, and how long it takes. A line starts half a second into its shot, or half a second after the line before it in the same shot, unless the shot's action says otherwise. Its length is its take's measured length. Only a line with no take yet is estimated, at about two and a half words a second, and marked *estimated*.

Use the names and numbers of the shot list and the script, never new ones. Every name, length, and line comes from the pipeline's table with `pipeline.py`, never typed in by hand.

## 1. Check what was handed in

Before laying anything out, check that:

- every shot of the shot list has its approved board, and every board belongs to a shot;
- every board is named by its shot number, and every end frame by its shot number too;
- every spoken line of the script is in exactly one shot.

When something is missing, say which shot and what, and stop. When the user asks to time the board without it, list the shot with its board marked *missing*, held for its length.

## 2. Lay it out

Fill the timing sheet from the shot list, the boards, and the script, in shot order. Count, before showing it:

- the ins and outs run on from zero without a gap or an overlap;
- every length is the shot list's;
- the total is the shot list's total, and how far it is from the film's length;
- every line is cued once, in order, word for word.

Note each shot whose lines, at their measured lengths with half a second before and after, need more than its length. A take's line is never squeezed or moved to fit: the shot's length changes, and the change goes back to the shot list.

## 3. Check the timing

Build the check's prompt from [the timing check template](templates/timing-check.md): the timing sheet, the approved script, and [the timing findings template](templates/timing-findings.md) as the exact form of its answer. The title and the length are written as `{{<film>: title}}` and `{{<film>: length}}`, filled from canon.

Plan the request: the model, and the cost when it bills, from the setup. It runs as its own cycle on the user's yes when it costs anything. Send it as the [prompt roles](../../docs/prompt-roles.md) say.

Check the answer before showing it: every shot is in it once, by its number; each finding names the shot and the line; and every count agrees with the sheet. When it does not, correct the prompt as the [prompt roles](../../docs/prompt-roles.md) say, as a new request.

The check proposes; it never changes a length. A shot too short for its lines, or a long silence, is shown to the user with what the check suggests.

## 4. Assemble the clip

The clip is assembled by [the assembly script](scripts/assemble.py), which needs ffmpeg and costs nothing. Its command, with `<build-animatic>` this skill's folder as the setup installs it, is:

```text
python3 <build-animatic>/scripts/assemble.py <assembly.json> <animatic>.mp4
```

Write its assembly JSON from the timing reference, as the script's usage gives it:

- **the frames:** each approved keyframe with its in and out, running on from zero to the film's length;
- **the bed:** the sound bed, under everything;
- **the clips:** each voice take, trimmed to the line or voice sound inside it and laid at its cue, with a gain that keeps the voices the loudest, as the sound design brief's mix asks;
- **the length, frame rate, and size:** the film's.

Each frame, the bed, and each take is named in the request by its canonical artifact, with its role in the cut, such as "frame, 0.0 to 3.0 s" or "clip 0.05 to 0.65 s, laid at 4.2 s, at 0 dB", in the order the JSON lists them; its file comes from the pipeline's table, never typed in by hand. The script mixes the audio, holds each frame for its length, and renders one video at the film's size and frame rate; it writes nothing else.

A camera move or a transition the timing sheet marks is added in the editor or by a later version of the script; say when a clip has none. Check the video against the timing reference: every frame, in order, for its length, and every line on its cue. The clip is assembled again, as a new request, whenever the sheet, a frame, or a take changes.

## 5. The user's review

An animatic with any line marked *estimated* is shown with those lines listed first. The user approves it only by accepting each estimated line by name, or after its take replaces the estimate and the shot is timed again.

Show the timing sheet with its total, the counted notes, and the check's findings, with the shots most at risk first. The user's corrections win. A correction the user writes, such as a length, a transition, or a cue, is made in the sheet directly, and every in and out after it is counted again.

A length that differs from the approved shot list is a change to the shot list. List each one, so the caller can carry it back; never leave the two disagreeing without saying so.

Revise until the user approves it. The approved sheet and clip are published by `project-pipeline`; a rejected one is never used as an input again. When the shot list or a board changes later, change only the rows it touches, count every in and out after them again, and list what changed. A shot keeps its number; a cut shot's row is removed, and its number is not used again.

## Hand back

Hand back to [project-requests](../project-requests/SKILL.md):

- **the check request,** when the setup offers a language model: its endpoint, the prompt as built from the timing check template, naming canon, and the timing sheet and the script it carries;
- **the assembly request,** a `script` request: the command above; its assembly JSON; each frame, the bed, and each take by its canonical artifact, with its role in the cut, in the order listed; and the file it makes, the animatic's video;
- the timing sheet, with its cue list and counted notes, for the user's approval;
- each shot whose length now differs from the approved shot list.
