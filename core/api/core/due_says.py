"""What the student says of a deadline themselves (T340): the lab's status poll — «✅ вклався · ☑️ з подовженням ·
⏱️ ще працюю · 🚫 не вклався». A poll is one when it is tagged `labN`, takes a single answer and offers both ✅ and 🚫."""
from core.models.poll import Poll

WORDS = {"✅": "ok", "☑": "ext", "⏱": "work", "🚫": "miss", "💬": "other"}


def word(emoji: str) -> str | None:
    return WORDS.get(emoji.replace("️", ""))


def status_polls(polls: list[Poll], labs: int) -> dict[int, Poll]:
    """Lab → its status poll; `polls` come newest first, so a poll asked again wins."""
    out: dict[int, Poll] = {}
    for p in polls:
        if p.multiple or not {"ok", "miss"} <= {word(o.emoji) for o in p.options}:
            continue
        for n in range(1, labs + 1):
            if f"lab{n}" in p.tags:
                out.setdefault(n, p)
    return out


def said(poll: Poll, vote: dict | None) -> tuple[str | None, str | None]:
    """(the word, when) off a student's latest vote — `{ids, at}` as core.table.answers gives it; a vote taken back says nothing."""
    if not vote or not vote["ids"] or vote["ids"][0] >= len(poll.options):
        return None, None
    return word(poll.options[vote["ids"][0]].emoji), vote["at"]
