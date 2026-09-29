from core import db
from models.media import Media

MODELS = [Media]  # the site's own, next to the platform's


async def init_db():
    await db.init_db(MODELS)
