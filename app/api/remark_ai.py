"""A model sorts a defense's remarks (T328 §6, step 2): one request for the lines just added — tags, kind, a cleaner text,
«says the same as №…». Tags and kind land where the teacher has not set them; the text is only ever a proposal.
No key or AI_REMARKS=off — nothing is asked: the first guess by words (remark_guess.py) stays."""
import logging

import defense_vocab as V
from ai.client import AskError, ask
from core.config import settings
from core.models.history import record
from models.defense import Remark

logger = logging.getLogger(__name__)
ACTOR = "model@agent"
ITEM = {"type": "object", "additionalProperties": False, "required": ["n", "tags", "kind", "text", "like"], "properties": {
    "n": {"type": "integer"}, "tags": {"type": "array", "items": {"type": "string", "enum": list(V.TAGS)}},
    "kind": {"type": "string", "enum": list(V.REMARK_KINDS)}, "text": {"type": "string"}, "like": {"type": "integer"}}}
SCHEMA = {"type": "object", "additionalProperties": False, "required": ["remarks"], "properties": {"remarks": {"type": "array", "items": ITEM}}}
RULES = """Ти допомагаєш викладачеві програмування: він диктує зауваження до коду студента (Python, гра на клітинному полі),
а ти розкладаєш кожне НОВЕ зауваження. Для кожного поверни:
- n — його номер;
- tags — один-два теги зі списку, перший — головний; не лягає нікуди — ["other"];
- kind — вид зі списку; сумніваєшся — "better";
- text — той самий зміст чистим коротким реченням українською, звертання на «ти», без слів-паразитів диктовки;
  нічого не додавай від себе; якщо рядок уже чистий — поверни його без змін;
- like — номер іншого зауваження цього захисту, яке каже те саме, або 0.
Старі зауваження дано лише для порівняння: їх не повертай."""


def on() -> bool:
    return settings.ai_remarks == "on" and bool(settings.anthropic_api_key)


def system() -> str:
    tags = "\n".join(f"- {k}: {title} — {hint}" for k, (title, hint) in V.TAGS.items())
    kinds = "\n".join(f"- {k}: {title} — {hint}" for k, (_, title, hint) in V.REMARK_KINDS.items())
    return f"{RULES}\n\nТеги:\n{tags}\n\nВиди:\n{kinds}"


async def sort(defense_id, fresh: list) -> None:
    """After the answer to the teacher: proposals for the remarks with the ids `fresh`."""
    if not on():
        return
    remarks = await Remark.find(Remark.defense == defense_id).sort("order", "created_at").to_list()
    by = {r.order: r for r in remarks}
    asked = "\n".join(f"№{r.order}{' (нове)' if r.id in fresh else ''}: {r.raw or r.text}" for r in remarks)
    try:
        answer, usage = await ask(settings.ai_remarks_model, system(), asked, SCHEMA)
    except AskError as e:
        logger.warning("remarks not sorted: %s", e.message)
        return
    logger.info("remarks sorted: %s", usage)
    for item in answer.get("remarks", []):
        r = by.get(item["n"])
        r = r and r.id in fresh and await Remark.get(r.id)  # as it is now: the teacher may have clicked meanwhile
        if not r:
            continue
        patch = {k: v for k, v in (("tags", list(dict.fromkeys(item["tags"]))[:V.MAX_TAGS]), ("kind", item["kind"])) if k not in r.own}
        text, like = item["text"].strip(), by.get(item["like"])
        hint = ({"text": text} if text and text != r.text and "text" not in r.own else {}) | ({"like": str(like.id)} if like and like.id != r.id else {})
        await record(r, patch | ({"hint": r.hint | hint | {"by": ACTOR}} if hint else {}), actor=ACTOR)
