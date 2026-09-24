"""Smoke: /note from a student's chat (Chat Automation), the forum and the bot's chat; Telegram replaced by a recorder.
Run from app/api: DB_NAME=python_labs_smoke uv run python tests/smoke_notes.py"""
import asyncio
import os
import sys
from types import SimpleNamespace

sys.path.insert(0, os.getcwd())
from pymongo import MongoClient  # noqa: E402

DB = os.environ["DB_NAME"]
assert DB.endswith("_smoke"), "refuse to run on a non-smoke DB"
MongoClient().drop_database(DB)
from aiogram.exceptions import TelegramAPIError  # noqa: E402

from bot import log, notes, notify  # noqa: E402
from config import settings  # noqa: E402
from db import init_db  # noqa: E402
from models.message import TgMessage  # noqa: E402
from models.note import Note  # noqa: E402
from models.user import Status, User  # noqa: E402

settings.tg_bot_token = "fake"
sent, deleted, results = [], [], []


class FakeBot:
    async def send_message(self, chat_id, text, message_thread_id=None):
        sent.append((chat_id, text))

    async def delete_business_messages(self, business_connection_id, message_ids):
        if business_connection_id == "broken":
            raise TelegramAPIError(method=None, message="not enough rights")
        deleted.append((business_connection_id, message_ids))


notify.bot = lambda: FakeBot()


def check(name, cond, extra=""):
    results.append(bool(cond))
    print(("PASS " if cond else "FAIL ") + name + (f" · {extra}" if extra and not cond else ""))


def fake(chat_id=42, user_id=7, chat_type="private", text="", conn="conn1", reply=None):
    answers = []

    async def answer(t, **kw):
        answers.append((t, kw))
    m = SimpleNamespace(chat=SimpleNamespace(id=chat_id, type=chat_type), from_user=SimpleNamespace(id=user_id, username="vitalik"),
                        text=text, business_connection_id=conn, message_id=5, reply_to_message=reply, answer=answer)
    return m, answers


def cmd(args):
    return SimpleNamespace(args=args)


async def run():
    await init_db()
    await User(email="vasya@nure.ua", status=Status.student, last_name="Пупкін", first_name="Василь", group="ПЗПІ-25-1",
               tg_chat_id=42, tg_username="vasya_tg").insert()
    admin = await User(email="v@nure.ua", status=Status.admin, tg_chat_id=7).insert()

    m, _ = fake(text="/note здав пізно")
    check("as_admin: the teacher's own line passes with data", (await notes.as_admin(m))["admin"].email == "v@nure.ua")
    check("as_admin: a student's line does not", await notes.as_admin(fake(user_id=42)[0]) is False)

    await notes.hidden(m, cmd("здав пізно"), admin)
    n = await Note.find_one(Note.text == "здав пізно")
    check("hidden /note: saved for the chat's student, invisible, source private",
          n.user == "vasya@nure.ua" and n.tg_id == 42 and not n.visible and n.source == "private" and n.by == "v@nure.ua")
    check("hidden /note: command taken out of the chat", deleted == [("conn1", [5])])
    check("hidden /note: alert 📝 with name-link and 🙈", sent[-1][0] == 7 and "📝 Нотатка" in sent[-1][1] and "Пупкін Василь" in sent[-1][1] and "🙈 здав пізно" in sent[-1][1])

    m, _ = fake(text="/note x", conn="broken")
    await notes.hidden(m, cmd("x"), admin)
    check("delete failed: note kept, ⚠️ alert", await Note.find_one(Note.text == "x") is not None and "⚠️ Команду з чату не прибрав" in sent[-1][1])

    m, _ = fake(text="📝 здай до пʼятниці")
    await notes.seen(m, admin)
    n = await Note.find_one(Note.text == "здай до пʼятниці")
    check("«📝 …»: visible note, nothing deleted, alert 👁", n.visible and len(deleted) == 1 and "👁 здай до пʼятниці" in sent[-1][1])

    m, _ = fake(chat_id=99, user_id=7, text="/note чужий")
    await notes.hidden(m, cmd("чужий"), admin)
    n = await Note.find_one(Note.text == "чужий")
    check("unlinked chat: note by tg id, alert says so", n.user == "" and n.tg_id == 99 and "не привʼязаний" in sent[-1][1])

    reply = SimpleNamespace(from_user=SimpleNamespace(id=42), forum_topic_created=None)
    m, answers = fake(chat_id=-100, chat_type="supergroup", text="/note запізнився", reply=reply)
    await notes.note(m, cmd("запізнився"), admin)
    n = await Note.find_one(Note.text == "запізнився")
    check("forum, reply to the student: source forum, linked", n.source == "forum" and n.user == "vasya@nure.ua")
    check("forum: ephemeral ✔️ to the teacher only", answers[0][0] == "✔️ Записав" and answers[0][1]["ephemeral_message_parameters"].receiver_user_id == 7)

    topic = SimpleNamespace(from_user=SimpleNamespace(id=7), forum_topic_created=object())
    m, answers = fake(chat_id=-100, chat_type="supergroup", text="/note @vasya_tg без ноута", reply=topic)
    await notes.note(m, cmd("@vasya_tg без ноута"), admin)
    n = await Note.find_one(Note.text == "без ноута")
    check("forum, topic message with @username: student found, text without the nick", n is not None and n.user == "vasya@nure.ua")

    m, answers = fake(chat_id=-100, chat_type="supergroup", text="/note nobody текст", reply=topic)
    await notes.note(m, cmd("nobody текст"), admin)
    check("forum, unknown nick: hint, no note", answers[0][0] == notes.HINT and await Note.find_one(Note.text == "текст") is None)

    m, answers = fake(chat_id=7, text="/note vasya здав")
    await notes.note(m, cmd("vasya здав"), admin)
    n = await Note.find_one(Note.text == "здав")
    check("bot's own chat: nick by email, source bot, plain answer", n.source == "bot" and n.user == "vasya@nure.ua" and answers[0][1] == {})

    rights = SimpleNamespace(can_reply=True, can_read_messages=False, can_delete_sent_messages=False, can_delete_all_messages=True)
    await notes.connected(SimpleNamespace(is_enabled=True, user=SimpleNamespace(username="vitalik"), rights=rights))
    check("business_connection: alert with state and rights", "🤖 Chat Automation · підключено · @vitalik" in sent[-1][1] and "can_reply, can_delete_all_messages" in sent[-1][1])

    await log.deleted(SimpleNamespace(chat=SimpleNamespace(id=42, type="private"), message_ids=[5, 6]))
    check("deleted_business_messages: a row per id", await TgMessage.find(TgMessage.kind == "deleted").count() == 2)
    check("note kind exists in KINDS", "note" in notify.KINDS)

asyncio.run(run())
ok = sum(results)
print(f"\n{ok}/{len(results)} PASS")
sys.exit(0 if ok == len(results) else 1)
