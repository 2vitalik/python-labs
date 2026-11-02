"""index/: README (registry + stats), mechanics (tag → games), proposals (harvested vocabulary proposals)."""
import re
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "index"
KL = {"avatar": "аватарна", "cursor": "курсорна", "figure": "фігурна", "puzzle": "пазл", "hybrid": "гібрид"}


def load():
    games = []
    for f in sorted((ROOT / "games").glob("*/*.md")):
        m = re.match(r"^---\n(.*?)\n---\n(.*)$", f.read_text(), re.S)
        if not m:
            continue
        try:
            fm = yaml.safe_load(m.group(1)) or {}
        except yaml.YAMLError:
            continue
        fm["_path"], fm["_body"] = f.relative_to(ROOT).as_posix(), m.group(2)
        games.append(fm)
    return games


def best(fm):
    for l in fm.get("links") or []:
        if isinstance(l, dict) and l.get("best"):
            return f"[{l.get('kind', 'link')}]({l['url']})"
    return "—"


def section(body, name):
    m = re.search(rf"^## {re.escape(name)}\s*\n(.*?)(?=^## |\Z)", body, re.S | re.M)
    return m.group(1).strip() if m else ""


def readme(games):
    fam = defaultdict(list)
    for g in games:
        fam[g.get("family", "?")].append(g)
    stages, klass = Counter(g.get("stage") for g in games), Counter(g.get("klass") for g in games)
    out = ["# Реєстр корпусу (автоген)", "", f"`scripts/build_index.py` · {date.today()} · **{len(games)} ігор** у {len(fam)} сімʼях.", "",
           "- Зрілість: " + " · ".join(f"{k}: {v}" for k, v in sorted(stages.items())),
           "- Класи: " + " · ".join(f"{KL.get(k, k)}: {v}" for k, v in klass.most_common()),
           "- Середнє покриття структурою: " + (f"{sum(int(g.get('coverage') or 0) for g in games) / len(games):.0f}%" if games else "—"),
           "- Механік-тегів унікальних: " + str(len({t for g in games for t in g.get("mechanics") or []})) +
           " · пропозицій до словників: " + str(sum(len(g.get("proposes") or []) for g in games)), ""]
    for family in sorted(fam):
        out += [f"## {family} · {len(fam[family])}", "", "| Гра | Клас | Рік | Осі | Стадія | Покриття | Тегів | ⭐ Вхід |", "|---|---|---|---|---|---|---|---|"]
        for g in sorted(fam[family], key=lambda x: str(x.get("title"))):
            ax = g.get("axes") or {}
            axes = "/".join(str(ax.get(k, "?")) for k in ("field", "time", "opponent", "info", "random", "goal"))
            out.append(f"| [{g.get('title')}]({'../' + g['_path']}) | {KL.get(g.get('klass'), g.get('klass'))} | {g.get('year', '')} | `{axes}` | {g.get('stage')} | {g.get('coverage', '')}% | {len(g.get('mechanics') or [])} | {best(g)} |")
        out.append("")
    (OUT / "README.md").write_text("\n".join(out))


def mechanics(games):
    by = defaultdict(list)
    for g in games:
        for t in g.get("mechanics") or []:
            by[str(t)].append(g)
    known = [(t, gs) for t, gs in by.items() if not t.startswith("+")]
    new = [(t, gs) for t, gs in by.items() if t.startswith("+")]
    out = ["# Механіки → ігри (автоген)", "", f"{len(known)} тегів каталогу · {len(new)} нових (`+`); нове з ≥3 іграми — кандидат у картку за правилом трьох.", ""]
    for title, rows in (("Нові (`+`) — відсортовано за частотою", new), ("Картки каталогу", known)):
        out += [f"## {title}", ""]
        for t, gs in sorted(rows, key=lambda x: (-len(x[1]), x[0])):
            flag = " 🔥" if t.startswith("+") and len(gs) >= 3 else ""
            names = ", ".join(f"[{g.get('title')}]({'../' + g['_path']})" for g in sorted(gs, key=lambda x: str(x.get("title"))))
            out.append(f"- `{t}` ×{len(gs)}{flag} — {names}")
        out.append("")
    (OUT / "mechanics.md").write_text("\n".join(out))


def proposals(games):
    kinds = defaultdict(list)
    for g in games:
        for p in g.get("proposes") or []:
            m = re.fullmatch(r"\+(\w+):(.+)", str(p))
            if m:
                kinds[m.group(1)].append((m.group(2).strip(), g))
    out = ["# Пропозиції до словників (автоген)", "", "Зібрано з шапок (`proposes`) і секцій «Пропозиції до словників». Частота ≥3 🔥 — правило трьох.", ""]
    for kind in sorted(kinds):
        cnt = Counter(name for name, _ in kinds[kind])
        out += [f"## {kind} · {len(cnt)}", ""]
        for name, n in cnt.most_common():
            gs = sorted({g.get("title") for nm, g in kinds[kind] if nm == name})
            out.append(f"- `{name}` ×{n}{' 🔥' if n >= 3 else ''} — {', '.join(map(str, gs))}")
        out.append("")
    out += ["## Тексти секцій «Пропозиції до словників»", ""]
    for g in sorted(games, key=lambda x: str(x.get("title"))):
        sec = section(g["_body"], "Пропозиції до словників")
        if sec and sec != "—":
            out += [f"### {g.get('title')} · `{g['_path']}`", "", sec, ""]
    (OUT / "proposals.md").write_text("\n".join(out))


def main():
    OUT.mkdir(exist_ok=True)
    games = load()
    readme(games), mechanics(games), proposals(games)
    print(f"index: {len(games)} games")


if __name__ == "__main__":
    sys.exit(main())
