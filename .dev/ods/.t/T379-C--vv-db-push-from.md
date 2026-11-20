# T379 · vv db push --from відновлює 0 документів: URI з базою фільтрує архів; обхід — локальна копія ods_labs

`2026-11-19` · 🔆 clarification

Контекст: 2026-11-20 Vitalik запустив команду з [T377](T377-C--ods-db-push.md) — `vv db push ods-labs vv3 --from ods_seed --drop`; на сервері «досі пусто». Цей тікет виправляє T377: **команда з `--from` там не працює**, решта T377 чинна.

**Коротко.** `vv db push --from` відновлює 0 документів щоразу, коли локальна база зветься не так, як серверна. База сервера при цьому не змінюється. Обхід без правки `vv` — локальна копія з імʼям серверної й push без `--from`:

```sh
vv db push ods-labs vv3 --drop                    # локальна ods_labs → серверна ods_labs
ssh -t vv3 sudo systemctl restart ods-labs-web    # індекси повертає старт API
```

---

## 1. Що сталось

Вивід сервера: `The --db and --collection flags are deprecated…`, далі `0 document(s) restored successfully`, колекцій до й після — 34.

- `MONGO_URI` у `shared/env` — `mongodb://ods_labs:…@127.0.0.1:27017/ods_labs` (`vps-infra/vv/lib/vv/db.py:117`): база в шляху.
- `mongorestore` бере базу з URI як `--db ods_labs`, тобто як фільтр «з архіву лише `ods_labs.*»`.
- В архіві — `ods_seed.*`. Фільтр діє до `--nsFrom/--nsTo`, тож не проходить нічого; `--drop` нічого не стирає.
- 34 колекції на сервері — порожні колекції моделей, створені стартом API (локально моделей теж 34).

## 2. Відтворено локально

`mongorestore` 100.16.1, архів `ods_seed` (595 документів, 9.1 МБ), URI з базою в шляху — як у `vv db restore`:

| Виклик | Відновлено |
|:--|:--|
| `--nsFrom=ods_seed.* --nsTo=<ціль>.*`, імена різні — як робить `vv` | 0 |
| те саме + `--nsInclude=ods_seed.*` | 595 |
| імена збігаються (`ods_labs` → `ods_labs`), без `--from` | 595 |

Скретч-базу `ods_t377_restore_smoke` після проби видалено.

## 3. Обхід: копія зветься як серверна

Локальна `ods_labs` створена 2026-11-20 копією `ods_seed`: `guide 47 · media 158 · lab_pages 27 · lab_shapes 5 · variants 310 · users 48`. Оновити її перед наступним push — рецепт [T372](T372--ods-roster/report.md) з `seed = "ods_labs"`. Локальний дев-сайт працює з `ods`, базу `ods_labs` не читає.

## 4. Лагодження `vv` — не застосовано

`vps-infra/vv/lib/vv/dbpush.py:107`, виклик `mongorestore` у `cmd_db_restore`:

```diff
-            f"--nsFrom={source}.*", f"--nsTo={name}.*", *(["--drop"] if a.drop else []))
+            f"--nsInclude={source}.*", f"--nsFrom={source}.*", f"--nsTo={name}.*", *(["--drop"] if a.drop else []))
```

Чужий репозиторій, і `vv` на сервері треба оновити (`restore` виконується там) — за словом Vitalik-а.

## Не перевірено

- Сам push на сервер: запускає Vitalik. Версія `mongorestore` на сервері може бути іншою, ніж 100.16.1; текст попередження збігається.
- Назва юніта `ods-labs-web` — з маніфесту `apps/ods-labs/units/ods-labs-web.conf`, не з машини.

## Твої думки та питання

> 
