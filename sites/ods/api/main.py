import table_seed  # noqa: F401 — the site's views of /table
from core.app import create_app
from db import MODELS
from routes import labs, media, student_variants  # noqa: F401 — student_variants: lab cards on a student's row

app = create_app(models=MODELS, routers=[media.router, labs.router])
