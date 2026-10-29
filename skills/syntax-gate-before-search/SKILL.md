---
name: syntax-gate-before-search
description: "Validate the dork before it reaches an engine, so a typo cannot masquerade as a clean result. Use when a query is about to be compiled or pasted into a search box"
pack: dorkforge
version: 1.0.0
category: bug-bounty-tooling
tags: [validate, syntax, gate]
---

# Syntax Gate Before Search

> Validate the dork before it reaches an engine, so a typo cannot masquerade as a clean result

**Use when:** a query is about to be compiled or pasted into a search box

**Avoid when:** the query is a single bare word with no operators

## Procedure

1. Run the validator and read every reported problem
2. Fix unbalanced quotes before anything else
3. Fix unknown fields, since they would silently become plain text
4. Check that no field has an empty value
5. Compile for the chosen engine and read the produced query
6. Run the search only after both checks pass

## Signals

- the validator returns no problems
- the compiled query contains every field you wrote
- no field survives as a bare word after compilation
- the query that runs is the query the compiler printed

## Patterns

**1. Syntax gate**

```text
validate then compile, never compile alone
```

**2. Empty value**

```text
site: with nothing after the colon is an error
```

**3. Typo catch**

```text
unknown field 'intitle2' rejected with the known list
```

## Pitfalls

- Skipping validation because the query looks fine to a human
- Letting an unknown field pass and treating the noise as evidence
- Editing the compiled query afterwards and re-running without validation

## Done when

- validation and compilation both pass before the search runs
- the executed query matches the compiler output exactly

## References

- [Google - search operators](https://support.google.com/websearch/answer/2466433)
- [Shodan - query fundamentals](https://help.shodan.io/the-basics/search-query-fundamentals)
