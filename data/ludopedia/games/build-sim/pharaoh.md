---
title: Pharaoh
slug: pharaoh
aka: [Фараон, Pharaoh Gold, Pharaoh and Cleopatra, "Pharaoh: A New Era"]
family: build-sim
also: []
klass: cursor
axes:
  field: iso
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: constraints
year: 1999
platforms: [PC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Pharaoh_(video_game)", best: true, note: "ходоки, житло від послуг, заплавні ферми, 5 богів, рейтинги Culture/Prosperity/Monument/Kingdom, кампанія, Cleopatra, A New Era"}
  - {kind: other, url: "https://pharaoh.heavengames.com/faqs/housing/", note: "HeavenGames FAQ: roadblock спиняє лише блукаючих, водонос ~27 клітин, пожежники з запасом води, бруківка й площі"}
  - {kind: other, url: "https://pharaoh.heavengames.com/faqs/docks/", note: "HeavenGames FAQ: заплавні й лучні ферми, робітничі табори, зрошення через water lift і канави"}
  - {kind: other, url: "https://pharaoh.heavengames.com/", note: "HeavenGames: будівлі, кварталові блоки, FAQ за темами"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=Pharaoh", note: "пошук; A New Era (2023)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Pharaoh+1999+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [cell-click, multi-cell-size, impassable-cells, round-currency, coverage-area, random-walk, chase-bfs, cell-transform, spawner-entity, enemy-waves, game-pause, save-game, minimap-radar, objective-text, status-panel, sequential-levels, in-game-editor, one-way-cell, +walker-coverage, +house-evolution, +roadblock-filter, +seasonal-flood, +labor-pool, +risk-meter, +map-overlay, +drag-build-line, +ratings-goal, +god-mood, +monument-construction, +influence-map]
proposes: ["+card:roadblock-filter", "+card:seasonal-flood", "+card:monument-construction", "+card:walker-coverage", "+card:house-evolution", "+role:walker", "+trigger:month_start", "+trigger:season_start", "+cond:walker_kind", "+effect:refill", "+ui:map-overlay", "+ui:rating-columns", "+window:advisor-window"]
author: opus
date: 2026-11-09
---

# Pharaoh — модель ходоків Caesar III у Єгипті: roadblock-фільтр за видом ходока, житло з довгою драбиною потреб і поле, яке щороку забирає Ніл

## Суть
Та сама гра Impressions, що й `caesar-3` (див. там базу: ходоки по дорогах, покриття = пройдений шлях, бажаність, еволюція дому, рейтинги). Тут описано **відмінності**: (1) **roadblock** — клітина дороги, що зупиняє лише *блукаючих* ходоків, а цільових пропускає, тож маршрут служб можна «замкнути» в кварталі; (2) **розлив Нілу** — заплавні клітини частину року під водою, ферми на них працюють лише між розливами; (3) **монументи** — багатоклітинні будови з фазами, які зводять робітники з матеріалів; (4) вода й базар — ходоки (водонос, торговець базару), а не лише радіус. Рейтинги: Culture, Prosperity, **Monument**, **Kingdom**.

## Поле і час
- Ізометрична квадратна сітка, фіксований зум, поворот виду на 90°; рельєф: Ніл, заплава (floodplain), луки (meadow — жовті квіточки), пустеля, скелі, болото з очеретом, ґрунтові води (видно на оверлеї води «W»).
- Шари як у Caesar III + **шар заплави**: клітини, що в сезон розливу вкриті водою; родючість клітини ферми (видно %, низька — <10 %).
- Real-time, календар місяцями; розлив Нілу — щорічна подія (?) у заданий сезон сценарію.
- Великих мостів нема: переправа через воду — пороми (Wikipedia).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Roadblock | switch | — | клітина дороги: блукаючі ходоки розвертаються, цільові проходять |
| Блукаючий ходок (торговець базару, пожежник, поліцейський, магістрат, водонос, шукач робітників) | neutral | вид, ~27 клітин маршруту у водоноса | `random-walk` дорогою; розвертається на roadblock і в кінці маршруту |
| Цільовий ходок (візник, артист, покупець базару, мисливець, солдат, іммігрант) | neutral | ціль | найкоротший шлях, roadblock ігнорує |
| Пожежник (fire marshal) | neutral | запас води | гасить пожежі й знижує ризик; запас скінченний — повертається в пожежну частину заповнитись |
| Водонос (water supply) | spawner | ґрунтова вода, апгрейд садами/статуями | будівля лише на ґрунтових водах; ходок дає дому воду; апгрейд — частіше випускає (?) |
| Колодязь | static | радіус | вода радіусом, як у Caesar III (?) |
| Базар | spawner | покупець + торговець, апгрейд | покупець (цільовий) бере товар у зерносховищі/складі, торговець (блукаючий) розносить по домах |
| Будинок | object | рівень, розмір 1×1…4×4 (?), бажаність | драбина рівнів від хатини до маєтку (≈20 (?)); росте від послуг, товарів і бажаності; деградує раптово |
| Заплавна ферма | object | родючість, зрошення | працює лише поза розливом; робочу силу дає робітничий табір по дорозі |
| Лучна ферма | object | родючість, пряма робоча сила | лише на луках; урожай в інший час, ніж заплавні |
| Робітничий табір (work camp) | spawner | — | випускає селян-фермерів до заплав і робітників на монумент |
| Water lift + зрошувальна канава | conduit | — | lift на краю ріки/заплави; канава тягнеться drag-ом, іде під дорогами; ферма зрошена, якщо торкається кутом або ≤2 клітин |
| Монумент (піраміда, мастаба, обеліск, сфінкс…) | object | розмір, фази, матеріали | будується роками: робітники + каменярі/цеглярі (?) кладуть блоки; завершений — рейтинг Monument |
| Палац | static | — | скарбниця (дебен), податки (?) |
| Храм / святилище (Ra, Bast, Osiris, Ptah, Seth) | spawner | бог | задовольняє бога; настрій → дари або кари |
| Бруківка / площа | terrain | бажаність | ґрунтова дорога стає бруківкою біля високої бажаності; площу можна класти лише на бруківку |
| Пожежа → руїни | hazard | — | горить, доки не дійде пожежник; пожежник не пройде крізь будову (навіть сад) |
| Ворожі армії, хижаки (крокодили, гієни (?)) | enemy | — | періодичні напади; військо, флот |

## Правила (КОЛИ → ЯКЩО → ТО)
Базові правила ходоків, ризиків, бажаності, еволюції дому — як у `caesar-3`; тут — відмінні й додані.
- КОЛИ `input(build, roadblock, road_cell)` → ТО `place(roadblock)`.
- КОЛИ `enter(walker, roadblock)` → ЯКЩО `custom: «ходок блукаючий»` (`+cond:walker_kind`) → ТО `custom: «розвернутись»`; інакше прохід.
- КОЛИ `counter(water_carrier.distance, >=, 27)` (правило великого пальця) → ТО `custom: «розвернутись назад»`; маршрут часом змінюється (?).
- КОЛИ `in_range(water_carrier, house, 2)` (?) → ТО `set_state(house, water, decay_time)`.
- КОЛИ `input(build, water_supply, cell)` → ЯКЩО `cell(cell, ground_water)` → ТО `place(water_supply)`; інакше `block`.
- КОЛИ `contact(fire_marshal, fire)` → ЯКЩО `has(fire_marshal, water)` → ТО `disappear_b`; КОЛИ `counter(fire_marshal.water, <=, 0)` → ТО `custom: «повернутись у пожежну частину по воду»` (`+effect:refill`).
- КОЛИ `tick` → ЯКЩО `state(fire, burning)` and `not path_exists(fire_marshal, fire)` → ТО `transform(building, ruins)` — пожежник не проходить крізь будівлі й сади.
- КОЛИ `schedule(flood_season)` (`+trigger:season_start`) → ТО `custom: «клітини заплави вкриваються водою; ферми на них не працюють»`.
- КОЛИ `schedule(flood_end)` → ТО `custom: «вода сходить; заплавні ферми знову працюють; родючість відновлено розливом (?)»`.
- КОЛИ `tick` → ЯКЩО `state(floodplain_farm, dry)` and `connected(farm, work_camp)` → ТО `custom: «селяни з табору йдуть на ферму; ближчий табір — швидше»`.
- КОЛИ `custom: «урожай»` → ТО `give(farm, grain × fertility)`, `give(farm, straw)` — солома повна завжди, незалежно від родючості й персоналу.
- КОЛИ `input(drag_ditch, from, to)` → ЯКЩО `connected(ditch, water_lift)` → ТО `custom: «канава з водою»`; ЯКЩО `in_range(farm, ditch, 2)` → ТО `set_state(farm, irrigated)` (+родючість).
- КОЛИ `input(build, meadow_farm, cells)` → ЯКЩО `custom: «усі клітини — луки»` → ТО `place(farm)`; підсвітка зелена/червона.
- КОЛИ `tick` → ЯКЩО `custom: «дорога поруч має високу бажаність»` → ТО `set_cell(road, paved)`; КОЛИ `input(build, plaza)` → ЯКЩО `cell(road, paved)` → ТО `place(plaza)`.
- КОЛИ `tick` → ЯКЩО `in_range(bazaar|water_supply, garden|statue, r)` → ТО `custom: «будівля переходить у покращений вигляд»`.
- КОЛИ `custom: «бажаність, товари й послуги дому ≥ вимог наступного рівня»` → ТО `transform(house, next_level)`; сусідні такі ж дома зливаються в більший (?).
- КОЛИ `tick` → ЯКЩО `state(monument_site, active)` and `has(storage, stone|brick)` → ТО `custom: «робітники й будівельники кладуть наступний блок; фаза за фазою»`.
- КОЛИ `custom: «монумент завершено»` → ТО `counter(monument_rating, +n)`; часто — умова перемоги сценарію (?).
- КОЛИ `timer(month)` (`+trigger:month_start`) → ТО `custom: «настрій 5 богів (Ra — царство, Bast — дім, Osiris — землеробство й розлив (?), Ptah — ремесла, Seth — війна) від храмів і свят»`; високий → дар, низький → кара.
- КОЛИ `custom: «Road to Egypt заблоковано»` → ТО `custom: «інженери фараона підривають завал і зносять місто, доки не очистять»`.
- КОЛИ `all_constraints_met` (населення + Culture/Prosperity/Monument/Kingdom ≥ цілей, монументи) → ТО `win` → наступна місія; підвищення аж до титулу Фараона.
- Рахунок — рейтинги; free-build сценарії частково без кінця.

## Керування і ввід
- Як у Caesar III: миша, меню будівель за категоріями, drag для доріг, канав, стін; поворот мапи на 90°; клік по будинку — чого бракує, по ходоку — його маршрут (?).
- Roadblock ставиться кліком на клітину дороги; правий клік по дому показує, куди змінився маршрут водоноса.
- Оверлеї (вода, пожежа, бажаність, родючість (?)) — клавіші/меню.

## Вікна, меню, HUD
- `main-menu`: кампанія (5 періодів, +1 у Cleopatra) · free-build (≈десяток сценаріїв) · завантажити · редактор мап.
- `game-screen`: ізометрія + бічна панель будівель, `minimap`, верхній рядок (дебени, населення, дата).
- `+window:advisor-window` — «Overseers»: зведення по праці, військах, царству, рейтингах, торгівлі, населенні, здоровʼю, освіті, розвагах, релігії, фінансах.
- `map-window`: мапа царства — торгові шляхи, імпорт/експорт.
- Вікно будівлі (`custom-window`): працівники, стан, для дому — потреби; для ферми — зрошення, родючість.
- HUD: `coins`, `objective-text`, `+ui:rating-columns` (Culture/Prosperity/Monument/Kingdom), `+ui:map-overlay`.
- `pause-menu`, `save-slots`, `end-screen` місії.

## Фічі поза полем
- `levels-sequential` кампанії за історичними періодами; `mode-sandbox` (open-ended free-build); `level-editor` (редактор мап); `save-slots`, `speed-control`, `pause`.
- Розширення Cleopatra: Queen of the Nile (2000, BreakAway) — +період; Pharaoh: A New Era (2023, Triskell/Dotemu) — ремейк з обома кампаніями.

## Варіації й родичі
- `caesar-3` — база моделі; Zeus, Emperor — наступні в серії Impressions; Augustus/Julius-рушій Caesar III теж додає roadblock.
- `timberborn` — вода як рівень і посухи; `simcity-1989` — покриття радіусом.
- **Осі варіацій «фільтр маршруту»**: нема (Caesar III) / roadblock для блукаючих (Pharaoh) / ворота лише для своїх (стіни).
- **Осі «сезонна клітина»**: клітина міняє тип за календарем (заплава ↔ вода) · родючість, яку поновлює подія · ферма лише на типі клітини (луки).
- Осі «води»: радіус (колодязь) / ходок (водонос) / мережа (акведуки Caesar III, канави тут).

## Цікавинки для курсу
- Roadblock як клітина-фільтр за видом агента — 🌱 (одна умова в `random-walk`).
- Блукаючий vs цільовий ходок на тому ж графі доріг — 🥉 (`random-walk` + BFS).
- Пожежник зі скінченним запасом, що вертається по воду — 📎.
- Розлив: клітини заплави за календарем стають водою, ферми «вимикаються» — 📎.
- Зрошення: канави як граф від water lift, ферма зрошена, якщо в межах 2 клітин — 📎.
- Монумент: фазне будівництво з черги матеріалів і робітників — 🥈.

## Мапа на каталог
- Є: `random-walk` + `chase-bfs` (два види ходоків) · `one-way-cell` (найближче до roadblock: прохід лише для частини — не точно) · `coverage-area` (колодязь) · `cell-transform` (дім, дорога → бруківка, будова → руїна) · `spawner-entity` · `multi-cell-size` · `impassable-cells` · `round-currency` · `enemy-waves` · `minimap-radar` · `objective-text` + `status-panel` · `sequential-levels` · `in-game-editor` · `save-game` · `game-pause`.
- **Нема** → пропозиції карток:
  - `+roadblock-filter` «Клітина спиняє лише агентів певного виду» · entities/legality · 🌱 · слоти {kinds}.
  - `+seasonal-flood` «Клітини міняють тип за календарем» · entities/state · 📎 · слоти {cells, season, effect}.
  - `+monument-construction` «Фазна будова з матеріалів і робітників» · game-logic/economy · 🥈.
  - `+walker-coverage`, `+house-evolution`, `+labor-pool`, `+risk-meter`, `+ratings-goal`, `+god-mood`, `+map-overlay`, `+influence-map`, `+drag-build-line` — уже пропоновані `caesar-3`, тут підтвердження.

## Пропозиції до словників
- `+card:roadblock-filter`, `+card:seasonal-flood`, `+card:monument-construction` — див. вище; `+card:walker-coverage`, `+card:house-evolution` — друга гра (правило трьох).
- `+role:walker` — друга гра після Caesar III.
- `+trigger:month_start` — календарний тік (друга гра); `+trigger:season_start` — початок сезону (розлив, Stardew-сезони).
- `+cond:walker_kind` — вид агента (блукаючий/цільовий) як умова фільтра.
- `+effect:refill` — агент повертається поповнити запас (вода пожежника, набої).
- `+ui:map-overlay`, `+ui:rating-columns`, `+window:advisor-window` — друга гра.

## Джерела
- ⭐ [Wikipedia: Pharaoh](https://en.wikipedia.org/wiki/Pharaoh_(video_game)) — жанр, ходоки служб, житло за потребами, заплавні ферми й зрошення, 5 богів і їхні сфери, рейтинги, кампанія, free-build, редактор, Cleopatra, A New Era.
- [HeavenGames FAQ: Housing, Roads & Walkers](https://pharaoh.heavengames.com/faqs/housing/) — повний список, кого спиняє roadblock; водонос ~27 клітин; пожежники з запасом; бруківка, площі, апгрейд базару/водоноса садами.
- [HeavenGames FAQ: Docks, Industry, Farming](https://pharaoh.heavengames.com/faqs/docks/) — заплавні ферми лише поза розливом, робітничі табори, лучні ферми, water lift, канави, «≤2 клітин», солома.
- [HeavenGames](https://pharaoh.heavengames.com/) — індекс будівель і кварталових блоків.

## Непевне
- (?) Точний календар розливу, якість розливу за роком і звʼязок з настроєм Osiris — з памʼяті, у відкритих сторінках не було.
- (?) Кількість рівнів житла (≈20) і злиття домів у 2×2/3×3/4×4 маєтки — з памʼяті.
- (?) Радіус обслуговування ходока (2 клітини), колодязь-радіус — перенесено з моделі Caesar III.
- (?) Хто саме будує піраміди (каменярі, цеглярі, теслі) і фази — з памʼяті; Wikipedia каже лише «worker facilities + materials, take time».
- (?) Податки через палац/збирачів і золоті копальні — з памʼяті.
