"""Smoke: notebook files of a lab (T354 §5, T375) — shapes and cards from a data folder (ODS_DATA), upload → versions of the card
the teacher pinned (none pinned — refused) → the line checked as an attempt; a foreign card, line or lab, oversize files refused;
a file without a card goes to the pinned one; the same bytes again; the viewer and the original with rights
(owner, admin, agent); a re-run report and its executed copy; check() → the site with the card's token; the student's own
notebook to start; the teacher's table, review and stats; a card freed and passed on; a Colab link pulled; the deadline
against the versions (in MY and in the list of labs).
Run from sites/ods/api: DB_NAME=ods_t354_a1_smoke ~/.venvs/python-labs/bin/python tests/smoke_files.py"""
import base64
import json
import os
import subprocess
import sys
import tempfile
import time
import zlib
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, os.getcwd())
sys.path.insert(0, str(Path(__file__).parent))
from pymongo import MongoClient  # noqa: E402

import nb_fixture as fx  # noqa: E402

DB = os.environ["DB_NAME"]
assert DB.endswith("_smoke"), "refuse to run on a non-smoke DB"
mongo = MongoClient()
mongo.drop_database(DB)
os.environ |= {"AGENT_TOKENS": "claude:tok-123", "SESSION_SECRET": os.environ.get("SESSION_SECRET", "x"),
               "LAB_GATES": ""}  # every lab takes files here, whatever site.env opens to students (T368; smoke_gates.py)
results = []
TRAP = "забув множник"
PINS = "Картки варіантів закріплює викладач"
PLAIN = fx.notebook(fx.TEMPLATE[:-1])  # the template without its last cell: no card, no «LABn» print
PAST = datetime(2026, 11, 1, tzinfo=timezone.utc)


def check(name, cond, extra=""):
    results.append((name, bool(cond)))
    print(("PASS " if cond else "FAIL ") + name + (f" · {extra}" if extra and not cond else ""))


def card(group, n, lab=1):
    vid = f"{group}-{n:02d}"
    return {"lab": lab, "vid": vid, "group": group, "n": n, "card": fx.CARD.format(vid=vid), "ask": ["Чому?"],
            "answers": {"x": {"value": 2, "step": 0, "traps": [{"value": 5, "why": TRAP}]}, "y": {"value": 3, "step": 0, "traps": []}}}


data = Path(tempfile.mkdtemp())
live = list(fx.TEMPLATE)
live[2] = ("code", live[2][1] + "\n    # → /api/variants/<lab>/live")
for n, where, cells in ((1, "new", live), (2, "new", fx.TEMPLATE), (2, "site", fx.TEMPLATE[:9] + [("code", "# ✍ 1.4 ще крок")] + fx.TEMPLATE[9:])):
    lab = data / f"labs/{where}/lab{n}"
    (lab / "solved").mkdir(parents=True, exist_ok=True)
    (lab / f"lab{n}-jupyter.ipynb").write_bytes(fx.notebook(cells))
    (lab / f"solved/lab{n}-jupyter.hid.ipynb").write_bytes(fx.notebook(fx.solved()))
    (lab / f"lab{n}-marimo.py").write_text(fx.marimo(cells))
for n in (1, 2):
    for group, nums in (("КН-1", (1, 2, 3)), ("ДЕМО", (0,))):
        (data / f"labs/new/lab{n}/out/{group}").mkdir(parents=True)
        (data / f"labs/new/lab{n}/out/{group}/site.hid.json").write_text(json.dumps([card(group, k, n) for k in nums], ensure_ascii=False))
out = subprocess.run([sys.executable, "lab_io.py"], env=os.environ | {"ODS_DATA": str(data)}, check=True, capture_output=True, text=True).stdout
check("lab_io from ODS_DATA: the cards and the shapes of both labs", "нових 8" in out and "будова ноутбуків: нових 2" in out, out)
check("lab_io: lab 2's shape is the site's version", "1.4" in [t["key"] for t in mongo[DB].lab_shapes.find_one({"lab": 2})["tasks"]]
      and mongo[DB].lab_shapes.find_one({"lab": 1})["live"])

import httpx  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

import labs_pull  # noqa: E402
import main  # noqa: E402
from core.config import settings  # noqa: E402

AGENT = {"Authorization": "Bearer tok-123"}


def login(c, email, status, group=""):
    settings.fake_user_email = email
    c.get("/api/auth/dev-login")
    mongo[DB].users.update_one({"email": email}, {"$set": {"status": status, "group": group}})


def pin(c, lab, vid, email):
    """The teacher pins the card on «Результати» (T375); the student is back in after it."""
    login(c, "admin@nure.ua", "admin")
    r = c.put(f"/api/variants/{lab}/results/{vid}", json={"student": email})
    settings.fake_user_email = email
    c.get("/api/auth/dev-login")
    return r


def send(c, body, name="lab.ipynb", lab=1):
    return c.post(f"/api/variants/{lab}/my/file", files={"file": (name, body, "application/octet-stream")})


def nb(vid="КН-1-01", line="x=2 y=3", lab=1, **kw):
    return fx.notebook(fx.student(vid, lab, line), **kw)


class Bare:
    """Calls without the session cookie — a guest, an agent, a notebook's check(); one client: Mongo's client keeps to one loop."""
    def __getattr__(self, method):
        def call(url, **kw):
            saved, c.cookies = c.cookies, httpx.Cookies()
            try:
                return getattr(c, method)(url, **kw)
            finally:
                c.cookies = saved
        return call


bare = Bare()
with TestClient(main.app) as c:
    login(c, "a@nure.ua", "student", "КН-1")
    r = send(c, nb(colab=True))
    check("A before the teacher pins a card: the file → 409 with the words, nothing stored", r.status_code == 409 and r.json()["detail"].startswith(PINS)
          and mongo[DB].lab_files.count_documents({"student": "a@nure.ua"}) == 0 and not mongo[DB].variants.find_one({"student": "a@nure.ua"}), r.text)
    check("the teacher pins КН-1-01 to A", pin(c, 1, "КН-1-01", "a@nure.ua").status_code == 200)
    r = send(c, nb(colab=True))
    my = r.json()
    check("A's first file goes to the pinned card and checks its line", r.status_code == 200 and my["vid"] == "КН-1-01" and my["attempts"] == 1
          and my["ok"] == 2 and len(my["files"]) == 1 and my["file"]["line"] and my["file"]["kind"] == "ipynb", r.text[:300])
    check("A: the facts and the grade hint off the file (a one-star lab: its star is all of them)", my["facts"]["count"]["tasks"] == [2, 2]
          and my["facts"]["tool"] == "colab" and (my["grade"]["work"], my["grade"]["hint"]) == (20, 20) and my["formats"] == {"jupyter": True, "marimo": True, "live": True}, my["grade"])
    first = my["file"]["id"]
    my = send(c, nb(line="x=5 y=3")).json()
    check("A: a second version, its line a second attempt with the trap named", len(my["files"]) == 2 and my["attempts"] == 2
          and my["verdict"]["x"] == {"ok": False, "why": TRAP} and my["files"][0]["id"] != first, my["verdict"])
    r = send(c, nb(vid="КН-1-02"))
    check("A: a file with another card → 422 naming both, nothing stored", r.status_code == 422 and "КН-1-02" in r.json()["detail"]
          and "КН-1-01" in r.json()["detail"] and mongo[DB].lab_files.count_documents({}) == 2, r.text)
    r = send(c, nb(lab=2))
    check("A: lab 2's notebook (its last cell prints LAB2) handed in to lab 1 → 422 naming both labs, nothing stored", r.status_code == 422
          and r.json()["detail"].startswith("Це ноутбук лаби 2, а тут лаба 1") and mongo[DB].lab_files.count_documents({}) == 2, r.text)
    bad = fx.student("КН-1-01", 1)
    bad[-1] = ("code", bad[-1][1], [fx.say("LAB1 КН-1-02 x=2\n")], 7)
    r = send(c, fx.notebook(bad))
    check("A: a file with another variant's line → 422", r.status_code == 422 and "КН-1-02" in r.json()["detail"], r.text)
    r = send(c, b"{" + b" " * (12 * 2**20) + b"}")
    check("A: over 12 MB → 422 with words", r.status_code == 422 and "12 МБ" in r.json()["detail"], r.text[:200])
    r = send(c, b"hello", "lab.txt")
    check("A: not a notebook → 422 with words", r.status_code == 422 and "не ноутбук" in r.json()["detail"], r.text)
    my = send(c, fx.marimo(fx.student("КН-1-01", 1)).encode(), "lab.py").json()
    check("A: a marimo file — a version without a line, facts without outputs", len(my["files"]) == 3 and my["attempts"] == 2
          and my["file"]["kind"] == "marimo" and my["facts"]["ran"] is None and my["grade"]["work"] is None, my["facts"]["count"])
    marimo_id = my["file"]["id"]
    alerts = [e["text"] for e in mongo[DB].events.find({"kind": "lab"})]
    check("an alert per file", len(alerts) == 3 and "📎 ноутбук: 2/2 ✅" in alerts[0] and "підказка 20" in alerts[0] and "версія 3" in alerts[2], alerts)

    v = c.get(f"/api/variants/file/{first}").json()
    check("viewer: the notebook with roles, tasks and outputs", v["lab"] == 1 and v["vid"] == "КН-1-01" and v["tool"] == "colab"
          and [x["role"] for x in v["cells"]][:3] == ["given", "card", "service"] and v["cells"][8]["key"] == "1.2" and v["facts"]["line"], v["cells"][8])
    outs = [o["type"] for x in v["cells"] for o in x["out"]]
    check("viewer: pictures inline, html skipped", "image" in outs and "skipped" in outs and "<script" not in json.dumps(v))
    check("raw: the original, as a file", c.get(f"/api/variants/file/{first}/raw").content == nb(colab=True))
    check("guest: 401", bare.get(f"/api/variants/file/{first}").status_code == 401)
    check("agent: reads by its token", bare.get(f"/api/variants/file/{first}", headers=AGENT).status_code == 200
          and bare.get(f"/api/variants/file/{first}/raw", headers=AGENT).status_code == 200)

    login(c, "b@nure.ua", "student", "КН-1")
    check("B: A's file → 403", c.get(f"/api/variants/file/{first}").status_code == 403 and c.get(f"/api/variants/file/{first}/raw").status_code == 403)
    r, blank = send(c, nb()), send(c, PLAIN)
    check("B without a card: a file with A's card and one with no card → 409 with the words, nothing stored, A's card stays A's",
          [r.status_code, blank.status_code] == [409, 409] and r.json()["detail"].startswith(PINS) and blank.json()["detail"].startswith(PINS)
          and mongo[DB].lab_files.count_documents({"student": "b@nure.ua"}) == 0
          and mongo[DB].variants.find_one({"lab": 1, "vid": "КН-1-01"})["student"] == "a@nure.ua", (r.text, blank.text))
    check("B: runs and the table are not a student's", c.put(f"/api/variants/file/{first}/run", json={}).status_code == 403
          and c.get("/api/variants/1/files").status_code == 403 and c.get("/api/variants/1/stats").status_code == 403)
    pin(c, 1, "КН-1-02", "b@nure.ua")
    r = send(c, nb(vid="ДЕМО-00"))
    check("B: the demo card in a student's file → 422 naming it and B's card", r.status_code == 422 and "ДЕМО-00" in r.json()["detail"]
          and "КН-1-02" in r.json()["detail"], r.text)
    r = send(c, nb())
    check("B: A's card in B's file → 422 naming both, A's card stays A's", r.status_code == 422 and "КН-1-01" in r.json()["detail"]
          and "КН-1-02" in r.json()["detail"] and mongo[DB].variants.find_one({"lab": 1, "vid": "КН-1-01"})["student"] == "a@nure.ua", r.text)
    my = send(c, PLAIN).json()
    check("B: a file with no card and no «LABn» print goes to B's pinned card — a version without a line", my.get("vid") == "КН-1-02" and len(my["files"]) == 1
          and my["attempts"] == 0 and not my["file"]["line"], my)
    send(c, nb(vid="КН-1-02", line="x=5 y=4"))

    todo = bare.get("/api/variants/1/files?todo=1", headers=AGENT).json()
    check("agent: the latest version of every card, not run yet", sorted(f["vid"] for f in todo) == ["КН-1-01", "КН-1-02"]
          and next(f for f in todo if f["vid"] == "КН-1-01")["id"] == marimo_id and all(len(f["sha"]) == 64 and not f["run"] for f in todo), todo)
    executed = base64.b64encode(zlib.compress(nb())).decode()
    r = bare.put(f"/api/variants/file/{marimo_id}/run", headers=AGENT, json={"ok": True, "seconds": 3.5, "engine": "nbrun 1", "log": "done", "executed": executed})
    run = r.json()
    check("run: RUN with the re-run line judged, against the student's own line", r.status_code == 200 and run["right"] == 2 and run["total"] == 2
          and run["same"] is False and run["line"] == "LAB1 КН-1-01 x=2 y=3" and run["by"] == "claude" and run["file"] and run["errors"] == [], run)
    check("run: the executed copy is a version of its own, the student's list keeps their files only",
          mongo[DB].lab_files.count_documents({"origin": "run", "of": marimo_id}) == 1 and bare.get(f"/api/variants/file/{run['file']}", headers=AGENT).status_code == 200)
    check("run: done files leave the todo list", [f["vid"] for f in bare.get("/api/variants/1/files?todo=1", headers=AGENT).json()] == ["КН-1-02"])
    check("run: a broken executed copy → 422", bare.put(f"/api/variants/file/{marimo_id}/run", headers=AGENT, json={"executed": "xx"}).status_code == 422)

    login(c, "a@nure.ua", "student", "КН-1")
    my = c.get("/api/variants/1/my").json()
    check("A: the marimo version's facts now come from the run", my["facts"].get("from") == "run" and my["facts"]["ran"]["fresh"]
          and my["file"]["run"]["right"] == 2 and len(my["files"]) == 3, my["facts"].get("from"))
    r = c.get("/api/variants/1/my/start?as=jupyter")
    got = json.loads(r.content)
    token = mongo[DB].variants.find_one({"lab": 1, "vid": "КН-1-01"})["token"]
    check("start: Jupyter with the card and the token", r.status_code == 200 and "lab1-%D0%9A%D0%9D-1-01.ipynb" in r.headers["content-disposition"]
          and 'VARIANT = "КН-1-01"' in "".join(got["cells"][1]["source"]) and f'TOKEN = "{token}"' in "".join(got["cells"][1]["source"]) and len(token) == 12)
    m = c.get("/api/variants/1/my/start?as=marimo")
    check("start: marimo with the card at the cell's indentation", '    VARIANT = "КН-1-01"' in m.text and f'    TOKEN = "{token}"' in m.text)
    check("start: an unknown format → 422", c.get("/api/variants/1/my/start?as=word").status_code == 422)
    cards = [c.get("/api/variants/1/my").json()["card"] for _ in range(2)]
    check("token: asked twice — the same one, the one the template carries", cards[0] == cards[1] and f'TOKEN = "{token}"' in cards[0]
          and mongo[DB].variants.find_one({"lab": 1, "vid": "КН-1-01"})["token"] == token, cards)

    history = mongo[DB].history.count_documents({})
    post = lambda body, **kw: bare.post("/api/variants/1/live", content=json.dumps(body), headers={"Content-Type": "text/plain"}, **kw)  # noqa: E731
    r = post({"vid": "КН-1-01", "token": token, "name": "x", "value": 2})
    check("live: text/plain without a cookie → ok, any origin", r.status_code == 200 and r.json() == {"ok": True} and r.headers["access-control-allow-origin"] == "*")
    post({"vid": "КН-1-01", "token": token, "name": "x", "value": 5})
    check("live: a wrong token → 403, no detail", post({"vid": "КН-1-01", "token": "nope", "name": "x", "value": 2}).status_code == 403
          and post({"vid": "КН-1-02", "token": token, "name": "x", "value": 2}).status_code == 403)
    check("live: garbage → 422", post({"vid": "КН-1-01"}).status_code == 422 and bare.post("/api/variants/1/live", content=b"x" * 3000).status_code == 422)
    pre = bare.options("/api/variants/1/live")
    check("live: the preflight", pre.status_code == 204 and pre.headers["access-control-allow-origin"] == "*" and "POST" in pre.headers["access-control-allow-methods"])
    lv = c.get("/api/variants/1/my").json()["live"]
    check("live: the last value judged by the site, tries counted, no history rows", lv["names"]["x"]["ok"] is False and lv["names"]["x"]["tries"] == 2
          and lv["at"] and mongo[DB].history.count_documents({}) == history, lv)

    login(c, "admin@nure.ua", "admin")
    check("admin: reads A's file", c.get(f"/api/variants/file/{first}").status_code == 200)
    rows = {r["vid"]: r for r in c.get("/api/variants/1/results").json()}
    a = rows["КН-1-01"]
    check("results: the row with the hint, counts, the file and the number of versions", a["who"]["nick"] == "a" and a["files"] == 3
          and a["file"]["kind"] == "marimo" and a["count"]["tasks"] == [2, 2] and set(a["grade"]) == {"work", "cap", "hint"} and "facts" not in a, a)
    rv = c.get("/api/variants/1/results/КН-1-01").json()
    check("review: the key, the values, the versions, the facts, the ladder, the tasks, the neighbours",
          rv["answers"]["x"]["value"] == 2 and rv["values"] == {"x": 5, "y": 3} and len(rv["files"]) == 3 and rv["facts"]["count"]
          and len(rv["grade"]["steps"]) == 5 and [t["key"] for t in rv["shape"]["tasks"]][:2] == ["1.1", "1.2"]
          and rv["prev"] is None and rv["next"] == "КН-1-02", {k: rv[k] for k in ("prev", "next")})
    st = {s["name"]: s for s in c.get("/api/variants/1/stats").json()}
    check("stats: where they go wrong, by answer, with the cause and who", (st["x"]["ok"], st["x"]["bad"]) == (0, 2)
          and st["x"]["why"][0] == {"text": TRAP, "n": 2, "who": st["x"]["why"][0]["who"]} and {w["vid"] for w in st["x"]["why"][0]["who"]} == {"КН-1-01", "КН-1-02"}
          and (st["y"]["ok"], st["y"]["bad"]) == (1, 1), st)
    r = c.put(f"/api/variants/file/{first}/run", json={"ok": False, "line": "LAB1 КН-1-01 x=2 y=3", "errors": [{"cell": 5, "name": "E", "text": "t"}]})
    check("run: an admin may report too; errors as sent; the file's own line is what `same` compares", r.status_code == 200 and r.json()["same"] is True
          and r.json()["errors"] == [{"key": "5", "name": "E", "text": "t"}], r.text)

    nobody, to_a = c.put("/api/variants/1/results/КН-1-02", json={"student": "zz@nure.ua"}), c.put("/api/variants/1/results/КН-1-02", json={"student": "a@nure.ua"})
    check("pass a card: to nobody known → 404, to one who holds another card of the lab → 409 naming it, to its own holder — as it was",
          nobody.status_code == 404 and to_a.status_code == 409 and "КН-1-01" in to_a.json()["detail"]
          and c.put("/api/variants/1/results/КН-1-02", json={"student": "b@nure.ua"}).json()["student"] == "b@nure.ua", (nobody.text, to_a.text))
    r = c.put("/api/variants/1/results/КН-1-01", json={"student": ""})
    check("free a card: the card starts afresh", r.json()["student"] == "" and r.json()["files"] == 0 and r.json()["attempts"] == 0 and r.json()["file"] is None, r.json())
    login(c, "c@nure.ua", "student", "КН-1")
    login(c, "admin@nure.ua", "admin")
    r = c.put("/api/variants/1/results/КН-1-02", json={"student": "c@nure.ua"})
    check("pass a card on: the work goes with it", r.json()["student"] == "c@nure.ua" and r.json()["files"] == 2 and r.json()["attempts"] == 1, r.json())
    row = next(s for s in c.get("/api/students").json() if s["nick"] == "c")["variants"]["1"]
    check("the students' row: versions, the last file's time, the hint", row["files"] == 2 and row["file_at"] and "work" in row and "hint" in row, row)

    login(c, "c@nure.ua", "student", "КН-1")
    my = c.get("/api/variants/1/my").json()
    check("C holds the card and reads B's versions", my["vid"] == "КН-1-02" and len(my["files"]) == 2
          and c.get(f"/api/variants/file/{my['files'][0]['id']}").status_code == 200)
    login(c, "a@nure.ua", "student", "КН-1")
    r = c.get("/api/variants/1/my")
    check("A without a card, A's old files still A's", r.status_code == 404 and c.get(f"/api/variants/file/{first}").status_code == 200,
          f"{r.status_code} {r.text[:120]} · lab 1 КН-1-01 → {mongo[DB].variants.find_one({'lab': 1, 'vid': 'КН-1-01'})['student']!r}")

    pin(c, 1, "КН-1-01", "a@nure.ua")
    check("pull: no link saved → 422", c.post("/api/variants/1/my/pull").status_code == 422)
    c.put("/api/variants/1/my", json={"notebook": "https://colab.research.google.com/drive/1AbC-dEf_ghIJkl"})

    async def html(url):
        return b"<!doctype html>"

    async def notebook(url):
        return nb()

    labs_pull.get = html
    r = c.post("/api/variants/1/my/pull")
    check("pull: a closed file → 422 asking to open access", r.status_code == 422 and r.json()["detail"] == labs_pull.FAIL, r.text)
    labs_pull.get = notebook
    my = c.post("/api/variants/1/my/pull").json()
    check("pull: the notebook behind the link becomes a version; A's own earlier versions are A's again, counted",
          my["files"][0]["name"] == "colab.ipynb" and my["ok"] == 2 and my["attempts"] == 1 and len(my["files"]) == 4
          and mongo[DB].variants.find_one({"lab": 1, "vid": "КН-1-01"})["files"] == 4, my.get("files"))

    # lab 2, D: the deadline against the versions — out of lab 1's table and stats
    login(c, "d@nure.ua", "student", "КН-1")
    pin(c, 2, "КН-1-03", "d@nure.ua")
    mongo[DB].deadlines.insert_one({"lab": 2, "at": PAST, "groups": [], "created_at": PAST})
    brief = {"n": 2, "mine": True, "vid": "КН-1-03", "handin": "site", "handed": False, "ok": 0, "total": 2, "points": None,
             "due": "2026-11-01T00:00:00+00:00", "late": True, "in_time": False}
    my, row = c.get("/api/variants/2/my").json(), c.get("/api/variants").json()[1]
    check("D, the deadline passed, no file yet: late, not in time — in MY and in BRIEF", (my["due"], my["late"], my["in_time"]) == (brief["due"], True, False)
          and row == brief, (my["due"], my["late"], my["in_time"], row))
    mongo[DB].lab_marks.insert_one({"user": "d@nure.ua", "lab": 2, "open": True})
    my, row = c.get("/api/variants/2/my").json(), c.get("/api/variants").json()[1]
    check("extended, the date not known yet: no deadline — in MY and in BRIEF", (my["due"], my["late"], my["in_time"]) == (None, None, None)
          and row == brief | {"due": None, "late": None, "in_time": None}, (my["due"], my["late"], my["in_time"], row))
    mongo[DB].lab_marks.delete_many({})
    mongo[DB].deadlines.delete_many({})
    v1, v2 = nb("КН-1-03", "x=2 y=3", lab=2), nb("КН-1-03", "x=5 y=3", lab=2)
    send(c, v1, lab=2)
    send(c, v2, lab=2)
    card2 = mongo[DB].variants.find_one({"lab": 2, "vid": "КН-1-03"})
    due = max(card2["checked_at"], mongo[DB].lab_files.find_one({"student": "d@nure.ua"}, sort=[("at", -1)])["at"]) + timedelta(milliseconds=1)
    mongo[DB].deadlines.insert_one({"lab": 2, "at": due, "groups": [], "created_at": due})
    time.sleep(0.02)
    my = send(c, v2, lab=2).json()
    check("the newest version's bytes again, after the deadline: no new version, no attempt, the time and «on time» stay",
          len(my["files"]) == 2 and my["attempts"] == 2 and mongo[DB].variants.find_one({"lab": 2, "vid": "КН-1-03"})["checked_at"] == card2["checked_at"]
          and (my["late"], my["in_time"]) == (False, True), (len(my["files"]), my["attempts"], my["late"], my["in_time"]))
    my = send(c, v1, lab=2).json()
    check("an older version's bytes again: a new version, its line an attempt — one version before the deadline, a newer after: late, in time",
          len(my["files"]) == 3 and my["attempts"] == 3 and (my["late"], my["in_time"]) == (True, True), (len(my["files"]), my["attempts"], my["late"], my["in_time"]))
    row = c.get("/api/variants").json()[1]
    check("BRIEF after the files: handed, 2 of 2, late and in time", row == brief | {"handed": True, "ok": 2, "due": my["due"], "late": True, "in_time": True}, row)

print(f"\n{sum(ok for _, ok in results)}/{len(results)} PASS")
sys.exit(not all(ok for _, ok in results))
