---
name: confirm-with-direct-request
description: "Treat an index hit as a lead and confirm it with one request, if the scope allows active testing. Use when a hit matters enough to report and the program permits fetching the asset"
pack: dorkforge
version: 1.0.0
category: bug-bounty-tooling
tags: [triage, confirmation, scope]
---

# Confirm With Direct Request

> Treat an index hit as a lead and confirm it with one request, if the scope allows active testing

**Use when:** a hit matters enough to report and the program permits fetching the asset

**Avoid when:** the program is passive-only, where the index result is the whole evidence

## Procedure

1. Confirm the hit's host is in scope for active testing
2. Send a single request to the exact URL from the result
3. Record status, content type and a size, not the full body
4. Compare against the snippet to see whether content changed
5. Stop at the first confirmation; do not enumerate siblings
6. Record the request and response as the finding's proof

## Signals

- the response status matches what the index implied
- content type confirms the artifact class the intent named
- a 401 or 403 means the artifact exists but is guarded
- the response differs from the snippet, indicating drift

## Patterns

**1. Single request**

```text
one GET of the exact indexed URL
```

**2. Minimal record**

```text
status, content-type, content-length only
```

**3. Stop rule**

```text
no sibling enumeration after confirmation
```

## Pitfalls

- Fetching the whole artifact to prove it exists
- Confirming a hit on a host the scope does not cover for active testing
- Enumerating neighbouring paths and turning confirmation into scanning

## Done when

- exactly one request confirms the hit, if active testing is allowed
- the recorded response is minimal and sufficient

## References

- [OWASP - testing scope](https://owasp.org/www-project-web-security-testing-guide/)
- [HackerOne - policy](https://docs.hackerone.com/)
