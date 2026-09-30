"""The two ways to look at votes (T174): one poll as Telegram shows it, and the table — students × polls."""
from datetime import datetime, timedelta, timezone

from bson import ObjectId

from core.models.history import stamp
from core.models.poll import Poll
from core.models.poll_send import PollSend
from core.polls_read import latest, mismatch, order, people, staff, student, votes_of, who


async def results(poll: Poll) -> dict:
    """Per answer — who chose it; who took the vote back; which students with the bot have not voted; every vote as it came.
    Teachers' and test students' votes are tries, kept apart: a teacher is never «on the class» of their own poll."""
    sends = await PollSend.find(PollSend.poll == poll.id).sort("at").to_list()
    votes = await votes_of(sends)
    users, by_tg = await people()
    where = {s.tg_poll_id: s.where for s in sends}
    options = [o.model_dump() | {"voters": []} for o in poll.options]
    retracted, tries = [], []
    for v in latest(votes, by=lambda v: 0).values():
        entry = {"who": who(v, by_tg), "at": stamp(v.at), "where": where[v.tg_poll_id]}
        if staff(by_tg.get(v.tg_id)):
            tries.append(entry | {"ids": v.option_ids})
            continue
        for i in v.option_ids:
            if i < len(options):
                options[i]["voters"].append(entry)
        if not v.option_ids:
            retracted.append(entry)
    for o in options:
        o["voters"].sort(key=lambda e: order(e["who"]))
    voted = {v.tg_id for v in votes}
    missing = {}
    for u in sorted(users, key=lambda u: (u.group, u.last_name, u.first_name)):
        if student(u) and u.tg_chat_id and u.tg_chat_id not in voted:
            missing.setdefault(u.group, []).append(u.person())
    return {"poll": poll.api(), "sends": [s.api() | {"mismatch": mismatch(s, votes)} for s in sends], "options": options,
            "retracted": retracted, "tries": tries, "missing": [{"group": g, "people": p} for g, p in missing.items()],
            "unlinked": sum(1 for u in users if student(u) and not u.tg_chat_id),
            "timeline": [{"who": who(v, by_tg), "at": stamp(v.at), "ids": v.option_ids, "where": where[v.tg_poll_id]} for v in reversed(votes)],
            "can_delete": all(staff(by_tg.get(v.tg_id)) for v in votes)}  # nobody's answer but the teachers' own tries


async def matrix(tag: str, template: str, days: int) -> dict:
    """Rows — students (not test ones); a cell — the student's answer in that poll. Everyone else who voted goes to `others`,
    so no vote is out of sight."""
    q = {"status": {"$ne": "draft"}}
    if tag:
        q["tags"] = tag
    if ObjectId.is_valid(template):
        q["template"] = ObjectId(template)
    if days:
        q["sent_at"] = {"$gte": datetime.now(timezone.utc) - timedelta(days=days)}
    polls = await Poll.find(q).sort("sent_at").to_list()
    sends = await PollSend.find({"poll": {"$in": [p.id for p in polls]}}).to_list()
    votes, poll_of = await votes_of(sends), {s.tg_poll_id: str(s.poll) for s in sends if s.tg_poll_id}
    users, by_tg = await people()
    rows = {u.email: u.person() | {"tg_linked": u.tg_chat_id is not None, "cells": {}}
            for u in sorted(filter(student, users), key=lambda u: (u.group, u.last_name, u.first_name))}
    others = {}
    for (poll, k), v in latest(votes, by=lambda v: poll_of[v.tg_poll_id]).items():
        cell = {"ids": v.option_ids, "at": stamp(v.at)}
        user = by_tg.get(v.tg_id)
        if user and user.email in rows:
            rows[user.email]["cells"][poll] = cell
        else:
            others.setdefault(k, {"who": who(v, by_tg), "cells": {}})["cells"][poll] = cell
    return {"polls": [p.api() for p in polls], "rows": list(rows.values()),
            "others": sorted(others.values(), key=lambda o: order(o["who"]))}
