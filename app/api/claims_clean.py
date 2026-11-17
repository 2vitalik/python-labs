"""What a claim may carry: slot values by the card's specs, the line to a card outside the core. Where it may live — zones.misplaced()."""
from fastapi import HTTPException

from models.task import Task

WHY_MIN, WHY_MAX = 20, 600
WHY = "Картка за запитом: напиши хоч одне речення, що саме у твоїй грі це робить (від 20 знаків)."


def clean_why(task: Task | None, why: str, free: bool) -> str:
    """A card outside the core asks the student why (T319); `free` — the teacher, a sandbox, a claim the description makes."""
    why = why.strip()
    if task and not task.core and not free and len(why) < WHY_MIN:
        raise HTTPException(422, WHY)
    return why[:WHY_MAX]


def clean_params(task: Task, params: dict, loose: bool = False) -> dict:
    """Slot values by the card's specs; `loose` lets a draft wait for its required params (the catalog's «＋ у гру»)."""
    specs = {s["key"]: s for s in task.slots}
    if unknown := set(params) - set(specs):
        raise HTTPException(422, f"Картка не має параметра «{unknown.pop()}».")
    out = {}
    for key, s in specs.items():
        v = params.get(key)
        if isinstance(v, str):
            v = v.strip()
        if v is None or v == "":
            if s.get("required") and not loose:
                raise HTTPException(422, f"Потрібен параметр «{s['label']}».")
            continue
        kind = s.get("type", "int")
        if kind == "int" and (not isinstance(v, int) or isinstance(v, bool)):
            raise HTTPException(422, f"«{s['label']}» — число.")
        if kind == "bool" and not isinstance(v, bool):
            raise HTTPException(422, f"«{s['label']}» — так/ні.")
        if kind == "choice" and v not in s.get("options", []):
            raise HTTPException(422, f"«{s['label']}» — зі списку варіантів.")
        if kind == "text" and not isinstance(v, str):
            raise HTTPException(422, f"«{s['label']}» — текст.")
        out[key] = v
    return out
