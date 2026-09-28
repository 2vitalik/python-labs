# data/catalog — git-знімок каталогу ігор і завдань

**Джерело правди — MongoDB** (колекції `games`, `tasks`); ці YAML — знімок для diff-ревізії, бекапу і масових правок (рішення: `.dev/platform/.t/T66-B--catalog-storage.md`, T69 Q1c).

- `games.yaml` · `tasks.yaml` — по одному запису на картку; порожні поля опущені.
- Обмін: з `app/api/` — `uv run python catalog_io.py export` (Mongo → YAML) та `... import` (YAML → Mongo, upsert по `slug`).
- **З 2026-09-28 знімок у git — із сервера** ([T155](../../.dev/platform/.t/T155--agent-catalog-snapshot/report.md)): `bin/catalog snap` пише сюди каталог із сайту (той самий формат, YAML віддає `GET /api/catalog/snapshot`); після правки агента на сервері це робиться само. Локальний `export` — для дев-бази, його результат не комітимо.
- Сид = перший import; далі оперативні правки — веб-адмінка, пачкові — правка YAML + import.
- Зони/підзони — константа `app/api/zones.py` (дзеркало `data/wiki/tasks/_map.md`); нові ключі спершу туди.
