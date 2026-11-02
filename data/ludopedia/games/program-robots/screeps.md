---
title: Screeps (Screeps World, Screeps Arena)
slug: screeps
family: program-robots
also: [build-sim, tactics]
klass: figure
axes:
  field: square
  time: programmed
  opponent: online
  info: partial
  random: setup
  goal: territory
year: 2016
platforms: [web, PC (Steam), self-hosted server]
links:
  - {kind: official, url: "https://docs.screeps.com/introduction.html", best: true, note: "вступ: кімнати 50×50, рельєф і ціни руху, спавни, джерела, стіни, рампарти, safe mode"}
  - {kind: steam, url: "https://store.steampowered.com/app/464350/Screeps_World/", note: "Screeps: World — 16.11.2016; тік 2–5 с на шардах; WebAssembly-мови; приватні сервери"}
  - {kind: official, url: "https://docs.screeps.com/creeps.html", note: "частини тіла, втома, 1500 тіків життя, 50 частин, шкода по частинах"}
  - {kind: official, url: "https://docs.screeps.com/control.html", note: "GCL, RCL 1–8 і що відкриває кожен рівень, зниження контролера"}
  - {kind: official, url: "https://docs.screeps.com/game-loop.html", note: "тік: незмінний стан → скрипти всіх → одночасне застосування наказів"}
  - {kind: official, url: "https://docs.screeps.com/cpu-limit.html", note: "ліміт CPU на тік, bucket 10 000, +500 з bucket"}
  - {kind: official, url: "https://docs.screeps.com/simultaneous-actions.html", note: "пайплайни дій: які накази конфліктують в одному тіку"}
  - {kind: official, url: "https://docs.screeps.com/defense.html", note: "safe mode 20 000 тіків, вежі, стіни, рампарти"}
  - {kind: official, url: "https://docs.screeps.com/api/", note: "API: Game, Memory, PathFinder, Creep, BODYPART_COST"}
  - {kind: official, url: "https://github.com/screeps/screeps", note: "відкритий сервер: npx screeps init/start, моди, CLI"}
  - {kind: official, url: "https://store.screeps.com/", note: "World (MMO) і Arena (1v1 сезони)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=screeps+beginner+tutorial", note: "пошук; туторіали"}
stage: v1
coverage: 70
mechanics: [impassable-cells, floor-types, chase-bfs, hp-damage, round-currency, spawn-points, timed-despawn, projectile-shot, melee-vs-ranged, minimap-radar, leaderboard, save-progress, game-screen, state-as-data, +command-program, +tick-script-loop, +cpu-budget-bucket, +body-parts-composition, +fatigue-movement, +intent-resolution-simultaneous, +action-pipelines, +controller-level-unlocks, +persistent-world-offline, +room-graph-world, +structure-decay-repair, +source-regen, +safe-mode, +memory-persistence, +cost-matrix-pathfinding, +code-editor-window, +user-procedures, +swarm-separate-programs, +private-server-mods, +simulation-room]
proposes: ["+trigger:exec(cmd)", "+trigger:phase_start", "+trigger:tick", "+cond:has", "+cond:in_range", "+cond:body_count(a, part, op, n)", "+cond:fatigue(a, op, n)", "+effect:intent(a, action)", "+effect:harvest", "+effect:transfer", "+effect:build", "+effect:repair", "+effect:upgrade", "+effect:claim", "+effect:decay", "+role:spawner", "+role:resource", "+role:zone", "+role:tower", "+window:code-editor", "+window:world-map", "+window:output-console", "+ui:cpu-meter", "+ui:room-visual", "+feature:persistent-world", "+feature:simulation-room", "+feature:private-server", "+axis:actors"]
author: opus
date: 2026-11-02
---

# Screeps — MMO-стратегія, де юнітів (creeps) веде лише твій JavaScript, щотіку й без тебе

## Суть
Гравець не клікає юнітами: він пише JavaScript-модуль `main`, який сервер виконує **кожен тік** для всіх його кріпів, спавнів і веж — навіть коли гравець офлайн. Колонія добуває енергію з джерел, будує розширення й дороги, прокачує контролер кімнати, розширюється на сусідні кімнати й воює з чужим кодом у спільному персистентному світі. Ядро — програмування агентів під жорсткий бюджет CPU: кожен кріп — «тіло» з частин (WORK/MOVE/CARRY/ATTACK…), а вся поведінка — твій код. Screeps: Arena — окремий режим 1v1 матчів із сезонами.

## Поле і час
- Світ — **сітка кімнат** (граф: у кімнати 1–4 виходи), кожна кімната — квадратна сітка 50×50 клітин. Шарди звʼязані міжшардовими порталами («вісь Z»).
- Рельєф клітини: рівнина (втома 2 за кожну не-MOVE частину), болото (10), природна стіна (непрохідна); дорога-споруда — 1 і зношується.
- Тік: (1) стан світу заморожений, (2) скрипти всіх гравців читають його й видають накази-наміри, (3) усі накази застосовуються **одночасно** і незалежно; `creep.move()` не змінює `pos` до наступного тіку. Тік 2–5 с на офіційних шардах; приватний сервер — до 10 тіків/с.
- Видимість: бачиш лише кімнати, де є твій кріп/споруда (або спостерігач — observer); решта світу — `info: partial`.
- Глобальні змінні JS можуть стертись між тіками; надійна памʼять — обʼєкт `Memory` (JSON).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Кріп (creep) | figure | тіло до 50 частин, 100 HP на частину, життя 1500 тіків, втома, вантаж | виконує накази коду; шкода вибиває частини у порядку тіла |
| Частина WORK | — (модуль) | ціна 100 | добувати, будувати, ремонтувати, прокачувати контролер |
| Частина MOVE | — (модуль) | 50 | знімає 2 втоми/тік; повна швидкість, коли MOVE ≥ інших |
| Частина CARRY | — (модуль) | 50 | носити ресурс; порожня не дає втоми |
| ATTACK · RANGED_ATTACK | — (модуль) | 80 · 150 | ближній / дальній удар |
| HEAL · TOUGH · CLAIM | — (модуль) | 250 · 10 · 600 | лікувати / «броня» / захоплювати контролер (з CLAIM живе 600 тіків) |
| Спавн | spawner | енергія до 300, ≤3 на кімнату | будує кріпа з тіла за енергію |
| Розширення (extension) | resource | +50…200 енергії | дає спавну більше енергії для дорожчих тіл |
| Джерело енергії | resource | 3000 (нейтральне 1500, лігво 4000) | вичерпується; відновлюється раз на 300 тіків |
| Контролер кімнати | zone | RCL 0–8, таймер зниження | прокачка → нові споруди; без апгрейдів — падає до 0 і стає нейтральним |
| Вежа (tower) | tower | з RCL 3, 10 енергії на дію | атакує/лікує/ремонтує будь-де в кімнаті; слабшає з відстанню |
| Дорога | terrain | HP | втома 1; зношується від руху |
| Стіна (споруда) | static | від 1 до 300 млн HP | блокує всіх, включно зі своїми; не ближче 2 клітин до краю |
| Рампарт | gate | HP за RCL | свої проходять, чужі ні; кріп на ньому невразливий; гниє |
| Контейнер · сховище · лінк · лаб · термінал | container | за RCL | зберігання/пересилання/хімія ресурсів |
| Будмайданчик (construction site) | mark | тип споруди | WORK-кріпи вкладають енергію → споруда |
| NPC-загарбники, Source Keeper | enemy | — | атакують колонію; охороняють багаті джерела (?) |
| Мінерали, руїни, надгробки | resource | — | добуток / залишки ресурсів після загибелі |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ТО `custom: «виконати module.exports.loop гравця над замороженим станом»`; КОЛИ `phase_start(apply)` → ТО всі `intent` застосовуються одночасно.
- КОЛИ `custom: «скрипт перевищив CPU цього тіку»` → ТО `crash` (виконання обірвано, невидані накази втрачені); невитрачений CPU → `counter(bucket, +)` до 10 000; тік може взяти до +500 з bucket.
- КОЛИ `exec(move|moveTo)` → ЯКЩО `fatigue(creep, ==, 0)` and `free(target)` → ТО `move(creep, dir)`, `counter(fatigue, +k·terrain)` за кожну не-MOVE частину (дорога 1, рівнина 2, болото 10); щотік `counter(fatigue, −2·MOVE)`.
- КОЛИ `exec(harvest)` → ЯКЩО `in_range(creep, source, 1)` and `has(source, energy)` → ТО `harvest`: енергія в CARRY (≈2 за WORK/тік (?)).
- КОЛИ `exec(transfer|build|repair|upgradeController)` → ЯКЩО `in_range(creep, target, 1|3)` and `has(creep, energy)` → ТО `transfer` / `build` / `repair` / `upgrade`.
- КОЛИ `exec(spawnCreep(body))` → ЯКЩО `counter(room_energy, >=, Σ BODYPART_COST)` → ТО `spawn(creep)` через кілька тіків (≈3 тіки на частину (?)).
- КОЛИ `counter(age, ==, 1500)` → ТО `disappear_a` (кріп помирає від старості, лишає надгробок).
- КОЛИ `exec(attack)` → ЯКЩО `in_range(1)` → ТО `damage(n·ATTACK)`; `rangedAttack` — `in_range(3)`; `heal` → `heal(target)`; шкода вибиває частини в порядку тіла → `custom: «частина з 0 HP не працює»`.
- Кілька наказів з одного **пайплайну** в одному тіку → виконується лише правіший за пріоритетом (`build` перекриває `harvest`); повторний виклик того самого методу → перемагає останній; методи з різних пайплайнів сумісні.
- КОЛИ `timer(300)` → ТО `custom: «джерело відновлює енергію до максимуму»`.
- КОЛИ `custom: «контролер не прокачували»` → ТО `decay(controller)`; RCL 0 → `set_side(controller, neutral)`. КОЛИ `exec(claimController)` → ЯКЩО `body_count(creep, CLAIM, >=, 1)` and GCL дозволяє → ТО `set_side(controller, player)`.
- КОЛИ `counter(energy_spent_upgrade)` росте → ТО `counter(GCL, +)` → більше CPU (з CPU Unlock: +10 за рівень до 300) і кімнат; GCL не втрачається.
- КОЛИ `counter(RCL, ==, n)` → ТО `unlock(structures[n])` (RCL 2: 5 розширень, стіни, рампарти; 3: вежа; 4: сховище; 5: лінки; 6: термінал, лаби; 7: 2-й спавн; 8: 3 спавни, 6 веж, observer, nuker).
- КОЛИ `custom: «перший спавн у кімнаті»` або активація → ТО `set_state(room, safe_mode, 20000)`: чужі не можуть шкодити; одна кімната на шард.
- КОЛИ `enter(hostile, rampart)` → ТО `block`; свої — проходять. Дороги й рампарти щотік `decay` → потрібен ремонт.
- Перемоги як такої нема (пісочниця): мета — GCL, кімнати, ресурси, місце в рейтингу. Arena: матч 1v1 з умовою перемоги сценарію (?).

## Керування і ввід
- Ввід — **лише код**: JS-модулі (`require`), або мови через WebAssembly (C/C++, Rust, Go, C#…), TypeScript. Внутрішній редактор або зовнішній IDE з синхронізацією.
- Консоль: виконати вираз над живим світом (`Game.spawns['Spawn1'].spawnCreep(...)`), вивід `console.log` щотіку.
- Ручне: розставити будмайданчики й прапорці мишею на карті кімнати, активувати safe mode; рух кріпів — лише через код.
- Приватний сервер: `npx screeps init/start`, CLI-консоль адміна (`bots.spawn`, `map.generateRoom`), моди Node.js.

## Вікна, меню, HUD
- `game-screen`: вид кімнати 50×50 (рельєф, споруди, кріпи з іменами й `creep.say`), панель вибраного обʼєкта (тіло, HP, втома, вантаж), `room-visual` (лінії/тексти, що малює код).
- `code-editor` — модулі, гілки коду; `output-console` — лог і ввід виразів.
- `world-map` — карта кімнат шарду з власниками, рівнями, безпечним режимом.
- HUD: `cpu-meter` (використано/ліміт/bucket), `turn-counter` (Game.time), енергія кімнати, GCL/RCL-прогрес.
- `leaderboard` — рейтинги за GCL/потужністю; `profile-window` гравця.
- `mode-select`: Simulation (тренування, тутор) · World (шарди) · Arena (окрема гра) (?).
- Переходи: вхід → вибір шарду і стартової кімнати (respawn) → кімната; карта світу ↔ кімната; редактор/консоль — панелі того ж екрана.

## Фічі поза полем
- `persistent-world`: код працює 24/7; `memory-persistence` (Memory як JSON); `respawn` усієї колонії при поразці.
- `simulation-room`: тренування й туторіал без ліміту CPU і офлайн-виконання.
- `private-server` + `mod-support` (моди, Steam Workshop) + `custom-rules` (змінити правила сервера).
- `leaderboard-online`, сезонні сервери (?), Arena — рейтингові сезони 1v1.
- Монетизація як механіка: CPU Unlock / підписка збільшує ліміт CPU (?).

## Варіації й родичі
- Screeps Arena — матчі 1v1 з асинхронним PvP і сезонами (окремий API, швидший темп).
- Родичі: Battlecode (автономні боти з лімітом байткоду), Halite, CodinGame-арени (див. `bot-arenas.md`), Colobot, Elevator Saga, The Farmer Was Replaced (дрони + тік-вартість).
- Осі варіацій: **світ** (персистентний MMO / матч / офлайн-пісочниця); **бюджет** (CPU мс / байткод / час на хід); **як вирішуються конфлікти** (одночасні наміри + пріоритети / почергово); **тіло юніта** (фіксовані типи / конструктор з частин).

## Цікавинки для курсу
- Двофазний тік «заморожений стан → наміри всіх → одночасне застосування» з правилами конфліктів — 🥇.
- Кріп як список частин: ціна, швидкість через втому, шкода по частинах у порядку тіла — 🥈.
- Втома й ціни рельєфу + пошук шляху з матрицею вартостей (рівнина/болото/дорога) — 🥇 (Дейкстра/A* з вагами).
- Бюджет CPU з «відром» — 🥈 (вимір часу виконання коду гравця, обрив, накопичення).
- Рівень контролера відкриває нові споруди + таймер деградації — 🥉.
- Світ з кімнат 50×50 як граф з виходами на краях — 🥉.
- Код гравця як агент, що працює без нього (тест-матч двох студентських ботів) — 🥇.

## Мапа на каталог
- Є: `impassable-cells` (стіни) · `floor-types` (рівнина/болото/дорога) · `chase-bfs` (`moveTo`, PathFinder) · `hp-damage` (по частинах) · `round-currency` (енергія) · `spawn-points` (спавни) · `timed-despawn` (1500 тіків) · `projectile-shot`/`melee-vs-ranged` (ATTACK vs RANGED_ATTACK) · `minimap-radar` (карта світу) · `leaderboard` · `save-progress` · `game-screen` · `state-as-data` (Memory).
- **Нема** → пропозиції карток:
  - `+tick-script-loop` «Код гравця щотік над замороженим станом» · code/architecture · 🥈.
  - `+cpu-budget-bucket` «Ліміт часу виконання з накопиченням» · game-logic · 🥈.
  - `+body-parts-composition` «Юніт зібраний з частин з цінами» · entities/state · 🥈.
  - `+fatigue-movement` «Втома від рельєфу й ваги» · entities/move · 🥉.
  - `+intent-resolution-simultaneous` «Наміри всіх застосовуються разом» · game-logic · 🥇 (сусід `+simultaneous-hidden-orders` з RoboRally).
  - `+action-pipelines` «Несумісні дії в одному тіку» · game-logic · 🥉.
  - `+controller-level-unlocks` «Рівень бази відкриває споруди» · game-logic/economy · 🥉.
  - `+persistent-world-offline` «Світ живе без гравця» · game-logic · 👑 (сервер).
  - `+room-graph-world` «Світ з кімнат-сіток» · levels · 🥉.
  - `+structure-decay-repair` «Споруди гниють, треба ремонт» · entities/state · 📎.
  - `+source-regen` «Джерело відновлюється за таймером» · entities/spawn · 🌱.
  - `+safe-mode` «Тимчасова невразливість бази» · game-logic · 🌱.
  - `+memory-persistence` «Памʼять агента між тіками» · code/architecture · 📎.
  - `+cost-matrix-pathfinding` «Пошук шляху з вагами клітин» · entities/move · 🥇 (дитина `chase-bfs`).
  - `+private-server-mods` · `+simulation-room` · `+command-program` · `+code-editor-window` · `+user-procedures` · `+swarm-separate-programs` (з інших файлів сімʼї).

## Пропозиції до словників
- `+trigger:exec(cmd)` (сімʼя) · `+trigger:phase_start` 🔥 — фаза застосування намірів · `+trigger:tick` ⏳.
- `+cond:has` ⏳, `+cond:in_range` ⏳ — головні умови дій; нові `+cond:body_count(a, part, op, n)`, `+cond:fatigue(a, op, n)`.
- `+effect:intent(a, action)` — наказ, що застосується в кінці тіку (не миттєвий `move`); `+effect:harvest` · `+effect:transfer` · `+effect:build` · `+effect:repair` · `+effect:upgrade` · `+effect:claim` · `+effect:decay` — економічні дієслова агентів.
- `+role:spawner` ⏳ (спавн) · `+role:resource` 🔥 (джерело) · `+role:zone` 🔥 (контролер = власник кімнати) · `+role:tower` 🔥.
- `+window:code-editor` 🔥 · `+window:world-map` (= ⏳ `map-window`) · `+window:output-console` (з The Farmer).
- `+ui:cpu-meter` — використання CPU/bucket; `+ui:room-visual` — малювання поверх поля з коду гравця.
- `+feature:persistent-world` · `+feature:simulation-room` · `+feature:private-server`.
- `+axis:actors` — `swarm` з різними тілами; `control: programmed`.

## Джерела
- ⭐ [Screeps docs: Introduction](https://docs.screeps.com/introduction.html) — світ, кімнати 50×50, рельєф і ціни руху, спавни, розширення, джерела, рампарти, safe mode.
- [Steam: Screeps World](https://store.steampowered.com/app/464350/Screeps_World/) — дата релізу 16.11.2016, тік 2–5 с, мови через WebAssembly, приватні сервери.
- [Creeps](https://docs.screeps.com/creeps.html) — частини тіла, втома, 1500 тіків, 50 частин, шкода по порядку.
- [Control](https://docs.screeps.com/control.html) — GCL, RCL 1–8, зниження, claim/reserve.
- [Game loop](https://docs.screeps.com/game-loop.html) · [CPU limit](https://docs.screeps.com/cpu-limit.html) · [Simultaneous actions](https://docs.screeps.com/simultaneous-actions.html) · [Defense](https://docs.screeps.com/defense.html).
- [API](https://docs.screeps.com/api/) — BODYPART_COST, SOURCE_ENERGY_CAPACITY, CREEP_LIFE_TIME, PathFinder.search (plainCost 1, swampCost 5).
- [GitHub: screeps/screeps](https://github.com/screeps/screeps) — сервер, моди, CLI.
- [store.screeps.com](https://store.screeps.com/) — World vs Arena.
- YouTube: пошук «screeps beginner tutorial».

## Непевне
- (?) Перший запуск (альфа/бета ~2014) — у шапці рік Steam-релізу 2016; ранню дату не перевірив.
- (?) Темп видобутку (2 енергії за WORK/тік), час спавну (3 тіки на частину), спад сили вежі (600 → 150) — з памʼяті, у прочитаних частинах API не знайшов.
- (?) Поведінка NPC-загарбників і Source Keeper-ів — не читав.
- (?) Умова перемоги в Screeps Arena і наявність сезонних серверів World — не перевіряв.
- (?) Зміст режиму Simulation (туторіал) — лише згадка в доках про відсутність ліміту CPU.
