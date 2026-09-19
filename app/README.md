# app — Python Labs (мікро-MVP)

- `api/` — FastAPI-бекенд (uv, MongoDB/Beanie, Google OAuth)
- `vue/` — Vue 3 SPA (Vite, Bootstrap 5)

## Перший запуск

1. локальний `mongod` має працювати;
2. `cd app/api && cp .env.example .env` — вписати Google-креди ([інструкція](../.dev/platform/.t/T43-C--gcp-oauth-setup.md)), `SESSION_SECRET` (`openssl rand -hex 32`) і свою пошту в `ADMIN_EMAILS`;
3. `cd app/api && uv sync`;
4. `cd app/vue && npm install`.

## Дев-запуск

Порти — №3 у крос-проєктній схемі (`dev-md-rules/DEV.md`): API 8030, фронт 5030.

- бекенд: `cd app/api && uv run fastapi dev --port 8030` → http://localhost:8030
- фронт: `cd app/vue && npm run dev` → **http://localhost:5030** (відкривати цю адресу)
- дев-вхід без Google: кнопка «Dev-вхід» у шапці (працює, якщо в `.env` заданий `FAKE_USER_EMAIL`)

У PyCharm (Pro): run-конфігурація FastAPI (`app/api/main.py`, в Uvicorn options — `--port 8030`) + npm-конфігурація `dev` (`app/vue/package.json`) + Compound «app» — запуск обох однією кнопкою.

## Telegram-бот

Живе в `app/api/bot/` — та сама база, моделі й `.env`, що й API (тому не окремий пакет). Уміє: `/start` + привʼязка акаунта deep link-ом з профілю; адмін-алерти (профілі, перші входи, заявки, гра студента, помилки API/бота) — без налаштувань особисто адмінам, що привʼязали бота, або в групу/гілку форуму після `/here change` там (`/here` — статус із ключами видів, `/here all`, `/here off`, `/mute game` — вимкнути вид). Алерти шле сам API (той самий `TG_BOT_TOKEN`), запущений бот потрібен лише для `/here` і ранкового дайджесту профілів (09:00 Київ).

- токен від BotFather → `TG_BOT_TOKEN` у `app/api/.env`;
- запуск: `cd app/api && uv run python -m bot` (long polling, вебхук не потрібен);
- смоуки без Telegram: `DB_NAME=python_labs_smoke uv run python tests/smoke_bot.py` (привʼязка), `… tests/smoke_notify.py` (алерти профілю, `/here`, `/mute`), `… tests/smoke_events.py` (заявки, гра, помилки, дайджест, перший вхід).
