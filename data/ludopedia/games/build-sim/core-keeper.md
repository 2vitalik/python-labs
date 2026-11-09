---
title: Core Keeper — сітковий шар (копання, ферма, автоматизація)
slug: core-keeper
aka: [Хранитель Ядра]
family: build-sim
also: [dig-gravity]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: coop
  info: hidden
  random: both
  goal: state
year: 2022
platforms: [PC, PS4, PS5, Xbox, Switch, Switch 2]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Core_Keeper", best: true, note: "огляд: стартова камера з Ядром, копання назовні, біоми, крафт, навички від використання, ферма, конвеєри й роботизовані руки, боси, кооп до 8"}
  - {kind: steam, url: "https://store.steampowered.com/app/1621690/Core_Keeper/", note: "Steam: майнінг, будування бази, ферма й тварини, автоматизація видобутку і плавки, біоми, Титани, кооп 1–8"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Core+Keeper+automation+drill+conveyor", note: "пошук; автоматизація"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Core+Keeper+farming+guide", note: "пошук; ферма"}
stage: v1
coverage: 55
mechanics: [move-8dir, impassable-cells, destructible-blocks, floor-types, cell-transform, cell-click, hover-highlight, item-pickup, inventory, inventory-items, inventory-limit, hp-damage, hunger-clock, respawn, unit-xp-skills, player-camera, minimap-radar, fog-of-war, map-window, dungeon-generation, save-game, save-autosave, online-multiplayer, row-conveyor, coverage-area, +dig-terrain, +dig-wall, +wall-hardness-tier, +ore-vein, +light-radius, +place-wall-floor, +till-soil, +watered-soil, +growth-stages, +seed-drop, +conveyor-belt, +item-arm-transfer, +powered-drill, +wire-power, +logic-gates, +concentric-biomes, +boss-gated-progress]
proposes: ["+trigger:mined", "+cond:tool_tier", "+cond:powered", "+cond:watered", "+effect:mine", "+effect:till", "+effect:water", "+effect:transport", "+role:machine", "+ui:light-radius", "+ui:placement-ghost", "+window:crafting-window", "+window:skill-tree", "+feature:dedicated-server", "+card:powered-drill", "+card:item-arm-transfer", "+card:concentric-biomes"]
author: opus
date: 2026-11-09
---

# Core Keeper — згори прокопуєш тайлову печеру від Ядра назовні, а в тій самій сітці ростиш ферму і кладеш конвеєри з дрелями

## Суть
Гравець прокидається в центральній камері зі сплячим **Ядром** і копає назовні крізь тайлові стіни підземного світу, згенерованого процедурно. Те, що викопав, іде в крафт: інструменти, верстати, стіни й підлога для власної бази. Особливість для корпусу — **один і той самий тайловий світ** є і шахтою (стіни з міцністю, руда), і фермою (зораний ґрунт, полив, ріст), і фабрикою (дрелі, конвеєри, роботизовані руки на тайлах під електрикою). Описано лише сітковий шар; бої з босами — як контекст прогресу.

## Поле і час
- **Вид згори**, квадратна тайлова сітка; кожна клітина — підлога (ґрунт, вода, зораний ґрунт, покладена плитка) **або** стіна (земля, камінь, глина, руда…), що блокує прохід.
- **Світ кільцями навколо Ядра**: внутрішні біоми (земляні печери, Clay Caves, руїни) — далі за Великою стіною (?) — зовнішні (Azeos' Wilderness, Sunken Sea, Desert of Beginnings, Shimmering Frontier); глибше від центру — сильніші вороги й твердіші стіни.
- **Видимість**: темрява, світло від факелів і джерел (`light-radius`); невідкрите — у тумані мапи.
- **Час**: real-time, без дня й ночі (?); культури ростуть за реальним часом.
- Аватар ходить вільно (8 напрямків, плавно), але копання, посадка і будова — по клітинах перед ним (курсор-клітина).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець | player | HP, голод, навички (копання, фермерство…), інвентар | ходить, копає стіну перед собою, ставить блоки, саджає, бʼється |
| Ядро | static | центр світу | мета: «оживити» Ядро, принісши артефакти босів (?); точка відродження |
| Ґрунтова стіна (земля, глина, камінь) | static | міцність, мінімальний тир кайла (?) | удари кайлом знімають міцність; 0 → стає підлогою, падає блок |
| Рудна жила (мідь, олово, залізо, далі рідкісні) | resource | тир, міцність | при копанні дає руду; переплавляється в злитки |
| Валун руди (?) | resource | велика міцність | ціль для автоматичної дрелі |
| Підлога природна | terrain | тип біому | по ній ходять; можна зорати (ґрунт) |
| Вода | terrain | — | непрохідна без мосту; рибалка; джерело поливу |
| Зораний ґрунт | terrain | сухий / политий | приймає насінину; полив прискорює ріст (?) |
| Культура (Heart Berry, Glow Tulip, Bomb Pepper…) | object | стадії росту, тип | росте за часом; зрілу збирають → плоди й насіння |
| Покладена стіна / підлога | static / terrain | матеріал | будова бази; підлога змінює тип клітини |
| Факел, лампа | static | радіус світла | розганяє темряву навколо |
| Генератор електрики | source | потужність | живить дроти |
| Дріт | conduit | — | передає живлення по суміжних клітинах |
| Дриль (Drill) | spawner | напрям, потрібне живлення | ставиться біля рудного валуна/стіни, сам видобуває руду й викидає вперед (?) |
| Конвеєр | terrain | напрям | рухає предмети, що на ньому, клітина за клітиною |
| Роботизована рука | conduit | напрям | бере предмет з клітини/скрині позаду й кладе вперед (скриня, конвеєр, піч) |
| Скриня | container | слоти | зберігає; приймач рук і конвеєрів |
| Верстат, піч | container | рецепти, паливо | крафт і плавка; плавка — за час |
| Логічні елементи (важіль, плита тиску, затримка) (?) | switch | — | вмикають/вимикають живлення ланцюга |
| Ворог біому | enemy | HP, шкода | атакує гравця й будівлі (?) |
| Бос (Glurch, Ghorm, Hive Mother…) | boss | фази, HP | перемога відкриває технології й наступні біоми |
| Ліжко | static | — | точка відродження |

## Правила (КОЛИ → ЯКЩО → ТО)
Копання:
- КОЛИ `input(mine(wall_cell))` → ЯКЩО `custom: «тир кайла ≥ тир стіни»` → ТО `hp(wall, -damage)`; інакше `block` (стіна «занадто тверда»).
- КОЛИ `hp_zero(wall)` → ТО `set_cell(cell, floor)`, `spawn_at(block_item, cell)`; рудна жила — `spawn_at(ore, cell)`.
- КОЛИ `custom: «копання стіни»` → ТО `counter(mining_skill, +xp)`; рівень навички підвищує шкоду кайла (?).
- КОЛИ `enter(player, dark_area)` → ТО `reveal(cells_in_light_radius)` на мапі.

Будування:
- КОЛИ `input(place(wall|floor|object, cell))` → ЯКЩО `free(cell)` and `has(player, item)` → ТО `place`, `take(player, item)`.
- КОЛИ `input(place(bridge, water))` → ТО `set_cell(water, walkable)` (?).

Ферма:
- КОЛИ `input(till(cell))` (мотика) → ЯКЩО `cell(cell, ground)` → ТО `set_cell(cell, tilled)`.
- КОЛИ `input(place(seed, cell))` → ЯКЩО `cell(cell, tilled)` and `free(cell)` → ТО `spawn_at(crop_stage1, cell)`.
- КОЛИ `input(water(cell))` (лійка) → ТО `set_state(cell, watered)`.
- КОЛИ `timer(every)` → ЯКЩО `state(crop, growing)` → ТО `transform(crop_next_stage)`; ЯКЩО `state(cell, watered)` → ТО ріст швидший (?).
- КОЛИ `input(harvest(crop))` → ЯКЩО `state(crop, ripe)` → ТО `give(player, fruit)`; ЯКЩО `prob(p)` → ТО `give(player, seed)`; клітина лишається зораною (?).

Автоматизація:
- КОЛИ `tick` → ЯКЩО `custom: «дриль живлена й перед нею рудний валун»` → ТО `custom: «відбиває руду»`, `spawn_at(ore, cell_in_front)` (?).
- КОЛИ `enter(item, conveyor)` → ТО `move(item, conveyor_dir)` щотіку.
- КОЛИ `tick` → ЯКЩО `occupied(cell_behind_arm, item)` and `free(cell_in_front)` → ТО `move(item, cell_in_front)` (рука переносить; у скриню — `give`).
- КОЛИ `custom: «генератор зʼєднаний дротом з машиною»` → ТО `set_state(machine, powered)`; без живлення — машина стоїть.
- КОЛИ `input(toggle(lever))` → ТО `custom: «ланцюг увімкнено / вимкнено»` (?).

Прогрес і виживання:
- КОЛИ `timer(every)` → ТО `counter(hunger, -1)`; КОЛИ `counter(hunger, ==, 0)` → ТО `custom: «штрафи, втрата HP»` (?).
- КОЛИ `hp_zero(player)` → ТО `respawn(player, bed|core)`; інвентар лишається на місці смерті (?).
- КОЛИ `died(boss)` → ТО `unlock(recipes)`, `give(player, boss_artifact)`; артефакти живлять Ядро (?).
- Мета: оживити Ядро й пройти біоми · Поразки нема (відродження) · Рахунку нема.

## Керування і ввід
- WASD — рух; миша — напрям дії, курсор підсвічує клітину перед гравцем; ЛКМ — копати/бити, ПКМ — використати/поставити предмет з активного слота.
- `inventory-bar` (швидкі слоти 1–0): кайло, мотика, лійка, насіння, блоки, конвеєри — інструмент визначає дію над клітиною.
- Поворот напрямку конвеєра/руки перед поставою (?); геймпад підтримується.

## Вікна, меню, HUD
- `main-menu`: Грати (вибір світу / новий світ з налаштуваннями) · Приєднатись (кооп) · Налаштування · Вихід.
- `character-select` / створення персонажа (зовнішність, стартовий клас (?)).
- `game-screen`: світ згори; HUD — `hp-bar`, `hunger-bar`, `inventory-bar`, `minimap`, `placement-ghost` для блоку, `light-radius`.
- `inventory-window` + екіпірування · `crafting-window` (верстат: рецепти за тирами) · `skill-tree` (навички, що ростуть від дій) · `map-window` (відкрита частина світу, мітки).
- `pause-menu` · `settings-window` (керування, графіка) · `lobby-window` для коопу.
- Переходи: game-screen ⇄ inventory-window / crafting-window / map-window; смерть → відродження без окремого екрана (?).

## Фічі поза полем
- `online-multiplayer` / `mode-coop` до 8 гравців, `dedicated-server`.
- `autosave` світу, кілька світів і персонажів (`save-slots`).
- `seed-input` / налаштування генерації світу (?), режими складності (Hard/Creative) (?).
- Прогресія: тири матеріалів, навички від використання (`xp-level` за діями), відкриття рецептів босами.
- `gamepad-support`, `remap-controls`.

## Варіації й родичі
- Родичі в корпусі: [dome-keeper.md](../dig-gravity/dome-keeper.md) (копання тайлових стін з міцністю й поверненням ресурсу на базу), [stardew-farm.md](stardew-farm.md) (зорати → посіяти → полити → зібрати на сітці), [terraria-liquids.md](terraria-liquids.md) (той самий жанр, але вид збоку з гравітацією), [factorio-belts.md](factorio-belts.md) (конвеєри й маніпулятори — повна версія автоматизації), [forager.md](forager.md), [graveyard-keeper.md](graveyard-keeper.md).
- **Осі варіацій**: вид (згори / збоку з гравітацією) · копання (стіна-тайл з HP / піксельна руйнація) · ферма (ріст за часом / за днями) · автоматизація (немає / дрелі й руки / повна логістика) · структура світу (кільця від центру / шари вглиб / вільна).

## Цікавинки для курсу
- Тайлова мапа «стіна або підлога» + копання з міцністю й тиром інструмента — 🌱.
- Радіус світла від факелів (flood fill з відстанню або коло) і туман мапи — 📎.
- Ферма на тій самій сітці: стан клітини (зорано/полито) + таймер стадій культури — 📎.
- Конвеєри й руки: предмети як сутності на клітинах, порядок оновлення за тік, щоб не «телепортувались» через ланцюжок — 🥉.
- Мережа живлення: компонента звʼязності дротів від генератора (BFS при кожній зміні) — 📎; логічні вентилі з затримкою — 🥈.
- Генерація світу кільцями біомів навколо центру з перешкодою-стіною — 🥉.

## Мапа на каталог
- Є: `move-8dir` · `impassable-cells` · `destructible-blocks` (стіни з HP) · `floor-types` · `cell-transform` (ґрунт → зорано) · `cell-click` / `hover-highlight` (клітина дії) · `item-pickup` · `inventory` / `inventory-items` / `inventory-limit` · `hp-damage` · `hunger-clock` · `respawn` · `unit-xp-skills` (навички від дій) · `player-camera` · `minimap-radar` · `fog-of-war` · `map-window` · `dungeon-generation` · `save-game` / `save-autosave` · `online-multiplayer` · `row-conveyor` (рух предметів конвеєром — лише частково) · `coverage-area` (світло).
- **Нема** → пропозиції карток:
  - `+powered-drill` «Машина на клітині сама видобуває сусідній ресурс, поки живлена» · simulation/automation · 📎.
  - `+item-arm-transfer` «Рука переносить предмет з клітини позаду на клітину попереду» · simulation/automation · 📎 — родич маніпулятора Factorio.
  - `+conveyor-belt` — предмет на клітині рухається в напрямку стрічки (не ряд, а окремі предмети).
  - `+wire-power` / `+logic-gates` — живлення як звʼязність дротів.
  - `+concentric-biomes` «Світ кільцями біомів навколо стартового центру» · generation · 🥉.
  - `+dig-terrain` / `+dig-wall` / `+wall-hardness-tier` / `+ore-vein` — як у Dome Keeper, + мінімальний тир кайла.
  - `+light-radius` · `+place-wall-floor` · `+till-soil` · `+watered-soil` · `+growth-stages` · `+seed-drop` · `+boss-gated-progress`.

## Пропозиції до словників
- `+trigger:mined` — клітину-стіну докопано (HP стіни 0) — точніше за `hp_zero` для тайлів.
- `+cond:tool_tier` — тир інструмента ≥ тир клітини · `+cond:powered` — машина під живленням · `+cond:watered` — клітина полита.
- `+effect:mine` — удар по стіні · `+effect:till` — зорати клітину · `+effect:water` — полити · `+effect:transport` — предмет зсувається машиною (конвеєр/рука).
- `+role:machine` — автомат на клітині зі своєю дією за тік (дриль, рука, піч).
- `+ui:light-radius` · `+ui:placement-ghost`.
- `+window:crafting-window` · `+window:skill-tree`.
- `+feature:dedicated-server`.
- `+card:powered-drill` · `+card:item-arm-transfer` · `+card:concentric-biomes`.

## Джерела
- ⭐ [Wikipedia: Core Keeper](https://en.wikipedia.org/wiki/Core_Keeper) — центральна камера з Ядром, копання назовні, біоми з ворогами й матеріалами, крафт за тирами, навички від використання, ферма/кулінарія/рибалка, конвеєри й механічні руки з проводкою, боси, відродження біля Ядра або ліжка, кооп до 8, дати релізу.
- [Steam: Core Keeper](https://store.steampowered.com/app/1621690/Core_Keeper/) — майнінг і інструменти, база, ферма й тварини, автоматизація видобутку/плавки/зберігання, біоми (Clay Caves, Shimmering Frontier, Sunken Sea, Desert of Beginnings), Титани, кооп 1–8, dedicated server.
- Фан-вікі (fandom 402, atma.gg 403) не відкрились; YouTube — пошукові лінки.

## Непевне
- (?) Поведінка дрелі (ціль — валун руди, вивід уперед), сухий/политий ґрунт і його вплив на ріст, мотика й лійка, логічні елементи — з памʼяті; Wikipedia підтверджує лише «конвеєри, механічні руки, проводка, виробничі пристрої».
- (?) Тири кайла проти стін, внесок навички копання в шкоду, мости через воду — не перевірено.
- (?) Велика стіна між внутрішніми й зовнішніми біомами, розташування біомів кільцями — з памʼяті.
- (?) Артефакти босів як ключ до Ядра, доля інвентаря після смерті, голод — не перевірено.
- (?) Режими складності й налаштування генерації світу — з памʼяті.
