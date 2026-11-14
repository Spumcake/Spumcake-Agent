# Skill categories

Every skill belongs to one category, by what it produces and how that can be checked. A category's skills have the same parts, so they cover their ground the same way. Read this before choosing, writing, or renaming a skill; [write-skill](../skills/write-skill/SKILL.md) writes a new one from it.

## Names

A skill's name starts with its category's word, then says what it makes, in lowercase joined by hyphens, such as `generate-keyframe` or `write-voice-brief`. A sorted list of skills is grouped by category. A `write` skill that builds a prompt for a language model, rather than writing the result itself, ends in `-prompt`, such as `write-script-prompt`.

A skill does the work of one category. A task that needs two, such as writing a document and then generating images from it, is a `make` skill that plans one request of each.

## The categories

| Category | Produces | Skills |
|---|---|---|
| **build** | a result made by a script or a simple 3D builder, with no generative model, so the same inputs make the same result again; the only skills with scripts | `build-animatic`, `build-line-up`, `build-previs` |
| **fix** | an existing result repaired from its review's findings, each fixed where the error came from, by removals only | `fix-canonical-image` |
| **generate** | images or sounds from a generative model, sent a prompt and reference files | `generate-background`, `generate-board`, `generate-canonical-image`, `generate-concept-artwork`, `generate-concept-design`, `generate-concept-reference`, `generate-detail-sheet`, `generate-keyframe`, `generate-model-sheet`, `generate-sound`, `generate-subject-dataset`, `generate-subject-reference`, `generate-voice` |
| **make** | one finished thing, planned as requests of other categories, with the user's approvals between them | `make-canonical`, `make-colour-script`, `make-style-guide` |
| **project** | one folder of a project, kept by the one skill that owns it, as [projects.md](projects.md) describes | `project-brief`, `project-library`, `project-output`, `project-pipeline`, `project-requests` |
| **prompt** | nothing of its own: the rules for wording a prompt for one kind of model, which other skills follow | `prompt-image` |
| **research** | material gathered from outside, such as the web, photographs, and films, each item with its source and the use allowed | `research-references` |
| **review** | a report of every difference between results or documents and what they must agree with; it never fixes, scores, or decides | `review-consistency`, `review-continuity` |
| **write** | a document, such as a brief, a story document, or a floor plan, drafted by the agent, or by a language model from a prompt the skill builds; or, for `write-skill`, a skill | `write-audio-identity-brief`, `write-beat-sheet-prompt`, `write-breakdown-prompt`, `write-floor-plan`, `write-mood-brief`, `write-script-prompt`, `write-shot-list-prompt`, `write-skill`, `write-sound-design-brief`, `write-timing-reference`, `write-visual-identity-brief`, `write-voice-brief` |

The order the skills run in to make a film is in [the pipeline](pipeline.md).

## What every skill has

- **Its front matter:** `name`, and a `description` that says what it makes, when to use it, and what it is not for.
- **What a good result is, and a failed one,** in a few sentences, so the agent can tell them apart.
- **What it needs:** each input by its canonical name, as the pipeline's table names it, such as `the diner: far-end layout` or `the front door: side in the far-end frame`, never by a file path or a folder.
- **Its method,** in numbered steps, with the user's yes before anything that costs money.
- **Its hand-back:** exactly what it returns to [project-requests](../skills/project-requests/SKILL.md), as its category below gives it.

No skill saves, copies, renames, or moves a file, writes a record, names a project folder, or says where a result goes. It returns its result: `project-requests` runs a request to a model and reports it; `project-library` files what no model made.

## What each category takes and returns

- **build:** takes canon by name and the script to run. Returns the build, which is not a request: the script's command and the files it makes, which `project-library` files into `prompts/resources/` with `request.py build`. A project's own script, such as a place's pre-vis builder, is itself a resource, so the chain can run it again.
- **fix:** takes a result and its review's findings. Returns one request per fix, each a removal at the source of its error: in the pre-vis or in the generation.
- **generate:** takes canon by name. Returns the request: the endpoint kind it needs, the prompt as a template naming canon, `{{<element>: <fact>}}`, and the references by canonical artifact, each with its role, in the order to send them.
- **make:** takes the thing to finish. Returns its plan: the requests it needs, in order, each with its skill, and where the user approves between them. It runs none itself.
- **project:** owns one folder; see [projects.md](projects.md).
- **prompt:** returns nothing. Other skills follow its rules while building a prompt.
- **research:** takes questions that come from the brief. Returns the research request: each file found, with its address, its page, and the use allowed, and its findings.
- **review:** takes a result and the canon it must agree with. Returns its findings, in its template: each difference, where it is, which canon it breaks, what it should be, and whether it blocks approval. It never fixes, scores, or decides.
- **write:** takes canon and intent by name. Returns the document as a draft, for the agent's own writing, which is not a request, or the prompt for a language model, which is; and the facts the document settles, by `<element>: <fact>`, for `project-pipeline` to publish. A section of the brief goes to `project-brief`; a canonical document, such as a floor plan or a style guide, to `project-library`, which files it into `prompts/resources/`.

## What the user is told

When a request to a model is done, `project-requests` tells the user what `request.py tell <id>` prints, the same for every category: what was asked and why, the endpoint, the references in the order sent, the canon read, the prompt as sent, the outputs, the cost, and the report. A review adds its findings; nothing else is added.
