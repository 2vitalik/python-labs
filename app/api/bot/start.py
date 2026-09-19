from aiogram import Router
from aiogram.filters import CommandObject, CommandStart
from aiogram.types import Message

from bot import texts
from bot.link import bind, by_token, sync
from models.user import User

router = Router()


@router.message.outer_middleware()
async def sync_username(handler, message: Message, data):
    data["user"] = await sync(message.chat.id, message.from_user.username or "")
    return await handler(message, data)


@router.message(CommandStart(deep_link=True))
async def start_link(message: Message, command: CommandObject):
    user = await by_token(command.args)
    if not user:
        await message.answer(texts.UNKNOWN)
        return
    prev_chat = user.tg_chat_id
    await bind(user, message.chat.id, message.from_user.username or "")
    await message.answer(texts.recorded(user, prev_chat))


@router.message(CommandStart(deep_link=False))
async def start(message: Message, user: User | None):
    await message.answer(texts.recorded(user, user.tg_chat_id) if user else texts.INTRO)


@router.message()
async def fallback(message: Message, user: User | None):
    await message.answer(texts.MORE_SOON if user else texts.INTRO)
