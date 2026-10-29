---
name: distinguish-index-from-live
description: "Separate what the index remembers from what the server serves now, because they are different claims. Use when a finding would be reported from index data alone"
pack: dorkforge
version: 1.0.0
category: bug-bounty-tooling
tags: [triage, evidence, freshness]
---

# Distinguish Index From Live

> Separate what the index remembers from what the server serves now, because they are different claims

**Use when:** a finding would be reported from index data alone

**Avoid when:** the artifact is live and confirmed by a direct response

## Procedure

1. State the claim twice: what was indexed and what is served
2. Check the snippet date if the engine provides one
3. If permitted, confirm the live state with one request
4. Record both states separately in the evidence
5. Decide which claim the report will make
6. Avoid asserting the live state from index data

## Signals

- the index explains how the artifact was discovered
- the live response either confirms or contradicts the snippet
- the report distinguishes discovery from confirmation
- a removed artifact is described as historically indexed

## Patterns

**1. Two claims**

```text
indexed 2026-10-20, served 2026-10-29 status 200
```

**2. Historical note**

```text
no longer served but indexed, reported as historical
```

**3. Report wording**

```text
publicly indexed and retrievable at the time of writing
```

## Pitfalls

- Writing that a file exists now because it appears in a snippet
- Discarding a historical exposure that still matters for data already leaked
- Conflating a cache with a live response

## Done when

- index state and live state are recorded as separate claims
- the report's wording matches the strongest claim actually supported

## References

- [Google - cached pages](https://support.google.com/websearch/answer/1682912)
- [OWASP - evidence handling](https://owasp.org/www-project-web-security-testing-guide/)
