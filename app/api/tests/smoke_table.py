"""Smoke: the table of students (T240) — a row from every source, the teacher's own fields of every type and scope, values checked
against the type, saved views, 🙋 with its alert, the agent reading polls. Run from app/api: DB_NAME=python_labs_smoke uv run python tests/smoke_table.py"""
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

ADMIN, VASYA, PETYA, TEST = "admin@nure.ua", "vasya@nure.ua", "petya@nure.ua", "tst@nure.ua"
settings.admin_emails, settings.tg_bot_token, settings.agent_tokens = ADMIN, "", "claude:tok"
AGENT = {"Authorization": "Bearer tok"}
REPO = "https://github.com/vasya/game"
now = datetime.now(timezone.utc)
results = []


def check(name, cond, extra=""):
    results.append(bool(cond))
    print(("PASS " if cond else "FAIL ") + name + (f" · {extra}" if extra and not cond else ""))


def student(email, group, github="", test=False, tg=None, seen=None):
    nick = email.split("@")[0]
    return {"email": email, "name": nick, "status": "student", "last_name": nick.title(), "first_name": "X", "patronymic": "", "picture": "",
            "group": group, "test": test, "github": github, "tg_username": "", "aliases": [], "tg_token": "", "tg_chat_id": tg, "first_seen_at": seen}


def commit(sha, at):
    return {"sha": sha, "at": at, "author": "Vasya", "msg": f"commit {sha}", "files": 1, "add": 10, "rm": 0}


hist = lambda coll: db.history.count_documents({"coll": coll})  # noqa: E731
last_alert = lambda: db.events.find({"kind": "due"}).sort("_id", -1)[0]["text"]  # noqa: E731
put = lambda c, nick, key, body: c.put(f"/api/students/{nick}/fields/{key}", json=body)  # noqa: E731

db.users.insert_many([student(VASYA, "ПЗПІ-25-1", REPO, tg=42, seen=now), student(PETYA, "ПЗПІ-25-2"), student(TEST, "ПЗПІ-25-0", test=True, seen=now)])
pid = db.polls.insert_one({"template": None, "title": "Перший дедлайн", "question": "Що зробили?", "options": [{"emoji": "🌐", "text": "сайт"}, {"emoji": "🐙", "text": "github"}],
                           "multiple": True, "tags": ["дедлайн", "lab1"], "status": "open", "by": ADMIN, "created_at": now, "sent_at": now, "closed_at": None}).inserted_id
db.poll_sends.insert_one({"poll": pid, "chat_id": -1, "thread_id": None, "where": "Polls", "silent": False, "status": "sent", "tg_poll_id": "tg1", "message_id": 1,
                          "url": "", "option_ids": [], "error": "", "state": {}, "by": ADMIN, "at": now, "sent_at": now, "closed_at": None})
db.votes.insert_one({"update_id": 1, "tg_poll_id": "tg1", "poll": pid, "tg_id": 42, "username": "v", "user": VASYA, "option_ids": [0, 1], "text": "", "raw": {}, "at": now})

with TestClient(main.app) as c:
    check("guest → 401", c.get("/api/table").status_code == 401)
    t = c.get("/api/table", headers=AGENT).json()
    rows = {r["nick"]: r for r in t["rows"]}
    check("rows: students by group, the test one out", list(rows) == ["vasya", "petya"], list(rows))
    v, p = rows["vasya"], rows["petya"]
    check("vasya: seen, bot, github, ПІБ", v["seen"] and v["seen_at"] and v["tg_linked"] and v["github"] == REPO and v["fio"] and v["email"] == VASYA, v)
    check("petya: nothing yet, no repo", not p["seen"] and not p["tg_linked"] and p["repo"] is None and p["polls"] == {}, p)
    check("five lab cells, nodue", list(v["labs"]) == ["1", "2", "3", "4", "5"] and v["labs"]["1"]["state"] == "nodue", v["labs"].keys())
    check("vasya's vote found by Telegram id", v["polls"][str(pid)]["ids"] == [0, 1] and v["polls"][str(pid)]["at"], v["polls"])
    check("polls, deadlines, no fields or views yet", t["polls"][0]["title"] == "Перший дедлайн" and len(t["labs"]) == 5 and t["fields"] == [] and t["views"] == [], t["polls"])
    c.put("/api/repos", json={"repos": [{"nick": "vasya", "url": REPO, "branch": "main", "head": "c2",
                                         "commits": [commit("c2", "2026-10-22T10:00:00+03:00"), commit("c1", "2026-10-10T10:00:00+03:00")]}]}, headers=AGENT)
    r = c.get("/api/table", headers=AGENT).json()["rows"][0]["repo"]
    check("repo card: commits, first and last", r["commits"] == 2 and r["first"].startswith("2026-10-10T07:00") and r["last"].startswith("2026-10-22T07:00"), r)

    settings.fake_user_email = ADMIN
    c.get("/api/auth/dev-login", follow_redirects=False)
    check("field needs a title → 422", c.post("/api/fields", json={"title": " ", "type": "bool"}).status_code == 422)
    check("select without options → 422", c.post("/api/fields", json={"title": "Якість", "type": "select"}).status_code == 422)
    check("a colour off the palette → 422", c.post("/api/fields", json={"title": "X", "type": "select", "options": [{"text": "a", "color": "mauve"}]}).status_code == 422)
    f = c.post("/api/fields", json={"title": "Якість коду", "emoji": "✨", "type": "select", "scope": "lab",
                                    "options": [{"text": "добре", "emoji": "🟢", "color": "green"}, {"text": "так собі", "emoji": "🟡", "color": "yellow"}]}).json()
    check("select on labs: key in Latin, option ids from the texts, first in order",
          f["key"] == "iakist-kodu" and [o["id"] for o in f["options"]] == ["dobre", "tak-sobi"] and f["order"] == 0 and f["scope"] == "lab" and f["by"] == "admin", f)
    f2 = c.post("/api/fields", json={"title": "Якість коду", "type": "bool"}).json()
    check("the same title again → key -2, next in order", f2["key"] == "iakist-kodu-2" and f2["order"] == 1, f2)
    for title, kind, more in (("Бали", "number", {}), ("Коментар", "text", {}), ("Захист", "date", {}), ("Теги", "multi", {"options": [{"text": "a"}, {"text": "b"}, {"text": "c"}]})):
        c.post("/api/fields", json={"title": title, "type": kind} | more)
    check("history: a row per field", hist("fields") == 6, hist("fields"))

    r = put(c, "vasya", "iakist-kodu", {"value": "dobre", "lab": 2}).json()
    check("a select on lab 2 → column key.2", r == {"column": "iakist-kodu.2", "value": "dobre"}, r)
    check("lab field without the lab → 422", put(c, "vasya", "iakist-kodu", {"value": "dobre"}).status_code == 422)
    check("unknown option → 422", put(c, "vasya", "iakist-kodu", {"value": "x", "lab": 1}).status_code == 422)
    check("bool: «1» is true, false stays", put(c, "vasya", "iakist-kodu-2", {"value": "1"}).json()["value"] is True
          and put(c, "vasya", "iakist-kodu-2", {"value": False}).json()["value"] is False)
    check("number: «3.0» → 3, «abc» → 422", put(c, "vasya", "baly", {"value": "3.0"}).json()["value"] == 3 and put(c, "vasya", "baly", {"value": "abc"}).status_code == 422)
    check("text trimmed", put(c, "vasya", "komentar", {"value": "  ok  "}).json()["value"] == "ok")
    check("date: ISO, «05.11» → 422", put(c, "vasya", "zakhyst", {"value": "2026-11-05"}).json()["value"] == "2026-11-05"
          and put(c, "vasya", "zakhyst", {"value": "05.11"}).status_code == 422)
    check("multi: the field's order, no twins, unknown → 422", put(c, "vasya", "tehy", {"value": ["c", "a", "c"]}).json()["value"] == ["a", "c"]
          and put(c, "vasya", "tehy", {"value": ["x"]}).status_code == 422)
    n = hist("field_values")
    r = put(c, "vasya", "komentar", {"value": None}).json()
    check("null clears: the document goes, history keeps the row", r == {"column": "komentar", "value": None}
          and db.field_values.count_documents({"field": "komentar"}) == 0 and hist("field_values") == n + 1, r)
    check("the same value again → no history", put(c, "vasya", "baly", {"value": 3}).status_code == 200 and hist("field_values") == n + 1)
    check("unknown field or nick → 404", put(c, "vasya", "nope", {"value": 1}).status_code == 404 and put(c, "nobody", "baly", {"value": 1}).status_code == 404)
    t = c.get("/api/table").json()
    v = {r["nick"]: r for r in t["rows"]}["vasya"]
    check("the row carries the values by column", v["fields"] == {"iakist-kodu.2": "dobre", "iakist-kodu-2": False, "baly": 3, "zakhyst": "2026-11-05", "tehy": ["a", "c"]}, v["fields"])
    check("fields in order of making", [f["key"] for f in t["fields"]] == ["iakist-kodu", "iakist-kodu-2", "baly", "komentar", "zakhyst", "tehy"])
    r = c.post("/api/fields/order", json={"keys": ["tehy", "iakist-kodu"]}).json()
    check("reorder: the named ones first", [f["key"] for f in r["fields"]][:2] == ["tehy", "iakist-kodu"], [f["key"] for f in r["fields"]])
    r = c.put("/api/fields/iakist-kodu", json={"title": "Якість", "emoji": "✨", "type": "select", "scope": "lab",
                                              "options": [{"id": "dobre", "text": "чудово", "emoji": "🟢", "color": "green"}, {"text": "погано", "emoji": "🔴", "color": "red"}]}).json()
    check("update: a renamed option keeps its id, a new one gets its own, the key stays",
          r["key"] == "iakist-kodu" and r["title"] == "Якість" and [o["id"] for o in r["options"]] == ["dobre", "pohano"], r)
    check("type frozen once there are values → 409", c.put("/api/fields/iakist-kodu", json={"title": "Якість", "type": "text", "scope": "lab"}).status_code == 409)
    check("type free while empty", c.put("/api/fields/komentar", json={"title": "Коментар", "type": "number"}).json()["type"] == "number")
    r = c.delete("/api/fields/iakist-kodu").json()
    check("delete: the field and its one value", r == {"ok": True, "values": 1} and db.field_values.count_documents({"field": "iakist-kodu"}) == 0
          and db.fields.count_documents({"key": "iakist-kodu"}) == 0, r)
    check("deleting it again → 404", c.delete("/api/fields/iakist-kodu").status_code == 404)

    check("view needs a title → 422", c.post("/api/views", json={"title": " "}).status_code == 422)
    r = c.post("/api/views", json={"title": "Лаба 1 — без репо", "emoji": "🚫", "query": {"cols": "seen,bot", "f.gh": "0", "junk": "x", "f.nested": {"a": 1}}}).json()
    check("view: slug from the title, query cleaned", r["slug"] == "laba-1-bez-repo" and r["query"] == {"cols": "seen,bot", "f.gh": "0"} and r["emoji"] == "🚫", r)
    r2 = c.post("/api/views", json={"title": "Lab1"}).json()
    check("a built-in slug steps aside", r2["slug"] == "lab1-2", r2)
    r = c.put("/api/views/laba-1-bez-repo", json={"title": "Без репо", "query": {"cols": "seen"}}).json()
    check("view updated", r["title"] == "Без репо" and r["query"] == {"cols": "seen"} and hist("views") == 3, r)
    check("views ride in the table", [x["slug"] for x in c.get("/api/table").json()["views"]] == ["laba-1-bez-repo", "lab1-2"])
    check("view deleted once", c.delete("/api/views/lab1-2").json() == {"ok": True} and c.delete("/api/views/lab1-2").status_code == 404)

    r = c.put("/api/students/vasya/labs/1", json={"asked": True, "asked_for": "на тиждень"}).json()
    check("🙋 asked, in their words", r["mark"]["asked"] is True and r["mark"]["asked_for"] == "на тиждень", r["mark"])
    check("alert: 🙋 просив подовжити · на тиждень", "🙋 просив подовжити · на тиждень" in last_alert(), last_alert())
    r = c.put("/api/students/vasya/labs/1", json={"asked": False}).json()
    check("🙅 taken back", r["mark"]["asked"] is False and "🙅" in last_alert(), last_alert())

    check("the agent reads polls, results, the matrix", c.get("/api/polls", headers=AGENT).status_code == 200
          and c.get(f"/api/polls/{pid}", headers=AGENT).status_code == 200 and c.get("/api/polls/matrix", headers=AGENT).status_code == 200)
    settings.fake_user_email = VASYA
    c.get("/api/auth/dev-login", follow_redirects=False)
    check("a student: no table, fields, views or polls → 403", {c.get(p).status_code for p in ("/api/table", "/api/fields", "/api/views", "/api/polls")} == {403})

print(f"\n{sum(results)}/{len(results)} passed")
sys.exit(0 if all(results) else 1)
