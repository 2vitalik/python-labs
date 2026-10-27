"""/due — the deadline of one student's lab (T235): from the chat with them (Chat Automation — the command vanishes like /hide),
the forum (ephemeral) or the bot's own chat. The answer is the admins' alert; the student's chat gets nothing."""
from aiogram import Router, html
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from core.bot import notify
from core.bot.alerts import who
from core.bot.notes import ack, as_admin, done, target, vanish
from core.config import settings
from core.lab_marks import kyiv, parse_due, set_mark
from core.labs import Index
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


async def status(student: User, lab: int | None = None) -> str:
    cells = (await Index.load([student.email])).cells(student.email, student.github, student.group, settings.labs)
    rows = [line(n, c) for n, c in cells.items() if lab is None or int(n) == lab]
    return "\n".join([f"📅 {who(student, '/edit')}", *rows])


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
    _, changed = await set_mark(student, int(args[0]), data, admin.email)  # the alert is the confirmation
    if not changed:
        await tell(f"☝️ Без змін · {who(student)} · Лаба {args[0]}")
    if business:
        if warn := await vanish(message):
            await notify.send("due", "\n".join(warn), student.email)
    else:
        await done(message)
