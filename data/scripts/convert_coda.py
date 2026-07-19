#!/usr/bin/env python3
"""Convert Coda v2 CSVs (per-year, heterogeneous columns) into v3 unified-schema CSVs.

Pure projection: cell values are copied verbatim, only column names/order change.
Dropped columns (T28 Q2): tasks-20 'Баллы' (duplicate of coins) and 'Title'
(derived emoji decor), tasks-21/props-23 'Add' (Coda-internal), props-23 '✔️'.
Row order is preserved; for years with props, tasks rows go first, then props.
"""
import csv
from pathlib import Path

DATA = Path(__file__).resolve().parents[1]
SRC = DATA / "v2" / "coda"
DST = DATA / "v3" / "coda"

HEADER = ["name", "description", "coins", "coin_type", "points", "category",
          "supercategory", "subcategory", "games", "report", "color", "author",
          "new", "used", "source"]

# v2 column -> v3 column; None = deliberately dropped
MAPPINGS = {
    "pzpi-18/tasks-18.csv": {
        "Название": "name", "Тип": "category", "Монеты": "coin_type",
        "Класс": "supercategory", "Комментарий": "description", "Очки": "points",
    },
    "pzpi-19/tasks-19.csv": {
        "Название": "name", "#": "coins", "Монета": "coin_type",
        "Категория": "category", "Описание задания": "description",
        "Игры из которых взяты идеи": "games", "Баллы": "points",
        "new": "new", "Used": "used",
    },
    "pzpi-20/tasks-20.csv": {
        "Название": "name", "Монеты": "coins", "Категория": "category",
        "Описание задания": "description", "Игры, давшие эту идею": "games",
        "use": "used", "Баллы": None, "new?": "new",
        "Тип задания": "supercategory", "Title": None,
    },
    "pzpi-21/tasks-21.csv": {
        "Add": None, "Название": "name", "Монеты": "coins", "used": "used",
        "Описание": "description", "Особые требования к отчёту": "report",
        "Тип": "category",
    },
    "pzpi-21/props-21.csv": {
        "Название": "name", "Монеты": "coins", "used": "used",
        "Описание": "description", "Идея взята из": "games",
        "color": "color", "Тип": "category",
    },
    "pzpi-22/tasks-22.csv": {
        "Описание": "description", "coins": "coins",
        "used in interface": "used", "who added": "author",
        "Название": "name", "Тип": "category",
    },
    "pzpi-22/props-22.csv": {
        "Название": "name", "coins": "coins", "used": "used",
        "Описание": "description", "Идея взята из": "games",
        "color": "color", "Тип": "category",
    },
    "pzpi-23/tasks-23.csv": {
        "Опис": "description", "coins": "coins",
        "used in interface": "used", "who added": "author",
        "Назва": "name", "Группа": "supercategory", "Тип": "category",
    },
    "pzpi-23/props-23.csv": {
        "✔️": None, "Add": None, "Назва": "name",
        "Опис (це не ваш звіт, а лише опис завдання!) ⚠️": "description",
        "coins": "coins", "used": "used", "Created by": "author",
        "color": "color", "Тип": "category",
    },
    "pzpi-24/tasks-24.csv": {
        "Категорія": "category", "Коротка назва": "name",
        "Coin": "coin_type", "Над-категорія": "supercategory",
    },
}

YEARS = {
    "pzpi-18": ["pzpi-18/tasks-18.csv"],
    "pzpi-19": ["pzpi-19/tasks-19.csv"],
    "pzpi-20": ["pzpi-20/tasks-20.csv"],
    "pzpi-21": ["pzpi-21/tasks-21.csv", "pzpi-21/props-21.csv"],
    "pzpi-22": ["pzpi-22/tasks-22.csv", "pzpi-22/props-22.csv"],
    "pzpi-23": ["pzpi-23/tasks-23.csv", "pzpi-23/props-23.csv"],
    "pzpi-24": ["pzpi-24/tasks-24.csv"],
}


def convert_file(rel: str) -> list[dict]:
    mapping = MAPPINGS[rel]
    source = "props" if "props" in rel else "tasks"
    out = []
    with open(SRC / rel, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        assert set(reader.fieldnames) == set(mapping), \
            f"{rel}: header mismatch: {reader.fieldnames}"
        for row in reader:
            new = dict.fromkeys(HEADER, "")
            for src_col, dst_col in mapping.items():
                if dst_col is not None:
                    new[dst_col] = row[src_col]
            new["source"] = source
            out.append(new)
    return out


def main() -> None:
    DST.mkdir(parents=True, exist_ok=True)
    for year, files in YEARS.items():
        rows = [r for rel in files for r in convert_file(rel)]
        dst = DST / f"{year}.csv"
        with open(dst, "w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=HEADER, lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)
        print(f"{dst.relative_to(DATA)}: {len(rows)} rows")


if __name__ == "__main__":
    main()
