"""What the votes say (T174). A person's answer is their latest vote in the poll, across all its messages; who the person is —
by Telegram id at reading (T150), so votes cast before the bot was linked count as theirs."""
from collections import defaultdict

from core.models.history import stamp
from core.models.poll import Poll
from core.models.poll_send import PollSend
from core.models.user import Status, User
from core.models.vote import Vote


def key(v: Vote):
    """Whose vote: a Telegram user, or a chat voting as itself (an anonymous admin)."""
    return v.tg_id if v.tg_id is not None else f"@{v.username}"


async def votes_of(sends: list[PollSend]) -> list[Vote]:
    """Oldest first, so the latest vote of a person is the last one met."""
    ids = [s.tg_poll_id for s in sends if s.tg_poll_id]
    return await Vote.find({"tg_poll_id": {"$in": ids}}).sort("at", "_id").to_list() if ids else []


def latest(votes: list[Vote], by=lambda v: v.tg_poll_id) -> dict:
    """(what `by` groups — a message or a poll, the person) → their last vote there."""
    return {(by(v), key(v)): v for v in votes}


def mismatch(s: PollSend, votes: list[Vote]) -> dict | None:
    """Telegram's count against ours for one message, or None when they agree. `votes` — any, the message's own are picked.
    They differ when votes were lost: Telegram drops what the bot has not fetched within a day."""
    if not s.state:
        return None
    now = [v for v in latest([v for v in votes if v.tg_poll_id == s.tg_poll_id]).values() if v.option_ids]
    counts = [sum(i in v.option_ids for v in now) for i in range(len(s.state["counts"]))]
    return None if (len(now), counts) == (s.state["total"], s.state["counts"]) else {"telegram": s.state["total"], "ours": len(now)}


async def people() -> tuple[list[User], dict[int, User]]:
    users = await User.find_all().to_list()
    return users, {u.tg_chat_id: u for u in users if u.tg_chat_id}


def who(v: Vote, by_tg: dict[int, User]) -> dict:
    user = by_tg.get(v.tg_id)
    return user.person() if user else {"tg_id": v.tg_id, "username": v.username}


def student(u: User | None) -> bool:
    return bool(u) and u.status == Status.student and not u.test


def staff(u: User | None) -> bool:
    """A teacher or a made-up student: their votes are tries, not answers."""
    return bool(u) and (u.status == Status.admin or u.test)


def order(w: dict) -> tuple:
    """Voters by group and name; people the site does not know go last."""
    return "nick" not in w, w.get("group") or "", w.get("name") or w.get("username") or ""


async def summary(polls: list[Poll]) -> dict[str, dict]:
    """The list's line of each poll: where it went, how many answer now (not counting teachers' tries), whether Telegram counts otherwise."""
    sends = await PollSend.find({"poll": {"$in": [p.id for p in polls]}}).sort("at").to_list()
    votes, poll_of = await votes_of(sends), {s.tg_poll_id: str(s.poll) for s in sends if s.tg_poll_id}
    _, by_tg = await people()
    by_send = defaultdict(list)
    for v in votes:
        by_send[v.tg_poll_id].append(v)
    out = {str(p.id): {"sends": [], "voters": 0, "mismatch": False} for p in polls}
    for s in sends:
        out[str(s.poll)]["sends"].append({"where": s.where, "status": s.status})
        out[str(s.poll)]["mismatch"] |= bool(mismatch(s, by_send[s.tg_poll_id]))
    for (poll, _), v in latest(votes, by=lambda v: poll_of[v.tg_poll_id]).items():
        out[poll]["voters"] += bool(v.option_ids) and not staff(by_tg.get(v.tg_id))  # teachers' tries are not answers
    return out
