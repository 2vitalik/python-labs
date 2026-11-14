"""The request without the site, to measure the models on (T292): the stable start, the schema and a user's message for an
empty game, into a folder. Run from app/api on a base with the catalog: uv run python -m ai.dump <folder>"""
import asyncio
import json
import sys
from pathlib import Path

from ai import prompt, schema, source
from db import init_db


async def main(folder: Path) -> None:
    await init_db()
    src = await source.load()
    folder.mkdir(parents=True, exist_ok=True)
    system = prompt.stable(src)
    (folder / "system.md").write_text(system)
    (folder / "schema.json").write_text(json.dumps(schema.build(src), ensure_ascii=False, indent=1) + "\n")
    (folder / "user-example.md").write_text(prompt.message(prompt.EMPTY, "Тут текст студента: що є в його грі, словами.") + "\n")
    print(f"{folder}: system.md {len(system)} знаків, schema.json, user-example.md")


if __name__ == "__main__":
    asyncio.run(main(Path(sys.argv[1])))
