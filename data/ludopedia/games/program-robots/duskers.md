---
title: Duskers
slug: duskers
aka: []
family: program-robots
also: [roguelike]
klass: figure
axes:
  field: graph
  time: realtime
  opponent: ai
  info: hidden
  random: both
  goal: survive
year: 2016
platforms: [PC, Mac, Linux]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Duskers", best: true, note: "Misfits Attic, 2016: метагра, абордаж, до 4 дронів, команди в консолі, знос, скрап і паливо"}
  - {kind: fandom, url: "https://namu.moe/w/Duskers", note: "корейська фан-вікі (v1.205): повний список команд, апгрейдів дронів і корабля, ворогів, дверей і живлення"}
  - {kind: other, url: "https://netizenry.codeberg.page/content/game_journalism/Duskers_Tips-ALIASES.html", note: "аліаси команд: navigate, generator, motion, close all, gather all, tow"}
  - {kind: other, url: "https://docs.google.com/document/d/1L9FUTiiekhGaKNmhSDmTgDoDifHbXjnT5z1Hw3yQ7BQ/pub", note: "release notes (бачив у пошуку, не відкривав)"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=Duskers", note: "пошук у Steam"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=duskers+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [console-render, keyboard-controls, fog-of-war, minimap-radar, key-and-door, button-toggle, teleport, hp-damage, permadeath, round-currency, shop-window, map-window, dungeon-generation, spawner-entity, chase-player, environment-death, explode-area, message-log, status-panel, stats-window, party-switch, +typed-command-console, +command-alias-macro, +room-graph-doors, +power-routing, +component-wear-failure, +lure-enemy, +motion-sensor-adjacent, +tow-disabled-unit, +module-swap, +ship-age-danger, +fuel-two-tier, +meta-keep-logs]
proposes: ["+window:command-console", "+window:ship-schematic", "+window:galaxy-map", "+ui:drone-camera-feeds", "+ui:room-flag", "+feature:command-alias", "+cond:powered(cell)", "+cond:docked", "+effect:wear(a)", "+effect:tow(a, b)", "+effect:lure(a, where)", "+trigger:motion(room)", "+axis:control"]
author: opus
date: 2026-11-09
---

# Duskers — веди до чотирьох дронів крізь темні кімнати покинутого корабля, набираючи команди в консолі

## Суть
Корабель гравця стикується з покинутою станцією; дрони заходять через шлюз і досліджують граф кімнат, зʼєднаних дверима. Керувати можна напряму (клавіші, по одному дрону) або — головне — командами в консолі: `navigate 1 2 r5`, `open d3`, `close all`, `gather all`, і зшивати їх у власні аліаси-макроси. Ворогів не бачиш напряму: їх виявляють сенсорами руху, заманюють і замикають дверима, вентилюють у космос. Дрони й модулі зношуються; коли всі дрони зламані — забіг завершено, лишаються лише статистика й прочитані логи.

## Поле і час
- Поле — **граф кімнат**: кімнати (r1 — власний шлюз), двері між ними (d1…), шлюзи (a1…); кожна станція генерується процедурно.
- Камера: схематична мапа (план кімнат і дверей, відкривається скануванням) + відеопотоки з дронів з шумом і глюками.
- Час `realtime`: дрони рухаються й діють неперервно; вороги діють паралельно.
- Метарівень: галактики → системи → покинуті кораблі; перельоти коштують паливо.
- Туман: невідомі кімнати не показують ні вмісту, ні ворогів; `motion` бачить лише рух у своїй і сусідніх кімнатах.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Дрон 1–4 | player | HP, знос, слоти модулів (основні + вторинні з зарядами), сигнал | виконує команди; поломка → лежить, його можна відбуксирувати або розібрати `swap` |
| Кімната | zone | номер, просканована?, радіація, вакуум | вузол графа; може мати вентиляцію, термінал, вхід живлення, скрап |
| Двері | gate | відкриті/закриті; живлені (зелені) / без живлення (сірі) / зламані (червоні) | `open`/`close`; без живлення відкриває лише `pry`; не закриваються, якщо в проході тіло/дрон |
| Шлюз (airlock) | gate | пристиковано? | вхід/вихід; відкрити шлюз без стикування — з підтвердженням |
| Вхід живлення (power inlet) | switch | 1–5 кімнат на генератор | дрон з `generator` живить привʼязані кімнати й двері |
| Термінал (interface) | switch | — | `interface` → `defense`, `shipscan`, `survey`, логи екіпажу |
| Турель станції | hazard | увімк./вимк. | стріляє по всіх, включно з дронами; керується з термінала |
| Вентиляція | spawner | — | породжує рої |
| Скрап | resource | — | `gather` збирає; валюта ремонту й покупок |
| Паливна труба | resource | обʼєм бака | `gather` дає паливо |
| Модуль-апгрейд на станції | pickup | тип | підібрати й поставити на дрон чи корабель |
| Жнець (reaper) | enemy | — | кидається, щойно бачить дрон; швидко вбиває |
| Рій (swarm) | enemy | — | виходить з вентиляції; міна вбиває з одного удару |
| Слиз (slime) | enemy | — | нерухомий — `motion` його не бачить; відштовхується `sonic` |
| Охоронний бот | enemy | — | атакує сенсори; турель і міна ефективні |
| «Пси» та інші організми | enemy | — | реагують на `sonic` |
| Радіація / вакуум | hazard | рівень | радіація шкодить; вакуум висмоктує дронів і ворогів з кімнати |
| Корабель гравця | container | паливо (два типи), скрап, модулі корабля | метагра: ремонт, переліт, апгрейди |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(navigate n… r)` → ЯКЩО `path_exists(drone, room)` → ТО `custom: «дрони йдуть до кімнати через відкриті двері»`; кілька номерів дронів — усі до останнього вказаного місця.
- КОЛИ `input(open d)` → ЯКЩО `custom: «двері живлені й цілі»` → ТО `set_state(door, open)`; інакше `block`, потрібен `pry`.
- КОЛИ `input(close d)` → ЯКЩО `occupied(door, drone|body)` → ТО `block`; інакше `set_state(door, closed)` — ворог за дверима замкнений.
- КОЛИ `input(generator)` → ЯКЩО `has(drone, generator)` і `cell(drone, power_inlet)` → ТО `custom: «живлення кімнат і дверей, привʼязаних до входу»`.
- КОЛИ `input(gather [all])` → ЯКЩО `has(drone, gather)` → ТО `pickup(scrap)` / паливо з труби, `currency(+n)`.
- КОЛИ `input(motion)` → ЯКЩО `has(drone, motion)` → ТО `custom: «показати рух у своїй і сусідніх кімнатах»`, `counter(motion_charges, -1)`; слизу не видно, тип ворога не визначено.
- КОЛИ `input(scan)` → ЯКЩО `has(drone, scan)` → ТО `reveal(room)` разом з прихованим скрапом.
- КОЛИ `input(tow)` → ЯКЩО `has(drone, tow)` і `state(other, disabled)` → ТО `carry(drone, other)`; розбитий дрон тягнути не можна — лише `swap` модулів.
- КОЛИ `input(lure)` → ТО `custom: «вороги йдуть на звук приблизно хвилину»`.
- КОЛИ `input(mine)` → ТО `place(drone, mine)`; КОЛИ `in_range(enemy, mine, room)` → ТО `explode(room)`: рій і бот гинуть з одного удару, жнецю треба два.
- КОЛИ `input(trap)` → ТО `place(drone, trap)`; детонація вручну → `explode(room)`, шкода всім, дронам теж (щит блокує).
- КОЛИ `input(sonic)` → ЯКЩО `custom: «дрон стоїть»` → ТО `custom: «органічні вороги тікають»`.
- КОЛИ `input(turret)` → ЯКЩО `custom: «дрон стоїть і сигнал цілий»` → ТО `damage(enemy_ahead)`.
- КОЛИ `input(stun)` → ТО `stun(enemies_near)`, `stun(drones_near)`.
- КОЛИ `input(stealth)` → ТО `set_state(drone, stealth, dur)`; більшість дій знімає стан; несумісно зі щитом.
- КОЛИ `input(teleport room)` → ЯКЩО `custom: «кімната відома»` → ТО `teleport(drone, room)`, `timer(cooldown)`.
- КОЛИ `contact(enemy, drone)` → ТО `damage(drone)`; `hp_zero(drone)` → `set_state(drone, disabled)`.
- КОЛИ `input(cmd)` → ЯКЩО `custom: «модуль зношений»` → ТО `custom: «шанс відмови модуля»` (`wear`).
- КОЛИ `timer(every)` → ТО `custom: «сигнал дрона деградує — глюки камери»`; `degauss` очищає картинку.
- КОЛИ `input(interface)` + `defense` → ТО `set_state(station_turrets, toggled)`.
- КОЛИ `input(cannon room)` (корабельна гармата) → ТО `custom: «кімната відкривається в космос»` — вакуум висмоктує всіх.
- КОЛИ `input(commandeer)` → ЯКЩО `custom: «усі кімнати проскановано, ворогів нема, радіація < 50 %, нема вакууму, не карантин»` → ТО `custom: «захопити корабель»`.
- КОЛИ `input(exit)` → ТО `custom: «відстикуватись»`; дрони, що лишились на станції, втрачені.
- КОЛИ `all_gone(working_drone)` → ТО `game_over`, `custom: «статистика й логи екіпажу переходять у новий забіг»`.
- Ризик станції: вік у днях (< 200 стабільно … 400+ фатально) → більше ворогів, радіації й поломок.
- Перемога: нема фінальної — виживати й розгадувати, що сталося з людством · Поразка: усі дрони зламані або скінчились ресурси · Рахунок: статистика забігу.

## Керування і ввід
- **Консоль** — основний ввід: команда + аргументи (`navigate 1 2 r5`, `open d3`, `close all`, `gather all`, `tow`, `generator`, `motion`, `degauss`, `info`, `status`, `time`, `flag r4`, `dock a2`, `destruct 2 10`); суфікс `all` — на всіх дронів.
- `alias` — власні макроси, ланцюжки через `;` з параметрами (`fetch`, `power`, `pop` = `open d; close d`).
- Пряме керування: вибір дрона й рух клавішами з камерою від першої особи дрона.
- Скорочення: `n` (navigate), `i` (info), `p` (pickup), `e` (exit).

## Вікна, меню, HUD
- `game-screen`: `ship-schematic` (план кімнат/дверей, позначки дронів, підсвічені `flag`-кімнати), `drone-camera-feeds` (до 4 відеопотоків), `command-console` з історією.
- HUD: `hp-bar` дронів, слоти модулів з зарядами, `fog-overlay` непросканованого, кольори дверей (живлення/зламано).
- `galaxy-map` (`map-window`): системи, покинуті кораблі з віком і небезпекою, паливо на переліт, зоряні брами.
- `custom-window` корабля: ремонт/переставляння модулів, `shop-window` торговельного поста.
- `log-window` — прочитані логи екіпажу; `stats-window` — статистика між забігами.
- Переходи: галактика → вибір корабля → стикування → абордаж → вихід → галактика.

## Фічі поза полем
- `command-alias` — макроси користувача (баг: >30–40 аліасів частина ігнорується).
- `meta-progression` у вигляді статистики й логів; сам забіг — `permadeath`.
- Процедурні станції; знос і ремонт за скрап; два палива (у системі / між системами); зоряні брами.
- Модулі корабля: Quarantine Bypass, Long Range Scanner, Remote/Reroute Power, Ship Surveyor, Transporter, Cannon, Collector, Decontaminate, Overload.

## Варіації й родичі
- Quadrilateral Cowboy (Blendo, 2016) — команди в консолі для хакерських пристроїв, але 3D-рівні (поза корпусом).
- [Untrusted](untrusted.md) — текст як ввід; [Screeps](screeps.md) і [Bot Arenas](bot-arenas.md) — програма замість прямого керування.
- Роглайки з графом кімнат і туманом (FTL — схожий метарівень корабля й галактики).
- Осі варіацій: **ввід** (пряме / консоль / макроси); **видимість** (камера дрона / план / сенсор руху); **оборона** (двері / пастки / вакуум); **ресурс** (скрап / паливо / знос).

## Цікавинки для курсу
- Парсер команд із суфіксом `all`, скороченнями і аліасами-макросами з параметрами — 🥉.
- Граф кімнат з дверима, живленням від входів і станами «живлені / без живлення / зламані» — 🥈.
- Ворог, якого видно лише сенсором руху в сусідніх кімнатах; заманювання й замикання дверима — 🥈.
- Знос модулів зі шансом відмови й ремонт за ресурс — 📎.
- Процедурна станція з віком-небезпекою (більше ворогів і радіації) — 🥇.
- Буксирування зламаного дрона й `swap` модулів — 📎.

## Мапа на каталог
- Є: `console-render` ↔ консоль; `keyboard-controls`; `fog-of-war` ↔ непросканувані кімнати; `minimap-radar` ↔ план; `key-and-door`/`button-toggle` ↔ двері й термінали; `teleport`; `hp-damage`; `permadeath`; `round-currency` ↔ скрап; `shop-window`; `map-window` ↔ галактика; `dungeon-generation` ↔ процедурні станції; `spawner-entity` ↔ вентиляція; `chase-player` ↔ жнець; `environment-death` ↔ вакуум/радіація; `explode-area` ↔ міна/пастка; `message-log`; `status-panel`; `stats-window`; `party-switch` ↔ вибір дрона.
- **Нема** → пропозиції карток:
  - `+typed-command-console` «Керування командами з аргументами в консолі» · interface/input · 🥉.
  - `+command-alias-macro` «Аліаси-макроси з параметрами» · interface/input · 🥉.
  - `+room-graph-doors` «Поле-граф кімнат і дверей» · entities/legality · 🥈.
  - `+power-routing` «Живлення кімнат і дверей від входу» · entities/interact · 🥈.
  - `+component-wear-failure` «Знос модуля → шанс відмови» · entities/state · 📎.
  - `+lure-enemy` «Приманка змінює ціль ворога» · entities/move · 📎.
  - `+motion-sensor-adjacent` «Сенсор руху в сусідніх вузлах» · interface/render · 📎.
  - `+tow-disabled-unit` «Буксирування непрацюючого юніта» · entities/move · 📎.
  - `+module-swap` «Переставляння модулів між юнітами» · entities/state · 🥉.
  - `+ship-age-danger` «Небезпека рівня за параметром генерації» · levels/generation · 📎.
  - `+fuel-two-tier` «Два палива: ближнє і дальнє» · game-logic/economy · 📎.
  - `+meta-keep-logs` «Між забігами лишаються лише знання/логи» · levels/progression · 🌱.

## Пропозиції до словників
- `+window:command-console` — консоль вводу команд з історією (Duskers, Quadrilateral Cowboy).
- `+window:ship-schematic` — план кімнат і дверей як основне поле.
- `+window:galaxy-map` — метамапа перельотів (якщо не досить `map-window`).
- `+ui:drone-camera-feeds` — кілька відеопотоків від юнітів.
- `+ui:room-flag` — позначка кімнати кольором (`flag r#`).
- `+feature:command-alias` — макроси з команд.
- `+cond:powered(cell)` — двері/кімната живлені.
- `+cond:docked` — корабель пристиковано (для відкриття шлюзу).
- `+effect:wear(a)` — знос модуля з ростом шансу відмови.
- `+effect:tow(a, b)` — буксирувати непрацюючого юніта (сусід 🔥 `carry`).
- `+effect:lure(a, where)` — приманити ворога.
- `+trigger:motion(room)` — сенсор зафіксував рух.
- `+axis:control` — значення `typed-command`.

## Джерела
- ⭐ [Wikipedia: Duskers](https://en.wikipedia.org/wiki/Duskers) — метагра й абордаж, до 4 дронів, команди (`Nav 1 R2`), знос, скрап, паливо, ресет зі збереженням статистики й логів.
- [namu.moe: Duskers](https://namu.moe/w/Duskers) — команди (`degauss`, `destruct`, `flag`, `swap`, `commandeer`, `alias`…), основні/вторинні модулі, модулі корабля, вороги, двері, живлення, вік станцій, два палива.
- [Duskers Tips: ALIASES](https://netizenry.codeberg.page/content/game_journalism/Duskers_Tips-ALIASES.html) — реальні рядки аліасів і синтаксис `navigate`, `open`, `close`, `dock`, `tow`.
- [Release notes](https://docs.google.com/document/d/1L9FUTiiekhGaKNmhSDmTgDoDifHbXjnT5z1Hw3yQ7BQ/pub) — лише бачив у результатах пошуку.

## Непевне
- (?) Числа (ціни модулів 8/10 скрапу, ремонт сигналу ~7, Decontaminate 3 заряди, Overload 4) — з фан-вікі однієї версії, не звірено з грою.
- (?) Чи є пауза в реальному часі (здається, нема).
- (?) Повний перелік ворогів і їхня поведінка — з фан-вікі; «пси» лише згадані.
- (?) Як саме `motion` позначає «непевні» кімнати; дальність `in_range` міни — «кімната».
- Fandom-сторінка команд віддала 402 — у шапку не взято.
