---
title: "Cosmoteer: Starship Architect & Commander"
slug: cosmoteer
aka: [Cosmoteer]
family: build-sim
also: [tactics]
klass: hybrid
axes:
  field: square
  time: realtime
  opponent: ai
  info: full
  random: both
  goal: state
year: 2022
platforms: [PC]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/799600/Cosmoteer_Starship_Architect_Commander/", best: true, note: "форма корпусу й план палуби, автономний екіпаж носить боєприпаси, модулі руйнуються окремо, корабель розпадається на шматки"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Cosmoteer", note: "тайлова 2D-сітка, екіпаж постачає системи, режими Career / Creative, PvP"}
  - {kind: official, url: "https://cosmoteer.net/", note: "офіційний сайт, FAQ"}
  - {kind: other, url: "https://steamcommunity.com/sharedfiles/filedetails/?id=2866401542", note: "Ultimate Ship Design and Part Guide (v0.20): батареї, реактори, двигунні відсіки, броня проти щитів, конвеєри"}
  - {kind: other, url: "https://steamcommunity.com/sharedfiles/filedetails/?id=2880746225", note: "Bullet Point Basics — Career: батареї за рейс S/M/L, зарплати, мінімальний корабель, захоплення через шлюз"}
  - {kind: other, url: "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=799600&count=60&maxlength=1200", note: "Steam News: тепло й пожежі (0.30), overclock, ramp-down двигунів, місткість складів"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Cosmoteer+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [multi-cell-size, orientation-state, impassable-cells, cursor-place, drag-drop-piece, hover-highlight, hp-damage, explode-area, chain-detonation, chase-bfs, round-currency, shop-window, ai-opponent, online-multiplayer, save-game, game-pause, coverage-area, +crew-hauling, +job-priority-grid, +power-battery-delivery, +ammo-feed, +adjacency-buff, +connectivity-split, +module-targeting, +fire-spread, +heat-diffusion, +armor-vs-shield, +roof-layer-block, +derelict-capture, +blueprint-ghost, +escalating-salary, +overclock-mode, +thrust-from-layout]
proposes: ["+effect:split_ship", "+cond:connected_to_core", "+trigger:part_destroyed", "+role:crew", "+role:module", "+window:ship-editor", "+window:crew-roles", "+window:galaxy-map", "+ui:supply-bars", "+ui:firing-arc", "+feature:ironman-mode", "+card:crew-hauling", "+card:connectivity-split", "+card:thrust-from-layout", "+card:roof-layer-block"]
author: opus
date: 2026-11-09
---

# Cosmoteer — корабель як план на клітинах: екіпаж бігає коридорами з батареями й снарядами, кожен модуль має HP, а розірвана сітка розпадається на окремі кораблі

## Суть
Гравець малює корабель на 2D-сітці: корпус, коридори, двері, каюти, реактори, двигуни, зброю, щити, броню, фабрики. Потім командує ним у реальному бою, задаючи лише курс і цілі; **екіпаж автономний** — бере батареї в реакторі й снаряди на складі чи фабриці та фізично несе їх до споживачів, тому довжина коридорів прямо визначає темп стрільби. Кожен модуль — окремий обʼєкт з HP: влучання знищує модулі по одному, а коли руйнується перемичка, **сітка корабля розпадається на кілька шматків**. Незвичне для сімʼї: логістика «працівник несе ресурс» усередині обʼєкта, що сам є полем бою.

## Поле і час
- Корабель — тайлова 2D-сітка, редагується будь-коли; модулі займають прямокутники клітин і мають орієнтацію (двигуни, ствольна зброя з дугою стрільби).
- Два шари: палуба (підлога, коридори, каюти, модулі) і «дах» — поверхневі гармати й щити стоять зверху; дахова зброя блокує одна одну.
- Космос навколо — вільний (`free`) фізичний простір: кораблі мають масу, тягу, інерцію; бій — real-time з паузою (?).
- Career: процедурна галактика з секторами, станціями, ресурсами в космосі; Creative — без обмежень ресурсів.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Член екіпажу | ally | швидкість, роль, пріоритети | автономно бере задачу: несе батарею/снаряд, ремонтує, гасить, пілотує, стріляє |
| Каюта / нари (crew quarters) | spawner | місткість | дає екіпаж; вільні повертаються сюди |
| Коридор | terrain | — | прохід для екіпажу; довжина шляху = затримка постачання |
| Рухома доріжка (walkway/conveyor) | terrain | напрям | прискорює екіпаж і доставку; постріл крізь неї рве потік |
| Двері | gate | дорогі | пропускають екіпаж; автопостановка може подовжити шляхи |
| Шлюз (airlock) | gate | — | вихід екіпажу назовні; потрібен для захоплення й кисню |
| Рубка (cockpit / control room) | static | — | керування кораблем; мінімальний корабель = рубка + реактор + каюта + шлюз |
| Реактор S / M / L | source | 1 / 2 / 3 батареї за рейс | виробляє батареї; M і L — величезний вибух при знищенні |
| Накопичувач (power capacitor) | container | 24 батареї | запас енергії далеко від реактора |
| Двигун (thruster) | object | тяга, напрям | штовхає корабель; великі — з ramp-down тяги |
| Двигунний відсік (engine room) | switch | — | живить сусідні двигуни без екіпажу; кожен прилеглий двигун: тяга +50 %, енергія +50 % |
| Лазер, іонний промінь, призма | object | батареї | енергетична зброя; промінь — фіксований напрям; призма складає промені зі спадом |
| Гармата, рейкотрон, flak | object | набої | балістика; гармати підпалюють |
| Ракетна установка + фабрика ракет | object + source | HE / EMP / ядерні | ракети наводяться; сусідні фабрики ракет і мін — бонус |
| Фабрика набоїв | source | ресурс | гармата : фабрика = 2 : 1, рейкотрон 1 : 1 |
| Склад (storage) | container | 40 одиниць на клітину (сталь, котушки…) | запас ресурсів і набоїв; слабке місце корабля |
| Броня (блоки, клини 1×3) | static | HP, пробиття | дешевий HP; захищає від прямих влучань |
| Щит | object | HP, енергія | купол над модулями; лише disruptor пробиває |
| Вогнегасник / пожежа | hazard | розмір вогню | вогонь шкодить з часом, поширюється з шансом |
| Тепло (0.30) | hazard | значення на клітину | поширюється між клітинами й згасає; гарячі частини дістають більше шкоди |
| Ворожий корабель / станція | enemy | дизайн, фракція | ціль контрактів; знищений — уламки й ресурси |
| Ресурси в космосі | resource | вид | збирає майнінг-лазер; плаваючі в сітці будівництва йдуть на будівництво першими |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ЯКЩО `custom: «модулю бракує батарей або набоїв»` and `custom: «є вільний член екіпажу з такою роллю/пріоритетом»` → ТО `custom: «задача постачання»`, `move(crew, source)`.
- КОЛИ `contact(crew, reactor)` → ТО `give(crew, battery)` (S — 1, M — 2, L — 3 за рейс), `carry(crew, battery)`.
- КОЛИ `contact(crew, consumer)` → ЯКЩО `has(crew, battery|ammo)` → ТО `take(crew, item)`, `custom: «запас модуля росте»`.
- КОЛИ `enter(crew, walkway)` → ТО `speed(crew, +k)`.
- КОЛИ `adjacent(thruster, engine_room)` → ТО `custom: «тяга +50 %, енергоспоживання +50 %, живлення без екіпажу»`.
- КОЛИ `timer(production)` → ЯКЩО `has(ammo_factory, resource)` → ТО `spawn(ammo)` у фабриці; ЯКЩО `adjacent(missile_factory, mine_factory)` → ТО `custom: «бонус швидкості»`.
- КОЛИ `input(target, enemy_part)` → ЯКЩО `custom: «ціль у дузі й дальності зброї»` and `custom: «у зброї є заряд»` → ТО `spawn(projectile)`.
- КОЛИ `contact(projectile, shield)` → ЯКЩО `not custom: «disruptor»` → ТО `damage(shield, n)`, `disappear(projectile)`.
- КОЛИ `contact(projectile, part)` → ТО `damage(part, n)`; ЯКЩО `state(part, hot)` → ТО `custom: «шкода більша»`.
- КОЛИ `hp_zero(part)` → ТО `disappear(part)`; ЯКЩО `custom: «реактор M/L»` → ТО `explode(area, large)`; ЯКЩО `custom: «фабрика набоїв або H.E.»` and `prob(p)` → ТО `set_state(tile, fire)`.
- КОЛИ `destroyed(part)` → ЯКЩО `not connected(ship_tiles)` → ТО `custom: «корабель розпадається на кілька окремих тіл»`.
- КОЛИ `contact(shell, part)` → ЯКЩО `prob(p)` → ТО `set_state(tile, fire)` (гармати й рейкотрони пробивають і підпалюють).
- КОЛИ `tick` → ЯКЩО `state(tile, fire)` → ТО `damage(tile, n)`; ЯКЩО `prob(15 %)` → ТО `custom: «вогонь на сусідню клітину»` (повнорозмірний; з 0.30.0b).
- КОЛИ `tick` → ТО `custom: «тепло дифундує між клітинами й згасає»`; ЯКЩО `custom: «тепло клітини ≥ поріг»` → ТО `set_state(tile, fire)`.
- КОЛИ `contact(crew, fire)` → ЯКЩО `has(crew, extinguisher)` (?) → ТО `clear_state(tile, fire)`.
- КОЛИ `destroyed(walkway)` → ТО `custom: «потік ресурсів далі по лінії обірвано»`.
- КОЛИ `input(place, roof_weapon)` → ЯКЩО `custom: «дахова зброя перекриває дугу іншої»` → ТО `custom: «блокує постріл»`.
- КОЛИ `tick` → ЯКЩО `custom: «членові екіпажу бракує O₂ і нема шлюзу на своєму кораблі»` → ТО `custom: «шукає шлюз / гине»` (?).
- КОЛИ `input(transfer_crew, derelict)` → ЯКЩО `custom: «у корабля є шлюз і місце для екіпажу»` → ТО `set_side(derelict, player)`.
- КОЛИ `input(place, part)` у редакторі (Career) → ТО `custom: «привид частини; екіпаж будує з ресурсів»`; ЯКЩО `not has(ship, resource)` на станції → ТО `currency(-price)` (докупити на місці).
- КОЛИ `input(hire, crew)` → ТО `currency(-salary)`; кожен наступний дорожчий за попереднього.
- КОЛИ `input(overclock, part)` → ТО `set_state(part, overclock)` — вища потужність, більше тепла (?).
- КОЛИ `custom: «двигун втратив живлення»` → ЯКЩО `custom: «Boost Thruster»` → ТО `custom: «вмикається лише після повного заряду»`.
- Перемога: знищити/знешкодити ціль контракту або ворога PvP · Поразка: корабель знищено (?) · Рахунок: кредити й слава (fame) в Career.

## Керування і ввід
- Редактор: палітра частин → привид на сітці → клік/drag; поворот частин; копіювання; завантаження готового корабля (Load Ship).
- Бій: курс і орієнтація корабля (мишею/клавішами), вибір цілі-модуля ворога ПКМ, групи кораблів і формації.
- Екіпажем напряму не керують: лише ролі, пріоритети робіт, призначення до станцій.
- Кастомні дальність і дуга стрільби кожної зброї (0.30.5).

## Вікна, меню, HUD
- `game-screen`: космос з кораблями, `+ui:supply-bars` (енергія / набої / екіпаж модуля), `hp-bar` модулів, `+ui:firing-arc`, `minimap` (?).
- `+window:ship-editor` — сітка корабля, палітра частин (`tool-palette`), статистика маси й тяги.
- `+window:crew-roles` — ролі й пріоритети екіпажу (аналог `+window:job-priorities`).
- `+window:galaxy-map` (Career), `shop-window` (станції: частини, ресурси, найм), контракти фракцій.
- `main-menu` → `mode-select` (Career · Creative · PvP · co-op) → `match-setup` (складність, Ironman) → `game-screen`; `pause-menu`, `settings-window`.

## Фічі поза полем
- Режими: Career (`mode-coop` онлайн), Creative (`mode-sandbox`), PvP (`mode-versus`, онлайн і LAN).
- `custom-difficulty` (Adjustable Difficulty; Grand Admiral), `+feature:ironman-mode` (0.30.4), `save-slots` («Save Anytime»), `cloud-save`.
- `mod-support` (Steam Workshop, моддинг-фреймворк), обмін дизайнами кораблів, фарбування корпусу й декалі.
- Доступність: альтернативні кольори, без таймінгового вводу.

## Варіації й родичі
- Ранні версії Cosmoteer до Early Access (гра в розробці 11+ років) (?).
- Корпус: `space-haven` (корабель-сітка, тепло, гази), `oxygen-not-included-cells`, `rimworld-rooms`, `prison-architect-rooms` (агенти-носії), `factorio-belts` (постачання), `mindustry` (`+ammo-feed`).
- Поза корпусом: FTL (корабель із відсіками), Starsector, Space Engineers, Avorion, Reassembly (розпад на шматки).
- Осі: **постачання** — дротом миттєво / агент несе ресурс (Cosmoteer) · **руйнування** — HP корабля / HP кожного модуля + розпад за звʼязністю · **керування** — пряме / лише цілі й пріоритети.

## Цікавинки для курсу
- Екіпаж-носій: черга задач «джерело → споживач» по BFS коридорами; темп = довжина шляху — 🥈.
- Розпад корабля: після знищення клітини — компоненти звʼязності (flood fill) стають окремими тілами — 🥉.
- Двигунний відсік: бонус кожному прилеглому модулю — 📎.
- Пожежа й тепло як клітинний автомат з шансом поширення і згасанням — 🥉.
- Реактор S/M/L: «батарей за рейс» замість потужності — гра з логістикою — 🌱.
- Дахові модулі блокують дуги одне одному — 📎.
- Захоплення уламка через шлюз — зміна власника сутності — 🌱.

## Мапа на каталог
- Є: `multi-cell-size` · `orientation-state` · `impassable-cells` · `cursor-place` + `drag-drop-piece` + `hover-highlight` (редактор) · `hp-damage` (модулі) · `explode-area` (реактори) · `chain-detonation` (вибухи складів/фабрик) · `chase-bfs` (шляхи екіпажу) · `round-currency` (кредити) · `shop-window` · `ai-opponent` · `online-multiplayer` · `save-game` · `game-pause` · `coverage-area` (щит).
- **Нема** → пропозиції карток:
  - `+crew-hauling` «Агенти несуть ресурс від джерела до споживача» · entities/move · 🥈.
  - `+power-battery-delivery` «Енергія як фізичні батареї» · entities/state · 📎.
  - `+connectivity-split` «Обʼєкт розпадається за компонентами звʼязності» · entities/state · 🥉.
  - `+module-targeting` «Ціль — окремий модуль ворога» · entities/combat · 📎.
  - `+fire-spread` «Вогонь поширюється з шансом і гаситься агентами» · entities/state · 📎.
  - `+armor-vs-shield` «Броня (HP за ціну) проти щита (купол, енергія)» · entities/combat · 📎.
  - `+roof-layer-block` «Верхній шар блокує дуги» · entities/legality · 📎.
  - `+derelict-capture` «Захоплення уламка» · entities/interact · 🌱.
  - `+escalating-salary` «Кожен найманий дорожчий» · game-logic/economy · 🌱.
  - `+overclock-mode` «Режим форсажу частини» · entities/state · 🌱.
  - `+thrust-from-layout` «Рух і поворот із розташування двигунів» · entities/move · 🥇.
  - Повтори: `+job-priority-grid`, `+ammo-feed`, `+adjacency-buff`, `+heat-diffusion`, `+blueprint-ghost`.

## Пропозиції до словників
- `+effect:split_ship` — обʼєкт із клітин розпадається на кілька за звʼязністю.
- `+cond:connected_to_core` — клітина звʼязана з рубкою/ядром (який шматок лишається «кораблем»).
- `+trigger:part_destroyed` — знищено модуль складеного обʼєкта (ланцюг вибухів, розпад).
- `+role:crew` — автономний агент усередині обʼєкта гравця; `+role:module` — частина складеного обʼєкта з власним HP.
- `+window:ship-editor`, `+window:crew-roles`, `+window:galaxy-map`.
- `+ui:supply-bars` — смужки енергії/набоїв/екіпажу на модулі; `+ui:firing-arc` — дуга стрільби.
- `+feature:ironman-mode` — один сейв у кампанії (родич `mode-hardcore`).
- `+card:crew-hauling`, `+card:connectivity-split`, `+card:thrust-from-layout`, `+card:roof-layer-block`.

## Джерела
- ⭐ [Steam: Cosmoteer](https://store.steampowered.com/app/799600/Cosmoteer_Starship_Architect_Commander/) — форма корпусу й план, від півдесятка до тисячі змодельованих людей, ролі й пріоритети, модулі окремо цілі й руйнуються, кораблі розпадаються; Career/co-op/PvP/Creative, Workshop; Early Access 24.10.2022.
- [Wikipedia: Cosmoteer](https://en.wikipedia.org/wiki/Cosmoteer) — «tile-based on a two-dimensional grid», екіпаж постачає системи, курс і цілі без наказів окремим членам, Career / Creative, fame.
- [Ultimate Ship Design and Part Guide](https://steamcommunity.com/sharedfiles/filedetails/?id=2866401542) — батареї M = 2 S, L = 3 S; двигунний відсік +50 %; броня проти щитів; рухомі доріжки; двері; дахові гармати; співвідношення фабрик.
- [Bullet Point Basics — Career](https://steamcommunity.com/sharedfiles/filedetails/?id=2880746225) — 1/2/3 батареї за рейс, зарплата зростає, мінімальний корабель, захоплення через шлюз, докупівля ресурсів на станції.
- [Steam News API](https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=799600&count=60&maxlength=1200) — тепло й пожежі 0.30, шанс поширення 40 → 15 %, overclock, ramp-down, склад 20 → 40 на клітину, Ironman.
- [Cosmoteer.net](https://cosmoteer.net/) — офіційний опис і FAQ.
- YouTube: пошук «Cosmoteer gameplay».

## Непевне
- (?) Умова поразки (що вважається знищенням корабля: рубка, екіпаж, усі шматки) і доля шматка без рубки — не знайдено; вікі (wiki.gg) недоступна.
- (?) Пауза в бою, мінікарта, гасіння пожежі «вогнегасником» як предметом чи модулем — з памʼяті.
- (?) Overclock: «більше тепла» — припущення з контексту 0.30.
- (?) Гайд з дизайну писаний для 0.20.x — числа (+50 %, співвідношення фабрик) могли змінитись.
- (?) Ранні версії (стара Cosmoteer до 2022) — Wikipedia згадує лише 11 років розробки.
