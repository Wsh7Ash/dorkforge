---
name: search-url-as-evidence
description: "Attach the exact search URL, since it encodes the query, engine and scoping in one string. Use when a report cites a search result as the discovery method"
pack: dorkforge
version: 1.0.0
category: bug-bounty-tooling
tags: [report, urls, evidence]
---

# Search Url As Evidence

> Attach the exact search URL, since it encodes the query, engine and scoping in one string

**Use when:** a report cites a search result as the discovery method

**Avoid when:** the finding was found by direct testing with no search involved

## Procedure

1. Copy the URL exactly as opened, without prettifying it
2. Check it still decodes to the intended query
3. Store it beside the query DSL source
4. Note the engine and whether results are personalised
5. Add the date, because index contents change
6. Quote the URL in the report as the reproduction method

## Signals

- the URL decodes to the query that was actually intended
- the URL includes the scoping field value
- the report's reader can open it and see comparable results
- the date is recorded next to the URL

## Patterns

**1. Exact copy**

```text
search URL stored verbatim, encoded
```

**2. Decode check**

```text
unquote shows site and filetype intact
```

**3. Engine context**

```text
engine google, run 2026-10-29
```

## Pitfalls

- Rewriting the URL into a readable form that no longer works
- Omitting the date so a changed index makes the citation unverifiable
- Attaching a URL from a logged-in session that others cannot open

## Done when

- the attached URL reproduces the query when decoded
- engine and date accompany the URL

## References

- [RFC 3986 - URIs](https://www.rfc-editor.org/rfc/rfc3986.html)
- [OWASP - reporting](https://owasp.org/www-project-web-security-testing-guide/)
