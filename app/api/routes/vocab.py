from fastapi import APIRouter, Depends

import options
from core.config import settings
from core.deps import viewer
from core.models.user import User
from models.vocab import vocab
from zones import KINDS

router = APIRouter()


def depth(user: User | None) -> str:
    """How much of «Моя гра» the asker fills: the teacher and test students — all of it, the rest — as the site says."""
    return "full" if user and (options.is_admin(user) or user.test) else settings.game_depth


@router.get("/api/vocab")
async def get_vocab(user: User | None = Depends(viewer)):
    """The description language for the forms: the rules' dictionaries, the arguments' names, the card kinds,
    and from the catalog — entity roles, stats, the field's options."""
    cat = await options.catalog(options.is_admin(user))
    return vocab() | await options.described(cat) | {"kinds": KINDS, "depth": depth(user)}
