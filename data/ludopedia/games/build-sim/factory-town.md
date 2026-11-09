---
title: Factory Town
slug: factory-town
aka: []
family: build-sim
also: [program-robots]
klass: cursor
axes:
  field: 3d
  time: realtime
  opponent: none
  info: full
  random: setup
  goal: state
year: 2021
platforms: [PC, Mac]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/860890/Factory_Town/", best: true, note: "опис: жолоби з гравітацією, конвеєри, залізниці, труби, сортери й фільтри; ворота й тригери; 8 карт кампанії, пісочниця, Workshop"}
  - {kind: other, url: "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=860890&count=6&maxlength=0&enddate=1632600000", note: "Steam News: «New Low-Tech wooden gadgets!» (2021-08-22) — дерев'яні вагонетки без працівника, повільно вгору, «на відміну від жолобів»; Happiness Overhaul (2021-09)"}
  - {kind: other, url: "https://steamcommunity.com/sharedfiles/filedetails/?id=2023835110", note: "гайд Logistics and Computing (v0.148): усі логістичні й обчислювальні блоки"}
  - {kind: other, url: "https://steamcommunity.com/sharedfiles/filedetails/?id=2697624855", note: "гайд кампанії v1.0: ступені технологій, транспорт за рівнями, жолоби лише вниз"}
  - {kind: other, url: "https://www.player.one/factory-town-update-0168-patch-notes-include-new-rail-cars-general-137141", note: "патч 0.168: вагони, фільтр Loose Bulk, глобальне правило Restrict Minecart Inventory"}
  - {kind: other, url: "https://steamcommunity.com/sharedfiles/filedetails/?id=1912479252", note: "гайд по будинках і магазинах: постачання лише будинкам, зʼєднаним дорогою"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Factory+Town+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [row-conveyor, orientation-state, height-levels, multi-cell-size, cursor-place, hover-highlight, button-toggle, coverage-area, round-currency, sequential-levels, save-game, game-loop, state-as-data, +gravity-chute, +rail-cart-logistics, +item-filter-sort, +splitter-balance, +overflow-gate, +inserter-transfer, +logic-gates, +logic-circuit-wiring, +container-level-sensor, +delay-line, +worker-task-list, +fluid-network, +terrain-sculpt, +road-network-range, +satisfaction-categories, +house-level-xp, +population-ratchet, +town-specialty, +tech-level-by-output, +tech-tree, +blueprint-ghost]
proposes: ["+cond:downhill", "+cond:powered", "+cond:road_connected", "+effect:level_up", "+effect:latch", "+trigger:signal_change", "+role:worker", "+window:research-window", "+window:worker-overview", "+window:logic-block-config", "+ui:signal-link", "+ui:item-filter-panel", "+card:gravity-chute", "+card:worker-task-list", "+card:satisfaction-categories", "+card:population-ratchet"]
author: opus
date: 2026-11-09
---

# Factory Town — фабрика-село на 3D-рельєфі: жолоби котять сипке лише вниз, вагонетки повільно вгору, ворота й логіка розводять потоки

## Суть
Містобудівна логістика: гравець ставить виробничі будівлі на блоковому 3D-рельєфі й веде товари від сировини до їжі, одягу, інструментів, книжок і магічних артефактів, а потім продає їх у ринки села. Спершу все носять **працівники** зі списками задач «взяти тут — віднести туди», далі гравець автоматизує: **жолоби** (сипке котиться під гору безкоштовно), конвеєри, вагонетки й потяги, труби, кораблі, дирижаблі. Незвичне для сімʼї — **рельєф як ресурс логістики** (вниз — даром, вгору — повільно або дорого) і повний набір **логічних блоків** (тумблер, AND/OR/NOT, лічильник, таймер, сенсор), що керують воротами на шляхах. Ворогів і голоду нема — тиск дають цілі кампанії й щастя села.

## Поле і час
- Блокова 3D-сітка рельєфу з висотами; рельєф можна скульптувати; риштування, опори й платформи дають шляхам і жолобам іти над дорогами. Будівлі займають кілька блоків; вагони — по 2 блоки.
- Шари: рельєф (вода, ліс, руда) · шляхи (стежки, дороги, рейки, конвеєри, жолоби, труби) · будівлі · агенти (працівники, вагонетки, потяги, човни, дирижаблі) · логічна мережа (звʼязки блоків поза полем).
- Час — реальний; рух предметів на жолобах залежить від нахилу (слоуп-дані блоків). Предмет, що увійшов у будівлю, «займає» всі її клітини одночасно.
- Карти: 8 кампанійних з цілями, власні/випадкові карти з пресетами (напр. «Flat», «Flat With Desert»), пісочниця.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Працівник (worker) | ally | місткість, список задач, потребує населення | ходить стежками; виконує задачі по черзі: Pick Up / Drop Off / Deliver / Move |
| Віз (wagon), караван | ally | слоти (караван — кілька) | возять дорогами; Packager ×4 місткість |
| Стежка, кам'яна дорога | terrain | швидкість | прискорює агентів; Ctrl — пряма лінія з риштуванням під нею |
| Жолоб (chute) | conduit | фільтр Loose Bulk | котить сипке (руда, кристали, зерно, борошно, добриво) рівно або вниз; вгору — ні |
| Конвеєр (дерев'яний / тканинний / металевий / магічний) | conduit | швидкість за ступенем | везе предмети; іде рампами вгору |
| OmniPipe | conduit | найшвидший | везе будь-що, зокрема вертикально (пізня технологія) |
| Труби: рідина, мана, пара | conduit | вид | рідини й кристали мани на відстань, під землею |
| Дерев'яна вагонетка | object | малий запас (20 → 50) | без працівника; повільно, але **вгору**; правило «Minecarts use Gravity» за замовчуванням вимкнене |
| Потяг: паровоз + Boxcar / Tank Car / Hopper Car | object | 40 предметів / 100 рідини / 100 сипкого; 2 блоки | вантажиться лише на Train Stop; паровоз їсть пальне, Magic Rail — ні |
| Rail Stop / Rail Loader / Rail Unloader | switch | фільтр вагонетки | миттєве завантаження/розвантаження вагонетки |
| Barrier Gate | gate | активна/ні | активна — блокує рух працівників і предметів на шляху/конвеєрі |
| One-Way | terrain | напрям | рух шляхом лише в один бік |
| Sorter | switch | фільтр | зганяє збіжні предмети в будівлю/сусідній конвеєр; ціль повна — **затор** |
| Pusher | switch | фільтр | як Sorter, але при повній цілі пропускає далі |
| Grabber | switch | фільтр | тягне предмети з будівлі на конвеєр (з колодязя — воду) |
| Splitter | switch | Output Ratio на кожен напрям; Overflow: Hold / Bypass | ділить потік між виходами |
| Filter / Blocker | gate | білий / чорний список | пропускає лише це / усе, крім цього |
| Toggle | switch | 1/0 | перемикає вихід; вмикає/вимикає інші блоки, ворота, лампи |
| Bool Function | switch | And · Or · Not · Nand · Nor · Xor | вихід 1/0 з входів |
| Agent Trigger | switch | клітина | 1, коли предмет входить/виходить; тримає 1 до скидання |
| Inventory Sensor | switch | ціль, фільтр | видає кількість предметів у цілі |
| Counter · Number · Math · Delta · Timer · Signal Gate · Set · Pusher-логіки · Lamp | switch | — | лічильник +1 · відображення · порівняння/арифметика · лише зміни · затримка · реле, коли відкрите · передати без зміни стану · змусити повторити вихід · світиться на 1 |
| Виробнича будівля (лісопилка, кузня, кухня, кравець, Mage Tower…) | container | рецепт, ступінь | перетворює входи на виходи; Schools — дослідження |
| Склад: ящик, барн, силос | container | висота входу ≤ 3 | спільний інвентар гравця; силоси піднімають/опускають товари |
| Будинок | container | рівень 1–10, категорії споживання | споживає товари → щастя, монети, XP рівня; рівень +1 = місткість +1 |
| Ринок / магазин (5 типів: Food Market, Tavern, General Store, Apothecary…) | container | радіус доставки | сам постачає будинки, зʼєднані дорогою; ринки одного міста ділять радіус |
| Town Center (колишня Base) | zone | рівень, AoE, спеціальність | обʼєднує будівлі вздовж доріг у «місто»; рівень за Linked House Levels |
| Монети | resource | кольори (жовті…) | з продажу; платять за будівництво й дослідження |
| Мана, ефір, Omnistone | resource | — | магічні ланцюги; Mana Reactor дає Omnistone (фінал кампанії) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ЯКЩО `occupied(chute_cell, item)` and `custom: «наступний блок жолоба не вище за поточний»` → ТО `move(item, chute_dir)`; інакше `block`.
- КОЛИ `enter(item, chute)` → ЯКЩО `not custom: «предмет у категорії Loose Bulk (руда, кристали, зерно, борошно, добриво; не яйця, ефір, мана-кристали)»` → ТО `block`.
- КОЛИ `tick` → ЯКЩО `occupied(conveyor_cell, item)` and `free(next_cell)` → ТО `move(item, conveyor_dir)` (зокрема рампою вгору).
- КОЛИ `tick` → ЯКЩО `custom: «правило Minecarts use Gravity вимкнене»` → ТО `move(wooden_minecart, rail_dir)` повільно, вгору теж; працівник не потрібен.
- КОЛИ `enter(minecart, rail_stop)` → ЯКЩО `same(cargo, rail_stop_filter, kind)` → ТО `give(minecart, cargo)` або `take(minecart, cargo)` миттєво.
- КОЛИ `input(load, minecart)` → ЯКЩО `mode(restrict_minecart_inventory)` → ТО `custom: «лише Loose Bulk»` (нові карти — ON, старі — OFF); фільтр вагонетки важить більше за фільтр потяга.
- КОЛИ `enter(train, train_stop)` → ЯКЩО `custom: «вагон Boxcar / Tank Car / Hopper Car»` → ТО `custom: «вантажиться лише тут»`.
- КОЛИ `enter(item, sorter)` → ЯКЩО `same(item, filter, kind)` → ТО `move(item, target)`; ЯКЩО `not free(target)` → ТО `block` (затор лінії).
- КОЛИ `enter(item, pusher)` → ЯКЩО `same(item, filter, kind)` and `free(target)` → ТО `move(item, target)`; інакше `move(item, conveyor_dir)` далі.
- КОЛИ `tick` → ЯКЩО `has(building, filtered_item)` → ТО `take(building, item)`, `place(item, conveyor)` (Grabber).
- КОЛИ `enter(item, splitter)` → ТО `custom: «вихід за Output Ratio напрямів»`; ЯКЩО `not free(out)` → ТО `custom: «Overflow: Hold — чекати; Bypass — в інший вихід»`.
- КОЛИ `enter(a, filtered_path)` → ЯКЩО `custom: «Filter: item ∉ білий список; Blocker: item ∈ чорний список»` → ТО `block`.
- КОЛИ `enter(worker|item, barrier_gate)` → ЯКЩО `state(barrier_gate, active)` → ТО `block`.
- КОЛИ `enter(a, one_way)` → ЯКЩО `not moving(a, allowed_dir)` → ТО `block`.
- КОЛИ `input(click, toggle)` → ТО `set_state(toggle, flip)`, `set_value(out, 1|0)`.
- КОЛИ `custom: «змінився вхід блока»` → ТО `set_value(bool_out, and|or|not|nand|nor|xor(inputs))`.
- КОЛИ `enter(item, trigger_tile)` або `leave(item, trigger_tile)` → ТО `set_value(agent_trigger, 1)`; тримається, доки Set-блок не скине (`custom: «засувка»`).
- КОЛИ `tick` → ЯКЩО `state(inventory_sensor, active)` → ТО `set_value(sensor, count(target_items))`.
- КОЛИ `custom: «вхід лічильника = 1»` → ТО `counter(counter_block, +1)`.
- КОЛИ `timer(delay)` → ТО `custom: «Timer віддає збережений вхід далі»`; режим repeat — годинник.
- КОЛИ `custom: «вхід Math-блока»` → ТО `set_value(out, compare|arith(input, stored))` (порівняння → 1/0; ділення без дробів).
- КОЛИ `custom: «вхід Delta-блока»` → ЯКЩО `custom: «значення змінилось»` → ТО `custom: «переслати»`; інакше нічого.
- КОЛИ `custom: «вхід Signal Gate»` → ЯКЩО `state(signal_gate, open)` → ТО `custom: «переслати»`.
- КОЛИ `custom: «працівник завершив задачу»` → ТО `custom: «наступна задача зі списку»`; Pick Up без предметів — пропуск; Hold Until Full / Hold Until Empty — чекати; непотрібні предмети в руках — викинути.
- КОЛИ `input(shift_assign, worker, task)` → ТО `custom: «додати задачу в кінець списку, а не замінити»`.
- КОЛИ `tick` → ЯКЩО `custom: «будинок зʼєднаний дорогою з ринком у радіусі міста»` and `has(market, goods)` → ТО `give(house, goods)`.
- КОЛИ `tick` → ЯКЩО `has(house, goods)` → ТО `take(house, goods)`, `custom: «щастя за категорією до межі категорії × рівень дому»`, `counter(house_xp, +item_xp)`, `currency(+coins)`.
- КОЛИ `counter(house_xp, >=, next_level)` → ТО `custom: «рівень дому +1 (до 10), місткість населення +1»`.
- КОЛИ `counter(town_happiness, >=, target)` → ТО `counter(population_level, +1)` — більше будинків; спад щастя рівень не забирає.
- КОЛИ `custom: «будинок зʼєднаний з дорожньою мережею Town Center»` → ТО `custom: «межі міста розширюються навколо будинку»`.
- КОЛИ `custom: «рецепт збігається зі спеціальністю міста»` → ЯКЩО `prob(20 % × рівень Town Center)` (прості; складні — 10 %) → ТО `custom: «подвоєний вихід»`.
- КОЛИ `counter(produced_items, >=, n)` → ТО `unlock(tech_level)` (рахує вироблене, а не збережене; не витрачає).
- КОЛИ `input(research, tech)` → ЯКЩО `has(player, coins)` → ТО `currency(-cost)`, `unlock(tech)`.
- КОЛИ `custom: «виконано всі цілі карти (напр. Base Level 4 на карті 2)»` → ТО `win`.
- Перемога: цілі кампанійної карти · Поразка: нема (без ворогів і голоду) · Рахунок: монети, щастя, рівень населення й технологій.

## Керування і ввід
- Миша: вибір будівлі/шляху з панелі → привид на рельєфі → клік/drag ставить; поворот; Ctrl — пряма лінія з риштуванням.
- Працівнику — клік по джерелу (Pick Up) і цілі (Drop Off/Deliver); Shift — додати задачу до списку; «…» — видалити/переставити задачі.
- Логіка: обрати вихід блока-джерела → ПКМ по цілі (звʼязок); ПКМ сенсора/тригера задає клітину-ціль.
- Інструменти Copy / Paste / Move (зокрема для потягів і груп працівників), скульптинг рельєфу; повна підтримка геймпада.

## Вікна, меню, HUD
- `game-screen`: 3D-поле, панель будівель (`tool-palette` за ступенями), HUD — `coins`, щастя, рівень населення/технологій, `tooltip` будівлі.
- `+window:worker-overview` — панель працівників із фільтром за будівлею; `+window:research-window` (дослідження за монети).
- Панелі будівель: Production (рецепт) · Research (школи) · `+ui:item-filter-panel` (фільтри шляхів, вагонеток) · `+window:logic-block-config` (тип функції, параметри, repeat таймера).
- `main-menu` → `mode-select` (кампанія з 8 карт · власна/випадкова карта · пісочниця) → `match-setup` (пресет карти, біоми, глобальні правила) → `game-screen`.
- `settings-window`, `pause-menu`, `achievements-window` (Steam).

## Фічі поза полем
- `mode-sandbox` (Creative), `levels-sequential` (кампанія з 8 карт із цілями), `custom-rules` (глобальні правила: Minecarts use Gravity, Restrict Minecart Inventory).
- `mod-support` (Steam Workshop: власні предмети), `cloud-save`, `achievements`, `gamepad-support`.
- Прогресія: ступені технологій 1 → 9+ (Normal → Industrial → Natural → Magical → Elemental), дослідження за монети, рівні Town Center і населення.

## Варіації й родичі
- **Factory Town 2** (анонс 2026): острови з океану, ріки, які можна повернути, жителі з домівками, що самі купують у ринках і екіпірують куплене, зиплайни, катапульти, кораблі між гаванями.
- **Factory Town Idle** (демо 2023): idle-гілка з дослідженнями й апгрейдами.
- Корпус: `factorio-belts`, `shapez`, `mindustry` (конвеєри, сортери, оверфлоу) · `minecraft-redstone` (логіка) · `settlers-2` (носії на дорогах) · `anno-1800-service-roads` (радіус ринку вздовж доріг) · `production-line`.
- Осі: **рельєф і транспорт** — плоско (Factorio) / вниз даром, вгору дорожче (Factory Town) / повна 3D-фізика (Minecraft) · **хто везе** — працівник за списком / пасивний шлях / вагон за логікою · **затор при повній цілі** — стоп (Sorter) / обхід (Pusher, Bypass).

## Цікавинки для курсу
- Жолоб: потік лише вниз схилом за картою висот — 📎 (порівняння висот + конвеєр).
- Sorter vs Pusher: одна дія, два режими поведінки при повній цілі — 🌱.
- Splitter з Output Ratio і Overflow Hold/Bypass — 🥉 (балансування потоків).
- Логічні блоки як граф із 1/0 і числами: тумблер, булеві, лічильник, таймер, засувка-тригер, Delta — 🥈.
- Працівник зі списком задач Pick Up / Drop Off і Hold Until Full — 🥉.
- Щастя за 11 категоріями з межею на категорію, що росте з рівнем дому; рівень населення, який не падає — 🥉.
- Місто як звʼязна компонента доріг навколо Town Center (BFS) — 📎.

## Мапа на каталог
- Є: `row-conveyor` (конвеєри) · `orientation-state` (напрям шляхів) · `height-levels` (рельєф) · `multi-cell-size` · `cursor-place` · `hover-highlight` · `button-toggle` (тумблер → ворота) · `coverage-area` (AoE міста, радіус ринку) · `round-currency` · `sequential-levels` · `save-game` · `game-loop` · `state-as-data`.
- **Нема** → пропозиції карток:
  - `+gravity-chute` «Жолоб: предмет котиться лише рівно або вниз» · entities/move · 📎.
  - `+worker-task-list` «Агент виконує список задач взяти/віддати» · entities/move · 🥉.
  - `+satisfaction-categories` «Щастя за категоріями з межами» · game-logic/economy · 🥉.
  - `+population-ratchet` «Поріг населення, що не падає назад» · game-logic/economy · 🌱.
  - `+house-level-xp` «Будинок росте з XP спожитого» · entities/state · 📎.
  - `+town-specialty` «Спеціальність міста: шанс подвоєння за рівнем» · game-logic/economy · 🌱.
  - `+tech-level-by-output` «Рівень технологій за виробленим, не витраченим» · game-logic/economy · 🌱.
  - `+road-network-range` «Радіус дії вздовж дорожньої мережі» · entities/state · 📎.
  - `+rail-cart-logistics` «Вагонетки з фільтрами й зупинками під логікою» · entities/move · 🥉.
  - `+terrain-sculpt` «Скульптинг рельєфу» · levels/editor · 📎.
  - Повтори: `+item-filter-sort`, `+splitter-balance`, `+overflow-gate`, `+inserter-transfer`, `+logic-gates`, `+logic-circuit-wiring`, `+container-level-sensor`, `+delay-line`, `+fluid-network`, `+tech-tree`, `+blueprint-ghost`.

## Пропозиції до словників
- `+cond:downhill` — наступна клітина шляху не вище (жолоби; родичі — водяні канали).
- `+cond:powered` — логічний вхід активний (повтор з `minecraft-redstone`, `core-keeper`).
- `+cond:road_connected` — сутність зʼєднана дорожньою мережею з іншою (будинок ↔ ринок, Anno, Settlers).
- `+effect:level_up` — рівень будівлі +1 за накопиченим лічильником.
- `+effect:latch` — вихід тримає 1, доки не скинуто (Agent Trigger, RS-тригер).
- `+trigger:signal_change` — змінився вхід логічного блока (замість `custom` у правилах логіки).
- `+role:worker` — підконтрольний агент без прямого керування, що виконує задачі (працівник, віз).
- `+window:research-window` (повтор), `+window:worker-overview`, `+window:logic-block-config`.
- `+ui:signal-link` — візуальний звʼязок логічних блоків; `+ui:item-filter-panel` — панель білого/чорного списку.
- `+card:gravity-chute`, `+card:worker-task-list`, `+card:satisfaction-categories`, `+card:population-ratchet`.

## Джерела
- ⭐ [Steam: Factory Town](https://store.steampowered.com/app/860890/Factory_Town/) — жолоби з гравітацією, конвеєри, залізниці, труби, сортери, фільтри, ворота й тригери; кампанія з 8 карт, пісочниця, Workshop; реліз 17.11.2021, Early Access 12.03.2019.
- [Steam News API](https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=860890&count=6&maxlength=0&enddate=1632600000) — «New Low-Tech wooden gadgets!»: вагонетки без працівника, повільно вгору «unlike chutes», запас 20 → 50; Happiness Overhaul: 11 категорій, рівні домів 1–10, Population Levels, Tech Level; Town Centers: AoE уздовж доріг, спеціальності; Multiple commands per-worker.
- [Гайд Logistics and Computing](https://steamcommunity.com/sharedfiles/filedetails/?id=2023835110) — Barrier Gate, Rail Stop, One-Way, Sorter/Pusher/Grabber/Splitter, Filter/Blocker; Toggle, Bool Function, Agent Trigger, Sensor, Counter, Math, Timer, Delta, Signal Gate.
- [Гайд кампанії v1.0](https://steamcommunity.com/sharedfiles/filedetails/?id=2697624855) — жолоби лише вниз, ступені технологій і транспорту, OmniPipe вертикально, цілі кампанії.
- [Патч 0.168 (player.one)](https://www.player.one/factory-town-update-0168-patch-notes-include-new-rail-cars-general-137141) — Boxcar 40, Tank 100, Hopper 100, Loose Bulk, Restrict Minecart Inventory.
- [Гайд по будинках](https://steamcommunity.com/sharedfiles/filedetails/?id=1912479252) — магазини постачають лише будинки на зʼєднаних стежках/риштуваннях.
- YouTube: пошук «Factory Town gameplay».

## Непевне
- (?) Точні швидкості жолобів, конвеєрів, вагонеток і кути рамп — у джерелах нема; коментар до старого гайда каже, що жолоб «працює і вгору» у вертикальній вежі силосів — суперечить основному правилу, ймовірно старша версія.
- (?) Ступені технологій для кожного транспорту — з гайда v1.0; пізніші патчі могли зсунути.
- (?) Логічні блоки описано за гайдом v0.148; у 2024 оновлення змінило логіку вагонеток («nothing works anymore» — коментар).
- (?) Кольори монет, крім жовтих, і їхні ролі не перевірені.
- (?) Повний список 11 категорій задоволення і 5 типів магазинів (відомі Food Market, Tavern, General Store, Apothecary).
- Черга: «вагонетки — повільно вгору» підтверджено лише для дерев'яних вагонеток і правила Minecarts use Gravity = off.
