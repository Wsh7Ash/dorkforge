---
name: query-reproducibility
description: "Store the exact query, engine, date and count so another person can reproduce the search. Use when a query produced a result that will appear in a report"
pack: dorkforge
version: 1.0.0
category: bug-bounty-tooling
tags: [validate, reproducibility, evidence]
---

# Query Reproducibility

> Store the exact query, engine, date and count so another person can reproduce the search

**Use when:** a query produced a result that will appear in a report

**Avoid when:** the query is exploratory and its results will not be cited

## Procedure

1. Store the DSL source, the compiled query and the engine name
2. Store the date and time the query ran
3. Store the result count and the page inspected
4. Store the exact URL that was opened
5. Note any personalisation or region that could affect results
6. Attach the record to the finding rather than paraphrasing the query

## Signals

- each stored query reproduces the same count on the same day
- the engine and date are recorded with the query
- the evidence contains the URL rather than a description of it
- a colleague can rerun the search from the record alone

## Patterns

**1. Record fields**

```text
dsl, compiled, engine, date, count, url
```

**2. Region note**

```text
results may differ by account region
```

**3. Attachment**

```text
query block quoted verbatim in the report
```

## Pitfalls

- Reporting the finding without the query that found it
- Storing a screenshot instead of the query and count
- Omitting the date, which makes an index-based result unverifiable later

## Done when

- each cited result carries its query, engine, date and count
- a colleague can reproduce the search from the record

## References

- [OWASP - evidence handling](https://owasp.org/www-project-web-security-testing-guide/)
- [NIST - evidence integrity](https://csrc.nist.gov/)
