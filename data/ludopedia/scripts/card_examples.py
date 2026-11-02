"""index/card-examples.yaml: catalog card slug → games of the corpus that use it (seed for Д3 «Як це буває в іграх»)."""
import re
import sys
from collections import defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def main():
    known = set(re.findall(r"^\| `([\w-]+)`", (ROOT / "vocab" / "catalog-cards.md").read_text(), re.M))
    by = defaultdict(list)
    for f in sorted((ROOT / "games").glob("*/*.md")):
        m = re.match(r"^---\n(.*?)\n---\n", f.read_text(), re.S)
        if not m:
            continue
        try:
            fm = yaml.safe_load(m.group(1)) or {}
        except yaml.YAMLError:
            continue
        best = next((l["url"] for l in fm.get("links") or [] if isinstance(l, dict) and l.get("best")), "")
        for t in fm.get("mechanics") or []:
            if t in known:
                by[t].append({"game": fm.get("title"), "slug": fm.get("slug"), "family": fm.get("family"), "url": best,
                              "file": f.relative_to(ROOT).as_posix()})
    out = {t: sorted(v, key=lambda x: str(x["game"])) for t, v in sorted(by.items())}
    (ROOT / "index" / "card-examples.yaml").write_text(yaml.safe_dump(out, allow_unicode=True, sort_keys=False, width=200))
    print(f"card-examples: {len(out)} cards, {sum(len(v) for v in out.values())} examples")


if __name__ == "__main__":
    sys.exit(main())
