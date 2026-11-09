---
title: ActRaiser (режим симуляції)
slug: actraiser-sim
aka: [ActRaiser, アクトレイザー, Actraiser Renaissance, Creation mode]
family: build-sim
also: []
klass: hybrid
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: state
year: 1990
platforms: [SNES, Wii Virtual Console, "Renaissance: Switch, PS4, PC, iOS, Android"]
links:
  - {kind: other, url: "https://archive.org/details/act-raiser-usa", best: true, note: "скан мануалу SNES (USA): Command Guide, Miracles (Acts of Nature), Offerings, Purpose of the Simulation Mode, монстри, Cultural Level, поради по землях"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/ActRaiser", note: "ангел, дороги, чудеса, 4 лігва на землю, запечатування, рівень Майстра від населення; Renaissance з tower defense"}
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/%E3%82%A2%E3%82%AF%E3%83%88%E3%83%AC%E3%82%A4%E3%82%B6%E3%83%BC", note: "JA: яке чудо прибирає яку перешкоду, 4 монстри симуляції, предмети-рішення проблем"}
  - {kind: other, url: "https://lparchive.org/Actraiser/Update%2002", note: "Let's Play: ціни чудес у SP, маркер напряму, пісочний годинник, хатина +4 / будинок +6"}
  - {kind: other, url: "http://almarsguides.com/retro/walkthroughs/snes/games/ActRaiser/", note: "ліміт 128 будівель на землю, пшениця через землетрус"}
  - {kind: other, url: "https://sneslab.net/wiki/ActRaiser_Quick_Links", note: "зміст мануалу з посиланнями на сторінки скану"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=ActRaiser+simulation+mode", note: "пошук; геймплей режиму симуляції"}
stage: v1
coverage: 45
mechanics: [cell-click, cell-transform, destructible-blocks, hidden-under-block, interaction-table, spawner-entity, reinforcements, projectile-shot, hp-damage, round-currency, inventory-items, inventory-limit, map-window, status-panel, stats-window, sequential-levels, level-unlock, save-single-slot, +direction-marker-growth, +build-phase-timer, +lair-seal-by-growth, +god-powers, +house-evolution, +town-requests, +population-xp, +cross-mode-link, +structure-cap]
proposes: ["+card:direction-marker-growth", "+card:build-phase-timer", "+card:lair-seal-by-growth", "+card:town-requests", "+card:population-xp", "+card:cross-mode-link", "+card:god-powers", "+card:house-evolution", "+ui:growth-indicator"]
author: opus
date: 2026-11-09
---

# ActRaiser (режим симуляції) — бог не будує місто, а вказує напрям: люди тягнуть дорогу до лігва й запечатують його забудовою

## Суть
ActRaiser чергує два режими: бічний екшн (статуя-воїн проходить ACT 1 і ACT 2 кожної землі) і між ними — симуляцію згори, де гравець — Ангел, слуга Майстра. Люди будують самі; гравець лише ставить маркер напряму, творить чудеса (блискавка, дощ, сонце, вітер, землетрус), щоб прибрати перешкоди, і стрілами відганяє летючих монстрів, що вилітають з чотирьох лігв. Лігво замовкає, коли місто доростає до нього й забудовує його клітину. Клас — `hybrid`: Ангел-аватар (політ, стрільба) + курсор (маркер, ціль чуда).

## Поле і час
- Мапа однієї землі згори; рельєф, дороги, будинки й поля — у клітинах; ціль чуда — «жовтий квадрат» на клітині. Ангел і монстри літають вільно над сіткою.
- Шість земель (Fillmore, Bloodpool, Kasandora, Aitos, Marahna, Northwall); на старті землі — храм і двоє людей.
- Час — real-time «пісочний годинник»: коли пісок пересипався, настає фаза «Town Under Construction» (нові будинки, ділянки, приріст населення). Час стоїть в Action Mode, у Sky Palace і в деяких фазах симуляції.
- Ліміт — 128 будівель на землю, разом із мостами.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Ангел | player | HP (залежить від рівня Майстра), стріли | літає, стріляє; HP 0 → не стріляє, доки HP не відновиться з часом |
| Храм | static | — | центр першого поселення; сюди «йдуть душі» вбитих монстрів (за LP) |
| Маркер напряму | mark | — | куди люди прокладуть дорогу; не можна поставити далі за порожню клітину, доки не виросте населення |
| Дорога | terrain | — | росте в бік маркера; уздовж неї зʼявляються будинки й поля |
| Будинок | object | культурний рівень 1–3; хатина +4 людини, будинок +6 | зводиться у фазі будівництва; рівень 3 — сейсмостійкий |
| Поле | terrain | продуктивне / висохле; кукурудза → пшениця → рис-чек | годує ріст; висохле зупиняє ріст |
| Кущі, дерева, скелі | static | знищувані | блокують забудову; блискавка прибирає |
| Болото, сніг | terrain | — | сонце осушує / розтоплює |
| Пустеля | terrain | — | дощ перетворює на луки |
| Ріка | static | — | без технології «Bridge» не забудовується |
| Невидалювані форми рельєфу | static | — | постійні («What's not destructible») |
| Лігво монстрів ×4 | spawner | запас монстрів (видно кнопкою B над лігвом) | породжує монстрів на заміну вбитим, доки не запечатане |
| Napper Bat | enemy | — | нападає на будинки й викрадає людей; убитий — люди повертаються |
| Blue Dragon | enemy | — | громом підпалює будинки |
| Red Demon | enemy | — | випалює й висушує продуктивні поля |
| Skull Head | enemy | висока міцність | якщо лишити — землетрус, великі руйнування |
| Пожежа | hazard | — | палить будинок, згасає сама |
| Підношення | pickup | ліміт у запасі | знаходять жителі під час забудови; Майстер бере і використовує |
| Source of Magic · Bomb · Wheat · Bridge · Herb · Sheep fleece · Music · Compass · Skull of Destruction | pickup | — | +MP · знищити монстрів на екрані · поля → пшениця · мости · ліки від чуми · теплий одяг · миряться сварки · морська подорож · запечатати лігво, яке люди не можуть |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(build_here, cell)` → ЯКЩО `custom: «клітина не далі за одну порожню від забудови»` → ТО `mark(cell, direction)`; інакше `block`.
- КОЛИ `timer(hourglass)` → ЯКЩО `not custom: «у місті невирішена проблема»` → ТО `custom: «Town Under Construction: дорога, будинки й поля ростуть у бік маркера»`, `counter(population, +n)`.
- КОЛИ `timer(hourglass)` → ТО `heal(angel, n)`.
- КОЛИ `counter(world_population, >=, next_level)` → ТО `custom: «рівень Майстра +1: більше HP і SP — і в Action Mode»`.
- КОЛИ `input(miracle, cell)` → ЯКЩО `not counter(sp, >=, cost)` → ТО `block`; інакше `counter(sp, -cost)` і ефект чуда (блискавка 10 · дощ 20 · сонце 30 · вітер 80 · землетрус 160 SP).
- КОЛИ `input(lightning, cell)` → ЯКЩО `cell(x, bush|tree|rock)` → ТО `set_cell(cell, plain)`; ЯКЩО `occupied(cell, monster)` → ТО `disappear(monster)`; ЯКЩО `occupied(cell, house)` → ТО `disappear(house)` (люди гинуть).
- КОЛИ `input(rain, cell)` → ЯКЩО `cell(x, dried_field)` → ТО `set_cell(cell, field)`; ЯКЩО `cell(x, desert)` → ТО `set_cell(cell, grassland)`.
- КОЛИ `input(sun, cell)` → ЯКЩО `cell(x, marsh|snow)` → ТО `set_cell(cell, plain)`.
- КОЛИ `input(wind)` → ТО `custom: «здуває летючих монстрів з екрана»`; у землі з вітряками — `custom: «вітряки рушають, ріст відновлюється»`.
- КОЛИ `input(earthquake)` → ТО `custom: «уся земля: руйнує будинки нижче рівня 3 і поля; відкриває приховане (піраміда в Kasandora)»`.
- КОЛИ `destroyed(house)` → ТО `custom: «на ділянці зводять будинок поточного культурного рівня»` — свідоме знесення старого прискорює рівень.
- КОЛИ `died(monster)` → ЯКЩО `not state(lair, sealed)` → ТО `spawn_at(monster, lair)`.
- КОЛИ `contact(arrow, monster)` → ТО `damage(monster, n)`; КОЛИ `died(monster)` → ТО `counter(sp, +n)`.
- КОЛИ `contact(angel, monster)` → ТО `damage(angel, n)`.
- КОЛИ `hp_zero(angel)` → ТО `set_state(angel, no_arrows)` до відновлення HP.
- КОЛИ `contact(napper_bat, house)` → ТО `custom: «викрадає людей»`, `counter(population, -n)`; КОЛИ `died(napper_bat)` → ТО `custom: «викрадені повертаються»`.
- КОЛИ `contact(blue_dragon, house)` → ТО `spawn_at(fire, house)`.
- КОЛИ `tick` → ЯКЩО `occupied(cell, fire)` → ТО `custom: «будинок згоряє, вогонь згасає сам»`.
- КОЛИ `contact(red_demon, field)` → ТО `set_cell(field, dried_field)`.
- КОЛИ `timer(n)` → ЯКЩО `state(skull_head, alive)` → ТО `custom: «землетрус у місті»`.
- КОЛИ `reach(road, lair)` → ЯКЩО `counter(population, >=, seal_threshold)` → ТО `set_state(lair, sealed)`, `counter(population, +n)`; частина лігв `give(master, offering)`.
- КОЛИ `counter(sealed_lairs, ==, 4)` → ТО `custom: «культурний рівень землі максимальний — найкращі будинки»`, `unlock(act2)`.
- КОЛИ `custom: «жителі просять допомоги (чума, сварка, холод, ріка)»` → ЯКЩО `has(master, herb|music|fleece|bridge)` → ТО `use(master, item)`, `custom: «ріст відновлюється»`; інакше `custom: «індикатор росту — Stop»`.
- КОЛИ `custom: «забудовано клітину зі схованим предметом»` → ЯКЩО `count(offerings, <, limit)` → ТО `give(master, offering)` (через «Take an Offering»).
- КОЛИ `input(use_offering, bomb)` → ТО `custom: «знищити всіх монстрів на екрані»`; `wheat` → `custom: «поля → пшеничні»`.
- КОЛИ `counter(structures, ==, 128)` → ТО `block`.
- Перемога: усі 4 лігва запечатано → ACT 2 цієї землі. Поразки в симуляції нема (?). Рахунок: населення світу = досвід Майстра.

## Керування і ввід
- Хрестовина — політ Ангела (і курсор); кнопка B — відкрити вікно команд / підтвердити; окрема кнопка — скасувати; B над лігвом — скільки в ньому монстрів.
- Команда «будувати / слухати людей» ставить маркер напряму; «Miracles» — вибір чуда, потім жовтий квадрат на клітині (вітер і землетрус — на всю землю).
- Стріли Ангела — кнопкою (?); у Sky Palace — X/L збільшують і зменшують мапу світу.

## Вікна, меню, HUD
- `splash-screen`: START / CONTINUE → `custom-window` введення імені (без імені гра не почнеться).
- `map-window` — Sky Palace над мапою світу: перелетіти до землі, «Fight Monsters» (Action Mode), «Observe the People» (симуляція), Select Magic, Status of Master, Other.
- `game-screen` симуляції: мапа землі, Ангел, `hp-bar` Ангела, пісочний годинник (`timer-countdown`), вікно повідомлень жителів.
- `custom-window` команд: будувати/слухати · Miracles (5 іконок із ціною SP) · Offerings (Take / Use) · Other.
- `stats-window` «Status of Master»: рівень, HP, SP, MP, населення світу, прийняті підношення, населення до наступного рівня; B — очки Action Mode.
- `stats-window` «Status of Cities»: по 6 землях — знайдені підношення, населення, культурний рівень, `+ui:growth-indicator` (нема людей / повільно / росте / проблема-стоп / повний потенціал).
- `dialogue-window` — «голос народу»: прохання, підказки, катастрофи.
- `confirm-dialog` «Progress Log» (Yes / No) — збереження; `settings-window` — швидкість повідомлень.

## Фічі поза полем
- `save-single-slot` — «Progress Log» з Sky Palace або симуляції, одна історія на картридж.
- Прогресія: населення світу → рівень Майстра → HP в екшені; низький рівень закриває вхід у деякі землі (`level-unlock`).
- Підношення з однієї землі розвʼязують проблеми іншої (Bridge, Compass) — прогресія через обмін предметами.
- Після проходження — режим лише з екшн-рівнями, без симуляції.

## Варіації й родичі
- **ActRaiser 2** (1993) — без режиму симуляції.
- **Actraiser Renaissance** (2021): квести, сутички «Mass Invasion» у дусі tower defense просто на мапах симуляції; технологію мостів жителі винаходять самі.
- Родичі в корпусі: `populous` (бог рівняє землю, люди будують самі), `reus` (гіганти тераформують, села ростуть самі), `simcity-1989` (зони ростуть від умов), `caesar-3` (будинок еволюціонує від умов).
- **Осі варіацій**: як бог керує ростом — маркер напряму / зонування / рівняння землі; як прибрати перешкоду — чудо-заклинання за ману / інструмент за гроші; ворог — лігво-спавнер до запечатування / хвилі / нема.

## Цікавинки для курсу
- Маркер напряму + періодична фаза будівництва: місто росте фронтом до маркера, лише по вільних клітинах — 🥉 (BFS-фронт з обмеженням).
- Лігво спавнить на заміну вбитим, доки місто не забудує його клітину — 📎 (спавнер зі станом «запечатано»).
- Чудеса як таблиця «тип клітини × чудо → новий тип» — 📎 (картка `interaction-table` на рельєфі).
- Знести старе, щоб виросло нове: землетрус чи пожежа → будинок поточного культурного рівня — 📎.
- Два режими живлять один одного: населення → HP героя, очки екшну → запас монстрів у лігвах — 🥉.
- Сховані в клітинах підношення, ліміт запасу й обмін ними між землями — 📎.

## Мапа на каталог
- Є: `cell-click` (ціль чуда) · `cell-transform` + `destructible-blocks` (чудеса змінюють клітини) · `hidden-under-block` (підношення в землі) · `interaction-table` · `spawner-entity` + `reinforcements` (лігва) · `projectile-shot` (стріли) · `hp-damage` (HP Ангела) · `round-currency` (SP) · `inventory-items` + `inventory-limit` (підношення) · `map-window` · `status-panel` · `stats-window` · `sequential-levels` · `level-unlock` · `save-single-slot`.
- **Нема** → пропозиції карток:
  - `+direction-marker-growth` «Маркер напряму росту поселення» · entities/spawn · 📎 · слот {max_gap}.
  - `+build-phase-timer` «Фаза будівництва за таймером» · game-logic/economy · 🌱 — приріст пакетом, а не щотік.
  - `+lair-seal-by-growth` «Спавнер вимикається, коли гравцева забудова накриває його» · entities/spawn · 📎.
  - `+town-requests` «Запит жителів зупиняє ріст до відповіді предметом чи чудом» · game-logic/economy · 📎.
  - `+population-xp` «Населення як досвід героя» · game-logic/economy · 🌱.
  - `+cross-mode-link` «Режими гри обмінюються ресурсами» · code/architecture · 🥉.
  - `+structure-cap` «Ліміт кількості будівель на мапі» · entities/legality · 🌱.
  - `+god-powers`, `+house-evolution` — підтвердження (Populous, Caesar III).

## Пропозиції до словників
- `+card:direction-marker-growth`, `+card:build-phase-timer`, `+card:lair-seal-by-growth`, `+card:town-requests`, `+card:population-xp`, `+card:cross-mode-link` — див. вище.
- `+card:god-powers`, `+card:house-evolution` — підтвердження наявних пропозицій.
- `+ui:growth-indicator` — стан росту кожного міста одним словом-іконкою (нема / повільно / росте / стоп / повний).

## Джерела
- ⭐ [Мануал SNES (USA), archive.org](https://archive.org/details/act-raiser-usa) — OCR сторінок симуляції: Command Guide, Acts of Nature, Offerings, Status of Cities, Purpose of the Simulation Mode, Monsters on the Ground Too, Cultural Level, поради по землях.
- [Wikipedia: ActRaiser](https://en.wikipedia.org/wiki/ActRaiser) — Ангел, дороги, чудеса, 4 лігва, запечатування, рівень від населення, Renaissance.
- [Wikipedia JA: アクトレイザー](https://ja.wikipedia.org/wiki/%E3%82%A2%E3%82%AF%E3%83%88%E3%83%AC%E3%82%A4%E3%82%B6%E3%83%BC) — блискавка/сонце/дощ по типах землі, Napper Bat / Blue Dragon / Red Devil / Skull Head, предмети-рішення.
- [LP Archive, Update 02](https://lparchive.org/Actraiser/Update%2002) — ціни чудес, маркер, годинник, хатина +4 / будинок +6, запас лігв від очок екшну.
- [Almar's Guides](http://almarsguides.com/retro/walkthroughs/snes/games/ActRaiser/) — 128 будівель, землетрус для пшениці й старих будинків.
- YouTube: пошук «ActRaiser simulation mode».

## Непевне
- (?) Ліміт підношень у запасі — OCR мануалу нечитабельний («only possess & offerings»), імовірно 8.
- (?) Чи може Ангел «програти» в симуляції — джерела кажуть лише, що при HP 0 він не стріляє.
- (?) Душі вбитих монстрів → нові люди в храмі і запас лігв від очок екшну — лише з Let's Play.
- (?) Культурний рівень зростає від запечатування лігв (JA) чи від знищення всіх монстрів (EN) — джерела формулюють по-різному.
- (?) Призначення кнопок (постріл, скасування) — OCR сторінки керування пошкоджений.
- (?) Поріг населення для запечатування лігва — мануал каже, що підказку дають жителі Fillmore; число не бачив.
