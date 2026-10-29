# Usage

## Install

```bash
git clone https://github.com/Wsh7Ash/dorkforge
cd dorkforge
python -m pip install -e ".[dev]"
dorkforge --version
```

Without installing, prefix every command with `PYTHONPATH=src python -m dorkforge`.

## A hunt, start to finish

### 1. State the intent

Before any query, write the exposure and how you would recognise it. The
`frame` phase skills cover this; the short version is one sentence plus a proof
and a refutation observable.

### 2. Pick a template

```bash
dorkforge templates --tag secret --risk low --verbose
dorkforge templates --tag vcs
```

Each entry shows its intent, so you are choosing a purpose rather than a string.

### 3. Fill and compile

```bash
dorkforge compile --template git-config-exposed --target api.example.test
```

```text
site:api.example.test inurl:"/.git/config"
https://www.google.com/search?q=site%3Aapi.example.test+inurl%3A%22%2F.git%2Fconfig%22
```

Missing a variable exits `2` and names it:

```text
$ dorkforge compile --template git-config-exposed
missing variables: {target}
```

### 4. Cross-check portability

```bash
dorkforge explore 'site:{target} inurl:"/.env"'
```

If the intent also fits a code index or a service index, compile the authored
DSL for each engine and keep whichever versions succeed. Refusals are
information: they tell you the constraint does not exist there.

### 5. Run the query and triage results

Index results are a snapshot. `triage` phase skills cover the traps: index
versus live, snippet versus content, lookalikes, and the count sanity check that
catches a query that silently dropped a constraint.

### 6. Confirm inside scope only

A hit is a hypothesis. The `validate` and `target` phase skills describe the
minimal direct check: one request, a status and a redacted sample, never a dump.
Read `SECURITY.md` before this step.

### 7. Report

Impact first, then the minimal reproduction, then the exact search URL and the
date it was run. The `report` phase has six skills for this, including redaction
and scope referencing.

## Authoring your own dork

```bash
dorkforge compile 'site:{target} inurl:"/admin" -inurl:"/admin/docs"' --target api.example.test
dorkforge explore 'filetype:sql intext:"INSERT INTO" site:{target}'
```

Rules the parser enforces:

- quotes must balance;
- a known field cannot be empty (`site:` is an error, not an empty constraint);
- unknown fields are rejected with the list of known ones;
- `OR` / `AND` / `NOT` must be upper case to be treated as operators.

## JSON output for scripting

```bash
dorkforge compile 'site:{target} inurl:"/.env"' --target api.example.test --json
dorkforge explore 'org:"Acme" port:9200' --json
dorkforge templates --json
dorkforge validate --json
```

Exit codes: `0` success, `1` a refused or unparsable dork (with a reason on
stderr), `2` missing template variables or unknown template.

## Working with the skills

```bash
dorkforge list --phase triage
dorkforge search index freshness
dorkforge show index-freshness-model
```

The same 50 skills are plain files under `skills/`, so any `SKILL.md` consumer
can load them directly. To serve them over MCP, see
[skillmcp](https://github.com/Wsh7Ash/skillmcp).

## Regenerating the pack

```bash
dorkforge build          # writes skills/, pack.json, results/validation.json
dorkforge validate       # after any corpus edit; fails on disk drift
python -m pytest -q
```
