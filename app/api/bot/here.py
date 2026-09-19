"""/here — bind alert kinds to the chat or forum topic the command was sent in; admins only (T111)."""
from aiogram import Router, html
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from bot.notify import KINDS
from models.notify import Route
from models.user import Status, User

router = Router()
HINT = "☝️ /here " + " · ".join([*KINDS, "all", "off"])


async def is_admin(message: Message) -> bool:
    """An admin who linked the bot: in private chats user id == chat id we stored."""
    return bool(message.from_user) and await User.find_one(
        {"status": Status.admin, "tg_chat_id": message.from_user.id}) is not None


router.message.filter(Command("here"), is_admin)


def title(message: Message) -> str:
    name = message.chat.title or "особистий чат"
    if message.is_topic_message:  # a topic message replies to the topic's opening service message
        reply = message.reply_to_message
        topic = reply.forum_topic_created.name if reply and reply.forum_topic_created else f"#{message.message_thread_id}"
        name += f" › {topic}"
    return name


async def status(chat_id: int, thread_id: int | None) -> str:
    routes = {r.kind: r for r in await Route.find_all().to_list()}
    lines = ["🗂 Куди що йде:"]
    for kind, label in KINDS.items():
        r = routes.get(kind)
        where = "<i>особисто адмінам</i>" if not r else \
            "тут" if (r.chat_id, r.thread_id) == (chat_id, thread_id) else f"<b>{html.quote(r.title)}</b>"
        lines.append(f"{label} → {where}")
    return "\n".join([*lines, HINT])


@router.message()
async def here(message: Message, command: CommandObject):
    chat_id, thread_id = message.chat.id, message.message_thread_id if message.is_topic_message else None
    kinds = (command.args or "").split()
    if not kinds:
        await message.answer(await status(chat_id, thread_id))
        return
    if kinds == ["off"]:
        gone = await Route.find(Route.chat_id == chat_id, Route.thread_id == thread_id).delete()
        await message.answer("✔️ Сюди більше нічого не йтиме" if gone.deleted_count else "☝️ Сюди й так нічого не йшло")
        return
    if kinds == ["all"]:
        kinds = list(KINDS)
    if unknown := [k for k in kinds if k not in KINDS]:
        await message.answer(f"❌ Не знаю «{html.quote(unknown[0])}»\n{HINT}")
        return
    await Route.find({"kind": {"$in": kinds}}).delete()
    await Route.insert_many([Route(kind=k, chat_id=chat_id, thread_id=thread_id, title=title(message)) for k in kinds])
    await message.answer("\n".join(["✔️ Сюди йтимуть:", *(KINDS[k] for k in kinds)]))
