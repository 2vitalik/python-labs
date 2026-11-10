"""What a claim may carry: slot values by the card's specs. Where it may live — zones.misplaced()."""
from fastapi import HTTPException

from models.task import Task


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
