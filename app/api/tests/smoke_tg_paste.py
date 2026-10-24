"""Smoke: a Telegram chat pasted on the student's card (T230) — header formats, multi-line texts, a bad header, the student guess,
the rows written, duplicates from a second paste and from the bot's own row, both sides in the student's feed. Run from app/api:
DB_NAME=python_labs_smoke uv run python tests/smoke_tg_paste.py"""
import os
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.getcwd())
from pymongo import MongoClient  # noqa: E402

DB = os.environ["DB_NAME"]
assert DB.endswith("_smoke"), "refuse to run on a non-smoke DB"
MongoClient().drop_database(DB)
db = MongoClient()[DB]
from fastapi.testclient import TestClient  # noqa: E402

import main  # noqa: E402
from core.config import settings  # noqa: E402
from core.tg_paste import parse_paste, when  # noqa: E402

ADMIN, VASYA = "admin@nure.ua", "vasya@nure.ua"
settings.admin_emails, settings.tg_bot_token, settings.tg_bot_name = ADMIN, "", "smoke_bot"
results = []

CHAT = ("Віталій Ляпота, [24.10.2026 12:34]\nПривіт! Коли здаєш лабу?\n\n"
        "Петро Петренко, [24.10.2026 12:36]\nДобрий день\n\nДумаю, у четвер\nабо в пʼятницю\n\n"
        "Віталій Ляпота, [24.10.2026 12:37]\nОк, [чекаю]\n")
MORE = "Петро Петренко, [25.10.2026 09:00]\nЗдав!\n"


def check(name, cond, extra=""):
    results.append(bool(cond))
    print(("PASS " if cond else "FAIL ") + name + (f" · {extra}" if extra and not cond else ""))


def utc(y, m, d, h, i, s=0):
    return datetime(y, m, d, h, i, s, tzinfo=timezone.utc)


rows, errors = parse_paste(CHAT)
check("3 messages, no errors", len(rows) == 3 and not errors, (rows, errors))
check("texts: multi-line with a blank line inside, brackets in text are text", [r["text"] for r in rows] == [
    "Привіт! Коли здаєш лабу?", "Добрий день\n\nДумаю, у четвер\nабо в пʼятницю", "Ок, [чекаю]"], rows)
check("times in Kyiv → UTC", rows[0]["at"].astimezone(timezone.utc) == utc(2026, 10, 24, 9, 34), rows[0]["at"])
for text, want in (("24.10.26 12:34", utc(2026, 10, 24, 9, 34)), ("2026-10-24 12:34:56", utc(2026, 10, 24, 9, 34, 56)),
                   ("24 Oct 2026 at 12:34 PM", utc(2026, 10, 24, 9, 34)), ("Oct 24, 2026 at 12:34:05 AM", utc(2026, 10, 23, 21, 34, 5)),
                   ("24/10/2026, 00:05", utc(2026, 10, 23, 21, 5))):
    check(f"date «{text}»", when(text) == want, when(text))
check("unknown date → None", when("24 жовт. 2026 12:34") is None and when("12:34") is None)
rows, errors = parse_paste("щось до шапки\nПетро, [вчора 12:34]\nтекст\n" + CHAT)
check("header with an unreadable date → error, the rest parsed, text before the first header dropped",
      errors == ["Петро, [вчора 12:34]"] and len(rows) == 3, (rows, errors))

with TestClient(main.app) as c:
    settings.fake_user_email = ADMIN
    c.get("/api/auth/dev-login", follow_redirects=False)
    db.users.update_one({"email": ADMIN}, {"$set": {"last_name": "Ляпота", "first_name": "Віталій", "tg_chat_id": 119, "tg_username": "lyapota"}})
    db.users.insert_one({"email": VASYA, "name": "Petro P", "status": "student", "last_name": "Петренко", "first_name": "Петро",
                         "tg_username": "", "aliases": [], "picture": "", "patronymic": "", "group": "", "test": False, "github": "",
                         "tg_token": "", "tg_chat_id": None})
    r = c.post("/api/students/nobody/messages", json={"text": CHAT})
    check("unknown nick → 404", r.status_code == 404, r.status_code)
    r = c.post("/api/students/vasya/messages", json={"text": CHAT}).json()
    check("look: authors with counts, the student guessed by name", r == {
        "authors": [{"name": "Віталій Ляпота", "n": 2}, {"name": "Петро Петренко", "n": 1}], "student": "Петро Петренко", "errors": []}, r)
    r = c.post("/api/students/vasya/messages", json={"text": CHAT.replace("Петро Петренко", "Buscha Rubino")}).json()
    check("look: a name unlike the student's — whoever is not the teacher", r["student"] == "Buscha Rubino", r)
    r = c.post("/api/students/vasya/messages", json={"text": "Петро, [вчора 12:34]\nтекст\n", "student": "Петро"})
    check("import with a bad header → 422", r.status_code == 422, r.status_code)
    r = c.post("/api/students/vasya/messages", json={"text": "просто текст", "student": ""})
    check("import with no messages → 422", r.status_code == 422, r.status_code)
    r = c.post("/api/students/vasya/messages", json={"text": CHAT, "student": "Петро Петренко"}).json()
    check("import: 3 added, sides counted", r == {"added": 3, "skipped": 0, "student": 1, "teacher": 2}, r)
    rows = list(db.messages.find({"kind": "import"}).sort("at"))
    check("rows: business, in, about the student, chat 0 while unlinked", all(
        m["chat_type"] == "business" and m["dir"] == "in" and m["about"] == VASYA and m["chat_id"] == 0 for m in rows), rows)
    check("teacher's line: his email, tg id, nick; author kept in raw", rows[0]["user"] == ADMIN and rows[0]["from_id"] == 119
          and rows[0]["username"] == "lyapota" and rows[0]["raw"] == {"author": "Віталій Ляпота"}, rows[0])
    check("student's line: her email, no tg id yet", rows[1]["user"] == VASYA and rows[1]["from_id"] is None and rows[1]["text"].startswith("Добрий"), rows[1])
    check("at as pasted, in UTC", rows[1]["at"].replace(tzinfo=timezone.utc) == utc(2026, 10, 24, 9, 36), rows[1]["at"])
    r = c.post("/api/students/vasya/messages", json={"text": CHAT + MORE, "student": "Петро Петренко"}).json()
    check("paste again with one more line: 3 skipped, 1 added", r == {"added": 1, "skipped": 3, "student": 1, "teacher": 0}, r)
    db.users.update_one({"email": VASYA}, {"$set": {"tg_chat_id": 555}})
    db.messages.insert_one({"dir": "in", "chat_id": 555, "chat_type": "business", "from_id": 555, "username": "", "user": "", "text": "Живий рядок",
                            "content_type": "text", "file_id": "", "message_id": 7, "kind": "", "raw": {}, "at": utc(2026, 10, 26, 8, 0, 41)})
    live = "Петро Петренко, [26.10.2026 10:00]\nЖивий рядок\n\nПетро Петренко, [26.10.2026 10:01]\nІ ще\n"
    r = c.post("/api/students/vasya/messages", json={"text": live, "student": "Петро Петренко"}).json()
    check("linked: the bot's own row at the same minute is a duplicate", r == {"added": 1, "skipped": 1, "student": 1, "teacher": 0}, r)
    last = db.messages.find_one({"text": "І ще"})
    check("linked: the student's id goes into chat_id and from_id", last["chat_id"] == 555 and last["from_id"] == 555, last)
    feed = c.get("/api/activity?user=vasya&src=tg&staff=1").json()["rows"]
    texts = [(r["user"], r["text"], r["kind"]) for r in feed]
    check("student's feed: both sides of the paste and the live row", len(feed) == 6 and (ADMIN, "Ок, [чекаю]", "import") in texts
          and (VASYA, "Здав!", "import") in texts and (VASYA, "Живий рядок", "") in texts, texts)
    db.users.update_one({"email": VASYA}, {"$set": {"tg_chat_id": None}})
    feed = c.get("/api/activity?user=vasya&src=tg").json()["rows"]
    check("unlinked again: the pasted rows of both sides stay in her feed", sum(r["kind"] == "import" for r in feed) == 5
          and any(r["user"] == ADMIN for r in feed), [(r["user"], r["text"]) for r in feed])
    all_feed = c.get("/api/activity?src=tg").json()["rows"]
    check("everyone's feed hides the teacher's lines, shows the student's", all(r["user"] != ADMIN for r in all_feed)
          and any(r["text"] == "Здав!" for r in all_feed), [(r["user"], r["text"]) for r in all_feed])

ok = sum(results)
print(f"\n{ok}/{len(results)} PASS")
sys.exit(0 if ok == len(results) else 1)
