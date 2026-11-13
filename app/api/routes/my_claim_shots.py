"""The proof of a claim (T284 §7): up to three pictures of what was done, files under uploads/<game-id>/, names in Claim.shots."""
from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException, UploadFile

import uploads
from core.models.history import record
from core.models.user import User
from models.game import Game
from routes.my_claims import get_claim
from routes.my_game import author, in_sandbox, my_game

router = APIRouter(prefix="/api/my/claims")
MAX = 3


@router.post("/{id}/shot")
async def add_shot(id: PydanticObjectId, file: UploadFile, game: Game = Depends(my_game), user: User = Depends(author)):
    if in_sandbox(user):
        raise HTTPException(403, "У пісочниці докази не зберігаються.")
    claim = await get_claim(id, game)
    if len(claim.shots) >= MAX:
        raise HTTPException(422, "Не більше трьох файлів на заявку.")
    name = await uploads.save_shot(str(game.id), file)
    await record(claim, {"shots": claim.shots + [name]}, actor=user.email)
    return claim.api()


@router.delete("/{id}/shot/{name}")
async def delete_shot(id: PydanticObjectId, name: str, game: Game = Depends(my_game), user: User = Depends(author)):
    claim = await get_claim(id, game)
    if name not in claim.shots:
        raise HTTPException(404)
    uploads.drop_shot(str(game.id), name)
    await record(claim, {"shots": [s for s in claim.shots if s != name]}, actor=user.email)
    return claim.api()
