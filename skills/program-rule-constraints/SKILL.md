---
name: program-rule-constraints
description: "Quote the rules that shape the hunt so a legitimate finding is not disqualified on process. Use when the program restricts automation, data access or how findings may be disclosed"
pack: dorkforge
version: 1.0.0
category: bug-bounty-tooling
tags: [frame, rules, compliance]
---

# Program Rule Constraints

> Quote the rules that shape the hunt so a legitimate finding is not disqualified on process

**Use when:** the program restricts automation, data access or how findings may be disclosed

**Avoid when:** the engagement is a direct engagement with no published constraints

## Procedure

1. Copy the relevant rule text into the engagement notes verbatim
2. Translate each rule into a constraint on your query set
3. List the queries that the constraints forbid
4. Choose alternatives that reach the same intent within the rules
5. Keep the quoted rule beside the evidence for any affected finding
6. Re-read the rules when the program updates them mid-engagement

## Signals

- each constraint maps to a query that was changed or dropped
- the quoted rule appears in the evidence for restricted findings
- no query contradicts a quoted constraint
- rule changes are checked before each session

## Patterns

**1. Quoted rule**

```text
automated scanning of production is not permitted
```

**2. Constraint**

```text
index queries only, no directory brute force
```

**3. Alternative**

```text
use the template pack instead of a fuzzer
```

## Pitfalls

- Paraphrasing a rule so the constraint is looser than written
- Assuming a rule applies only to other researchers
- Reporting a finding without the rule context that framed the method

## Done when

- every constraint that shaped the hunt is quoted in the notes
- no executed query contradicts a quoted rule

## References

- [HackerOne - program policies](https://docs.hackerone.com/)
- [OWASP - engagement rules](https://owasp.org/www-project-web-security-testing-guide/)
