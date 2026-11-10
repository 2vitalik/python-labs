"""Screenshots of a part: files under uploads/<game-id>/, names in Part.screenshots."""
from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException, UploadFile

import uploads
from core.deps import active_user
from core.models.history import record
from core.models.user import User
from models.game import Game
from routes.my_game import my_game
from routes.my_parts import get_part

router = APIRouter(prefix="/api/my/game/parts")


@router.post("/{id}/screenshot")
async def add_screenshot(id: PydanticObjectId, file: UploadFile, game: Game = Depends(my_game),
                         user: User = Depends(active_user)):
    part = await get_part(id, game)
    name = await uploads.save_shot(str(game.id), file)
    await record(part, {"screenshots": part.screenshots + [name]}, actor=user.email)
    return part.api()


@router.delete("/{id}/screenshot/{name}")
async def delete_screenshot(id: PydanticObjectId, name: str, game: Game = Depends(my_game),
                            user: User = Depends(active_user)):
    part = await get_part(id, game)
    if name not in part.screenshots:
        raise HTTPException(404)
    uploads.drop_shot(str(game.id), name)
    await record(part, {"screenshots": [s for s in part.screenshots if s != name]}, actor=user.email)
    return part.api()
