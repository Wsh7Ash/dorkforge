---
name: redaction-of-pii
description: "Redact personal data in dork evidence while keeping the shape that proves the exposure. Use when a hit contains emails, names, tokens or identifiers belonging to third parties"
pack: dorkforge
version: 1.0.0
category: bug-bounty-tooling
tags: [report, redaction, privacy]
---

# Redaction of Pii

> Redact personal data in dork evidence while keeping the shape that proves the exposure

**Use when:** a hit contains emails, names, tokens or identifiers belonging to third parties

**Avoid when:** the artifact contains no personal data at all

## Procedure

1. Identify which fields in the evidence are personal data
2. Replace each with a labelled marker that preserves the shape
3. Keep counts and field names, which prove the class of data
4. Remove full records and keep one redacted example
5. Scan the final artifact for patterns that survived
6. State in the report that data was redacted and why

## Signals

- the evidence shows field names and counts without values
- no email, phone or token string survives a pattern scan
- the redaction preserves enough shape to prove impact
- the report states that redaction occurred

## Patterns

**1. Redaction marker**

```text
"email": "[REDACTED-EMAIL]"
```

**2. Counts kept**

```text
4121 records, 6 fields, sample redacted
```

**3. Post-export scan**

```text
search the artifact for @ and for 16+ digit runs
```

## Pitfalls

- Attaching a full dump to prove an exposure
- Redacting so much that the finding becomes unprovable
- Leaving a personal email in the query URL itself

## Done when

- no personal data value survives in the evidence
- the remaining evidence still proves the data class

## References

- [OWASP - privacy risks](https://owasp.org/www-project-top-10-privacy-risks/)
- [GDPR - principles](https://gdpr-info.eu/)
