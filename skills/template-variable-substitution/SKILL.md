---
name: template-variable-substitution
description: "Keep templates variable-driven so one pack works across every asset in scope. Use when a pack of dorks will be reused for several domains, orgs or products"
pack: dorkforge
version: 1.0.0
category: bug-bounty-tooling
tags: [compose, templates, reuse]
---

# Template Variable Substitution

> Keep templates variable-driven so one pack works across every asset in scope

**Use when:** a pack of dorks will be reused for several domains, orgs or products

**Avoid when:** a dork is a one-off for a single host and will never be reused

## Procedure

1. List the variables the pack needs, such as target, org and product
2. Write every template against those variables only
3. Reject a template that hardcodes a host
4. Render templates from a scope file rather than editing them
5. Validate the rendered query before running it
6. Version the pack, not the rendered queries

## Signals

- no template contains a literal domain
- rendering the same template for two assets produces two queries
- a missing variable is an error rather than an empty string
- the pack version is recorded with each result

## Patterns

**1. Variable**

```text
site:{target} inurl:".env"
```

**2. Render source**

```text
assets.yaml with in-scope hosts
```

**3. Missing variable**

```text
error: {target} is required
```

## Pitfalls

- Hardcoding a host in one template and copying it everywhere
- Substituting an empty string and searching the whole internet
- Editing rendered queries in place so the template drifts

## Done when

- every template is free of literal hosts
- a missing variable fails loudly

## References

- [Python - string formatting](https://docs.python.org/3/library/string.html)
- [OWASP - testing scope](https://owasp.org/www-project-web-security-testing-guide/)
