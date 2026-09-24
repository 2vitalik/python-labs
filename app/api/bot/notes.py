"""/note and /hide — teacher's notes about a student (T132, T134): /note the student sees, /hide is only ours.
From a student's chat (Chat Automation) the command is taken out of the chat; in the forum both are ephemeral."""
import re

from aiogram import Router, html
from aiogram.exceptions import TelegramAPIError
from aiogram.filters import Command, CommandObject
from aiogram.types import BusinessConnection, Message

from bot import notify
from bot.alerts import who
from bot.note_show import ack, show, target
from models.note import Note
from models.user import Status, User

router = Router()
HINT = "☝️ /note <текст> — студент побачить · /hide <текст> — лише тобі\n☝️ у форумі й у чаті з ботом — відповіддю або /note <нік> <текст>"
RIGHTS = ("can_reply", "can_read_messages", "can_delete_sent_messages", "can_delete_all_messages")
COMMANDS = {"note": "нотатка, яку студент побачить", "hide": "нотатка лише тобі"}


async def as_admin(message: Message) -> dict | bool:
    """Filter + data: the sender is an admin who linked the bot; in a student's chat that is the teacher's own line."""
    admin = await User.find_one({"status": Status.admin, "tg_chat_id": message.from_user.id}) if message.from_user else None
    return {"admin": admin} if admin else False


def guest_command(message: Message) -> dict | bool:
    """A guest mention carries the command after the @bot: «@python_nure_bot /note текст»."""
    m = re.search(r"/(note|hide)\b\s*(.*)", message.text or "", re.S)
    return {"command": CommandObject(prefix="/", command=m[1], args=m[2].strip())} if m else False


router.message.filter(Command(*COMMANDS), as_admin)
router.business_message.filter(Command(*COMMANDS), as_admin)
router.guest_message.filter(guest_command, as_admin)


@router.message()
@router.business_message()
@router.guest_message()
async def note(message: Message, command: CommandObject, admin: User):
    business = message.business_connection_id
    student, tg_id, text = await target(message, command.args or "")
    if not (student or tg_id) or not (text := text.strip()):
        await (notify.send("note", HINT) if business else ack(message, HINT))
        return
    visible = command.command == "note"
    shown = await show(message, student, text, admin) if visible else ""
    source = "private" if business else "guest" if message.guest_query_id else "forum" if message.chat.type != "private" else "bot"
    await Note(user=student.email if student else "", tg_id=tg_id, text=text, by=admin.email, visible=visible, shown=shown, source=source).insert()
    lines = [f"📝 Нотатка · {who(student) if student else f'<i>не привʼязаний</i> · tg {tg_id}'}", f"{'👁' if visible else '🙈'} {html.quote(text)}"]
    if visible:
        lines.append(f"📍 {shown}" if shown else "⚠️ Не показав: студент не привʼязав бота")
    if business and (shown or not visible):  # the command must not stay in the student's chat
        try:
            await notify.bot().delete_business_messages(business_connection_id=business, message_ids=[message.message_id])
        except TelegramAPIError as e:  # no «delete all messages» right
            lines.append(f"⚠️ Команду з чату не прибрав: {html.quote(e.message)}")
    await notify.send("note", "\n".join(lines))
    if not business and not message.guest_query_id:
        await ack(message, "✔️ Записав" + (f" · {shown}" if shown else "\n⚠️ Студент не привʼязав бота — не показав" if visible else ""))


@router.business_connection()
async def connected(event: BusinessConnection):
    on = [r for r in RIGHTS if event.rights and getattr(event.rights, r)]
    state = "підключено" if event.is_enabled else "відключено"
    await notify.send("note", f"🤖 Chat Automation · {state} · @{html.quote(event.user.username or '')}\n🔑 {', '.join(on) or '—'}")
