---
name: encoded-url-review
description: "Decode the generated search URL once to confirm nothing was double-encoded or lost. Use when a query contains spaces, quotes, colons or boolean operators"
pack: dorkforge
version: 1.0.0
category: bug-bounty-tooling
tags: [validate, encoding, urls]
---

# Encoded Url Review

> Decode the generated search URL once to confirm nothing was double-encoded or lost

**Use when:** a query contains spaces, quotes, colons or boolean operators

**Avoid when:** the query is a single unquoted token with no special characters

## Procedure

1. Take the generated URL and decode the query parameter
2. Compare it against the compiled query character by character
3. Check that quotes survived as quotes rather than encoded quote marks
4. Check that plus signs and slashes were not mangled
5. Rebuild the URL from the compiled query if anything differs
6. Record the final URL as the evidence artifact

## Signals

- the decoded parameter equals the compiled query exactly
- quoted phrases still read as phrases
- no doubled percent signs appear
- the final URL is what was actually opened

## Patterns

**1. Decode check**

```text
unquote_plus(url.split('q=')[1]) == compiled
```

**2. Doubled encoding**

```text
%2522 instead of %22
```

**3. Evidence**

```text
the opened URL is stored verbatim
```

## Pitfalls

- Opening a URL that was encoded twice and blaming the engine for no results
- Losing a quoted phrase to over-encoding so the query widens
- Storing a pretty version of the URL that was never actually used

## Done when

- the decoded URL matches the compiled query
- the URL that was opened is stored as the evidence artifact

## References

- [RFC 3986 - percent encoding](https://www.rfc-editor.org/rfc/rfc3986.html)
- [Python - urllib.parse](https://docs.python.org/3/library/urllib.parse.html)
