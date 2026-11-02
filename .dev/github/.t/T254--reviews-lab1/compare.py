"""Agreement between the main run and a second run (data/reviews/.second or .sonnet): kind, verdict, required per item, level, ai."""
import json
import re
import sys
from pathlib import Path

ROOT = Path.cwd()
alt = sys.argv[1]  # .second | .sonnet | .v1


def header(path: Path) -> dict:
    text = path.read_text()
    head, _, body = text[4:].partition("\n---\n")
    d = dict((k.strip(), v.strip()) for k, _, v in (line.partition(":") for line in head.splitlines()) if k.strip())
    d["required"] = d.get("required", "").split()
    d["lines"] = body.strip().count("\n") + 1
    d["evidence"] = len(re.findall(r"[\w./-]+\.py:\d+", body))
    return d


rows = []
for b in sorted((ROOT / "data/reviews" / alt).glob("*/lab1.md")):
    nick = b.parent.name
    a = ROOT / "data/reviews" / nick / "lab1.md"
    if not a.exists():
        continue
    ha, hb = header(a), header(b)
    pa = json.load(open(a.with_suffix(".profile.json"))) if a.with_suffix(".profile.json").exists() else {}
    pb = json.load(open(b.with_suffix(".profile.json"))) if b.with_suffix(".profile.json").exists() else {}
    same_items = sum(x == y for x, y in zip(ha["required"], hb["required"])) if ha["required"] and hb["required"] else None
    rows.append((nick, ha, hb, pa, pb, same_items))

print(f"## {alt} проти основного прогону · пар: {len(rows)}\n")
print("| Нік | kind A/B | verdict A/B | ✔/6 A/B | збіг пунктів | рівень A/B | ШІ A/B | рядків A/B | доказів A/B |\n|:--|:--|:--|:--|--:|:--|:--|:--|:--|")
for nick, ha, hb, pa, pb, same in rows:
    d = lambda h: sum(1 for x in h["required"] if x == "done")  # noqa: E731
    print(f"| {nick} | {ha.get('kind', '-')}/{hb.get('kind', '-')} | {ha.get('verdict')}/{hb.get('verdict')} | {d(ha)}/{d(hb)} | {same if same is not None else '-'}/6 | "
          f"{pa.get('level', '-')}/{pb.get('level', '-')} | {(pa.get('ai') or {}).get('level', '-')}/{(pb.get('ai') or {}).get('level', '-')} | {ha['lines']}/{hb['lines']} | {ha['evidence']}/{hb['evidence']} |")
n = len(rows)
print(f"\n- kind збігається: {sum(ha.get('kind') == hb.get('kind') for _, ha, hb, *_ in rows)}/{n}")
print(f"- verdict збігається: {sum(ha.get('verdict') == hb.get('verdict') for _, ha, hb, *_ in rows)}/{n}")
items = [s for *_, s in rows if s is not None]
print(f"- пунктів required збігається: {sum(items)}/{6 * len(items)}")
print(f"- required повністю однаковий: {sum(s == 6 for s in items)}/{len(items)}")
lv = [(pa.get("level"), pb.get("level")) for _, _, _, pa, pb, _ in rows if pa.get("level") and pb.get("level")]
print(f"- рівень: той самий {sum(a == b for a, b in lv)}/{len(lv)}, у межах ±1 — {sum(abs(a - b) <= 1 for a, b in lv)}/{len(lv)}")
ai = [((pa.get("ai") or {}).get("level"), (pb.get("ai") or {}).get("level")) for _, _, _, pa, pb, _ in rows if pa.get("ai") and pb.get("ai")]
print(f"- ШІ-ознаки той самий рівень: {sum(a == b for a, b in ai)}/{len(ai)}")
