# platform — вебсистема: техстек, архітектура, ролі, деплой

Реалізаційний вузол: бекенд, БД, фронтенд, авторизація, ролі, фонові задачі, ШІ-інтеграція, VPS. Обслуговує всі інші вузли.

Шапка:
- Оновлено: 2026-07-26
- Інтегровано: [T40](.t/T40-Q--auth-mvp-questions.md) / [T41](../.rounds/.t/T41-R--auth-mvp-decisions.md) (стек і рамки), [T45](.t/T45-P--app-skeleton.md) (каркас), [T46](.t/T46-Q--pre-code-questions.md) (назва, dev-вхід, PyCharm Pro), [T44](.t/T44--auth-mvp/report.md) (реалізація)
- Не інтегровано: —

## Реалізовано

- ✅ Мікро-MVP «сторінка + вхід» — код готовий і працює локально: `app/api/` (FastAPI + Beanie + Authlib) + `app/vue/` (Vue 3 + Bootstrap 5); dev-цикл перевірено · [T44](.t/T44--auth-mvp/report.md)
- Робоча назва UI — «Python Labs» ([T46](.t/T46-Q--pre-code-questions.md) Q1; фінальна — T22 Q5); dev-вхід через `FAKE_USER_EMAIL` (кнопка лише в dev-режимі Vite) · [T46](.t/T46-Q--pre-code-questions.md) Q2
- Запуск: `app/README.md` (uv + npm); PyCharm Pro покроково — [T47](.t/T47-C--pycharm-setup.md); працювати завжди через http://localhost:5173

## Стек (затверджено, T40 Q1)

- Бекенд: **FastAPI** (Python, uv) · [T39](.t/T39-B--stack-rethink.md), [T41](../.rounds/.t/T41-R--auth-mvp-decisions.md)
- БД: **MongoDB**, база `python_labs` (підкреслення замість дефіса — mongo-конвенція, чат 2026-07-26); ODM — **Beanie** (затверджено, чат 2026-07-25; обґрунтування · [T42](.t/T42-C--beanie-vs-alternatives.md)); дев — локальний mongod (уже є), прод — mongod на VPS **без docker** · [T41](../.rounds/.t/T41-R--auth-mvp-decisions.md)
- Фронт: **Vue 3** SPA (Vite, JS без TS) + **Bootstrap 5**; у проді FastAPI віддає збірку статикою · [T39](.t/T39-B--stack-rethink.md)
- Авторизація: Google OAuth (Authlib), лише @nure.ua — перевірка клейму `hd` на бекенді; `ADMIN_EMAILS` у конфігу; сесія — підписана cookie · [T39](.t/T39-B--stack-rethink.md)
- Знято: рекомендація Django + Postgres і docker-ескіз із [T21](.t/T21-B--tech-stack.md) · [T41](../.rounds/.t/T41-R--auth-mvp-decisions.md)

## Принципи

- Код-стайл: лаконічний, максимально зрозумілий код («ніби писав сам Vitalik») → зафіксувати в `CLAUDE.md` кореня репо · [T38](../.rounds/.t/T38-R--auth-mvp-readback.md)
- Дрібні файли: один файл — одна відповідальність, орієнтир ≤ ~80 рядків; «портянки» розбиваються (чат 2026-07-25) · [T45](.t/T45-P--app-skeleton.md)
- Код живе в цьому репо: `app/` з теками `api/` (FastAPI) і `vue/` (SPA) — імена з чату 2026-07-25 · [T41](../.rounds/.t/T41-R--auth-mvp-decisions.md), [T45](.t/T45-P--app-skeleton.md)
- Стани користувача з першого дня: анонім → `pending` → `student` / `admin` · [T39](.t/T39-B--stack-rethink.md)

## Відкладене

- Деплой (VPS без docker: systemd + Caddy, домен, HTTPS, Publish OAuth-апки, віддача `dist/` статикою) — окремим кроком після мікро-MVP · [T40](.t/T40-Q--auth-mvp-questions.md) Q5.
- ~~Виключення `.venv`/`node_modules` із синку Dropbox~~ — знято: Vitalik свідомо синхронізує все (чат 2026-07-26).

## Відкрите

- Реальний Google-вхід не перевірений: чекає кредів у `app/api/.env` за [T43](.t/T43-C--gcp-oauth-setup.md).
- [T22](.t/T22-Q--platform-open-questions.md) Q2–Q5: VPS (що за сервер), ролі поза статусами, ШІ-бюджет, назва/домен.

## Наступний крок

- Vitalik вписує `GOOGLE_CLIENT_ID`/`GOOGLE_CLIENT_SECRET`/`ADMIN_EMAILS` у `app/api/.env` → перевірка справжнього входу @nure.ua; далі — черга 1 за [T25](../.t/T25-B--mvp-strategy.md).
