"""Smoke: T113 alerts of the python site — game/claim events, ideas (T270) — on a scratch DB; the platform's alerts —
core/api/tests/smoke_events.py. Run from app/api: DB_NAME=python_labs_events_smoke ~/.venvs/python-labs/bin/python tests/smoke_events.py"""
import asyncio
import os
import sys

sys.path.insert(0, os.getcwd())
from pymongo import MongoClient  # noqa: E402

DB = os.environ["DB_NAME"]
assert DB.endswith("_smoke"), "refuse to run on a non-smoke DB"
MongoClient().drop_database(DB)

from bot import game_alerts  # noqa: E402
from core.bot import notify  # noqa: E402
from core.config import settings  # noqa: E402
from core.models.history import record  # noqa: E402
from core.models.user import Status, User  # noqa: E402
from db import init_db  # noqa: E402
from models.game import Claim, Game, Part  # noqa: E402
from models.ref import Ref  # noqa: E402
from models.rule import Rule  # noqa: E402
from models.task import Task  # noqa: E402

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
                      cond=[{"kind": "state", "a": "@a", "s": "щит", "not": True}],
                      then=[{"kind": "damage", "a": "@b", "n": 3}, {"kind": "spawn", "entity": str(hero.id)},
                            {"kind": "custom", "text": "бум <b>"}]).insert()
    await game_alerts.rule(vasya, rule, 0)
    check("rule added → sentence with names, condition, effects, quoted text",
          last() == f"🟢 Гра · {head}\n📜 КОЛИ «Гравець» × «Ворог» → ЯКЩО «Гравець» не у стані «щит» → ТО «Ворог» отримує шкоду 3 · зʼявляється «Гравець» · бум &lt;b&gt;", last())
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
    await game_alerts.claim(vasya, await Claim(game=game.id, task="pause-menu", rule=str(rule.id)).insert(), 0)
    check("claim on a rule → the rule's sentence", last() == f"🟢 Заявка · {head}\n🎯 Меню паузи\n📜 КОЛИ «Гравець» × «Ворог» → ЯКЩО "
          "«Гравець» не у стані «щит» → ТО «Ворог» отримує шкоду 3 · зʼявляється «Гравець» · бум &lt;b&gt;", last())
    await game_alerts.part(vasya, await Part(game=game.id, kind="level", title="Печери").insert(), 0)
    check("level added → 🧩 рівень «…»", last() == f"🟢 Гра · {head}\n🧩 рівень «Печери»", last())
    await game_alerts.idea(vasya, Ref(author=vasya.email, kind="idea", title="Тип вікна «Мапа»", note="нема <такого>"))
    check("idea → 💡 title + 💬 note", last() == f"🟢 Ідея · {head}\n💡 Тип вікна «Мапа»\n💬 нема &lt;такого&gt;", last())

asyncio.run(run())
ok = sum(results)
print(f"\n{ok}/{len(results)} PASS")
sys.exit(0 if ok == len(results) else 1)
