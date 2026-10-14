"""Smoke: lessons (T218) — drafts are the admin's, students read what is published, rev/409, history, files (sources stay
the admin's, attachments open to readers), speakers → students by ПІБ and aliases, the agent's token, bundle. Run from app/api:
DB_NAME=python_labs_smoke uv run python tests/smoke_lessons.py"""
import os
import sys

sys.path.insert(0, os.getcwd())
from pymongo import MongoClient  # noqa: E402

DB = os.environ["DB_NAME"]
assert DB.endswith("_smoke"), "refuse to run on a non-smoke DB"
mongo = MongoClient()
mongo.drop_database(DB)

from fastapi.testclient import TestClient  # noqa: E402

import main  # noqa: E402
from core.config import settings  # noqa: E402

results = []
settings.agent_tokens = "claude:tok-claude"
AGENT = {"Authorization": "Bearer tok-claude"}
TRANSCRIPT = """---
course: python · lesson: 1 · kind: practice · date: 2026-10-07
---
# ПЗ 1 · Знайомство

## Початок · 18:35

**Віталій** · 18:35 — Добрий день.

**Денис Конишев** · 18:36 — Добрий.

**Zoom Guy** · 18:37 — Привіт.

*[пауза]*

## Далі · 18:40

**Віталій** · 18:40 — Продовжимо.
"""


def check(name, cond, extra=""):
    results.append((name, bool(cond)))
    print(("PASS " if cond else "FAIL ") + name + (f" · {extra}" if extra and not cond else ""))


def login(c, email, status, **more):
    settings.fake_user_email = email
    c.get("/api/auth/dev-login")
    mongo[DB].users.update_one({"email": email}, {"$set": {"status": status, **more}})


with TestClient(main.app) as c:
    check("guest: list 401", c.get("/api/lessons").status_code == 401)
    login(c, "stud@nure.ua", "student", last_name="Конишев", first_name="Денис")
    check("student: empty list, POST 403", c.get("/api/lessons").json() == [] and c.post("/api/lessons", json={}).status_code == 403)
    login(c, "admin@nure.ua", "admin", first_name="Віталій", last_name="Ляпота")

    r = c.post("/api/lessons", json={"kind": "pz", "title": "Знайомство", "date": "2026-10-07", "groups": ["ПЗПІ-25-1", " "],
                                     "links": [{"label": "Відео", "url": "https://youtu.be/x "}, {"label": "порожнє", "url": " "}]})
    l = r.json()
    check("POST: pz1, label ПЗ 1, next n, links and groups cleaned", r.status_code == 200 and l["slug"] == "pz1" and l["label"] == "ПЗ 1"
          and l["groups"] == ["ПЗПІ-25-1"] and l["links"] == [{"label": "Відео", "url": "https://youtu.be/x"}] and l["rev"] == 0, r.text)
    check("POST again: pz2 by default, lab1 of its own kind", c.post("/api/lessons", json={"kind": "pz"}).json()["slug"] == "pz2"
          and c.post("/api/lessons", json={"kind": "lab", "title": "Захист"}).json()["slug"] == "lab1")
    check("POST: taken n → 409, bad kind → 422", c.post("/api/lessons", json={"kind": "pz", "n": 1}).status_code == 409
          and c.post("/api/lessons", json={"kind": "zz"}).status_code == 422)
    check("created logged", mongo[DB].history.count_documents({"coll": "lessons", "actor": "admin@nure.ua"}) == 3)

    r = c.put("/api/lessons/pz1", json={"rev": 0, "transcript": TRANSCRIPT, "note": "транскрипт"})
    l = r.json()
    check("PUT: rev 1, transcript, speakers in order", r.status_code == 200 and l["rev"] == 1
          and l["speakers"] == ["Віталій", "Денис Конишев", "Zoom Guy"], r.text)
    check("people: the admin by first name, the student by ПІБ, Zoom Guy unknown",
          l["people"]["Віталій"]["nick"] == "admin" and l["people"]["Денис Конишев"]["nick"] == "stud" and "Zoom Guy" not in l["people"], l["people"])
    check("stale rev → 409", c.put("/api/lessons/pz1", json={"rev": 0, "title": "x"}).status_code == 409)
    r = c.put("/api/lessons/pz1", json={"rev": 1, "transcript": TRANSCRIPT})
    check("same text: no new rev", r.json()["rev"] == 1)
    h = mongo[DB].history.find_one({"coll": "lessons", "note": "транскрипт"})
    check("history: the note and the diff", h and h["changes"]["transcript"]["old"] == "" and h["changes"]["transcript"]["new"] == TRANSCRIPT.strip())

    r = c.post("/api/lessons/pz1/alias", json={"name": "Zoom Guy", "nick": "stud"})
    check("alias: Zoom Guy → stud, from now on", r.json()["people"]["Zoom Guy"]["nick"] == "stud"
          and mongo[DB].users.find_one({"email": "stud@nure.ua"})["aliases"] == ["Zoom Guy"], r.text)
    check("student edit keeps aliases", c.put("/api/students/stud", json={"last_name": "Конишев", "first_name": "Денис", "aliases": [" Zoom Guy ", "ZG", ""]}).json()["aliases"] == ["Zoom Guy", "ZG"])

    r = c.post("/api/lessons/pz1/files", files={"file": ("zoom.txt", "[Віталій] 18:35:00\nДобрий день\n".encode(), "text/plain")}, data={"role": "source"})
    src = r.json()
    check("source: words counted, role source", r.status_code == 200 and src["role"] == "source" and src["words"] == 4 and src["size"] > 0, r.text)
    r = c.post("/api/lessons/pz1/files", files={"file": ("zoom.txt", b"x y z", "text/plain")}, data={"role": "source"})
    check("same name replaces: one source, 3 words", r.json()["id"] == src["id"] and r.json()["words"] == 3
          and mongo[DB].lesson_files.count_documents({"lesson": "pz1"}) == 1)
    c.post("/api/lessons/pz1/files", files={"file": ("chat.txt", "18:40:00 From Денис: +1".encode(), "text/plain")}, data={"role": "source"})
    check("chat.txt → lesson.chat, rev 2", c.get("/api/lessons/pz1").json()["chat"] == "18:40:00 From Денис: +1" and c.get("/api/lessons/pz1").json()["rev"] == 2)
    att = c.post("/api/lessons/pz1/files", files={"file": ("Лаба.pdf", b"%PDF", "application/pdf")}).json()
    check("attachment: role file by default, pdf", att["role"] == "file" and att["type"] == "application/pdf", att)
    check("bad role → 422", c.post("/api/lessons/pz1/files", files={"file": ("a", b"1")}, data={"role": "x"}).status_code == 422)
    r = c.get(f"/api/lessons/pz1/files/{att['id']}")
    check("download: inline pdf with the name", r.status_code == 200 and r.content == b"%PDF" and "inline" in r.headers["content-disposition"]
          and "%D0%9B%D0%B0%D0%B1%D0%B0.pdf" in r.headers["content-disposition"], r.headers.get("content-disposition"))
    rows = c.get("/api/lessons").json()
    check("list: admin sees drafts, newest first, has.files", [r["slug"] for r in rows] == ["pz1", "pz2", "lab1"]
          and rows[0]["has"] == {"summary": False, "transcript": True, "chat": True, "files": 1}, rows)
    check("full: 3 files for the admin", len(c.get("/api/lessons/pz1").json()["files"]) == 3)

    login(c, "stud@nure.ua", "student")
    check("student: draft 404, file of a draft 404", c.get("/api/lessons/pz1").status_code == 404
          and c.get(f"/api/lessons/pz1/files/{att['id']}").status_code == 404)
    login(c, "admin@nure.ua", "admin")
    c.put("/api/lessons/pz1", json={"rev": 2, "published": True, "summary": "**Коротко.** Було добре.", "notes": "зсув 2 с", "context": "дедлайни"})
    login(c, "stud@nure.ua", "student")
    l = c.get("/api/lessons/pz1").json()
    check("student: published lesson without notes, context, speakers; only attachments; people resolved",
          l["summary"] and "notes" not in l and "context" not in l and "speakers" not in l
          and [f["role"] for f in l["files"]] == ["file"] and l["people"]["Денис Конишев"]["nick"] == "stud", l)
    check("student: list = published only", [r["slug"] for r in c.get("/api/lessons").json()] == ["pz1"])
    check("student: attachment 200, source 403, PUT 403, alias 403",
          c.get(f"/api/lessons/pz1/files/{att['id']}").status_code == 200 and c.get(f"/api/lessons/pz1/files/{src['id']}").status_code == 403
          and c.put("/api/lessons/pz1", json={"rev": 3, "title": "x"}).status_code == 403
          and c.post("/api/lessons/pz1/alias", json={"name": "a", "nick": "stud"}).status_code == 403)
    check("student: bundle 403, delete 403", c.get("/api/lessons/pz1/bundle").status_code == 403 and c.delete("/api/lessons/pz1").status_code == 403)

    c.cookies.clear()
    b = c.get("/api/lessons/pz1/bundle", headers=AGENT)
    check("agent: bundle with sources as text and the roster", b.status_code == 200 and {s["name"] for s in b.json()["sources"]} == {"zoom.txt", "chat.txt"}
          and b.json()["roster"] == {"Zoom Guy": "Денис Конишев", "ZG": "Денис Конишев"} and b.json()["notes"] == "зсув 2 с", b.text)
    r = c.put("/api/lessons/pz1", json={"rev": 3, "summary": "**Коротко.** Агент.", "note": "конспект"}, headers=AGENT)
    check("agent: PUT, updated by claude, rev 4", r.status_code == 200 and r.json()["updated_by"] == "claude" and r.json()["rev"] == 4, r.text)
    r = c.post("/api/lessons", json={"kind": "lec", "title": "Лекція"}, headers=AGENT)
    check("agent: POST lec1, upload, list with drafts", r.json()["slug"] == "lec1"
          and c.post("/api/lessons/lec1/files", files={"file": ("plaud.txt", b"a b")}, data={"role": "source"}, headers=AGENT).status_code == 200
          and len(c.get("/api/lessons", headers=AGENT).json()) == 4)
    check("agent: delete stays the admin's", c.delete("/api/lessons/lec1", headers=AGENT).status_code == 401)

    login(c, "admin@nure.ua", "admin")
    check("delete: lesson and its files", c.delete("/api/lessons/lec1").json()["ok"] and c.get("/api/lessons/lec1").status_code == 404
          and mongo[DB].lesson_files.count_documents({"lesson": "lec1"}) == 0)
    check("delete file", c.delete(f"/api/lessons/pz1/files/{att['id']}").status_code == 200 and c.get(f"/api/lessons/pz1/files/{att['id']}").status_code == 404)

ok = sum(1 for _, p in results if p)
print(f"\n{ok}/{len(results)} PASS")
sys.exit(0 if ok == len(results) else 1)
