---
name: operator-combining
description: "Combine operators deliberately, using OR only where the engine treats it as a boolean. Use when several constraints must hold at once, or a value has synonyms worth covering"
pack: dorkforge
version: 1.0.0
category: bug-bounty-tooling
tags: [compose, operators, boolean]
---

# Operator Combining

> Combine operators deliberately, using OR only where the engine treats it as a boolean

**Use when:** several constraints must hold at once, or a value has synonyms worth covering

**Avoid when:** a single field already expresses the constraint unambiguously

## Procedure

1. Write the constraints that must all hold
2. Write the synonyms that could each satisfy one condition
3. Join required constraints by plain juxtaposition
4. Use OR between synonyms and group them with parentheses where supported
5. Compile and check the engine did not rewrite the grouping
6. Record whether the engine honours OR and parentheses

## Signals

- the compiled query keeps the grouping you intended
- result counts jump when an OR branch is added
- the engine ignores parentheses and the query widens unexpectedly
- synonym branches return different slices of the result set

## Patterns

**1. Conjunction**

```text
site:{target} inurl:admin intitle:"login"
```

**2. Disjunction**

```text
"password" OR "passwd"
```

**3. Grouping**

```text
(intitle:"login" OR intitle:"signin") site:{target}
```

## Pitfalls

- Assuming every engine supports parentheses the same way
- Combining OR with a site restriction and losing the restriction
- Writing synonyms that also match the noise class you excluded

## Done when

- the compiled query preserves the intended grouping
- the engine's OR and parenthesis behaviour is recorded

## References

- [Google - search operators](https://support.google.com/websearch/answer/2466433)
- [Shodan - query fundamentals](https://help.shodan.io/the-basics/search-query-fundamentals)
