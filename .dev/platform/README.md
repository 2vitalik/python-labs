# platform — вебсистема: техстек, архітектура, ролі, деплой

Реалізаційний вузол: бекенд, БД, фронтенд, авторизація, ролі, фонові задачі, ШІ-інтеграція, VPS. Обслуговує всі інші вузли.

Шапка:
- Оновлено: 2026-07-25
- Інтегровано: [T40](.t/T40-Q--auth-mvp-questions.md) / [T41](../.rounds/.t/T41-R--auth-mvp-decisions.md) (стек і рамки мікро-MVP)
- Не інтегровано: —

## Стек (затверджено, T40 Q1)

- Бекенд: **FastAPI** (Python, uv) · [T39](.t/T39-B--stack-rethink.md), [T41](../.rounds/.t/T41-R--auth-mvp-decisions.md)
- БД: **MongoDB**; ODM — **Beanie** (затверджено, чат 2026-07-25; обґрунтування · [T42](.t/T42-C--beanie-vs-alternatives.md)); дев — локальний mongod (уже є), прод — mongod на VPS **без docker** · [T41](../.rounds/.t/T41-R--auth-mvp-decisions.md)
- Фронт: **Vue 3** SPA (Vite, JS без TS) + **Bootstrap 5**; у проді FastAPI віддає збірку статикою · [T39](.t/T39-B--stack-rethink.md)
- Авторизація: Google OAuth (Authlib), лише @nure.ua — перевірка клейму `hd` на бекенді; `ADMIN_EMAILS` у конфігу; сесія — підписана cookie · [T39](.t/T39-B--stack-rethink.md)
- Знято: рекомендація Django + Postgres і docker-ескіз із [T21](.t/T21-B--tech-stack.md) · [T41](../.rounds/.t/T41-R--auth-mvp-decisions.md)

## Принципи

- Код-стайл: лаконічний, максимально зрозумілий код («ніби писав сам Vitalik») → зафіксувати в `CLAUDE.md` кореня репо · [T38](../.rounds/.t/T38-R--auth-mvp-readback.md)
- Дрібні файли: один файл — одна відповідальність, орієнтир ≤ ~80 рядків; «портянки» розбиваються (чат 2026-07-25) · [T45](.t/T45-P--app-skeleton.md)
- Код живе в цьому репо: `app/` з теками `api/` (FastAPI) і `vue/` (SPA) — імена з чату 2026-07-25 · [T41](../.rounds/.t/T41-R--auth-mvp-decisions.md), [T45](.t/T45-P--app-skeleton.md)
- Стани користувача з першого дня: анонім → `pending` → `student` / `admin` · [T39](.t/T39-B--stack-rethink.md)

## Не реалізовано

- ⬜ Мікро-MVP «сторінка + вхід» — задача [T44](.t/T44--auth-mvp/plan.md): план готовий, детальний каркас файлів — [T45](.t/T45-P--app-skeleton.md) (чекає ок), код не стартував.

## Відкладене

- Деплой (VPS без docker: systemd + Caddy, домен, HTTPS, Publish OAuth-апки) — окремим кроком після мікро-MVP · [T40](.t/T40-Q--auth-mvp-questions.md) Q5.

## Відкрите

- Ок/правки по каркасу [T45](.t/T45-P--app-skeleton.md) і відповіді [T46](.t/T46-Q--pre-code-questions.md) (назва, dev-вхід, PyCharm-версія).
- Секрети Google за [T43](.t/T43-C--gcp-oauth-setup.md) → `app/api/.env` (не блокують код — лише перевірку реального входу).
- [T22](.t/T22-Q--platform-open-questions.md) Q2–Q5: VPS (що за сервер), ролі поза статусами, ШІ-бюджет, назва/домен.

## Наступний крок

- Vitalik: ок/правки [T45](.t/T45-P--app-skeleton.md) + відповіді [T46](.t/T46-Q--pre-code-questions.md) → я кодую [T44](.t/T44--auth-mvp/plan.md) (секрети можуть доїхати пізніше).
