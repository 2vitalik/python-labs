"""Smoke: defenses as parts of a lesson's day (T333, lesson_defenses.py) — a student's own sent one joins the day, a date without
a lesson is a day too, the teacher sees them all, one inside a private part joins its card; the day itself is the platform's:
core/api/tests/smoke_lesson_days.py. Run from app/api:
DB_NAME=python_labs_lesson_days_smoke ~/.venvs/python-labs/bin/python tests/smoke_lesson_days.py"""
import os
import sys
from datetime import datetime

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


def check(name, cond, extra=""):
    results.append((name, bool(cond)))
    print(("PASS " if cond else "FAIL ") + name + (f" · {extra}" if extra and not cond else ""))


def login(c, email, status, **more):
    settings.fake_user_email = email
    c.get("/api/auth/dev-login")
    mongo[DB].users.update_one({"email": email}, {"$set": {"status": status, **more}})


def slugs(c, **kw):
    return [r["slug"] for r in c.get("/api/lessons", **kw).json()]


with TestClient(main.app) as c:
    login(c, "stud@nure.ua", "student", last_name="Конишев", first_name="Денис", group="ПЗПІ-25-1")
    login(c, "other@nure.ua", "student", last_name="Інший", first_name="Студент", group="ПЗПІ-25-1")
    login(c, "admin@nure.ua", "admin", first_name="Віталій", last_name="Ляпота")
    c.post("/api/lessons", json={"date": "2026-11-10", "title": "Лаба 3 і захисти", "groups": ["ПЗПІ-25-1"], "published": True, "parts": [
        {"kind": "pz", "title": "Про лабу 3", "start": "15:31:42", "end": "16:41"}, {"kind": "break", "start": "16:41", "end": "16:55"},
        {"key": "p9", "kind": "def", "title": "Захист", "start": "17:10", "only": ["stud@nure.ua"]}]})
    login(c, "stud@nure.ua", "student")

    # defenses (T327) as the site's parts: 16:05 UTC is 18:05 by the classes' clock
    base = {"labs": [1, 2], "kind": "online", "result": "passed", "link": "", "created_at": datetime(2026, 11, 10)}
    mongo[DB].defenses.insert_many([
        base | {"student": "stud@nure.ua", "started_at": datetime(2026, 11, 10, 16, 5), "ended_at": datetime(2026, 11, 10, 16, 28), "sent_at": datetime(2026, 11, 10, 17)},
        base | {"student": "other@nure.ua", "started_at": datetime(2026, 11, 10, 16, 30), "ended_at": None, "sent_at": None},
        base | {"student": "stud@nure.ua", "started_at": datetime(2026, 11, 14, 9), "ended_at": datetime(2026, 11, 14, 9, 20), "sent_at": datetime(2026, 11, 14, 10)},
        base | {"student": "other@nure.ua", "started_at": None, "ended_at": None, "sent_at": None}])
    l = c.get("/api/lessons/2026-11-10").json()
    d = l["parts"][-1]
    check("student: own sent defense joins the day — 18:05–18:28, лаби 1, 2, leads to /my/remarks", len(l["parts"]) == 3 and d["kind"] == "def"
          and (d["start"], d["end"], d["title"], d["to"], d["result"]) == ("18:05", "18:28", "лаби 1, 2", "/my/remarks", "passed"), l["parts"])
    rows = c.get("/api/lessons").json()
    check("student: a defense on a date without a lesson is a day too", rows[0]["slug"] == "2026-11-14" and rows[0]["virtual"]
          and rows[0]["parts"][0]["start"] == "11:00" and c.get("/api/lessons/2026-11-14").json()["parts"][0]["to"] == "/my/remarks", rows[0])
    login(c, "other@nure.ua", "student")
    check("another student: a defense not sent yet is not shown, the foreign day is 404",
          len(c.get("/api/lessons/2026-11-10").json()["parts"]) == 1 and c.get("/api/lessons/2026-11-14").status_code == 404 and slugs(c) == ["2026-11-10"])
    login(c, "admin@nure.ua", "admin")
    l = c.get("/api/lessons/2026-11-10").json()
    check("admin: both defenses of the date with the students, each leads to its page", [p["people"][0]["nick"] for p in l["parts"][3:]] == ["stud", "other"]
          and l["parts"][3]["to"].startswith("/defenses/") and "2026-11-14" in slugs(c), l["parts"][3:])
    own = [p for p in l["parts"] if not p.get("site")]
    own[2] |= {"start": "18:00", "end": "18:40", "title": ""}
    l = c.put("/api/lessons/2026-11-10", json={"rev": l["rev"], "parts": own}).json()
    p9 = next(p for p in l["parts"] if p["key"] == "p9")
    check("a defense inside the student's private part joins its card: one card, the badge and the link there; the other stays its own",
          len(l["parts"]) == 4 and p9["to"].startswith("/defenses/") and p9["title"] == "лаби 1, 2" and "site" not in p9 and l["parts"][3]["site"], l["parts"])

ok = sum(1 for _, p in results if p)
print(f"\n{ok}/{len(results)} PASS")
sys.exit(0 if ok == len(results) else 1)
