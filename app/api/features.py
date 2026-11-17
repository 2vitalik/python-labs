"""The game page's features beyond the core (T319): a student turns them on in «Моя гра» (Game.extras); the teacher closes
the unready ones for the whole site (the pref `game.closed`) — a closed one is offered to nobody."""
from core.models.pref import get_pref

EXTRAS = {  # id → how the game's history names it, in the page's order
    "stats": "параметри й стани", "mechanics": "механіки", "phases": "порядок ходу", "tables": "таблиці правил",
    "elements": "елементи вікон", "field": "поле", "levels": "рівні", "map": "мапа рівня клітинками", "moments": "розкадровка",
    "logic": "логіка гри", "interface": "інтерфейс", "support": "супровід: картки", "cards": "вигляд «Картки»",
    "looks": "налаштування вигляду", "etalon": "еталон основи",
}
CLOSED = ("map", "moments")  # not ready yet: while the teacher has not said otherwise
PREF = "game.closed"


async def closed() -> list[str]:
    shut = await get_pref(PREF, CLOSED)
    return [x for x in EXTRAS if x in shut]
