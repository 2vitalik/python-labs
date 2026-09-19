"""Smoke: admin alerts + /here routing on a scratch DB, Telegram replaced by a recorder. Run from app/api:
DB_NAME=python_labs_smoke uv run python tests/smoke_notify.py"""
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

from bot import alerts, notify  # noqa: E402
from bot.here import here, is_admin  # noqa: E402
from bot.link import bind  # noqa: E402
from config import settings  # noqa: E402
from db import init_db  # noqa: E402
from models.history import record  # noqa: E402
from models.notify import Route  # noqa: E402
from models.user import Status, User  # noqa: E402

settings.tg_bot_token = "fake"
sent, results, broken = [], [], set()


class FakeBot:
    async def send_message(self, chat_id, text, message_thread_id=None):
        if chat_id in broken:
            raise TelegramAPIError(method=None, message="chat not found")
        sent.append((chat_id, message_thread_id, text))


notify.bot = lambda: FakeBot()


def check(name, cond, extra=""):
    results.append(bool(cond))
    print(("PASS " if cond else "FAIL ") + name + (f" · {extra}" if extra and not cond else ""))


def msg(chat_id, user_id, thread=None, title=None):
    """Message stand-in for /here: chat, sender, topic; replies captured."""
    replies = []

    async def answer(text):
        replies.append(text)
    m = SimpleNamespace(chat=SimpleNamespace(id=chat_id, title=title), from_user=SimpleNamespace(id=user_id),
                        is_topic_message=thread is not None, message_thread_id=thread, reply_to_message=None, answer=answer)
    return m, replies


def last():
    return sent[-1] if sent else (None, None, "")


async def run():
    await init_db()
    await User(email="v@nure.ua", status=Status.admin, tg_chat_id=1).insert()
    vasya = await User(email="vasya@nure.ua", status=Status.student, group="ПЗПІ-25-1", tg_token="tok").insert()

    ch = await record(vasya, {"last_name": "Пупкін", "first_name": "Василь", "patronymic": "Іванович",
                              "github": "https://github.com/vasya/labs"}, actor=vasya.email)
    await alerts.profile(vasya, ch)
    chat, thread, text = last()
    check("unrouted fill → admin private chat", chat == 1 and thread is None)
    check("fill text: 🟢, linked name · group, ПІБ + GitHub rows",
          text.startswith('🟢 Профіль · <b><a href="http://localhost:5030/students/vasya">Пупкін Василь</a></b> · ПЗПІ-25-1\n')
          and "🪪 ПІБ: Пупкін Василь Іванович\n" in text
          and text.endswith('🐙 GitHub: <a href="https://github.com/vasya/labs">github.com/vasya/labs</a>'), text)

    n = len(sent)
    await alerts.profile(vasya, {})
    check("no changes → no alert", len(sent) == n)

    m, replies = msg(-100, 1, thread=7, title="Labs")
    check("is_admin: by tg_chat_id + status", await is_admin(m))
    await here(m, SimpleNamespace(args="change"))
    check("/here change → confirms with the kind label",
          replies[0] == "✔️ Сюди йтимуть:\n🟠 зміни й видалення в профілі", replies[0])

    await alerts.profile(vasya, await record(vasya, {"first_name": "Вася"}, actor=vasya.email))
    chat, thread, text = last()
    check("replaced name → bound topic, 🟠, old → new",
          (chat, thread) == (-100, 7) and text.startswith("🟠") and "🪪 ПІБ: Пупкін Василь Іванович → Пупкін Вася Іванович" in text, text)

    await alerts.profile(vasya, await record(vasya, {"github": ""}, actor=vasya.email))
    chat, thread, text = last()
    check("deleted GitHub → 🔴 with ✖️",
          thread == 7 and text.startswith("🔴") and "github.com/vasya/labs</a> → ✖️" in text, text)

    await record(vasya, {"patronymic": ""}, actor="x")
    await alerts.profile(vasya, await record(vasya, {"patronymic": "Іванович"}, actor=vasya.email))
    chat, _, text = last()
    check("filled an empty name part → 🟢 private, new ПІБ only",
          chat == 1 and text.startswith("🟢") and "🪪 ПІБ: Пупкін Вася Іванович" in text and "→" not in text, text)

    await bind(vasya, 42, "vasya_tg")
    chat, _, text = last()
    check("bot linked → 🟢: Бот привʼязано + @nick link", chat == 1 and text.startswith("🟢") and "🤖 Бот: привʼязано" in text
          and '✈️ Telegram: <a href="https://t.me/vasya_tg">@vasya_tg</a>' in text, text)

    await bind(vasya, 43, "vasya_tg")
    chat, thread, text = last()
    check("re-linked from another chat → 🟠 topic: інший Telegram",
          (chat, thread) == (-100, 7) and text.startswith("🟠") and "🤖 Бот: інший Telegram" in text, text)

    await alerts.profile(vasya, await record(vasya, {"tg_chat_id": None, "tg_username": ""}, actor=vasya.email))
    text = last()[2]
    check("unlinked → 🔴: відвʼязано + @nick → ✖️",
          text.startswith("🔴") and "🤖 Бот: відвʼязано" in text and "@vasya_tg</a> → ✖️" in text, text)

    m, replies = msg(-100, 1, thread=7, title="Labs")
    await here(m, SimpleNamespace(args=None))
    check("/here status in the topic: change → тут, rest → особисто, hint",
          "🟠 зміни й видалення в профілі → тут" in replies[0] and "🟢 нові дані в профілі → <i>особисто адмінам</i>" in replies[0]
          and replies[0].endswith("☝️ /here fill · change · login · all · off"), replies[0])

    m, replies = msg(1, 1)
    await here(m, SimpleNamespace(args=""))
    check("/here status elsewhere shows the bound title", "→ <b>Labs › #7</b>" in replies[0], replies[0])
    await here(m, SimpleNamespace(args="bogus"))
    check("unknown kind → ❌ + hint", replies[-1].startswith("❌ Не знаю «bogus»\n☝️ /here"), replies[-1])

    broken.add(-100)
    await alerts.profile(vasya, await record(vasya, {"first_name": "Василь"}, actor=vasya.email))
    chat, _, text = last()
    check("undeliverable route → admin private with ⚠️ + original",
          chat == 1 and text.startswith("⚠️ Не доставив у <b>Labs › #7</b>: chat not found\n\n🟠"), text)
    broken.clear()

    await here(m, SimpleNamespace(args="all"))
    check("/here all → three kinds bound to the private chat", replies[-1].count("\n") == 3 and await Route.count() == 3)
    await here(m, SimpleNamespace(args="off"))
    check("/here off → routes gone", replies[-1] == "✔️ Сюди більше нічого не йтиме" and await Route.count() == 0)
    await here(m, SimpleNamespace(args="off"))
    check("/here off again → nothing was bound", replies[-1].startswith("☝️"))

    newbie = await User(email="new@nure.ua", name="New Person").insert()
    await alerts.signed_in(newbie)
    text = last()[2]
    check("new sign-in → 👋 + edit link + email + pending hint",
          text.startswith('👋 Новий вхід · <b><a href="http://localhost:5030/students/new/edit">New Person</a></b>\n📧 new@nure.ua\n☝️')
          and "очікує" in text, text)

    m, _ = msg(42, 42)
    check("student is not admin", not await is_admin(m))

    settings.tg_bot_token = ""
    n = len(sent)
    await alerts.signed_in(newbie)
    check("empty token → nothing sent", len(sent) == n)

asyncio.run(run())
ok = sum(results)
print(f"\n{ok}/{len(results)} PASS")
sys.exit(0 if ok == len(results) else 1)
