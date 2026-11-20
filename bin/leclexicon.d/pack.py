"""lexicon.json: { "v": 1, "lemmas": [[lemma, form, …], …], "stop": [word, …] } — CONTRACT §6.1 plus "stop"."""
from __future__ import annotations

import json
from pathlib import Path

from corpus import SEARCH

LEXICON = SEARCH / "lexicon.json"


def prune(groups: dict[tuple, set[str]]) -> list[list[str]]:
    """Groups worth shipping: 2+ forms, none inside another group of the same lemma; lemma first, then sorted."""
    by_lemma: dict[str, list[set[str]]] = {}
    for (lemma, _), forms in groups.items():
        by_lemma.setdefault(lemma, []).append(forms | {lemma})
    out = []
    for lemma, sets in sorted(by_lemma.items()):
        sets.sort(key=lambda s: (-len(s), sorted(s)))
        kept: list[set[str]] = []
        for s in sets:
            if len(s) > 1 and not any(s <= k for k in kept):  # "головний" the noun is a part of the adjective
                kept.append(s)
        out += [[lemma] + sorted(s - {lemma}) for s in kept]
    return out


def dump(lemmas: list[list[str]], stop: list[str], path: Path = LEXICON) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)

    def line(value) -> str:
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))

    rows = ",\n".join(map(line, lemmas))  # a group a line: readable git diffs
    path.write_text('{"v":1,"lemmas":[\n' + rows + '\n],\n"stop":' + line(stop) + "}\n", encoding="utf-8")
    return path.stat().st_size


def read(path: Path = LEXICON) -> dict:
    if not path.exists():
        return {"lemmas": [], "stop": []}
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("v") != 1:
        raise SystemExit(f"{path.name}: невідома версія {data.get('v')!r}")
    return data


def load(path: Path = LEXICON) -> list[list[str]]:
    return read(path)["lemmas"]


def index(lemmas: list[list[str]]) -> dict[str, set[str]]:
    """Form → every form of every group it belongs to (itself included): what the search will accept for it."""
    out: dict[str, set[str]] = {}
    for group in lemmas:
        for form in group:
            out.setdefault(form, set()).update(group)
    return out
