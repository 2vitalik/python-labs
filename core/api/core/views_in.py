"""What the view forms send (T315): cleaned field by field — a PUT carries only the fields it changes."""
from fastapi import HTTPException
from pydantic import BaseModel

KEYS = ("cols", "group", "sort", "lab", "q")  # plus f.<column>: a filter
ABOUT, FOLDER, TAG, TAGS, NAME, NOTE = 500, 60, 30, 12, 80, 500
EDITABLE = ("title", "emoji", "about", "folder", "tags", "etalon", "pinned", "query")


class ViewIn(BaseModel):
    title: str = ""
    emoji: str = ""
    about: str = ""
    folder: str = ""
    tags: list[str] = []
    etalon: bool = False
    pinned: bool = True
    query: dict = {}
    parent: str = ""  # a new view: the view and version it is made from
    parent_version: int = 0
    note: str = ""  # the note of the version this save makes


class VersionIn(BaseModel):
    name: str = ""
    note: str = ""
    star: bool = False


def words(s: str) -> str:
    return " ".join(s.split())


def short(s: str, most: int, what: str) -> str:
    if len(s) > most:
        raise HTTPException(422, f"{what} — до {most} символів")
    return s


def title(s: str) -> str:
    if not words(s):
        raise HTTPException(422, "Назви вид")
    return words(s)


def tags(items: list[str]) -> list[str]:
    out = list(dict.fromkeys(t for t in (short(words(t).lstrip("#"), TAG, "Тег") for t in items) if t))
    if len(out) > TAGS:
        raise HTTPException(422, f"Тегів — до {TAGS}")
    return out


def query(q: dict) -> dict:
    return {k: str(v)[:2000] for k, v in q.items() if (k in KEYS or k.startswith("f.")) and isinstance(v, (str, int, float))}


CLEAN = {"title": title, "emoji": str.strip, "about": lambda s: short(s.strip(), ABOUT, "«Для чого»"),
         "folder": lambda s: short(words(s), FOLDER, "Назва папки"), "tags": tags, "etalon": bool, "pinned": bool, "query": query}


def clean(data: ViewIn, keys=EDITABLE) -> dict:
    """The view's own fields among `keys`, cleaned."""
    return {k: CLEAN[k](getattr(data, k)) for k in EDITABLE if k in keys}


def clean_note(s: str) -> str:
    return short(s.strip(), NOTE, "Нотатка")


def clean_version(data: VersionIn) -> dict:
    out = {"name": short(words(data.name), NAME, "Назва версії"), "note": clean_note(data.note), "star": data.star}
    return {k: v for k, v in out.items() if k in data.model_fields_set}
