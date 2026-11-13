# Prompt roles

How Spumcake Agent's skills hand their prompts to whatever runs them. A skill here plans the work, writes its prompts, and leaves running a model to the setup it is used in, such as Spumcake Studio, the platform, or any agent with its own execution stack.

## Roles

A skill fills a prompt by role, never by a model's own argument names, so the same prompt fits any model that takes those roles. A model that names its inputs its own way, such as `first_frame`, says so in its own documentation, and a prompt for it uses those names.

**Fields** are text, each sent as written:

- `prompt`: what to make, in words;
- `negative`: what to avoid, when the model takes it;
- `text`: the exact words to speak;
- `voice`: a voice described in words;
- `lyrics`: the words to sing.

**Inputs** are files, each an ordered list:

- `references`: what the output should look or sound like: images of a character, an object, or a style; or a clip of a voice;
- `structure`: what the output follows: a sketch or a source image; a first frame, then a last frame; a source or control video; or a source speech recording;
- `audio`: sound the output must carry, such as the speech a lip-sync matches.

## What a setup provides

A skill here names no model, service, server, key, price, or command. The setup it runs in lists, for the agent:

- **the model's own documentation,** for the model the request names or the user chooses: its **workflow skill**, which says what is true of the model, such as which inputs it takes, its sizes and lengths, and its licence; and a **prompt skill** for each way of running it, which gives its syntax and limits. When the request names no model and more than one fits, ask.
- **a prompt writer,** which turns the skill's prompt into the file the model's runner reads;
- **a renderer,** which runs a written prompt, shows its plan and cost first, and saves what comes back beside the prompt. A setup may have an **execution skill** made for one of these skills, which says so by listing it under `implements`; that one renders for it.

When one is missing, say which and stop. Never do a step by hand because the setup lacks it.

## What every skill keeps

- Nothing renders, trains, downloads, or spends money before the user's yes to that specific plan. A yes to a plan never approves downloading a model.
- The user chooses keepers and judges results. A skill never scores a picture or a sound.
- Every proposal and every result is shown to the user with the whole prompt sent, word for word and never shortened, with its negative, its settings, and its cost, and every image or clip sent with it: shown, in the order sent, labelled by its place in that order, with its full path.
- Every prompt built from references is shown with its inspiration: a sheet of the references it drew from, each labelled with what was taken from it and why, which were left out and why, and, once rendered, its results beside them. The user gives feedback from the references, which a prompt alone hides.
- Every image or clip a step makes, and every sheet made from them, is given to the user by its full absolute path, every time it is mentioned, never by a link or a path relative to a folder: links to generated files often fail to open, and the user finds files by path.
- Every image prompt's words are written with `write-image-prompt`: labelled visual phrases, not prose, and nothing a picture cannot show.
- A prompt sent with references tells the model plainly what each attached image is, how it was made in the pipeline, and how the images relate, then what is needed, in the same words throughout. It speaks to a model about the process, never to an artist about a painting.
- Text describes what is wanted only when no image gives that context, as in a text-to-image request. A request that sends images never also carries text that describes what those images already show: the text and the images would compete as context. Its text says only what no attached image provides. The one exception is a reinterpretation, such as a place repainted in a style: it names each object the image holds only to say how its form is reduced, such as "blocky dispensers" or "receding red stools", never where it is.
- Every image of a character who reads as a minor stays ordinary and everyday. Nothing is sexual or suggestive, in any step, prompt, or caption.
- Use only images and recordings the user has the right to use this way. Show a recognisable real person, or use a real person's voice, only when the user confirms that the person agreed to this use, or a guardian did for a child. Never make anything that shows a real person doing or saying something they did not, to deceive anyone.
- A prompt to a language model is sent alone: only the saved prompt and its files, as a fresh request, so the answer depends on nothing but the prompt. When the agent itself is the language model, it answers the saved prompt alone, as if it had seen nothing else of the conversation.
- When a check of a model's answer fails, build a corrected prompt that says what was wrong, and run it again.
- Each step is made only from the latest approved results of the steps before it; a rejected round is never an input. Do only the step asked, and never design ahead of it. When a step fails, fix the skill that made it, then run the step again.
- Capitals, labels, and names stay out of a prompt, as `write-image-prompt` says.
- Long steps report progress, and say what is running and how long it takes before waiting.
- **The model knows nothing but what it is sent.** It has no character, prop, place, story, or canonical context of any kind beyond the prompt's words and the images attached. Our names mean nothing to it: "the front door", "Otis", "the far-end view", and "the line" are words from our documents, not things it has seen. The images are context too, and the strongest: what an image shows is never described again in words, since the two compete. So a prompt points at what the images show, as they show it, such as "the door in image 1, the door that has just opened", and says in words only what no image gives. The agent's job is to map what it knows, from the floor plan and the documents, onto what is actually in the images it sends, and to write the prompt from that mapping (the user, 2026-11-13).
- **Every file keeps a record,** as [records](records.md) defines it: a `.record.json` beside it saying what kind of file it is, its camera, what made it, what it was made from (each source with its role in the request, and the prompt), and its **contents**, each named thing in the frame by its floor-plan name, with where it is in the frame and its state, such as a door half open. A pre-vis render's record is written by the builder from the geometry; an image made from others inherits their contents, changed only where the request changed them, and adds what it put in, such as a character. Whatever renders a result writes its record with [`scripts/records.py`](../scripts/records.py), as [`scripts/generate.py`](../scripts/generate.py) does; files are copied or moved only with it, and its `check` comes back clean before a result is shown. Before writing a prompt, read the record of each image to be sent, to know what it shows and what each thing is. The records are the agent's, never sent to the model. The chain of `made_from` is the paper trail back to the geometry (the user, 2026-11-13).
- **Never the character's own left or right alone in a prompt.** "Over his right shoulder" alone is read as the frame's or the page's side, and sends heads and looks the wrong way. Point at a drawn thing instead, such as "towards the door in image 1"; where nothing is drawn, say the frame's or the page's side; and a hand named by the character's side is always named by the frame's side too, "his right hand, the hand on the left of the frame", which held (2026-11-11). "He turns slightly to his right" proved this on 2026-11-11, and "over his right shoulder" again on 2026-11-13.
- Before a step places or directs a character, it reads the place's **floor plan** (`create-previs`) to get its bearings: where each object is, what each is called, each camera, and each character's marks. Every position, facing, and look is decided there, in room terms, against named objects, such as "towards the front door"; a direction in a frame's terms, left or right, is worked out from the plan for that shot's camera, never invented. Every object is called by its floor-plan name, never "the door" in a place with several (the user, 2026-11-13).
- A skill calls whoever uses it **the user**.
