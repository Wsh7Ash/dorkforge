---
name: engine-selection
description: "Pick the engine that indexes the artifact you want, because operators do not transfer between them. Use when the target artifact could be a web page, a repository file or an exposed service"
pack: dorkforge
version: 1.0.0
category: bug-bounty-tooling
tags: [frame, engines, selection]
---

# Engine Selection

> Pick the engine that indexes the artifact you want, because operators do not transfer between them

**Use when:** the target artifact could be a web page, a repository file or an exposed service

**Avoid when:** the artifact type is already known and one engine obviously indexes it

## Procedure

1. Classify the artifact: page, code, service or document
2. Match the class to an engine: web search, code search, service search
3. Check which operators that engine actually supports
4. Compose in the shared DSL so the mapping is explicit
5. Compile for the chosen engine and read the rewrites the compiler reports
6. Record the engine with the query so a rerun uses the same index

## Signals

- the engine indexes the artifact class you are hunting
- the compiler reports field to operator rewrites for the chosen engine
- an unsupported field is refused rather than silently dropped
- the recorded engine matches the URL that was opened

## Patterns

**1. Web page**

```text
google with site and inurl
```

**2. Repository file**

```text
github with filename and language
```

**3. Service index**

```text
shodan with port and product
```

## Pitfalls

- Sending site: to a code search engine and getting nothing useful
- Assuming Shodan indexes page content the way a web engine does
- Composing per engine by hand and losing the intent when you switch

## Done when

- the artifact class and chosen engine are recorded together
- unsupported fields are named by the compiler, not discovered by silence

## References

- [Google - search operators](https://support.google.com/websearch/answer/2466433)
- [GitHub - code search syntax](https://docs.github.com/en/search-github/github-code-search/understanding-github-code-search-syntax)
