from fastapi.staticfiles import StaticFiles

import uploads
from core.app import create_app
from db import MODELS
from routes import (card_history, catalog, etalon, games, ludopedia, my_claims, my_game, my_parts, my_rules, my_shots,
                    my_template, refs, student_games, tasks, taxonomy, vocab)

app = create_app(models=MODELS, routers=[
    student_games.router, games.router, etalon.router, tasks.router, taxonomy.router, catalog.router, card_history.router,
    vocab.router, my_game.router, my_parts.router, my_shots.router, my_claims.router, my_rules.router, my_template.router,
    refs.router, ludopedia.router,
])
uploads.ROOT.mkdir(parents=True, exist_ok=True)
app.mount("/api/uploads", StaticFiles(directory=uploads.ROOT), name="uploads")
