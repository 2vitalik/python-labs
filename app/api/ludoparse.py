"""One corpus file (data/ludopedia/games/<family>/<slug>.md) → the dict of models/ludo_game.py:
the YAML head as is, the body by H2 (TEMPLATE.md), the entities table, the rules and the sources parsed on top."""
import re
from pathlib import Path

import yaml

SECTIONS = {  # H2 of TEMPLATE.md → key
    "Суть": "essence", "Поле і час": "field", "Сутності": "entities", "Правила (КОЛИ → ЯКЩО → ТО)": "rules",
    "Керування і ввід": "controls", "Вікна, меню, HUD": "ui", "Фічі поза полем": "features", "Варіації й родичі": "variations",
    "Цікавинки для курсу": "course", "Мапа на каталог": "catalog_map", "Пропозиції до словників": "proposals",
    "Джерела": "sources", "Непевне": "uncertain",
}
HEAD = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.DOTALL)
TERM = re.compile(r"`([^`]+)`")
LINK = re.compile(r"\[([^\]]+)\]\((https?://[^)\s]+)\)")


def strs(xs) -> list[str]:
    return [str(x) for x in xs or []]


def parse(path: Path, root: Path) -> dict | None:
    m = HEAD.match(path.read_text())
    if not m:
        return None
    fm, body = yaml.safe_load(m.group(1)) or {}, m.group(2)
    h1 = re.search(r"^# (.+)$", body, re.MULTILINE)
    headline = h1.group(1).split(" — ", 1)[1].strip() if h1 and " — " in h1.group(1) else ""
    sections = split(body)
    return {
        "slug": str(fm.get("slug") or path.stem), "title": str(fm.get("title") or path.stem), "headline": headline,
        "aka": strs(fm.get("aka")), "family": str(fm.get("family") or path.parent.name), "also": strs(fm.get("also")),
        "klass": str(fm.get("klass") or ""), "axes": {k: str(v) for k, v in (fm.get("axes") or {}).items()},
        "year": str(fm.get("year") or ""), "platforms": strs(fm.get("platforms")),
        "links": [l for l in fm.get("links") or [] if isinstance(l, dict)], "stage": str(fm.get("stage") or "v1"),
        "coverage": int(fm.get("coverage") or 0), "mechanics": strs(fm.get("mechanics")), "proposes": strs(fm.get("proposes")),
        "author": str(fm.get("author") or ""), "date": str(fm.get("date") or ""), "sections": sections,
        "entities": table(sections.get("entities", "")), "rules": rules(sections.get("rules", "")),
        "sources": sources(sections.get("sources", "")), "path": path.relative_to(root).as_posix(),
    }


def split(body: str) -> dict:
    out, heads = {}, list(re.finditer(r"^## (.+?)\s*$", body, re.MULTILINE))
    for i, h in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(body)
        out[SECTIONS.get(h.group(1), h.group(1))] = body[h.end():end].strip()
    return out


def table(text: str) -> list[dict]:
    rows = [[c.strip() for c in ln.strip().strip("|").split("|")] for ln in text.splitlines() if ln.startswith("|") and not re.match(r"^\|\s*-{2,}", ln)]
    keys = ("name", "role", "params", "behavior")
    return [dict(zip(keys, r + [""] * 4)) for r in rows[1:] if r and r[0]]


def rules(text: str) -> list[dict]:
    out = []
    for ln in text.splitlines():
        if not ln.startswith("- "):
            continue
        s = ln[2:].strip()
        r = {"text": s, "when": [], "cond": [], "then": []}
        for label, key in (("КОЛИ", "when"), ("ЯКЩО", "cond"), ("ТО", "then")):
            for m in re.finditer(rf"(?<![\w])(?:{label})\s+(.*?)(?=\s*→\s*(?:КОЛИ|ЯКЩО|ТО)\b|$)", s):
                r[key] += TERM.findall(m.group(1))
        out.append(r)
    return out


def sources(text: str) -> list[dict]:
    out = []
    for ln in text.splitlines():
        if not ln.startswith("- "):
            continue
        s, link = ln[2:].strip(), LINK.search(ln)
        note = s.split(" — ", 1)[1].strip() if " — " in s else ""
        out.append({"title": link.group(1) if link else s.replace("⭐", "").strip(), "url": link.group(2) if link else "",
                    "note": note, "best": "⭐" in s})
    return out
