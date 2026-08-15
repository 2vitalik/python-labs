"""Screenshot files: uploads/<work-id>/<uuid>.<ext>, served as /api/uploads (git-ignored)."""
from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile

from config import settings

ROOT = Path(settings.uploads_dir) if settings.uploads_dir else Path(__file__).parent / "uploads"
TYPES = {"image/png": "png", "image/jpeg": "jpg", "image/webp": "webp", "image/gif": "gif"}
MAX_BYTES = 8 * 2**20


async def save_shot(work_id: str, file: UploadFile) -> str:
    ext = TYPES.get(file.content_type)
    if not ext:
        raise HTTPException(422, "Формат не підтримується: потрібен png, jpg, webp або gif.")
    data = await file.read()
    if len(data) > MAX_BYTES:
        raise HTTPException(422, "Файл завеликий: ліміт 8 МБ.")
    name = f"{uuid4().hex}.{ext}"
    folder = ROOT / work_id
    folder.mkdir(parents=True, exist_ok=True)
    (folder / name).write_bytes(data)
    return name


def drop_shot(work_id: str, name: str) -> None:
    path = ROOT / work_id / name
    if path.is_file():
        path.unlink()
