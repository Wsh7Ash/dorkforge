---
name: result-count-sanity
description: "Read the result count as a diagnostic, because a suspicious count usually means a broken query. Use when a narrowed query returns an implausibly large or small number"
pack: dorkforge
version: 1.0.0
category: bug-bounty-tooling
tags: [validate, counts, diagnostics]
---

# Result Count Sanity

> Read the result count as a diagnostic, because a suspicious count usually means a broken query

**Use when:** a narrowed query returns an implausibly large or small number

**Avoid when:** the engine does not expose a count and only shows pages

## Procedure

1. Record the count before and after each narrowing step
2. Compare against the expected order of magnitude for the artifact
3. Investigate a count that did not change after adding a constraint
4. Investigate a count that dropped to zero after a mild constraint
5. Check whether the engine is estimating rather than counting exactly
6. Record the counts as query metadata, not as evidence of exposure

## Signals

- the count falls by orders of magnitude after one added field
- the count is identical across queries with different constraints
- the engine reports an approximation rather than an exact total
- the count changes between two runs of the same query

## Patterns

**1. Count delta**

```text
site only: 48000, with filetype: 12
```

**2. Unchanged count**

```text
adding a term changed nothing, so it was ignored
```

**3. Estimate note**

```text
engine reports approximations above a threshold
```

## Pitfalls

- Quoting a result count as if it measured the number of vulnerable hosts
- Ignoring a count that did not move, which signals an ignored operator
- Comparing counts across engines as if they shared an index

## Done when

- counts are recorded per narrowing step
- an unchanged count is treated as a possible ignored operator

## References

- [Google - search results](https://support.google.com/websearch/answer/2466433)
- [Shodan - result totals](https://help.shodan.io/the-basics/search-query-fundamentals)
