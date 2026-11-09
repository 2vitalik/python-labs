---
title: SimCity (1989) / Micropolis
slug: simcity-1989
aka: [SimCity Classic, Micropolis, Сімсіті]
family: build-sim
also: []
klass: cursor
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: none
year: 1989
platforms: [Amiga, Mac, DOS, C64, SNES, web (Micropolis), Linux (OLPC)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/SimCity_(1989_video_game)", best: true, note: "зони R/C/I, енергія, транспорт, податки, катастрофи, сценарії, версії, Micropolis GPL"}
  - {kind: other, url: "https://github.com/SimHacker/micropolis/blob/wiki/InsideTheSimulator.md", note: "«Inside the Simulator»: як рахуються населення, трафік, вартість землі, злочинність, забруднення, бюджет"}
  - {kind: other, url: "https://micropolisweb.com/doc/classMicropolis.html", note: "Doxygen рушія MicropolisCore: карти-поля симуляції"}
  - {kind: other, url: "https://github.com/SimHacker/micropolis", note: "відкриті сирці (GPL-3, січень 2008)"}
  - {kind: other, url: "https://github.com/SimHacker/MicropolisCore", note: "C++-рушій → WebAssembly"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=SimCity", note: "пошук; оригіналу 1989 у Steam не бачив"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=simcity+1989+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [cell-click, hover-highlight, multi-cell-size, connectivity-check, coverage-area, round-currency, chain-reaction, spawn-random-cell, cell-transform, level-select, difficulty-levels, game-pause, save-game, map-window, minimap-radar, editor-window, +zone-growth, +influence-map, +field-smoothing, +power-grid, +trip-generation, +tax-budget, +upkeep-decay, +disasters, +scenario-timed, +rci-demand, +fire-spread]
proposes: ["+effect:diffuse", "+cond:field", "+role:field-map", "+ui:rci-demand", "+ui:map-overlay", "+window:budget-window", "+window:evaluation-window", "+card:influence-map", "+card:zone-growth", "+feature:disaster-toggle"]
author: opus
date: 2026-11-09
---

# SimCity (1989) — розмічаєш зони R/C/I, тягнеш дороги й дроти, а місто росте саме за невидимими полями-картами вартості землі, злочинності й забруднення

## Суть
Гравець-мер не будує будинки — він **розмічає зони** (житлові R, комерційні C, промислові I), прокладає дороги, рейки й лінії електропередач, ставить станції поліції й пожежних. Симуляція сама вирішує, де зона росте чи занепадає, дивлячись на кілька **полів-карт** над сіткою: щільність населення, трафік, забруднення, вартість землі, злочинність, покриття станцій. Мети в звичайній грі нема — є бюджет і податки; сценарії дають обмежену в часі мету з перемогою/поразкою. Відкритий клон Micropolis (GPL) робить рушій доступним для вивчення.

## Поле і час
- Квадратна сітка клітин-тайлів; карта з землею, водою й лісом (генерується або малюється в редакторі ландшафту). Розмір у Micropolis — 120×100 (?).
- Шари: тайл (рельєф/будова) + **карти симуляції** (у сирцях: `populationDensityMap`, `trafficDensityMap`, `pollutionDensityMap`, `landValueMap`, `crimeRateMap`, `terrainDensityMap`, `rateOfGrowthMap`, `fireStationMap`, `policeStationMap`, `comRateMap` — відстань до центру міста), частина — нижчої роздільності (?).
- Real-time: симуляція йде циклами; у звичайній грі — ігрові місяці/роки; податки й утримання — раз на рік. Швидкості й пауза (?).
- Видимість повна; карти показуються як оверлеї.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Житлова зона (R) | zone | 3×3 (?) · щільність · живлено | росте/занепадає за попитом, трафіком, вартістю землі, злочинністю, забрудненням; дає мешканців-працівників |
| Комерційна зона (C) | zone | 3×3 (?) | внутрішній ринок: послуги для мешканців |
| Промислова зона (I) | zone | 3×3 (?) | зовнішній ринок: виробляє товари на продаж; головне джерело забруднення |
| Дорога | conduit | місткість, стан | несе поїздки; затор знижує місткість; без утримання псується |
| Залізниця (+ тунель) | conduit | — | транспорт; утримання $4 / $10 за тунель |
| Міст | conduit | — | дорога над водою; утримання $4 |
| ЛЕП | conduit | — | передає живлення; можна збити пожежею/торнадо/землетрусом |
| Електростанція (вугільна, атомна) | source | 4×4 (?) | живить зʼєднані зони |
| Поліцейська станція | source | фінансування $100/рік | зменшує злочинність у сфері впливу; радіус від фінансування |
| Пожежна станція | source | фінансування $100/рік | гасить пожежі, знижує шанс займання; радіус від фінансування |
| Парк · ліс · вода | terrain | — | підвищують вартість землі поруч |
| Стадіон · порт · аеропорт | static | великі (?) | розблокування росту за попитом (?) |
| Пожежа | hazard | — | поширюється сусідами, лишає руїни |
| Катастрофи: повінь, торнадо, землетрус, монстр, авіа-/корабельна аварія | hazard | — | руйнують тайли, спричиняють пожежі; торнадо/монстр можуть зіткнутися з потягом |
| Сіми (поїздки) | neutral | дальність поїздки | ходять R→C/I, C→R/I, I→R; невдалі поїздки виганяють з зони |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(zone_tool, cell)` → ЯКЩО `free(area)` and `has(city, funds >= cost)` → ТО `place(zone)`, `currency(-cost)`.
- КОЛИ `input(bulldoze, cell)` → ТО `set_cell(cell, dirt)`, `currency(-cost)`.
- КОЛИ `tick` → ЯКЩО `connected(zone, power_plant)` (через ЛЕП або інші зони) → ТО `set_state(zone, powered)`; інакше `clear_state(zone, powered)`.
- КОЛИ `tick` → ЯКЩО `not state(zone, powered)` → ТО `custom: «зона не розвивається»`.
- КОЛИ `tick` → ЯКЩО `state(zone, powered)` and `custom: «попит на тип зони > 0 і поїздка вдалася»` → ТО `transform(zone, denser_building)`, `counter(population, +n)`.
- КОЛИ `tick` → ЯКЩО `path_exists(zone, target_zone)` and `in_range(zone, target_zone, trip_max)` → ТО `custom: «трафік +1 на дорогах маршруту»`; інакше `custom: «невдала поїздка»`.
- КОЛИ `counter(failed_trips, >=, n)` → ТО `transform(zone, lower_density)` — сіми їдуть геть.
- КОЛИ `timer(scan)` → ТО `custom: «land_value = f(рельєф, доступність, відстань до центру, забруднення); вода/ліс/парк поруч ↑, довга поїздка R ↓»`.
- КОЛИ `timer(scan)` → ТО `custom: «crime = f(щільність ↑, вартість землі ↓) − покриття поліції»` — у сирцях crimeScan: «згладити карту станцій і порахувати злочинність».
- КОЛИ `timer(scan)` → ТО `custom: «pollution = промисловість + трафік (+ електростанції (?))»`; забруднення гальмує житловий ріст.
- КОЛИ `timer(scan)` → ТО `custom: «згладити карти сусідами (дифузія)»`.
- КОЛИ `tick` → ЯКЩО `in_range(cell, police_station, r_funding)` → ТО `custom: «злочинність тут знижено пропорційно фінансуванню»`.
- КОЛИ `rng(p)` → ЯКЩО `not in_range(cell, fire_station, r_funding)` → ТО `spawn_at(fire, cell)`; пожежні станції знижують шанс.
- КОЛИ `tick` → ЯКЩО `adjacent_count(cell, fire, >=, 1)` and `prob(p)` → ТО `spawn_at(fire, cell)`; догоріле — `set_cell(cell, rubble)`.
- КОЛИ `timer(year)` → ТО `currency(+tax)`, де tax = f(вартість землі, розвиток, ставка); ставка 0–4% — ріст, 10–20% — більше грошей зараз, відтік населення згодом.
- КОЛИ `timer(year)` → ТО `currency(-upkeep)`: $1 дорога · $4 міст · $4 рейка · $10 тунель; поліція й пожежні — $100 за станцію.
- КОЛИ `timer(year)` → ЯКЩО `not has(city, funds >= upkeep)` → ТО `custom: «дороги поступово псуються й стають непроїзними»`.
- КОЛИ `rng(p)` → ЯКЩО `custom: «катастрофи увімкнено»` → ТО `spawn_at(disaster, random)`; також з меню вручну.
- КОЛИ `counter(population, >=, 100000)` → ТО `message(metropolis)`; ≥ 500 000 — `message(megalopolis)` (SNES: статуя Маріо).
- КОЛИ `timer(scenario_end)` → ЯКЩО `custom: «мета сценарію виконана»` → ТО `win`; інакше `lose`.
- Звичайна гра: без перемоги/поразки; «рахунок» — населення, клас міста, оцінка мера (?).

## Керування і ввід
- Миша: вибір інструмента на палітрі (зони R/C/I, дорога, рейки, ЛЕП, парк, станції, електростанції, стадіон, порт, аеропорт, бульдозер, запит/query) → клік/протягування по сітці.
- Інструмент query — показати дані клітини (вартість землі, злочинність, забруднення…) (?).
- Меню: швидкість, катастрофи, бюджет, карти, оцінка.

## Вікна, меню, HUD
- `game-screen`: мапа міста; HUD — палітра інструментів (`tool-palette`), `coins` (кошти), дата, `rci-demand` (індикатор попиту R/C/I) (?), `message-log`/`toast` повідомлень («потрібна електрика», «високий рівень злочинності») (?).
- `map-window` з перемикачем оверлеїв (`map-overlay`): форма міста, електромережа, транспорт, щільність населення, темп росту, трафік, забруднення, злочинність, вартість землі, покриття поліції й пожежних (?).
- `budget-window`: ставка податку, фінансування поліції / пожежних / транспорту (три окремі статті).
- `evaluation-window`: оцінка мера, опитування, головні проблеми, клас міста (?).
- `custom-window` графіків (населення, злочинність, забруднення в часі) (?).
- `level-select` сценаріїв; `editor-window` — Terrain Editor (ліс, земля, вода); `save-slots` / завантаження міста.
- Переходи: старт → нове місто / сценарій / завантажити → game-screen; щороку → `budget-window`.

## Фічі поза полем
- `mode-sandbox` (вільна гра) і `mode-puzzle` — сценарії з обмеженим часом і перемогою/поразкою: реальні міста й вигадані катастрофи (Detroit 1972 — злочинність, SNES: Las Vegas — прибульці, Freeland — без води).
- `difficulty-presets` (стартові кошти (?)), `pause`, `speed-control` (?), `save-slots`.
- `level-editor` — редактор ландшафту.
- Перемикач катастроф (`+feature:disaster-toggle`); SNES — нагороди-будівлі (казино, парки, експо), позика $10 000.
- Відкриті сирці Micropolis (GPL-3, 2008) — рушій можна читати й змінювати; назву «SimCity» вживати заборонено.

## Варіації й родичі
- C64-версія без поліції/пожежних, стадіонів і залізниці; SNES — сезони й Bowser замість монстра.
- Наступники: SimCity 2000 (висоти, водогін, підземний шар), 3000, 4, 2013; клони — OpenTTD у корпусі (`openttd-rails`) як транспортна гілка, Cities: Skylines, Micropolis.
- Родичі в корпусі: `prison-architect-rooms` (зони-кімнати), `oxygen-not-included-cells` (поля-карти газів і температури), `game-of-life` (ріст за станом сусідства).
- Осі варіацій:
  - **хто будує:** гравець ставить будівлю / гравець розмічає зону, а росте сама;
  - **вплив:** радіус від станції · дифузія поля · поїздка по дорозі;
  - **живлення:** звʼязність графа (так/ні) / потужність з лімітом;
  - **мета:** пісочниця / сценарій на час / квота.

## Цікавинки для курсу
- Зона, що росте сама за набором умов (живлення, попит, вартість землі, злочинність) — 🥉.
- Поля-карти над сіткою з дифузією-згладжуванням (land value, crime, pollution) — 🥈 (кілька скалярних полів, що впливають одне на одне).
- Електромережа як звʼязність: BFS від станцій по ЛЕП і зонах — 📎.
- Генерація поїздок R→C/I з обмеженою дальністю й заторами — 🥇 (пошук шляху + місткість доріг).
- Покриття станцій з радіусом від фінансування — 📎.
- Поширення пожежі сусідами з шансом — 📎.
- Річний бюджет: податки від вартості землі, утримання доріг, деградація при нестачі — 🥉.
- Читання справжніх сирців Micropolis як дослідницьке завдання — 👑.

## Мапа на каталог
- Є: `cell-click` + `hover-highlight` · `multi-cell-size` (зони, станції) · `connectivity-check` (мережа) · `coverage-area` (поліція/пожежні) · `round-currency` (кошти міста) · `chain-reaction` (пожежа) · `spawn-random-cell` (катастрофи) · `cell-transform` (ріст/занепад, руїни) · `level-select` (сценарії) · `difficulty-levels` · `game-pause` · `save-game` · `map-window` + `minimap-radar` (?) · `editor-window` (Terrain Editor).
- **Нема** → пропозиції карток:
  - `+zone-growth` «Зона росте сама за умовами» · game-logic · 🥉 · слоти {conditions}.
  - `+influence-map` «Поле-карта над сіткою» · game-logic · 🥈 · слоти {sources, decay, resolution}.
  - `+field-smoothing` «Згладжування/дифузія поля сусідами» · game-logic · 📎.
  - `+power-grid` «Живлення через звʼязність мережі» · game-logic · 📎.
  - `+trip-generation` «Поїздки між зонами по дорогах» · game-logic · 🥇.
  - `+tax-budget` «Податки й статті бюджету» · game-logic/economy · 📎.
  - `+upkeep-decay` «Без утримання — деградація» · game-logic/economy · 🌱.
  - `+disasters` «Катастрофи на мапі» · entities/spawn · 📎.
  - `+scenario-timed` «Сценарій з метою на час» · game-logic · 🌱.
  - `+rci-demand` «Індикатор попиту R/C/I» · interface/hud · 🌱.
  - `+fire-spread` «Пожежа поширюється сусідами» · entities/spawn · 📎.

## Пропозиції до словників
- `+effect:diffuse` — згладити поле-карту сусідами (дифузія/blur); зараз `custom`.
- `+cond:field` — значення поля-карти в клітині порівняно з порогом (`field(land_value, >, n)`).
- `+role:field-map` — невидима скалярна карта над сіткою як «сутність» гри.
- `+ui:rci-demand` — стовпчики попиту за типами зон; `+ui:map-overlay` — перемикач оверлеїв карт.
- `+window:budget-window` — річний бюджет зі ставкою й статтями; `+window:evaluation-window` — оцінка мера й проблеми міста.
- `+card:influence-map`, `+card:zone-growth` — див. вище.
- `+feature:disaster-toggle` — увімк/вимк і ручний виклик катастроф.

## Джерела
- ⭐ [Wikipedia: SimCity (1989)](https://en.wikipedia.org/wiki/SimCity_(1989_video_game)) — зони, енергія, транспорт, податки, катастрофи, сценарії, клас міста 100 000 / 500 000, версії, Micropolis.
- [Inside the Simulator](https://github.com/SimHacker/micropolis/blob/wiki/InsideTheSimulator.md) — населення, поїздки R↔C↔I, вартість землі, злочинність, забруднення, станції $100/рік, податки 0–4% / 10–20%, утримання $1/$4/$4/$10.
- [Micropolis Doxygen](https://micropolisweb.com/doc/classMicropolis.html) — назви карт симуляції, `crimeScan`, `computeComRateMap` (відстань до центру).
- [GitHub: SimHacker/micropolis](https://github.com/SimHacker/micropolis) · [MicropolisCore](https://github.com/SimHacker/MicropolisCore) — відкриті сирці.
- Steam: пошук «SimCity»; YouTube: пошук «simcity 1989 gameplay».

## Непевне
- (?) Розміри: зони 3×3, електростанції 4×4, стадіон/порт/аеропорт; мапа 120×100; роздільність карт (½, ¼) — з власних знань про сирці, не бачив.
- (?) Індикатор попиту RCI, перелік оверлеїв, вікно оцінки, графіки, швидкості гри, стартові кошти за складністю — класичні елементи, у відкритих сторінках не підтверджено.
- (?) Чи електростанції забруднюють; роль стадіону/порту/аеропорту як «стелі» росту.
- (?) Повний перелік сценаріїв (крім Detroit 1972, Las Vegas, Freeland).
