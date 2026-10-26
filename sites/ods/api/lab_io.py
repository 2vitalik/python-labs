"""Lab variants: site.hid.json snapshots on disk (the lab's generator, outside git) → Mongo `variants`.
Run from sites/ods/api: uv run python lab_io.py [file …]; no files — every labs/new/lab*/out/*/site.hid.json.
A known variant (the same lab and vid) gets its card and answers refreshed; whose it is and what they sent stays."""
import asyncio
import json
import sys
from pathlib import Path

from db import init_db
from models.lab import LabVariant

DATA = Path("../data")
FIELDS = ("lab", "group", "n", "card", "ask", "answers")


async def put(entry: dict) -> str:
    v = await LabVariant.find_one(LabVariant.lab == entry["lab"], LabVariant.vid == entry["vid"])
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


async def drop_old_index():
    """Before T234 `vid` alone was unique; the index survives in old databases and would reject the second lab's cards."""
    try:
        await LabVariant.get_pymongo_collection().drop_index("vid_1")
    except Exception:  # noqa: BLE001 — already gone
        pass


async def main():
    await init_db()
    await drop_old_index()
    c = await import_(sys.argv[1:] or sorted(DATA.glob("labs/new/lab*/out/*/site.hid.json")))
    print(f"варіанти: нових {c['new']} · оновлено {c['updated']} · без змін {c['']}")


if __name__ == "__main__":
    asyncio.run(main())
