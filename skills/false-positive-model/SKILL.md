---
name: false-positive-model
description: "Decide in advance what a plausible-but-wrong result looks like for this query. Use when a class of results tends to look like exposure but usually is not"
pack: dorkforge
version: 1.0.0
category: bug-bounty-tooling
tags: [frame, triage, quality]
---

# False Positive Model

> Decide in advance what a plausible-but-wrong result looks like for this query

**Use when:** a class of results tends to look like exposure but usually is not

**Avoid when:** the query has one unambiguous observable and no lookalikes exist

## Procedure

1. Write the lookalike that will appear most often
2. Write what distinguishes it from the real target
3. Add a negative term to the query if the lookalike is filterable
4. Keep the unfiltered query too, so a filter cannot hide the real case
5. Record how many lookalikes appeared in the first page of results
6. Revisit the model when a result surprises you

## Signals

- the first page contains lookalikes the model predicted
- the distinguishing feature is checkable without touching the target
- the filtered query returns fewer but cleaner results
- the unfiltered query is retained for comparison

## Patterns

**1. Lookalike**

```text
documentation pages that mention .env without shipping one
```

**2. Distinguisher**

```text
a 200 with KEY=value pairs rather than prose
```

**3. Noise filter**

```text
add -inurl:docs to drop documentation paths
```

## Pitfalls

- Filtering so aggressively that the real case is excluded
- Treating a marketing page about misconfiguration as an exposure
- Skipping the unfiltered query and calling the clean results complete

## Done when

- the predicted lookalike is written before the first search
- both filtered and unfiltered queries are recorded

## References

- [OWASP - reporting](https://owasp.org/www-project-web-security-testing-guide/)
- [NIST - testing guidance](https://csrc.nist.gov/pubs/sp/800/115/final)
