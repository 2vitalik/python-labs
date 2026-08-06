# Taxonomy "one home + tags" — mirrors data/wiki/tasks/_map.md; changing it is a deliberate git act.
# Zone: title + icon + color (base hue, front derives subzone tints); subzone: (title, icon).
ZONES = {
    "entities": {"title": "Сутності", "icon": "👾", "color": "#43a047", "subzones": {
        "spawn": ("Поява", "✨"), "move": ("Рух", "🏃"), "legality": ("Легальність ходу", "🚦"),
        "interact": ("Взаємодія", "🤝"), "combat": ("Бій і снаряди", "💥"),
        "state": ("Параметри і стан", "❤️"), "death": ("Зникнення і смерть", "💀"),
    }},
    "game-logic": {"title": "Логіка", "icon": "🎲", "color": "#8e24aa", "subzones": {
        "win": ("Перемога", "🏆"), "lose": ("Поразка", "🏳️"), "score": ("Рахунок і час", "⏱️"),
        "waves": ("Хвилі та спавн", "🌊"), "economy": ("Економіка", "💰"),
        "opponent": ("Суперник і черга ходів", "🤖"), "constraints": ("Перевірка обмежень", "🚧"),
        "save": ("Збереження", "💾"), "difficulty": ("Чіти і складність", "🎚️"),
    }},
    "levels": {"title": "Рівні", "icon": "🗺️", "color": "#ef6c00", "subzones": {
        "format": ("Формат і завантаження", "📄"), "progression": ("Прогресія", "🪜"),
        "generation": ("Генерація", "🎰"), "editor": ("Редактор", "✏️"),
        "solvability": ("Перевірка проходимості", "🧭"), "bank": ("Банк пазлів", "🗃️"),
    }},
    "interface": {"title": "Інтерфейс", "icon": "🕹️", "color": "#0288d1", "subzones": {
        "render": ("Поле і рендер", "🖼️"), "input": ("Ввід і курсорні взаємодії", "⌨️"),
        "hud": ("HUD-інфо", "📟"), "menus": ("Вікна і меню", "🪟"), "settings": ("Налаштування", "⚙️"),
        "results": ("Результати і статистика", "📈"), "graphics": ("Графіка й анімація", "🎨"),
        "sound": ("Звук", "🔊"),
    }},
    "code": {"title": "Код", "icon": "💻", "color": "#3949ab", "subzones": {
        "architecture": ("Архітектура", "🏛️"), "python": ("Python-фічі", "🐍"), "tests": ("Тести", "🧪"),
        "git": ("Git", "🔀"), "packaging": ("Пакування і запуск", "📦"),
    }},
    "support": {"title": "Супровід", "icon": "📣", "color": "#d81b60", "subzones": {
        "video": ("Відео-демки", "🎬"), "sites": ("Сайти і канали", "🌐"), "docs": ("Документація", "📖"),
    }},
}

KLASSES = {"avatar", "cursor", "figure", "puzzle"}
COINS = {"wood", "tin", "bronze", "silver", "gold", "crown"}
STATUSES = {"draft", "active", "archived"}
