"""One-off (T275): apply the second catalog review to Mongo; `catalog_io export` then writes the YAML.
Inputs lie beside this file: drafts.yaml (a verdict per draft card), logic.yaml (kinds, merges, rewordings, new cards),
code.yaml (the «Код» zone: lab requirements and small Python features), polish.yaml (texts and extra synonyms).
What the reviews proposed and this script does not take is in the SKIP_* sets — the reasons are in the task's report.
Run from app/api:  uv run python ../../.dev/platform/.t/T275--game-desc-v4/catalog/apply.py [--dry]"""
import asyncio
import sys
from pathlib import Path

import yaml
from fastapi import HTTPException

sys.path.insert(0, ".")
from core.models.history import record, record_new  # noqa: E402
from db import init_db  # noqa: E402
from models.task import LANGS, Task  # noqa: E402
from tasks_clean import clean_rule, clean_slots  # noqa: E402
from zones import ZONES, default_kind  # noqa: E402

HERE = Path(__file__).parent
DRY = "--dry" in sys.argv
ACTOR = "claude@agent"
LABS = {1: "Лаба 1: основи Python", 2: "Лаба 2: структури даних і файли", 3: "Лаба 3: ООП", 4: "Лаба 4: просунуті можливості",
        5: "Лаба 5*: web-розробка"}
LAB_OF = {  # cards that live elsewhere and belong to a lab too: the tag `labN` finds them from the lab's family
    "level-from-txt": 2, "score-records": 2, "logic-render-split": 3, "custom-exceptions": 4, "unit-tests": 4,
    "generators-iterators": 4, "fixture-level-tests": 4, "typing-mypy": 4, "profile-stats": 5,
}
SKIP_MERGE = {"random-placement"}  # the bomberman reference claims it on a level: stays its own card, activated
SKIP_COIN = {"logic-render-split", "unit-tests", "editor-window"}  # settled prices are the teacher's to change (the Q-ticket asks)
SKIP_REVIEW = {"check-stalemate", "game-settings"}  # a new name narrows what a settled card pays for (T273 Q5) — the Q-ticket asks

load = lambda name: yaml.safe_load((HERE / name).read_text()) if (HERE / name).is_file() else {}  # noqa: E731
log: list[str] = []


async def put(task: Task, patch: dict, what: str) -> None:
    patch = {k: v for k, v in patch.items() if getattr(task, k) != v}
    if not patch:
        return
    log.append(f"{task.slug}: {what} — {', '.join(patch)}")
    if not DRY:
        await record(task, patch, actor=ACTOR)


async def create(tasks: dict, slug: str, d: dict) -> Task:
    order = max((t.order for t in tasks.values() if t.zone == d["zone"] and t.subzone == d["subzone"]), default=0) + 10
    task = Task(slug=slug, order=order, **d)
    log.append(f"{slug}: нова картка ({d['zone']}/{d['subzone']}{' · у сімʼї ' + d['parent'] if d.get('parent') else ''})")
    if not DRY:
        await task.insert()
        await record_new(task, actor=ACTOR)
    tasks[slug] = task
    return task


def texts(r: dict, task: Task | None = None, coin: bool = True) -> dict:
    """The fields a proposal may carry, checked the way the card form checks them; aliases replace only the languages given."""
    d = {k: r[k] for k in ("title", "description", "games", "tags", "max_count") if k in r}
    if coin and r.get("coin"):
        d["coin"] = r["coin"]
    if "slots" in r:
        d["slots"] = clean_slots(r["slots"] or [])
    if r.get("rule"):
        d["rule"] = clean_rule(r["rule"])
    if r.get("aliases"):
        old = task.aliases if task else {}
        d["aliases"] = {k: list(r["aliases"].get(k) or old.get(k) or []) for k in LANGS}
    return d


def kind_for(kind: str, zone: str, subzone: str, tags: list) -> str:
    """The kind to store: empty when the card's home already says it."""
    return "" if kind == default_kind(zone, subzone, tags) else kind


async def drafts(tasks: dict) -> None:
    for slug, r in load("drafts.yaml").items():
        task = tasks.get(slug)
        if not task:
            log.append(f"{slug}: нема в каталозі — пропущено")
            continue
        action = "activate" if slug in SKIP_MERGE else r["action"]
        if action == "keep":
            continue
        if action in ("merge", "archive"):
            await put(task, {"status": "archived"}, f"злито в {r['into']}" if action == "merge" else "в архів")
            continue
        patch = texts(r, task) | {"status": "active"}
        if r.get("kind"):
            patch["kind"] = kind_for(r["kind"], task.zone, task.subzone, task.tags)
        await put(task, patch, "активовано")


async def logic(tasks: dict) -> None:
    d = load("logic.yaml")
    for slug, r in (d.get("review") or {}).items():
        task = tasks.get(slug)
        if not task or slug in SKIP_REVIEW:
            log.append(f"{slug}: {'пропущено за рішенням' if task else 'нема в каталозі'}")
            continue
        if r["action"] == "merge":
            target = tasks.get(r.get("into", ""))
            if not target:
                log.append(f"{slug}: злиття в «{r.get('into')}», якої нема — пропущено")
                continue
            await put(task, {"status": "archived"}, f"злито в {target.slug}")
            continue
        zone, sub = (r.get("move_to") or f"{task.zone}/{task.subzone}").split("/")
        patch = texts(r, task, coin=slug not in SKIP_COIN) | {"zone": zone, "subzone": sub}
        if "parent" in r:  # out of a family: its parent becomes a card one can claim
            patch["parent"] = r["parent"]
        if r.get("kind"):
            patch["kind"] = kind_for(r["kind"], zone, sub, task.tags)
            if r["kind"] != "rule":
                patch["rule"] = {}
        await put(task, patch, r["action"])
    for slug, c in (d.get("new") or {}).items():
        if slug in tasks or slug in SKIP_REVIEW:
            continue
        zone, sub = c["home"].split("/")
        base = texts(c) | {"zone": zone, "subzone": sub, "status": c.get("status", "draft")}
        if c.get("kind"):
            base["kind"] = kind_for(c["kind"], zone, sub, c.get("tags") or [])
        await create(tasks, slug, base)


async def code(tasks: dict) -> None:
    d = load("code.yaml")
    for n, title in LABS.items():  # a family per lab: its page's requirements, the mandatory ones first
        if f"lab{n}" not in tasks:
            await create(tasks, f"lab{n}", {
                "title": title, "zone": "code", "subzone": "labs", "coin": "wood", "status": "active", "tags": [f"lab{n}"],
                "description": f"Картки зі [сторінки лаби](/labs/{n}): спершу обовʼязкове, далі додаткове. "
                               f"Картки цієї лаби з інших категорій — [пошук «lab{n}»](/tasks?q=lab{n})."})
    for slug, c in (d.get("new") or {}).items():
        if slug in tasks:
            continue
        lab, family = c.get("lab"), bool(c.get("home_wish"))
        zone, sub = ("code", "labs") if family else c["home"].split("/")
        base = texts(c) | {"zone": zone, "subzone": sub, "status": c.get("status", "draft")}
        if lab:
            base["tags"] = [f"lab{lab}"]
        if family:
            base["parent"] = f"lab{lab}"
            base["description"] = f"{'Обовʼязкове' if c.get('required') else 'Додаткове'} в лабі {lab}. {c['description']}"
        await create(tasks, slug, base)
    for slug, r in (d.get("reword") or {}).items():
        if slug in tasks:
            await put(tasks[slug], texts(r, tasks[slug], coin=slug not in SKIP_COIN), "новий текст")
    for slug, n in LAB_OF.items():
        if slug in tasks and f"lab{n}" not in tasks[slug].tags:
            await put(tasks[slug], {"tags": tasks[slug].tags + [f"lab{n}"]}, f"тег лаби {n}")


async def polish(tasks: dict) -> None:
    d = load("polish.yaml")
    for slug, r in (d.get("reword") or {}).items():
        if slug in tasks:
            await put(tasks[slug], texts(r, tasks[slug], coin=False), "текст")
    for slug, a in (d.get("aliases") or {}).items():
        if task := tasks.get(slug):
            more = {k: task.aliases.get(k, []) + [w for w in a.get(k) or [] if w not in task.aliases.get(k, [])] for k in LANGS}
            await put(task, {"aliases": more}, "синоніми")


async def main():
    assert "labs" in ZONES["code"]["subzones"], "zones.py: the subzone code/labs first"
    await init_db()
    tasks = {t.slug: t for t in await Task.find_all().to_list()}
    for step in (drafts, logic, code, polish):
        try:
            await step(tasks)
        except HTTPException as e:
            sys.exit(f"{step.__name__}: {e.detail}\n" + "\n".join(log[-3:]))
    (HERE / "apply.log").write_text("\n".join(log) + "\n")
    by = lambda word: sum(word in line for line in log)  # noqa: E731
    print(f"{'DRY · ' if DRY else ''}{len(log)} змін · активовано {by('активовано')} · нових {by('нова картка')} · в архів {by('злито') + by('в архів')}")


if __name__ == "__main__":
    asyncio.run(main())
