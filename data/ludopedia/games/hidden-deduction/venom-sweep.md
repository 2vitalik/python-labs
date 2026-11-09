---
title: Venom Sweep
slug: venom-sweep
aka: [MINESWEEPER X SNAKE]
family: hidden-deduction
also: [maze-arcade]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: hidden
  random: setup
  goal: score
year: 2026
platforms: [web (itch.io, HTML5 Godot 4.7)]
links:
  - {kind: itch, url: "https://houjousxnnyside.itch.io/venom-sweep", best: true, note: "грати в браузері; опис (ES): живі числа, змія з 3 кроками телеграфу, яйця й пурга 1 с, отруйний слід, нескінченний скрол, комбо до ×4, режими Classic/Sudden Death, керування"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Venom+Sweep+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [move-by-input, move-4dir, keyboard-controls, impassable-cells, neighbor-count-clue, flood-reveal, infinite-field, body-queue, pattern-automaton, chase-player, telegraphed-intents, telegraph-marker, spawn-random-cell, player-death, environment-death, combo-multiplier, event-points, score-records, difficulty-levels, game-pause, restart-level, main-menu, pause-menu, help-window, game-screen, end-screen, sound-effects, +facing-reveal, +live-recount-clue, +enemy-lays-hazards, +timed-purge-flag, +toxic-trail, +stale-clue, +wound-by-own-egg, +advancing-hazard-front, +chunk-generation]
proposes: ["+effect:purge", "+effect:retreat", "+axis:scroll", "+feature:mode-sudden-death", "+card:facing-reveal", "+card:live-recount-clue", "+card:enemy-lays-hazards", "+card:timed-purge-flag", "+card:toxic-trail", "+card:stale-clue", "+card:wound-by-own-egg"]
author: opus
date: 2026-11-09
---

# Venom Sweep — сапер на болоті, що повзе вниз: Рука відкриває клітину перед собою, а змія кладе нові «міни» просто під час гри

## Суть
Гравець — **Рука**, що ходить сіткою сапера в реальному часі й ступає лише на відкриті клітини. Болото безперервно прокручується вниз: хто відстав від верхнього краю — проковтнутий. Головна новинка — **живі числа**: змія-хижак повзе полем за видимим планом, кожні кілька кроків кладе яйце в закриту клітину й лишає отруйний слід, тож число на вже відкритій клітині може зрости просто під ногами. Яйце, в якому впевнений, гравець «пурґує» (1 с нерухомості); знищене яйце самої змії ранить її.

## Поле і час
- Сітка 12 стовпців × нескінченно вгору; на екрані 12×20 клітин (16 px, екран 192×320), поле генерується чанками по 8 рядків, чанки нижче екрана видаляються.
- Щільність яєць у новому чанку росте з 12 % до 19 % за перші 400 рядків; у збірці 28.10.2026 зерно світу — константа, тож стартова розкладка яєць однакова в кожному забігу (з коду).
- Камера їде вгору зі швидкістю 6 px/с + 0,08 px/с за кожну секунду гри, до 30 px/с (≈ 0,4 → 1,9 клітини/с); рядок нижче нижнього краю — «проковтнутий».
- Реальний час: Рука ходить з паузою 0,12 с між кроками (на отруйній клітині ×2,5); змія — крок 0,32 с, у ривку 0,22 с, поранена — ×1,4 повільніше.
- Старт: Рука в центрі (стовпець 6) за 5 рядків від низу; довкола очищено 5×5 від яєць і відкрито 3×3 з каскадом.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Рука | player | життя 3 (Classic) / 1 (Sudden Death), напрям погляду | крок на 4 сторони лише на відкриту клітину; дивиться на сусідню клітину-«курсор»; невразлива 1,2 с після укусу |
| Закрита клітина | tile | — | відкривається пробілом, якщо Рука дивиться на неї |
| Відкрита клітина з числом | mark | 0–8 | кількість небезпек серед 8 сусідів: яйця + отруєні + отруйні клітини; перераховується наживо |
| Яйце | hazard | природне / знесене змією | відкрити = −1 життя; пурґувати = прибрати |
| Отруєна клітина | hazard | — | яйце, яке відкрили: лишається відкритою, але й далі рахується в числах сусідів |
| Отруйний слід (череп) | hazard | 20 с, блимає останні 3 с | клітина, що лишилась за 2 кроки позаду голови змії: не відкривається, хода по ній ×2,5 повільніша, рахується в числах |
| «?» — застаріле число | mark | — | відкрита клітина після зникнення сліду: число невідоме, поки Рука не підтвердить пробілом |
| Прапорець | mark | звичайний / хибний | ставиться клавішею E і запускає пургу; хибний лишається позначеним |
| Змія | enemy | довжина 8 (мін. 4), крок 0,32 / 0,22 с | рухається за планом SWEEP / WEAVE / CHARGE; тіло займає клітини; кусає Руку головою; кожні 10 кроків кладе яйце в радіусі 2 від голови |
| Телеграф змії | mark | 3 кроки | зелені дужки на 3 наступних клітинах плану |
| Болото (нижній край) | zone | швидкість росте | клітини нижче екрана проковтнуті; Рука там гине |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(move, dir)` → ЯКЩО `cell(target, revealed)` і `not occupied(target, serpent)` і `custom: «рядок у межах екрана»` → ТО `move(hand, dir)`; інакше `face(hand, dir)` (лише поворот).
- КОЛИ `input(space)` → ЯКЩО `state(front, stale)` → ТО `clear_state(front, stale)`, `custom: «каскад від нулів довкола»`.
- КОЛИ `input(space)` → ЯКЩО `custom: «клітина закрита, без прапорця, не отруйна»` і `not occupied(front, egg)` → ТО `reveal(front)`, `score(1 × multiplier)`, `combo(+1)`.
- КОЛИ `after(reveal)` → ЯКЩО `adjacent_count(cell, hazard, ==, 0)` → ТО `reveal(neighbors8)` хвилею з кроком 0,08 с, `score(+1 за кожну клітину, без множника)`; хвиля не заходить у проковтнуті рядки.
- КОЛИ `input(space)` → ЯКЩО `occupied(front, egg)` → ТО `transform(egg, poisoned_cell)`, `lives(-1)`, `reset_combo`, `flash`, `shake`.
- КОЛИ `input(E)` → ЯКЩО `state(front, flagged)` → ТО `unmark(front)`.
- КОЛИ `input(E)` → ЯКЩО `custom: «клітина закрита й не отруйна»` → ТО `mark(front, flag)`, `freeze(hand, 1 s)` (`+effect:purge`).
- КОЛИ `after(freeze)` → ЯКЩО `occupied(front, egg)` → ТО `disappear(egg)`, `reveal(front)`, `score(25 × multiplier)`, `combo(+1)`, `custom: «каскад від нулів довкола»`; інакше `mark(front, wrong)`, `reset_combo` (хибна пурга коштує лише часу).
- … ЯКЩО `custom: «яйце знесла змія»` → ТО `shrink(serpent, 1)` (не менше 4), `speed(serpent, ×1/1.4, 6 s)`, `custom: «змія відступає на 1 крок»` (`+effect:retreat`), `score(50)`.
- КОЛИ `timer(serpent_step)` → ТО `move(serpent, plan[0])`; ЯКЩО `not free(target)` → ТО `custom: «запасний напрям: вниз → вліво → вправо → вгору»`.
- КОЛИ `custom: «у плані змії менше 4 кроків»` → ТО `custom: «дописати візерунок: SWEEP — до 8 клітин у бік далекого краю й 2 вниз; WEAVE — 8 кроків «вниз-убік»; CHARGE — до 6 клітин до стовпця Руки й 3–8 вниз швидко; CHARGE не двічі поспіль»`.
- КОЛИ `after(move serpent)` → ТО `set_cell(cell_2_steps_behind_head, toxic)` на 20 с.
- КОЛИ `counter(serpent_steps, ==, 10)` → ТО `spawn_at(egg, random free closed cell in radius 2 of head, not hand)`, `counter(serpent_steps, 0)`; числа сусідів зростають одразу.
- КОЛИ `timer(20 s)` для отруйної клітини → ТО `set_cell(cell, normal)`; ЯКЩО `state(cell, revealed)` → ТО `set_state(cell, stale)` («?»).
- КОЛИ `contact(serpent_head, hand)` → ЯКЩО `not state(hand, invulnerable)` → ТО `lives(-1)`, `set_state(hand, invulnerable, 1.2 s)`, `reset_combo`, `custom: «змія відступає на 4 кроки»`.
- КОЛИ `custom: «голова змії більш ніж на 14 рядків вище екрана або все тіло проковтнуте»` → ТО `disappear(serpent)`; через 2 с — `spawn_at(serpent, random column, 3 rows above view)` (перша поява — через 3 с від старту).
- КОЛИ `tick` → ТО `camera(up, speed)`, `score(+2 за кожен новий рядок дистанції)`.
- КОЛИ `edge(hand)` (рядок Руки нижче екрана) → ТО `lose` («SWALLOWED BY THE SWAMP») — незалежно від життів.
- КОЛИ `counter(lives, ==, 0)` → ТО `lose` («POISONED» або «BITTEN BY THE SERPENT»), `reveal(all eggs)`, `window(end-screen)`.
- Множник: `multiplier(min(1 + streak / 5, 4))`; помилки (відкрите яйце, хибна пурга, укус) — `reset_combo`.
- Перемоги нема (нескінченний забіг) · Поразка: проковтнуло болото або скінчились життя · Рахунок: клітини + яйця + поранення + дистанція, рекорд окремо для кожного режиму.

## Керування і ввід
- W A S D / стрілки — крок; утримання — повтор кроку; упор у закриту клітину чи змію лише повертає Руку (курсор — клітина попереду).
- Пробіл — відкрити клітину попереду або підтвердити «?»; E — прапорець + пурга (1 с без руху), повторно на прапорці — зняти.
- Esc — пауза; R — рестарт забігу; T — у меню; M — звук; на титулі W/S — режим, Space — старт, H — правила.

## Вікна, меню, HUD
- `main-menu` (титул «MINESWEEPER X SNAKE»): вибір режиму W/S (`difficulty-select` у рядку: Classic 3 життя / Sudden death 1 життя, з рекордом), SPACE — старт, H — правила.
- `help-window` «HOW TO PLAY»: 7 правил з анімованими іконками, «PRESS ANY KEY»; перед першим забігом показується саме (?).
- `game-screen`: поле з `cursor` перед Рукою, `telegraph-marker` (3 кроки змії), `lives` (серця), `score`, дистанція, `combo-meter` (×N, коли більше 1), назва режиму; перші 14 с — `hint-text` «FACE A DARK CELL: SPACE OPENS · E PURGES»; червоний спалах і трус екрана при уколі; смужка прогресу пурги під Рукою.
- `pause-menu`: «PAUSED», ESC — продовжити, R — рестарт, T — титул, M — звук.
- `end-screen` (панель поверх поля): причина смерті, SCORE і DIST, «NEW BEST!» або BEST, «R: RESTART · T: TITLE»; усі яйця показуються.

## Фічі поза полем
- `difficulty-presets`: Classic / Sudden Death (`+feature:mode-sudden-death`); рекорд для кожного (`leaderboard-local`, файл `venomsweep.cfg`).
- `pause`, `restart-level`, `sound-toggle`, `rules-page`; звук синтезується в коді (8-біт).
- Статус — прототип; збереження прогресу нема, лише рекорди.

## Варіації й родичі
- У корпусі: [minesweeper](minesweeper.md) (база чисел), [mined-out](mined-out.md) і [lizzi-crossing](lizzi-crossing.md) (аватар іде полем сапера), [mamono-mower](mamono-mower.md) (сапер у реальному часі), [minesweeper-infinite](minesweeper-infinite.md) (нескінченне поле чанками), [endless-mines](endless-mines.md) і [tetrisweeper](tetrisweeper.md) (сапер під тиском часу), [snake](../maze-arcade/snake.md) (сама змія).
- **Осі варіацій:** приховані небезпеки статичні / додаються під час гри (яйця) / рухаються ([minesweeper-dimensions](minesweeper-dimensions.md), Timesweeper); число — знімок на момент відкриття / живе й перераховується / може «застаріти» до підтвердження; відкривати — кліком будь-де / лише перед аватаром; прапорець — позначка / дія з ціною часу й перевіркою.

## Цікавинки для курсу
- Живе число: `adjacent_count` рахується при рендері з бітових прапорців клітини (EGG | POISONED | TOXIC), а не зберігається — 🌱.
- Рука, що відкриває лише клітину перед собою й ходить лише по відкритому — 📎.
- Автоскрол з прискоренням і смерть за нижнім краєм + генерація чанками з лінійно зростаючою щільністю — 🥉.
- Змія-планувальник: черга кроків із трьох візерунків, телеграф 3 кроків, ривок до стовпця гравця, запасний напрям при упорі — 🥉.
- Слід з таймером, що «псує» числа: отрута 20 с → «?» до підтвердження — 📎.
- Пурга: прапорець як дія на 1 с з перевіркою, поранення змії її ж яйцем (коротша, повільніша, відступ) — 📎.
- Комбо: множник `min(1 + streak // 5, 4)` і скидання на помилці — 🌱.

## Мапа на каталог
- Є: `move-by-input` + `move-4dir` + `keyboard-controls` ↔ Рука; `impassable-cells` ↔ закриті клітини й тіло змії; `neighbor-count-clue` ↔ числа; `flood-reveal` ↔ каскад; `infinite-field` ↔ нескінченне болото; `body-queue` ↔ тіло змії; `pattern-automaton` ↔ SWEEP/WEAVE; `chase-player` ↔ CHARGE; `telegraphed-intents` + `telegraph-marker` ↔ зелені дужки; `spawn-random-cell` ↔ яйця біля голови; `player-death` (lives 3/1) і `environment-death` ↔ проковтнутий; `combo-multiplier`; `event-points`; `score-records`; `difficulty-levels` ↔ Classic / Sudden Death; `game-pause`, `restart-level`, `main-menu`, `pause-menu`, `help-window`, `game-screen`, `end-screen`, `sound-effects`.
- **Нема** → пропозиції карток:
  - `+facing-reveal` «Аватар відкриває лише клітину, на яку дивиться» · entities/interact · 🌱.
  - `+live-recount-clue` «Підказка перераховується, коли приховане зʼявляється чи зникає» · game-logic/constraints · 📎.
  - `+enemy-lays-hazards` «Ворог під час гри кладе приховані небезпеки» · entities/spawn · 📎.
  - `+timed-purge-flag` «Прапорець — дія з тривалістю й перевіркою» · entities/interact · 📎 · слоти {duration, penalty}.
  - `+toxic-trail` «Слід ворога — тимчасова небезпечна клітина» · entities/state · 📎 · слоти {delay_steps, lifetime}.
  - `+stale-clue` «Число стає невідомим, доки його не підтвердять» · game-logic/constraints · 🌱.
  - `+wound-by-own-egg` «Знищення сутності, яку створив ворог, ранить ворога» · entities/combat · 📎.
  - `+advancing-hazard-front` (вже пропонована) — болото знизу; `+chunk-generation` (вже пропонована) — чанки по 8 рядків.

## Пропозиції до словників
- `+effect:purge` — позначити клітину й через N с перевірити: небезпека знищується або позначка стає хибною.
- `+effect:retreat` — ворог відходить на N кроків назад своїм шляхом (після укусу чи поранення).
- `+axis:scroll` — тут `forced` (автоскрол із прискоренням).
- `+feature:mode-sudden-death` — режим з одним життям і окремим рекордом.
- `+card:facing-reveal`, `+card:live-recount-clue`, `+card:enemy-lays-hazards`, `+card:timed-purge-flag`, `+card:toxic-trail`, `+card:stale-clue`, `+card:wound-by-own-egg` — див. вище.

## Джерела
- ⭐ [itch.io: Venom Sweep](https://houjousxnnyside.itch.io/venom-sweep) — опис іспанською: живі числа, змія з візерунками Barrido/Zigzag/Carga і 3 кроками телеграфу, пурга 1 с, рана й уповільнення змії, отруйний слід із «?», нескінченний скрол, комбо ×4, режими, керування; Godot 4.7, прототип, опубліковано 28.10.2026.
- Збірка гри (`index.pck`, GDScript-токени, збірка 28.10.2026) — константи `Tuning` (12 стовпців, швидкості скролу, змії, отрути, яєць, очки), `Grid` (прапорці клітин, що рахується в числі), `SerpentModel` (три візерунки), `Scoring`, `Difficulty`, тексти `HelpScreen`, HUD і паузи.
- YouTube: пошук «Venom Sweep gameplay».

## Непевне
- (?) Усі числа — з однієї збірки-прототипу (28.10.2026); автор може їх міняти.
- (?) Чи довідка відкривається сама перед першим забігом (у коді є прапорець `help_seen`, поведінку не бачив наживо).
- (?) Фіксоване зерно світу означає однакові природні яйця щозабігу — висновок з коду, наживо не перевірено.
- (?) Чи стає змія небезпечною тілом (у коді шкодить лише голова; тіло лише блокує прохід).
