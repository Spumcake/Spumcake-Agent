---
name: review-continuity
description: Review a result for continuity errors before the user approves it - a pre-production image, a keyframe, a background plate, a line keyframe, a line-art or lip-synced shot, a final shot, a sound, or a whole sequence of shots across its cuts - against everything it must agree with (the characters' A-pose views, the other subjects' reference sheets, model sheets, and colour lists, the line-up's heights, the place's primary canonical location and its views with their neutral passes, its mood reference, the style guide's rules and the colour script, the shot list's framing, camera, action, and lines, the script's words, and the shots on either side), by sampling the result and building the prompt a vision-capable, or for a sound an audio-capable, language model runs on it, then checking that every difference comes back with where it is, the reference it breaks, what it should be, whether it blocks approval, and its evidence, and taking each finding to the user to accept or remake. Use when the user asks for a continuity check or review, to check an image, a shot, a sheet, a clip, a lip-sync, or a sound against its references, or to check a sequence across its cuts, and whenever a step that made an image, a clip, or a sound reaches the user's approval. Not for fixing, redrawing, or re-rendering a result, for scoring or choosing between takes, or for checking an animatic's timing.
---

# Continuity review

A continuity review compares a result with everything it must agree with, before the user approves it, and reports every difference. It runs at the end of every step that makes an image, a clip, or a sound: pre-production images, keyframes, background plates, line keyframes, line-art shots, lip-synced shots, final shots, and sounds, and across a sequence of shots at its cuts. A result is ready for the user's approval when its review is clear, or when the user has accepted each finding. This skill reports; it never scores, fixes, redraws, or re-renders, and it never decides for the user.

A good review finds every difference a careful viewer would, and says exactly where each one is, a frame, a time, a word, or a region; which reference it breaks; what it should be; whether it blocks approval; and what shows it. It lists what it checked and found clear, and what it could not check. A failed review misses a swapped prop or a flipped screen direction, reports a difference without saying where, cites a reference that was not sent, gives a score or a verdict, or proposes a redraw. A clear review is not an approval: the user still looks, and approves.

## The models

- **An image, a clip, or a sequence** is reviewed by a **vision-capable language model**, sent the result's samples and the references as images, on a prompt this skill builds.
- **A sound** is reviewed by a **language model that takes audio**, sent the sound and its voice reference.
- **A lip-synced shot** is reviewed by a vision-capable language model on its frames; when the model also takes the shot's sound, the words are checked by ear too.

The language model may be the agent itself, when the setup says so.

## Find the specifics

The **workflow skill** of the model the request names, or that the user chooses, says whether it takes images, video, or audio, how many files one request takes, and the largest size it takes. **Its prompt skill** gives its syntax and limits. The setup says what a request costs, and takes a clip's frames.

All come from the setup, as the [prompt roles](../../docs/prompt-roles.md) describe. If one is missing, say which and stop. This skill builds the review's request and hands it back; `project-requests` runs it with `scripts/request.py`, which sends it exactly as built. When the request names no model and more than one fits, ask. When the setup cannot take frames from a clip, or has no model that takes the result's kind, say so and stop; never review by hand in its place.

## What it needs

- the result: the request that made it, its kind, its name, such as its shot number or its sheet's name, and the step that made it;
- the published references it must agree with, by canonical name from the pipeline's table, such as `<character>: A-pose front` or `<place>: view <wall>`, as step 1 lists them for its kind, each with what it fixes;
- what each of those images shows, and the facts the checks need, such as `<character>: mark in <frame>`, from the pipeline's table with `pipeline.py`;
- for a clip, a lip-synced shot, or a final shot, its length and frame rate (`<film>: frame rate`), and the cuts in it, when it was assembled from several shots;
- the neighbouring shots' published results, when the result is a shot, such as `<shot>: keyframe`: the last frame of the shot before and the first frame of the shot after, or their sounds.

Each step waits for the user's yes before the next. Every paid request waits for a yes to its plan: the model, the number of requests, and the cost. A first review on a new model is a short test, one result, before a batch.

Characters who read as minors, and a recognisable real person's likeness or voice, are reviewed only as the [prompt roles](../../docs/prompt-roles.md) say.

## Review prompts

A review prompt says what the result is, what each file is, what the written references say, what to check, and how to report. Write it in this order, for any model:

1. **What the result is:** its kind, its name, the film, and its job in one line, such as "the keyframe for shot 3-2, the first frame its clip is animated from". The job tells the model what matters most.
2. **The files,** numbered in the order sent: the result's samples first, each with its frame number and time, or its word; then the references, each subject's together, a character's front A-pose view first, then its other A-pose views and sheets, or another subject's reference sheet first; then the place's, then the neighbouring shots', and the style sheet last. Say what each reference fixes, such as "Mira's front A-pose view: her face, hair, proportions, and outfit". A model cannot guess which reference is for what.
3. **The written references,** quoted from their published artifacts and facts, never reworded or typed by hand: the colour list's rows, the line-up's heights and landmarks, the style guide's rules, the colour script's line, the shot list's row, and the script's lines. In the prompt, each canonical value is written as `{{<element>: <fact>}}`, filled from the pipeline's table. Written values settle what an image leaves unclear.
4. **The checks,** one short line each, each concrete enough to see or hear, and each against a named reference: "her jacket is Rust, #B5512C, as her colour list gives it", not "her colours are right". Leave out the checks the result has no reference for.
5. **How to report:** every difference, however small; where; against what; what it should be; whether it blocks approval or is a note; and the evidence. No score, no verdict, no fix.
6. **The answer's form:** [the findings template](templates/findings.md), exactly.

Leave out praise, taste, and anything about how the result was made. Keep each check to a line; a long prompt with many images makes a model skip checks. When the samples and references are more than one request takes, split the samples across requests in time order, each sent with the same references and the same checks, and overlapping by one sample.

Put the words in `prompt`, and the files, numbered as the prompt numbers them, in `references`, by the [prompt roles](../../docs/prompt-roles.md); or by the names the language model's workflow skill gives when it does not take roles. Each reference is named by its canonical artifact, with its role, such as "image 3, `<character>: A-pose front`, her face, hair, proportions, and outfit".

## 1. Gather the references

First run `request.py check`. A result with no report, a report pointing at a missing file, or a library file changed since it was made is not reviewed until `project-requests` sets it right. Gather every reference from the pipeline's table by its canonical name, never by a file name, and read what each published image shows, its camera, its named things, where each is, its state, and what it looks at, from the table with `pipeline.py`.

Choose the template for the result's kind, and gather what it must agree with:

- **A pre-production image,** such as an A-pose view, a reference or model sheet, concept art, a line-up, a place's primary canonical location or one of its views, a neutral pass, or a mood reference, uses [the image template](templates/review-image.md). It agrees with the characters' A-pose views, the other subjects' reference sheets, model sheets, and colour lists; the line-up's heights; the place's primary canonical location and its views, with their neutral passes, and its mood reference; the style guide's rules and style sheet; and, for an image of a beat, the colour script's line. Checks: the subjects, the heights, the place, the look.
- **A keyframe or an end frame** uses the image template. It agrees with all of the above for the subjects and place in it, the shot list's row, and the neighbouring shots' keyframes. Checks: the subjects, the heights, the place, the look, the shot, across the cut.
- **A background plate** uses the image template. It agrees with the place's views, with their neutral passes, and its mood reference, the style guide, and the shot list's row, and has no subject in it. Checks: the place, the plate, the look, the shot.
- **A line keyframe** uses the image template. It agrees with the keyframe it was redrawn from, the subjects' reference sheets, and the style guide's line rules. Checks: the subjects, by shape only, the image it came from, the shot, line art.
- **A clip,** such as a line-art shot or a motion test, uses [the clip template](templates/review-clip.md). It agrees with its start and end keyframes, or line keyframes, the subjects' reference sheets and colour lists, the line-up, the place, the shot list's row, and the shots on either side. Checks: the keyframes, holding through the shot, the subjects, the heights, the place, the shot, across the cut, the look; line art for a line-art shot; a loop for a walk cycle or an idle loop.
- **A lip-synced shot** uses [the lip-sync template](templates/review-lip-sync.md). It agrees with its voice line, word for word with each word's time, the speaker's mouth chart and front A-pose view, and the line-art shot it was made from. Every group of checks applies.
- **A final shot** uses [the final shot template](templates/review-final-shot.md). It agrees with the line-art or lip-synced shot it was made from, the colour models and colour lists, the place's mood reference for its mood, the colour script's line for its beat, the place's views or its background plate, the characters' A-pose views and the other subjects' reference sheets, the style guide, and the final shots on either side. Every group of checks applies.
- **A sound,** a voice line, an effect, an ambience, or music, uses [the sound template](templates/review-sound.md). It agrees with the script's words and directions, the speaker's voice reference, the timing sheet's cue and the shot's length, the shot list's action, the place, and the beat's mood, and with the sounds on either side. Checks: the words and the voice for a voice line; the timing, the place and the mood, and across the cut for every sound.
- **A sequence of shots** uses [the sequence template](templates/review-sequence.md), when the user asks for one, or once every shot of a scene has its own review. It agrees with the shot list's rows, the subjects' and the place's references, and the colour script. Every group of checks applies.

**Space.** Every image with a character in a place is also checked against the place's floor plan (`<place>: floor plan`) and the blocking the timing settles, as the pipeline's table holds it, such as `<character>: mark in <frame>`: each character stands on their mark, faces the way it gives, and looks at the named object it gives, as this camera sees it; each named object is where the plan puts it, and in the state the blocking gives, such as a door open or closed. A look aimed at the wrong door is a finding, however good the frame.

**A generated image's own sources.** Every image a model made from a request is also checked against what it descends from, which is how `fix-canonical-image` finds what to fix:

- **its canonical prompt,** the text-to-image prompt it descends from, as sent, from its request's report with `request.py show`, however many edits came after it: what the image has that a line rules out, such as many elements where the prompt asks for minimal ones, and what a line asks for that came out wrong, each finding quoting the line. The prompt is the only measure here: what it does not say, such as a number of stools, is not a finding;
- **its pre-vis,** when it was made from one, as what it was made from in the pipeline's table shows, as its inventory: anything the pre-vis does not represent, except the world seen through the windows; and for each such thing, whether it reads clearly as a thing the place needs, such as a door;
- **each visible object, one by one:** an object that does not read clearly as any one thing, or a thing formed wrongly, such as a partition that could be a door, a window, or a cabinet;
- **on a form pass,** a view with no textures: texture that shows through, such as lettering, or patterns on floors, walls, or upholstery;

A style the model chose for something that was asked for, and a thing asked for that is right, are not findings.

Send only published references; a rejected result is never sent. When one is missing, say which, and ask whether to stop or to review without it; without it, its checks go under *Could not check*. When a reference was replaced by a later publish since the result was made, say so: the result is out of date, and is reviewed against the new version.

Use the canonical names the pipeline's table gives for every character, place, prop, and shot, and the numbers the user approved.

## 2. Sample the result

- **An image** is sent whole.
- **A clip** is sampled at its first frame, its last frame, the last frame before and the first frame after each cut, and a spaced set between: one frame every half second, or every second in a clip longer than ten seconds, and never fewer than four between the first and the last. Add a frame at each moment the shot list's action names, and any frame the user points to.
- **A lip-synced shot** is sampled as a clip, and also at each word's main sound and in each pause, by the voice line's word timings, which the caller or the setup gives. With none given, estimate each word's time from the line's cue at about two and a half words a second, and mark every such time *estimated*. Take the line-art shot's frames at the same frame numbers.
- **A final shot** is sampled as a clip, with the line-art shot's frames at the same frame numbers.
- **A sound** is sent whole, with its voice reference.
- **A sequence** is sampled at each shot's first, middle, and last frames.

The setup takes the frames as part of the request. Label each in the request by the result, its frame number, and its time.

## 3. Build the prompt

Fill the kind's template, following the review prompts above:

- `{{files}}` is one numbered line per file, in the order sent, with what it is and what it fixes.
- `{{written_references}}` quotes each written reference under its name.
- `{{result_job}}` is one line on what the result is for and what comes next from it.
- Keep only the groups of checks step 1 gives for the result's kind, and remove the rest. A group whose reference is missing is removed, and named in the prompt as one to list under "Could not check".
- `{{colour_script_check}}` is "Against the colour script's line for its beat: its dominant colours, accent, light, and contrast." when the result has a beat and is in colour; otherwise it is empty.
- In the lip-sync template, `{{timing_note}}` is ", estimated" when the times are estimated; `{{words_check}}` is "Against the voice line, by ear: every word is said, in order, none added, dropped, or changed, by the speaker's voice." when the model takes the sound, and otherwise "The words cannot be heard in frames; list this check under 'Could not check'."
- In the image template, `{{allowed_change}}` says what the step was meant to change, such as "the finish: colour, tone, and background are taken out, and the lines are cleaned" for a line keyframe.
- In the clip template, `{{cuts}}` lists the cuts by frame number, or is "none" for a clip of one shot, so a jump inside it is a finding.
- In the final shot template, `{{plate_note}}` is ", and its background plate" when the shot was composited over one; otherwise it is empty.
- In the sound template, `{{use}}` says where the sound goes, such as "the line of cue 12, in shot 3-2", and `{{timing}}` gives its cue, its start, and its shot's length.
- `{{findings_template}}` is [the findings template](templates/findings.md), as the exact form of the answer.

## 4. Hand it to be run

Hand the request back: the model, the number of requests, and the cost from the setup when it bills. `project-requests` runs it on the user's yes when it costs anything, with its files sent as the [prompt roles](../../docs/prompt-roles.md) say, and its report holds the answer. When the review was split across requests, merge the answers into one findings list, in order, and report a difference found in two overlapping requests once.

## 5. Check the answer

Before handing it back, check that:

- it is in the findings form, every section present;
- every finding has a what, a where, an against, a should be, a serious of *blocks approval* or *note*, and evidence;
- every where points to a sample that was sent, a frame or time inside the result, or a word of the line;
- every against names a reference that was sent, and its should be is what that reference says;
- every check in the prompt is a finding, under "Checked and clear", or under "Could not check";
- the names are the script's and the shot list's;
- there is no score, no overall verdict, and no fix, redraw, or re-render proposed.

When a check fails, correct the prompt as the [prompt roles](../../docs/prompt-roles.md) say.

Then look at the sample each finding points to. When the difference cannot be seen there, say so beside the finding; never drop a finding, and never add one of your own to the model's list. A difference you see that the review missed is handed back separately, as yours.

## 6. The user's decision

The findings go in order, those that block approval first, each with its sample beside the reference it breaks; then what was checked and clear, and what could not be checked. A review that found nothing is not proof that nothing is wrong.

The user decides each finding:

- **accept it:** the result stands with that difference, with the user's reason when they give one, and may be published by `project-pipeline`;
- **remake:** the result goes back to the step that made it, as a new request, with the finding as what to change; the rejected result is never used as an input again.

Never choose for them, never fix the result, and never remake it here. When `fix-canonical-image` called the review, its findings go to its fixes instead. The findings form's "The user's decision" lines and "Decided" are left empty by the review, for the user's decisions. When a remade result comes back, review it again from step 2 with the same references, and say which earlier findings are gone and which remain.

## Hand back

- the review's request, for `project-requests`: the endpoint kind, a language model that takes the result's kind; the prompt, with each canonical value as `{{<element>: <fact>}}`; and the files in the order sent, the result's samples first, then each reference by its canonical artifact with its role;
- once the answer is checked, the findings, in [the findings template](templates/findings.md): each difference, where it is, which canon it breaks, what it should be, and whether it blocks approval, with what was checked and clear;
- each reference that was missing or out of date, and the checks that could not be made.
