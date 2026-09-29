"""The site's part of the bot; the bot itself is core.bot."""
from core.bot import notify

notify.add({"claim": "🎯 заявки на картки", "game": "🧩 гра студента: картка, обʼєкти, правила"}, after="login")
