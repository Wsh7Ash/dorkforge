---
name: cloud-bucket-naming
description: "Derive the organisation's bucket naming convention, then search for it rather than guessing. Use when the target stores assets in object storage and names buckets predictably"
pack: dorkforge
version: 1.0.0
category: bug-bounty-tooling
tags: [target, cloud, naming]
---

# Cloud Bucket Naming

> Derive the organisation's bucket naming convention, then search for it rather than guessing

**Use when:** the target stores assets in object storage and names buckets predictably

**Avoid when:** the organisation uses opaque generated bucket names with no convention

## Procedure

1. Collect bucket names visible in the target's frontend or documentation
2. Identify the shared prefix or suffix pattern
3. Search for that pattern within the organisation's own namespace
4. Record each candidate with the source that suggested it
5. Do not probe bucket permissions during the passive phase
6. Report naming candidates as reconnaissance, not as findings

## Signals

- several known buckets share a suffix such as -assets or -backup
- candidate names follow the same convention as confirmed ones
- the search returns buckets only inside the organisation's namespace
- no permission probe was performed to confirm existence

## Patterns

**1. Convention**

```text
{org}-assets, {org}-backup, {org}-uploads
```

**2. Bucket search**

```text
"{org}-backup" site:s3.amazonaws.com
```

**3. Record fields**

```text
candidate from a JS bundle reference, not probed
```

## Pitfalls

- Guessing bucket names and probing them, which is active testing
- Searching a generic name and surfacing other tenants' buckets
- Reporting a naming convention as if it were an access control defect

## Done when

- the naming convention is documented from observed evidence
- candidates are recorded without any permission probe

## References

- [AWS - bucket naming rules](https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucketnamingrules.html)
- [OWASP - cloud storage exposure](https://owasp.org/www-project-web-security-testing-guide/)
