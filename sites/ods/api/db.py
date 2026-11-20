from core import db
from models.forward import Forward
from models.lab import LabVariant
from models.lab_file import LabFile
from models.lab_gate import LabGate
from models.lab_page import LabPage
from models.lab_shape import LabShape
from models.lecture_change import LectureChanges
from models.media import Media

MODELS = [Media, LabVariant, LabFile, LabShape, LabPage, LabGate, Forward, LectureChanges]  # the site's own, next to the platform's


async def init_db():
    await db.init_db(MODELS)
