---
title: Tetris Plus
slug: tetris-plus
aka: [テトリスプラス, "Tetris Plus 2", テトリスプラス2]
family: falling-match
also: [grid-platformer]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: hotseat
  info: full
  random: runtime
  goal: state
year: 1995
platforms: [arcade, Sega Saturn, PlayStation, Game Boy]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Tetris_Plus", best: true, note: "Puzzle Mode: професор, стеля з шипами, 5 зон × 20 рівнів, редактор, versus, дати"}
  - {kind: other, url: "https://tetris.wiki/Tetris_Plus", note: "TetrisWiki: поля 10×20 / 10×17 / 10×15, превʼю, Sega-обертання, без hold і hard drop, очки Normal, бонус часу Puzzle, VS-розкладки"}
  - {kind: other, url: "https://tetris.wiki/Tetris_Plus_2", note: "TetrisWiki: Endless з главами, Puzzle з розгалуженням, VS Classic/Professor/Assistant, предмети сміття"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Tetris+Plus+puzzle+mode+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [gravity-fall, piece-rotate-flip, next-queue, keyboard-controls, turn-when-blocked, environment-death, time-bonus, time-out, event-points, score-records, sequential-levels, level-unlock, in-game-editor, simultaneous-versus, garbage-attack, difficulty-levels, progress-acceleration, mode-select, +line-clear, +auto-walker-guide, +ceiling-descend, +ceiling-crush-blocks, +climb-onto-piece, +fall-stun, +npc-reach-bottom]
proposes: ["+effect:ceiling_down", "+trigger:crushed", "+role:walker", "+card:auto-walker-guide", "+card:ceiling-crush-blocks", "+card:climb-onto-piece", "+card:npc-reach-bottom"]
author: opus
date: 2026-11-09
---

# Tetris Plus — став тетроміно й чисть ряди, щоб професор-ходок спустився на дно раніше, ніж його розчавить стеля з шипами

## Суть
Jaleco додає до Tetris режим-головоломку: у колодязі вже лежить задана кладка, зверху на неї виходить **професор** — автономний ходок, що йде вперед, розвертається від перешкод і падає в достатньо широкі щілини. Гравець керує звичайними тетроміно: кладе й чистить ряди, прокладаючи професору шлях на дно. Згори повільно опускається **стеля з шипами**: вона трощить кладку на своєму шляху, а торкнувшись професора, вбиває його. Класичний режим (Normal) — Tetris у дусі Sega 1988; деталі — у [tetris](tetris.md).

## Поле і час
- Колодязь: Puzzle і VS — 10×15; Normal — 10×20 (Game Boy — 10×17).
- Real-time: тетроміно падає з темпом; стеля опускається на позначку приблизно кожні 18 с; на 125-й секунді — швидке падіння, що гарантовано розчавлює професора.
- Шари: кладка (задана + покладені фігури) + професор (автономна сутність 2×2 (?)) + стеля (рухома межа зверху).
- VS — два колодязі поруч, той самий пазл, хто швидше доведе професора.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Тетроміно | player | 7 форм, Sega-обертання | зсув, поворот, прискорене падіння; без hold і hard drop |
| Професор | ally | напрям, стан normal / stunned / panic | іде вперед; упершись у блок — розвертається; падає в щілину, де вміщається; після довгого падіння — оглушений; фігуру поклали на нього — вилазить нагору |
| Кладка | object | задана розстановка рівня | звичайні клітини Tetris; ряд заповнено — зникає |
| Стеля з шипами | hazard | висота | опускається за таймером; трощить блоки на шляху; торкнулась професора — смерть |
| Ворота входу | gate | — | професор виходить через ворота, що потім зникають |
| Дно колодязя | zone | — | професор досяг — рівень пройдено |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ЯКЩО `free(cells_below)` → ТО `move(piece, down)`; інакше `custom: «lock»`, наступна з черги (2 превʼю).
- КОЛИ `input(shift|rotate)` → ЯКЩО `free(new_cells)` → ТО `move(piece, dir)` / `rotate(piece, 90)`.
- КОЛИ `locked(piece)` → ЯКЩО `pattern(row_full)` → ТО `clear(row)`, `custom: «ряди вище осідають»`.
- КОЛИ `tick` → ЯКЩО `free(cell_ahead)` і `custom: «є опора»` → ТО `move(professor, facing)`.
- КОЛИ `blocked(professor)` → ТО `face(professor, reverse)`.
- КОЛИ `tick` → ЯКЩО `custom: «під професором щілина, куди він вміщається»` → ТО `fall(professor)`.
- КОЛИ `custom: «довге падіння професора закінчилось»` → ТО `stun(professor, n)`.
- КОЛИ `locked(piece)` → ЯКЩО `occupied(professor_cells, piece)` → ТО `custom: «професор вилазить на верх фігури»`.
- КОЛИ `timer(18 s)` → ТО `custom: «ceiling_down — стеля опускається на позначку»`.
- КОЛИ `custom: «стеля зустріла блок»` → ТО `disappear(block)` — так можна позбутись невдалих фігур.
- КОЛИ `locked(piece)` → ЯКЩО `counter(rows_cleared_at_once, >=, 3)` → ТО `custom: «стеля піднімається»`.
- КОЛИ `in_range(professor, ceiling, near)` → ТО `set_state(professor, panic)`, `sound(frantic_music)` — біжить або метушиться, якщо нема куди.
- КОЛИ `contact(professor, ceiling)` (стеля опустилась на нього або він виліз у неї) → ТО `lose` рівня.
- КОЛИ `timer(125 s)` → ТО `custom: «стеля прискорено падає й розчавлює професора»`.
- КОЛИ `reach(professor, bottom)` → ТО `win`, `score(time_bonus)` — максимум 20 000 за ≤10 с, −100 за кожну ¼ с понад 10 с; `next_level`.
- КОЛИ `custom: «пройдено 4 зони»` → ТО `unlock(atlantis)`.
- Normal: КОЛИ `clear(rows)` → ТО `score(100|400|800|1600 × level)` (множник до 10-го рівня); КОЛИ `custom: «бічні шкали заповнились»` → ТО `custom: «level +1»`, `speed(piece, +n)`.
- VS: КОЛИ `reach(professor, bottom)` першим → ТО `win`; Tetris Plus 2 — сміття від предметів-скриньок 1/2/3.
- Перемога: професор на дні · Поразка: професор торкнувся стелі · Рахунок: Puzzle — бонус часу; Normal — лінії × рівень.

## Керування і ввід
- ←/→ — зсув, ↓ — прискорення, кнопки — поворот; hard drop і hold нема. Професором гравець **не керує** — лише середовищем.
- VS — двоє одночасно (аркада / консолі).

## Вікна, меню, HUD
- `splash-screen`, `attract-demo` (аркада (?)).
- `mode-select`: Normal («Regular Tetris») · Puzzle · VS · Edit (консолі).
- `map-window` / `level-select` зон: Egypt → Angkor Wat → Maya → Knossos → Atlantis (після чотирьох), по 20 рівнів (?: чи є вибір зони, чи послідовно).
- `game-screen` Puzzle: колодязь 10×15 зі стелею, `next-piece-preview` ×2, `timer-elapsed`, `level-number`, зона; Normal — бічні `progress-bar` рівня, `score`, ×3 превʼю.
- `editor-window` — редактор рівнів Puzzle Mode.
- `end-screen`: рівень пройдено (бонус часу) / професор загинув; `game-over-continue` (аркада (?)).
- `difficulty-select` для Normal: Easy / Normal / Hard / Hardest (таблиця швидкостей).
- Переходи: mode-select → (Puzzle) зона → game-screen → end-screen → наступний рівень; (Edit) editor-window → game-screen.

## Фічі поза полем
- `levels-sequential` 5 × 20 = 100 рівнів, `level-unlock` (Atlantis).
- `level-editor` (консолі) — власні рівні Puzzle Mode.
- `mode-versus` / `local-multiplayer`; VS цикл з 10 розкладок, що скидається після перезапуску автомата.
- `difficulty-presets` Normal (Easy…Hardest).

## Варіації й родичі
- **Tetris Plus 2** (аркада, 1997): поле 10×15, 2 превʼю, Sega-обертання з wall kick. Нове: грається **асистентка** професора (швидша); Endless — 22 глави: картинка тла завершується очищеннями ≥2 ліній або збиранням літер одиночними; Puzzle — розгалужений маршрут (26 стадій, 7 за прохід, 8 з кришталевою кулею); VS — Classic / Professor / Assistant, скриньки 1/2/3 додають сміття, якщо зчищені «без сліду» в тому ж очищенні.
- Родичі: Tetris (ядро), Lemmings і Troddlers (автономний ходок, якого ведуть зміною середовища), Wario's Woods (стеля, що опускається), Puzzle Bobble (стеля), Yoshi (NES).
- **Осі варіацій**: ціль колодязя (очки / **довести NPC до дна**) · загроза (стек росте / **стеля опускається**) · що робить стеля з блоками (нічого / **трощить**) · ходок (нема / професор / швидша асистентка).

## Цікавинки для курсу
- Професор-ходок: «вперед → упор → розворот → щілина → падіння → оглушення → вилізти на фігуру» — 🥉 (скінченний автомат NPC поверх Tetris).
- Перевірка «щілина достатньо широка» для сутності 2×2 — 📎.
- Стеля за таймером, що трощить кладку й відступає за 3–4 ряди одним ходом — 📎.
- Бонус часу з лінійним спадом (20 000 − 100 за ¼ с) — 🌱.
- Редактор рівнів: задана кладка + точка входу професора — 🥉.
- Розвʼязувач «чи можна довести професора за N фігур» — 👑 (пошук по фігурах + симуляція NPC).

## Мапа на каталог
- Є: `gravity-fall` · `piece-rotate-flip` · `next-queue` · `keyboard-controls` · `turn-when-blocked` (професор) · `environment-death` (шипи стелі) · `time-bonus` · `time-out` (125 с) · `event-points` · `score-records` · `sequential-levels` + `level-unlock` · `in-game-editor` · `simultaneous-versus` + `garbage-attack` (TP2) · `difficulty-levels` · `progress-acceleration` (Normal) · `mode-select`.
- **Нема** → пропозиції карток:
  - `+line-clear` (вже є з Tetris).
  - `+auto-walker-guide` (вже пропонована Troddlers) — ведеш автономного ходока зміною поля.
  - `+ceiling-descend` (вже пропонована Wario's Woods) — стеля опускається за таймером.
  - `+ceiling-crush-blocks` «Стеля трощить блоки на шляху» · entities/interact · 🌱.
  - `+climb-onto-piece` «NPC вилазить на фігуру, покладену на нього» · entities/move · 📎.
  - `+fall-stun` «Довге падіння оглушує» · entities/state · 🌱.
  - `+npc-reach-bottom` «Ціль — довести NPC до дна/виходу» · game-logic/win · 🌱.

## Пропозиції до словників
- `+effect:ceiling_down` — межа поля зверху зсувається вниз на крок (вже ×1 Wario's Woods).
- `+trigger:crushed` — сутність опинилась під обʼєктом, що опускається (стеля, фігура) — як в I.Q.
- `+role:walker` — автономний NPC, якого не керують, а ведуть (вже ×2 в іншому значенні — Caesar III).
- `+card:*` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Tetris Plus](https://en.wikipedia.org/wiki/Tetris_Plus) — Puzzle Mode: професор (іде, розвертається, падає, оглушення, вилазить на фігуру, паніка), стеля (~18 с, 3–4 ряди піднімають, трощить блоки, 125 с), 5 зон × 20, Atlantis, редактор, VS, платформи й дати, Tetris Plus 2 з асистенткою.
- [TetrisWiki: Tetris Plus](https://tetris.wiki/Tetris_Plus) — поля 10×20 / 10×17 / 10×15, превʼю 3/2/2, Sega-обертання, без hold/hard drop, очки Normal, бічні шкали рівня, швидкості, бонус часу Puzzle, 10 VS-розкладок.
- [TetrisWiki: Tetris Plus 2](https://tetris.wiki/Tetris_Plus_2) — Endless з 22 главами, розгалужений Puzzle (26 стадій), VS Classic/Professor/Assistant, скриньки сміття, wall kicks.
- YouTube: пошук «Tetris Plus puzzle mode gameplay».

## Непевне
- (?) Розмір професора (VS-розкладки позначають 2×2 зону спавну) і яка щілина «достатньо широка».
- (?) Чи стеля піднімається за 3 ряди так само, як за 4, і на скільки позначок.
- (?) Чи зони обираються з карти, чи йдуть послідовно; кнопки повороту; attract/continue-екрани.
- (?) Відмінності версій Saturn/PS/GB у Puzzle Mode (редактор — лише консолі за EN-вікі).
