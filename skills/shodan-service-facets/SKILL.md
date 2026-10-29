---
name: shodan-service-facets
description: "Use service facets to enumerate what an organisation exposes, without scanning a single port. Use when the program covers an organisation's internet-facing services"
pack: dorkforge
version: 1.0.0
category: bug-bounty-tooling
tags: [target, shodan, services]
---

# Shodan Service Facets

> Use service facets to enumerate what an organisation exposes, without scanning a single port

**Use when:** the program covers an organisation's internet-facing services

**Avoid when:** the scope is a single web application with no infrastructure coverage

## Procedure

1. Search by organisation or net block rather than by hostname
2. Break results down by port, product and country facets
3. Identify services outside the expected web ports
4. Record each service with its banner and certificate subject
5. Flag services whose banner reveals a default installation
6. Do not connect to any discovered service during the passive phase

## Signals

- facets reveal database or remote-access ports
- certificate subjects differ from the organisation's main domain
- a product version in a banner is end-of-life
- the same service appears on many hosts, suggesting a template deployment

## Patterns

**1. Org scope query**

```text
org:"{target}" facet:port,product
```

**2. Facet breakdown**

```text
org:"{target}" port:22,3389,9200
```

**3. Banner note**

```text
product and version recorded per host
```

## Pitfalls

- Connecting to a discovered database to check whether it is open
- Assuming Shodan's organisation mapping covers every subsidiary
- Reporting an exposed port as a finding when the program excludes infrastructure

## Done when

- the exposed service inventory is recorded with banners
- no connection was made to a discovered service

## References

- [Shodan - search filters](https://help.shodan.io/the-basics/search-query-fundamentals)
- [OWASP - infrastructure exposure](https://owasp.org/www-project-web-security-testing-guide/)
