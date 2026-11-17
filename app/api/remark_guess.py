"""The first guess at a remark's tags (T328 §6, step 1): by the words in the line — at once, with no model and no
network. A model or an agent says it better later; what the teacher set by hand none of them touches."""
from defense_vocab import MAX_TAGS

STEMS = {  # lower-case pieces of words; a tag with more of them in the line leads
    "naming": ("назв", "імен", "імʼя", "ім'я", "неймінг", "naming", "переймен", "незрозуміл"),
    "style": ("pep", "формат", "відступ", "імпорт", "комент", "стиль", "конвенц", "мертвий код", "пробіл", "snake", "camel", "докстрінг", "анотац"),
    "dup": ("дубл", "копіпаст", "копі-паст", "повтор", "однаков", "те саме двічі"),
    "size": ("велик", "громіздк", "довгий", "довга", "довгі", "розбити", "розбий", "вкладен", "рядків"),
    "structure": ("архітект", "структур", "модул", "відповідальн", "окремий файл", "окремий клас", "винести", "винеси", "залежн", "впереміш", "розділи"),
    "oop": ("клас", "наслідув", "інкапсул", "поліморф", "обʼєкт", "об'єкт", "property", "dataclass", "ооп", "абстракт", "приватн"),
    "data": ("магічн", "констант", "глобальн", "словник", "enum", "кортеж", "тип дан", "структуру дан", "список замість"),
    "logic": ("умов", "спрост", "зайв", "простіше", "складний вираз", "цикл", "else", "вкладені if"),
    "bug": ("баг", "падає", "не працює", "вилітає", "неправильно", "зависа", "крайн", "ламається"),
    "errors": ("винят", "exception", "except", "валідац", "перевірка ввод", "перевірку ввод", "некоректн", "файл не"),
    "game": ("геймплей", "інтерфейс", "меню", "рівень", "рівні", "гравец", "гравц", "керуванн", "екран", "управлінн"),
    "repo": ("коміт", "git", "гіт", "репозитор", "readme", "гілк", "зайві файли", "тека", "теки"),
    "learn": ("розібратись", "розберись", "вивчи", "почитай", "поясниш", "наступного разу розкаж"),
}
TIP = ("на майбутнє", "порада", "можна було б", "як ідея")
DEBT = {"bug"}  # a guess of this tag makes the remark a debt


def tags(text: str) -> list[str]:
    low = text.lower()
    hits = {tag: sum(s in low for s in stems) for tag, stems in STEMS.items()}
    best = sorted((t for t, n in hits.items() if n), key=lambda t: -hits[t])  # equal counts keep the order of STEMS
    return best[:MAX_TAGS]


def kind(text: str, found: list[str]) -> str:
    if any(t in text.lower() for t in TIP):
        return "tip"
    return "debt" if found and found[0] in DEBT else "better"
