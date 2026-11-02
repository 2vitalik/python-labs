"""vocab/catalog-cards.md from data/catalog/tasks.yaml — the card slugs agents tag mechanics with."""
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
YAML = ROOT.parent / "catalog" / "tasks.yaml"
COIN = {"🌱": "wood", "📎": "tin", "🥉": "bronze", "🥈": "silver", "🥇": "gold", "👑": "crown"}


def card(slug, body, zone, sub, parent):
    if isinstance(body, dict):
        title, coin = body.get("title", slug), body.get("coin", "")
        desc, status = body.get("description", ""), body.get("status", "active")
        slots = [s["key"] for s in body.get("slots", [])]
    else:
        line = body
        desc = ""
        if " — " in line:
            line, desc = (s.strip() for s in line.split(" — ", 1))
        coin = next((COIN[c] for c in COIN if line.startswith(c)), "")
        line = re.sub(r"\[[^\]]*\]|#[\w-]+|⭐|🔁\d*|[🌱📎🥉🥈🥇👑]×?[\d.]*", " ", line)
        status = "draft" if "✍" in line else "active"
        title = " ".join(line.replace("✍️", "").replace("✍", "").split())
        slots = []
    return (slug, title, f"{zone}/{sub}", coin, parent, ", ".join(slots), desc, status)


def main():
    data = yaml.safe_load(YAML.read_text())
    rows = []
    for zone, subs in data.items():
        for sub, items in subs.items():
            for item in items:
                children = item.pop("children", [])
                (slug, body), = item.items()
                rows.append(card(slug, body, zone, sub, ""))
                for ch in children:
                    (cslug, cbody), = ch.items()
                    rows.append(card(cslug, cbody, zone, sub, slug))
    out = ["# Картки каталогу (автоген)", "", f"Джерело: `data/catalog/tasks.yaml` · {len(rows)} карток. Теги `mechanics` у шапці гри — ці slug-и; нове — з `+`.", "",
           "| slug | Назва | Зона/підзона | Монетка | Батько | Слоти | Опис |", "|---|---|---|---|---|---|---|"]
    for slug, title, zs, coin, parent, slots, desc, status in rows:
        mark = " ✍️" if status == "draft" else ""
        out.append(f"| `{slug}` | {title}{mark} | {zs} | {coin} | {parent} | {slots} | {desc} |")
    (ROOT / "vocab" / "catalog-cards.md").write_text("\n".join(out) + "\n")
    print(f"catalog-cards.md: {len(rows)} cards")


if __name__ == "__main__":
    sys.exit(main())
