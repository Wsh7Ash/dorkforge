---
name: passive-recon-boundary
description: "Keep index queries passive so no packet reaches the target during the discovery phase. Use when the program allows passive reconnaissance but restricts active scanning"
pack: dorkforge
version: 1.0.0
category: bug-bounty-tooling
tags: [frame, passive, scope]
---

# Passive Recon Boundary

> Keep index queries passive so no packet reaches the target during the discovery phase

**Use when:** the program allows passive reconnaissance but restricts active scanning

**Avoid when:** the engagement explicitly permits active enumeration on the listed assets

## Procedure

1. Read the program rules for language about scanning and automated tools
2. Classify each planned query as index-only or direct-to-target
3. Run index-only queries first and record what they reveal
4. Treat any query that fetches the target as an active test needing permission
5. Keep the two classes in separate files so they cannot be confused
6. Note the classification in the evidence for each finding

## Signals

- no request in the passive phase reaches the target's own infrastructure
- the passive file and the active file are clearly separated
- the program's scanning language is quoted in the notes
- any finding states which phase produced it

## Patterns

**1. Passive phase**

```text
search engine or code index queries only
```

**2. Active phase**

```text
a direct fetch of the discovered path
```

**3. Classification note**

```text
phase: passive, no traffic to target
```

## Pitfalls

- Opening a discovered URL during what you called passive recon
- Assuming a search engine's cache is a copy that never touches the origin
- Mixing passive and active results so the evidence trail is ambiguous

## Done when

- every query is labelled passive or active before it runs
- the program's scanning restriction is quoted in the notes

## References

- [OWASP - information gathering](https://owasp.org/www-project-web-security-testing-guide/)
- [HackerOne - policy guidance](https://docs.hackerone.com/)
