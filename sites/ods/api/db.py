from core import db
from models.lab import LabVariant
from models.media import Media

MODELS = [Media, LabVariant]  # the site's own, next to the platform's


async def init_db():
    await db.init_db(MODELS)
