---
name: cache-staleness-check
description: "Date every cached copy, because a snapshot proves history rather than current exposure. Use when the evidence for a finding is a search engine or archive cache"
pack: dorkforge
version: 1.0.0
category: bug-bounty-tooling
tags: [triage, cache, dates]
---

# Cache Staleness Check

> Date every cached copy, because a snapshot proves history rather than current exposure

**Use when:** the evidence for a finding is a search engine or archive cache

**Avoid when:** the finding rests on a live response you captured yourself

## Procedure

1. Locate the cache date or capture timestamp on the copy
2. Record it with a timezone if available
3. Compare against the target's current behaviour if permitted
4. Describe the copy as a snapshot at that date
5. Note whether the content has since been removed or guarded
6. Avoid attributing the snapshot's content to the present

## Signals

- the cache carries a visible date
- the live response contradicts the cached copy
- the copy references content that no longer exists
- the copy predates a known remediation

## Patterns

**1. Dated copy**

```text
cached 2026-09-14, live 404 on 2026-10-29
```

**2. Snapshot wording**

```text
as indexed on the stated date
```

**3. Contradiction**

```text
cache shows a config file, live host redirects to login
```

## Pitfalls

- Presenting cached content as a live exposure
- Ignoring the possibility that data was already exposed historically
- Reporting a cache of a page the target never served publicly

## Done when

- every cached copy is dated in the evidence
- the report's tense matches the snapshot rather than the present

## References

- [Google - cache](https://support.google.com/websearch/answer/1682912)
- [NIST - evidence integrity](https://csrc.nist.gov/)
