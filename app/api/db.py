from beanie import init_beanie
from pymongo import AsyncMongoClient

from config import settings
from models.user import User


async def init_db():
    client = AsyncMongoClient(settings.mongo_uri)
    await init_beanie(client[settings.db_name], document_models=[User])
