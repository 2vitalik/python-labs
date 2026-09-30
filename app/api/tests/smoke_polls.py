"""Smoke: polls on the bot's side (T176) — votes, Telegram's counts, the file copy and its replay, the places polls go to.
Run from app/api: DB_NAME=python_labs_smoke uv run python tests/smoke_polls.py"""
import asyncio
import os
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, os.getcwd())
from pymongo import MongoClient  # noqa: E402

DB = os.environ["DB_NAME"]
assert DB.endswith("_smoke"), "refuse to run on a non-smoke DB"
MongoClient().drop_database(DB)
from aiogram.methods import SendPoll  # noqa: E402
from aiogram.types import Chat, ChatMemberUpdated, ForumTopicCreated, Message, PollAnswer, PollOption, Update  # noqa: E402
from aiogram.types import Poll as TgPoll  # noqa: E402
from aiogram.types import User as TgUser  # noqa: E402

from core import polls_replay  # noqa: E402
from core.bot import chats, notify, polls, spot  # noqa: E402
from core.bot.run import build  # noqa: E402
from core.models.message import TgMessage  # noqa: E402
from core.models.poll import Option, Poll  # noqa: E402
from core.models.poll_send import PollSend  # noqa: E402
from core.models.user import Status, User  # noqa: E402
from core.models.vote import TgChat, Vote  # noqa: E402
from db import init_db  # noqa: E402

NOW = datetime(2026, 9, 30, 12, 0, tzinfo=timezone.utc)
VASYA = TgUser(id=42, is_bot=False, first_name="Вася", username="vasya_tg")
FORUM = Chat(id=-100, type="supergroup", title="ПЗПІ-25 Python", is_forum=True)
polls.LOG = Path(tempfile.mkdtemp()) / "logs" / "poll_updates.jsonl"
results, handled = [], []


def check(name, cond, extra=""):
    results.append(bool(cond))
    print(("PASS " if cond else "FAIL ") + name + (f" · {extra}" if extra and not cond else ""))


def answer(update_id, ids, poll_id="p1", **who):
    a = PollAnswer(poll_id=poll_id, option_ids=ids, option_persistent_ids=[str(i) for i in ids], **(who or {"user": VASYA}))
    return a, Update(update_id=update_id, poll_answer=a)


def tg_poll(total, counts, closed=False, poll_id="p1"):
    options = [PollOption(persistent_id=str(i), text=f"#{i}", voter_count=n) for i, n in enumerate(counts)]
    return TgPoll(id=poll_id, question="Хто на парі?", options=options, total_voter_count=total, is_closed=closed, is_anonymous=False,
                  type="regular", allows_multiple_answers=False, allows_revoting=True, members_only=False)


def lines() -> int:
    return len(polls.LOG.read_text(encoding="utf-8").splitlines()) if polls.LOG.exists() else 0


def forum_msg(message_id, thread=None, reply=None, chat=FORUM, **extra):
    return Message(message_id=message_id, date=NOW, chat=chat, from_user=VASYA, text="привіт", message_thread_id=thread,
                   is_topic_message=bool(thread) or None, reply_to_message=reply, **extra)


async def handler(event, data):
    handled.append(event)
    return "ok"


async def run():
    await init_db()
    used = set(build().resolve_used_update_types())
    check("the bot asks Telegram for polls: poll, poll_answer, my_chat_member", {"poll", "poll_answer", "my_chat_member", "message"} <= used, used)
    check("alert kind `poll` exists", "poll" in notify.KINDS)

    await User(email="vasya@nure.ua", status=Status.student, tg_chat_id=42).insert()
    poll = await Poll(title="Пара 3", question="Хто на парі?", options=[Option(emoji="✅", text="так"), Option(emoji="❌", text="ні")],
                      status="open", by="admin@nure.ua").insert()
    send = await PollSend(poll=poll.id, chat_id=-100, thread_id=5, where="форум", status="sent", tg_poll_id="p1", message_id=9).insert()

    a, u = answer(1, [0])
    await polls.answered(a, u)
    v = await Vote.find_one(Vote.update_id == 1)
    check("vote: saved with the linked student, our poll and a feed line", v and v.user == "vasya@nure.ua" and v.poll == poll.id
          and v.tg_id == 42 and v.username == "vasya_tg" and v.text == "Пара 3: ✅ так" and v.raw.get("poll_id") == "p1", v)
    check("…and the raw update is on disk first", lines() == 1)

    await polls.answered(a, u)
    check("the same update delivered twice: one vote", await Vote.count() == 1 and lines() == 2)

    await polls.answered(*answer(2, []))
    check("vote taken back: a new row, empty ids, ↩︎ in the text", (await Vote.find_one(Vote.update_id == 2)).text == "Пара 3: ↩︎ відкликано")

    await polls.answered(*answer(3, [1], voter_chat=FORUM))
    v = await Vote.find_one(Vote.update_id == 3)
    check("an admin voting as the chat: no tg id, the chat's title", v and v.tg_id is None and v.username == "ПЗПІ-25 Python" and v.user == "")

    await polls.answered(*answer(1, [1], poll_id="other"))
    v = await Vote.find_one(Vote.tg_poll_id == "other")
    check("a poll we do not know: kept anyway; the same update id in another poll is not a repeat", v and v.poll is None and v.text == "")

    await polls.counted(tg_poll(3, [2, 1]), Update(update_id=5, poll=tg_poll(3, [2, 1])))
    send = await PollSend.get(send.id)
    check("Telegram's count lands on the send", send.state["total"] == 3 and send.state["counts"] == [2, 1] and send.status == "sent")

    await polls.counted(tg_poll(3, [2, 1], closed=True), Update(update_id=6, poll=tg_poll(3, [2, 1], closed=True)))
    send = await PollSend.get(send.id)
    check("poll stopped in Telegram: the send is closed", send.status == "closed" and send.closed_at and send.state["is_closed"])

    await polls.counted(tg_poll(1, [1], poll_id="stranger"), Update(update_id=7, poll=tg_poll(1, [1], poll_id="stranger")))
    check("a count for a poll we do not know: only on disk", lines() == 8 and await PollSend.count() == 1)

    await Vote.find(Vote.update_id == 1, Vote.tg_poll_id == "p1").delete()
    seen, added = await polls_replay.replay(polls.LOG)
    check("replay: the vote Mongo lost is back, with its text", added == 1 and (await Vote.find_one(Vote.update_id == 1, Vote.tg_poll_id == "p1")).text
          == "Пара 3: ✅ так", (seen, added))
    seen, added = await polls_replay.replay(polls.LOG)
    check("replay again: nothing doubled", added == 0 and seen == 5 and await Vote.count() == 4, (seen, added))

    topic = Message(message_id=5, date=NOW, chat=FORUM, forum_topic_created=ForumTopicCreated(name="25-1 пари", icon_color=0))
    r = await chats.seen(handler, forum_msg(10, thread=5, reply=topic), {})
    place = await TgChat.find_one(TgChat.chat_id == -100, TgChat.thread_id == 5)
    check("a message in a topic: the place noted with the topic's name, the message went on", r == "ok" and place
          and place.where == "ПЗПІ-25 Python › 25-1 пари" and not place.left)
    await place.set({TgChat.name: "Пари 25-1", TgChat.hidden: True})
    await chats.seen(handler, forum_msg(11, thread=5), {})
    place = await TgChat.get(place.id)
    check("later messages keep the admin's name and choice", place.name == "Пари 25-1" and place.hidden and place.topic == "25-1 пари")
    await chats.seen(handler, forum_msg(12), {})
    await chats.seen(handler, forum_msg(13, chat=Chat(id=42, type="private")), {})
    check("General topic — the chat itself; a private chat — not a place", await TgChat.find_one(TgChat.chat_id == -100, TgChat.thread_id == None)  # noqa: E711
          and await TgChat.count() == 2 and len(handled) == 4)

    def member(status):
        return ChatMemberUpdated(chat=FORUM, from_user=VASYA, date=NOW, old_chat_member={"status": "member", "user": VASYA},
                                 new_chat_member={"status": status, "user": {"id": 1, "is_bot": True, "first_name": "bot"}})
    await chats.joined(handler, member("left"), {})
    check("the bot thrown out: every place of the chat is left", await TgChat.find(TgChat.left == True).count() == 2)  # noqa: E712
    await chats.joined(handler, member("member"), {})
    check("…and back: the chat itself is a place again", not (await TgChat.find_one(TgChat.chat_id == -100, TgChat.thread_id == None)).left)  # noqa: E711

    broken = chats.note

    async def boom(*args):
        raise RuntimeError("mongo down")
    chats.note = boom
    r = await chats.seen(handler, forum_msg(14, thread=5), {})
    chats.note = broken
    check("noting a place fails: the message still goes on", r == "ok" and len(handled) == 7)

    deleted, said = [], []

    class FakeBot:
        async def delete_message(self, chat_id, message_id):
            deleted.append((chat_id, message_id))
    spot.bot, spot.ack = FakeBot, lambda m, text: said.append(text) or asyncio.sleep(0)
    await chats.seen(lambda m, data: spot.poll(m), forum_msg(15, thread=7, reply=topic), {})
    check("/poll in a topic: the place noted, the command deleted, the answer names the topic",
          await TgChat.find_one(TgChat.chat_id == -100, TgChat.thread_id == 7) and deleted == [(-100, 15)] and "25-1 пари" in said[-1],
          (deleted, said))

    async def make_request(bot, method):
        return Message(message_id=99, date=NOW, chat=FORUM, poll=tg_poll(0, [0, 0]), from_user=TgUser(id=1, is_bot=True, first_name="bot"))
    await notify.outgoing(make_request, None, SendPoll(chat_id=-100, question="Хто на парі?", options=["✅ так", "❌ ні"]))
    row = await TgMessage.find_one(TgMessage.message_id == 99)
    check("a sent poll is in the message log with its question", row and row.dir == "out" and row.text == "Хто на парі?"
          and row.content_type == "poll")

asyncio.run(run())
ok = sum(results)
print(f"\n{ok}/{len(results)} PASS")
sys.exit(0 if ok == len(results) else 1)
