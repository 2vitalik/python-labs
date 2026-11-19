"""Smoke: import of the ods texts through the API (T357) — who may; pages new · updated · same; files, their reading and limits;
the list of the labs' pages; what the site has; the staff's pages (`guide_staff`) and their files; «Очима студента» in one click.
All data made up. Run from sites/ods/api: DB_NAME=ods_content_smoke SESSION_SECRET=x ~/.venvs/python-labs/bin/python tests/smoke_content.py"""
import hashlib
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, os.getcwd())
from pymongo import MongoClient  # noqa: E402

DB = os.environ["DB_NAME"]
assert DB.endswith("_smoke"), "refuse to run on a non-smoke DB"
mongo = MongoClient()
mongo.drop_database(DB)
db = mongo[DB]

from fastapi.testclient import TestClient  # noqa: E402

import main  # noqa: E402
from core import guide_io  # noqa: E402
from core.config import settings  # noqa: E402

settings.agent_tokens, settings.guide_staff, settings.guide_readers = "smoke:tok-smoke", "old-", "active"
guide_io.ROOT = Path(tempfile.mkdtemp())  # no seed: the site's guide files are the site's
AGENT = {"Authorization": "Bearer tok-smoke"}
PNG, PNG2 = b"\x89PNG smoke", b"\x89PNG smoke 2"
ROWS = [{"slug": "lab9", "kind": "lab", "lab": 9, "part": "", "nav": "Умова", "order": 0,
         "files": [{"name": "n.ipynb", "title": "Ноутбук", "url": "/api/media/files/lab9/n.ipynb"}]},
        {"slug": "lab9-guide", "kind": "lab", "lab": 9, "part": "guide", "nav": "Розбір", "order": 1, "files": []},
        {"slug": "labs-faq", "kind": "common", "lab": None, "part": "faq", "nav": "Питання", "order": 8, "files": []}]
results = []


def check(name, cond, extra=""):
    results.append((name, bool(cond)))
    print(("PASS " if cond else "FAIL ") + name + (f" · {extra}" if extra and not cond else ""))


def login(c, email, status):
    settings.fake_user_email = email
    c.get("/api/auth/dev-login")
    db.users.update_one({"email": email}, {"$set": {"status": status}})


def calls(c, **kw):
    return [c.get("/api/content", **kw).status_code, c.put("/api/content/pages/lab9", json={"title": "x", "body": "y"}, **kw).status_code,
            c.put("/api/content/media/lab9/x.png", content=PNG, **kw).status_code, c.put("/api/content/labpages", json=ROWS, **kw).status_code]


def page(c, slug, title, body, note="", **kw):
    r = c.put(f"/api/content/pages/{slug}", json={"title": title, "body": body, "note": note}, headers=AGENT, **kw)
    return r.json() if r.status_code == 200 else r.status_code


def media(c, path, data, kind="image/png"):
    r = c.put(f"/api/content/media/{path}", content=data, headers=AGENT | {"Content-Type": kind})
    return r.json()["state"] if r.status_code == 200 else r.status_code


def staff(c, **kw):
    """old-lab1 — in the list, the page, its picture, its file."""
    return ("old-lab1" in [p["slug"] for p in c.get("/api/guide", **kw).json()],
            *(c.get(p, **kw).status_code for p in ("/api/guide/old-lab1", "/api/media/old-lab1/x.png", "/api/media/files/old-lab1/n.ipynb")))


with TestClient(main.app) as c:
    check("guest: what the site has, a page, a file, the list → 401", calls(c) == [401] * 4, calls(c))
    login(c, "stud@nure.ua", "student")
    check("student: the same → 403", calls(c) == [403] * 4, calls(c))
    check("student: nothing written", db.guide.count_documents({}) == db.media.count_documents({}) == db.lab_pages.count_documents({}) == 0)
    c.cookies.clear()

    check("agent: a new page", page(c, "lab9", " Лаба 9 ", "текст\n") == {"state": "new", "rev": 0})
    g = db.guide.find_one({"slug": "lab9"})
    check("… stripped, by the agent, its birth in history", (g["title"], g["body"], g["updated_by"]) == ("Лаба 9", "текст", "smoke@agent")
          and db.history.count_documents({"coll": "guide", "doc_id": g["_id"], "actor": "smoke@agent"}) == 1, g)
    check("agent: the same text → same, rev 0", page(c, "lab9", "Лаба 9", "текст") == {"state": "same", "rev": 0})
    check("agent: a changed text → updated, rev 1", page(c, "lab9", "Лаба 9", "текст 2", note="правка") == {"state": "updated", "rev": 1})
    check("… the note in history", db.history.find_one({"coll": "guide", "doc_id": g["_id"], "note": "правка"}) is not None)
    check("bad slug → 422", page(c, "Lab_9", "x", "y") == page(c, "lab%209", "x", "y") == 422)

    check("file: new · same · updated", [media(c, "lab9/x.png", PNG), media(c, "lab9/x.png", PNG), media(c, "lab9/x.png", PNG2)]
          == ["new", "same", "updated"])
    check("file: another type is a change", media(c, "lab9/x.png", PNG2, "image/webp") == "updated")
    check("file: a deeper path", media(c, "files/lab9/n.ipynb", b"{}", "application/x-ipynb+json") == "new")
    bad = [media(c, p, PNG) for p in ("lab9/%2e%2e/x.png", "lab9/x%20y.png", "lab9/х.png", "lab9//x.png")]
    check("file: «..», a space, Cyrillic, an empty segment → 422", bad == [422] * 4, bad)
    r = c.put("/api/content/media/lab9/big.bin", content=b"0" * (12 * 2**20 + 1), headers=AGENT)
    check("file over 12 MB → 413 with words", r.status_code == 413 and "12 МБ" in r.json()["detail"], r.text)
    check("… and nothing kept", db.media.count_documents({"path": "lab9/big.bin"}) == 0)

    check("the list: replaced", c.put("/api/content/labpages", json=ROWS, headers=AGENT).json() == {"count": 3})
    check("the list: again, shorter — replaced whole", c.put("/api/content/labpages", json=ROWS[1:], headers=AGENT).json() == {"count": 2}
          and db.lab_pages.count_documents({}) == 2)
    r = c.put("/api/content/labpages", json=ROWS + ROWS[:1], headers=AGENT)
    check("the list: a slug twice → 422, the old list stays", r.status_code == 422 and db.lab_pages.count_documents({}) == 2, r.text)
    c.put("/api/content/labpages", json=ROWS, headers=AGENT)

    have = c.get("/api/content", headers=AGENT).json()
    check("what the site has: a page's sha1 from title and body", have["pages"].get("lab9") == hashlib.sha1("Лаба 9\nтекст 2".encode()).hexdigest(), have)
    check("… a file's from its bytes", have["media"] == {"lab9/x.png": hashlib.sha1(PNG2).hexdigest(), "files/lab9/n.ipynb": hashlib.sha1(b"{}").hexdigest()})
    check("… the list as it was sent", sorted(have["labpages"], key=lambda r: r["slug"]) == sorted(ROWS, key=lambda r: r["slug"]), have["labpages"])

    login(c, "stud@nure.ua", "student")
    r = c.get("/api/media/lab9/x.png")
    check("student: the file with its type", r.status_code == 200 and r.content == PNG2 and r.headers["content-type"] == "image/webp", r.headers)
    check("student: the list of the labs' pages", sorted(p["slug"] for p in c.get("/api/labpages").json()) == ["lab9", "lab9-guide", "labs-faq"])

    login(c, "admin@nure.ua", "admin")
    r = c.put("/api/content/pages/lec99", json={"title": "Тема 99", "body": "текст"})
    check("admin's session: a page by the admin", r.json()["state"] == "new" and db.guide.find_one({"slug": "lec99"})["updated_by"] == "admin@nure.ua", r.text)
    c.cookies.clear()

    page(c, "old-lab1", "Стара лаба 1", "![](/api/media/old-lab1/x.png)")
    media(c, "old-lab1/x.png", PNG)
    media(c, "files/old-lab1/n.ipynb", b"{}", "application/x-ipynb+json")
    check("agent: the staff's page, picture and file all open", staff(c, headers=AGENT) == (True, 200, 200, 200), staff(c, headers=AGENT))
    login(c, "stud@nure.ua", "student")
    check("student: the staff's page — not listed, 404 for it, its picture and its file", staff(c) == (False, 404, 404, 404), staff(c))
    check("student: a page of their own still opens", c.get("/api/guide/lab9").status_code == 200)
    login(c, "admin@nure.ua", "admin")
    check("admin: the staff's page, picture and file", staff(c) == (True, 200, 200, 200), staff(c))

    r = c.post("/api/me/as")
    check("admin: one click → a made-up test student", r.status_code == 200 and r.json()["email"] == "test.student@nure.ua" and r.json()["viewing"], r.text)
    check("… who does not see the staff's page", staff(c) == (False, 404, 404, 404), staff(c))
    check("… and back to the admin", c.delete("/api/me/as").json()["email"] == "admin@nure.ua" and staff(c)[0])

print(f"\n{sum(ok for _, ok in results)}/{len(results)} PASS")
sys.exit(not all(ok for _, ok in results))
