---
title: Tetris Worlds (режими-варіанти)
slug: tetris-worlds
aka: ["Tetris Worlds Online"]
family: falling-match
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: hotseat
  info: full
  random: runtime
  goal: score
year: 2001
platforms: [PC, Game Boy Advance, PS2, GameCube, Xbox]
links:
  - {kind: other, url: "https://tetris.wiki/Tetris_Worlds", best: true, note: "TetrisWiki: 10×20, 6 next, hold, SRS, infinity; правила й цілі кожного режиму — Square, Cascade, Hot-Line (ряди 5/10/14/17/19/20), Sticky, Fusion (3 атоми на мішок 10), Original, Popular"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Tetris_Worlds", note: "сюжет шести світів, Arcade по 2 хв, коротко про кожен варіант; фігура не лочиться до hard drop (PS2/PC/GBA)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Tetris+Worlds+fusion+hot-line+gameplay", note: "пошук; режими"}
stage: v1
coverage: 60
mechanics: [gravity-fall, multi-cell-size, keyboard-controls, next-queue, chain-reaction, stick-together, event-points, time-out, mode-select, sequential-levels, hot-seat, online-multiplayer, +line-clear, +hold-piece, +hard-drop, +srs-wall-kicks, +lock-delay, +cascade-gravity, +connected-group-pop, +square-detection, +bag-randomizer, +back-to-back, +t-spin-detection, +hot-line-rows, +atom-fusion-connect, +multicolor-piece-split, +floating-garbage-start, +level-goal-points, +rank-progression]
proposes: ["+cond:row_in", "+effect:lock", "+card:hot-line-rows", "+card:atom-fusion-connect", "+card:multicolor-piece-split", "+card:floating-garbage-start", "+card:level-goal-points"]
author: opus
date: 2026-11-09
---

# Tetris Worlds — шість правил поверх одного Tetris: очки лише на «гарячих» рядах, злипання кольорів, атоми до блоку синтезу

## Суть
Tetris від THQ / Blue Planet (2001–2002) з ядром Guideline ([tetris](tetris.md): SRS, hold, 6 next, hard drop) і набором режимів-варіантів, де змінюється не керування, а **що вважається успіхом** і **як осідає стек**. Найновіші для корпусу — **Hot-Line** (зчищений ряд дає очки лише на шести заданих висотах) і **Fusion** (у потоці фігур — атоми, які треба зʼєднати з блоком синтезу в куті дна). Цей файл — лише відмінності режимів від базового Tetris.

## Поле і час
- Матриця 10×20; черга next — 6 (GBA — 3); hold; hard drop, що лочить; SRS з автоповтором повороту.
- Lock: «infinity» — на PS2/PC/GBA фігура не лочиться, доки гравець сам її не залочить (hard drop), тоді як годинник раунду йде; на GameCube/Xbox — опція «Easy Spin».
- Real-time; Arcade — партії по дві хвилини; Story — шість світів, кожен зі своїм варіантом.
- Осідання після зчищення різне за режимом: наївне (Tetris, Square) · по фігурах (Cascade, Hot-Line) · за звʼязністю кольору (Sticky) · від атома вгору (Fusion).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Тетроміно | player | 7 форм, кольори Guideline | як у Tetris; у Cascade/Hot-Line після зчищення кожна фігура осідає окремо |
| Багатоколірне тетроміно | player | клітини різних кольорів | Sticky: 20 % фігур; на локу розпадається на шматки за кольором; Hot-Line: 10 % (?) |
| Клітина стеку | tile | колір; памʼять «з якої фігури» (Cascade) | зникає з повним рядом; у Sticky злипається з сусідами свого кольору |
| Гарячий ряд (Hot-Line) | zone | висота 5 · 10 · 14 · 17 · 19 · 20 знизу; вартість 1–6 | лише повний ряд на цій висоті дає очки |
| Квадрат 4×4 (Square) | zone | з цілих тетроміно | ряд, що містить квадрат, — великий бонус |
| Критична маса (Sticky) | zone | звʼязна група одного кольору ≥ 25 | зникає без повного ряду |
| Плаваюче сміття (Sticky, Fusion) | object | L + 1 рядів на рівні L | стартова кладка; у Sticky мета — зчистити її нижній ряд |
| Атом (Fusion) | object | 1 клітина; 3 на кожен мішок з 10 фігур | звичайним зчищенням не знищується; ряд з атомом зносить усі не-атомні клітини ряду й запускає каскад вище |
| Блок синтезу (Fusion) | static | у одному з нижніх кутів | не знищується; ціль — приєднати до нього 2 × L атомів |

## Правила (КОЛИ → ЯКЩО → ТО)
- Спільне: КОЛИ `input(hard_drop)` → ТО `custom: «lock»`; на PS2/PC/GBA фігура без hard drop не лочиться (infinity), КОЛИ `input(move|rotate)` → ТО `custom: «таймер локу не тікає»`.
- КОЛИ `counter(goal_points, ≥, k × L)` → ТО `counter(level, +1)`; k = 10 у Square, 5 у Cascade і Hot-Line; режим закінчується після 15 рівнів.
- **Tetris (Marathon)**: КОЛИ `locked(piece)` → ЯКЩО `pattern(row_full)` → ТО `clear(rows)`, `counter(goal_points, +n)`: Single 1 · Double 3 · Triple 5 · Tetris 8 · B2B Tetris 12 · T-spin без рядів 1 · T-spin Single 3 · Double 7 · Triple 6.
- **Square**: КОЛИ `locked(piece)` → ЯКЩО `custom: «цілі тетроміно утворили квадрат 4×4»` → ТО `transform(cells, square)`; КОЛИ `after(clear)` → ЯКЩО `occupied(cleared_row, square)` → ТО `score(big_bonus)`.
- **Square**: КОЛИ `after(clear)` → ЯКЩО `custom: «зчищення T-spin-ом»` → ТО `custom: «лавина, як у The New Tetris»` (кількість додаткових рядів — (?)).
- **Cascade**: КОЛИ `after(clear)` → ТО `fall(each_piece_remnant)` — кожна фігура падає окремо, доки має куди; КОЛИ `settled` → ЯКЩО `pattern(row_full)` → ТО `clear(rows)`, `combo(+1)` (крок каскаду n).
- **Cascade**: крок n каскаду з L рядами дає `counter(goal_points, (L + n) × 2 − 3)`; приклад: Tetris → Double → Single = 7 + 5 + 5 = 17.
- **Hot-Line**: КОЛИ `after(clear)` → ЯКЩО `custom: «row_in — ряд на висоті 5 / 10 / 14 / 17 / 19 / 20»` → ТО `counter(goal_points, +1…+6)` за висотою; інакше `custom: «ряд зникає без очок»`; осідання — як у Cascade.
- **Sticky**: КОЛИ `locked(multicolor_piece)` → ТО `split(piece)` на шматки одного кольору.
- **Sticky**: КОЛИ `locked(piece)` → ЯКЩО `adjacent_count(cell, same_color, >, 0)` → ТО `attach(cell, neighbor)` — однакові кольори злипаються в одне тіло.
- **Sticky**: КОЛИ `pattern(group(25+, same_color))` → ТО `clear(group)` («Critical Mass»), `fall(unsupported_groups)`.
- **Sticky**: КОЛИ `level_start` → ТО `spawn_at(garbage, L + 1 rows)`; КОЛИ `custom: «нижній ряд сміття зчищено»` → ТО `next_level`.
- **Fusion**: КОЛИ `spawned(piece)` → ТО `custom: «з мішка на 10: 7 тетроміно + 3 атоми»`.
- **Fusion**: КОЛИ `pattern(row_full)` → ЯКЩО `occupied(row, atom)` → ТО `clear(non_atom_cells_in_row)`, `custom: «каскад у кожному ряду на висоті атома й вище»`; атоми й блок синтезу лишаються.
- **Fusion**: КОЛИ `locked(atom)` → ЯКЩО `connected(atom, fusion_block)` → ТО `counter(fused, +1)` (як саме атом «поглинається» — (?)); КОЛИ `counter(fused, ≥, 2 × L)` → ТО `next_level`.
- КОЛИ `spawned(piece)` → ЯКЩО `not free(spawn_cells)` → ТО `lose` (top out, як у Tetris).
- **Arcade**: КОЛИ `timer(round, ==, 0)` → ТО `game_over` — дві хвилини, будь-який варіант.
- Перемога: Story — пройти світ свого варіанта · Поразка: top out · Рахунок: goal-очки рівня за таблицею режиму.

## Керування і ввід
- Як у Guideline: зсув, поворот у дві сторони (утримання — автоповтор повороту), soft drop, hard drop (лочить), hold.
- Без hard drop фігура «висить» безкінечно (PS2/PC/GBA) — уся відповідальність за темп на гравці, бо раунд обмежений часом.

## Вікна, меню, HUD
- `main-menu` → Story · Arcade · Options.
- `mode-select` (Arcade): Tetris · Square · Cascade · Hot-Line · Sticky · Fusion (+ Original на PC/PS2, Popular на GBA — приховані).
- `map-window` (Story): шість світів Мінос, кожен з варіантом; результат — скільки Мінос врятовано.
- `game-screen`: матриця 10×20, `next-piece-preview` (6 / 3), `hold-slot`, `timer-countdown` (2 хв), рівень, goal-лічильник; Hot-Line — підсвічені гарячі ряди; Fusion — блок синтезу в куті й лічильник приєднаних атомів (?).
- `stats-window` / ранг 1–15 гравця (PS2/PC — ранг росте від повторних партій).
- `end-screen` — підсумок раунду.
- Переходи: main-menu → mode-select / map-window → game-screen → end-screen.

## Фічі поза полем
- `mode-time-attack` (Arcade 2 хв), `custom-rules`-подібний набір варіантів, `local-multiplayer` (до 4 гравців (?)), `online-multiplayer` — Tetris Worlds Online (Xbox Live, 2003).
- `rank-tiers`: ранг до 15 (PS2/PC — за повторні партії; GC/Xbox/GBA — підняттям рівня); Original Tetris відкривається рангом 11 у всіх головних режимах.
- Опція «Easy Spin» (GC/Xbox) — вмикає/вимикає нескінченне обертання.

## Варіації й родичі
- Original Tetris (PC/PS2) — копія версії Electronika 60, рівень кожні 10 рядів; Popular Tetris (GBA) — як Game Boy, з hard drop і кольорами The New Tetris, без ліміту часу, рахунок зупиняється на 1 000 000.
- Square — з The New Tetris (1999); Sticky — з The Next Tetris; Cascade — як фанатська Quadra.
- **Осі варіацій «що вважається успіхом»**: будь-який повний ряд (Tetris) / ряд лише на заданих висотах (Hot-Line) / форма в стеку (Square: квадрат 4×4) / звʼязна маса кольору (Sticky) / звʼязність до цільової клітини (Fusion) / зчистити дно сміття (Sticky).
- **Осі «як осідає стек»**: наївно рядами · кожна фігура окремо (Cascade) · кольорові тіла (Sticky) · каскад від атома вгору (Fusion) — пор. Puyo (`puyo-puyo`), Columns (`columns`).
- Родичі: Tetris (`tetris`), Tetris Plus (`tetris-plus`, ціль у стеку), Bombliss (`bombliss`, вибухи замість рядів), Magical Tetris Challenge (`magical-tetris-challenge`).

## Цікавинки для курсу
- Hot-Line: ціна ряду з таблиці висот — 🌱 (лише перевірка індексу ряду; але змінює всю стратегію).
- Cascade: памʼять «яка фігура» в клітині + осідання шматків фігур як тіл + повторні зчищення з формулою кроку — 🥈.
- Sticky: злипання за кольором (union-find), розпад багатоколірних фігур, Critical Mass ≥ 25, падіння непідпертих груп — 🥇.
- Fusion: атоми, що переживають зчищення, і перевірка звʼязності з блоком синтезу BFS-ом — 🥉.
- Square: детектор квадрата 4×4 саме з цілих тетроміно — 🥉.
- Мішок 10 з 3 атомами як керований рандом — 🌱.

## Мапа на каталог
- Є: `gravity-fall`, `multi-cell-size`, `keyboard-controls`, `next-queue` (6); `chain-reaction` ↔ каскади; `stick-together` ↔ злипання кольорів у Sticky; `event-points` ↔ таблиці goal-очок; `time-out` ↔ Arcade 2 хв; `mode-select`; `sequential-levels` ↔ світи Story; `hot-seat`, `online-multiplayer`.
- Уже пропоновані іншими: `+line-clear` (слот gravity: naive / sticky / cascade), `+hold-piece`, `+hard-drop`, `+srs-wall-kicks`, `+lock-delay` (infinity), `+cascade-gravity`, `+connected-group-pop` (n = 25), `+square-detection`, `+bag-randomizer` (мішок 10 з атомами), `+back-to-back`, `+t-spin-detection`.
- **Нема** → пропозиції карток:
  - `+hot-line-rows` «Очки лише за ряди на заданих висотах» · game-logic/score · 🌱 · слот {rows: {5:1, 10:2, 14:3, 17:4, 19:5, 20:6}}.
  - `+atom-fusion-connect` «Приєднати N особливих клітин до цілі» · game-logic/win · 🥉 · слоти {atoms_per_bag: 3/10, goal: 2L}.
  - `+multicolor-piece-split` «Фігура розпадається за кольором на локу» · entities/state · 📎.
  - `+floating-garbage-start` «Стартова кладка L+1 рядів» · levels/generation · 🌱.
  - `+level-goal-points` «Рівень за goal-очками, а не рядами» · game-logic/waves · 🌱 · слот {k: 5|10}.
  - `+rank-progression` «Ранг гравця 1–15 між партіями» · levels/progression · 🌱.

## Пропозиції до словників
- `+cond:row_in` — ряд належить заданому набору висот (Hot-Line; також «ряд у зоні»).
- `+effect:lock` — фігура стає клітинами стеку (вже пропонована в `tetris`; тут — лише через hard drop).
- `+card:hot-line-rows`, `+card:atom-fusion-connect`, `+card:multicolor-piece-split`, `+card:floating-garbage-start`, `+card:level-goal-points`.

## Джерела
- ⭐ [TetrisWiki: Tetris Worlds](https://tetris.wiki/Tetris_Worlds) — загальні правила (10×20, 6/3 next, hold, SRS, infinity), таблиця goal-очок Tetris, цілі рівнів k × L, формула каскаду, гарячі ряди й їхня вартість, Sticky 20 %, Critical Mass 25, Fusion (3 атоми на 10, 2L атомів, L+1 рядів сміття), Original і Popular.
- [Wikipedia: Tetris Worlds](https://en.wikipedia.org/wiki/Tetris_Worlds) — Story (шість світів, Міно), Arcade по 2 хв, опис кожного варіанта, атоми й блок синтезу не знищуються зчищенням, lock лише гравцем (PS2/PC/GBA), Easy Spin (GC/Xbox), Tetris Worlds Online (2003), платформи й дати.
- YouTube: пошук «Tetris Worlds fusion hot-line gameplay».

## Непевне
- (?) Hot-Line: «10 % багатоколірних фігур» — так у переказі TetrisWiki, але для режиму без кольорових правил це дивно; речення сторінки про найдорожчу очистку було нечитабельне.
- (?) Fusion: що відбувається з атомом після приєднання (зникає, світиться, лишається) і чи зʼєднання — через сусідні атоми чи будь-які клітини.
- (?) «Плаваюче» сміття: чи воно висить без опори до першого зчищення (при каскадній гравітації) — не уточнено.
- (?) Square: золоті/срібні квадрати й точні бонуси — з The New Tetris, тут не перевірено; кількість рядів лавини після T-spin TetrisWiki сама називає невизначеною.
- (?) Мультиплеєр: до 4 гравців, сміття між гравцями — не описано в прочитаних джерелах.
- (?) Ліміт часу поза Arcade (Story) і швидкість гравітації — не знайдено.
