# Taxonomy "one home + tags" — mirrors data/wiki/tasks/_map.md; changing it is a deliberate git act.
# Zone: title + icon + color (base hue, front derives subzone tints); subzone: (title, icon, the default kind of its cards).
KINDS = {  # what a card is and where its claim lives (T270 §6)
    "role": "тип сутності", "stat": "параметр сутності", "mechanic": "механіка сутності", "rule": "картка на правило",
    "fieldopt": "властивість поля", "field": "картка про поле", "level": "картка про рівні", "window": "тип вікна",
    "element": "елемент вікна", "game": "гра загалом",
}
AUTO_KINDS = {"window", "role", "stat", "fieldopt"}  # claimed by the form itself: auto_claims.py

M, R, G, F, L, E = "mechanic", "rule", "game", "fieldopt", "level", "element"
ZONES = {
    "field": {"title": "Поле", "icon": "🗺️", "color": "#00897b", "subzones": {
        "grid": ("Сітка", "🔲", F), "view": ("Вид", "👁️", F), "time": ("Час", "⏳", F),
        "control": ("Керування", "🎮", F), "physics": ("Фізика поля", "🧲", F),
    }},
    "entities": {"title": "Сутності", "icon": "👾", "color": "#43a047", "subzones": {
        "roles": ("Типи сутностей", "🎭", "role"), "params": ("Параметри", "🔢", "stat"),
        "spawn": ("Поява", "✨", M), "move": ("Рух", "🏃", M), "legality": ("Легальність ходу", "🚦", M),
        "interact": ("Взаємодія", "🤝", M), "combat": ("Бій і снаряди", "💥", M),
        "state": ("Стани й ефекти", "❤️", M), "death": ("Зникнення і смерть", "💀", M),
    }},
    "game-logic": {"title": "Логіка", "icon": "🎲", "color": "#8e24aa", "subzones": {
        "win": ("Перемога", "🏆", R), "lose": ("Поразка", "🏳️", R), "score": ("Рахунок і час", "⏱️", G),
        "waves": ("Хвилі та спавн", "🌊", G), "economy": ("Економіка", "💰", G),
        "opponent": ("Суперник і черга ходів", "🤖", G), "constraints": ("Перевірка обмежень", "🚧", G),
        "save": ("Збереження", "💾", G), "history": ("Історія ходів", "↩️", G), "difficulty": ("Чіти і складність", "🎚️", G),
        "program": ("Програма гравця", "🤖", G),
    }},
    "levels": {"title": "Рівні", "icon": "🪜", "color": "#ef6c00", "subzones": {
        "format": ("Формат і завантаження", "📄", L), "progression": ("Прогресія", "🔓", L),
        "generation": ("Генерація", "🎰", L), "editor": ("Редактор", "✏️", L),
        "solvability": ("Перевірка проходимості", "🧭", L), "bank": ("Банк пазлів", "🗃️", L),
    }},
    "interface": {"title": "Інтерфейс", "icon": "🕹️", "color": "#0288d1", "subzones": {
        "render": ("Поле і рендер", "🖼️", "field"), "input": ("Ввід і курсорні взаємодії", "⌨️", "field"),
        "hud": ("HUD-інфо", "📟", E), "menus": ("Вікна і меню", "🪟", E), "settings": ("Налаштування", "⚙️", E),
        "results": ("Результати і статистика", "📈", G), "graphics": ("Графіка й анімація", "🎨", G),
        "sound": ("Звук", "🔊", G),
    }},
    "code": {"title": "Код", "icon": "💻", "color": "#3949ab", "subzones": {
        "labs": ("Завдання лаб", "📚", G), "architecture": ("Архітектура", "🏛️", G), "python": ("Python-фічі", "🐍", G), "tests": ("Тести", "🧪", G),
        "git": ("Git", "🔀", G), "packaging": ("Пакування і запуск", "📦", G),
    }},
    "support": {"title": "Супровід", "icon": "📣", "color": "#d81b60", "subzones": {
        "video": ("Відео-демки", "🎬", G), "sites": ("Сайти і канали", "🌐", G), "docs": ("Документація", "📖", G),
    }},
}

KLASSES = {"avatar", "cursor", "figure", "puzzle"}
COINS = {"wood", "tin", "bronze", "silver", "gold", "crown"}
STATUSES = {"draft", "active", "archived"}


def default_kind(zone: str, subzone: str, tags: list[str]) -> str:
    """A window type by its tag, else the subzone's kind."""
    if "window" in tags:
        return "window"
    sub = ZONES.get(zone, {}).get("subzones", {}).get(subzone)
    return sub[2] if sub else "game"


def kind_of(task) -> str:
    return task.kind or default_kind(task.zone, task.subzone, task.tags)


AUTO = "Ця картка обирається в формі (тип сутності, параметр, властивість поля, тип вікна) — окремо не заявляється."
HOMES = {  # kind → where its claim lives ("" — the game itself) and the reason when it is put elsewhere
    "element": ("window", "Елемент вікна додається до вікна."),
    "mechanic": ("entity", "Механіка додається до сутності."),
    "field": ("field", "Картка про поле додається до поля."),
    "level": ("level", "Картка про рівні — у секції «Рівні» або на рівні."),
    "rule": ("rule", "Ця картка — про поведінку: додається до правила."),
    "game": ("", "Картка гри загалом — без привʼязки."),
}


def misplaced(kind: str, where: str) -> str:
    """Why a card of this kind cannot be claimed on `where` (a part's kind, "rule", or "" — unanchored); "" when it can.
    Unanchored is open to every kind but the automatic ones: that is the drafts pool."""
    if kind in AUTO_KINDS:
        return AUTO
    home, why = HOMES.get(kind, ("", ""))
    return why if where and where != home else ""
