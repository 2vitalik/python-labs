"""Packs of ≤5 queue rows for describe agents: `remaining` rows (p1 first) plus `maybe` rows (fuzzy match to a slug —
nearly always a different game, so the row carries a ⚠ hint); `skipped` rows never. All p1–p2 packs come before
any p3 pack (a pack never mixes them), round-robin across families inside each tier. Reads index/queue-status.json
(run queue_status.py first); prints the prompts for packs from..to and writes batches-<P>.json to --out (outside the repo).
Usage: make_batches.py [from] [to] [--prefix I] [--out DIR] [--skip I1-12,H3] [--no-maybe]"""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BRIEF = ROOT / "AGENT-BRIEF.md"
SIZE = 5
norm = lambda s: re.sub(r"[^a-z0-9]+", " ", s.lower().split("(")[0].split("/")[0]).strip()  # noqa: E731


def load(args):
    status = json.loads((ROOT / "index" / "queue-status.json").read_text())
    seen = set()
    for spec in filter(None, args.skip.split(",")):  # packs still in flight: their rows have no file yet
        pfx, lo, _, hi = re.match(r"([A-Z])(\d+)(-(\d+))?$", spec).groups()
        for b in json.loads((args.out / f"batches-{pfx}.json").read_text()):
            if int(lo) <= int(b["id"][1:]) <= int(hi or lo):
                seen |= {norm(r["name"]) for r in b["rows"]}
    tiers = ({}, {})  # p1–p2, then p3: a run cut short by a limit leaves only the minor rows undone
    for fam, items in sorted(status.items()):
        rows = []
        for r in sorted(items, key=lambda r: (r["status"] == "maybe", r["prio"])):
            if r["status"] == "remaining" or (r["status"] == "maybe" and not args.no_maybe):
                if norm(r["name"]) not in seen:  # the same game queued in two families → the first family wins
                    seen.add(norm(r["name"]))
                    rows.append(r)
        for r in rows:
            r["family"] = fam
        for tier, part in zip(tiers, ([r for r in rows if r["prio"] < 3], [r for r in rows if r["prio"] == 3])):
            tier[fam] = [part[i:i + SIZE] for i in range(0, len(part), SIZE)]
    for tier in tiers:  # 1–2-row leftovers of several families share one pack: the agent's reading costs the same
        tails = [r for fam in tier for r in (tier[fam].pop() if tier[fam] and len(tier[fam][-1]) <= 2 else [])]
        tier["mixed"] = [tails[i:i + SIZE] for i in range(0, len(tails), SIZE)]
    batches, k = [], 0
    for per_family in tiers:
        while any(per_family.values()):  # round-robin: the first packs touch every family
            for fam in sorted(per_family, key=lambda f: -len(per_family[f])):
                if per_family[fam]:
                    k += 1
                    rows = per_family[fam].pop(0)
                    batches.append({"id": f"{args.prefix}{k:03d}", "family": fam, "rows": rows, "prio": min(r["prio"] for r in rows)})
    return batches


def prompt(b, described):
    family_of = {s: f for f, slugs in described.items() for s in slugs}
    fams = sorted({r["family"] for r in b["rows"]})
    lines = [f"Ти — описовий агент корпусу лудопедії (пачка {b['id']}). Спершу прочитай цілком `{BRIEF}` (з доповненнями v1.1–v1.4) "
             f"і все, що він велить прочитати; корінь репо — `{ROOT.parents[1]}`."]
    for fam in fams:
        lines += ["", f"Сімʼя: **{fam}** → тека `data/ludopedia/games/{fam}/`.",
                  "Уже описані в сімʼї (не дублюй; посилайся на них у «Варіації й родичі»; список міг застаріти — перед записом `ls` "
                  f"теки ще раз): {', '.join(described.get(fam, [])) or '—'}."]
    lines += ["", "Твої ігри (рядки черг `queue/<сімʼя>.md`; починай дослідження з ⭐):"]
    for i, r in enumerate(b["rows"], 1):
        hint = (f" · ⚠ автоматика сплутала з `{family_of.get(r['match'], '?')}/{r['match']}` — спершу відкрий той файл; та сама гра, "
                "ремейк чи сиквел без нових механік — не пиши новий файл (за потреби — підрозділ туди) і скажи у звіті") if r["status"] == "maybe" else ""
        fam = f" · сімʼя **{r['family']}**" if len(fams) > 1 else ""
        lines.append(f"{i}. **{r['name']}** ({r['year']}) — {r['why']} · ⭐ {r['star']} · інші: {r['other']} · пріоритет {r['prio']}{fam}{hint}")
    lines += ["", "Напиши файл на кожну гру за брифом, прожени лінт, поверни звіт ≤12 рядків."]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("frm", nargs="?", type=int, default=1)
    ap.add_argument("to", nargs="?", type=int, default=20)
    ap.add_argument("--prefix", default="I")
    ap.add_argument("--out", type=Path, default=Path.cwd())
    ap.add_argument("--skip", default="")
    ap.add_argument("--no-maybe", action="store_true")
    args = ap.parse_args()
    batches = load(args)
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / f"batches-{args.prefix}.json").write_text(json.dumps(batches, ensure_ascii=False, indent=1))
    described = {d.name: sorted(p.stem for p in d.glob("*.md")) for d in (ROOT / "games").iterdir() if d.is_dir()}
    print(f"batches: {len(batches)} · rows: {sum(len(b['rows']) for b in batches)} · p1 packs: {sum(b['prio'] == 1 for b in batches)}")
    for b in batches[args.frm - 1:args.to]:
        print(f"\n===== {b['id']} · {b['family']} · {len(b['rows'])} ігор · п{b['prio']} =====\n{prompt(b, described)}")


if __name__ == "__main__":
    main()
