"""The site's part of the bot; the bot itself is core.bot."""
from core.bot import notify

notify.add({"lab": "🧪 лаби: студент здав рядок відповідей або ноутбук"}, after="login")
