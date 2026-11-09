"""index/queue-status.md + .json: which queue candidates are already described (title / aka / slug / ⭐-URL match),
what remains per family and priority. `maybe` = close but not exact — the curator eyeballs those."""
import json
import re
import sys
from collections import Counter, defaultdict
from difflib import SequenceMatcher
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SPLIT = re.compile(r"\s*(?:/|\+|·|—|–|;|\(|\)|\[|\]|,| і | and | або | or )\s*")


def norm(s: str) -> str:
    s = re.sub(r"[’'`´!?:.*]", "", str(s).lower())
    s = re.sub(r"^(the|a|an)\s+", "", s)
    return " ".join(re.sub(r"[^a-z0-9а-яіїєґ]+", " ", s).split())


def names(title: str) -> set[str]:
    out = {n for n in (norm(p) for p in SPLIT.split(title) if p) if len(n) >= 3}
    if n := norm(title):
        out.add(n)
    return out


def url_key(u: str) -> str:
    return re.sub(r"^https?://(www\.)?", "", str(u).strip().lower()).rstrip("/")


def described():
    games = []
    for f in sorted((ROOT / "games").glob("*/*.md")):
        m = re.match(r"^---\n(.*?)\n---\n", f.read_text(), re.S)
        if not m:
            continue
        try:
            fm = yaml.safe_load(m.group(1)) or {}
        except yaml.YAMLError:
            continue
        aliases = names(str(fm.get("title", ""))) | {norm(f.stem.replace("-", " "))}
        full = {norm(str(fm.get("title", ""))), norm(f.stem.replace("-", " "))}  # whole names only, no sub-parts
        for a in fm.get("aka") or []:
            aliases |= names(str(a))
            full.add(norm(str(a)))
        urls = {url_key(l["url"]) for l in fm.get("links") or [] if isinstance(l, dict) and l.get("url")}
        games.append({"slug": f.stem, "family": f.parent.name, "title": fm.get("title"), "aliases": aliases, "full": full, "urls": urls})
    return games


def rows(path: Path):
    for line in path.read_text().splitlines():
        if not line.startswith("|") or re.match(r"^\|\s*-{2,}", line) or line.startswith("| Назва"):
            continue
        cols = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cols) < 6:
            continue
        prio = re.search(r"[123]", cols[-1])
        yield {"name": cols[0], "year": cols[1], "why": cols[2], "star": cols[3], "other": cols[4], "prio": int(prio.group()) if prio else 3}


def classify(row, games):
    cands = names(row["name"])
    first = norm(SPLIT.split(row["name"])[0]) if row["name"] else ""
    star = url_key(re.sub(r"\s.*$", "", row["star"]))
    best = (0.0, None)
    for g in games:
        if cands & g["aliases"] or (star and star in g["urls"] and "search" not in star and "results" not in star):
            return "described", g["slug"]
        for a in g["aliases"]:
            if len(first) >= 5 and len(a) >= 5:
                r = SequenceMatcher(None, first, a).ratio()
                if r > best[0]:
                    best = (r, g["slug"])
    if best[0] >= 0.92:
        return "described", best[1]
    if best[0] >= 0.8:
        return "maybe", best[1]
    return "remaining", None


def main():
    games = described()
    status, out = {}, ["# Стан черг (автоген)", "", f"`scripts/queue_status.py` · {len(games)} описаних ігор у корпусі.", ""]
    total = Counter()
    for q in sorted((ROOT / "queue").glob("*.md")):
        if q.name.startswith("_"):
            continue
        fam = q.stem
        items = []
        for row in rows(q):
            row["status"], row["match"] = classify(row, games)
            items.append(row)
        status[fam] = items
        c = Counter((r["status"], r["prio"]) for r in items)
        rem = [r for r in items if r["status"] == "remaining"]
        for r in rem:
            total[r["prio"]] += 1
        out += [f"## {fam} · у черзі {len(items)} · описано {sum(1 for r in items if r['status'] == 'described')} · "
                f"лишилось {len(rem)} (п1 {c[('remaining', 1)]} · п2 {c[('remaining', 2)]} · п3 {c[('remaining', 3)]})", ""]
        if rem:
            out += ["| Назва | рік | чим нова | ⭐ | інші | п |", "|---|---|---|---|---|---|"]
            out += [f"| {r['name']} | {r['year']} | {r['why']} | {r['star']} | {r['other']} | {r['prio']} |" for r in sorted(rem, key=lambda r: r["prio"])]
            out.append("")
        maybe = [r for r in items if r["status"] == "maybe"]
        if maybe:
            out += ["Можливо вже описані (перевірити): " + " · ".join(f"{r['name']} ≈ `{r['match']}`" for r in maybe), ""]
    out.insert(3, f"Лишилось описати: п1 {total[1]} · п2 {total[2]} · п3 {total[3]} = {sum(total.values())}.")
    (ROOT / "index" / "queue-status.md").write_text("\n".join(out))
    (ROOT / "index" / "queue-status.json").write_text(json.dumps(status, ensure_ascii=False, indent=1))
    print(f"queue-status: remaining p1 {total[1]} · p2 {total[2]} · p3 {total[3]}")


if __name__ == "__main__":
    sys.exit(main())
