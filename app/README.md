# app — Python Labs (мікро-MVP)

- `api/` — FastAPI-бекенд (uv, MongoDB/Beanie, Google OAuth)
- `vue/` — Vue 3 SPA (Vite, Bootstrap 5)

## Перший запуск

1. локальний `mongod` має працювати;
2. `cd app/api && cp .env.example .env` — вписати Google-креди ([інструкція](../.dev/platform/.t/T43-C--gcp-oauth-setup.md)), `SESSION_SECRET` (`openssl rand -hex 32`) і свою пошту в `ADMIN_EMAILS`;
3. `cd app/api && uv sync`;
4. `cd app/vue && npm install`.

## Дев-запуск

- бекенд: `cd app/api && uv run fastapi dev` → http://localhost:8000
- фронт: `cd app/vue && npm run dev` → **http://localhost:5173** (відкривати цю адресу)
- дев-вхід без Google: кнопка «Dev-вхід» у шапці (працює, якщо в `.env` заданий `FAKE_USER_EMAIL`)

У PyCharm (Pro): run-конфігурація FastAPI (`app/api/main.py`) + npm-конфігурація `dev` (`app/vue/package.json`) + Compound «app» — запуск обох однією кнопкою.
