---
title: Mindustry — клітинна логістика й оборона
slug: mindustry
family: build-sim
also: [tower-lanes]
klass: hybrid
axes:
  field: square
  time: realtime
  opponent: ai
  info: partial
  random: setup
  goal: survive
year: 2017
platforms: [PC, Mac, Linux, Android, iOS]
links:
  - {kind: fandom, url: "https://mindustrygame.github.io/wiki/", best: true, note: "офіційна вікі: кожен блок зі статами й описом (конвеєри, роутери, сортери, турелі, енергія, ядра)"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Mindustry", note: "огляд, режими, ядра, хвилі, історія версій, GPLv3"}
  - {kind: official, url: "https://mindustrygame.github.io/", note: "офіційний сайт, завантаження"}
  - {kind: steam, url: "https://store.steampowered.com/app/1127400/Mindustry/", note: "Steam: фабрика + TD + RTS"}
  - {kind: other, url: "https://mindustrygame.github.io/wiki/content/blocks/distribution/266-router/", note: "приклад сторінки блока: Router"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=mindustry+gameplay+tutorial", note: "пошук; геймплей і туторіал"}
stage: v1
coverage: 60
mechanics: [row-conveyor, multi-cell-size, orientation-state, impassable-cells, cell-click, drag-drop-piece, hover-highlight, round-currency, enemy-waves, spawn-points, enemy-reached-base, hp-damage, chase-bfs, projectile-shot, shoot-cooldown, player-camera, minimap-radar, save-game, in-game-editor, game-pause, +entity-rotate, +sideload, +underground-link, +splitter-balance, +item-filter-sort, +overflow-gate, +junction-cross, +ore-drill, +ammo-feed, +power-graph, +coverage-area, +unit-factory, +core-deposit, +blueprint-ghost, +fluid-network]
proposes: ["+role:terrain", "+role:resource", "+role:container", "+role:spawner", "+role:ally", "+trigger:tick", "+trigger:enter", "+trigger:in_range", "+trigger:hp_zero", "+trigger:schedule", "+cond:facing", "+cond:free", "+cond:has", "+cond:in_range", "+cond:cell", "+effect:move", "+effect:give", "+effect:take", "+effect:rotate", "+effect:set_state", "+effect:speed", "+effect:spawn_at", "+ui:wave-counter", "+ui:next-wave-preview", "+ui:tool-palette", "+ui:minimap", "+ui:drag-ghost", "+ui:hp-bar", "+window:map-window", "+window:tech-tree", "+feature:mode-sandbox", "+feature:mode-versus", "+feature:mode-coop", "+feature:level-editor", "+feature:mod-support", "+feature:custom-rules", "+card:ammo-feed", "+card:power-graph"]
author: opus
date: 2026-11-02
---

# Mindustry — конвеєр несе мідь від бура до турелі, турель стріляє в хвилю, хвиля йде до ядра

## Суть
Top-down клітинна фабрика з tower defense: з ядра вилітає маленький корабель-будівельник, ставить бури на рудні клітини, тягне конвеєри, сортує предмети роутерами/сортерами, годує ними турелі й заводи юнітів. Хвилі ворогів ідуть шляхами до ядра; програш — коли знищено всі ядра. Тут описано лише **клітинну логістику + оборону** як правила сітки: кожен блок — маленький автомат «приймає предмет з боку → віддає в бік».

## Поле і час
- Квадратна сітка: шар підлоги (камінь, пісок, вода, **руда** — мідь/свинець/пісок/вугілля/титан/скрап) + шар блоків (1×1, 2×2, 3×3…) + вільні юніти й снаряди поверх (`field: square`, юніти рухаються вільно).
- Блоки мають **напрям** (конвеєр, сортер, турель — ні; конвеєр/міст — так) і власну ємність предметів.
- Real-time: предмети їдуть конвеєром зі швидкістю (Conveyor 5 предм./с, Titanium — швидше), бури видають предмет раз на період, хвиля — за таймером зворотного відліку.
- Камера слідує за кораблем гравця, мінікарта; деякі карти з туманом війни (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Ядро (Core: Shard 3×3) | static | HP 1100, ємність 4000 | склад: усе, що в нього заїхало, — валюта будування; знищено всі ядра → поразка; ставиться лише на зону ядра |
| Рудна клітина | resource | тип руди | під буром визначає, що він видобуває |
| Механічний бур (2×2) | spawner | тір, швидкість ~0.36–0.4/с | на руді щоперіоду видає предмет у сусідній блок; вода — ×2.56 |
| Конвеєр | terrain | напрям, 3 предмети, 5/с | несе предмети вперед; приймає ззаду і з боків |
| Розвилка (Junction) | terrain | 6 предм./бік, 13/с | пропускає два потоки навхрест, не змішуючи |
| Роутер | container | 1 предмет | віддає вхідні предмети по черзі в усі 4 боки (і назад теж) |
| Сортер / інверсний сортер | terrain | фільтр-предмет | збіг → прямо; інакше вліво/вправо (інверсний — навпаки) |
| Overflow / Underflow gate | terrain | — | прямо, а вбік — лише коли спереду заблоковано (underflow — навпаки) |
| Міст-конвеєр | terrain | 10 предм., 11/с, дальність ~4 (?) | переносить предмети над клітинами/будівлями до парного мосту |
| Розвантажувач (Unloader) | terrain | фільтр | витягує предмети з сусіднього контейнера/ядра |
| Турель Duo | ally | HP 250, дальність 20, 30 пострілів | приймає мідь/графіт/кремній як набій; вода/кріорідина — швидше; стріляє по ворогу в радіусі |
| Енергетичні турелі (Lancer, Arc) | ally | енергія | стріляють коштом енергомережі, не предметів (?) |
| Генератор (combustion, solar…) | spawner | вихід енергії | дає енергію в мережу (палить предмети / від сонця) |
| Батарея | container | заряд | накопичує надлишок енергії |
| Енергетичний вузол | static | дальність 6, 10 звʼязків | зʼєднує мережу «лазером» з іншими вузлами; живить сусідні блоки |
| Наземна фабрика (3×3) | spawner | 72 енергії/с; Dagger: 10 кремнію + 10 свинцю, 15 с | з предметів і енергії робить юніт; далі — реконструктор апгрейдить |
| Mender / overdrive (?) | static | радіус | лікує / прискорює блоки в зоні |
| Стіни (мідь, титан…) | static | HP | поглинають шкоду, блокують шлях |
| Ворожий юніт (наземний/повітряний/морський) | enemy | HP, зброя | іде до ядра; стріляє по блоках на шляху |
| Точка спавну | spawner | — | місце появи хвиль |
| Корабель гравця (Alpha) | player | — | літає, будує, руйнує, копає руду вручну, носить предмети |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `timer(drill_period)` для бура ЯКЩО `cell(under, ore)` → ТО `give(drill, ore_item)`; швидкість ∝ кількості рудних клітин під буром (?).
- КОЛИ `tick` ЯКЩО `has(block, item) and free(front)` → ТО `move(item, front)` (бур/завод виштовхують у сусідній блок, що приймає; конвеєр — лише вперед).
- КОЛИ `enter(item, conveyor)` збоку → ТО `custom: «вливається в потік»` (sideload); навпроти напрямку — `block`.
- КОЛИ `enter(item, junction)` → ТО `move(item, opposite_side)` (прохід навхрест).
- КОЛИ `enter(item, router)` → ТО `move(item, next_side_round_robin)` — будь-який із 4 боків, що приймає (включно з «назад»).
- КОЛИ `enter(item, sorter[f])` → ЯКЩО `same(item, f)` → ТО `move(item, front)`; інакше `move(item, left|right)`. Інверсний — навпаки.
- КОЛИ `enter(item, overflow_gate)` → ЯКЩО `free(front)` → ТО `move(item, front)`; інакше `move(item, left|right)`. Underflow — дзеркально.
- КОЛИ `enter(item, bridge_in)` → ТО `teleport(item, paired_bridge)` у межах дальності.
- КОЛИ `tick` для розвантажувача ЯКЩО `has(adjacent_container, f)` → ТО `take` звідти, `give` у сусідній конвеєр.
- КОЛИ `enter(item, core)` → ТО `currency(+1, item_type)`; будування `currency(-cost)`.
- КОЛИ `enter(item, turret)` ЯКЩО `same(item, accepted_ammo)` → ТО `counter(ammo, +shots_per_item)`; інакше `block`.
- КОЛИ `in_range(turret, enemy, range)` ЯКЩО `counter(ammo, >, 0)` → ТО `spawn(bullet)`, `counter(ammo, -1)`; кулдаун між пострілами; рідина-охолоджувач → `speed(fire_rate, ×1.4|×1.9)`.
- КОЛИ `tick` в енергомережі → ТО `custom: «сума генерації ↔ споживання по звʼязному графу вузлів і сусідніх блоків»`; дефіцит → блоки працюють повільніше (?) / зупиняються.
- КОЛИ фабрика ЯКЩО `has(factory, recipe_items) and powered` → ТО `timer(build_time)` → `spawn(unit)`.
- КОЛИ `schedule(waves)` / `counter(wave_timer, ==, 0)` → ТО `spawn_at(wave_units, spawn_point)`; хвилі сильнішають.
- КОЛИ `tick` для наземного ворога → ТО `custom: «рух за полем потоку до ядра; шлях шукає слабко захищені місця»`; блок на шляху — атакує його.
- КОЛИ `hp_zero(block)` → ТО `disappear_b`, лишається «привид» для відбудови (?).
- КОЛИ `all_gone(core)` → ТО `lose`.
- Перемога: Survival — вистояти N хвиль (у кампанії — захопити сектор); Attack — знищити ворожі ядра; PvP — ядра суперника.

## Керування і ввід
- WASD/стік — корабель; клік по клітині — поставити обраний блок; R — повернути блок; drag — лінія конвеєрів з автоповоротами.
- ПКМ — розібрати; виділення рамкою — розібрати/скопіювати в схему.
- Вибір блока з категорій меню (Turret, Production, Distribution, Liquid, Power, Defense, Crafting, Units, Effect, Logic).
- Конфіг блока кліком: фільтр сортера/розвантажувача, рецепт фабрики, звʼязок мосту/вузла.
- Кнопка «наступна хвиля зараз» (skip wave) (?); команди юнітам (v6+ RTS).

## Вікна, меню, HUD
- `main-menu`: Play (Campaign / Custom Game / Join Game) · Editor · Settings · Mods · Schematics (?).
- `game-screen`: поле, `tool-palette` категорій блоків, `drag-ghost` блока, `wave-counter` + таймер до хвилі, `next-wave-preview` (склад хвилі) (?), ресурси ядра (`coins`-подібний список), `minimap`, `hp-bar` блоків.
- `map-window` планети з секторами (кампанія); `custom-window` «Tech tree» — дослідження блоків за ресурси.
- `pause-menu`, `settings-window`, `end-screen` (сектор втрачено/захоплено), `level-select` (Custom Game: вибір мапи + правила).
- Вікно схем (бібліотека креслень) — `custom-window`.
- Переходи: main-menu → карта планети → сектор (`game-screen`) → (ядро втрачено) end-screen → карта.

## Фічі поза полем
- `mode-sandbox`, `mode-versus` (PvP), `mode-coop`, режими Survival/Attack; `custom-rules` — правила гри налаштовуються (швидкість хвиль, ресурси, шкода).
- `level-editor` (вбудований), `mod-support` (відкритий код GPLv3, Workshop), `export-import` схем рядком (?).
- `meta-progression` — дерево технологій кампанії; сектори експортують ресурси один одному.
- `save-slots`, `autosave`, `online-multiplayer` / кросплатформа.
- Логічні процесори — асемблероподібна мова для керування блоками (за межами цього опису).

## Варіації й родичі
- Factorio (`factorio-belts` у корпусі): конвеєр із двома доріжками й маніпулятори; Mindustry — однодоріжковий конвеєр і блоки, що **самі** віддають у сусідів, без маніпуляторів.
- Shapez — та сама логістика без ворогів; класичний TD (`tower-lanes`) — оборона без логістики.
- Дві «планети» = два набори правил: Serpulo (класика) і Erekir (інші блоки, канали, туман) (?).
- Осі варіацій: **розподіл** — round-robin роутер / фільтр-сортер / пріоритет-overflow; **живлення турелі** — предмети / енергія / рідина; **перетин потоків** — розвилка / міст / тунель.

## Цікавинки для курсу
- Роутер, сортер, overflow, розвилка — 4 блоки-автомати «вхід → вихід» на одній сітці; студент збирає логістику з правил по 2 рядки — 🥉 за набір.
- Бур на руді → конвеєр → ядро як лічильник валюти: мінімальний «конвеєр предметів» у консолі — 📎.
- Турель, що стріляє лише з набоїв, які їй привіз конвеєр: звʼязок економіки й оборони — 🥉.
- Енергомережа як звʼязний граф (вузли + сусідні блоки), баланс генерації/споживання — 🥈.
- Хвилі, що йдуть полем потоку (BFS від ядра) і атакують блоки на шляху — 🥇: flow field + перерахунок, коли гравець ставить стіну.
- Міст-конвеєр як «телепорт предмета» в межах N — 📎.

## Мапа на каталог
- Є: `row-conveyor` (потік предметів конвеєром) · `multi-cell-size` (бури 2×2, ядро 3×3) · `orientation-state` (напрям конвеєра/мосту) · `impassable-cells` · `cell-click` + `drag-drop-piece` + `hover-highlight` · `round-currency` (ресурси ядра) · `enemy-waves` + `spawn-points` · `enemy-reached-base` (ядро) · `hp-damage` · `chase-bfs` (шлях до ядра) · `projectile-shot` + `shoot-cooldown` (турелі) · `player-camera` + `minimap-radar` · `save-game` · `in-game-editor` · `game-pause`.
- **Нема** → пропозиції карток:
  - `+entity-rotate`, `+sideload`, `+underground-link` (міст), `+splitter-balance` (роутер), `+blueprint-ghost` (схеми), `+fluid-network` (рідини), `+coverage-area` (радіус турелі, вузла, mender) — ті самі, що в Factorio/Stardew.
  - `+item-filter-sort` «Сортер: фільтр прямо, решта вбік» · entities/interact · 📎 · слот {inverted}.
  - `+overflow-gate` «Вбік лише при заторі спереду» · entities/interact · 📎.
  - `+junction-cross` «Перехрестя двох потоків без змішування» · entities/move · 🌱.
  - `+ore-drill` «Бур на рудній клітині видає предмет» · entities/spawn · 📎 · слоти {period, tier}.
  - `+ammo-feed` «Турель живиться предметами з конвеєра» · entities/combat · 🥉 · слоти {ammo_types, shots_per_item}.
  - `+power-graph` «Енергомережа як граф із балансом» · entities/interact · 🥈.
  - `+unit-factory` «Фабрика юнітів з рецептом» · entities/spawn · 🥉.
  - `+core-deposit` «Склад-ядро: предмет у ядро = валюта» · game-logic/economy · 🌱.

## Пропозиції до словників
- `+role:terrain` (конвеєр, сортер — по них їдуть предмети), `+role:resource` (руда), `+role:container` (роутер, батарея), `+role:spawner` (бур, фабрика, точка спавну), `+role:ally` (турелі, свої юніти).
- `+trigger:tick`, `+trigger:enter` (предмет увійшов у блок), `+trigger:in_range` (турель), `+trigger:hp_zero`, `+trigger:schedule` (хвилі).
- `+cond:facing`, `+cond:free` (спереду вільно — overflow), `+cond:has`, `+cond:in_range`, `+cond:cell` (руда під буром).
- `+effect:move`, `+effect:give`/`+effect:take`, `+effect:rotate`, `+effect:set_state` (powered), `+effect:speed` (охолодження, дефіцит енергії), `+effect:spawn_at`.
- `+ui:wave-counter`, `+ui:next-wave-preview`, `+ui:tool-palette`, `+ui:minimap`, `+ui:drag-ghost`, `+ui:hp-bar`.
- `+window:map-window` (планета), `+window:tech-tree` — дерево досліджень (нове).
- `+feature:mode-sandbox`, `+feature:mode-versus`, `+feature:mode-coop`, `+feature:level-editor`, `+feature:mod-support`, `+feature:custom-rules`.
- `+card:ammo-feed`, `+card:power-graph`.

## Джерела
- ⭐ [Mindustry Wiki](https://mindustrygame.github.io/wiki/) — довідник блоків: Conveyor (5/с, 3 предмети), Junction, Router («у всі 4 боки порівну»), Sorter, Overflow Gate, Bridge, Unloader, Duo (набої, охолодження), Power Node (6 клітин, 10 звʼязків), Mechanical Drill, Ground Factory, Core: Shard.
- [Wikipedia](https://en.wikipedia.org/wiki/Mindustry) — режими, ядра й зони ядер, хвилі шукають слабкі місця, версії, GPLv3.
- [Офіційний сайт](https://mindustrygame.github.io/) — завантаження, безкоштовна збірка.
- [Steam](https://store.steampowered.com/app/1127400/Mindustry/) — опис «factory + TD + RTS», кампанії Serpulo/Erekir.
- YouTube: пошук «mindustry gameplay tutorial».

## Непевне
- (?) Дальність мосту-конвеєра (~4 клітини) — на сторінці блока не вказано.
- (?) Як швидкість бура залежить від кількості рудних клітин під ним — вікі не пояснює; з памʼяті — пропорційно.
- (?) Поведінка при дефіциті енергії (сповільнення пропорційно «задоволенню» vs зупинка) — з памʼяті.
- (?) Туман війни, «привиди» знищених блоків для відбудови, кнопка skip wave, превʼю складу хвилі — з памʼяті, залежать від версії.
- (?) Ворог атакує блоки на шляху — наземні юніти так, повітряні цілять інакше; деталі ШІ не перевірено.
