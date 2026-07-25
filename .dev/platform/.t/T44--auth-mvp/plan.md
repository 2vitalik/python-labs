# T44 · Мікро-MVP: сторінка + Google OAuth — план

`2026-07-25` · ⚙️ задача

Контекст:
- рішення — [T41](../../../.rounds/.t/T41-R--auth-mvp-decisions.md): FastAPI + MongoDB + Vue 3 + Bootstrap 5; SPA одразу; код у `app/`; поки localhost; mongo локально без docker;
- обґрунтування ODM — [T42](../T42-C--beanie-vs-alternatives.md); секрети Google — Vitalik за [T43](../T43-C--gcp-oauth-setup.md).

## Рамки

- Результат: локальний застосунок — головна-заглушка «це майбутня система; щоб отримати доступ, авторизуйтесь» + вхід через Google лише для @nure.ua; після входу видно свій статус.
- Поза рамками: деплой, реальні розділи системи, ролі понад поле `status`, бот, публічні read-only сторінки (закладаємо лише стани).

## Передумови (Vitalik)

- [ ] ок щодо Beanie ([T42](../T42-C--beanie-vs-alternatives.md))
- [ ] Client ID/secret за [T43](../T43-C--gcp-oauth-setup.md) → `app/backend/.env`
- [ ] локальний mongod працює (вже є)

## Кроки

- [ ] Каркас `app/`: `backend/` (uv + FastAPI) і `frontend/` (Vite + Vue 3 + Bootstrap 5, JS без TypeScript — лаконічність); `CLAUDE.md` кореня репо з код-стайл принципом; `.env.example`
- [ ] Бекенд-основа: `config.py` (pydantic-settings: mongo uri, google client id/secret, session secret, `ADMIN_EMAILS`), підключення Mongo, модель `User` (Beanie: email, name, picture, status, created_at)
- [ ] Auth-роути: `/api/auth/login` → редирект на Google (Authlib) · `/api/auth/callback` → перевірка `email_verified` + клейму `hd == nure.ua` (або email в `ADMIN_EMAILS`) → upsert User → сесія в підписаній cookie · `/api/auth/logout` · `/api/me`
- [ ] Стани: після першого входу — `pending`; `admin` — за `ADMIN_EMAILS`; `student` — призначатиме викладач (поки лише поле). Не-nure.ua — чемна відмова «вхід лише з поштою @nure.ua»
- [ ] Фронт: navbar (назва + «Увійти» / аватар + «Вийти»), Home: заглушка для анонімів; для залогінених — імʼя і статус («доступ надає викладач» для pending)
- [ ] Дев-запуск: `uvicorn --reload` (8000) + `vite dev` (5173, proxy `/api`); коротка інструкція запуску в `app/README.md`
- [ ] Перевірка: вхід з @nure.ua ок · сторонній gmail — відмова · сесія переживає рефреш сторінки й рестарт бекенда · logout працює

## Нотатки

- Порти 8000/5173 і шлях `/api/auth/callback` зафіксовані в redirect URIs GCP ([T43](../T43-C--gcp-oauth-setup.md)) — міняти лише синхронно.
- Поки OAuth-апка в режимі Testing, входять лише додані тест-користувачі — додай себе (@nure.ua).
