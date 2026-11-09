---
title: BomBliss (Tetris 2 + BomBliss, Tetris Blast)
slug: bombliss
aka: [ボンブリス, Tetris 2 + BomBliss, テトリス2+ボンブリス, Tetris Blast, Super Bombliss]
family: falling-match
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: state
year: 1991
platforms: [Famicom, Game Boy, 3DS]
links:
  - {kind: other, url: "https://tetris.wiki/Tetris_2_%2B_Bombliss", best: true, note: "TetrisWiki: поле 10×21, пентаміно й інші поліоміно, таблиця вибухів за рядами, Contest 60 етапів, Puzzle, Construction"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Tetris_2_%2B_BomBliss", note: "повний ряд підриває бомби, ряди без бомб збільшують наступний вибух, 4 бомби квадратом → велика, липка гравітація"}
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/テトリス2+ボンブリス", note: "JA: вибух з центром у бомбі, детонація бомб у зоні, ланцюг додається до рядів, デカボム 10×10, 100 фігур у Contest"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Tetris_Blast", note: "GB 1995 (Super Bombliss): Training, Contest, Fight з комахами, ковзання після приземлення"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Bombliss+famicom+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [gravity-fall, multi-cell-size, keyboard-controls, explode-area, chain-detonation, chain-reaction, move-limit, sequential-levels, progress-acceleration, in-game-editor, mode-select, garbage-attack, simultaneous-versus, +line-counter-blast, +big-bomb-merge, +blast-size-by-lines, +clear-all-goal, +move-limit-puzzle, +cascade-gravity, +polyomino-set-progression, +enemies-in-well]
proposes: ["+card:line-counter-blast", "+card:big-bomb-merge", "+card:blast-size-by-lines"]
author: opus
date: 2026-11-09
---

# BomBliss — Tetris, де повний ряд не зникає, а підриває бомби в ньому, і що більше рядів зібрано — то ширший вибух

## Суть
Друга половина касети Tetris 2 + BomBliss (Chunsoft / BPS, Famicom, 1991): падають поліоміно, в яких частина клітин — бомби. Повний ряд сам не зникає: якщо в ньому є бомба, вона вибухає прямокутником, розмір якого залежить від кількості повних рядів, а ряди без бомб лишаються й «накопичуються» для наступного вибуху. Бомби в зоні вибуху детонують теж, після вибуху незакріплені шматки падають і можуть скласти нові ряди — ланцюг додається до лічильника рядів. Чотири бомби квадратом 2×2 зливаються у велику бомбу на 10×10.

## Поле і час
- Колодязь 10×21 у BomBliss (10×20 у Tetris-режимах) (TetrisWiki).
- Real-time падіння; у Contest гравітація прискорюється кожні три етапи.
- Шари: осілі клітини (звичайні + бомби + великі бомби) + активна фігура; після вибуху — фаза «липкого» осідання й ланцюгів.
- Contest: частина етапів (1–30) — з попередньо розставленими бомбами й клітинами; 31–60 — ті самі розкладки без готових бомб.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Фігура | player | поліоміно 2–5 клітин (пентаміно основні), частина клітин — бомби | зсув, поворот, падіння; hard drop і hold нема |
| Звичайна клітина | tile | — | повний ряд її не прибирає; гине лише в зоні вибуху |
| Бомба | tile | — | вибухає, коли її ряд повний або коли її зачепив інший вибух |
| Велика бомба (デカボム) | tile | 2×2 | з 4 бомб квадратом; вибух 10×10 незалежно від рядів |
| Повний ряд без бомби | zone | — | лишається на полі; рахується в лічильник рядів наступного вибуху |
| Попередньо розставлені клітини й бомби (Contest) | tile | — | частина етапу; мета — прибрати все |
| Комахи-вороги (Tetris Blast, Fight) | enemy | HP (?) | літають колодязем: додають клітини, зʼїдають бомби, додають ряд; шкоду дістають від вибухів і фігур згори |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ЯКЩО `free(cells_below)` → ТО `move(piece, down)`.
- КОЛИ `input(left|right)` → ЯКЩО `free(target)` → ТО `move(piece, dir)`.
- КОЛИ `input(rotate)` → ЯКЩО `free(new_cells)` → ТО `rotate(piece, ±90)`.
- КОЛИ `locked(piece)` → ЯКЩО `custom: «чотири бомби стоять квадратом 2×2»` → ТО `merge(bombs, big_bomb)`.
- КОЛИ `pattern(row_full)` → ЯКЩО `occupied(row, bomb)` → ТО `explode(rect, n)` з центром у бомбі; розмір за кількістю повних рядів L — 1 → 7×1 · 2 → 7×3 · 3 → 7×5 · 4 → 7×7 · 5–6 → 9×9 · 7–8 → 11×11 · 9–10 → 13×13 · 11–12 → 15×15 · 13+ → 17×17.
- КОЛИ `pattern(row_full)` → ЯКЩО `not occupied(row, bomb)` → ТО `counter(full_rows, +1)` — ряд лишається й збільшує наступний вибух.
- КОЛИ `pattern(row_full)` → ЯКЩО `occupied(row, big_bomb)` → ТО `explode(square, 10)`.
- КОЛИ `destroyed(bomb)` → ТО `explode(rect, n)` — бомба в зоні вибуху детонує сама.
- КОЛИ `after(explode)` → ТО `fall(unsupported)` — незʼєднані шматки падають (липка гравітація).
- КОЛИ `settled` → ЯКЩО `chain(n)` → ТО `custom: «довжина ланцюга додається до лічильника рядів для наступного вибуху»`.
- Contest: КОЛИ `all_gone(minoes)` → ТО `win`, `next_level`.
- Contest: КОЛИ `counter(pieces_left, ==, 0)` → ЯКЩО `count(minoes, >, 0)` → ТО `lose`.
- Contest: КОЛИ `custom: «велика бомба або вибух від 4+ рядів»` → ТО `counter(pieces_left, +n)` — +1 за велику бомбу, +2 за 4 ряди, +4 за 5, +10 за 6 … +999 за 19+; запас до 999.
- Contest: КОЛИ `level_start` → ЯКЩО `custom: «етап кратний трьом»` → ТО `speed(piece, +1)`, `custom: «у набір додано дві нові поліоміно»`.
- Puzzle: КОЛИ `all_gone(minoes)` → ЯКЩО `mode(puzzle)` → ТО `win` — заданий набір фігур, без очок.
- Versus: КОЛИ `after(explode)` → ЯКЩО `mode(versus)` → ТО `send_garbage(blocks)` — звичайні клітини в поле суперника.
- Fight (Tetris Blast): КОЛИ `custom: «ворог у зоні вибуху або під фігурою, що впала»` → ТО `damage(enemy, n)`.
- КОЛИ `reach(stack, top)` → ТО `lose`.
- Перемога: Contest/Puzzle — порожній колодязь; versus — задана кількість раундів. · Поразка: скінчились фігури (Contest) або стос дійшов до верху. · Рахунок: Contest — рекорд залишку фігур на етапі; бонус фігурами за великі вибухи.

## Керування і ввід
- Хрестовина ←/→ — зсув, ↓ — прискорення (?), кнопки — поворот у два боки (?); hard drop і hold нема (TetrisWiki).
- Tetris Blast (GB): фігуру можна ковзати й після приземлення.
- Versus — двоє одночасно (FC); GB — Link Cable.

## Вікна, меню, HUD
- `main-menu` — вибір Tetris 2 чи BomBliss на одній касеті.
- `mode-select` BomBliss: Contest · Puzzle · Construction · 2 Player.
- `game-screen`: колодязь; HUD — `remaining-counter` (фігур лишилось у Contest), `level-number` (етап), `next-piece-preview` (?), `score` (?).
- `editor-window` — Construction: створити/редагувати до 10 власних етапів.
- `end-screen` — етап пройдено / Game Over; `credits-window` після першого проходження етапу 30 і 60.
- Переходи: main-menu → mode-select → game-screen → (етап) наступний етап / (поразка) end-screen.

## Фічі поза полем
- Contest: `levels-sequential` 60 етапів, нові поліоміно кожні 3 етапи (до 28 фігур на етапі 33, далі поступово лише пентаміно до етапу 55); рекорди залишку фігур на етап.
- Puzzle: `puzzle-bank` задач із фіксованим набором фігур.
- `level-editor` (Construction, 10 слотів).
- `mode-versus` до 3 перемог; `local-multiplayer`.
- Tetris 2 на тій самій касеті: A-Type марафон, B-Type 30 рівнів × 6 висот сміття, C-Type зі сміттям, що піднімається за інтервалом — це звичайний Tetris (`tetris`).

## Варіації й родичі
- Tetris Blast (GB, 1995; JP — Super Bombliss): Training (10 швидкостей, без кінця), Contest (напівзаповнений колодязь), Fight (комахи-вороги), ковзання після приземлення; BomBliss Plus — у Tetris для 3DS (сміття швидко, hold).
- Родичі: Tetris (`tetris`, ряд зникає сам), Puzznic/Meteos (каскади), Bomberman (`maze-arcade/bomberman`, вибух хрестом, ланцюгова детонація), Tetrisweeper (бомби в тетрис-полі).
- **Осі варіацій**: що робить повний ряд (зникає / **детонує бомбу** / нічого без бомби) · розмір вибуху (фіксований / **за кількістю рядів** / велика бомба) · гравітація після зчищення (наївна / **липка, шматками**) · мета (очки / **порожній колодязь** з лімітом фігур).

## Цікавинки для курсу
- Вибух прямокутником із центром у бомбі, розмір за таблицею від кількості рядів — 🌱.
- Ланцюгова детонація бомб у зоні (черга вибухів, BFS) — 📎.
- Злиття 4 бомб у квадрат 2×2 у велику бомбу — 🌱.
- Липка гравітація: знайти звʼязні шматки й опустити кожен до опори — 🥉.
- Contest: ліміт фігур із бонусами за великі вибухи + прогресія набору поліоміно — 📎.
- Розвʼязувач Puzzle-задач із фіксованим набором фігур — 🥇.

## Мапа на каталог
- Є: `gravity-fall` · `multi-cell-size` (поліоміно) · `keyboard-controls` · `explode-area` (прямокутник за рядами) · `chain-detonation` (бомба в зоні вибуху) · `chain-reaction` (осідання → нові ряди) · `move-limit` (ліміт фігур Contest) · `sequential-levels` · `progress-acceleration` · `in-game-editor` (Construction) · `mode-select` · `garbage-attack` + `simultaneous-versus`.
- **Нема** → пропозиції карток:
  - `+line-counter-blast` «Повні ряди не зникають, а накопичуються для вибуху» · entities/interact · 📎.
  - `+big-bomb-merge` «4 бомби квадратом → велика бомба» · entities/state · 🌱 · слот {shape: 2x2, blast: 10}.
  - `+blast-size-by-lines` «Розмір вибуху за кількістю рядів» · entities/combat · 🌱 · слот {table}.
  - `+polyomino-set-progression` «Набір фігур росте з етапами» · levels/progression · 🌱.
  - `+enemies-in-well` «Вороги в колодязі псують стос» (Tetris Blast Fight) · entities/combat · 🥉.
  - `+clear-all-goal` · `+move-limit-puzzle` · `+cascade-gravity` — теги вже є в корпусі.

## Пропозиції до словників
- `+card:line-counter-blast`, `+card:big-bomb-merge`, `+card:blast-size-by-lines` — див. «Мапу». Слова правил лягли в наявні (`explode`, `merge`, `destroyed`, `settled`).

## Джерела
- ⭐ [TetrisWiki: Tetris 2 + Bombliss](https://tetris.wiki/Tetris_2_%2B_Bombliss) — поле 10×21, поліоміно 2–5, таблиця вибухів, Contest 60 етапів і прогресія фігур, Puzzle, Construction, бонуси Contest, режими Tetris 2.
- [Wikipedia: Tetris 2 + BomBliss](https://en.wikipedia.org/wiki/Tetris_2_%2B_BomBliss) — ряд підриває бомби, порожні ряди збільшують наступний вибух, 4 бомби квадратом → велика, липка гравітація, Chunsoft/BPS.
- [JA Wikipedia: ボンブリス (за адресою テトリス2+ボンブリス)](https://ja.wikipedia.org/wiki/テトリス2+ボンブリス) — центр вибуху в бомбі, детонація бомб у зоні, ланцюг додається до рядів, デカボム 10×10, таблиця 1×7…17×17, Contest зі 100 фігурами до 999, Puzzle без бомб у фігурах, versus.
- [Wikipedia: Tetris Blast](https://en.wikipedia.org/wiki/Tetris_Blast) — GB 1995, Training / Contest / Fight, ковзання, Link Cable.
- YouTube: пошук «Bombliss famicom gameplay».

## Непевне
- (?) Склад фігур: EN-вікі — «без бомб, одна бомба або вся з бомб»; JA — «принаймні одна бомба» (крім Puzzle, де бомб у фігурах нема — тоді бомби, мабуть, лише на полі).
- (?) Wikipedia формулює велику бомбу як «коли фігура входить у поле», JA — будь-які 4 бомби квадратом 2×2; узято JA.
- (?) Розмір вибуху бомби, підірваної іншим вибухом (той самий за рядами чи мінімальний).
- (?) Чи «+N» у таблиці Contest — це фігури в запас (JA) чи очки (TetrisWiki «score»); стартові 100 фігур — з JA.
- (?) Призначення кнопок, наявність превʼю наступної фігури й очок поза Contest.
