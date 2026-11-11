"""History of one student's game (T278 §12): read-only, for the owner and the teacher."""
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query

import game_log
from core.deps import active_user
from core.models.user import Status, User
from models.game import Game
from routes.student_games import visible_owner

router = APIRouter(prefix="/api/students")


@router.get("/{nick}/game/history")
async def game_history(nick: str, before: datetime | None = None, limit: int = Query(50, ge=1, le=200),
                       user: User = Depends(active_user)):
    """Newest first; `before` — `at` of the last row seen, for the next page. A fellow student sees the game, not its history."""
    owner = await visible_owner(nick, user)
    if owner.email != user.email and user.status != Status.admin:
        raise HTTPException(403, "Історію гри бачать її автор і викладач.")
    game = await Game.find_one(Game.owner == owner.email)
    return await game_log.rows(game, before, limit) if game else []
