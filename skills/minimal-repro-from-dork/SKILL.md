---
name: minimal-repro-from-dork
description: "Reduce a dork finding to a query plus one response, so a reviewer can reproduce it in two steps. Use when a passive finding is being written up for a triager"
pack: dorkforge
version: 1.0.0
category: bug-bounty-tooling
tags: [report, reproduction, minimal]
---

# Minimal Repro From Dork

> Reduce a dork finding to a query plus one response, so a reviewer can reproduce it in two steps

**Use when:** a passive finding is being written up for a triager

**Avoid when:** the finding needs a multi-step sequence to demonstrate impact

## Procedure

1. Choose the single query that finds the artifact with the fewest terms
2. Choose the single response that proves it
3. Write the two steps in order: query, then response
4. Remove extra hosts and extra terms that do not affect the result
5. Verify the reduced query still returns the artifact
6. Attach the reduced pair and keep the wider set as reference

## Signals

- the reduced query returns the same artifact
- the reproduction is two steps in the report
- the attachments contain only the pair
- the wider result set is clearly labelled as reference

## Patterns

**1. Two steps**

```text
1 run query, 2 observe response
```

**2. Reduced query**

```text
site and filetype only, no extra terms
```

**3. Reference set**

```text
full result list attached separately
```

## Pitfalls

- Attaching twenty results so the reviewer cannot find the relevant one
- Reducing the query until it no longer reproduces the artifact
- Describing the steps in prose instead of quoting the query

## Done when

- the reduced pair reproduces the artifact
- the report's reproduction is two quotable steps

## References

- [OWASP - reporting](https://owasp.org/www-project-web-security-testing-guide/)
- [NIST - evidence handling](https://csrc.nist.gov/)
