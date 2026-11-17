from fastapi.staticfiles import StaticFiles

import lesson_defenses  # noqa: F401 — defenses as parts of a lesson's day
import table_seed  # noqa: F401 — the site's views of /table
import uploads
from core.app import create_app
from db import MODELS
from routes import (asks, card_history, catalog, defenses, etalon, features, game_history, games, ludopedia, my_ai, my_claim_shots, my_claims,
                    my_game, my_parts, my_remarks, my_rules, my_shots, my_states, my_template, my_videos, refs, remarks, sandbox, student_games,
                    tasks, taxonomy, vocab)

app = create_app(models=MODELS, routers=[
    student_games.router, game_history.router, games.router, etalon.router, sandbox.router, tasks.router, taxonomy.router, catalog.router,
    card_history.router, asks.router, vocab.router, features.router, my_game.router, my_parts.router, my_states.router, my_shots.router, my_claims.router,
    my_claim_shots.router, my_rules.router, my_template.router, my_videos.router, my_ai.router, refs.router, ludopedia.router,
    defenses.router, remarks.router, my_remarks.router,
])
uploads.ROOT.mkdir(parents=True, exist_ok=True)
app.mount("/api/uploads", StaticFiles(directory=uploads.ROOT), name="uploads")
