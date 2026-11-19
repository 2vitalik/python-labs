---
title: SteamWorld Build
slug: steamworld-build
aka: [SWB]
family: build-sim
also: [dig-gravity, tower-lanes]
klass: cursor
axes:
  field: layers
  time: realtime
  opponent: ai
  info: partial
  random: runtime
  goal: state
year: 2023
platforms: [PC, Switch, PS4, PS5, Xbox One, Xbox Series X/S]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/SteamWorld_Build", best: true, note: "два етапи (місто → шахта), 4 класи жителів за порогами населення, 4 професії в шахті, ракета як ціль, DLC Mechanized"}
  - {kind: fandom, url: "https://steamworld.wiki.gg/wiki/Buildings", note: "wiki.gg: будівлі за класами жителів, дороги Dirt / Paved / Maglev з покриттям Low / Medium / High, шахтна інфраструктура за шарами"}
  - {kind: fandom, url: "https://steamworld.wiki.gg/wiki/SteamWorld_Build", note: "wiki.gg: майлстоуни, ремонт шахти, потяг і предмети, мапи, 4 складності"}
  - {kind: other, url: "https://estnn.com/steamworld-build-dusty-caverns-guide", note: "гайд: ціна ремонту шахти, нестабільність і завали, колона 5×5, радар, по 2 частини ракети на шар, 6 шахтарів на частину"}
  - {kind: other, url: "https://gamingbolt.com/steamworld-build-review-we-all-lift-together", note: "огляд: потреби робітників, потяг з 3 предметами, перекотиполе, вороги другого поверху, черви"}
  - {kind: other, url: "https://thesixthaxis.com/2023/11/27/steamworld-build-review", note: "огляд: усе має мати дорогу до станції, гнізда не знищити, конвеєри й телепорти"}
  - {kind: steam, url: "https://store.steampowered.com/app/2134770/SteamWorld_Build/"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=SteamWorld+Build+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [cursor-place, multi-cell-size, cell-click, hover-highlight, coverage-area, dig-terrain, floor-types, teleport-pair, hp-damage, spawner-entity, enemy-waves, tower-placement, round-currency, shop-catalog, shop-window, collect-quota, minimap-radar, difficulty-levels, level-select, +road-connection-required, +road-tier, +house-evolution, +production-chain, +population-milestone-reward, +worker-assignment, +job-queue, +hauling-jobs, +two-layer-field, +conveyor-belt, +cave-in-support, +monster-nest, +dig-ambush, +extractor-on-vein, +visiting-trader, +building-boost-item, +crew-size-task, +sandbox-mode, +meta-unlocks]
proposes: ["+cond:road_distance", "+trigger:dug", "+effect:sell", "+effect:stabilize", "+ui:weak-spot-overlay", "+window:milestones-window", "+axis:control", "+card:cave-in-support", "+card:monster-nest", "+card:dig-ambush", "+card:extractor-on-vein", "+card:visiting-trader", "+card:building-boost-item", "+card:crew-size-task"]
author: opus
date: 2026-11-19
---

# SteamWorld Build — містечко на поверхні годує шахту під ним, шахта — місто; у глибині — частини ракети для втечі з планети

## Суть
Казуальний містобудівник у світі SteamWorld (The Station, 2023) з **двома етапами**. Спершу гравець будує на поверхні містечко стимботів: дороги до залізничної станції, житло, сервіси й виробничі ланцюжки; закриті потреби дають щастя, нові класи жителів і пороги населення (майлстоуни), що відкривають будівлі. Відремонтувавши стару шахту, гравець позначає стіни під землею, а боти-професіонали (шахтарі, старателі, механіки, охоронці) самі копають, носять руду, ставлять машини й відбивають монстрів. Ядро — **петля двох шарів**: підземні ресурси потрібні наземним ланцюжкам, а більше міста дає більше робітників для шахти; ціль — знайти частини старої технології й запустити ракету.

## Поле і час
- **Шари:** поверхня (місто) + кілька поверхів шахти, звʼязаних шахтним стволом (Mineshaft). Вікі називає шарові будівлі «за шарами»: базовий шар шахти, Dusty Caverns, Marshy Ruins, Crackling Depths; огляд TheSixthAxis рахує «три підземні рівні» (див. «Непевне»).
- Поверх шахти — клітинна сітка скелі: прокопана клітина стає проходом; будівлі шахти мають розміри в клітинах (Workshop і радар — щонайменше 3×3, колона тримає зону 5×5).
- Поверхня — сітка під будівлі й дороги (будівлі N×M, дорога — смуга клітин) (?).
- Real-time: виробництво, доставки, потяг і атаки йдуть таймерами; боти ходять самі.
- Видимість: місто відкрите; у шахті частини ракети знаходить радар, а повзуни вилазять із ще не розкопаних ділянок, тож підземний шар відкритий лише частково (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Дорога Dirt / Paved / Maglev | terrain | покриття Low / Medium / High; ціна 1 $ · 100 $ + Tools · 200 $ + Sheet Metal + Plastics | зʼєднує будівлі; нею йдуть ресурси й задоволення потреб |
| Залізнична станція | static | руїна → ремонт (ранній майлстоун) | корінь дорожньої мережі; сюди періодично приходить потяг |
| Потяг | neutral | період | торгівля ресурсами, продаж надлишку, 3 предмети на вибір |
| Житло Worker / Engineer / Aristobot / Scientist | object | клас мешканців, потреби, щастя | дає населення; із закритими потребами апгрейдиться в наступний клас |
| Сервіс (General Store, Service Shop, Saloon, Surveyor Office, Wash Service Shop…) | object | покриття | закриває потребу житла поруч |
| Виробництво (Forester, Lumbermill, Cactus Farm + поля, Charcoal Kiln, Toolmaker…) | object | входи → вихід; працівники | перетворює ресурси (колоди → дошки); без дороги не працює |
| Склад (Warehouse) | object | кількість одночасних доставок | розвозить товари між будівлями (?) |
| Металеве перекотиполе | pickup | випадкова нагорода | клік → гроші, Tools, Rubies тощо |
| Декор (кактуси, паркани, стіни) | static | — | прикраса; вплив на щастя (?) |
| Шахтний ствол (Abandoned Mineshaft → Mineshaft) | gate | ремонт: 8 Boards, 18 Engineers, 1200 $ | відкриває шахту; через нього ресурси йдуть нагору |
| Памʼятка (Rail Rush, Cinematon…) | static | — | відкривається завершенням своєї мапи |
| Скеля шахти | terrain | — | позначена клітина → шахтар прокопує прохід |
| Жила (Scrap, Ironium…) | resource | — | старателі добувають вручну або механіки ставлять екстрактор |
| Разове родовище (Gold Nuggets, Rubies, Tool Veins) | resource | одна виїмка | вибирається один раз; самородки наймають нових ботів |
| Скриня | container | матеріали, бафи, креслення | відкривається, віддає вміст |
| Частина ракети (Old Tech) | pickup | по 2 набори на шар | радар показує; добувають 6 шахтарів ≈ 1 хв |
| Шахтар | ally | — | копає позначене, прибирає завали; вільний укріплює стіни поруч |
| Старатель | ally | — | добуває жили й гриби (?), носить ресурси до ствола |
| Механік | ally | — | будує й ремонтує машини та ботів |
| Охоронець | ally | — | бʼється з монстрами |
| Мех (DLC Mechanized) | ally | п'ятий тип працівника | (?) |
| Квартали (Miner / Prospector / Mechanic / Guard Quarters) | spawner | місткість; діють лише на своєму поверсі | дають місця ботам професії; розширюються |
| Колона (Pillar) | static | 300 $ + 1 Board | назавжди стабілізує зону 5×5 |
| Слабке місце | zone | нестабільність | без опори → обвал; показується штрихуванням під інструментом колони |
| Завал (debris) | hazard | — | падає: руйнує будівлі в зоні, шкодить ботам; позначений — шахтарі прибирають |
| Workshop + екстрактори (Scrap, Dirty Water, Ironium, Oil, Gas, Vectron Scrap) | object | ≥ 3×3; ціна (Scrap: 1000 $ + 5 Boards + 5 Tools) | машина на жилі добуває сама |
| Міст | terrain | шар Dusty Caverns | дає ходити й будувати над проваллям |
| Speed Vent | terrain | шар Dusty Caverns | пришвидшує ботів, що проходять |
| Конвеєр | terrain | шар Marshy Ruins | везе ресурси від екстракторів до ствола |
| Телепорт | terrain | пара майданчиків, шар Crackling Depths | переносить бота з одного на інший |
| Surveillance Facility + радар | object | ≥ 3×3 | показує частини ракети |
| Armoury: Thumper, Grenade / Flame / Lightning Turret | ally | — | пастки й турелі проти монстрів |
| Гніздо монстрів | spawner | незнищенне | регулярно випускає атаки |
| Повзуни (creeps) | enemy | — | вилазять, коли розкопано певні ділянки |
| Гігантський черв | enemy | — | зʼїдає шахтарів і механіків |
| Будмайданчик ракети | zone | частини ракети | збирає ракету; запуск — фінал |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(place, building)` → ЯКЩО `fits(building, cells)` і `has(colony, cost)` → ТО `place(building)`, `take(colony, cost)`; інакше `block`.
- КОЛИ `tick` → ЯКЩО `not path_exists(building, station)` дорогами → ТО `set_state(building, inactive)` («усе має мати дорогу до станції»).
- КОЛИ `tick` → ЯКЩО `in_range(service, house, coverage)` → ТО `set_state(house, need_met)`; дальність — `custom: «покриття дороги: Low / Medium / High»` (`+cond:road_distance`) (?).
- КОЛИ `tick` → ЯКЩО `has(producer, inputs)` і `custom: «є працівники з житла»` → ТО `take(producer, inputs)`, `give(producer, output)` (колоди → дошки; кактусова вода, вугілля → потреби робітників).
- КОЛИ `tick` → ТО `carry(bot, goods → consumer)` дорогами; склад задає кількість одночасних доставок (?).
- КОЛИ `tick` → ЯКЩО `state(house, all_needs_met)` → ТО `custom: «щастя тримається»`; інакше `custom: «щастя падає»`.
- КОЛИ `input(upgrade, house)` → ЯКЩО `state(house, all_needs_met)` і `has(colony, upgrade_resources)` → ТО `transform(house, next_class_house)` (Worker → Engineer → Aristobot → Scientist).
- КОЛИ `counter(population, >=, milestone)` → ТО `unlock(buildings)`, `unlock(next_class)` (майлстоун).
- КОЛИ `timer(train_period)` → ТО `spawn(train)`, `window(shop-window)`: `custom: «обмін ресурсів і продаж надлишку»` (`+effect:sell`), `choose(3 items)`.
- КОЛИ `input(equip, item, building)` → ЯКЩО `custom: «предмет не стоїть на іншій будівлі»` → ТО `set_state(building, boosted)` (податок сервісу, більше доставок складу, менше працівників).
- КОЛИ `input(click, tumbleweed)` → ТО `disappear`, `custom: «випадкова нагорода: гроші, Tools, Rubies…»`.
- КОЛИ `input(repair, mineshaft)` → ЯКЩО `has(colony, 8 boards + 1200 $)` і `count(engineer, >=, 18)` → ТО `transform(abandoned_mineshaft, mineshaft)`, `unlock(mine)` (числа — з гайду).
- КОЛИ `input(place, quarters)` → ТО `place(quarters)`; квартал діє лише на своєму поверсі.
- КОЛИ `input(hire, quarters)` → ЯКЩО `has(colony, gold_nuggets)` і `custom: «у кварталі є місце»` → ТО `spawn(miner|prospector|mechanic|guard)`.
- КОЛИ `input(mark, wall)` → ТО `mark(wall, dig)`.
- КОЛИ `tick` → ЯКЩО `occupied(marked_wall, dig_mark)` і `count(idle_miner, >, 0)` → ТО `custom: «шахтар іде до позначки»`, `set_cell(wall, floor)`.
- КОЛИ `tick` → ЯКЩО `state(miner, idle)` → ТО `custom: «укріплює стіни в межах 1 клітини»` (`+effect:stabilize`).
- КОЛИ `custom: «розкопано відкриту площу без опори»` (`+trigger:dug`) → ТО `counter(instability, +n)`; `custom: «слабкі клітини видно штрихуванням під інструментом колони»`.
- КОЛИ `counter(instability, >=, limit)` → ТО `spawn_at(debris, weak_cells)`, `custom: «руйнує будівлі в зоні»`, `damage(bot, n)`.
- КОЛИ `input(place, pillar)` → ТО `place(pillar)`, `clear_state(area_5x5, unstable)` назавжди.
- КОЛИ `destroyed(pillar)` → ТО `set_state(area_5x5, unstable)` (?).
- КОЛИ `input(mark, debris)` → ТО `mark(debris, clear)`; шахтар прибирає → `disappear`.
- КОЛИ `contact(prospector, vein)` → ТО `pickup(resource)`, `carry(prospector, resource → mineshaft)`.
- КОЛИ `reach(prospector, mineshaft)` → ТО `counter(resource, +n)` (ресурс іде нагору).
- КОЛИ `input(place, extractor, vein)` → ЯКЩО `custom: «у Workshop ≥ 3×3 є місце»` і `count(mechanic, >, 0)` → ТО `place(extractor)`.
- КОЛИ `timer(n)` → ЯКЩО `occupied(vein, extractor)` → ТО `give(colony, resource)` або `carry(conveyor, resource → mineshaft)`.
- КОЛИ `enter(bot, speed_vent)` → ТО `speed(bot, ×k)`.
- КОЛИ `enter(bot, teleporter)` → ТО `teleport(bot, pair)`.
- КОЛИ `contact(bot, chest)` → ТО `give(colony, materials|buff|blueprint)`.
- КОЛИ `custom: «розкопано певну ділянку»` → ТО `spawn_at(creeps, area)` (засідка).
- КОЛИ `timer(attack_period)` → ТО `spawn_at(enemy, nest)`; `custom: «гніздо незнищенне — тримати оборону»`.
- КОЛИ `in_range(turret|guard, enemy, r)` → ТО `damage(enemy, n)`.
- КОЛИ `hp_zero(enemy)` → ТО `disappear`.
- КОЛИ `contact(worm, miner|mechanic)` → ТО `disappear_b`.
- КОЛИ `hp_zero(bot)` → ТО `set_state(bot, broken)`; механік ремонтує → `clear_state(bot, broken)` (?).
- КОЛИ `input(place, radar)` → ТО `reveal(rocket_parts)` на поверсі.
- КОЛИ `tick` → ЯКЩО `count(miner_at_part, >=, 6)` → ТО `timer(≈1 min)`, `give(colony, rocket_part)`.
- КОЛИ `counter(rocket_parts, ==, all)` → ТО `custom: «зібрати ракету на будмайданчику й запустити»`, `win`.
- Перемога: запуск ракети. · Поразка: явної нема (обвали, черви й атаки лише руйнують і забирають ботів) (?). · Рахунок: нема; прогрес — майлстоуни, населення, частини ракети.

## Керування і ввід
- Курсор: панель будівництва → привид будівлі → клік по клітинах; drag — дорога (?). Клік по житлу/будівлі — її потреби й стан.
- Шахта: інструмент позначення стін «копати», позначення завалів «прибрати», розміщення колон, кварталів, машин; боти виконують самі — керування **непряме**.
- Перемикання шару: місто ↔ поверх шахти.
- Консолі: кнопка, що ставить курсор на найближче допустиме місце екстрактора; колони — ручним скролом курсора.
- Гарячих клавіш нема, окремих швидкостей гри — теж (за оглядом GamingBolt) (?).

## Вікна, меню, HUD
- `main-menu` → вибір мапи (`level-select`: Giddyup Gorge, Highroller Dunes, Grand Gully, Tumbleton… + тематичні мапи) → `difficulty-select` (Casual / Balanced / Difficult / Sandbox) → `game-screen`.
- `game-screen`: місто або поверх шахти; HUD — ресурси й гроші (`status-panel`), населення за класами (?), `tool-palette` будівель за класами, сповіщення про обвали (`toast`).
- `custom-window` майлстоунів (`+window:milestones-window`): поточні пороги населення й що вони відкриють (?).
- `shop-window` потяга: обмін, продаж, 3 предмети за гроші й Rubies; вікно предметів будівлі — що вдягнено (?).
- Оверлей слабких місць під інструментом колони (`+ui:weak-spot-overlay`); підсвітка допустимих клітин екстрактора.
- `confirm-dialog` знесення будівлі (на Difficult без повернення ресурсів) (?).
- Переходи: main-menu → мапа → складність → game-screen; game-screen ↔ шар шахти; запуск ракети → фінал/`end-screen` (?).

## Фічі поза полем
- `difficulty-presets`: Casual (багато ресурсів, слабкі вороги, дешеві будівлі) · Balanced · Difficult (мало ресурсів, більше й сильніші вороги, знесення без повернення) · Sandbox (`mode-sandbox`: необмежені ресурси, без досягнень і унікальних будівель).
- 5 базових мап + тематичні мапи з оновлень; завершення мапи відкриває її памʼятку для інших мап (`unlockables`).
- `achievements`, `cloud-save` (Steam).
- DLC Mechanized (2024): пʼятий тип працівника — Мех.

## Варіації й родичі
- [SteamWorld Dig](../dig-gravity/steamworld-dig.md) — той самий світ і містечко Tumbleton; там копає сам аватар, тут — найняті боти за позначками.
- Покриття сервісів по дорогах і ярус дороги — [Anno 1800](anno-1800-service-roads.md); еволюція житла за потребами — [Caesar III](caesar-3.md), [Pharaoh](pharaoh.md).
- Позначки «копати» + черга робіт + обвали — [Dwarf Fortress](dwarf-fortress-tiles.md); шахта під базою з обороною — [Dome Keeper](../dig-gravity/dome-keeper.md); вертикальні поверхи — [Fallout Shelter](fallout-shelter.md); підземна колонія — [Oxygen Not Included](oxygen-not-included-cells.md); конвеєри й жили — [Core Keeper](core-keeper.md).
- **Осі варіацій:** хто копає — «аватар (SteamWorld Dig) / позначки для агентів (SWB, DF)»; як шар звʼязаний з іншим — «ствол / конвеєр до ствола / телепорт»; покриття сервісу — «радіус / відстань дорогою / ярус дороги»; опора стелі — «нема / стіни поруч + колони 5×5 (SWB) / фізика конструкцій».

## Цікавинки для курсу
- Два шари поля зі спільною економікою: ресурс знизу — вхід виробництва нагорі, населення нагорі — ліміт ботів унизу — 🥈 (два поля, один стан).
- Позначки «копати / прибрати» + вільні агенти беруть найближчу роботу — 🥉 (черга робіт і пошук шляху).
- Нестабільність стелі: клітина далі ніж N від стіни, укріпленої стіни чи колони 5×5 → слабке місце, завал — 🥉 (поле відстаней BFS від опор).
- Еволюція житла: усі потреби в покритті + ресурси → наступний клас — 🥈.
- Гнізда, засідки при розкопуванні, охоронці й турелі — 📎 за кожне.
- Потяг-торговець: 3 предмети, кожен — на одну будівлю — 📎.
- Завдання на бригаду: «частина ракети добувається, коли поруч 6 шахтарів» — 🌱.

## Мапа на каталог
- Є: `cursor-place` + `multi-cell-size` ↔ будівлі на сітці · `cell-click` + `hover-highlight` · `coverage-area` ↔ покриття сервісів · `dig-terrain` ↔ прокопування скелі · `floor-types` ↔ міст, Speed Vent · `teleport-pair` ↔ телепорти Crackling Depths · `hp-damage` ↔ завали й монстри · `spawner-entity` ↔ гнізда й квартали · `enemy-waves` ↔ регулярні атаки · `tower-placement` ↔ турелі Armoury · `round-currency` ↔ гроші · `shop-catalog` + `shop-window` ↔ потяг · `collect-quota` ↔ частини ракети · `minimap-radar` ↔ радар · `difficulty-levels` · `level-select` ↔ мапи.
- **Нема** → пропозиції карток:
  - Повтори: `+road-connection-required`, `+road-tier` (Anno), `+house-evolution`, `+production-chain`, `+population-milestone-reward`, `+worker-assignment` (квартали), `+job-queue` (позначки), `+hauling-jobs` (старателі), `+two-layer-field` {layers: 1 + поверхи, link: ствол}, `+conveyor-belt`, `+sandbox-mode`, `+meta-unlocks` (памʼятки).
  - `+cave-in-support` «Нестабільна стеля: колони й укріплені стіни, інакше обвал» · entities/legality · 🥉 · слоти {pillar_area: 5×5, wall_reach: 1}.
  - `+monster-nest` «Незнищенне гніздо шле атаки» · entities/spawn · 📎 · слот {period}.
  - `+dig-ambush` «Розкопав ділянку — вилізли вороги» · entities/spawn · 🌱.
  - `+extractor-on-vein` «Машина на жилі добуває сама» · game-logic/economy · 📎 · слоти {cost, rate}.
  - `+visiting-trader` «Торговець приходить періодично з обмеженою пропозицією» · game-logic/economy · 📎 · слоти {period, offers: 3}.
  - `+building-boost-item` «Предмет-підсилення на одну будівлю» · entities/state · 🌱.
  - `+crew-size-task` «Завдання виконується, коли поруч N агентів» · game-logic · 🌱 · слот {n: 6}.

## Пропозиції до словників
- `+cond:road_distance` — повтор з Anno 1800: дальність сервісу вздовж доріг, а не по прямій.
- `+trigger:dug(cell)` — клітину розкопано (засідка повзунів, ріст нестабільності).
- `+effect:sell` — повтор з SteamWorld Dig: надлишок ресурсу → гроші (потяг).
- `+effect:stabilize(area)` — зона стає стійкою до обвалу (колона, шахтар біля стіни).
- `+ui:weak-spot-overlay` — штрихування клітин під загрозою обвалу.
- `+window:milestones-window` — список порогів населення з нагородами.
- `+axis:control` — `indirect`: позначки й будівлі, агенти діють самі.
- `+card:cave-in-support`, `+card:monster-nest`, `+card:dig-ambush`, `+card:extractor-on-vein`, `+card:visiting-trader`, `+card:building-boost-item`, `+card:crew-size-task` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: SteamWorld Build](https://en.wikipedia.org/wiki/SteamWorld_Build) — два етапи гри, 4 класи жителів (Workers, Engineers, Aristobots, Scientists) за порогами, 4 професії шахти (шахтарі, старателі, механіки, охоронці), більше Engineers → більше шахтарів, ракета з частин, платформи, DLC Mechanized.
- [wiki.gg: Buildings](https://steamworld.wiki.gg/wiki/Buildings) — будівлі за класами, Engineer Residential потребує сервісів поруч, дороги з покриттям і цінами, шахта: колона, міст, Speed Vent, конвеєр, телепорт за шарами; квартали, Workshop з екстракторами, радар, Armoury з турелями; памʼятки за завершення мап.
- [wiki.gg: SteamWorld Build](https://steamworld.wiki.gg/wiki/SteamWorld_Build) — майлстоуни, ремонт шахти, потяг із предметами, мапи, складності Casual / Balanced / Difficult / Sandbox.
- [ESTNN: Dusty Caverns guide](https://estnn.com/steamworld-build-dusty-caverns-guide) — ремонт шахти (8 Boards, 18 Engineers, 1200 $), нестабільність і завали, колона 5×5, шахтарі укріплюють стіни в межах 1 клітини, Workshop і радар ≥ 3×3, по 2 частини ракети на шар, 6 шахтарів, ціни екстракторів.
- [GamingBolt: review](https://gamingbolt.com/steamworld-build-review-we-all-lift-together) — потреби робітників, потяг із 3 предметами по одному на будівлю, перекотиполе, самородки для найму, вороги другого поверху й черви, Armoury, радар.
- [TheSixthAxis: review](https://thesixthaxis.com/2023/11/27/steamworld-build-review) — дорога до станції, класи за потребами, колони, мости, конвеєри, телепорти, незнищенні гнізда.
- [Steam](https://store.steampowered.com/app/2134770/SteamWorld_Build/) — опис, 4 складності, мапи з оновлень, Steam Cloud.

## Непевне
- (?) Скільки поверхів шахти: вікі дає 4 назви шарів, TheSixthAxis — «три підземні рівні»; можливо, базовий шар рахують окремо.
- (?) Чи покриття сервісу рахується вздовж доріг (як Anno), чи радіусом; вікі каже лише «Low / Medium / High coverage» для типів доріг.
- (?) Розміри будівель на поверхні, drag доріг, вплив декору на щастя, роль складу — не бачив у джерелах.
- (?) Апгрейд житла — дія гравця чи автоматичний; що буває з незадоволеними жителями.
- (?) Що саме роблять Thumper і кожна турель; чи монстри руйнують колони (так каже лише вторинний гайд); чи зламаного бота лагодить механік (ESTNN каже «потрібен механік»).
- (?) Чи нерозкопана шахта схована туманом; гриби як справа старателів; «квартал діє лише на своєму поверсі» (гайд Epic Games Store), штрихування слабких місць (Destructoid) і «колону не ставлять на екстрактор» (GameSkinny) — з пошукового підсумку, самі сторінки віддали 403 або не відкривались.
- (?) Числа (8 Boards, 18 Engineers, 1200 $, 120 Engineers для механіків, 200 для радару) — з одного гайду, можуть залежати від складності.
- (?) Мех з DLC — лише назва типу; поведінку не перевірено.
