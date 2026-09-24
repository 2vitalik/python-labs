"""Who a note is about and how the student gets to see it (T134); the handlers are in notes.py."""
from aiogram import html
from aiogram.exceptions import TelegramAPIError
from aiogram.types import EphemeralMessageParameters, InlineQueryResultArticle, InputTextMessageContent, Message, ReplyParameters

from bot import notify
from models.user import User


async def target(message: Message, text: str) -> tuple[User | None, int | None, str]:
    """The student: the chat's owner (Chat Automation, guest), the replied-to sender, or the first word — nick or @username."""
    reply = message.reply_to_message
    if reply and reply.from_user and not reply.forum_topic_created:  # a topic message «replies» to the topic itself
        return await User.find_one(User.tg_chat_id == reply.from_user.id), reply.from_user.id, text
    if message.business_connection_id or message.guest_query_id:
        return await User.find_one(User.tg_chat_id == message.chat.id), message.chat.id, text
    nick, _, rest = text.partition(" ")
    nick = nick.lstrip("@")
    student = (await User.by_nick(nick) or await User.find_one(User.tg_username == nick)) if nick else None
    return student, student.tg_chat_id if student else None, rest


async def show(message: Message, student: User | None, text: str, admin: User) -> str:
    """Deliver a visible note the best way there is; returns where the student sees it, "" if nowhere."""
    line = f"📝 {html.quote(text)}"
    if message.guest_query_id:  # as the bot itself, right in that chat
        await message.answer_guest_query(InlineQueryResultArticle(id="note", title="📝", input_message_content=InputTextMessageContent(message_text=line)))
        return "від бота у вашому чаті"
    if message.business_connection_id:  # as the teacher — clients show no bot mark, hence 🤖
        try:
            await notify.bot().send_message(message.chat.id, f"🤖 {line}", business_connection_id=message.business_connection_id)
            return "у вашому чаті"
        except TelegramAPIError:  # no reply right, or the student was silent for 24 h → fall back to the bot's chat
            pass
    elif message.chat.type != "private":  # the forum: in the thread, as a reply when the command was one
        reply = message.reply_to_message
        if reply and not reply.forum_topic_created:
            await message.answer(line, reply_parameters=ReplyParameters(message_id=reply.message_id))
        else:
            name = f"@{student.tg_username}" if student and student.tg_username else student.first_name if student else ""
            await message.answer(f"📝 {html.quote(name)} {html.quote(text)}")
        return "у форумі"
    if student and student.tg_chat_id:
        await notify.bot().send_message(student.tg_chat_id, f"📝 {html.quote(admin.first_name or admin.name)}: {html.quote(text)}")
        return "особисто від бота"
    return ""


async def ack(message: Message, text: str) -> None:
    """In groups the answer is ephemeral — only the teacher sees it."""
    if message.chat.type == "private":
        await message.answer(text)
    else:
        await message.answer(text, ephemeral_message_parameters=EphemeralMessageParameters(receiver_user_id=message.from_user.id))
