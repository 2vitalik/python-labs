from fastapi import Request

from models.user import User


async def current_user(request: Request) -> User | None:
    email = request.session.get("email")
    return await User.find_one(User.email == email) if email else None
