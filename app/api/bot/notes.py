"""/note — teacher's note about a student (T132): hidden via Chat Automation (the command is taken out of the chat),
ephemeral in the forum, plain in the bot's own chat; «📝 …» written to a student = a note the student saw too."""
from aiogram import F, Router, html
from aiogram.exceptions import TelegramAPIError
from aiogram.filters import Command, CommandObject
from aiogram.types import BusinessConnection, EphemeralMessageParameters, Message

from bot import notify
from bot.alerts import who
from models.note import Note
from models.user import Status, User

router = Router()
HINT = "☝️ /note <текст> у чаті зі студентом · у форумі — відповіддю на його повідомлення або /note <нік> <текст>"
RIGHTS = ("can_reply", "can_read_messages", "can_delete_sent_messages", "can_delete_all_messages")


async def as_admin(message: Message) -> dict | bool:
    """Filter + data: the sender is an admin who linked the bot; in a student's chat that is the teacher's own line."""
    admin = await User.find_one({"status": Status.admin, "tg_chat_id": message.from_user.id}) if message.from_user else None
    return {"admin": admin} if admin else False


router.message.filter(Command("note"), as_admin)
router.business_message.filter(as_admin)


async def save(student: User | None, tg_id: int | None, text: str, admin: User, visible: bool, source: str) -> None:
    await Note(user=student.email if student else "", tg_id=tg_id, text=text, by=admin.email, visible=visible, source=source).insert()
    target = who(student) if student else f"<i>не привʼязаний</i> · tg {tg_id}"
    await notify.send("note", f"📝 Нотатка · {target}\n{'👁' if visible else '🙈'} {html.quote(text)}")


async def ack(message: Message, text: str) -> None:
    """In groups the answer is ephemeral — only the teacher sees it."""
    if message.chat.type == "private":
        await message.answer(text)
    else:
        await message.answer(text, ephemeral_message_parameters=EphemeralMessageParameters(receiver_user_id=message.from_user.id))


@router.business_message(Command("note"))
async def hidden(message: Message, command: CommandObject, admin: User):
    """/note in a student's chat: keep the note, take the command out of the chat before the student reads it."""
    if command.args:
        await save(await User.find_one(User.tg_chat_id == message.chat.id), message.chat.id, command.args, admin, False, "private")
    else:
        await notify.send("note", HINT)
    try:
        await notify.bot().delete_business_messages(business_connection_id=message.business_connection_id, message_ids=[message.message_id])
    except TelegramAPIError as e:  # no «delete all messages» right
        await notify.send("note", f"⚠️ Команду з чату не прибрав: {html.quote(e.message)}")


@router.business_message(F.text.startswith("📝"))
async def seen(message: Message, admin: User):
    await save(await User.find_one(User.tg_chat_id == message.chat.id), message.chat.id,
               message.text.removeprefix("📝").strip(), admin, True, "private")


@router.message()
async def note(message: Message, command: CommandObject, admin: User):
    """/note in the forum (ephemeral) or in the bot's own chat: the student is the replied-to sender or the first word."""
    text, reply = command.args or "", message.reply_to_message
    if reply and reply.from_user and not reply.forum_topic_created:  # a topic message «replies» to the topic itself
        student, tg_id = await User.find_one(User.tg_chat_id == reply.from_user.id), reply.from_user.id
    else:
        nick, _, text = text.partition(" ")
        nick = nick.lstrip("@")
        student = (await User.by_nick(nick) or await User.find_one(User.tg_username == nick)) if nick else None
        tg_id = student.tg_chat_id if student else None
    if not (student or tg_id) or not text.strip():
        await ack(message, HINT)
        return
    await save(student, tg_id, text.strip(), admin, False, "forum" if message.chat.type != "private" else "bot")
    await ack(message, "✔️ Записав")


@router.business_connection()
async def connected(event: BusinessConnection):
    on = [r for r in RIGHTS if event.rights and getattr(event.rights, r)]
    state = "підключено" if event.is_enabled else "відключено"
    await notify.send("note", f"🤖 Chat Automation · {state} · @{html.quote(event.user.username or '')}\n🔑 {', '.join(on) or '—'}")
