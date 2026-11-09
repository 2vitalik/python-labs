---
title: Panex (Toshio Akanuma)
slug: panex
aka: [Panex Puzzle, Panex Silver, Panex Gold]
family: push-slide
also: []
klass: figure
axes:
  field: graph
  time: static
  opponent: none
  info: full
  random: none
  goal: state
year: 1983
platforms: [puzzle, web, Java]
links:
  - {kind: other, url: "https://www.jaapsch.net/puzzles/panex.htm", best: true, note: "Jaap's Puzzle Page: опис, Silver/Gold, розвʼязок через операції T/S/X/Z, лінки на симуляції"}
  - {kind: play, url: "https://www.jaapsch.net/puzzles/javascript/panexj.htm", note: "JavaScript-симуляція Jaap: клік колонка → колонка, Mix/Reset/Edit/Up/Down/Solve/Play/Help"}
  - {kind: other, url: "https://www.cs.brandeis.edu/~storer/JimPuzzles/ZPAGES/zzzPanex.html", note: "J. A. Storer: TRICKS 1983, правила, мінімуми висот 1–4, 3D-друк висот 4 і 5"}
  - {kind: other, url: "http://baxterweb.com/puzzles/panex/", note: "Nick Baxter, Panex Resources: Kisman 2010 — 31 537 ходів, висоти 11–13, статті й програма пошуку"}
  - {kind: other, url: "http://baxterweb.com/puzzles/panex/panex5.pdf", note: "Manasse, Sleator, Wei, Baxter «The Panex Puzzle»: правила, T(n), X(n), BFS-пошук"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=panex+puzzle", note: "пошук; розвʼязок"}
stage: v1
coverage: 75
mechanics: [cell-click, restart-level, field-size-picker, in-game-editor, unsolvable-states, level-solver, help-window, +stack-columns, +depth-limit-by-level, +tower-exchange, +move-vs-step, +random-legal-position]
proposes: ["+cond:top_of", "+cond:max_depth", "+card:stack-columns", "+card:depth-limit-by-level", "+card:tower-exchange", "+card:random-legal-position"]
author: opus
date: 2026-11-09
---

# Panex — дві вежі в трьох жолобах обмінятися місцями, коли жодна плитка не опускається нижче свого поверху

## Суть
Механічна головоломка Тосіо Акануми (TRICKS Co., Токіо, 1983): плоска дошка з трьома вертикальними коліями й горизонтальною колією зверху, у лівій — синя вежа з 10 плиток, у правій — помаранчева. Плитки ковзають колією, не виймаються й не перестрибують одна одну; плитка поверху *i* може стояти лише в шарах 0…*i*, тож на відміну від Ханойської вежі її не можна «сховати» на дно. Мета — обміняти вежі місцями; найкоротший розвʼязок — 31 537 ходів.

## Поле і час
- Три вертикальні колії по 11 позицій (шари 0–10: вежа + одне місце понад неї); шари 0 зʼєднані горизонтальною колією — граф із 33 позицій.
- Обмеження вбудоване в механіку: під кожною плиткою язичок, що зменшується від 1-ї до 10-ї, а горловина колії звужується від шару 1 до шару 10.
- Часу нема (`static`); хід = переміщення однієї плитки, незалежно від того, як далеко й з якими поворотами вона проїхала.
- Узагальнення: вежі висоти *n* (менші версії — нижні 10 − *n* плиток не чіпати); симуляція Jaap — *n* від 2 до 10.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Синя плитка #i | piece | поверх i = 1…10 | ковзає колією; стоїть лише в шарах 0…i; ціль — права колія, свій поверх |
| Помаранчева плитка #i | piece | поверх i = 1…10 | те саме; ціль — ліва колія |
| Вертикальна колія ×3 | static | 11 позицій, горловина звужується вниз | тримає стос; з неї береться лише верхня плитка |
| Горизонтальна колія | static | зʼєднує шари 0 | шлях між колонками; плитки не обганяють одна одну |
| Язичок плитки | static | розмір за поверхом | механічно не пускає плитку нижче шару i |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(click, column_from)` → ТО `custom: «вибрати колонку»`; КОЛИ `input(click, column_to)` → ЯКЩО `custom: «плитка верхня в column_from»` і `free(top_cell(column_to))` → ТО `move(tile, column_to)`, `counter(moves, +1)`.
- КОЛИ `custom: «плитка їде колією»` → ЯКЩО `not path_exists(tile, target_cell)` (на шляху інша плитка) → ТО `block` — перестрибувати не можна.
- КОЛИ `custom: «плитка #i опускається в колонці»` → ЯКЩО `custom: «шар глибший за i»` → ТО `block` (язичок не проходить горловину).
- Порядку розмірів у стосі нема: велику плитку можна класти на малу (на відміну від Ханойської вежі).
- Симуляція Jaap: КОЛИ `custom: «плитка увійшла в колонку»` → ТО `fall(tile)` до найнижчої вільної позиції, яку дозволяє її поверх.
- Мета X (обмін): КОЛИ `all_on(blue, right_column)` і `all_on(orange, left_column)` → ТО `win`, `message(«You solved it! You don't get a prize for this though!»)` (Jaap).
- Мета T (перенос, з літератури): КОЛИ `all_on(blue, center_column)` → ТО `win`.
- КОЛИ `input(edit)` → ТО `custom: «поле очищено, плитки ставляться по черзі: сині від великої до малої, потім помаранчеві»`; КОЛИ `input(click, cell)` → ЯКЩО `custom: «клітина не глибша за поверх плитки»` → ТО `place(tile)`; інакше `message(«That piece must lie in one of the top N rows!»)`.
- КОЛИ `custom: «позицію відредаговано»` → ЯКЩО `custom: «позиція нерозвʼязна»` → ТО `message(«This position is not solvable!»)`.
- КОЛИ `input(mix)` → ТО `custom: «випадкова легальна позиція, не випадкові ходи»`.
- КОЛИ `input(solve)` → ТО `custom: «один хід розвʼязувача»`; КОЛИ `input(play)` → ТО `custom: «усі ходи підряд, повтор — пауза»`.
- КОЛИ `input(up|down)` → ТО `custom: «висота веж ±1 (2…10)»`, `restart`.
- Перемога: вежі обміняно, кожна плитка на своєму поверсі. · Поразки нема: усі ходи зворотні. · Рахунок: кількість ходів проти мінімуму X(n).

## Керування і ввід
- Фізична дошка: пальцем ковзати плитку колією; кришка тримає плитки всередині.
- Симуляція Jaap: клік по колонці (береться верхня плитка), клік по іншій колонці — плитка переїжджає й опускається; у режимі Edit — клік по клітині ставить наступну плитку.
- Кнопки: Mix, Reset, Edit, Up, Down, Solve, Play, Help.

## Вікна, меню, HUD
- `game-screen` (симуляція Jaap): зображення дошки з трьома колонками й плитками; під ним два ряди кнопок.
- `help-window` — модальне вікно Help: мета, правило рівнів, керування, опис кнопок.
- `editor-window`-режим на тому ж екрані (Edit): порожня дошка, плитки ставляться по черзі, перевірка допустимих шарів.
- `end-screen` — діалог «You solved it!»; діалог «This solution has N moves.» після розвʼязування.
- Переходи: game-screen → Help → назад; Edit → розстановка → Edit (вихід) → перевірка розвʼязності.

## Фічі поза полем
- `custom-difficulty`: висота веж 2…10 кнопками Up/Down.
- `auto-solve` / `show-solution`: Solve — по одному ходу, Play — автопрогравання з паузою; розвʼязувач Jaap не оптимальний, але розвʼязує будь-яку позицію.
- `level-editor`: довільна легальна позиція з перевіркою розвʼязності; `restart-level` (Reset); Mix — випадкова позиція.
- Інші симуляції: аплет David Bagley (Java), Cheesy Games (висота 4, без розвʼязувача), Paul's PC Repair (з C-кодом), програма пошуку Manasse–Sleator–Wei.

## Варіації й родичі
- Panex Silver — плитки з синіми/помаранчевими мітками, що складаються у вузький трикутник (поверх видно одразу); Panex Gold — усі плитки вежі виглядають однаково (сіра й коричнева), той самий механізм.
- Інші назви від Storer: Panex Towers, Panex Junior, Panex Junior Towers; варіації Oscar van Deventer — Panex Galaxy, Panex Duo; 3D-друк Storer — висоти 4 і 5.
- Розміри (T — перенос однієї вежі в центр, X — обмін; U/L — верхня й нижня оцінка обміну):

| n | T(n) | X(n) | U(n) | L(n) |
|---|---|---|---|---|
| 1 | 1 | 3 | | |
| 2 | 3 | 13 | | |
| 3 | 9 | 42 | | |
| 4 | 24 | 128 | | |
| 5 | 58 | 343 | 343 | 320 |
| 6 | 143 | 881 | 881 | 796 |
| 7 | 345 | 2 189 | 2 189 | 1 944 |
| 8 | 836 | 5 359 | 5 359 | 4 716 |
| 9 | 2 018 | — | 13 023 | 11 408 |
| 10 | 4 875 | — | 31 537 | 27 564 |

- Derek Kisman (2010): 31 537 для n = 10 — оптимум; n = 11, 12, 13 — 76 245, 184 191, 444 807 ходів.
- Осі варіацій «стос у колонках»: менше на більшому (Ханойська вежа) / будь-який порядок, але глибина за поверхом (Panex); мета: перенести одну вежу / обміняти дві; вигляд: мітки поверху (Silver) / однакові плитки (Gold).
- Родичі: `sliding-tile-permutation`, `train-shunting-puzzle` (перестановки колією), `klotski`.

## Цікавинки для курсу
- Модель Panex: 3 колонки × 11 шарів, верхня плитка, обмеження глибини за поверхом — 📎.
- BFS-розвʼязувач для малих висот (n ≤ 4: до 128 ходів) — 🥈.
- Пошук Manasse–Sleator–Wei: BFS без зберігання графа (три списки поколінь у хеш-таблиці), пошук з двох кінців і зведення за симетріями «дзеркало + обмін кольорів» — 🥇.
- Рекурсивний алгоритм T(n) через T(n−1), S(n−1) і T(n−2), як у Ханойській вежі — 🥇.
- Редактор позицій із перевіркою допустимих шарів і розвʼязності — 📎.
- Генератор випадкової **легальної** позиції (а не випадкових ходів) — 📎.
- Оптимум X(10) = 31 537 (Kisman) — 👑.

## Мапа на каталог
- Є: `cell-click` ↔ клік по колонці; `restart-level` ↔ Reset; `field-size-picker` ↔ Up/Down; `in-game-editor` ↔ Edit; `unsolvable-states` ↔ «This position is not solvable!»; `level-solver` ↔ Solve/Play; `help-window` ↔ Help.
- **Нема** → пропозиції карток:
  - `+stack-columns` «Колонки-стоси: береться лише верхня фігура» · entities/legality · 🌱 — Ханойська вежа, Panex.
  - `+depth-limit-by-level` «Фігура не опускається нижче свого рівня» · entities/legality · 📎.
  - `+tower-exchange` «Обміняти два стоси через третій» · game-logic/win · 🌱.
  - `+move-vs-step` (вже пропонована Rush Hour) — хід = переміщення фігури будь-якої довжини.
  - `+random-legal-position` «Випадкова легальна позиція замість випадкових ходів» · levels/generation · 📎.

## Пропозиції до словників
- `+cond:top_of` — фігура верхня в стосі/колонці (Panex, Ханойська вежа).
- `+cond:max_depth` — шар/клітина не глибше за дозволений рівень фігури.
- `+card:stack-columns` · `+card:depth-limit-by-level` · `+card:tower-exchange` · `+card:random-legal-position` — див. «Мапа на каталог».

## Джерела
- ⭐ [Jaap's Puzzle Page: Panex](https://www.jaapsch.net/puzzles/panex.htm) — опис, Silver і Gold, розвʼязок операціями T/S/X/Z, лінки на симуляції Baxter, Bagley, Paul's PC Repair, Cheesy Games.
- [Jaap: JavaScript Panex](https://www.jaapsch.net/puzzles/javascript/panexj.htm) — сирці симуляції: Help, кнопки, висота 2…10, правило падіння плитки, перевірка редактора й розвʼязності.
- [Manasse, Sleator, Wei, Baxter: The Panex Puzzle (PDF)](http://baxterweb.com/puzzles/panex/panex5.pdf) — два правила, шари 0…i, язичок і горловина, цілі T і X, «хід = переміщення плитки», таблиця T/X/U/L, програма пошуку (VAX 11/750: X5 — година, X6 — менше доби, X7 — не вмістився).
- [J. A. Storer: Panex](https://www.cs.brandeis.edu/~storer/JimPuzzles/ZPAGES/zzzPanex.html) — TRICKS 1983, «можна класти на меншу», мінімуми висот 1–4, Kisman 2010, 3D-друк.
- [Nick Baxter: Panex Resources](http://baxterweb.com/puzzles/panex/) — Kisman 21.11.2010, висоти 11–13, Bagley перевірив оптимальність до 9.
- YouTube: пошук «panex puzzle».

## Непевне
- (?) Чи може плитка з лівої колонки пройти в праву, коли шар 0 центральної зайнятий: стаття каже «не перелітають одна одну», а симуляція Jaap перевіряє лише цільову колонку (для центру — шари 0 і 1).
- (?) У фізичній дошці плитка може зупинитись на будь-якому дозволеному шарі; у симуляції Jaap вона завжди падає донизу — чи впливає це на мінімуми, не перевірено.
- (?) Таблиці Jaap (5, 16, 50, 140, 366 ходів для n = 1…5) розходяться з X(n) статті (3, 13, 42, 128, 343) — імовірно, це ходи його методу, а не мінімуми.
- (?) Panex Towers / Junior / Junior Towers, Galaxy, Duo — лише назви, правила не дивився.
