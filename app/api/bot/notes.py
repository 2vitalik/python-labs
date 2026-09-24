"""/note and /hide — teacher's notes about a student, for the teacher only (T132, T135): `notes` + an alert, nothing else.
/note stays in the chat as typed; /hide is taken out of the student's chat (Chat Automation) or ephemeral in the forum."""
from aiogram import Router, html
from aiogram.exceptions import TelegramAPIError
from aiogram.filters import Command, CommandObject
from aiogram.types import BusinessConnection, EphemeralMessageParameters, Message, ReactionTypeEmoji

from bot import notify
from bot.alerts import who
from models.note import Note
from models.user import Status, User

router = Router()
HINT = "☝️ /note <текст> — лишається в чаті · /hide <текст> — зникає\n☝️ у форумі й у чаті з ботом — відповіддю або /note <нік> <текст>"
RIGHTS = ("can_reply", "can_read_messages", "can_delete_sent_messages", "can_delete_all_messages")
COMMANDS = {"note": "нотатка про студента", "hide": "нотатка, що зникає з чату"}  # hide is registered as ephemeral


async def as_admin(message: Message) -> dict | bool:
    """Filter + data: the sender is an admin who linked the bot; in a student's chat that is the teacher's own line."""
    admin = await User.find_one({"status": Status.admin, "tg_chat_id": message.from_user.id}) if message.from_user else None
    return {"admin": admin} if admin else False


router.message.filter(Command(*COMMANDS), as_admin)
router.business_message.filter(Command(*COMMANDS), as_admin)


async def target(message: Message, text: str) -> tuple[User | None, int | None, str]:
    """The student: the replied-to sender, the chat's owner (Chat Automation), or the first word — nick or @username."""
    reply = message.reply_to_message
    if reply and reply.from_user and not reply.forum_topic_created:  # a topic message «replies» to the topic itself
        return await User.find_one(User.tg_chat_id == reply.from_user.id), reply.from_user.id, text
    if message.business_connection_id:
        return await User.find_one(User.tg_chat_id == message.chat.id), message.chat.id, text
    nick, _, rest = text.partition(" ")
    nick = nick.lstrip("@")
    student = (await User.by_nick(nick) or await User.find_one(User.tg_username == nick)) if nick else None
    return student, student.tg_chat_id if student else None, rest


async def ack(message: Message, text: str) -> None:
    """In groups the answer is ephemeral — only the teacher sees it."""
    if message.chat.type == "private":
        await message.answer(text)
    else:
        await message.answer(text, ephemeral_message_parameters=EphemeralMessageParameters(receiver_user_id=message.from_user.id))


async def done(message: Message) -> None:
    """✍ on the command itself; an ephemeral command has nothing to react to, a group may have reactions off."""
    if not message.ephemeral_message_id:
        try:
            await notify.bot().set_message_reaction(message.chat.id, message.message_id, [ReactionTypeEmoji(emoji="✍")])
            return
        except TelegramAPIError:
            pass
    await ack(message, "✔️ Записав")


@router.message()
@router.business_message()
async def note(message: Message, command: CommandObject, admin: User):
    business = message.business_connection_id
    student, tg_id, text = await target(message, command.args or "")
    if not (student or tg_id) or not (text := text.strip()):
        await (notify.send("note", HINT) if business else ack(message, HINT))
        return
    hidden = command.command == "hide"
    source = "private" if business else "forum" if message.chat.type != "private" else "bot"
    await Note(user=student.email if student else "", tg_id=tg_id, text=text, by=admin.email, hidden=hidden, source=source).insert()
    lines = [f"{'🙈' if hidden else '📝'} Нотатка · {who(student) if student else f'<i>не привʼязаний</i> · tg {tg_id}'}", html.quote(text)]
    if business and hidden:
        try:
            await notify.bot().delete_business_messages(business_connection_id=business, message_ids=[message.message_id])
        except TelegramAPIError as e:  # no «delete all messages» right
            lines.append(f"⚠️ Команду з чату не прибрав: {html.quote(e.message)}")
    await notify.send("note", "\n".join(lines))
    if not business:  # in a student's chat the bot can neither react nor edit: the alert is the confirmation
        await done(message)


@router.business_connection()
async def connected(event: BusinessConnection):
    on = [r for r in RIGHTS if event.rights and getattr(event.rights, r)]
    state = "підключено" if event.is_enabled else "відключено"
    await notify.send("note", f"🤖 Chat Automation · {state} · @{html.quote(event.user.username or '')}\n🔑 {', '.join(on) or '—'}")
