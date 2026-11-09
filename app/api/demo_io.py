"""Demo students for clicking through «Моя гра»: data/demo/<name>.yaml → Mongo, dev only. A file is a made-up test
student (👁 on /students) and their game: the base's reference description (`etalon: true`) plus the file's own
additions in the templates' format — see data/demo/README.md. Usage: uv run python demo_io.py seed|drop [name…]"""
import asyncio
import shutil
import sys
from pathlib import Path
from uuid import uuid4

import yaml

import templates
import uploads
from core.config import settings
from core.models.history import Change, record_new
from core.models.user import Status, User
from db import init_db
from demo_shots import png
from models.game import Claim, Game, Part
from models.rule import Rule
from models.task import Task
from routes.my_parts import clean_props

DEMO = Path(__file__).resolve().parents[2] / "data" / "demo"
EXTRA = ("note", "link", "status", "verdict")  # what a claim carries beyond its card


async def drop(email: str) -> None:
    user = await User.find_one(User.email == email)
    if not user:
        return
    assert user.test, f"{email} is not a test student"
    if game := await Game.find_one(Game.owner == email):
        for model in (Part, Claim, Rule):
            await model.find(model.game == game.id).delete()
        shutil.rmtree(uploads.ROOT / str(game.id), ignore_errors=True)
        await game.delete()
    await Change.find(Change.actor == email).delete()
    await user.delete()


async def set_field(game: Game, f: dict) -> list[str]:
    """The file's field replaces the etalon's; the cards claimed on it are the file's too."""
    await Part.find(Part.game == game.id, Part.kind == "field").delete()
    part = Part(game=game.id, kind="field", title="Поле", props=clean_props(f), description=f.get("description", ""))
    await part.insert()
    slugs = [x if isinstance(x, str) else x["slug"] for x in f.get("claims") or []]
    known = {t.slug for t in await Task.find({"slug": {"$in": slugs}}).to_list()}
    for x in f.get("claims") or []:
        slug, params = (x, {}) if isinstance(x, str) else (x["slug"], x.get("params") or {})
        if slug in known:
            await Claim(game=game.id, task=slug, part=str(part.id), params=params).insert()
    return [f"картка поля «{s}»" for s in slugs if s not in known]


async def finish(game: Game, d: dict, field: dict) -> None:
    """What the templates' format has no words for: screenshots of a part, a claim's note, link and verdict."""
    parts = {(p.kind, p.title.lower()): p for p in await Part.find(Part.game == game.id).to_list()}
    nodes = [(None, d), (parts.get(("field", "поле")), field)]
    nodes += [(parts[(kind, x["title"].lower())], x) for kind, key in (("entity", "entities"), ("window", "windows")) for x in d.get(key) or []]
    for part, node in nodes:
        if part and node.get("shots"):
            folder = uploads.ROOT / str(game.id)
            folder.mkdir(parents=True, exist_ok=True)
            names = [f"{uuid4().hex}.png" for _ in node["shots"]]
            for name, art in zip(names, node["shots"]):
                (folder / name).write_bytes(png(art.splitlines()))
            await part.set({Part.screenshots: names})
        for x in node.get("claims") or []:
            if isinstance(x, dict) and (extra := {k: x[k] for k in EXTRA if k in x}):
                claim = await Claim.find_one(Claim.game == game.id, Claim.task == x["slug"], Claim.part == (str(part.id) if part else ""))
                await claim.set(extra)


async def seed(path: Path, email: str) -> None:
    d = yaml.safe_load(path.read_text())
    await drop(email)
    who = d["student"]
    user = User(email=email, status=Status.student, test=True, name=f"{who['first_name']} {who['last_name']}", **who)
    await user.insert()
    if not d.get("game"):
        return print(f"{user.nick}: без гри")
    game = Game(owner=email, **d["game"])
    await game.insert()
    await record_new(game, actor=email)
    skipped = (await templates.apply(game, user, game.base_game))["skipped"] if d.get("etalon") else []
    field = d.pop("field", None) or {}
    for w in d.get("windows") or []:  # the file's menu of a window goes instead of the etalon's
        if w.get("items"):
            await Part.find(Part.game == game.id, Part.kind == "menu", Part.title == f"Меню «{w['title']}»").delete()
    skipped += (await templates.pour(game, user, d))["skipped"]
    if field:
        skipped += await set_field(game, field)
    await finish(game, d, field)
    counts = [await m.find(m.game == game.id).count() for m in (Part, Rule, Claim)]
    print(f"{user.nick}: «{game.title}» — обʼєктів {counts[0]}, правил {counts[1]}, заявок {counts[2]}" + (f"\n  пропущено: {skipped}" if skipped else ""))


async def main():
    assert settings.fake_user_email, "dev only: made-up students have no place on the server"
    cmd, *names = sys.argv[1:]
    await init_db()
    for path in sorted(DEMO.glob("*.yaml")):
        email = f"demo.{path.stem}@nure.ua"
        if names and path.stem not in names:
            continue
        if cmd == "seed":
            await seed(path, email)
        else:
            await drop(email)
            print(f"demo.{path.stem}: прибрано")


if __name__ == "__main__":
    asyncio.run(main())
