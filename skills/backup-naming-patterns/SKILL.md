---
name: backup-naming-patterns
description: "Search the suffixes and dates that backup tooling produces instead of guessing random names. Use when an application may have left a dated backup beside its live files"
pack: dorkforge
version: 1.0.0
category: bug-bounty-tooling
tags: [target, backup, naming]
---

# Backup Naming Patterns

> Search the suffixes and dates that backup tooling produces instead of guessing random names

**Use when:** an application may have left a dated backup beside its live files

**Avoid when:** the platform serves only from a build artefact with no writable directory

## Procedure

1. List the suffixes common tooling produces, such as bak, old, copy and dates
2. Combine the suffix with the likely application file name
3. Search the combination scoped to the host
4. Record hits with their extension and directory
5. Confirm a hit is a real backup by its size and content type, if fetching is allowed
6. Report the pattern that worked so the pack can be improved

## Signals

- results show the same base name with several suffixes
- dated names cluster around plausible deployment dates
- the extension matches an archive or dump rather than a page
- one host yields several backup variants

## Patterns

**1. Suffix pattern**

```text
site:{target} inurl:"config.bak"
```

**2. Dated name**

```text
site:{target} inurl:"backup-2026"
```

**3. Combination**

```text
site:{target} ext:sql inurl:backup
```

## Pitfalls

- Trying hundreds of guessed names, which becomes brute force
- Fetching a large archive to confirm it exists
- Reporting a backup without checking whether it is actually downloadable

## Done when

- the naming pattern is recorded from observed evidence
- hits are confirmed without downloading archive contents

## References

- [OWASP - backup file exposure](https://owasp.org/www-project-web-security-testing-guide/)
- [Google - filetype](https://support.google.com/websearch/answer/2466433)
