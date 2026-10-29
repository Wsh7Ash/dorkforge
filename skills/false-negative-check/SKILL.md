---
name: false-negative-check
description: "Prove the query can find a known case before trusting its failures. Use when a query returns nothing and the conclusion would be that the exposure is absent"
pack: dorkforge
version: 1.0.0
category: bug-bounty-tooling
tags: [validate, false-negative, controls]
---

# False Negative Check

> Prove the query can find a known case before trusting its failures

**Use when:** a query returns nothing and the conclusion would be that the exposure is absent

**Avoid when:** the result set is positive and the question is about the exposure rather than the query

## Procedure

1. Find or create a known instance the query should match
2. Run the query against that known instance
3. Confirm the known instance appears in the results
4. If it does not, fix the query before drawing any conclusion
5. Only then run the query against the target
6. Record the positive control alongside the target result

## Signals

- the known instance appears in the results
- the control uses the same engine and same query text
- the target result is interpreted only after the control passes
- the control case is recorded in the evidence

## Patterns

**1. Positive control**

```text
your own test deployment appears in the results
```

**2. Same query**

```text
control and target differ only in the site field
```

**3. Blocked conclusion**

```text
cannot conclude absence until the control passes
```

## Pitfalls

- Reporting absence from a query that was never proven to work
- Using a different query for the control so the comparison is invalid
- Building a control page on infrastructure you do not own

## Done when

- the query finds a known instance before it is used for absence claims
- the positive control is recorded with the target result

## References

- [OWASP - testing controls](https://owasp.org/www-project-web-security-testing-guide/)
- [NIST - testing guidance](https://csrc.nist.gov/pubs/sp/800/115/final)
