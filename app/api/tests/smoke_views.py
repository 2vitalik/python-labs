"""Smoke: the python site's own views of /table (T315 §10, table_seed.py) — what each lab's deadline asks for; the views
themselves are the platform's: core/api/tests/smoke_views.py. Run from app/api:
DB_NAME=python_labs_views_smoke ~/.venvs/python-labs/bin/python tests/smoke_views.py"""
import os
import sys

sys.path.insert(0, os.getcwd())
from pymongo import MongoClient  # noqa: E402

DB = os.environ["DB_NAME"]
assert DB.endswith("_smoke"), "refuse to run on a non-smoke DB"
MongoClient().drop_database(DB)
from fastapi.testclient import TestClient  # noqa: E402

import main  # noqa: E402
from core.config import settings  # noqa: E402

ADMIN = "admin@nure.ua"
settings.admin_emails, settings.tg_bot_token, settings.labs = ADMIN, "", 5
results = []


def check(name, cond, extra=""):
    results.append(bool(cond))
    print(("PASS " if cond else "FAIL ") + name + (f" · {extra}" if extra and not cond else ""))


with TestClient(main.app) as c:
    settings.fake_user_email = ADMIN
    c.get("/api/auth/dev-login", follow_redirects=False)
    views = {v["slug"]: v for v in c.get("/api/table").json()["views"]}
    l1, l2, l3, l5 = views["lab1"], views["lab2"], views["lab3"], views["lab5"]
    check("«Лаба 2»: lab 2, the site's columns for it (table_seed.py), its «для чого»", l2["title"] == "Лаба 2" and l2["emoji"] == "📅" and l2["query"]["lab"] == "2"
          and l2["query"]["cols"].startswith("lab,lab.review") and "gfill" in l2["query"]["cols"] and l2["about"].startswith("Дедлайн 2"), l2)
    check("«Лаба 1» asks for the registration, lab 3 — for a demo, a later lab — for the game's table", l1["query"]["cols"].startswith("reg,seen,bot,gh,repo,lab,")
          and "demo3" in l3["query"]["cols"] and "gents" in l5["query"]["cols"] and "demo" not in l5["query"]["cols"]
          and l5["about"].startswith("Дедлайн лаби"), (l1["query"], l3["query"], l5["query"]))

print(f"\n{sum(results)}/{len(results)} passed")
sys.exit(0 if all(results) else 1)
