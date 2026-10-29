---
name: legal-and-ethics-gate
description: "Stop before a query that would collect other people's data, even when the index makes it easy. Use when a query could surface credentials, personal data or another tenant's content"
pack: dorkforge
version: 1.0.0
category: bug-bounty-tooling
tags: [frame, ethics, safety]
---

# Legal and Ethics Gate

> Stop before a query that would collect other people's data, even when the index makes it easy

**Use when:** a query could surface credentials, personal data or another tenant's content

**Avoid when:** the query only returns public marketing pages about the target

## Procedure

1. Ask what the query would return if it worked perfectly
2. Identify whether that output belongs to someone other than the program
3. Stop and report the existence of the exposure without collecting the data
4. Use a minimal proof such as a header or status, not the content
5. Record the decision not to collect, with the reasoning
6. Escalate to the program when the correct action is unclear

## Signals

- the proof is a status, header or redacted sample rather than a dump
- no personal data was downloaded at any point
- the decision not to collect is written in the notes
- the program was told before any sensitive data was touched

## Patterns

**1. Minimal proof**

```text
200 with Content-Type application/json, body not retained
```

**2. Stop point**

```text
first record containing a user email
```

**3. Recorded decision**

```text
did not download the dump; reported the endpoint instead
```

## Pitfalls

- Downloading a database dump because the query made it findable
- Screenshotting personal data to strengthen a report
- Assuming a bug-bounty scope authorises handling third-party personal data

## Done when

- no third-party personal data was retained at any point
- the collection decision and its reasoning are recorded

## References

- [OWASP - privacy risks](https://owasp.org/www-project-top-10-privacy-risks/)
- [HackerOne - disclosure guidance](https://docs.hackerone.com/)
