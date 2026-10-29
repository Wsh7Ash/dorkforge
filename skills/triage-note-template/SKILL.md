---
name: triage-note-template
description: "Keep one line per hit so a long result set stays reviewable and nothing is lost. Use when a query produced many candidates and each needs a decision"
pack: dorkforge
version: 1.0.0
category: bug-bounty-tooling
tags: [triage, notes, discipline]
---

# Triage Note Template

> Keep one line per hit so a long result set stays reviewable and nothing is lost

**Use when:** a query produced many candidates and each needs a decision

**Avoid when:** the query produced one candidate you are already verifying

## Procedure

1. Define the fields: host, url, artifact class, verdict, reason
2. Write one line per candidate as you review it
3. Use a small verdict set such as keep, drop, unclear
4. Record the reason for every drop, not only for keeps
5. Re-sort the notes by verdict before verification begins
6. Count the verdicts as the query's real yield

## Signals

- every candidate has a verdict and a reason
- the drop reasons cluster into a few classes
- the counts reconcile with the number of candidates reviewed
- the notes can be re-sorted by verdict without editing

## Patterns

**1. One line per hit**

```text
api.example.test /config.php keep: returns env pairs
```

**2. Verdict set**

```text
verdicts: keep, drop, unclear per reviewed hit
```

**3. Query yield**

```text
3 keep, 11 drop, 2 unclear from 16 candidates
```

## Pitfalls

- Recording only the interesting hits and losing the audit trail
- Using free text verdicts that cannot be counted
- Reviewing the same candidate twice because no line was written

## Done when

- every reviewed candidate has a verdict and a reason
- the verdict counts match the number of lines

## References

- [OWASP - reporting](https://owasp.org/www-project-web-security-testing-guide/)
- [NIST - documentation](https://csrc.nist.gov/)
