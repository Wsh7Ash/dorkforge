"""dorkforge command line interface.

Shared corpus commands (validate / list / show / search / build) come from the
pack harness. The domain commands are the compiler:

    dorkforge compile 'site:{target} inurl:".env"' --target api.example.test
    dorkforge compile 'inurl:admin filetype:php' --engine github
    dorkforge explore 'org:{org} "api_key"'
    dorkforge templates --tag cloud
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from . import __version__
from .corpus import PACK, SKILLS
from .dsl import ENGINES, DorkError, compile_all, compile_dork, explore, fields_for
from .render import build_pack, render_skill, word_count
from .templates import TEMPLATES, by_id, by_risk, by_tag
from .validate import (
    MAX_DESCRIPTION,
    MIN_DONE,
    MIN_PATTERNS,
    MIN_PITFALLS,
    MIN_SIGNALS,
    MIN_STEPS,
    MIN_SUMMARY,
    MIN_WORDS,
    Issue,
    validate_pack,
)

PHASE_ORDER = ("frame", "compose", "validate", "target", "triage", "report")

FLOORS = {
    "min_steps": MIN_STEPS,
    "min_signals": MIN_SIGNALS,
    "min_patterns": MIN_PATTERNS,
    "min_pitfalls": MIN_PITFALLS,
    "min_done_when": MIN_DONE,
    "min_summary_chars": MIN_SUMMARY,
    "min_words": MIN_WORDS,
    "max_description_chars": MAX_DESCRIPTION,
}

# Variables a template may require, in the order they are documented.
VARIABLES = ("target", "host", "org", "product", "country")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _report(issues: list[Issue], total: int, as_json: bool, title: str) -> int:
    bad = {issue.slug for issue in issues if issue.slug}
    valid = total - len(bad)
    if as_json:
        print(
            json.dumps(
                {
                    "pack": title,
                    "checked": total,
                    "valid": valid,
                    "passed": not issues,
                    "floors": FLOORS,
                    "issues": [
                        {"slug": i.slug, "rule": i.rule, "message": i.message} for i in issues
                    ],
                },
                indent=2,
            )
        )
    else:
        print(f"{title}: {valid}/{total} skills valid")
        for issue in issues:
            print(f"  FAIL {issue}")
        if not issues:
            print(
                f"  ok  steps>={MIN_STEPS} signals>={MIN_SIGNALS} patterns>={MIN_PATTERNS} "
                f"pitfalls>={MIN_PITFALLS} words>={MIN_WORDS} refs canonical https"
            )
    return 0 if not issues else 1


def cmd_validate(args: argparse.Namespace) -> int:
    issues = validate_pack(PACK, SKILLS)
    root = Path(args.root) if args.root else repo_root()
    if not args.skip_files:
        for skill in SKILLS:
            path = root / "skills" / skill.slug / "SKILL.md"
            if not path.exists():
                issues.append(Issue(skill.slug, "file-missing", "SKILL.md missing"))
                continue
            if path.read_text(encoding="utf-8") != render_skill(PACK, skill):
                issues.append(Issue(skill.slug, "file-drift", "SKILL.md differs from corpus render"))
    return _report(issues, len(SKILLS), args.json, PACK["name"])


def cmd_list(args: argparse.Namespace) -> int:
    skills = [
        skill
        for skill in SKILLS
        if (not args.tag or args.tag in skill.tags)
        and (not args.phase or skill.meta_get("phase") == args.phase)
    ]
    if args.json:
        print(
            json.dumps(
                [
                    {
                        "slug": s.slug,
                        "title": s.title,
                        "tags": list(s.tags),
                        "meta": s.meta,
                        "words": word_count(render_skill(PACK, s)),
                    }
                    for s in skills
                ],
                indent=2,
            )
        )
        return 0
    for skill in skills:
        print(f"{skill.slug:38s} {skill.meta_get('phase', '-'):10s} {skill.title}")
    print(f"-- {len(skills)} skills")
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    for skill in SKILLS:
        if skill.slug == args.slug:
            print(render_skill(PACK, skill), end="")
            return 0
    print(f"unknown skill: {args.slug}", file=sys.stderr)
    return 1


def cmd_search(args: argparse.Namespace) -> int:
    terms = [term.lower() for term in args.terms]
    scored: list[tuple[int, Any]] = []
    for skill in SKILLS:
        haystack = " ".join(
            [skill.slug, skill.title, skill.summary, " ".join(skill.tags), " ".join(skill.steps)]
        ).lower()
        score = sum(haystack.count(term) for term in terms)
        if score:
            scored.append((score, skill))
    scored.sort(key=lambda pair: (-pair[0], pair[1].slug))
    for score, skill in scored[: args.limit]:
        print(f"{score:3d}  {skill.slug:38s} {skill.title}")
    if not scored:
        print("no matches")
        return 1
    return 0


def cmd_build(args: argparse.Namespace) -> int:
    root = Path(args.root) if args.root else repo_root()
    build_pack(root, PACK, SKILLS)
    issues = validate_pack(PACK, SKILLS)
    for skill in SKILLS:
        path = root / "skills" / skill.slug / "SKILL.md"
        if path.read_text(encoding="utf-8") != render_skill(PACK, skill):
            issues.append(Issue(skill.slug, "file-drift", "render mismatch"))
    bad = {issue.slug for issue in issues if issue.slug}
    report = {
        "pack": PACK["name"],
        "version": PACK["version"],
        "expected_skills": PACK.get("expected_skills", len(SKILLS)),
        "checked": len(SKILLS),
        "valid": len(SKILLS) - len(bad),
        "passed": not issues,
        "floors": FLOORS,
        "issues": [{"slug": i.slug, "rule": i.rule, "message": i.message} for i in issues],
    }
    results = root / "results"
    results.mkdir(parents=True, exist_ok=True)
    (results / "validation.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"built {len(SKILLS)} skills -> {root / 'skills'}")
    return 0 if not issues else 1


# ------------------------------------------------------------- compiler commands


def _fill(text: str, variables: dict[str, str]) -> tuple[str, list[str]]:
    """Substitute {name} placeholders, reporting any that remain."""
    filled = text
    for name, value in variables.items():
        filled = filled.replace("{" + name + "}", value)
    missing = [name for name in VARIABLES if "{" + name + "}" in filled]
    return filled, missing


def cmd_compile(args: argparse.Namespace) -> int:
    variables = {
        "target": args.target,
        "host": args.host,
        "org": args.org,
        "product": args.product,
        "country": args.country,
    }
    variables = {key: value for key, value in variables.items() if value}
    text = args.dork
    if args.template:
        try:
            text = by_id(args.template)["dork"]
        except KeyError:
            print(f"unknown template: {args.template}", file=sys.stderr)
            return 2
    text, missing = _fill(text, variables)
    if missing:
        print(
            "missing variables: " + ", ".join(f"{{{name}}}" for name in missing),
            file=sys.stderr,
        )
        return 2
    try:
        result = compile_dork(text, args.engine)
    except DorkError as exc:
        print(f"cannot compile: {exc}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))
    else:
        print(result.query)
        print(result.url)
        if result.rewrites:
            print("rewrites: " + ", ".join(result.rewrites))
        for note in result.notes:
            print(f"note: {note}")
    return 0


def cmd_explore(args: argparse.Namespace) -> int:
    try:
        payload = explore(args.dork)
    except DorkError as exc:
        print(f"cannot parse: {exc}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0
    print(payload["plain"])
    print(f"fields: {', '.join(payload['fields']) or 'none'}")
    if payload["problems"]:
        for problem in payload["problems"]:
            print(f"problem: {problem}")
    for engine, data in payload["engines"].items():
        if "error" in data:
            print(f"{engine:7s} unsupported: {data['error']}")
        else:
            print(f"{engine:7s} {data['query']}")
    return 0 if not payload["problems"] else 1


def cmd_fields(args: argparse.Namespace) -> int:
    if args.engine:
        print(" ".join(fields_for(args.engine)))
        return 0
    for engine in ENGINES:
        print(f"{engine:7s} {' '.join(fields_for(engine))}")
    return 0


def cmd_templates(args: argparse.Namespace) -> int:
    templates = TEMPLATES
    if args.risk:
        templates = by_risk(args.risk)
    if args.tag:
        templates = [template for template in templates if args.tag in template.get("tags", [])]
    if args.json:
        print(json.dumps(templates, indent=2, ensure_ascii=False))
        return 0
    for template in templates:
        print(f"{template['id']:34s} {template['risk']:6s} {template['title']}")
        if args.verbose:
            print(f"  intent: {template['intent']}")
            print(f"  dork:   {template['dork']}")
    print(f"-- {len(templates)} templates")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog=PACK["name"], description=PACK["description"])
    parser.add_argument("--version", action="version", version=f"{PACK['name']} {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("validate", help="run every corpus rule and check disk sync")
    p.add_argument("--json", action="store_true")
    p.add_argument("--root", default=None)
    p.add_argument("--skip-files", action="store_true")
    p.set_defaults(func=cmd_validate)

    p = sub.add_parser("list", help="list skills")
    p.add_argument("--tag", default=None)
    p.add_argument("--phase", default=None)
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("show", help="print one SKILL.md")
    p.add_argument("slug")
    p.set_defaults(func=cmd_show)

    p = sub.add_parser("search", help="rank skills by keyword")
    p.add_argument("terms", nargs="+")
    p.add_argument("--limit", type=int, default=10)
    p.set_defaults(func=cmd_search)

    p = sub.add_parser("build", help="regenerate skills/, pack.json and results/")
    p.add_argument("--root", default=None)
    p.set_defaults(func=cmd_build)

    p = sub.add_parser("compile", help="compile a dork (or a template) for one engine")
    p.add_argument("dork", nargs="?", default="")
    p.add_argument("--template", default=None)
    p.add_argument("--engine", default="google", choices=list(ENGINES))
    p.add_argument("--target", default=None)
    p.add_argument("--host", default=None)
    p.add_argument("--org", default=None)
    p.add_argument("--product", default=None)
    p.add_argument("--country", default=None)
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_compile)

    p = sub.add_parser("explore", help="show a dork's terms and every engine's result")
    p.add_argument("dork")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_explore)

    p = sub.add_parser("fields", help="list the fields each engine supports")
    p.add_argument("--engine", default=None, choices=list(ENGINES))
    p.set_defaults(func=cmd_fields)

    p = sub.add_parser("templates", help="list the curated template pack")
    p.add_argument("--tag", default=None)
    p.add_argument("--risk", default=None, choices=["low", "medium", "high"])
    p.add_argument("--verbose", action="store_true")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_templates)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
