# T56 · Дизайн сторінок: профіль студента + студенти (адмін)

`2026-08-04` · 💡 proposal

Контекст:
- ввід Vitalik — [T55](../../.rounds/.t/T55-R--profile-round-readback.md); питання з варіантами — [T60](T60-Q--profile-questions.md);
- історія змін — [T57](T57-B--history-storage.md); Telegram-привʼязка — [T58](../../tgbot/.t/T58-C--tg-link-binding.md);
- будується поверх каркаса [T45](T45-P--app-skeleton.md) (роутер, `user.js`, `api.js`, NavBar).

## Сторінки й маршрути

- `/profile` — профіль студента (доступ: `student`/`admin`; `pending` і анонім — редірект на `/`).
- `/students` — перелік студентів + масове додавання (лише `admin`).
- `/students/:id` — редагування одного студента (лише `admin`): та сама формочка профілю + адмінські поля (статус).
- NavBar: залогіненому — лінк «Профіль»; адміну — ще «Студенти».

## Профіль — одна сторінка, три секції-картки

Одна сторінка (не окремі підсторінки — даних мало), вертикально три Bootstrap-картки; одна форма, одна кнопка «Зберегти» внизу, після збереження — короткий alert «Збережено».

- **ПІБ** — прізвище / імʼя / по батькові; під полями дрібний текст «як у заліковці». Пошта поруч — read-only (з OAuth).
- **GitHub** — поле URL репозиторію + блок-інструкція (стисло, зі старих Notion-інструкцій): приватний; єдиний на всі лаби (без папок Lab1/Lab2); розшарити на `2vitalik` (Settings → Collaborators). Валідація: `https://github.com/<user>/<repo>`.
- **Telegram** — поле «нік» (плейсхолдер `@username`, інструкція де взяти: Telegram → Settings → Username) + кнопка «Привʼязати бота» (deep link з токеном, [T58](../../tgbot/.t/T58-C--tg-link-binding.md)); кнопка зʼявляється лише коли `TG_BOT_NAME` заданий у конфігу; бейдж «✅ привʼязано», коли бот записав `tg_chat_id`.

## Студенти (адмін)

- Таблиця: ПІБ · пошта · група · GitHub (іконка-лінк або «—») · Telegram (`@нік` або «—») · статус. Порожнє — сірим «—», щоб одразу видно, хто чого не вніс.
- Зверху кнопка «Додати студентів» розгортає textarea: вставка TSV-подібного тексту → парсер (пошта за регексом, решта рядка — ПІБ, зайве ігнорується) → створення users зі статусом `student`; підсумок «додано N, пропущено M (вже є)».
- Рядок таблиці → `/students/:id`: та сама `ProfileForm` + селект статусу. Масове інлайн-редагування всіх полів у таблиці — не в v1 (питання в [T60](T60-Q--profile-questions.md)).
- Логіка привʼязки вже є безкоштовно: імпорт створює user з поштою; OAuth-вхід робить upsert по пошті — студент падає у свій створений акаунт.

## API

- `GET /api/me` — розширити повним профілем (+нові поля).
- `PUT /api/profile` — студент редагує своє (whitelist полів: ПІБ, github, tg_username).
- `GET /api/students` · `PUT /api/students/{id}` · `POST /api/students/import` — адмінське; залежність `admin_required` поруч із `current_user` у `deps.py`.
- Кожен PUT: порівняти старі/нові значення → записати дифф в історію ([T57](T57-B--history-storage.md)) → зберегти.

## Модель User — нові поля

- `last_name`, `first_name`, `patronymic` (рядки, порожні за замовчуванням) — окремо від OAuth-івського `name`, який лишається як є.
- `github: str` (v1 — одне поле; список — питання [T60](T60-Q--profile-questions.md) Q2).
- `tg_username: str` · `tg_token: str` (генерується ліниво) · `tg_chat_id: int | None` (запише бот).
- `group: str` (сетиться імпортом; питання [T60](T60-Q--profile-questions.md) Q5).

## Нові файли (орієнтир ≤80 рядків кожен)

- api: `routes/profile.py`, `routes/students.py`, `models/history.py` (+ розширення `models/user.py`, `deps.py`).
- vue: `pages/ProfilePage.vue`, `pages/StudentsPage.vue`, `pages/StudentEditPage.vue`, `components/ProfileForm.vue` (+ маршрути в `router.js`, методи в `api.js`).

## Твої думки та питання

> 
