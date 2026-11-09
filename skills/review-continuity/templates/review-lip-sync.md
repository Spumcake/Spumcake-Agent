## Prompt

You are reviewing the lip-synced shot "{{result_name}}" from "{{title}}", an animated film, for continuity errors before the user approves it. It is {{seconds}} seconds long, at {{frame_rate}} frames a second, and {{speaker}} says the line below in it. It was made from the line-art shot {{source_shot}}: only the mouths should have changed. Find every way it differs from what it must agree with, below, and report each one. You do not score it, judge its taste, or fix it: the user decides what to do about each difference.

The files are attached in this order. First, frames sampled from the lip-synced shot, in time order, each with its frame number, its time, and the word or pause it falls on; then the line-art shot's frames at the same frame numbers; then the references, each with what it fixes:

{{files}}

The voice line, word for word, as the script gives it, with each word's time in the shot{{timing_note}}:

{{line_timing}}

The mouth chart's shapes, each with the sounds it makes:

{{mouth_shapes}}

The other written references, quoted as approved:

{{written_references}}

Check each of these, against the references given and nothing else.

### Word by word

For each word, at the sample that falls on it:

- the speaker's mouth shows the mouth chart's shape for the word's main sound, as the mouth chart draws it on this subject;
- the shape is there at the word's time, not a word early or late;
- the mouth is shut, or in the chart's rest shape, at every pause, before the first word, and after the last;
- only the speaker's mouth moves; every other mouth stays as it is in the line-art shot.

### The words

{{words_check}}

### Unchanged from the line-art shot

At each pair of frames with the same frame number: every subject's position, pose, facing, head angle, eyes, and outline, and every prop, are as they are in the line-art shot. Only the speaker's mouth, jaw, and the lines around them differ.

### The subject

Against the speaker's base sheet and mouth chart: the mouth, teeth, and jaw keep the subject's design in every sample, and the face around them does not change shape.

### Line art

In every sample:

- character outlines only: no colour fill, no shading or tone, no background, floor, or ground line;
- every line clean and unbroken, around the mouth as everywhere else, with no stray marks, doubled lines, gaps, or smudges;
- line weight as in the line-art shot.

How to report:

- Report every difference you can see, however small, each as its own finding. Do not leave one out because the rest is right. A difference that lasts is one finding, at the first sample that shows it, with the span it lasts.
- Say where it is: the word, the sample's frame number and time, and the region, such as "the word 'lantern', frame 58, 0:02.42, the lower lip".
- Say which reference it breaks, by the name given above and the part of it, such as "the mouth chart, the 'MBP' panel", and what that reference says it should be.
- Mark it **blocks approval** when it breaks something a reference fixes: a wrong mouth shape on a word, a mouth moving in a pause or on the wrong character, a word missing, added, or changed, anything but the mouth moved from the line-art shot, the speaker off model, or any fill, shading, background, or broken line. Mark everything else a **note**: a small difference that leaves what the reference fixes intact, or one where the references say nothing.
- Give the evidence: what the sample shows, and what the reference shows or says, side by side. When you are unsure, report it anyway and say why.
- Compare only with the references given. Do not judge whether it looks good, give it a score or an overall verdict, or say how to fix or re-render it.
- List every check above that found nothing under "Checked and clear", and every check the samples could not show under "Could not check".
- Use the names given above for every character, word, and shot, and no others.

Characters who read as minors stay in ordinary, everyday situations; nothing about them is sexual or suggestive.

Answer with the findings only, in exactly this form:

{{findings_template}}
