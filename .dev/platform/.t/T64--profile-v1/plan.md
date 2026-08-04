# T64 · Профіль студента v1: сторінки, історія, імпорт — план

`2026-08-04` · ⚙️ задача

Контекст:
- рішення раунду — [T61](../../../.rounds/.t/T61-R--profile-decisions.md); дизайн — [T56](../T56-P--profile-pages-design.md); історія — [T57](../T57-B--history-storage.md) (варіант a, дифф); Telegram — [T58](../../../tgbot/.t/T58-C--tg-link-binding.md);
- CSS — Bootstrap 5 (статус-кво до відповіді на [T63](../T63-Q--css-framework-choice.md)).

## Кроки

api:
- [ ] `models/user.py` — нові поля: ПІБ (3), `group`, `github`, `tg_username`, `tg_token`, `tg_chat_id`
- [ ] `models/history.py` — `Change` (колекція `history`) + `record()` / `record_new()`
- [ ] `db.py` — реєстрація `Change` в Beanie
- [ ] `config.py` + `.env`/`.env.example` — `TG_BOT_NAME=python_nure_bot`
- [ ] `deps.py` — `active_user` (не pending), `admin_user`
- [ ] `routes/auth.py` — префіл ПІБ з `family_name`/`given_name` лише в порожні поля; history на створення юзера
- [ ] `routes/me.py` — повний профіль + `tg_link` (лінива генерація токена) + `tg_linked`
- [ ] `routes/profile.py` — `PUT /api/profile` (whitelist полів, валідація github-URL, дифф в history)
- [ ] `routes/students.py` — `GET /api/students` · `GET/PUT /api/students/{id}` · `POST /api/students/import` (парсер під `data/students/cist.txt`)

vue:
- [ ] `api.js` — універсальні `get`/`send` + методи
- [ ] `router.js` — `/profile`, `/students`, `/students/:id`
- [ ] `components/ProfileForm.vue` — спільна форма (режим підказок для студента, режим адміна з групою/статусом)
- [ ] `pages/ProfilePage.vue` — картки ПІБ/GitHub/Telegram, інструкції, кнопка привʼязки бота
- [ ] `pages/StudentsPage.vue` — таблиця «хто що вніс» + textarea-імпорт
- [ ] `pages/StudentEditPage.vue` — редагування одного студента
- [ ] `NavBar.vue` — лінки «Профіль» (активним) і «Студенти» (адміну)

Перевірка:
- [ ] smoke API: dev-login → `PUT /api/profile` → дифф у колекції `history`; імпорт `cist.txt` → усі студенти файлу в списку, група розпізнана
- [ ] `npm run build` без помилок
