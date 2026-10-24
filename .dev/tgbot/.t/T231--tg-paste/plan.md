# T231 · Імпорт листування з Telegram вставкою тексту — код — план

`2026-10-24` · ⚙️ задача · звіт — `report.md` (на завершенні)

Контекст:
- дизайн і «чому» — [T230](../T230-P--tg-paste-import.md): читати першим, тут — лише «що зробити»;
- запит Vitalik (чат, 2026-10-24): «ок, заводь тікет і роби вставку тексту».

## Рамки

- Усе в `core/` (бекенд `core/api/core/…`, фронт `core/ui/…`); сайти лише успадковують маршрут і картку.
- Правила `CLAUDE.md`: файл ≤ ~80 рядків, коментарі лише «чому», UI — UA, код — EN; наявні компоненти й стиль форм.
- Живі рядки бота й стрічка `/activity` поводяться як раніше; смоуки `smoke_log`, `smoke_activity`, `smoke_import` лишаються зеленими.

## Кроки

- [ ] `core/api/core/tg_paste.py`: `parse_paste(text) → (rows, errors)` — шапка `Імʼя, [дата]`, текст до наступної шапки; `when()` — терпимий розбір дати в зоні `TZ`; `guess(authors, student, admin)` — хто студент.
- [ ] `core/api/core/models/message.py`: поле `about` (пошта студента на імпортованих рядках), `kind=import` у коментарі.
- [ ] `core/api/core/routes/student_messages.py`: `POST /api/students/{nick}/messages` — без `student` → огляд (автори, здогад, помилки); з `student` → запис як бізнес-рядки з дедуплікацією `(хвилина, текст)`; реєстрація в `core/app.py`.
- [ ] `core/api/core/activity_feed.py`: стрічка студента бере й рядки з `about`.
- [ ] `core/ui/components/TgPaste.vue` — картка «Telegram: вставити листування» (textarea → «Розібрати» → перемикач студента → «Імпортувати» → підсумок); `core/ui/api.js` — `importMessages`; `StudentEditPage.vue` — картка під формою; `activity.js` — бейдж `import`.
- [ ] `app/api/tests/smoke_tg_paste.py`: формати дат, багаторядкові тексти, помилкова шапка, здогад студента, запис, дублі з повторної вставки і з живим рядком, стрічка студента показує обидві сторони.
- [ ] `ruff`, збірка `app/vue` і `sites/ods/vue`, старі смоуки; README вузла, CHANGELOG, STATUS-жест, коміт-меседж.
