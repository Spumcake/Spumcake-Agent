---
name: create-detail-sheet
description: Paint a character's or a prop's level-of-detail sheet - the same subject four times, from close to very far, painted with one brush size so the further it is, the fewer brushstrokes it is made of - from its concept art reference, so concept artwork paints it with the detail its distance from the camera allows. Use once a character or prop has its concept art reference, before it is staged into concept artwork. Not for the reference itself (create-concept-reference), for sizes against other characters (create-line-up), or for staging (create-concept-artwork).
---

# Level-of-detail sheet

A painter puts fewer strokes into a figure far away than into one close by, because the brush stays the same size while the figure shrinks. Image models do not: staged into a loosely painted place, a character keeps all the detail of its study, so the model either paints it more finely than the room around it or makes it huge to fit that detail (the user, 2026-11-12). Level of detail is the computer-graphics term for the same idea, a simpler model the further away it is.

This skill paints that knowledge as an image: the subject at four distances, side by side, with one brush size across the sheet. Concept artwork then sends the sheet with the study and names the figure whose distance matches the subject's place in the shot, and the subject comes out with the detail of that distance. The user judged the idea right on its first test, staging a character into a theatre (2026-11-12).

A good sheet keeps the subject's pose, colours, and shapes in all four figures, and loses detail figure by figure: the face's marks, then the small parts, then everything but a few patches of colour. A failed one shrinks the same detailed figure four times, or changes the subject as it shrinks.

## The models and the route

As `create-concept-reference` says: an image-edit model that takes the prompt exactly as written, such as OpenAI's image edit with gpt-image-2.6-sunburst, at high quality and the film's aspect ratio.

## What it needs

- the subject's concept art reference, from `create-concept-reference`;
- a folder for the prompt and the sheet.

## Making it

Fill [the detail sheet template](templates/detail-sheet.md) and send the concept art reference alone. Every slot is filled:

- `{{subject}}`: what the reference shows, such as "a character, a grinning showman in a white tailcoat"; `{{it}}`, `{{its}}`: the pronoun for the subject on the sheet.
- `{{background}}`: a plain background of a value that both the subject's lightest and darkest colours stand out against, such as "a plain mid-grey background"; a light subject on a light background loses its silhouette at a distance.
- `{{close_marks}}`, `{{middle_marks}}`, `{{far_marks}}`, `{{very_far_marks}}`: what each figure is made of, from the subject's own parts, losing detail step by step. For a character: close, the face's marks and the fingers read as their own simple marks; middle, the face is a stroke or two and the hands plain shapes; far, a few patches of colour and no face; very far, one small silhouette of a few strokes with touches of its key colours. For a prop: close, its parts and markings; middle, its main parts as single shapes; far, its silhouette and main colours; very far, one shape.

The figures stand on one ground line at halving heights, so concept artwork can match a figure to the subject's height in the frame. Make one; a second call is for a sheet that failed. Show it with its prompt and the reference sent.

## Hand back

- the sheet, with its prompt and the reference sent;
- the film map, updated: the sheet sits beside the subject's concept art reference, and `create-concept-artwork` sends it whenever the subject is staged.
