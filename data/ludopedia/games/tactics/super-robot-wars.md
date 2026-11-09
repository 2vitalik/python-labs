---
title: Super Robot Wars
slug: super-robot-wars
aka: [SRW, "スーパーロボット大戦", "Super Robot Taisen", "Super Robot Wars Original Generation", "Super Robot Wars Alpha"]
family: tactics
also: []
klass: figure
axes:
  field: square
  time: turn
  opponent: ai
  info: full
  random: runtime
  goal: state
year: 1991
platforms: [Game Boy, NES, SNES, PS1, GBA, PS2, NDS, PS3, PS4, Switch, PC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Super_Robot_Wars", best: true, note: "серія: хід, місцевість, бази й крейсери, супер- і реал-типи, розмір, трансформація, MAP-зброя, вибір відповіді, анімація бою, кросовер"}
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/精神コマンド", note: "JA: дух-команди (必中, ひらめき, 熱血, 魂, 鉄壁, 加速, 集中, 信頼…), SP, воля 気力 50–150"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Super_Robot_Wars_Alpha", note: "Skill Points (Battle Mastery), маршрути супер/реал, 2D/3D анімації"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Super_Robot_Wars_Original_Generation", note: "два герої-маршрути, перенесення зброї між реал-мехами, Pilot Points"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=super+robot+wars", note: "пошук; SRW 30, SRW T, SRW V, SRW X"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Super+Robot+Wars+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [move-by-input, impassable-cells, hp-damage, melee-vs-ranged, explode-area, status-effects, temporary-modes, unit-xp-skills, reachable-highlight, threat-range, shop-between-levels, sequential-levels, save-game, game-over-continue, game-screen, end-screen, +spirit-commands, +morale-meter, +will-gated-weapons, +terrain-adaptation, +unit-size-modifiers, +counter-choice, +combat-animation, +transform-mode, +carrier-dock-repair, +energy-ammo, +support-abilities, +combination-attack, +skill-point-routes, +branching-campaign, +unit-upgrade-money, +enemy-phase-after-player, +hit-chance, +area-attack]
proposes: ["+trigger:battle_resolved", "+cond:will", "+cond:terrain_rank", "+effect:will", "+effect:sp", "+effect:spirit", "+role:carrier", "+ui:sp-counter", "+ui:will-meter", "+ui:hit-forecast", "+window:battle-animation", "+window:spirit-menu", "+window:intermission-menu", "+feature:animation-toggle-per-battle"]
author: opus
date: 2026-11-09
---

# Super Robot Wars — кросовер-SRPG з мехами з різних аніме: пілоти витрачають SP на «дух-команди», воля росте в бою й відкриває суперудари

## Суть
Загін мехів із десятків аніме-серій (Gundam, Mazinger, Getter Robo…) бʼється покроково на сітці проти AI. Кожен юніт = машина (HP, енергія EN, броня, рух, місцевість, зброя) + пілот (характеристики, SP, навички). Атака — вибір зброї за дальністю, захисник обирає відповідь (контратака / блок / ухилення), далі — **анімаційна сцена бою**. Механічна родзинка — **дух-команди** (Spirit Commands): пілот витрачає SP на разові бафи («влучання 100 %», «ухилитися від наступної атаки», «шкода ×2»), і **воля** (Will/気力) — лічильник, що росте від бою й відмикає найсильнішу зброю.

## Поле і час
- Квадратна сітка; кожен юніт займає 1 клітину незалежно від «розміру» (розмір лише модифікує бій).
- Місцевість чотирьох типів: суша, повітря, море, космос — впливає на машини, пілотів і зброю по-різному; об'єкти поля (військова база: ремонт і заправка EN, бонус захисту наземним, гальмує рух).
- Хід — фаза гравця (усі свої юніти по одному), потім фаза ворога (AI).
- Інформація повна; статки ворога видно (дух-команда «розвідка» відкриває більше).
- Випадковість: влучання/ухилення, критичні удари; на рівні серії — маршрути й приховані юніти за діями гравця.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Супер-тип робот | piece | високі HP і броня, енергоємна ближня зброя | бʼє сильно впритул, ухиляється погано |
| Реал-тип робот | piece | менше HP/броні, спритний | ухиляється, далекобійна точна зброя, менша шкода |
| Юніт підтримки | piece | лікування/заправка | відновлює HP і/або EN союзникам |
| Крейсер (battleship) | piece | повітря/космос, далекобійний | приймає юніти на борт: ремонт і заправка |
| Пілот | — | стати (melee/shooting…), SP, воля, навички, рівень | визначає ефективність зброї класу; витрачає SP |
| Зброя | — | дальність, модифікатор точності, сила, EN/набої, мін. воля, клас melee/shooting | обирається при атаці й відповіді |
| MAP-зброя | — | область | бʼє кілька клітин; частина не зачіпає союзників |
| Трансформований юніт | piece | форми з різною зброєю й атрибутами | змінює форму (Getter Robo) |
| Ворожий юніт | enemy | ті самі параметри | AI фази ворога |
| Бос / «найсильніший» ворог | boss | великий HP, часто регенерація (?) | ціль місії |
| Військова база / місто | terrain | бонус захисту, ремонт | стоїш — відновлюєшся |
| Місцевість (суша/повітря/море/космос) | terrain | рейтинг пристосованості юніта й зброї | множить ефективність |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(player)` → ТО `custom: «кожен юніт: рух → атака / дух / ремонт / посадка на крейсер, у будь-якому порядку до кінця дії (?)»`; потім фаза ворога.
- КОЛИ `input(move, unit, cell)` → ЯКЩО `custom: «шлях у межах руху з урахуванням місцевості»` → ТО `move(unit, cell)`.
- КОЛИ `input(attack, unit, target, weapon)` → ЯКЩО `in_range(unit, target, weapon_range)` and `custom: «EN/набої є і воля ≥ мінімуму зброї»` → ТО `choose(відповідь цілі: контратака | блок | ухилення)`.
- КОЛИ `custom: «ціль обрала блок»` → ТО `custom: «захист вищий проти цієї атаки»`; ухилення → `custom: «шанс влучання нижчий»`; контратака → `custom: «відповідний удар своєю зброєю»`.
- КОЛИ `custom: «відповідь обрано»` → ТО `window(battle-animation)`; `damage(target, n)` з урахуванням місцевості, розміру, захисту цілі.
- КОЛИ `custom: «більший юніт атакує менший»` → ТО `custom: «бонус атаки/захисту, але штраф до ухилення й точності»`.
- КОЛИ `input(attack, map_weapon, area)` → ТО `damage(all_in_area, n)`; `custom: «деяка MAP-зброя пропускає союзників»`.
- КОЛИ `custom: «зброя з ефектом»` → ТО `set_state(target, drained_en | weakened_armor | pilot_stat_down)`.
- КОЛИ `input(spirit, pilot, command)` → ЯКЩО `custom: «SP ≥ ціни»` → ТО `custom: «SP − ціна»` і `set_state(unit, command, duration)`.
- КОЛИ дух «必中 Strike» → ТО `custom: «влучання 100 % на 1 хід»`; «ひらめき Alert» → `custom: «гарантоване ухилення від наступної атаки»`; «熱血 Valor» → `custom: «наступна атака ×1.5–2»`; «魂 Soul» → `custom: «×2.5 (ранні — ×3), не разом з Valor»`.
- КОЛИ дух «鉄壁 Iron Wall» → ТО `custom: «шкода по собі ×1/4 на 1 хід»`; «集中 Focus» → `custom: «+30 % влучання й ухилення на 1 хід»`; «加速 Accel» → `speed(unit, +2..5)` на наступний рух.
- КОЛИ дух «信頼 Trust» → ТО `heal(ally, 2000)`; «気合 Spirit» → `custom: «воля +10»`; «脱力 Disrupt» → `custom: «воля ворога −10»`; «幸運 Fortune» → `currency(×2)` за наступний бій; «努力 Gain» → `custom: «досвід ×2»`.
- КОЛИ дух «覚醒 Awaken» → ТО `extra_move`; «再動 Reactivate» → `custom: «юніт, що вже діяв, діє знову»`; «復活» → `respawn(unit)` з повними HP/EN/SP.
- КОЛИ `level_start` → ТО `custom: «воля кожного = 100»`; КОЛИ влучив / отримав шкоду / знищив ворога → `custom: «воля +n»` у межах 50–150 (навичкою до 170); вища воля → більша шкода.
- КОЛИ `custom: «юніт вижив і пошкодив ворога»` → ТО `custom: «досвід → рівень пілота»`; КОЛИ `destroyed(enemy)` → `currency(+n)`.
- КОЛИ `contact(unit, carrier)` (посадка) → ТО `custom: «щохід ремонт HP і заправка EN»`; база — те саме для юніта на клітині.
- КОЛИ `input(transform, unit)` → ТО `transform(unit, form)` з іншою зброєю й атрибутами.
- Перемога: `custom: «умова місії: знищити всіх / боса / дожити N ходів / дійти до точки (?)»` → `win` · Поразка: `custom: «знищено флагман або ключового пілота (?)»` → `lose` · Рахунок: гроші й досвід; Skill Points за додаткові цілі (Alpha) відкривають юніти й складність.

## Керування і ввід
- Курсор по сітці: вибрати юніт → `reachable-highlight` → клітина → меню команд: Атака / Дух / Трансформація / Ремонт / Посадка / Чекати.
- Атака: список зброї з дальністю, точністю, силою, ціною EN; перед боєм — вікно прогнозу (шанс влучання, шкода) і вибір відповіді цілі під час фази ворога.
- Меню духу: список команд пілота з ціною SP.
- Анімацію бою можна пропустити або вимкнути (?).

## Вікна, меню, HUD
- `main-menu`: нова гра / продовжити / налаштування.
- `custom-window` «Інтермісія» (`intermission-menu`) — апгрейд юнітів за гроші, навички пілотів (Pilot Points у OG), розподіл пілотів, зброя (OG — перенесення між реал-мехами), збереження.
- `game-screen`: сітка з місцевістю, юніти, `reachable-highlight`, `threat-range`, панель юніта (HP, EN, `ui:will-meter`, `ui:sp-counter`), `turn-counter`.
- `custom-window` «Прогноз бою» (`ui:hit-forecast`) — шанс влучання, шкода, вибір відповіді.
- `custom-window` «Сцена бою» (`battle-animation`) — анімація атаки й відповіді, HP-бари, репліки пілотів.
- `custom-window` «Дух-команди» (`spirit-menu`).
- `custom-window` «Розвідка» — статки ворога.
- `end-screen` / брифінг між главами; `game-over-continue` (?).

## Фічі поза полем
- Кампанія з глав і маршрутів (вибір супер/реал-маршруту в Alpha, два герої в OG; рішення впливають на складність і відкриття юнітів).
- Апгрейд машин за гроші (HP, EN, броня, рухливість, зброя) (?).
- Прогресія пілотів: рівень, навички, Pilot Points (OG) на навички/стати/місцевість.
- Кросовер-реєстр: десятки серій — у кожній грі свій набір ліцензій.
- Налаштування: анімація бою вкл/вимк (`animation-toggle`) (?).

## Варіації й родичі
- Серія: SRW (GB 1991) → 第2/3/4次 → Alpha → OG (лише власні робот-персонажі) → Z, V, X, T, 30.
- Сусіди: [front-mission](front-mission.md) (меха без кросоверу, з частинами), [fire-emblem](fire-emblem.md) (фаза гравця/ворога, відповідь, анімація бою), [langrisser](langrisser.md), [disgaea](disgaea.md) (гринд і апгрейди).
- **Осі варіацій**: баф — постійний / **разовий за SP** / за волею · відповідь — автоматична (FE) / **вибір блок/ухилення/контра** · розмір — клітина / бонуси розміру / багатоклітинні · пристосованість — один тип / **4 типи місцевості з рейтингом**.

## Цікавинки для курсу
- Дух-команди: разові бафи з тривалістю «наступна атака / 1 хід» за ресурс SP — 🥉.
- Воля: лічильник 50–150, росте від подій і відмикає зброю — 📎.
- Вибір відповіді захисника (контра / блок / ухилення) з прогнозом — 🥉.
- Рейтинг місцевості суша/повітря/море/космос як множник — 📎.
- MAP-зброя з пропуском союзників — 📎.
- Посадка на крейсер з ремонтом щоходу — 🌱.
- Трансформація юніта з новою зброєю — 📎.

## Мапа на каталог
- Є: `move-by-input` · `impassable-cells` · `hp-damage` · `melee-vs-ranged` (melee/shooting) · `explode-area` (MAP-зброя) · `status-effects` (виснаження EN, броні) · `temporary-modes` (дух-команди на 1 хід) · `unit-xp-skills` · `reachable-highlight` · `threat-range` · `shop-between-levels` (апгрейди) · `sequential-levels` · `save-game` · `game-over-continue` · `game-screen` · `end-screen`.
- **Нема** → пропозиції карток:
  - `+combat-animation` · `+support-abilities` · `+branching-campaign` · `+enemy-phase-after-player` · `+hit-chance` · `+area-attack` — наявні пропозиції корпусу.
  - `+morale-meter` «Воля: лічильник, що росте від бою» · entities/state · 📎.
  - `+spirit-commands` «Разові бафи пілота за SP» · entities/state · 🥉.
  - `+will-gated-weapons` «Зброя доступна з порогу волі» · entities/combat · 📎.
  - `+terrain-adaptation` «Рейтинг юніта для 4 типів місцевості» · entities/state · 📎.
  - `+unit-size-modifiers` «Розмір дає бонуси/штрафи в бою» · entities/combat · 🌱.
  - `+counter-choice` «Захисник обирає відповідь» · entities/combat · 🥉.
  - `+transform-mode` «Юніт змінює форму» · entities/state · 📎.
  - `+carrier-dock-repair` «Посадка на носій: ремонт» · entities/interact · 🌱.
  - `+energy-ammo` «Зброя їсть EN або набої» · entities/combat · 🌱.
  - `+combination-attack` «Спільна атака двох юнітів» · entities/combat · 📎.
  - `+skill-point-routes` «Приховані очки за цілі відкривають маршрути» · levels/progression · 📎.
  - `+unit-upgrade-money` «Апгрейд статків машини за гроші» · game-logic/economy · 📎.

## Пропозиції до словників
- `+trigger:battle_resolved` — завершилась сцена бою (досвід, воля, гроші).
- `+cond:will` — воля ≥ N (зброя, навички); `+cond:terrain_rank` — рейтинг місцевості.
- `+effect:will` — ±воля; `+effect:sp` — ±SP; `+effect:spirit` — накласти дух-команду.
- `+role:carrier` — юніт, що приймає інших на борт.
- `+ui:sp-counter` — SP пілота; `+ui:will-meter` — воля; `+ui:hit-forecast` — прогноз влучання/шкоди.
- `+window:battle-animation` — сцена бою; `+window:spirit-menu` — меню дух-команд; `+window:intermission-menu` — інтермісія.
- `+feature:animation-toggle-per-battle` — увімкнути/пропустити анімацію конкретного бою.

## Джерела
- ⭐ [Wikipedia: Super Robot Wars](https://en.wikipedia.org/wiki/Super_Robot_Wars) — покроковість, 4 місцевості, база й крейсер, супер/реал/підтримка, розмір, трансформація, MAP-зброя, блок/ухилення/контра, анімація, досвід, перша гра GB 1991, кросовер.
- [Wikipedia (JA): 精神コマンド](https://ja.wikipedia.org/wiki/精神コマンド) — ефекти дух-команд за поколіннями, відновлення SP, воля 100 на старті, 50–150, до 170 навичкою, мін. воля зброї.
- [Wikipedia: SRW Alpha](https://en.wikipedia.org/wiki/Super_Robot_Wars_Alpha) — Skill Points, маршрути, 2D/3D анімації.
- [Wikipedia: SRW Original Generation](https://en.wikipedia.org/wiki/Super_Robot_Wars_Original_Generation) — маршрути двох героїв, перенесення зброї, Pilot Points.

## Непевне
- (?) Апгрейд машин за гроші, комбіновані атаки, умова поразки «знищено флагман/героя», екран «продовжити після поразки» — з памʼяті, у відкритих джерелах нема.
- (?) Ціни SP дух-команд різні в кожній грі й пілоті — не писав.
- (?) Порядок «рух → дія» і можливість діяти після руху — з памʼяті.
- (?) Перемикач анімацій — з памʼяті.
- (?) Платформи серії — з памʼяті, широкий перелік; fandom SRW віддав 402, WebSearch вичерпано.
