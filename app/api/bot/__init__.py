"""The site's part of the bot; the bot itself is core.bot."""
from core.bot import notify

notify.add({"claim": "🎯 заявки на картки", "game": "🧩 гра студента: картка, обʼєкти, правила",
            "idea": "💡 ідеї й пропозиції карток", "ai": "✨ опис гри словами: запити до ШІ й витрати",
            "defense": "🛡 захисти: зауваження надіслано, студент відповів на всі"}, after="login")
