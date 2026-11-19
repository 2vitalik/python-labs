from fastapi import APIRouter, Depends

from core.models.user import User
from core.routes.guide import reader
from models.lab_page import LabPage

router = APIRouter(prefix="/api/labpages")


@router.get("")
async def list_pages(user: User | None = Depends(reader)):
    """The labs' pages beyond the list of labs, in the order the site shows them; open to whoever reads the texts."""
    pages = await LabPage.find_all().sort("lab", "order").to_list()
    return [p.model_dump(exclude={"id"}) for p in pages]
