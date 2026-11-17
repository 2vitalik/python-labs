from core import db
from models.base_game import BaseGame
from models.draft import Draft
from models.game import Claim, Game, Part
from models.ludo_game import LudoGame
from models.ref import Ref
from models.rule import Rule
from models.task import Task
from models.video import Video

MODELS = [BaseGame, Task, Game, Part, Claim, Rule, Ref, LudoGame, Draft, Video]  # the site's own, next to the platform's


async def init_db():
    await db.init_db(MODELS)
