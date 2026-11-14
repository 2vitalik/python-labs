"""Entities, windows and levels of the answer → proposals: checked as the parts' forms check them (parts_clean.kind_fields),
«exists» when the game has the thing with every card, a menu's links checked against the windows."""
from fastapi import HTTPException

from ai.out import Out, quote, text, title
from parts_clean import kind_fields
from zones import kind_of

HAS_CARDS = "уже є в грі — додадуться лише картки"


def checked(out: Out, kind: str, d: dict, x: dict, label: str) -> bool:
    try:
        kind_fields(kind, d, out.ctx.cat)
        return True
    except HTTPException as e:
        out.unknown(quote(x), f"{label}: {e.detail}")
        return False


def named(out: Out, label: str, x: dict, taken: set) -> str:
    """The thing's title, or "" with the reason told; `taken` — the titles of its kind seen in this answer."""
    t = title(x)
    if not t:
        out.unknown(quote(x), f"{label} без назви")
        return ""
    if t.lower() in taken:
        out.unknown(quote(x), f"{label} «{t}» уже є серед пропозицій вище")
        return ""
    taken.add(t.lower())
    return t


def part(out: Out, kind: str, label: str, x: dict, d: dict, needs=()) -> None:
    have = out.ctx.part(kind, d["title"])
    claims, old = out.claims(x, kind, f"{label} «{d['title']}»", (have[0], "") if have else None)
    if claims:
        d["claims"] = claims
    key = out.add(kind, d, quote(x), HAS_CARDS if have and not old else "", needs, "exists" if have and old else "open")
    if not have:
        out.keys[(kind, d["title"].lower())] = key


def entity(out: Out, x: dict, taken: set) -> None:
    if not (t := named(out, "Сутність", x, taken)):
        return
    stats = [{k: str(s.get(k, "")).strip() for k in ("key", "value", "unit")} for s in x.get("stats") or []]
    d = {"title": t, "role": x.get("role", ""), "icon": text(x, "icon"), "description": text(x, "description"),
         "stats": [{k: v for k, v in s.items() if v} for s in stats if s["key"] and s["value"]],
         "states": [s for s in map(str, x.get("states") or []) if s.strip()]}
    d = {k: v for k, v in d.items() if v or k == "role"}
    if not checked(out, "entity", d, x, f"Сутність «{t}»"):
        return out.failed.add(("entity", t.lower()))
    if not out.ctx.part("entity", t):
        out.name("entity", t)
    part(out, "entity", "Сутність", x, d)


def menu(out: Out, x: dict, host: str) -> tuple[list, list]:
    """A window's menu items: a link to a window nobody has, or to a card the catalog lacks, is dropped with a word."""
    items, needs = [], []
    for it in x.get("items") or []:
        row = {k: text(it, k) for k in ("title", "window", "task", "note")}
        if not row["title"]:
            continue
        ref = ("window", row["window"].lower())
        if row["window"] and ref not in out.names:
            out.unknown(quote(x), f"Вікно «{host}»: пункт «{row['title']}» веде на вікно «{row['window']}», якого нема")
            row["window"] = ""
        elif row["window"]:
            row["window"] = out.names[ref][1]
            needs.append(ref)
        if row["task"] and row["task"] not in out.ctx.cards:
            out.unknown(quote(x), f"Вікно «{host}»: пункт «{row['title']}» веде на картку «{row['task']}», якої нема")
            row["task"] = ""
        items.append({k: v for k, v in row.items() if v})
    return items, needs


def windows(out: Out, xs: list[dict]) -> None:
    """First every window that may be — the menus point at each other — then each with its menu."""
    ok, taken = [], set()
    for x in xs:
        if not (t := named(out, "Вікно", x, taken)):
            continue
        task = out.ctx.cards.get(str(x.get("task", "")))
        if not task or kind_of(task) != "window":
            out.failed.add(("window", t.lower()))
            out.unknown(quote(x), f"Вікно «{t}»: «{x.get('task')}» — не тип вікна")
            continue
        if not out.ctx.part("window", t):
            out.name("window", t)
        ok.append((x, {"title": t, "task": task.slug} | ({"description": d} if (d := text(x, "description")) else {})))
    for x, d in ok:
        items, needs = menu(out, x, d["title"])
        part(out, "window", "Вікно", x, d | ({"items": items} if items else {}), needs)


def level(out: Out, x: dict, taken: set) -> None:
    if not (t := named(out, "Рівень", x, taken)):
        return
    props = {k: text(x, k) for k in ("mode", "count", "size")}
    d = {"title": t} | ({"description": s} if (s := text(x, "description")) else {}) | {k: v for k, v in props.items() if v}
    if checked(out, "level", {"props": props, "stats": []}, x, f"Рівень «{t}»"):
        part(out, "level", "Рівень", x, d)
