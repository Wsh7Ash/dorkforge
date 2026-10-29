---
name: quoted-phrase-precision
description: "Quote exact strings when the artifact has a known signature, so results match the bytes not the topic. Use when the artifact contains a fixed signature such as a header line or a key name"
pack: dorkforge
version: 1.0.0
category: bug-bounty-tooling
tags: [compose, phrases, precision]
---

# Quoted Phrase Precision

> Quote exact strings when the artifact has a known signature, so results match the bytes not the topic

**Use when:** the artifact contains a fixed signature such as a header line or a key name

**Avoid when:** the artifact varies too much for one exact string to appear

## Procedure

1. Identify the fixed substring that any real match must contain
2. Quote it exactly, including punctuation and casing
3. Test with and without the quotes to compare result quality
4. Combine the phrase with one scoping field
5. Check whether the engine honours the quotes for that field
6. Record both variants so the difference in yield is visible

## Signals

- the quoted variant returns far fewer, more relevant results
- every returned page contains the literal phrase
- the unquoted variant returns topical discussions instead
- the quoted phrase survives the compiler unchanged

## Patterns

**1. Signature**

```text
"BEGIN RSA PRIVATE KEY"
```

**2. Exact header**

```text
"Access-Control-Allow-Origin: *"
```

**3. Variant comparison**

```text
quoted: 12 results, unquoted: 48000
```

## Pitfalls

- Quoting a phrase with the snippet's ellipsis included
- Assuming quotes work identically in every field of every engine
- Quoting something so generic that the phrase adds no precision

## Done when

- both quoted and unquoted variants are recorded with their yields
- every sampled result contains the literal phrase

## References

- [Google - search operators](https://support.google.com/websearch/answer/2466433)
- [Shodan - query fundamentals](https://help.shodan.io/the-basics/search-query-fundamentals)
