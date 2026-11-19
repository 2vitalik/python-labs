"""Lint games/*/*.md against TEMPLATE.md: front matter, sections, vocab values, duplicates. Exit 1 on problems."""
import re
import sys
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
FAMILIES = {p.name for p in (ROOT / "games").iterdir() if p.is_dir()}
KLASS = {"avatar", "cursor", "figure", "puzzle", "hybrid"}
AXES = {
    "field": {"square", "hex", "graph", "free", "iso", "layers", "1d", "3d", "nested", "hyperbolic", "pyramid", "tri", "tube"},
    "time": {"turn", "realtime", "static", "rhythm", "programmed", "wego"},
    "opponent": {"none", "ai", "hotseat", "online", "coop", "live"},
    "info": {"full", "hidden", "partial", "asymmetric"},
    "random": {"none", "setup", "runtime", "both"},
    "goal": {"score", "survive", "state", "constraints", "race", "territory", "collect", "none"},
}
STAGES = {"v1", "v2", "v3"}
REQUIRED = ["title", "slug", "family", "klass", "axes", "links", "stage", "coverage", "mechanics", "author", "date"]
SECTIONS = ["Суть", "Поле і час", "Сутності", "Правила (КОЛИ → ЯКЩО → ТО)", "Керування і ввід", "Вікна, меню, HUD",
            "Фічі поза полем", "Варіації й родичі", "Цікавинки для курсу", "Мапа на каталог", "Пропозиції до словників",
            "Джерела", "Непевне"]
PREFIX = {"trigger", "cond", "effect", "role", "window", "ui", "feature", "axis", "card"}


def split(text):
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        return None, text
    try:
        return yaml.safe_load(m.group(1)), m.group(2)
    except yaml.YAMLError as e:
        return {"_yaml_error": str(e).splitlines()[-1]}, m.group(2)


def cards():
    p = ROOT / "vocab" / "catalog-cards.md"
    return set(re.findall(r"^\| `([\w-]+)`", p.read_text(), re.M)) if p.exists() else set()


def check(path, fm, body, known):
    errs = []
    if fm is None:
        return ["шапка YAML не читається"]
    if "_yaml_error" in fm:
        return [f"YAML: {fm['_yaml_error']}"]
    for k in REQUIRED:
        if k not in fm:
            errs.append(f"нема поля {k}")
    if fm.get("slug") != path.stem:
        errs.append(f"slug {fm.get('slug')!r} ≠ імʼя файла")
    if fm.get("family") != path.parent.name:
        errs.append(f"family {fm.get('family')!r} ≠ тека {path.parent.name}")
    if fm.get("klass") not in KLASS:
        errs.append(f"klass {fm.get('klass')!r}")
    for ax, allowed in AXES.items():
        v = (fm.get("axes") or {}).get(ax)
        if v is None:
            errs.append(f"axes.{ax} відсутня")
        elif v not in allowed:
            errs.append(f"axes.{ax}={v!r} не зі словника")
    if fm.get("stage") not in STAGES:
        errs.append(f"stage {fm.get('stage')!r}")
    links = fm.get("links") or []
    if not links:
        errs.append("нема лінків")
    if sum(1 for l in links if isinstance(l, dict) and l.get("best")) != 1:
        errs.append("має бути рівно один best: true")
    for l in links:
        if not isinstance(l, dict) or not str(l.get("url", "")).startswith("http"):
            errs.append(f"лінк без url: {l!r}")
    cov = fm.get("coverage")
    if not isinstance(cov, int) or not 0 <= cov <= 100:
        errs.append(f"coverage {cov!r} не 0–100")
    for t in fm.get("mechanics") or []:
        if not re.fullmatch(r"\+?[a-z0-9]+(-[a-z0-9]+)*", str(t)):
            errs.append(f"тег {t!r} не kebab")
        elif not t.startswith("+") and known and t not in known:
            errs.append(f"тег {t!r} нема в каталозі (додай «+»)")
    for p in fm.get("proposes") or []:
        m = re.fullmatch(r"\+(\w+):(.+)", str(p))
        if not m or m.group(1) not in PREFIX:
            errs.append(f"пропозиція {p!r} без префікса виду")
    heads = re.findall(r"^## (.+?)\s*$", body, re.M)
    for s in SECTIONS:
        if s not in heads:
            errs.append(f"нема секції «{s}»")
    if heads and [h for h in heads if h in SECTIONS] != [s for s in SECTIONS if s in heads]:
        errs.append("порядок секцій не як у шаблоні")
    if re.search(r"youtube\.com/watch\?v=|youtu\.be/", body + str(links)) and "results?search_query" not in body + str(links):
        pass  # direct video links are fine when verified; nothing to check mechanically
    return errs


def main():
    known = cards()
    files = sorted((ROOT / "games").glob("*/*.md"))
    problems, slugs = 0, Counter()
    for f in files:
        fm, body = split(f.read_text())
        slugs[f.stem] += 1
        errs = check(f, fm, body, known)
        if errs:
            problems += 1
            print(f"{f.relative_to(ROOT)}:")
            for e in errs:
                print(f"  - {e}")
    for s, n in slugs.items():
        if n > 1:
            problems += 1
            print(f"дубль slug: {s} ×{n}")
    print(f"{len(files)} файлів · {problems} з проблемами")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
