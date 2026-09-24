"""Admin alerts (T111): a kind goes to the chat/topic bound with /here; unbound — to every admin's private chat."""
import logging
from contextvars import ContextVar
from functools import cache

from aiogram import Bot, html
from aiogram.client.default import DefaultBotProperties
from aiogram.exceptions import TelegramAPIError
from aiogram.methods import SendMessage

from bot import log
from config import settings
from models.notify import Route
from models.user import Status, User

KINDS = {
    "fill": "🟢 нові дані в профілі",
    "change": "🟠 зміни й видалення в профілі",
    "login": "👋 перші входи на сайт",
    "claim": "🎯 заявки на картки",
    "game": "🧩 гра студента: картка, обʼєкти, правила",
    "error": "💥 помилки API і бота",
    "digest": "📊 ранковий дайджест профілів",
}
MUTED = 0  # Route.chat_id for "nowhere" (/mute)
kind_var: ContextVar[str] = ContextVar("kind", default="reply")  # what send() is sending, for the outgoing log
logger = logging.getLogger(__name__)


def label(kind: str) -> str:
    """'🟢 fill · нові дані в профілі' — the key is what /here takes."""
    emoji, desc = KINDS[kind].split(" ", 1)
    return f"{emoji} {kind} · {desc}"


async def outgoing(make_request, bot: Bot, method):
    """Session middleware of the shared Bot: every sent message → `messages`, from the bot and the API alike."""
    result = await make_request(bot, method)
    if isinstance(method, SendMessage):
        await log.save(result, "out", kind_var.get())
    return result


@cache
def bot() -> Bot:
    b = Bot(settings.tg_bot_token, default=DefaultBotProperties(parse_mode="HTML", link_preview_is_disabled=True))
    b.session.middleware(outgoing)
    return b


async def send(kind: str, text: str) -> None:
    if not settings.tg_bot_token:
        return
    token = kind_var.set(kind)
    try:
        await deliver(kind, text)
    finally:
        kind_var.reset(token)


async def deliver(kind: str, text: str) -> None:
    route = await Route.find_one(Route.kind == kind)
    if route and route.chat_id == MUTED:
        return
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
            logger.warning("alert to %s failed: %s", admin.email, e.message)
