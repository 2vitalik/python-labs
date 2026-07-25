# T44 · Мікро-MVP: сторінка + Google OAuth — звіт

`2026-07-26` · ⚙️ звіт

## Зроблено

- Каркас за [T45](../T45-P--app-skeleton.md): `app/api/` — FastAPI + Beanie + Authlib (9 файлів, найбільший ~65 рядків); `app/vue/` — Vue 3 + vue-router + Bootstrap 5 на Vite (10 файлів). Корінь: `CLAUDE.md` (правила код-стайлу), `app/README.md` (запуск), `.gitignore` доповнено (`.env`, `.venv`, `node_modules`, `dist`).
- Рішення [T46](../T46-Q--pre-code-questions.md) враховано: назва «Python Labs»; dev-вхід — `FAKE_USER_EMAIL` у `.env` + кнопка «Dev-вхід», видима лише в dev-режимі Vite; PyCharm Pro-конфіги описані в `app/README.md`.
- `app/api/.env` створено локально: `SESSION_SECRET` згенеровано, `FAKE_USER_EMAIL=dev@nure.ua`; Google-поля порожні — впише Vitalik.

## Перевірено

- Бекенд-цикл: `/api/me` анонімно → `null` · dev-вхід → юзер у Mongo (`status=pending`) · `/api/me` віддає його · logout чистить сесію · `/api/auth/login` → 302 на Google.
- Фронт: `npm run build` збирається; Vite dev (:5173) віддає сторінку, proxy `/api` → бекенд працює.

## Хвости

- **Реальний Google-вхід не перевірений** — чекає кредів у `app/api/.env` (крок Vitalik за [T43](../T43-C--gcp-oauth-setup.md)).
- Порт 8000 на IPv6 зайнятий Docker Desktop («404 page not found» при зверненні на `localhost:8000`) → у vite-proxy і перевірках всюди явний `127.0.0.1`; на роботу системи не впливає.
- `.venv`/`node_modules` живуть у Dropbox: шум синку і зайві релоади watchfiles — варто виключити ці теки з синку Dropbox (рішення за Vitalik).
- Прод-режим (FastAPI віддає `dist/` статикою) — свідомо відкладено до деплою.
