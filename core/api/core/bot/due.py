"""/due — the deadline of one student's lab (T235): from the chat with them (Chat Automation — the command vanishes like /hide),
the forum (ephemeral) or the bot's own chat. The answer is the admins' alert; in the student's chat an extension is told to them
from the teacher's account, the bot named first (T245)."""
from aiogram import Router, html
from aiogram.exceptions import TelegramAPIError
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from core.bot import notify
from core.bot.alerts import who
from core.bot.notes import ack, as_admin, done, target, vanish
from core.config import settings
from core.lab_marks import day, kyiv, parse_due, set_mark
from core.labs import Index
from core.models.deadline import LabMark
from core.models.user import User

router = Router()
COMMANDS = {"due": "дедлайн лаби студента (команда зникає)"}  # registered as ephemeral
HINT = html.quote("☝️ /due <лаба> <дата | ? | ! | -> [текст] — 5.11 подовжити до дати · ? подовжено, дата поки невідома · "
                  "! лише просив, ще не вирішено · - зняти подовження\n"
                  "☝️ /due — стани лаб студента · у форумі й чаті з ботом: відповіддю або /due <нік> …")
STATES = {"ok": "✅ вчасно", "late": "🕒 пізно", "partial": "🟡 частково", "miss": "❌ не вклався", "open": "⏳ подовжено, дата невідома",
          "wait": "⏱ ще є час", "check": "🔍 не перевірено", "norepo": "🚫 без репозиторію", "noaccess": "⚠️ репозиторій недоступний",
          "nodue": "— дедлайн не заданий"}

router.message.filter(Command(*COMMANDS), as_admin)
router.business_message.filter(Command(*COMMANDS), as_admin)


def line(n: str, c: dict) -> str:
    m = c["mark"] or {}
    due = f" · до {kyiv(c['due'])}" if c["due"] else ""
    commits = f" · комітів до дедлайну: {c['facts']['before']}" if c["facts"]["before"] else ""
    asked = (" · 🙋 просив" + (f" {html.quote(m['asked_for'])}" if m.get("asked_for") else "")) if m.get("asked") else ""
    reason = f" · 💬 {html.quote(m['reason'])}" if m.get("reason") else ""
    return f"{STATES[c['state']]} · Лаба {n}{due}{commits}{asked}{reason}"


async def cells(student: User) -> dict[str, dict]:
    return (await Index.load([student.email])).cells(student.email, student.github, student.group, settings.labs)


async def status(student: User, lab: int | None = None) -> str:
    rows = [line(n, c) for n, c in (await cells(student)).items() if lab is None or int(n) == lab]
    return "\n".join([f"📅 {who(student, '/edit')}", *rows])


async def told(student: User, lab: int, mark: LabMark, changed: set[str]) -> str:
    """What the student reads: only an extension is theirs to know; a reason, a verdict, 🙋 stay with the teacher."""
    if not changed & {"until", "open"}:
        return ""
    if mark.until:
        what = f"дедлайн подовжено:  {day(mark.until)}"
    elif mark.open:
        what = "дедлайн подовжено, дату узгодимо окремо"
    else:
        base = (await cells(student))[str(lab)]["due"]
        what = f"подовження знято, дедлайн знову:  {day(base)}" if base else "подовження знято"
    return f"🤖 <i>Бот записав:</i>\n{lab}\ufe0f\u20e3 {what}"  # 1️⃣ — the lab's keycap


async def tell_student(message: Message, text: str) -> list[str]:
    """Into this chat from the teacher's account (Chat Automation); the lines say when Telegram refused."""
    try:
        await notify.bot().send_message(message.chat.id, text, business_connection_id=message.business_connection_id)
        return []
    except TelegramAPIError as e:
        return [f"⚠️ Студентові не написав: {html.quote(e.message)}",
                "☝️ потрібне право «Reply to messages» (Business → Chatbots), і студент має писати в цей чат за останню добу"]


def patch(what: str, text: str) -> dict | None:
    """The second word; `text` — the reason, or after `!` what they asked for. An extension given here means they asked (🙋);
    a date without words keeps the reason already written."""
    if what == "!":
        return {"asked": True} | ({"asked_for": text} if text else {})
    if what == "-":
        return {"open": False, "until": None, "reason": ""}
    if what == "?":
        return {"open": True, "until": None, "asked": True} | ({"reason": text} if text else {})
    if at := parse_due(what):
        return {"until": at, "asked": True} | ({"reason": text} if text else {})
    return None


@router.message()
@router.business_message()
async def due(message: Message, command: CommandObject, admin: User):
    business = message.business_connection_id
    student, _, text = await target(message, command.args or "")

    async def tell(t: str) -> None:  # in the student's chat the bot stays silent: the teacher hears through the alert
        await (notify.send("due", t, student.email if student else "") if business else ack(message, t))

    args = text.split(maxsplit=2)
    if not student or (args and not (args[0].isdigit() and 1 <= int(args[0]) <= settings.labs)):
        await tell(HINT)
        return
    if len(args) < 2:
        await tell(await status(student, int(args[0]) if args else None))
        return
    data = patch(args[1], args[2] if len(args) > 2 else "")
    if data is None:
        await tell(HINT)
        return
    mark, changed = await set_mark(student, int(args[0]), data, admin.email)  # the alert is the confirmation
    if not changed:
        await tell(f"☝️ Без змін · {who(student)} · Лаба {args[0]}")
    if business:
        warn = []
        if said := await told(student, int(args[0]), mark, changed):
            warn += await tell_student(message, said)
        warn += await vanish(message)
        if warn:
            await notify.send("due", "\n".join(warn), student.email)
    else:
        await done(message)
