"""Smoke: finds and ideas (T274 §4) — kinds, the place in the catalog and the card checked, alerts to the teacher, the
teacher's verdict — on a scratch DB. Run from app/api: DB_NAME=python_labs_smoke TG_BOT_TOKEN= uv run python tests/smoke_refs.py"""
import os
import subprocess
import sys

sys.path.insert(0, os.getcwd())
from pymongo import MongoClient  # noqa: E402

DB = os.environ["DB_NAME"]
assert DB.endswith("_smoke"), "refuse to run on a non-smoke DB"
mongo = MongoClient()
mongo.drop_database(DB)
subprocess.run(["uv", "run", "python", "catalog_io.py", "import"], check=True, capture_output=True)

from fastapi.testclient import TestClient  # noqa: E402

import main  # noqa: E402
from core.config import settings  # noqa: E402

results = []


def check(name, cond, extra=""):
    results.append(bool(cond))
    print(("PASS " if cond else "FAIL ") + name + (f" · {extra}" if extra and not cond else ""))


def login(c, email, status):
    settings.fake_user_email = email
    c.get("/api/auth/dev-login")
    mongo[DB].users.update_one({"email": email}, {"$set": {"status": status}})


def alerts():
    return [e["text"].split("\n") for e in mongo[DB].events.find({"kind": "idea"}).sort("_id")]


def post(c, **kw):
    r = c.post("/api/refs", json=kw)
    return r.json() if r.status_code == 200 else r.json()["detail"]


with TestClient(main.app) as c:
    check("guest: no refs → 401", c.get("/api/refs").status_code == 401)
    login(c, "stud@nure.ua", "student")

    link, idea = post(c, url="https://youtu.be/x"), post(c, title="Телепорт")
    check("no kind: a url → link, none → idea (as before)", link["kind"] == "link" and idea["kind"] == "idea")
    check("a link with no url → 422", isinstance(post(c, kind="link", title="x"), str))
    check("an unknown kind → 422", post(c, kind="dragon", title="x") == "Невідомий вид запису")
    check("an empty idea → 422", post(c, kind="site") == "Ідея порожня — напиши хоч рядок")

    r = post(c, kind="idea", zone="entities", subzone="move", title="Телепорт", note="крок крізь стіну")
    check("idea with its place", r["zone"] == "entities" and r["subzone"] == "move" and r["reply"] == "" and r["status"] == "inbox", r)
    check("an unknown category → 422", post(c, kind="idea", zone="nope", title="x") == "Немає такої категорії")
    check("a subcategory of another category → 422", post(c, kind="idea", zone="entities", subzone="grid", title="x")
          == "Немає такої підкатегорії в цій категорії")
    check("a subcategory with no category → 422", isinstance(post(c, kind="idea", subzone="move", title="x"), str))
    check("an unknown card → 422", post(c, kind="fix", task="no-such", title="x") == "Немає такої картки в каталозі")
    fix = post(c, kind="fix", task="console-render", title="Не там лежить")
    check("fix: the card's place filled in by the card", fix["task"] == "console-render" and fix["zone"] == "interface"
          and fix["subzone"] == "render", fix)
    site = post(c, kind="site", note="кнопка <не> тисне")
    check("site: a word on the site", site["kind"] == "site", site)

    a = alerts()
    check("alerts: idea, fix, site — not a link", len(a) == 4 and [x[0].split(" · ")[0] for x in a]
          == ["🟢 Ідея", "🟢 Ідея", "🟢 Про картку", "🟢 Про сайт"], [x[0] for x in a])
    check("alert of an idea: the category → subcategory line", a[1][1:] == ["💡 Телепорт", "🗂 Сутності → Рух", "💬 крок крізь стіну"], a[1])
    check("alert of a fix: the card's place and title", a[2][1:] == ["🛠 Не там лежить", "🗂 Інтерфейс → Поле і рендер", "🎯 Консольний рендер"], a[2])
    check("alert of a site word: no title — the kind, the note quoted", a[3][1:] == ["🐞 про сайт", "💬 кнопка &lt;не&gt; тисне"], a[3])

    r = c.put(f"/api/refs/{idea['id']}", json={"kind": "fix", "title": "Телепорт", "task": "console-render", "zone": "entities", "subzone": "move"})
    check("edit: kind, card, place kept as sent", r.status_code == 200 and r.json()["kind"] == "fix" and r.json()["zone"] == "entities"
          and r.json()["mine"] is True, r.text)
    rows = c.get("/api/refs").json()
    check("list: every row with its place and the reply", all({"zone", "subzone", "reply", "status", "mine"} <= set(x) for x in rows) and len(rows) == 5)

    check("a student's verdict → 403", c.put(f"/api/refs/{fix['id']}/verdict", json={"status": "linked"}).status_code == 403)
    login(c, "admin@nure.ua", "admin")
    n = len(alerts())
    r = c.put(f"/api/refs/{fix['id']}/verdict", json={"status": "linked", "reply": "  перенесу  "})
    check("the teacher: взято with a reply", r.status_code == 200 and r.json()["status"] == "linked" and r.json()["reply"] == "перенесу"
          and r.json()["mine"] is False, r.text)
    check("verdict: a bad status → 422", c.put(f"/api/refs/{fix['id']}/verdict", json={"status": "maybe"}).status_code == 422)
    check("verdict: an unknown ref → 404", c.put("/api/refs/000000000000000000000000/verdict", json={"status": "dropped"}).status_code == 404)
    check("verdict: in the history by the teacher, no alert", len(alerts()) == n
          and mongo[DB].history.find_one({"coll": "refs", "actor": "admin@nure.ua"})["changes"]["reply"]["new"] == "перенесу")
    login(c, "stud@nure.ua", "student")
    mine = next(x for x in c.get("/api/refs").json() if x["id"] == fix["id"])
    check("the author sees the state and the reply", mine["status"] == "linked" and mine["reply"] == "перенесу", mine)
    r = c.put(f"/api/refs/{fix['id']}", json={"kind": "fix", "task": "console-render", "title": "Не там лежить", "note": "ще"})
    check("the author's edit keeps the teacher's word", r.json()["status"] == "linked" and r.json()["reply"] == "перенесу", r.text)

ok = sum(results)
print(f"\n{ok}/{len(results)} PASS")
sys.exit(0 if ok == len(results) else 1)
