"""Who speaks in a transcript → a student of the site: by the names Zoom shows (User.aliases, the admin adds them once)
or by ПІБ as the registry writes it; the teacher goes by first name (merge.md)."""
import re

from core.models.user import Status, User

SPEAKER = re.compile(r"^\*\*([^*]+)\*\*(?: · \d{1,2}:\d{2})? — ", re.M)


def speakers(transcript: str) -> list[str]:
    """Names as written, in order of first appearance."""
    return list(dict.fromkeys(m.strip() for m in SPEAKER.findall(transcript)))


def names(u: User) -> set[str]:
    out = {a.strip().lower() for a in u.aliases if a.strip()}
    if u.last_name and u.first_name:
        out |= {f"{u.last_name} {u.first_name}".lower(), f"{u.first_name} {u.last_name}".lower()}
    if u.status == Status.admin and u.first_name:
        out.add(u.first_name.lower())
    return out


async def known() -> list[User]:
    return await User.find(User.status != Status.pending).to_list()


def match(who: list[str], users: list[User]) -> dict[str, User]:
    by = {}
    for u in users:
        for n in names(u):
            by.setdefault(n, u)
    return {w: by[w.lower()] for w in who if w.lower() in by}


async def people(transcript: str) -> dict[str, dict]:
    """speaker as written → person(); unmatched speakers are left out — the page shows them by name alone."""
    who = speakers(transcript)
    return {w: u.person() for w, u in match(who, await known()).items()} if who else {}


def roster(users: list[User]) -> dict[str, str]:
    """For the merge (meta.yml): a name in Zoom → «Імʼя Прізвище» as the transcript should write it."""
    out = {}
    for u in users:
        if u.first_name and u.last_name:
            for a in u.aliases:
                out[a] = u.first_name if u.status == Status.admin else f"{u.first_name} {u.last_name}"
    return out
