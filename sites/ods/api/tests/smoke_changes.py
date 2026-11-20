"""Smoke: the catalogue of changes in the lectures (T374) — who may (a guest 401, a student 403, an admin and an agent — yes);
a push new · updated · same by the site's sha1, which bin/content counts the same way; the list without the blocks, the
blocks per lecture; the lecturer's slides as pictures open like the lecture. All data made up. Run from sites/ods/api:
DB_NAME=ods_t374_changes_smoke SESSION_SECRET=x PYTHONPATH=../../../core/api ~/.venvs/python-labs/bin/python tests/smoke_changes.py"""
import copy
import hashlib
import json
import os
import sys

sys.path.insert(0, os.getcwd())
from pymongo import MongoClient  # noqa: E402

DB = os.environ["DB_NAME"]
assert DB.endswith("_smoke"), "refuse to run on a non-smoke DB"
mongo = MongoClient()
mongo.drop_database(DB)
db = mongo[DB]

from fastapi.testclient import TestClient  # noqa: E402

import main  # noqa: E402
from core.config import settings  # noqa: E402

settings.agent_tokens, settings.guide_readers = "smoke:tok-smoke", "active"
AGENT = {"Authorization": "Bearer tok-smoke"}
EDIT = {"del": "стара річ", "ins": "нова річ", "a": [6, 15], "b": [6, 14]}
ITEM = {"id": "99-k0000aaaa", "lec": 99, "slide": 3, "group": "lang", "kind": "term", "sev": 1, "status": "fixed", "where": "text",
        "origin": "slide", "size": 17, "auto": False, "verified": False, "title": "", "note": "", "why": "", "ref": "",
        "hunk": "h1", "edits": [EDIT]}
HUNK = {"slide": 3, "before": "Перша стара річ тут.", "after": "Перша нова річ тут.", "prev": "## Розділ", "next": "Далі $x_1$."}
LEC = {"lec": 99, "slug": "lec99", "base": "orig", "head": "f" * 40, "built": "2026-11-20T00:00:00+00:00",
       "items": [ITEM], "hunks": {"h1": HUNK}, "todo": 0}
results = []


def check(name, cond, extra=""):
    results.append((name, bool(cond)))
    print(("PASS " if cond else "FAIL ") + name + (f" · {extra}" if extra and not cond else ""))


def login(c, email, status):
    settings.fake_user_email = email
    c.get("/api/auth/dev-login")
    db.users.update_one({"email": email}, {"$set": {"status": status}})


def sha(data: dict) -> str:
    """As the site counts it (routes/lecture_changes.py) and bin/content after it."""
    return hashlib.sha1(json.dumps(data, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def calls(c, **kw):
    return [c.get("/api/lectures/changes", **kw).status_code, c.get("/api/lectures/changes/lec99", **kw).status_code,
            c.put("/api/content/changes/lec99", json=LEC, **kw).status_code]


def push(c, data, slug="lec99"):
    r = c.put(f"/api/content/changes/{slug}", json=data, headers=AGENT)
    return r.json().get("state") if r.status_code == 200 else r.status_code


with TestClient(main.app) as c:
    check("guest: the list, a lecture's blocks, a push → 401", calls(c) == [401] * 3, calls(c))
    login(c, "stud@nure.ua", "student")
    check("student: the same → 403", calls(c) == [403] * 3, calls(c))
    check("student: nothing written", db.lecture_changes.count_documents({}) == 0)
    c.cookies.clear()

    check("agent: a new catalogue", push(c, LEC) == "new")
    check("agent: the same again → same", push(c, copy.deepcopy(LEC)) == "same")
    later = copy.deepcopy(LEC) | {"built": "2026-11-21T00:00:00+00:00"}
    later["items"][0] |= {"kind": "calque", "note": "калька"}
    check("agent: a changed one → updated", push(c, later) == "updated")
    check("… kept whole, with its sha1", db.lecture_changes.find_one({"slug": "lec99"})["sha"] == sha(later))
    check("no items list or no hunks → 422", push(c, {"items": {}, "hunks": {}}) == push(c, {"items": []}) == 422)
    check("what the site has: the catalogue's sha1, as bin/content counts it",
          c.get("/api/content", headers=AGENT).json().get("changes") == {"lec99": sha(later)})
    push(c, copy.deepcopy(LEC) | {"lec": 98, "slug": "lec98", "todo": 1}, "lec98")

    login(c, "admin@nure.ua", "admin")
    r = c.get("/api/lectures/changes")
    rows = r.json().get("lectures", [])
    check("admin: every lecture, by slug", r.status_code == 200 and [x["slug"] for x in rows] == ["lec98", "lec99"], r.text[:300])
    check("… with its items and numbers, without the blocks", "hunks" not in rows[1] and rows[1]["items"] == later["items"]
          and (rows[1]["lec"], rows[1]["todo"], rows[1]["head"]) == (99, 0, "f" * 40) and rows[0]["todo"] == 1, rows[1:])
    r = c.get("/api/lectures/changes/lec99")
    check("admin: a lecture's blocks apart", r.status_code == 200 and r.json() == {"hunks": later["hunks"]}, r.text[:300])
    check("admin: a lecture without a catalogue → 404", c.get("/api/lectures/changes/lec97").status_code == 404)
    c.cookies.clear()
    check("agent: reads the list and the blocks too", c.get("/api/lectures/changes", headers=AGENT).status_code == 200
          and c.get("/api/lectures/changes/lec98", headers=AGENT).json()["hunks"] == LEC["hunks"])

    webp = c.put("/api/content/media/lec99/orig/s03.webp", content=b"RIFF smoke WEBP", headers=AGENT | {"Content-Type": "image/webp"})
    check("agent: a slide of the lecturer as a picture", webp.json().get("state") == "new", webp.text)
    check("guest: the slide's picture → 401", c.get("/api/media/lec99/orig/s03.webp").status_code == 401)
    login(c, "stud@nure.ua", "student")
    r = c.get("/api/media/lec99/orig/s03.webp")
    check("student: the slide's picture, like the lecture's own", r.status_code == 200 and r.headers["content-type"] == "image/webp", r.status_code)

print(f"\n{sum(ok for _, ok in results)}/{len(results)} PASS")
sys.exit(not all(ok for _, ok in results))
