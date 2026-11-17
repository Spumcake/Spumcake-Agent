# The setup

The skills name no key, price, or computer. A **setup** gives them: one UTF-8 JSON file, `format` `setup-v1`, that the scripts here read. It names key files, never keys. A relative path in it is relative to the file.

`scripts/request.py` and `scripts/pipeline.py` find it in this order:

1. `--setup <file>` on the command;
2. the `SKILLS_SETUP` environment variable;
3. `~/.config/spumcake-skills/setup.json`.

An application such as Spumcake Studio writes its own setup file and passes it as `SKILLS_SETUP` to every script it runs. An agent's harness can do the same, or keep one at the third place.

## The keys request.py reads

```json
{
  "format": "setup-v1",
  "env_file": "<a file of NAME=value secrets>",
  "openai_key": "<a file holding the OpenAI key>",
  "openrouter_key": "<a file holding the OpenRouter key>",
  "fal_key": "<a file holding the fal key>",
  "credentials_dir": "<a folder holding .<service>/credentials>",
  "prices": {
    "fal": { "minimax/h3-max/reference-to-video": { "per_minute": 4.8 } },
    "openrouter": { "openai/gpt-image-2.5-sunburst": { "per_request": 0.05 } }
  }
}
```

A tool reads only the keys it needs, and ignores the rest, so one setup file serves several tools.

**A service's key** is looked for in this order, and the first found is used:

1. its environment variable: `OPENAI_API_KEY`, `OPENROUTER_API_KEY`, or `FAL_KEY`;
2. `--key-file <file>` on the command;
3. `env_file`, by the same variable's name;
4. `<service>_key`: `openai_key`, `openrouter_key`, or `fal_key`;
5. `credentials_dir`, as `<credentials_dir>/.<service>/credentials`.

When none holds it, the request stops before anything is sent, and names the variable to set.

**A builder gets no key.** `request.py build`, and `pipeline.py rerun` of a script step, run the project's own builder, such as an ffmpeg command or a pre-vis script, without those three variables, or any other whose name ends in `KEY`, `KEY_ID`, `SECRET`, `TOKEN`, `PASSWORD`, or `CREDENTIALS`. Only Skills' own scripts receive a key. This keeps keys out of the builder's environment; it is not a sandbox, so a builder still runs as the user, and is approved like any other code before it runs.

**Prices** are by service, `fal`, `openai`, or `openrouter`, then by the model's ID, each with `per_minute` (for a video, times its length), `per_request`, or `per_million_tokens`, as `{"input_text": …, "input_image": …, "output_image": …}` in dollars a million tokens, copied from the service's published prices. For a model priced by tokens, such as OpenAI's image models, the report records the token usage the endpoint returned and a cost computed from it and these prices, marked as computed, never a bill. `request.py plan` shows the estimate from them, then from the endpoint's own price in the spec. A missing price shows as unknown, never as zero, and a small price is printed with enough places that it never reads as zero.

## One computer's fallback

Until a computer's setup names its keys, `request.py` still finds them in the one folder that computer used before setups existed, and prints a warning each time it does. That fallback goes once every setup names its keys.
