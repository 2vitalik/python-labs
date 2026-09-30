"""Admin alerts (T111): a kind goes to the chat/topic bound with /here; unbound — to every admin's private chat."""
import logging
from contextvars import ContextVar
from functools import cache

from aiogram import Bot, html
from aiogram.client.default import DefaultBotProperties
from aiogram.exceptions import TelegramAPIError
from aiogram.methods import SendMessage, SendPoll

from core.bot import log
from core.config import settings
from core.models.event import Event
from core.models.notify import Route
from core.models.user import Status, User

KINDS = {  # the platform's; a site puts its own in with add()
    "fill": "🟢 нові дані в профілі",
    "change": "🟠 зміни й видалення в профілі",
    "login": "👋 перші входи на сайт",
    "note": "📝 нотатки про студентів, Chat Automation",
    "msg": "💬 повідомлення боту від студентів",
    "poll": "🗳 опитування: не надіслано, голоси розходяться з Telegram",
    "error": "💥 помилки сайту, API і бота",
    "digest": "📊 ранковий дайджест профілів",
}
MUTED = 0  # Route.chat_id for "nowhere" (/mute)
kind_var: ContextVar[str] = ContextVar("kind", default="reply")  # what send() is sending, for the outgoing log
logger = logging.getLogger(__name__)


def add(kinds: dict[str, str], after: str) -> None:
    """A site's own kinds; /here lists them right after the kind `after`."""
    items = [(k, v) for k, v in KINDS.items() if k not in kinds]
    at = [k for k, _ in items].index(after) + 1
    KINDS.clear()  # in place: whoever imported the dict sees the new kinds
    KINDS.update(items[:at] + list(kinds.items()) + items[at:])


def label(kind: str) -> str:
    """'🟢 fill · нові дані в профілі' — the key is what /here takes."""
    emoji, desc = KINDS[kind].split(" ", 1)
    return f"{emoji} {kind} · {desc}"


async def outgoing(make_request, bot: Bot, method):
    """Session middleware of the shared Bot: every sent message → `messages`, from the bot and the API alike."""
    result = await make_request(bot, method)
    if isinstance(method, (SendMessage, SendPoll)):
        await log.save(result, "out", kind_var.get())
    return result


@cache
def bot() -> Bot:
    b = Bot(settings.tg_bot_token, default=DefaultBotProperties(parse_mode="HTML", link_preview_is_disabled=True))
    b.session.middleware(outgoing)
    return b


async def send(kind: str, text: str, user: str = "") -> None:
    """`user` — email of whom the event is about. The event lands in `events` first: Telegram may get nothing."""
    event = await Event(kind=kind, text=text, user=user).insert()
    if not settings.tg_bot_token:
        return
    token = kind_var.set(kind)
    try:
        if await deliver(kind, text):
            await event.set({Event.sent: True})
    finally:
        kind_var.reset(token)


async def deliver(kind: str, text: str) -> bool:
    """True once somebody got it."""
    route = await Route.find_one(Route.kind == kind)
    if route and route.chat_id == MUTED:
        return False
    if route:
        try:
            await bot().send_message(route.chat_id, text, message_thread_id=route.thread_id)
            return True
        except TelegramAPIError as e:  # kicked from the group, topic closed… — tell the admins instead
            text = f"⚠️ Не доставив у <b>{html.quote(route.title)}</b>: {html.quote(e.message)}\n\n{text}"
    got = False
    for admin in await User.find({"status": Status.admin, "tg_chat_id": {"$ne": None}}).to_list():
        try:
            await bot().send_message(admin.tg_chat_id, text)
            got = True
        except TelegramAPIError as e:
            logger.warning("alert to %s failed: %s", admin.email, e.message)
    return got
