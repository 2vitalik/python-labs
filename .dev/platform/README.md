# platform — вебсистема: техстек, архітектура, ролі, деплой

Реалізаційний вузол: бекенд, БД, фронтенд, авторизація, ролі, фонові задачі, ШІ-інтеграція, VPS. Обслуговує всі інші вузли.

Шапка:
- Оновлено: 2026-07-25
- Інтегровано: [T40](.t/T40-Q--auth-mvp-questions.md) / [T41](../.rounds/.t/T41-R--auth-mvp-decisions.md) (стек і рамки мікро-MVP)
- Не інтегровано: —

## Стек (затверджено, T40 Q1)

- Бекенд: **FastAPI** (Python, uv) · [T39](.t/T39-B--stack-rethink.md), [T41](../.rounds/.t/T41-R--auth-mvp-decisions.md)
- БД: **MongoDB**; ODM — **Beanie** (обґрунтування · [T42](.t/T42-C--beanie-vs-alternatives.md), чекає фінального ок); дев — локальний mongod (уже є), прод — mongod на VPS **без docker** · [T41](../.rounds/.t/T41-R--auth-mvp-decisions.md)
- Фронт: **Vue 3** SPA (Vite, JS без TS) + **Bootstrap 5**; у проді FastAPI віддає збірку статикою · [T39](.t/T39-B--stack-rethink.md)
- Авторизація: Google OAuth (Authlib), лише @nure.ua — перевірка клейму `hd` на бекенді; `ADMIN_EMAILS` у конфігу; сесія — підписана cookie · [T39](.t/T39-B--stack-rethink.md)
- Знято: рекомендація Django + Postgres і docker-ескіз із [T21](.t/T21-B--tech-stack.md) · [T41](../.rounds/.t/T41-R--auth-mvp-decisions.md)

## Принципи

- Код-стайл: лаконічний, максимально зрозумілий код («ніби писав сам Vitalik») → зафіксувати в `CLAUDE.md` кореня репо · [T38](../.rounds/.t/T38-R--auth-mvp-readback.md)
- Код живе в цьому репо: `app/` (backend + frontend) · [T41](../.rounds/.t/T41-R--auth-mvp-decisions.md)
- Стани користувача з першого дня: анонім → `pending` → `student` / `admin` · [T39](.t/T39-B--stack-rethink.md)

## Не реалізовано

- ⬜ Мікро-MVP «сторінка + вхід» — задача [T44](.t/T44--auth-mvp/plan.md): план готовий, код не стартував.

## Відкладене

- Деплой (VPS без docker: systemd + Caddy, домен, HTTPS, Publish OAuth-апки) — окремим кроком після мікро-MVP · [T40](.t/T40-Q--auth-mvp-questions.md) Q5.

## Відкрите

- Фінальний ок щодо Beanie → [T42](.t/T42-C--beanie-vs-alternatives.md).
- [T22](.t/T22-Q--platform-open-questions.md) Q2–Q5: VPS (що за сервер), ролі поза статусами, ШІ-бюджет, назва/домен.

## Наступний крок

- Vitalik: ок по [T42](.t/T42-C--beanie-vs-alternatives.md) + кроки [T43](.t/T43-C--gcp-oauth-setup.md) (секрети в `.env`) → я кодую [T44](.t/T44--auth-mvp/plan.md).
