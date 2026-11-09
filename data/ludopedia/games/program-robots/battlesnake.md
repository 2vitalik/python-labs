---
title: Battlesnake
slug: battlesnake
aka: [Battle Snake]
family: program-robots
also: [maze-arcade]
klass: avatar
axes:
  field: square
  time: programmed
  opponent: online
  info: full
  random: both
  goal: survive
year: 2015
platforms: [web, local CLI]
links:
  - {kind: official, url: "https://docs.battlesnake.com/rules", best: true, note: "правила: колізії, здоровʼя, їжа, небезпеки, три стадії ходу й порядок розвʼязання"}
  - {kind: official, url: "https://github.com/BattlesnakeOfficial/rules", note: "рушій на Go (AGPL-3.0): standard, royale, constrictor, wrapped, solo, maps/, CLI"}
  - {kind: other, url: "https://raw.githubusercontent.com/BattlesnakeOfficial/rules/main/standard.go", note: "стадії Movement → Starvation → HazardDamage → FeedSnakes → Elimination, голова в голову"}
  - {kind: other, url: "https://raw.githubusercontent.com/BattlesnakeOfficial/rules/main/constants.go", note: "розміри 7/11/19/21/25, SnakeMaxHealth 100, SnakeStartSize 3, причини вибування"}
  - {kind: other, url: "https://raw.githubusercontent.com/BattlesnakeOfficial/rules/main/cli/README.md", note: "CLI: 11×11, timeout 500 мс, foodSpawnChance 15, minimumFood 1, hazardDamagePerTurn 14, shrinkEveryNTurns 25"}
  - {kind: official, url: "https://docs.battlesnake.com/api/webhooks", note: "GET /, POST /start, /move, /end; відповідь move + shout ≤ 256 символів"}
  - {kind: official, url: "https://docs.battlesnake.com/maps", note: "карти Standard, Royale, Constrictor, Snail Mode"}
  - {kind: official, url: "https://docs.battlesnake.com/maps/royale", note: "небезпеки наступають від країв кожні 25 ходів, −14 HP"}
  - {kind: official, url: "https://docs.battlesnake.com/maps/snail-mode", note: "хвіст лишає стек небезпек завдовжки зі змійку, стек тане по 1"}
  - {kind: official, url: "https://docs.battlesnake.com/guides/leaderboards", note: "TrueSkill, рейтинг μ − 3σ → 0…10 000, щоденні прогони"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=battlesnake+gameplay", note: "пошук; реплеї й розбори ботів"}
stage: v1
coverage: 75
mechanics: [move-4dir, move-auto, body-queue, self-collision, wrap-edges, hunger-clock, hp-damage, spawn-random-cell, spawn-points, environment-death, touch-death, replay, leaderboard, rating-system, online-multiplayer, state-as-data, game-loop, +http-webhook-bot, +turn-time-limit, +simultaneous-hidden-orders, +head-to-head-length-wins, +collect-then-apply-eliminations, +default-move-on-timeout, +shrinking-hazard-zone, +hazard-stack-decay, +food-min-and-chance, +shout-message, +local-referee, +rule-stage-pipeline]
proposes: ["+cond:greater(a, b, prop)", "+trigger:timeout(bot)", "+effect:eliminate(bot)", "+effect:decay(a, n)", "+feature:webhook-bot", "+feature:local-referee", "+window:replay-viewer", "+ui:shout-bubble"]
author: opus
date: 2026-11-09
---

# Battlesnake — змійка, якою керує твій веб-сервер: щоходу HTTP-запит, 500 мс на відповідь, голова в голову виживає довша

## Суть
Багатокористувацька змійка для програмістів: кожну змійку веде окремий веб-сервер автора, рушій щоходу шле йому JSON зі станом поля, сервер відповідає одним словом — `up`/`down`/`left`/`right`. Усі змійки ходять одночасно, кожна щоходу втрачає 1 здоровʼя й мусить їсти; зіткнення з тілом, стіною чи коротшою головою — вибування. Виграє остання жива. Рушій відкритий (Go), є CLI для локальних матчів і онлайн-ліги з TrueSkill.

## Поле і час
- Квадратна сітка; стандартні розміри 7×7, 11×11, 19×19 (є 21 і 25 у константах); дефолт CLI — 11×11. Карта Arcade Maze — фіксовано 19×21.
- Координати `(x, y)`, `up` = y+1 (тобто (0,0) — лівий нижній кут).
- Хід = три стадії: **Requests** (рушій паралельно шле `/move` усім змійкам) → **Responses** (обмежений час на відповідь) → **Resolution** (рушій застосовує всі ходи разом).
- Розвʼязання у standard — конвеєр стадій: `GameOver → Movement → Starvation → HazardDamage → FeedSnakes → Elimination`, потім карта додає їжу/небезпеки (`PostUpdateBoard`).
- Інформація повна: кожна змійка бачить усе поле, здоровʼя й тіла суперників.
- Старт: змійка довжини 3 згорнута в одну клітину (3 сегменти в одній точці) і «розгортається» за перші ходи; до 8 змійок — у фіксованих точках (кути на відстані 1 від краю й середини сторін), більше — розподіл по квадрантах.

### Режими (game type) і карти
| Назва | Що змінює |
|---|---|
| `standard` | базові правила; карта Standard: 1–16 змійок, непарні розміри 7…25 |
| `solo` | одна змійка; гра йде, доки вона жива (тренування на виживання) |
| `wrapped` | край поля — тор: голова виходить з протилежного боку |
| `constrictor` | їжі нема, кожна змійка росте щоходу, здоровʼя завжди 100 — бій за простір |
| `wrapped_constrictor` | constrictor на торі |
| `royale` | кожні N ходів одна випадкова сторона безпечної зони зсувається на 1 всередину; зовні — небезпека |
| Snail Mode (карта) | там, де пройшов хвіст, лишається стек небезпек висотою = довжина змійки; стек тане на 1 щоходу |
| `hz_*` (карти) | статичні (внутрішня стіна, кільця, колони) або ростучі (спіраль кожні 3 ходи, розкид кожні 2, бокс кожні 12/20) зони небезпек |
| Sinkholes | у центрі зʼявляється «вирва», що росте кільцем без кутів кожні 10 ходів |
| Healing Pools | кілька фіксованих одноклітинних зон за розміром поля (1 / 2 / 4) |
| Arcade Maze | лабіринт 19×21, стіни — смертельні небезпеки; їжа лише в 12 точках |

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Змійка (бот) | player | `id`, `health` 0–100, `body` (голова → хвіст), `length`, `latency`, `shout`, `squad` | щоходу рухається на 1; тіло — черга сегментів |
| Голова | player | `head` = `body[0]` | визначає всі зіткнення |
| Тіло / хвіст | static | сегменти | непрохідне для всіх; хвіст звільняє клітину, якщо змійка не їла минулого ходу |
| Їжа | pickup | — | здоровʼя → 100, +1 сегмент; спавн за мінімумом і шансом |
| Небезпека (hazard) | hazard | `damagePerTurn` (дефолт 14) | голова на ній без їжі — додаткова шкода |
| Стек небезпек (Snail) | hazard | висота = довжина змійки | шкода × висота; −1 щоходу |
| Безпечна зона (Royale) | zone | межі minX..maxX, minY..maxY | звужується з випадкової сторони |
| Край поля | static | — | вихід за край = вибування (крім wrapped) |
| Рушій (referee) | — | seed, ruleset, map | шле запити, застосовує стадії, пише реплей |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start` → ТО `custom: «рушій паралельно шле POST /move кожній живій змійці: game, turn, board, you»`.
- КОЛИ `custom: «нема відповіді за game.timeout»` → ТО `move(snake, dir)` у попередньому напрямку (шия → голова), `custom: «latency = timeout»`; напрям не визначити → `up`.
- КОЛИ `input(move)` → ЯКЩО `custom: «значення не up/down/left/right»` → ТО теж хід за замовчуванням.
- КОЛИ `phase_start(movement)` → ТО `move(head, dir)` і `custom: «останній сегмент хвоста знімається»` (усі змійки одночасно).
- КОЛИ `phase_start(starvation)` → ТО `damage(snake, 1)` кожній живій змійці.
- КОЛИ `phase_start(hazard)` → ЯКЩО `occupied(head_cell, hazard)` and `not occupied(head_cell, food)` → ТО `damage(snake, damagePerTurn)`; здоровʼя обрізається до 0…100; ≤ 0 → `disappear(snake)` з причиною `hazard`.
- КОЛИ `contact(head, food)` → ТО `custom: «health = 100»`, `grow(snake, 1)` (копія хвоста — сегмент зʼявляється наступного ходу), `disappear(food)`; кілька голів на одній їжі — їдять усі.
- КОЛИ `phase_start(elimination)` → ЯКЩО `counter(health, <=, 0)` → ТО `disappear(snake)` (`out-of-health`) — одразу.
- КОЛИ `edge(head)` → ЯКЩО `not mode(wrapped)` → ТО `disappear(snake)` (`wall-collision`); ЯКЩО `mode(wrapped)` → ТО `wrap(head)`.
- КОЛИ `contact(head, own_body)` → ТО `disappear(snake)` (`snake-self-collision`).
- КОЛИ `contact(head, other_body)` (будь-який сегмент, крім голови) → ТО `disappear(snake)` — гине той, хто вʼїхав (`snake-collision`).
- КОЛИ `contact(head, other_head)` → ЯКЩО `custom: «довжина A ≤ довжини B»` → ТО `disappear(A)`; рівні — гинуть обидві (`head-collision`).
- Самозіткнення, тіла й голови спершу **збираються** для всіх змійок (сортування за довжиною), потім застосовуються разом: змійка, що вибуває цього ходу, все одно вбиває того, хто вʼїхав у її тіло.
- КОЛИ `contact(head, tail_cell)` → ЯКЩО `custom: «власник хвоста не їв минулого ходу»` → ТО безпечно (хвіст уже зрушив); інакше — зіткнення з тілом.
- КОЛИ `phase_start(food)` → ЯКЩО `count(food, <, minimumFood)` → ТО `spawn_at(food, random_free)` до мінімуму; інакше ЯКЩО `prob(foodSpawnChance %)` → ТО `spawn_at(food, random_free)` ×1.
- КОЛИ `game_start` → ТО `custom: «їжа діагонально біля кожної змійки (від центру, не в кут) + одна в центрі»` (квадратне поле ≥ 7).
- **Royale**: КОЛИ `timer(shrinkEveryNTurns)` → ТО `custom: «одна з 4 сторін (випадково) безпечної зони зсувається на 1 всередину»`, `set_cell(outside_zone, hazard)`; небезпека під щойно зайшовшою змійкою шкодить з наступного ходу.
- **Constrictor**: КОЛИ `tick` → ТО `grow(snake, 1)`, `custom: «health = 100»`; `custom: «їжа не спавниться»`.
- **Snail Mode**: КОЛИ `leave(tail, cell)` → ЯКЩО `custom: «у клітину не вʼїжджає інша змійка слідом»` → ТО `spawn_at(hazard_stack(length), cell)`; КОЛИ `tick` → ТО `custom: «висота стеку −1»`; шкода = `damagePerTurn × висота`.
- **hz_spiral / hz_scatter / hz_grow_box / hz_expand_box / sinkholes**: КОЛИ `timer(3 | 2 | 12 | 20 | 10)` → ТО `set_cell(next_cell_or_ring, hazard)`.
- КОЛИ `input(shout)` → ТО `message(text ≤ 256)` усім змійкам наступного ходу.
- КОЛИ `custom: «живих змійок ≤ 1»` → ТО `game_over`; остання жива → `win`. **Solo**: КОЛИ `all_gone(snake)` → ТО `game_over`.
- Перемога: остання жива змійка · Поразка: вибування (здоровʼя, край, тіло, голова, небезпека) · Рахунок: місце в матчі → TrueSkill у лізі.

## Керування і ввід
- Гравець пише **веб-сервер** будь-якою мовою: `GET /` (вигляд: `apiversion` "1", `color` #RRGGBB, `head`, `tail`, `author`), `POST /start`, `POST /move` (відповідь `{"move": "up", "shout": "…"}`), `POST /end`.
- Тіло запиту: `game` (ruleset, map, timeout), `turn`, `board` (розміри, `food`, `hazards`, `snakes`), `you`.
- Локально: `battlesnake play -W 11 -H 11 --name A --url http://… -g solo -v` — прапорці `--timeout 500`, `--gametype`, `--map`, `--foodSpawnChance 15`, `--minimumFood 1`, `--hazardDamagePerTurn 14`, `--shrinkEveryNTurns 25`, `--seed`, `--output` (JSON-лог), `--browser` (відкрити у board viewer), `--sequential`, `--delay`.
- Ручного керування нема: ввід — лише код сервера.

## Вікна, меню, HUD
- `replay-viewer` (board.battlesnake.com): поле, змійки кольорами власників, їжа, небезпеки, номер ходу, перемотування; CLI відкриває його з `--browser`.
- `leaderboard`: щоденні ліги за картами, рейтинг 0…10 000.
- Дашборд автора: створення змійки (Server URL), список ігор з реплеями, турніри (?).
- HUD реплея: імʼя, здоровʼя й довжина кожної змійки, `latency`, `shout`-повідомлення (?).
- Переходи: дашборд → створити гру (карта, розмір, змійки) → реплей → ліга/турнір.

## Фічі поза полем
- `bot-upload` у формі «вкажи URL свого сервера»; хостинг — справа автора (регіони рушія для низької латентності).
- `leaderboard-online` з TrueSkill: кожна ліга прогониться раз на 24 год (6–10 год ігор), матчмейкінг близьких за рангом; щомісячні Battlesnake Points за місце.
- Турніри й змагання; глобальний рейтинг гравця = сума ліг (експериментально).
- `local-referee`: відкритий рушій + CLI, `seed-input`, JSON-вивід ходів, `custom-rules` через параметри (`foodSpawnChance`, `minimumFood`, `damagePerTurn`, `shrinkEveryNTurns`).
- Стартові проєкти на різних мовах; кастомізація вигляду змійки (колір, голова, хвіст).
- Squad Mode (параметри `sharedElimination`, `sharedHealth`, `sharedLength`, поле `squad`) — командні змійки (?).

## Варіації й родичі
- Класична змійка — [snake](../maze-arcade/snake.md); масова онлайн-змійка — [slither-io](../maze-arcade/slither-io.md); світлові цикли — [armagetron-advanced](../maze-arcade/armagetron-advanced.md) і Tron Battle у [bot-arenas](bot-arenas.md).
- Інші арени ботів сімʼї: [codingame-hypersonic](codingame-hypersonic.md), [ai-challenge-ants](ai-challenge-ants.md), [screeps](screeps.md).
- Осі варіацій: **край** (смерть / тор); **їжа** (мінімум + шанс / відсутня, ріст щоходу); **небезпеки** (нема / звуження зони / сліди хвоста, що тануть / ростуча спіраль); **колізія голів** (довша виживає / обидві гинуть); **кількість** (solo / дуель / до 16); **таймаут** (повтор напрямку / вибування).

## Цікавинки для курсу
- Рушій Battlesnake на Python як конвеєр стадій (рух → голод → небезпеки → їжа → вибування) з JSON-станом — 🥈: стадії = функції, режими = інший список стадій.
- Вибування «спершу зібрати, потім застосувати» з голова-в-голову за довжиною — 🥉: класична пастка порядку перевірок.
- Хвіст безпечний лише тоді, коли змійка не їла (подвоєний сегмент) — 📎.
- Бот-сервер на FastAPI з `/move` і локальний матч через CLI — 📎.
- Бот flood fill + minimax/paranoid на 2–4 змійки з бюджетом 500 мс (ітеративне поглиблення) — 🥇.
- Royale-звуження з випадкової сторони і Snail-стеки, що тануть — 🥉.
- Ліга групи з TrueSkill (μ − 3σ) — 🥈.

## Мапа на каталог
- Є: `move-4dir` · `move-auto` (стоп нема; без відповіді — продовжує напрям) · `body-queue` · `self-collision` (смерть) · `wrap-edges` (wrapped) · `hunger-clock` (здоровʼя −1 щоходу, їжа відновлює) · `hp-damage` (небезпеки) · `spawn-random-cell` (їжа) · `spawn-points` (фіксовані старти) · `environment-death` · `touch-death` · `replay` · `leaderboard` · `rating-system` · `online-multiplayer` · `state-as-data` · `game-loop`.
- **Нема** → пропозиції карток:
  - `+http-webhook-bot` «Бот — HTTP-сервер, що відповідає на запити рушія» · code/architecture · 🥉.
  - `+turn-time-limit`, `+simultaneous-hidden-orders`, `+local-referee` — з [bot-arenas](bot-arenas.md).
  - `+head-to-head-length-wins` «Зіткнення голів: виживає довша, рівні — обидві» · entities/combat · 📎.
  - `+collect-then-apply-eliminations` «Вибування рахуються на знімку й застосовуються разом» · game-logic · 📎.
  - `+default-move-on-timeout` «Без відповіді — повтор попереднього ходу» · game-logic/opponent · 🌱.
  - `+shrinking-hazard-zone` «Зона безпеки звужується з випадкової сторони» · game-logic/waves · 📎.
  - `+hazard-stack-decay` «Слід лишає стек шкоди, що тане щотіку» · entities/state · 🥉.
  - `+food-min-and-chance` «Спавн: добрати до мінімуму, інакше з шансом» · entities/spawn · 🌱.
  - `+shout-message` «Коротке повідомлення суперникам на наступний хід» · interface/hud · 🌱.
  - `+rule-stage-pipeline` «Правила як упорядкований список стадій; режим = інший список» · code/architecture · 🥈.

## Пропозиції до словників
- `+cond:greater(a, b, prop)` — А більше за Б за властивістю (довжина змійки, кораблі флоту, ранг робота); пара до `same`.
- `+trigger:timeout(bot)` — підтвердження з bot-arenas; тут — не вибування, а хід за замовчуванням.
- `+effect:eliminate(bot)` — підтвердження; з причиною (`out-of-health`, `wall-collision`, `head-collision`…).
- `+effect:decay(a, n)` — лічильник/стек сутності зменшується щотіку до 0 (Snail-стеки; біти Terminal).
- `+feature:webhook-bot` — бот як веб-сервер за URL замість завантаження коду.
- `+feature:local-referee` — підтвердження (CLI з тими самими правилами).
- `+window:replay-viewer` — підтвердження (board viewer).
- `+ui:shout-bubble` — текст бота над змійкою в реплеї (?).

## Джерела
- ⭐ [Battlesnake Game Rules](https://docs.battlesnake.com/rules) — мета, колізії, здоровʼя, їжа, небезпеки, три стадії й порядок розвʼязання.
- [BattlesnakeOfficial/rules](https://github.com/BattlesnakeOfficial/rules) — рушій: `standard.go` (стадії, голова в голову, сортування за довжиною), `constants.go` (100 HP, довжина 3, розміри, причини), `royale.go`, `constrictor.go`, `wrapped.go`, `solo.go`, `board.go` (старти, їжа), `maps/` (`standard`, `hazards` з hz_*, `sinkholes`, `healing_pools`, `arcade_maze`, `snail_mode`…).
- [CLI README](https://raw.githubusercontent.com/BattlesnakeOfficial/rules/main/cli/README.md) — прапорці й дефолти.
- [Webhooks](https://docs.battlesnake.com/api/webhooks) і [Battlesnake object](https://docs.battlesnake.com/api/objects/battlesnake) — протокол і поля змійки.
- [Maps](https://docs.battlesnake.com/maps) · [Royale](https://docs.battlesnake.com/maps/royale) · [Snail Mode](https://docs.battlesnake.com/maps/snail-mode).
- [Leaderboards](https://docs.battlesnake.com/guides/leaderboards) — TrueSkill, розклад, матчмейкінг, Points.

## Непевне
- (?) Рік появи (2015) і місце (Вікторія, Канада) — з памʼяті; документація історії не містить.
- (?) Інтервал Royale: сторінка карти каже 25 ходів (і дефолт CLI 25), а код `royale.go` має дефолт 20 — на сервері, ймовірно, 25.
- (?) Код `maps/standard.go` порівнює `100 − rand(100) < chance` строго — реальна ймовірність спавну ≈ (chance − 1) %.
- (?) Healing Pools: код лише ставить клітини-небезпеки; лікування, мабуть, дає відʼємна шкода в налаштуваннях карти — не перевірено.
- (?) Нічия, коли останні змійки гинуть одночасно, і очки solo-режиму — не бачив у джерелах.
- (?) Вигляд дашборда, HUD реплея, турніри й Squad Mode — сторінок не відкривав.
