---
title: The Last Spell
slug: the-last-spell
aka: [TLS]
family: tactics
also: [build-sim, tower-lanes]
klass: figure
axes:
  field: square
  time: turn
  opponent: ai
  info: partial
  random: both
  goal: survive
year: 2023
platforms: [PC, Switch, PS4, PS5]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/The_Last_Spell", best: true, note: "цикл день/ніч, магічне коло, дії від зброї, Omens, мета-прогресія, DLC"}
  - {kind: steam, url: "https://store.steampowered.com/app/1105670/The_Last_Spell/", note: "AP, оборонні споруди (стіни, пастки, вежі, катапульти), 5 міст, 6 рівнів Apocalypse"}
  - {kind: official, url: "https://lastspell.com/?p=647", note: "дев-блог #6: статистики героїв, формула шкоди (Accuracy звужує діапазон, Block, Armor, Resistance, Dodge)"}
  - {kind: other, url: "https://www.thegamer.com/the-last-spell-beginner-tips-tricks-strategies/", note: "поради: робітники, шахти/збирачі, Mist-лінія, undo одного руху, Oraculum, Omen-слоти"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=The+Last+Spell+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [hp-damage, melee-vs-ranged, explode-area, status-effects, reachable-highlight, hover-highlight, destroy-all-enemies, enemy-waves, progress-acceleration, unit-xp-skills, inventory-items, shop-between-levels, shop-catalog, round-currency, tower-placement, destructible-blocks, world-map, difficulty-levels, undo-step, save-autosave, game-screen, end-screen, +action-points, +movement-points, +day-night-cycle, +town-building, +worker-assignment, +protect-core, +damage-range-accuracy, +armor-layer, +weapon-grants-skills, +weapon-swap, +run-modifiers, +meta-progression, +mist-line, +wound-slows, +elite-enemies, +boss-night]
proposes: ["+trigger:day_start", "+trigger:night_start", "+role:building", "+role:core", "+effect:build", "+effect:repair", "+effect:assign_worker", "+effect:recruit", "+effect:swap_weapons", "+cond:beyond_mist", "+cond:mp", "+ui:ap-mp-banner", "+ui:worker-counter", "+ui:night-counter", "+window:omen-select", "+window:recruit-window", "+window:night-report", "+window:meta-tree", "+feature:run-modifiers", "+card:protect-core"]
author: opus
date: 2026-11-09
---

# The Last Spell — вдень відбудуй місто, вночі втримай магічне коло проти орди на клітинах

## Суть
Кілька героїв захищають **магічне коло** в центрі міста, доки маги не дочитають останнє закляття. Гра чергує дві фази: **день** — економіка й будування (гроші, матеріали, робітники, стіни, вежі, найм), **ніч** — покрокова битва на квадратній сітці проти сотень нежиті, що суне до кола. Навмисна асиметрія: 2–3 героя проти орди, тож ядро — ефективність кожного Action Point і зональний контроль (AoE, стіни, вузькі проходи). Дії героя дає **зброя**, а не клас; класи складаються з перків і спорядження.

## Поле і час
- Квадратна сітка в 2D-ізометрії; у центрі — магічне коло, навколо — будівлі міста; з країв мапи приходить орда (?).
- **Mist** — лінія на полі: ворогів за нею не можна атакувати, вони «поза досяжністю»; орда виходить з туману.
- Цикл мапи-міста: N пар «день → ніч», остання ніч — бос; число ночей фіксоване для міста.
- Ніч: хід гравця (усі герої в довільному порядку, витрачаючи AP/MP) → хід орди (усі вороги рухаються до кола й атакують усе в радіусі: героїв, будівлі, стіни, коло). Кожна наступна ніч важча.
- День: без сітки ходів — екран міста; дві підфази (будування/виробництво і розставлення оборони) (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой | piece | Health, Mana, AP, MP, Armor, Block, Resistance, Dodge, Accuracy, Crit, Phys+/Mag+ | рух за MP (1 клітина = 1 MP), навички зброї за AP; два набори зброї (перемикання) |
| Магічне коло | static | HP | ціль орди; знищене → поразка міста |
| Будівля міста | static | HP, рівень | ворог може зруйнувати; вдень — ремонт/апгрейд |
| Шахта | spawner | — | дає золото (за робітників) |
| Збирачі (Scavengers) | spawner | — | дають матеріали для будування |
| Село / житло | static | — | дає робітників; апгрейд розширює їхні можливості |
| Таверна (Inn) | static | — | найм нових героїв |
| Кузня / зброярня / храм | static | — | крафт і купівля зброї, броні, зілля |
| Стіна / брама | static | HP | блокує шлях орди; ворог бʼє її |
| Вежа, катапульта, балiста | ally | дальність | стріляє в нічну фазу; на вежу ставлять героя (?) |
| Пастка (Seeds у DLC ельфів) | hazard | — | спрацьовує в хід ворогів |
| Clawer / ближній бієць | enemy | HP, Armor | іде до кола, бʼє сусіда |
| Runner | enemy | швидкий | обходить, дістається будівель |
| Archer / Spitter | enemy | дальність | стріляє здалеку |
| Ghost / маг | enemy | магія | ігнорує частину захисту (?) |
| Elite | enemy | посилений | рідкісний, з особливою властивістю |
| Бос | boss | фази (?) | остання ніч міста |
| Mist | zone | — | за лінією ворог недосяжний |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `phase_start(day)` → ТО `custom: «нараховано золото/матеріали з шахт і збирачів за робітників»`, `heal(hero, частково)` і `custom: «часткове відновлення мани»`, `custom: «level up за XP минулої ночі → вибір перка»`.
- КОЛИ `input(build, cell, building)` → ЯКЩО `has(player, gold)` і `has(player, materials)` → ТО `place(building)`, `currency(−price)`.
- КОЛИ `input(assign, worker, building)` → ЯКЩО `has(player, worker)` → ТО `custom: «робітник виробляє ресурс/дію цієї будівлі»`.
- КОЛИ `input(recruit, inn)` → ЯКЩО `has(player, gold)` → ТО `spawn(hero)` з випадковими статами й спорядженням.
- КОЛИ `input(buy|craft, item)` → ЯКЩО `has(player, gold)` → ТО `give(hero, item)`, `currency(−price)`.
- КОЛИ `phase_start(night)` → ТО `spawn_at(horde, edge)`; склад — випадкова суміш типів; `custom: «складність росте з номером ночі»`.
- КОЛИ `turn_start(player)` → ТО `custom: «AP і MP героїв відновлюються до максимуму»`, `custom: «Armor регенерує»` (?).
- КОЛИ `input(move, hero, cell)` → ЯКЩО `custom: «MP ≥ довжина шляху»` і `free(cell)` → ТО `move`, `counter(MP, −клітин)`.
- КОЛИ `input(skill, target)` → ЯКЩО `custom: «AP ≥ ціна і Mana ≥ ціна»` і `in_range(hero, target, n)` → ТО `damage(n)` по зоні навички, `counter(AP, −ціна)`.
- Шкода: `custom: «база minmax → Accuracy підтягує мінімум до максимуму (влучання завжди) → −Resistance% (лише фізична) → −Block → спершу знімає Armor, потім Health»`; `prob(Crit)` → `custom: «×2»`; `prob(Dodge)` → `block`.
- КОЛИ `input(skill, target)` → ЯКЩО `custom: «ціль за лінією Mist»` → ТО `block`.
- КОЛИ `input(swap_weapons)` → ТО `custom: «інший набір навичок»` (Tab).
- КОЛИ `input(undo)` → ЯКЩО `custom: «останній рух і ще не атакував»` → ТО `custom: «повернути героя»`.
- КОЛИ `damage(enemy)` → ЯКЩО `not hp_zero` → ТО `custom: «поранення знижує рух і шкоду ворога»`.
- КОЛИ `turn_end(player)` → ТО `custom: «кожен ворог рухається до кола»`; КОЛИ `in_range(enemy, target, n)` → ТО `damage(n)` по героєві / будівлі / стіні / колу.
- КОЛИ `blocked(enemy)` стіною → ТО `custom: «бʼє стіну»` (?); `hp_zero(wall)` → `disappear_b`.
- КОЛИ `turn_end(enemy)` → ЯКЩО `occupied(cell, trap)` → ТО `damage(n)` (DLC Seeds).
- КОЛИ `hp_zero(hero)` → ТО `disappear_a` (?) — герой гине для забігу.
- КОЛИ `all_gone(enemy)` → ТО `custom: «ніч виграно»`, `currency(+gold)`, `give(player, items)` → `phase_start(day)`.
- КОЛИ `hp_zero(magic_circle)` → ТО `lose` (місто втрачено).
- КОЛИ `all_gone(boss)` на останній ночі → ТО `win` (місто захищене) → `window(map-window)`.
- КОЛИ `game_over` (перемога чи поразка) → ТО `custom: «мета-валюта за вбитих і пережиті ночі»`; `custom: «Feats of Prowess за міні-цілі (герой з 300 HP тощо)»`.
- Перемога: пережити всі ночі й убити боса · Поразка: магічне коло знищене · Рахунок: — (нагорода мета-валютою).

## Керування і ввід
- Миша: клік на героя → підсвічені досяжні клітини (зелений = MP), клік на клітину → рух; клавіші 1–0 — навички, наведення показує зону ураження; Tab — інший набір зброї.
- Банер у правому верхньому куті — AP (помаранчевий) і MP (зелений) обраного героя.
- Кнопка кінця ходу → хід орди (анімація всіх ворогів).
- День: клік на будівлі (будувати, апгрейдити, призначити робітника), панелі магазину й таверни, екран героя (спорядження drag-and-drop, перки).
- Undo — лише останній рух до атаки.

## Вікна, меню, HUD
- `main-menu`: Нова гра → `map-window` (вибір міста: Swampfurt-туторіал, Gildenberg, Lakeburg, Glenwald, Elderlitch, DLC Runenberg/Amberwald) · Продовжити · Налаштування → `settings-window` · Вихід.
- `custom-window` «Omens» — вибір бонусів у слоти міста (кожен Omen займає кілька слотів; Boundless-режим знімає ліміт); вибір рівня Apocalypse → `difficulty-select`.
- `game-screen` (ніч): сітка з містом, `reachable-highlight`, `threat-range` навички, `hp-bar` над сутностями, `action-points` (AP/MP-банер), `skill-bar`, `turn-counter` ночі (?), `end-turn-button`.
- `game-screen` (день): місто з будівлями, лічильники золота/матеріалів/робітників, кнопки будівель.
- `shop-window` (крамниця/кузня), `custom-window` «Inn» (найм), `inventory-window` (спорядження героя), `upgrade-window` (перки при level up).
- `end-screen` — звіт ночі (вбиті, нагороди) / поразка міста / перемога над босом.
- `custom-window` «Oraculum» — мета-дерево (Богиня Темряви за Tainted Essence; Богиня Світла за Feats of Prowess).
- Переходи: main-menu → map-window → Omens → день ↔ ніч ×N → бос → end-screen → map-window / Oraculum.

## Фічі поза полем
- `meta-progression`: мета-валюта відкриває Omens, зброю, броню, будівлі; постійні бафи всім героям.
- `world-map`: 5 міст + DLC-мапи, кожне з власною розстановкою; повтор міста на вищому Apocalypse (`difficulty-presets`, 6 рівнів).
- `achievements` (Steam), `cloud-save`, `autosave` між фазами (?).
- Run-модифікатори (Omens) — бонуси на всю мапу (+MP, +шкода, більше героїв, кращий лут).
- DLC: дварфи (Runestones, Stone Medals), ельфи (Seeds — пастки, що спрацьовують у хід ворога).

## Варіації й родичі
- Родичі: Into the Breach (захист будівель, але наміри відомі), Kingdom Rush / TD (орда до ядра), They Are Billions (день-ніч і стіни в real-time), Darkest Dungeon (місто між вилазками), Battle Brothers / XCOM (ростер і спорядження).
- **Осі варіацій**: ворогів — жменька (більшість тактик) / орда сотнями · ціль — знищити ворога / втримати ядро N ночей · між боями — меню / будування на тій самій мапі · влучання — шанс (XCOM) / завжди влучає, змінюється діапазон шкоди (TLS).

## Цікавинки для курсу
- Цикл «день — будуємо на тій самій мапі, ніч — ця мапа стає полем бою» — 🥈 (два режими однієї сітки, стан будівель переходить).
- Орда з сотень ворогів, що кожна йде до кола й бʼє найближче в радіусі — 🥉 (BFS/потенціальне поле до цілі один раз на хід).
- Формула шкоди «діапазон → Accuracy звужує → Resistance → Block → Armor → Health» — 📎 (конвеєр модифікаторів, легко тестувати).
- AP + MP як два окремі бюджети ходу, навички від зброї, перемикання сетів — 📎.
- Стіни, що ворог мусить пробити, і вежі зі стрільбою — 🥉 (місток з TD).
- Mist-лінія як межа досяжності атак — 🌱.
- Omens зі слотами різної ваги перед забігом — 📎 (рюкзак-задача на модифікаторах).

## Мапа на каталог
- Є: `hp-damage` · `melee-vs-ranged` · `explode-area` (AoE навичок) · `status-effects` (отрута, поранення) · `reachable-highlight` · `hover-highlight` · `destroy-all-enemies` (ніч) · `enemy-waves` + `progress-acceleration` (ніч за ніччю важче) · `unit-xp-skills` · `inventory-items` · `shop-between-levels` + `shop-catalog` · `round-currency` (золото/матеріали) · `tower-placement` (вежі, катапульти) · `destructible-blocks` (стіни, будівлі) · `world-map` · `difficulty-levels` (Apocalypse) · `undo-step` · `save-autosave` (?) · `game-screen` · `end-screen`.
- **Нема** → пропозиції карток:
  - `+day-night-cycle` «Дві фази однієї мапи: будування і бій» · game-logic/waves · 🥈.
  - `+protect-core` «Захисти ядро: поразка, коли ціль у центрі знищена» · game-logic/lose · 🌱.
  - `+town-building` / `+worker-assignment` «Будівлі й робітники між боями» · game-logic/economy · 🥉.
  - `+damage-range-accuracy` «Точність звужує діапазон шкоди, без промахів» · entities/combat · 🌱.
  - `+armor-layer` «Шар броні, що з'їдається перед HP і регенерує» · entities/state · 🌱.
  - `+weapon-grants-skills` / `+weapon-swap` «Навички від зброї, два сети» · entities/state · 📎.
  - `+run-modifiers` «Модифікатори забігу зі слотами» · game-logic/difficulty · 📎.
  - `+meta-progression` «Постійні відкриття між забігами» · game-logic/economy · 📎.
  - `+mist-line` «Межа, за якою атаки неможливі» · interface/render · 🌱.
  - `+wound-slows` «Поранений ворог повільніший і слабший» · entities/state · 🌱.
  - `+elite-enemies` / `+boss-night` — рідкісні посилені вороги, бос останньої ночі · 📎.
  - `+action-points` / `+movement-points` — спільні з XCOM і корпусом.

## Пропозиції до словників
- `+trigger:day_start` / `+trigger:night_start` — початок фази циклу (уточнення ⏳ `phase_start`).
- `+role:building` — будівля міста з HP і функцією; `+role:core` — сутність, загибель якої = поразка (магічне коло, База в TD).
- `+effect:build` / `+effect:repair` — поставити / відновити будівлю за ресурси; `+effect:assign_worker` — призначити робітника; `+effect:recruit` — найняти юніт; `+effect:swap_weapons` — змінити набір навичок.
- `+cond:beyond_mist` — ціль за лінією туману; `+cond:mp` — вистачає очок руху.
- `+ui:ap-mp-banner` — два лічильники бюджету ходу; `+ui:worker-counter` · `+ui:night-counter` — ніч N з M.
- `+window:omen-select` — вибір модифікаторів у слоти; `+window:recruit-window` — найм; `+window:night-report` — підсумок ночі; `+window:meta-tree` — дерево мета-відкриттів (Oraculum).
- `+feature:run-modifiers` — модифікатори забігу; `+card:protect-core`.

## Джерела
- ⭐ [Wikipedia: The Last Spell](https://en.wikipedia.org/wiki/The_Last_Spell) — день/ніч, магічне коло, дії від зброї, орда, Omens, мета-прогресія, DLC, дати.
- [Steam](https://store.steampowered.com/app/1105670/The_Last_Spell/) — AP, AoE/контроль/отрута, Elites, бос кожної мапи, стіни/пастки/вежі/катапульти, 5 міст, 6 Apocalypse.
- [Дев-блог #6 «Heroes Stats»](https://lastspell.com/?p=647) — Health/Mana/AP/MP, Accuracy як звуження діапазону, Crit ×2, Block, Armor, Resistance, Dodge, приклад розрахунку.
- [TheGamer: beginner tips](https://www.thegamer.com/the-last-spell-beginner-tips-tricks-strategies/) — робітники, шахти, збирачі, таверна, Mist, undo одного руху, Oraculum, Богині Світла/Темряви, слоти Omens.
- YouTube: пошук «The Last Spell gameplay».

## Непевне
- (?) Стартова кількість героїв: Wikipedia — три, TheGamer — два (може залежати від Omens/версії).
- (?) Регенерація Armor щоходу — з дев-блогу раннього доступу; у релізі могло змінитись.
- (?) Чи гинуть герої остаточно в межах забігу, чи лише виходять з бою — не перевірено.
- (?) Точні назви й ефекти будівель (храм, зброярня, вежі, балісти) і чи ставлять героя на вежу — частково з памʼяті.
- (?) Звідки приходить орда (краї мапи) і як вороги поводяться перед стіною — з памʼяті.
- (?) Поділ дня на «виробництво» і «розставлення» — з памʼяті.
- (?) Panic (паніка міста, що зменшує нагороди) — є в грі за памʼяттю, у джерелах не підтверджено, тому не описано.
