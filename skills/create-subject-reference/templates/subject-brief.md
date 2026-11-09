# Subject brief: {{name}}

Fill every field from the user's request and the input images. Write "not specified" rather than inventing, and "not applicable" for a field that does not fit the subject, such as hair on a vehicle. Keep it short: the brief feeds the reference sheets and the dataset, and anything not listed here should not appear in either.

## Identity

- **Name:**
- **Trigger word:** a short, unusual token for the LoRA, such as `miraoc`
- **Kind of subject:** a character, a creature, a prop, a vehicle, or another
- **Role or concept:** one line
- **Personality:** three to five words, for a character or creature
- **Signature expression:** the face it makes most, beyond the core set, for a character or creature

## Look

- **Art style:** when the concept has a style guide, its written rules, quoted; otherwise the style of the input images, in a few words (for example, flat 2D cel shading, clean black linework)
- **Hair:** colour, length, shape, for a character or creature
- **Eyes:** colour, shape, for a character or creature
- **Skin, fur, or surface:**
- **Build, shape, and proportions:** describe as drawn in the input images; do not add body measurements
- **Parts and materials:** for an object or vehicle, its main parts and what each is made of
- **Fixed traits:** what never changes between outfits or variants
- **Fixed tags:** the fixed traits, comma-separated, in the prompting style of the model family the LoRA is for (its workflow skill says which; for a tag-prompted family, for example `long hair, green hair, green eyes`); every caption and every prompt for the subject writes them after the trigger word

## Outfits or variants

One entry per outfit, or per version of the subject. The first is the default.

- **{{outfit}}:** every visible garment, colour, and detail, top to bottom; or, for another subject, what changes in this version

## Props

- **{{prop}}:** what it is, colour, material, and how it is held or worn

## Palette

Five to eight colours, named, in order of area.

## Input images

- `{{path}}`: what it shows (outfit, expression, prop)
