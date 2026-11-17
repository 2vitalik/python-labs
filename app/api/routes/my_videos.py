"""The videos of «Супровід» (T318): the student gives a link — a new one is a new version, the old ones stay; the teacher
says whether a video is wanted from this student and accepts or returns it."""
from datetime import datetime, timezone
from urllib.parse import urlparse

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from pydantic import BaseModel

import videos
from bot import game_alerts
from core.deps import admin_user
from core.models.history import record, record_new
from core.models.user import User
from models.game import CLAIM_STATUSES, Claim, Game
from models.task import Task
from models.video import NEEDS, Video
from routes.my_game import author, in_sandbox, my_game

router = APIRouter(prefix="/api")
LINK_MAX, NOTE_MAX = 500, 300


class LinkIn(BaseModel):
    link: str = ""  # "" — the note alone, while the row has no link yet
    note: str = ""


class WordIn(BaseModel):
    """The fields sent are the fields set."""
    need: str | None = None
    why: str | None = None
    status: str | None = None
    verdict: str | None = None


async def spec_of(game: Game, slot: str) -> dict:
    """The row a slot names in this game; a gold card's — while the game claims the card."""
    if fixed := next((s for s in videos.FIXED if s["slot"] == slot), None):
        return fixed
    slug = slot.removeprefix(videos.MARK)
    task = await Task.find_one(Task.slug == slug) if slug != slot else None
    if not task or task.coin not in videos.GOLD or not await Claim.find_one(Claim.game == game.id, Claim.task == slug):
        raise HTTPException(404, "Такого відео в цій грі не просять.")
    return {"slot": slot, "kind": "gold", "task": slug}


def clean_link(link: str) -> str:
    """A web address; the scheme may be left out — people paste «youtu.be/…»."""
    link = link.strip()
    if link and "://" not in link:
        link = "https://" + link
    u = urlparse(link)
    if u.scheme not in ("http", "https") or "." not in u.netloc or " " in link or len(link) > LINK_MAX:
        raise HTTPException(422, "Потрібне посилання на відео: YouTube, Google Drive, Loom…")
    return link


async def answer(game: Game, spec: dict, doc: Video) -> dict:
    owner = await User.find_one(User.email == game.owner)
    return videos.row(spec, doc, (await videos.dues(owner)).get(spec.get("lab")))


async def put_note(game: Game, slot: str, doc: Video | None, note: str, user: User) -> Video:
    """A line on a row that has no link yet (T344): a version is a link — «вчасно», the lists and the alerts count on it."""
    if (doc and doc.versions) or not (note or (doc and doc.note)):
        raise HTTPException(422, "Потрібне посилання на відео: YouTube, Google Drive, Loom…")
    if doc:
        await record(doc, {"note": note}, actor=user.email)
        return doc
    doc = Video(game=game.id, slot=slot, note=note)
    await doc.insert()
    await record_new(doc, actor=user.email)
    return doc


@router.put("/my/game/videos/{slot}")
async def put_link(slot: str, data: LinkIn, tasks: BackgroundTasks, game: Game = Depends(my_game), user: User = Depends(author)):
    """The same link again changes its note; another one is a new version. No link — the row's own note."""
    if in_sandbox(user):
        raise HTTPException(422, "У пісочниці відео не здають — це копія зразка.")
    spec = await spec_of(game, slot)
    note = " ".join(data.note.split())[:NOTE_MAX]
    doc = await Video.find_one(Video.game == game.id, Video.slot == slot)
    if not data.link.strip():
        return await answer(game, spec, await put_note(game, slot, doc, note, user))
    link = clean_link(data.link)
    now = datetime.now(timezone.utc).replace(tzinfo=None)  # the way Mongo gives it back
    if doc and doc.versions and doc.versions[-1]["link"] == link:
        changes = await record(doc, {"versions": doc.versions[:-1] + [doc.versions[-1] | {"note": note}]}, actor=user.email)
    elif doc:  # the first link takes the row's note along
        version = {"link": link, "note": note or ("" if doc.versions else doc.note), "at": now, "by": user.email}
        changes = await record(doc, {"versions": doc.versions + [version], "note": ""}, actor=user.email)
    else:
        doc = Video(game=game.id, slot=slot, versions=[{"link": link, "note": note, "at": now, "by": user.email}])
        await doc.insert()
        await record_new(doc, actor=user.email)
        changes = True
    if changes:
        tasks.add_task(game_alerts.video, user, doc)
    return await answer(game, spec, doc)


@router.put("/students/{nick}/videos/{slot}")
async def put_word(nick: str, slot: str, data: WordIn, tasks: BackgroundTasks, admin: User = Depends(admin_user)):
    """The teacher's word: wanted or not from this student (with a line why), accepted or returned (with a line to the student)."""
    owner = await User.by_nick(nick)
    game = owner and await Game.find_one(Game.owner == owner.email)
    if not game:
        raise HTTPException(404)
    spec = await spec_of(game, slot)
    patch = {k: v.strip() for k, v in data.model_dump(exclude_none=True).items()}
    if patch.get("need", "") not in NEEDS:
        raise HTTPException(422, "Потрібне відео чи ні — обовʼязково, не потрібно або як у всіх.")
    if patch.get("status", "claimed") not in CLAIM_STATUSES:
        raise HTTPException(422, "Статус — заявлено, зараховано або повернуто.")
    doc = await Video.find_one(Video.game == game.id, Video.slot == slot)
    if not doc:  # a word on a video that is not there yet: «обовʼязково» before the student gave a link
        doc = Video(game=game.id, slot=slot)
        if any(patch.values()):
            await doc.insert()
    if doc.id and (changes := await record(doc, patch, actor=admin.email)) and {"status", "verdict", "need"} & changes.keys():
        tasks.add_task(game_alerts.video_word, owner, doc, changes)
    return await answer(game, spec, doc)
