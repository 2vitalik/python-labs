"""Smoke: message log — incoming middleware, edited handler, outgoing session middleware. Run from app/api:
DB_NAME=python_labs_smoke uv run python tests/smoke_log.py"""
import asyncio
import os
import sys
from datetime import datetime, timezone
from itertools import count

sys.path.insert(0, os.getcwd())
from pymongo import MongoClient  # noqa: E402

DB = os.environ["DB_NAME"]
assert DB.endswith("_smoke"), "refuse to run on a non-smoke DB"
MongoClient().drop_database(DB)
from aiogram.methods import SendChatAction, SendMessage  # noqa: E402
from aiogram.types import (Chat, ChatJoinRequest, ChatMemberLeft, ChatMemberMember, ChatMemberUpdated, Message,  # noqa: E402
                           MessageReactionUpdated, PhotoSize, ReactionTypeEmoji)
from aiogram.types import User as TgUser  # noqa: E402

from bot import log, notify  # noqa: E402
from config import settings  # noqa: E402
from db import init_db  # noqa: E402
from models.message import TgMessage  # noqa: E402
from models.user import Status, User  # noqa: E402

NOW = datetime(2026, 9, 24, 12, 0, tzinfo=timezone.utc)
results, handled, ids = [], [], count(10)


def check(name, cond, extra=""):
    results.append(bool(cond))
    print(("PASS " if cond else "FAIL ") + name + (f" · {extra}" if extra and not cond else ""))


def msg(chat_id=42, user_id=42, chat_type="private", text="hi", message_id=1, **extra):
    return Message(message_id=message_id, date=NOW, chat=Chat(id=chat_id, type=chat_type), text=text,
                   from_user=TgUser(id=user_id, is_bot=False, first_name="Вася", username="vasya_tg"), **extra)


async def handler(message, data):
    handled.append(message.message_id)
    return "ok"


async def make_request(bot, method):
    """Telegram stand-in: SendMessage → the Message it would return."""
    if not isinstance(method, SendMessage):
        return True
    return Message(message_id=next(ids), date=NOW, chat=Chat(id=method.chat_id, type="private"), text=method.text,
                   message_thread_id=method.message_thread_id, from_user=TgUser(id=1, is_bot=True, first_name="bot"))


class FakeBot:
    async def send_message(self, chat_id, text, message_thread_id=None):
        await notify.outgoing(make_request, None, SendMessage(chat_id=chat_id, text=text, message_thread_id=message_thread_id))


async def run():
    await init_db()
    await User(email="vasya@nure.ua", status=Status.student, tg_chat_id=42).insert()
    await User(email="admin@nure.ua", status=Status.admin, tg_chat_id=7).insert()

    r = await log.incoming(handler, msg(text="/start"), {})
    row = await TgMessage.find_one(TgMessage.message_id == 1)
    check("incoming: saved with the linked user's email, handler ran", r == "ok" and handled == [1] and row.dir == "in"
          and row.user == "vasya@nure.ua" and row.text == "/start" and row.content_type == "text" and row.at.replace(tzinfo=timezone.utc) == NOW)

    await log.incoming(handler, msg(chat_id=99, user_id=99, message_id=2), {})
    row = await TgMessage.find_one(TgMessage.message_id == 2)
    check("stranger: saved without email, with tg id + username", row.user == "" and row.from_id == 99 and row.username == "vasya_tg")

    sizes = [PhotoSize(file_id="small", file_unique_id="a", width=1, height=1), PhotoSize(file_id="big", file_unique_id="b", width=9, height=9)]
    await log.incoming(handler, msg(message_id=3, text=None, caption="скрін", photo=sizes), {})
    row = await TgMessage.find_one(TgMessage.message_id == 3)
    check("photo: caption as text, biggest file_id", row.text == "скрін" and row.content_type == "photo" and row.file_id == "big")

    await log.incoming(handler, msg(chat_id=-100, chat_type="supergroup", message_id=4, message_thread_id=5, is_topic_message=True), {})
    row = await TgMessage.find_one(TgMessage.message_id == 4)
    check("forum topic: chat_type + thread_id, sender still linked", row.chat_type == "supergroup" and row.thread_id == 5 and row.user == "vasya@nure.ua")

    await log.incoming(handler, msg(chat_id=42, user_id=7, message_id=5, text="привіт", business_connection_id="conn"), {})
    row = await TgMessage.find_one(TgMessage.message_id == 5)
    check("Chat Automation: chat_type=business, chat is the student, sender the teacher",
          row.chat_type == "business" and row.chat_id == 42 and row.from_id == 7 and row.user == "admin@nure.ua")

    check("incoming keeps the raw Telegram object", row.raw.get("text") == "привіт" and row.raw.get("business_connection_id") == "conn")

    vasya = TgUser(id=42, is_bot=False, first_name="Вася", username="vasya_tg")
    forum = Chat(id=-100, type="supergroup")
    await log.member(ChatMemberUpdated(chat=forum, from_user=vasya, date=NOW, old_chat_member=ChatMemberLeft(user=vasya),
                                       new_chat_member=ChatMemberMember(user=vasya)))
    row = await TgMessage.find_one(TgMessage.kind == "member")
    check("forum join: kind=member, 'left → member', linked user, raw", row.text == "left → member" and row.from_id == 42
          and row.user == "vasya@nure.ua" and row.content_type == "chat_member" and row.raw["new_chat_member"]["status"] == "member")

    await log.join_request(ChatJoinRequest(chat=forum, from_user=vasya, user_chat_id=42, date=NOW, bio="ПЗПІ-25-1"))
    row = await TgMessage.find_one(TgMessage.content_type == "join_request")
    check("join request: kind=member, bio as text", row.kind == "member" and row.text == "ПЗПІ-25-1" and row.from_id == 42)

    await log.reaction(MessageReactionUpdated(chat=forum, message_id=4, date=NOW, user=vasya, old_reaction=[],
                                              new_reaction=[ReactionTypeEmoji(emoji="👍"), ReactionTypeEmoji(emoji="🔥")]))
    row = await TgMessage.find_one(TgMessage.kind == "reaction")
    check("reaction: kind=reaction on message 4, emojis as text, linked user", row.message_id == 4 and row.text == "👍 🔥" and row.user == "vasya@nure.ua")

    await log.reaction(MessageReactionUpdated(chat=forum, message_id=4, date=NOW, user=vasya, old_reaction=[ReactionTypeEmoji(emoji="👍")], new_reaction=[]))
    check("reaction removed: second row with empty text", await TgMessage.find(TgMessage.kind == "reaction", TgMessage.text == "").count() == 1)

    await log.edited(msg(text="/start edited", edit_date=int(NOW.timestamp())))
    check("edited: second row for the same message_id, kind=edit",
          await TgMessage.find(TgMessage.message_id == 1, TgMessage.kind == "edit").count() == 1)

    await notify.outgoing(make_request, None, SendMessage(chat_id=42, text="👋 Привіт"))
    row = await TgMessage.find_one(TgMessage.text == "👋 Привіт")
    check("outgoing reply: dir=out, kind=reply, email of the chat's user, no from_id, no raw",
          row.dir == "out" and row.kind == "reply" and row.user == "vasya@nure.ua" and row.from_id is None and row.message_id == 10 and row.raw == {})

    settings.tg_bot_token = "fake"
    notify.bot = lambda: FakeBot()
    await notify.send("change", "🟠 Профіль")
    row = await TgMessage.find_one(TgMessage.text == "🟠 Профіль")
    check("alert via send(): kind=change, delivered to the admin's chat", row.kind == "change" and row.chat_id == 7 and row.user == "admin@nure.ua")
    check("kind resets after send()", notify.kind_var.get() == "reply")

    await notify.outgoing(make_request, None, SendChatAction(chat_id=42, action="typing"))
    check("non-message request: not logged", await TgMessage.count() == 12)

asyncio.run(run())
ok = sum(results)
print(f"\n{ok}/{len(results)} PASS")
sys.exit(0 if ok == len(results) else 1)
