---
name: subdomain-enumeration-passive
description: "Enumerate indexed subdomains without sending a single packet to the target. Use when the program allows passive recon and the asset list includes subdomains"
pack: dorkforge
version: 1.0.0
category: bug-bounty-tooling
tags: [target, subdomains, passive]
---

# Subdomain Enumeration Passive

> Enumerate indexed subdomains without sending a single packet to the target

**Use when:** the program allows passive recon and the asset list includes subdomains

**Avoid when:** the scope covers only one exact host with no subdomains listed

## Procedure

1. Scope the query to the root domain and exclude the main host
2. Collect indexed hostnames from result URLs
3. Deduplicate against the scope list to see what is new
4. Check each new host against the exclusion list
5. Record hosts that are in scope but not in the brief, as candidates to report
6. Never resolve or fetch the new hosts without permission

## Signals

- the result set contains hosts absent from the scope brief
- some discovered hosts are clearly staging or internal naming
- deduplication leaves a small list of genuinely new hosts
- every new host is checked against exclusions

## Patterns

**1. Scoped query**

```text
site:*.{target} -site:www.{target}
```

**2. Dedup hosts**

```text
discovered hosts minus scope list
```

**3. Candidate note**

```text
staging.example.test indexed, not in brief
```

## Pitfalls

- Resolving discovered hosts during a passive phase
- Reporting a partner-hosted subdomain as an out-of-scope discovery
- Treating an indexed host that no longer resolves as an active asset

## Done when

- a deduplicated list of in-scope hosts not in the brief exists
- no packet was sent to a discovered host

## References

- [OWASP - information gathering](https://owasp.org/www-project-web-security-testing-guide/)
- [Google - site operator](https://support.google.com/websearch/answer/2466433)
