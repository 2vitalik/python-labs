"""index/known-names.txt — every name the corpus or the queues already know (titles, aka, slugs, queue rows), one per line
`назва | нормалізована | game:<сімʼя>/<slug> або queue:<файл>`; plus names search agents rejected (`- Назва — причина` in
queue/_*checked*.md → `skipped:<файл>`). Search agents grep it before adding a candidate."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from queue_status import described, norm, rows  # noqa: E402


def main():
    out = set()
    for g in described():
        ref = f"game:{g['family']}/{g['slug']}"
        out.add(f"{g['title']} | {norm(str(g['title']))} | {ref}")
        out |= {f"{a} | {a} | {ref}" for a in g["aliases"] if a != norm(str(g["title"]))}
    for q in sorted((ROOT / "queue").glob("**/*.md")):
        if q.name.startswith("_"):
            continue
        ref = f"queue:{q.relative_to(ROOT / 'queue').with_suffix('')}"
        out |= {f"{r['name']} | {norm(r['name'])} | {ref}" for r in rows(q) if r["name"]}
    for q in sorted((ROOT / "queue").glob("_*checked*.md")):
        out |= {f"{n} | {norm(n)} | skipped:{q.stem}" for n in re.findall(r"^- (.+?) — ", q.read_text(), re.M)}
    lines = sorted(out, key=str.lower)
    (ROOT / "index" / "known-names.txt").write_text("\n".join(lines) + "\n")
    print(f"known-names: {len(lines)} рядків")


if __name__ == "__main__":
    main()
