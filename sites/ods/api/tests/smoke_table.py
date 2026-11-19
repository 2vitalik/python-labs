"""Smoke: the site's part of /table and /students (T352) — a student's lab cards on their row, the site's own factory views.
Run from sites/ods/api: DB_NAME=ods_t352_table_smoke SESSION_SECRET=x ~/.venvs/python-labs/bin/python tests/smoke_table.py"""
import os
import sys

sys.path.insert(0, os.getcwd())
from pymongo import MongoClient  # noqa: E402

DB = os.environ["DB_NAME"]
assert DB.endswith("_smoke"), "refuse to run on a non-smoke DB"
mongo = MongoClient()
mongo.drop_database(DB)
os.environ["LAB_GATES"] = ""  # every lab takes lines here, whatever site.env opens to students (T368; smoke_gates.py)

results = []
ANSWERS ={"x": {"value": 1, "step": 0, "traps": []}, "y": {"value": 2, "step": 0, "traps": []}}


def check(name, cond, extra=""):
    results.append((name, bool(cond)))
    print(("PASS " if cond else "FAIL ") + name + (f" · {extra}" if extra and not cond else ""))


from fastapi.testclient import TestClient  # noqa: E402

import main  # noqa: E402
from core.config import settings  # noqa: E402


def login(c, email, status, group=""):
    settings.fake_user_email = email
    c.get("/api/auth/dev-login")
    mongo[DB].users.update_one({"email": email}, {"$set": {"status": status, "group": group, "last_name": email[0].upper()}})


with TestClient(main.app) as c:
    mongo[DB].variants.insert_many([{"lab": lab, "vid": f"КН-1-{n:02d}", "group": "КН-1", "n": n, "card": "", "answers": ANSWERS, "student": ""}
                                    for lab, n in [(1, 1), (1, 2), (2, 1)]])
    login(c, "a@nure.ua", "student", "КН-1")
    c.post("/api/variants/1/my/claim", json={"n": 1})
    c.put("/api/variants/1/my", json={"line": "LAB1 КН-1-01 x=1 y=5", "notebook": "https://colab/a", "way": "record"})
    c.get("/api/variants/2/my")  # the same number of lab 2 taken silently, no line yet
    login(c, "b@nure.ua", "student", "КН-1")
    login(c, "admin@nure.ua", "admin")
    c.put("/api/variants/1/results/КН-1-01", json={"points": 14, "note": "охайно"})

    data = c.get("/api/table").json()
    rows = {r["email"]: r for r in data["rows"]}
    a, b = rows["a@nure.ua"]["variants"], rows["b@nure.ua"]["variants"]
    check("table: A's lab 1 — the card, 1 of 2 right, the attempt, the notebook, the points",
          a["1"]["vid"] == "КН-1-01" and (a["1"]["ok"], a["1"]["total"], a["1"]["attempts"]) == (1, 2, 1)
          and a["1"]["notebook"] == "https://colab/a" and (a["1"]["points"], a["1"]["note"]) == (14, "охайно"), a)
    check("table: A's lab 1 — dates with the zone", a["1"]["checked_at"].endswith("+00:00") and a["1"]["assigned_at"].endswith("+00:00"), a)
    check("table: A's lab 2 — a card without a line", a["2"]["vid"] == "КН-1-01" and a["2"]["attempts"] == 0 and a["2"]["checked_at"] is None
          and a["2"]["points"] is None, a)
    check("table: A holds labs 1 and 2 only, nothing of the key", set(a) == {"1", "2"} and "answers" not in a["1"] and "card" not in a["1"], a)
    check("table: A's lab 1 — the defence, no file yet, no hint (no answers right, no notebook)",
          (a["1"]["way"], a["1"]["defended"], a["1"]["stars"], a["1"]["files"], a["1"]["file_at"], a["1"]["work"], a["1"]["hint"])
          == ("record", "", None, 0, None, None, None), a["1"])
    check("table: B without a card → {}", b == {}, b)
    check("table: the teacher is not a row", "admin@nure.ua" not in rows)

    people = {s["email"]: s for s in c.get("/api/students").json()}
    check("students: A's row carries the same cards", people["a@nure.ua"]["variants"] == a, people["a@nure.ua"])
    check("students: B and the teacher → {}", people["b@nure.ua"]["variants"] == {} and people["admin@nure.ua"]["variants"] == {})

    views = {v["slug"]: v["query"] for v in data["views"]}
    cols = {slug: q["cols"].split(",") for slug, q in views.items()}
    check("views: «Усе», «Старт» and every lab's are made", {"all", "start", *(f"lab{n}" for n in range(1, settings.labs + 1))} <= set(views), list(views))
    check("views: no repository anywhere, no «Дедлайн N»", not any(k in ks for ks in cols.values() for k in ("gh", "repo", "commits", "lastc", "reg", "lab.before", "lab.review"))
          and not any(slug.startswith("due") for slug in views), cols)
    check("views: «Усе» and «Старт» without reg", "reg" not in cols["all"] + cols["start"], cols)
    check("views: «Усе» — the answers and the points of every lab",
          all({f"lab{n}.ok", f"lab{n}.points"} <= set(cols["all"]) for n in range(1, settings.labs + 1)), cols["all"])
    check("views: «Старт» says what it is on this site", "GitHub" not in next(v["about"] for v in data["views"] if v["slug"] == "start"))
    lab3 = cols["lab3"]
    check("views: «Лаба 3» — the card, the answers, the deadline, the points, the teacher's word; no state off repositories",
          views["lab3"]["lab"] == "3" and lab3[:2] == ["lab.vid", "lab.ok"] and "lab" not in lab3
          and {"lab.due", "lab.points", "lab.pnote", "lab.met", "polls:lab"} <= set(lab3), lab3)

    login(c, "a@nure.ua", "student", "КН-1")
    check("student: /api/table is the teacher's", c.get("/api/table").status_code == 403)
    mine = c.get("/api/students").json()
    check("student: the list of students carries nobody's cards, points or notebooks", mine and not any("variants" in s for s in mine), mine)

print(f"\n{sum(ok for _, ok in results)}/{len(results)} PASS")
sys.exit(not all(ok for _, ok in results))
