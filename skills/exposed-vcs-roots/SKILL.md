---
name: exposed-vcs-roots
description: "Look for a served repository directory, which often exposes history and therefore secrets. Use when a deployment may have shipped its working copy into the web root"
pack: dorkforge
version: 1.0.0
category: bug-bounty-tooling
tags: [target, vcs, exposure]
---

# Exposed Vcs Roots

> Look for a served repository directory, which often exposes history and therefore secrets

**Use when:** a deployment may have shipped its working copy into the web root

**Avoid when:** the hosting platform is known to deny dot-directories at the edge

## Procedure

1. Search for the common metadata paths of git and subversion
2. Record candidates per host rather than per URL
3. If permitted, fetch only the metadata file, not the whole repository
4. Check whether the metadata names a remote or a branch
5. Report the exposure with the single metadata response as proof
6. Do not pull object history during a passive phase

## Signals

- the metadata path returns content rather than a 404
- the metadata file names a repository remote
- the response is served as text rather than blocked by the edge
- the same host serves other dot-paths

## Patterns

**1. Git head pointer**

```text
site:{target} inurl:"/.git/HEAD"
```

**2. Config file**

```text
inurl:"/.git/config"
```

**3. Proof observable**

```text
single metadata fetch, history not downloaded
```

## Pitfalls

- Mirroring the whole repository and pulling other people's code
- Reporting a 404 on one path as proof the repository is not served
- Fetching history before confirming the scope allows active testing

## Done when

- the exposure is proven with a single metadata response
- no repository history was downloaded

## References

- [Git - repository layout](https://git-scm.com/docs)
- [OWASP - source disclosure](https://owasp.org/www-project-web-security-testing-guide/)
