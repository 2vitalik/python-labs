# T106 · Telegram-бот: пустишка на aiogram — план

`2026-09-19` · ⚙️ задача · запит Vitalik у чаті: «давай реалізуємо Telegram-бота, поки що просто майже пустишка» · звіт — [report.md](report.md)

Контекст: концепт [T19](../T19-C--tgbot-concept.md) (бот = інтерфейс до тієї ж БД; aiogram), контракт привʼязки [T58](../T58-C--tg-link-binding.md), бік сайту готовий ([T64](../../../platform/.t/T64--profile-v1/report.md)), бот `@python_nure_bot` існує ([T60](../../../platform/.t/T60-Q--profile-questions.md) Q3).

## Рамки

- Мінімум, що має сенс: бот стартує, відповідає на `/start`, виконує контракт T58 (привʼязка за токеном). Нотифікацій, опитувань, «мого прогресу» нема — чекають [T20](../T20-Q--tgbot-open-questions.md).
- Той самий код-простір, що й API: тека `app/api/bot/`, спільні `config`/`db`/`models`; окремий пакет `app/bot/` потребував би path-хаків до моделей — не заради пустишки.
- Long polling у деві (публічної адреси нема); вебхук — разом із VPS (T19).
- Бібліотека — aiogram 3 (async, як FastAPI/Beanie).

## Кроки

1. `aiogram` у `pyproject.toml`; `TG_BOT_TOKEN` у `config.py` + `.env.example`.
2. `bot/__main__.py` — `init_db` + polling; `bot/start.py` — `/start` з payload і без, fallback; `bot/link.py` — `bind()` за T58 через `record()`.
3. Смоук `tests/smoke_bot.py` — хендлери на заглушці повідомлення, без Telegram.
4. Доки: `app/README.md`, README вузла, CHANGELOG.
