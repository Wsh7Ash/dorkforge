---
name: api-doc-discovery
description: "Find published API documentation, because it hands you the endpoint list and parameter shapes for free. Use when the target exposes an API and the client-side routes are unknown"
pack: dorkforge
version: 1.0.0
category: bug-bounty-tooling
tags: [target, api, documentation]
---

# Api Doc Discovery

> Find published API documentation, because it hands you the endpoint list and parameter shapes for free

**Use when:** the target exposes an API and the client-side routes are unknown

**Avoid when:** the API is documented in a public developer portal you already have

## Procedure

1. Search for documentation UI titles and machine-readable spec paths
2. Prefer the machine-readable document over the rendered UI
3. Record the spec version and the server it names
4. Extract endpoint paths and parameter names as the parameter surface
5. Check whether the spec lists servers that are not in the scope brief
6. Hand the extracted surface to the planning phase rather than testing inline

## Signals

- a spec document is reachable and parses
- the spec names internal servers or staging hosts
- the spec lists deprecated endpoints still served
- endpoint paths in the spec exceed what the UI calls

## Patterns

**1. Docs UI page**

```text
site:{target} intitle:"Swagger UI"
```

**2. Spec file**

```text
site:{target} inurl:"openapi.json"
```

**3. Extract surface**

```text
paths and parameters taken from the spec, not guesses
```

## Pitfalls

- Testing endpoints the spec lists but the scope excludes
- Treating the rendered UI as the authoritative source over the spec
- Missing deprecated endpoints that are listed but not documented

## Done when

- a spec document is captured with its servers and version
- the extracted surface is filtered against the scope before use

## References

- [OpenAPI - specification](https://spec.openapis.org/oas/latest.html)
- [OWASP API Security - inventory](https://owasp.org/API-Security/editions/2023/en/0xa9-improper-inventory-management/)
