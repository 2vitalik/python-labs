---
title: Kingdoms and Castles
slug: kingdoms-and-castles
aka: [K&C, KaC]
family: build-sim
also: [tower-lanes]
klass: cursor
axes:
  field: square
  time: realtime
  opponent: ai
  info: full
  random: both
  goal: survive
year: 2017
platforms: [PC, Mac, Linux, Xbox One, Xbox Series, PS4, PS5]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Kingdoms_and_Castles", best: true, note: "ресурси, селяни як обмежений ресурс, зима, блискавки, чума, дракони/вікінги/огри, дипломатія"}
  - {kind: steam, url: "https://store.steampowered.com/app/569480", note: "замок із блоків, вежі ростуть у дальності з висотою, вікінги крадуть і палять, дракон палить зерносховище, редактор, Workshop"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Kingdoms+and+Castles+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [cursor-place, multi-cell-size, impassable-cells, coverage-area, height-levels, tower-placement, tower-range, enemy-waves, spawn-schedule, hp-damage, chase-greedy, projectile-shot, round-currency, in-game-editor, level-exchange, save-autosave, field-scaling, player-camera, hover-highlight, cell-click, +context-tile-rules, +fertility-yield, +seasonal-wipe, +stacked-castle-blocks, +height-range-bonus, +disaster-events, +worker-pool, +tax-happiness-tradeoff, +sustainable-forestry]
proposes: ["+trigger:season(s)", "+cond:fertility(cell, op, n)", "+effect:burn(building)", "+effect:kidnap(raider, peasant)", "+ui:resource-overlay", "+feature:disaster-toggles", "+card:fertility-yield", "+card:stacked-castle-blocks"]
author: opus
date: 2026-11-09
---

# Kingdoms and Castles — місто на клітинах, де ферми люблять родючу землю, а замок складається з блоків, що самі стають стінами й вежами

## Суть
Гравець ставить на клітинний острів замок, житла, ферми, лісорубів і каменоломні; селяни — обмежений ресурс, що розходиться по роботах. Економіка тримається на їжі, деревині, камені й золоті з податків. Зверху — **сезони** (щорічна зима знищує посіви), лиха (блискавка → пожежа, чума) і **набіги**: вікінги з моря, дракони з неба, огри. Оборона будується як «конструктор»: блоки замку можна класти будь-де, стіни й вежі формуються автоматично з того, як їх складено, а вежі лучників бʼють далі, коли вищі.

## Поле і час
- Поле — квадратна сітка острова (?), процедурно згенерована; клітини: суходіл, вода, ліс, камінь, залізо, родюча земля (?).
- Будівлі займають N×N клітин (житло, ферма, замкова вежа — різні розміри) (?); дороги — 1 клітина.
- Блоки замку **складаються у висоту** (стовпчики), тож поле фактично має висоту на клітині.
- Час — real-time з паузою й прискоренням (?); рік ділиться на сезони «літо → зима».
- Камера — вільна 3D над мапою (pan/zoom/обертання).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Замок (Keep) | static | стартова будівля | ставиться першим; поруч бажано родюча земля й залізо |
| Селянин | neutral | 1 одиниця робочої сили, щастя | йде на вільне робоче місце; їсть; хворіє; може бути вкрадений вікінгами |
| Житло (хатина / камʼяний дім) | static | місткість | збільшує населення; більший дім потребує каменю |
| Ферма | static | N×N (?) | дає їжу; врожай залежить від родючості клітин (?); зима знищує неприбраний урожай |
| Зерносховище | container | запас їжі | зберігає їжу; ціль дракона |
| Лісоруб (Forester) | static | радіус (?) | рубає дерева і **садить нові**; режим вирубки «під корінь» або сталий |
| Каменоломня | static | на камінь-клітині | дає камінь (житла, замок) |
| Шахта заліза | static | на залізі (?) | залізо для зброї/солдатів (?) |
| Дерево / камінь / залізо | resource | запас клітини | вичерпується видобутком; дерева відростають, якщо їх садять |
| Церква, таверна, міська площа | static | радіус впливу (?) | підтримують щастя; площа дає свята |
| Податки | resource | ставка | золото на зарплати й відкриття будівель; висока ставка → невдоволення |
| Блок замку (дерево/камінь) | static | висота стовпчика | сусідні блоки зливаються в стіну; кутові/високі — у вежу |
| Вежа лучників | tower | дальність росте з висотою | стріляє в найближчого ворога в радіусі |
| Баліста (?) | tower | — | бʼє по драконах/кораблях (?) |
| Солдати / казарма | ally | HP | рекрутуються, атакують нападників |
| Вікінг-рейдер | enemy | HP | висаджується з човна; викрадає/вбиває селян, краде ресурси, підпалює |
| Дракон | enemy | HP, літає | палить будівлі (зерносховище); його можна відігнати |
| Огр | enemy | HP | атакує місто з суходолу (?) |
| Пожежа | hazard | поширюється (?) | від блискавки/дракона; знищує будівлю |
| Чума | hazard | — | селяни хворіють; потрібне лікування |
| Сусіднє AI-королівство | neutral | дипломатія | союз, торгівля або війна (якщо дипломатію ввімкнено) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(place, building, cell)` → ЯКЩО `fits(building, cell)` і `has(player, cost)` → ТО `place(player, building)`, `take(player, cost)`; інакше `block`.
- КОЛИ `input(place, castle_block, cell)` → ТО `place(player, castle_block)`, `custom: «перерахувати форму: ланцюжок блоків → стіна, стовпчик/кут → вежа»`.
- КОЛИ `custom: «зʼявилось вільне робоче місце»` → ЯКЩО `count(idle_peasant, >, 0)` → ТО `custom: «селянин іде працювати»`.
- КОЛИ `timer(harvest)` → ЯКЩО `occupied(farm, peasant)` → ТО `counter(food, +yield)`, `custom: «yield залежить від родючості клітин ферми»` (?).
- КОЛИ `custom: «настала зима»` → ТО `custom: «неприбрані посіви знищено»`; селяни їдять зі сховищ.
- КОЛИ `timer(meal)` → ЯКЩО `counter(food, ==, 0)` → ТО `damage(peasant, n)` (голод) (?).
- КОЛИ `timer(tax)` → ТО `currency(+rate × population)`; ЯКЩО `custom: «ставка вища за поріг»` → ТО `custom: «щастя падає»`.
- КОЛИ `counter(happiness, <, n)` → ТО `custom: «селяни йдуть / не приходять нові»` (?).
- КОЛИ `input(chop, forester)` → ЯКЩО `mode(sustainable)` → ТО `set_cell(cell, sapling)` після вирубки; інакше `set_cell(cell, ground)`.
- КОЛИ `rng(p)` (гроза) → ТО `spawn_at(fire, building)`; КОЛИ `tick` → ЯКЩО `occupied(cell, fire)` → ТО `damage(building, n)` → `hp_zero` → `disappear(building)`.
- КОЛИ `rng(p)` (чума) → ТО `set_state(peasant, sick)`; ЯКЩО `custom: «нема лікування»` → ТО `disappear(peasant)` (?).
- КОЛИ `schedule(raids)` → ТО `spawn_at(viking_boat, sea_edge)`; КОЛИ `reach(viking, shore)` → ТО `custom: «вікінги висаджуються і йдуть до найближчих селян/запасів»`.
- КОЛИ `adjacent(viking, peasant)` → ТО `custom: «викрасти або вбити селянина»`; КОЛИ `adjacent(viking, building)` → ТО `custom: «підпалити»`, `spawn_at(fire, building)`.
- КОЛИ `schedule(dragon)` → ТО `spawn_at(dragon, edge)`; КОЛИ `in_range(dragon, granary, r)` → ТО `spawn_at(fire, granary)`.
- КОЛИ `in_range(archer_tower, enemy, r)` → ТО `damage(enemy, n)`; `r` = `custom: «базова дальність + бонус за висоту стовпчика»`.
- КОЛИ `hp_zero(enemy)` → ТО `disappear(enemy)`; дракон при низькому HP відлітає (?).
- Поразка: `custom: «нема явної поразки — місто вимирає (0 селян)»` (?) · Перемога: нема, гра нескінченна (`goal: survive`).

## Керування і ввід
- Миша: вибір будівлі на нижній панелі → привид на сітці (червоний — не можна) → клік; обертання будівлі клавішею (?).
- Дороги — протягування лінії; знесення — інструмент «зруйнувати».
- Замок — пензель блоків: клік ставить блок, клік на блок — додає висоту (?).
- Клік по будівлі — панель: працівники, режим (лісоруб: сталий/вирубка), апгрейд.
- Ставка податку — слайдер; камера WASD/миша.

## Вікна, меню, HUD
- `main-menu`: Нова гра (налаштування мапи й лих), Завантажити, Налаштування, Workshop/редактор.
- `match-setup` (`custom-window`): тип/розмір острова, чи вмикати дипломатію, частота набігів (?).
- `game-screen`: мапа; ресурси вгорі (їжа, деревина, камінь, золото, населення, щастя); `timer-elapsed` з роком і сезоном (?); панель будівель знизу.
- HUD: `resource-overlay` (родючість, щастя, покриття церквою — перемикач шарів) (?), `toast` про набіги й пожежі, `threat-range` вежі при виборі.
- `custom-window` дипломатії: сусіди, торгівля, союз, війна.
- `pause-menu`, `settings-window`, `save-slots`.
- `editor-window` — редактор мап (Steam: level editor) → Workshop.

## Фічі поза полем
- `level-editor` + `level-sharing` через Steam Workshop; `cloud-save`, `achievements`.
- `custom-difficulty`: які лиха й вороги ввімкнені (?), дипломатія як перемикач.
- `localization` (18 мов), `speed-control` (?).

## Варіації й родичі
- Натхнення: SimCity ([simcity-1989](simcity-1989.md)), Banished, Stronghold. Родичі в корпусі: [caesar-3](caesar-3.md) (покриття сервісами), [frostpunk](frostpunk.md) (зима як тиск), [townscaper](townscaper.md) (блоки, що самі обирають форму), [stardew-farm](stardew-farm.md) (сезони й ферми), [clash-of-clans-base](clash-of-clans-base.md) (оборона від AI-нападників).
- **Осі варіацій**: загроза (немає / хвилі / випадкові лиха) · урожай (рівний / за родючістю / з виснаженням) · стіни (окремий тип / автоформа з блоків) · ліс (вичерпний / відновлюваний).

## Цікавинки для курсу
- Автоформа замку: блок дивиться на сусідів і висоту, щоб стати стіною/вежею — 🥉 (контекстні плитки + висота).
- Дальність вежі = база + висота стовпчика — 🌱.
- Родючість клітин як множник урожаю ферми N×N — 📎.
- Сезонний цикл, де зима «стирає» незібране — 📎 (стан поля за календарем).
- Пожежа, що поширюється на сусідні будівлі — 📎 (клітинний автомат на будівлях).
- Пул селян як робоча сила, що сама розходиться на вакансії — 🥉.
- Вікінг із пріоритетом цілі «селянин → запас → підпал» — 📎.

## Мапа на каталог
- Є: `cursor-place` · `multi-cell-size` ↔ будівлі N×N · `impassable-cells` ↔ вода/скелі · `coverage-area` ↔ церква/таверна · `height-levels` ↔ стовпчики блоків · `tower-placement` + `tower-range` ↔ вежі лучників · `enemy-waves` + `spawn-schedule` ↔ набіги · `hp-damage` · `chase-greedy` ↔ вікінги до найближчої цілі · `projectile-shot` ↔ стріли · `round-currency` ↔ золото · `in-game-editor` + `level-exchange` ↔ редактор + Workshop · `save-autosave` · `field-scaling` · `player-camera` · `hover-highlight` · `cell-click`.
- **Нема** → пропозиції карток:
  - `+fertility-yield` «Родючість клітин множить вихід будівлі» · entities/state · 📎 · слот {fertility_levels}.
  - `+seasonal-wipe` «Сезон стирає частину стану поля» · game-logic · 📎.
  - `+stacked-castle-blocks` «Блоки, що за сусідами й висотою стають стіною/вежею» · entities/state · 🥉 — дитина `+context-tile-rules`.
  - `+height-range-bonus` «Дальність вежі росте з висотою» · entities/combat · 🌱 — дитина `tower-range`.
  - `+disaster-events` «Випадкові лиха: блискавка, чума, пожежа» · game-logic/waves · 📎.
  - `+worker-pool` «Спільний пул робочої сили, що розходиться по вакансіях» · game-logic/economy · 🥉.
  - `+tax-happiness-tradeoff` «Податок проти щастя» · game-logic/economy · 🌱.
  - `+sustainable-forestry` «Видобуток з відновленням (садити після рубки)» · entities/state · 🌱.
  - `+context-tile-rules` — повторно (Townscaper, CoC).

## Пропозиції до словників
- `+trigger:season(s)` — почався сезон (зима, весна) — календарний тригер, не `timer`.
- `+cond:fertility(cell, op, n)` — родючість клітини порівняно з N.
- `+effect:burn(building)` — підпалити (стан «горить» із поширенням); зараз `spawn_at(fire)` + custom.
- `+effect:kidnap(raider, peasant)` — нападник забирає сутність з поля (вікінги).
- `+ui:resource-overlay` — перемикач шарів мапи (родючість, щастя, покриття).
- `+feature:disaster-toggles` — увімкнути/вимкнути окремі лиха й ворогів перед грою.
- `+card:fertility-yield`, `+card:stacked-castle-blocks` — див. вище.

## Джерела
- ⭐ [Wikipedia: Kingdoms and Castles](https://en.wikipedia.org/wiki/Kingdoms_and_Castles) — ресурси (їжа, деревина, камінь, золото), селяни як ресурс, щорічна зима знищує посіви, блискавка/пожежі, чума, дракони/вікінги/огри, дипломатія, платформи й дати.
- [Steam: Kingdoms and Castles](https://store.steampowered.com/app/569480) — замок із блоків з автоформою стін і веж, дальність лучників росте з висотою, вікінги крадуть/вбивають/палять, дракон і зерносховище, церкви/таверни/площа, податки, сезони, сталий/суцільний ліс, редактор, Workshop.
- YouTube: пошук «Kingdoms and Castles gameplay».

## Непевне
- (?) Сітка квадратна, розміри будівель (ферма N×N) і доріг — з памʼяті; фан-вікі fandom (402) і wiki.gg (401) не відкрились.
- (?) Як саме родючість впливає на урожай (рівні родючості, виснаження) — Wikipedia згадує лише «fertile land» як бажане місце; механізм не перевірено.
- (?) Баліста, огри (звідки приходять), поведінка дракона при низькому HP, голод як шкода, відхід невдоволених селян.
- (?) Пауза/прискорення часу, перемикачі лих у налаштуваннях нової гри, оверлеї мапи.
- (?) Чи є умова поразки, крім вимирання міста.
