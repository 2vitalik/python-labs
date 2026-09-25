from aiogram import F, Router
from aiogram.filters import CommandObject, CommandStart
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent, LinkPreviewOptions, Message

from aiogram import html

from bot import texts
from bot.alerts import who
from bot.link import bind, by_token, sync
from bot.notes import HINT
from models.user import Status, User

router = Router()
router.message.filter(F.chat.type == "private")  # in groups the bot only listens to /here


@router.message.outer_middleware()
async def sync_username(handler, message: Message, data):
    data["user"] = await sync(message.chat.id, message.from_user.username or "")
    return await handler(message, data)


async def student_card(tg_id: str) -> str:
    """/start bizChat<id>: the teacher opened the bot from a student's chat (T137) — who that is + the note commands."""
    student = await User.find_one(User.tg_chat_id == int(tg_id)) if tg_id.isdigit() else None
    if not student:
        return f"🎓 tg {html.quote(tg_id)} · <i>бота ще не привʼязав</i>\n{HINT}"
    return f"🎓 {who(student)}" + (f" · @{student.tg_username}" if student.tg_username else "") + f"\n{HINT}"


@router.message(CommandStart(deep_link=True))
async def start_link(message: Message, command: CommandObject, user: User | None = None):
    if command.args.startswith("bizChat") and user and user.status == Status.admin:
        await message.answer(await student_card(command.args.removeprefix("bizChat")))
        return
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


@router.guest_message()
async def guest(message: Message):
    """@mentioned in a chat the bot is not in (Guest Mode): one visible reply — the intro."""
    content = InputTextMessageContent(message_text=texts.INTRO, parse_mode="HTML", link_preview_options=LinkPreviewOptions(is_disabled=True))
    await message.answer_guest_query(InlineQueryResultArticle(id="intro", title="Python Labs", input_message_content=content))
