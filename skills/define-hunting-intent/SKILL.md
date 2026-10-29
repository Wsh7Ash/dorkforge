---
name: define-hunting-intent
description: "Write the one exposure you are looking for before composing any query, so results have a test. Use when a hunt is starting from a vague goal such as finding something interesting"
pack: dorkforge
version: 1.0.0
category: bug-bounty-tooling
tags: [frame, intent, method]
---

# Define Hunting Intent

> Write the one exposure you are looking for before composing any query, so results have a test

**Use when:** a hunt is starting from a vague goal such as finding something interesting

**Avoid when:** the program names an exact asset and an exact class of bug to test

## Procedure

1. State the exposure in one sentence, naming the artifact and who can reach it
2. Name the observable that would prove it, such as a config file body
3. Name the observable that would refute it, such as a login wall
4. Write the query only after both observables exist
5. Record the intent beside the query so later readers know what it was for
6. Retire the intent when results prove or disprove it

## Signals

- the intent sentence names an artifact, not a technology
- a proof observable exists before the first search
- the refuting observation is specific enough to recognise
- the query can be judged against the intent afterwards

## Patterns

**1. Intent sentence**

```text
a deployed dotenv readable by anyone on the internet
```

**2. Proof observable**

```text
a 200 response whose body contains KEY=value pairs
```

**3. Refutation**

```text
a 404 or an authentication redirect on every path
```

## Pitfalls

- Searching first and inventing a purpose for whatever appears
- Writing an intent so broad that no result can refute it
- Leaving the intent unrecorded so a later reader misreads the query

## Done when

- each query in the hunt has an intent sentence with proof and refutation
- the intent is stored beside the query template used

## References

- [OWASP - testing methodology](https://owasp.org/www-project-web-security-testing-guide/)
- [Google - refine web searches](https://support.google.com/websearch/answer/2466433)
