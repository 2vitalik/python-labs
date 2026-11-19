"""Strike queue rows the curator decided not to describe: `~~Name~~` and `⊘ <date>: <reason>` in the «інші» column;
queue_status.py then reports them as `skipped` and make_batches.py leaves them out.
Usage: queue_skip.py <family> "<exact name>" "<reason>"  ·  queue_skip.py --tsv rows.tsv (family, name, reason)"""
import sys
from datetime import date
from pathlib import Path

QUEUE = Path(__file__).resolve().parents[1] / "queue"


def skip(fam, name, why):
    path = QUEUE / f"{fam}.md"
    lines = path.read_text().split("\n")
    hits = [i for i, l in enumerate(lines) if l.startswith("|") and l.strip("|").split("|")[0].strip() == name]
    if len(hits) != 1:
        return f"!! {fam} · {name}: рядків {len(hits)}"
    cols = lines[hits[0]].strip().strip("|").split("|")
    cols[0], cols[4] = f" ~~{name}~~ ", f" {cols[4].strip()} · ⊘ {date.today()}: {why} "
    lines[hits[0]] = "|" + "|".join(cols) + "|"
    path.write_text("\n".join(lines))
    return f"ok {fam} · {name}"


if __name__ == "__main__":
    args = sys.argv[1:]
    todo = [l.split("\t") for l in Path(args[1]).read_text().splitlines() if l.strip()] if args[0] == "--tsv" else [args]
    for fam, name, why in todo:
        print(skip(fam, name, why))
