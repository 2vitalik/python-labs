"""Admin alerts (T111): a kind goes to the chat/topic bound with /here; unbound — to every admin's private chat."""
import logging
from functools import cache

from aiogram import Bot, html
from aiogram.client.default import DefaultBotProperties
from aiogram.exceptions import TelegramAPIError

from config import settings
from models.notify import Route
from models.user import Status, User

KINDS = {
    "fill": "🟢 нові дані в профілі",
    "change": "🟠 зміни й видалення в профілі",
    "login": "👋 нові входи на сайт",
}
log = logging.getLogger(__name__)


@cache
def bot() -> Bot:
    return Bot(settings.tg_bot_token, default=DefaultBotProperties(parse_mode="HTML", link_preview_is_disabled=True))


async def send(kind: str, text: str) -> None:
    if not settings.tg_bot_token:
        return
    route = await Route.find_one(Route.kind == kind)
    if route:
        try:
            await bot().send_message(route.chat_id, text, message_thread_id=route.thread_id)
            return
        except TelegramAPIError as e:  # kicked from the group, topic closed… — tell the admins instead
            text = f"⚠️ Не доставив у <b>{html.quote(route.title)}</b>: {html.quote(e.message)}\n\n{text}"
    for admin in await User.find({"status": Status.admin, "tg_chat_id": {"$ne": None}}).to_list():
        try:
            await bot().send_message(admin.tg_chat_id, text)
        except TelegramAPIError as e:
            log.warning("alert to %s failed: %s", admin.email, e.message)
