"""Smoke: `?next=` round-trip via dev-login, safe_path, 401 vs 403. Run from app/api:
DB_NAME=python_labs_smoke uv run python tests/smoke_auth.py"""
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
from config import settings  # noqa: E402
from routes.auth import safe_path  # noqa: E402

results = []


def check(name, cond, extra=""):
    results.append((name, bool(cond)))
    print(("PASS " if cond else "FAIL ") + name + (f" · {extra}" if extra and not cond else ""))


for path, want in [("/students/vasya", "/students/vasya"), ("/tasks?zone=ui&q=x", "/tasks?zone=ui&q=x"),
                   ("//evil.com", "/"), ("/\\evil.com", "/"), ("https://evil.com", "/"), ("", "/")]:
    check(f"safe_path({path!r}) → {want}", safe_path(path) == want, safe_path(path))

settings.fake_user_email = "dev@nure.ua"
with TestClient(main.app, follow_redirects=False) as c:
    check("guest: /students → 401", c.get("/api/students").status_code == 401)
    check("guest: /my/game → 401", c.get("/api/my/game").status_code == 401)

    r = c.get("/api/auth/dev-login", params={"next": "/students/vasya"})
    check("dev-login → 307 to next", r.status_code == 307 and r.headers["location"] == "/students/vasya",
          r.headers.get("location"))
    check("session set", c.get("/api/me").json()["email"] == "dev@nure.ua")
    check("pending: /students → 403", c.get("/api/students").status_code == 403)
    check("pending: /my/game → 403", c.get("/api/my/game").status_code == 403)

    r = c.get("/api/auth/dev-login", params={"next": "https://evil.com"})
    check("dev-login foreign next → /", r.headers["location"] == "/", r.headers.get("location"))
    check("dev-login without next → /", c.get("/api/auth/dev-login").headers["location"] == "/")

    check("logout → /", c.get("/api/auth/logout").headers["location"] == "/")
    check("logged out", c.get("/api/me").json() is None)

failed = [n for n, ok in results if not ok]
print(f"\n{len(results) - len(failed)}/{len(results)} passed")
sys.exit(1 if failed else 0)
