"""Corpus, DSL, compiler and template tests."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote_plus

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from dorkforge.corpus import PACK, SKILLS  # noqa: E402
from dorkforge.dsl import (  # noqa: E402
    ENGINES,
    DorkError,
    compile_all,
    compile_dork,
    explore,
    fields_for,
    parse,
    validate,
)
from dorkforge.render import render_skill, word_count  # noqa: E402
from dorkforge.templates import TEMPLATES, by_id, by_risk, by_tag  # noqa: E402
from dorkforge.validate import pack_issues, skill_issues, validate_pack  # noqa: E402

PHASES = ("frame", "compose", "validate", "target", "triage", "report")


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    env = {"PYTHONPATH": str(ROOT / "src"), "PYTHONIOENCODING": "utf-8"}
    return subprocess.run(
        [sys.executable, "-m", "dorkforge", *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
        timeout=120,
    )


# ---------------------------------------------------------------- corpus shape


def test_pack_declares_fifty_and_delivers_fifty() -> None:
    assert PACK["expected_skills"] == 50
    assert len(SKILLS) == 50


def test_slugs_and_titles_are_unique() -> None:
    assert len({skill.slug for skill in SKILLS}) == 50
    assert len({skill.title.lower() for skill in SKILLS}) == 50


def test_every_skill_passes_every_rule() -> None:
    assert validate_pack(PACK, SKILLS) == []


def test_phases_are_known_and_balanced() -> None:
    counts: dict[str, int] = {}
    for skill in SKILLS:
        phase = skill.meta_get("phase")
        assert phase in PHASES
        counts[phase] = counts.get(phase, 0) + 1
    assert set(counts) == set(PHASES)
    assert min(counts.values()) >= 7
    assert max(counts.values()) <= 15


def test_word_floor_is_real_not_theoretical() -> None:
    counts = [word_count(render_skill(PACK, skill)) for skill in SKILLS]
    assert min(counts) >= 180
    assert sum(counts) / len(counts) > 200


def test_committed_skills_match_corpus_render() -> None:
    for skill in SKILLS:
        path = ROOT / "skills" / skill.slug / "SKILL.md"
        assert path.exists(), f"missing {path}"
        assert path.read_text(encoding="utf-8") == render_skill(PACK, skill)


def test_pack_json_hashes_match_files() -> None:
    import hashlib

    manifest = json.loads((ROOT / "pack.json").read_text(encoding="utf-8"))
    assert manifest["skill_count"] == 50
    for entry in manifest["skills"]:
        text = (ROOT / entry["path"]).read_text(encoding="utf-8")
        assert hashlib.sha256(text.encode("utf-8")).hexdigest() == entry["sha256"]


# ---------------------------------------------------------------------- parser


def test_parse_keeps_fields_phrases_and_negation() -> None:
    dork = parse('site:example.test inurl:"admin" -intitle:"index of"')
    kinds = [term.kind for term in dork.terms]
    assert kinds == ["field", "field", "field"]
    assert dork.terms[1].quoted is True
    assert dork.terms[2].negated is True
    assert dork.plain == 'site:example.test inurl:"admin" -intitle:"index of"'


def test_parse_supports_boolean_operators() -> None:
    dork = parse('"password" OR "passwd"')
    assert [term.kind for term in dork.terms] == ["phrase", "operator", "phrase"]


def test_parse_rejects_bad_input() -> None:
    with pytest.raises(DorkError):
        parse("")
    with pytest.raises(DorkError):
        parse('site:x intitle:"unterminated')
    with pytest.raises(DorkError) as unknown:
        parse("bogusfield:value")
    assert "unknown field" in str(unknown.value)


# ------------------------------------------------------------------- compiler


def test_google_compile_preserves_quoting() -> None:
    result = compile_dork('site:{target} inurl:".env"'.replace("{target}", "api.test"), "google")
    assert result.query == 'site:api.test inurl:".env"'
    assert unquote_plus(result.url.split("q=", 1)[1]) == result.query
    assert result.used == [("site", "site"), ("inurl", "inurl")]


def test_field_mapping_is_reported_as_a_rewrite() -> None:
    result = compile_dork("filetype:env", "github")
    assert result.query == "extension:env"
    assert result.rewrites == ["filetype -> extension"]


def test_unsupported_field_is_refused_with_alternatives() -> None:
    with pytest.raises(DorkError) as excinfo:
        compile_dork("site:api.test", "github")
    message = str(excinfo.value)
    assert "site" in message and "supported there" in message


def test_unknown_engine_is_refused() -> None:
    with pytest.raises(DorkError):
        compile_dork("site:x.test", "bing")


def test_shodan_compile_uses_service_facets() -> None:
    result = compile_dork('org:"Acme" port:9200 product:elastic', "shodan")
    assert result.query == 'org:"Acme" port:9200 product:elastic'
    assert any("services" in note for note in result.notes)


def test_compile_all_reports_per_engine_errors() -> None:
    payload = compile_all('site:api.test inurl:"/.env"')
    assert payload["google"].query.startswith("site:api.test")
    assert isinstance(payload["github"], str)
    assert isinstance(payload["shodan"], str)


def test_validate_flags_empty_values_and_refuses_per_engine() -> None:
    assert validate('site:{target} inurl:"/.git/config"') == []
    assert validate("site:") != []
    # hostname is a real field, but only Shodan has it: valid overall, refused elsewhere.
    assert validate("hostname:x.test") == []
    assert compile_dork("hostname:x.test", "shodan").query == "hostname:x.test"
    with pytest.raises(DorkError):
        compile_dork("hostname:x.test", "google")
    with pytest.raises(DorkError):
        compile_dork("hostname:x.test", "github")


def test_explore_payload_shape() -> None:
    payload = explore('org:"Acme" port:9200')
    assert payload["fields"] == ["org", "port"]
    assert payload["problems"] == []
    assert payload["engines"]["shodan"]["query"] == 'org:"Acme" port:9200'
    assert "error" in payload["engines"]["google"]


def test_fields_for_each_engine() -> None:
    for engine in ENGINES:
        fields = fields_for(engine)
        assert fields == sorted(fields)
        assert fields
    assert "site" in fields_for("google")
    assert "site" not in fields_for("shodan")


# -------------------------------------------------------------------- templates


def test_templates_have_unique_ids_and_valid_risk() -> None:
    ids = [template["id"] for template in TEMPLATES]
    assert len(ids) == len(set(ids))
    assert all(template["risk"] in ("low", "medium", "high") for template in TEMPLATES)
    assert len(TEMPLATES) >= 60


def test_every_template_parses_and_compiles_somewhere() -> None:
    for template in TEMPLATES:
        dork = template["dork"]
        parse(dork)  # raises on syntax problems
        engines = [engine for engine in ENGINES if _compiles(dork, engine)]
        assert engines, f"{template['id']} compiles on no engine"


def _compiles(dork: str, engine: str) -> bool:
    try:
        compile_dork(dork, engine)
        return True
    except DorkError:
        return False


def test_every_template_placeholder_is_documented() -> None:
    allowed = {"target", "host", "org", "product", "country"}
    for template in TEMPLATES:
        import re

        used = set(re.findall(r"\{([a-z_]+)\}", template["dork"]))
        assert used <= allowed, f"{template['id']} uses {used - allowed}"


def test_template_lookup_helpers() -> None:
    assert by_id("git-config-exposed")["risk"] == "low"
    assert by_risk("medium")
    assert all("cloud" in template["tags"] for template in by_tag("cloud"))
    with pytest.raises(KeyError):
        by_id("does-not-exist")


# -------------------------------------------------------------------------- CLI


def test_cli_validate_reports_fifty_of_fifty() -> None:
    proc = run_cli("validate")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "50/50 skills valid" in proc.stdout


def test_cli_compile_from_template() -> None:
    proc = run_cli("compile", "--template", "git-config-exposed", "--target", "shop.example.test")
    assert proc.returncode == 0, proc.stderr
    assert "site:shop.example.test" in proc.stdout
    assert "https://www.google.com/search?q=" in proc.stdout


def test_cli_compile_reports_missing_variables() -> None:
    proc = run_cli("compile", "--template", "git-config-exposed")
    assert proc.returncode == 2
    assert "missing variables" in proc.stderr


def test_cli_compile_refuses_an_unsupported_engine_field() -> None:
    proc = run_cli("compile", "site:x.test", "--engine", "github")
    assert proc.returncode == 1
    assert "does not exist on github" in proc.stderr


def test_cli_explore_and_fields_and_templates() -> None:
    explored = run_cli("explore", 'site:{target} filetype:env'.replace("{target}", "a.test"))
    assert explored.returncode == 0
    assert "google" in explored.stdout and "shodan" in explored.stdout

    fields = run_cli("fields", "--engine", "shodan")
    assert "port" in fields.stdout and "site" not in fields.stdout

    templates = run_cli("templates", "--tag", "cloud")
    assert templates.returncode == 0
    assert "templates" in templates.stdout

    as_json = run_cli("templates", "--risk", "medium", "--json")
    payload = json.loads(as_json.stdout)
    assert payload and all(item["risk"] == "medium" for item in payload)


def test_cli_list_show_and_search() -> None:
    listed = run_cli("list", "--phase", "triage")
    assert listed.returncode == 0
    assert listed.stdout.strip().endswith("skills")

    show = run_cli("show", SKILLS[0].slug)
    assert show.returncode == 0
    assert show.stdout.startswith(f"---\nname: {SKILLS[0].slug}")

    assert run_cli("show", "not-a-real-skill").returncode == 1

    search = run_cli("search", "passive")
    assert search.returncode == 0
    assert search.stdout.strip() != ""

    nohit = run_cli("search", "zzzz-no-such-term")
    assert nohit.returncode == 1
    assert "no matches" in nohit.stdout


# ------------------------------------------------------------------ integrity


def test_pack_issues_catches_a_short_corpus() -> None:
    issues = pack_issues(PACK, SKILLS[:-1])
    assert any(issue.rule == "skill-count" for issue in issues)


def test_single_skill_rule_violations_are_reported() -> None:
    broken = dict(SKILLS[0].__dict__)
    broken["steps"] = ("one", "two")
    from dorkforge.model import skill_from_dict

    issues = skill_issues(PACK, skill_from_dict(broken), "")
    assert "steps-count" in {issue.rule for issue in issues}
