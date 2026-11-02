---
title: Hitori (Хіторі, Singles)
slug: hitori
family: pencil-logic
also: []
klass: puzzle
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: none
  goal: constraints
year: 1990
platforms: [paper, web, mobile, PC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Hitori", best: true, note: "3 правила, Nikoli №29 (березень 1990), техніки розвʼязання, NP-повнота"}
  - {kind: official, url: "https://www.nikoli.co.jp/en/puzzles/hitori/", note: "Nikoli: 3 правила, Sample → Progressing → Solution"}
  - {kind: official, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/singles.html", note: "Tatham Singles: правила, миша/клавіатура, параметри, преференс видимості чисел"}
  - {kind: play, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/singles.html", note: "Singles у браузері (WebAssembly)"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/hitori.js", note: "puzz.link: текст правил, тести вводу (use=1/2), коди помилок"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=hitori+puzzle+how+to+solve", note: "пошук; розвʼязання"}
stage: v1
coverage: 80
mechanics: [markup-validity, completion-detection, satisfy-constraints, cell-click, keyboard-controls, reachability-check, unique-puzzle-generation, difficulty-levels, level-solver, field-size-picker, game-settings, import-open-formats, +undo-redo, +seed-share, +cell-shade-toggle, +dot-mark, +global-connectivity, +no-adjacent-check, +line-uniqueness-by-removal, +solve-into-undo, +input-scheme-toggle]
proposes: ["+cond:connected", "+cond:duplicate_in_line", "+ui:shaded-value-visibility", "+card:no-adjacent-check", "+card:line-uniqueness-by-removal", "+card:input-scheme-toggle"]
author: opus
date: 2026-11-02
---

# Hitori — зафарбуй «зайві» числа так, щоб у рядках не лишилось дублів

## Суть
Сітка повністю заповнена числами; гравець зафарбовує частину клітинок, «стираючи» числа, доки в кожному рядку й стовпці не лишиться жодного повтору серед незафарбованих. Дві додаткові умови роблять задачу глобальною: зафарбовані не торкаються сторонами, а всі білі клітинки утворюють одну звʼязну область. Незвичне: це «зворотне» судоку — не вписуєш, а прибираєш, і найсильніший аргумент дедукції — звʼязність білих (не можна відрізати острів).

## Поле і час
- Прямокутна (зазвичай квадратна) сітка; кожна клітинка має число (у Nikoli — до розміру сітки (?)).
- Сусідство ортогональне (4) для заборони «чорне поруч із чорним» і для звʼязності білих; діагональний дотик чорних дозволено.
- Шари клітинки: число (незмінне) · стан гравця: невідомо / зафарбовано / кружечок («точно біле»).
- Час статичний; хід = зміна стану однієї клітинки.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітинка з числом | mark | value, стан unknown / shaded / circle | клік змінює стан; число завжди присутнє в даних |
| Зафарбована клітинка | mark | — | вилучає своє число з перевірки рядка/стовпця; не сусідить із іншою зафарбованою |
| Кружечок (circle) | mark | — | позначка гравця «тут біле»; Tatham: правою кнопкою |
| Рядок / стовпець | zone | n клітинок | серед незафарбованих кожне число ≤ 1 раз |
| Біла область | zone | кількість компонент | усі незафарбовані — одна 4-звʼязна компонента |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left_click, cell)` → ЯКЩО `state(cell, unknown)` → ТО `mark(cell, shaded)`; повтор → `unmark(cell)` (Tatham: «restore the number»).
- КОЛИ `input(right_click, cell)` → ТО `mark(cell, circle)`; повтор → `unmark(cell)`.
- КОЛИ `input(click_outside_grid)` → ТО `custom: «перемкнути: зафарбовані ховають число / показують темно-сірим»` (Tatham).
- КОЛИ `constraint_broken(unique_in_line)` — ЯКЩО `custom: «два незафарбовані з однаковим числом у рядку/стовпці»` → ТО обидва підсвічуються (puzz.link `nmDupRow`).
- КОЛИ `constraint_broken(no_adjacent_shaded)` — ЯКЩО `adjacent_count(cell, shaded, >, 0)` для зафарбованої → ТО конфлікт (`csAdjacent`).
- КОЛИ `constraint_broken(white_connected)` — ЯКЩО `not custom: «білі утворюють одну компоненту»` → ТО конфлікт (`cuDivideRB`; перевірка flood fill / BFS).
- КОЛИ `constraint_broken(board_not_empty)` — нічого не зафарбовано, а дублі є → ТО конфлікт (`brNoShade` (?)).
- КОЛИ `all_constraints_met` → ТО `win`, `flash` (Tatham) / повідомлення (puzz.link).
- Дедукційні наслідки (не правила гри, а техніки з Wikipedia): сусід чорного → біле; біле число → усі його дублі в рядку й стовпці чорні; три однакові поспіль → середнє біле, крайні чорні; кут, рівний обом сусідам, — чорний; клітинка, чиє зафарбування розрізає білих, — біла.
- Перемога: нема дублів у рядках/стовпцях, чорні не торкаються, білі звʼязні. Поразки й рахунку нема.

## Керування і ввід
- Tatham Singles: ліва кнопка — чорне/повернути число; права — кружечок/зняти; клік поза сіткою — перемкнути видимість чисел під чорним.
- Клавіатура (Tatham): стрілки — курсор; Return — чорне; Space — кружечок.
- puzz.link: налаштування `use=1` (ліва — фарба, права — кружечок) або `use=2` (одна кнопка циклює unknown → shaded → circle; права — у зворотному порядку); drag протягує стан через кілька клітинок.
- Спільні дії Tatham: N — нова гра, U/Ctrl+Z — undo, R/Ctrl+R — redo, Solve, Restart.

## Вікна, меню, HUD
- `game-screen`: сітка чисел + `conflict-highlight` (дублі, сусідні чорні, розріз білих) + `cursor` (клавіатура).
- Tatham: меню Game (New, Restart, Undo, Redo, Solve, Enter game ID, Enter random seed, Download/Upload save file, Preferences) · меню Type (пресети розміру/складності + Custom…).
- `settings-window` (Preferences): чи видно числа на чорних клітинках — постійно між іграми.
- `custom-window` → `+window:params-dialog`: Width, Height, Difficulty (Tatham Custom…).
- `+window:game-id-dialog`: ввести/показати ID чи seed.
- `help-window`: правила (Nikoli Sample / Progressing / Solution).
- Переходи: Type → params-dialog → нова генерація → game-screen; game-screen → (розвʼязано) спалах → New game.

## Фічі поза полем
- `auto-check` (миттєве підсвічування порушень у Tatham; puzz.link — за кнопкою Check з текстом коду помилки).
- `undo` ∞ і `redo`; Solve вставляє розвʼязок в історію undo — можна відкотити й розвʼязувати далі.
- `seed-input` / `share-code` (game ID, random seed), `save-slots` через файл (Download/Upload save file).
- `custom-difficulty`: розмір і складність генератора; генерація з унікальним розвʼязком.
- `level-editor` + `share-code` (puzz.link: edit mode, числа з клавіатури, пазл у URL).
- `puzzle-bank` (Nikoli-книги, сайти з пазлами).

## Варіації й родичі
- Tatham **Singles** (James Harvey) — та сама гра під іншою назвою.
- Родичі за правилами: Nurikabe (звʼязність одного кольору), Kurodoko/Range (чорні не торкаються + білі звʼязні), Heyawake (ті самі дві умови + кімнати з числами), Sudoku (унікальність у рядку — але вписуванням).
- **Осі варіацій**: звідки дублі (числа / літери / кольори) · що звʼязне (білі / чорні) · заборона дотику чорних (4-сусідство / 8-сусідство / нема) · області (лише рядки й стовпці / ще й регіони) (?).

## Цікавинки для курсу
- Перевірка дублів у рядках/стовпцях серед незафарбованих — 🌱 (лічильник `Counter` по лінії).
- Заборона сусідства зафарбованих — 🌱; спільна механіка з Yajilin і Star Battle (там — 8-сусідство).
- Звʼязність білих через flood fill / BFS — 📎 (картка `reachability-check`).
- Перемикач «чорне ховає число / показує сірим» — 🌱, гарний приклад налаштування подання без впливу на логіку.
- Розвʼязувач правилами (сусід чорного → біле, біле → дублі чорні, «точка розрізу» → біле) — 🥇 (останнє — пошук точок зчленування графа).
- Генератор: латинський квадрат → вибрати чорні з умовами → заповнити дублями → перевірити унікальність — 👑.

## Мапа на каталог
- Є: `markup-validity` ↔ дублі й сусідні чорні · `completion-detection`, `satisfy-constraints` ↔ перемога · `cell-click` ↔ фарба/кружечок · `keyboard-controls` ↔ курсор Tatham · `reachability-check` ↔ звʼязність білих · `unique-puzzle-generation`, `level-solver`, `difficulty-levels`, `field-size-picker`, `game-settings` ↔ Tatham Custom · `import-open-formats` ↔ puzz.link URL / pzprv3.
- Перевикористано пропозиції корпусу: `+undo-redo`, `+seed-share`, `+cell-shade-toggle`, `+dot-mark` (кружечок = «точно біле»), `+global-connectivity`, `+solve-into-undo`.
- **Нема** → пропозиції карток:
  - `+no-adjacent-check` «Позначені клітинки не торкаються» · game-logic/constraints · 🌱 · слот {adjacency: 4|8} — Hitori, Yajilin (4), Star Battle (8).
  - `+line-uniqueness-by-removal` «Унікальність у лінії через вилучення» · game-logic/constraints · 🌱 — дубль рахується лише серед незафарбованих.
  - `+input-scheme-toggle` «Схема вводу: дві кнопки / одна кнопка-цикл» · interface/input · 🌱 — puzz.link `use=1/2`.

## Пропозиції до словників
- `+cond:connected` — клітинки одного стану утворюють одну компоненту (білі в Hitori).
- `+cond:duplicate_in_line` — у рядку/стовпці серед активних клітинок є повтор значення.
- `+ui:shaded-value-visibility` — перемикач «зафарбоване ховає / показує значення» (Tatham Singles).
- `+card:no-adjacent-check`, `+card:line-uniqueness-by-removal`, `+card:input-scheme-toggle` — див. мапу.

## Джерела
- ⭐ [Wikipedia: Hitori](https://en.wikipedia.org/wiki/Hitori) — правила, Nikoli №29 (березень 1990), техніки, NP-повнота (Hearn, Demaine 2009).
- [Nikoli: Hitori](https://www.nikoli.co.jp/en/puzzles/hitori/) — три правила, приклад «Sample / Progressing / Solution».
- [Tatham: Singles](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/singles.html) — правила, миша й клавіатура, параметри, преференс; автор порту — James Harvey.
- [Singles у браузері](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/singles.html) — меню Game/Type, кнопки New/Restart/Undo/Redo/Solve.
- [Tatham: common actions](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/common.html) — спільні клавіші й Solve-в-undo.
- [puzz.link hitori.js](https://puzz.link/js/pzpr-samples/hitori.js) — правила плеєра, тести вводу, коди помилок `brNoShade`, `csAdjacent`, `cuDivideRB`, `nmDupRow`.
- YouTube: пошук «hitori puzzle how to solve».

## Непевне
- (?) Значення `brNoShade` — вивів із назви («нічого не зафарбовано»); тексту повідомлення не бачив.
- (?) Пресети складності Tatham Singles (назви рівнів) — сторінка документації їх не перелічує.
- (?) Чи обмежені числа в Nikoli-Хіторі розміром сітки — з памʼяті.
- (?) Варіанти з регіонами / 8-сусідством — ймовірні фан-варіанти, джерела не бачив.
