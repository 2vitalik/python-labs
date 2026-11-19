"""One forward → a `forwards` document (T368 §2.2): who wrote it and when, the words, the file — a notebook fetched from
Telegram or by the Colab / Drive link in the text, then read (intake_read.py). The same message twice is stored once."""
import re

from aiogram.types import Message

import intake_match
import intake_read
import labs_pull
from core.bot import notify
from core.models.user import User
from lab_store import TOO_BIG
from models.forward import Forward
from models.lab_file import MAX_BYTES

ASKS = ("подовж", "продовж", "відстроч", "не встиг", "не встигаю", "запізн", "пізніше", "ще час", "більше часу", "перенес",
        "хворі", "лікарн", "дедлайн", "можна здати")
URL = re.compile(r"https?://\S+")
NO_FILE = "Telegram не віддав файл: {}"


def asks(text: str) -> bool:
    return any(w in text.lower() for w in ASKS)


def media(message: Message) -> dict:
    """{name, size, uid, tg} of whatever file the message carries; a photo is named by its type."""
    m = message.document or message.video or message.audio or message.voice or message.animation or (message.photo or [None])[-1]
    return {"name": getattr(m, "file_name", None) or message.content_type, "size": m.file_size or 0, "uid": m.file_unique_id,
            "tg": m.file_id} if m else {}


async def fetch(file: dict, text: str) -> tuple[dict, bytes | None, str]:
    """(file, bytes, why there are none): a notebook from Telegram, or behind a Google link when no file came."""
    if file:
        if not intake_read.wanted(file["name"]):
            return file, None, intake_read.NOT_NB
        if file["size"] > MAX_BYTES:
            return file, None, TOO_BIG
        try:
            return file, (await notify.bot().download(file["tg"])).read(), ""
        except Exception as e:  # noqa: BLE001 — whatever Telegram says, the message is kept with the words
            return file, None, NO_FILE.format(getattr(e, "message", "") or type(e).__name__)
    if not (link := next((u for u in URL.findall(text) if labs_pull.drive_id(u)), "")):
        return {}, None, ""
    try:
        return {"name": "colab.ipynb", "link": link}, await labs_pull.pull(link), ""
    except ValueError as e:
        return {"name": "colab.ipynb", "link": link}, None, str(e)


async def take(message: Message, admin: User) -> Forward | None:
    """The forward of a person (not a chat or channel); None — this very message is here already: the same file of the same
    writer, or, without a file, the same writer, moment and words (an album's files share the moment and have no words)."""
    o = message.forward_origin
    tg = o.sender_user if o.type == "user" else None
    name = tg.full_name if tg else o.sender_user_name
    text, file = message.text or message.caption or "", media(message)
    author = {"tg_id": tg.id} if tg else {"tg_id": None, "name": name}
    if await Forward.find_one(author | ({"file.uid": file["uid"]} if file else {"sent_at": o.date, "text": text})):
        return None
    file, data, why = await fetch(file, text)
    got = await intake_read.read(file["name"], data) if data else {"why": why}
    mine = bool(tg) and tg.id == message.from_user.id
    key = "" if mine else f"tg:{tg.id}" if tg else f"name:{name}"
    return await Forward(key=key, tg_id=tg.id if tg else None, name=name, username=(tg.username if tg else None) or "", mine=mine,
                         sent_at=o.date, by=admin.email, msg=message.message_id, text=text, file=file, asks=not mine and asks(text),
                         **await intake_match.owner(key), **got).insert()
