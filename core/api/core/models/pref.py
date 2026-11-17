from typing import Any

from beanie import Document
from pymongo import IndexModel


class Pref(Document):
    """The teacher's setting for the whole site (T315): `table.quiet`, `table.folders`, `table.seeds_gone`."""
    key: str
    value: Any = None

    class Settings:
        name = "prefs"
        indexes = [IndexModel([("key", 1)], unique=True)]


async def get_pref(key: str, default: Any = None) -> Any:
    p = await Pref.find_one(Pref.key == key)
    return p.value if p else default


async def set_pref(key: str, value: Any):
    await Pref.get_pymongo_collection().update_one({"key": key}, {"$set": {"value": value}}, upsert=True)
