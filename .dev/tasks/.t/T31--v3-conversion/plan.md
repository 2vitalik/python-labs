# T31 · Конвертація даних v2 → v3 (єдина CSV-схема) — план

`2026-07-19` · ⚙️ задача

Контекст:
- Схема — [T27](../T27-P--v3-csv-schema.md), рішення — [T28](../T28-Q--v3-csv-questions.md) (все «a»), аномалії виправлено руками у v2 — [T29](../T29-C--v2-data-anomalies.md)/[T30](../T30-Q--v3-anomaly-fixes.md) зняті.

Кроки:

- [ ] `data/scripts/convert_coda.py` — 10 v2-CSV → 7 файлів `data/v3/coda/pzpi-YY.csv` (15 колонок, props влиті після tasks, значення verbatim)
- [ ] `data/scripts/convert_notion.py` — `games/tasks.md` + `games/algo.md` → `data/v3/notion/{tasks,algo}.csv` (та сама схема; lead-in групи → `subcategory`, вкладені пункти → description через `\n`)
- [ ] `data/scripts/check.py` — зворотна перевірка: Coda — проєкція v3 назад у формат v2 і порівняння значень рядок-у-рядок; Notion — флеттен CSV проти флеттену md
- [ ] прогін конвертації + чистий звіт check.py
- [ ] report.md + README вузла
