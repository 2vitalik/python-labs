"""Smoke: /due from the student's chat (Chat Automation), the forum and the bot's chat (T235); the dates it takes; Telegram replaced
by a recorder. Run from app/api: DB_NAME=python_labs_smoke uv run python tests/smoke_due.py"""
import asyncio
import os
import sys
from datetime import datetime, timezone
from types import SimpleNamespace

sys.path.insert(0, os.getcwd())
from pymongo import MongoClient  # noqa: E402

DB = os.environ["DB_NAME"]
assert DB.endswith("_smoke"), "refuse to run on a non-smoke DB"
MongoClient().drop_database(DB)

from core.bot import due, notify  # noqa: E402
from core.config import settings  # noqa: E402
from core.lab_marks import TZ, parse_due  # noqa: E402
from core.models.deadline import Deadline, LabMark  # noqa: E402
from core.models.user import Status, User  # noqa: E402
from db import init_db  # noqa: E402

settings.tg_bot_token = "fake"
sent, deleted, reacted, results = [], [], [], []


class FakeBot:
    async def send_message(self, chat_id, text, message_thread_id=None):
        sent.append((chat_id, text))

    async def set_message_reaction(self, chat_id, message_id, reaction):
        reacted.append((chat_id, message_id, reaction[0].emoji))

    async def get_business_connection(self, business_connection_id):
        return SimpleNamespace(rights=SimpleNamespace(can_reply=True, can_read_messages=True, can_delete_sent_messages=False, can_delete_all_messages=False))

    async def delete_business_messages(self, business_connection_id, message_ids):
        deleted.append((business_connection_id, message_ids))


notify.bot = lambda: FakeBot()


def check(name, cond, extra=""):
    results.append(bool(cond))
    print(("PASS " if cond else "FAIL ") + name + (f" · {extra}" if extra and not cond else ""))


def fake(chat_id=42, user_id=7, chat_type="private", conn=None, reply=None, ephemeral=None):
    answers = []

    async def answer(t, **kw):
        answers.append((t, kw))
    m = SimpleNamespace(chat=SimpleNamespace(id=chat_id, type=chat_type), from_user=SimpleNamespace(id=user_id, username="vitalik"),
                        business_connection_id=conn, message_id=5, reply_to_message=reply, answer=answer, ephemeral_message_id=ephemeral)
    return m, answers


cmd = lambda args: SimpleNamespace(command="due", args=args)  # noqa: E731
alert = lambda: sent[-1][1]  # noqa: E731
utc = lambda *a: datetime(*a, tzinfo=timezone.utc)  # noqa: E731

today = datetime(2026, 10, 25, tzinfo=TZ)
check("5.11 → 2026-11-05 23:59 Kyiv = 21:59Z", parse_due("5.11", today) == utc(2026, 11, 5, 21, 59), parse_due("5.11", today))
check("05.11.26 · 5.11.2026 · 2026-11-05 → the same", parse_due("05.11.26", today) == parse_due("5.11.2026", today) == parse_due("2026-11-05", today) == utc(2026, 11, 5, 21, 59))
check("2026-11-05 18:35 keeps its time → 16:35Z", parse_due("2026-11-05 18:35", today) == utc(2026, 11, 5, 16, 35), parse_due("2026-11-05 18:35", today))
check("summer: 5.6 → 20:59Z", parse_due("5.6", today) == utc(2026, 6, 5, 20, 59))
check("not a date → None", parse_due("?", today) is None and parse_due("вчора", today) is None and parse_due("32.13", today) is None)


async def run():
    await init_db()
    await User(email="vasya@nure.ua", status=Status.student, last_name="Пупкін", first_name="Василь", group="ПЗПІ-25-1", tg_chat_id=42,
               tg_username="vasya_tg", github="https://github.com/v/g").insert()
    admin = await User(email="v@nure.ua", status=Status.admin, tg_chat_id=7).insert()
    await Deadline(lab=1, at=datetime(2026, 10, 20, 20, 59)).insert()

    m, _ = fake(conn="c1")
    await due.due(m, cmd("1 5.11 хворів"), admin)
    mark = await LabMark.find_one(LabMark.user == "vasya@nure.ua")
    check("/due 1 5.11 хворів in the student's chat: until 5.11 21:59Z, reason, by the teacher",
          mark and mark.until == datetime(2026, 11, 5, 21, 59) and mark.reason == "хворів" and mark.by == "v@nure.ua", mark)
    check("command taken out of the chat, alert 📅 with ⏳ and 💬, the card link",
          deleted == [("c1", [5])] and alert().startswith("📅 Лаба 1 · ") and "⏳ до 5.11 23:59" in alert() and "💬 хворів" in alert() and "/students/vasya/edit" in alert(), alert())
    check("nothing to the student: one message, the alert", len(sent) == 1)

    m, _ = fake(conn="c1")
    await due.due(m, cmd("1 ?"), admin)
    mark = await LabMark.find_one(LabMark.user == "vasya@nure.ua")
    check("/due 1 ? → open, no date", mark.open and mark.until is None and "дата поки невідома" in alert(), alert())
    m, _ = fake(conn="c1")
    await due.due(m, cmd("1 ?"), admin)
    check("the same again → «без змін», the command still taken out", alert().startswith("☝️ Без змін") and len(deleted) == 3, alert())
    m, _ = fake(conn="c1")
    await due.due(m, cmd("1 -"), admin)
    mark = await LabMark.find_one(LabMark.user == "vasya@nure.ua")
    check("/due 1 - → extension gone", not mark.open and mark.until is None and "✖️ подовження знято" in alert(), alert())

    m, _ = fake(conn="c1")
    await due.due(m, cmd(""), admin)
    check("/due → the student's labs as an alert: 🔍 for lab 1, — for lab 5",
          alert().startswith("📅 ") and "🔍 не перевірено · Лаба 1 · до 20.10 23:59" in alert() and "— дедлайн не заданий · Лаба 5" in alert(), alert())
    m, _ = fake(conn="c1")
    await due.due(m, cmd("1"), admin)
    check("/due 1 → one lab", "Лаба 1" in alert() and "Лаба 2" not in alert(), alert())
    m, _ = fake(conn="c1")
    await due.due(m, cmd("9 5.11"), admin)
    check("/due 9 → hint", alert() == due.HINT)
    m, _ = fake(conn="c1")
    await due.due(m, cmd("1 вчора"), admin)
    check("not a date → hint", alert() == due.HINT)
    check("hint is HTML-safe", "<" not in due.HINT and "&lt;лаба&gt;" in due.HINT)

    reply = SimpleNamespace(from_user=SimpleNamespace(id=42), forum_topic_created=None)
    m, answers = fake(chat_id=-100, chat_type="supergroup", reply=reply, ephemeral=9)
    await due.due(m, cmd("2 2026-11-20 поїздка"), admin)
    mark = await LabMark.find_one(LabMark.lab == 2)
    check("forum, ephemeral reply: lab 2 until 20.11, ephemeral ✔️ to the teacher",
          mark.until == datetime(2026, 11, 20, 21, 59) and answers[0][0] == "✔️ Записав" and answers[0][1]["ephemeral_message_parameters"].receiver_user_id == 7, (mark, answers))

    m, answers = fake(chat_id=7)
    await due.due(m, cmd("vasya 3 1.12"), admin)
    mark = await LabMark.find_one(LabMark.lab == 3)
    check("bot's chat with a nick: lab 3, ✍ reaction, no text", mark.until == datetime(2026, 12, 1, 21, 59) and reacted[-1] == (7, 5, "✍") and not answers, (mark, answers))
    m, answers = fake(chat_id=7)
    await due.due(m, cmd("nobody 1 1.12"), admin)
    check("unknown nick → the hint as the answer", answers[0][0] == due.HINT, answers)
    m, answers = fake(chat_id=7)
    await due.due(m, cmd("vasya"), admin)
    check("bot's chat: /due nick → the labs answered", answers[0][0].startswith("📅 ") and "⏱ ще є час · Лаба 3 · до 1.12 23:59" in answers[0][0], answers)
    check("history: a row per change", await LabMark.find_all().count() == 3)


asyncio.run(run())
print(f"\n{sum(results)}/{len(results)} passed")
sys.exit(0 if all(results) else 1)
