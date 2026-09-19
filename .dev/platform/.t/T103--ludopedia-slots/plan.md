# T103 · Лудопедія: слоти параметрів (E2) + топ-20 (E4) — план

`2026-08-19` · ⚙️ задача · дизайн — [T96](../T96-P--entities-slots-model.md) §2 і §4; запит Vitalik з чату («рухаємось далі, E2 та E4»)

Рівень 1 драбини: картка каталогу отримує **слоти параметрів**, заявка — **значення** в них; «Спавн за розкладом · Кожні 20 тіків · Макс. на полі 4» читається з чіпа заявки. Плюс сид слотів на топ-20 карток через YAML-канал.

## Бекенд

- `Task.slots: list[dict]` — спека слота `{key, label, type: int|choice|bool|text, options?, unit?, required?}` (T96 §2 дослівно); порожньо = картка рівня 0, таких більшість — назавжди. Віддається в `api()` і в `task_index` паспорта.
- `Claim.params: dict` — значення `{key: value}`; валідація по слотах картки в `my_claims.py` (обовʼязкові присутні, типи збігаються, choice зі списку options, невідомий ключ — 422); редагується разом з нотаткою/лінком.
- YAML-канал: dict-fallback картки в `tasks.yaml` тепер і при непорожніх `slots` (не лише при багаторядковому описі); `taskline.py` не чіпаємо (T96).
- Адмін-форма картки слоти **не** редагує — канал слотів v1 це YAML (`tasks.yaml` → `catalog_io.py import`); `TaskIn` без `slots`, тож PUT з форми їх не затирає.

## Сид E4 — слоти на ~20 карток

Розкид по підзонах entities/game-logic/levels; типи: майже всюди `int` + `unit`, для розмаїття — `choice` (maze-generation: dfs/prim), `bool` (enemy-waves: фінальна хвиля), `text` (pattern-automaton: цикл ходів). Список: spawn-schedule (кожні + макс) · blast-wave (радіус) · hp-damage (hp + кого) · shoot-cooldown · shoot-burst · shoot-spread · chain-detonation · timed-despawn · respawn · temporary-modes · inventory-limit · inventory-duration · player-death (життя) · time-out (ліміт) · collect-quota · enemy-waves · move-timer · maze-generation · ai-minimax · pattern-automaton.

Канал: `export` (звірка бази з YAML) → правка `tasks.yaml` → `import` → `export` (канонізація dict-нод) — roundtrip ловить помилки руками.

## Фронт

- `SlotFields.vue` — інпути по спеці слотів (число/селект/чекбокс/текст), один компонент на створення і редагування.
- `ClaimPicker`: картка зі слотами не заявляється одним кліком — розгортає міні-форму параметрів; emit стає `pick(slug, params)` (WindowCard/EntityCard/MyGamePage оновити).
- `ClaimRow`: параметри в чіпі текстом (`paramsText` у catalog.js) + редагування в розгорнутій формі.
- Паспорт (`StudentGamePage`): текст параметрів у read-only чіпах усіх трьох секцій.
- `TaskCard`: рядок «⚙️ параметри» у розгорнутій картці — видно, що картка рівня 1.

## Перевірка

Смоук: +~9 перевірок (створення з params, обовʼязковий відсутній, не той тип, невідомий ключ, редагування, params+slots у паспорті; адміном — choice поза options / ок, bool). `npm run build`.

Поза скоупом: Д3 «приклади на картках» — після пояснення [T104](../../games/.t/T104-C--ludopedia-d3-d6.md) і «ок» Vitalik.
