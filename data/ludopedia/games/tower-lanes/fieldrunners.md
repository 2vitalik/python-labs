---
title: Fieldrunners
slug: fieldrunners
family: tower-lanes
also: []
klass: cursor
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: none
  goal: survive
year: 2008
platforms: [iOS, Android, DSiWare, PSP, PS3, PC, Mac, Linux]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Fieldrunners", best: true, note: "вільна розстановка, вороги обходять вежі, типи веж, мапи, режими"}
  - {kind: steam, url: "https://store.steampowered.com/app/209690/Fieldrunners/", note: "PC-версія"}
  - {kind: steam, url: "https://store.steampowered.com/app/215710/_Fieldrunners_2/", note: "сиквел: шляхи-головоломки, більше веж"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=fieldrunners+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 75
mechanics: [enemy-waves, spawn-schedule, enemy-reached-base, chase-bfs, reachability-check, round-currency, in-round-upgrades, shop-buyback, shop-catalog, projectile-shot, shoot-cooldown, blast-wave, temporary-modes, hp-damage, melee-vs-ranged, speed-per-type, goal-counter, difficulty-levels, level-select, +tower-placement, +maze-by-towers, +path-recompute, +tower-range, +flying-ignores-maze, +call-wave-early]
proposes: ["+trigger:path_changed", "+cond:path_exists", "+effect:recompute_path", "+effect:sell", "+effect:upgrade", "+role:tower", "+ui:range-circle", "+ui:tower-panel", "+ui:next-wave-button", "+window:mode-select", "+feature:mode-endless", "+axis:session"]
author: opus
date: 2026-11-02
---

# Fieldrunners — tower defense без доріг: вежі на відкритому полі самі стають лабіринтом

## Суть
Гравець ставить вежі будь-де на відкритій сітці, а наземні вороги йдуть від входу до виходу **найкоротшим шляхом, що перераховується** після кожної вежі. Отже, оборона одночасно будує лабіринт: що довший шлях, то довше вороги під вогнем. Повністю перекрити прохід заборонено. Вороги, що дійшли до виходу, забирають життя; гра — 100 хвиль або нескінченно.

## Поле і час
- Поле — прямокутна сітка без доріг (Grasslands: вхід зліва, вихід справа); мапи додають кілька входів, перешкоди, залізничні маршрути, що перетинають поле (Crystal Caves, MudSlide, LavaFlow).
- Вежа займає блок клітин сітки (?) і стає непрохідною для наземних ворогів; повітряні летять напряму.
- Real-time з хвилями: хвиля за таймером або раніше за кнопкою; між хвилями розстановка не зупиняє гру (можна будувати й під час хвилі).
- Камера: уся мапа на одному екрані (мобільний формат), без туману.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Вхід | spawner | 1–4 на мапі | хвилі ворогів зʼявляються тут |
| Вихід | static | — | ворог дійшов → −життя |
| Перешкода (скеля, дерево) | static | — | непрохідна, на ній не будують |
| Gatling Tower | ally | дешева, рівні апгрейда | швидкі постріли по одній цілі, наземні й повітряні |
| Goo Tower | ally | — | сповільнює ціль (слизом) |
| Missile Tower | ally | дорога, далекобійна | ракети з невеликим сплеском (?) |
| Tesla Tower | ally | — | електрика по наземних, висока шкода (?) |
| Flame Tower | ally | Extended | вогонь на короткій дистанції |
| Mortar Tower | ally | Extended | навісний снаряд зі сплеском по наземних |
| Laser / Ice Tower | ally | мапи Skyway / Frostbite | замінюють Tesla / Goo |
| Піхота | enemy | мало HP | іде найкоротшим шляхом |
| Швидкий юніт (мотоцикл) | enemy | висока швидкість | той самий шлях, швидше (?) |
| Броньований (танк) | enemy | багато HP | повільний, міцний (?) |
| Повітряний (гелікоптер, дирижабль) | enemy | летить | ігнорує лабіринт: пряма лінія до виходу |
| Потяг | hazard | маршрут по рейках | на окремих мапах перетинає поле (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(place, tower, cell)` → ЯКЩО `has(money, cost)` and `free(cells)` and `custom: «cond path_exists: від кожного входу до виходу лишається шлях»` → ТО `spawn(tower)`, `currency(-cost)`, `custom: «effect recompute_path для всіх наземних»`; інакше `block` + `message`.
- КОЛИ `custom: «trigger path_changed»` → ТО кожен наземний ворог `custom: «новий найкоротший шлях від своєї поточної клітини»` (BFS/A*).
- КОЛИ `tick` → наземний ворог `move(a, next_on_path)`; повітряний — `move(a, straight_to_exit)`.
- КОЛИ `in_range(tower, enemy, r)` → ЯКЩО `custom: «тип цілі дозволений (наземна/повітряна)»` → ТО `spawn(projectile)` з періодом `shoot-cooldown`.
- КОЛИ `contact(projectile, enemy)` → ТО `damage(n)`; Goo — `speed(enemy, ×k, duration)`; Mortar/Missile — `damage` по радіусу.
- КОЛИ `hp_zero(enemy)` → ТО `disappear_a`, `currency(+bounty)`, `score(+n)`.
- КОЛИ `reach(enemy, exit)` → ТО `lives(-1)`, `disappear_a`.
- КОЛИ `counter(lives, ==, 0)` → ТО `lose`.
- КОЛИ `input(select, tower)` → ТО `window(tower-panel)`: апгрейд (`currency(-price)`, `custom: «effect upgrade: +рівень, більше шкода/дальність»`) або продаж (`custom: «effect sell: повернути частину вкладеного»`, `disappear_a`, `recompute_path`).
- КОЛИ `schedule(waves)` або `input(next_wave)` → ТО `wave_start`, `spawn_at(enemies, entrances)`; ранній виклик дає бонус (?).
- КОЛИ `custom: «хвиля 100 завершена»` → ЯКЩО `mode(classic|extended)` → ТО `win`; `mode(endless)` — без кінця, рахунок — номер хвилі й очки.
- Перемога: пережити 100 хвиль · Поразка: життя = 0 · Рахунок: очки за вбивства (+ бонуси), рекорд мапи.

## Керування і ввід
- Тач/миша: перетягнути іконку вежі з панелі на поле (`drag-drop-piece`), привид вежі показує радіус і чи легальна позиція.
- Тап по вежі — панель апгрейда/продажу; тап по порожньому — закрити.
- Кнопки: пауза, наступна хвиля раніше, (у пізніх версіях) прискорення (?).

## Вікна, меню, HUD
- `main-menu` — Play → вибір мапи; налаштування; рекорди.
- `level-select` — мапи (Grasslands, Crossroads, Drylands; Skyway, Frostbite, Crystal Caves, MudSlide, LavaFlow).
- `mode-select` (⏳) — Classic · Extended · Endless; `difficulty-select` — Easy / Medium / Hard.
- `game-screen`: поле, панель веж з цінами, `coins`, `lives`, `wave-counter`, `score`, кнопка паузи й наступної хвилі.
- `custom-window` панель вежі (`+ui:tower-panel`): рівень, параметри, ціна апгрейда, ціна продажу; `+ui:range-circle` навколо вибраної.
- `pause-menu` — продовжити, рестарт, вихід; `end-screen` — поразка/перемога з очками; `leaderboard` — рекорди мап.
- Переходи: main-menu → level-select → mode/difficulty → game-screen → end-screen → level-select.

## Фічі поза полем
- `mode-classic` (100 хвиль), Extended (100 хвиль + Flame/Mortar), `mode-endless`; `difficulty-presets` Easy/Medium/Hard для кожного.
- Нові мапи як `unlockables`/покупки (Skyway, Frostbite, MudSlide, LavaFlow — in-app; Crystal Caves — безкоштовна).
- `leaderboard-local` / онлайн-рекорди (?), `pause`, `sound-toggle`.

## Варіації й родичі
- Fieldrunners 2 (2012): головоломкові рівні, більше веж, задані маршрути; Fieldrunners Attack!.
- Родичі «лабіринту з веж»: Desktop Tower Defense (2007, браузер), Gemcraft, Bloons (навпаки — фіксований шлях), Isle of Arrows (шлях будує гравець плитками), Defense Grid.
- **Осі варіацій**: шлях — фіксований / лабіринт з веж / будує гравець · блокування — заборонено / дозволено (тоді вороги ламають вежі) · повітряні — ігнорують лабіринт / ні · вхід — один / кілька / що змінюється.

## Цікавинки для курсу
- Перерахунок шляху BFS на сітці після кожної вежі для кожного ворога з його клітини — 🥇 (класичний алгоритм у живій грі).
- Заборона повного перекриття: перед посадкою перевірити досяжність виходу з усіх входів — 🥈 (`reachability-check` у реальному часі).
- Вежа: радіус, вибір цілі (перший / найближчий / найслабший), cooldown — 🥉.
- Апгрейд/продаж з поверненням частини вартості — 📎.
- Повітряні вороги поза лабіринтом — 🌱 (той самий двіжок, інший рух).

## Мапа на каталог
- Є: `enemy-waves` + `spawn-schedule` · `enemy-reached-base` ↔ вихід і життя · `chase-bfs` ↔ найкоротший шлях · `reachability-check` ↔ заборона блокування · `round-currency` ↔ гроші за вбивства · `in-round-upgrades` ↔ апгрейди веж · `shop-buyback` ↔ продаж вежі · `shop-catalog` ↔ панель веж з цінами · `projectile-shot` + `shoot-cooldown` · `blast-wave` ↔ сплеск ракет/мортири · `temporary-modes` ↔ сповільнення · `hp-damage` · `melee-vs-ranged` ↔ наземні/повітряні цілі · `speed-per-type` · `goal-counter` + `status-panel` · `difficulty-levels` · `level-select` · `game-pause`.
- **Нема** → пропозиції карток:
  - `+tower-placement` «Розстановка веж» · entities/spawn · 🥉 · слоти {footprint, cost}.
  - `+maze-by-towers` «Лабіринт із веж» · levels/solvability · 🥇 — вежі = стіни, шлях ворога росте.
  - `+path-recompute` «Перерахунок шляху після зміни поля» · entities/move · 🥈 (дитина `chase-bfs`).
  - `+tower-range` «Радіус і вибір цілі» · entities/combat · 🥉 · слот {target: first|nearest|weakest}.
  - `+flying-ignores-maze` «Повітряні ігнорують перешкоди» · entities/move · 🌱.
  - `+call-wave-early` «Хвиля раніше за бонус» · game-logic/waves · 🌱.

## Пропозиції до словників
- `+trigger:path_changed` — змінилась прохідність поля (поставили/продали вежу).
- `+cond:path_exists` — від точки A до B існує шлях (легальність розстановки).
- `+effect:recompute_path` — сутність перебудовує маршрут; `+effect:sell` — прибрати свою сутність з поверненням частини ціни; `+effect:upgrade` — +рівень сутності з новими параметрами.
- `+role:tower` — стаціонарний союзник, що атакує в радіусі (відрізняти від `ally`, що рухається).
- `+ui:range-circle` — коло дальності вибраної/привида вежі; `+ui:tower-panel` — панель апгрейд/продаж; `+ui:next-wave-button`.
- `+window:mode-select` — уже ⏳; тут Classic/Extended/Endless.
- `+feature:mode-endless` — уже ⏳; підтвердження.
- `+axis:session` — тут `match` (100 хвиль) і `endless` в одній грі.

## Джерела
- ⭐ [Wikipedia: Fieldrunners](https://en.wikipedia.org/wiki/Fieldrunners) — вільна розстановка, «вороги обходять вежі, не можна повністю перекрити», вежі по режимах, 8 мап, 100 хвиль / Endless, платформи.
- [Steam: Fieldrunners](https://store.steampowered.com/app/209690/Fieldrunners/) — PC-версія, 8 мап, наземні й повітряні вороги, апгрейди веж.
- [Steam: Fieldrunners 2](https://store.steampowered.com/app/215710/_Fieldrunners_2/) — сиквел.
- YouTube: пошук «fieldrunners gameplay».

## Непевне
- (?) Розмір сітки і скільки клітин займає вежа (2×2 чи 1×1).
- (?) Точний список ворогів (мотоцикли, танки, гелікоптери, дирижаблі) і хто з них повітряний.
- (?) Кількість життів на старті (20?) і чи коштують великі вороги більше одного.
- (?) Ціна продажу (частка вкладеного), кількість рівнів апгрейда, бонус за ранню хвилю, кнопка прискорення.
- (?) Характеристики Tesla/Missile (по яких цілях бʼють, сплеск).
