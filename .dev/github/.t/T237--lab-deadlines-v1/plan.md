# T237 · Дедлайни лаб, репозиторії, звіти — код — план

`2026-10-25` · ⚙️ задача · дизайн — [T235](../T235-P--lab-deadlines-design.md) · вибори — [T236](../T236-Q--lab-deadlines-questions.md)

## Кроки

- [ ] Ядро, моделі: `models/deadline.py` (`Deadline`, `LabMark`), `models/repo.py` (`Repo` з журналом комітів, `Review`); у `db.MODELS`.
- [ ] Ядро, логіка: `labs.py` — дедлайн студента (групи, подовження), факти з комітів, стан клітинки; `repos.py` — git: clone/fetch/log (stdlib).
- [ ] Ядро, API: `routes/labs.py` — матриця, дедлайни, позначки, звіти, факти пачкою; `deps.lister` — агент у `GET /api/students`; `app.ROUTERS`.
- [ ] Бот: `bot/due.py` — `/due` з чату зі студентом (тихо), форуму (ефемерно), чату з ботом; вид алерту `due` 📅; реєстрація команди.
- [ ] Скрипт `bin/repos`: `sync` · `pull` · `status` · `push` · `cut` · `reviews`; `.gitignore` — `data/repos/`, `data/reviews/`.
- [ ] Фронт ядра: `labs.js`, `pages/DeadlinesPage.vue`, `components/LabMatrix.vue`, `LabEdit.vue`, `LabReport.vue`, `DeadlineForm.vue`, картка «Лаби» на `StudentEditPage`; `api.js`.
- [ ] Сайт python: маршрут `/deadlines`, пункт меню «Дедлайни».
- [ ] Смоук `tests/smoke_labs.py`: дедлайни по групах, подовження, стани, звіт, факти пачкою, агент у списку студентів, `/due` у трьох місцях.
- [ ] Прогін: усі смоуки, збірка `app/vue` і `sites/ods/vue`; локально — `bin/repos sync -t dev` → `pull` → `push` → матриця в деві.
- [ ] Доки: README вузлів github (інтегрувати й T16), tgbot, grading; `core/README.md`; корінь, CHANGELOG, STATUS.
