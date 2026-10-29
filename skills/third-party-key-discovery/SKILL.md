---
name: third-party-key-discovery
description: "Find client-side third-party keys and then determine what the key actually permits. Use when the frontend embeds keys for maps, analytics or API gateways"
pack: dorkforge
version: 1.0.0
category: bug-bounty-tooling
tags: [target, keys, frontend]
---

# Third Party Key Discovery

> Find client-side third-party keys and then determine what the key actually permits

**Use when:** the frontend embeds keys for maps, analytics or API gateways

**Avoid when:** the frontend loads no third-party script with an embedded key

## Procedure

1. Identify the key shapes used by services the target loads
2. Search the target's own pages for those shapes
3. Extract the key from page source rather than from a screenshot
4. Determine the documented restrictions for that key type
5. Record what the key is scoped to, such as referrer or domain
6. Report only if the key exceeds its documented restriction

## Signals

- a key appears in page source with a known prefix
- the key type has documented referrer or domain restrictions
- the service bills per request, so misuse is measurable
- the key is reused across several of the target's own properties

## Patterns

**1. Key shape**

```text
intext:"AIza" for a Google API key
```

**2. Restriction**

```text
key limited by HTTP referrer to the target's domain
```

**3. Escalation test**

```text
only if the scope permits, check a restricted endpoint
```

## Pitfalls

- Reporting any embedded key as a finding without checking restrictions
- Testing the key against endpoints the scope does not cover
- Publishing the full key in a report instead of a redacted sample

## Done when

- the key's documented restrictions are recorded
- the finding states whether the key exceeds those restrictions

## References

- [Google - API key restrictions](https://cloud.google.com/docs/authentication/api-keys)
- [OWASP - secret exposure](https://owasp.org/www-project-top-10-privacy-risks/)
