# Skill categories

Every skill belongs to one category, by what it produces and how that can be checked. A category's skills have the same parts, so they cover their ground the same way. Read this before choosing, writing, or renaming a skill.

## Names

A skill's name starts with its category's word, then says what it makes, in lowercase joined by hyphens, such as `generate-keyframe` or `write-voice-brief`. A sorted list of skills is grouped by category. A `write` skill that builds a prompt for a language model, rather than writing the result itself, ends in `-prompt`, such as `write-script-prompt`.

A skill does the work of one category. A task that needs two, such as writing a document and then generating images from it, is a `make` skill that runs one skill of each.

## The categories

| Category | Produces | Skills |
|---|---|---|
| **build** | a result made by a script or a simple 3D builder, with no generative model, so the same inputs make the same result again; the only skills with scripts | `build-animatic`, `build-line-up`, `build-previs` |
| **fix** | an existing result repaired from its review's findings, each fixed where the error came from, by removals only | `fix-canonical-image` |
| **generate** | images or sounds from a generative model, sent a prompt and reference files | `generate-background`, `generate-board`, `generate-concept-artwork`, `generate-concept-design`, `generate-concept-reference`, `generate-detail-sheet`, `generate-keyframe`, `generate-model-sheet`, `generate-sound`, `generate-subject-dataset`, `generate-subject-reference`, `generate-voice` |
| **make** | one finished thing, carried through skills of other categories, with the user's approvals between them | `make-canonical`, `make-colour-script`, `make-style-guide` |
| **prompt** | nothing of its own: the rules for wording a prompt for one kind of model, which other skills follow | `prompt-image` |
| **research** | material gathered from outside, such as the web, photographs, and films, each item with its source and the use allowed | `research-references` |
| **review** | a report of every difference between results or documents and what they must agree with; it never fixes, scores, or decides | `review-consistency`, `review-continuity` |
| **write** | a document, such as a brief, a story document, or a timing reference, drafted by the agent, or by a language model from a prompt the skill builds | `write-audio-identity-brief`, `write-beat-sheet-prompt`, `write-breakdown-prompt`, `write-script-prompt`, `write-shot-list-prompt`, `write-sound-design-brief`, `write-timing-reference`, `write-visual-identity-brief`, `write-voice-brief` |

The order the skills run in to make a film is in [the pipeline](pipeline.md).
