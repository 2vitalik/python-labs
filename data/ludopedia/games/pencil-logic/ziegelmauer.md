---
title: Ziegelmauer (Bricks, Цегляна стіна)
slug: ziegelmauer
aka: [Bricks, Brick Wall, Sudoku-Mauer, Brick Sudoku, Цегляна стіна]
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
year: null
platforms: [paper, web]
links:
  - {kind: other, url: "https://www.janko.at/Raetsel/Ziegelmauer/index.htm", best: true, note: "Janko: правила DE/EN, назви, 210 пазлів 6×6/8×8, рейтинг 1–8, приклад з розвʼязком"}
  - {kind: play, url: "https://www.janko.at/Raetsel/Ziegelmauer/001.a.htm", note: "грати в браузері (applet Bricks.js); у коді сторінки — [problem], [solution], [moves]"}
  - {kind: other, url: "https://www.janko.at/Raetsel/Ziegelmauer/Bedienung.htm", note: "керування applet-ом Janko: меню значень, кандидати F7, помилки F6, undo, підказка F3, розвʼязок F4"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=brick+sudoku+ziegelmauer+puzzle", note: "пошук; розвʼязання"}
stage: v1
coverage: 65
mechanics: [markup-validity, completion-detection, satisfy-constraints, cell-click, keyboard-controls, pencil-marks, conflict-highlight, level-bank, level-rating, puzzle-select, help-window, save-game, undo-redo, replay, +latin-square, +parity-domino, +wrap-edges, +hint-reveal, +cell-coloring]
proposes: ["+cond:odd_even_pair(a, b)", "+card:parity-domino", "+ui:solved-frame", "+ui:value-popup-menu", "+window:puzzle-info"]
author: opus
date: 2026-11-09
---

# Ziegelmauer (Bricks) — латинський квадрат, укладений «цеглою»: у кожній цеглині одне парне й одне непарне число

## Суть
Сітка N×N поділена на горизонтальні «цеглини» по дві клітинки, ряди зсунуті на півцеглини, як у кладці. Гравець вписує 1…N так, щоб кожне число було рівно раз у рядку й стовпці, а в кожній цеглині стояли одне парне й одне непарне. Незвичне: у зсунутому ряду дві крайні півцеглини (ліва й права) вважаються **однією** цеглиною — для цього правила рядок замкнений у кільце.

## Поле і час
- Квадратна сітка N×N; у Janko — 6×6 (93 пазли) і 8×8 (117).
- Цеглини: горизонтальні пари клітинок; ряди чергуються «цілі цеглини / зсув на півцеглини» (так на прикладі правил і в даних пазла №1; яким рядом починається — залежить від пазла).
- Шари: шви цеглин (незмінні) · дані числа (сині) · числа гравця (чорні) · кандидати, символьні й кольорові позначки (applet).
- Час статичний; хід = вписати / стерти число чи позначку.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітинка | mark | 1…N або порожньо; кандидати | одне число |
| Дане число | mark | n, синє | незмінне |
| Цеглина | zone | 2 сусідні клітинки рядка | одне парне + одне непарне |
| Крайова півцеглина | zone | 1 клітинка на краю зсунутого ряду | разом із півцеглиною протилежного краю — одна цеглина |
| Рядок / стовпець | zone | N клітинок | кожне 1…N рівно раз |
| Позначка гравця | mark | символ або колір | лише для гравця; на перевірку не впливає |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left_click, cell)` → ТО `window(+value-popup-menu)`; вибір числа → `set_value(cell, n)`; «•» → `unmark(cell)` (Janko).
- КОЛИ `input(key_digit, cell)` → ТО `set_value(cell, n)`; `0`, `X`, `-`, `,`, Del, ⌫ → `unmark(cell)` (Janko).
- КОЛИ `input(enter|space|ins, cell)` → ТО `set_value(cell, n+1)` — значення по колу (Janko).
- КОЛИ `input(right_click, cell)` → ТО `window(+value-popup-menu)` з позначками → `mark(cell, symbol|color)` (Janko).
- КОЛИ `input(F7)` → ТО `custom: «режим кандидатів: клік редагує список можливих значень клітинки»` (Janko).
- Латинський квадрат: КОЛИ `constraint_broken(latin)` → ЯКЩО `not unique(row)` or `not unique(col)` → ТО конфлікт.
- Цеглина: КОЛИ `constraint_broken(brick)` → ЯКЩО `not custom: «у цеглині одне парне й одне непарне число»` (`+cond:odd_even_pair`) → ТО конфлікт.
- Зшивка країв: ЯКЩО `custom: «ряд зсунутий на півцеглини»` → ТО `custom: «клітинки стовпців 1 і N цього ряду — одна цеглина»`.
- КОЛИ `input(F6)` → ТО `custom: «усі порушення правил — червоним»` (Janko).
- КОЛИ `all_constraints_met` → ТО `custom: «зелена рамка довкола діаграми»` + `win` (Janko).
- КОЛИ `input(F3)` → ТО `custom: «режим підказки: у вибрані далі клітинки ставиться правильне число»` (Janko).
- КОЛИ `input(F4)` → ТО `custom: «вписати розвʼязок, а логічний шлях — у список ходів»` (Janko; дані `[moves]`).
- КОЛИ `input(ctrl_z|pgup)` → ТО `undo(1)`; `input(pos1)` → `undo(all)`; Ctrl+Y / PgDn і End — повернути один / усі (Janko).
- Дедукція «пара»: відома парність однієї клітинки цеглини задає протилежну парність сусідки — кандидати другої ділимо навпіл (наслідок правил).
- Дедукція «кількість»: у рядку N/2 цеглин з одним парним у кожній — рівно стільки ж парних і серед 1…N, тож правило цеглин керує лише **розташуванням** парних, а не їх кількістю (наслідок правил).
- Перемога: латинський квадрат + усі цеглини (і зшиті крайові) змішаної парності · Поразка: — · Рахунок: —.

## Керування і ввід
- Миша (Janko applet): лівий клік — спливне меню чисел (і «•» = стерти); правий клік — меню позначок (символи, кольори).
- Дотик: тап — меню чисел; утримання — меню позначок; два пальці — масштаб і зсув діаграми.
- Клавіатура: стрілки — рамка вибору; Enter / Space / Ins — число +1; цифри — пряме введення; 0 / X / - / , / Del / ⌫ — стерти.
- Наведення миші без кліку + клавіша — введення в клітинку під курсором.
- Символьні маркери Ctrl+Q/W/E/R/X/A/B/C/D; кольори Alt+0…9 (наступні ходи цим кольором) і Ctrl+0…9 (клітинка під рамкою).
- F7 — кандидати; Ctrl+стрілки — масштаб; Alt+стрілки — прокрутка.
- Вибір пазла: випадне меню номера або Ctrl+PgDn / PgUp / Pos1 / End.
- Папір: без JavaScript сторінка показує картинку для друку.

## Вікна, меню, HUD
- `game-screen`: діаграма зі швами цеглин, сині дані й чорні введені числа, кандидати (`pencil-marks`), символи й кольори, `conflict-highlight` (F6), зелена рамка розвʼязку (`+ui:solved-frame`), спливне меню (`+ui:value-popup-menu`).
- `puzzle-select` — індекс Janko: 210 пазлів за датою, розміром, складністю 1–8.
- `help-window` — «Regeln» (приклад + розвʼязок), «Bedienungsanleitung», «Quelle und Copyright» — акордеоном на сторінці пазла.
- `+window:puzzle-info` (F1) — інфо про пазл і лист вебмайстру з поточним станом і ходами.
- Переходи: індекс → сторінка пазла (applet) → Zurück / Weiter між пазлами.

## Фічі поза полем
- `auto-check` (F6) і автовизнання розвʼязку зеленою рамкою.
- `undo` / `redo` по одному й усі; збереження стану Ctrl+S, завантаження Ctrl+L.
- `hint` (F3) — правильне число в обрану клітинку; `show-solution` (F4) — з логічним шляхом у списку ходів.
- `puzzle-bank` — рейтинг 1–8 за часом розвʼязання (1–3 «leicht», 4–8 «schwer»); пазли з відтворюваним логічним шляхом виділено кольором.
- `touch-controls`, масштаб діаграми, друк для паперу. Власні пазли Janko — CC BY-NC-SA 3.0.

## Варіації й родичі
- Назви: Bricks (англомовні країни), Sudoku-Mauer, Brick Sudoku (Sachsentext Уве Відеманна).
- Родичі: [Sudoku](sudoku.md) (латинський квадрат + блоки), Odd/Even у [Sudoku variants](sudoku-variants.md) (парність задана значками), [Takuzu](takuzu.md) (двійкова розмітка з балансом), [Dominosa](dominosa.md) (пари клітинок як доміно), [Магічний і латинський квадрати](magic-latin-squares.md), [Doppelblock](doppelblock.md), [Zahlenlabyrinth](zahlenlabyrinth.md).
- **Осі варіацій**: форма «цеглини» (2 клітинки / довші) · відношення всередині (парне+непарне / сума / різниця) · зсув рядів (кладка / без зсуву) · зшивка країв (так / ні).

## Цікавинки для курсу
- Перевірка латинського квадрата + парності в цеглинах — 🌱.
- Рендер кладки: зсув через рядок і зшиті півцеглини (індекс стовпця по модулю N) — 📎.
- Applet як у Janko: спливне меню значень + кандидати + символи й кольори — 🥉.
- Відтворення логічного шляху з рядка `[moves]` (пари «клітинка, значення») за кнопкою — 📎.
- Розвʼязувач: латинські виключення + поділ кандидатів за парністю + backtracking — 🥇.
- Генератор з єдиним розвʼязком і рейтингом за технікою — 👑.

## Мапа на каталог
- Є: `markup-validity`, `completion-detection`, `satisfy-constraints` · `cell-click`, `keyboard-controls`, `pencil-marks`, `conflict-highlight` · `level-bank`, `level-rating`, `puzzle-select`, `help-window` · `save-game` ↔ Ctrl+S / Ctrl+L · `undo-redo` · `replay` ↔ логічний шлях F4 у списку ходів.
- Перевикористано: `+latin-square`, `+hint-reveal` ↔ F3, `+cell-coloring` ↔ кольорові позначки, `+wrap-edges` ↔ крайові півцеглини зшиваються через край.
- **Нема** → пропозиції карток:
  - `+parity-domino` «Пара клітинок зі змішаною парністю» · game-logic/constraints · 🌱 · слот {shape: brick|domino, rel: odd-even|sum|diff} — Ziegelmauer.

## Пропозиції до словників
- `+cond:odd_even_pair(a, b)` — у парі одне значення парне, інше непарне.
- `+card:parity-domino` — див. мапу.
- `+ui:solved-frame` — повтор (Detektivschach): рамка довкола розвʼязаного поля.
- `+ui:value-popup-menu` — повтор: спливне меню значень біля клітинки.
- `+window:puzzle-info` — повтор: інфо про пазл + лист автору зі станом.

## Джерела
- ⭐ [Janko: Ziegelmauer](https://www.janko.at/Raetsel/Ziegelmauer/index.htm) — правила DE (4 речення) і EN (3), назви, «автор невідомий, можливо, конкурс», 210 пазлів, розміри, рейтинг.
- [Janko: Ziegelmauer №1](https://www.janko.at/Raetsel/Ziegelmauer/001.a.htm) — applet; у коді `puzzle bricks`, `size 6`, `[problem]`, `[solution]`, `[moves]`; автор Otto Janko.
- [Janko: Bedienung](https://www.janko.at/Raetsel/Ziegelmauer/Bedienung.htm) — повне керування applet-ом.
- YouTube: пошук «brick sudoku ziegelmauer puzzle».

## Непевне
- (?) Автор жанру і перша публікація невідомі (Janko: «можливо, конкурс»).
- (?) Чи завжди ряди чергуються «цілі / зсунуті» — бачив лише приклад правил і пазл №1 (у них перший ряд різного типу); позначка `double` у даних пазла не пояснена.
- (?) Чи бувають непарні N (тоді цеглини не лягають рівно) — у Janko лише 6×6 і 8×8.
- (?) Ctrl+S / Ctrl+L — один слот чи кілька — не перевіряв.
- (?) Роль Адольфо Дзанелатті (посилання на сторінці жанру) — автор частини пазлів чи джерело, не зʼясовано.
