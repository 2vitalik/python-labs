import table_seed  # noqa: F401 — the site's views of /table
from core.app import create_app
from db import MODELS
from routes import content, intake, lab_files, lab_gates, lab_live, lab_pages, lab_review, lab_run, lab_start, lab_stats, labs, media, student_variants  # noqa: F401 — student_variants: lab cards on a student's row

LABS = [labs.router, lab_start.router, lab_files.router, lab_review.router, lab_stats.router, lab_run.router, lab_live.router, lab_gates.router]
app = create_app(models=MODELS, routers=[media.router, *LABS, lab_pages.router, content.router, intake.router])
