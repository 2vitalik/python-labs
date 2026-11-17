from fastapi import APIRouter, Depends

import features
import grading
import options
from core.config import settings
from core.deps import viewer
from core.models.user import User
from models.vocab import vocab
from zones import KINDS

router = APIRouter()


@router.get("/api/vocab")
async def get_vocab(user: User | None = Depends(viewer)):
    """The description language for the forms: the rules' dictionaries, the arguments' names, the card kinds,
    and from the catalog — entity roles, stats, the field's options; the page's features — which are closed, and to whom it matters."""
    admin = options.is_admin(user)
    cat = await options.catalog(admin)
    seen = settings.grade_scale == "open" or admin
    return vocab() | await options.described(cat) | {
        "kinds": KINDS, "features": {"all": list(features.EXTRAS), "closed": await features.closed(), "free": admin},
        "grade": {"wood": grading.WOOD, "scale": grading.SCALE if seen else [], "draft": settings.grade_scale != "open"},
    }
