"""Smoke: the proof of a claim (T284 §7) — a card's `proof` (the form, the catalog, the passport), up to three pictures on a
claim (an auto one too), no files in the sandbox, the game's history, proof.yaml through export / import — on a scratch DB.
Run from app/api: DB_NAME=python_labs_proof_smoke TG_BOT_TOKEN= UPLOADS_DIR=... uv run python tests/smoke_proof.py"""
import os
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, os.getcwd())
from bson import ObjectId  # noqa: E402
from pymongo import MongoClient  # noqa: E402

DB = os.environ["DB_NAME"]
assert DB.endswith("_smoke"), "refuse to run on a non-smoke DB"
mongo = MongoClient()
mongo.drop_database(DB)
subprocess.run(["uv", "run", "python", "catalog_io.py", "import"], check=True, capture_output=True)

from fastapi.testclient import TestClient  # noqa: E402

import catalog_io  # noqa: E402
import main  # noqa: E402
import uploads  # noqa: E402
from core.config import settings  # noqa: E402

PNG = b"\x89PNG\r\n\x1a\n" + b"0" * 100
GIF = b"GIF89a" + b"0" * 100
CLAIMS, H = "/api/my/claims", "/api/students/stud/game/history"
# catalog_io's CLI over another folder: the repo's data/catalog stays as git has it
IO = "import asyncio, sys, pathlib, catalog_io; catalog_io.CATALOG = pathlib.Path(sys.argv.pop(1)); asyncio.run(catalog_io.main())"
results = []


def check(name, cond, extra=""):
    results.append(bool(cond))
    print(("PASS " if cond else "FAIL ") + name + (f" · {extra}" if extra and not cond else ""))


def login(c, email, status):
    settings.fake_user_email = email
    c.get("/api/auth/dev-login")
    mongo[DB].users.update_one({"email": email}, {"$set": {"status": status, "group": "ПЗПІ-25-1"}})


def put_proof(c, slug, proof):
    t = next(x for x in c.get("/api/tasks").json() if x["slug"] == slug)
    return c.put(f"/api/tasks/{t['id']}", json=t | ({"proof": proof} if proof is not None else {}))


def proof_of(slug):
    return mongo[DB].tasks.find_one({"slug": slug}).get("proof")


def shot(c, cid, data=PNG, kind="image/png", name="s.png", **kw):
    return c.post(f"{CLAIMS}/{cid}/shot", files={"file": (name, data, kind)}, **kw)


def io(folder, cmd):
    return subprocess.run([sys.executable, "-c", IO, str(folder), cmd], capture_output=True, text=True)


with TestClient(main.app) as c:
    check("the repo's proof.yaml: the header, then the values", (catalog_io.CATALOG / "proof.yaml").read_text().startswith(catalog_io.PROOF_HEAD))
    asked = {t["slug"]: t["proof"] for t in mongo[DB].tasks.find({"proof": {"$ne": ""}})}
    lines = [x for x in (catalog_io.CATALOG / "proof.yaml").read_text().splitlines() if x and not x.startswith("#")]
    check("import of the repo's catalog: the cards ask what proof.yaml says", lines == [f"{k}: {v}" for k, v in sorted(asked.items())], len(asked))
    mongo[DB].tasks.update_many({}, {"$set": {"proof": ""}})  # the checks below start from a catalog that asks nothing

    login(c, "admin@nure.ua", "admin")
    r = put_proof(c, "player-death", "gif")
    check("PUT: proof gif", r.status_code == 200 and r.json()["proof"] == "gif", r.text)
    r = put_proof(c, "player-death", "movie")
    check("PUT: an unknown proof → 422 in words", r.status_code == 422 and "gif" in r.json()["detail"] and proof_of("player-death") == "gif", r.text)
    check("PUT without proof: left as it is", put_proof(c, "player-death", None).json()["proof"] == "gif")
    check("PUT: proof back to nothing", put_proof(c, "status-panel", "shot").json()["proof"] == "shot"
          and put_proof(c, "status-panel", "").json()["proof"] == "" and put_proof(c, "status-panel", " shot ").json()["proof"] == "shot")
    check("GET /api/tasks: proof", {t["slug"]: t["proof"] for t in c.get("/api/tasks").json()}["player-death"] == "gif")
    snap = c.get("/api/catalog/snapshot").json()
    check("snapshot: proof.yaml beside the rest, tasks.yaml without proof", snap["proof.yaml"].startswith(catalog_io.PROOF_HEAD)
          and "player-death: gif\n" in snap["proof.yaml"] and "proof" not in snap["tasks.yaml"] and {"games.yaml", "aliases.yaml"} <= set(snap))

    login(c, "stud2@nure.ua", "student")
    c.post("/api/my/game", json={"title": "Чужа", "base_custom": "своя"})
    alien = c.post(CLAIMS, json={"task": "player-death"}).json()

    login(c, "stud@nure.ua", "student")
    c.post("/api/my/game", json={"title": "Привиди", "base_game": "sokoban"})
    gid = c.get("/api/my/game").json()["id"]
    claim = c.post(CLAIMS, json={"task": "player-death"}).json()
    check("a new claim: no proof yet", claim["shots"] == [])
    r = shot(c, claim["id"])
    check("png → the claim", r.status_code == 200 and len(r.json()["shots"]) == 1, r.text)
    first = r.json()["shots"][0]
    check("the file on disk and served", (uploads.ROOT / gid / first).is_file() and c.get(f"/api/uploads/{gid}/{first}").status_code == 200)
    r = shot(c, claim["id"], b"x", "text/plain", "s.txt")
    check("not a picture → 422", r.status_code == 422 and "gif" in r.json()["detail"], r.text)
    r = shot(c, claim["id"], GIF, "image/gif", "s.gif")
    check("gif → the claim", r.status_code == 200 and r.json()["shots"][1].endswith(".gif"), r.text)
    shot(c, claim["id"], PNG, "image/jpeg", "s.jpg")
    r = shot(c, claim["id"], PNG, "image/webp", "s.webp")
    check("the fourth → 422 «Не більше трьох»", r.status_code == 422 and r.json()["detail"] == "Не більше трьох файлів на заявку."
          and len(mongo[DB].claims.find_one({"_id": ObjectId(claim["id"])})["shots"]) == 3, r.text)
    check("someone else's claim → 404", shot(c, alien["id"]).status_code == 404
          and c.delete(f"{CLAIMS}/{alien['id']}/shot/x.png").status_code == 404)
    check("no such claim → 404", shot(c, "0" * 24).status_code == 404)
    check("the note's PUT keeps the proof", len(c.put(f"{CLAIMS}/{claim['id']}", json={"note": "ось"}).json()["shots"]) == 3)

    check("delete: an unknown name → 404", c.delete(f"{CLAIMS}/{claim['id']}/shot/nope.png").status_code == 404)
    r = c.delete(f"{CLAIMS}/{claim['id']}/shot/{first}")
    check("delete → the file in the trash", r.status_code == 200 and first not in r.json()["shots"] and len(r.json()["shots"]) == 2
          and not (uploads.ROOT / gid / first).is_file() and (uploads.TRASH / gid / first).is_file(), r.text)

    win = c.post("/api/my/game/parts", json={"kind": "window", "task": "main-menu", "title": "Меню"}).json()
    auto = next(x for x in c.get("/api/students/stud/game").json()["claims"] if x["auto"] and x["part"] == win["id"])
    check("an auto-claim takes a proof too", shot(c, auto["id"]).status_code == 200)

    p = c.get("/api/students/stud/game").json()
    mine = next(x for x in p["claims"] if x["id"] == claim["id"])
    check("passport: the claim's shots, the card's proof", len(mine["shots"]) == 2 and p["tasks"]["player-death"]["proof"] == "gif"
          and p["tasks"]["main-menu"]["proof"] == "", p["tasks"].get("player-death"))
    rows = c.get(H, params={"limit": 100}).json()
    ups = [f for x in rows if x["what"] == "заявка" for f in x["fields"] if f["key"] == "shots"]
    check("history: «докази» with the count, added and taken off", len(ups) == 5 and all(f["label"] == "докази" for f in ups)
          and {"old": "3", "new": "2"} in [{"old": f["old"], "new": f["new"]} for f in ups]
          and {"old": None, "new": "1"} in [{"old": f["old"], "new": f["new"]} for f in ups], ups)

    c.post("/api/games/sokoban/sandbox")
    box = c.get("/api/my/game", headers={"X-Sandbox": "sokoban"}).json()
    some = mongo[DB].claims.find_one({"game": ObjectId(box["id"])})
    r = shot(c, str(some["_id"]), headers={"X-Sandbox": "sokoban"})
    check("sandbox → 403, no file", r.status_code == 403 and not (uploads.ROOT / box["id"]).exists(), r.text)

    login(c, "stud3@nure.ua", "student")
    seen = c.get("/api/students/stud/game")
    check("a fellow student sees the proof", seen.status_code == 200 and len(next(x for x in seen.json()["claims"] if x["id"] == claim["id"])["shots"]) == 2, seen.text[:200])
    check("…but adds none to it: no game of his → 404", shot(c, claim["id"]).status_code == 404)
    login(c, "admin@nure.ua", "admin")
    seen = c.get("/api/students/stud/game").json()
    check("the teacher sees the proof", len(next(x for x in seen["claims"] if x["id"] == claim["id"])["shots"]) == 2)

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        out = io(tmp, "export")
        text = (tmp / "proof.yaml").read_text()
        check("export: the header, then the asking cards by slug", out.returncode == 0
              and text == catalog_io.PROOF_HEAD + "player-death: gif\nstatus-panel: shot\n" and "proof" not in (tmp / "tasks.yaml").read_text(),
              out.stderr[-300:] + text)
        (tmp / "proof.yaml").write_text(catalog_io.PROOF_HEAD + "status-panel: code\ntime-out: video\n")
        out = io(tmp, "import")
        check("import: the file's values, a card it lacks → ''", out.returncode == 0 and "оновлено 3" in out.stdout
              and (proof_of("status-panel"), proof_of("time-out"), proof_of("player-death")) == ("code", "video", ""), out.stdout + out.stderr[-300:])
        (tmp / "proof.yaml").unlink()
        out = io(tmp, "import")
        check("import with no proof.yaml: the proofs as they were", out.returncode == 0 and "оновлено 0" in out.stdout
              and (proof_of("status-panel"), proof_of("time-out")) == ("code", "video"), out.stdout + out.stderr[-300:])
        out = io(tmp, "export")
        again = io(tmp, "import")
        check("export → import: nothing changes", out.returncode == 0 and "оновлено 0" in again.stdout
              and (tmp / "proof.yaml").read_text() == catalog_io.PROOF_HEAD + "status-panel: code\ntime-out: video\n", again.stdout)
        (tmp / "proof.yaml").write_text("time-out: film\n")
        out = io(tmp, "import")
        check("import: an unknown proof stops it in words", out.returncode != 0 and "time-out" in out.stderr and proof_of("time-out") == "video", out.stderr[-300:])

ok = sum(results)
print(f"\n{ok}/{len(results)} PASS")
sys.exit(0 if ok == len(results) else 1)
