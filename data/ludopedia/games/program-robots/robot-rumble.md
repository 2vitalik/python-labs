---
title: Robot Rumble
slug: robot-rumble
aka: [RR, rumblebot]
family: program-robots
also: [tactics]
klass: figure
axes:
  field: square
  time: programmed
  opponent: online
  info: full
  random: runtime
  goal: score
year: 2020
platforms: [web, local CLI]
links:
  - {kind: official, url: "https://rr-docs.readthedocs.io/en/latest/", best: true, note: "огляд правил: арена 19×19, 5 HP, удар 1, спавн щодесять ходів, 100 ходів, функція robot(state, unit)"}
  - {kind: official, url: "https://rr-docs.readthedocs.io/en/latest/api.html", note: "API: State, Obj, Coords, Direction, Action, debug, MAP_SIZE, SPAWN_COORDS, HILL_COORDS"}
  - {kind: official, url: "https://rr-docs.readthedocs.io/en/latest/quickstart.html", note: "приклади: найближчий ворог, спільна ціль, init_turn"}
  - {kind: official, url: "https://rr-docs.readthedocs.io/en/latest/debugging.html", note: "debug.inspect, debug.locate, лог, помилки роботів"}
  - {kind: official, url: "https://rr-docs.readthedocs.io/en/latest/publishing.html", note: "чернетки, дошки (boards), сезони, матчмейкер, деактивація"}
  - {kind: official, url: "https://rr-docs.readthedocs.io/en/latest/rumblebot.html", note: "CLI rumblebot: локальні бої в терміналі чи веб-GUI"}
  - {kind: official, url: "https://rr-docs.readthedocs.io/en/latest/technical-details.html", note: "wasm (Wasmer), RustPython і QuickJS, Lambda + SQS"}
  - {kind: official, url: "https://github.com/robot-rumble/logic", note: "рушій на Rust (GPL-3.0), lang-runners, env-runners"}
  - {kind: other, url: "https://raw.githubusercontent.com/robot-rumble/logic/master/logic/src/lib.rs", note: "порядок ходу, пріоритет руху, блок обміну, атаки, спавн дзеркальними парами, Hill"}
  - {kind: other, url: "https://raw.githubusercontent.com/robot-rumble/logic/master/logic/src/types.rs", note: "дефолти спавну 4/4/10, GameMode Normal/NormalHeal/Hill, ActionType Move/Attack/Heal"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=robot+rumble+programming+game", note: "пошук"}
stage: v1
coverage: 75
mechanics: [move-4dir, hp-damage, spawn-schedule, spawn-points, impassable-cells, replay, state-as-data, game-loop, ai-greedy, +swarm-same-program, +per-unit-function, +simultaneous-hidden-orders, +move-conflict-cancel, +move-priority-by-direction, +swap-blocked, +spawn-zone-clear, +symmetric-map-generation, +damage-by-attacker-count, +friendly-fire, +king-of-the-hill, +local-referee, +wasm-sandbox, +board-seasons]
proposes: ["+cond:in_zone(a, zone)", "+cond:idle(a)", "+ui:unit-inspector", "+window:replay-viewer", "+feature:bot-upload", "+feature:local-referee"]
author: opus
date: 2026-11-09
---

# Robot Rumble — одна функція `robot(state, unit)` керує кожним твоїм солдатом на круглій арені 19×19

## Суть
Онлайн-арена ботів 1v1 (2020 (?)): гравець пише на Python або JavaScript одну функцію, яку рушій викликає щоходу для кожного свого робота; вона повертає «рух» або «атаку» в одному з 4 напрямків. Кожні 10 ходів на краю арени зʼявляються підкріплення, а тих, хто лишився стояти на клітинах спавну, прибирає. Після 100 ходів виграє команда з більшою кількістю роботів. Глобальний стан між викликами дозволено — координацію загону гравець пише сам.

## Поле і час
- Сітка 19×19; стіни — клітини з квадратом відстані до центру (9, 9) ≥ 81, тобто кругла арена (документація називає її октагоном).
- Клітини спавну — внутрішні клітини, сусідні зі стіною (зелене кільце вздовж краю).
- Режим Hill: 9 клітин навколо центру — «пагорб».
- Хід: обидві програми виконуються паралельно → рушій валідує дії → рух → атаки → (лікування в NormalHeal) → запис кадру.
- Партія — 100 ходів (`max_turn` у рушії); інформація повна.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Солдат (Unit/Soldier) | piece | команда Red/Blue, 5 HP, `id`, `coords` | щоходу одна дія: рух або атака в 4 напрямки (або нічого) |
| Стіна (Terrain/Wall) | static | — | непрохідна; задає круглу арену |
| Клітина спавну | zone | `is_spawn()` | тут зʼявляються підкріплення; стоїш тут під час спавну — зникаєш |
| Пагорб (Hill) | zone | 9 клітин центру, `is_hill()` | очко команді за кожного юніта, що стоїть тут і не діяв |
| Програма команди | player | `robot()`, опційно `init_turn()`, глобальні змінні | один код на всіх роботів команди |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start` → ТО `custom: «init_turn(state) один раз для команди»`, потім `custom: «robot(state, unit) для кожного свого юніта → Action або None»`; обидві команди — паралельно.
- КОЛИ `schedule(хід 1, далі щодесять ходів)` → ТО `custom: «прибрати всіх юнітів, що стоять на клітинах спавну»`, потім `spawn_at(soldier, spawn_pair)` ×4 кожній команді.
- КОЛИ `spawned(soldier)` → ЯКЩО `free(cell)` and `free(mirror_cell)` → ТО `custom: «синій у клітині, червоний у дзеркальній (18 − x, 18 − y)»`; вільних пар нема — спавну менше.
- КОЛИ `input(action)` → ЯКЩО `custom: «дія невалідна: чужий чи неіснуючий id тощо»` → ТО `custom: «ігнорується, юніт стоїть»`.
- КОЛИ `exec(move dir)` → ЯКЩО `custom: «кілька юнітів ідуть в одну клітину»` → ТО `custom: «виграє один за пріоритетом N > E > S > W»`, решта `block`.
- КОЛИ `exec(move dir)` → ЯКЩО `custom: «юніт у цілі йде назустріч, в мою клітину»` → ТО `block` для обох (обмін заборонено).
- КОЛИ `exec(move dir)` → ЯКЩО `not free(target)` після руху інших → ТО `block`; `custom: «ланцюжок: хто йде за юнітом, що звільнив клітину, проходить»`.
- КОЛИ `phase_start(attack)` → ТО `damage(target_cell, n)`, де n — кількість атак у цю клітину (сила 1); цілі — за позиціями **після** руху.
- КОЛИ `exec(attack dir)` → ЯКЩО `occupied(target, ally)` → ТО `damage(ally, 1)` — дружній вогонь; порожня клітина — нічого.
- КОЛИ `custom: «юніт отримав смертельний удар цього ходу»` → ТО `custom: «його власна атака все одно спрацьовує»` (цілі зібрані до застосування).
- КОЛИ `hp_zero(soldier)` → ТО `disappear(soldier)`.
- **NormalHeal**: КОЛИ `exec(heal dir)` → ТО `heal(target, 1)`, максимум 5; команду цілі не перевіряють.
- **Hill**: КОЛИ `turn_end` → ЯКЩО `occupied(hill, soldier)` and `custom: «юніт цього ходу повернув None»` → ТО `score(+1)` його команді (крім останнього ходу).
- КОЛИ `custom: «програма команди впала: InitError, Timeout, IO…»` → ТО `game_over`; виграє команда без помилки, обидві з помилкою → `draw`.
- КОЛИ `custom: «помилка в одному виклику robot()»` → ТО `custom: «юніт не діє, позначка ⚠ на мапі; бій триває»`.
- КОЛИ `counter(turn, ==, 100)` → ТО `game_over`: більше юнітів на арені → `win`; порівну → `draw`. Hill — більше очок пагорба.
- Перемога: більше роботів після 100 ходів (Hill — очки) · Поразка: менше роботів або падіння програми · Рахунок: кількість живих юнітів.

## Керування і ввід
- Ввід — код: `def robot(state, unit): return Action.move(Direction.East)` (JS — `function robot(state, unit)`, camelCase).
- `State`: `turn`, `our_team`, `other_team`, `obj_by_id`, `ids_by_team`, `objs_by_team`, `id_by_coords`, `obj_by_coords`.
- `Coords`: `x`, `y`, `is_spawn()`, `is_hill()`, `distance_to`, `walking_distance_to`, `direction_to`, `+`/`−`/`*`; `Direction`: `North/South/East/West`, `opposite`, `rotate_cw`, `rotate_ccw`, `to_coords`.
- Дебаг: `print`/`console.log` — спільний лог ходу; `debug.inspect(key, val)` — таблиця значень біля робота; `debug.locate(unit)` — зірочка на мапі.
- Локально — CLI `rumblebot`: робот з диска, бій у терміналі або веб-GUI, створення й оновлення роботів з командного рядка.

## Вікна, меню, HUD
- `code-editor-window` (веб): редактор коду, запуск бою проти обраного робота, лог ходу в нижньому правому куті (?).
- `replay-viewer`: арена по ходах, відтінок робота = здоровʼя, вибір робота → `unit-inspector` з таблицею `debug.inspect`, зірочка `locate`, ⚠ помилки.
- `leaderboard` дошки (board): опубліковані роботи, бої між ними; дошка може належати сезону.
- Переходи: чернетка → тестовий бій → Publish на дошку → матчмейкер → бої дошки.

## Фічі поза полем
- Чернетки й публікація на конкретну дошку; сезони — дошки з обмеженим часом.
- Матчмейкер ставить бої після публікації і далі кожні X годин; робот деактивується після 2 фатальних помилок поспіль, 2 запусків довше 3 хв, 14 днів без нової версії або вручну.
- Пісочниця: кожна програма — WebAssembly (Wasmer; Python через RustPython, JS через QuickJS); доступу до системи нема, крім часу й ентропії; зовнішні бібліотеки не підключаються.
- `local-referee`: відкритий рушій на Rust (GPL-3.0), той самий у браузері, на десктопі й на сервері (AWS Lambda + SQS).
- Debug-дані недоступні в боях матчмейкера.

## Варіації й родичі
- Режими рушія: `Normal`, `NormalHeal` (дія лікування), `Hill` (утримання центру); тип мапи `Rect` є в коді, але не використовується.
- Родичі: [gladiabots](gladiabots.md) (загін за спільною програмою), [ai-challenge-ants](ai-challenge-ants.md) (рій, одночасні накази), [screeps](screeps.md), [bot-arenas](bot-arenas.md); попередник за духом — RoboCode (неперервний простір).
- Осі варіацій: **одиниця коду** (функція на юніта / програма на команду / процес-бот); **розвʼязання руху** (пріоритет напрямку / обидва стоять / обмін дозволено); **мета** (більше юнітів / очки пагорба); **шкода** (сума атак / фокус); **дружній вогонь** (так / ні).

## Цікавинки для курсу
- Рушій на 100 ходів з двома студентськими `robot()`-функціями, імпортованими як модулі — 🥉.
- Розвʼязання руху: пріоритет напрямку, заборона обміну, ланцюжок звільнених клітин — 🥈 (порядок і каскад — пастка).
- Атаки за позиціями після руху, шкода = кількість атакувальників, загиблий теж бʼє — 📎.
- Спавн дзеркальними парами + «очищення» клітин спавну — 🌱.
- Бот «фокус на одній цілі» через глобальний стан і `init_turn` — 🥉; рій з формацією й відходом поранених — 🥇.
- Hill: очко лише юніту, що не діяв, — компроміс захоплення і бою — 📎.

## Мапа на каталог
- Є: `move-4dir` · `hp-damage` (5 HP, удар 1) · `spawn-schedule` (кожні 10 ходів, 4 юніти) · `spawn-points` (кільце спавну) · `impassable-cells` (стіни) · `replay` · `state-as-data` · `game-loop` · `ai-greedy` (приклад «до найближчого ворога»).
- **Нема** → пропозиції карток:
  - `+swarm-same-program`, `+simultaneous-hidden-orders`, `+local-referee`, `+symmetric-map-generation` — з [bot-arenas](bot-arenas.md); `+move-conflict-cancel` — з [lux-ai](lux-ai.md).
  - `+per-unit-function` «Функція викликається для кожного юніта окремо» · game-logic/program · 📎.
  - `+move-priority-by-direction` «Конфлікт за клітину: перемагає напрямок за пріоритетом» · entities/legality · 🌱.
  - `+swap-blocked` «Обмін місцями зустрічних — обидва стоять» · entities/legality · 🌱.
  - `+spawn-zone-clear` «Перед спавном зона очищується від юнітів» · entities/spawn · 🌱.
  - `+damage-by-attacker-count` «Шкода = кількість атак у клітину» · entities/combat · 🌱.
  - `+friendly-fire` «Атака бʼє і своїх» · entities/combat · 🌱.
  - `+king-of-the-hill` «Очки за утримання центральної зони» · game-logic/score · 📎.
  - `+wasm-sandbox` «Код гравця в пісочниці з лімітом часу» · code/architecture · 🥇.
  - `+board-seasons` «Дошки й сезони з матчмейкером» · interface/results · 🥉.

## Пропозиції до словників
- `+cond:in_zone(a, zone)` — А в зоні (клітина спавну, пагорб, своя половина поля).
- `+cond:idle(a)` — юніт цього ходу не діяв (Hill); пара до тригера `idle(n)`, що стосується гравця.
- `+ui:unit-inspector` — таблиця значень, які код записав для обраного юніта (debug.inspect).
- `+window:replay-viewer` · `+feature:bot-upload` · `+feature:local-referee` — підтвердження з bot-arenas.

## Джерела
- ⭐ [rr-docs: огляд](https://rr-docs.readthedocs.io/en/latest/) — арена, 5 HP, удар 1, дружній вогонь, спавн щодесять ходів, 100 ходів, сигнатура `robot`.
- [API reference](https://rr-docs.readthedocs.io/en/latest/api.html) — усі класи й константи; [Quickstart](https://rr-docs.readthedocs.io/en/latest/quickstart.html) — приклади стратегій.
- [Debugging](https://rr-docs.readthedocs.io/en/latest/debugging.html) · [Publishing](https://rr-docs.readthedocs.io/en/latest/publishing.html) · [rumblebot](https://rr-docs.readthedocs.io/en/latest/rumblebot.html) · [Technical details](https://rr-docs.readthedocs.io/en/latest/technical-details.html).
- [robot-rumble/logic](https://github.com/robot-rumble/logic) — структура рушія; [lib.rs](https://raw.githubusercontent.com/robot-rumble/logic/master/logic/src/lib.rs) — порядок ходу, рух, атаки, спавн, Hill, помилки; [types.rs](https://raw.githubusercontent.com/robot-rumble/logic/master/logic/src/types.rs) — дефолти й перелічення.
- Сайт гри не лінкую: за даними черги домен тепер редиректить на спам.

## Непевне
- (?) Рік запуску (2020) — з черги, не перевірено.
- (?) Пріоритет N > E > S > W: незрозуміло, чи це напрямок руху юніта, чи бік, з якого він заходить у клітину; документація каже «за годинниковою стрілкою від North».
- (?) Ліміт часу на хід у боях не знайшов; у рушії є помилка `Timeout(Duration)`, у матчмейкері — 3 хв на весь бій.
- (?) Рейтингова система дошок і вигляд веб-редактора — у документації не описані.
- (?) Валідація «targeting an enemy unit» — з переказу коду; точний перелік невалідних дій не дивився.
