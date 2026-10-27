"""The teacher's own columns (T240): the fields themselves and a student's value in one of them."""
from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from core.config import settings
from core.deps import editor_user
from core.fields import FieldIn, clean, clean_value, free_key, slugify
from core.models.field import Field, FieldValue
from core.models.history import record, record_delete, record_new
from core.models.user import User

router = APIRouter(prefix="/api")
FROZEN = ("type", "scope")  # once a value is written, these stay: the values would stop making sense


class ValueIn(BaseModel):
    value: Any = None  # None clears the cell
    lab: int = 0  # for a field on labs


class OrderIn(BaseModel):
    keys: list[str]


async def get_field(key: str) -> Field:
    f = await Field.find_one(Field.key == key)
    if not f:
        raise HTTPException(404, f"Поля «{key}» нема")
    return f


@router.get("/fields")
async def list_fields(user: User = Depends(editor_user)):
    return {"fields": [f.api() for f in await Field.find_all().sort("order", "created_at").to_list()]}


@router.post("/fields")
async def create_field(data: FieldIn, user: User = Depends(editor_user)):
    """The key is the title in Latin; a second «Якість» becomes `iakist-2`. New fields go last."""
    fields = await Field.find_all().to_list()
    key = free_key(slugify(data.title), {f.key for f in fields}, "pole")
    f = await Field(key=key, **clean(data), order=max((x.order for x in fields), default=-1) + 1, by=user.email).insert()
    await record_new(f, user.email)
    return f.api()


@router.put("/fields/{key}")
async def update_field(key: str, data: FieldIn, user: User = Depends(editor_user)):
    f = await get_field(key)
    fields = clean(data)
    if any(fields[k] != getattr(f, k) for k in FROZEN) and await FieldValue.find(FieldValue.field == key).count():
        raise HTTPException(409, "У полі вже є значення — тип і «на що» не змінити; створи нове поле")
    await record(f, fields, user.email)
    return f.api()


@router.delete("/fields/{key}")
async def delete_field(key: str, user: User = Depends(editor_user)):
    """The field and every value in it; the values' history stays."""
    f = await get_field(key)
    n = 0
    for v in await FieldValue.find(FieldValue.field == key).to_list():
        await record_delete(v, user.email)
        n += 1
    await record_delete(f, user.email)
    return {"ok": True, "values": n}


@router.post("/fields/order")
async def order_fields(data: OrderIn, user: User = Depends(editor_user)):
    for i, key in enumerate(data.keys):
        await Field.find(Field.key == key).update({"$set": {"order": i}})
    return {"fields": [f.api() for f in await Field.find_all().sort("order", "created_at").to_list()]}


@router.put("/students/{nick}/fields/{key}")
async def put_value(nick: str, key: str, data: ValueIn, user: User = Depends(editor_user)):
    """One cell: the value checked against the field's type, written with history; None deletes the cell."""
    u = await User.by_nick(nick)
    if not u:
        raise HTTPException(404)
    f = await get_field(key)
    lab = data.lab if f.scope == "lab" else 0
    if f.scope == "lab" and not 1 <= lab <= settings.labs:
        raise HTTPException(422, f"Поле «{f.title}» — на лабу: якої лаби значення?")
    value = clean_value(f, data.value)
    cell = await FieldValue.find_one(FieldValue.user == u.email, FieldValue.field == key, FieldValue.lab == lab)
    column = f"{key}.{lab}" if lab else key
    if value is None:
        if cell:
            await record_delete(cell, user.email)
        return {"column": column, "value": None}
    if cell:
        if cell.value != value:  # the same value again is not a change
            await record(cell, {"value": value, "by": user.email, "at": datetime.now(timezone.utc)}, user.email)
    else:
        cell = await FieldValue(user=u.email, field=key, lab=lab, value=value, by=user.email).insert()
        await record_new(cell, user.email)
    return {"column": column, "value": cell.value}
