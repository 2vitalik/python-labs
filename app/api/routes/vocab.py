from fastapi import APIRouter

from models.vocab import vocab

router = APIRouter()


@router.get("/api/vocab")
async def get_vocab():
    """The description language for the forms: roles, triggers, conditions, effects, field props, stat hints."""
    return vocab()
