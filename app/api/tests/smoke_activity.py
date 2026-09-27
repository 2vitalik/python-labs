"""Smoke: the activity page (T146) — `events` journal, the 500 row, the merged feed, the people summary. Run from app/api:
DB_NAME=python_labs_smoke uv run python tests/smoke_activity.py"""
import os
import sys
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.getcwd())
from bson import ObjectId  # noqa: E402
from pymongo import MongoClient  # noqa: E402

DB = os.environ["DB_NAME"]
assert DB.endswith("_smoke"), "refuse to run on a non-smoke DB"
MongoClient().drop_database(DB)
db = MongoClient()[DB]
from aiogram.exceptions import TelegramAPIError  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

import main  # noqa: E402
from activity_people import TZ  # noqa: E402
from bot import notify  # noqa: E402
from config import settings  # noqa: E402

ADMIN, VASYA, PETRO = "admin@nure.ua", "vasya@nure.ua", "petro@nure.ua"
settings.admin_emails, settings.tg_bot_token = ADMIN, "fake"
sent, results, broken = [], [], []
now = datetime.now(timezone.utc)


class FakeBot:
    async def send_message(self, chat_id, text, message_thread_id=None):
        if broken:
            raise TelegramAPIError(method=None, message="chat not found")
        sent.append(text)


notify.bot = lambda: FakeBot()


@main.app.get("/api/boom")
async def boom():
    raise RuntimeError("boom")


def check(name, cond, extra=""):
    results.append(bool(cond))
    print(("PASS " if cond else "FAIL ") + name + (f" · {extra}" if extra and not cond else ""))


def ago(**delta):
    return now - timedelta(**delta)


def tg(text, at, user="", chat_id=42, from_id=42, **extra):
    return {"dir": "in", "chat_id": chat_id, "chat_type": "private", "from_id": from_id, "username": "", "user": user, "text": text,
            "content_type": "text", "kind": "", "raw": {"text": text}, "at": at} | extra


vasya = db.users.insert_one({"email": VASYA, "status": "student", "group": "ПЗПІ-25-1", "last_name": "Пупкін", "first_name": "Василь",
                             "tg_chat_id": 42}).inserted_id
db.users.insert_one({"email": PETRO, "status": "student", "group": "ПЗПІ-25-1"})  # imported, never showed up
db.users.insert_one({"email": ADMIN, "status": "admin", "tg_chat_id": 1})
db.activity.insert_many([{"user": VASYA, "kind": "view", "path": "/old", "at": ago(days=3)} for _ in range(2)])
db.messages.insert_many([
    tg("привіт", ago(minutes=9), VASYA, username="vasya_tg"),
    tg("далі буде", ago(minutes=8), VASYA, dir="out", from_id=None, kind="reply"),
    tg("🟢 Профіль", ago(minutes=7), ADMIN, chat_id=1, dir="out", from_id=None, kind="fill"),  # a sent alert
    tg("здай лабу", ago(minutes=6), ADMIN, from_id=1, chat_type="business"),  # the teacher in the student's chat
    tg("хто тут", ago(minutes=5), chat_id=99, from_id=99, username="stranger"),
])
db.notes.insert_one({"user": VASYA, "tg_id": 42, "text": "сильний", "by": ADMIN, "hidden": False, "source": "forum", "at": ago(minutes=4)})
db.history.insert_many([
    {"coll": "users", "doc_id": vasya, "actor": ADMIN, "changes": {"group": {"old": None, "new": "ПЗПІ-25-1"}}, "note": "", "at": ago(hours=1)},
    {"coll": "guide", "doc_id": ObjectId(), "actor": "seed", "changes": {"body": {"old": None, "new": "x" * 500}}, "note": "", "at": ago(days=5)},
])


def sign_in(c, email):
    settings.fake_user_email = email
    c.get("/api/auth/dev-login", follow_redirects=False)


def feed(c, **params):
    return c.get("/api/activity", params=params).json()


def has(rows, **want):
    return [r for r in rows if all(r.get(k) == v for k, v in want.items())]


with TestClient(main.app, raise_server_exceptions=False) as c:
    check("guest: feed → 401", c.get("/api/activity").status_code == 401)
    sign_in(c, VASYA)
    check("student: feed → 403, people → 403", c.get("/api/activity").status_code == c.get("/api/activity/people").status_code == 403)
    c.post("/api/me/view", json={"path": "/my/profile"})
    c.put("/api/profile", json={"last_name": "Пупкін", "first_name": "Василь", "github": "https://github.com/vasya/labs"})
    check("crash: the client gets 500", c.get("/api/boom").status_code == 500)
    check("crash: `activity` row with status 500", db.activity.count_documents({"user": VASYA, "path": "/api/boom", "status": 500}) == 1)
    ev = db.events.find_one({"kind": "error"})
    check("crash: event `error` about the student, delivered", ev and ev["user"] == VASYA and ev["sent"] and "RuntimeError" in ev["text"], ev)
    ev = db.events.find_one({"kind": "login"})
    check("first sign-in: event `login`, the same text Telegram got", ev and ev["user"] == VASYA and ev["sent"] and ev["text"] in sent, ev)

    n = len(sent)
    db.routes.insert_one({"kind": "game", "chat_id": notify.MUTED, "title": ""})
    c.portal.call(notify.send, "game", "🧩 muted", VASYA)
    broken.append(True)
    c.portal.call(notify.send, "claim", "🎯 undelivered", VASYA)
    broken.clear()
    settings.tg_bot_token = ""
    c.portal.call(notify.send, "digest", "📊 no token")
    settings.tg_bot_token = "fake"
    kept = {e["text"]: e["sent"] for e in db.events.find({"kind": {"$in": ["game", "claim", "digest"]}})}
    check("muted kind, Telegram failure, empty token: nothing sent, all three kept with sent=False",
          len(sent) == n and kept == {"🧩 muted": False, "🎯 undelivered": False, "📊 no token": False}, kept)

    sign_in(c, ADMIN)
    rows = feed(c)["rows"]
    check("feed: newest first, time with a zone", rows == sorted(rows, key=lambda r: r["at"], reverse=True)
          and all(r["at"].endswith(("Z", "+00:00")) for r in rows))
    check("feed by default: no staff, no seed, no plain API calls, no alerts or their copies from `messages`",
          not has(rows, user=ADMIN) and not has(rows, user="seed") and not has(rows, src="api") and not has(rows, src="event")
          and not has(rows, text="🟢 Профіль"))
    check("feed by default: the journals + failed calls", {r["src"] for r in rows} == {"login", "view", "edit", "tg", "note", "fail"}
          and {r["path"] for r in has(rows, src="fail")} == {"/api/boom"}, {r["src"] for r in rows})
    rows = feed(c, src="event")["rows"]
    check("src=event: alerts as sent, delivered or not", has(rows, kind="login", user=VASYA, sent=True) and has(rows, text="🧩 muted", sent=False))
    rows = feed(c)["rows"]
    check("feed: a stranger's message, the bot's reply, the note", has(rows, src="tg", text="хто тут", username="stranger", user="")
          and has(rows, src="tg", dir="out", kind="reply") and has(rows, src="note", text="сильний", by=ADMIN, user=VASYA))
    check("feed: `raw` stays in the base", not any("raw" in r for r in rows))
    edit = has(rows, src="edit", user=VASYA)
    check("feed: the student's own edit with old → new, about themselves",
          edit and edit[0]["coll"] == "users" and edit[0]["about"] == VASYA
          and {"field": "github", "old": "", "new": "https://github.com/vasya/labs"} in edit[0]["changes"], edit)

    rows = feed(c, src="api,fail,bogus")["rows"]
    check("src=api,fail: every call once, the crash among them", {r["src"] for r in rows} == {"api"} and len(has(rows, path="/api/boom", status=500)) == 1)
    rows = feed(c, staff=1, src="edit,tg")["rows"]
    check("staff=1: the teacher's and seed rows too, long values cut",
          has(rows, user=ADMIN) and has(rows, user="seed", changes=[{"field": "body", "old": "", "new": "x" * 200}]))

    one = feed(c, user="vasya")
    rows = one["rows"]
    check("one person: both sides of their chat and edits of their profile by others",
          has(rows, text="здай лабу", user=ADMIN) and has(rows, src="edit", user=ADMIN, about=VASYA) and not has(rows, text="хто тут"))
    check("one person: who it is + people behind the rows", one["one"] == VASYA and one["people"][VASYA]["name"] == "Пупкін Василь"
          and one["people"][VASYA]["nick"] == "vasya" and ADMIN in one["people"])
    check("unknown nick → 404", c.get("/api/activity", params={"user": "nobody"}).status_code == 404)

    first = feed(c, limit=3)
    rest = feed(c, limit=500, before=first["rows"][-1]["at"])
    ids = [r["id"] for r in first["rows"] + rest["rows"]]
    check("pages: 3 rows + more, then the older ones without overlap", len(first["rows"]) == 3 and first["more"] and not rest["more"]
          and len(ids) == len(set(ids)) == len(feed(c, limit=500)["rows"]) and rest["rows"][0]["at"] < first["rows"][-1]["at"])

    p = c.get("/api/activity/people").json()
    row = p["rows"][0]
    today, old = datetime.now(TZ).date().isoformat(), ago(days=3).astimezone(TZ).date().isoformat()
    check("people: only who showed up, staff hidden; totals over students", [r["nick"] for r in p["rows"]] == ["vasya"]
          and p["total"] == {"students": 2, "seen": 1, "linked": 1}, p)
    check("people: counts by source over 7 days — own Telegram lines only",
          row["n"] == {"login": 1, "view": 3, "api": 2, "edit": 1, "tg": 1}, row["n"])
    days = dict(zip(p["spark"], row["days"]))
    check("people: 14 days, API calls are not actions", len(p["spark"]) == 14 and p["spark"][-1] == today and days[old] == 2
          and days[today] == 4, days)
    check("people: last activity with a zone", row["last"].endswith(("Z", "+00:00")) and row["tg_linked"] is True)
    row = c.get("/api/activity/people", params={"days": 1}).json()["rows"][0]
    check("people days=1: today's counts, the same two weeks of bars", row["n"]["view"] == 1 and sum(row["days"]) == 6, row)
    rows = c.get("/api/activity/people", params={"days": 0, "staff": 1}).json()["rows"]
    check("people days=0 staff=1: all time, the teacher too", {r["nick"] for r in rows} == {"vasya", "admin"}, rows)

    check("the page's own polling leaves no footprint", db.activity.count_documents({"path": {"$regex": "^/api/activity"}}) == 0)

ok = sum(results)
print(f"\n{ok}/{len(results)} PASS")
sys.exit(0 if ok == len(results) else 1)
