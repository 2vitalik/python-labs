# T103 · Лудопедія: слоти параметрів (E2) + топ-20 (E4) — звіт

`2026-08-19` · ⚙️ задача · план — [plan.md](plan.md); пояснення Д3–Д6 — [T104](../../games/.t/T104-C--ludopedia-d3-d6.md)

Зроблено все за планом; смоук **70/70 PASS** (+10 перевірок), `npm run build` зелений.

## Бекенд

- `Task.slots` (спека `{key, label, type, options?, unit?, required?}`) — в `api()` і в `task_index` паспорта; `Claim.params` — значення, в `api()`.
- `my_claims.py` → `clean_params()`: невідомий ключ / відсутній обовʼязковий / не той тип / choice поза options → 422 з людським текстом; текст стрипається; params редагуються PUT-ом разом з нотаткою (якщо картки вже нема в каталозі — params заморожені як заявлені).
- `catalog_io.py`: dict-fallback картки тепер і при непорожніх `slots`; `taskline.py` не чіпав.
- Адмін-форма слоти не редагує (канал v1 — YAML); `TaskIn` без `slots`, PUT з форми їх не затирає.

## Сид E4 — слоти на 20 картках

spawn-schedule (кожні\* + макс) · blast-wave (радіус\*) · hp-damage (hp\* + кого) · shoot-cooldown\* · shoot-burst\* · shoot-spread\* · chain-detonation · timed-despawn\* · respawn · temporary-modes\* · inventory-limit\* · inventory-duration\* · player-death (життя) · time-out\* · collect-quota\* · enemy-waves (хвиль\* + фінальна bool) · move-timer\* · maze-generation (choice dfs/prim) · ai-minimax\* · pattern-automaton (text\*). Зірочка = required.

Канал пройдено повним колом: export-звірка (diff порожній) → правка `tasks.yaml` мінімальними dict-нодами → `import` (оновлено 20) → `export` (канонізація) → повторний `import` (без змін 209).

## Фронт

- **`SlotFields.vue`** — інпути по спеці (число з юнітом / селект / чекбокс / текст), один компонент на створення і редагування.
- `ClaimPicker`: картка зі слотами розгортає міні-форму параметрів («Спавн за розкладом: Кожні [20] тіків · Макс. [4]»), кнопка блокується без обовʼязкових; emit тепер `pick(slug, params)` — WindowCard/EntityCard/MyGamePage оновлені (підказка-hint у WindowCard виділена в `addHint`).
- `ClaimRow`: параметри текстом у чіпі (`paramsText` у catalog.js: «Кожні 20 тіків · Фінальна хвиля») + редагування в розгорнутій формі.
- Паспорт: той самий текст у read-only чіпах трьох секцій; `TaskCard` каталогу показує рядок «⚙️ Кожні (тіків) · Макс. на полі» — видно картки рівня 1.

## Далі

Д3 «приклади на картках» — після реакції на [T104](../../games/.t/T104-C--ludopedia-d3-d6.md) · E3-речення вже покриті Rule (T101) · відповіді [T102](../../games/.t/T102-Q--ludopedia-build-questions.md).
