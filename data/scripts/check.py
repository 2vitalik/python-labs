#!/usr/bin/env python3
"""Verify that v3 is a lossless projection of v2.

Coda direction: for every v2 CSV, project the corresponding v3 rows back into
the original column set/order (minus the deliberately dropped columns) and
compare cell-by-cell, row-by-row.

Notion direction: flatten each md file into its ordered list of bullet items
and compare with the same flattening rebuilt from the v3 CSV (normalized:
markdown emphasis stripped, whitespace collapsed).

Exit code 0 = everything matches.
"""
import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from convert_coda import DATA, MAPPINGS, YEARS, HEADER  # noqa: E402
from convert_notion import SKIP_SECTIONS, strip_md  # noqa: E402

failures = 0


def fail(msg: str) -> None:
    global failures
    failures += 1
    print(f"❌ {msg}")


def read_csv(path: Path) -> tuple[list[str], list[dict]]:
    with open(path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        return list(reader.fieldnames), list(reader)


def check_coda() -> None:
    for year, files in YEARS.items():
        v3_path = DATA / "v3" / "coda" / f"{year}.csv"
        v3_header, v3_rows = read_csv(v3_path)
        if v3_header != HEADER:
            fail(f"{year}: v3 header differs from unified schema")
            continue
        for rel in files:
            mapping = MAPPINGS[rel]
            source = "props" if "props" in rel else "tasks"
            v2_header, v2_rows = read_csv(DATA / "v2" / "coda" / rel)
            kept = [c for c in v2_header if mapping[c] is not None]
            dropped = [c for c in v2_header if mapping[c] is None]
            expected = [[r[c] for c in kept] for r in v2_rows]
            projected = [[r[mapping[c]] for c in kept]
                         for r in v3_rows if r["source"] == source]
            if expected == projected:
                note = f" (dropped: {', '.join(dropped)})" if dropped else ""
                print(f"✅ {rel} ⇄ {year}.csv[{source}]: "
                      f"{len(expected)} rows × {len(kept)} cols identical{note}")
                continue
            if len(expected) != len(projected):
                fail(f"{rel}: {len(expected)} v2 rows vs {len(projected)} v3 rows")
                continue
            for i, (e, p) in enumerate(zip(expected, projected)):
                if e != p:
                    fail(f"{rel} row {i + 2}: v2={e} v3={p}")
                    break


def flatten_norm(text: str) -> str:
    return re.sub(r"\s+", " ", strip_md(text)).strip()


def flatten_md(path: Path) -> list[str]:
    items: list[str] = []
    in_aside = skip_section = False
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped == "<aside>":
            in_aside = True
        elif stripped == "</aside>":
            in_aside = False
        elif in_aside:
            continue
        elif stripped.startswith("## ") and not stripped.startswith("### "):
            skip_section = stripped[3:].strip() in SKIP_SECTIONS
        elif not skip_section and stripped.startswith("- "):
            items.append(flatten_norm(stripped[2:]))
    return items


def flatten_csv(path: Path) -> list[str]:
    items: list[str] = []
    for row in read_csv(path)[1]:
        parts = row["description"].split("\\n") if row["description"] else []
        if parts and parts[0].startswith("("):
            items.append(flatten_norm(f"{row['name']} {parts[0]}"))
            parts = parts[1:]
        else:
            items.append(flatten_norm(row["name"]))
        items.extend(flatten_norm(p) for p in parts)
    return items


def check_notion() -> None:
    for md_name, csv_name in [("tasks.md", "tasks.csv"), ("algo.md", "algo.csv")]:
        md_items = flatten_md(DATA / "v2" / "notion" / "games" / md_name)
        csv_items = flatten_csv(DATA / "v3" / "notion" / csv_name)
        if md_items == csv_items:
            print(f"✅ {md_name} ⇄ {csv_name}: {len(md_items)} items identical")
            continue
        if len(md_items) != len(csv_items):
            fail(f"{md_name}: {len(md_items)} md items vs {len(csv_items)} csv items")
        for i, (m, c) in enumerate(zip(md_items, csv_items)):
            if m != c:
                fail(f"{md_name} item {i}: md={m!r} csv={c!r}")
                break


def main() -> None:
    check_coda()
    check_notion()
    if failures:
        print(f"⚠️ {failures} failure(s)")
        sys.exit(1)
    print("🎉 v3 = v2, втрат немає")


if __name__ == "__main__":
    main()
