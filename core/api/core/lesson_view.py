"""A lesson as its reader sees it (T333): the admin — everything; a student — a published day with its open parts and
the ones that are theirs. A site adds its own parts of a day (python: defenses) through SITE_PARTS."""
from core.lesson_people import known, people, speakers
from core.models.lesson import HIDDEN, Lesson, Meeting, Part
from core.models.lesson_file import FileMeta, LessonFile, file_api
from core.models.user import Status, User

SITE_PARTS: list = []  # async (user, admin) -> {date: [a part as the page reads it]}; a date without a lesson is a day too


def is_admin(user: User) -> bool:
    return user.status == Status.admin  # the agent comes built as an admin


def mine(l: Lesson, user: User, admin: bool) -> list[Part]:
    return [p for p in l.parts if admin or (p.kind not in HIDDEN and (not p.only or user.email in p.only))]


def can_see(l: Lesson, user: User, admin: bool) -> bool:
    """A draft is the admin's; a day made of private parts — theirs whose parts they are."""
    return admin or (l.published and (not l.parts or bool(mine(l, user, admin))))


def part(p: Part, users: dict[str, User], admin: bool, texts: bool) -> dict:
    row = p.model_dump(exclude={"only"} if texts else {"only", "summary", "transcript"}) | {"private": bool(p.only)}
    return row | ({"only": p.only, "people": [users[e].person() for e in p.only if e in users]} if admin else {})


async def site_parts(user: User, admin: bool) -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = {}
    for give in SITE_PARTS:
        for date, found in (await give(user, admin)).items():
            out.setdefault(date, []).extend(p | {"site": True} for p in found)
    return out


def joined(own: list[dict], site: list[dict]) -> list[dict]:
    """A site's part that starts inside a private part of the same kind and people is that part: its badge and its link
    join the card instead of a second one (a defense recorded as a piece of the day and noted on the defense's page)."""
    rest = []
    for s in site:
        who = {u["nick"] for u in s.get("people", [])}
        host = next((p for p in own if p["private"] and p["kind"] == s["kind"] and p["end"] and p["start"][:5] <= s["start"][:5] < p["end"][:5]
                     and (not who or "people" not in p or who & {u["nick"] for u in p["people"]})), None)
        if host:
            host |= {k: s[k] for k in ("badge", "to", "more") if s.get(k)} | {"title": host["title"] or s["title"]}
        else:
            rest.append(s)
    return own + rest


def day(date: str, parts: list[dict]) -> dict:
    """A date that has the site's parts and no lesson: a day all the same — a defense alone makes one."""
    return Lesson(slug=date, date=date, published=True).row() | {"updated": None, "virtual": True, "parts": parts}


async def rows(lessons: list[Lesson], user: User) -> list[dict]:
    admin = is_admin(user)
    extra = await site_parts(user, admin)
    users = {u.email: u for u in await known()} if admin else {}
    out = [l.row() | {"parts": joined([part(p, users, admin, False) for p in mine(l, user, admin)], extra.pop(l.slug, []))}
           for l in lessons if can_see(l, user, admin)]
    return sorted(out + [day(d, parts) for d, parts in extra.items()], key=lambda r: (r["date"], r["slug"]), reverse=True)


async def full(l: Lesson, user: User) -> dict:
    admin = is_admin(user)
    files = await LessonFile.find(LessonFile.lesson == l.slug).sort("role", "name").project(FileMeta).to_list()
    users = {u.email: u for u in await known()} if admin else {}
    own = mine(l, user, admin)
    text = "\n".join([l.transcript, *(p.transcript for p in own)])
    data = l.api(admin) | {"files": [file_api(f) for f in files if admin or f.role == "file"], "people": await people(text),
                           "parts": joined([part(p, users, admin, True) for p in own], (await site_parts(user, admin)).get(l.slug, []))}
    return data | ({"speakers": speakers(text)} if admin else {})


async def virtual(date: str, user: User) -> dict | None:
    """The page of a day without a lesson: only what the site gives this reader for the date."""
    parts = (await site_parts(user, is_admin(user))).get(date)
    return parts and day(date, parts) | {"video_start": "", "transcript": "", "summary": "", "report": "", "chat": "", "zoom": Meeting().model_dump(),
                                         "rev": 0, "updated_by": "", "files": [], "people": {}}
