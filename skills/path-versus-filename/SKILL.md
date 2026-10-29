---
name: path-versus-filename
description: "Choose between path and filename filters depending on whether you know where or what. Use when an artifact is known by its directory location or by its exact file name"
pack: dorkforge
version: 1.0.0
category: bug-bounty-tooling
tags: [compose, path, filename]
---

# Path Versus Filename

> Choose between path and filename filters depending on whether you know where or what

**Use when:** an artifact is known by its directory location or by its exact file name

**Avoid when:** the artifact's location and name are both unknown, where text search fits better

## Procedure

1. Decide whether you know the directory, the file name, or both
2. Use a path filter when the directory convention is known
3. Use a filename filter when the exact name is known
4. Combine both when the convention is strong and the name is stable
5. Check how the engine treats case in each filter
6. Record which filter carried the precision

## Signals

- path results cluster in the expected directory
- filename results include only files with the exact name
- case sensitivity differs between the two filters
- combining both narrows without emptying the result set

## Patterns

**1. Path filter**

```text
path:".aws" filename:credentials
```

**2. Filename**

```text
filename:credentials
```

**3. Both filters**

```text
filename:docker-compose.yml path:deploy
```

## Pitfalls

- Using a filename filter for a file whose name varies by environment
- Assuming a path filter matches a substring anywhere in the path
- Treating a case-sensitive miss as proof the file is absent

## Done when

- the chosen filter matches what is actually known about the artifact
- case behaviour is recorded for the filter used

## References

- [GitHub - code search syntax](https://docs.github.com/en/search-github/github-code-search/understanding-github-code-search-syntax)
- [Git - repository layout](https://git-scm.com/docs)
