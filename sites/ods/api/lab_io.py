"""Lab variants: site.hid.json snapshots on disk (the lab's generator, outside git) → Mongo `variants`.
Run from sites/ods/api: uv run python lab_io.py [file …]; no files — every labs/new/lab*/out/*/site.hid.json.
A known variant gets its card and answers refreshed; whose it is and what they sent stays."""
import asyncio
import json
import sys
from pathlib import Path

from db import init_db
from models.lab import LabVariant

DATA = Path("../data")
FIELDS = ("lab", "group", "n", "card", "ask", "answers")


async def put(entry: dict) -> str:
    v = await LabVariant.find_one(LabVariant.vid == entry["vid"])
    if not v:
        await LabVariant(vid=entry["vid"], **{k: entry[k] for k in FIELDS}).insert()
        return "new"
    if all(getattr(v, k) == entry[k] for k in FIELDS):
        return ""
    for k in FIELDS:
        setattr(v, k, entry[k])
    await v.save()
    return "updated"


async def import_(paths) -> dict:
    counts = {"new": 0, "updated": 0, "": 0}
    for path in paths:
        for entry in json.loads(Path(path).read_text()):
            counts[await put(entry)] += 1
    return counts


async def main():
    await init_db()
    c = await import_(sys.argv[1:] or sorted(DATA.glob("labs/new/lab*/out/*/site.hid.json")))
    print(f"варіанти: нових {c['new']} · оновлено {c['updated']} · без змін {c['']}")


if __name__ == "__main__":
    asyncio.run(main())
