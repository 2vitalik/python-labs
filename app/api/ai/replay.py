"""A model's answer through the site's own checks, without the site (T292): the proposals the student would see for an empty
game, or one with the named entities and windows. Schema mismatches go to stderr. Run from app/api on a base with the catalog:
uv run python -m ai.replay <answer.json> [--have "Сутність;Вікно;…"]"""
import argparse
import asyncio
import json
import sys
from pathlib import Path

from ai import context, normalize, schema, source
from db import init_db


async def main(path: Path, have: str) -> None:
    await init_db()
    answer = json.loads(path.read_text())
    for p in schema.mismatch(answer, schema.build(await source.load())):
        print("schema:", p, file=sys.stderr)
    ctx = await context.of_names([n.strip() for n in have.split(";") if n.strip()])
    items = normalize.items(answer, ctx)
    unknown = sum(1 for it in items if it["group"] == "unknown")
    print(json.dumps({"items": items, "problems": unknown - len(answer.get("unknown") or [])}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("answer", type=Path)
    args.add_argument("--have", default="", help="names of the entities and windows the game has, by «;»")
    a = args.parse_args()
    asyncio.run(main(a.answer, a.have))
