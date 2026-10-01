"""Smoke: «Мій тиждень» (T179) — the grid, marks put in order, «Готово» that asks for reasons, the alert, the history, the teacher's list.
Run from app/api: DB_NAME=python_labs_smoke uv run python tests/smoke_week.py"""
import os
import sys

sys.path.insert(0, os.getcwd())
from pymongo import MongoClient  # noqa: E402

DB = os.environ["DB_NAME"]
assert DB.endswith("_smoke"), "refuse to run on a non-smoke DB"
MongoClient().drop_database(DB)
db = MongoClient()[DB]
from fastapi.testclient import TestClient  # noqa: E402

import main  # noqa: E402
from core.bot import notify  # noqa: E402
from core.config import settings  # noqa: E402

ADMIN, VASYA, PETRO, TEST = "admin@nure.ua", "vasya@nure.ua", "petro@nure.ua", "test.student@nure.ua"
settings.admin_emails, settings.tg_bot_token = ADMIN, "fake"
sent, results = [], []
db.users.insert_many([
    {"email": VASYA, "status": "student", "group": "ПЗПІ-25-1", "last_name": "Пупкін", "first_name": "Василь", "tg_username": "vasya_tg"},
    {"email": PETRO, "status": "student", "group": "ПЗПІ-25-2", "last_name": "Петренко", "first_name": "Петро"},
    {"email": TEST, "status": "student", "group": "TEST", "test": True},
    {"email": ADMIN, "status": "admin", "tg_chat_id": 1},
])


class FakeBot:
    async def send_message(self, chat_id, text, message_thread_id=None):
        sent.append(text)


notify.bot = lambda: FakeBot()


def check(name, cond, extra=""):
    results.append(bool(cond))
    print(("PASS " if cond else "FAIL ") + name + (f" · {extra}" if extra and not cond else ""))


def sign_in(c, email):
    settings.fake_user_email = email
    c.get("/api/auth/dev-login", follow_redirects=False)


def minutes(clock):
    h, m = clock.split(":")
    return int(h) * 60 + int(m)


def mark(day, start, end, kind="no", why=""):
    return {"day": day, "start": minutes(start), "end": minutes(end), "kind": kind, "why": why}


def put(c, marks, **more):
    return c.put("/api/my/week", json={"marks": marks, **more})


def alerts():
    return [t for t in sent if t.startswith("🗓")]


GYM = "🏋️ тренування"
with TestClient(main.app) as c:
    check("guest: reading → 401, saving → 401", c.get("/api/my/week").status_code == put(c, []).status_code == 401)

    sign_in(c, VASYA)
    w = c.get("/api/my/week").json()
    check("a new week: the grid Mon–Sat 15:00–23:00 by 15 minutes", w["frame"] == {"days": 6, "from": 900, "to": 1380, "step": 15}, w)
    check("a new week: nothing marked, nothing saved", (w["marks"], w["comment"], w["done_at"], w["updated_at"]) == ([], "", None, None)
          and db.weeks.count_documents({}) == 0, w)
    settings.week_hours, settings.week_days = "8-20", 7
    check("the grid is the site's setting", c.get("/api/my/week").json()["frame"] == {"days": 7, "from": 480, "to": 1200, "step": 15})
    settings.week_hours, settings.week_days = "15-23", 6

    r = put(c, [mark(3, "18:45", "19:30", why=f"  {GYM} "), mark(1, "18:00", "19:30", why=GYM), mark(3, "18:00", "18:45", why=GYM)])
    check("neighbours of one kind and reason become one mark, days in order, the reason trimmed",
          r.json()["marks"] == [mark(1, "18:00", "19:30", why=GYM), mark(3, "18:00", "19:30", why=GYM)], r.text)
    r = put(c, [mark(0, "15:00", "16:30", why="🏫 пара за розкладом"), mark(0, "16:30", "17:15", why="🚌 дорога"), mark(0, "17:15", "18:00", "meh")])
    check("neighbours with different reasons or kinds stay apart", len(r.json()["marks"]) == 3, r.text)
    r = put(c, [mark(2, "20:00", "22:00", "ok", why="бо так")])
    check("a reason is kept only for «не можу»", r.json()["marks"] == [mark(2, "20:00", "22:00", "ok")], r.text)
    kept = r.json()["marks"]

    check("off the step → 422", put(c, [mark(0, "15:05", "16:00")]).status_code == 422)
    check("outside the grid → 422: too early, too late, Sunday, empty",
          {put(c, [m]).status_code for m in (mark(0, "14:00", "16:00"), mark(0, "22:00", "23:15"), mark(6, "15:00", "16:00"), mark(0, "16:00", "16:00"))} == {422})
    r = put(c, [mark(0, "18:00", "19:30"), mark(0, "19:00", "20:00", "meh")])
    check("one mark over another → 422, both named", r.status_code == 422 and r.json()["detail"] == "Позначки перетинаються: Пн 18:00–19:30 і Пн 19:00–20:00", r.text)
    check("an unknown kind → 422", put(c, [mark(0, "18:00", "19:30", "maybe")]).status_code == 422)
    slots = [(d, 900 + 15 * i) for d in range(6) for i in range(32)][:101]
    many = [{"day": d, "start": s, "end": s + 15, "kind": "ok" if i % 2 else "meh", "why": ""} for i, (d, s) in enumerate(slots)]
    check("101 marks → 422, 100 are fine", put(c, many).status_code == 422 and put(c, many[:100]).status_code == 200)
    check("a reason over 200 characters → 422, a comment over 1000 → 422",
          put(c, [mark(0, "18:00", "19:30", why="x" * 201)]).status_code == put(c, [], comment="x" * 1001).status_code == 422)
    put(c, kept)
    check("a refused save changes nothing", c.get("/api/my/week").json()["marks"] == kept)

    week = [mark(1, "18:00", "19:30"), mark(3, "18:00", "19:30", why=GYM), mark(0, "21:00", "23:00", "meh"), mark(5, "15:00", "18:00", "ok")]
    r = put(c, week, done=True)
    check("«Готово» with an unexplained «не можу» → 422 that names it", r.status_code == 422 and r.json()["detail"] == "Поясни червоні слоти: Вт 18:00–19:30", r.text)
    check("…and nothing is saved or sent", c.get("/api/my/week").json()["marks"] == kept and not alerts() and db.weeks.find_one({"user": VASYA})["done_at"] is None)
    r = put(c, week)
    check("the same week without «Готово» is saved as a draft", r.status_code == 200 and r.json()["done_at"] is None and len(r.json()["marks"]) == 4, r.text)

    week[0]["why"] = GYM
    r = put(c, week, comment=" можу лише онлайн ", done=True)
    w = r.json()
    check("«Готово» with every reason given → done, with the time", r.status_code == 200 and w["done_at"] and w["done_at"].endswith("+00:00")
          and w["comment"] == "можу лише онлайн", r.text)
    text = alerts()[0] if alerts() else ""
    check("one alert: who, a line per reason with days that share hours, 🟡 and 🟢, the comment",
          len(alerts()) == 1 and "Пупкін Василь" in text and "ПЗПІ-25-1" in text and f"🔴 {GYM}: Вт, Чт 18:00–19:30" in text
          and "🟡 Пн 21:00–23:00" in text and "🟢 Сб 15:00–18:00" in text and "💬 можу лише онлайн" in text, text)
    ev = db.events.find_one({"kind": "week"})
    check("the alert is an event `week` about the student, with a link to /week", ev and ev["user"] == VASYA and ev["sent"] and "/week\">Тиждень</a>" in ev["text"], ev)

    done_at, rows = w["done_at"], db.history.count_documents({"coll": "weeks"})
    w = put(c, week, comment="можу лише онлайн, з телефона").json()
    last = db.history.find_one({"coll": "weeks"}, sort=[("at", -1)])
    check("a later change: saved, still done, no second alert", w["done_at"] == done_at and len(alerts()) == 1 and w["updated_at"] > done_at, w)
    check("…and it is one row of the history: who, what, the marks counted", db.history.count_documents({"coll": "weeks"}) == rows + 1
          and last["actor"] == VASYA and list(last["changes"]) == ["comment"] and last["note"] == "🔴 2 · 🟡 1 · 🟢 1", last)
    again = put(c, week, comment="можу лише онлайн, з телефона").json()
    check("the same week saved again: no row, the time stays", db.history.count_documents({"coll": "weeks"}) == rows + 1 and again["updated_at"] == w["updated_at"])
    week.append(mark(4, "15:00", "16:00"))
    w = put(c, week, comment="можу лише онлайн, з телефона").json()
    check("after «Готово» an unexplained «не можу» is kept, the week stays done", len(w["marks"]) == 5 and w["done_at"] == done_at and len(alerts()) == 1, w)
    check("the week is one document a person", db.weeks.count_documents({}) == 1)
    check("student: the teacher's list → 403", c.get("/api/weeks").status_code == 403)
    check("saving is in the footprint", db.activity.count_documents({"user": VASYA, "method": "PUT", "path": "/api/my/week", "status": 200}) > 5)

    sign_in(c, PETRO)
    r = put(c, [], done=True)
    check("an empty week can be done: «може будь-коли»", r.json()["done_at"] and len(alerts()) == 2 and "✅ може будь-коли" in alerts()[1], alerts()[-1])

    sign_in(c, ADMIN)
    data = c.get("/api/weeks").json()
    by = {s["nick"]: s for s in data["students"]}
    check("teacher: every student but the test one, no staff; the grid", sorted(by) == ["petro", "vasya"] and data["frame"]["days"] == 6, sorted(by))
    check("teacher: a student's week with reasons, the Telegram nick, the group", len(by["vasya"]["week"]["marks"]) == 5
          and by["vasya"]["week"]["marks"][1]["why"] == GYM and by["vasya"]["tg_username"] == "vasya_tg" and by["vasya"]["group"] == "ПЗПІ-25-1", by["vasya"])
    check("teacher: no week of their own yet", data["me"] is None)
    put(c, [mark(0, "15:00", "18:00", why="🏫 пара за розкладом")])
    me = c.get("/api/weeks").json()["me"]
    check("teacher: their own week comes as `me`", me and me["marks"][0]["why"] == "🏫 пара за розкладом", me)
    check("teacher: reading the list leaves no footprint", db.activity.count_documents({"path": "/api/weeks"}) == 0)
    rows = c.get("/api/activity", params={"src": "edit", "user": "vasya"}).json()["rows"]
    first = [r for r in rows if r["coll"] == "weeks"][-1]
    check("activity: the student's saves are edits of `weeks`, the marks in words",
          first["note"] == "🔴 2" and first["changes"] == [{"field": "marks", "old": "", "new": f"🔴 Вт, Чт 18:00–19:30 — {GYM}"}], first)

    c.post("/api/me/as/petro")
    r = put(c, [mark(0, "18:00", "19:30", "meh")])
    check("«Очима студента»: their week is shown, saving → 403", c.get("/api/my/week").json()["done_at"]
          and r.status_code == 403 and r.json()["detail"].startswith("Лише перегляд"), r.text)
    check("…and the week is as it was", db.weeks.find_one({"user": PETRO})["marks"] == [])
    c.delete("/api/me/as")
    check("`week` is a kind of alerts: /here and /mute know it", "week" in notify.KINDS)

ok = sum(results)
print(f"\n{ok}/{len(results)} PASS")
sys.exit(0 if ok == len(results) else 1)
