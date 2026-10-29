# Security Policy

## Reporting a vulnerability in dorkforge

Email the maintainer via the address on the GitHub profile, or open a private
security advisory at
[github.com/Wsh7Ash/dorkforge/security/advisories](https://github.com/Wsh7Ash/dorkforge/security/advisories/new).

Please include the version, a minimal reproduction, and the impact you expect.
Do not open a public issue. Expect an acknowledgement within seven days.

dorkforge has no runtime dependencies, no network code and no privileged
operations, so the realistic attack surface is small: a crafted dork that makes
the parser or compiler hang or crash, or a template that produces a query the
author did not intend.

## Scope of this tool

dorkforge produces search queries and URLs. It does not send them. Everything it
emits targets a public search index, so using it is passive by construction —
but the results are real systems, and the rules below still apply.

### Authorized use only

- Use it only on assets that are in scope for a program you have joined, or on
  assets you own.
- Read the program's rules on automated tooling before running a batch of
  queries. Some programs forbid automated enumeration even against an index.
- The `medium` risk templates can reach infrastructure wider than one host.
  Do not run them outside an explicit allowance.

### Do not collect what you find

A dotenv file, a database dump or a credentials file is not yours to read. The
skills in the `validate` and `report` phases describe the minimum proof: the
status, the content type, a redacted sample — never the body of someone else's
data. If you have already fetched it, delete it and say so in the report.

### Credentials

If a dork surfaces live credentials, do not test them, do not pivot with them,
and do not paste them into a report. Say what kind of secret it was, where it
was served from, and that it should be rotated.

### Reports

Findings about a third party's infrastructure go to that party's program, not to
this repository's issue tracker. Keep evidence redacted and minimal.

## Supported versions

| Version | Supported |
|---|---|
| 1.x | yes |
