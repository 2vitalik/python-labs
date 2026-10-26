"""Labs × students (T235): a student's deadline, the facts off the commit log, the state of a cell.
Precedence — the teacher's word, then the agent's review, then the facts."""
from datetime import datetime, timezone

from core.models.deadline import Deadline, LabMark
from core.models.history import when
from core.models.repo import Repo, Review

STATES = ("ok", "late", "partial", "miss", "open", "wait", "check", "norepo", "noaccess", "nodue")  # what a cell can say


def utc(d: datetime | None) -> datetime | None:
    """Mongo gives naive UTC, a request gives an aware moment: compare them on one footing."""
    return d.replace(tzinfo=timezone.utc) if d and not d.tzinfo else d


def naive(d: datetime | None) -> datetime | None:
    """What goes into a document: the way Mongo will give it back, so a diff in history sees a real change only."""
    return d.astimezone(timezone.utc).replace(tzinfo=None) if d and d.tzinfo else d


def due_for(deadlines: list[Deadline], lab: int, group: str) -> Deadline | None:
    """The lab's deadline for a group: its own over the one for everyone."""
    own = [d for d in deadlines if d.lab == lab and group in d.groups]
    everyone = [d for d in deadlines if d.lab == lab and not d.groups]
    return (own or everyone or [None])[0]


def effective(mark: LabMark | None, base: Deadline | None) -> datetime | None:
    return utc(mark.until) if mark and mark.until else utc(base.at) if base else None


def facts(repo: Repo | None, since: datetime | None, due: datetime | None) -> dict:
    """Commits before the deadline, in the lab's window (after the previous one) and after; the last one before it."""
    commits = repo.commits if repo else []
    before = [c for c in commits if due and utc(c.at) <= due]
    last = max(before, key=lambda c: utc(c.at), default=None)
    return {"before": len(before), "window": sum(1 for c in before if not since or utc(c.at) > since),
            "after": sum(1 for c in commits if due and utc(c.at) > due), "last": when(last.at) if last else None,
            "last_sha": last.sha if last else ""}


def state(github: str, repo: Repo | None, mark: LabMark | None, review: Review | None, due: datetime | None, now: datetime) -> str:
    if mark and mark.met is not None:
        return "ok" if mark.met else "miss"
    if mark and mark.open:
        return "open"
    if not due:
        return "nodue"
    if review and review.verdict == "done":
        return "ok"
    if review and review.head_verdict == "done":
        return "late"
    if due > now:
        return "wait"
    if review:
        return "partial" if review.verdict == "partial" else "miss"
    if not github:
        return "norepo"
    if repo and not repo.ok:
        return "noaccess"
    return "check"


def cell(github: str, repo: Repo | None, mark: LabMark | None, review: Review | None, base: Deadline | None,
         since: datetime | None, now: datetime | None = None) -> dict:
    """One student × one lab, as the matrix and the student's card show it."""
    due = effective(mark, base)
    f = facts(repo, since, due)
    out = {"state": state(github, repo, mark, review, due, now or datetime.now(timezone.utc)),
           "due": when(due), "base": when(utc(base.at)) if base else None, "facts": f,
           "mark": mark.api() if mark else None, "review": None}
    if review:  # a short sha from `bin/repos cut` names the same commit
        out["review"] = review.api() | {"stale": bool(f["last_sha"]) and not f["last_sha"].startswith(review.commit or "-")}
    return out


class Index:
    """Everything the cells of many students need, read once."""

    def __init__(self, deadlines: list[Deadline], marks: list[LabMark], reviews: list[Review], repos: list[Repo]):
        self.deadlines = deadlines
        self.marks = {(m.user, m.lab): m for m in marks}
        self.reviews = {(r.user, r.lab): r for r in reviews}
        self.repos = {r.user: r for r in repos}

    @classmethod
    async def load(cls, users: list[str] | None = None) -> "Index":
        q = {"user": {"$in": users}} if users is not None else {}
        return cls(await Deadline.find_all().sort("lab").to_list(), await LabMark.find(q).to_list(),
                   await Review.find(q).to_list(), await Repo.find(q).to_list())

    def cells(self, email: str, github: str, group: str, labs: int) -> dict[str, dict]:
        """Lab n → cell; a lab's window opens where the previous lab's effective deadline closed."""
        out, since = {}, None
        for n in range(1, labs + 1):
            base, mark = due_for(self.deadlines, n, group), self.marks.get((email, n))
            out[str(n)] = cell(github, self.repos.get(email), mark, self.reviews.get((email, n)), base, since)
            since = effective(mark, base) or since
        return out
