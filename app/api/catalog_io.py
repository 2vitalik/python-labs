"""Catalog snapshot: Mongo ↔ data/catalog/*.yaml. Truth lives in Mongo; YAML is a git-diffable
snapshot and the bulk-edit channel (upsert by slug). games.yaml — flat dicts; tasks.yaml — a tree
zone → subzone → one-line tasks (taskline.py), file position = order, family children nested.
Usage: uv run python catalog_io.py export|import"""
import asyncio
import sys
from pathlib import Path

import yaml

from db import init_db
from models.game import Game
from models.task import Task
from taskline import parse_line, render_line
from zones import ZONES

CATALOG = Path(__file__).resolve().parents[2] / "data" / "catalog"


def dump(doc, exclude=("id", "created_at")) -> dict:
    d = doc.model_dump(exclude=set(exclude))
    return {k: v for k, v in d.items() if not (v == "" or v == [] or v == {})}


def task_node(t) -> dict | str:  # dict fallback for multi-line descriptions
    if "\n" in t.description:
        return dump(t, exclude=("id", "created_at", "slug", "zone", "subzone", "order", "parent"))
    return render_line(t)


async def export():
    CATALOG.mkdir(parents=True, exist_ok=True)
    games = await Game.find_all().sort("order", "slug").to_list()
    (CATALOG / "games.yaml").write_text(yaml.safe_dump([dump(g) for g in games], allow_unicode=True, sort_keys=False, width=120))
    tasks = await Task.find_all().sort("zone", "subzone", "order", "slug").to_list()
    kids = {}
    for t in tasks:
        if t.parent:
            kids.setdefault(t.parent, []).append(t)
    tree = {}
    for t in tasks:
        if t.parent:
            continue
        entry = {t.slug: task_node(t)}
        if t.slug in kids:
            entry["children"] = [{k.slug: task_node(k)} for k in kids[t.slug]]
        tree.setdefault(t.zone, {}).setdefault(t.subzone, []).append(entry)
    tree = {z: tree[z] for z in ZONES if z in tree}
    (CATALOG / "tasks.yaml").write_text(yaml.safe_dump(tree, allow_unicode=True, sort_keys=False, width=200))
    print(f"games.yaml: {len(games)} · tasks.yaml: {len(tasks)} ({len(kids)} сімей)")


def task_rows() -> list[dict]:
    tree = yaml.safe_load((CATALOG / "tasks.yaml").read_text()) or {}
    rows = []
    for zone, subs in tree.items():
        for sub, items in subs.items():
            for i, item in enumerate(items, 1):
                slug = next(k for k in item if k != "children")
                row = to_row(slug, item[slug], zone, sub, i * 10)
                rows.append(row)
                for j, ch in enumerate(item.get("children") or [], 1):
                    cslug = next(iter(ch))
                    rows.append(to_row(cslug, ch[cslug], zone, sub, j * 10) | {"parent": slug})
    return rows


def to_row(slug, node, zone, sub, order) -> dict:
    if isinstance(node, str):
        return parse_line(slug, node, zone, sub, order)
    return {"slug": slug, "zone": zone, "subzone": sub, "order": order, "parent": ""} | node


async def upsert(model, rows) -> None:
    added = updated = same = 0
    for row in rows:
        doc = await model.find_one(model.slug == row["slug"])
        if not doc:
            await model(**row).insert()
            added += 1
            continue
        patch = {k: v for k, v in row.items() if getattr(doc, k) != v}
        for k, v in patch.items():
            setattr(doc, k, v)
        if patch:
            await doc.save()
            updated += 1
        else:
            same += 1
    print(f"{model.Settings.name}: додано {added} · оновлено {updated} · без змін {same}")


async def import_():
    await upsert(Game, yaml.safe_load((CATALOG / "games.yaml").read_text()) or [])
    await upsert(Task, task_rows())


async def main():
    await init_db()
    await {"export": export, "import": import_}[sys.argv[1]]()


if __name__ == "__main__":
    asyncio.run(main())
