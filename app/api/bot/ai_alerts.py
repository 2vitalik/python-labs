"""Alerts of «Описати словами» (kind `ai`, T291 §14): every request — who, the text, what came of it, its price and the
month's sum; and once per step — when the month's spending reaches 50, 80, 100 % of the ceiling."""
from aiogram import html

from core.bot import notify
from core.bot.alerts import who
from core.config import settings
from core.models.user import User
from models.draft import Draft

CUT = 700  # the text's quote: a long one is cut here


def money(x: float) -> str:
    return f"${x:.3f}" if x < 0.1 else f"${x:.2f}"


async def asked(user: User, draft: Draft, month: float) -> None:
    """`month` — the month's spending with this request."""
    text = draft.text if len(draft.text) <= CUT else draft.text[:CUT].rstrip() + "…"
    unknown = sum(1 for it in draft.items if it["group"] == "unknown")
    rows = [f"✨ Опис словами · {who(user)}", f"<blockquote>{html.quote(text)}</blockquote>",
            f"⚠️ {html.quote(draft.error)}" if draft.error else f"🧩 пропозицій {len(draft.items) - unknown} · не розпізнано {unknown}",
            f"💵 {money(draft.cost)} · за місяць {money(month)} з ${settings.ai_budget_usd:g}"]
    await notify.send("ai", "\n".join(rows), user.email)


async def steps(crossed: list[int], month: float) -> None:
    for p in crossed:
        await notify.send("ai", f"💸 ШІ-помічник: витрачено {p} % місячної стелі · {money(month)} з ${settings.ai_budget_usd:g}"
                          + ("\n⛔ Нові запити до кінця місяця не приймаються" if p >= 100 else ""))
