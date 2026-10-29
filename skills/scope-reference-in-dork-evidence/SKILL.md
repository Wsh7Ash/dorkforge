---
name: scope-reference-in-dork-evidence
description: "Tie each passive finding to the scope line that authorised searching that asset. Use when the program lists assets and the finding came from a dork query"
pack: dorkforge
version: 1.0.0
category: bug-bounty-tooling
tags: [report, scope, audit]
---

# Scope Reference in Dork Evidence

> Tie each passive finding to the scope line that authorised searching that asset

**Use when:** the program lists assets and the finding came from a dork query

**Avoid when:** the engagement has a single asset and scope is unambiguous

## Procedure

1. Copy the exact asset entry from the scope table
2. Quote any rule that shaped the hunt, such as passive-only
3. Record the phase the evidence came from
4. Check the asset string matches the scope exactly
5. Attach the reference beside the query record
6. Update the reference if the program changes scope

## Signals

- each finding names the asset entry it belongs to
- the quoted rule explains why no direct request was sent
- the phase label matches the method used
- the asset string matches character for character

## Patterns

**1. Scope line**

```text
programme: example | asset: api.example.test
```

**2. Rule quoted**

```text
passive reconnaissance only
```

**3. Phase label**

```text
evidence from passive phase, no request to target
```

## Pitfalls

- Citing a wildcard when the hit is on a partner host
- Omitting the rule that made the method passive
- Reporting a hit on a host absent from the asset list

## Done when

- each finding carries programme, asset and phase
- any constraint that shaped the method is quoted

## References

- [HackerOne - scope](https://docs.hackerone.com/)
- [OWASP - engagement documentation](https://owasp.org/www-project-web-security-testing-guide/)
