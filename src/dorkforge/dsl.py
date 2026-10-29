"""A small dork DSL that compiles to engine-specific query syntax.

The point is not to hide syntax but to make the *intent* portable. One dork
("find exposed git configuration on this host") compiles to Google's operators,
GitHub's code-search filters or Shodan's facet names, and the compiler refuses
rather than guessing when a field has no equivalent on that engine.
"""

from __future__ import annotations

import re
import urllib.parse
from dataclasses import dataclass, field
from typing import Iterable, Sequence

ENGINES = ("google", "github", "shodan")

# field -> per-engine operator name. None means the engine has no equivalent.
FIELDS: dict[str, dict[str, str | None]] = {
    "site": {"google": "site", "github": None, "shodan": None},
    "inurl": {"google": "inurl", "github": "path", "shodan": None},
    "intitle": {"google": "intitle", "github": None, "shodan": "http.title"},
    "intext": {"google": "intext", "github": None, "shodan": "http.html"},
    "filetype": {"google": "filetype", "github": "extension", "shodan": None},
    "ext": {"google": "filetype", "github": "extension", "shodan": None},
    "filename": {"google": None, "github": "filename", "shodan": None},
    "path": {"google": None, "github": "path", "shodan": None},
    "language": {"google": None, "github": "language", "shodan": None},
    "repo": {"google": None, "github": "repo", "shodan": None},
    "user": {"google": None, "github": "user", "shodan": None},
    "org": {"google": None, "github": "org", "shodan": "org"},
    "hostname": {"google": None, "github": None, "shodan": "hostname"},
    "net": {"google": None, "github": None, "shodan": "net"},
    "port": {"google": None, "github": None, "shodan": "port"},
    "country": {"google": None, "github": None, "shodan": "country"},
    "server": {"google": None, "github": None, "shodan": "server"},
    "product": {"google": None, "github": None, "shodan": "product"},
    "has": {"google": None, "github": None, "shodan": "has"},
    "os": {"google": None, "github": None, "shodan": "os"},
}

SEARCH_URLS = {
    "google": "https://www.google.com/search?q=",
    "github": "https://github.com/search?type=code&q=",
    "shodan": "https://www.shodan.io/search?query=",
}

TEMPLATE = "https://{engine}/search"


class DorkError(ValueError):
    """A dork that cannot be compiled for the requested engine."""


@dataclass(frozen=True)
class Term:
    """One unit of a dork: a field query, a quoted phrase or a bare word."""

    kind: str  # "field" | "phrase" | "word" | "operator"
    value: str
    negated: bool = False
    quoted: bool = False

    def render(self) -> str:
        if self.kind == "phrase" or (self.kind == "field" and self.quoted):
            name, _, rest = self.value.partition(":")
            inner = f'{name}:"{rest}"' if self.kind == "field" else f'"{self.value}"'
            return f"-{inner}" if self.negated else inner
        inner = self.value
        if self.kind == "operator":
            return self.value
        return f"-{inner}" if self.negated else inner


@dataclass(frozen=True)
class Dork:
    terms: tuple[Term, ...]
    raw: str

    @property
    def plain(self) -> str:
        return " ".join(term.render() for term in self.terms)


@dataclass
class CompileResult:
    engine: str
    query: str
    url: str
    used: list[tuple[str, str]]
    rewrites: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return {
            "engine": self.engine,
            "query": self.query,
            "url": self.url,
            "used": [{"field": name, "operator": operator} for name, operator in self.used],
            "rewrites": self.rewrites,
            "notes": self.notes,
        }


TOKEN_RE = re.compile(r'(-?)(?:([a-z_]+):)?(?:"([^"]*)"|([^\s"]+))')


def parse(text: str) -> Dork:
    """Tokenise a dork. Quoted values keep their spaces; ``-`` negates."""
    if not text or not text.strip():
        raise DorkError("dork is empty")
    if text.count('"') % 2 != 0:
        raise DorkError("unbalanced double quote")
    terms: list[Term] = []
    position = 0
    for match in TOKEN_RE.finditer(text):
        if match.start() != position:
            gap = text[position : match.start()]
            if gap.strip():
                raise DorkError(f"unparsable segment: {gap.strip()!r}")
        position = match.end()
        negated, key, quoted, bare = match.group(1), match.group(2), match.group(3), match.group(4)
        value = quoted if quoted is not None else (bare or "")
        if quoted is None and value in ("OR", "AND", "NOT"):
            terms.append(Term(kind="operator", value=value))
            continue
        if key is None and bare and bare.endswith(":"):
            name = bare[:-1]
            if name in FIELDS:
                raise DorkError(f"field {name!r} has an empty value")
        if key:
            if key not in FIELDS:
                raise DorkError(
                    f"unknown field {key!r}; known: {', '.join(sorted(FIELDS))}"
                )
            if not value:
                raise DorkError(f"field {key!r} has an empty value")
            terms.append(
                Term(
                    kind="field",
                    value=f"{key}:{value}",
                    negated=bool(negated),
                    quoted=quoted is not None,
                )
            )
        elif quoted is not None:
            terms.append(Term(kind="phrase", value=quoted, negated=bool(negated)))
        else:
            terms.append(Term(kind="word", value=value, negated=bool(negated)))
    tail = text[position:]
    if tail.strip():
        raise DorkError(f"unparsable tail: {tail.strip()!r}")
    if not terms:
        raise DorkError("dork produced no terms")
    return Dork(terms=tuple(terms), raw=text.strip())


def _split_field(value: str) -> tuple[str, str]:
    name, _, rest = value.partition(":")
    return name, rest


def compile_dork(text: str | Dork, engine: str) -> CompileResult:
    """Compile a dork for one engine, refusing fields that do not exist there."""
    if engine not in ENGINES:
        raise DorkError(f"unknown engine {engine!r}; choose from {', '.join(ENGINES)}")
    dork = parse(text) if isinstance(text, str) else text

    pieces: list[str] = []
    used: list[tuple[str, str]] = []
    rewrites: list[str] = []
    for term in dork.terms:
        if term.kind == "field":
            name, value = _split_field(term.value)
            operator = FIELDS[name][engine]
            if operator is None:
                supported = sorted(
                    key for key, mapping in FIELDS.items() if mapping[engine]
                )
                raise DorkError(
                    f"field {name!r} does not exist on {engine}; supported there: "
                    + ", ".join(supported)
                )
            if operator != name:
                rewrites.append(f"{name} -> {operator}")
            rendered = f'{operator}:"{value}"' if term.quoted else f"{operator}:{value}"
            used.append((name, operator))
        elif term.kind == "phrase":
            rendered = f'"{term.value}"'
        else:
            rendered = term.value
        if term.negated:
            rendered = f"-{rendered}"
        pieces.append(rendered)

    query = " ".join(pieces)
    if engine == "google" and any(term.kind == "operator" for term in dork.terms):
        query = query.replace("OR", "OR")
    url = SEARCH_URLS[engine] + urllib.parse.quote_plus(query)
    notes: list[str] = []
    if engine == "github" and any(_split_field(t.value)[0] == "site" for t in dork.terms if t.kind == "field"):
        notes.append("GitHub has no site: operator; search the org or repo explicitly")
    if engine == "shodan":
        notes.append("Shodan indexes services, not pages: text filters apply to what it crawled")
    return CompileResult(engine=engine, query=query, url=url, used=used, rewrites=rewrites, notes=notes)


def compile_all(text: str | Dork) -> dict[str, CompileResult | str]:
    """Compile for every engine, reporting the ones that cannot express the dork."""
    results: dict[str, CompileResult | str] = {}
    for engine in ENGINES:
        try:
            results[engine] = compile_dork(text, engine)
        except DorkError as exc:
            results[engine] = str(exc)
    return results


def validate(text: str) -> list[str]:
    """Return every problem that stops this dork from compiling anywhere."""
    problems: list[str] = []
    try:
        dork = parse(text)
    except DorkError as exc:
        return [str(exc)]
    for term in dork.terms:
        if term.kind == "field":
            name, value = _split_field(term.value)
            if not value.strip():
                problems.append(f"field {name!r} has an empty value")
    engines_ok = [
        engine
        for engine in ENGINES
        if all(FIELDS[_split_field(term.value)[0]][engine] for term in dork.terms if term.kind == "field")
    ]
    if not engines_ok:
        problems.append("no engine supports every field in this dork")
    return problems


def explore(text: str) -> dict[str, object]:
    """One machine-readable view: terms, per-engine results and validation."""
    dork = parse(text)
    return {
        "raw": dork.raw,
        "plain": dork.plain,
        "terms": [
            {"kind": term.kind, "value": term.value, "negated": term.negated}
            for term in dork.terms
        ],
        "fields": sorted(
            {_split_field(term.value)[0] for term in dork.terms if term.kind == "field"}
        ),
        "problems": validate(text),
        "engines": {
            engine: (
                result.to_dict() if isinstance(result, CompileResult) else {"error": result}
            )
            for engine, result in compile_all(dork).items()
        },
    }


def fields_for(engine: str) -> list[str]:
    """Fields that compile on one engine, for help output and validation."""
    if engine not in ENGINES:
        raise DorkError(f"unknown engine {engine!r}")
    return sorted(key for key, mapping in FIELDS.items() if mapping[engine])
