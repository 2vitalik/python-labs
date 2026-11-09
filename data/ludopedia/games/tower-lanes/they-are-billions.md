---
title: They Are Billions
slug: they-are-billions
aka: [TAB]
family: tower-lanes
also: [build-sim]
klass: cursor
axes:
  field: square
  time: realtime
  opponent: none
  info: hidden
  random: both
  goal: survive
year: 2019
platforms: [PC, PS4, Xbox One]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/They_Are_Billions", best: true, note: "8 ресурсів, стіни/турелі/пастки, дрібні атаки й орди за розкладом, фінальна орда, інфекція будівель, типи заражених, пауза"}
  - {kind: steam, url: "https://store.steampowered.com/app/644930/They_Are_Billions/", note: "real-time з паузою, Tesla-вежі розносять енергію, шум приваблює, один заражений у будівлі = зараження, Survival і кампанія"}
  - {kind: other, url: "https://www.magicgameworld.com/they-are-billions-how-to-survive-the-final-wave/", note: "гайд фінальної хвилі: усі йдуть до штабу, ≤2 ряди стін поспіль, пріоритети цілей"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=they+are+billions+survival+gameplay", note: "пошук; геймплей Survival"}
stage: v1
coverage: 50
mechanics: [tower-placement, tower-range, cursor-place, multi-select, impassable-cells, destructible-blocks, coverage-area, enemy-waves, spawn-schedule, spawn-random-cell, enemy-reached-base, round-currency, in-round-upgrades, hp-damage, projectile-shot, explode-area, melee-vs-ranged, speed-per-type, chase-bfs, random-walk, fog-of-war, minimap-radar, game-pause, difficulty-levels, sequential-levels, map-window, leaderboard, +infection-spread, +noise-attraction, +power-grid, +housing-workers, +real-time-pause, +final-wave, +wall-ring-defense, +target-priority]
proposes: ["+trigger:heard", "+effect:infect", "+cond:powered", "+cond:infected", "+role:base", "+role:building", "+ui:resource-bar", "+ui:day-counter", "+ui:horde-warning", "+window:research-tree", "+window:survival-setup", "+axis:time", "+card:infection-spread", "+card:noise-attraction", "+card:power-grid"]
author: opus
date: 2026-11-09
---

# They Are Billions — RTS-TD з паузою: оброби колонію стінами на сітці, бо один заражений у будинку запускає ланцюгову епідемію

## Суть
Гравець будує колонію на сітці процедурної мапи: житло, їжа, енергія, видобуток, потім периметр зі **стін, воріт, веж і пасток** і загін найманців. Мапою блукають тисячі заражених; вони йдуть на **шум**, атакують дрібними групами у випадкові моменти, а **орди** приходять за розкладом аж до фінальної. Ключ — **інфекція**: заражений, що увійшов у невійськову будівлю, перетворює мешканців, і ті розносять зараження далі. Гра real-time, але **пауза будь-коли** дозволяє віддавати накази й ставити будівлі без поспіху.

## Поле і час
- Квадратна сітка великої процедурної мапи (Survival): ліс, вода, гори, родовища (камінь, залізо, нафта), руїни й «Villages of Doom» із зараженими.
- `fog-of-war`: відкрито лише довкола своїх будівель і юнітів; мінімапа показує відкрите й велетнів.
- Real-time із паузою (RTwP); час рахується днями — орди за календарем (до фіналу) (?).
- Будівлі займають прямокутники клітинок; стіни — 1 клітинка, не більше двох рядів підряд (за гайдом).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Командний центр (штаб) | static (`+role:base`) | HP | дає стартові ресурси й енергію; усі орди йдуть до нього; знищено — поразка (?) |
| Житло (намет → хатина → дім) | static (`+role:building`) | колоністи, золото | заселяється, якщо є їжа; дає робітників і золото |
| Ферма / мисливець / рибалка | static | їжа | виробляє їжу з клітинок довкола |
| Лісопилка / каменоломня / шахта | static | ресурс | видобуває з клітинок поруч (ліс, камінь, залізо) |
| Tesla-вежа | static | радіус живлення | розносить енергію: будувати можна лише в покритій зоні |
| Млин / електростанція | static | енергія | виробляють енергію для мережі |
| Склад / ринок / банк | static | місткість, золото | збільшують ліміти й дохід (?) |
| Дерев'яна / кам'яна стіна | static | HP | непрохідна; заражені ламають |
| Ворота | gate | HP | свої юніти проходять, заражені — ні |
| Балісти / вежі / Executor | tower | дальність, шкода | стріляють по заражених у радіусі; в оглядову вежу садять юнітів (?) |
| Пастки (дерев'яні кілки, лезові) | hazard | — | шкодять тим, хто наступив |
| Ranger / Soldier / Sniper | ally | дальність, шум пострілу | найманці: обираються рамкою, накази рух/атака |
| Lucifer / Thanatos / Titan | ally | площа, шкода | вогнемет / ракети по площі / важкий робот |
| Заражений повільний | enemy | HP | блукає, йде на шум, атакує будівлі й людей |
| Harpy | enemy | швидкий | обганяє решту, пролазить у дірки (?) |
| Chubby | enemy | дуже міцний | танк орди |
| Infected Giant | boss | великі HP, швидкість, шкода | видно на мінімапі |
| Заражена будівля | spawner | — | з неї виходять нові заражені |
| Village of Doom | spawner | лут | грабуєш — отримуєш ресурси, але будиш рій |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(pause)` → ТО `custom: «час стоїть; дозволено ставити будівлі, віддавати накази, дивитися інформацію»`.
- КОЛИ `input(place, building, cells)` → ЯКЩО `free(cells)` and `custom: «cond powered(cells): у радіусі Tesla-вежі»` and `counter(resources, >=, cost)` and `counter(workers, >=, need)` → ТО `place(player, building)`, витрати; інакше `block`.
- КОЛИ `input(place, wall, cell)` → ЯКЩО `custom: «поруч менше двох рядів стін»` (?) → ТО `place(player, wall)`.
- КОЛИ `timer(every)` → ТО `custom: «житло з їжею заселяється → +колоністи, +робітники, +золото»`; `custom: «виробничі будівлі дають ресурс від клітинок поруч»`.
- КОЛИ `custom: «енергії або їжі не вистачає»` → ТО `set_state(building, unpowered)` — не працює.
- КОЛИ `input(select_box)` → ТО `custom: «обрати юніти рамкою»`; КОЛИ `input(move|attack, cell)` → ТО `custom: «загін іде шляхом (BFS/A*)»`.
- КОЛИ `in_range(unit|tower, infected, n)` → ТО `spawn(projectile)` → `damage(n)`; ціль — за пріоритетом `custom: «найближчий / найсильніший»`.
- КОЛИ `custom: «постріл, бій або видобуток створює шум»` → ТО `custom: «heard: заражені в радіусі шуму йдуть до джерела»`.
- КОЛИ `rng(p)` → ТО `spawn_at(infected_group, край туману)` — дрібна атака у випадковий момент.
- КОЛИ `schedule(дні орд)` → ТО `message(«орда з напрямку X»)`, `spawn_at(horde, край мапи)`; рух — `custom: «до командного центру»`.
- КОЛИ `custom: «фінальна орда»` → ТО `custom: «усі вцілілі заражені мапи приєднуються до штурму»`.
- КОЛИ `adjacent(infected, wall|tower)` → ТО `damage(n)`; `hp_zero` → `disappear`.
- КОЛИ `contact(infected, building)` → ЯКЩО not `custom: «військова будівля»` → ТО `custom: «infect: будівля заражена»`, `transform(building, infected_building)`.
- КОЛИ `timer(every)` біля зараженої будівлі → ТО `spawn_at(infected, будівля)` — мешканці стають зараженими й ідуть до сусідніх будівель (каскад).
- КОЛИ `contact(infected, unit)` → ТО `damage(n)`; `hp_zero(unit)` → `transform(unit, infected)`.
- КОЛИ `died(infected)` біля юніта → ТО `custom: «юніт набирає досвід (veteran)»` (?).
- КОЛИ `input(research, tech)` → ЯКЩО `counter(resources, >=, cost)` → ТО `unlock(tech)` (нові будівлі/юніти/апгрейди).
- КОЛИ `hp_zero(command_center)` → ТО `lose` (?).
- КОЛИ `counter(days, >=, survival_days)` → ЯКЩО `custom: «командний центр цілий»` → ТО `win`, `score(×множник складності)`.
- Перемога: Survival — пережити задану кількість днів і фінальну орду; кампанія — мета місії · Поразка: падіння штабу (?) · Рахунок: множник за налаштування складності (?).

## Керування і ввід
- Миша: ЛКМ — вибір/рамка, ПКМ — наказ; меню будівель знизу; гарячі клавіші для типів (?).
- Пробіл — пауза; на паузі можна будувати й віддавати накази (RTwP).
- Накази юнітам: рух, атака, утримання позиції, патруль; налаштування пріоритету цілей (найближчий / найсильніший).
- Розміщення: тінь будівлі на сітці; зелене/червоне за легальністю, підсвічена зона живлення Tesla (?).

## Вікна, меню, HUD
- `main-menu`: кампанія · Survival · Weekly Challenge · налаштування.
- `+window:survival-setup` — мапа, кількість заражених, тривалість у днях; разом дають множник рахунку (?).
- `map-window` — кампанія: мапа імперії з місіями, лабораторія досліджень, герой-місії.
- `+window:research-tree` — понад 90 технологій кампанії.
- `game-screen`: мапа з туманом, `minimap`, `+ui:resource-bar` (золото, їжа, робітники, енергія, дерево, камінь, залізо, нафта), `+ui:day-counter`, `+ui:horde-warning` (напрямок і час орди), панель обраного юніта/будівлі, меню будівель, `threat-range` вежі (?).
- `pause-menu` — окремо від «тактичної» паузи.
- `end-screen` — перемога/поразка, рахунок.
- Переходи: main-menu → survival-setup → game-screen → end-screen.

## Фічі поза полем
- `pause` з наказами (RTwP) — головна фіча доступності.
- `custom-difficulty`: розмір мапи, щільність заражених, тривалість Survival.
- Кампанія «The New Empire»: 48 місій, `map-window`, дослідження, герої.
- Weekly Challenge: однакова випадкова мапа для всіх + `leaderboard-online`.
- Збереження: у Survival — лише при виході (?).

## Варіації й родичі
- Survival vs кампанія (тактичні міні-місії з героєм, оборона залізничних колоній).
- Родичі: [rampart](rampart.md) і [locks-quest](locks-quest.md) (стіни-периметр), [creeper-world](creeper-world.md) (енергомережа + розповзання загрози), [anomaly-warzone-earth](anomaly-warzone-earth.md), Age of Empires / StarCraft (RTS), Diplomacy is Not an Option (наступник ідеї), Factorio (нерест «кусак» на шум забруднення).
- **Осі варіацій**: загроза — по шляху / блукає й іде на шум · прорив — мінус життя / ланцюгова інфекція · пауза — нема / пауза з наказами · база — точка-ціль / уся колонія з економікою.

## Цікавинки для курсу
- Інфекція як каскад: заражена будівля стає генератором, мешканці йдуть до сусідніх — BFS-епідемія на графі будівель — 🥈.
- Шум як приманка: подія створює коло, усі заражені всередині змінюють ціль — 📎.
- Енергомережа: Tesla-вежі з радіусом, будувати лише в покритті; брак — будівлі вимикаються — 🥉.
- RTwP: пауза, на якій працюють будування й накази, — розділення «логіка тіку» / «ввід» — 🥉.
- Тисячі ворогів з AI — потік (flow field) до штабу замість A* для кожного — 🥇.
- Розклад орд за днями з попередженням напрямку + фінальна орда, що збирає всіх уцілілих — 📎.
- Обмеження «≤2 ряди стін підряд» як правило легальності розміщення — 🌱.

## Мапа на каталог
- Є: `tower-placement`, `tower-range`, `cursor-place` · `multi-select` ↔ рамка юнітів · `impassable-cells`, `destructible-blocks` ↔ стіни · `coverage-area` ↔ Tesla-радіус · `enemy-waves`, `spawn-schedule` ↔ орди, `spawn-random-cell` ↔ випадкові атаки · `enemy-reached-base` ↔ штаб · `round-currency`, `in-round-upgrades` ↔ дослідження · `hp-damage`, `projectile-shot`, `explode-area`, `melee-vs-ranged`, `speed-per-type` · `chase-bfs`, `random-walk` ↔ блукання заражених · `fog-of-war`, `minimap-radar`, `game-pause` · `difficulty-levels`, `sequential-levels`, `map-window`, `leaderboard`.
- **Нема** → пропозиції карток:
  - `+infection-spread` «Заражена будівля стає генератором ворогів» · entities/spawn · 🥈.
  - `+noise-attraction` «Шум приваблює ворогів у радіусі» · entities/move · 📎.
  - `+power-grid` «Мережа енергії: будівництво лише в покритті, брак вимикає» · game-logic/economy · 🥉.
  - `+housing-workers` «Житло + їжа → робітники, що потрібні будівлям» · game-logic/economy · 📎.
  - `+real-time-pause` «Пауза з наказами (RTwP)» · game-logic/difficulty · 🥉.
  - `+final-wave` «Фінальна хвиля збирає всіх уцілілих ворогів» · game-logic/waves · 🌱.
  - `+wall-ring-defense` «Периметр стін: прорив = поразка» · game-logic/lose · 📎.
  - `+target-priority` «Налаштування пріоритету цілей вежі/юніта» · entities/combat · 🌱.

## Пропозиції до словників
- `+trigger:heard` — сутність почула шум у радіусі (зміна цілі).
- `+effect:infect` — будівля/юніт переходить на бік ворога і стає генератором (≈ `set_side` + `transform`, але з каскадом).
- `+cond:powered` — клітинка в зоні енергомережі; `+cond:infected` — будівля заражена.
- `+role:base` — штаб: ціль орд; `+role:building` — споруда економіки (не вежа, не стіна).
- `+ui:resource-bar` — рядок ресурсів; `+ui:day-counter` — дні до кінця; `+ui:horde-warning` — напрямок і час орди.
- `+window:research-tree`, `+window:survival-setup` — дерево технологій; налаштування Survival з множником.
- `+axis:time` — значення `rtwp` (real-time з паузою для наказів).
- `+card:infection-spread`, `+card:noise-attraction`, `+card:power-grid` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: They Are Billions](https://en.wikipedia.org/wiki/They_Are_Billions) — 8 ресурсів, стіни/турелі/вежі/пастки, дрібні атаки у випадкові моменти й орди за розкладом із фінальною, інфекція «доміно», типи заражених (Harpy, Chubby, Giant), Villages of Doom, пауза з наказами.
- [Steam: They Are Billions](https://store.steampowered.com/app/644930/They_Are_Billions/) — RTwP, Tesla-вежі й енергія, житло + їжа, найманці за золото і їжу, шум, «один заражений у будівлі», до 20 000 юнітів, Survival і кампанія (48 місій, 90+ технологій).
- [MagicGameWorld: фінальна хвиля](https://www.magicgameworld.com/they-are-billions-how-to-survive-the-final-wave/) — усі йдуть до штабу, ≤2 ряди стін поспіль, пріоритети цілей, Thanatos, балісти за енергію.
- YouTube: пошук «they are billions survival gameplay».

## Непевне
- (?) Поразка — саме знищення командного центру (гайди натякають, Wikipedia не каже).
- (?) Тривалості Survival у днях, дні орд, множник рахунку за налаштування — не бачив у відкритому джерелі.
- (?) Розміри будівель у клітинках; чи стіни справді обмежені двома рядами (гайд) і чи вежа стріляє крізь 5 рядів.
- (?) Досвід юнітів (veterans), «збереження лише при виході» в Survival.
- (?) Оглядова вежа з юнітом усередині; лезові пастки — назви з памʼяті.
- (?) Як саме поширюється інфекція з будівлі (таймер, кількість мешканців).
