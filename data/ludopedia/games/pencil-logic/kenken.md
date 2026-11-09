---
title: KenKen (Keen, CalcuDoku, Кенкен)
slug: kenken
aka: [Keen, CalcuDoku, MathDoku, KenDoku, Inshi no heya, Кенкен, Калькудоку]
family: pencil-logic
also: [word-number]
klass: puzzle
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: none
  goal: constraints
year: 2004
platforms: [paper, web, mobile, PC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/KenKen", best: true, note: "правила, автор Tetsuya Miyamoto (2004), торгова марка, варіанти операцій, історія публікацій"}
  - {kind: official, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/keen.html", note: "Tatham Keen: правила, pencil marks, клавіша M, Custom (3–9, Unreasonable, Multiplication only)"}
  - {kind: play, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/keen.html", note: "Keen у браузері; меню Game/Type"}
  - {kind: other, url: "https://www.conceptispuzzles.com/index.aspx?uri=puzzle/calcudoku", note: "Conceptis CalcuDoku: правила, SingleOp/DualOp/QuadOp"}
  - {kind: other, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/common.html", note: "спільні дії Tatham"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=kenken+how+to+solve", note: "пошук; розвʼязання"}
stage: v1
coverage: 70
mechanics: [markup-validity, completion-detection, satisfy-constraints, cell-click, keyboard-controls, pencil-marks, hover-highlight, unique-puzzle-generation, difficulty-levels, difficulty-rating, level-solver, field-size-picker, game-settings, rule-variants, undo-redo, seed-share, import-open-formats, +auto-candidates, +solve-into-undo, +sum-clue, +arith-cage, +latin-square]
proposes: ["+cond:sum_eq", "+cond:cage_op", "+cond:duplicate_in_line", "+window:params-dialog", "+window:game-id-dialog", "+card:arith-cage", "+card:latin-square"]
author: opus
date: 2026-11-09
---

# KenKen (Keen) — латинський квадрат, де клітки задають результат арифметичної дії

## Суть
Сітка n×n (3×3…9×9) розбита жирними лініями на клітки; у кутку кожної — ціль і операція (+, −, ×, ÷). Гравець вписує цифри 1…n так, щоб у кожному рядку й стовпці кожна цифра була рівно раз (латинський квадрат), а цифри кожної клітки давали ціль своєю операцією. Цифри в клітці можуть повторюватися, якщо не стоять в одному рядку чи стовпці. Незвичне: підказка — **арифметичний вираз над групою**, а не значення; розвʼязання — перебір розкладів числа на множники/доданки.

## Поле і час
- Квадратна сітка n×n; Wikipedia і Tatham: n від 3 до 9 (Tatham: більше — незручно вводити цифри).
- Клітки — довільні звʼязні групи клітинок; клітка з однієї клітинки — «вільна» (ціль = цифра).
- Шари: межі кліток і підказки (незмінні) · цифра гравця · pencil marks (кілька кандидатів у клітинці).
- Час статичний; хід = вписати/стерти цифру чи кандидата.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітинка | mark | цифра 1…n або порожньо; кандидати | одна цифра або набір олівцевих кандидатів |
| Цифра | mark | 1…n | рахується в рядку, стовпці й клітці |
| Кандидат (pencil mark) | mark | набір цифр | ігнорується перевіркою (Tatham) |
| Клітка (cage) | zone | ціль T, операція op, розмір k | цифри, скомбіновані op, дають T |
| Клітка «+» / «×» | zone | k ≥ 1 | сума / добуток усіх цифр = T |
| Клітка «−» / «÷» | zone | k = 2 (Tatham, Shortz) | різниця / частка двох цифр у будь-якому порядку = T |
| Вільна клітка | zone | k = 1 | цифра = T |
| Рядок / стовпець | zone | n | кожна цифра 1…n рівно раз |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left_click, cell)` + `input(key_digit)` → ТО `set_value(cell, d)`; Space → `unmark(cell)` (Tatham).
- КОЛИ `input(right_click, cell)` + `input(key_digit)` → ТО `mark(cell, candidate d)`; повтор тієї ж цифри — зняти кандидата (Tatham).
- КОЛИ `input(key_M)` → ТО `custom: «заповнити всі порожні клітинки повним набором кандидатів»` (Tatham).
- КОЛИ `after(set_value)` → ЯКЩО `custom: «у клітинці були кандидати»` → ТО `custom: «кандидати стираються, лишається цифра»` (Tatham: цифра і кандидати разом не співіснують).
- КОЛИ `constraint_broken(latin)` → ЯКЩО `custom: «цифра повторюється в рядку чи стовпці»` (`+cond:duplicate_in_line`) → ТО конфлікт.
- КОЛИ `constraint_broken(cage)` → ЯКЩО `custom: «клітка заповнена, але op(цифри) ≠ T»` (`+cond:cage_op`) → ТО клітка конфліктна (?).
- Клітка «+»: ЯКЩО `custom: «сума цифр = T»` (`+cond:sum_eq`) → задоволена.
- Клітка «×»: ЯКЩО `custom: «добуток цифр = T»` (`+cond:cage_op`) → задоволена.
- Клітка «−»: ЯКЩО `custom: «|a − b| = T»` → задоволена; клітка «÷»: ЯКЩО `custom: «max/min = T»` → задоволена.
- КОЛИ `all_constraints_met` → ТО `win`.
- Повтор у клітці: ЯКЩО `not same(row or col)` → дозволено (Tatham: «зворотне до Killer-режиму Solo»; Conceptis — те саме).
- Дедукція «комбінації»: для кожної клітки перелічити всі кортежі цифр 1…n з потрібним результатом і без повторів у рядку/стовпці; викреслювати, коли сусідні клітки звужують варіанти (Wikipedia).
- Дедукція «вільна клітка» — цифра відома одразу; «−» з T = n−1 — лише пара {1, n}; «÷» з T = n у сітці n — лише {1, n}.
- Дедукція з судоку: прихована одиничка в рядку/стовпці; правило суми рядка = n(n+1)/2 для «+»-кліток, що повністю лежать у рядку.
- Перемога: латинський квадрат + усі клітки задоволені. Поразки й рахунку нема.

## Керування і ввід
- Tatham Keen: лівий клік по порожній клітинці + цифра — вписати; Space або Undo — виправити.
- Pencil: правий клік + цифра — додати/прибрати кандидата; правий клік + Space — очистити кандидатів; лівий клік + цифра/Space теж стирає кандидатів.
- Клавіатура: стрілки — курсор; цифра — вписати; Return — перемикач режиму «олівець»; M — усі кандидати скрізь.
- Спільні дії Tatham: New, Restart, Undo, Redo, Solve; Enter game ID / random seed; Download/Upload save file; Preferences.

## Вікна, меню, HUD
- `game-screen`: сітка з жирними клітками, підказки «T op» у кутку клітки, цифри, `pencil-marks`, курсор, `conflict-highlight` (?).
- Tatham: меню Game (Enter game ID…, Enter random seed…, Download save file…, Upload save file…, Preferences…) · Type (пресети + Custom…) · кнопки New game, Restart game, Undo move, Redo move, Solve game.
- `+window:params-dialog` (Custom…): Grid size (3–9), Difficulty (найвища — Unreasonable), Multiplication only.
- `+window:game-id-dialog` — ID/seed; на сторінці «Link to this puzzle: by game ID / by random seed».
- `settings-window` (Preferences) — вміст не перевіряв (?).
- `help-window` — «Full instructions» (Tatham doc).
- Переходи: Type → Custom → params-dialog → генерація → game-screen; розвʼязано → New game.

## Фічі поза полем
- `undo` / `redo` без ліміту; `auto-solve` (Solve) у історії undo.
- `seed-input`, `share-code`, збереження у файл.
- `custom-difficulty`: розмір 3–9, складність; `custom-rules`: «Multiplication only» (варіант Inshi no heya).
- Складність Tatham: легші рівні — без перебору, з дедалі складнішими дедукціями; Unreasonable може вимагати backtracking, але розвʼязок єдиний.
- Газети: The Times з березня 2008, NYT та понад 200 видань (Wikipedia); Conceptis — банк SingleOp/DualOp/QuadOp.

## Варіації й родичі
- **Inshi no heya** — усі клітки «×» (Tatham, опція Multiplication only).
- Conceptis: **SingleOp** (одна операція на все поле, вказана над сіткою), **DualOp**, **QuadOp**.
- Wikipedia: без символів операцій (операцію теж треба вгадати); степінь, модуль, побітові операції, нуль і відʼємні; великі клітки «−»/«÷» в інших авторів.
- Родичі: [Sudoku](sudoku.md) (латинський квадрат + блоки), Killer Sudoku у [Sudoku variants](sudoku-variants.md) (суми в клітках, без повтору в клітці), [Kakuro](kakuro.md) (суми прогонів), Towers/Unequal у [Tatham Collection](tatham-collection.md).
- **Осі варіацій**: набір операцій (+ / × / усі 4 / приховані / екзотичні) · повтор у клітці (дозволено / ні) · розмір клітки для −/÷ (2 / будь-який) · діапазон цифр (1…n / з 0 / відʼємні).

## Цікавинки для курсу
- Перевірка латинського квадрата — 🌱.
- Перевірка клітки з 4 операціями (−/÷ у будь-якому порядку для двох клітинок) — 🌱.
- Перелік комбінацій клітки з урахуванням рядків/стовпців (генератор кортежів + фільтр) — 📎; як помічник кандидатів «M» + звуження — 🥉.
- Розвʼязувач: пропагація кандидатів кліток і рядків + backtracking — 🥇.
- Генератор: випадковий латинський квадрат → випадкове розбиття на клітки → вибір операцій → перевірка єдиності розвʼязку — 👑.
- Рівні складності за набором дедукцій, потрібних розвʼязувачу (як у Tatham), — 🥇.

## Мапа на каталог
- Є: `markup-validity` ↔ дублікати в рядку/стовпці · `completion-detection`, `satisfy-constraints` · `cell-click`, `keyboard-controls`, `hover-highlight` · `pencil-marks` ↔ кандидати · `unique-puzzle-generation`, `difficulty-levels`, `difficulty-rating`, `level-solver` · `field-size-picker`, `game-settings` ↔ Custom · `rule-variants` ↔ Multiplication only · `undo-redo`, `seed-share`, `import-open-formats` ↔ game ID.
- Перевикористано: `+auto-candidates` (з Sudoku) ↔ клавіша M · `+solve-into-undo` · `+sum-clue` (з Kakuro) ↔ «+»-клітки.
- **Нема** → пропозиції карток:
  - `+arith-cage` «Клітка з ціллю й операцією» · game-logic/constraints · 📎 · слот {ops: +|−|×|÷|hidden, repeat: allowed|forbidden} — KenKen, Killer (лише +, без повтору).
  - `+latin-square` «Кожна цифра раз у рядку й стовпці» · game-logic/constraints · 🌱 — KenKen, Towers, Futoshiki, Sudoku без блоків.

## Пропозиції до словників
- `+cond:sum_eq` — сума групи = N (повтор з Kakuro).
- `+cond:cage_op` — op(цифри групи) = T, op ∈ {+, −, ×, ÷}; узагальнення `sum_eq`.
- `+cond:duplicate_in_line` — повтор значення в рядку/стовпці (повтор з інших файлів).
- `+window:params-dialog`, `+window:game-id-dialog` — повтор Tatham-вікон.
- `+card:arith-cage`, `+card:latin-square` — див. мапу.

## Джерела
- ⭐ [Wikipedia: KenKen](https://en.wikipedia.org/wiki/KenKen) — правила, Miyamoto 2004, «ken» = мудрість, торгові марки (Nextoy), Calcudoku/Mathdoku, варіанти, The Times 2008, NYT.
- [Tatham: Keen](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/keen.html) — правила з повтором у клітці, pencil marks, M, Return, Custom (3–9, Unreasonable, Multiplication only = Inshi no heya).
- [Keen у браузері](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/keen.html) — меню й кнопки.
- [Conceptis: CalcuDoku](https://www.conceptispuzzles.com/index.aspx?uri=puzzle/calcudoku) — правила, «a number may be used more than once in the same block», SingleOp/DualOp/QuadOp.
- [Tatham: common actions](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/common.html) — спільні дії збірки.
- YouTube: пошук «kenken how to solve».

## Непевне
- (?) Як Tatham Keen підсвічує помилки (дублікати червоним; клітка з неправильним результатом) — у документації не описано.
- (?) Повний список рівнів складності Keen (між Easy і Unreasonable) — сторінка називає лише Unreasonable.
- (?) Вміст Preferences у Keen.
- (?) Дедукція «рядок = n(n+1)/2» — стандартна техніка Killer Sudoku, у відкритих джерелах для KenKen прямо не бачив.
