---
name: reproducible-search-date
description: "Date every query in the report so an index change cannot make the finding look invented. Use when the report will be read weeks after the search was run"
pack: dorkforge
version: 1.0.0
category: bug-bounty-tooling
tags: [report, dates, reproducibility]
---

# Reproducible Search Date

> Date every query in the report so an index change cannot make the finding look invented

**Use when:** the report will be read weeks after the search was run

**Avoid when:** the evidence is a live response captured with its own timestamp

## Procedure

1. Record the UTC date and time beside every query
2. Record the result count observed at that time
3. Record whether results differed from an earlier run
4. State that index contents change and the date fixes the observation
5. Re-run cited queries before submission and note any change
6. Update the report if a query no longer returns the artifact

## Signals

- every cited query carries a UTC timestamp
- counts are recorded with the timestamp
- a pre-submission re-run is noted in the report
- changed results are disclosed rather than hidden

## Patterns

**1. Timestamp**

```text
queried 2026-10-29T08:14Z, 12 results
```

**2. Re-run note**

```text
re-ran before submission: 12 results, unchanged
```

**3. Change disclosure**

```text
one host no longer indexed as of submission
```

## Pitfalls

- Omitting dates so a later mismatch looks like fabrication
- Quietly dropping a citation that stopped reproducing
- Recording local time without a zone

## Done when

- every cited query has a UTC timestamp and count
- a pre-submission re-run is recorded

## References

- [NIST - evidence integrity](https://csrc.nist.gov/)
- [OWASP - reporting](https://owasp.org/www-project-web-security-testing-guide/)
