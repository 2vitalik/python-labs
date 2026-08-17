"""Screenshot files: uploads/<game-id>/<uuid>.<ext>, served as /api/uploads (git-ignored).
Deleted files move to the uploads.trash/ sibling (kept out of StaticFiles) — nothing is lost forever."""
from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile

from config import settings

ROOT = Path(settings.uploads_dir) if settings.uploads_dir else Path(__file__).parent / "uploads"
TRASH = ROOT.parent / (ROOT.name + ".trash")
TYPES = {"image/png": "png", "image/jpeg": "jpg", "image/webp": "webp", "image/gif": "gif"}
MAX_BYTES = 8 * 2**20


async def save_shot(game_id: str, file: UploadFile) -> str:
    ext = TYPES.get(file.content_type)
    if not ext:
        raise HTTPException(422, "Формат не підтримується: потрібен png, jpg, webp або gif.")
    data = await file.read()
    if len(data) > MAX_BYTES:
        raise HTTPException(422, "Файл завеликий: ліміт 8 МБ.")
    name = f"{uuid4().hex}.{ext}"
    folder = ROOT / game_id
    folder.mkdir(parents=True, exist_ok=True)
    (folder / name).write_bytes(data)
    return name


def drop_shot(game_id: str, name: str) -> None:
    path = ROOT / game_id / name
    if path.is_file():
        folder = TRASH / game_id
        folder.mkdir(parents=True, exist_ok=True)
        path.rename(folder / name)
