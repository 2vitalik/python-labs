"""A chat pasted from Telegram (T230): the clipboard text of selected messages → rows the way bot/log.py sees them."""
import re
from datetime import datetime

from core.activity_people import TZ
from core.models.user import User

# «Імʼя, [24.10.2026 12:34]»: the clients' header of a copied message. A time inside the brackets tells it from a line of text
# like «Ок, [чекаю]»; a header-looking line whose date still makes no sense is reported, not swallowed
HEAD_RE = re.compile(r"^(?P<name>.+?), \[(?P<when>[^\]]*\d{1,2}:\d{2}[^\]]*)\]$")
MONTHS = "jan feb mar apr may jun jul aug sep oct nov dec".split()
DATE_RES = [re.compile(p, re.I) for p in (
    r"(?P<d>\d{1,2})[./](?P<m>\d{1,2})[./](?P<y>\d{2,4})",
    r"(?P<y>\d{4})-(?P<m>\d{2})-(?P<d>\d{2})",
    r"(?P<d>\d{1,2}) (?P<mon>[a-z]{3})[a-z]* (?P<y>\d{4})",
    r"(?P<mon>[a-z]{3})[a-z]* (?P<d>\d{1,2}),? (?P<y>\d{4})",
)]
TIME_RE = re.compile(r"(?P<h>\d{1,2}):(?P<i>\d{2})(?::(?P<s>\d{2}))?\s*(?P<ap>[ap]m)?", re.I)


def when(text: str) -> datetime | None:
    """`24.10.2026 12:34`, `24.10.26 12:34`, `2026-10-24 12:34`, `24 Oct 2026 at 12:34 PM` — the teacher's zone, as the client shows."""
    date = next((m for r in DATE_RES if (m := r.search(text))), None)
    clock = date and TIME_RE.search(text[date.end():])
    if not clock:
        return None
    g = date.groupdict()
    month = MONTHS.index(g["mon"][:3].lower()) + 1 if g.get("mon") else int(g["m"])
    year = int(g["y"]) + (2000 if len(g["y"]) == 2 else 0)
    hour = int(clock["h"]) % 12 + (12 if clock["ap"].lower() == "pm" else 0) if clock["ap"] else int(clock["h"])
    try:
        return datetime(year, month, int(g["d"]), hour, int(clock["i"]), int(clock["s"] or 0), tzinfo=TZ)
    except ValueError:
        return None


def parse_paste(text: str) -> tuple[list[dict], list[str]]:
    """Messages `{name, at, text}` in paste order; `errors` — header-like lines whose date made no sense (an unknown client format
    should be seen, not swallowed into the previous message). Text before the first header is dropped."""
    rows, errors = [], []
    for line in text.splitlines():
        if m := HEAD_RE.match(line.strip()):
            if at := when(m["when"]):
                rows.append({"name": m["name"].strip(), "at": at, "lines": []})
            else:
                errors.append(line.strip())
        elif rows:
            rows[-1]["lines"].append(line)
    for r in rows:
        r["text"] = "\n".join(r.pop("lines")).strip()
    return rows, errors


def words(*names: str) -> set[str]:
    return {w.lower() for n in names for w in n.replace("_", " ").split()}


def guess(authors: list[str], student: User, admin: User) -> str:
    """Which pasted name is the student: one sharing a word with their names or nick; else whoever is not the teacher."""
    theirs = words(student.name, student.last_name, student.first_name, student.tg_username, *student.aliases)
    mine = words(admin.name, admin.last_name, admin.first_name, admin.tg_username)
    hits = [a for a in authors if words(a) & theirs] or [a for a in authors if not words(a) & mine]
    return (hits or authors or [""])[0]
