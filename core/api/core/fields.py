"""The teacher's own columns (T240): a new field cleaned, its key made of its title, a value checked against the field's type."""
import re
from datetime import date
from typing import Any

from fastapi import HTTPException
from pydantic import BaseModel

from core.models.field import COLORS, Field, Option, Scope, Type

TRANSLIT = dict(zip("абвгґдеєжзиіїйклмнопрстуфхцчшщьюяыэёъ", ["a", "b", "v", "h", "g", "d", "e", "ie", "zh", "z", "y", "i", "i", "i", "k", "l", "m",
                                                           "n", "o", "p", "r", "s", "t", "u", "f", "kh", "ts", "ch", "sh", "shch", "", "iu", "ia", "y", "e", "e", ""]))
TEXT = 500  # characters a text value keeps


class OptionIn(BaseModel):
    id: str = ""  # an existing answer keeps its id; a new one gets the next free
    text: str = ""
    emoji: str = ""
    color: str = ""


class FieldIn(BaseModel):
    title: str = ""
    emoji: str = ""
    type: Type = "bool"
    options: list[OptionIn] = []
    scope: Scope = "student"


def slugify(text: str) -> str:
    """«Якість коду» → `iakist-kodu`: the key of a field or a view, Latin only, so a URL reads."""
    latin = "".join(TRANSLIT.get(c, c) for c in text.lower().replace("'", "").replace("ʼ", "").replace("’", ""))
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", latin)).strip("-")


def free_key(key: str, taken: set[str], fallback: str) -> str:
    """`key`, or `key-2`, `key-3`… while it is taken; an empty key becomes `fallback`."""
    base = key or fallback
    out, n = base, 1
    while out in taken:
        n += 1
        out = f"{base}-{n}"
    return out


def clean_options(data: list[OptionIn]) -> list[Option]:
    options, taken = [], {o.id for o in data if o.id}
    for o in data:
        text, emoji = " ".join(o.text.split()), o.emoji.strip()
        if not text and not emoji:
            continue
        if o.color and o.color not in COLORS:
            raise HTTPException(422, f"Кольору «{o.color}» нема в палітрі")
        oid = o.id or free_key(slugify(text) or "o", taken, "o")
        taken.add(oid)
        options.append(Option(id=oid, text=text, emoji=emoji, color=o.color))
    if len({(o.emoji, o.text) for o in options}) < len(options):
        raise HTTPException(422, "Два однакові варіанти")
    return options


def clean(data: FieldIn) -> dict:
    title = " ".join(data.title.split())
    if not title:
        raise HTTPException(422, "Назви поле")
    options = clean_options(data.options) if data.type in ("select", "multi") else []
    if data.type in ("select", "multi") and not options:
        raise HTTPException(422, "Селекту потрібен хоча б один варіант")
    return {"title": title, "emoji": data.emoji.strip(), "type": data.type, "options": options, "scope": data.scope}


def clean_value(field: Field, value: Any) -> Any:
    """The value as it is stored; None — the cell is cleared."""
    if value is None or value == "" or value == []:
        return None
    if field.type == "bool":
        return bool(value) if not isinstance(value, str) else value.lower() in ("1", "true", "yes", "так")
    if field.type == "number":
        try:
            n = float(value)
        except (TypeError, ValueError):
            raise HTTPException(422, f"«{value}» — не число")
        return int(n) if n.is_integer() else n
    if field.type == "text":
        return str(value).strip()[:TEXT] or None
    if field.type == "date":
        try:
            return date.fromisoformat(str(value)[:10]).isoformat()
        except ValueError:
            raise HTTPException(422, f"«{value}» — не дата (рік-місяць-день)")
    ids = [o.id for o in field.options]
    picked = [str(v) for v in (value if isinstance(value, list) else [value])]
    if unknown := [v for v in picked if v not in ids]:
        raise HTTPException(422, f"У поля «{field.title}» нема варіанта {', '.join(unknown)}")
    if field.type == "select":
        return picked[-1]
    return [i for i in ids if i in picked]  # multi: in the field's own order, no twins
