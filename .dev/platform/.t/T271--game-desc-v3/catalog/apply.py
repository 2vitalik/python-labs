"""One-off (T271): apply the reviewed catalog proposals to the catalog in Mongo; `catalog_io export` then writes the YAML.
Inputs lie beside this file: review-*.yaml (a kind and an action for every card), new-cards.yaml (texts of the role / stat /
field-option cards), aliases-by-lang.yaml, extra-cards.yaml (cards the reviews found missing). What the reviews proposed and
this script does not take is listed in OVERRIDES — the reasons are in the task's report.
Run from app/api:  uv run python ../../.dev/platform/.t/T271--game-desc-v3/catalog/apply.py [--dry]"""
import asyncio
import sys
from pathlib import Path

import yaml

sys.path.insert(0, ".")
from core.models.history import record, record_new  # noqa: E402
from db import init_db  # noqa: E402
from models.task import Task  # noqa: E402
from zones import default_kind  # noqa: E402

HERE = Path(__file__).parent
DRY = "--dry" in sys.argv
ACTOR = "claude@agent"
RANK = ["", "wood", "tin", "bronze", "silver", "gold", "crown"]
VALUE = [{"key": "value", "label": "Значення", "type": "text", "required": True}]

# merges and archives the reviews proposed and we do not take: the card stays, with this kind
OVERRIDES = {
    "check-stalemate": {"kind": "rule", "rule": {"when": {"kind": "no_moves"}, "cond": [{"kind": "in_check"}], "then": [{"kind": "draw"}]}},
    "game-pause": {"kind": "game"}, "editor-map-check": {"kind": "level"}, "level-exchange": {"kind": "level"},
    "pattern-automaton": {"kind": "rule", "rule": {"when": {"kind": "tick"}, "then": [{"kind": "move"}]}},
    "floor-types": {"kind": "field"}, "death-animation": {"kind": "game"}, "spawn-animation": {"kind": "game"},
    "game-settings": {"kind": "game"}, "dual-frontends": {"kind": "game"},
    "sound-warnings": {"kind": "rule", "rule": {"when": {"kind": "counter"}, "then": [{"kind": "sound"}]}},
    "hunger-clock": {"kind": "rule", "rule": {"when": {"kind": "counter"}, "then": [{"kind": "damage"}]}},
}
SKIP_REWORD = {"checkmate", "logic-render-split", "enemy-patrol", "map-validation", "sound-effects"}  # their new texts assumed a merge we skip
HOME = {  # cards that move to another subzone
    "interaction-table": "code/architecture", "legal-move-highlight": "interface/hud", "move-limit": "game-logic/lose",
    "rule-variants": "game-logic/difficulty", "seed-share": "levels/generation", "level-select": "interface/menus",
    "telegraphed-intents": "entities/combat", "death-animation": "interface/graphics", "spawn-animation": "interface/graphics",
}
PARENT = {"legal-move-highlight": "highlights", "restart-level": ""}

load = lambda name: yaml.safe_load((HERE / name).read_text()) if (HERE / name).is_file() else {}  # noqa: E731
log: list[str] = []


async def put(task: Task, patch: dict, what: str) -> None:
    patch = {k: v for k, v in patch.items() if getattr(task, k) != v}
    if not patch:
        return
    log.append(f"{task.slug}: {what} — {', '.join(patch)}")
    if not DRY:
        await record(task, patch, actor=ACTOR)


async def create(slug: str, d: dict) -> Task:
    task = Task(slug=slug, **d)
    log.append(f"{slug}: нова картка ({d['zone']}/{d['subzone']})")
    if not DRY:
        await task.insert()
        await record_new(task, actor=ACTOR)
    return task


def explicit(task: Task, kind: str, zone: str, subzone: str) -> str:
    """The kind to store: empty when the card's home already says it."""
    return "" if kind == default_kind(zone, subzone, task.tags) else kind


async def new_cards(tasks: dict) -> None:
    """Texts, prices and synonyms of the role / stat / field-option cards; the ones marked `new` are created."""
    homes = {"role": ("entities", "roles"), "stat": ("entities", "params")}
    for slug, c in load("new-cards.yaml").items():
        base = {"title": c["title"], "icon": c.get("icon", ""), "description": c.get("description", ""), "coin": c.get("coin", ""),
                "aliases": {k: c.get("aliases", {}).get(k, []) for k in ("uk", "ru", "en")}}
        task = tasks.get(slug)
        if task:
            if "unit" in c and task.slots:
                base["slots"] = [task.slots[0] | {"unit": c["unit"]}] if c["unit"] else [{k: v for k, v in task.slots[0].items() if k != "unit"}]
            await put(task, base | {"status": "active"}, "тексти й ціна")
        elif c.get("new") and c.get("kind") in homes:
            zone, sub = homes[c["kind"]]
            order = max((t.order for t in tasks.values() if t.zone == zone and t.subzone == sub), default=0) + 10
            slots = [VALUE[0] | ({"unit": c["unit"]} if c.get("unit") else {})] if c["kind"] == "stat" else []
            tasks[slug] = await create(slug, base | {"zone": zone, "subzone": sub, "opt": c["key"], "parent": c.get("parent", ""),
                                                     "slots": slots, "status": "active", "order": order})


async def extra_cards(tasks: dict) -> None:
    for slug, c in load("extra-cards.yaml").items():
        if slug in tasks:
            continue
        zone, sub = c.pop("home").split("/")
        order = max((t.order for t in tasks.values() if t.zone == zone and t.subzone == sub), default=0) + 10
        tasks[slug] = await create(slug, c | {"zone": zone, "subzone": sub, "order": order})


async def review(tasks: dict) -> dict:
    """Kinds, rule blanks, new wordings and slots, merges; returns {merged slug: the card that absorbed it}."""
    merged = {}
    for name in ("review-entities.yaml", "review-logic-levels.yaml", "review-interface-code.yaml"):
        for slug, r in load(name).items():
            task = tasks.get(slug)
            if not task:
                log.append(f"{slug}: нема в каталозі — пропущено")
                continue
            r = r | OVERRIDES.get(slug, {})
            action = "keep" if slug in OVERRIDES else r["action"]
            if action == "merge":
                target = tasks.get(r["into"])
                if not target:
                    log.append(f"{slug}: злиття в «{r['into']}», якої нема — пропущено")
                    continue
                merged[slug] = r["into"]
                await put(task, {"status": "archived"}, f"злито в {r['into']}")
                if RANK.index(r.get("coin", "")) > RANK.index(target.coin):
                    await put(target, {"coin": r["coin"]}, f"ціна від {slug}")
                continue
            if action == "archive":
                await put(task, {"status": "archived"}, "в архів")
                continue
            zone, sub = HOME.get(slug, f"{task.zone}/{task.subzone}").split("/")
            patch = {"zone": zone, "subzone": sub, "kind": explicit(task, r["kind"], zone, sub),
                     "rule": r.get("rule") or {} if r["kind"] == "rule" else {}}
            if slug in PARENT:
                patch["parent"] = PARENT[slug]
            if slug not in SKIP_REWORD and slug not in OVERRIDES:
                patch |= {k: r[k] for k in ("title", "description", "coin", "games") if k in r}
                slots = [s for s in task.slots if s["key"] not in r.get("drop_slots", [])]
                keys = {s["key"] for s in r.get("slots") or []}
                if "slots" in r or "drop_slots" in r:
                    patch["slots"] = [s for s in slots if s["key"] not in keys] + (r.get("slots") or []) if r.get("slots") != [] else []
            await put(task, patch, action)
    return merged


async def aliases(tasks: dict) -> None:
    own = set(load("new-cards.yaml"))  # their synonyms came with their texts
    for slug, a in load("aliases-by-lang.yaml").items():
        if slug in tasks and slug not in own:
            await put(tasks[slug], {"aliases": {k: a.get(k) or [] for k in ("uk", "ru", "en")}}, "синоніми за мовами")


async def main():
    await init_db()
    tasks = {t.slug: t for t in await Task.find_all().to_list()}
    await new_cards(tasks)
    await extra_cards(tasks)
    merged = await review(tasks)
    await aliases(tasks)
    (HERE / "merged.yaml").write_text(yaml.safe_dump(merged, allow_unicode=True, sort_keys=True))
    (HERE / "apply.log").write_text("\n".join(log) + "\n")
    print(f"{'DRY · ' if DRY else ''}{len(log)} змін · злито {len(merged)} · журнал — apply.log, злиття — merged.yaml")


if __name__ == "__main__":
    asyncio.run(main())
