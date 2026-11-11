---
name: create-animatic
description: Build an animatic from an approved shot list and its approved keyframes, or rough boards for shots that have no keyframe yet - each board held for its shot's length, in order, with its camera move and the transition into it marked and the script's lines cued at their recorded lengths - written as a plain, editable timing sheet (shot, board file, in, out, length, camera move, transition, lines) that any editor or timeline can play, and, where the setup offers a language model, the prompt it runs to check each shot's timing against its lines, then take it to the user for approval. Use when the user asks for an animatic, a story reel, a timed board, or to time the boards to the shot list. Not for drawing the boards or writing the shot list.
---

# Animatic

An animatic is made of each shot's on-model keyframe, generated and approved; a rough board stands in for a shot whose keyframe is not made yet. Below, "board" means the shot's keyframe, or its rough board when it has none. The clip assembled from them is not generated.

An animatic is the board played in time: each frame held for as long as its shot lasts, in order, with the camera's moves, the transitions, and the lines where they fall. It is the first time the user sees the film's rhythm, and the camera tests and the shots that follow are cut to it. This skill writes it as a timing sheet, a plain list that any editor or timeline can lay out and play, and that the user can change by hand, then has it assembled into one clip the user can watch, which the camera tests, restyling, and sound are cut to.

A good animatic holds every shot of the approved shot list once, in order, for exactly its length, on its approved board. Its ins and outs run on without a gap or an overlap, and it adds up to the film's length. Every spoken line of the script is cued once, word for word, in the shot that covers it, with room to be said. A failed one drops or repeats a shot, holds a board for a length the shot list does not give, cues a line in the wrong shot, or squeezes a line into a shot too short to say it, however smoothly it plays.

## The model

The timing sheet is not generated: it is laid out from the shot list and the boards, and its sums are counted, not guessed. A **language model** checks it: whether each shot gives its lines time to be said, and where the pauses fall. It runs on a prompt this skill builds. The language model may be the agent itself, when the setup says so.

## Find the specifics

- **The workflow skill** of the language model the request names, or that the user chooses, says how it runs and what it takes; **its prompt skill** gives its syntax and limits.
- **The execution skill** that implements `create-animatic` in this setup renders the check and assembles the clip; when none does, the setup's renderer. It says what a request costs.

All come from the setup, as the [prompt roles](../../docs/prompt-roles.md) describe. If one is missing, say which and stop. When the setup offers no language model for the check, say so, and give the user the counted checks of step 2 alone.

## What it needs

From the caller:

- an approved shot list, with each shot's number, length, camera, and lines; with none, one is planned and approved first;
- the approved board for it: one frame per shot, named by its shot number, and an end frame, named by the number and `-end`, for each camera move that has one; with none, the board is made and approved first;
- the approved script, for its lines and any transitions it writes, such as a fade in;
- the approved voice recording of every spoken line, each with its measured length, since voices are made before the animatic, so it is timed to the real lines; a line with no recording yet is marked *estimated*;
- the film's length and frame rate;
- a folder for the timing sheet, the check's prompt, and its answer.

Each step waits for the user's yes before the next. A check that costs anything waits for a yes to its plan: the model, the number of requests, and the cost.

Characters who read as minors are kept as the [prompt roles](../../docs/prompt-roles.md) say.

## The timing sheet

Fill [the timing sheet template](templates/timing-sheet.md). It has one row per shot, in the shot list's order:

- **Shot:** its number, as the shot list gives it, such as `3-1` or `3-2A`.
- **Board:** the file of its approved frame; for a camera move with an end frame, both, start first.
- **In and out:** timecode at the film's frame rate, hours, minutes, seconds, and frames. The first shot is in at zero. Each shot's in is the last one's out, and its out is its in plus its length.
- **Length:** the shot list's length, in seconds.
- **Camera move:** the shot list's move, said as a move on the board, such as "push in from the full frame to the inner rectangle", "pan right to the end frame", or "still". A move between a start and an end frame goes from one to the other across the shot.
- **Transition:** how the shot begins: a cut, unless the script writes another, such as a fade in, a dissolve, or a fade to black, or the user asks for one. A dissolve or a fade has its length in frames, centred on the cut, so no shot's in or out moves.
- **Lines:** each spoken line it covers, by speaker, marked on or off screen, quoted word for word from the script, with its cue number.

Below the rows, the **cue list** gives each line: its number, its shot, its speaker, the line word for word, its recording, where it starts, and how long it takes. A line starts half a second into its shot, or half a second after the line before it in the same shot, unless the shot's action says otherwise. Its length is its recording's measured length. Only a line with no recording yet is estimated, at about two and a half words a second, and marked *estimated*.

Use the names and numbers of the shot list and the script, never new ones.

## 1. Check what was handed in

Before laying anything out, check that:

- every shot of the shot list has its approved board, and every board belongs to a shot;
- every file is named by its shot number, and every end frame by its number and `-end`;
- every spoken line of the script is in exactly one shot.

When something is missing, say which shot and what, and stop. When the user asks to time the board without it, list the shot with its board marked *missing*, held for its length.

## 2. Lay it out

Fill the timing sheet from the shot list, the boards, and the script, in shot order. Count, before showing it:

- the ins and outs run on from zero without a gap or an overlap;
- every length is the shot list's;
- the total is the shot list's total, and how far it is from the film's length;
- every line is cued once, in order, word for word.

Note each shot whose lines, at their recorded lengths with half a second before and after, need more than its length. A recorded line is never squeezed or moved to fit: the shot's length changes, and the change goes back to the shot list.

## 3. Check the timing

Build the check's prompt from [the timing check template](templates/timing-check.md): the timing sheet, the approved script, and [the timing findings template](templates/timing-findings.md) as the exact form of its answer. Save the prompt beside the sheet.

Plan the run: the model, and the cost when it bills. Run it on the user's yes when it costs anything, with the setup's renderer. Send it as the [prompt roles](../../docs/prompt-roles.md) say.

Check the answer before showing it: every shot is in it once, by its number; each finding names the shot and the line; and every count agrees with the sheet. When it does not, correct the prompt as the [prompt roles](../../docs/prompt-roles.md) say.

The check proposes; it never changes a length. A shot too short for its lines, or a long silence, is shown to the user with what the check suggests.

## 4. Assemble the clip

Have the timing sheet assembled into one video, with the setup's renderer or editor: each board held for its length, in order; a camera move shown as a slow move across its board, from its start frame to its end frame when there is one; the transitions as marked; and the recorded lines on their own track, at their cues; a cue card stands in only for a line marked *estimated*. Plan it, with the cost when it bills, and assemble it on the user's yes. Watch it against the sheet: every shot, in order, for its length. The clip is named for the film and the sheet's version, and is remade whenever the sheet changes.

## 5. The user's review

An animatic with any line marked *estimated* is shown with those lines listed first. The user approves it only by accepting each estimated line by name, or after its recording replaces the estimate and the shot is timed again.


Show the timing sheet with its total, the counted notes, and the check's findings, with the shots most at risk first. The user's corrections win. A correction the user writes, such as a length, a transition, or a cue, is made in the sheet directly, and every in and out after it is counted again.

A length that differs from the approved shot list is a change to the shot list. List each one, so the caller can carry it back; never leave the two disagreeing without saying so.

Revise until the user approves it, and mark it approved with the date. When the shot list or a board changes later, change only the rows it touches, count every in and out after them again, and list what changed. A shot keeps its number; a cut shot's row is removed, and its number is not used again.

## Hand back

Hand back to the caller:

- the approved timing sheet, with its cue list;
- the assembled clip, which the camera tests, restyling, and sound are cut to;
- the timing check's prompt and its answer, with what the user chose to do about each finding;
- each shot whose length now differs from the approved shot list.
