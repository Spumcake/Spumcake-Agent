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
- Every image of a character who reads as a minor stays ordinary and everyday. Nothing is sexual or suggestive, in any step, prompt, or caption.
- Use only images and recordings the user has the right to use this way. Show a recognisable real person, or use a real person's voice, only when the user confirms that the person agreed to this use, or a guardian did for a child. Never make anything that shows a real person doing or saying something they did not, to deceive anyone.
- Long steps report progress, and say what is running and how long it takes before waiting.
- A skill calls whoever uses it **the user**.
