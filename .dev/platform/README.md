# platform — вебсистема: техстек, архітектура, ролі, деплой

Реалізаційний вузол: бекенд, БД, фронтенд, авторизація, ролі, фонові задачі, ШІ-інтеграція, VPS. Обслуговує всі інші вузли.

Шапка:
- Оновлено: 2026-08-10
- Інтегровано: [T81](.t/T81-C--dev-ports.md) (порти дев-серверів), [T40](.t/T40-Q--auth-mvp-questions.md) / [T41](../.rounds/.t/T41-R--auth-mvp-decisions.md) (стек і рамки), [T45](.t/T45-P--app-skeleton.md) (каркас), [T46](.t/T46-Q--pre-code-questions.md) (назва, dev-вхід, PyCharm Pro), [T44](.t/T44--auth-mvp/report.md) (auth-реалізація), [T56](.t/T56-P--profile-pages-design.md)/[T57](.t/T57-B--history-storage.md)/[T59](.t/T59-C--data-model-sketch.md) + рішення [T60](.t/T60-Q--profile-questions.md)/[T61](../.rounds/.t/T61-R--profile-decisions.md) (профіль v1), [T64](.t/T64--profile-v1/report.md) (реалізація профілю), [T66](.t/T66-B--catalog-storage.md)/[T67](.t/T67-B--catalog-ui.md)/[T68](.t/T68-P--catalog-v1-design.md) + рішення [T69](.t/T69-Q--catalog-v1-questions.md)/[T70](../.rounds/.t/T70-R--catalog-decisions.md) (каталог v1), [T71](.t/T71--catalog-v1/report.md) (реалізація каталогу), [T72](.t/T72-B--catalog-columns.md)/[T75](.t/T75-C--masonry-layouts.md) (розкладка стрічки), відповіді [T74](.t/T74-Q--catalog-visuals.md)/[T78](.t/T78-Q--catalog-ui2.md) (монетки, зони, YAML v2 — [T77](.t/T77-P--yaml-tree-format.md)+правки), [T79](.t/T79-C--family-v2.md) (сімʼї батько-діти)
- Не інтегровано: [T80](.t/T80-B--colors-plan.md) (кольори v2 — пропозиція П1 на `/colors2`, чекає вибору)

## Реалізовано

- ✅ Мікро-MVP «сторінка + вхід» — працює: `app/api/` (FastAPI + Beanie + Authlib) + `app/vue/` (Vue 3 + Bootstrap 5); **реальний Google-вхід підтверджено Vitalik-ом 2026-07-26**; `prompt=select_account` — вибір акаунта щоразу (спільні лаб-компи) · [T44](.t/T44--auth-mvp/report.md)
- Робоча назва UI — «Python Labs» ([T46](.t/T46-Q--pre-code-questions.md) Q1; фінальна — T22 Q5); dev-вхід через `FAKE_USER_EMAIL` (кнопка лише в dev-режимі Vite) · [T46](.t/T46-Q--pre-code-questions.md) Q2
- Запуск: `app/README.md` (uv + npm); PyCharm Pro покроково — [T47](.t/T47-C--pycharm-setup.md); працювати завжди через http://localhost:5030
- **Порти дев-серверів** (2026-08-10, [T81](.t/T81-C--dev-ports.md)): python-labs = №3 у крос-проєктній схемі (формула й реєстр — `dev-md-rules/DEV.md`) → API **8030** (`fastapi dev --port 8030`), фронт **5030** (`strictPort: true`, proxy → 8030); порти в T47 застарілі — чинні тут
- ✅ **Профіль v1** (2026-08-04, [T64](.t/T64--profile-v1/report.md)): `/profile` — картки ПІБ/GitHub/Telegram з інструкціями (приватний єдиний репо → розшарити на `2vitalik`) і кнопкою «Привʼязати бота»; `/students` (адмін) — таблиця «хто що вніс» + textarea-імпорт формату ЦІСТ (`data/students/cist.txt`); `/students/:id` — та сама форма + група/статус · рішення [T60](.t/T60-Q--profile-questions.md)/[T61](../.rounds/.t/T61-R--profile-decisions.md)
- Імпорт (фікс 2026-08-04): багатогруповий — шапки «Список групи …» перемикають поточну групу; повторний імпорт **оновлює** наявних по пошті (група — завжди, ПІБ — лише в порожні поля: самоперейменування студента важливіше за ЦІСТ), внесене в профілі не чіпається; звіт «додано/оновлено/без змін»
- ✅ **Каталог v1** (2026-08-05, [T71](.t/T71--catalog-v1/report.md)): `/games` — галерея з чіпами класів; `/games/:slug` — осі бейджами, markdown-опис, «Завдання гри»; `/tasks` — дерево зон з лічильниками + стрічка карток з розгортанням + пошук/чіпи (стан у query-URL → шерні лінки); адмін-форми create/edit для ігор і завдань; сид з wiki: **17 ігор + 162 завдання** (7 сімей, 16 золотих); export/import YAML-знімка `data/catalog/` — `catalog_io.py` · рішення [T70](../.rounds/.t/T70-R--catalog-decisions.md)
- **UI-ітерація каталогу** (2026-08-05, чат): `/tasks` — верхня дворядкова навігація зон/підзон замість лівого дерева, стрічка колонками на всю ширину ([T72](.t/T72-B--catalog-columns.md)); іконки зон/підзон + кольори зон у `zones.py`; сімʼї-«стопки» ([T73](../tasks/.t/T73-C--task-families.md)), чернетки приглушені
- **UI-ітерація 2** (2026-08-06, відповіді T74 + чат): masonry-розкладка без залежностей ([T75](.t/T75-C--masonry-layouts.md)); монетки 👑🥇🥈🥉📎🌱 (корона замість «золото×2»); відтінки підзон — сусідні хʼю; **гостьовий перегляд** `/games`+`/tasks` (GET публічні, лише active); сторінка гри — той самий каталог (`TaskCatalog.vue`), фільтр «🌍 Універсальні»; «＋» нового завдання в шапці підзони з префілом; майстерня кольорів `/colors`
- **Сімʼї v2 + YAML v2** (2026-08-06, [T79](.t/T79-C--family-v2.md)): `Task.parent` замість `variants` — діти = повноцінні завдання (опис/статус/history/✏️), UI рекурсивний, сімʼя в шапці — сірий ×N + діапазон «📎‥🥇»; `tasks.yaml` — дерево з рядками `🥉 Назва [ігри] ⭐ ✍️ — опис` (`taskline.py`, позиція = order, `children:`), раундтрип чистий; **активовано 74 впевнені картки** — каталог для гостей уже живий; пропозиція кольорів — `/colors2` ([T80](.t/T80-B--colors-plan.md))

## Дані

- `users`: ПІБ трьома полями (префіл з Google-клеймів лише в порожні), `group` рядком, `github` — одне поле-URL (старі значення видно в історії), `tg_username` + `tg_token`/`tg_chat_id` (механіка привʼязки — [T58](../tgbot/.t/T58-C--tg-link-binding.md)) · [T61](../.rounds/.t/T61-R--profile-decisions.md)
- **Історія змін** — одна глобальна колекція `history` з диффами `{coll, doc_id, actor, at, {поле: old→new}}` ([T57](.t/T57-B--history-storage.md), варіант a): `record()` у PUT-роутах + `record_new()` при створенні; покриває всі майбутні колекції тим самим хелпером; сторінка перегляду — потім
- `games` + `tasks` — каталог ([T68](.t/T68-P--catalog-v1-design.md) + [T79](.t/T79-C--family-v2.md)): дім зона/підзона (константа `zones.py` — дзеркало `data/wiki/tasks/_map.md`), теги (`algo` = ⭐), застосовність `games` ([] = універсальне), ціна `coin`+`amount` (довідково до рішень grading), `max_count` (1 / N / 0=∞), `parent` (сімʼї батько-діти, 1 рівень), статуси draft/active/archived (draft бачить лише адмін, DELETE нема); правки — через `record()`; знімок — `data/catalog/` (games плоско, tasks — дерево рядків `taskline.py`)
- Ескіз майбутніх колекцій (reports, defenses, remarks, coins-журнал, surveys…) — [T59](.t/T59-C--data-model-sketch.md); зараз існують `users` + `history` + `games` + `tasks`

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

- [T80](.t/T80-B--colors-plan.md): вибір палітри — П1 на `/colors2` (або правки кодами); потім застосувати в `zones.py`.
- Іконки підзон — точкові правки за Vitalik (T74 Q4 → T78 Q5, поки без відповіді).
- Кнопка «＋ у звіт» на картці — дизайн ок (T78 Q4a), реалізація у черзі звітів ([T10](../reports/.t/T10-Q--reports-open-questions.md)).
- [T22](.t/T22-Q--platform-open-questions.md) Q2–Q5: VPS (що за сервер), ролі поза статусами, ШІ-бюджет, назва/домен.
- ~~[T63](.t/T63-Q--css-framework-choice.md) CSS-фреймворк~~ — вирішено в чаті 2026-08-04 після порівняння [T62](.t/T62-C--css-frameworks.md): **лишаємось на Bootstrap 5**.

## Наступний крок

- Vitalik: додати в GCP нові redirect URI (`http://localhost:5030/api/auth/callback` + `http://localhost:8030/...`) — кроки в [T81](.t/T81-C--dev-ports.md); без цього Google-вхід у деві на нових портах не працюватиме (dev-вхід не залежить). Заодно — `--port 8030` у PyCharm-конфігурації FastAPI.
- Vitalik: повторний імпорт `cist.txt` на живій базі (розкладе всіх по правильних групах); хвости — у [T64](.t/T64--profile-v1/report.md).
- Каталог v1 (2026-08-05, [T71](.t/T71--catalog-v1/report.md)) + три ітерації (2026-08-06: masonry, корона, гостьовий доступ, сімʼї v2, YAML v2, 74 активні); Vitalik: клік-тест http://localhost:5030/tasks + вибір палітри на `/colors2` ([T80](.t/T80-B--colors-plan.md)) + ревізія решти чернеток (111 draft) — тепер зручно пачкою в `data/catalog/tasks.yaml` (прибрати ✍️ = активувати) + import.
- Далі за [T25](../.t/T25-B--mvp-strategy.md): кабінет студента — вибір завдань і заявки ([reports](../reports/README.md), чекає рішень [T10](../reports/.t/T10-Q--reports-open-questions.md)).
