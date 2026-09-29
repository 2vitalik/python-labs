"""Smoke: lectures and labs for signed-in students (guide_readers=active), slide borders are not drafts, pictures behind sign-in.
Run from sites/ods/api: DB_NAME=ods_smoke uv run python tests/smoke_ods.py"""
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
from core.drafts import public  # noqa: E402

results = []
BODY = "<!-- слайд 1 -->\n\n## План\n\nТекст $x_1$\n\n<!-- ще не читати -->\n\n<!-- слайд 2 -->\n\n![Хмара](/api/media/lec01/cloud.png)"


def check(name, cond, extra=""):
    results.append((name, bool(cond)))
    print(("PASS " if cond else "FAIL ") + name + (f" · {extra}" if extra and not cond else ""))


def login(c, email, status):
    settings.fake_user_email = email
    c.get("/api/auth/dev-login")
    mongo[DB].users.update_one({"email": email}, {"$set": {"status": status}})


check("drafts: a slide border stays, a note goes", public(BODY).count("<!-- слайд") == 2 and "ще не читати" not in public(BODY))
check("drafts: `<!--слайд` inside a word is still a draft", "слайдшоу" not in public("a <!-- слайдшоу --> b"))

with TestClient(main.app) as c:
    db = mongo[DB]
    db.guide.insert_one({"slug": "lec01", "title": "Тема 1. Вступ", "body": BODY, "rev": 0, "updated_by": "import"})
    db.guide.insert_one({"slug": "changes-draft", "title": "Чернетка", "body": "- рядок", "rev": 0, "updated_by": "x"})
    db.media.insert_one({"path": "lec01/cloud.png", "type": "image/png", "data": b"\x89PNG"})
    check("guest: list, page and picture 401",
          all(c.get(p).status_code == 401 for p in ("/api/guide", "/api/guide/lec01", "/api/media/lec01/cloud.png")))

    login(c, "new@nure.ua", "pending")
    check("pending: 403 until the teacher lets them in",
          all(c.get(p).status_code == 403 for p in ("/api/guide", "/api/guide/lec01", "/api/media/lec01/cloud.png")))

    login(c, "stud@nure.ua", "student")
    page = c.get("/api/guide/lec01").json()
    check("student: the page without drafts, slide borders kept",
          "ще не читати" not in page["body"] and page["body"].count("<!-- слайд") == 2, page)
    check("student: the list, the admin's draft page left out",
          [p["slug"] for p in c.get("/api/guide").json()] == ["lec01"] and c.get("/api/guide/changes-draft").status_code == 404)
    check("student: history and editing are the admin's", c.get("/api/guide/history").status_code == 403
          and c.put("/api/guide/lec01", json={"title": "x", "body": "y", "rev": 0}).status_code == 403)
    r = c.get("/api/media/lec01/cloud.png")
    check("student: the picture with its type", r.status_code == 200 and r.headers["content-type"] == "image/png" and r.content == b"\x89PNG")
    check("missing picture 404", c.get("/api/media/lec01/none.png").status_code == 404)

    login(c, "admin@nure.ua", "admin")
    check("admin: the page with its drafts", "ще не читати" in c.get("/api/guide/lec01").json()["body"])

print(f"\n{sum(ok for _, ok in results)}/{len(results)} PASS")
sys.exit(not all(ok for _, ok in results))
