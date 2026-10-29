---
name: dead-query-detection
description: "Notice when a query has stopped working because an operator was deprecated or a field renamed. Use when a query that used to return results now returns nothing across several assets"
pack: dorkforge
version: 1.0.0
category: bug-bounty-tooling
tags: [validate, maintenance, queries]
---

# Dead Query Detection

> Notice when a query has stopped working because an operator was deprecated or a field renamed

**Use when:** a query that used to return results now returns nothing across several assets

**Avoid when:** the target genuinely has no such content and you have other evidence for that

## Procedure

1. Test the query against a known-good asset where it used to work
2. Remove one operator at a time to find the one causing the failure
3. Check the engine's documentation for recent operator changes
4. Rewrite the query with the current syntax
5. Record the change and the date it was made
6. Add the rewrite to the template pack for future runs

## Signals

- the query returns results on an asset where it previously worked
- removing one operator restores results
- the engine's docs list the operator as deprecated
- the pack contains the corrected query

## Patterns

**1. Known-good control**

```text
run against an asset you have results for
```

**2. Bisect operators**

```text
drop one operator per run until results return
```

**3. Pack update**

```text
template rewritten, changelog entry added
```

## Pitfalls

- Concluding the exposure is gone when only the syntax broke
- Rewriting locally and leaving the shared pack broken
- Testing only against the failing asset so the cause stays hidden

## Done when

- the failing operator is identified on a known-good asset
- the pack carries the corrected query

## References

- [Google - search operators](https://support.google.com/websearch/answer/2466433)
- [GitHub - search syntax changes](https://docs.github.com/en/search-github)
