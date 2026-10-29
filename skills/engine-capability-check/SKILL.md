---
name: engine-capability-check
description: "Confirm the engine supports each field before trusting a zero-result answer. Use when a compiled query returns nothing and the cause is unclear"
pack: dorkforge
version: 1.0.0
category: bug-bounty-tooling
tags: [validate, engines, capability]
---

# Engine Capability Check

> Confirm the engine supports each field before trusting a zero-result answer

**Use when:** a compiled query returns nothing and the cause is unclear

**Avoid when:** the field set is already proven for that engine in this session

## Procedure

1. List the fields the query uses
2. Ask the compiler which fields the engine supports
3. Replace unsupported fields with that engine's equivalent
4. Re-run and compare the result count
5. If a field has no equivalent, rewrite the intent instead of dropping it
6. Record the substitution in the query notes

## Signals

- the compiler names the unsupported field rather than returning silence
- the rewritten query returns results where the original returned none
- the substitution preserves the intent
- the notes record which field changed and why

## Patterns

**1. Unsupported**

```text
site: on github has no equivalent
```

**2. Rewrite mapping**

```text
filetype -> extension for a code index
```

**3. Count comparison**

```text
0 with the wrong field, 14 after the rewrite
```

## Pitfalls

- Reading a zero-result answer as proof the exposure is absent
- Dropping the field instead of translating the intent
- Assuming a field means the same thing on every engine

## Done when

- every field in the query is supported by the chosen engine
- each substitution is recorded with its reason

## References

- [GitHub - code search syntax](https://docs.github.com/en/search-github/github-code-search/understanding-github-code-search-syntax)
- [Shodan - search filters](https://help.shodan.io/the-basics/search-query-fundamentals)
