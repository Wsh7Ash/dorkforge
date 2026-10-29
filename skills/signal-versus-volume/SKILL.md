---
name: signal-versus-volume
description: "Narrow a query until each page of results contains a plausible hit, not just a match. Use when a query returns thousands of results that are technically matches but useless"
pack: dorkforge
version: 1.0.0
category: bug-bounty-tooling
tags: [frame, precision, queries]
---

# Signal Versus Volume

> Narrow a query until each page of results contains a plausible hit, not just a match

**Use when:** a query returns thousands of results that are technically matches but useless

**Avoid when:** the result set is already small enough to read in one pass

## Procedure

1. Read the first page of results and count plausible hits
2. Identify what the plausible hits share that the noise does not
3. Add one narrowing term or field reflecting that shared trait
4. Re-run and compare plausible hits per page
5. Stop narrowing when a page yields at least one plausible hit
6. Record the final query and the page yield as the query's precision

## Signals

- plausible hits per page rises after each narrowing step
- the narrowing term is justified by observed results, not guessed
- the final query still returns at least one page of results
- the recorded precision explains how the query was tuned

## Patterns

**1. Yield measure**

```text
page 1: 2 plausible of 10 before, 6 of 10 after
```

**2. Narrowing term**

```text
add inurl:config after noticing all hits are config pages
```

**3. Stop rule**

```text
stop at one plausible hit per page
```

## Pitfalls

- Narrowing until the query returns nothing and calling the target clean
- Adding terms that reflect your assumption rather than the observed hits
- Reporting volume as if it were evidence of exposure

## Done when

- each narrowing step is justified by the previous page of results
- the final query's per-page yield is recorded

## References

- [Google - refine searches](https://support.google.com/websearch/answer/2466433)
- [OWASP - information gathering](https://owasp.org/www-project-web-security-testing-guide/)
