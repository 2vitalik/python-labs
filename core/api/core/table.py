"""The table of students (T240): a row per student with all the site knows about them, read once — the profile, the repository,
the cells of the labs, the latest vote in every poll, the teacher's own fields, the site's part (students.EXTRAS)."""
from core.config import settings
from core.labs import Index
from core.models.field import Field, FieldValue
from core.models.history import stamp, when
from core.models.poll import Poll
from core.models.poll_send import PollSend
from core.models.user import Status, User
from core.models.view import View
from core.polls_read import latest, votes_of
from core.routes import students
from core.routes.labs import labs_api


async def answers(users: list[User]) -> tuple[list[Poll], dict[str, dict]]:
    """Every sent poll, newest first, and email → {poll id: the person's latest vote} — by Telegram id, like /polls/matrix."""
    polls = await Poll.find({"status": {"$ne": "draft"}}).sort("-sent_at").to_list()
    sends = await PollSend.find({"poll": {"$in": [p.id for p in polls]}}).to_list()
    votes, poll_of = await votes_of(sends), {s.tg_poll_id: str(s.poll) for s in sends if s.tg_poll_id}
    by_tg = {u.tg_chat_id: u.email for u in users if u.tg_chat_id}
    out: dict[str, dict] = {}
    for (poll, _), v in latest(votes, by=lambda v: poll_of[v.tg_poll_id]).items():
        if email := by_tg.get(v.tg_id):
            out.setdefault(email, {})[poll] = {"ids": v.option_ids, "at": stamp(v.at)}
    return polls, out


def profile(u: User) -> dict:
    return {"email": u.email, "fio": bool(u.last_name and u.first_name), "seen": u.first_seen_at is not None, "seen_at": when(u.first_seen_at),
            "last_seen_at": when(u.last_seen_at), "github": u.github, "tg_username": u.tg_username,
            "tg_linked": u.tg_chat_id is not None, "tg_linked_at": when(u.tg_linked_at)}


async def table() -> dict:
    users = await User.find(User.status == Status.student, User.test != True).sort("group", "last_name", "first_name").to_list()  # noqa: E712
    index = await Index.load()
    polls, votes = await answers(users)
    values: dict[str, dict] = {}
    for v in await FieldValue.find_all().to_list():
        values.setdefault(v.user, {})[v.column] = v.value
    extras: dict[str, dict] = {}
    for extra in students.EXTRAS:
        for email, more in (await extra(users)).items():
            extras.setdefault(email, {}).update(more)
    rows = []
    for u in users:
        repo = index.repos.get(u.email)
        rows.append(u.person() | profile(u) | extras.get(u.email, {}) | {
            "repo": repo.api() if repo else None, "labs": index.cells(u.email, u.github, u.group, settings.labs),
            "polls": votes.get(u.email, {}), "fields": values.get(u.email, {})})
    return {"rows": rows, "labs": labs_api(index.deadlines), "polls": [p.api() for p in polls],
            "fields": [f.api() for f in await Field.find_all().sort("order", "created_at").to_list()],
            "views": [v.api() for v in await View.find_all().sort("order", "created_at").to_list()]}
