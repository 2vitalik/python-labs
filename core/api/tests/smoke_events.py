"""Smoke: T113 alerts — first sign-in, error handlers, digest — on a scratch DB; the python site's game alerts — app/api/tests.
Run from a site's api folder:
DB_NAME=<db>_smoke ~/.venvs/python-labs/bin/python <repo>/core/api/tests/smoke_events.py"""
import asyncio
import os
import sys
from types import SimpleNamespace

sys.path.insert(0, os.getcwd())
from pymongo import MongoClient  # noqa: E402

DB = os.environ["DB_NAME"]
assert DB.endswith("_smoke"), "refuse to run on a non-smoke DB"
MongoClient().drop_database(DB)
from starlette.background import BackgroundTasks  # noqa: E402

from core.bot import digest, errors, notify  # noqa: E402
from core.config import settings  # noqa: E402
from core.models.user import Status, User  # noqa: E402
from core.routes.auth import upsert_user  # noqa: E402
from db import init_db  # noqa: E402

settings.tg_bot_token = "fake"
settings.site_url = "http://localhost:5030"  # not the one from .env
sent, results = [], []


class FakeBot:
    async def send_message(self, chat_id, text, message_thread_id=None):
        sent.append((chat_id, text))


notify.bot = lambda: FakeBot()


def check(name, cond, extra=""):
    results.append(bool(cond))
    print(("PASS " if cond else "FAIL ") + name + (f" · {extra}" if extra and not cond else ""))


def last():
    return sent[-1][1] if sent else ""


browser = SimpleNamespace(headers={"user-agent": "smoke"}, client=None)  # what upsert_user reads from a request


async def run():
    await init_db()
    await User(email="v@nure.ua", status=Status.admin, tg_chat_id=1).insert()
    vasya = await User(email="vasya@nure.ua", status=Status.student, group="ПЗПІ-25-1",
                       last_name="Пупкін", first_name="Василь").insert()
    head = '<b><a href="http://localhost:5030/students/vasya">Пупкін Василь</a></b> · ПЗПІ-25-1'

    tasks = BackgroundTasks()
    await upsert_user({"email": vasya.email, "name": "Vasyl P"}, tasks, browser)
    await tasks()
    check("imported student's first sign-in → 👋 Перший вхід, no pending hint",
          last() == f"👋 Перший вхід · {head}" and (await User.get(vasya.id)).first_seen_at is not None, last())
    n = len(sent)
    tasks = BackgroundTasks()
    await upsert_user({"email": vasya.email, "name": "Vasyl P"}, tasks, browser)
    await tasks()
    check("second sign-in → silent", len(sent) == n)
    tasks = BackgroundTasks()
    await upsert_user({"email": "who@nure.ua", "name": "Who Dis"}, tasks, browser)
    await tasks()
    check("unknown sign-in → pending hint + edit link", "students/who/edit" in last() and "очікує" in last(), last())

    try:
        raise ValueError("boom\nsecond line")
    except ValueError as e:
        exc = e
    req = SimpleNamespace(method="PUT", url=SimpleNamespace(path="/api/x", query=""), scope={"session": {"email": vasya.email}},
                          headers={}, client=None)
    resp = await errors.api_handler(req, exc)
    await resp.background()
    check("API error → 500 + 💥 head with nick, ❗ first line, 📍 our frame",
          resp.status_code == 500
          and last().startswith("💥 API · PUT /api/x · vasya\n❗ ValueError: boom\n📍 ") and "tests/smoke_events.py:" in last(), last())
    ev = SimpleNamespace(update=SimpleNamespace(update_id=7, event_type="message",
                                                message=SimpleNamespace(from_user=SimpleNamespace(id=42, username="vasya_tg"))), exception=exc)
    check("bot error → handled, 💥 Бот · message · @nick",
          await errors.bot_handler(ev) is True and last().startswith("💥 Бот · message · @vasya_tg\n❗ ValueError: boom"), last())

    await User(email="full@nure.ua", status=Status.student, group="ПЗПІ-25-2", last_name="A", first_name="B",
               github="https://github.com/a/b", tg_chat_id=5).insert()
    await User(email="lazy@nure.ua", status=Status.student, group="ПЗПІ-25-2").insert()
    await User(email="test.student@nure.ua", status=Status.student, group="TEST", test=True).insert()  # not counted
    text = await digest.text()
    check("digest: counts per group, complete group hides its zeros",
          text == "📊 Профілі не заповнені · студентів: 3\n👥 ПЗПІ-25-1 · 🐙 1 · 🤖 1\n👥 ПЗПІ-25-2 · 🪪 1 · 🐙 1 · 🤖 1"
          "\n☝️ 🪪 ПІБ · 🐙 GitHub · 🤖 бот", text)
    await User.find(User.status == Status.student).delete()
    check("digest: nobody missing → None", await digest.text() is None)
    check("digest: next 09:00 within a day", 0 < digest.seconds_until(9) <= 86400)

asyncio.run(run())
ok = sum(results)
print(f"\n{ok}/{len(results)} PASS")
sys.exit(0 if ok == len(results) else 1)
