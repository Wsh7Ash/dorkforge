---
name: intitle-signature
description: "Use page titles as a fingerprint for default installations and generated pages. Use when the target runs a product whose default pages have a recognisable title"
pack: dorkforge
version: 1.0.0
category: bug-bounty-tooling
tags: [compose, intitle, fingerprint]
---

# Intitle Signature

> Use page titles as a fingerprint for default installations and generated pages

**Use when:** the target runs a product whose default pages have a recognisable title

**Avoid when:** the product is heavily customised and titles are rewritten per customer

## Procedure

1. Find the default page title from product documentation
2. Quote the distinctive part of the title, not the generic words
3. Scope with the site field to stay on the target
4. Check that the title still appears on a fetched page if active testing is allowed
5. Add a negative term for documentation pages with the same title
6. Record the title string as the fingerprint used

## Signals

- results are default installations rather than marketing pages
- the title string appears verbatim in sampled results
- documentation pages dominate until a negative term is added
- the fingerprint distinguishes product versions where titles differ

## Patterns

**1. Default title**

```text
intitle:"Dashboard [Jenkins]"
```

**2. Scoped query**

```text
intitle:"phpMyAdmin" site:{target}
```

**3. Negation term**

```text
-inurl:docs -inurl:blog site:{target}
```

## Pitfalls

- Using a title so generic that unrelated products match
- Forgetting that a title can be translated for other locales
- Treating a title match as proof of the product version

## Done when

- the title fingerprint is recorded verbatim
- sampled results are confirmed to carry the title

## References

- [Google - search operators](https://support.google.com/websearch/answer/2466433)
- [OWASP - fingerprinting](https://owasp.org/www-project-web-security-testing-guide/)
