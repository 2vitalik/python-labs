---
title: Motos
slug: motos
aka: [モトス, Motors Spanner, Pac-Motos]
family: maze-arcade
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: full
  random: none
  goal: state
year: 1985
platforms: [arcade, C64, Amstrad CPC, ZX Spectrum, X68000, PlayStation, PSP, Xbox 360, PS4, Switch]
links:
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/モトス", best: true, note: "найповніше: маса й деталі, панелі, тор, усі вороги з очками, Navicon, метеори, життя, порти"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Motos_(video_game)", note: "коротко: бампер, power/jump parts, 62 раунди, порти"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Motos+Namco+arcade", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [move-8dir, environment-death, player-death, destroy-all-enemies, wrap-edges, item-pickup, inventory, inventory-limit, pattern-automaton, chase-player, speed-per-type, spawner-entity, hp-damage, event-points, extra-life-threshold, sequential-levels, difficulty-levels, hot-seat, +ring-out, +mass-knockback, +crumbling-floor, +jump-over-gap, +part-loadout, +falling-hazard]
proposes: ["+effect:knockback", "+effect:crack", "+trigger:land", "+card:ring-out", "+card:mass-knockback", "+card:crumbling-floor", "+card:part-loadout", "+window:loadout-select", "+feature:operator-settings"]
author: opus
date: 2026-11-09
---

# Motos — машинка-бампер виштовхує жуків за край діркуватої бази; маса вирішує, хто полетить

## Суть
Гравець керує бронекатером-бампером Motos на «сонячній базі» з панелей посеред порожнечі. Атакувати нічим: треба врізатися в Space Bee так, щоб її відкинуло за край або в дірку. Вороги роблять з Motos те саме, тож кожне зіткнення — дуель мас (японці порівнюють з «охадзікі», клацанням фішок). Деталі сили роблять Motos важчим, деталі стрибка дають крила для стрибків над дірками; обидва види обираються перед етапом із накопиченого запасу.

## Поле і час
- 62 етапи, кожен — фіксований екран бази з панелей; навколо й у дірках — порожнеча. Поле зʼєднане з усіх чотирьох боків: стрибок через край екрана переносить на протилежний («warp jump»), ворогів теж можна перекинути через шов.
- Панелі руйнуються: тріснута панель провалюється після короткої затримки, метеор пробиває панель, тож поле з часом меншає.
- Real-time; рух не клітинний, а фізичний: обидва учасники зіткнення відскакують, сила відкидання залежить від маси.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Motos (Motors Spanner) | player | маса = база + power parts (до 7); 3 життя | рух 8 напрямків; таран; стрибок, якщо є jump part |
| Панель | terrain | ціла / тріснута | опора; тріснута провалюється за мить |
| Порожнеча (край, дірка) | hazard | — | хто впав — зник (для Motos — промах) |
| Power part | pickup | у запасі | +маса на етап, коли встановлена |
| Jump part | pickup | у запасі | дає стрибок на етап (Motos з крилами) |
| Pupa (300) | enemy | червона / синя / чорна | кулька; частина виходить з Navicon |
| Polar (800) | enemy | — | часто ядро формації |
| Spiral (1000) | enemy | — | павук, рух Z-зигзагом |
| Fire Bug (1300) | enemy | швидкий | великі червоні очі |
| Fire Bee (1500) | enemy | швидкий | лінійніший; іноді різко зупиняється |
| Titorian (2000) | enemy | швидкий | цілиться в гравця |
| Lady Bug (2500) | enemy | — | таранить, після удару міняє кут |
| Beetle (3000) | enemy | — | таранить, обертаючись |
| Mega (3500) / Giga (5000) | enemy | великі; Giga важча | — |
| Beacon | object | нерухомий | скинутий будь-ким — 1000 очок |
| Navicon | spawner | 6 руйнівних на всю гру | випускає Pupa в одному з 4 фіксованих напрямків |
| Метеор | hazard | частішає з часом | падає туди, де Motos; гравця не ранить, але пробиває панель |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ТО `move(motos, dir)` — 8 напрямків.
- КОЛИ `contact(motos, bee)` → ТО `custom: «обидва відлітають; легший відлітає далі»` — `+effect:knockback`.
- КОЛИ `contact(bee, bee)` → ТО `custom: «так само відкидання за масами»` (?).
- КОЛИ `custom: «сутність опинилась над порожнечею»` → ТО для bee: `disappear(bee)`, `score(value)`; для Motos: `lives(-1)`, `restart`.
- КОЛИ `custom: «beacon скинуто в порожнечу»` → ТО `score(1000)` — хоч гравцем, хоч ворогом.
- КОЛИ `edge(a)` → ТО `wrap(a)`.
- КОЛИ `contact(motos, part)` → ТО `pickup` → `counter(power_parts|jump_parts, +1)` у запас; відразу не діє.
- КОЛИ `contact(bee, part)` → ТО `push(part)`; скинута деталь зникає назавжди, навіть після промаху.
- КОЛИ `level_start` → ТО `choose(power_parts 0..7, jump_part)` → `custom: «маса Motos = база + встановлені power parts»`.
- КОЛИ `input(jump)` → ЯКЩО `has(motos, jump_part)` → ТО `custom: «стрибок над діркою; посадку можна зсунути на ½ спрайта»`.
- КОЛИ `custom: «Motos приземлився»` → ТО `set_cell(panel, cracked)`; КОЛИ `timer(short)` → ЯКЩО `state(panel, cracked)` → ТО `set_cell(panel, void)` — і все, що стоїть на ній, падає.
- КОЛИ `timer(n)` → ТО `spawn(meteor)` над Motos; КОЛИ `contact(meteor, panel)` → ТО `set_cell(panel, void)`.
- КОЛИ `timer(n)` → ТО `spawn(pupa)` з Navicon в один із 4 напрямків.
- КОЛИ `contact(motos, navicon)` → ЯКЩО `has(motos, power_parts ≥ 5)` → ТО `counter(navicon_hits, +1)`; КОЛИ `counter(navicon_hits, ==, 15)` → ТО `disappear(navicon)`, `score(50000)`.
- КОЛИ `all_gone(bee)` → ТО `next_level`, `take(motos, equipped_parts)` — встановлені деталі витрачаються на чистому проходженні.
- КОЛИ `died(motos)` → ТО `restart` етапу: скинуті вороги не повертаються, Pupa з Navicon відновлюються, встановлені деталі не витрачаються; промах після зачистки до зміни екрана — все одно промах.
- КОЛИ `counter(score, >=, 10000|30000|+50000)` → ТО `lives(+1)`.
- КОЛИ `level_end` → ЯКЩО `level(==, 62)` → ТО `score(100000 × lives)`.
- КОЛИ `level_start` → ЯКЩО `mode(hard)` → ТО `custom: «маса Space Bee більша»`.
- Перемога етапу: усі Space Bee за межами бази. · Поразка: Motos упав, життя скінчились. · Рахунок: вартість ворога (300–5000), beacon 1000, Navicon 50 000, бонус за життя після 62-го.

## Керування і ввід
- 8-напрямний важіль — рух; одна кнопка — стрибок (коли є jump part) і підтвердження на екрані вибору деталей.
- 1–2 гравці по черзі.

## Вікна, меню, HUD
- `game-screen`: база з панелей, вороги, деталі; HUD — `score`, `lives` (?).
- `custom-window` → `+window:loadout-select`: перед етапом гравець обирає, скільки power parts і чи брати jump part із запасу; кнопка підтверджує.
- Переходи: loadout-select → game-screen → (зачистка) loadout-select наступного етапу; промах → рестарт етапу.

## Фічі поза полем
- `levels-sequential`: 62 фіксовані етапи.
- Запас деталей між етапами — 100 power і jump parts на всю гру; мета-економіка «витратити зараз чи зберегти».
- `difficulty-presets`: Normal / Hard; стартові життя й пороги бонусних життів — налаштування власника автомата (`+feature:operator-settings`).
- `hotseat`: два гравці по черзі.

## Варіації й родичі
- Порти 1987 (C64, CPC, Spectrum — Binary Design / Mastertronic), X68000 (1989) з аранжованою музикою; збірки Namco Museum, Arcade Archives (2022).
- Pac-Motos (Wii, «Minna de Asobou! Namco Carnival»; також у PAC-MAN MUSEUM+) — персонажі Pac-Man, 5 світів по 7 етапів.
- Родичі: [`pengo`](../push-slide/pengo.md) (ворогів розчавлюють крижиною), [`auro`](../tactics/auro.md) (монстрів штовхають у воду, покроково), [`pac-man-battle-royale`](pac-man-battle-royale.md) (суперники в одній арені).
- Осі варіацій «як позбутися ворога без зброї»: розчавити ковзним блоком (Pengo) / виштовхнути в воду (Auro) / виштовхнути за край (Motos). Вісь «опора»: поле незмінне / панелі тріскаються після приземлення (Motos) / платформи зникають за таймером.

## Цікавинки для курсу
- Відкидання за масами (обидва відлітають, легший — далі) замість HP — 🥈 (фізика зіткнень + сітка панелей під нею).
- Тріснута панель після приземлення провалюється з затримкою, забираючи все, що на ній — 📎.
- Тор-поле з дірками: перекинути ворога через шов екрана — 🌱 (картка `wrap-edges` є).
- Запас деталей між етапами + вибір завантаження перед етапом — 🥉 (економіка «зараз чи потім»).
- Зоопарк ворогів з одного параметра поведінки (зигзаг, прицільний, таран із зміною кута, обертання) — 🥉.
- Navicon: спавнер, що руйнується лише 15 ударами за умови маси ≥ 5 деталей — 📎.

## Мапа на каталог
- Є: `move-8dir` ↔ важіль; `environment-death` + `player-death` ↔ падіння в порожнечу; `destroy-all-enemies` ↔ зачистка бази; `wrap-edges` ↔ warp jump; `item-pickup` + `inventory` + `inventory-limit` ↔ деталі, до 7 power parts; `pattern-automaton` ↔ Spiral, Lady Bug, Beetle; `chase-player` ↔ Titorian; `speed-per-type` ↔ швидкі Fire Bug/Bee; `spawner-entity` ↔ Navicon; `hp-damage` ↔ 15 ударів по Navicon; `event-points` ↔ таблиця вартостей; `extra-life-threshold` ↔ 10k/30k/кожні 50k; `sequential-levels` ↔ 62 етапи; `difficulty-levels` ↔ Normal/Hard; `hot-seat` ↔ 2 гравці по черзі.
- **Нема** → пропозиції карток:
  - `+ring-out` «Виштовхни за край» · game-logic/win · 🥉 — ворог гине, лише покинувши поле.
  - `+mass-knockback` «Відкидання за масами» · entities/combat · 🥈 · слот {mass} — обидва відлітають.
  - `+crumbling-floor` (уже пропонував Manic Miner) — тут: тріщина після приземлення, провал за затримкою.
  - `+jump-over-gap` «Стрибок над діркою» · entities/move · 📎 — доступний лише з деталлю.
  - `+part-loadout` «Завантаження деталей перед етапом» · game-logic/economy · 🥉 · слоти {max: 7}.
  - `+falling-hazard` «Метеор падає на гравця й пробиває підлогу» · entities/spawn · 📎.

## Пропозиції до словників
- `+effect:knockback` — відкидання при зіткненні з урахуванням маси (уже ×11 у корпусі).
- `+effect:crack` — клітина стає тріснутою (тут — від приземлення); уже пропонували Dig Dug II і Drop7.
- `+trigger:land` — сутність приземлилась після стрибка.
- `+card:ring-out`, `+card:mass-knockback`, `+card:crumbling-floor`, `+card:part-loadout` — див. вище.
- `+window:loadout-select` — вибір завантаження перед етапом (уже ×10).
- `+feature:operator-settings` — налаштування власника автомата (життя, пороги, складність).

## Джерела
- ⭐ [Wikipedia JA: モトス](https://ja.wikipedia.org/wiki/モトス) — керування (важіль + кнопка), маса й деталі (до 7, вибір перед етапом, витрата), тріснуті панелі, тор, 10 ворогів з очками й поведінкою, beacon, Navicon, метеори, життя й бонуси, Pac-Motos, порти.
- [Wikipedia EN: Motos](https://en.wikipedia.org/wiki/Motos_(video_game)) — бампер, power/jump parts, 62 раунди, порти 1987.
- YouTube: пошук «Motos Namco arcade».

## Непевне
- (?) Панелі як квадратна сітка — джерела кажуть лише «панелі»; рух акторів — вільний, не по клітинах, тому `field: square` описує лише шар панелей.
- (?) Де зʼявляються деталі на полі (фіксовані місця чи з ворогів) і скільки jump parts треба для стрибка.
- (?) Чи вороги відкидають одне одного так само, як Motos; точна формула маси й відкидання.
- (?) Чи є ліміт часу етапу, бонус-етапи, екран введення ініціалів — джерела не згадують.
- (?) Чи є в поведінці ворогів випадковість (`random: none` — за відсутністю згадок).
