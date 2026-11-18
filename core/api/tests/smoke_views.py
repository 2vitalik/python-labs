"""Smoke: saved views v2 (T315/T316) — the site's own views made once and never brought back, version 1 on making, a new version
on a new look and the 15-minute amend with its exceptions, restore, a version named and starred, archive, delete with the versions,
where a view came from, the use count (text/plain too), folders, prefs, an old view's lazy version 1, access.
Run from a site's api folder:
DB_NAME=<db>_smoke ~/.venvs/python-labs/bin/python <repo>/core/api/tests/smoke_views.py"""
import json
import os
import sys
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.getcwd())
from pymongo import MongoClient  # noqa: E402

DB = os.environ["DB_NAME"]
assert DB.endswith("_smoke"), "refuse to run on a non-smoke DB"
MongoClient().drop_database(DB)
db = MongoClient()[DB]
from fastapi.testclient import TestClient  # noqa: E402

import main  # noqa: E402
from core import views_seed  # noqa: E402
from core.config import settings  # noqa: E402

ADMIN, VASYA = "admin@nure.ua", "vasya@nure.ua"
settings.admin_emails, settings.tg_bot_token, settings.agent_tokens, settings.labs = ADMIN, "", "claude:tok", 5
AGENT = {"Authorization": "Bearer tok"}
views_seed.DUE = True  # a site may turn «Дедлайн N» off
SEEDS = ["all", "start", "lab1", "lab2", "lab3", "lab4", "lab5", "due1", "due2", "due3", "due4", "due5"]
now = datetime.now(timezone.utc)
results = []


def check(name, cond, extra=""):
    results.append(bool(cond))
    print(("PASS " if cond else "FAIL ") + name + (f" · {extra}" if extra and not cond else ""))


vers = lambda slug: list(db.view_versions.find({"view": slug}).sort("n", 1))  # noqa: E731
hist = lambda: db.history.count_documents({"coll": "views"})  # noqa: E731
pref = lambda key: (db.prefs.find_one({"key": key}) or {}).get("value")  # noqa: E731

db.users.insert_one({"email": VASYA, "name": "vasya", "status": "student", "last_name": "Vasya", "first_name": "X", "group": "ПЗПІ-25-1", "test": False})
db.views.insert_one({"slug": "old", "title": "Старий", "emoji": "🗂", "query": {"cols": "fio"}, "order": 3, "by": ADMIN, "created_at": now - timedelta(days=9)})

with TestClient(main.app) as c:
    check("guest: no table, views, versions or count → 401", {c.get("/api/table").status_code, c.get("/api/views").status_code,
                                                                c.get("/api/views/versions").status_code, c.post("/api/views/all/seen").status_code} == {401})
    settings.fake_user_email = ADMIN
    c.get("/api/auth/dev-login", follow_redirects=False)

    t = c.get("/api/table").json()
    views = {v["slug"]: v for v in t["views"]}
    check("the site's own views made, first in order, then the old one", [v["slug"] for v in t["views"]] == [*SEEDS, "old"], list(views))
    check("prefs ride in the table", t["prefs"] == {"quiet": [], "folders": []}, t["prefs"])
    a, l2 = views["all"], views["lab2"]
    seed = {s["slug"]: s for s in views_seed.seeds(views_seed.course_labs())}  # the site may replace the columns, so they come from there
    check("«Усе»: an etalon of the site, pinned, version 1, the site's columns", a["by"] == "" and a["etalon"] and a["pinned"] and a["version"] == 1
          and a["query"] == seed["all"]["query"] and a["about"] == seed["all"]["about"], a)
    check("«Лаба 2»: lab 2, the site's columns for it, its «для чого»", l2["title"] == "Лаба 2" and l2["emoji"] == "📅" and l2["query"]["lab"] == "2"
          and l2["query"] == seed["lab2"]["query"] and l2["about"] == seed["lab2"]["about"], l2)
    check("«Лаба 1», 3, 5: the columns and «для чого» of each lab's number", all(views[s]["query"] == seed[s]["query"] and views[s]["about"] == seed[s]["about"]
                                                                               for s in ("lab1", "lab3", "lab5")), [views[s]["query"] for s in ("lab1", "lab3", "lab5")])
    check("api: every field, dates as ISO or null", {"about", "folder", "tags", "archived_at", "parent", "parent_version", "updated_at", "opens", "opened_at",
                                                     "uses", "used_at", "seconds", "order", "created_at"} <= set(a) and a["archived_at"] is None and "id" not in a, a)
    old = db.views.find_one({"slug": "old"})
    v1 = vers("old")
    check("an old view gets its version 1 lazily: its look, its author, made when it was",
          old["version"] == 1 and len(v1) == 1 and v1[0]["query"] == {"cols": "fio"} and v1[0]["by"] == ADMIN
          and v1[0]["at"].replace(tzinfo=timezone.utc) - old["created_at"].replace(tzinfo=timezone.utc) < timedelta(seconds=1), v1)
    c.get("/api/table")
    c.get("/api/views")
    check("read again: nothing doubled", db.views.count_documents({}) == len(SEEDS) + 1 and db.view_versions.count_documents({}) == len(SEEDS) + 1,
          (db.views.count_documents({}), db.view_versions.count_documents({})))

    r = c.post("/api/views/start/archive", json={"on": True}).json()
    check("archived", r["archived_at"] is not None, r)
    c.get("/api/table")
    check("an archived site's view is not made again", db.views.count_documents({"slug": "start"}) == 1)
    check("unarchived", c.post("/api/views/start/archive", json={"on": False}).json()["archived_at"] is None)
    check("a site's view deleted with its version", c.delete("/api/views/lab5").json() == {"ok": True} and vers("lab5") == [] and pref("table.seeds_gone") == ["lab5"])
    check("…and never made again", "lab5" not in [v["slug"] for v in c.get("/api/table").json()["views"]])
    check("a built-in slug is taken → -2; a deleted one is free", c.post("/api/views", json={"title": "lab1"}).json()["slug"] == "lab1-2"
          and c.post("/api/views", json={"title": "lab5"}).json()["slug"] == "lab5")
    c.delete("/api/views/lab5")
    check("deleting the slug again does not double the list", pref("table.seeds_gone") == ["lab5"], pref("table.seeds_gone"))

    check("view needs a title → 422", c.post("/api/views", json={"title": " "}).status_code == 422)
    check("13 tags, a long «для чого» or folder → 422", c.post("/api/views", json={"title": "x", "tags": [str(i) for i in range(13)]}).status_code == 422
          and c.post("/api/views", json={"title": "x", "about": "a" * 501}).status_code == 422 and c.post("/api/views", json={"title": "x", "folder": "f" * 61}).status_code == 422)
    r = c.post("/api/views", json={"title": "Боржники", "emoji": "🔥", "query": {"cols": "fio", "lab": 2, "junk": 1}, "about": " для дедлайну ", "folder": "  Дедлайни ",
                                   "tags": ["a", " a ", "", "#b"], "etalon": True, "parent": "lab2", "parent_version": 1, "note": "перша"}).json()
    check("made: cleaned, from «Лаба 2» v1, version 1 with its note", r["slug"] == "borzhnyky" and r["query"] == {"cols": "fio", "lab": "2"} and r["about"] == "для дедлайну"
          and r["folder"] == "Дедлайни" and r["tags"] == ["a", "b"] and r["parent"] == "lab2" and r["parent_version"] == 1 and r["version"] == 1 and r["by"] == "admin"
          and [(x["n"], x["note"]) for x in vers("borzhnyky")] == [(1, "перша")], r)
    check("its folder joins the list", pref("table.folders") == ["Дедлайни"], pref("table.folders"))

    def look(cols, body=None, h=None):
        return c.put("/api/views/borzhnyky", json={"query": {"cols": cols}} | (body or {}), headers=h or {}).json()

    check("a new look → version 2 (version 1 is never amended)", look("fio,seen")["version"] == 2)
    check("the same person again within 15 minutes → version 2 amended", look("fio,seen,bot")["version"] == 2 and vers("borzhnyky")[-1]["query"] == {"cols": "fio,seen,bot"})
    h0 = hist()
    r = c.put("/api/views/borzhnyky", json={"about": "інше", "tags": ["c"], "pinned": False}).json()
    check("only the fields sent; no version for them; history and updated_at", r["about"] == "інше" and r["tags"] == ["c"] and not r["pinned"] and r["etalon"]
          and r["emoji"] == "🔥" and r["query"] == {"cols": "fio,seen,bot"} and r["version"] == 2 and r["updated_at"] and hist() == h0 + 1, r)
    check("the same look again → no version, no history", look("fio,seen,bot")["version"] == 2 and hist() == h0 + 1)
    check("another person → a new version", look("fio,seen,bot,gh", h=AGENT)["version"] == 3 and vers("borzhnyky")[-1]["by"] == "claude@agent")
    check("back to me → new, then amended", look("fio")["version"] == 4 and look("fio,tg")["version"] == 4)
    check("a note → always a new version", look("fio,tg,gh", {"note": "додав GitHub"})["version"] == 5 and vers("borzhnyky")[-1]["note"] == "додав GitHub")
    check("the last one has a note → not amended", look("fio,gh")["version"] == 6)
    r = c.put("/api/views/borzhnyky/versions/6", json={"star": True}).json()
    check("a version starred", r["star"] and r["n"] == 6 and r["name"] == "" and r["by"] == "admin", r)
    check("a starred last → not amended", look("fio,repo")["version"] == 7)
    r = c.put("/api/views/borzhnyky/versions/7", json={"name": "  до   дедлайну "}).json()
    check("a version named; star untouched", r["name"] == "до дедлайну" and not r["star"], r)
    check("a named last → not amended", look("fio,repo,gh")["version"] == 8)
    kid = c.post("/api/views", json={"title": "Дитина", "query": {"cols": "fio"}, "parent": "borzhnyky", "parent_version": 8}).json()
    check("a view made of version 8 → it is not amended", kid["parent_version"] == 8 and look("fio,gh,bot")["version"] == 9)
    db.view_versions.update_one({"view": "borzhnyky", "n": 9}, {"$set": {"at": now - timedelta(minutes=20)}})
    check("older than 15 minutes → not amended", look("fio,bot")["version"] == 10)
    check("a note alone, the look the same → a version too", c.put("/api/views/borzhnyky", json={"note": "просто нотатка"}).json()["version"] == 11)
    check("an empty title → 422, a bad version → 404", c.put("/api/views/borzhnyky", json={"title": ""}).status_code == 422
          and c.put("/api/views/borzhnyky/versions/99", json={"star": True}).status_code == 404 and c.put("/api/views/nope", json={"title": "x"}).status_code == 404)

    r = c.post("/api/views/borzhnyky/versions/2/restore").json()
    v12 = vers("borzhnyky")[-1]
    check("restore: version 2's look on top as 12", r["version"] == 12 and r["query"] == {"cols": "fio,seen,bot"} and v12["n"] == 12
          and v12["note"] == "повернуто версію 2" and v12["query"] == {"cols": "fio,seen,bot"}, (r, v12))
    check("restore an unknown version → 404", c.post("/api/views/borzhnyky/versions/99/restore").status_code == 404)
    vs = c.get("/api/views/versions").json()["versions"]
    check("all versions, by view and number", [(x["view"], x["n"]) for x in vs] == sorted((x["view"], x["n"]) for x in vs) and len(vs) == db.view_versions.count_documents({})
          and {"view", "n", "title", "emoji", "query", "name", "note", "star", "by", "at"} == set(vs[0]), vs[0])

    h0, before = hist(), db.views.find_one({"slug": "borzhnyky"})
    c.post("/api/views/borzhnyky/seen", json={"open": True})
    c.post("/api/views/borzhnyky/seen", content=json.dumps({"use": True, "seconds": 9999}), headers={"Content-Type": "text/plain"})
    c.post("/api/views/borzhnyky/seen", json={"seconds": -5})
    after = db.views.find_one({"slug": "borzhnyky"})
    check("count: opened, used (text/plain body), seconds capped at an hour", after["opens"] == 1 and after["uses"] == 1 and after["seconds"] == 3600
          and after["opened_at"] and after["used_at"], after)
    check("count: no history, no updated_at", hist() == h0 and after["updated_at"] == before["updated_at"])
    check("count: not JSON → 422, unknown view → 404", c.post("/api/views/borzhnyky/seen", content="nope", headers={"Content-Type": "text/plain"}).status_code == 422
          and c.post("/api/views/nope/seen", json={}).status_code == 404)

    r = c.post("/api/views/folders", json={"folders": ["Порожня"]}).json()
    check("folders: the order kept, a folder in use not lost", r["folders"] == ["Порожня", "Дедлайни"] and len(r["views"]) == db.views.count_documents({}), r["folders"])
    r = c.post("/api/views/folders", json={"rename": ["Дедлайни", "Строки"]}).json()
    check("rename: the list and the views", r["folders"] == ["Порожня", "Строки"] and db.views.find_one({"slug": "borzhnyky"})["folder"] == "Строки", r["folders"])
    r = c.post("/api/views/folders", json={"rename": ["Строки", ""]}).json()
    check("rename to nothing: the folder goes, its views go up", r["folders"] == ["Порожня"] and db.views.find_one({"slug": "borzhnyky"})["folder"] == "", r["folders"])
    c.put("/api/views/old", json={"folder": "Нова"})
    check("a view saved into a new folder → it goes last", pref("table.folders") == ["Порожня", "Нова"], pref("table.folders"))
    check("a bad rename → 422", c.post("/api/views/folders", json={"rename": ["x"]}).status_code == 422)

    r = c.put("/api/table/prefs", json={"quiet": ["lab.after", " lab.after ", "", "commits"]}).json()
    check("prefs: quiet cleaned", r == {"quiet": ["lab.after", "commits"], "folders": ["Порожня", "Нова"]}, r)
    check("prefs: nothing sent → nothing changed", c.put("/api/table/prefs", json={}).json()["quiet"] == ["lab.after", "commits"])
    check("prefs in the table", c.get("/api/table").json()["prefs"]["quiet"] == ["lab.after", "commits"])

    r = c.post("/api/views/order", json={"slugs": ["borzhnyky", "all"]}).json()
    check("order: the named ones first", [v["slug"] for v in r["views"]][:2] == ["borzhnyky", "all"], [v["slug"] for v in r["views"]])
    check("deleted for good with all 12 versions; not a site's view", c.delete("/api/views/borzhnyky").json() == {"ok": True} and vers("borzhnyky") == []
          and pref("table.seeds_gone") == ["lab5"] and c.delete("/api/views/borzhnyky").status_code == 404)

    settings.fake_user_email = VASYA
    c.get("/api/auth/dev-login", follow_redirects=False)
    check("a student: views, versions, prefs, count → 403", {c.get("/api/views").status_code, c.get("/api/views/versions").status_code,
                                                            c.put("/api/table/prefs", json={}).status_code, c.post("/api/views/all/seen", json={}).status_code,
                                                            c.post("/api/views/folders", json={}).status_code} == {403})

print(f"\n{sum(results)}/{len(results)} passed")
sys.exit(0 if all(results) else 1)
