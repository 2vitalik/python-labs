---
title: Kakuro (Cross Sums, Какуро)
slug: kakuro
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
year: 1966
platforms: [paper, web, mobile]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Kakuro", best: true, note: "правила, позначення «16-in-two», техніки, NP-повнота"}
  - {kind: official, url: "https://www.nikoli.co.jp/en/puzzles/kakuro/", note: "правила Nikoli, «король олівцевих пазлів»"}
  - {kind: play, url: "https://www.puzzle-kakuro.com/", note: "грати онлайн: 6×6…30×30, pencil, помічник комбінацій"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Killer_sudoku", note: "родич: суми в клітках поверх судоку"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=kakuro+how+to+solve", note: "пошук; розвʼязання"}
stage: v1
coverage: 70
mechanics: [satisfy-constraints, markup-validity, completion-detection, cell-click, keyboard-controls, pencil-marks, hover-highlight, unique-puzzle-generation, difficulty-levels, difficulty-rating, level-solver, daily-puzzle, field-size-picker, level-from-txt, +undo-redo, +sum-clue, +combination-helper, +auto-candidates, +seed-share]
proposes: ["+trigger:constraint_broken", "+trigger:all_constraints_met", "+trigger:input", "+effect:set_value", "+effect:mark", "+cond:sum_eq", "+role:mark", "+role:zone", "+ui:pencil-marks", "+ui:conflict-highlight", "+ui:combination-helper", "+ui:number-pad", "+feature:auto-check", "+feature:daily-puzzle"]
author: opus
date: 2026-11-02
---

# Kakuro — кросворд із цифр: кожен прогін дає задану суму без повторів

## Суть
Сітка, схожа на кросворд: чорні клітини несуть підказки-суми, білі утворюють горизонтальні й вертикальні «прогони» (runs). У кожну білу клітину пишеш цифру 1–9 так, щоб сума прогону дорівнювала підказці, а цифри в прогоні не повторювались. Ядро — **комбінаторика розкладів суми** («3 у двох» = лише 1+2) плюс перехресні обмеження: кожна клітина належить рівно двом прогонам. Відомий з 1966 р. як Dell «Cross Sums»; в Японії — Kakuro, найпопулярніший пазл до Sudoku.

## Поле і час
- Прямокутна сітка (типово до 16×16; онлайн — 6×6…30×30) з двома типами клітин: блок (чорна, можливо з діагоналлю й однією-двома сумами) і клітина для цифри.
- Прогін — максимальна неперервна послідовність білих клітин у рядку чи стовпці; сума прогону стоїть у блоці зліва (горизонталь) або зверху (вертикаль) у половинці, розділеній діагоналлю.
- Час статичний; цифрова версія — опційний таймер (секундомір) і лічильник прогресу.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Блок (чорна клітина) | static | — | непрохідна; розриває прогони |
| Блок-підказка | static | `across` і/або `down` сума (3…45) | задає суму прогону праворуч / донизу |
| Клітина цифри | mark | значення 1–9 або порожньо | належить одному горизонтальному й одному вертикальному прогону |
| Прогін (run) | zone | довжина 2–9, сума | сума цифр = підказка, усі цифри різні |
| Олівцеві кандидати | mark | множина ⊆ {1..9} | нотатка гравця; на перевірку не впливають (цифрова версія) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(cell, digit)` → ЯКЩО `cell(cell, white)` → ТО `set_value(cell, digit)`; на блоці — `block`.
- КОЛИ `constraint_broken(duplicate in run)` → ТО `custom: «підсвітити дубль»` (цифрова версія, опційно).
- КОЛИ `constraint_broken(sum(run) ≠ clue)` → ЯКЩО `count(empty in run, ==, 0)` → ТО `custom: «підсвітити неправильну суму»`.
- КОЛИ `constraint_broken(sum(run) > clue)` → ТО той самий сигнал навіть до заповнення прогону (рання перевірка, опційно (?)).
- КОЛИ `input(cell, pencil, d)` → ТО `mark(cell, candidate d)` toggle; ЯКЩО `custom: «auto remove notes»` → ТО після `set_value(x, d)` кандидат `d` зникає з усіх клітин обох прогонів x.
- КОЛИ `all_constraints_met` → ТО `win`, `custom: «зупинити таймер»`, `window(end-screen)`.
- Обмеження генерації: розвʼязок єдиний; кожен прогін має довжину ≥ 2; деякі видавці забороняють однаковий набір цифр у двох прогонах (?).
- Ключові дедукції (не правила, а техніки — для солвера/підказок): унікальні розклади (3/2 = {1,2}, 4/2 = {1,3}, 16/2 = {7,9}, 17/2 = {8,9}, 6/3 = {1,2,3}, 45/9 = {1..9}); перетин двох множин кандидатів; «ізольована цифра» — потрібна цифра можлива лише в одній клітині прогону; «бокс» — сума кількох прогонів мінус відомі частини дає одну клітину.
- Перемога: усі білі клітини заповнені, усі суми й заборона повторів виконані. Поразки нема (у цифрі — опційне «Done» з перевіркою). Рахунок: час розвʼязання.

## Керування і ввід
- (цифрова версія) Клік/тап по клітині — вибір; цифра з клавіатури або екранного `number-pad`; Backspace/0 — стерти; стрілки — рух курсору.
- Режим олівця: перемикач `mode-toggle` або правий клік / тривале натискання (puzzle-kakuro.com: «toggle pencil mode with left/right click»).
- Помічник комбінацій: утримання клітини / Shift показує всі набори цифр для суми й довжини обох прогонів (puzzle-kakuro.com).
- Папір: пишеш цифри, кандидати — дрібно в кутах клітини.

## Вікна, меню, HUD
- `game-screen` (цифрова версія): сітка, `timer-elapsed`, `number-pad` (опційно), `pencil-marks`, `conflict-highlight` (дублі, хибні суми, хибні нотатки), підсвітка поточного рядка/стовпця і поточних підказок, «посірілі» вже використані цифри.
- `combination-helper` — спливна панель «сума/довжина → набори цифр».
- `puzzle-select` / вибір розміру × складності (Easy/Normal/Hard) + Special Daily/Weekly/Monthly (`daily-window`).
- `settings-window`: показ кнопок/цифрової панелі, ліворукий режим, автонотатки, автоприбирання нотаток, підсвітки помилок, нічна тема, особистий таймер.
- `end-screen` — час і місце в Hall of Fame (`leaderboard`); `stats-window`.
- Переходи: вибір розміру → game-screen → Done → end-screen → New Puzzle.

## Фічі поза полем
- `difficulty-presets` за розміром і складністю; `daily-puzzle`/weekly/monthly; `leaderboard-online` (Hall of Fame), `stats`.
- `auto-check` (опції підсвітки помилок), `pencil-marks` з `auto-pencil` (автозаповнення кандидатів) і автоприбиранням.
- `share-code`: ID пазла і «permalink прогресу»; «Specific puzzle» — відкрити за ID; друк і масовий друк.
- `undo` (?) — на сайтах зазвичай є; «Start Over» — рестарт.

## Варіації й родичі
- **Killer Sudoku** (Nishio, The Times 2005): ті самі суми без повторів, але клітки довільної форми поверх повного судоку — правило «45» (innies/outies) — прямий аналог «бокс»-техніки Kakuro.
- Cross Sums у вигляді кросворда з нумерованими входами і окремим списком підказок; Kakurasu (сума індексів зачорнених клітин); Keen/KenKen — латинський квадрат із клітками +−×÷.
- **Осі варіацій**: операція підказки (сума / добуток / будь-яка арифметика) · домен цифр (1–9 / з нулем / більші числа (?)) · форма групи (прямий прогін / довільна клітка) · чи є додаткове латинське обмеження (Killer — так, Kakuro — ні).

## Цікавинки для курсу
- Таблиця розкладів «сума × довжина → набори різних цифр» (генерація рекурсією/бітмасками) — 📎.
- Перевірка валідності прогонів (дубль, сума, рання «переповненість») з підсвіткою — 🥉 (`markup-validity` у двох напрямках).
- Помічник комбінацій + автопрополювання кандидатів після вводу — 🥉.
- Солвер: поширення обмежень по прогонах + бектрекінг; кандидати як бітмаски — 🥇.
- Генератор: спершу заповнити білу сітку цифрами без повторів, потім обчислити суми й перевірити єдиність розвʼязку — 👑 (картка `unique-puzzle-generation`), окремо 🥈 генерація форми сітки (симетрична, прогони ≥2).
- Парсер Kakuro-формату (блоки з «across\down») — 📎.

## Мапа на каталог
- Є: `satisfy-constraints` · `markup-validity` (дубль/сума) · `completion-detection` · `cell-click` · `keyboard-controls` · `pencil-marks` · `hover-highlight` (рядок/стовпець/підказки) · `unique-puzzle-generation` · `difficulty-levels` · `difficulty-rating` · `level-solver` · `daily-puzzle` · `field-size-picker` · `level-from-txt`.
- **Нема** → пропозиції карток:
  - `+undo-redo` (уже є в корпусі).
  - `+sum-clue` «Підказка-сума групи клітин» · game-logic/constraints · 📎 · слот {group: run|cage, op: sum|product} — Kakuro, Killer Sudoku, Keen; узагальнення `+killer-cage` (sudoku-variants).
  - `+combination-helper` «Помічник розкладів суми» · interface/hud · 📎.
  - `+auto-candidates` (є в sudoku) — автонотатки й автоприбирання (дитина `pencil-marks`).
  - `+seed-share` (уже пропоновано в tatham-collection) — ID пазла / Specific puzzle.

## Пропозиції до словників
- `+trigger:input`, `+trigger:constraint_broken`, `+trigger:all_constraints_met` — ядро пазла.
- `+effect:set_value` (цифра в клітині), `+effect:mark` (кандидат олівцем).
- `+cond:sum_eq(group, n)` — сума значень групи дорівнює N (Kakuro, Killer, Keen); без неї обмеження доводиться писати текстом.
- `+role:mark` (цифра, кандидат), `+role:zone` (прогін).
- `+ui:pencil-marks`, `+ui:conflict-highlight`, `+ui:combination-helper` — панель наборів цифр; `+ui:number-pad` — екранна панель цифр 1–9 (тач).
- `+feature:auto-check`, `+feature:daily-puzzle`.

## Джерела
- ⭐ [Wikipedia: Kakuro](https://en.wikipedia.org/wiki/Kakuro) — правила, позначення «clue-in-length», техніки (комбінаторика, бокс), NP-повнота, історія Dell 1966.
- [Nikoli: Kakuro](https://www.nikoli.co.jp/en/puzzles/kakuro/) — три правила від видавця, перша поява в Nikoli Vol. 11.
- [puzzle-kakuro.com](https://www.puzzle-kakuro.com/) — цифрова версія: розміри, pencil, помічник комбінацій, підсвітки, daily, Hall of Fame.
- [Wikipedia: Killer sudoku](https://en.wikipedia.org/wiki/Killer_sudoku) — родич: клітки-суми поверх судоку, правило 45.
- YouTube: [пошук «kakuro how to solve»](https://www.youtube.com/results?search_query=kakuro+how+to+solve).

## Непевне
- (?) Рання підсвітка «сума вже перевищена» до заповнення прогону — залежить від реалізації, не перевіряв.
- (?) Заборона повторного набору цифр у двох прогонах — згадано як правило «деяких видавців» (Wikipedia), конкретних не знайшов.
- (?) Undo на puzzle-kakuro.com — на сторінці не згадано явно.
- (?) Рік 1966 — дата назви «Cross Sums» у Dell (Wikipedia); японська історія Nikoli (Vol. 11) — без року.
