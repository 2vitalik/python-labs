# T106 · Telegram-бот: пустишка на aiogram — звіт

`2026-09-19` · ⚙️ задача · план — [plan.md](plan.md)

Зроблено за планом; смоук **7/7 PASS**; з фейковим токеном бот доходить до Telegram і отримує очікуваний `Unauthorized` — живий запуск чекає справжнього токена.

## Код (`app/api/bot/`)

- `__main__.py` — `uv run python -m bot` з `app/api`: `init_db()` (та сама Mongo), `Bot(TG_BOT_TOKEN)`, long polling, у лог — `polling as @username`; порожній токен → зрозумілий exit без трейсбека.
- `start.py` — три хендлери: `/start <payload>` (`CommandStart(deep_link=True)`) → `bind()`; голий `/start` (`deep_link=False`) → привітання + підказка про кнопку в профілі; будь-що інше → «поки вмію лише /start».
- `link.py` — `bind(token, chat_id, username)`: контракт [T58](../T58-C--tg-link-binding.md) — юзер за `tg_token`, запис `tg_chat_id` + справжній `tg_username` через `record()` з actor `tgbot` (видно в `history` — саме для відкату захоплення чужого токена); порожній токен ніколи не шукається (інакше знайшовся б перший юзер без токена); без `@username` у Telegram ручне поле не затирається; повторний `/start` — перепривʼязка chat_id (фіча за T58).
- Привітання на імʼя: `first_name` → `name` (Google) → нік.
- Конфіг: `tg_bot_token` у `config.py`, `TG_BOT_TOKEN=` у `.env.example`; залежність `aiogram>=3.31` (+ aiohttp і компанія в lock).

## Смоук — `tests/smoke_bot.py`

Хендлери викликаються напряму із `SimpleNamespace`-заглушкою повідомлення (лише те, чого вони торкаються: `chat.id`, `from_user.username`, `answer`) — без Telegram і без aiogram-фільтрів: голий `/start` · невідомий токен нічого не пише · відомий → привіт на імʼя + chat_id + username + запис у history · перепривʼязка з іншого chat без username лишає username · fallback. Запуск: `DB_NAME=python_labs_smoke uv run python tests/smoke_bot.py`.

## Рішення по ходу

- Бот усередині `app/api/`, не окремий пакет: плоскі імпорти бекенду (`from models…`) працюють лише з cwd `app/api`; окрема тека означала б path-хаки або перетворення api на пакет — не для пустишки. Переїзд, якщо бот виросте, — `git mv` + імпорти.
- Long polling замість вебхука: дев без публічної адреси; вебхук — разом із деплоєм (T19).
- `actor="tgbot"` у history замість пошти студента: дія технічно студентова, але важливо бачити, що поле поставив бот — так помітне захоплення чужого токена.

## Далі

- Vitalik: токен від BotFather у `app/api/.env` (`TG_BOT_TOKEN`) → `uv run python -m bot` → «Привʼязати бота» в профілі → «Привіт, …! Записав тебе ✅».
- Функції бота — після відповідей [T20](../T20-Q--tgbot-open-questions.md) (перша черга за T19 — нотифікації + «мій прогрес»).
- PyCharm: run-конфігурація Python «Module: bot», working dir `app/api`.
