---
name: github-org-code-search
description: "Search an organisation's public code for configuration mistakes rather than for secrets alone. Use when the target publishes repositories under a known organisation"
pack: dorkforge
version: 1.0.0
category: bug-bounty-tooling
tags: [target, github, code]
---

# Github Org Code Search

> Search an organisation's public code for configuration mistakes rather than for secrets alone

**Use when:** the target publishes repositories under a known organisation

**Avoid when:** the organisation has no public repositories

## Procedure

1. Identify the organisation name and confirm its public repositories
2. Search for configuration files rather than for key-shaped strings
3. Prioritise pipeline files, deployment manifests and test fixtures
4. Check whether a match is current or only in history
5. Record the repository, path and commit for each match
6. Report only matches that reveal a live exposure

## Signals

- pipeline files embed environment values instead of reading secrets
- deployment manifests name internal hosts and ports
- test fixtures contain credentials that also work elsewhere
- a match exists only in a deleted file's history

## Patterns

**1. Pipeline**

```text
org:{org} filename:.github/workflows
```

**2. Manifest**

```text
org:{org} filename:values.yaml
```

**3. Test fixture**

```text
org:{org} filename:conftest.py password
```

## Pitfalls

- Grepping for key shapes and reporting every match without triage
- Reporting a secret that is already revoked in the same commit history
- Missing that the repository is a fork of another organisation's code

## Done when

- each match is recorded with repository, path and commit
- only matches implying a live exposure are carried forward

## References

- [GitHub - code search](https://docs.github.com/en/search-github/github-code-search/understanding-github-code-search-syntax)
- [GitHub - secret scanning](https://docs.github.com/en/code-security/secret-scanning)
