"""One-off (T285): apply the sure verdicts of review-*.yaml (catalog review v6, T284 §8) to Mongo; `catalog_io export` then
writes the YAML. A verdict changes title, description, price, `games`, `proof` and status of a card that exists; `merge`
archives the card and hands its other names to the card it goes into; `new` cards are created active. Slugs, homes, kinds
and rule blanks stay. `certainty: unsure` is skipped — those are questions for the teacher. Everything goes through
`record`, so /tasks/history shows each change and can take it back. Every run appends to apply.log beside this file.
Run from app/api:  uv run python ../../.dev/platform/.t/T285--game-desc-v6/catalog/apply.py [--dry] [--skip slug,slug]"""
import asyncio
import sys
from datetime import datetime
from pathlib import Path

import yaml

sys.path.insert(0, ".")
from core.config import settings  # noqa: E402
from core.models.history import record, record_new  # noqa: E402
from db import init_db  # noqa: E402
from models.task import LANGS, PROOFS, Task  # noqa: E402
from zones import COINS, KINDS, ZONES  # noqa: E402

HERE = Path(__file__).parent
DRY = "--dry" in sys.argv
SKIP = set(sys.argv[sys.argv.index("--skip") + 1].split(",")) if "--skip" in sys.argv else set()
ACTOR = "claude@agent"
PROOF = {*PROOFS, ""}
FIELDS = ("title", "description", "coin", "games", "proof")


def patch_for(task: Task, r: dict) -> dict:
    patch = {k: r[k] for k in FIELDS if k in r}
    patch |= {k: v.strip() for k, v in patch.items() if isinstance(v, str)}
    if r["action"] == "activate":
        patch["status"] = "active"
    if r["action"] in ("merge", "archive"):
        patch = {"status": "archived"}
    assert patch.get("coin", "wood") in COINS, f"{task.slug}: монетка {patch.get('coin')}"
    assert patch.get("proof", "") in PROOF, f"{task.slug}: доказ {patch.get('proof')}"
    assert " — " not in patch.get("title", ""), f"{task.slug}: « — » у назві"
    return {k: v for k, v in patch.items() if getattr(task, k) != v}


def born(n: dict, tasks: dict) -> Task:
    zone, sub = n["zone"], n["subzone"]
    assert sub in ZONES[zone]["subzones"], f"{n['slug']}: нема підкатегорії {zone}/{sub}"
    assert n["coin"] in COINS and n.get("kind", "") in set(KINDS) | {""} and n.get("proof", "") in PROOF, n["slug"]
    assert not n.get("parent") or n["parent"] in tasks, f"{n['slug']}: нема сімʼї {n.get('parent')}"
    kin = [t.order for t in tasks.values() if (t.zone, t.subzone) == (zone, sub) and (not n.get("parent") or t.parent == n["parent"])]
    return Task(slug=n["slug"], title=n["title"].strip(), description=n["description"].strip(), zone=zone, subzone=sub,
                kind=n.get("kind", ""), opt=n.get("opt", ""), parent=n.get("parent", ""), coin=n["coin"],
                max_count=n.get("max_count", 1), proof=n.get("proof", ""), aliases=n.get("aliases") or {},
                status="active", order=max(kin, default=0) + 5)


async def main():
    await init_db()
    tasks = {t.slug: t for t in await Task.find_all().to_list()}
    log, changed = [], 0
    for path in sorted(HERE.glob("review-*.yaml")):
        data = yaml.safe_load(path.read_text())
        log.append(f"## {data['group']}")
        for slug, r in data["cards"].items():
            task = tasks.get(slug)
            if not task:
                log.append(f"{slug}: нема в каталозі — пропущено")
                continue
            if r.get("certainty") == "unsure" or slug in SKIP:
                if r["action"] != "keep" or any(k in r for k in FIELDS[:4]):
                    log.append(f"{slug}: {r['action']} — не застосовано ({'відкладено' if slug in SKIP else 'питання викладачеві'})")
                continue
            patch = patch_for(task, r)
            if r["action"] == "merge" and task.status != "archived":  # its other names go on finding the card it became
                into = tasks[r["into"]]
                names = {k: list(dict.fromkeys(into.aliases[k] + task.aliases[k])) for k in LANGS}
                if names != into.aliases and not DRY:
                    await record(into, {"aliases": names}, actor=ACTOR)
            if not patch:
                continue
            changed += 1
            was = f" {task.coin} → {patch['coin']}" if "coin" in patch else ""
            log.append(f"{slug}: {r['action']}{' → ' + r['into'] if r.get('into') else ''} — {', '.join(patch)}{was}")
            if not DRY:
                await record(task, patch, actor=ACTOR)
        for n in data.get("new") or []:
            if n["slug"] in tasks or n["slug"] in SKIP:
                log.append(f"{n['slug']}: нова — {'відкладено' if n['slug'] in SKIP else 'вже є'}")
                continue
            task = born(n, tasks)
            tasks[task.slug] = task
            changed += 1
            log.append(f"{task.slug}: нова картка — {task.zone}/{task.subzone} {task.coin} «{task.title}»")
            if not DRY:
                await task.insert()
                await record_new(task, actor=ACTOR)
    head = f"# {datetime.now():%Y-%m-%d %H:%M} · {settings.db_name}{' · dry' if DRY else ''} · змінено {changed}"
    with (HERE / "apply.log").open("a") as f:
        f.write("\n".join([head, *log]) + "\n\n")
    print(f"{'DRY · ' if DRY else ''}{settings.db_name}: змінено {changed} карток")
    print("\n".join(line for line in log if line.startswith("##") or "не застосовано" in line or "нова" in line or "merge" in line or "пропущено" in line))


if __name__ == "__main__":
    asyncio.run(main())
