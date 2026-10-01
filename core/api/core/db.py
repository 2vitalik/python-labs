from beanie import init_beanie
from pymongo import AsyncMongoClient

from core.config import settings
from core.models.activity import Activity
from core.models.error import Error
from core.models.event import Event
from core.models.guide import Guide
from core.models.history import Change
from core.models.message import TgMessage
from core.models.note import Note
from core.models.notify import Route
from core.models.poll import Poll, PollTemplate
from core.models.poll_send import PollSend
from core.models.user import User
from core.models.vote import TgChat, Vote
from core.models.week import Week

MODELS = [User, Change, Route, Activity, Guide, TgMessage, Note, Event, Error, PollTemplate, Poll, PollSend, Vote, TgChat, Week]
mongo = AsyncMongoClient(settings.mongo_uri)  # connects lazily, so it is safe to build at import


async def init_db(models=()):
    """`models` — the site's own documents."""
    await init_beanie(mongo[settings.db_name], document_models=[*MODELS, *models])
