"""Smoke: lab variants (T200, T354) — a card claimed by number, the same number in another lab, the demo; answer lines checked,
the teacher's marks and the defence. Run from sites/ods/api: DB_NAME=ods_smoke ~/.venvs/python-labs/bin/python tests/smoke_labs.py"""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, os.getcwd())
from pymongo import MongoClient  # noqa: E402

DB = os.environ["DB_NAME"]
assert DB.endswith("_smoke"), "refuse to run on a non-smoke DB"
mongo = MongoClient()
mongo.drop_database(DB)

results = []
TRAP = "Δy без множення на y"


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


with TestClient(main.app) as c:
    check("guest: 401", c.get("/api/variants").status_code == 401 and c.get("/api/variants/1/my").status_code == 401)
    login(c, "new@nure.ua", "pending", "КН-1")
    check("pending: 403", c.get("/api/variants/1/my").status_code == 403)

    login(c, "a@nure.ua", "student", "КН-1")
    r = c.get("/api/variants/1/my")
    check("A before naming a number: 404 asking for it", r.status_code == 404 and r.json()["detail"].startswith("Ще не знаю твого варіанта"), r.text)
    check("A: the free numbers of the stream", c.get("/api/variants/1/free").json() == {"group": "КН-1", "free": [1, 2], "same": None, "demo": False},
          c.get("/api/variants/1/free").text)
    my = c.post("/api/variants/1/my/claim", json={"n": 1}).json()
    check("A claims number 1", my["vid"] == "КН-1-01" and 'VARIANT = "КН-1-01"' in my["card"] and len(my["ask"]) == 2, my)
    check("A: the card keeps nothing of the key", "answers" not in my and "traps" not in json.dumps(my) and my["total"] == 3 and my["ok"] == 0)
    check("A: MY carries the new parts", all(k in my for k in ("way", "video", "defended", "file", "files", "facts", "grade", "live", "formats", "due", "late"))
          and my["files"] == [] and my["file"] is None and my["grade"]["work"] is None and my["formats"] == {"jupyter": False, "marimo": False, "live": False}, my)
    check("A opens again: the same card", c.get("/api/variants/1/my").json()["vid"] == "КН-1-01")
    check("A claims number 1 again: the same card", c.post("/api/variants/1/my/claim", json={"n": 1}).json()["vid"] == "КН-1-01")
    r = c.post("/api/variants/1/my/claim", json={"n": 2})
    check("A claims another number: 409 with words", r.status_code == 409 and "КН-1-01" in r.json()["detail"], r.text)
    login(c, "b@nure.ua", "student", "кн-1-3")
    check("B (group кн-1-3 of the stream КН-1): only number 2 is free", c.get("/api/variants/1/free").json()["free"] == [2])
    r = c.post("/api/variants/1/my/claim", json={"n": 1})
    check("B claims A's number: 409 with words", r.status_code == 409 and r.json()["detail"].startswith("Номер 1 уже взяв"), r.text)
    check("B claims number 2", c.post("/api/variants/1/my/claim", json={"n": 2}).json()["vid"] == "КН-1-02")
    login(c, "c@nure.ua", "student", "КН-1")
    r = c.post("/api/variants/1/my/claim", json={"n": 5})
    check("C: a number not in the list → 404 naming it", r.status_code == 404 and r.json()["detail"].startswith("Номера 5"), r.text)
    check("C: nothing free, 404 on «my»", c.get("/api/variants/1/free").json()["free"] == [] and c.get("/api/variants/1/my").status_code == 404)
    check("C: GET /api/variants says mine=false for both labs", c.get("/api/variants").json() == [{"n": 1, "mine": False}, {"n": 2, "mine": False}], c.get("/api/variants").text[:200])
    login(c, "d@nure.ua", "student", "")
    r = c.get("/api/variants/1/my")
    check("D: no group → 404 saying so", r.status_code == 404 and r.json()["detail"].startswith("У профілі немає групи"), r.text)
    login(c, "e@nure.ua", "student", "ДЕМО")
    r = c.post("/api/variants/1/my/claim", json={"n": 0})
    check("a student may not take the demo card", r.status_code == 403 and "Демо" in r.json()["detail"], r.text)

    login(c, "a@nure.ua", "student", "КН-1")
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
    my = c.put("/api/variants/1/my", json={"line": "", "notebook": "https://colab/y"}).json()
    check("A: an empty line keeps the old verdict, saves the link", my["attempts"] == 2 and my["ok"] == 1 and my["notebook"] == "https://colab/y", my)
    alerts = [e["text"] for e in mongo[DB].events.find({"kind": "lab"})]
    check("an alert per checked line: 🟢 all right, 🟠 not yet", len(alerts) == 2 and alerts[0].startswith("🟢 Лаба 1") and "3 із 3" in alerts[0]
          and alerts[1].startswith("🟠 Лаба 1") and "спроба 2" in alerts[1], alerts)
    check("A: GET /api/variants says mine=true for lab 1 only", c.get("/api/variants").json() == [{"n": 1, "mine": True}, {"n": 2, "mine": False}], c.get("/api/variants").text[:200])
    check("A: lab 2 says which number A holds", c.get("/api/variants/2/free").json()["same"] == 1)
    my2 = c.get("/api/variants/2/my").json()
    check("A: lab 2 takes the same number silently, a card of its own", my2["vid"] == "КН-1-01" and "# lab 2" in my2["card"] and my2["attempts"] == 0, my2)
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
    check("admin: free numbers are the student's word — admin has no group, may take the demo",
          c.get("/api/variants/1/free").json() == {"group": "", "free": [], "same": None, "demo": True})
    check("admin takes the demo card", c.post("/api/variants/1/my/claim", json={"n": 0}).json()["vid"] == "ДЕМО-00")
    check("admin: lab 2 takes the demo silently too", c.get("/api/variants/2/my").json()["vid"] == "ДЕМО-00")
    settings.fake_user_email = "t@nure.ua"
    c.get("/api/auth/dev-login")
    mongo[DB].users.update_one({"email": "t@nure.ua"}, {"$set": {"status": "student", "test": True}})
    check("a test student takes the demo over from the admin", c.post("/api/variants/1/my/claim", json={"n": 0}).json()["vid"] == "ДЕМО-00"
          and mongo[DB].variants.find_one({"lab": 1, "vid": "ДЕМО-00"})["student"] == "t@nure.ua")

    login(c, "a@nure.ua", "student", "КН-1")
    my = c.get("/api/variants/1/my").json()
    check("A sees the mark", my["points"] == 14 and my["note"] == "охайно" and my["defended"] == "record", my)

print(f"\n{sum(ok for _, ok in results)}/{len(results)} PASS")
sys.exit(not all(ok for _, ok in results))
