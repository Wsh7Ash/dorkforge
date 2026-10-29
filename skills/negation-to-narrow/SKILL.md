---
name: negation-to-narrow
description: "Use negative terms to remove a known noise class instead of adding more positive terms. Use when results are dominated by a predictable class such as documentation or blogs"
pack: dorkforge
version: 1.0.0
category: bug-bounty-tooling
tags: [compose, negation, precision]
---

# Negation to Narrow

> Use negative terms to remove a known noise class instead of adding more positive terms

**Use when:** results are dominated by a predictable class such as documentation or blogs

**Avoid when:** the noise class is itself a plausible place for the exposure

## Procedure

1. Identify the dominant noise class from the first page
2. Add one negative term or field for that class only
3. Re-run and count how many noise pages remain
4. Check that the real target class still appears
5. Keep the pre-negation query for comparison
6. Stop negating when further terms remove plausible hits

## Signals

- noise pages per page of results drops sharply
- the plausibility of remaining hits stays constant or improves
- the negative term is one the target itself would not use
- the comparison query is retained

## Patterns

**1. Negative field term**

```text
-inurl:docs site:{target}
```

**2. Excluded term**

```text
-"documentation" site:{target}
```

**3. Control guard**

```text
re-run without the negation to confirm nothing plausible was lost
```

## Pitfalls

- Negating a term the real artifact also contains
- Stacking negatives until the query returns nothing
- Negating without keeping the original query as a control

## Done when

- each negation is justified by an observed noise class
- the pre-negation query is retained for comparison

## References

- [Google - exclude terms](https://support.google.com/websearch/answer/2466433)
- [GitHub - search qualifiers](https://docs.github.com/en/search-github/getting-started-with-searching-on-github)
