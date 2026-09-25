"""Smoke: `?next=` round-trip via dev-login, safe_path, 401 vs 403, activity rows (login ua/ip, api calls), /api/health. Run from app/api:
DB_NAME=python_labs_smoke uv run python tests/smoke_auth.py"""
import os
import sys

sys.path.insert(0, os.getcwd())
from pymongo import AsyncMongoClient, MongoClient  # noqa: E402

DB = os.environ["DB_NAME"]
assert DB.endswith("_smoke"), "refuse to run on a non-smoke DB"
mongo = MongoClient()
mongo.drop_database(DB)

from fastapi.testclient import TestClient  # noqa: E402

import main  # noqa: E402
from config import settings  # noqa: E402
from routes import health  # noqa: E402
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
    check("guest: /api/health → 200 ok", c.get("/api/health").json() == {"ok": True})
    check("guest: /students → 401", c.get("/api/students").status_code == 401)
    check("guest: /my/game → 401", c.get("/api/my/game").status_code == 401)

    r = c.get("/api/auth/dev-login", params={"next": "/students/vasya"})
    check("dev-login → 307 to next", r.status_code == 307 and r.headers["location"] == "/students/vasya",
          r.headers.get("location"))
    check("session set", c.get("/api/me").json()["email"] == "dev@nure.ua")
    check("pending: /students → 403", c.get("/api/students").status_code == 403)
    check("pending: /my/game → 403", c.get("/api/my/game").status_code == 403)

    def acts(**q):
        return list(mongo[DB].activity.find(q))
    login = acts(kind="login")[0]
    check("login row: user-agent + ip", login["ua"] == "testclient" and login["ip"] == "testclient", login)
    api = acts(kind="api")
    check("api rows: the two 403s only — not the guest 401s, /api/me or /api/auth", sorted(a["path"] for a in api) == ["/api/my/game", "/api/students"]
          and all(a["status"] == 403 and a["method"] == "GET" and a["ms"] >= 0 for a in api), api)
    c.get("/api/students", params={"group": "x"})
    row = acts(kind="api", path="/api/students?group=x")
    check("api row keeps the query and carries ua + ip", row != [] and row[0]["ua"] == "testclient" and row[0]["ip"] == "testclient")
    c.post("/api/me/view", json={"path": "/tasks"}, headers={"x-forwarded-for": "5.6.7.8", "user-agent": "Mozilla/5.0 (iPhone)"})
    row = acts(kind="view")
    check("view row: page + ua + proxied ip", row != [] and row[-1]["path"] == "/tasks" and row[-1]["ua"] == "Mozilla/5.0 (iPhone)" and row[-1]["ip"] == "5.6.7.8", row)
    c.get("/api/auth/dev-login", headers={"x-forwarded-for": "1.2.3.4, 10.0.0.1"})
    check("login behind a proxy: first X-Forwarded-For ip", acts(kind="login")[-1]["ip"] == "1.2.3.4")

    r = c.get("/api/auth/dev-login", params={"next": "https://evil.com"})
    check("dev-login foreign next → /", r.headers["location"] == "/", r.headers.get("location"))
    check("dev-login without next → /", c.get("/api/auth/dev-login").headers["location"] == "/")

    check("logout → /", c.get("/api/auth/logout").headers["location"] == "/")
    check("logged out", c.get("/api/me").json() is None)

    health.mongo = AsyncMongoClient("mongodb://127.0.0.1:9", serverSelectionTimeoutMS=100)  # nobody listens there
    check("health without db → 503", c.get("/api/health").status_code == 503)

failed = [n for n, ok in results if not ok]
print(f"\n{len(results) - len(failed)}/{len(results)} passed")
sys.exit(1 if failed else 0)
