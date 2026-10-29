---
name: filetype-targeting
description: "Target the document type that would hold the artifact, not the page that mentions it. Use when the exposure would live in a config, archive, dump or document file"
pack: dorkforge
version: 1.0.0
category: bug-bounty-tooling
tags: [compose, filetype, documents]
---

# Filetype Targeting

> Target the document type that would hold the artifact, not the page that mentions it

**Use when:** the exposure would live in a config, archive, dump or document file

**Avoid when:** the artifact is rendered HTML with no file behind it

## Procedure

1. Decide which file type would actually contain the artifact
2. Add the filetype or extension field with that type
3. Pair it with one scoping field so results stay on target
4. Check that the engine maps the field to its own operator
5. Sample a few results to confirm the type matches the intent
6. Record the mapping used, since engines name it differently

## Signals

- sampled results carry the extension you targeted
- the extension maps to a different operator on the code index
- the filetype field reduces results without losing plausible hits
- the recorded operator name differs from the DSL field name

## Patterns

**1. Config file**

```text
site:{target} filetype:env inurl:config
```

**2. Database dump**

```text
site:{target} filetype:sql intext:"INSERT INTO"
```

**3. Backup archive**

```text
site:{target} filetype:zip inurl:backup
```

## Pitfalls

- Targeting the file type of the page rather than of the artifact
- Assuming an engine indexes archive contents
- Forgetting that some engines require an extension without a leading dot

## Done when

- the targeted file type matches the artifact the intent names
- the engine's operator name for that field is recorded

## References

- [Google - filetype operator](https://support.google.com/websearch/answer/2466433)
- [GitHub - extension qualifier](https://docs.github.com/en/search-github/github-code-search/understanding-github-code-search-syntax)
