---
name: asset-scope-mapping
description: "Map each query variable to an in-scope asset so a wildcard never points at someone else's host. Use when a template takes a domain, org or product variable that will be substituted"
pack: dorkforge
version: 1.0.0
category: bug-bounty-tooling
tags: [frame, scope, variables]
---

# Asset Scope Mapping

> Map each query variable to an in-scope asset so a wildcard never points at someone else's host

**Use when:** a template takes a domain, org or product variable that will be substituted

**Avoid when:** the hunt uses no variable and every query is fully literal

## Procedure

1. Write the in-scope list from the program brief
2. Write the exclusions, including shared infrastructure and partner domains
3. List every variable a template expects and what fills it
4. Fill variables only from the in-scope list
5. Fill wildcard variables with the narrowest form that still works
6. Re-check the filled query against the exclusion list before running it

## Signals

- every substituted value traces to a line in the scope brief
- no wildcard covers a partner domain
- exclusions are checked after substitution, not before
- the filled query is stored with the asset it targeted

## Patterns

**1. Variable fill**

```text
{target} = api.example.test, not *.example.test
```

**2. Exclusion check**

```text
cdn.example.net excluded: shared infrastructure
```

**3. Scope trace**

```text
scope ref PROGRAM-123, asset api.example.test
```

## Pitfalls

- Using a wildcard because it finds more, and landing on a partner host
- Filling a variable from a search result rather than the scope brief
- Forgetting that an in-scope root domain may exclude specific paths

## Done when

- each variable substitution is traceable to a scope entry
- no filled query matches an exclusion

## References

- [HackerOne - scope](https://docs.hackerone.com/)
- [OWASP - testing scope](https://owasp.org/www-project-web-security-testing-guide/)
