"""Smoke: /note and /hide from a student's chat (Chat Automation), the forum, the bot's chat and a guest mention;
Telegram replaced by a recorder. Run from app/api: DB_NAME=python_labs_smoke uv run python tests/smoke_notes.py"""
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
    async def send_message(self, chat_id, text, message_thread_id=None, business_connection_id=None):
        if business_connection_id == "silent":
            raise TelegramAPIError(method=None, message="no incoming messages in 24h")
        sent.append((chat_id, text, business_connection_id))

    async def delete_business_messages(self, business_connection_id, message_ids):
        if business_connection_id == "broken":
            raise TelegramAPIError(method=None, message="not enough rights")
        deleted.append((business_connection_id, message_ids))


notify.bot = lambda: FakeBot()


def check(name, cond, extra=""):
    results.append(bool(cond))
    print(("PASS " if cond else "FAIL ") + name + (f" · {extra}" if extra and not cond else ""))


def fake(chat_id=42, user_id=7, chat_type="private", text="", conn=None, reply=None, guest=None):
    answers, guest_answers = [], []

    async def answer(t, **kw):
        answers.append((t, kw))

    async def answer_guest_query(result):
        guest_answers.append(result.input_message_content.message_text)
    m = SimpleNamespace(chat=SimpleNamespace(id=chat_id, type=chat_type), from_user=SimpleNamespace(id=user_id, username="vitalik"),
                        text=text, business_connection_id=conn, guest_query_id=guest, message_id=5, reply_to_message=reply,
                        answer=answer, answer_guest_query=answer_guest_query)
    return m, answers, guest_answers


def cmd(command, args):
    return SimpleNamespace(command=command, args=args)


def alert():
    return sent[-1][1]


async def run():
    await init_db()
    await User(email="vasya@nure.ua", status=Status.student, last_name="Пупкін", first_name="Василь", group="ПЗПІ-25-1",
               tg_chat_id=42, tg_username="vasya_tg").insert()
    await User(email="petya@nure.ua", status=Status.student, first_name="Петро").insert()
    admin = await User(email="v@nure.ua", status=Status.admin, first_name="Віталій", tg_chat_id=7).insert()

    m, *_ = fake(conn="c1")
    check("as_admin: the teacher's own line passes with data", (await notes.as_admin(m))["admin"].email == "v@nure.ua")
    check("as_admin: a student's line does not", await notes.as_admin(fake(user_id=42)[0]) is False)
    check("guest_command: parses the command after the mention",
          notes.guest_command(SimpleNamespace(text="@python_nure_bot /note здай лабу"))["command"].args == "здай лабу")

    m, *_ = fake(conn="c1")
    await notes.note(m, cmd("hide", "здав пізно"), admin)
    n = await Note.find_one(Note.text == "здав пізно")
    check("/hide in the student's chat: saved, invisible, source private", n.user == "vasya@nure.ua" and not n.visible and n.shown == "" and n.source == "private")
    check("/hide: command taken out, alert 🙈", deleted == [("c1", [5])] and "🙈 здав пізно" in alert() and "Пупкін Василь" in alert())

    m, *_ = fake(conn="c1")
    await notes.note(m, cmd("note", "здай до пʼятниці"), admin)
    n = await Note.find_one(Note.text == "здай до пʼятниці")
    check("/note in the student's chat: sent as the teacher with 🤖, business id", sent[-2] == (42, "🤖 📝 здай до пʼятниці", "c1"))
    check("/note: shown «у вашому чаті», command taken out, alert 👁 + 📍", n.visible and n.shown == "у вашому чаті" and deleted[-1] == ("c1", [5])
          and "👁 здай до пʼятниці" in alert() and "📍 у вашому чаті" in alert())

    m, *_ = fake(conn="silent")
    await notes.note(m, cmd("note", "план Б"), admin)
    n = await Note.find_one(Note.text == "план Б")
    check("teacher-send failed, student linked: DM from the bot, signed", sent[-2] == (42, "📝 Віталій: план Б", None) and n.shown == "особисто від бота")

    m, *_ = fake(chat_id=99, conn="silent")
    await notes.note(m, cmd("note", "нікуди"), admin)
    n = await Note.find_one(Note.text == "нікуди")
    check("nowhere to show: note kept, command stays, ⚠️", n.shown == "" and n.tg_id == 99 and deleted[-1][0] == "silent" and len(deleted) == 3 and "⚠️ Не показав" in alert())

    m, *_ = fake(conn="broken")
    await notes.note(m, cmd("hide", "x"), admin)
    check("delete failed: ⚠️ line in the alert", "⚠️ Команду з чату не прибрав" in alert())

    reply = SimpleNamespace(from_user=SimpleNamespace(id=42), forum_topic_created=None, message_id=77)
    m, answers, _ = fake(chat_id=-100, chat_type="supergroup", reply=reply)
    await notes.note(m, cmd("note", "молодець"), admin)
    n = await Note.find_one(Note.text == "молодець")
    check("forum /note as a reply: bot replies to the student's message", answers[0][0] == "📝 молодець" and answers[0][1]["reply_parameters"].message_id == 77)
    check("forum: source forum, ephemeral ✔️ with 📍", n.source == "forum" and n.shown == "у форумі" and answers[1][0] == "✔️ Записав · у форумі"
          and answers[1][1]["ephemeral_message_parameters"].receiver_user_id == 7)

    topic = SimpleNamespace(from_user=SimpleNamespace(id=7), forum_topic_created=object(), message_id=1)
    m, answers, _ = fake(chat_id=-100, chat_type="supergroup", reply=topic)
    await notes.note(m, cmd("hide", "@vasya_tg без ноута"), admin)
    n = await Note.find_one(Note.text == "без ноута")
    check("forum /hide by @username: hidden, only the ephemeral ✔️", n.user == "vasya@nure.ua" and not n.visible and len(answers) == 1 and answers[0][0] == "✔️ Записав")

    m, answers, _ = fake(chat_id=-100, chat_type="supergroup", reply=topic)
    await notes.note(m, cmd("note", "vasya на пару"), admin)
    check("forum /note by nick, no reply: post mentions the student", answers[0][0] == "📝 @vasya_tg на пару")

    m, answers, _ = fake(chat_id=-100, chat_type="supergroup", reply=topic)
    await notes.note(m, cmd("note", "nobody текст"), admin)
    check("unknown nick: hint, no note", answers[0][0] == notes.HINT and await Note.find_one(Note.text == "текст") is None)

    m, answers, _ = fake(chat_id=7)
    await notes.note(m, cmd("note", "vasya здав"), admin)
    check("bot's chat /note: DM to the student, plain ✔️", sent[-2] == (42, "📝 Віталій: здав", None) and answers[0] == ("✔️ Записав · особисто від бота", {}))

    m, answers, _ = fake(chat_id=7)
    await notes.note(m, cmd("note", "petya здав"), admin)
    check("bot's chat /note, student not linked: saved, ⚠️ in the ✔️", (await Note.find_one(Note.user == "petya@nure.ua")).shown == "" and "не привʼязав" in answers[0][0])

    m, answers, guest = fake(text="@python_nure_bot /note здай лабу", guest="g1")
    await notes.note(m, notes.guest_command(m)["command"], admin)
    n = await Note.find_one(Note.text == "здай лабу")
    check("guest mention: bot answers as itself, source guest", guest == ["📝 здай лабу"] and n.source == "guest" and n.shown == "від бота у вашому чаті" and not answers)

    rights = SimpleNamespace(can_reply=True, can_read_messages=False, can_delete_sent_messages=False, can_delete_all_messages=True)
    await notes.connected(SimpleNamespace(is_enabled=True, user=SimpleNamespace(username="vitalik"), rights=rights))
    check("business_connection: alert with state and rights", "🤖 Chat Automation · підключено · @vitalik" in alert() and "can_reply, can_delete_all_messages" in alert())

    await log.deleted(SimpleNamespace(chat=SimpleNamespace(id=42, type="private"), message_ids=[5, 6]))
    check("deleted_business_messages: a row per id", await TgMessage.find(TgMessage.kind == "deleted").count() == 2)
    check("commands: note + hide registered as ephemeral", set(notes.COMMANDS) == {"note", "hide"} and "note" in notify.KINDS)

asyncio.run(run())
ok = sum(results)
print(f"\n{ok}/{len(results)} PASS")
sys.exit(0 if ok == len(results) else 1)
