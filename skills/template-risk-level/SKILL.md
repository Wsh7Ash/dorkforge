---
name: template-risk-level
description: "Classify a template's blast radius before running it, since some queries land on shared infrastructure. Use when a template targets cloud storage, service indexes or organisation-wide code"
pack: dorkforge
version: 1.0.0
category: bug-bounty-tooling
tags: [validate, risk, safety]
---

# Template Risk Level

> Classify a template's blast radius before running it, since some queries land on shared infrastructure

**Use when:** a template targets cloud storage, service indexes or organisation-wide code

**Avoid when:** the template only searches one host's own pages for a known path

## Procedure

1. Ask whose infrastructure the query would surface
2. Classify as low when results are pages on the target's own host
3. Classify as medium when results include shared cloud or service infrastructure
4. For medium templates, confirm the scope covers the infrastructure
5. Add a scoping field where possible to keep results on target
6. Record the risk level with the result set

## Signals

- the template's risk label matches whose hosts its results contain
- medium templates carry an extra scoping field
- results from shared infrastructure are identified and excluded
- the risk label appears in the evidence notes

## Patterns

**1. Low risk**

```text
site:{target} inurl:admin
```

**2. Medium risk**

```text
site:s3.amazonaws.com reserved for the org's own bucket names
```

**3. Scope guard**

```text
org filter or bucket naming convention added
```

## Pitfalls

- Running an organisation-wide service query against a shared provider
- Treating indexed metadata as harmless when it belongs to another tenant
- Skipping the risk label because the query is read-only

## Done when

- each template carries a risk level matching its blast radius
- medium templates are scoped or explicitly cleared against the brief

## References

- [HackerOne - scope](https://docs.hackerone.com/)
- [OWASP - testing scope](https://owasp.org/www-project-web-security-testing-guide/)
