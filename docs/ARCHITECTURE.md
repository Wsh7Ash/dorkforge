# Architecture

dorkforge is three small layers over one idea: the artifact worth version
controlling is the *intent*, not any engine's punctuation.

```text
corpus/part1..part3.py   authored skill dicts (50)
        │
        ├── model.py     skill_from_dict -> frozen Skill
        ├── validate.py  structural + strength + hygiene rules
        └── render.py    Skill -> SKILL.md (front matter + sections)

templates.py             66 curated dicts: id, title, intent, dork, risk, tags
        │
dsl.py                   parse -> Term/Dork; compile_dork -> CompileResult
        │
cli.py                   compile / explore / fields / templates
                         validate / list / show / search / build
```

## The DSL

`parse` tokenises into `Term` objects of four kinds:

| Kind | Example | Meaning |
|---|---|---|
| `field` | `site:api.example.test` | a portable constraint |
| `phrase` | `"PRIVATE KEY"` | an exact string an engine must match |
| `word` | `elastic` | free text |
| `operator` | `OR` / `AND` / `NOT` | boolean glue, upper case only |

A leading `-` sets `negated`, and a quoted value sets `quoted`, which survives
into the compiled output so `inurl:"/.env"` keeps its quotes.

Parsing fails closed on: an empty dork, an unbalanced quote, an unknown field,
a known field with an empty value (`site:`), an unparsable tail, and a dork that
produced no terms. Every failure is a `DorkError`, which the CLI turns into a
non-zero exit with a fix in the message.

## Compilation

```text
FIELDS[field][engine] -> operator | None
```

Compiling walks the terms, looks up each field for the requested engine, and
raises on `None` — naming the fields that engine *does* support. A field whose
operator differs from the DSL name is reported in `rewrites` (`inurl -> path`),
so a reader can see the translation rather than trusting it.

`CompileResult` carries `engine`, `query`, `url`, `used`, `rewrites` and
`notes`. `notes` is where engine-shaped caveats live, for example that GitHub
has no `site:` and that Shodan indexes services rather than pages.

`compile_all` returns a `CompileResult` per engine, or the error string for the
engines that cannot express the dork. `explore` wraps that for the CLI and adds
`validate`'s problems, so one command answers "what does this mean everywhere".

## Templates

A template is data, not code: `id`, `title`, `intent`, `dork`, `risk`, `tags`.
Variables are `{target}`, `{host}`, `{org}`, `{product}`, `{country}`. The CLI
fills only the variables that were supplied and refuses to compile while any
remain, which is what keeps a template from becoming a query against the whole
internet.

`risk` is advisory ordering: `low` is scoped to one host, `medium` can reach
wider infrastructure, `high` is reserved for intents that should not run without
an explicit written allowance (none ship today).

## The corpus harness

The skill corpus is the same harness used by the other packs in this series:
skills authored as dicts, rendered to `SKILL.md`, validated against floors
(6 steps, 4 signals, 3 patterns, 3 pitfalls, 2 done-when, 180 words, canonical
https references), plus a disk-drift check so a hand-edited `SKILL.md` cannot
silently diverge from its source.

## Extension points

| Want to | Change |
|---|---|
| add an engine | extend `FIELDS` and `SEARCH_URLS`, then `ENGINES` |
| add a field | one row in `FIELDS`; `fields` and the compiler pick it up |
| add a template | one dict in `templates.py` |
| add a skill | one dict in `corpus/partN.py`, then `build` |
