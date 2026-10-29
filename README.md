# dorkforge

Write a hunt once in a small **DSL**, compile it to Google, GitHub and Shodan
syntax — and be told, loudly, when an engine cannot express it. Ships with
**50 validated skills** and **66 curated templates**.

A dork is an intent, not a string. `site: inurl: intitle:` mean one thing to
Google, another to GitHub's code search, and nothing at all to Shodan. dorkforge
keeps the intent in portable fields and lets each engine's compiler choose the
right operator, refusing instead of silently dropping a constraint.

```text
dorkforge compile 'site:{target} inurl:"/.env"' --target api.example.test
dorkforge explore 'org:"Acme" port:9200 product:elastic'
dorkforge compile --template git-config-exposed --target api.example.test --json
dorkforge templates --tag secret --verbose
```

```text
$ dorkforge compile 'site:{target} inurl:"/.env"' --target api.example.test
site:api.example.test inurl:"/.env"
https://www.google.com/search?q=site%3Aapi.example.test+inurl%3A%22%2F.env%22
```

## Refusal is the feature

```text
$ dorkforge explore 'org:"Acme" port:9200 product:elastic'
org:"Acme" port:9200 product:elastic
fields: org, port, product
google  unsupported: field 'org' does not exist on google; supported there: ext, filetype, intext, intitle, inurl, site
github  unsupported: field 'port' does not exist on github; supported there: ext, filename, filetype, inurl, language, org, path, repo, user
shodan  org:"Acme" port:9200 product:elastic
```

Note the GitHub line: `org` *is* supported there, but `port` is not, so the
whole dork is refused for that engine rather than half-translated. That is the
difference between "no results" and "no results because your constraint was
thrown away".

## Field map

| DSL field | Google | GitHub | Shodan |
|---|---|---|---|
| `site` | `site` | — | — |
| `inurl` | `inurl` | `path` | — |
| `intitle` | `intitle` | — | `http.title` |
| `intext` | `intext` | — | `http.html` |
| `filetype` / `ext` | `filetype` | `extension` | — |
| `filename` | — | `filename` | — |
| `path` | — | `path` | — |
| `language` | — | `language` | — |
| `repo` | — | `repo` | — |
| `user` | — | `user` | — |
| `org` | — | `org` | `org` |
| `hostname` | — | — | `hostname` |
| `net` | — | — | `net` |
| `port` | — | — | `port` |
| `country` | — | — | `country` |
| `server` | — | — | `server` |
| `product` | — | — | `product` |
| `has` | — | — | `has` |
| `os` | — | — | `os` |

```text
$ dorkforge fields
google  ext filetype intext intitle inurl site
github  ext filename filetype inurl language org path repo user
shodan  country has hostname intext intitle net org os port product server
```

## Templates

66 curated templates, each with an intent sentence and a risk level: 53 `low`
and 13 `medium`. `medium` means the query can reach infrastructure wider than a
single host and should only run where the program explicitly allows it.

```text
$ dorkforge templates --tag secret --verbose
env-file-exposed                   low    Exposed .env file
  intent: find a deployed dotenv file at the web root
  dork:   site:{target} inurl:".env" -intitle:"index of"
git-config-exposed                 low    Exposed .git/config
  intent: find a git directory served to the public
  dork:   site:{target} inurl:"/.git/config"
ssh-private-key                    low    Committed private key
  intent: find an id_rsa style key in a public repository
  dork:   filename:id_rsa "PRIVATE KEY"
```

## Commands

| Command | Purpose |
|---|---|
| `compile DORK` | Compile for one engine (`--engine`), print query, URL, rewrites and notes |
| `compile --template ID --target HOST` | Fill a curated template's variables and compile it |
| `explore DORK` | Terms, fields, per-engine outcome and every problem |
| `fields [--engine]` | The field map above, from the source of truth |
| `templates [--tag] [--risk] [--verbose]` | Browse the template pack |
| `validate` | Every corpus rule plus disk-sync check (`--json` for CI) |
| `list` / `show` / `search` | Browse the 50 skills by phase, slug or keyword |
| `build` | Regenerate `skills/`, `pack.json`, `results/` |

Templates fail closed: a missing variable exits `2` with the names of the
variables that were not supplied, so a pack can never be rendered half-filled.

## The 50 skills

| Phase | Count | Covers |
|---|---|---|
| `frame` | 9 | intent, passive boundary, scope mapping, index freshness, engine choice, false positives, program rules, ethics |
| `compose` | 9 | field mapping, quoting, negation, filetype, path vs filename, title and error-text signatures, templates, operators |
| `validate` | 8 | syntax gate, empty values, unsupported fields, engine capability, result-count sanity |
| `target` | 8 | asset selection, subdomain and cloud naming, VCS roots, API docs, third-party keys |
| `triage` | 8 | index versus live, dedupe, snippet reading, signal versus volume, negative results |
| `report` | 8 | impact first, minimal repro, search URL as evidence, scope reference, redaction |

```text
$ dorkforge validate
dorkforge: 50/50 skills valid
  ok  steps>=6 signals>=4 patterns>=3 pitfalls>=3 words>=180 refs canonical https
```

Every skill is a `SKILL.md` an agent can load: front matter with a trigger
description, then When to use / When not to use / Procedure / Signals / Patterns /
Pitfalls / Done when / References. `validate` enforces structural floors, so a
thin skill cannot ship.

## Install

```bash
git clone https://github.com/Wsh7Ash/dorkforge
cd dorkforge
python -m pip install -e ".[dev]"    # or: PYTHONPATH=src python -m dorkforge --help
python -m pytest -q
```

Python 3.10+, no runtime dependencies. `pytest` is the only dev dependency.

## Using the skills with an agent

Point Claude Code, opencode or any `SKILL.md` consumer at `skills/`. Ask for a
task, for example "find exposed git directories on this host", and the matching
skill's procedure is loaded. To serve packs over MCP instead, use
[skillmcp](https://github.com/Wsh7Ash/skillmcp).

## Safety

Index queries are passive, but a hit is not permission. Confirm only inside a
declared program scope, never collect other people's data to strengthen a
report, and read `SECURITY.md` before pointing this at a target.

## License

MIT.
