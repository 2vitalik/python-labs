"""Smoke: how open each lab is to students (T368) — hidden · telegram · site: where a lab starts (LAB_GATES), the teacher's
click over it, what a student with a pinned card (T375) reads and may send in each state. All data made up.
Run from sites/ods/api: DB_NAME=ods_t368_gates_smoke SESSION_SECRET=x ~/.venvs/python-labs/bin/python tests/smoke_gates.py"""
import os
import sys

sys.path.insert(0, os.getcwd())
from pymongo import MongoClient  # noqa: E402

DB = os.environ["DB_NAME"]
assert DB.endswith("_smoke"), "refuse to run on a non-smoke DB"
mongo = MongoClient()
mongo.drop_database(DB)
db = mongo[DB]
os.environ |= {"LAB_GATES": "telegram, site, hidden", "AGENT_TOKENS": "claude:tok-123"}  # labs 4 and 5 are not named: site

from fastapi.testclient import TestClient  # noqa: E402

import main  # noqa: E402
from core.config import settings  # noqa: E402

results = []
AGENT = {"Authorization": "Bearer tok-123"}
NB = {"file": ("x.ipynb", b"{}", "application/x-ipynb+json")}
COLAB = "https://colab.research.google.com/drive/1AbC-dEf_ghIJkl"
BRIEF = {"mine": True, "vid": "КН-1-01", "handin": "site", "handed": False, "ok": 0, "total": 1, "points": None, "due": None, "late": None, "in_time": None}


def check(name, cond, extra=""):
    results.append((name, bool(cond)))
    print(("PASS " if cond else "FAIL ") + name + (f" · {extra}" if extra and not cond else ""))


def login(c, email, status, group=""):
    settings.fake_user_email = email
    c.get("/api/auth/dev-login")
    db.users.update_one({"email": email}, {"$set": {"status": status, "group": group}})


def codes(c, *paths):
    return [c.get(p).status_code for p in paths]


with TestClient(main.app) as c:
    answers = {"x": {"value": 2, "step": 0, "traps": []}}
    db.variants.insert_many([{"lab": lab, "group": "КН-1", "n": 1, "vid": "КН-1-01", "card": 'VARIANT = "КН-1-01"', "ask": [],  # pinned to A: the
                              "answers": answers, "student": "a@nure.ua"} for lab in (1, 2, 3)])  # teacher's pin goes for every lab, a hidden one too
    db.guide.insert_many([{"slug": s, "title": s, "body": "текст", "rev": 0, "updated_by": "import"}
                          for s in ("lab1", "lab2", "lab3", "lab3-case1", "labs-grading", "old-lab3", "lec01")])
    db.lab_pages.insert_many([{"slug": f"lab{n}", "kind": "lab", "lab": n, "part": "", "nav": "Умова", "order": 0, "files": []} for n in (1, 3)]
                             + [{"slug": "labs-grading", "kind": "common", "lab": None, "part": "grading", "nav": "Оцінювання", "order": 1, "files": []}])
    db.media.insert_many([{"path": p, "type": "image/png", "data": b"\x89PNG"} for p in ("lab1/x.png", "lab3/x.png", "lab3-case1/y.png", "files/lab3/n.ipynb")])

    login(c, "a@nure.ua", "student", "КН-1")
    check("student: the gates list has no hidden lab; a lab not named in LAB_GATES takes files here",
          c.get("/api/labgates").json() == {"1": "telegram", "2": "site", "4": "site", "5": "site"}, c.get("/api/labgates").text)
    check("student: the labs with cards — without the hidden one", [x["n"] for x in c.get("/api/variants").json()] == [1, 2])
    check("hidden lab: «Моя лаба», asked softly too, the notebook to start — 404", codes(c, "/api/variants/3/my", "/api/variants/3/my?soft=1",
                                                                                         "/api/variants/3/my/start") == [404] * 3)
    r = c.post("/api/variants/3/my/demo")
    check("hidden lab: the card pinned there stays out of sight — the demo click too: 404 with the words", r.status_code == 404
          and "Лаби 3 ще нема" in r.json()["detail"] and db.variants.find_one({"lab": 3})["student"] == "a@nure.ua", r.text)
    check("hidden lab: nothing is sent", c.put("/api/variants/3/my", json={"way": "live"}).status_code == 404
          and c.post("/api/variants/3/my/file", files=NB).status_code == 404 and c.post("/api/variants/3/my/pull").status_code == 404)
    check("hidden lab: its pages are not there — the lab's own and its parts", codes(c, "/api/guide/lab3", "/api/guide/lab3-case1") == [404, 404])
    slugs = sorted(p["slug"] for p in c.get("/api/guide").json())
    check("the guide's list: the open labs, the common pages and lectures stay", slugs == ["lab1", "lab2", "labs-grading", "lec01"], slugs)
    check("the labs' pages: no row of the hidden lab", sorted(p["slug"] for p in c.get("/api/labpages").json()) == ["lab1", "labs-grading"])
    check("hidden lab: its pictures and files — 404; an open lab's picture — 200",
          codes(c, "/api/media/lab3/x.png", "/api/media/lab3-case1/y.png", "/api/media/files/lab3/n.ipynb", "/api/media/lab1/x.png") == [404, 404, 404, 200])

    my = c.get("/api/variants/1/my").json()
    check("telegram lab: the pinned card, «Моя лаба» says how it is handed in", my.get("vid") == "КН-1-01" and my.get("handin") == "telegram", my)
    r = c.put("/api/variants/1/my", json={"line": "LAB1 КН-1-01 x=2"})
    check("telegram lab: an answer line — 409 with the words", r.status_code == 409 and "Telegram" in r.json()["detail"], r.text)
    check("telegram lab: a file and a link's file — 409", c.post("/api/variants/1/my/file", files=NB).status_code == 409
          and c.post("/api/variants/1/my/pull").status_code == 409)
    my = c.put("/api/variants/1/my", json={"way": "record", "notebook": COLAB}).json()
    check("telegram lab: the form of defence and the link are kept; no attempt counted", my.get("way") == "record" and my.get("notebook") == COLAB
          and my.get("attempts") == 0 and db.lab_files.count_documents({}) == 0, my)
    my = c.put("/api/variants/2/my", json={"line": "LAB2 КН-1-01 x=2"}).json()
    check("site lab: the card of the same number, the line is checked", my.get("handin") == "site" and my.get("attempts") == 1 and my.get("ok") == 1, my)
    labs = c.get("/api/variants").json()
    check("the list of labs: BRIEF says where each is handed in — lab 1 by Telegram, nothing handed; lab 2 here, the line",
          labs == [{"n": 1} | BRIEF | {"handin": "telegram"}, {"n": 2} | BRIEF | {"handed": True, "ok": 1}], labs)
    check("student: the switch is the teacher's", c.put("/api/labgates/3", json={"state": "site"}).status_code == 403)

    login(c, "admin@nure.ua", "admin")
    check("teacher: every lab with its state", c.get("/api/labgates").json() == {"1": "telegram", "2": "site", "3": "hidden", "4": "site", "5": "site"})
    check("teacher: the hidden lab is there — cards, page, picture", [x["n"] for x in c.get("/api/variants").json()] == [1, 2, 3]
          and codes(c, "/api/guide/lab3", "/api/media/lab3/x.png", "/api/guide/old-lab3") == [200, 200, 200]
          and "lab3" in [p["slug"] for p in c.get("/api/labpages").json()])
    check("teacher: a state not in the list — 422, a lab not in the course — 404",
          c.put("/api/labgates/3", json={"state": "open"}).status_code == 422 and c.put("/api/labgates/9", json={"state": "site"}).status_code == 404)
    r = c.put("/api/labgates/3", json={"state": "telegram"})
    check("teacher opens lab 3 for Telegram: the answer is every lab", r.status_code == 200 and r.json()["3"] == "telegram" and r.json()["1"] == "telegram", r.text)
    c.put("/api/labgates/3", json={"state": "telegram"})
    c.put("/api/labgates/1", json={"state": "site"})
    check("history: a row per change, none for the same word again", db.history.count_documents({"coll": "lab_gates"}) == 2)

    login(c, "a@nure.ua", "student", "КН-1")
    check("student after the click: lab 3 is there, handed in by Telegram", c.get("/api/labgates").json()["3"] == "telegram"
          and codes(c, "/api/guide/lab3", "/api/guide/lab3-case1", "/api/media/lab3/x.png") == [200, 200, 200]
          and c.get("/api/variants/3/my").json().get("handin") == "telegram", c.get("/api/variants/3/my").text)
    my = c.put("/api/variants/1/my", json={"line": "LAB1 КН-1-01 x=2"}).json()
    check("student after the click: lab 1 takes the line here", my.get("handin") == "site" and my.get("attempts") == 1, my)
    labs = c.get("/api/variants").json()
    check("…and the list follows the clicks: labs 1 and 2 here, lab 3 by Telegram", labs == [{"n": 1} | BRIEF | {"handed": True, "ok": 1},
                                                                                         {"n": 2} | BRIEF | {"handed": True, "ok": 1},
                                                                                         {"n": 3} | BRIEF | {"handin": "telegram"}], labs)
    check("student: a staff page stays the teacher's", c.get("/api/guide/old-lab3").status_code == 404)

    c.cookies.clear()
    check("agent: every lab, and the switch", c.get("/api/labgates", headers=AGENT).json()["3"] == "telegram"
          and c.put("/api/labgates/3", json={"state": "hidden"}, headers=AGENT).json()["3"] == "hidden")
    check("guest: 401", c.get("/api/labgates").status_code == 401 and c.put("/api/labgates/3", json={"state": "site"}).status_code == 401)

print(f"\n{sum(ok for _, ok in results)}/{len(results)} PASS")
sys.exit(not all(ok for _, ok in results))
