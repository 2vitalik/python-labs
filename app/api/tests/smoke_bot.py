"""Smoke: bot /start handlers on a scratch DB, no Telegram needed. Run from app/api:
DB_NAME=python_labs_smoke uv run python tests/smoke_bot.py"""
import asyncio
import os
import sys
from types import SimpleNamespace

sys.path.insert(0, os.getcwd())
from pymongo import MongoClient  # noqa: E402

DB = os.environ["DB_NAME"]
assert DB.endswith("_smoke"), "refuse to run on a non-smoke DB"
mongo = MongoClient()
mongo.drop_database(DB)
from bot.start import fallback, start, start_link, sync_username  # noqa: E402
from db import init_db  # noqa: E402
from models.user import Status, User  # noqa: E402

results = []


def check(name, cond, extra=""):
    results.append((name, bool(cond)))
    print(("PASS " if cond else "FAIL ") + name + (f" · {extra}" if extra and not cond else ""))


def fake(chat_id=42, username="vasya_tg"):
    """Message stand-in: only what handlers touch, replies captured."""
    replies = []

    async def answer(text):
        replies.append(text)
    msg = SimpleNamespace(chat=SimpleNamespace(id=chat_id), from_user=SimpleNamespace(username=username), answer=answer)
    return msg, replies


async def run():
    await init_db()
    user = await User(email="vasya@nure.ua", status=Status.student, first_name="Вася",
                      tg_token="tok123", tg_username="typed").insert()

    msg, replies = fake()
    await start(msg)
    check("/start: hint to profile", "профіль" in replies[0])

    msg, replies = fake()
    await start_link(msg, SimpleNamespace(args="nope"))
    check("unknown token: hint, nothing saved", "профіль" in replies[0] and (await User.get(user.id)).tg_chat_id is None)

    msg, replies = fake()
    await start_link(msg, SimpleNamespace(args="tok123"))
    u = await User.get(user.id)
    check("known token: greets by first name", replies[0].startswith("Привіт, Вася"), replies[0])
    check("chat_id + real username saved", u.tg_chat_id == 42 and u.tg_username == "vasya_tg")
    check("history recorded by tgbot", mongo[DB].history.count_documents({"actor": "tgbot", "changes.tg_chat_id.new": 42}) == 1)

    msg, replies = fake(chat_id=43, username="")
    await start_link(msg, SimpleNamespace(args="tok123"))
    u = await User.get(user.id)
    check("re-link: new chat_id, username kept", u.tg_chat_id == 43 and u.tg_username == "vasya_tg")

    msg, replies = fake(chat_id=43, username="vasya_new")
    await sync_username(lambda m, _: fallback(m), msg, {})
    u = await User.get(user.id)
    check("any message: username change tracked", u.tg_username == "vasya_new" and "/start" in replies[0])

    msg, replies = fake(chat_id=99)
    await sync_username(lambda m, _: fallback(m), msg, {})
    check("unlinked chat: nothing touched, /start hint", "/start" in replies[0]
          and mongo[DB].users.count_documents({"tg_username": "vasya_tg"}) == 0)


asyncio.run(run())
ok = sum(1 for _, p in results if p)
print(f"\n{ok}/{len(results)} PASS")
sys.exit(0 if ok == len(results) else 1)
