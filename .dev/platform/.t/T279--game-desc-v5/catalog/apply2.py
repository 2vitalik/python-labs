"""One-off (T279): apply the sure verdicts of logic2.yaml («Логіка» vs entities) to Mongo; `catalog_io export` then writes the YAML.
Updates of existing cards only — home, kind, rule blank, description; never price, title, slug, status; nothing is created
or deleted. Every run appends to apply2.log beside this file.
Run from app/api:  uv run python ../../.dev/platform/.t/T279--game-desc-v5/catalog/apply2.py [--dry]"""
import asyncio
import sys
from datetime import datetime
from pathlib import Path

import yaml
from fastapi import HTTPException

sys.path.insert(0, ".")
from core.config import settings  # noqa: E402
from core.models.history import record  # noqa: E402
from db import init_db  # noqa: E402
from models.task import Task  # noqa: E402
from tasks_clean import clean_rule  # noqa: E402
from zones import ZONES, default_kind  # noqa: E402

HERE = Path(__file__).parent
DRY = "--dry" in sys.argv
ACTOR = "claude@agent"
ALLOWED = {"move_to", "after", "kind", "rule", "description"}


def patch_for(task: Task, change: dict, tasks: dict) -> dict:
    zone, sub = (change.get("move_to") or f"{task.zone}/{task.subzone}").split("/")
    assert sub in ZONES[zone]["subzones"], f"{task.slug}: нема підкатегорії {zone}/{sub}"
    kind = change.get("kind") or task.kind or default_kind(task.zone, task.subzone, task.tags)
    patch = {"zone": zone, "subzone": sub, "kind": "" if kind == default_kind(zone, sub, task.tags) else kind}
    if "after" in change:  # right after that card (and its family) in the new home; export renumbers
        patch["order"] = tasks[change["after"]].order + 5
    if "rule" in change:
        patch["rule"] = clean_rule(change["rule"])
    elif kind != "rule":
        patch["rule"] = {}
    if "description" in change:
        patch["description"] = change["description"].strip()
    return {k: v for k, v in patch.items() if getattr(task, k) != v}


async def main():
    await init_db()
    tasks = {t.slug: t for t in await Task.find_all().to_list()}
    data = yaml.safe_load((HERE / "logic2.yaml").read_text())
    log = []
    for section in ("review", "interface", "neighbors"):
        for slug, r in (data.get(section) or {}).items():
            change = r.get("change")
            if r.get("certainty") != "sure" or not change:
                continue
            assert set(change) <= ALLOWED, f"{slug}: {set(change) - ALLOWED}"
            task = tasks.get(slug)
            if not task:
                log.append(f"{slug}: нема в каталозі — пропущено")
                continue
            try:
                patch = patch_for(task, change, tasks)
            except HTTPException as e:
                sys.exit(f"{slug}: {e.detail}")
            if not patch:
                log.append(f"{slug}: без змін")
                continue
            log.append(f"{slug}: {r['verdict']} — {', '.join(patch)}"
                       + (f" ({task.zone}/{task.subzone} → {patch.get('zone', task.zone)}/{patch.get('subzone', task.subzone)})"
                          if "subzone" in patch or "zone" in patch else ""))
            if not DRY:
                await record(task, patch, actor=ACTOR)
    head = f"# {datetime.now():%Y-%m-%d %H:%M} · {settings.db_name}{' · dry' if DRY else ''}"
    with (HERE / "apply2.log").open("a") as f:
        f.write("\n".join([head, *log]) + "\n\n")
    changed = sum(not line.endswith(("пропущено", "без змін")) for line in log)
    print(f"{'DRY · ' if DRY else ''}{settings.db_name}: змінено {changed} карток\n" + "\n".join(log))


if __name__ == "__main__":
    asyncio.run(main())
