---
name: result-triage-first-look
description: "Read the first page of results as a sample of the query's behaviour, not as a list of findings. Use when a query returned results and it is unclear whether any are relevant"
pack: dorkforge
version: 1.0.0
category: bug-bounty-tooling
tags: [triage, sampling, quality]
---

# Result Triage First Look

> Read the first page of results as a sample of the query's behaviour, not as a list of findings

**Use when:** a query returned results and it is unclear whether any are relevant

**Avoid when:** the query returned a single unambiguous result you already verified

## Procedure

1. Read the first ten results and classify each as plausible, noise or unclear
2. Count how many are plausible before touching any of them
3. Identify what the plausible ones share
4. Look for a pattern in the noise that suggests a missing negative term
5. Decide whether to refine the query or proceed to verification
6. Record the classification counts as the sample's shape

## Signals

- the plausible count is stable across the first page
- the noise class is consistent enough to filter
- unclear results cluster around one host
- the sample suggests a refinement before verification

## Patterns

**1. First page sample**

```text
plausible 3, noise 6, unclear 1
```

**2. Noise trait**

```text
all noise results are documentation subdomains
```

**3. Decision**

```text
refine with a negative term before verifying
```

## Pitfalls

- Treating the first result as the best result
- Starting verification on three hits before the sample is understood
- Reading only titles and never the snippets that show the artifact

## Done when

- the first page is classified and counted
- a decision to refine or verify is recorded with its reason

## References

- [Google - results](https://support.google.com/websearch/answer/2466433)
- [OWASP - triage](https://owasp.org/www-project-web-security-testing-guide/)
