"""Bot replies. Style (T109): every line opens with an emoji naming its role, one thought per line,
no trailing periods, ")" instead of a smiley; bold for names/buttons/links, italic for asides."""
from aiogram import html

from config import settings
from models.user import User

STEPS = (f'🌐 відкрий <b><a href="{settings.site_url}/profile">свій профіль</a></b> на сайті\n'
         "✅ й натисни <b>«Привʼязати бота»</b>")
INTRO = "👋 Привіт!\n🤖 Я бот <b>Python Labs</b>\n\n➕ <i>Якщо ти студент цього курсу:</i>\n" + STEPS
UNKNOWN = "👋 Привіт!\n❌ Не впізнаю це посилання — мабуть, застаріле\n\n" + STEPS
MORE_SOON = "🤖 Поки що більше нічого не вмію — далі буде)"
NO_USERNAME = "☝️ У тебе в Telegram немає юзернейму — додай його в налаштуваннях, щоб тобі можна було написати"


def recorded(user: User, prev_chat: int | None) -> str:
    """Reply to a linked student; prev_chat is what was bound before this message."""
    lines = [f"👋 Привіт, {html.quote(user.first_name or user.name or user.nick)}!"]
    if prev_chat == user.tg_chat_id:
        lines.append("✔️ Тебе вже було записано раніше, дякую)")
    else:
        lines.append("✔️ Дякую, записав тебе)")
        if prev_chat:
            lines.append("🔁 Раніше був інший Telegram — тепер писатиму сюди")
    if not user.tg_username:
        lines.append(NO_USERNAME)
    return "\n".join(lines)
