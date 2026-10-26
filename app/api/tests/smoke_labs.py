"""Smoke: labs × students (T235) — the agent in the students' list, deadlines by group, the facts off a pushed commit log,
the states of a cell, the teacher's word, the agent's review. Run from app/api: DB_NAME=python_labs_smoke uv run python tests/smoke_labs.py"""
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

ADMIN, VASYA, PETYA, TEST = "admin@nure.ua", "vasya@nure.ua", "petya@nure.ua", "tst@nure.ua"
settings.admin_emails, settings.tg_bot_token, settings.agent_tokens = ADMIN, "", "claude:tok"
AGENT = {"Authorization": "Bearer tok"}
REPO = "https://github.com/vasya/game"
results = []


def check(name, cond, extra=""):
    results.append(bool(cond))
    print(("PASS " if cond else "FAIL ") + name + (f" · {extra}" if extra and not cond else ""))


def student(email, group, github="", test=False):
    nick = email.split("@")[0]
    return {"email": email, "name": nick, "status": "student", "last_name": nick.title(), "first_name": "X", "patronymic": "", "picture": "",
            "group": group, "test": test, "github": github, "tg_username": "", "aliases": [], "tg_token": "", "tg_chat_id": None}


def commit(sha, at, **kw):
    return {"sha": sha, "at": at, "author": "Vasya", "msg": f"commit {sha}", "files": 1, "add": 10, "rm": 0} | kw


COMMITS = [commit("c3", "2026-10-22T10:00:00+03:00"), commit("c2", "2026-10-18T10:00:00+03:00", authored="2026-10-01T10:00:00+03:00"),
           commit("c1", "2026-10-10T10:00:00+03:00")]
hist = lambda coll: db.history.count_documents({"coll": coll})  # noqa: E731
last_alert = lambda: db.events.find({"kind": "due"}).sort("_id", -1)[0]["text"]  # noqa: E731

with TestClient(main.app) as c:
    check("guest on the list → 401", c.get("/api/students").status_code == 401)
    db.users.insert_many([student(VASYA, "ПЗПІ-25-1", REPO), student(PETYA, "ПЗПІ-25-2"), student(TEST, "ПЗПІ-25-0", test=True)])
    r = c.get("/api/students", headers=AGENT)
    check("agent sees the admin's list, github included", r.status_code == 200 and any(x.get("github") == REPO for x in r.json()), r.text[:200])
    check("matrix needs an admin or an agent → 401", c.get("/api/labs").status_code == 401)
    settings.fake_user_email = ADMIN
    c.get("/api/auth/dev-login", follow_redirects=False)
    m = c.get("/api/labs").json()
    check("matrix: 5 labs, students without the test one, no deadlines → nodue",
          len(m["labs"]) == 5 and [x["nick"] for x in m["rows"]] == ["vasya", "petya"] and m["rows"][0]["cells"]["1"]["state"] == "nodue", m)

    r = c.put("/api/labs/1/deadline", json={"at": "2026-10-20T21:59:00+00:00"}).json()
    check("deadline for everyone", len(r[0]["deadlines"]) == 1 and r[0]["deadlines"][0]["groups"] == [], r)
    r = c.put("/api/labs/1/deadline", json={"at": "2026-10-20T20:59:00Z"}).json()
    check("same set of groups → rewritten, still one", len(r[0]["deadlines"]) == 1 and r[0]["deadlines"][0]["at"].startswith("2026-10-20T20:59"), r)
    r = c.put("/api/labs/2/deadline", json={"at": "2026-10-24T20:59:00Z", "groups": ["ПЗПІ-25-2", " "]}).json()
    check("lab 2 for one group, blanks dropped", r[1]["deadlines"][0]["groups"] == ["ПЗПІ-25-2"], r)
    check("lab 0 and 6 → 404", c.put("/api/labs/0/deadline", json={"at": "2026-10-20T20:59:00Z"}).status_code == 404
          and c.put("/api/labs/6/deadline", json={"at": "2026-10-20T20:59:00Z"}).status_code == 404)
    check("history: a row per deadline change", hist("deadlines") == 3, hist("deadlines"))

    body = {"repos": [{"nick": "vasya", "url": REPO, "branch": "main", "head": "c3", "commits": COMMITS}, {"nick": "nobody", "url": "x"}]}
    r = c.put("/api/repos", json=body, headers=AGENT).json()
    check("repos in bulk: saved 1, unknown nobody", r == {"saved": 1, "unknown": ["nobody"]}, r)
    v, p = c.get("/api/labs").json()["rows"]
    cell = v["cells"]["1"]
    check("vasya lab 1: check · 2 before, 1 after, last c2 in UTC", cell["state"] == "check" and cell["facts"] == {
        "before": 2, "window": 2, "after": 1, "last": "2026-10-18T07:00:00+00:00", "last_sha": "c2"}, cell)
    check("repo card: 3 commits, head, branch, ok", v["repo"]["commits"] == 3 and v["repo"]["head"] == "c3" and v["repo"]["branch"] == "main" and v["repo"]["ok"], v["repo"])
    check("petya: lab 1 norepo, lab 2 due of his group; vasya lab 2 nodue",
          p["cells"]["1"]["state"] == "norepo" and p["cells"]["2"]["due"].startswith("2026-10-24T20:59") and v["cells"]["2"]["state"] == "nodue", (p["cells"], v["cells"]["2"]))
    c.put("/api/repos", json={"repos": [{"nick": "vasya", "url": REPO, "ok": False, "error": "нема доступу"}]}, headers=AGENT)
    cell = c.get("/api/students/vasya/labs").json()["labs"][0]
    check("pushed again: replaced whole — noaccess, one doc, no history", cell["state"] == "noaccess" and db.repos.count_documents({}) == 1 and hist("repos") == 0, cell)
    c.put("/api/repos", json=body, headers=AGENT)

    r = c.put("/api/students/vasya/labs/1", json={"met": True}).json()
    check("met true → ok, by admin", r["state"] == "ok" and r["mark"]["met"] is True and r["mark"]["by"] == "admin", r)
    check("alert due: lab, the word, link to the card", "Лаба 1" in last_alert() and "✅ вклався" in last_alert() and "/students/vasya/edit" in last_alert(), last_alert())
    r = c.put("/api/students/vasya/labs/1", json={"met": None}).json()
    check("met null → the site's count again", r["state"] == "check" and r["mark"]["met"] is None, r)
    r = c.put("/api/students/vasya/labs/1", json={"until": "2099-12-01T21:59:00Z", "reason": "хворів"}).json()
    check("extension: due moved ahead → wait, all 3 commits before, reason kept",
          r["state"] == "wait" and r["due"].startswith("2099-12-01T21:59") and r["facts"]["before"] == 3 and r["mark"]["reason"] == "хворів", r)
    check("alert: ⏳ до 1.12 23:59 · 💬 хворів", "⏳ до 1.12 23:59" in last_alert() and "💬 хворів" in last_alert(), last_alert())
    n_hist, n_ev = hist("lab_marks"), db.events.count_documents({"kind": "due"})
    c.put("/api/students/vasya/labs/1", json={"until": "2099-12-01T21:59:00Z", "reason": "хворів"})
    check("the same word again → no history row, no alert", hist("lab_marks") == n_hist and db.events.count_documents({"kind": "due"}) == n_ev)
    r = c.put("/api/students/vasya/labs/1", json={"open": True, "until": None}).json()
    check("open-ended → open, base due shown", r["state"] == "open" and r["mark"]["open"] and r["due"].startswith("2026-10-20"), r)
    check("alert: дата поки невідома", "дата поки невідома" in last_alert(), last_alert())
    r = c.put("/api/students/vasya/labs/1", json={"open": False}).json()
    check("extension off → check again, ✖️ in the alert", r["state"] == "check" and "✖️ подовження знято" in last_alert(), (r["state"], last_alert()))
    c.put("/api/students/vasya/labs/1", json={"until": "2099-12-01T21:59:00Z"})
    r = c.put("/api/students/vasya/labs/1", json={"until": None}).json()
    check("until null clears the date", r["due"].startswith("2026-10-20") and r["mark"]["until"] is None, r)
    check("a date closes open", c.put("/api/students/vasya/labs/1", json={"open": True}).json()["state"] == "open"
          and c.put("/api/students/vasya/labs/1", json={"until": "2099-12-01T21:59:00Z"}).json()["mark"]["open"] is False)
    c.put("/api/students/vasya/labs/1", json={"until": None})

    review = {"commit": "c2", "verdict": "none", "head": "c3", "head_verdict": "done", "summary": "поле є лише в HEAD", "report": "# Лаба 1\n\nтекст"}
    r = c.put("/api/students/vasya/labs/1/review", json=review).json()
    check("review: none at the cut, done at head → late, not stale, by admin",
          r["state"] == "late" and r["review"]["summary"] == "поле є лише в HEAD" and r["review"]["stale"] is False and r["review"]["by"] == "admin", r)
    n = hist("reviews")
    c.put("/api/students/vasya/labs/1/review", json=review)
    check("the same review again → no history", hist("reviews") == n)
    check("done at the cut → ok", c.put("/api/students/vasya/labs/1/review", json=review | {"verdict": "done"}).json()["state"] == "ok")
    check("partial, head unknown → partial", c.put("/api/students/vasya/labs/1/review", json=review | {"verdict": "partial", "head_verdict": ""}).json()["state"] == "partial")
    check("none, head none → miss", c.put("/api/students/vasya/labs/1/review", json=review | {"head_verdict": "none"}).json()["state"] == "miss")
    check("history grew with the verdicts", hist("reviews") == n + 3, hist("reviews"))
    r = c.put("/api/students/vasya/labs/1/review", json=review | {"commit": "c1"}).json()
    check("another cut reviewed → stale", r["review"]["stale"] is True and r["review"]["commit"] == "c1", r["review"])
    r = c.put("/api/students/vasya/labs/1/review", json=review | {"commit": "c2"[:1]}).json()
    check("a short sha of the same cut → not stale", r["review"]["stale"] is False, r["review"])
    check("bad verdict → 422", c.put("/api/students/vasya/labs/1/review", json=review | {"verdict": "ok"}).status_code == 422)
    r = c.get("/api/students/vasya/labs/1/review").json()
    check("the full review carries the report", r["report"] == "# Лаба 1\n\nтекст", r)
    check("no review for lab 3 → 404", c.get("/api/students/vasya/labs/3/review").status_code == 404)
    check("the teacher's word beats the review", c.put("/api/students/vasya/labs/1", json={"met": True}).json()["state"] == "ok")
    r = c.put("/api/students/petya/labs/1/review", json={"commit": "x", "verdict": "none"}, headers=AGENT)
    check("the agent may review, signs as itself", r.status_code == 200 and r.json()["review"]["by"] == "claude", r.text[:200])
    check("review with the due ahead → wait", c.put("/api/students/petya/labs/1", json={"until": "2099-01-01T21:59:00Z"}).json()["state"] == "wait")

    card = c.get("/api/students/vasya/labs").json()
    check("card: 5 labs numbered, the repo card", [x["n"] for x in card["labs"]] == [1, 2, 3, 4, 5] and card["repo"]["commits"] == 3 and card["student"]["nick"] == "vasya", card)
    check("unknown nick → 404", c.get("/api/students/nobody/labs").status_code == 404 and c.put("/api/students/nobody/labs/1", json={}).status_code == 404)
    ids = [d["id"] for d in c.get("/api/labs").json()["labs"][1]["deadlines"]]
    r = c.delete(f"/api/labs/deadlines/{ids[0]}").json()
    check("deadline deleted, history row", r[1]["deadlines"] == [] and hist("deadlines") == 4, r)
    check("deleting it again → 404", c.delete(f"/api/labs/deadlines/{ids[0]}").status_code == 404)
    check("api footprint rows for the admin's calls", db.activity.count_documents({"kind": "api", "path": {"$regex": "^/api/labs"}}) > 3)

print(f"\n{sum(results)}/{len(results)} passed")
sys.exit(0 if all(results) else 1)
