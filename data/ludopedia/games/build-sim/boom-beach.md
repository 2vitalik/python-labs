---
title: Boom Beach
slug: boom-beach
aka: []
family: build-sim
also: [tower-lanes]
klass: hybrid
axes:
  field: square
  time: realtime
  opponent: online
  info: partial
  random: none
  goal: state
year: 2014
platforms: [iOS, Android, PC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Boom_Beach", best: true, note: "канонерка з енергією, ракетниці й артилерія, висадка лише на пляж, перемога = знищити штаб, архіпелаг, Task Force, Warships"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Boom+Beach+attack+flare+gameplay", note: "пошук; атаки з ракетницями"}
stage: v1
coverage: 55
mechanics: [multi-cell-size, cursor-place, drag-drop-piece, cell-click, chase-greedy, hp-damage, projectile-shot, explode-area, tower-placement, tower-range, round-currency, in-round-upgrades, fog-of-war, map-window, world-map, online-multiplayer, simultaneous-versus, replay, leaderboard, player-camera, field-scaling, +deploy-zone, +key-target-win, +support-energy-pool, +flare-redirect, +energy-from-kills, +friendly-fire, +async-pvp, +shared-raid-target, +hidden-trap]
proposes: ["+effect:redirect(group, cell)", "+cond:key_target_alive", "+role:key-target", "+ui:support-energy-bar", "+window:archipelago-map", "+feature:task-force-operation", "+card:flare-redirect", "+card:key-target-win"]
author: opus
date: 2026-11-09
---

# Boom Beach — Clash of Clans на острові: висаджуєш десант з човнів на пляж, а керуєш ним лише ракетницею й гарматами канонерки; перемога — тільки знищений штаб

## Суть
Та сама модель, що в [clash-of-clans-base](clash-of-clans-base.md): база-сітка з будівлями N×N, оборона стріляє сама, атака — асинхронна проти «знімка» чужої або NPC-бази. Описано **лише відмінності**. Війська приходять **десантними човнами** і висаджуються тільки на пляж з одного краю острова. Після висадки вони біжать до найближчої цілі, а гравець впливає на бій **пулом енергії канонерки**: сигнальна ракета (flare) веде весь десант у точку, артилерія та інші удари бʼють по обороні. Перемога бінарна: знищив **штаб (HQ)** — уся база руйнується й лут твій; не знищив — поразка без ресурсів, хоч би скільки зруйнував.

## Поле і час
- База — сітка острова з будівлями N×N (як у CoC); **стін нема**, тож лабіринту-фанелінгу нема: оборона — радіуси веж, міни й розташування штабу.
- Висадка не з будь-якого краю, а лише на смугу пляжу з моря — фіксований фронт атаки.
- Над островами — **архіпелаг** з туманом: мапа відкривається радаром, на ній NPC-бази, ресурсні бази, бази гравців, точки занурення (?) — шар `map-window` над полем бою.
- Атака — real-time з обмеженим часом (?); розстановка бази — статика.

## Сутності
Сутності бази й військ — як у [clash-of-clans-base](clash-of-clans-base.md) (оборонні вежі, ресурси, пастки). Нові або змінені:

| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Штаб (HQ) | static | HP, рівень | **ключова ціль**: знищення = миттєва перемога, база колапсує; рівень відкриває будівлі й війська |
| Канонерка (Gunboat) | player | пул енергії | поза полем; витрачає енергію на удари підтримки |
| Енергія канонерки | resource | старт + апгрейди | поповнюється за кожну знищену будівлю ворога |
| Десантний човен | container | місткість (?) | везе загін одного типу; висаджує на пляж |
| Пляж | zone | — | єдина зона висадки |
| Сигнальна ракета (flare) | projectile | ціна енергії | усі війська йдуть до точки, ігноруючи ціль, доки не дійдуть (?) |
| Артилерія / Barrage / Shock (?) | projectile | ціна росте з кожним використанням (?) | шкода або оглушення по області; може зачепити свої війська |
| Димова завіса, аптечка (?) | projectile | — | невидимість / лікування на області |
| Міни (звичайні, Boom, Shock) (?) | hazard | прихована | вибух при наближенні |
| Статуя з Power Stone | static | бафф | пасивний бонус для бази або атаки |
| NPC-база Blackguard / Hammerman / Dr. T | enemy | — | AI-бази на мапі; Hammerman згодом сам атакує гравця |
| Ресурсна база | resource | генерація | захоплюється; інші гравці можуть відбити |
| Power Core (операції) | static | 1–2 на базу | замінює HQ у кооперативних операціях; треба знищити всі |
| Engine Room (Warships) | static | — | ціль сезонного режиму з одночасною атакою |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(tap, beach_cell)` → ЯКЩО `cell(x, beach)` і `has(attacker, landing_craft)` → ТО `spawn_at(troops, x)`, `take(attacker, landing_craft)`.
- КОЛИ `spawned(troop)` або `destroyed(current_target)` → ЯКЩО `not state(troop, flared)` → ТО `custom: «обрати найближчу ціль за пріоритетом свого типу»`, `move`.
- КОЛИ `input(flare, cell)` → ЯКЩО `counter(energy, >=, cost)` → ТО `counter(energy, −cost)`, `set_state(troops, flared)`, `custom: «усі війська йдуть до точки ракети»`.
- КОЛИ `reach(troop, flare_point)` → ТО `clear_state(troop, flared)`, `custom: «знову обирає ціль сам»`.
- КОЛИ `input(artillery, cell)` → ЯКЩО `counter(energy, >=, cost)` → ТО `counter(energy, −cost)`, `explode(area, n)`; `custom: «шкода й по своїх військах (friendly fire)»`; ціна наступного удару зростає (?).
- КОЛИ `destroyed(building)` → ТО `counter(energy, +n)`.
- КОЛИ `in_range(tower, troop, r)` → ТО `damage(troop, n)` — як у CoC.
- КОЛИ `in_range(mine, troop, r)` → ТО `reveal(mine)`, `explode(area, n)`; одноразова.
- КОЛИ `destroyed(hq)` → ТО `custom: «усі будівлі бази руйнуються»`, `win`, `currency(+all_loot)`, `counter(victory_points, +n)`.
- КОЛИ `all_gone(troop)` або `custom: «час атаки вийшов»` → ЯКЩО `custom: «HQ живий»` → ТО `lose`, `custom: «жодного луту»`.
- Операція Task Force: КОЛИ `destroyed(building)` → ТО `counter(force_points, +1)`; КОЛИ `all_gone(power_core)` → ТО `win`; кожен гравець має 1 атаку на операцію.
- Warships: обидва атакують одночасно; КОЛИ `custom: «час бою вийшов»` → ТО `custom: «перемагає той, у кого більше Engine Rooms; далі — більший % руйнування; далі — більше часу; інакше нічия»` → `draw`.

## Керування і ввід
- Атака: на мапі архіпелагу тап по базі → розвідка → бій; тап по пляжу висаджує човни; тап по кнопці удару канонерки → тап по точці (ракета / артилерія / інше).
- Більше нічого: шляхи й цілі обирає AI, вплив — тільки через енергію.
- База: drag будівель з крамниці; без стін, тож без інструменту ряду стін.

## Вікна, меню, HUD
- `map-window` (архіпелаг): туман, радар відкриває сектори, на мапі бази й ресурсні острови, точки занурення субмарини.
- `game-screen` бою: пляж знизу, панель човнів, панель ударів канонерки з ціною, `support-energy-bar`, таймер (?), HP штабу.
- `end-screen`: перемога/поразка, лут, victory points.
- `shop-window`, `custom-window` Weapon Lab (прототипи на тиждень), Task Force (чат, операції), Warships (сезонне дерево техніки), `leaderboard`.

## Фічі поза полем
- PvE-шар на мапі: NPC-бази, що відновлюються, ресурсні бази з конкуренцією гравців, події Dr. T.
- `mode-coop` асинхронний (операції Task Force зі спільною нагородою) і сезонний PvP Warships з лігами.
- Прогресія за рівнем HQ; тимчасові прототипи оборони з Weapon Lab.

## Варіації й родичі
- [clash-of-clans-base](clash-of-clans-base.md) — базова модель (стіни-лабіринт, висадка з усіх боків, зірки за %).
- **Осі варіацій** відносно CoC: фронт висадки (будь-який край / пляж) · вплив на бій після висадки (нема / пул енергії з ударами й ракетою) · умова перемоги (зірки за % / тільки ключова ціль) · стіни (є / нема).

## Цікавинки для курсу
- Ракета-маяк: глобальна команда «усі до точки», після досягнення — повернення до власного AI — 📎.
- Пул енергії, що поповнюється знищеннями, + зростаюча ціна повторного удару — 🌱.
- Ключова ціль = вся база (бінарна перемога) — 🌱.
- Friendly fire від області удару — 🌱.
- Мапа-архіпелаг з радаром-туманом над окремими «рівнями»-базами — 📎.

## Мапа на каталог
- Є: `multi-cell-size` · `cursor-place` + `drag-drop-piece` ↔ розстановка · `cell-click` · `chase-greedy` ↔ найближча ціль · `hp-damage` · `projectile-shot` · `explode-area` ↔ артилерія · `tower-placement` + `tower-range` · `round-currency` · `in-round-upgrades` ↔ удари канонерки · `fog-of-war` + `map-window` + `world-map` ↔ архіпелаг · `online-multiplayer` · `simultaneous-versus` ↔ Warships · `replay` · `leaderboard` · `player-camera` · `field-scaling`.
- **Нема** → пропозиції карток:
  - `+flare-redirect` «Маяк: група йде до точки, потім знову сама» · entities/move · 📎.
  - `+support-energy-pool` «Пул енергії на удари підтримки» · game-logic/economy · 🌱 · слоти {start, regen_per_kill, cost_growth}.
  - `+energy-from-kills` «Енергія за знищення» · game-logic/economy · 🌱.
  - `+key-target-win` «Знищити ключову ціль = перемога, інакше нуль» · game-logic/win · 🌱.
  - `+friendly-fire` «Удар по області шкодить своїм» · entities/combat · 🌱.
  - `+shared-raid-target` «Спільна ціль клану, кожен — одна атака» · game-logic/opponent · 📎.
  - `+deploy-zone`, `+async-pvp`, `+hidden-trap` — повторно (CoC).

## Пропозиції до словників
- `+effect:redirect(group, cell)` — тимчасово перевизначити ціль AI-групи (ракета); зараз `set_state(flared)` + custom.
- `+cond:key_target_alive` — ключова ціль ще стоїть (HQ, Power Core).
- `+role:key-target` — будівля, від якої залежить результат бою.
- `+ui:support-energy-bar` — пул енергії з ціною наступного удару на кнопках.
- `+window:archipelago-map` — мапа з туманом і радаром, де вузли — бази (дитина `map-window`).
- `+feature:task-force-operation` — кооперативна атака на спільну базу з очками за будівлі.
- `+card:flare-redirect`, `+card:key-target-win` — див. вище.

## Джерела
- ⭐ [Wikipedia: Boom Beach](https://en.wikipedia.org/wiki/Boom_Beach) — канонерка й енергія (поповнення за знищені будівлі), flares і artillery, friendly fire, висадка на пляж, HQ = перемога, архіпелаг, NPC-бази Blackguard/Hammerman/Dr. T, Power Stones і статуї, Task Force, Warships з тай-брейками, Weapon Lab.
- YouTube: пошук «Boom Beach attack flare gameplay».

## Непевне
- (?) Типи ударів канонерки, крім flare і artillery (barrage, smoke, medkit, shock bomb), зростання ціни повторного удару — з памʼяті.
- (?) Типи мін, ліміт часу атаки, місткість човнів — не перевірено (фан-вікі не відкривав: fandom віддає 402 у цій хвилі).
- (?) Чи ракета змушує військо ігнорувати оборону дорогою; поведінка після досягнення точки.
- (?) Розміри сітки бази й будівель.
