from datetime import datetime, timezone
from typing import Annotated, Literal

from beanie import Document, Indexed
from core.models.history import when
from pydantic import BaseModel, Field
from pymongo import IndexModel

Verdict = Literal["done", "partial", "none"]


class Commit(BaseModel):
    sha: str
    at: datetime  # the committer's clock
    authored: datetime | None = None  # the author's, when it differs — a rewritten history or `--date`
    author: str = ""
    msg: str = ""  # the first line
    files: int = 0
    add: int = 0
    rm: int = 0
    seen: datetime | None = None  # when our pull first saw it: the upper bound of when it really appeared


class Repo(Document):
    """A student's repository as the last pull saw it (T235): the link, the branch, the commit log — the site counts
    the facts of a lab off the log, for any deadline, without cloning anything itself."""
    user: Annotated[str, Indexed(unique=True)]  # email
    url: str
    ok: bool = True
    error: str = ""  # why the pull failed, for the teacher
    branch: str = ""
    head: str = ""
    commits: list[Commit] = []
    pulled_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    by: str = ""  # the agent that pushed the facts

    class Settings:
        name = "repos"

    def api(self) -> dict:
        """The short card for a row: no log."""
        when_ = [c.at for c in self.commits]
        return {"url": self.url, "ok": self.ok, "error": self.error, "branch": self.branch, "head": self.head[:7],
                "commits": len(self.commits), "first": when(min(when_, default=None)), "last": when(max(when_, default=None)),
                "pulled_at": when(self.pulled_at)}


class Review(Document):
    """The agent's report on one student and one lab (T235): the cut commit before the deadline and the verdict on it;
    the head too, when looked at. One document per pair, rewritten with history."""
    user: str
    lab: int
    commit: str  # the cut reviewed
    verdict: Verdict
    head: str = ""
    head_verdict: Verdict | Literal[""] = ""
    summary: str = ""  # one line for the cell
    report: str = ""  # markdown
    by: str = ""
    at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "reviews"
        indexes = [IndexModel([("user", 1), ("lab", 1)], unique=True)]

    def api(self, full: bool = False) -> dict:
        data = {"commit": self.commit[:7], "verdict": self.verdict, "head": self.head[:7], "head_verdict": self.head_verdict,
                "summary": self.summary, "by": self.by.split("@")[0], "at": when(self.at)}
        return data | ({"report": self.report} if full else {})
