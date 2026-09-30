from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException

from core.deps import admin_user
from core.models.history import record, record_delete, record_new
from core.models.poll import Poll, PollTemplate
from core.models.user import User
from core.polls_in import PollIn, clean

router = APIRouter(prefix="/api/polls/templates")


async def known_tags() -> list[str]:
    """For the tag field's hints: every tag of polls and templates."""
    both = [*await Poll.get_pymongo_collection().distinct("tags"), *await PollTemplate.get_pymongo_collection().distinct("tags")]
    return sorted(set(both), key=str.lower)


async def get_template(id: PydanticObjectId) -> PollTemplate:
    template = await PollTemplate.get(id)
    if not template:
        raise HTTPException(404)
    return template


@router.get("")
async def list_templates(admin: User = Depends(admin_user)):
    templates = await PollTemplate.find_all().to_list()
    return {"templates": [t.api() for t in sorted(templates, key=lambda t: t.title.lower())], "tags": await known_tags()}


@router.post("")
async def create_template(data: PollIn, admin: User = Depends(admin_user)):
    template = PollTemplate(**clean(data), by=admin.email)
    await template.insert()
    await record_new(template, actor=admin.email)
    return template.api()


@router.put("/{id}")
async def update_template(id: PydanticObjectId, data: PollIn, admin: User = Depends(admin_user)):
    template = await get_template(id)
    await record(template, clean(data), actor=admin.email)
    return template.api()


@router.delete("/{id}")
async def delete_template(id: PydanticObjectId, admin: User = Depends(admin_user)):
    """Polls made from it keep their copy."""
    await record_delete(await get_template(id), actor=admin.email)
    return {"ok": True}
