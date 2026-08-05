# Taxonomy "one home + tags" — mirrors data/wiki/tasks/_map.md; changing it is a deliberate git act.
ZONES = {
    "entities": {"title": "Сутності", "subzones": {
        "spawn": "Поява", "move": "Рух", "legality": "Легальність ходу", "interact": "Взаємодія",
        "combat": "Бій і снаряди", "state": "Параметри і стан", "death": "Зникнення і смерть",
    }},
    "game-logic": {"title": "Логіка гри", "subzones": {
        "win": "Перемога", "lose": "Поразка", "score": "Рахунок і час", "waves": "Хвилі та спавн",
        "economy": "Економіка", "opponent": "Суперник і черга ходів", "constraints": "Перевірка обмежень",
        "save": "Збереження", "difficulty": "Чіти і складність",
    }},
    "levels": {"title": "Рівні", "subzones": {
        "format": "Формат і завантаження", "progression": "Прогресія", "generation": "Генерація",
        "editor": "Редактор", "solvability": "Перевірка проходимості", "bank": "Банк пазлів",
    }},
    "interface": {"title": "Інтерфейс", "subzones": {
        "render": "Поле і рендер", "input": "Ввід і курсорні взаємодії", "hud": "HUD-інфо",
        "menus": "Вікна і меню", "settings": "Налаштування", "results": "Результати і статистика",
        "graphics": "Графіка й анімація", "sound": "Звук",
    }},
    "code": {"title": "Код і платформа", "subzones": {
        "architecture": "Архітектура", "python": "Python-фічі", "tests": "Тести",
        "git": "Git", "packaging": "Пакування і запуск",
    }},
    "support": {"title": "Супровід і промо", "subzones": {
        "video": "Відео-демки", "sites": "Сайти і канали", "docs": "Документація",
    }},
}

KLASSES = {"avatar", "cursor", "figure", "puzzle"}
COINS = {"wood", "tin", "bronze", "silver", "gold"}
STATUSES = {"draft", "active", "archived"}
