"""A deadline's verdict (T340): everything the site knows of one student and one lab → «так · ні · спитати · чекає» and
the case it is. The teacher's word first, then the agent's review against the commit log, then the bare facts.
What the student says in the status poll never decides — it only raises a flag when it differs."""
from datetime import datetime, timedelta, timezone

from core.due_says import said, status_polls
from core.labs import Index, due_for, effective, utc
from core.models.deadline import Deadline, LabMark
from core.models.poll import Poll
from core.models.repo import Repo, Review
from core.models.user import User
from core.repos import EMPTY

YES, NO, ASK, WAIT = "yes", "no", "ask", "wait"
SLIP, NEAR, DAYS = 1, 24, 72  # hours late: a clock or a slow push · «трохи пізніше» · «на день-три»; beyond — «значно пізніше»


def hours(d: timedelta) -> float:
    return round(d.total_seconds() / 3600, 1)


def by_review(repo: Repo | None, review: Review, due: datetime, extended: bool, idle: bool) -> tuple[str, str, float | None]:
    fine = YES, "extended" if extended else "ontime", None
    if review.verdict == "done":
        return fine
    if review.head_verdict == "done":  # done later: by how much — off the commit the review found it done at
        c = next((c for c in repo.commits if c.sha.startswith(review.head)), None) if repo and review.head else None
        if not c:
            return ASK, "late", None
        late = hours(utc(c.at) - due)
        if late <= SLIP:  # ≤ 0 — the deadline moved after the review was cut
            return fine if late <= 0 else (YES, "slip", late)
        return ASK, "late_bit" if late <= NEAR else "late_days" if late <= DAYS else "late_far", late
    if idle:  # not a commit since the previous deadline: the review read the previous lab's code — or we cannot pull any more
        return (NO, "nowork", None) if repo and repo.ok else (ASK, "noaccess", None)
    if "partial" in (review.verdict, review.head_verdict):
        return ASK, "near" if [w for w in review.required if w != "done"] == ["partial"] else "partial", None
    return (ASK, "other", None) if review.kind in ("tasks", "other") else (NO, "nothing", None)


def decide(u: User, repo: Repo | None, mark: LabMark | None, review: Review | None, base: Deadline | None,
           due: datetime | None, since: datetime | None, now: datetime) -> tuple[str, str, float | None]:
    """(answer, case, hours late)."""
    if mark and mark.met is not None:
        return (YES, "grace" if mark.grace else "word", None) if mark.met else (NO, "word_no", None)
    if not due:
        return WAIT, "nodue", None
    if mark and mark.open:
        return WAIT, "ext_open", None
    if due > now:
        return WAIT, "ext_run" if mark and mark.until else "ahead", None
    if not u.first_seen_at:
        return NO, "nosite", None
    if not u.github:
        return NO, "norepo", None
    at = sorted(utc(c.at) for c in repo.commits) if repo else []
    if review:  # «з подовженням» — work went on past the common deadline
        return by_review(repo, review, due, bool(mark and mark.until) and any(t <= due and (not base or t > utc(base.at)) for t in at),
                         bool(since) and not any(since < t <= due for t in at))
    if not at and repo and (repo.ok or repo.error == EMPTY):  # the pull calls an empty repository a failure too
        return NO, "empty", None
    if not repo or not repo.ok:
        return ASK, "noaccess", None
    if at[0] <= due:
        return WAIT, "unreviewed", None  # there is code, nobody has read it yet
    return ASK, "after", hours(at[0] - due)


def flags(u: User, n: int, repo: Repo | None, mark: LabMark | None, review: Review | None, due: datetime | None,
          answer: str, says: str | None) -> list[str]:
    """What to look at besides the case: the student's word against the facts, a review grown old, registration."""
    seen = (review.head or review.commit) if review else ""
    return [f for f, on in (
        ("says_more", says in ("ok", "ext") and answer in (NO, ASK)),
        ("says_less", says in ("work", "miss") and answer == YES),
        ("ext_unknown", says == "ext" and not (mark and (mark.asked or mark.until or mark.open))),
        ("fresh", bool(seen and repo and repo.head) and answer != YES and not repo.head.startswith(seen)),
        ("noaccess", bool(review and repo and not repo.ok)),
        ("nobot", bool(u.first_seen_at) and u.tg_chat_id is None),
        ("reg_late", n == 1 and bool(due) and any(t and utc(t) > due for t in (u.first_seen_at, u.tg_linked_at))),
    ) if on]


def fill(rows: list[dict], users: list[User], index: Index, polls: list[Poll], votes: dict[str, dict], labs: int,
         now: datetime | None = None) -> dict[int, Poll]:
    """`case` into every lab cell of the rows (core.table); returns lab → its status poll."""
    now, status = now or datetime.now(timezone.utc), status_polls(polls, labs)
    for row, u in zip(rows, users):
        since, repo = None, index.repos.get(u.email)
        for n in range(1, labs + 1):
            base, mark, review = due_for(index.deadlines, n, u.group), index.marks.get((u.email, n)), index.reviews.get((u.email, n))
            due = effective(mark, base)
            says, at = said(status[n], votes.get(u.email, {}).get(str(status[n].id))) if n in status else (None, None)
            answer, code, late = decide(u, repo, mark, review, base, due, since, now)
            row["labs"][str(n)]["case"] = {"answer": answer, "code": code, "late": late, "says": says, "said_at": at,
                                           "flags": flags(u, n, repo, mark, review, due, answer, says)}
            since = due or since
    return status
