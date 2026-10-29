---
name: impact-before-reporting
description: "Decide what an exposure would let someone do before deciding that it is a finding. Use when a hit is confirmed and the report's severity is still undecided"
pack: dorkforge
version: 1.0.0
category: bug-bounty-tooling
tags: [triage, impact, severity]
---

# Impact Before Reporting

> Decide what an exposure would let someone do before deciding that it is a finding

**Use when:** a hit is confirmed and the report's severity is still undecided

**Avoid when:** the exposure is obviously critical, such as live credentials for production

## Procedure

1. List the data or capability the artifact exposes
2. Determine whether the data is already public elsewhere
3. Estimate who could reach it and with what effort
4. Check whether the artifact is a fixture, a decoy or a live secret
5. State the impact in one sentence using the artifact's content class
6. Drop the finding when the impact is only a naming convention

## Signals

- the artifact contains values that grant access elsewhere
- the data is not obtainable from any public source
- reaching it requires no credential at all
- the same content is deliberately published as documentation

## Patterns

**1. Impact sentence**

```text
an unauthenticated reader obtains production database credentials
```

**2. Live check**

```text
the exposed key still authenticates
```

**3. Drop reason**

```text
sample values are documented placeholders
```

## Pitfalls

- Reporting an exposed file without reading what class of data it holds
- Assuming a key works without a scoped, permitted check
- Inflating severity because the artifact type sounds serious

## Done when

- the impact sentence names data or capability, not the file type
- placeholder and fixture artefacts are excluded

## References

- [CVSS - specification](https://www.first.org/cvss/specification-document)
- [OWASP - risk rating](https://owasp.org/www-project-web-security-testing-guide/)
