from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request
from pydantic import BaseModel

import auto_claims
from bot import game_alerts
from core.deps import active_user
from core.models.history import Change, record, record_new
from core.models.user import Status, User
from models.base_game import BaseGame
from models.game import Game

router = APIRouter(prefix="/api/my/game")
SANDBOX = "x-sandbox"  # header: the base game's slug of the sandbox the editor works in (T274 §7, routes/sandbox.py)
GAME_OF = "x-game-of"  # header: the nick of the student whose game the teacher edits (T282 Б)


class GameIn(BaseModel):
    title: str
    base_game: str = ""
    base_custom: str = ""
    description: str = ""
    phases: list[str] = []
    moments: str | None = None  # None — left as it is: the forms of the title and the phases do not send it


MOMENTS_MAX = 20_000


def sandbox_owner(email: str) -> str:
    """The sandbox game's owner: no user has such an email, so the gallery, the table and the passports never meet it."""
    return email.replace("@", "+") + "@sandbox"


def in_sandbox(user: User) -> bool:
    return user.email.endswith("@sandbox")


async def author(request: Request, user: User = Depends(active_user)):
    """Who writes «Моя гра»: the user, or under `X-Sandbox` a made-up test student who owns the sandbox copy.
    Under `X-Game-Of` it stays the teacher — the history and the catalog's drafts are theirs, the game is the student's (game_of)."""
    if request.headers.get(GAME_OF):
        if user.status != Status.admin:
            raise HTTPException(403, "Редагувати чужу гру може лише викладач.")
        if request.headers.get(SANDBOX):
            raise HTTPException(422, "Пісочниця й гра студента разом не відкриваються.")
    if not request.headers.get(SANDBOX):
        yield user
        return
    me = User(email=sandbox_owner(user.email), status=Status.student, test=True)
    try:
        yield me
    finally:  # no trace in `history`: the activity feed and the card history read it
        await Change.find(Change.actor == me.email).delete()


async def game_of(request: Request, user: User) -> Game | None:
    """The game «Моя гра» works on: the writer's own, or under `X-Game-Of` the student's — which must be there already."""
    if not (nick := request.headers.get(GAME_OF)):
        return await Game.find_one(Game.owner == user.email)
    student = await User.by_nick(nick)
    if not student:
        raise HTTPException(404, f"Студента «{nick}» не знайдено.")
    game = await Game.find_one(Game.owner == student.email)
    if not game:
        raise HTTPException(404, f"У студента {student.person()['name'] or nick} ще нема гри — створити її може лише він сам.")
    return game


async def my_game(request: Request, user: User = Depends(author)) -> Game:
    game = await game_of(request, user)
    slug = request.headers.get(SANDBOX)
    if slug and (not game or game.base_game != slug):
        raise HTTPException(404, "Пісочницю не відкрито — натисни «Спробувати редагувати» на сторінці гри.")
    if not game:
        raise HTTPException(404, "Спершу створи свою гру.")
    return game


def clean_phases(phases: list[str]) -> list[str]:
    out = []
    for p in phases:
        p = " ".join(str(p).split())
        if p and p.lower() not in {x.lower() for x in out}:
            out.append(p)
    if len(out) > 12:
        raise HTTPException(422, "Фаз забагато — до 12.")
    return out


async def clean(data: GameIn) -> dict:
    d = data.model_dump()
    d["title"] = d["title"].strip()
    if not d["title"]:
        raise HTTPException(422, "Назва — обовʼязкова.")
    if d["base_game"]:
        if not await BaseGame.find_one(BaseGame.slug == d["base_game"]):
            raise HTTPException(422, "Немає такої гри-основи в каталозі.")
    elif not d["base_custom"].strip():
        raise HTTPException(422, "Обери гру-основу з каталогу або опиши свою.")
    d["phases"] = clean_phases(d["phases"])
    if d["moments"] is None:
        del d["moments"]
    elif len(d["moments"]) > MOMENTS_MAX:
        raise HTTPException(422, "Розкадровка задовга — до 20 000 знаків: менше кадрів чи сценаріїв.")
    return d


@router.get("")
async def get_my_game(request: Request, user: User = Depends(author)):
    game = await game_of(request, user)
    return game.api() if game else None


@router.post("")
async def create_game(data: GameIn, request: Request, tasks: BackgroundTasks, user: User = Depends(author)):
    if request.headers.get(GAME_OF):
        raise HTTPException(403, "Створити гру за студента не можна — лише редагувати наявну.")
    if await Game.find_one(Game.owner == user.email):
        raise HTTPException(409, "Гра вже створена — вона в тебе одна.")
    game = Game(owner=user.email, **await clean(data))
    await game.insert()
    await record_new(game, actor=user.email)
    if game.moments:
        await auto_claims.sync(game, user.email)
    tasks.add_task(game_alerts.game, user, game)
    return game.api()


@router.put("")
async def update_game(data: GameIn, tasks: BackgroundTasks, game: Game = Depends(my_game),
                      user: User = Depends(author)):
    d = await clean(data)
    if in_sandbox(user) and d["base_game"] != game.base_game:  # X-Sandbox names the base: another one would lock the copy out
        raise HTTPException(422, "У пісочниці основа не міняється — це копія зразка.")
    if changes := await record(game, d, actor=user.email):
        tasks.add_task(game_alerts.game, user, game, changes)
        if "moments" in changes:  # a scenario of three frames claims its card by itself (T276)
            await auto_claims.sync(game, user.email)
    return game.api()
