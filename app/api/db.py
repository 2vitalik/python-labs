from beanie import init_beanie
from pymongo import AsyncMongoClient

from config import settings
from models.activity import Activity
from models.base_game import BaseGame
from models.game import Claim, Game, Part
from models.guide import Guide
from models.history import Change
from models.message import TgMessage
from models.note import Note
from models.notify import Route
from models.ref import Ref
from models.rule import Rule
from models.task import Task
from models.user import User


mongo = AsyncMongoClient(settings.mongo_uri)  # connects lazily, so it is safe to build at import


async def init_db():
    await init_beanie(mongo[settings.db_name],
                      document_models=[User, Change, Route, BaseGame, Task, Game, Part, Claim, Rule, Ref, Activity, Guide, TgMessage, Note])
