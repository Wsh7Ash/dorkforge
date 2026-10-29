---
name: ownership-verification
description: "Prove the discovered host belongs to the target before treating the result as theirs. Use when a hit lands on a host whose ownership is inferred from its name"
pack: dorkforge
version: 1.0.0
category: bug-bounty-tooling
tags: [triage, ownership, scope]
---

# Ownership Verification

> Prove the discovered host belongs to the target before treating the result as theirs

**Use when:** a hit lands on a host whose ownership is inferred from its name

**Avoid when:** the host appears verbatim in the program's asset list

## Procedure

1. Compare the hit's host against the scope list character by character
2. If absent from the list, look for ownership evidence in the response
3. Check certificate subject and DNS delegation from public data
4. Look for the organisation's identifiers in the page or error pages
5. Record the ownership evidence or the absence of it
6. If ownership is unclear, report the fact rather than claiming the asset

## Signals

- the certificate subject names the organisation
- the page footer carries the organisation's legal entity
- the host resolves to the organisation's own address space
- the host is a shared provider with a custom domain

## Patterns

**1. Scope match**

```text
exact host string in the asset list
```

**2. Certificate**

```text
subject CN and SANs recorded
```

**3. Unclear ownership**

```text
owned by a provider, no organisation identifier present
```

## Pitfalls

- Assuming a subdomain belongs to the target because it resolves under their domain
- Reporting a partner's branded host as the target's asset
- Skipping the check because the name looks right

## Done when

- ownership evidence is recorded for every reported host
- unclear ownership is stated as unclear, not inferred

## References

- [HackerOne - scope](https://docs.hackerone.com/)
- [RFC 5280 - certificates](https://www.rfc-editor.org/rfc/rfc5280.html)
