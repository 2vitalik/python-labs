"""Corpus → Mongo: data/ludopedia/games/*/*.md → `ludo_games`, upsert by slug; `--prune` drops rows whose file is gone.
Truth is the files (git); the site reads the collection. Usage from app/api: python ludopedia_io.py import [--prune]"""
import asyncio
import sys
from datetime import UTC, datetime
from pathlib import Path

import yaml

from db import init_db
from ludoparse import parse
from models.ludo_game import LudoGame

ROOT = Path(__file__).resolve().parents[2] / "data" / "ludopedia"


async def import_(prune: bool) -> None:
    seen, added, updated, same, bad = set(), 0, 0, 0, []
    for f in sorted((ROOT / "games").glob("*/*.md")):
        try:
            row = parse(f, ROOT)
        except (yaml.YAMLError, ValueError, TypeError) as e:  # one broken file must not stop the corpus
            row = None
            bad.append(f"{f.relative_to(ROOT)}: {e}")
        if not row:
            bad.append(str(f.relative_to(ROOT)))
            continue
        seen.add(row["slug"])
        doc = await LudoGame.find_one(LudoGame.slug == row["slug"])
        if not doc:
            await LudoGame(**row).insert()
            added += 1
        elif any(getattr(doc, k) != v for k, v in row.items()):
            for k, v in row.items():
                setattr(doc, k, v)
            doc.imported_at = datetime.now(UTC)
            await doc.save()
            updated += 1
        else:
            same += 1
    gone = await LudoGame.find({"slug": {"$nin": list(seen)}}).to_list()
    if prune:
        for g in gone:
            await g.delete()
    print(f"ludo_games: додано {added} · оновлено {updated} · без змін {same} · "
          f"{'видалено' if prune else 'без файла'} {len(gone)}" + (f" · не розібрано {len(bad)}: {bad}" if bad else ""))


async def main():
    await init_db()
    await import_("--prune" in sys.argv)


if __name__ == "__main__":
    asyncio.run(main())
