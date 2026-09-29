"""Smoke: «Очима студента» (T148, T161) — only an admin; a test student can be edited, a real one is read-only;
whose rights, whose footprint; test students in the lists. Run from app/api:
DB_NAME=python_labs_smoke uv run python tests/smoke_view_as.py"""
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
from core.config import settings  # noqa: E402

ADMIN, TEST, VASYA, PETRO = "admin@nure.ua", "test.student@nure.ua", "vasya@nure.ua", "petro@nure.ua"
settings.admin_emails, settings.tg_bot_token, settings.tg_bot_name = ADMIN, "", "smoke_bot"  # no token: nothing leaves for Telegram
results = []
db.users.insert_many([
    {"email": TEST, "status": "student", "group": "TEST", "test": True, "last_name": "Тестовий", "first_name": "Студент"},
    {"email": VASYA, "status": "student", "group": "ПЗПІ-25-1"},  # a row from before the flag: no `test` at all
    {"email": PETRO, "status": "student", "group": "ПЗПІ-25-1", "last_name": "Петренко"},  # imported, never showed up
])


def check(name, cond, extra=""):
    results.append(bool(cond))
    print(("PASS " if cond else "FAIL ") + name + (f" · {extra}" if extra and not cond else ""))


def sign_in(c, email):
    settings.fake_user_email = email
    c.get("/api/auth/dev-login", follow_redirects=False)


def nicks(c):
    return sorted(s["nick"] for s in c.get("/api/students").json())


with TestClient(main.app) as c:
    check("guest: start → 401", c.post("/api/me/as/test.student").status_code == 401)
    check("guest: stop → null", c.delete("/api/me/as").json() is None)

    sign_in(c, VASYA)
    check("student: start → 403", c.post("/api/me/as/test.student").status_code == 403)
    check("student: the gallery hides the test student", nicks(c) == ["petro", "vasya"], nicks(c))

    sign_in(c, ADMIN)
    check("admin: not viewing", c.get("/api/me").json()["viewing"] is False)
    check("admin: the list has the test student, flagged",
          {s["nick"]: s["test"] for s in c.get("/api/students").json()} == {"admin": False, "petro": False, "test.student": True, "vasya": False})
    check("admin: into a teacher → 404", c.post("/api/me/as/admin").status_code == 404)
    check("admin: into nobody → 404", c.post("/api/me/as/ghost").status_code == 404)

    r = c.post("/api/me/as/test.student")
    check("admin: start → the test student", r.status_code == 200 and r.json()["email"] == TEST and r.json()["viewing"], r.text)
    me = c.get("/api/me").json()
    check("viewing: /api/me is the student", (me["email"], me["status"], me["viewing"]) == (TEST, "student", True), me)
    check("viewing: the test student has the bot link", "start=" in me.get("tg_link", ""), me)
    check("viewing: admin pages → 403", c.get("/api/students/vasya").status_code == c.get("/api/activity").status_code == 403)
    check("viewing: start again → 403", c.post("/api/me/as/test.student").status_code == 403)
    check("viewing: the gallery is the student's — with themselves", nicks(c) == ["admin", "petro", "test.student", "vasya"], nicks(c))

    r = c.put("/api/profile", json={"last_name": "Тестовий", "first_name": "Студент", "github": "https://github.com/test/labs"})
    check("viewing: the profile saved is the student's", r.status_code == 200 and db.users.find_one({"email": TEST})["github"].endswith("test/labs"))
    check("viewing: the admin's profile is untouched", not db.users.find_one({"email": ADMIN}).get("github"))

    c.post("/api/me/view", json={"path": "/my/profile"})
    check("viewing: page views are the admin's", db.activity.count_documents({"kind": "view", "user": ADMIN, "path": "/my/profile"}) == 1
          and db.activity.count_documents({"user": TEST}) == 0)
    check("viewing: the student has still never been on the site", db.users.find_one({"email": TEST}).get("last_seen_at") is None)
    check("viewing: start and stop are in the admin's footprint",
          db.activity.count_documents({"kind": "api", "user": ADMIN, "method": "POST", "path": "/api/me/as/test.student", "status": 200}) == 1)

    r = c.delete("/api/me/as")
    check("stop → the admin", r.json()["email"] == ADMIN and r.json()["viewing"] is False, r.text)
    check("stopped: admin pages are back", c.get("/api/students/vasya").status_code == 200)

    r = c.post("/api/me/as/petro")
    check("real: start → the student, read-only", r.status_code == 200 and r.json()["email"] == PETRO and r.json()["viewing"], r.text)
    me = c.get("/api/me").json()
    check("real: /api/me is the student, not a test one", (me["email"], me["status"], me["test"]) == (PETRO, "student", False), me)
    check("real: no bot link, no token minted", "tg_link" not in r.json() and "tg_link" not in me
          and not db.users.find_one({"email": PETRO}).get("tg_token"))
    check("real: reading works", c.get("/api/my/game").status_code == 200 and "petro" in nicks(c))
    r = c.put("/api/profile", json={"last_name": "Зламав", "first_name": "Я", "github": "https://github.com/oops/labs"})
    check("real: saving the profile → 403 with a reason", r.status_code == 403 and r.json()["detail"].startswith("Лише перегляд"), r.text)
    check("real: creating a game → 403, unlinking the bot → 403",
          c.post("/api/my/game", json={"title": "x", "base_custom": "y"}).status_code == c.delete("/api/me/telegram").status_code == 403)
    petro = db.users.find_one({"email": PETRO})
    check("real: the student is as they were", petro["last_name"] == "Петренко" and not petro.get("github")
          and petro.get("last_seen_at") is None and db.history.count_documents({"actor": PETRO}) == 0, petro)
    check("real: page views are still the admin's", c.post("/api/me/view", json={"path": "/my/game"}).status_code == 204
          and db.activity.count_documents({"kind": "view", "user": ADMIN, "path": "/my/game"}) == 1
          and db.activity.count_documents({"user": PETRO}) == 0)
    check("real: stop → the admin, writing is back", c.delete("/api/me/as").json()["email"] == ADMIN
          and c.put("/api/students/petro", json={"last_name": "Петренко", "group": "ПЗПІ-25-1", "status": "student"}).status_code == 200)

    c.post("/api/me/as/test.student")
    sign_in(c, VASYA)
    me = c.get("/api/me").json()
    check("a new sign-in ends the view", (me["email"], me["viewing"]) == (VASYA, False), me)

    sign_in(c, ADMIN)
    r = c.put("/api/students/vasya", json={"group": "TEST", "status": "student", "test": True})
    check("admin: the flag is set in the student form", r.json()["test"] is True and c.post("/api/me/as/vasya").status_code == 200, r.text)

ok = sum(results)
print(f"\n{ok}/{len(results)} PASS")
sys.exit(0 if ok == len(results) else 1)
