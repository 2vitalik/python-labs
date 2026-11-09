---
title: Str8ts (Стрейтс)
slug: str8ts
aka: [Straights, Mini Str8ts, Asymmetrical Str8ts, B-Str8ts, Стрейтс]
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
year: 2008
platforms: [paper, web, mobile, board]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Str8ts", best: true, note: "правила, Jeff Widderich + Andrew Stuart, 2008, compartments і straights, варіанти"}
  - {kind: official, url: "https://www.str8ts.com/", note: "щоденні Mini / Str8ts / Asymmetrical, Weekly Extreme, розвʼязувач, стратегії, застосунок"}
  - {kind: other, url: "https://www.str8ts.com/str8ts", note: "How to Play: три правила, приклади straights, коментарі автора про чорні підказки"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=str8ts+how+to+solve", note: "пошук; розвʼязання"}
stage: v1
coverage: 65
mechanics: [markup-validity, completion-detection, satisfy-constraints, cell-click, keyboard-controls, pencil-marks, conflict-highlight, difficulty-levels, difficulty-rating, level-solver, daily-puzzle, level-bank, undo-redo, +auto-candidates, +straight-compartment, +blocked-digit-clue]
proposes: ["+cond:consecutive_set(cells)", "+cond:duplicate_in_line", "+card:straight-compartment", "+card:blocked-digit-clue", "+feature:step-solver"]
author: opus
date: 2026-11-09
---

# Str8ts — чорні клітинки ділять рядки й стовпці на відсіки, і кожен відсік — «стрит» послідовних цифр у будь-якому порядку

## Суть
Сітка 9×9 (стандарт) частково розбита чорними клітинками на **відсіки** (compartments) — неперервні відрізки білих клітинок у рядку чи стовпці. Гравець вписує цифри 1…9 у білі клітинки: цифри не повторюються в рядку й стовпці (як у судоку, але без блоків 3×3), а кожен відсік по горизонталі й вертикалі утворює **стрит** — набір без пропусків у будь-якому порядку ([6,8,7], [3,2,4,5]). Чорні клітинки з цифрою прибирають цю цифру з рядка і стовпця, але в стрити не входять.

## Поле і час
- Квадратна сітка n×n, цифри 1…n; стандарт 9×9, Mini — менша (Wikipedia: «1 to n»).
- Типи клітинок: біла (заповнює гравець або дана) · чорна порожня · чорна з цифрою.
- Відсік — максимальний неперервний відрізок білих клітинок у рядку або стовпці; кожна біла клітинка належить двом відсікам (горизонтальному і вертикальному).
- Шари: чорна маска і чорні підказки · дані білі цифри · цифри гравця · кандидати.
- Час статичний; хід = вписати/стерти цифру чи кандидата.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Біла клітинка | mark | цифра 1…n або порожньо; кандидати | рахується в рядку, стовпці і двох відсіках |
| Дана біла цифра | mark | d | закріплена |
| Чорна клітинка | static | — | розриває рядок/стовпець на відсіки; не заповнюється |
| Чорна клітинка з цифрою | static | d | d заборонена у її рядку і стовпці; не входить у стрит |
| Відсік (compartment) | zone | довжина L | L послідовних цифр у будь-якому порядку |
| Рядок / стовпець | zone | n | без повторів (крізь усі відсіки й чорні підказки) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(click, cell)` + `input(key_digit)` → ЯКЩО `cell(cell, white)` and `free(cell)` → ТО `set_value(cell, d)` (цифрова версія).
- КОЛИ `input(pencil, cell)` → ТО `mark(cell, candidate d)` (цифрова версія).
- КОЛИ `input(click, black_cell)` → ТО `block` — чорні клітинки не редагуються (цифрова версія, ?).
- Рядок/стовпець: ЯКЩО `unique(row)` and `unique(col)` → задоволено; чорна цифра рахується як зайнята в рядку і стовпці.
- КОЛИ `constraint_broken(line)` → ЯКЩО `custom: «цифра повторюється в рядку чи стовпці або збігається з чорною підказкою»` (`+cond:duplicate_in_line`) → ТО конфлікт.
- Відсік: ЯКЩО `custom: «цифри відсіку утворюють набір послідовних чисел без пропусків»` (`+cond:consecutive_set`) → стрит задоволений.
- КОЛИ `constraint_broken(straight)` → ЯКЩО `custom: «відсік заповнено, але є пропуск (1, 3, 8, 7)»` → ТО конфлікт.
- КОЛИ `all_constraints_met` → ЯКЩО `cover_all(white_cells)` → ТО `win`.
- Дедукція «діапазон відсіку»: відсік довжини L з відомою цифрою x може містити лише цифри з [x−L+1, x+L−1]; що поза ним — викреслити.
- Дедукція «обовʼязкові цифри»: якщо всі можливі стрити відсіку містять цифру c, то c заборонена в решті рядка поза відсіком («Sure candidates»/Stranded, ?).
- Дедукція «розрив»: кандидат, від якого до решти кандидатів відсіку є пропуск ≥ L, неможливий.
- Дедукції судоку: naked/hidden singles і пари в рядку/стовпці; на сайті — Unique Rectangle, Setti, «B-Str8ts» стратегії.
- Перемога: усі білі клітинки заповнені, рядки/стовпці без повторів, кожен відсік — стрит. Поразки й рахунку нема.

## Керування і ввід
- Паперова гра; дерев'яна настільна версія (серпень 2010, Wikipedia).
- Цифрова версія (сайт, iOS-застосунок з 2009): клік по білій клітинці + цифра; режим кандидатів; покроковий розвʼязувач на сайті.

## Вікна, меню, HUD
- `game-screen` (цифрова версія): сітка з чорною маскою, чорні підказки (світлі цифри на чорному), цифри, `pencil-marks`, `conflict-highlight` (?).
- `daily-window` — щоденні Mini Str8ts, Str8ts, Asymmetrical Str8ts; оновлення опівночі EST (str8ts.com).
- `puzzle-select` — Weekly Extreme, архів, книжки.
- `hints-window` / покроковий розвʼязувач — «Step by step solver» (str8ts.com).
- `help-window` — How to Play і сторінки стратегій.
- Застосунок «5 Daily Puzzles» (iPad): 4 Str8ts на день, по одному кожного з чотирьох рівнів.

## Фічі поза полем
- `daily-puzzle`, `mode-daily`; чотири рівні складності (grades) у друкованому і щоденному форматі (str8ts.com).
- `difficulty-presets` — рейтинг за кількістю місць, де «логічна дедукція ставить цифру або викреслює кандидата» (Wikipedia).
- Розвʼязувач і покрокова підказка — `auto-solve`, `hint` (`+feature:step-solver`).
- `localization` — сайт EN/FR/PT/NL/DE/ES.
- Публікації: Süddeutsche Zeitung (з березня 2010), Die Rheinpfalz (з серпня 2010), книжки 2009 і 2010 (Wikipedia).

## Варіації й родичі
- **Symmetric / Asymmetric Str8ts** — симетрія чорної маски; **Mini-Str8ts** — менша сітка; **Transformations**; **B-Str8ts** (стратегії на str8ts.com) — правила варіантів у джерелах не описані.
- Родичі в сімʼї: [Sudoku](sudoku.md) (без повторів у рядку/стовпці), [Kakuro](kakuro.md) (чорні клітинки розбивають ряди на прогони з підказками сум), [KenKen](kenken.md), [Futoshiki](futoshiki.md) (латинський квадрат з іншою підказкою), [Sudoku variants](sudoku-variants.md).
- **Осі варіацій**: розмір (Mini / 9×9) · симетрія маски · підказки на чорних (є / нема) · умова відсіку (стрит / сума як у Kakuro / зростання).

## Цікавинки для курсу
- Розбиття рядків і стовпців на відсіки за чорною маскою — 🌱.
- Перевірка стриту: `max − min = L − 1` і без повторів — 🌱.
- Чорна підказка, що діє на рядок/стовпець, але не входить у стрит — 🌱.
- Кандидати з діапазоном відсіку і «обовʼязковими цифрами» — 🥉.
- Розвʼязувач: судоку-пропагація + діапазони стритів + backtracking; покроковий режим з назвою техніки — 🥇.
- Генератор: маска + латинське заповнення, де кожен відсік — стрит, + мінімізація з єдиністю — 👑.

## Мапа на каталог
- Є: `markup-validity`, `completion-detection`, `satisfy-constraints` · `cell-click`, `keyboard-controls`, `pencil-marks`, `conflict-highlight` · `difficulty-levels`, `difficulty-rating`, `level-solver` · `daily-puzzle`, `level-bank` · `undo-redo`.
- Перевикористано: `+auto-candidates`.
- **Нема** → пропозиції карток:
  - `+straight-compartment` «Відсік між чорними клітинками — набір послідовних цифр у будь-якому порядку» · game-logic/constraints · 📎 · слот {rule: straight|sum|increasing}.
  - `+blocked-digit-clue` «Підказка-заборона: цифра в чорній клітинці виключає себе з рядка і стовпця» · game-logic/constraints · 🌱.

## Пропозиції до словників
- `+cond:consecutive_set(cells)` — значення клітинок утворюють послідовний набір без пропусків.
- `+cond:duplicate_in_line` — повтор з інших файлів.
- `+feature:step-solver` — покроковий розвʼязувач з назвою техніки (str8ts.com, SudokuWiki).
- `+card:straight-compartment`, `+card:blocked-digit-clue` — див. мапу.

## Джерела
- ⭐ [Wikipedia: Str8ts](https://en.wikipedia.org/wiki/Str8ts) — Jeff Widderich (прототип 2007), Andrew Stuart, Nuremberg Toy Fair лютий 2008, compartments/straights, чорні підказки, 9×9 і «1 to n», варіанти, публікації, iOS-застосунок (2009), дерев'яна версія (2010).
- [str8ts.com](https://www.str8ts.com/) — щоденні Mini/Str8ts/Asymmetrical, Weekly Extreme, Str8ts Solver і Step by step solver, стратегії, чотири grades, мови.
- [str8ts.com: How to Play](https://www.str8ts.com/str8ts) — три правила, [6,8,7] / [3,2,4,5], чорні підказки; Andrew Stuart про побудову чорних підказок.
- YouTube: пошук «str8ts how to solve».

## Непевне
- (?) Назви чотирьох рівнів складності — на сайті не побачив.
- (?) Правила варіантів Transformations і B-Str8ts — у джерелах лише назви.
- (?) Розмір Mini Str8ts (6×6?) — не бачив.
- (?) Техніка «Stranded / Sure candidates» — назва з памʼяті; на сайті бачив лише назви Unique Rect. і Setti.
- (?) Чи бувають дані цифри в білих клітинках завжди — Wikipedia прямо не каже, приклади на сайті не читав.
- (?) Поведінка цифрового інтерфейсу (підсвітка конфліктів, режим кандидатів) — не перевіряв.
