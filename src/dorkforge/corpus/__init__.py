"""dorkforge corpus: pack metadata plus 50 authored dork-hunting skills."""

from __future__ import annotations

from typing import Any

from ..model import skill_from_dict
from .part1 import SKILLS as PART1
from .part2 import SKILLS as PART2
from .part3 import SKILLS as PART3

PACK: dict[str, Any] = {
    "name": "dorkforge",
    "version": "1.0.0",
    "category": "bug-bounty-tooling",
    "license": "MIT",
    "runtime": "Claude Code, opencode, or any agent runtime that loads SKILL.md files",
    "description": (
        "50 validated skills for dork-driven asset discovery, plus a DSL that "
        "compiles one intent to Google, GitHub or Shodan syntax with a validation "
        "gate and a curated template pack."
    ),
    "expected_skills": 50,
    "meta_keys": ("phase",),
    "requires_verification": False,
}

SKILLS: list[Any] = [skill_from_dict(raw) for raw in (*PART1, *PART2, *PART3)]
BY_SLUG: dict[str, Any] = {skill.slug: skill for skill in SKILLS}
