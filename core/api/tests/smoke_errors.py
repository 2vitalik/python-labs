"""Smoke: the `errors` journal (T149) — API and bot failures whole, JS errors from the SPA with their limits, the feed. Run from app/api:
DB_NAME=python_labs_smoke uv run python tests/smoke_errors.py"""
import os
import sys
from types import SimpleNamespace

sys.path.insert(0, os.getcwd())
from pymongo import MongoClient  # noqa: E402

DB = os.environ["DB_NAME"]
assert DB.endswith("_smoke"), "refuse to run on a non-smoke DB"
MongoClient().drop_database(DB)
db = MongoClient()[DB]
from fastapi.testclient import TestClient  # noqa: E402

import main  # noqa: E402
from core.bot import errors, notify  # noqa: E402
from core.config import settings  # noqa: E402

ADMIN, VASYA, TEST = "admin@nure.ua", "vasya@nure.ua", "test.student@nure.ua"
settings.admin_emails, settings.tg_bot_token = ADMIN, "fake"
sent, results = [], []
db.users.insert_many([
    {"email": ADMIN, "status": "admin", "tg_chat_id": 1},
    {"email": VASYA, "status": "student", "group": "ПЗПІ-25-1", "tg_chat_id": 42},
    {"email": TEST, "status": "student", "group": "TEST", "test": True},
])


class FakeBot:
    async def send_message(self, chat_id, text, message_thread_id=None):
        if text.startswith("💥"):  # first sign-ins alert too
            sent.append(text)


notify.bot = lambda: FakeBot()


@main.app.get("/api/boom")
async def boom():
    raise RuntimeError("boom\nsecond line")


def check(name, cond, extra=""):
    results.append(bool(cond))
    print(("PASS " if cond else "FAIL ") + name + (f" · {extra}" if extra and not cond else ""))


def sign_in(c, email):
    settings.fake_user_email = email
    c.get("/api/auth/dev-login", follow_redirects=False)


def tell(c, message, ip="10.0.0.1", **data):
    return c.post("/api/errors", json={"message": message} | data, headers={"x-forwarded-for": ip, "user-agent": "smoke"}).status_code


def last(**match):
    return db.errors.find_one(match, sort=[("_id", -1)])


with TestClient(main.app, raise_server_exceptions=False) as c:
    code = tell(c, "TypeError: r.ua is null", stack="render@ActivityRow.vue:26", path="/labs/1", where="GuidePage · render function")
    e = last()
    check("guest's JS error → 204, the whole of it in `errors`",
          code == 204 and e["source"] == "front" and e["title"] == "TypeError: r.ua is null" and e["trace"] == "render@ActivityRow.vue:26"
          and e["path"] == "/labs/1" and e["where"] == "GuidePage · render function" and e["user"] == "", e)
    check("whose browser and where from", e["ua"] == "smoke" and e["ip"] == "10.0.0.1", e)
    check("alert: 💥 Сайт · page, ❗ message, 📍 where",
          sent == ["💥 Сайт · /labs/1\n❗ TypeError: r.ua is null\n📍 GuidePage · render function"], sent)
    ev = db.events.find_one({"kind": "error"})
    check("the alert is an event `error`, delivered", ev and ev["sent"] and ev["user"] == "" and ev["text"] == sent[0], ev)

    sign_in(c, VASYA)
    code = tell(c, "TypeError: r.ua is null", path="/my/profile")
    check("the same message within 10 min: saved with the student, no second alert",
          code == 204 and last()["user"] == VASYA and db.errors.count_documents({}) == 2 and len(sent) == 1, sent)
    code = tell(c, "<b>boom</b>" + "x" * 500, stack="s" * 9000, path="/my/profile?tab=<1>")
    e = last()
    check("long values are cut", code == 204 and len(e["title"]) == 300 and len(e["trace"]) == 5000, e)
    check("alert: the nick in the head, markup quoted, no 📍 without `where`",
          sent[-1] == f"💥 Сайт · /my/profile?tab=&lt;1&gt; · vasya\n❗ &lt;b&gt;boom&lt;/b&gt;{'x' * 289}", sent[-1])
    check("no message → 422, nothing saved", c.post("/api/errors", json={"stack": "s"}).status_code == 422 and db.errors.count_documents({}) == 3)

    codes = [tell(c, f"flood {i}") for i in range(3)]
    check("6th from one IP within a minute → 429, neither saved nor alerted",
          codes == [204, 204, 429] and db.errors.count_documents({}) == 5 and len(sent) == 4, (codes, sent))
    check("another IP is let in", tell(c, "flood 9", ip="10.0.0.2") == 204)

    sign_in(c, ADMIN)
    check("admin: into the test student", c.post("/api/me/as/test.student").status_code == 200)
    tell(c, "as a student", ip="10.0.0.3")
    check("«Очима студента»: the error is of who has signed in", last()["user"] == ADMIN, last())
    c.delete("/api/me/as")

    sign_in(c, VASYA)
    check("crash: the client gets 500", c.get("/api/boom?x=1", headers={"user-agent": "smoke"}).status_code == 500)
    e = last(source="api")
    check("crash: the request and the student in `errors`",
          e and e["title"] == "RuntimeError: boom\nsecond line" and e["method"] == "GET" and e["path"] == "/api/boom?x=1"
          and e["user"] == VASYA and e["ua"] == "smoke", e)
    check("crash: the whole traceback", e["trace"].startswith("Traceback (most recent call last)") and "in boom" in e["trace"]
          and e["trace"].rstrip().endswith("second line"), e["trace"])
    check("crash: alert as before — head, ❗ first line, 📍 our frame",
          sent[-1].startswith("💥 API · GET /api/boom · vasya\n❗ RuntimeError: boom\n📍 tests/smoke_errors.py:"), sent[-1])

    try:
        raise ValueError("bot boom")
    except ValueError as exc:
        ev = SimpleNamespace(update=SimpleNamespace(update_id=7, event_type="message",
                                                    message=SimpleNamespace(from_user=SimpleNamespace(id=42, username="vasya_tg"))), exception=exc)
        handled = c.portal.call(errors.bot_handler, ev)
    e = last(source="bot")
    check("bot error: handled, in `errors` with who wrote and the update type",
          handled is True and e and e["title"] == "ValueError: bot boom" and e["user"] == VASYA and e["path"] == "message"
          and "ValueError: bot boom" in e["trace"] and sent[-1].startswith("💥 Бот · message · @vasya_tg\n❗ ValueError: bot boom"), e)

    sign_in(c, ADMIN)
    rows = c.get("/api/activity", params={"src": "error"}).json()["rows"]
    check("feed src=error: newest first, no staff rows", [r["source"] for r in rows][:2] == ["bot", "api"]
          and {r["src"] for r in rows} == {"error"} and not [r for r in rows if r["user"] == ADMIN], rows)
    row = next(r for r in rows if r["source"] == "api")
    check("feed: the traceback and the request come along", row["trace"].startswith("Traceback") and row["method"] == "GET"
          and row["path"] == "/api/boom?x=1" and row["title"].startswith("RuntimeError"), row)
    rows = c.get("/api/activity").json()["rows"]
    check("feed by default: errors are in", [r for r in rows if r["src"] == "error"])
    rows = c.get("/api/activity", params={"src": "error", "staff": 1}).json()["rows"]
    check("staff=1: the teacher's error too", [r for r in rows if r["user"] == ADMIN and r["title"] == "as a student"], rows)

ok = sum(results)
print(f"\n{ok}/{len(results)} PASS")
sys.exit(0 if ok == len(results) else 1)
