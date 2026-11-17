"""How a change of a student's game reads in its history (T278 §12): what the object is, what was done, its fields in
Ukrainian with values in words (game_log_names.py)."""
import videos
from game_log_names import PARTS, Names

WHAT = {"student_games": "гра", "rules": "правило", "claims": "заявка", "game_drafts": "✨ опис словами", "videos": "відео"}
LABELS = {
    "title": "назва", "description": "опис", "base_game": "основа", "base_custom": "своя основа", "phases": "порядок тіку",
    "task": "тип вікна", "role": "роль", "icon": "іконка", "screenshots": "скриншоти", "window": "вікно", "items": "переходи",
    "props": "властивості", "stats": "параметри", "states": "стани", "when": "коли", "cond": "якщо", "then": "то",
    "note": "нотатка", "part": "де", "rule": "правило", "params": "параметри", "link": "посилання", "shots": "докази", "status": "стан",
    "verdict": "коментар викладача", "moments": "як це грається", "text": "текст",
    "versions": "посилання", "need": "чи потрібне", "why": "чому", "extras": "можливості",
}
OWN = {("claims", "task"): "картка", ("claims", "why"): "пояснення"}  # a claim's fields named apart from the same keys elsewhere
HIDDEN = ("game", "owner", "order", "kind", "auto", "poured", "created_at", "slot")  # the plumbing: nobody typed these


def what(coll: str, snap: dict) -> str:
    return PARTS.get(snap.get("kind"), "обʼєкт") if coll == "game_parts" else WHAT.get(coll, coll)


def proposals(n: int) -> str:
    return f"{n} " + ("пропозиція" if n % 10 == 1 and n % 100 != 11 else "пропозиції" if 2 <= n % 10 <= 4 and not 12 <= n % 100 <= 14 else "пропозицій")


def title(names: Names, coll: str, snap: dict) -> str:
    if coll == "game_drafts":  # the AI's proposals (T291 §14): the text is the row's field, their states live in the draft
        items = snap.get("items") or []
        unknown = sum(1 for it in items if it.get("group") == "unknown")
        return proposals(len(items) - unknown) + (f" · не розпізнано {unknown}" if unknown else "")
    if coll == "rules":
        return names.sentence(snap)
    if coll == "videos":
        return videos.title(snap.get("slot") or "", names.card)
    if snap.get("kind") == "menu" and snap.get("window"):  # «Меню «Пауза»» says less than the window whose transitions these are
        return names.part(snap["window"])
    return names.card(snap.get("task", "")) if coll == "claims" else snap.get("title") or ""


def action(coll: str, changes: dict) -> str:
    """added · deleted · changed; a claim's new status says it in the teacher's words: accepted · returned · claimed."""
    if all(c.get("old") is None for c in changes.values()):
        return "added"
    if all(c.get("new") is None for c in changes.values()):
        return "deleted"
    return changes["status"]["new"] if coll in ("claims", "videos") and "status" in changes else "changed"


def fields(names: Names, coll: str, changes: dict, snap: dict) -> list[dict]:
    out = []
    for key, c in changes.items():
        if key in HIDDEN:
            continue
        old, new = c.get("old"), c.get("new")
        if key == "props" and isinstance(old, dict) and isinstance(new, dict):  # only the properties that changed
            diff = {k for k in old.keys() | new.keys() if old.get(k) != new.get(k)}
            old, new = ({k: x for k, x in d.items() if k in diff} for d in (old, new))
        old, new = names.text(key, old, snap), names.text(key, new, snap)
        if old != new:
            label = OWN.get((coll, key)) or LABELS.get(key, key)
            out.append({"key": key, "label": label, "old": old, "new": new})
    return out
