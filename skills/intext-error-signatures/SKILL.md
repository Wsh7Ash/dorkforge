---
name: intext-error-signatures
description: "Search for error text that only a failing application would emit. Use when a stack trace or framework error would leak paths and versions if indexed"
pack: dorkforge
version: 1.0.0
category: bug-bounty-tooling
tags: [compose, intext, errors]
---

# Intext Error Signatures

> Search for error text that only a failing application would emit

**Use when:** a stack trace or framework error would leak paths and versions if indexed

**Avoid when:** the application renders friendly errors with no technical detail

## Procedure

1. Pick a signature that only a real error page contains
2. Quote it exactly, since traces have fixed wording
3. Scope to the target's host
4. Exclude pages that discuss the error rather than emit it
5. Sample results and check that the surrounding text is a trace
6. Record the signature and the framework it identifies

## Signals

- sampled pages show a trace rather than a tutorial
- the signature names a framework version
- results include file paths from the deployment
- excluding documentation removes most false positives

## Patterns

**1. Trace signature**

```text
"Traceback (most recent call last)"
```

**2. Framework page**

```text
intitle:"Whoops" intext:"Laravel"
```

**3. Exclusion**

```text
-inurl:blog -inurl:stackoverflow
```

## Pitfalls

- Matching a page that quotes the error instead of emitting it
- Confusing a cached debug page with a live one
- Reporting the trace as a finding without the paths it revealed

## Done when

- sampled results are verified to be error pages, not discussions
- the signature and the framework it identifies are recorded

## References

- [OWASP - error handling](https://cheatsheetseries.owasp.org/)
- [Google - exact phrase search](https://support.google.com/websearch/answer/2466433)
