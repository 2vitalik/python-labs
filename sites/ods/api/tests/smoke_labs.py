"""Smoke: lab variants (T200, T354, T375) — the teacher pins a card, the same number in every lab at once, the students left
without one; the demo by a click in each lab; answer lines checked, links, the deadline in MY and in the list of labs (BRIEF),
the teacher's marks and the defence.
Run from sites/ods/api: DB_NAME=ods_smoke ~/.venvs/python-labs/bin/python tests/smoke_labs.py"""
import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, os.getcwd())
from pymongo import MongoClient  # noqa: E402

DB = os.environ["DB_NAME"]
assert DB.endswith("_smoke"), "refuse to run on a non-smoke DB"
mongo = MongoClient()
mongo.drop_database(DB)
os.environ["LAB_GATES"] = ""  # every lab takes lines and files here, whatever site.env opens to students (T368; smoke_gates.py)

results = []
TRAP = "Δy без множення на y"
PINS = "Картки варіантів закріплює викладач"
BRIEF = {"mine": True, "vid": "КН-1-01", "handin": "site", "handed": False, "ok": 0, "total": 3, "points": None, "due": None, "late": None, "in_time": None}
DUE = datetime(2026, 11, 1, tzinfo=timezone.utc)


def check(name, cond, extra=""):
    results.append((name, bool(cond)))
    print(("PASS " if cond else "FAIL ") + name + (f" · {extra}" if extra and not cond else ""))


def variant(group, n, lab=1):
    return {"lab": lab, "vid": f"{group}-{n:02d}", "group": group, "n": n, "card": f'VARIANT = "{group}-{n:02d}"\nX = {n}  # lab {lab}',
            "ask": ["Питання А?", "Питання Б?"],
            "answers": {"d1": {"value": 0.2049, "step": 0.002, "traps": [{"value": 0.1, "why": TRAP}]},
                        "pi": {"value": 3, "step": 0, "traps": []}, "out": {"value": 1, "step": 0, "traps": []}}}


snap = Path(tempfile.mkdtemp()) / "site.hid.json"
snap.write_text(json.dumps([variant("КН-1", 1), variant("КН-1", 2), variant("ДЕМО", 0), variant("КН-1", 1, lab=2), variant("ДЕМО", 0, lab=2)], ensure_ascii=False))
run = lambda: subprocess.run([sys.executable, "lab_io.py", str(snap)], check=True, capture_output=True, text=True).stdout  # no `uv run`: it would re-sync a venv shared with running servers
check("import: five new variants — the same vid in two labs lives twice", "нових 5" in run())
check("import again: nothing changes", "без змін 5" in run())

from fastapi.testclient import TestClient  # noqa: E402

import main  # noqa: E402
from core.config import settings  # noqa: E402


def login(c, email, status, group=""):
    settings.fake_user_email = email
    c.get("/api/auth/dev-login")
    mongo[DB].users.update_one({"email": email}, {"$set": {"status": status, "group": group}})


def card(lab, vid):
    return mongo[DB].variants.find_one({"lab": lab, "vid": vid})


def loose(c, lab):
    got = c.get(f"/api/variants/{lab}/loose").json()
    return sorted(s["email"] for s in got["students"]), got["free"], got


with TestClient(main.app) as c:
    check("guest: 401", c.get("/api/variants").status_code == 401 and c.get("/api/variants/1/my").status_code == 401)
    login(c, "new@nure.ua", "pending", "КН-1")
    check("pending: 403", c.get("/api/variants/1/my").status_code == 403)
    for email, group in (("b@nure.ua", "кн-1-3"), ("c@nure.ua", "КН-1"), ("d@nure.ua", ""), ("e@nure.ua", "ДЕМО"), ("t@nure.ua", "")):
        login(c, email, "student", group)
    mongo[DB].users.update_one({"email": "t@nure.ua"}, {"$set": {"test": True}})

    login(c, "a@nure.ua", "student", "КН-1")
    r = c.get("/api/variants/1/my")
    check("A before the teacher pins a card: 404 saying who pins them", r.status_code == 404 and r.json()["detail"].startswith(PINS), r.text)
    r = c.get("/api/variants/1/my?soft=1")
    check("A: «my» asked softly — 200 with no card, the words, no demo for a student", r.status_code == 200 and r.json()["vid"] is None
          and r.json()["why"].startswith(PINS) and r.json()["demo"] is None, r.text)
    free, claim = c.get("/api/variants/1/free"), c.post("/api/variants/1/my/claim", json={"n": 1})
    check("a student's own pick is gone: /free and /my/claim — no such route, no card taken", (free.status_code, claim.status_code) == (404, 404)
          and free.json() == claim.json() == {"detail": "Not Found"} and not card(1, "КН-1-01")["student"], (free.text, claim.text))
    r = c.put("/api/variants/1/my", json={"line": "LAB1 КН-1-01 d1=0.2049"})
    check("A without a card: a line naming one → 404 with the words, the card stays free", r.status_code == 404 and r.json()["detail"].startswith(PINS)
          and not card(1, "КН-1-01")["student"], r.text)
    check("A: pinning is the teacher's — the students without a card and a pin → 403", c.get("/api/variants/1/loose").status_code == 403
          and c.put("/api/variants/1/results/КН-1-01", json={"student": "a@nure.ua"}).status_code == 403)

    login(c, "admin@nure.ua", "admin")
    r = c.put("/api/variants/1/results/КН-1-01", json={"student": "a@nure.ua"})
    check("the teacher pins КН-1-01 to A", r.status_code == 200 and r.json()["student"] == "a@nure.ua" and r.json()["assigned_at"], r.text)
    two = card(2, "КН-1-01")
    check("…and A holds number 1 of lab 2 at once, before opening it — by the teacher's hand in history", two["student"] == "a@nure.ua" and two["assigned_at"]
          and mongo[DB].history.find_one({"coll": "variants", "doc_id": two["_id"]})["actor"] == "admin@nure.ua", two)
    history = mongo[DB].history.count_documents({"coll": "variants"})
    r = c.put("/api/variants/1/results/КН-1-01", json={"student": "a@nure.ua"})
    check("A's own card pinned again: nothing changes", r.status_code == 200 and r.json()["student"] == "a@nure.ua"
          and mongo[DB].history.count_documents({"coll": "variants"}) == history, r.text)
    r = c.put("/api/variants/1/results/КН-1-02", json={"student": "a@nure.ua"})
    check("a second card of lab 1 to A → 409 naming A's card, the other stays free", r.status_code == 409 and "КН-1-01" in r.json()["detail"]
          and not card(1, "КН-1-02")["student"], r.text)
    r = c.put("/api/variants/1/results/КН-1-02", json={"student": "zz@nure.ua"})
    check("a card to an email the site does not know → 404 naming it", r.status_code == 404 and "zz@nure.ua" in r.json()["detail"]
          and not card(1, "КН-1-02")["student"], r.text)
    check("a card the lab has not → 404", c.put("/api/variants/1/results/КН-1-05", json={"student": "c@nure.ua"}).status_code == 404)
    r = c.put("/api/variants/1/results/ДЕМО-00", json={"student": "c@nure.ua"})
    check("the demo card to an ordinary student → 409 with words, the demo stays free", r.status_code == 409 and r.json()["detail"].startswith("Демо-картка — лише")
          and not card(1, "ДЕМО-00")["student"], r.text)
    who, free, got = loose(c, 1)
    check("loose: the students without a card of lab 1 — not A, not the test one, not the pending one, not the teacher",
          who == ["b@nure.ua", "c@nure.ua", "d@nure.ua", "e@nure.ua"] and all(s["nick"] and s["status"] == "student" and not s["test"] for s in got["students"]), got)
    check("loose: the free cards — not A's, not the demo", free == ["КН-1-02"], got)
    check("loose of lab 2: A's number came along, the demo is not one to pin — nothing free", loose(c, 2)[1] == [], loose(c, 2))
    r = c.put("/api/variants/1/results/КН-1-02", json={"student": "b@nure.ua"})
    check("the teacher pins КН-1-02 to B (group кн-1-3: the group plays no part); lab 2 has no number 2 — nothing more",
          r.status_code == 200 and r.json()["student"] == "b@nure.ua" and mongo[DB].variants.count_documents({"student": "b@nure.ua"}) == 1, r.text)
    check("loose after: C, D and E; nothing free", loose(c, 1)[:2] == (["c@nure.ua", "d@nure.ua", "e@nure.ua"], []), loose(c, 1))

    login(c, "b@nure.ua", "student", "кн-1-3")
    r = c.get("/api/variants/2/my")
    check("B: the pinned card on «Моя лаба»; lab 2 without number 2 — no card there", c.get("/api/variants/1/my").json()["vid"] == "КН-1-02"
          and r.status_code == 404 and r.json()["detail"].startswith(PINS), r.text)
    login(c, "c@nure.ua", "student", "КН-1")
    check("C: no card pinned, 404 on «my»", c.get("/api/variants/1/my").status_code == 404)
    check("C: GET /api/variants says mine=false for both labs", c.get("/api/variants").json() == [{"n": 1, "mine": False}, {"n": 2, "mine": False}], c.get("/api/variants").text[:200])
    login(c, "d@nure.ua", "student", "")
    r = c.get("/api/variants/1/my")
    check("D without a group: the same words — the profile's group plays no part", r.status_code == 404 and r.json()["detail"].startswith(PINS), r.text)
    soft = c.get("/api/variants/1/my?soft=1").json()
    check("D: «my» softly — no card, no demo offered", soft["vid"] is None and soft["demo"] is None, soft)
    login(c, "e@nure.ua", "student", "ДЕМО")
    r = c.post("/api/variants/1/my/demo")
    check("a student, even of group ДЕМО, may not open the demo — 403 with words, the demo stays free", r.status_code == 403 and "Демо" in r.json()["detail"]
          and not card(1, "ДЕМО-00")["student"], r.text)

    login(c, "a@nure.ua", "student", "КН-1")
    check("A's labs before anything is handed in: BRIEF on each — the card, here, nothing handed, no deadline",
          c.get("/api/variants").json() == [{"n": n} | BRIEF for n in (1, 2)], c.get("/api/variants").text)
    my = c.get("/api/variants/1/my").json()
    check("A: the pinned card on «Моя лаба»", my["vid"] == "КН-1-01" and 'VARIANT = "КН-1-01"' in my["card"] and len(my["ask"]) == 2, my)
    check("A: the card keeps nothing of the key", "answers" not in my and "traps" not in json.dumps(my) and my["total"] == 3 and my["ok"] == 0)
    check("A: MY carries the new parts", all(k in my for k in ("way", "video", "defended", "file", "files", "facts", "grade", "live", "formats", "due", "late", "in_time"))
          and my["files"] == [] and my["file"] is None and my["grade"]["work"] is None and my["formats"] == {"jupyter": False, "marimo": False, "live": False}
          and (my["due"], my["late"], my["in_time"]) == (None, None, None), my)
    check("A opens again: the same card", c.get("/api/variants/1/my").json()["vid"] == "КН-1-01")
    my = c.put("/api/variants/1/my", json={"line": "LAB1 КН-1-01  d1=0.2049 pi=3 out=1.0", "notebook": " https://colab/x "}).json()
    check("A: a correct line → all ok, attempt 1", my["ok"] == 3 and my["attempts"] == 1 and all(v["ok"] for v in my["verdict"].values()) and my["notebook"] == "https://colab/x", my)
    my = c.put("/api/variants/1/my", json={"line": "LAB1 КН-1-01 d1=0.1 pi=3", "notebook": ""}).json()
    check("A: a trap value is named, a missing one marked", my["verdict"]["d1"] == {"ok": False, "why": TRAP} and my["verdict"]["out"]["why"] == "нема в рядку"
          and my["ok"] == 1 and my["attempts"] == 2, my)
    r = c.put("/api/variants/1/my", json={"line": "LAB1 КН-1-02 d1=0.2049", "notebook": ""})
    check("A: somebody else's line → 422", r.status_code == 422 and "КН-1-02" in r.json()["detail"] and "КН-1-01" in r.json()["detail"], r.text)
    r = c.put("/api/variants/1/my", json={"line": "hello", "notebook": ""})
    check("A: garbage → 422", r.status_code == 422 and "LAB" in r.json()["detail"], r.text)
    r = c.put("/api/variants/1/my", json={"line": "LAB1 КН-1-01 d1=abc", "notebook": ""})
    check("A: a non-number → 422 naming the pair", r.status_code == 422 and "d1=abc" in r.json()["detail"], r.text)
    before = c.get("/api/variants/1/my").json()
    my = c.put("/api/variants/1/my", json={"line": " LAB1  КН-1-01 d1=0.1   pi=3 "}).json()
    check("A: the same line again is not one more attempt — the attempts, the verdict and the time stay", my["attempts"] == 2
          and my["checked_at"] == before["checked_at"] and my["verdict"] == before["verdict"], (my["attempts"], my["checked_at"], before["checked_at"]))
    bad = [c.put("/api/variants/1/my", json={k: v, "line": "LAB1 КН-1-01 d1=0.2049"}) for k, v in (("notebook", "colab.research.google.com/x"), ("video", "youtu.be/x"))]
    now = c.get("/api/variants/1/my").json()
    check("A: a link not starting with https:// → 422 with the words, nothing of the request kept; an empty one cleared the old",
          all(r.status_code == 422 and r.json()["detail"] == "Посилання має починатися з https://" for r in bad)
          and (now["notebook"], now["video"], now["attempts"]) == ("", "", 2), [r.text for r in bad])
    my = c.put("/api/variants/1/my", json={"line": "", "notebook": "https://colab/y"}).json()
    check("A: an empty line keeps the old verdict, saves the link", my["attempts"] == 2 and my["ok"] == 1 and my["notebook"] == "https://colab/y", my)
    alerts = [e["text"] for e in mongo[DB].events.find({"kind": "lab"})]
    check("an alert per checked line: 🟢 all right, 🟠 not yet", len(alerts) == 2 and alerts[0].startswith("🟢 Лаба 1") and "3 із 3" in alerts[0]
          and alerts[1].startswith("🟠 Лаба 1") and "спроба 2" in alerts[1], alerts)
    check("A's labs after a line: lab 1 handed, 1 of 3 right; lab 2 untouched", c.get("/api/variants").json()
          == [{"n": 1} | BRIEF | {"handed": True, "ok": 1}, {"n": 2} | BRIEF], c.get("/api/variants").text)
    mongo[DB].deadlines.insert_one({"lab": 1, "at": DUE, "groups": [], "created_at": DUE})
    my, labs = c.get("/api/variants/1/my").json(), c.get("/api/variants").json()
    check("a deadline passed, no file: late, not in time — in MY and in BRIEF; lab 2 without a deadline",
          (my["due"], my["late"], my["in_time"]) == ("2026-11-01T00:00:00+00:00", True, False)
          and labs == [{"n": 1} | BRIEF | {"handed": True, "ok": 1, "due": my["due"], "late": True, "in_time": False}, {"n": 2} | BRIEF], (my["due"], my["late"], my["in_time"], labs))
    mongo[DB].lab_marks.insert_one({"user": "a@nure.ua", "lab": 1, "open": True})
    my, labs = c.get("/api/variants/1/my").json(), c.get("/api/variants").json()
    check("extended, the date not known yet: no deadline — nothing late, in MY and in BRIEF", (my["due"], my["late"], my["in_time"]) == (None, None, None)
          and labs[0] == {"n": 1} | BRIEF | {"handed": True, "ok": 1}, (my["due"], my["late"], my["in_time"], labs[0]))
    mongo[DB].lab_marks.delete_many({})
    mongo[DB].deadlines.delete_many({})
    my2 = c.get("/api/variants/2/my").json()
    check("A: lab 2 — the same number, a card of its own", my2["vid"] == "КН-1-01" and "# lab 2" in my2["card"] and my2["attempts"] == 0, my2)
    check("A: lab 1 is still A's, with the line", c.get("/api/variants/1/my").json()["attempts"] == 2)
    my = c.put("/api/variants/1/my", json={"way": "live", "video": " https://youtu.be/x "}).json()
    check("A: the form of defence and the video; absent fields stay", my["way"] == "live" and my["video"] == "https://youtu.be/x"
          and my["notebook"] == "https://colab/y" and my["attempts"] == 2 and my["grade"]["cap"] == 20, my)
    check("A: a form of defence not in the list → 422", c.put("/api/variants/1/my", json={"way": "zoom"}).status_code == 422)
    check("A: results are the teacher's", c.get("/api/variants/1/results").status_code == 403
          and c.put("/api/variants/1/results/КН-1-01", json={"points": 20}).status_code == 403)

    login(c, "admin@nure.ua", "admin")
    rows = c.get("/api/variants/1/results").json()
    check("admin: three rows of lab 1, students joined", len(rows) == 3 and rows[1]["vid"] == "КН-1-01" and rows[1]["who"]["nick"] == "a" and rows[1]["ok"] == 1
          and rows[0]["vid"] == "ДЕМО-00" and rows[0]["who"] is None, rows)
    r = c.put("/api/variants/1/results/КН-1-01", json={"points": 14, "note": " охайно "})
    check("admin: marks saved", r.status_code == 200 and r.json()["points"] == 14 and r.json()["note"] == "охайно", r.text)
    check("admin: 21 points → 422", c.put("/api/variants/1/results/КН-1-01", json={"points": 21, "note": ""}).status_code == 422)
    check("admin: unknown variant → 404", c.put("/api/variants/1/results/КН-9-01", json={"points": 1, "note": ""}).status_code == 404)
    check("history keeps the trail", mongo[DB].history.count_documents({"coll": "variants"}) >= 5)
    r = c.put("/api/variants/1/results/КН-1-01", json={"defended": "record", "stars": 2})
    check("admin: the defence and the stars; the points stay", r.json()["defended"] == "record" and r.json()["stars"] == 2 and r.json()["points"] == 14
          and r.json()["grade"]["cap"] == 16, r.text)
    check("admin: a defence not in the list → 422", c.put("/api/variants/1/results/КН-1-01", json={"defended": "zoom"}).status_code == 422)
    soft = c.get("/api/variants/1/my?soft=1").json()
    check("admin: «my» softly — no card of the stream's, the demo offered", soft["vid"] is None and soft["why"].startswith(PINS) and soft["demo"] == "ДЕМО-00", soft)
    check("admin opens the demo card", c.post("/api/variants/1/my/demo").json()["vid"] == "ДЕМО-00")
    c.put("/api/variants/1/my", json={"line": "LAB1 ДЕМО-00 d1=0.1"})
    r, soft = c.get("/api/variants/2/my"), c.get("/api/variants/2/my?soft=1").json()
    check("admin: lab 1's demo is not lab 2's — no card there until its own click, the demo offered", r.status_code == 404 and soft["demo"] == "ДЕМО-00"
          and not card(2, "ДЕМО-00")["student"], r.text)
    check("admin: lab 2's own click — its demo", c.post("/api/variants/2/my/demo").json()["vid"] == "ДЕМО-00" and card(2, "ДЕМО-00")["student"] == "admin@nure.ua")
    check("the teacher holding the demo is not loose, the demo never free to pin", loose(c, 1)[:2] == (["c@nure.ua", "d@nure.ua", "e@nure.ua"], []))
    settings.fake_user_email = "t@nure.ua"
    c.get("/api/auth/dev-login")
    soft = c.get("/api/variants/1/my?soft=1").json()
    check("a test student without a group is offered the demo", soft["vid"] is None and soft["demo"] == "ДЕМО-00", soft)
    my = c.post("/api/variants/1/my/demo").json()
    check("a test student takes the demo over from the admin — afresh, the admin's line is not theirs", my["vid"] == "ДЕМО-00"
          and mongo[DB].variants.find_one({"lab": 1, "vid": "ДЕМО-00"})["student"] == "t@nure.ua" and my["attempts"] == 0 and my["line"] == "", my)

    login(c, "a@nure.ua", "student", "КН-1")
    my = c.get("/api/variants/1/my").json()
    check("A sees the mark — on «Моя лаба» and in the list", my["points"] == 14 and my["note"] == "охайно" and my["defended"] == "record"
          and c.get("/api/variants").json()[0]["points"] == 14, my)

print(f"\n{sum(ok for _, ok in results)}/{len(results)} PASS")
sys.exit(not all(ok for _, ok in results))
