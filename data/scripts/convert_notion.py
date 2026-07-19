#!/usr/bin/env python3
"""Convert Notion markdown task lists into v3 unified-schema CSVs.

games/tasks.md -> v3/notion/tasks.csv, games/algo.md -> v3/notion/algo.csv.
One CSV row per bullet: bold/plain text -> name, trailing italic "(...)"
explanation -> description (parentheses kept, Coda-18/19 style), nested
sub-bullets -> description joined with a literal \\n (v2 Coda convention).
Headings: ### -> category, ## -> supercategory (tasks.md only). Lead-in
paragraphs ending with ":" group the bullets below them -> subcategory
(T28 Q3/Q4); other paragraphs describe the category itself and stay in md only.
The "Основний задум" sections hold general rules, not tasks — skipped.
"""
import csv
import re
from pathlib import Path

DATA = Path(__file__).resolve().parents[1]
SRC = DATA / "v2" / "notion" / "games"
DST = DATA / "v3" / "notion"

HEADER = ["name", "description", "coins", "coin_type", "points", "category",
          "supercategory", "subcategory", "games", "report", "color", "author",
          "new", "used", "source"]

SKIP_SECTIONS = {"Основний задум"}  # general rules, not tasks

PAREN_DESC = re.compile(r"\s*\*+\((.*)\)\*+\s*$", re.S)
KEYCAP_STAR = "*️⃣"  # the *️⃣ emoji contains a literal asterisk


def strip_md(text: str) -> str:
    """Remove markdown emphasis/backticks, preserving the *️⃣ keycap emoji."""
    text = text.replace(KEYCAP_STAR, "\x00")
    text = text.replace("*", "").replace("`", "")
    return text.replace("\x00", KEYCAP_STAR).strip()


def split_bullet(text: str) -> tuple[str, str]:
    """'**Name** *(explanation)*' -> ('Name', '(explanation)')."""
    m = PAREN_DESC.search(text)
    desc = ""
    if m:
        desc = f"({m.group(1)})"
        text = text[: m.start()]
    return strip_md(text), desc


def parse(path: Path, source: str, use_supercategory: bool) -> list[dict]:
    rows: list[dict] = []
    supercategory = category = subcategory = ""
    in_aside = skip_section = False
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped == "<aside>":
            in_aside = True
            continue
        if stripped == "</aside>":
            in_aside = False
            continue
        if in_aside or not stripped or stripped.startswith("# "):
            continue
        if stripped.startswith("## ") and not stripped.startswith("### "):
            title = stripped[3:].strip()
            skip_section = title in SKIP_SECTIONS
            supercategory = title if use_supercategory and not skip_section else ""
            category = subcategory = ""
            continue
        if skip_section:
            continue
        if stripped.startswith("### "):
            category = stripped[4:].strip()
            subcategory = ""
            continue
        if line.startswith("- "):
            name, desc = split_bullet(stripped[2:])
            rows.append(dict.fromkeys(HEADER, "") | {
                "name": name, "description": desc, "category": category,
                "supercategory": supercategory, "subcategory": subcategory,
                "source": source,
            })
            continue
        if re.match(r"\s+- ", line):  # nested bullet -> parent's description
            part = strip_md(stripped[2:])
            prev = rows[-1]["description"]
            rows[-1]["description"] = f"{prev}\\n{part}" if prev else part
            continue
        if stripped.endswith(":"):  # lead-in grouping the bullets below
            subcategory = strip_md(stripped)
        # any other paragraph describes the category itself -> stays in md
    return rows


def main() -> None:
    DST.mkdir(parents=True, exist_ok=True)
    jobs = [("tasks.md", "tasks.csv", "notion-tasks", True),
            ("algo.md", "algo.csv", "notion-algo", False)]
    for src_name, dst_name, source, use_super in jobs:
        rows = parse(SRC / src_name, source, use_super)
        dst = DST / dst_name
        with open(dst, "w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=HEADER, lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)
        print(f"{dst.relative_to(DATA)}: {len(rows)} rows")


if __name__ == "__main__":
    main()
