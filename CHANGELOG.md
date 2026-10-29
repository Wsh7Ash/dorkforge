# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project uses
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-10-29

### Added

- Portable dork DSL: `parse` tokenises fields, phrases, words and boolean
  operators with negation and quoting preserved.
- Compiler for Google, GitHub and Shodan, with per-engine field rewrites and
  explicit refusals naming the fields an engine does support.
- `compile`, `explore`, `fields` and `templates` commands, plus JSON output and
  documented exit codes.
- 66 curated dork templates, each with an intent sentence and a risk level.
- 50 validated bug-bounty skills across frame, compose, validate, target,
  triage and report phases, with a render/validate/build harness.
- 31 tests covering tokenising, compilation, refusals, the field map, template
  filling and the real CLI as a subprocess.

### Fixed

- `validate('site:')` returned no problems because a trailing-colon field was
  tokenised as a bare word; the parser now reports an empty field value.
- A test asserted that a Shodan-only field (`hostname`) is invalid everywhere.
  It is valid for Shodan and refused for Google and GitHub, so the test now
  checks both behaviours instead of the wrong one.
