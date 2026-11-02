---
title: Arimaa
slug: arimaa
family: chess-abstract
also: [push-slide]
klass: figure
axes:
  field: square
  time: turn
  opponent: online
  info: full
  random: none
  goal: race
year: 2002
platforms: [board, web]
links:
  - {kind: official, url: "https://arimaa.com/arimaa/learn/rulesIntro.html", best: true, note: "офіційні правила одним екраном: кроки, push/pull, заморожування, пастки, перемога"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Arimaa", note: "правила, історія, Arimaa Challenge, перемога Sharp 2015"}
  - {kind: official, url: "http://www.arimaa.com", note: "офіційний сайт: ігрова кімната, турніри, боти"}
  - {kind: other, url: "https://en.wikibooks.org/wiki/Arimaa", note: "Wikibooks: стратегія, нотація, приклади"}
  - {kind: other, url: "https://boardgamegeek.com/geeksearch.php?action=search&q=arimaa", note: "пошук BGG"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=arimaa+rules+explained", note: "пошук; пояснення правил"}
stage: v1
coverage: 75
mechanics: [piece-move-patterns, move-4dir, push-object, piece-capture, no-moves-left, hot-seat, turn-enforcement, move-timer, ai-opponent, ai-minimax, drag-drop-piece, legal-move-highlight, cell-click, game-screen, end-screen, help-window, replay, state-as-data, +step-budget, +push-pull-weaker, +freeze-adjacent, +trap-squares, +free-setup, +reach-row-win, +repetition-loss, +move-notation, +rating-system]
proposes: ["+cond:stronger", "+cond:guarded", "+trigger:step_done", "+trigger:repetition", "+effect:pull", "+effect:place", "+role:zone", "+role:supply", "+ui:action-points", "+ui:trap-marker", "+window:setup-phase", "+feature:send-move", "+axis:turn-structure", "+axis:win-condition", "+card:step-budget", "+card:push-pull-weaker", "+card:freeze-adjacent", "+card:trap-squares"]
author: opus
date: 2026-11-02
---

# Arimaa — шахи без патернів ходу: 4 кроки на хід, сильніший штовхає й тягне слабшого, пастки знімають самотніх

## Суть
Гра на шаховій дошці й шаховим набором, але всі фігури ходять однаково — на одну клітину ортогонально; відрізняються лише **силою** (слон > верблюд > кінь > пес > кіт > кролик). Хід — бюджет до 4 кроків, розподілених між будь-якими фігурами; сильніший може штовхнути або потягнути слабшого суперника, а поруч із сильнішим ворогом самотня фігура «замерзає». Взяття лише через 4 пастки: фігура на пастці без сусіда-союзника зникає. Мета — довести свого кролика до тилу суперника; гру Omar Syed спроєктував так, щоб вона була важкою для компʼютерів (Arimaa Challenge, виграно ботом лише 2015).

## Поле і час
- Дошка 8×8 (шахова), 4 клітини-пастки c3, f3, c6, f6 — позначаються монетками (на дошці не намальовані).
- Дві фази: **розстановка** (Gold ставить 16 фігур довільно на ряди 1–2, потім Silver на 7–8) і **гра** (Gold ходить першим).
- Хід = 1–4 **кроки**; крок — атомарна зміна позиції, після кожного — перевірка пасток. Кроки можна недобрати (частковий пас), але весь хід пасувати не можна — позиція має змінитися.
- Турнірний контроль часу — свій (резерв + час на хід, matchRules на сайті).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Слон (Elephant) | piece | сила 6, 1 шт. | крок 1 ортогонально; нікому не можна штовхнути/потягнути, нікого не боїться |
| Верблюд (Camel) | piece | сила 5, 1 шт. | крок 1; замерзає біля ворожого слона |
| Кінь (Horse) | piece | сила 4, 2 шт. | крок 1 |
| Пес (Dog) | piece | сила 3, 2 шт. | крок 1 |
| Кіт (Cat) | piece | сила 2, 2 шт. | крок 1 |
| Кролик (Rabbit) | piece | сила 1, 8 шт. | крок 1 вперед/убік, **не назад**; ціль — тил суперника |
| Пастка | zone | 4 клітини | фігура без ортогонального сусіда-союзника знімається |
| Тил (goal row) | zone | ряд 8 для Gold, 1 для Silver | кролик тут = перемога |
| Резерв розстановки | supply | 16 фігур | джерело `place` у фазі розстановки |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `game_start` → ТО `custom: «фаза розстановки»`: `place(piece, rows 1–2)` для Gold, потім rows 7–8 для Silver; довільний порядок.
- КОЛИ `turn_start(side)` → ТО `counter(steps_left, =4)`.
- КОЛИ `input(step(a, dir))` → ЯКЩО `turn_of(side(a))` and `free(target)` and `not state(a, frozen)` and `not (a == rabbit and dir == back)` and `counter(steps_left, >=, 1)` → ТО `move(a, dir)`, `counter(steps_left, -1)`.
- **Push** — КОЛИ `input(push(a, b, dir))` → ЯКЩО `adjacent(a, b)` and `stronger(a, b)` and `free(cell next to b)` and `counter(steps_left, >=, 2)` and `not state(a, frozen)` → ТО `move(b, dir)`, `move(a, old_cell_b)`, `counter(steps_left, -2)` (атомарно).
- **Pull** — КОЛИ `input(pull(a, b, dir))` → ЯКЩО `adjacent(a, b)` and `stronger(a, b)` and `free(cell for a)` and `counter(steps_left, >=, 2)` → ТО `move(a, dir)`, `pull(b)` у звільнену клітину, `counter(steps_left, -2)`; одна фігура не може штовхати і тягнути одночасно.
- Заморожування — КОЛИ `step_done` → ТО для кожної фігури x: ЯКЩО `adjacent(x, enemy stronger)` and `not adjacent(x, friend)` → ТО `set_state(x, frozen)`; інакше `clear_state(x, frozen)`. Рівні за силою не заморожують.
- Пастка — КОЛИ `step_done` → ЯКЩО `occupied(trap, x)` and `not guarded(x)` (нема ортогонального союзника) → ТО `disappear(x)`; спрацьовує і тоді, коли союзник **зійшов** із сусідньої клітини (`leave`), і під час pull (той, хто тягне, може сам зайти в пастку).
- КОЛИ `turn_end(side)` → ЯКЩО `custom: «позиція не змінилась»` → ТО хід нелегальний (`block`).
- КОЛИ `turn_end(side)` → ЯКЩО `repetition(position, 3)` → ТО `lose(side)` (той, хто створив третє повторення).
- КОЛИ `turn_end(side)` → ЯКЩО `reach(own_rabbit, goal_row)` → ТО `win(side)`; якщо кролик суперника затягнутий/виштовхнутий на його тил і там лишився — `win(opponent)` (?).
- КОЛИ `turn_end(side)` → ЯКЩО `all_gone(enemy rabbits)` → ТО `win(side)`; (турнірно — 8 знятих кроликів).
- КОЛИ `turn_start(side)` → ЯКЩО `no_moves(side)` → ТО `lose(side)` (іммобілізація).
- Кролик, що увійшов у тил і вийшов з нього в межах того самого ходу, перемоги не дає.
- Перемога: кролик у тилі · знищення кроликів · іммобілізація суперника · суперник створив третє повторення. Нічия: практично неможлива. Рахунок: 1/0, рейтинг гравців на arimaa.com.

## Керування і ввід
- Фаза розстановки: drag фігур з резерву на два свої ряди (цифрова версія — кнопки «випадкова/стандартна розстановка» (?)).
- Гра: drag фігури на сусідню клітину = 1 крок; push/pull — два послідовні кроки (спершу ворожа фігура, потім своя — або навпаки), клієнт перевіряє, що пара складає легальний push/pull.
- Undo кроку в межах свого ходу й явна кнопка «Send/Done» — хід відправляється, коли гравець вирішив, що кроків досить.
- Нотація ходу: кроки як `<фігура><клітина><напрям>` (`Ed2n`, `rc6x` — зняття в пастці) (?).

## Вікна, меню, HUD
- `setup-phase` (цифрова версія): дошка з підсвіченими двома рядами + резерв 16 фігур + кнопка «готово».
- `game-screen`: дошка з `trap-marker` на c3/f3/c6/f6, `action-points` (лишилось кроків 4→0), `player-clock`, `turn-indicator`, `captured-pieces`, `move-list`, кнопки `undo-button` (крок), «Send», `resign-button`.
- `help-window`: правила (на arimaa.com — сторінка з діаграмами).
- `end-screen`: причина кінця (goal / elimination / immobilization / repetition / time).
- `replay-window`: перегляд партій з архіву (кроки по одному) (?).
- `lobby-window` / `leaderboard` — ігрова кімната й рейтинги сайту (?).
- Переходи: lobby → setup-phase (Gold, потім Silver) → game-screen → end-screen → replay.

## Фічі поза полем
- `online-multiplayer`, `ai-opponent-levels` (боти ігрової кімнати), `rating`, `replay` + архів партій, `turn-timer` (власний контроль часу з резервом).
- `undo` в межах ходу (до відправки) — природна функція при бюджеті кроків.
- Щорічні World Championship (з 2004) і Arimaa Challenge — приклад «гри як бенчмарку для AI».
- Ліцензія Arimaa Public License, патент і торгова марка — правила вільні для некомерційних реалізацій.

## Варіації й родичі
- Родичі: шахи (той самий набір фігур, інша фізика), Breakthrough (гонка до тилу) [breakthrough-loa.md](breakthrough-loa.md), Sokoban-подібне штовхання/тягнення [push-slide](../push-slide/), Stratego (сила-ранг вирішує взаємодію).
- **Осі варіацій**:
  - **Бюджет ходу**: 1 дія (шахи) · N кроків, розподілюваних між фігурами (Arimaa) · очки дій (тактики).
  - **Взаємодія за силою**: бити (шахи) · штовхати/тягнути слабшого (Arimaa) · заморожувати (Arimaa) · ранг-дуель (Stratego).
  - **Взяття**: прямий удар · через клітини поля (пастки) · оточенням (го).
  - **Перемога**: мат · дійти рядом · знищити ключовий тип · іммобілізація · повторення = поразка.

## Цікавинки для курсу
- Бюджет кроків на хід із розподілом між фігурами + undo кроку до «Send» — 🥉: стан ходу окремо від стану позиції.
- Push/pull слабшого як атомарна пара кроків з перевіркою сили — 🥉 (родич `push-object` + `pull`).
- Заморожування: стан фігури, що перераховується після кожного кроку з сусідів (сильніший ворог vs союзник) — 📎.
- Пастки з перевіркою «охоронця» після кожного кроку, включно з тим, що охоронець пішов — 📎.
- Правило «хід має змінити позицію» + третє повторення = поразка — 🥉 (хеш позицій, Zobrist).
- AI: розгалуження ~17 000 ходів на позицію (через 4 кроки) робить minimax безнадійним — 👑: класичний приклад, чому brute-force не працює (?).
- Фаза розстановки як окреме вікно з валідацією — 📎.

## Мапа на каталог
- Є: `piece-move-patterns` (усі — крок 1, кролик без «назад») · `move-4dir` · `push-object` ↔ push · `piece-capture` (лише через пастки) · `no-moves-left` ↔ іммобілізація · `hot-seat` · `turn-enforcement` · `move-timer` · `ai-opponent` / `ai-minimax` · `drag-drop-piece` · `legal-move-highlight` · `cell-click` · `game-screen` · `end-screen` · `help-window` · `replay` · `state-as-data`.
- **Нема** → пропозиції карток:
  - `+step-budget` «Бюджет кроків на хід» · game-logic/opponent · 🥉 · слоти {steps: 4, partial_pass: yes} — хід як N атомарних кроків різних фігур.
  - `+push-pull-weaker` «Штовхнути/потягнути слабшого» · entities/legality · 🥉 · слоти {cost: 2, rank_rule: stronger} — Arimaa.
  - `+freeze-adjacent` «Заморожування сусідством» · entities/state · 📎 — стан від сусідів, знімається союзником.
  - `+trap-squares` «Клітини-пастки з охороною» · entities/interact · 📎 · слоти {guard: orthogonal_friend}.
  - `+free-setup` «Вільна розстановка перед партією» · game-logic/opponent · 📎 · слоти {rows: 2}.
  - `+repetition-loss` «Повторення = поразка» · game-logic/lose · 📎 — на відміну від `+repetition-draw` у шахах.
  - (`+reach-row-win`, `+move-notation`, `+rating-system` — уже запропоновані в quoridor/chess.)

## Пропозиції до словників
- `+cond:stronger(a, b)` — порівняння сили/рангу двох фігур (Arimaa, Stratego, Jungle) — без нього push/pull/freeze пишуться `custom`.
- `+cond:guarded(a)` — поруч є союзник (пастка Arimaa, рятує від заморожування).
- `+trigger:step_done` — після кожного кроку всередині ходу (≠ `turn_end`): тут перевіряються пастки й заморожування.
- `+trigger:repetition` — підтверджую (тут — третє повторення як поразка).
- `+effect:pull` (⏳ є) — підтверджую вживання в абстрактній грі; `+effect:place` — розстановка з резерву.
- `+role:zone` — пастки і тил; `+role:supply` — резерв розстановки.
- `+ui:action-points` (⏳ є) — лічильник кроків, що лишились у ході; `+ui:trap-marker` — позначка клітини-пастки на дошці.
- `+window:setup-phase` — вікно розстановки перед партією (Arimaa, Stratego, Kriegspiel-подібні).
- `+feature:send-move` — хід підтверджується явно після кількох кроків (з undo кроків до відправки).
- `+axis:turn-structure` — нове значення `step-budget` (хід = N кроків між фігурами).
- `+axis:win-condition` — значення `race` + `elimination(kind)` + `immobilize`.

## Джерела
- ⭐ [Arimaa: Rules](https://arimaa.com/arimaa/learn/rulesIntro.html) — офіційні правила: 4 кроки, частковий пас, атомарні push/pull, пастки, заморожування, розстановка.
- [Wikipedia: Arimaa](https://en.wikipedia.org/wiki/Arimaa) — правила, умови перемоги (goal, elimination, immobilization, repetition), історія, Arimaa Challenge і Sharp (2015).
- [arimaa.com](http://www.arimaa.com) — офіційний сайт (ігрова кімната, турніри).
- [Wikibooks: Arimaa](https://en.wikibooks.org/wiki/Arimaa) — стратегія й нотація (лінк зі статті Wikipedia).
- YouTube: пошук «arimaa rules explained».

## Непевне
- (?) Пріоритет умов кінця гри, коли в одному ході і свій, і ворожий кролик опинились у тилі — з памʼяті (переможець — той, хто ходив, якщо його кролик у тилі; інакше — суперник).
- (?) Формат нотації (`Ed2n`, `rc6x`) і число ~17 000 ходів на позицію — з памʼяті.
- (?) Вигляд клієнта arimaa.com (кнопка Send, undo кроку, кнопки розстановки, архів/replay) — не відкривав.
- `opponent: online` — гра популяризувалась через ігрову кімнату arimaa.com; настільний набір Z-Man (2009) — hotseat.
