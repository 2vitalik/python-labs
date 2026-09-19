from aiogram import Router
from aiogram.filters import CommandObject, CommandStart
from aiogram.types import Message

from bot.link import bind

router = Router()

LINK_HINT = "Відкрий свій профіль на сайті й натисни «Привʼязати бота»."


@router.message(CommandStart(deep_link=True))
async def start_link(message: Message, command: CommandObject):
    user = await bind(command.args, message.chat.id, message.from_user.username or "")
    if not user:
        await message.answer("Не знаю такого посилання. " + LINK_HINT)
        return
    await message.answer(f"Привіт, {user.first_name or user.name or user.nick}! Записав тебе ✅")


@router.message(CommandStart(deep_link=False))
async def start(message: Message):
    await message.answer("Привіт! Я бот Python Labs. " + LINK_HINT)


@router.message()
async def fallback(message: Message):
    await message.answer("Поки що вмію лише /start, далі буде 🙂")
