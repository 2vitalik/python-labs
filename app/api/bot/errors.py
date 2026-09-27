"""Unhandled errors → kind `error` (T113): FastAPI exceptions from the API process, aiogram ones from the bot.
The alert is a line of the failure; all of it goes to `errors` (T149)."""
import logging
import os
import traceback

from aiogram import html
from aiogram.types import ErrorEvent
from fastapi import Request
from starlette.background import BackgroundTask
from starlette.responses import JSONResponse

from bot import notify
from bot.log import email as linked_email
from models.activity import client
from models.error import Error

log = logging.getLogger(__name__)


def describe(exc: BaseException) -> list[str]:
    """❗ type: message (first line) · 📍 the last frame in our own code."""
    msg = str(exc).splitlines()[0] if str(exc) else ""
    rows = [f"❗ {type(exc).__name__}: {html.quote(msg[:300])}"]
    frames = traceback.extract_tb(exc.__traceback__)
    if ours := [f for f in frames if "site-packages" not in f.filename] or frames:
        f = ours[-1]
        rows.append(f"📍 {html.quote(f.filename.removeprefix(os.getcwd() + '/'))}:{f.lineno} {html.quote(f.name)}")
    return rows


async def keep(source: str, exc: BaseException, head: str, user: str, **fields) -> None:
    await Error(source=source, title=f"{type(exc).__name__}: {exc}"[:300], trace="".join(traceback.format_exception(exc))[-20000:],
                user=user, **fields).insert()
    await notify.send("error", "\n".join([head, *describe(exc)]), user)


async def api_handler(request: Request, exc: Exception) -> JSONResponse:
    """500 for the client; the rest happens after the response, so neither Mongo nor Telegram delays the API."""
    email = request.scope.get("session", {}).get("email", "")
    head = f"💥 API · {request.method} {html.quote(request.url.path)}"
    if email:
        head += f" · {html.quote(email.split('@')[0])}"
    path = request.url.path + (f"?{request.url.query}" if request.url.query else "")
    task = BackgroundTask(keep, "api", exc, head, email, method=request.method, path=path, **client(request))
    return JSONResponse({"detail": "Internal Server Error"}, 500, background=task)


async def bot_handler(event: ErrorEvent) -> bool:
    log.error("update %s failed", event.update.update_id, exc_info=event.exception)
    msg = event.update.message
    head = f"💥 Бот · {event.update.event_type}"
    if msg and msg.from_user and msg.from_user.username:
        head += f" · @{html.quote(msg.from_user.username)}"
    sender = await linked_email(msg.from_user.id) if msg and msg.from_user else ""
    await keep("bot", event.exception, head, sender, path=event.update.event_type)
    return True
