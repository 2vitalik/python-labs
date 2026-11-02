---
title: Creeper World
slug: creeper-world
family: tower-lanes
also: [build-sim, dig-gravity]
klass: cursor
axes:
  field: layers
  time: realtime
  opponent: none
  info: full
  random: none
  goal: state
year: 2009
platforms: [PC (Windows, macOS, Linux), web (Flash), Steam]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Creeper_World", best: true, note: "уся серія: рідина-ворог, висоти, колектори й мережа, бластери/мортири, сиквели"}
  - {kind: official, url: "https://knucklecracker.com/", note: "студія Knuckle Cracker: сторінки ігор, мапи, рекорди"}
  - {kind: fandom, url: "https://knucklecracker.com/wiki/doku.php?id=cw1:creeper_world_1", note: "офіційна вікі CW1 (юніти)"}
  - {kind: fandom, url: "https://knucklecracker.com/wiki/doku.php?id=cw3:creeper_world_3", note: "офіційна вікі CW3 (юніти, CRPL)"}
  - {kind: steam, url: "https://store.steampowered.com/app/422910/Creeper_World_Anniversary_Edition/", note: "CW1 Anniversary Edition (2016)"}
  - {kind: steam, url: "https://store.steampowered.com/app/280220/Creeper_World_3_Arc_Eternal/", note: "CW3: тераформінг, редактор, CRPL"}
  - {kind: steam, url: "https://store.steampowered.com/app/848480/Creeper_World_4/", note: "CW4 (3D)"}
  - {kind: steam, url: "https://store.steampowered.com/app/2257010/Creeper_World_IXE/", note: "IXE: falling sand"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=creeper+world+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [spawn-schedule, spawn-points, impassable-cells, round-currency, projectile-shot, shoot-cooldown, blast-wave, hp-damage, game-pause, player-camera, minimap-radar, level-select, level-unlock, sequential-levels, in-game-editor, score-records, time-bonus, game-loop, +tower-placement, +tower-range, +mass-equalize-flow, +height-levels, +power-graph, +fluid-network, +coverage-area, +packet-delivery, +build-by-packets, +ammo-feed, +line-of-sight-height, +relocate-building, +annihilate-opposites, +terraform-cell, +connect-goals-win]
proposes: ["+trigger:tick", "+trigger:flooded", "+cond:connected", "+cond:line_of_sight", "+cond:higher", "+effect:flow", "+effect:drain_cell", "+effect:send_packet", "+effect:relocate", "+role:tower", "+role:source", "+role:conduit", "+role:fluid", "+ui:energy-graph", "+ui:packet-flow", "+ui:depth-shading", "+window:map-window", "+feature:mode-daily", "+feature:level-editor", "+axis:field=heightmap"]
author: opus
date: 2026-11-02
---

# Creeper World — ворог-рідина на карті висот: стримуй потоп вежами й мережею енергії

## Суть
Ворог — не юніти, а **рідина Creeper**: її викидають емітери, вона розтікається клітинами карти висот, заповнює низини й піднімається вгору лише набравши об'єм. Гравець будує мережу з колекторів і релеїв, по якій від бази (Odin City) летять **пакети енергії** — ними будуються споруди й заряджаються бластери, мортири, дрони. Зброя «вичерпує» рідину з клітин, відштовхуючи фронт; мета — зʼєднати мережею тотеми (CW1) або знищити емітери (CW2–3). Незвичне: поразка — не «ворог дійшов до бази», а повільне затоплення, тож гра — про гідродинаміку й логістику.

## Поле і час
- Поле — квадратна сітка клітин з **висотою** (рівні 1–10 (?)) — `field: layers` як карта висот. Кожна клітина має висоту землі `h` і глибину рідини `d`.
- CW1/CW3/CW4 — вид згори (CW4 у 3D), CW2 — поперечний розріз (бічний вид, підземелля).
- Real-time з паузою; симуляція рідини тікає незалежно від вводу; є прискорення часу (?).
- Камера: CW1 — мапа на екран; CW3 — великі мапи з прокруткою і зумом. Туману нема: рідину видно, її глибину показує насиченість синього.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Creeper | fluid (+role) | глибина `d` у клітині | розтікається до сусідів з нижчим `h+d`; шкодить спорудам, які заливає |
| Емітер | spawner | обсяг, період | кожні N тіків додає `d` у свою клітину |
| Спорова вежа | spawner | період | запускає спори, що летять і при падінні дають рідину (?) |
| Odin City (CW1) / Command Node (CW3) | source (+role) | енергія/с, запас | генерує пакети; будує; може перелітати (?) |
| Колектор | source | радіус збору | збирає енергію з клітин навколо; перекриття радіусів ділить землю; несполучений — неактивний; також вузол мережі |
| Релей | conduit (+role) | дальність лінку | продовжує мережу на більшу відстань |
| Реактор | source | +енергія | додаткова генерація (CW1: фіксований вихід) |
| Сховище (storage) | container | +місткість | збільшує запас енергії |
| Speed node | conduit | — | пришвидшує пакети (?) |
| Бластер (CW3: Pulse Cannon) | tower (+role) | радіус, амуніція | прямий постріл по клітині з рідиною, потрібна пряма видимість; не б'є вище себе |
| Мортира | tower | радіус, сплеск | навісний снаряд у найглибшу рідину, б'є і по вищих клітинах |
| Дрони / бомбардувальник / страфер | tower | база + дрони | повітряні удари по рідині (?) |
| SAM / Beam | tower | — | збиває спори в повітрі |
| Sprayer (CW3) | tower | — | розпилює антикрипер |
| Антикрипер | fluid | від'ємна глибина | тече як рідина; при зустрічі з Creeper — взаємне знищення |
| Нуліфаєр (CW3) | tower | — | знищує емітер у радіусі (ціль місії) |
| TERP (CW3) | tower | — | змінює висоту клітин (тераформінг) |
| Тотем (CW1) | static | — | цільова точка: приєднати мережею |
| Технологічний артефакт | pickup | — | відкриває апгрейд/тип юніта (?) |
| Пакет енергії | projectile | 1 одиниця | летить мережею від джерела до споживача; у CW2 летить напряму й гине в рідині |
| Рельєф (висота) | terrain | `h` | рідина спершу заповнює низини; вища клітина — природна стіна |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `timer(every)` → емітер `custom: «effect add_depth(cell, amount)»`.
- КОЛИ `tick` → для кожної клітини з `d > 0` `custom: «effect flow: передати частку різниці (h+d) − (h'+d') кожному нижчому сусіду; рідина вирівнюється»` (`+mass-equalize-flow`).
- КОЛИ `tick` → ЯКЩО `custom: «cond higher: сусід вищий за поверхню рідини»` → ТО `block` (рідина не тече вгору, доки не набереться).
- КОЛИ `tick` → ЯКЩО `occupied(cell, structure)` and `custom: «d > 0»` → ТО `damage(structure, ∝d)`; `hp_zero` → `disappear_a` (CW1: заливання знищує).
- КОЛИ `input(place, unit, cell)` → ЯКЩО `free(cell)` and `custom: «нема рідини»` and `custom: «рівна ділянка під footprint»` → ТО `custom: «привид споруди»`; вона будується, коли отримає N пакетів.
- КОЛИ `tick` → джерело `custom: «effect send_packet: пакет іде найкоротшим шляхом мережі до споживача (будівництво → амуніція → решта)»`.
- КОЛИ `custom: «cond connected: споруда не з'єднана з джерелом»` → ТО `set_state(unit, inactive)`; колектор не збирає, зброя не заряджається.
- КОЛИ `tick` → колектор `counter(energy, +k×вільні_клітини_в_радіусі)`; клітини, вкриті рідиною чи іншим колектором, не рахуються (?).
- КОЛИ `counter(consumption, >, production)` → ТО `custom: «пакети ділять дефіцит: зброя перезаряджається повільніше»`.
- КОЛИ `in_range(blaster, creeper, r)` → ЯКЩО `line_of_sight` and `custom: «ціль не вища за бластер»` and `has(blaster, ammo)` → ТО `custom: «effect drain_cell: d -= n»`, `take(blaster, ammo)`.
- КОЛИ `in_range(mortar, creeper, r)` → ЯКЩО `has(mortar, ammo)` → ТО `custom: «ціль — найглибша клітина»`, `explode(area)` → `drain_cell` по області.
- КОЛИ `contact(anticreeper, creeper)` → ТО `custom: «effect annihilate: d1 і d2 взаємно гасяться»`.
- КОЛИ `input(relocate, unit, cell)` → ТО `custom: «effect relocate: споруда злітає й сідає деінде; поки летить — не працює»` (?).
- КОЛИ `custom: «TERP працює»` → ТО `set_cell(x, h±1)` до цільової висоти (CW3).
- КОЛИ `custom: «усі тотеми приєднані до мережі»` (CW1) або `all_gone(emitters)` (CW2–3, нуліфаєрами) → ТО `win`.
- КОЛИ `custom: «рідина залила базу (Odin City / усі command nodes)»` → ТО `lose`.
- Перемога: мережа до тотемів / знищені емітери · Поразка: база знищена рідиною · Рахунок: час проходження → очки й онлайн-рекорди.

## Керування і ввід
- Миша: вибір юніта з панелі (або гаряча клавіша) → ЛКМ по клітині ставить привид; лінії мережі показуються, поки ведеш курсором.
- Вибір споруди → переміщення (релокація) кліком у нову клітину (?); вимкнення/увімкнення зброї, щоб зберегти енергію (?).
- Пауза (пробіл (?)), прискорення; прокрутка і зум (CW3).
- Ціль зброї — автоматична (найближча/найглибша рідина), гравець лише розставляє.

## Вікна, меню, HUD
- `main-menu`: Story · Conquest/Special Ops (?) · Evermore/Prospector · Options · Credits.
- `map-window` (⏳): карта планет/систем кампанії; CW3 — сектор із сотнями світів (Prospector) і генератор DMD.
- `game-screen`: поле з глибиною рідини відтінками синього, лінії мережі між вузлами, летючі пакети (`+ui:packet-flow`); нижня панель будівництва з цінами в пакетах; `energy-bar` і графік виробництво/споживання (`+ui:energy-graph`); таймер місії.
- `+ui:range-circle` (як Fieldrunners) навколо зброї; індикатор амуніції біля кожної вежі.
- `pause-menu` — продовжити, рестарт, вихід; `end-screen` — час, очки, кнопка в рекорди.
- `leaderboard` — онлайн-рекорди часу по мапах.
- `editor-window` (CW3): редактор мап + скрипти CRPL.
- Переходи: main-menu → map-window → (брифінг) → game-screen → end-screen → map-window.

## Фічі поза полем
- `levels-sequential` + `world-map` у сюжеті; апгрейди з вузлів/артефактів у CW1 (3 на енергію, 3 на зброю).
- `mode-daily` — експансія Evermore: щоденні випадкові мапи; User Space — мапи спільноти; CW3 Prospector — генеровані світи з кодом-адресою (`seed-input` / `share-code`).
- `level-editor` + `user-levels-browser` + `level-sharing` (CW3: завантаження онлайн), `mod-support` через CRPL.
- `leaderboard-online` часу, `pause`, `speed-control` (?).

## Варіації й родичі
- CW2 Redemption (2011): бічний розріз, копання ґрунту (?), пакети летять напряму, ore → антикрипер, дрони й фантоми.
- CW3 Arc Eternal (2013): тераформінг, 3 command nodes, антикрипер, спори, редактор і CRPL; Abraxis (2014) — браузерний пролог.
- CW4 (2020): 3D-рельєф; IXE (2024): falling-sand фізика (дальній родич `the-powder-toy`); Particle Fleet: Emergence — та сама студія, рідина в космосі.
- Родичі: Oxygen Not Included (рідина як клітинний автомат), Dwarf Fortress (вода), Mindustry (мережа енергії), Tower Defense загалом.
- **Осі варіацій**: ворог — юніти / рідина / сипучий пісок (IXE) · вид — згори / розріз · енергія — мережа з пакетами / по повітрю / миттєва · перемога — зʼєднати / знищити джерела / вижити.

## Цікавинки для курсу
- Рідина на карті висот: щотіку вирівнювати `h+d` між сусідами (подвійний буфер, збереження маси) — 🥇 (клітинний автомат з плаваючими значеннями й стабільністю).
- Мережа енергії як граф: компоненти зʼєднаності, активні/неактивні вузли — 🥈.
- Пакети як сутності: найкоротший шлях у графі мережі + черга пріоритетів споживачів — 🥇.
- Вежа з обмеженням «не стріляє вгору» і прямою видимістю по висотах — 🥉.
- Антикрипер: дві рідини, що взаємно гасяться — 🥉 (той самий двіжок, знак глибини).
- Колектор із радіусом збору, перекриття ділить урожай — 📎 (`coverage-area`).

## Мапа на каталог
- Є: `spawn-schedule` + `spawn-points` ↔ емітери · `impassable-cells` ↔ висока стіна для рідини · `round-currency` ↔ енергія · `projectile-shot` + `shoot-cooldown` ↔ бластер · `blast-wave` ↔ мортира · `hp-damage` ↔ споруди під рідиною · `game-pause` · `player-camera` + `minimap-radar` (CW3) · `level-select` / `level-unlock` / `sequential-levels` · `in-game-editor` (CW3) · `score-records` + `time-bonus` · `game-loop`.
- **Нема** → пропозиції карток:
  - `+tower-placement`, `+tower-range` (спільні з Fieldrunners) — тут ще й «не вище себе».
  - `+mass-equalize-flow` (є в корпусі, ONI) — рідина-ворог; `+height-levels` (є) — висота клітин.
  - `+power-graph` (є), `+fluid-network` (є), `+coverage-area` (є) — мережа й радіус збору.
  - `+packet-delivery` «Ресурс летить мережею пакетами до споживача» · entities/move · 🥇.
  - `+build-by-packets` «Споруда будується, отримавши N одиниць» · entities/spawn · 📎.
  - `+ammo-feed` (є в корпусі, Mindustry) — вежа стріляє, лише отримавши амуніцію.
  - `+line-of-sight-height` «Пряма видимість з урахуванням висот» · entities/combat · 🥉.
  - `+relocate-building` «Перенести споруду (недоступна в дорозі)» · entities/move · 📎.
  - `+annihilate-opposites` «Дві рідини гасять одна одну» · entities/interact · 🥉.
  - `+terraform-cell` «Змінити висоту клітини» · entities/interact · 📎.
  - `+connect-goals-win` «Перемога — зʼєднати цілі мережею» · game-logic/win · 🥉.

## Пропозиції до словників
- `+trigger:tick` — підтвердження (симуляція рідини щотіку); `+trigger:flooded` — клітину зі спорудою залило.
- `+cond:connected` — вузол у компоненті з джерелом (є 🔥 у корпусі); `+cond:line_of_sight` — уже ⏳; `+cond:higher` — клітина вища за іншу/поверхню рідини.
- `+effect:flow` — передати частку маси сусіду; `+effect:drain_cell` — зменшити глибину рідини; `+effect:send_packet` — запустити одиницю ресурсу графом; `+effect:relocate` — перелетіти споруді.
- `+role:tower` (підтвердження), `+role:source` / `+role:conduit` (є 🔥), `+role:fluid` — ворог як поле значень на клітинах, не сутність.
- `+ui:energy-graph` — графік виробництво/споживання; `+ui:packet-flow` — видимі пакети на лініях; `+ui:depth-shading` — глибина відтінком.
- `+window:map-window` — карта кампанії/світів.
- `+feature:mode-daily` — Evermore; `+feature:level-editor` — CW3.
- `+axis:field=heightmap` — сітка з висотою й рідиною поверх (відрізняти від `layers` Mahjong).

## Джерела
- ⭐ [Wikipedia: Creeper World](https://en.wikipedia.org/wiki/Creeper_World) — рідина збирається, перш ніж піднятись; бластери потребують прямої видимості й не б'ють вище; мортири б'ють у густу рідину й вище; колектори мусять мати місце й з'єднання; CW2–IXE.
- [Knuckle Cracker](https://knucklecracker.com/) — сторінки всіх частин, лінки на вікі, мапи й рекорди.
- [KC Wiki: CW1](https://knucklecracker.com/wiki/doku.php?id=cw1:creeper_world_1) · [KC Wiki: CW3](https://knucklecracker.com/wiki/doku.php?id=cw3:creeper_world_3) — повні списки юнітів (лінки з офіційного сайту; сторінки повернули 403).
- [Steam: CW Anniversary](https://store.steampowered.com/app/422910/Creeper_World_Anniversary_Edition/) · [CW3](https://store.steampowered.com/app/280220/Creeper_World_3_Arc_Eternal/) — опис: рідина на тераформованому рельєфі, редактор, CRPL, Prospector, DMD.
- [Steam: CW4](https://store.steampowered.com/app/848480/Creeper_World_4/) · [IXE](https://store.steampowered.com/app/2257010/Creeper_World_IXE/).
- YouTube: пошук «creeper world gameplay».

## Непевне
- (?) Точна формула течії (яку частку різниці передає клітина за тік) і діапазон висот — з памʼяті; офіційну вікі не відкрив.
- (?) Спорові вежі, дрони, SAM, speed node в CW1 — частину могли додати лише в CW3.
- (?) Пріоритет пакетів (будівництво vs амуніція) і чи пакети в CW1 гинуть у рідині.
- (?) Релокація споруд і Odin City — з памʼяті.
- (?) Як саме перекриття колекторів ділить клітини.
