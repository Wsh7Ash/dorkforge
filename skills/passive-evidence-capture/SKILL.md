---
name: passive-evidence-capture
description: "Capture what the index showed, with its date, so a passive finding does not depend on the index later. Use when the finding rests on search results and the index will change"
pack: dorkforge
version: 1.0.0
category: bug-bounty-tooling
tags: [report, evidence, passive]
---

# Passive Evidence Capture

> Capture what the index showed, with its date, so a passive finding does not depend on the index later

**Use when:** the finding rests on search results and the index will change

**Avoid when:** the finding is proven by a live response you stored yourself

## Procedure

1. Store the query, engine, date and result count
2. Store the snippet text for the specific result
3. Store the result URL and the timestamp of the view
4. Note the cache date if the result exposes one
5. Avoid storing the full page from the cache unless permitted
6. Reference the stored record in the report rather than the live index

## Signals

- the record is enough to re-run the query later
- the snippet text is preserved verbatim
- the date appears in the evidence, not only in prose
- the report cites the record rather than a fresh search

## Patterns

**1. Record fields**

```text
engine, query, date, count, snippet, url
```

**2. Snippet verbatim**

```text
exact indexed text preserved
```

**3. Cite record**

```text
evidence record 3, captured 2026-10-29
```

## Pitfalls

- Citing a search that no longer returns the result
- Storing only a screenshot, which cannot be re-run
- Capturing more cached content than the report needs

## Done when

- the evidence record is reproducible and dated
- the report cites the record rather than describing it

## References

- [OWASP - evidence handling](https://owasp.org/www-project-web-security-testing-guide/)
- [NIST - evidence integrity](https://csrc.nist.gov/)
