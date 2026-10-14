"""Smoke: attendance from Zoom (T222) with a fake Zoom — not set up → 503, the run by the lesson's date, segments merged,
late, the threshold, the teacher apart, unknown names → alias, students see the published block only, the matrix,
the recording's files as sources, the agent's token. Run from app/api: DB_NAME=python_labs_smoke uv run python tests/smoke_attendance.py"""
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
from core.routes import attendance as ar  # noqa: E402
from core.zoom import path_id  # noqa: E402

results = []
settings.agent_tokens = "claude:tok-claude"
AGENT = {"Authorization": "Bearer tok-claude"}
D = "2026-10-07T"


class Fake:
    """Zoom as the fixture: one recurring meeting with two runs, the cloud recording of the later one."""
    runs = {"123456789": [{"uuid": "abc/def==", "start_time": D + "15:33:10Z"}, {"uuid": "old==", "start_time": "2026-09-30T15:35:00Z"}]}
    meetings = {"abc/def==": {"uuid": "abc/def==", "topic": "ПЗ Python", "start_time": D + "15:33:10Z", "end_time": D + "17:13:10Z", "duration": 100},
                "old==": {"uuid": "old==", "topic": "ПЗ Python", "start_time": "2026-09-30T15:35:00Z", "duration": 90}}
    parts = {"abc/def==": [
        {"name": "Віталій", "user_email": "admin@nure.ua", "join_time": D + "15:33:10Z", "leave_time": D + "17:13:10Z", "duration": 6000},
        {"name": "Денис Конишев", "user_email": "", "join_time": D + "15:40:10Z", "leave_time": D + "16:30:00Z"},
        {"name": "денис конишев", "join_time": D + "16:20:00Z", "leave_time": D + "17:10:00Z"},  # the same person, overlapping
        {"name": "Zoom Guy", "join_time": D + "15:33:00Z", "leave_time": D + "17:13:00Z"},
        {"name": "Поп Ін", "join_time": D + "16:00:00Z", "leave_time": D + "16:10:00Z"},
        {"name": "", "join_time": D + "16:00:00Z", "leave_time": D + "17:00:00Z"},
        {"name": "Ghost", "join_time": None, "leave_time": None},
    ], "old==": []}
    recs = {"abc/def==": {"share_url": "https://zoom.us/rec/share/xyz", "download_access_token": "dl", "recording_files": [
        {"file_type": "MP4", "download_url": "https://z/mp4", "status": "completed"},
        {"file_type": "TRANSCRIPT", "download_url": "https://z/vtt", "status": "completed"},
        {"file_type": "CHAT", "download_url": "https://z/chat", "status": "completed"}]}}
    files = {"https://z/vtt": b"WEBVTT\n\n1\n00:00:01.000 --> 00:00:03.000\nVitalii: Dobryi den\n", "https://z/chat": "15:40:10\tДенис Конишев:\t+1\n".encode()}

    async def instances(self, mid): return self.runs.get(mid, [])
    async def details(self, m): return self.meetings[m]
    async def participants(self, uuid): return self.parts[uuid]
    async def recordings(self, uuid): return self.recs[uuid]
    async def download(self, url, token=""):
        assert token == "dl"
        return self.files[url]


def check(name, cond, extra=""):
    results.append((name, bool(cond)))
    print(("PASS " if cond else "FAIL ") + name + (f" · {extra}" if extra and not cond else ""))


def login(c, email, status, **more):
    settings.fake_user_email = email
    c.get("/api/auth/dev-login")
    mongo[DB].users.update_one({"email": email}, {"$set": {"status": status, **more}})


check("path_id: a UUID with / is double-encoded, a numeric ID as is, = once", path_id("abc/def==") == "abc%252Fdef%253D%253D" and path_id("123") == "123" and path_id("x+y==") == "x%2By%3D%3D")

with TestClient(main.app) as c:
    login(c, "stud@nure.ua", "student", last_name="Конишев", first_name="Денис", group="ПЗПІ-25-1")
    login(c, "other@nure.ua", "student", last_name="Інший", first_name="Студент", group="ПЗПІ-25-2")
    login(c, "admin@nure.ua", "admin", first_name="Віталій", last_name="Ляпота")
    c.post("/api/lessons", json={"kind": "pz", "title": "Знайомство", "date": "2026-10-07", "groups": ["ПЗПІ-25-1"]})
    c.post("/api/lessons", json={"kind": "pz", "date": "2026-10-08"})
    c.post("/api/lessons", json={"kind": "pz"})
    r = c.post("/api/lessons/pz1/zoom", json={"meeting": "123456789"})
    check("not set up: 503 with the three variables", r.status_code == 503 and "ZOOM_ACCOUNT_ID" in r.text, r.text)
    ar.zoom = Fake()
    check("no meeting given, none on the lesson → 422", c.post("/api/lessons/pz1/zoom", json={}).status_code == 422)
    check("unknown lesson → 404", c.post("/api/lessons/pz9/zoom", json={"meeting": "1"}).status_code == 404)

    r = c.post("/api/lessons/pz1/zoom", json={"meeting": "123456789"})
    a = r.json()
    check("pull: the run of the lesson's date, 5 rows (no times → skipped), meeting span 6000 s", r.status_code == 200 and a["pulled"] == 5
          and a["meeting"]["uuid"] == "abc/def==" and a["meeting"]["topic"] == "ПЗ Python" and a["seconds"] == 6000, r.text)
    stud = a["people"][0]
    check("student: segments merged (case aside) 15:40:10–17:10:00 = 5390 s, late 420 s, present, 2→1 segment", len(a["people"]) == 1
          and stud["person"]["nick"] == "stud" and stud["seconds"] == 5390 and stud["late"] == 420 and stud["present"] and len(stud["segments"]) == 1, stud)
    check("teacher apart by first name, with email", a["teachers"][0]["person"]["nick"] == "admin" and a["teachers"][0]["email"] == "admin@nure.ua", a["teachers"])
    names = [u["name"] for u in a["unknown"]]
    check("unknown: Zoom Guy on time, Поп Ін 600 s under 25 % → not present, the nameless row; others = 3",
          names == ["Zoom Guy", "(без імені)", "Поп Ін"] and a["unknown"][0]["late"] == 0 and not a["unknown"][2]["present"] and a["others"] == 3, a["unknown"])
    check("of: students of the lesson's groups", a["of"] == 1)
    l = c.get("/api/lessons/pz1").json()
    check("lesson remembers the meeting, zoom.start/end, has.zoom, history note", l["meeting"] == "123456789" and l["zoom"]["start"] == D + "15:33:10Z"
          and l["zoom"]["end"] == D + "17:13:10Z" and l["has"]["zoom"] and l["rev"] == 1
          and mongo[DB].history.count_documents({"coll": "lessons", "note": "відвідування із Zoom"}) == 1, l)
    check("again without a meeting: the lesson's own, rows replaced not doubled", c.post("/api/lessons/pz1/zoom", json={}).json()["pulled"] == 5
          and mongo[DB].attendance.count_documents({"lesson": "pz1"}) == 5)

    r = c.post("/api/lessons/pz2/zoom", json={"meeting": "123456789"})
    check("a date Zoom has no run for → 404 naming the last runs", r.status_code == 404 and "2026-10-07" in r.text and "2026-09-30" in r.text, r.text)
    r = c.post("/api/lessons/pz3/zoom", json={"meeting": "123456789"})
    check("no date on the lesson: the last run", r.json()["meeting"]["uuid"] == "abc/def==", r.text)
    r = c.post("/api/lessons/pz3/zoom", json={"meeting": "old=="})
    check("a UUID names one run; end from duration when Zoom gives none; empty room → 0 rows", r.json()["meeting"]["uuid"] == "old=="
          and r.json()["meeting"]["end"] == "2026-09-30T17:05:00+00:00" and r.json()["pulled"] == 0 and r.json()["people"] == [], r.text)

    c.post("/api/lessons/pz1/alias", json={"name": "Zoom Guy", "nick": "stud"})
    a = c.get("/api/lessons/pz1/attendance").json()
    check("alias: Zoom Guy is the student from now on, 2 people rows, others 2", [p["person"]["nick"] for p in a["people"]] == ["stud", "stud"] and a["others"] == 2, a["people"])
    check("PUT meeting is stripped", c.put("/api/lessons/pz3", json={"rev": c.get("/api/lessons/pz3").json()["rev"], "meeting": " 999 "}).json()["meeting"] == "999")

    login(c, "stud@nure.ua", "student")
    check("student: draft → 404, pull 403, matrix 403", c.get("/api/lessons/pz1/attendance").status_code == 404
          and c.post("/api/lessons/pz1/zoom", json={}).status_code == 403 and c.get("/api/attendance").status_code == 403)
    login(c, "admin@nure.ua", "admin")
    c.put("/api/lessons/pz1", json={"rev": c.get("/api/lessons/pz1").json()["rev"], "published": True})
    login(c, "stud@nure.ua", "student")
    a = c.get("/api/lessons/pz1/attendance").json()
    check("student: people with avatars and seconds only, no unknown names, others counted, teacher there",
          a["people"] and all(set(p) == {"name", "person", "seconds", "present"} for p in a["people"]) and a["unknown"] == [] and a["others"] == 2
          and a["teachers"][0]["person"]["nick"] == "admin", a)
    check("student: no meeting ID in the lesson, zoom span yes", "meeting" not in c.get("/api/lessons/pz1").json() and c.get("/api/lessons/pz1").json()["zoom"]["uuid"])
    c.cookies.clear()
    check("guest: 401", c.get("/api/lessons/pz1/attendance").status_code == 401)

    login(c, "admin@nure.ua", "admin")
    m = c.get("/api/attendance").json()
    check("matrix: lessons with a pull in date order, rows = students, the two aliases add up to 11390 s, unknown 2",
          [l["slug"] for l in m["lessons"]] == ["pz3", "pz1"] and m["lessons"][1]["seconds"] == 6000 and m["lessons"][1]["unknown"] == 2
          and [r["nick"] for r in m["rows"]] == ["stud", "other"] and m["rows"][0]["cells"] == {"pz1": {"seconds": 11390, "present": True}}
          and m["rows"][1]["cells"] == {}, m)

    r = c.post("/api/lessons/pz1/zoom", json={"sources": True})
    l = c.get("/api/lessons/pz1").json()
    check("sources: zoom.vtt and chat.txt stored, the chat is the lesson's, the recording linked once",
          r.status_code == 200 and {f["name"] for f in l["files"] if f["role"] == "source"} == {"zoom.vtt", "chat.txt"}
          and l["chat"] == "15:40:10\tДенис Конишев:\t+1" and [x["label"] for x in l["links"]] == ["Запис Zoom"], l)
    c.post("/api/lessons/pz1/zoom", json={"sources": True})
    check("sources again: still one link", len(c.get("/api/lessons/pz1").json()["links"]) == 1)

    c.cookies.clear()
    r = c.post("/api/lessons/pz1/zoom", json={}, headers=AGENT)
    check("agent: pull by token, the lesson updated by claude", r.status_code == 200 and c.get("/api/lessons/pz1", headers=AGENT).json()["updated_by"] == "claude", r.text)
    check("agent: the lesson's rows yes, the matrix stays the admin's", c.get("/api/lessons/pz1/attendance", headers=AGENT).json()["unknown"]
          and c.get("/api/attendance", headers=AGENT).status_code == 401)

ok = sum(1 for _, p in results if p)
print(f"\n{ok}/{len(results)} PASS")
sys.exit(0 if ok == len(results) else 1)
