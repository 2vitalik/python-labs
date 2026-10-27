# T242 · Таблиця студентів v1: API, сторінка, свої поля, дедлайн 1 — план

`2026-10-26` · ⚙️ задача · дизайн — [T240](../T240-P--table-views.md) · питання — [T241](../T241-Q--table-views-questions.md)

## Кроки

- [x] Ядро, моделі: `models/field.py` (`Field`, `FieldValue`), `models/view.py` (`View`); `LabMark.asked`; у `db.MODELS`.
- [x] Ядро, логіка: `table.py` — рядки `GET /api/table` з профілю, `labs.Index`, `Repo`, голосів (`polls_read.latest`), своїх полів, `students.EXTRAS`; `fields.py` — перевірка значення за типом, slug/транслітерація.
- [x] Ядро, API: `routes/table.py`, `routes/fields.py`, `routes/views.py`; `MarkIn.asked` + рядок алерту; опитування (`GET` список, результати, таблиця) — і агентові (`editor_user`); `app.ROUTERS`.
- [x] Фронт ядра: `table.js` (реєстр колонок, типи, фільтри, сортування, групування, стан у URL, вбудовані види), `pages/TablePage.vue`, `components/Table*.vue` (таблиця, клітинка, колонки, фільтр, види, поля, редактор значення); `api.js`.
- [x] `/deadlines`: назва лаби → `/table?view=labN`; сайт python: маршрут `/table`, пункт меню «Таблиця»; `site.table.cols` (гра, заявки, монетки).
- [x] Смоук `tests/smoke_table.py`: рядок таблиці з усіх джерел, поля всіх типів і scope, перевірка значень, види, 🙋 з алертом, агент читає опитування; прогін решти смоуків; збірки `app/vue`, `sites/ods/vue`.
- [x] Клік-тест у деві через Chrome: вид «Лаба 1», колонки, фільтри, групування, своє поле, збережений вид.
- [x] Факти з проду: `bin/repos sync → pull → push` (T241 Q4); вибірка звітів (Q5) — якщо є дата дедлайну.
- [x] Доки: README platform і github, `core/README.md`, корінь, CHANGELOG, STATUS; звіт `report.md`.
