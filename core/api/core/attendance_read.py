"""The attendance rows as the pages read them (T222): names → students by lesson_people.match, so an alias added later
counts too; the teacher apart; unknown names for the admin only."""
from collections import Counter

from core.attendance import cell, span, view
from core.lesson_people import known, match
from core.models.attendance import Attendance
from core.models.lesson import Lesson
from core.models.user import Status


async def attendance(l: Lesson, admin: bool) -> dict:
    """The lesson's block: students, the teacher apart, unknown names for the admin only (a student sees how many).
    `of` — students of the lesson's groups in the registry, the «із 57»."""
    found = await Attendance.find(Attendance.lesson == l.slug).to_list()
    users = await known()
    who = match([a.name for a in found], users)
    total = span(l)
    out = {"meeting": l.zoom.model_dump(), "seconds": total, "people": [], "teachers": [], "unknown": [], "others": 0,
           "of": sum(1 for u in users if u.status == Status.student and not u.test and (not l.groups or u.group in l.groups))}
    for a in found:
        u = who.get(a.name)
        if u and u.status == Status.admin:
            out["teachers"].append(view(a, u, total, admin))
        elif u:
            out["people"].append(view(a, u, total, admin))
        else:
            out["others"] += 1
            if admin:
                out["unknown"].append(view(a, None, total, admin))
    return out


async def matrix() -> dict:
    """Students × lessons with a pull: seconds in each cell; `unknown` — names of that lesson nobody is yet."""
    lessons = await Lesson.find({"zoom.uuid": {"$ne": ""}}).sort("date", "kind", "n").to_list()
    found = await Attendance.find({"lesson": {"$in": [l.slug for l in lessons]}}).to_list()
    users = await known()
    who = match(list({a.name for a in found}), users)
    spans = {l.slug: span(l) for l in lessons}
    cells: Counter = Counter()
    unknown: Counter = Counter()
    for a in found:
        u = who.get(a.name)
        if u and u.status == Status.student:
            cells[(u.nick, a.lesson)] += a.seconds  # two aliases of one student in one meeting add up
        elif not u:
            unknown[a.lesson] += 1
    return {"lessons": [l.row() | {"seconds": spans[l.slug], "unknown": unknown[l.slug]} for l in lessons],
            "rows": [u.person() | {"cells": {s: cell(cells[(u.nick, s)], spans[s]) for s in spans if (u.nick, s) in cells}}
                     for u in users if u.status == Status.student and not u.test]}
