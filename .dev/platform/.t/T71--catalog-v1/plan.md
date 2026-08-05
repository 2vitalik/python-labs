# T71 · Каталог v1: реалізація — план

`2026-08-05` · ⚙️ задача

Контекст:
- дизайн — [T68](../T68-P--catalog-v1-design.md); рішення — [T70](../../../.rounds/.t/T70-R--catalog-decisions.md); ідіоми коду — за наявним `app/` (файли ≤80 рядків, `.api()`, `record()`).

## Кроки

- [ ] Бекенд: `zones.py` (константа з `_map.md`), моделі `Game`/`Task` (+`Variant`), роути `games`/`tasks`/`zones` (GET всім активним, POST/PUT адміну, без DELETE), реєстрація в `db.py`/`main.py`.
- [ ] `catalog_io.py`: export/import YAML ↔ Mongo (upsert по slug) + залежність pyyaml.
- [ ] Сид: `data/catalog/games.yaml` (17 ігор з wiki) + `tasks.yaml` (~150 карток із зон, орієнтовні ціни) → import у базу.
- [ ] Фронт: стор `catalog.js`, сторінки `/games` (галерея з чіпами класів), `/games/:slug` (опис + завдання гри), `/tasks` (дерево зон + стрічка з розгортанням + пошук/чіпи, стан у query), адмін-форми `/games/new|:slug/edit`, `/tasks/new|:slug/edit`; компоненти ZoneTree/TaskCard/CoinBadge/GameCard; markdown — `marked`; NavBar-пункти.
- [ ] Смоук: імпорт сиду, GET/POST/PUT через dev-вхід, видимість draft лише адміну, `npm run build`.
- [ ] Доки: README вузлів (platform/tasks/games/grading — інтеграція рішень), CHANGELOG, report.md, STATUS-жест.
