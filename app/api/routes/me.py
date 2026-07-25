from fastapi import APIRouter, Depends

from deps import current_user
from models.user import User

router = APIRouter()


@router.get("/api/me")
async def me(user: User | None = Depends(current_user)):
    if not user:
        return None
    return {"email": user.email, "name": user.name, "picture": user.picture, "status": user.status}
