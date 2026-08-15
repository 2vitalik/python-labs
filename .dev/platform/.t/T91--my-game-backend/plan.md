# T91 · Бекенд «Моєї гри» v1: Work, обʼєкти, заявки, скриншоти

`2026-08-16` · ⚙️ задача · етап B пілота ([T87](../../../.rounds/.t/T87-R--game-round-decisions.md))

Контекст:
- дизайн — [T90](../T90-P--my-game-v1-design.md); рішення — [T84](../../../reports/.t/T84-Q--game-objects-questions.md)/[T89](../T89-Q--my-game-questions.md).

## Кроки

- [ ] `models/work.py`: Work, WorkObject, Claim (+ api()); реєстрація в `db.py`.
- [ ] `models/history.py`: `record_delete`.
- [ ] `uploads.py`: корінь тек аплоадів (налаштовується env), хелпери збереження/видалення.
- [ ] Роути: `works.py` (галерея, my, паспорт) · `work_objects.py` (CRUD + скриншоти) · `work_claims.py` (CRUD з дедупом).
- [ ] `main.py`: роутери + StaticFiles `/api/uploads`; `.gitignore`: `app/api/uploads/`.
- [ ] Смоук: тест-база `python_labs_smoke` (сид каталогу import-ом), TestClient-сценарій студент/адмін — створення, валідації, аплоад, каскадне видалення, 409-и.
- [ ] report.md + README вузлів (platform, reports) + CHANGELOG.
