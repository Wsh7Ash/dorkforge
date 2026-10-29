---
name: dedupe-findings
description: "Collapse results that share one root cause so a report has one finding instead of twenty symptoms. Use when many hosts or paths show the same exposure from one deployment mistake"
pack: dorkforge
version: 1.0.0
category: bug-bounty-tooling
tags: [triage, dedupe, reporting]
---

# Dedupe Findings

> Collapse results that share one root cause so a report has one finding instead of twenty symptoms

**Use when:** many hosts or paths show the same exposure from one deployment mistake

**Avoid when:** each hit has a distinct cause and would need a separate fix

## Procedure

1. Group hits by the artifact's content shape, not by hostname
2. Group again by the deployment pattern that would explain them
3. Pick the clearest instance as the representative
4. List the other affected hosts as scope, not as separate findings
5. Verify at least one other instance matches the representative
6. Record the grouping rule used

## Signals

- all instances share byte-identical content apart from host
- the hosts share a deployment platform or template
- one remediation would fix every instance
- instances differ enough to need separate fixes

## Patterns

**1. Grouping**

```text
same .env content shape across six staging hosts
```

**2. Representative**

```text
one capture plus a host list
```

**3. Split rule**

```text
different secrets per host means separate findings
```

## Pitfalls

- Submitting twenty near-identical reports and losing reviewer trust
- Collapsing genuinely different exposures into one report
- Listing hosts without confirming they show the same artifact

## Done when

- each finding represents one root cause with a host list
- at least one additional instance is confirmed to match

## References

- [OWASP - reporting](https://owasp.org/www-project-web-security-testing-guide/)
- [HackerOne - duplicate policy](https://docs.hackerone.com/)
