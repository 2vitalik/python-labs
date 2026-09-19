"""Smoke: T113 alerts — game/claim events, first sign-in, error handlers, digest — on a scratch DB. Run from app/api:
DB_NAME=python_labs_smoke uv run python tests/smoke_events.py"""
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

from bot import digest, errors, game_alerts, notify  # noqa: E402
from config import settings  # noqa: E402
from db import init_db  # noqa: E402
from models.game import Claim, Game, Part  # noqa: E402
from models.history import record  # noqa: E402
from models.rule import Rule  # noqa: E402
from models.task import Task  # noqa: E402
from models.user import Status, User  # noqa: E402
from routes.auth import upsert_user  # noqa: E402

settings.tg_bot_token = "fake"
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


async def run():
    await init_db()
    await User(email="v@nure.ua", status=Status.admin, tg_chat_id=1).insert()
    vasya = await User(email="vasya@nure.ua", status=Status.student, group="ПЗПІ-25-1",
                       last_name="Пупкін", first_name="Василь").insert()
    head = '<b><a href="http://localhost:5030/students/vasya">Пупкін Василь</a></b> · ПЗПІ-25-1'

    game = await Game(owner=vasya.email, title="Танчики", base_game="tanks").insert()
    await game_alerts.game(vasya, game)
    check("game created → 🟢 Гра + title + base", last() == f"🟢 Гра · {head}\n🏷 Танчики\n🕹 tanks", last())
    ch = await record(game, {"title": "Танки", "description": "# нове"}, actor=vasya.email)
    await game_alerts.game(vasya, game, ch)
    check("card edited → 🟠 with old → new, description filled",
          last() == f"🟠 Гра · {head}\n🏷 Назва: Танчики → Танки\n📄 Опис: # нове", last())
    ch = await record(game, {"description": "# інше"}, actor=vasya.email)
    await game_alerts.game(vasya, game, ch)
    check("description replaced → 'змінено', no dump", last().endswith("📄 Опис: змінено"), last())

    win = await Part(game=game.id, kind="window", title="Головне", task="main-window").insert()
    hero = await Part(game=game.id, kind="entity", title="Гравець", role="player").insert()
    foe = await Part(game=game.id, kind="entity", title="Ворог", role="enemy").insert()
    await game_alerts.part(vasya, win, 0)
    check("part added → 🧩 вікно «…»", last() == f"🟢 Гра · {head}\n🧩 вікно «Головне»", last())
    await game_alerts.part(vasya, foe, 2)
    check("part deleted → 🔴 … → ✖️", last() == f"🔴 Гра · {head}\n🧩 сутність «Ворог» → ✖️", last())

    rule = await Rule(game=game.id, when={"kind": "contact", "a": str(hero.id), "b": str(foe.id)},
                      then=[{"kind": "damage", "n": 3}, {"kind": "spawn", "part": str(hero.id)},
                            {"kind": "custom", "text": "бум <b>"}]).insert()
    await game_alerts.rule(vasya, rule, 0)
    check("rule added → sentence with names, effects, quoted text",
          last() == f"🟢 Гра · {head}\n📜 КОЛИ «Гравець» × «Ворог» → ТО шкода 3 · спавн «Гравець» · бум &lt;b&gt;", last())
    timer = await Rule(game=game.id, when={"kind": "timer", "every": 5}, then=[{"kind": "win"}]).insert()
    await game_alerts.rule(vasya, timer, 2)
    check("timer rule deleted", last().endswith("📜 КОЛИ кожні 5 тіків → ТО перемога 🏆 → ✖️"), last())

    await Task(slug="pause-menu", title="Меню паузи", zone="ui", subzone="menus", status="active").insert()
    claim = await Claim(game=game.id, task="pause-menu", part=str(win.id)).insert()
    await game_alerts.claim(vasya, claim, 0)
    check("claim created → 🎯 title + 🧩 part", last() == f"🟢 Заявка · {head}\n🎯 Меню паузи\n🧩 вікно «Головне»", last())
    ch = await record(claim, {"note": "готово", "link": "https://github.com/v/r/commit/1"}, actor=vasya.email)
    await game_alerts.claim(vasya, claim, 1, ch)
    check("claim edited → note + link rows",
          last().endswith("🧩 вікно «Головне»\n📝 Нотатка: готово\n🔗 Лінк: https://github.com/v/r/commit/1"), last())
    orphan = Claim(game=game.id, task="gone-card")
    await game_alerts.claim(vasya, orphan, 2)
    check("claim deleted, card gone → slug + ✖️", last() == f"🔴 Заявка · {head}\n🎯 gone-card → ✖️", last())

    tasks = BackgroundTasks()
    await upsert_user({"email": vasya.email, "name": "Vasyl P"}, tasks)
    await tasks()
    check("imported student's first sign-in → 👋 Перший вхід, no pending hint",
          last() == f"👋 Перший вхід · {head}" and (await User.get(vasya.id)).seen_at is not None, last())
    n = len(sent)
    tasks = BackgroundTasks()
    await upsert_user({"email": vasya.email, "name": "Vasyl P"}, tasks)
    await tasks()
    check("second sign-in → silent", len(sent) == n)
    tasks = BackgroundTasks()
    await upsert_user({"email": "who@nure.ua", "name": "Who Dis"}, tasks)
    await tasks()
    check("unknown sign-in → pending hint + edit link", "students/who/edit" in last() and "очікує" in last(), last())

    try:
        raise ValueError("boom\nsecond line")
    except ValueError as e:
        exc = e
    req = SimpleNamespace(method="PUT", url=SimpleNamespace(path="/api/x"), scope={"session": {"email": vasya.email}})
    resp = await errors.api_handler(req, exc)
    await resp.background()
    check("API error → 500 + 💥 head with nick, ❗ first line, 📍 our frame",
          resp.status_code == 500
          and last().startswith("💥 API · PUT /api/x · vasya\n❗ ValueError: boom\n📍 tests/smoke_events.py:"), last())
    ev = SimpleNamespace(update=SimpleNamespace(update_id=7, event_type="message",
                                                message=SimpleNamespace(from_user=SimpleNamespace(username="vasya_tg"))), exception=exc)
    check("bot error → handled, 💥 Бот · message · @nick",
          await errors.bot_handler(ev) is True and last().startswith("💥 Бот · message · @vasya_tg\n❗ ValueError: boom"), last())

    await User(email="full@nure.ua", status=Status.student, group="ПЗПІ-25-2", last_name="A", first_name="B",
               github="https://github.com/a/b", tg_chat_id=5).insert()
    await User(email="lazy@nure.ua", status=Status.student, group="ПЗПІ-25-2").insert()
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
