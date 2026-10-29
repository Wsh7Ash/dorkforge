---
name: negative-result-logging
description: "Log the dorks that found nothing, because a clean query is evidence about coverage. Use when a session runs many templates and only some produce hits"
pack: dorkforge
version: 1.0.0
category: bug-bounty-tooling
tags: [report, coverage, logging]
---

# Negative Result Logging

> Log the dorks that found nothing, because a clean query is evidence about coverage

**Use when:** a session runs many templates and only some produce hits

**Avoid when:** a single template was run and the outcome is obvious

## Procedure

1. Record every template run with its variables and result count
2. Mark zero-result runs explicitly, with the date
3. Note whether a positive control passed for that template
4. Group negatives by artifact class to show coverage
5. Reference the log in the report's methodology
6. Re-run a sample of negatives after the pack changes

## Signals

- the log shows one line per template run
- zero-result runs record the control status
- coverage claims in the report match the log
- a template that starts producing hits shows in a later entry

## Patterns

**1. One line per hit**

```text
env-file-exposed site:example 0 results, control ok
```

**2. Coverage**

```text
12 templates run, 4 hits, 8 clean with controls
```

**3. Rerun check**

```text
clean templates re-checked after a pack update
```

## Pitfalls

- Recording only hits, which makes coverage unverifiable
- Logging a zero result without stating whether the control passed
- Treating an unproven zero as evidence the artifact is absent

## Done when

- every template run has a line with its count and control status
- the report's coverage claims match the log

## References

- [OWASP - reporting](https://owasp.org/www-project-web-security-testing-guide/)
- [NIST - documentation](https://csrc.nist.gov/)
