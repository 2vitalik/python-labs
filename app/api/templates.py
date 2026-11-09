"""Reference descriptions of the catalog's base games (Д4, T257): data/catalog/templates/<slug>.yaml, written in the
vocab's words with entities named by title. `apply()` pours one into the student's game — the menu to cross out and add to."""
from pathlib import Path

import yaml
from fastapi import HTTPException

from core.models.history import record_new
from core.models.user import User
from models.game import Claim, Game, Part
from models.rule import Rule
from models.task import Task
from models.vocab import CONDITIONS, EFFECTS, TRIGGERS
from routes.my_claims import clean_params
from routes.my_parts import clean_props, clean_stats, clean_states, check_role
from routes.my_rules import RuleIn, clean

DIR = Path(__file__).resolve().parents[2] / "data" / "catalog" / "templates"


def load(slug: str) -> dict | None:
    path = DIR / f"{slug}.yaml"
    return yaml.safe_load(path.read_text()) if slug and path.is_file() else None


def summary(slug: str) -> dict | None:
    """Counts for the «Почати з еталона» button."""
    t = load(slug)
    if not t:
        return None
    return {"slug": slug, "field": bool(t.get("field")), "entities": len(t.get("entities") or []),
            "rules": len(t.get("rules") or []), "windows": len(t.get("windows") or []),
            "claims": len(t.get("claims") or []) + sum(len(e.get("claims") or []) for e in t.get("entities") or [])}


def all_summaries() -> dict:
    return {p.stem: summary(p.stem) for p in sorted(DIR.glob("*.yaml"))} if DIR.is_dir() else {}


async def apply(game: Game, user: User, slug: str) -> dict:
    t = load(slug)
    if not t:
        raise HTTPException(404, "Еталона для цієї основи ще нема.")
    return await pour(game, user, t)


async def pour(game: Game, user: User, t: dict) -> dict:
    """Add what the student's game does not have yet: the field, entities, windows with menus, rules, claims.
    Matching is by title, so the import is safe to repeat; unknown cards and bad words are reported, not fatal."""
    parts = await Part.find(Part.game == game.id).to_list()
    claims = await Claim.find(Claim.game == game.id).to_list()
    by_title = {(p.kind, p.title.lower()): p for p in parts}
    claimed = {(c.task, c.part) for c in claims}
    added = {"field": 0, "entities": 0, "windows": 0, "menus": 0, "rules": 0, "claims": 0}
    skipped: list[str] = []

    async def new_part(**d) -> Part:
        part = Part(game=game.id, **d)
        await part.insert()
        await record_new(part, actor=user.email)
        by_title[(part.kind, part.title.lower())] = part
        return part

    async def claim(task_slug: str, part_id: str, params: dict | None = None):
        task = await Task.find_one(Task.slug == task_slug)
        if not task or task.status == "archived":
            skipped.append(f"картка «{task_slug}»")
            return
        if (task_slug, part_id) in claimed:
            return
        try:
            values = clean_params(task, params or {}, loose=True)
        except HTTPException as e:
            skipped.append(f"«{task_slug}»: {e.detail}")
            return
        c = Claim(game=game.id, task=task_slug, part=part_id, params=values)
        await c.insert()
        await record_new(c, actor=user.email)
        claimed.add((task_slug, part_id))
        added["claims"] += 1

    def card(x) -> tuple[str, dict]:  # 'slug' or {slug: …, params: {…}}
        return (x, {}) if isinstance(x, str) else (x.get("slug", ""), x.get("params") or {})

    if t.get("field") and ("field", "поле") not in by_title and not any(p.kind == "field" for p in parts):
        await new_part(kind="field", title="Поле", props=clean_props(t["field"]))
        added["field"] = 1
    for e in t.get("entities") or []:
        key = ("entity", e["title"].lower())
        if key not in by_title:
            check_role(e.get("role", ""))
            part = await new_part(kind="entity", title=e["title"], role=e["role"], description=e.get("description", ""),
                                  stats=clean_stats(e.get("stats") or []), states=clean_states(e.get("states") or []))
            added["entities"] += 1
        else:
            part = by_title[key]
        for x in e.get("claims") or []:
            await claim(*card(x)[:1], str(part.id), card(x)[1])
    for wdef in t.get("windows") or []:
        key = ("window", wdef["title"].lower())
        if key not in by_title:
            task = await Task.find_one(Task.slug == wdef.get("task", ""))
            if not task or "window" not in task.tags:
                skipped.append(f"тип вікна «{wdef.get('task')}»")
                continue
            part = await new_part(kind="window", title=wdef["title"], task=task.slug, description=wdef.get("description", ""))
            added["windows"] += 1
            await claim(task.slug, str(part.id))
        else:
            part = by_title[key]
        for x in wdef.get("claims") or []:
            await claim(*card(x)[:1], str(part.id), card(x)[1])
    for wdef in t.get("windows") or []:  # menus after every window exists: items point at windows by title
        items = wdef.get("items") or []
        host = by_title.get(("window", wdef["title"].lower()))
        if not items or not host or ("menu", f"меню «{wdef['title']}»".lower()) in by_title:
            continue
        rows = []
        for it in items:
            target = by_title.get(("window", str(it.get("window", "")).lower()))
            rows.append({"title": it["title"], "window": str(target.id) if target else "", "task": it.get("task", ""), "note": it.get("note", "")})
        await new_part(kind="menu", title=f"Меню «{wdef['title']}»", window=str(host.id), items=rows)
        added["menus"] += 1
    names = {k[1]: str(p.id) for k, p in by_title.items() if k[0] == "entity"}
    names |= {k[1]: str(p.id) for k, p in by_title.items() if k[0] == "window"}
    existing = {sentence_key(r.when, r.cond, r.then) for r in await Rule.find(Rule.game == game.id).to_list()}
    for r in t.get("rules") or []:
        def resolve(dic, d):  # titles → ids, only where the word expects an entity or a window
            spec = dic.get(d.get("kind")) or {"args": []}
            refs = {a["name"] for a in spec["args"] if a["type"] in ("entity", "window")}
            return {k: (names.get(str(v).lower(), v) if k in refs and isinstance(v, str) else v) for k, v in d.items()}
        data = RuleIn(when=resolve(TRIGGERS, r.get("when") or {}), cond=[resolve(CONDITIONS, c) for c in r.get("cond") or []],
                      then=[resolve(EFFECTS, e) for e in r.get("then") or []], note=r.get("note", ""))
        try:
            d = await clean(data, game)
        except HTTPException as e:
            skipped.append(f"правило: {e.detail}")
            continue
        if sentence_key(d["when"], d["cond"], d["then"]) in existing:
            continue
        rule = Rule(game=game.id, **d)
        await rule.insert()
        await record_new(rule, actor=user.email)
        added["rules"] += 1
    for x in t.get("claims") or []:
        await claim(*card(x)[:1], "", card(x)[1])
    return {"added": added, "skipped": skipped}


def sentence_key(when, cond, then) -> str:
    return repr((when, cond, then))
