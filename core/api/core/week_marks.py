"""«Мій тиждень» (T177): what the page sends is checked against the grid and put in order; how marks read in words."""
from collections import Counter

from fastapi import HTTPException

from core.models.week import Mark

DAYS = ("Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Нд")
EMOJI = {"no": "🔴", "meh": "🟡", "ok": "🟢"}
WHY, MOST = 200, 100  # a reason's length · marks in a week: a painted one has a dozen


def hm(minutes: int) -> str:
    return f"{minutes // 60}:{minutes % 60:02d}"


def label(m: Mark) -> str:
    return f"{DAYS[m.day]} {hm(m.start)}–{hm(m.end)}"


def clean(marks: list[Mark], frame: dict) -> list[Mark]:
    """In order, inside the grid and on its step, never one over another; neighbours of one kind and reason become one mark."""
    out: list[Mark] = []
    for m in sorted(marks, key=lambda m: (m.day, m.start)):
        inside = 0 <= m.day < frame["days"] and frame["from"] <= m.start < m.end <= frame["to"]
        if not inside or m.start % frame["step"] or m.end % frame["step"]:
            raise HTTPException(422, "Позначка поза сіткою тижня — онови сторінку")
        why = " ".join(m.why.split()) if m.kind == "no" else ""
        if len(why) > WHY:
            raise HTTPException(422, f"Причина — до {WHY} символів")
        last = out[-1] if out else None
        if last and last.day == m.day and m.start < last.end:
            raise HTTPException(422, f"Позначки перетинаються: {label(last)} і {label(m)}")
        if last and (last.day, last.end, last.kind, last.why) == (m.day, m.start, m.kind, why):
            last.end = m.end
        else:
            out.append(Mark(day=m.day, start=m.start, end=m.end, kind=m.kind, why=why))
    if len(out) > MOST:
        raise HTTPException(422, f"Забагато позначок: більше за {MOST}")
    return out


def missing_why(marks: list[Mark]) -> list[str]:
    return [label(m) for m in marks if m.kind == "no" and not m.why]


def summary(marks: list[Mark]) -> str:
    """«🔴 3 · 🟡 2 · 🟢 4» — marks of each kind: what a row of the history says."""
    n = Counter(m.kind for m in marks)
    return " · ".join(f"{emoji} {n[kind]}" for kind, emoji in EMOJI.items() if n[kind]) or "без позначок"


def days_label(days: list[int]) -> str:
    """[0, 1, 2, 3, 4] → «Пн–Пт», [1, 3] → «Вт, Чт»."""
    row = len(days) > 2 and days == list(range(days[0], days[0] + len(days)))
    return f"{DAYS[days[0]]}–{DAYS[days[-1]]}" if row else ", ".join(DAYS[d] for d in days)


def spans(marks: list[Mark]) -> str:
    """«Вт, Чт 18:00–19:30 · Сб 15:00–17:00» — days with the same hours go together."""
    days: dict[tuple[int, int], list[int]] = {}
    for m in marks:
        days.setdefault((m.start, m.end), []).append(m.day)
    return " · ".join(f"{days_label(d)} {hm(start)}–{hm(end)}" for (start, end), d in days.items())


def by_reason(marks: list[Mark]) -> dict[str, list[Mark]]:
    """The «не можу» marks under their reasons, in the order they come."""
    out: dict[str, list[Mark]] = {}
    for m in marks:
        if m.kind == "no":
            out.setdefault(m.why, []).append(m)
    return out


def words(marks: list[Mark]) -> str:
    """«🔴 Вт, Чт 18:00–19:30 — 🏋️ тренування · 🟡 Пн 21:00–23:00» — a week in one line."""
    red = [f"🔴 {spans(ms)}" + (f" — {why}" if why else "") for why, ms in by_reason(marks).items()]
    return " · ".join(red + [f"{EMOJI[kind]} {spans(ms)}" for kind in ("meh", "ok") if (ms := [m for m in marks if m.kind == kind])])
