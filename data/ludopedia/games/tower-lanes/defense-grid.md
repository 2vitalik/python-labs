---
title: "Defense Grid: The Awakening"
slug: defense-grid
aka: [Defense Grid, DG, DGTA]
family: tower-lanes
also: []
klass: cursor
axes:
  field: square
  time: realtime
  opponent: none
  info: partial
  random: none
  goal: survive
year: 2008
platforms: [PC, Xbox 360, Mac]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Defense_Grid:_The_Awakening", best: true, note: "ядра, носії, ядро повзе додому, 10 веж, відсотки, орбітальний лазер, DLC"}
  - {kind: steam, url: "https://store.steampowered.com/app/18500/", note: "10 веж × 3 рівні, 15 ворогів, 20 мап, челенджі, медалі"}
  - {kind: other, url: "https://ayumilove.net/defense-grid/", note: "гайд: кожна вежа (ціни апгрейдів, проти кого), повітряні, щити, стелс, чіти"}
  - {kind: other, url: "https://www.alteredgamer.com/strategy/41948-defense-grid-the-awakening-tower-guide/", note: "гайд по розміщенню всіх 10 веж"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=defense+grid+the+awakening+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [enemy-waves, spawn-schedule, spawn-points, enemy-reached-base, chase-bfs, reachability-check, tower-placement, tower-range, line-of-sight-attack, round-currency, in-round-upgrades, shop-buyback, shop-catalog, projectile-shot, shoot-cooldown, explode-area, temporary-modes, status-effects, hp-damage, speed-per-type, coverage-area, drop-on-death, spawner-entity, height-levels, save-autosave, restart-level, level-select, level-unlock, difficulty-levels, cheat-codes, leaderboard, status-panel, +maze-by-towers, +path-recompute, +flying-ignores-maze, +interest-economy, +aura-buff, +core-carry, +core-drift-home, +stealth-reveal, +shield-layer, +charge-while-idle, +min-range, +global-strike-cooldown, +checkpoint-rewind]
proposes: ["+trigger:path_changed", "+effect:recompute_path", "+effect:sell", "+effect:upgrade", "+effect:interest", "+effect:drop", "+effect:drift_to", "+role:tower", "+role:core", "+ui:range-circle", "+ui:wave-ticker", "+ui:air-path-overlay", "+ui:core-counter", "+feature:checkpoint-rewind", "+feature:challenge-modes", "+feature:medal-tiers"]
author: opus
date: 2026-11-09
---

# Defense Grid: The Awakening — вороги приходять не вбити тебе, а вкрасти ядра і втекти з ними

## Суть
Класичний TD з вежами, що можуть бути лабіринтом, але ціль ворогів інша: дійти до електростанції, **взяти енергоядро і віднести його до виходу**. Убитий носій кидає ядро, і воно саме повільно пливе додому — по дорозі його може підхопити наступний прибулець. Рівень пройдено, якщо після останньої хвилі лишилось хоча б одне ядро. Відмінність від Desktop TD і Fieldrunners: «життя» — фізичні предмети на полі, які рухаються туди й назад, а шлях ворога двофазний (до ядер, потім до виходу).

## Поле і час
- 3D-мапа з дорогами на піднесених доріжках і будівельною сіткою: вежі ставлять лише на спеціальні платформи (квадратні клітини), частина мап має відкриті поля, де вежі формують лабіринт.
- Кілька висот: платформи на різних рівнях; Cannon стріляє через рівні, Gun/Inferno залежать від лінії бачення.
- Real-time з хвилями; є прискорення гри і три рівні зуму; камера вільна.
- Інформація часткова: стелс-вороги невидимі без Command Tower; стрічка-тікер анонсує склад наступної хвилі.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Електростанція | static | N ядер (?) | сховище ядер; прибулець, що дійшов, бере ядро |
| Енергоядро | pickup | — | лежить на станції / везеться носієм / пливе додому |
| Ядро в дорозі | object | повільне | після смерті носія пливе до станції; його можна перехопити |
| Вхід (spawn) | spawner | 1+ на мапу | хвилі виходять звідси |
| Вихід | static | — | носій, що дійшов, забирає ядро назавжди |
| Будівельна платформа | terrain | клітини | лише тут можна ставити вежі |
| Дорога | terrain | — | вороги йдуть по ній найкоротшим шляхом |
| Gun | tower | 3 рівні | швидкі постріли по одній цілі, наземні й повітряні; добре по щитах; постріл можуть закрити інші вежі |
| Inferno | tower | лінія бачення | вогнемет по лінії, сильний по групах, слабкий по щитах |
| Laser | tower | — | шкода + горіння після виходу з радіусу; не бʼє щити й повітря (?) |
| Cannon | tower | мін. дальність | важкий постріл, далеко, через рівні висоти; не бʼє близьких; бʼє і повітряних |
| Concussion | tower | — | вибухи у випадкових точках радіусу, без лінії бачення; проти роїв |
| Missile | tower | лише повітря | ракети по літаючих |
| Tesla | tower | заряд | накопичує заряд, поки нема цілей, тоді вдаряє з великою шкодою |
| Meteor | tower | найбільший радіус | повільний балістичний снаряд по площі, лише наземні |
| Temporal | tower | без атаки | сповільнює наземних у радіусі (½ швидкості) |
| Command | tower | без атаки | показує стелс-ворогів, +% ресурсів за вбивства поруч |
| Орбітальний лазер | custom | перезарядка | удар з неба вбиває всіх у зоні, без ресурсів за них; не на ранніх місіях |
| Звичайний прибулець | enemy | HP | іде до станції, бере ядро, несе до виходу |
| Рій (swarmer) | enemy | багато дрібних | натовп, вигідний для площі |
| Racer | enemy | швидкий | проскакує повільні снаряди |
| Щитоносець | enemy | щит | щит береже групу; спершу знімається щит, потім HP |
| Стелс | enemy | невидимий | без Command Tower — недоступний для веж |
| Літаючий | enemy | повітря | летить окремим повітряним шляхом над вежами |
| Spawner | enemy | портал | дорогою виводить ще прибульців крізь портал |
| Бос | boss | багато HP | окремі босові хвилі (Racer Boss тощо) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(place, tower, cell)` → ЯКЩО `has(player, resources)` and `free(cell)` and `cell(cell, build_platform)` and `path_exists(spawn, power_station)` → ТО `place(player, tower)`, `currency(-cost)`, `custom: «effect recompute_path для наземних»`; інакше `block`.
- КОЛИ `tick` → наземний прибулець `move(a, next_on_path)` до станції, а з ядром — до виходу; літаючий — `custom: «рух окремим повітряним маршрутом»`.
- КОЛИ `reach(alien, power_station)` → ЯКЩО `count(core_at_station, >, 0)` → ТО `pickup(alien, core)` (до 1–3 ядер за типом прибульця) і `custom: «ціль = вихід»`.
- КОЛИ `hp_zero(alien)` → ЯКЩО `has(alien, core)` → ТО `spawn(core_floating)` на місці смерті, `disappear(alien)`, `currency(+salvage)`.
- КОЛИ `tick` → ЯКЩО `state(core, floating)` → ТО `custom: «ядро повільно пливе до станції»`; дісталось — `custom: «ядро знову на станції»`.
- КОЛИ `contact(alien, core_floating)` → ТО `pickup(alien, core)` — перехоплення в дорозі.
- КОЛИ `reach(alien, exit)` → ЯКЩО `has(alien, core)` → ТО `counter(cores, -n)`, `disappear(alien)`.
- КОЛИ `counter(cores, ==, 0)` → ТО `lose`.
- КОЛИ `wave_cleared` → ЯКЩО `custom: «це остання хвиля»` and `counter(cores, >=, 1)` → ТО `win`, медаль за кількістю збережених ядер (?).
- КОЛИ `in_range(tower, alien, r)` → ЯКЩО `line_of_sight(tower, alien)` → ТО `spawn(projectile)` (Gun, Inferno, Laser); Cannon / Meteor / Concussion — без лінії бачення.
- КОЛИ `in_range(cannon, alien, r)` → ЯКЩО `custom: «відстань < мінімальної»` → ТО `block`.
- КОЛИ `contact(projectile, alien)` → ЯКЩО `state(alien, shielded)` → ТО `custom: «шкода йде в щит»`; інакше `damage(n)`.
- КОЛИ `contact(laser_beam, alien)` → ТО `damage(n)`, `set_state(alien, burning, dur)` — горить і після виходу з радіусу.
- КОЛИ `in_range(temporal, alien, r)` → ЯКЩО `not state(alien, flying)` → ТО `speed(alien, ×0.5)`.
- КОЛИ `in_range(command, alien, r)` → ЯКЩО `state(alien, stealth)` → ТО `clear_state(alien, stealth)`; убитий поруч дає `currency(+salvage × 1.25…1.45)`.
- КОЛИ `tick` → ЯКЩО `count(alien_in_range(tesla), ==, 0)` → ТО `counter(tesla_charge, +1)`; ціль зʼявилась → `damage(charge)`, `counter(tesla_charge, =0)` (?).
- КОЛИ `timer(every)` → прибулець-Spawner `spawn(alien)` крізь портал біля себе (?).
- КОЛИ `timer(every)` → ТО `custom: «effect interest: +% від банку; ставка росте з розміром банку»`.
- КОЛИ `input(orbital_laser, area)` → ЯКЩО `custom: «лазер заряджений»` → ТО `explode(area, n)` — усі в зоні гинуть без salvage; `timer(recharge)`.
- КОЛИ `input(upgrade, tower)` → ЯКЩО `has(player, resources)` → ТО `custom: «effect upgrade: рівень 1→2→3, шкода/темп/радіус»`.
- КОЛИ `input(sell, tower)` → ТО `custom: «effect sell: повернути ресурси»`, `disappear(tower)`, `custom: «trigger path_changed»`.
- КОЛИ `input(rewind)` → ТО `custom: «відкат до автоматичного чекпоінта рівня»`.
- Перемога: після останньої хвилі ≥1 ядро · Поразка: усі ядра винесено · Рахунок: медалі (бронза/срібло/золото) й онлайн-таблиця очок.

## Керування і ввід
- Миша (або геймпад на Xbox): вибір вежі з меню → «привид» над платформою з радіусом → клік ставить.
- Клік по вежі — апгрейд / продаж.
- Кнопки: прискорення гри, показ радіусів веж і повітряних маршрутів, зум (3 рівні), відкат до чекпоінта, орбітальний лазер (ціль на мапі).
- Чіт-коди вводяться з клавіатури (`=jeanmarie` вимикає крадіжку ядер тощо); сейв позначається як «cheated», таблиці й досягнення вимикаються.

## Вікна, меню, HUD
- `main-menu`: кампанія → `level-select` (20 мап базової гри + DLC) → вибір режиму (кампанія / челенджі мапи, `mode-select`).
- `game-screen`: мапа 3D, меню веж з цінами, `coins` (ресурси), `+ui:core-counter` (ядра на станції/в дорозі), `wave-counter`, `+ui:wave-ticker` (тікер складу хвилі), `+ui:range-circle`, `+ui:air-path-overlay`, `zoom-control`, `fast-forward`, кнопка лазера з перезарядкою.
- `dialogue-window` — репліки ШІ Fletcher поверх гри (сюжет).
- `pause-menu` → рестарт / відкат до чекпоінта / вихід.
- `end-screen` — медаль, очки, статистика; `leaderboard` (Steam).
- Переходи: main-menu → level-select → game-screen → end-screen → level-select.

## Фічі поза полем
- `levels-sequential` + `level-unlock`: проходження мапи відкриває її челенджі (інші стартові умови й цілі; `+feature:challenge-modes`).
- `+feature:medal-tiers`: бронза за проходження, срібло/золото — за додаткові цілі (ефективність).
- `+feature:checkpoint-rewind`: автоматичні чекпоінти всередині рівня, відкат без рестарту.
- `speed-control`, `leaderboard-online`, `achievements`, чіт-коди (вимикають таблиці).
- DLC: Borderlands, Resurgence (8 мап × кампанія + 4 режими), You Monster (GLaDOS, 8 рівнів + 35 челенджів), Community Levels, Containment.

## Варіації й родичі
- Родичі в корпусі: `desktop-tower-defense` і `fieldrunners` (лабіринт з веж, але ворог «тече» до виходу й коштує життя), `gemcraft` (мана як життя), `dungeon-warfare` (пастки на шляху до серця).
- Наступник — Defense Grid 2 (2014). Ідея «вороги крадуть і несуть» — також у Plants vs. Zombies (зомбі-вкрадач рослин) лише фрагментом.
- **Осі варіацій**: що втрачає гравець — абстрактні життя / фізичні ядра · шлях ворога — один / двофазний (туди й назад) · вбитий носій — ядро зникає / падає / пливе додому · будування — будь-де / лише платформи · атака вежі — по лінії бачення / балістична / площею.

## Цікавинки для курсу
- Ядро як рухомий предмет: стани «на станції / несуть / пливе / винесено», перехоплення в дорозі — 🥈 (машина станів предмета + кілька власників).
- Двофазний шлях прибульця (до станції → до виходу) з перерахунком після кожної посадки — 🥈.
- Лінія бачення по сітці з перешкодами-вежами (Gun, Inferno) проти балістики (Cannon, Meteor) — 🥉.
- Tesla, що копить заряд, поки нема цілей — 📎 (стан + лічильник).
- Відсотки на банк зі ставкою, що росте з банком — 📎 (дилема «будувати зараз чи копити»).
- Чекпоінт-відкат усередині real-time рівня — 🥉 (знімок стану).

## Мапа на каталог
- Є: `enemy-waves` + `spawn-schedule` + `spawn-points` · `enemy-reached-base` ↔ вихід з ядром · `chase-bfs` + `reachability-check` · `tower-placement` + `tower-range` · `line-of-sight-attack` ↔ Gun/Inferno · `round-currency` · `in-round-upgrades` · `shop-buyback` ↔ продаж · `projectile-shot` + `shoot-cooldown` · `explode-area` ↔ Concussion/Meteor/лазер · `temporary-modes` + `status-effects` ↔ сповільнення, горіння · `hp-damage` · `speed-per-type` · `coverage-area` ↔ Command/Temporal · `drop-on-death` ↔ носій кидає ядро · `spawner-entity` ↔ ворог-портал · `height-levels` ↔ рівні платформ · `save-autosave` ↔ чекпоінти · `cheat-codes`.
- **Нема** → пропозиції карток:
  - `+core-carry` «Ворог краде й несе предмет» · entities/interact · 🥉 · слот {capacity}.
  - `+core-drift-home` «Втрачений предмет повертається сам» · entities/move · 🥉 · слоти {speed, can_intercept}.
  - `+stealth-reveal` «Невидимі, доки не виявлені» · entities/state · 📎 · слот {reveal_radius}.
  - `+shield-layer` «Щит поверх HP» · entities/combat · 📎.
  - `+charge-while-idle` «Заряд, поки нема цілі» · entities/combat · 📎.
  - `+min-range` «Мінімальна дальність» · entities/combat · 🌱.
  - `+global-strike-cooldown` «Удар по зоні з перезарядкою» · entities/combat · 📎.
  - `+checkpoint-rewind` «Відкат до чекпоінта» · game-logic/history · 🥉.
  - `+maze-by-towers`, `+path-recompute`, `+flying-ignores-maze`, `+interest-economy`, `+aura-buff` — див. desktop-tower-defense, fieldrunners.

## Пропозиції до словників
- `+trigger:path_changed`, `+effect:recompute_path`, `+effect:sell`, `+effect:upgrade`, `+role:tower`, `+ui:range-circle` — підтвердження з родини.
- `+effect:interest` — нарахувати % від поточної валюти (підтвердження).
- `+effect:drop` — носій кидає предмет на свою клітину (протилежність `pickup`).
- `+effect:drift_to` — предмет сам рухається до точки (ядро → станція).
- `+role:core` — цінність, яку крадуть: стан визначає програш.
- `+ui:wave-ticker` — бігучий рядок про склад наступної хвилі.
- `+ui:air-path-overlay` — показ повітряних маршрутів на мапі.
- `+ui:core-counter` — ядра на місці / в дорозі / втрачені.
- `+feature:checkpoint-rewind`, `+feature:challenge-modes`, `+feature:medal-tiers`.

## Джерела
- ⭐ [Wikipedia: Defense Grid: The Awakening](https://en.wikipedia.org/wiki/Defense_Grid:_The_Awakening) — ядра й носії (1–3), ядро повільно пливе назад і його можна перехопити, 10 веж, лише платформи, продаж змінює шлях, відсотки, орбітальний лазер, тікер, прискорення, 3 зуми, автоматичний чекпоінт, медалі, DLC.
- [Steam](https://store.steampowered.com/app/18500/) — 10 веж × 3 рівні, 15 ворогів, 20 мап, лінія бачення проти балістики, вежі-підсилювачі, челенджі, бронза/срібло/золото.
- [ayumilove: Defense Grid Guide](https://ayumilove.net/defense-grid/) — опис кожної вежі (Gun, Temporal, Laser, Command, Tesla, Missile, Inferno, Concussion, Cannon, Meteor), щити, стелс, Spawner, Racer, чіти.
- [AlteredGamer: tower guide](https://www.alteredgamer.com/strategy/41948-defense-grid-the-awakening-tower-guide/) — розміщення веж, Tesla «не контролюєш, коли стріляє».
- YouTube: пошук «defense grid the awakening gameplay».

## Непевне
- (?) Скільки ядер на станції (у різних мапах різне?), скільки несе кожен тип; чи медаль залежить від кількості збережених ядер.
- (?) Чи заборонено повністю перекрити шлях на відкритих полях і як саме (як у Desktop TD).
- (?) Повний список 15 ворогів (назви: Walker, Swarmer, Racer, Crasher, Dart, Decoy, Bulwark, Juggernaut, Seeker, Manta, Spire, Gargoyle — з памʼяті, не перевірено).
- (?) Laser і щити: гайди розходяться (один — «не бʼє щити», інший — «слабкий по щитах»).
- (?) Точна механіка Tesla (заряд → один удар чи серія); Spawner виводить ворогів періодично чи раз.
- (?) Чи є окремий тип «ворог, що несе ядро швидше/більше» і як працює ціль «пливе додому» через перешкоди.
