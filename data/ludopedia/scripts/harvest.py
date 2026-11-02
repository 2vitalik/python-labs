"""index/harvest.md: section-level harvest — windows/HUD/features tokens, proposed cards, taxonomy matrices, custom-rule density."""
import re
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "index" / "harvest.md"
SEC = {"win": "Вікна, меню, HUD", "feat": "Фічі поза полем", "rules": "Правила (КОЛИ → ЯКЩО → ТО)", "map": "Мапа на каталог"}


def vocab_words(name):
    return set(re.findall(r"`([a-z][a-z0-9-]+)`", (ROOT / "vocab" / name).read_text()))


def section(body, name):
    m = re.search(rf"^## {re.escape(name)}\s*\n(.*?)(?=^## |\Z)", body, re.S | re.M)
    return m.group(1) if m else ""


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
        fm["_body"], fm["_path"] = m.group(2), f.relative_to(ROOT).as_posix()
        games.append(fm)
    return games


def tokens(games, sec, known):
    cnt, unknown = Counter(), Counter()
    for g in games:
        seen = set(re.findall(r"`\+?([a-z][a-z0-9-]+)`", section(g["_body"], SEC[sec])))
        for t in seen:
            (cnt if t in known else unknown)[t] += 1
    return cnt, unknown


def cards(games):
    rows = defaultdict(list)  # slug -> [(title, zone, coin, game)]
    pat = re.compile(r"`\+([a-z0-9-]+)`\s*«([^»]*)»\s*·\s*([a-z-]+/[a-z-]+|[a-z-]+)\s*·\s*([🌱📎🥉🥈🥇👑]|без монетки|—)?")
    for g in games:
        for line in section(g["_body"], SEC["map"]).splitlines():
            for m in pat.finditer(line):
                rows[m.group(1)].append((m.group(2), m.group(3), m.group(4) or "", g.get("title")))
    return rows


def main():
    games = load()
    out = [f"# Жнива по секціях (автоген) · {date.today()} · {len(games)} ігор", ""]
    for sec, vocab, title in (("win", "windows.md", "Вікна"), ("win", "ui-elements.md", "HUD-елементи"), ("feat", "features.md", "Фічі поза полем")):
        known = vocab_words(vocab)
        cnt, unknown = tokens(games, sec, known)
        out += [f"## {title} — слова словника `{vocab}` у секції «{SEC[sec]}»", "", "Відомі: " + " · ".join(f"`{t}` ×{n}" for t, n in cnt.most_common(60)), ""]
        if title == "Фічі поза полем" or title == "Вікна":
            out += ["Невідомі словнику (≥2 ігор): " + " · ".join(f"`{t}` ×{n}" for t, n in unknown.most_common(80) if n >= 2), ""]
    out += ["## Пропоновані картки з «Мапи на каталог» (рядок «`+slug` «Назва» · зона · монетка»)", "", "| +slug | Назва (перша) | Зона | Монетки | Ігор | Ігри |", "|---|---|---|---|---|---|"]
    for slug, rs in sorted(cards(games).items(), key=lambda x: (-len(x[1]), x[0])):
        zones = Counter(z for _, z, _, _ in rs).most_common(1)[0][0]
        coins = "".join(sorted({c for _, _, c, _ in rs if c}))
        out.append(f"| `+{slug}` | {rs[0][0]} | {zones} | {coins} | {len(rs)} | {', '.join(sorted({str(g) for *_, g in rs}))[:120]} |")
    out += ["", "## Таксономія", ""]
    fam_k = defaultdict(Counter)
    for g in games:
        fam_k[g.get("family")][g.get("klass")] += 1
    ks = ["avatar", "cursor", "figure", "puzzle", "hybrid"]
    out += ["| Сімʼя | " + " | ".join(ks) + " |", "|---|" + "---|" * len(ks)]
    for fam in sorted(fam_k):
        out.append(f"| {fam} | " + " | ".join(str(fam_k[fam][k] or "") for k in ks) + " |")
    out += [""]
    for ax in ("field", "time", "opponent", "info", "random", "goal"):
        c = Counter(str((g.get("axes") or {}).get(ax)) for g in games)
        out.append(f"- `{ax}`: " + " · ".join(f"{v} ×{n}" for v, n in c.most_common()))
    also = Counter(a for g in games for a in (g.get("also") or []))
    out += ["- `also`: " + " · ".join(f"{a} ×{n}" for a, n in also.most_common()), ""]
    out += ["## Щільність `custom` у правилах і покриття по сімʼях", "", "| Сімʼя | Ігор | Рядків правил | з `custom` | % custom | Середнє покриття |", "|---|---|---|---|---|---|"]
    stat = defaultdict(lambda: [0, 0, 0, 0])
    for g in games:
        rules = [l for l in section(g["_body"], SEC["rules"]).splitlines() if l.strip().startswith("-")]
        s = stat[g.get("family")]
        s[0] += 1; s[1] += len(rules); s[2] += sum("custom" in l for l in rules); s[3] += int(g.get("coverage") or 0)
    for fam, (n, r, c, cov) in sorted(stat.items()):
        out.append(f"| {fam} | {n} | {r} | {c} | {100 * c / r if r else 0:.0f}% | {cov / n:.0f}% |")
    tot = [sum(v[i] for v in stat.values()) for i in range(4)]
    out.append(f"| **разом** | {tot[0]} | {tot[1]} | {tot[2]} | {100 * tot[2] / tot[1]:.0f}% | {tot[3] / tot[0]:.0f}% |")
    OUT.write_text("\n".join(out) + "\n")
    print(f"harvest: {len(games)} games → {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    sys.exit(main())
