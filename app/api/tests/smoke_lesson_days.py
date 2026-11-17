"""Smoke: a lesson as a day (T333) — the address is the date, parts with keys, a private part is its student's, a break
is the teacher's, a day of private parts only; defenses as the site's parts (a day without a lesson too); clicks on links;
the attendance summary of the table. Run from app/api: DB_NAME=python_labs_smoke uv run python tests/smoke_lesson_days.py"""
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
settings.agent_tokens = "claude:tok-claude"
AGENT = {"Authorization": "Bearer tok-claude"}
TG, DRIVE = "https://t.me/c/1/2/3", "https://drive.google.com/file/d/x/view"


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

    r = c.post("/api/lessons", json={"date": "2026-11-10", "title": "Лаба 3 і захисти", "time": "15:31–19:49", "groups": ["ПЗПІ-25-1"], "parts": [
        {"kind": "pz", "title": "Про лабу 3", "start": "15:31:42", "end": "16:41", "links": [{"label": "", "url": TG}, {"label": "", "url": " "}]},
        {"kind": "break", "start": "16:41", "end": "16:55"},
        {"key": "p9", "kind": "def", "title": "Захист", "start": "17:10", "only": [" Stud@nure.ua "], "summary": "Лише йому.", "links": [{"label": "", "url": DRIVE}]}]})
    l = r.json()
    check("POST by date: the slug is the date, label 10.11, no kind", r.status_code == 200 and l["slug"] == "2026-11-10" and l["label"] == "10.11" and l["kind"] == "", r.text)
    check("parts: keys p1, p2 given, p9 kept; link cleaned; only lowercased; people for the admin",
          [p["key"] for p in l["parts"]] == ["p1", "p2", "p9"] and l["parts"][0]["links"] == [{"label": "", "url": TG}]
          and l["parts"][2]["only"] == ["stud@nure.ua"] and l["parts"][2]["people"][0]["nick"] == "stud" and l["parts"][2]["private"], l["parts"])
    check("has.video from a part's link", c.get("/api/lessons").json()[0]["has"]["video"])
    check("same date → 409, no date → 422, bad date → 422, a tag → its own day",
          c.post("/api/lessons", json={"date": "2026-11-10"}).status_code == 409 and c.post("/api/lessons", json={}).status_code == 422
          and c.post("/api/lessons", json={"date": "10.11.2026"}).status_code == 422
          and c.post("/api/lessons", json={"date": "2026-11-10", "tag": "CPO"}).json()["slug"] == "2026-11-10-cpo")
    check("PUT: another date → 422, the same → fine", c.put("/api/lessons/2026-11-10", json={"rev": 0, "date": "2026-11-11"}).status_code == 422
          and c.put("/api/lessons/2026-11-10", json={"rev": 0, "date": "2026-11-10", "published": True}).status_code == 200)
    check("PUT parts: bad kind → 422", c.put("/api/lessons/2026-11-10", json={"rev": 1, "parts": [{"kind": "zz"}]}).status_code == 422)
    check("an old address still works: pz1", c.post("/api/lessons", json={"kind": "pz", "date": "2026-10-08"}).json()["slug"] == "pz1")

    login(c, "stud@nure.ua", "student")
    l = c.get("/api/lessons/2026-11-10").json()
    check("the student of the private part: the talk and own defense, no break, no emails",
          [p["key"] for p in l["parts"]] == ["p1", "p9"] and l["parts"][1]["private"] and l["parts"][1]["summary"] == "Лише йому."
          and all("only" not in p and "people" not in p for p in l["parts"]), l["parts"])
    login(c, "other@nure.ua", "student")
    l = c.get("/api/lessons/2026-11-10").json()
    check("another student: the talk only; the list row the same", [p["key"] for p in l["parts"]] == ["p1"]
          and [p["key"] for p in c.get("/api/lessons").json()[0]["parts"]] == ["p1"], l["parts"])
    check("click: a link of a part not theirs → 404, the talk's → counted",
          c.post("/api/lessons/2026-11-10/click", json={"url": DRIVE}).status_code == 404
          and c.post("/api/lessons/2026-11-10/click", json={"url": TG}).json() == {"ok": True}
          and c.post("/api/lessons/2026-11-10/click", json={"url": TG}).status_code == 200)
    check("clicks are the teacher's to read", c.get("/api/lessons/2026-11-10/clicks").status_code == 403 and c.get("/api/lesson-clicks").status_code == 403)
    login(c, "stud@nure.ua", "student")
    c.post("/api/lessons/2026-11-10/click", json={"url": TG})
    c.post("/api/lessons/2026-11-10/click", json={"url": DRIVE})

    login(c, "admin@nure.ua", "admin")
    c.post("/api/lessons/2026-11-10/click", json={"url": TG})
    k = c.get("/api/lessons/2026-11-10/clicks").json()
    check("counts per link: 3 clicks of 2 people, the admin's own not counted", k == {TG: {"clicks": 3, "people": 2}, DRIVE: {"clicks": 1, "people": 1}}, k)
    k = c.get("/api/lesson-clicks").json()
    check("counts per hosting and per lesson", k["hostings"] == {"telegram": {"clicks": 3, "people": 2}, "drive": {"clicks": 1, "people": 1}}
          and k["lessons"] == {"2026-11-10": {"clicks": 4, "people": 2}}, k)

    c.post("/api/lessons", json={"date": "2026-11-12", "published": True, "parts": [{"kind": "def", "only": ["stud@nure.ua"]}, {"kind": "off", "title": "після пари"}]})
    login(c, "other@nure.ua", "student")
    check("a day of private parts only: not in the list, 404 by address", slugs(c) == ["2026-11-10"] and c.get("/api/lessons/2026-11-12").status_code == 404, slugs(c))
    login(c, "stud@nure.ua", "student")
    check("…and its student has it, without the part «поза заняттям»", slugs(c) == ["2026-11-12", "2026-11-10"]
          and [p["kind"] for p in c.get("/api/lessons/2026-11-12").json()["parts"]] == ["def"])

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
    check("a day that is not there and has no parts → 404", c.get("/api/lessons/2026-11-15").status_code == 404 and c.get("/api/lessons/nope").status_code == 404)

    # attendance summary for the table: 100 min meeting, stud 60 min, other 10 min (under a quarter)
    mongo[DB].lessons.update_one({"slug": "2026-11-10"}, {"$set": {"zoom": {"uuid": "u", "topic": "", "start": "2026-11-10T13:30:00Z", "end": "2026-11-10T15:10:00Z", "pulled": ""}}})
    mongo[DB].attendance.insert_many([{"lesson": "2026-11-10", "name": "Денис Конишев", "email": "", "segments": [], "seconds": 3600, "late": 0, "meeting_uuid": "u", "fetched_at": datetime(2026, 11, 10)},
                                      {"lesson": "2026-11-10", "name": "Студент Інший", "email": "", "segments": [], "seconds": 600, "late": 0, "meeting_uuid": "u", "fetched_at": datetime(2026, 11, 10)}])
    att = {r["nick"]: r["attendance"] for r in c.get("/api/table").json()["rows"]}
    check("table: seen of total, minutes, the last date; under the threshold is not «був»",
          att == {"stud": {"seen": 1, "total": 1, "minutes": 60, "last": "2026-11-10"}, "other": {"seen": 0, "total": 1, "minutes": 10, "last": None}}, att)

    c.cookies.clear()
    b = c.get("/api/lessons/2026-11-10/bundle", headers=AGENT)
    check("agent: the bundle carries the parts with their texts", b.status_code == 200 and b.json()["parts"][2]["summary"] == "Лише йому.", b.text[:300])

ok = sum(1 for _, p in results if p)
print(f"\n{ok}/{len(results)} PASS")
sys.exit(0 if ok == len(results) else 1)
