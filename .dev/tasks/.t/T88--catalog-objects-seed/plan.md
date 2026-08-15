# T88 · Сид чернеток: елементи налаштувань, типи вікон, редактор, магазин

`2026-08-15` · ⚙️ задача · етап A пілота ([T87](../../../.rounds/.t/T87-R--game-round-decisions.md))

Контекст:
- рішення: [T84](../../../reports/.t/T84-Q--game-objects-questions.md) Q8a (сімʼя налаштувань + типи вікон чернетками) + [T86](../../../games/.t/T86-Q--mechanics-questions.md) Q4a (діти редактора/магазину);
- канал — YAML v2 (`data/catalog/tasks.yaml`) + `catalog_io.py import` (upsert по slug), ревізія — Vitalik в адмінці.

## Кроки

- [ ] Свіжий export з Mongo (підхопити можливі адмін-правки) + бекап YAML у tmp.
- [ ] Типи вікон у interface/menus: splash-screen, settings-window, shop-window, game-screen, help-window, about-window, custom-window (без монетки — ціна договірна, 🔁).
- [ ] Тег `#window` на картки-типи вікон (нові + main-menu, pause-menu, confirm-dialog, end-screen, level-select, leaderboard) — з нього етап B збере дропдаун типів.
- [ ] Сімʼя settings-elements у interface/settings: гучність, перемикач музики, аватар, розмір поля, мова, перепризначення клавіш; функція sound-volume у interface/sound.
- [ ] Діти in-game-editor: палітра, інструменти малювання, гумка, undo/redo, плейтест.
- [ ] Діти shop-between-levels: вітрина, превʼю товару, знижики/розпродажі, продаж назад.
- [ ] `catalog_io.py import` → перевірка лічильників; повторний export+import → «без змін» (раундтрип).
- [ ] report.md + оновлення README вузла.
