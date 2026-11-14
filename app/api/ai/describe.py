"""One request of «Описати словами» (T291 §14): the prompt, the model, the proposals, a draft in the base, a row in the game's
history, alerts. A failed call keeps its draft with the error and its price, and is not counted in the student's limits."""
from fastapi import BackgroundTasks, HTTPException

import options
from ai import client, context, cost, limits, normalize, prompt, schema, source
from bot import ai_alerts
from core.config import settings
from core.models.history import Change
from core.models.user import User
from models.draft import Draft
from models.game import Game


async def describe(game: Game, user: User, text: str, tasks: BackgroundTasks) -> dict:
    src = await source.load()
    ctx = await context.of_game(game, options.is_admin(user))
    before = await limits.spent()
    draft = Draft(game=game.id, owner=user.email, text=text, model=settings.ai_model)
    try:
        answer, draft.usage = await client.ask(settings.ai_model, prompt.stable(src), prompt.message(await context.have(game, ctx), text),
                                               schema.build(src))
    except client.AskError as e:
        draft.error, draft.usage = e.message, e.usage
    draft.cost = cost.of(draft.usage, settings.ai_model)
    after = before + draft.cost
    if draft.error:  # the response is the error: background tasks would never run
        await draft.insert()
        await ai_alerts.asked(user, draft, after)
        await ai_alerts.steps(limits.crossed(before, after), after)
        raise HTTPException(502, draft.error)
    draft.items = normalize.items(answer, ctx)
    await draft.insert()
    # not record_new: the history shows the text, the proposals and their states are the draft's (game_log_text.title)
    await Change(coll=Draft.Settings.name, doc_id=draft.id, actor=user.email,
                 changes={"game": {"old": None, "new": game.id}, "text": {"old": None, "new": text}}).insert()
    tasks.add_task(ai_alerts.asked, user, draft, after)
    tasks.add_task(ai_alerts.steps, limits.crossed(before, after), after)
    return draft.api()
