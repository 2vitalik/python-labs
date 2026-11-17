"""Defenses and their remarks as the API gives them (T327, T328). Three readers: the teacher gets everything, an agent —
all but the teacher's impressions and note, a student — own remarks once they are sent, in the student's words only."""
import re

from core.config import settings
from core.models.history import when
from core.models.user import User
from models.defense import Defense, Remark

PRIVATE = ("facts", "rates", "marks", "note", "rank", "scale")  # the teacher's own
OPEN = ("open", "answered", "returned")  # sent and not closed yet
PIN = re.compile(r"^https://github\.com/[^/]+/[^/]+/(commit/[0-9a-f]{7,40}|blob/[0-9a-f]{40}/|pull/\d+)")


def link_note(link: str, repo: str) -> str:
    """What to tell about an answer's link: "" — fine · branch — its lines will shift · foreign — not the student's repo."""
    if not link:
        return ""
    if repo and not link.lower().startswith(repo.lower().removesuffix(".git").rstrip("/") + "/"):
        return "foreign"
    return "" if PIN.match(link) else "branch"


def stamped(d: dict) -> dict:
    return d | {"at": when(d["at"])} if d.get("at") else d


def remark(r: Remark, reader: str = "teacher", repo: str = "") -> dict:
    """`reader`: teacher · agent · student."""
    coins = settings.remark_coins == "open" or (reader != "student" and settings.remark_coins != "off")
    row = {"id": str(r.id), "defense": str(r.defense), "text": r.text, "tags": r.tags, "kind": r.kind, "state": r.state, "order": r.order,
           "at": when(r.created_at), "reply": stamped(r.reply) | ({"link_note": link_note(r.reply.get("link", ""), repo)} if r.reply else {}),
           "check": stamped({k: v for k, v in r.check.items() if k != "by"}), "coin": r.coin if coins else "", "amount": r.amount if coins else 0}
    if reader == "student":
        return row
    return row | {"raw": r.raw, "hint": r.hint, "own": r.own, "agent": stamped(r.agent)}


def counts(remarks: list[Remark]) -> dict:
    """How many remarks stand where; `debts` — the ones that block «зараховано»."""
    out = {s: sum(r.state == s for r in remarks) for s in ("draft", "open", "answered", "accepted", "returned")}
    return out | {"all": len(remarks), "debts": sum(r.kind == "debt" and r.state != "accepted" for r in remarks)}


def minutes(d: Defense) -> int | None:
    return round((d.ended_at - d.started_at).total_seconds() / 60) if d.started_at and d.ended_at else None


def defense(d: Defense, owner: User | None, remarks: list[Remark], reader: str = "teacher") -> dict:
    """A row of the list; the page adds the remarks themselves."""
    row = {"id": str(d.id), "labs": d.labs, "kind": d.kind, "started_at": when(d.started_at), "ended_at": when(d.ended_at),
           "minutes": minutes(d), "result": d.result, "sent_at": when(d.sent_at), "counts": counts(remarks)}
    if reader == "student":
        return row
    who = owner.person() | {"github": owner.github} if owner else {"nick": d.student.split("@")[0], "name": d.student, "group": ""}
    return row | {"student": who, "link": d.link} | ({k: getattr(d, k) for k in PRIVATE} if reader == "teacher" else {})


async def of_student(email: str, but=None) -> list[Defense]:
    """The student's defenses, the newest first; `but` — all except this one."""
    return [d for d in await Defense.find(Defense.student == email).sort("-created_at").to_list() if d.id != but]


async def debts(email: str, but) -> list[Remark]:
    """What the student still owes from the other defenses: sent, not accepted, a tip aside."""
    return await Remark.find({"student": email, "defense": {"$ne": but}, "state": {"$in": OPEN}, "kind": {"$ne": "tip"}}).sort("created_at").to_list()
