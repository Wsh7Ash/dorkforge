---
name: dsl-field-mapping
description: "Author the intent in shared fields and let the compiler choose each engine's operator. Use when the same hunt should run across a web engine, a code index and a service index"
pack: dorkforge
version: 1.0.0
category: bug-bounty-tooling
tags: [compose, dsl, portability]
---

# Dsl Field Mapping

> Author the intent in shared fields and let the compiler choose each engine's operator

**Use when:** the same hunt should run across a web engine, a code index and a service index

**Avoid when:** the hunt is single-engine and the operator names are already memorised

## Procedure

1. Write each constraint as a field and value pair in the DSL
2. Use site for host scoping, inurl for path, intitle for page title
3. Use filename and language for repository searches
4. Compile for each engine and read the reported rewrites
5. Replace any field the compiler refuses with an equivalent on that engine
6. Store the DSL source, not the compiled query, as the artifact

## Signals

- the compiler reports field to operator rewrites per engine
- an unsupported field produces a named error, not an empty result
- the DSL source is what gets version controlled
- compiling twice produces the same query

## Patterns

**1. Field pair**

```text
filetype:env site:{target}
```

**2. Rewrite mapping**

```text
filetype -> extension on github
```

**3. Stored source**

```text
templates/env-file-exposed.dork
```

## Pitfalls

- Editing the compiled query so the source and output diverge
- Assuming inurl and path mean the same thing to both engines
- Dropping an unsupported field silently and losing the constraint

## Done when

- the stored artifact is DSL, and compiled queries are reproducible
- each refused field has a documented engine-specific replacement

## References

- [GitHub - code search syntax](https://docs.github.com/en/search-github/github-code-search/understanding-github-code-search-syntax)
- [Shodan - search filters](https://help.shodan.io/the-basics/search-query-fundamentals)
