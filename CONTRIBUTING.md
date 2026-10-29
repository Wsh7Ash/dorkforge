# Contributing

Thanks for helping. This repo has two kinds of contribution: code and skills.

## Setup

```bash
python -m pip install -e ".[dev]"
python -m pytest -q
python -m dorkforge validate
```

Both commands must pass before you open a pull request.

## Adding or editing a skill

Skills live in [`src/dorkforge/corpus/`](src/dorkforge/corpus/) as plain dicts.
Do not edit `skills/**/SKILL.md` by hand: `build` rewrites them and `validate`
reports disk drift.

The validator enforces, per skill:

| Rule | Floor |
|---|---|
| steps | 6, each at least 25 chars |
| signals | 4 |
| patterns | 3, as `(label, code)` pairs |
| pitfalls | 3, each at least 30 chars |
| done-when | 2 |
| references | 1, `[label](https://...)` |
| summary | 40 chars |
| rendered words | 180 |

Also rejected: placeholder tokens (`TODO`, `TBD`, `lorem ipsum`), machine-local
paths, duplicate slugs or titles, and non-https references.

Write for an agent that has to act, not for a reader who wants background. Each
step should be something you could watch someone do.

## Adding a template

One dict in [`src/dorkforge/templates.py`](src/dorkforge/templates.py):

```python
{
    "id": "kebab-case-id",
    "title": "Human readable title",
    "intent": "the exposure this finds, in one sentence",
    "dork": 'site:{target} inurl:"/path"',
    "risk": "low",          # low | medium | high
    "tags": ["secret"],     # kebab-case
}
```

Use the DSL fields only; a template that cannot compile is a bug, and
`templates` output is checked by the tests.

## Adding an engine or field

1. Extend `FIELDS` in [`src/dorkforge/dsl.py`](src/dorkforge/dsl.py) with the
   operator each engine uses, or `None` where it has none.
2. Add the engine to `ENGINES` and its URL prefix to `SEARCH_URLS`.
3. Update the field table in `README.md` and the tests that enumerate engines.

## Style

- Python 3.10+, standard library only at runtime.
- Type hints on public functions; `from __future__ import annotations`.
- Docstrings explain *why* a rule exists, not what the line does.
- No network in tests. No `sleep`. No random seeds without an explicit seed.

## Reporting a problem

Open an issue with the command you ran, the output, and what you expected.
Security issues go through [SECURITY.md](SECURITY.md), not the issue tracker.
