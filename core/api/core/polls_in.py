"""What the poll and template forms send (T174): cleaned, and checked against Telegram's limits before Telegram says them in English."""
from fastapi import HTTPException
from pydantic import BaseModel

from core.models.poll import Option

QUESTION, OPTION, FEWEST, MOST, TITLE = 300, 100, 2, 12, 60  # Telegram's limits, and our column header's


class PollIn(BaseModel):
    title: str = ""
    question: str = ""
    options: list[Option] = []
    multiple: bool = False
    tags: list[str] = []
    template: str = ""  # a new poll: the template it came from


def words(s: str) -> str:
    return " ".join(s.split())


def clean(data: PollIn) -> dict:
    question = data.question.strip()
    options = [o for o in (Option(emoji=o.emoji.strip(), text=words(o.text)) for o in data.options) if o.label]
    title = words(data.title) or words(question)[:TITLE]
    if not question:
        raise HTTPException(422, "Напиши питання")
    if len(question) > QUESTION:
        raise HTTPException(422, f"Питання довше за {QUESTION} символів — Telegram не прийме")
    if not FEWEST <= len(options) <= MOST:
        raise HTTPException(422, f"Варіантів має бути від {FEWEST} до {MOST}")
    if long := next((o.label for o in options if len(o.label) > OPTION), None):
        raise HTTPException(422, f"Варіант довший за {OPTION} символів: «{long[:30]}…»")
    if len({o.label for o in options}) < len(options):
        raise HTTPException(422, "Два однакові варіанти — Telegram їх не розрізнить")
    if len(title) > TITLE:
        raise HTTPException(422, f"Заголовок — до {TITLE} символів: він стає назвою колонки в таблиці")
    tags = list(dict.fromkeys(t for t in (words(t).lstrip("#") for t in data.tags) if t))
    return {"title": title, "question": question, "options": options, "multiple": data.multiple, "tags": tags}
