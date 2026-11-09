"""Merge queue/<wave>/*.md (rows `| Назва | рік | чим нова | ⭐ | інші | п | сімʼя |`, family column optional) into
queue/<family>.md under a dated heading; drops rows the corpus already describes, a queue already lists, or the wave
repeats. Dry run by default; `--apply` appends. Usage: queue_merge.py wave3 [--apply]"""
import re
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from difflib import SequenceMatcher  # noqa: E402

from queue_status import SPLIT, described, norm, rows, url_key  # noqa: E402

FAMILIES = {p.name for p in (ROOT / "games").iterdir() if p.is_dir()}
HEAD = "| Назва | рік | чим нова для корпусу | лінк-⭐ | інші лінки | пріоритет |\n|---|---|---|---|---|---|"


def wave_rows(path):
    for line in path.read_text().splitlines():
        if not line.startswith("|") or re.match(r"^\|\s*-{2,}", line) or line.startswith("| Назва"):
            continue
        cols = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cols) < 6 or not cols[0]:
            continue
        fam = cols[6] if len(cols) > 6 and cols[6] in FAMILIES else path.stem
        prio = re.search(r"[123]", cols[5])
        yield {"name": cols[0], "year": cols[1], "why": cols[2], "star": cols[3], "other": cols[4],
               "prio": int(prio.group()) if prio else 3, "family": fam}


def known(r, games):
    """Slug of the corpus game this row names (whole name, aka or ⭐-URL), else None; second value — a near miss to flag.
    Sub-part aliases alone ("7DRL", "Kingdoms" of "Kingdoms and Castles") are only a near miss, not a match."""
    key, full = norm(SPLIT.split(r["name"])[0]), norm(r["name"])
    star = url_key(re.sub(r"\s.*$", "", r["star"]))
    near = (0.0, None)
    for g in games:
        if key in g["full"] or full in g["full"] or (star and star in g["urls"] and "search" not in star and "results" not in star):
            return g["slug"], None
        if key in g["aliases"]:
            near = max(near, (0.9, g["slug"]))
        elif len(key) >= 5:
            for a in g["full"]:
                if len(a) >= 5 and (ratio := SequenceMatcher(None, key, a).ratio()) > near[0]:
                    near = (ratio, g["slug"])
    return None, near[1] if near[0] >= 0.85 else None


def notes(path):  # the agent's header paragraph (sources, what was blocked) — kept with the merged section
    head = path.read_text().split("\n|", 1)[0]
    return " ".join(l.strip() for l in head.splitlines() if l.strip() and not l.startswith("#"))


def main():
    wave, apply = sys.argv[1], "--apply" in sys.argv
    games = described()
    queued = {norm(SPLIT.split(r["name"])[0]) for q in (ROOT / "queue").glob("*.md") if not q.name.startswith("_") for r in rows(q)}
    keep, drop, seen, src, dropped = defaultdict(list), Counter(), set(), {}, []
    for f in sorted((ROOT / "queue" / wave).glob("*.md")):
        src[f.stem] = notes(f)
        for r in wave_rows(f):
            key = norm(SPLIT.split(r["name"])[0])
            slug, near = known(r, games)
            if slug:
                drop["в корпусі"] += 1
                dropped.append(f"{r['name']} → {slug}")
            elif key in queued:
                drop["вже в черзі"] += 1
            elif key in seen:
                drop["дубль у хвилі"] += 1
            else:
                seen.add(key)
                if near:
                    r["why"] += f" (перевірити: ≈ `{near}`)"
                keep[r["family"]].append(r)
    title = wave.replace("wave", "Хвиля ")
    for fam in sorted(keep):
        rs = sorted(keep[fam], key=lambda r: r["prio"])
        print(f"{fam}: +{len(rs)} (п1 {sum(r['prio'] == 1 for r in rs)} · п2 {sum(r['prio'] == 2 for r in rs)} · п3 {sum(r['prio'] == 3 for r in rs)})")
        if apply:
            part = [f"\n## {title} — {date.today()}: нові кандидати (пошукові агенти Opus)\n"]
            if src.get(fam):
                part.append(src[fam] + "\n")
            part += [HEAD] + [f"| {r['name']} | {r['year']} | {r['why']} | {r['star']} | {r['other']} | {r['prio']} |" for r in rs]
            with (ROOT / "queue" / f"{fam}.md").open("a") as fh:
                fh.write("\n".join(part) + "\n")
    print(f"разом +{sum(len(v) for v in keep.values())} · відкинуто: " + " · ".join(f"{k} {v}" for k, v in drop.items()) + ("" if apply else " · (dry run, --apply щоб записати)"))
    if dropped:
        print("в корпусі: " + " · ".join(dropped))


if __name__ == "__main__":
    main()
