# Results

Every number below comes from a run on this machine against the committed corpus
and template pack.

## Environment

- OS: Windows (MSYS2 shell), Python 3.14.3
- Runtime: Python 3.10+ standard library only; `pytest` as dev dependency
- Network: none. `compile` builds a search URL and never opens a connection.

## Corpus gate

```text
$ python -m dorkforge validate
dorkforge: 50/50 skills valid
  ok  steps>=6 signals>=4 patterns>=3 pitfalls>=3 words>=180 refs canonical https
```

Phase distribution: `frame` 9, `compose` 9, `validate` 8, `target` 8, `triage` 8,
`report` 8 — 50 unique slugs, 50 unique titles, every rendered skill at or above
the 180-word floor.

## Test suite

```text
$ python -m pytest -q
...............................                                          [100%]
```

31 tests: corpus floors and disk-drift, DSL tokenising (quotes, negation,
operators, empty values, unparsable tails), compiler rewrites and refusals,
per-engine field maps, template variable filling, and a subprocess run of the
real CLI.

## Compiler demo

```text
$ python -m dorkforge compile 'site:{target} inurl:"/.env"' --target api.example.test
site:api.example.test inurl:"/.env"
https://www.google.com/search?q=site%3Aapi.example.test+inurl%3A%22%2F.env%22
```

```text
$ python -m dorkforge compile --template git-config-exposed --target api.example.test
site:api.example.test inurl:"/.git/config"
https://www.google.com/search?q=site%3Aapi.example.test+inurl%3A%22%2F.git%2Fconfig%22
```

The `{target}` placeholder is filled from the flag, and a template rendered
without `--target` exits `2` naming `{target}` rather than searching the whole
internet.

## Refusal demo

```text
$ python -m dorkforge explore 'org:"Acme" port:9200 product:elastic'
org:"Acme" port:9200 product:elastic
fields: org, port, product
google  unsupported: field 'org' does not exist on google; supported there: ext, filetype, intext, intitle, inurl, site
github  unsupported: field 'port' does not exist on github; supported there: ext, filename, filetype, inurl, language, org, path, repo, user
shodan  org:"Acme" port:9200 product:elastic
```

The Shodan compile is exact; the other two name the offending field *and* the
fields that engine does accept, so the fix is one edit away.

## Field map demo

```text
$ python -m dorkforge fields
google  ext filetype intext intitle inurl site
github  ext filename filetype inurl language org path repo user
shodan  country has hostname intext intitle net org os port product server
```

## Template pack

```text
$ python -m dorkforge templates
...
-- 66 templates
```

53 `low`, 13 `medium`, 0 `high` risk. Each template carries an intent sentence,
so the reason for a query survives longer than the query.

## Known limitations

- `compile` produces URLs and queries; it does not call any search API, and no
  result parsing is included. Fetching is the human's or another tool's job.
- Shodan results are service records, not page content; the `intext` mapping to
  `http.html` only searches what Shodan already crawled.
- Quoted values are preserved verbatim, but no engine-side escaping of embedded
  quotes is attempted — a value containing `"` must be split by the author.
- GitHub code search requires authentication in a browser; the generated URL
  opens the search UI, it is not an API call.
