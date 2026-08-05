"""Catalog snapshot: Mongo ↔ data/catalog/*.yaml. Truth lives in Mongo; YAML is a git-diffable
snapshot and the bulk-edit/seed channel (upsert by slug). Usage: uv run python catalog_io.py export|import"""
import asyncio
import sys
from pathlib import Path

import yaml

from db import init_db
from models.game import Game
from models.task import Task

CATALOG = Path(__file__).resolve().parents[2] / "data" / "catalog"
FILES = {"games.yaml": Game, "tasks.yaml": Task}
SORTS = {"games.yaml": ("order", "slug"), "tasks.yaml": ("zone", "subzone", "order", "slug")}


def dump(doc) -> dict:
    d = doc.model_dump(exclude={"id", "created_at"})
    return {k: v for k, v in d.items() if not (v == "" or v == [] or v == {})}


async def export():
    CATALOG.mkdir(parents=True, exist_ok=True)
    for name, model in FILES.items():
        docs = await model.find_all().sort(*SORTS[name]).to_list()
        text = yaml.safe_dump([dump(d) for d in docs], allow_unicode=True, sort_keys=False, width=120)
        (CATALOG / name).write_text(text)
        print(f"{name}: {len(docs)}")


async def import_():
    for name, model in FILES.items():
        rows = yaml.safe_load((CATALOG / name).read_text()) or []
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
        print(f"{name}: додано {added} · оновлено {updated} · без змін {same}")


async def main():
    await init_db()
    await {"export": export, "import": import_}[sys.argv[1]]()


if __name__ == "__main__":
    asyncio.run(main())
