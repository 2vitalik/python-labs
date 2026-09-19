"""Unhandled errors → kind `error` (T113): FastAPI exceptions from the API process, aiogram ones from the bot."""
import logging
import os
import traceback

from aiogram import html
from aiogram.types import ErrorEvent
from fastapi import Request
from starlette.background import BackgroundTask
from starlette.responses import JSONResponse

from bot import notify

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


async def api_handler(request: Request, exc: Exception) -> JSONResponse:
    """500 for the client; the alert goes out after the response, so Telegram never delays the API."""
    email = request.scope.get("session", {}).get("email", "")
    head = f"💥 API · {request.method} {html.quote(request.url.path)}"
    if email:
        head += f" · {html.quote(email.split('@')[0])}"
    text = "\n".join([head, *describe(exc)])
    return JSONResponse({"detail": "Internal Server Error"}, 500, background=BackgroundTask(notify.send, "error", text))


async def bot_handler(event: ErrorEvent) -> bool:
    log.error("update %s failed", event.update.update_id, exc_info=event.exception)
    msg = event.update.message
    head = f"💥 Бот · {event.update.event_type}"
    if msg and msg.from_user and msg.from_user.username:
        head += f" · @{html.quote(msg.from_user.username)}"
    await notify.send("error", "\n".join([head, *describe(event.exception)]))
    return True
