"""Catalog snapshot: Mongo ↔ data/catalog/*.yaml. Truth lives in Mongo; YAML is a git-diffable
snapshot and the bulk-edit channel (upsert by slug, logged in `history` as `import`). games.yaml — flat dicts; tasks.yaml — a tree
zone → subzone → one-line tasks (taskline.py), file position = order, family children nested; aliases.yaml — slug → names,
a list (Ukrainian) or {uk, ru, en}. Usage: uv run python catalog_io.py export | import [--prune] (--prune: what the YAML
lacks goes to the archive)"""
import asyncio
import sys
from pathlib import Path

import yaml

from core.models.history import record, record_new
from db import init_db
from models.base_game import BaseGame
from models.task import LANGS, Task, langs
from taskline import parse_line, plain, render_line
from zones import ZONES

CATALOG = Path(__file__).resolve().parents[2] / "data" / "catalog"


class Dumper(yaml.SafeDumper):
    """Texts of several lines go as literal blocks `|`: a field grid reads in the snapshot as it does in the text."""


Dumper.add_representer(str, lambda d, s: d.represent_scalar("tag:yaml.org,2002:str", s, style="|" if "\n" in s else None))


def dump(doc, exclude=("id", "created_at")) -> dict:
    d = doc.model_dump(exclude=set(exclude))
    return {k: v for k, v in d.items() if not (v == "" or v == [] or v == {})}


def reads_back(t) -> bool:
    """Does the one-line form read back as the same card: a title with « — », [ ], a #word or a mark inside does not."""
    d = parse_line(t.slug, render_line(t), t.zone, t.subzone, t.order)
    same = ("title", "description", "games", "kind", "rule", "coin", "amount", "max_count", "status")
    return all(d[k] == getattr(t, k) for k in same) and sorted(d["tags"]) == sorted(t.tags)


def task_node(t) -> dict | str:  # dict fallback for multi-line descriptions, slot specs, icons, opts, rule blanks; aliases live in aliases.yaml
    if "\n" in t.description or t.slots or t.icon or t.opt or not plain(t.rule) or not reads_back(t):
        return dump(t, exclude=("id", "created_at", "slug", "zone", "subzone", "order", "parent", "aliases"))
    return render_line(t)


async def render() -> dict[str, str]:
    """File name → its YAML: the catalog as it is in Mongo."""
    games = await BaseGame.find_all().sort("order", "slug").to_list()
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
    aliases = {t.slug: alias_node(t.aliases) for t in sorted(tasks, key=lambda t: t.slug) if any(t.aliases.values())}
    return {"games.yaml": yaml.dump([dump(g) for g in games], Dumper=Dumper, allow_unicode=True, sort_keys=False, width=120),
            "tasks.yaml": yaml.dump(tree, Dumper=Dumper, allow_unicode=True, sort_keys=False, width=200),
            "aliases.yaml": yaml.dump(aliases, Dumper=Dumper, allow_unicode=True, sort_keys=False, width=200, default_flow_style=None)}


def alias_node(a: dict) -> list | dict:
    """The plain list while there are only Ukrainian names, the languages apart once there are others."""
    return {k: a[k] for k in LANGS if a[k]} if a["ru"] or a["en"] else a["uk"]


async def export():
    CATALOG.mkdir(parents=True, exist_ok=True)
    for name, text in (await render()).items():
        (CATALOG / name).write_text(text)
        print(f"{name}: {len(text.splitlines())} рядків → {CATALOG}")


def task_rows() -> list[dict]:
    tree = yaml.safe_load((CATALOG / "tasks.yaml").read_text()) or {}
    path = CATALOG / "aliases.yaml"
    aliases = (yaml.safe_load(path.read_text()) if path.is_file() else None) or {}
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
    for row in rows:
        row["aliases"] = langs(aliases.get(row["slug"]))
    return rows


def to_row(slug, node, zone, sub, order) -> dict:
    if isinstance(node, str):
        return parse_line(slug, node, zone, sub, order)
    return {"slug": slug, "zone": zone, "subzone": sub, "order": order, "parent": "", "kind": "", "icon": "", "opt": "", "rule": {}} | node


async def upsert(model, rows) -> None:
    added = updated = same = 0
    for row in rows:
        doc = await model.find_one(model.slug == row["slug"])
        if not doc:
            doc = model(**row)
            await doc.insert()
            await record_new(doc, actor="import")
            added += 1
        elif await record(doc, row, actor="import"):
            updated += 1
        else:
            same += 1
    print(f"{model.Settings.name}: додано {added} · оновлено {updated} · без змін {same}")


async def import_():
    await upsert(BaseGame, yaml.safe_load((CATALOG / "games.yaml").read_text()) or [])
    rows = task_rows()
    await upsert(Task, rows)
    if "--prune" in sys.argv:
        await prune({r["slug"] for r in rows})


async def prune(slugs: set[str]) -> None:
    gone = await Task.find({"slug": {"$nin": list(slugs)}, "status": {"$ne": "archived"}}).to_list()
    for t in gone:
        await record(t, {"status": "archived"}, actor="import")
        print(f"в архів: {t.slug} · {t.title}")
    print(f"tasks: в архів {len(gone)}")


async def main():
    await init_db()
    await {"export": export, "import": import_}[sys.argv[1]]()


if __name__ == "__main__":
    asyncio.run(main())
