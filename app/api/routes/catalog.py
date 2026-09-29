"""The catalog as its git snapshot (T155): the YAML that `catalog_io.py export` writes, for `bin/catalog snap`."""
from fastapi import APIRouter, Depends

from catalog_io import render
from core.deps import editor_user
from core.models.user import User

router = APIRouter(prefix="/api/catalog")


@router.get("/snapshot")
async def snapshot(user: User = Depends(editor_user)):
    return await render()
