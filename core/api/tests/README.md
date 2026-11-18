# Смоуки платформи

Те, що перевіряє лише ядро: вхід, «очима студента», бот і алерти, активність, помилки, методичка, опитування, тиждень, лаби й дедлайни, таблиця й види, заняття. Кожен файл запускається з теки `api` будь-якого сайту й проходить на обох: бере `main` і `db` того сайту, з якого запущений. Смоуки ігор, каталогу, захистів і ШІ — у `app/api/tests/`, ods — у `sites/ods/api/tests/`. Частину сайту в смоуку, що сам по собі платформний, сайт тримає поруч під тією ж назвою (python: `smoke_views`, `smoke_events`, `smoke_lesson_days`, `smoke_agent`).

## Запуск

База — лише з `_smoke` у кінці назви: смоук її стирає. Без `uv run`: він пересинхронізує venv, спільний із дев-серверами.

```sh
# python
cd app/api && DB_NAME=python_labs_<назва>_smoke SESSION_SECRET=x UPLOADS_DIR="$TMPDIR/smoke-up" ~/.venvs/python-labs/bin/python ../../core/api/tests/smoke_<назва>.py
# ods
cd sites/ods/api && DB_NAME=ods_<назва>_smoke SESSION_SECRET=x ~/.venvs/python-labs/bin/python ../../../core/api/tests/smoke_<назва>.py
```

Усі для одного сайту — з його теки `api`:

```sh
P=python_labs T=../../core/api/tests  # ods: P=ods T=../../../core/api/tests
for f in $T/smoke_*.py; do n=$(basename $f .py); printf '%s · ' $n
  DB_NAME=${P}_${n#smoke_}_smoke SESSION_SECRET=x UPLOADS_DIR=$TMPDIR/smoke-up ~/.venvs/python-labs/bin/python $f | tail -1; done
```

## Правило

Платформний смоук ставить потрібні йому налаштування сам і не спирається на файли сайту. Налаштування — `core.config.settings` на початку файла (`admin_emails`, `tg_bot_token`, `labs`, `guide_readers`, `week_hours` …), а не `site.env` чи `.env` якогось сайту. Дані — свої: сторінки методички в тимчасовій теці (`guide_io.ROOT`), колонки видів `/table` — з `views_seed.seeds()` під час прогону, види алертів — ядра. Що є лише в одному сайті — у смоуку того сайту.
