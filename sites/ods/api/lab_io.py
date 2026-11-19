"""Labs from disk (the lab's generator, outside git) → Mongo: the variants (`variants`, from site.hid.json snapshots)
and each lab's notebook shape (`lab_shapes`, labs_shape.py). Run from sites/ods/api: python lab_io.py [file …];
no files — every labs/new/lab*/out/*/site.hid.json and the shape of every lab; files — those snapshots only.
ODS_DATA — another data folder (a stand's invented files). A known variant (the same lab and vid) gets its card and
answers refreshed; whose it is and what they sent stays."""
import asyncio
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import labs_shape
from db import init_db
from models.lab import LabVariant
from models.lab_shape import LabShape

DATA = Path(os.environ.get("ODS_DATA", "../data"))
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


async def put_shape(s: dict) -> str:
    old = await LabShape.find_one(LabShape.lab == s["lab"])
    if not old:
        await LabShape(**s).insert()
        return "new"
    if all(getattr(old, k) == s[k] for k in s):
        return ""
    for k, x in s.items():
        setattr(old, k, x)
    old.updated_at = datetime.now(timezone.utc)
    await old.save()
    return "updated"


async def shapes() -> dict:
    counts = {"new": 0, "updated": 0, "": 0}
    found = [*DATA.glob("labs/new/lab*"), *DATA.glob("labs/site/lab*")]
    labs = sorted({int(m[1]) for p in found if (m := re.fullmatch(r"lab(\d+)", p.name))})
    for n in labs:
        if s := labs_shape.build(n, labs_shape.folder(DATA, n)):
            counts[await put_shape(s)] += 1
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
    if not sys.argv[1:]:
        c = await shapes()
        print(f"будова ноутбуків: нових {c['new']} · оновлено {c['updated']} · без змін {c['']}")


if __name__ == "__main__":
    asyncio.run(main())
