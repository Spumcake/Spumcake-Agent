---
name: generate-concept-design
description: Explore what a subject or a place could look like before anything about it is fixed - a brief with three or four directions, text-to-image candidates from the concept context template, one image per chosen direction, and refinements - so the user can choose a design by eye. Use when the user asks for concept designs or to explore a character, prop, or place, in the breakdown stage, before it is made canonical. Not for canonical images (make-canonical), concept art references (generate-concept-reference), or concept artwork (generate-concept-artwork).
---

# Explore a concept

Concept art finds what one subject looks like before anything fixes it. It answers the subject's brief several ways at once, so the user can choose by eye, and the design they settle on becomes the input images its reference is drawn from. A subject is anything that must look the same every time it appears: a character, a creature, a prop, a vehicle, or a place.

A good set gives the user real choices. Each direction answers the brief differently in its silhouette, proportions, costume, parts, or materials, and all of them are in the concept's look, clear enough to be drawn again from any side. A failed set is one design repeated with different colours, a design off the style guide, or a design that ignores the user's own sketch.

## The models

- **With nothing to send,** no sketch, no art, and no style sheet, use a **text-to-image model**. The words carry the whole design and the whole look, so the brief and the style must be concrete.
- **With anything to send,** the user's sketches or art of the subject, or the concept's style sheet, use an **image-edit model** with them as references. The user's own sketch is the strongest source of a design, and is never replaced by a model's guess.
- **A mix or a refinement** of chosen directions always comes from an **image-edit model**, sent with the chosen images. Never remake a chosen design from text alone: it would drift from what the user chose.

## Find the specifics

- **The workflow skill** of the model the request names, or that the user chooses, says which way of running it takes text alone and which takes references, how many references it takes, and the sizes it makes. **Its prompt skill** gives its syntax and limits.
- **The execution skill** that implements `generate-concept-design` in this setup renders it; when none does, the setup's renderer. It says what a request costs and where its output lands.

All come from the setup, as the [prompt roles](../../docs/prompt-roles.md) describe. If one is missing, say which and stop. When the request names no model and more than one fits, ask.

## What it needs

From the caller:

- the user's request: the subject, what it is for, and anything it must or must not be;
- the subject's name as the script uses it, and the scenes it appears in, when there is a script;
- the user's sketches or art of the subject, when there are any;
- the concept's style guide, when it has one: its written rules and its style sheet;
- a folder for the brief, the prompts, and the images, each image saved beside its prompt.

Each step waits for the user's yes before the next. Every paid request waits for a yes to its plan: the model, the number of requests, and the cost. A first run on a new model is one image, as a test, before the rest.

Characters who read as minors are kept as the [prompt roles](../../docs/prompt-roles.md) say.

Use only sketches, art, and photographs the user has the right to use this way. Base a design on a recognisable real person only when the user confirms that the person agreed to this use, or a guardian did for a child; never to deceive anyone.

## Image prompts

These parts are for the design directions: an optional exploration made by text alone or from the user's own sketches, before an element is made canonical.

A concept prompt says what the picture is for, then what the subject must be, then how this direction answers it, then how it looks. Write it in this order, for any model:

1. **What the image is:** "a concept design" for a subject, or "a concept painting" for a place, for an animated production. It is an exploration, not a reference sheet: one clear view, not a turnaround.
2. **The subject:** what it is, its role, and the brief's must-haves, in the same words in every direction. Name it as the script does, or by role ("the night watchman"), never by a real person's name.
3. **The direction:** the one or two lines that change between directions, such as "a tall, narrow silhouette; long coat; brass and leather". Change shapes and proportions before colours; a palette swap is not a new direction.
4. **The layout:** for a subject, the whole of it in a three-quarter view on a plain ground, with at most two small close-ups of the details that make it recognisable. For a place, one wide view that shows its layout, its scale, and what makes it this place.
5. **The look:** the style guide's written rules, quoted, not reworded: shapes, line, colour, light, and texture. With no style guide, the look the user described, in concrete terms.
6. **The references,** when there are any: what each one is, in the order they are sent, and what to keep from it. A sketch keeps its pose and the main shapes of its design, redrawn cleanly in the look. The style sheet comes last, for its line, colour, and light only, never its subjects.
7. **What to leave out:** text, logos, borders, extra figures, and anything the brief rules out, as a plain sentence.

Keep each part to a sentence or a few short lines, as `prompt-image` says. Keep every part but the direction the same between directions, so the differences the user sees are the directions' differences. Leave out what the model ignores, as its prompt skill says.

Put each part into its field in the model's syntax, as its prompt skill says: the words in `prompt`, what to avoid in `negative` when the model takes it, and the images, in order, in `references`, by the [prompt roles](../../docs/prompt-roles.md). Write each prompt with the setup's prompt writer.

## Filling the templates

- `{{references_line}}` says what each attached image is, in order, such as "The first attached image is the user's sketch: keep its pose and the main shapes of its design, redrawn cleanly in this look. The last attached image is the concept's style sheet: match its line, colour, and light, not its subjects." With nothing attached, it is empty.
- `{{style_sheet_line}}` is " The last attached image is the concept's style sheet: match its line, colour, and light." when one is sent; otherwise it is empty.
- `{{references_list}}` names each attached image on its own line, in the order sent, such as "1. Direction A, which leads."
- **For a character or a creature,** `{{stance}}` is "full body, standing in a relaxed pose that shows its character", and `{{identity_features}}` is "face, hair, eyes, skin, and markings" as it has them.
- **For a prop or a vehicle,** `{{stance}}` is "at rest on a level surface", and `{{identity_features}}` is its shape, parts, and markings.
- **For a place,** `{{concept_kind}}` is "concept painting", `{{aspect_ratio}}` is "16:9", and `{{identity_features}}` is its layout, architecture, and materials. For any other subject, `{{concept_kind}}` is "concept design" and `{{aspect_ratio}}` is "3:2".
- `{{must_not}}` is the brief's must-nots as one plain sentence, or empty.

## 1. The brief

Fill [the concept brief template](templates/concept-brief.md) from the request, the script's scenes, the sketches, and the style guide's rules, quoted. It ends with three or four **directions**, each one or two lines saying how it answers the brief differently from the others.

Show the brief to the user; their corrections win. They may add, drop, or rewrite directions before anything is made.

## 2. The directions

First, explore. Concept art is created with a text-to-image workflow. A concept-stage image is written from the concept context template, word for word, with only two things added:
- **a premise,** in as few words as possible, such as "two dogs talking seriously";
- **its purpose,** such as "16:9 concept illustration".

Add nothing else. No style words, no description of the character or the place, no lighting or composition, and no negative prompt unless the user asks for one. The fewer words, the better, because the context template works best when the rest is left to the model's interpretation. Make many candidates, eight or more, each with a new seed, so each is a different interpretation, the way an artist explores. The point is to find what the concept should be, not to get an exact picture. Exact, consistent prompts come later, once a concept is chosen.

For a character design, leave out the template's "rule of thirds" and its line on characters as minimal painted geometric masses: a character design is centred and clear. Fill [the concept context template](templates/concept-context.md) with the premise, such as "a tired diner cook" or "a roadside diner at night", and its purpose: "16:9 concept illustration" for a place or a moment, or "concept character design" for a subject. Plan the candidates, render them on the user's yes, and show them with the exact prompt sent. The user picks the candidates worth developing.

**Text gives context only where no image does,** as the [prompt roles](../../docs/prompt-roles.md) say.

Then, for the picks, make one image per direction, to settle the design.

- For a character, a creature, a prop, or a vehicle, fill [the design template](templates/concept-design.md); for a place, fill [the place template](templates/concept-place.md). Only the direction's lines change between them.
- Send the user's sketches first, in the order the brief lists them, and the style sheet last, when there are any.
- Plan the directions, render them on the user's yes, and report each output's path, named by its direction's letter.
- Inspect each against the brief and the style guide's rules, and report honestly where it breaks them, or where two directions came out alike.

The user chooses one direction, asks for a mix, or asks for new directions; never choose for them. New directions are a new plan.

## 3. Refine

When the user asks for a mix or changes, fill [the refine template](templates/concept-refine.md):

- send the chosen direction whose design leads first, then any other chosen direction, then the sketches, then the style sheet last;
- say what to take from each, such as "the silhouette and coat of the first; the hat and colours of the second";
- say what must not change.

Each round is a new paid request, and needs the user's yes. Inspect it against what the user asked for, and report drift honestly. Repeat until the user says the design is settled.

## 4. Hand back

Record in the brief's Chosen design section which image the user settled on, what they took from each direction, and the date.

Hand back to the caller:

- the settled design, as the input images for the subject's reference, or the place's;
- the brief, with the user's choice recorded;
- the other directions, kept for the record, not as references.

A settled design goes on to be made canonical, through `make-canonical`. The subject's reference is drawn from the settled design, and holds it from then on; the concept art is not sent with later images once the reference exists.
