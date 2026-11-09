---
title: Sukoro (数コロ)
slug: sukoro
aka: [数コロ, Сукоро]
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
year: 1992
platforms: [paper, web]
links:
  - {kind: other, url: "https://www.janko.at/Raetsel/Sukoro/index.htm", best: true, note: "Janko: правила DE/EN/JP, історія (Nikoli №40, 12.1992, Tea.M), 140 пазлів 6×6–12×12 з applet-ом, рейтинг"}
  - {kind: other, url: "https://puzz.link/rules.html?sukoro", note: "puzz.link: сторінка правил (рендериться JS)"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/sukoro.js", note: "pzpr: правила EN/JP, Nikoli vol.40, коди помилок"}
  - {kind: official, url: "https://www.nikoli.co.jp/ja/puzzles/sukoro/", note: "Nikoli: правила JP, приклад і розвʼязок картинками"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/sukororoom.js", note: "варіант Sukoro-room (Nikoli vol.130)"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/view.js", note: "варіант View (ヴィウ)"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/master/test/script/sukoro.js", note: "тест pzprjs: цикл вводу мишею й клавіатурою, коди помилок"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=sukoro+puzzle+nikoli", note: "пошук; розвʼязання"}
stage: v1
coverage: 75
mechanics: [neighbor-count-clue, connectivity-check, markup-validity, completion-detection, satisfy-constraints, cell-click, keyboard-controls, flag-cycle, conflict-highlight, level-bank, level-rating, puzzle-select, help-window, in-game-editor, seed-share, save-game, undo-redo, replay, +no-adjacent-check, +dot-mark, +self-referential-clues, +room-all-or-nothing, +hint-reveal, +cell-coloring]
proposes: ["+cond:all_or_none(region)", "+card:self-referential-clues", "+card:room-all-or-nothing", "+ui:solved-frame", "+ui:value-popup-menu", "+window:puzzle-info"]
author: opus
date: 2026-11-09
---

# Sukoro (数コロ) — впиши 1…4 у частину клітинок: число = скільки сусідів теж мають число, рівні не торкаються, усі числа — одна група

## Суть
На сітці кілька даних чисел; гравець сам вирішує, які клітинки отримають число 1…4, а які лишаться порожніми. Кожне число дорівнює кількості своїх ортогональних сусідів, у яких теж стоїть число; однакові числа не можуть бути сусідами; усі клітинки з числами утворюють одну ортогонально звʼязну область. Незвичне: підказки **самопосилальні** — кожне вписане число водночас і підказка, і предмет підрахунку для сусідів.

## Поле і час
- Прямокутна сітка; у Janko — 6×6 (30), 8×8 (48), 10×10 (39), 12×12 (23); зразок pzpr — 5×5.
- Сусідство — 4 ортогональні; кутова клітинка ≤ 2, крайова ≤ 3 (наслідок правил).
- Шари: дані числа · числа гравця · позначки ○ «тут число» і × «порожньо».
- Час статичний; хід = вписати число / позначку / стерти.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітинка | mark | порожньо / 1…4 / ○ / × | одне значення |
| Дане число | mark | 1…4 | незмінне; теж рахується сусідами |
| Число гравця | mark | 1…4 | = кількість сусідів із числами |
| Позначка ○ | mark | «тут число, ще невідоме» | лише для гравця |
| Позначка × | mark | «точно порожньо» | лише для гравця |
| Група чисел | zone | усі клітинки з числами | одна звʼязна компонента |
| Кімната (Sukoro-room) | zone | обведена область | уся з числами або вся порожня; без повторів |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left_click, cell)` → ТО `set_value(cell, next)` — цикл порожньо → 1 → 2 → 3 → 4 → ○ → × → порожньо; правий клік — у зворотний бік (puzz.link, тест pzprjs).
- КОЛИ `input(key_digit, cell)` → ТО `set_value(cell, n)`; `input(key_minus)` → `mark(cell, ×)`; пробіл → `unmark(cell)` (puzz.link).
- КОЛИ `input(enter|space|ins, cell)` → ТО `mark(cell, …)` по колу порожньо → × → ○ → порожньо; X / `,` → ×; o / `.` → ○; `-`, Del, ⌫ — стерти (Janko).
- Підрахунок: КОЛИ `constraint_broken(count)` → ЯКЩО `not adjacent_count(cell, number, =, value)` → ТО конфлікт «The number of numbers placed in four adjacent cells is not equal to the number» (nmNumberNe).
- Рівні не поруч: КОЛИ `constraint_broken(equal)` → ЯКЩО `not no_adjacent(equal_numbers)` → ТО конфлікт «Equal numbers are adjacent» (nmAdjacent).
- Звʼязність: КОЛИ `constraint_broken(connect)` → ЯКЩО `not connected(number)` → ТО конфлікт «Numbers are divided» (nmDivide).
- Порожнє поле: КОЛИ `constraint_broken(empty)` → ЯКЩО `count(number, =, 0)` → ТО «There are no numbers on the board» (brNoValidNum).
- КОЛИ `all_constraints_met` → ТО `win` (Janko — `custom: «зелена рамка»`).
- Janko: F6 — помилки червоним; F3 — режим підказки; F4 — розвʼязок з логічним шляхом; Ctrl+Z / Pos1 → `undo(1)` / `undo(all)`.
- Дедукція «4»: четвірка → усі 4 сусіди з числами, жоден із них не 4 (наслідок правил).
- Дедукція «1 — листок»: одиниця має рівно одного сусіда-число, тож у звʼязній групі вона — кінцева клітинка (наслідок правил).
- Дедукція «межа»: число не більше кількості сусідів, що можуть бути числами (кут ≤ 2, край ≤ 3, кожен сусід-× зменшує межу) (наслідок правил).
- Дедукція «міст»: порожня клітинка, без якої група чисел розпадається, мусить бути числом (наслідок правил).
- Дедукція «ступені»: числа повністю задані множиною заповнених клітинок (це ступені вершин), тож пазл — знайти множину, де сусіди мають різні ступені (наслідок правил).
- Перемога: усі числа = кількість сусідів-чисел, рівні не поруч, група звʼязна · Поразка: — · Рахунок: —.

## Керування і ввід
- puzz.link, play: лівий клік — цикл значень уперед, правий — назад; клавіші 1–4, «-» — ×, пробіл — стерти; edit-режим: розмір поля й дані числа.
- Janko applet: лівий клік / тап — меню чисел; правий клік / утримання — меню позначок (символи, кольори); стрілки + Enter / Space / Ins; F7 — кандидати; Ctrl+S / Ctrl+L — зберегти / завантажити стан.
- Наведення без кліку + клавіша (Janko); масштаб Ctrl+стрілки.
- Папір: журнал Puzzle Communication Nikoli.

## Вікна, меню, HUD
- `game-screen`: сітка, дані й введені числа, ○ і ×, `conflict-highlight`, `+ui:solved-frame` (Janko), `+ui:value-popup-menu` (Janko).
- puzz.link: перемикач play / edit, перевірка з першою помилкою (коди pzpr).
- `puzzle-select` — Janko: 140 пазлів за датою, розміром, складністю.
- `help-window` — правила DE/EN/JP, Bedienungsanleitung, сторінка Beispiel.
- `+window:puzzle-info` (F1, Janko) — інфо про пазл і лист вебмайстру.

## Фічі поза полем
- `auto-check` (puzz.link, Janko F6), автовизнання розвʼязку.
- `undo` / `redo`; збереження стану (Janko).
- `hint` (F3), `show-solution` (F4) з логічним шляхом у списку ходів (дані `[moves]`).
- `puzzle-bank` Janko: рейтинг за часом — 1–2: 15 пазлів, 3: 57, 4: 40, 5: 21, 6: 4, 7: 1, 8: 2; нові без оцінки; пазли з логічним шляхом — кольором.
- `level-editor` + `share-code` — URL puzz.link (зразок `5/5/2a2c4a2g2a4c2a2`).

## Варіації й родичі
- **Sukoro-room** (数コロ部屋, Nikoli vol.130): поле поділене на кімнати; кімната або вся з числами, або вся порожня; у кімнаті без повторів; у списку правил pzpr нема «рівні не поруч». Коди bkMixed, bkDupNum.
- **View** (ヴィウ): число = загальна кількість порожніх клітинок, видимих по вертикалі й горизонталі; рівні не поруч; група звʼязна (код nmSumViewNe).
- Родичі в корпусі: [Kuromasu](kuromasu.md) (число рахує видимі білі), [Nurikabe](nurikabe.md) і [Hitori](hitori.md) (звʼязність множини клітинок), [Fill-a-Pix](fill-a-pix.md) і [Context](context.md) (число рахує сусідів виду), [Zeiger](zeiger.md) (теж самопосилальні числа).
- **Осі варіацій**: що рахує число (сусідів-чисел / видимі порожні) · заборона (рівні поруч / повтор у кімнаті) · кімнати «все або нічого» (так / ні) · звʼязність групи (так).

## Цікавинки для курсу
- Перевірка: підрахунок 4-сусідів + рівні не поруч + BFS-звʼязність — 🌱.
- Цикл вводу з 7 станів уперед / назад двома кнопками миші — 🌱.
- Самопосилальні підказки: зміна однієї клітинки зачіпає до 5 обмежень, перевірка інкрементально — 📎.
- Розвʼязувач: стани {порожньо, 1…4} + межі + точки зчленування для звʼязності + backtracking — 🥇.
- Генератор: випадкова звʼязна множина, де сусіди мають різні ступені → числа = ступені → прибирання даних з перевіркою єдиності — 👑.

## Мапа на каталог
- Є: `neighbor-count-clue` ↔ число = скільки сусідів-чисел · `connectivity-check` ↔ усі числа одна група · `markup-validity`, `completion-detection`, `satisfy-constraints` · `cell-click`, `keyboard-controls`, `flag-cycle` ↔ цикл ○ / × кнопками · `conflict-highlight` · `level-bank`, `level-rating`, `puzzle-select`, `help-window` · `in-game-editor`, `seed-share` ↔ URL puzz.link · `save-game`, `undo-redo`, `replay` ↔ логічний шлях F4.
- Перевикористано: `+no-adjacent-check` (слот: рівні значення), `+dot-mark` ↔ ○ / ×, `+hint-reveal`, `+cell-coloring`.
- **Нема** → пропозиції карток:
  - `+self-referential-clues` «Вписані гравцем значення самі є підказками й рахують одне одного» · game-logic/constraints · 📎 — Sukoro, View, Zeiger.
  - `+room-all-or-nothing` «Регіон або повністю заповнений, або порожній» · game-logic/constraints · 🌱 — Sukoro-room.

## Пропозиції до словників
- `+cond:all_or_none(region)` — регіон повністю заповнений або повністю порожній (Sukoro-room).
- `+card:self-referential-clues`, `+card:room-all-or-nothing` — див. мапу.
- `+ui:solved-frame`, `+ui:value-popup-menu`, `+window:puzzle-info` — повтори Janko-applet-а.

## Джерела
- ⭐ [Janko: Sukoro](https://www.janko.at/Raetsel/Sukoro/index.htm) — 4 правила DE/EN/JP, Nikoli №40 (грудень 1992), автор Tea.M, 140 пазлів, рейтинг.
- [puzz.link: правила](https://puzz.link/rules.html?sukoro) — сторінка рендериться JS; правила взято з файла нижче.
- [pzpr: sukoro.js](https://puzz.link/js/pzpr-samples/sukoro.js) — правила EN/JP, «up to 4», коди brNoValidNum / nmAdjacent / nmNumberNe / nmDivide.
- [Nikoli: 数コロ](https://www.nikoli.co.jp/ja/puzzles/sukoro/) — правила JP.
- [pzpr: sukororoom.js](https://puzz.link/js/pzpr-samples/sukororoom.js), [pzpr: view.js](https://puzz.link/js/pzpr-samples/view.js) — варіанти.
- [pzprjs test: sukoro.js](https://raw.githubusercontent.com/robx/pzprjs/master/test/script/sukoro.js) — цикл значень мишею, клавіші «-» і пробіл.
- YouTube: пошук «sukoro puzzle nikoli».

## Непевне
- (?) Значення станів «+» / «-» у циклі pzprjs як ○ / × — з тестового скрипта, на живій сторінці не перевіряв.
- (?) У View: чи числа перекривають огляд — правило каже лише «seen in a straight line».
- (?) Значення «コロ» у назві — Janko сам ставить «?».
- (?) Автор «Tea.M» — лише за Janko.
