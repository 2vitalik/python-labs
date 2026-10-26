"""One student's labs (T235): the rows of the card, the teacher's word, the agent's review; the facts of repositories in bulk."""
from datetime import datetime, timezone
from typing import Literal

from core.config import settings
from core.deps import editor_user
from core.lab_marks import set_mark
from core.labs import Index
from core.models.history import record, record_new
from core.models.repo import Commit, Repo, Review, Verdict
from core.models.user import User
from core.routes.labs import lab_no
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/api")


class MarkIn(BaseModel):
    """The fields sent are the fields set: `until: null` clears the date, `met: null` gives the word back to the site."""
    until: datetime | None = None
    open: bool = False
    reason: str = ""
    met: bool | None = None
    note: str = ""


class ReviewIn(BaseModel):
    commit: str
    verdict: Verdict
    head: str = ""
    head_verdict: Verdict | Literal[""] = ""
    summary: str = ""
    report: str = ""


class RepoIn(BaseModel):
    nick: str
    url: str
    ok: bool = True
    error: str = ""
    branch: str = ""
    head: str = ""
    commits: list[Commit] = []


class ReposIn(BaseModel):
    repos: list[RepoIn]


async def student(nick: str) -> User:
    u = await User.by_nick(nick)
    if not u:
        raise HTTPException(404)
    return u


async def card(u: User) -> dict:
    index = await Index.load([u.email])
    cells = index.cells(u.email, u.github, u.group, settings.labs)
    repo = index.repos.get(u.email)
    return {"student": u.person(), "github": u.github, "repo": repo.api() if repo else None,
            "labs": [{"n": n} | cells[str(n)] for n in range(1, settings.labs + 1)]}


@router.get("/students/{nick}/labs")
async def student_labs(nick: str, user: User = Depends(editor_user)):
    return await card(await student(nick))


@router.put("/students/{nick}/labs/{n}")
async def put_mark(nick: str, n: int, data: MarkIn, user: User = Depends(editor_user)):
    u = await student(nick)
    await set_mark(u, lab_no(n), data.model_dump(exclude_unset=True), user.email)
    return (await card(u))["labs"][n - 1]


@router.get("/students/{nick}/labs/{n}/review")
async def get_review(nick: str, n: int, user: User = Depends(editor_user)):
    u = await student(nick)
    r = await Review.find_one(Review.user == u.email, Review.lab == lab_no(n))
    if not r:
        raise HTTPException(404)
    return r.api(full=True)


@router.put("/students/{nick}/labs/{n}/review")
async def put_review(nick: str, n: int, data: ReviewIn, user: User = Depends(editor_user)):
    """The agent's report on the pair, rewritten with history; the same report again changes nothing."""
    u = await student(nick)
    r = await Review.find_one(Review.user == u.email, Review.lab == lab_no(n))
    fields = data.model_dump()
    if not r:
        r = await Review(user=u.email, lab=n, **fields, by=user.email).insert()
        await record_new(r, user.email)
    elif any(getattr(r, k) != v for k, v in fields.items()):
        await record(r, fields | {"by": user.email, "at": datetime.now(timezone.utc)}, user.email)
    return (await card(u))["labs"][n - 1]


@router.put("/repos")
async def put_repos(data: ReposIn, user: User = Depends(editor_user)):
    """The facts of many repositories at once (bin/repos push): a document per student, rewritten whole — a pull is not an edit,
    so no history. `unknown` — nicks the site does not know."""
    saved, unknown = 0, []
    for item in data.repos:
        u = await User.by_nick(item.nick)
        if not u:
            unknown.append(item.nick)
            continue
        doc = Repo(user=u.email, **item.model_dump(exclude={"nick"}), by=user.email)
        if was := await Repo.find_one(Repo.user == u.email):
            doc.id = was.id
        await doc.save()
        saved += 1
    return {"saved": saved, "unknown": unknown}
