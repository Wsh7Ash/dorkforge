---
name: batch-report-structure
description: "Structure a multi-finding report so the reader meets the strongest result first and the method last. Use when one session produced several related passive findings"
pack: dorkforge
version: 1.0.0
category: bug-bounty-tooling
tags: [report, structure, editorial]
---

# Batch Report Structure

> Structure a multi-finding report so the reader meets the strongest result first and the method last

**Use when:** one session produced several related passive findings

**Avoid when:** the session produced a single finding that needs no grouping

## Procedure

1. Order findings by impact rather than by discovery order
2. Group related findings under one root cause heading
3. Put the reproduction for each finding before its analysis
4. Put the method and coverage section at the end
5. Keep each finding to one page of evidence
6. Check that no finding depends on a section written later

## Signals

- the first finding is the highest impact one
- each finding has reproduction then analysis
- the method section explains coverage without repeating findings
- no cross-reference points forward to an unwritten section

## Patterns

**1. Ordering**

```text
impact first, method last
```

**2. Evidence budget**

```text
one page per finding
```

**3. Coverage**

```text
templates run and clean results listed at the end
```

## Pitfalls

- Ordering by discovery time, which buries the serious finding
- Repeating the whole method in every finding
- Letting one finding's evidence spill into another's section

## Done when

- findings are ordered by impact with grouped causes
- the method section accounts for coverage without repetition

## References

- [OWASP - reporting](https://owasp.org/www-project-web-security-testing-guide/)
- [HackerOne - report quality](https://docs.hackerone.com/)
