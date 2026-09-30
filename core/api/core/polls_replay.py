"""Put back what Mongo missed (T176): the bot writes every poll update to disk before the database, so a vote lost to a database
that was down is still in the file. Run from the site's folder: `uv run python -m core.polls_replay [file]`; it is safe to repeat."""
import asyncio
import json
import sys
from pathlib import Path

from aiogram.types import Update

from core.bot import polls
from core.db import init_db


async def replay(path: Path) -> tuple[int, int]:
    """(votes in the file, of them added now); poll states are applied in the file's order, so the latest stays."""
    seen = added = 0
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        update = Update.model_validate(json.loads(line))
        if update.poll_answer:
            seen += 1
            added += await polls.record_answer(update.poll_answer, update.update_id)
        elif update.poll:
            await polls.record_state(update.poll)
    return seen, added


async def main(path: Path) -> None:
    await init_db()
    seen, added = await replay(path)
    print(f"голосів у файлі: {seen} · додано зараз: {added}")


if __name__ == "__main__":
    asyncio.run(main(Path(sys.argv[1]) if len(sys.argv) > 1 else polls.LOG))
