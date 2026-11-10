"""Reference descriptions of the catalog's base games (Д4, T257, T270): data/catalog/templates/<slug>.yaml, written in the
vocab's words with entities named by title. `apply()` pours one into the student's game — the menu to cross out and add to."""
from pathlib import Path

import yaml
from fastapi import HTTPException

import auto_claims
import options
from claims_clean import clean_params
from core.models.history import record_new
from core.models.user import User
from models.game import Claim, Game, Part
from models.task import Task
from parts_clean import kind_fields
from template_rules import pour_rules
from zones import kind_of, misplaced

DIR = Path(__file__).resolve().parents[2] / "data" / "catalog" / "templates"
LEVEL_KEYS = ("title", "description", "stats", "claims")  # the rest of a level's node is its props


def load(slug: str) -> dict | None:
    path = DIR / f"{slug}.yaml"
    return yaml.safe_load(path.read_text()) if slug and path.is_file() else None


def summary(slug: str) -> dict | None:
    """Counts for the «Почати з еталона» button."""
    t = load(slug)
    if not t:
        return None
    nodes = [t] + [x for k in ("entities", "windows", "levels", "rules") for x in t.get(k) or []]
    return {"slug": slug, "field": bool(t.get("field")), "entities": len(t.get("entities") or []),
            "rules": len(t.get("rules") or []), "windows": len(t.get("windows") or []), "levels": len(t.get("levels") or []),
            "claims": sum(len(x.get("claims") or []) for x in nodes)}


def all_summaries() -> dict:
    return {p.stem: summary(p.stem) for p in sorted(DIR.glob("*.yaml"))} if DIR.is_dir() else {}


async def apply(game: Game, user: User, slug: str) -> dict:
    t = load(slug)
    if not t:
        raise HTTPException(404, "Еталона для цієї основи ще нема.")
    return await pour(game, user, t)


def card(x) -> tuple[str, dict]:  # 'slug' or {slug: …, params: {…}}
    return (x, {}) if isinstance(x, str) else (x.get("slug", ""), x.get("params") or {})


async def pour(game: Game, user: User, t: dict) -> dict:
    """Add what the student's game does not have yet: the field, entities, windows with menus, levels, rules, claims.
    Matching is by title, so the import is safe to repeat; unknown cards, bad words and cards out of their place
    (the card's kind says where it lives) are reported in `skipped`, not fatal."""
    cat = await options.catalog(options.is_admin(user))
    parts = await Part.find(Part.game == game.id).to_list()
    by_title = {(p.kind, p.title.lower()): p for p in parts}
    claimed = {(c.task, c.part, c.rule) for c in await Claim.find(Claim.game == game.id).to_list()}
    added = {"field": 0, "entities": 0, "windows": 0, "menus": 0, "levels": 0, "rules": 0, "claims": 0}
    skipped: list[str] = []

    async def new_part(kind: str, title: str, d: dict, **more) -> Part | None:
        try:
            fields = kind_fields(kind, d, cat)
        except HTTPException as e:
            skipped.append(f"«{title}»: {e.detail}")
            return None
        part = Part(game=game.id, kind=kind, title=title, description=d.get("description", ""), **fields | more)
        await part.insert()
        await record_new(part, actor=user.email)
        by_title[(kind, title.lower())] = part
        added[{"field": "field", "entity": "entities", "window": "windows", "menu": "menus", "level": "levels"}[kind]] += 1
        return part

    async def claim(x, part: Part | None = None, rule: str = "", where: str = ""):
        slug, params = card(x)
        task = await Task.find_one(Task.slug == slug)
        if not task or task.status == "archived":
            skipped.append(f"картка «{slug}»")
            return
        pid = str(part.id) if part else ""
        if why := misplaced(kind_of(task), part.kind if part else "rule" if rule else ""):
            skipped.append(f"«{slug}» {where}: {why}")
            return
        if (slug, pid, rule) in claimed:
            return
        try:
            values = clean_params(task, params, loose=True)
        except HTTPException as e:
            skipped.append(f"«{slug}»: {e.detail}")
            return
        c = Claim(game=game.id, task=slug, part=pid, rule=rule, params=values)
        await c.insert()
        await record_new(c, actor=user.email)
        claimed.add((slug, pid, rule))
        added["claims"] += 1

    field = next((p for p in parts if p.kind == "field"), None)
    if t.get("field") and not field:
        field = await new_part("field", "Поле", {"props": t["field"]})
    for e in t.get("entities") or []:
        part = by_title.get(("entity", e["title"].lower())) or await new_part("entity", e["title"], e)
        for x in (e.get("claims") or []) if part else []:
            await claim(x, part, where=f"на сутності «{e['title']}»")
    for w in t.get("windows") or []:
        part = by_title.get(("window", w["title"].lower()))
        if not part:
            task = await Task.find_one(Task.slug == w.get("task", ""))
            if not task or kind_of(task) != "window":
                skipped.append(f"тип вікна «{w.get('task')}»")
                continue
            part = await new_part("window", w["title"], w, task=task.slug)
        for x in w.get("claims") or []:
            await claim(x, part, where=f"на вікні «{w['title']}»")
    for w in t.get("windows") or []:  # menus after every window exists: items point at windows by title
        items = w.get("items") or []
        host = by_title.get(("window", w["title"].lower()))
        title = f"Меню «{w['title']}»"
        if not items or not host or ("menu", title.lower()) in by_title:
            continue
        rows = []
        for it in items:
            target = by_title.get(("window", str(it.get("window", "")).lower()))
            rows.append({"title": it["title"], "window": str(target.id) if target else "", "task": it.get("task", ""), "note": it.get("note", "")})
        await new_part("menu", title, {}, window=str(host.id), items=rows)
    for lv in t.get("levels") or []:
        node = {"description": lv.get("description", ""), "stats": lv.get("stats") or [],
                "props": {k: v for k, v in lv.items() if k not in LEVEL_KEYS}}
        part = by_title.get(("level", lv["title"].lower())) or await new_part("level", lv["title"], node)
        for x in (lv.get("claims") or []) if part else []:
            await claim(x, part, where=f"на рівні «{lv['title']}»")
    for rule, claims in await pour_rules(game, user, t.get("rules") or [], by_title, added, skipped):
        for x in claims:
            await claim(x, rule=str(rule.id), where="на правилі")
    for x in t.get("claims") or []:  # the game's own: a field card goes onto the field, the rest wait unanchored
        slug = card(x)[0]
        task = await Task.find_one(Task.slug == slug)
        on_field = field and task and kind_of(task) == "field"
        await claim(x, field if on_field else None, where="на рівні гри")
    await auto_claims.sync(game, user.email)
    return {"added": added, "skipped": skipped}
