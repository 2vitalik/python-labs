"""/poll — makes a group or topic a place for polls without leaving a trace: `chats.seen` has already noted it,
the command itself is ephemeral or deleted at once; the answer is ephemeral too."""
from aiogram import Router, html
from aiogram.exceptions import TelegramAPIError
from aiogram.filters import Command
from aiogram.types import Message

from core.bot.chats import GROUPS
from core.bot.here import is_admin, title
from core.bot.notes import ack
from core.bot.notify import bot

router = Router()
COMMANDS = {"poll": "гілка для опитувань (команда зникає)"}  # registered as ephemeral

router.message.filter(Command(*COMMANDS), is_admin)


@router.message()
async def poll(message: Message):
    if message.chat.type not in GROUPS:
        await message.answer("☝️ /poll — у групі чи гілці форуму")
        return
    lines = [f"🗳 Сюди можна слати опитування: <b>{html.quote(title(message))}</b>"]
    if not message.ephemeral_message_id:
        try:
            await bot().delete_message(message.chat.id, message.message_id)
        except TelegramAPIError as e:
            lines.append(f"⚠️ Команду не прибрав: {html.quote(e.message)}\n☝️ боту потрібне право «Delete messages»")
    await ack(message, "\n".join(lines))
