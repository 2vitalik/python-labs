"""What a find may carry (T274 §4): its kind, the place in the catalog it is about, the card."""
from fastapi import HTTPException
from pydantic import BaseModel

from models.task import Task
from zones import ZONES

KINDS = ("link", "idea", "fix", "site")


class RefIn(BaseModel):
    url: str = ""
    title: str = ""
    note: str = ""
    parent: str = ""
    kind: str = ""  # "" — by the url, as before: a link, else an idea
    zone: str = ""
    subzone: str = ""
    task: str = ""


async def clean(data: RefIn) -> dict:
    url, title, note = data.url.strip(), data.title.strip(), data.note.strip()
    kind = data.kind or ("link" if url else "idea")
    if kind not in KINDS:
        raise HTTPException(422, "Невідомий вид запису")
    if url and not url.startswith(("http://", "https://")):
        raise HTTPException(422, "Посилання починається з http(s)://")
    if kind == "link" and not url:
        raise HTTPException(422, "Посилання порожнє — встав адресу")
    if not url and not (title or note):
        raise HTTPException(422, "Ідея порожня — напиши хоч рядок")
    zone, subzone, slug = data.zone.strip(), data.subzone.strip(), data.task.strip()
    if zone and zone not in ZONES:
        raise HTTPException(422, "Немає такої категорії")
    if subzone and subzone not in ZONES.get(zone, {}).get("subzones", {}):
        raise HTTPException(422, "Немає такої підкатегорії в цій категорії")
    task = await Task.find_one(Task.slug == slug) if slug else None
    if slug and not task:
        raise HTTPException(422, "Немає такої картки в каталозі")
    if task and not zone:  # a word on a card is about the card's place
        zone, subzone = task.zone, task.subzone
    return {"url": url, "title": title, "note": note, "kind": kind, "parent": data.parent.strip(),
            "zone": zone, "subzone": subzone, "task": slug}
