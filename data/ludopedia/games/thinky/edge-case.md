---
title: Edge Case
slug: edge-case
aka: []
family: thinky
also: [push-slide, connect-rotate]
klass: hybrid
axes:
  field: graph
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2021
platforms: [web]
links:
  - {kind: itch, url: "https://parachor.itch.io/edgecase", best: true, note: "грати в браузері; 22 рівні; сесія «about a half-hour» за itch; Esc — меню й вибір рівня"}
  - {kind: other, url: "https://docs.google.com/spreadsheets/d/1knagib_rnXImRkZ8f6k6tZBEcLRBpwWaXsl2sWUBRps/edit?usp=sharing", note: "таблиця підказок від автора (hint sheet)"}
  - {kind: other, url: "https://auroriax.github.io/PuzzleScript/", note: "PuzzleScript Plus — рушій (flickscreen, вбудований вибір рівня)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Edge+Case+puzzlescript+Parachor", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [move-4dir, move-by-input, keyboard-controls, push-object, impassable-cells, all-on-targets, reach-exit, fill-hole, one-way-cell, button-toggle, teleport, wrap-edges, path-drawing, level-select, sequential-levels, undo-unlimited, restart-level, sound-effects, +glued-edges, +edge-rewiring, +terminal-screen, +pressure-plate, +exit-unlocks-on-goal, +no-crossing-lines, +crossing-pipe-tile, +line-presses-plate, +door-cuts-line]
proposes: ["+cond:edge_linked", "+effect:link", "+effect:unlink", "+role:terminal", "+window:wiring-terminal", "+feature:hint-sheet", "+card:edge-rewiring", "+card:terminal-screen", "+card:line-presses-plate", "+card:door-cuts-line"]
author: opus
date: 2026-11-19
---

# Edge Case — кімнати, чиї краї ти сам склеюєш лініями на схемі терміналу: вийдеш угорі — зайдеш туди, куди підʼєднав

## Суть
PuzzleScript Plus-гра Parachor: бігун штовхає блоки на цілі, щоб відчинити вихід, у кількох кімнатах 9×9. Кожен із чотирьох країв кімнати — портал, але куди він веде, вирішує гравець: на клітині-терміналі X перемикає керування на курсор у схемі, де кожна кімната — кольоровий вузол, а 4 боки вузла — 4 її краї. Лінія від боку одного вузла до боку іншого склеює два краї: вийшов за верхній край у k-й клітині — зайшов з відповідної клітини склеєного краю (склейка «верх–низ» дає тор, «верх–верх» розвертає на 180°). Схема — окремий пазл: лінії не перетинаються (крім хрестовин), підкоряються стрілкам, тиснуть кнопки й накривають цілі, а двері, що зачиняються, стирають лінії. Клас `hybrid`: аватар у кімнатах + курсор-олівець у схемі.

## Поле і час
- Карта рівня 33×22 = 3×2 екрани по 11×11 (`flickscreen 11x11`): ліворуч угорі — червона кімната, праворуч угорі — синя, внизу — жовта й зелена, вгорі посередині — схема терміналу, внизу посередині — службовий екран (таблиця склейок і лічильники, гравець його не бачить). Камера показує екран, де зараз гравець, — одну кімнату або схему.
- Кімната — 9×9 разом зі стінами кольору кімнати; довкола — смуга країв (4 краї по 9 клітин), у кутах — службові позначки. Рівні 1–6 — лише червона кімната; синя зʼявляється з 7-го, зелена — з 13-го, жовта — лише в 20–22, де задіяні всі чотири (з коду).
- Склейка країв (з коду): кожен край нумерується за годинниковою стрілкою (верх — зліва направо, правий — згори вниз, низ — справа наліво, лівий — знизу вгору); вихід у позиції k (1–9) веде в позицію 10−k склеєного краю, і обʼєкт робить крок усередину. Отже кожна склейка — поворот на 0/90/180/270° без дзеркала.
- Покроково: хід — крок, поштовх або дія X; стирання лінії й телепорт іде анімацією `again` без участі гравця. Таймерів нема; видно все, але по одному екрану — автор радить папір і олівець.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Бігун | player | у кімнаті / схований біля терміналу | рух 4 напрямки; штовхає один блок; виходить за край кімнати крізь склейку |
| Блок | object | — | штовхається на 1 (ланцюга нема); проходить склейки, як бігун; дає вагу кнопці й цілі; у дірці стає підлогою; у схемі його штовхає олівець, на лінію — не можна |
| Стіна | static | колір кімнати | непрохідна |
| Край кімнати | zone | 4 краї × 9 клітин | ступив на край → телепорт за склейкою; край без склейки не пускає |
| Дірка | terrain | — | бігун не входить; блок засипає її |
| Ціль | zone | у кімнаті або в схемі | потребує ваги: блок або лінія |
| Вихід | gate | зачинений / відчинений | відчинений, коли всі цілі під вагою; бігун на відчиненому — перемога |
| Кнопка 1/2/3 | switch | канал | двері каналу відчинені, доки на всіх кнопках каналу є вага (блок або лінія) |
| Двері 1/2/3 | gate | канал; стан | зачинені — непрохідні; не зачиняються на бігуні, блоці чи олівці; зачиняючись на лінії, стирають її |
| Стрілка | terrain | напрямок | не пускає рух проти себе — бігуна, блок і олівець |
| Термінал | switch | — | бігун на ньому + X → керування переходить до курсора схеми |
| Курсор схеми | player | білий | ходить вільно в межах схеми; X на вузлі — стати олівцем; X на лінії — стерти її; X на виході внизу схеми — повернутися до бігуна |
| Олівець | player | колір стартового вузла | кожен крок лишає відрізок лінії; лише по доріжках схеми; не назад; X — скасувати всю лінію |
| Вузол R/B/G/Y | source | колір = кімната; 4 боки = 4 краї | старт і фініш лінії; бік виходу чи входу визначає край |
| Лінія | conduit | відрізки, колір | склейка двох країв; вага для кнопок і цілей у схемі |
| Хрестовина | terrain | — | єдина клітина, де лінія перетинає іншу, і лише навхрест |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next_cell)` → ТО `move(walker, dir)`.
- КОЛИ `contact(walker, block)` → ЯКЩО `free(cell_behind)` → ТО `push`; інакше `block`.
- КОЛИ `input(dir)` → ЯКЩО `cell(next_cell, hole)` → ТО `block`.
- КОЛИ `enter(block, hole)` → ТО `disappear(block)`, `set_cell(hole, floor)`.
- КОЛИ `input(dir)` → ЯКЩО `cell(next_cell, oneway_against)` → ТО `block` — для бігуна, блоку й олівця.
- КОЛИ `edge(obj)` (бігун чи блок ступив на край) → ЯКЩО `not custom: «край склеєний»` → ТО `block`.
- КОЛИ `edge(obj)` → ЯКЩО `custom: «край склеєний»` and `free(entry_cell)` → ТО `teleport(obj, позиція 10−k склеєного краю)`, `move(obj, inward)`; якщо прибуває бігун, а на вхідній клітині блок і за ним вільно, — `push` блока (блок у блок не заходить).
- КОЛИ `edge(obj)` → ЯКЩО `cell(entry_cell, wall|closed_door|oneway_against)` or (`occupied(entry_cell, block)` and `not free(cell_behind_block)`) → ТО `block` — увесь хід скасовано.
- КОЛИ `input(X)` → ЯКЩО `occupied(walker_cell, terminal)` → ТО `set_state(walker, hidden)`, `spawn_at(cursor, центр схеми)`, `camera(schematic)`.
- КОЛИ `input(X)` → ЯКЩО `occupied(cursor_cell, node)` → ТО `transform(cursor, pen)` кольору вузла.
- КОЛИ `leave(pen, node)` → ТО `set_state(link_start, край кімнати вузла з боку виходу)`.
- КОЛИ `input(dir)` (олівець) → ЯКЩО `cell(next_cell, path)` and `not occupied(next_cell, line)` (хрестовина — лише навхрест) → ТО `move(pen, dir)`, `mark(cell, line_segment)`; назад на свою попередню клітину — `block`.
- КОЛИ `contact(pen, block)` → ЯКЩО `free(cell_behind)` and `not occupied(cell_behind, line)` → ТО `push`.
- КОЛИ `enter(pen, node)` → ТО `custom: «склеїти стартовий край із краєм цього вузла з боку входу»`, `transform(pen, cursor)`, `sound(link)`.
- КОЛИ `input(X)` (олівець) → ТО `unmark(line)` анімацією, `transform(pen, cursor)`.
- КОЛИ `input(X)` → ЯКЩО `occupied(cursor_cell, line)` → ТО `unmark(line)`, `custom: «розірвати склейку»`.
- КОЛИ `input(X)` → ЯКЩО `occupied(cursor_cell, schematic_exit)` → ТО `disappear(cursor)`, `clear_state(walker, hidden)`, `camera(room)`.
- КОЛИ `turn_end(player)` → ЯКЩО `count(unweighted_button_N, ==, 0)` → ТО `set_state(door_N, open)`; інакше `set_state(door_N, closed)` (крім дверей, на яких стоїть бігун, блок чи олівець).
- КОЛИ `state_on(door, closed)` → ЯКЩО `occupied(door, line)` → ТО `unmark(line)` — склейка рветься.
- КОЛИ `turn_end(player)` → ЯКЩО `count(unweighted_target, ==, 0)` → ТО `set_state(exit, open)`; інакше `set_state(exit, closed)`.
- КОЛИ `enter(walker, exit)` → ЯКЩО `state(exit, open)` → ТО `win`, `next_level`.
- КОЛИ `input(Z)` → ТО `undo(1)`.
- КОЛИ `input(R)` → ТО `restart`.
- Перемога: бігун на відчиненому виході. · Поразки нема (глухий кут — undo/рестарт). · Рахунку нема.

## Керування і ввід
- Стрілки — крок бігуна, курсора чи олівця (залежно від того, хто активний); X — дія: увійти в термінал, взяти вузол, стерти лінію, скасувати малювання, вийти зі схеми (`norepeat_action`).
- Z — undo, R — рестарт, Esc — меню й вибір рівня (опис на itch); лише клавіатура.
- Лінію малюють кроками курсора, не мишею; виправити — X (скасувати) або стерти й намалювати знову.

## Вікна, меню, HUD
- `main-menu` — титул «EDGE CASE» (PuzzleScript Plus).
- `level-select` — вбудований вибір рівня (з оновлення квітня 2022, раніше — GameBar Pedro PSI).
- `custom-window` — картки «N — НАЗВА» (STARTUP, PRELIMINARY, WORKAROUND … RACETRACK) і підказки «Press [X] to access terminals», «Use terminals to connect the room's edges».
- `game-screen` — кадр 11×11 з однією кімнатою; HUD нема.
- `custom-window` схема терміналу — окремий екран рівня з вузлами, доріжками, хрестовинами, стрілками, кнопками й дверима (`+window:wiring-terminal`).
- Переходи: титул → вибір рівня → картка → кімната ⇄ схема (X на терміналі / X на виході схеми) → відчинений вихід → наступна картка.

## Фічі поза полем
- `levels-sequential` (22 рівні, зростання складності) + `level-select` з меню Esc; `undo` без ліміту; `restart-level`; автозбереження (стандарт рушія).
- Підказки — поза грою: таблиця від автора (`+feature:hint-sheet`).
- Звуки: поштовх, склейка, стирання, вхід і вихід з терміналу, телепорт, перемога.
- Оновлення: жовтень 2021 — правки рівнів і полегшення WAREHOUSE; квітень 2022 — рушій PuzzleScript Plus із вбудованим вибором рівня. У коді лишились закоментовані чернетки («Unfinished 4-node concept», стара WAREHOUSE).

## Варіації й родичі
- Родичі в корпусі: [Gridmount](gridmount.md) (`+glued-edges`), [Toroban](toroban.md) (тор), [Patrick's Parabox](patricks-parabox.md) (нестандартна суміжність), [All the Gold in Fort Locks](all-the-gold-in-fort-locks.md) (повʼязані копії кімнат), [ZZT](../maze-arcade/zzt.md) (вихід за край → інша дошка), [Flow Free](../connect-rotate/flow-free.md) і [Cosmic Express](../connect-rotate/cosmic-express.md) (малювання ліній без перетинів).
- Осі варіацій:
  - **хто задає склейку країв**: ніхто — тор (Pac-Man) / дизайнер (ZZT, Gridmount) / гравець під час рівня (тут);
  - **орієнтація склейки**: лише перенос / поворот на 90°·k (тут) / дзеркало;
  - **що проходить крізь край**: лише аватар / аватар і блоки (тут);
  - **як задають склейку**: меню / лінія на схемі з власними перешкодами (тут).

## Цікавинки для курсу
- Склейка країв кімнати з позицією k → 10−k і кроком усередину: тор, розворот, поворот на 90° однією формулою — 🥈.
- Склейка, яку гравець перемикає під час гри (таблиця «край → край», симетрична) — 🥉.
- Схема як другий пазл: малювання лінії кроками, заборона перетину крім хрестовин, навхрест — 🥉.
- Лінія як вага на кнопці й цілі, двері, що стирають лінію, зачиняючись: звʼязок двох екранів через спільні канали — 🥈.
- Скасування телепорту, коли вхід зайнятий, і поштовх блока на вході — 📎.
- Розвʼязувач: стан = позиції бігуна й блоків + таблиця склейок (до 16 країв) + лінії схеми — 👑 (простір станів вибухає через схему).

## Мапа на каталог
- Є: `move-4dir` · `move-by-input` · `keyboard-controls` ↔ крок; `push-object` ↔ блоки; `impassable-cells` ↔ стіни; `all-on-targets` + `reach-exit` ↔ цілі відчиняють вихід; `fill-hole` ↔ дірки; `one-way-cell` ↔ стрілки; `button-toggle` ↔ кнопки й двері каналів; `teleport` ↔ краї-портали; `wrap-edges` ↔ склейка «верх–низ» однієї кімнати; `path-drawing` ↔ лінії схеми (клавіатурою); `level-select` · `sequential-levels` · `undo-unlimited` · `restart-level` · `sound-effects`.
- **Нема** → пропозиції карток:
  - `+edge-rewiring` «Гравець сам склеює краї кімнат» · entities/move · 🥇 · слоти {rooms: 1..4, rotation: on} — дитина `+glued-edges`.
  - `+terminal-screen` «Термінал перемикає керування на окремий екран-схему» · interface/input · 📎.
  - `+line-presses-plate` «Намальована лінія — вага для кнопки чи цілі» · entities/interact · 📎.
  - `+door-cuts-line` «Двері, що зачиняються, стирають лінію» · entities/interact · 🌱.
  - `+glued-edges` · `+pressure-plate` · `+exit-unlocks-on-goal` · `+no-crossing-lines` · `+crossing-pipe-tile` — вже в корпусі.

## Пропозиції до словників
- `+cond:edge_linked` — край кімнати має склейку (тут `custom: «край склеєний»`).
- `+effect:link` — склеїти два краї (тут `custom: «склеїти стартовий край…»`); `+effect:unlink` — розірвати склейку.
- `+role:terminal` — клітина, що перемикає керування на інший екран.
- `+window:wiring-terminal` — екран-схема для перепідключення світу.
- `+feature:hint-sheet` — підказки окремою таблицею поза грою.
- `+card:edge-rewiring`, `+card:terminal-screen`, `+card:line-presses-plate`, `+card:door-cuts-line` — див. «Мапа на каталог».
- ⏳-слова, вжиті тут: `input`, `edge`, `leave`, `state_on`, `turn_end`, `count`, `teleport`, `camera`, `spawn_at`, `transform`, `mark`, `unmark`, `set_state`, `clear_state`, `set_cell`, `sound`.

## Джерела
- ⭐ [itch: EDGE CASE](https://parachor.itch.io/edgecase) — опис («navigating, linking and altering the game world», 22 рівні, папір і олівець, Esc — меню й вибір рівня), історія оновлень, теги, коментарі гравців; вихідний код узято з HTML вбудованої гри (`sourceCode`): OBJECTS, LEGEND, COLLISIONLAYERS, RULES (кнопки, двері, склейки, телепорт із лічильником позиції, малювання й стирання ліній), 22 рівні.
- [Hint sheet](https://docs.google.com/spreadsheets/d/1knagib_rnXImRkZ8f6k6tZBEcLRBpwWaXsl2sWUBRps/edit?usp=sharing) — таблиця підказок автора (відкривається, зміст не читали).
- [PuzzleScript Plus](https://auroriax.github.io/PuzzleScript/) — рушій.
- YouTube: [пошук](https://www.youtube.com/results?search_query=Edge+Case+puzzlescript+Parachor).

## Непевне
- (?) Формула склейки (k → 10−k, поворот без дзеркала) виведена з правил лічильника в коді, у грі не перевірена.
- (?) Чи можна почати й закінчити лінію на тому самому вузлі (склейка двох країв однієї кімнати) — з коду так, якщо доріжки схеми дозволяють обійти вузол.
- (?) Вибір рівня: у прелюдії є `level_select` без `level_select_lock` — схоже, усі 22 рівні відкриті одразу.
- (?) Точна дата виходу: 2021 (за приміткою «Oct 2021 Update»); дату публікації сторінка не показує.
