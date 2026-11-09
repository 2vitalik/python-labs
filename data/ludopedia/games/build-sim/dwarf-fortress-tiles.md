---
title: Dwarf Fortress — призначення клітин і рідини
slug: dwarf-fortress-tiles
aka: [Dwarf Fortress, DF, Slaves to Armok II, Гномья крепость, Фортеця гномів]
family: build-sim
also: [roguelike]
klass: cursor
axes:
  field: 3d
  time: realtime
  opponent: ai
  info: partial
  random: both
  goal: survive
year: 2006
platforms: [PC, macOS, Linux]
links:
  - {kind: fandom, url: "https://dwarffortresswiki.org/index.php/Water", best: true, note: "вікі DF: глибина 0–7 у клітині, таблиця ефектів глибин, течія в 9 напрямках, випаровування, лід, солона/застійна вода"}
  - {kind: fandom, url: "https://dwarffortresswiki.org/index.php/Stockpile", note: "склади: малювання прямокутниками й пензлем, 18 категорій, give/take-лінки, бочки й скрині"}
  - {kind: fandom, url: "https://dwarffortresswiki.org/index.php/Pressure", note: "тиск: вода піднімається до рівня на 1 нижче джерела (бачив у пошуку, фетч 429)"}
  - {kind: fandom, url: "https://dwarffortresswiki.org/index.php/Zone", note: "типи зон (фетч 429)"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Dwarf_Fortress", note: "огляд: режими, непряме керування, z-рівні, Steam 2022, «Losing is Fun»"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=Dwarf+Fortress", note: "пошук; Steam-версія Kitfox 2022"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=dwarf+fortress+water+pressure+stockpile+tutorial", note: "пошук; туторіали"}
stage: v1
coverage: 60
mechanics: [cell-click, multi-select, editor-draw-tools, editor-erase, hover-highlight, impassable-cells, floor-types, environment-death, gravity-fall, height-levels, interaction-table, cell-transform, dig-terrain, game-pause, game-loop, state-as-data, field-scaling, save-game, status-panel, message-log, map-window, +zone-paint, +stockpile-filter, +hauling-jobs, +stockpile-links, +container-capacity, +job-queue, +liquid-volume, +liquid-flow, +liquid-pressure, +evaporation, +phase-change-threshold, +depth-effects-table, +map-edge-drain, +liquid-contamination, +pump-lift, +z-level-view]
proposes: ["+role:liquid", "+effect:flow", "+effect:evaporate", "+cond:volume", "+cond:accepts", "+effect:haul", "+effect:designate", "+trigger:job_done", "+cond:temperature", "+effect:freeze", "+ui:depth-digit", "+ui:z-level-indicator", "+window:stockpile-settings", "+window:zone-panel", "+feature:link-graph", "+card:liquid-pressure", "+card:stockpile-filter", "+card:depth-effects-table"]
author: opus
date: 2026-11-09
---

# Dwarf Fortress (клітини) — гравець фарбує клітини призначеннями (склад, зона), гноми самі носять речі, а вода й магма живуть у клітині рівнем 1–7 і течуть під тиском

## Суть
Описано **лише клітинний шар** фортечного режиму Dwarf Fortress: (1) **призначення клітин** — гравець не керує гномами, а розмічає клітини як склади з фільтром речей і зони (кімнати, пасовища, звалище, джерело води…), після чого гноми самі беруть роботи «перенести», «викопати», «наповнити»; (2) **рідини** — вода й магма лежать у клітині як ціле число 1–7, падають униз, розтікаються в 8 сусідів по рівню, переносять тиск через заповнені обʼєми, випаровуються, замерзають. Ефекти рідини на гномів залежать від глибини (від «не заважає» до «тоне»). Решта (історія світу, бої, настрої, пригодницький режим) — поза описом.

## Поле і час
- Воксельна мапа: квадратна сітка × z-рівні (камера показує один z-рівень зверху; рух між рівнями — сходи, скати, падіння). Мапа обирається як ділянка висадки (embark) на згенерованому світі.
- Шари клітини: тип тайла (стіна/підлога/відкритий простір/сходи…), будова, речі, **рідина з глибиною 0–7**, призначення (склад/зона), забрудники, температура.
- Тік — внутрішній крок симуляції; real-time з паузою (гра зазвичай грається на паузі + швидкими прогонами).
- Видимість: туман над нерозкопаним камінням (`info: partial`); підземні шари відкриваються копанням.
- Глибина — **на один z-рівень**: 7/7 у клітині не означає, що вода сягає семи рівнів униз.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гном | ally | навички, роботи (labors), плавання | бере роботи з черги (копати, носити, будувати); гравець не керує напряму |
| Склад (stockpile) | zone | клітини, категорії/фільтри, лінки, max скринь/бочок/тачок | приймає дозволені речі; кожна клітина — одне місце |
| Зона активності | zone | тип, клітини, увімк/вимк | задає роботу/поведінку на клітинах (звалище, пасовище, ставок, джерело води…) |
| Кімната / локація | zone | меблі-якір, клітини | спальня, їдальня; локації (лікарня, таверна, бібліотека, храм) «привласнюють» речі |
| Нора (burrow) | zone | клітини | обмежує, де можуть бути гноми |
| Річ (item) | object | категорія, якість, матеріал | лежить у клітині; дозволена складом → стає роботою «перенести» |
| Скриня (bin) / бочка (barrel) | container | місткість | бин — до 10 зливків/блоків; бочка/горщик — до 60 страв |
| Тачка (wheelbarrow) | container | — | склад каміння за замовч. має 1; займає клітину складу |
| Майстерня | static | лінки входів/виходів | виріб лежить у ній, доки склад-лінк не прийме |
| Вода | terrain | глибина 1–7, солона/застійна/брудна, температура | падає, тече вбік, тиск, випаровується, замерзає |
| Магма | hazard | глибина 1–7 | ті ж правила глибини й випаровування; без тиску, якщо не качати |
| Лід | static | — | вода нижче 10000 °U миттєво; стіна з ≥ 4/7; тане — завжди 7/7 води |
| Джерело (річка, ключ, аквіфер, край мапи) | spawner | — | ніколи не вичерпується (може замерзнути) |
| Мутний ставок | terrain | не джерело | дощ повільно доливає навіть після осушення |
| Насос (screw pump) | switch | вхід/вихід | качає рідину на рівень виходу (тиск і для магми); опріснює |
| Колодязь, ґрати на підлозі | static | — | вода під ними замерзла → конструкція руйнується |
| Укріплення (fortification) | gate | — | пропускає рідину, тримає істот (не гасить тиск) |
| Край мапи | static | — | рідина, що витекла за край, зникає |

## Правила (КОЛИ → ЯКЩО → ТО)
Призначення клітин:
- КОЛИ `input(p, rect)` → ЯКЩО `custom: «клітина не стіна, не майстерня, не інший склад»` → ТО `set_cell(cell, stockpile)` (несуміжні області дозволені; пензель і гумка — поклітинно).
- КОЛИ `input(accept)` → ТО `choose(preset | custom)` — пресет категорії або власні фільтри.
- КОЛИ `custom: «річ лежить поза складом»` → ЯКЩО `custom: «склад приймає річ (категорія, матеріал, якість)»` and `custom: «є вільна клітина»` → ТО `custom: «робота перенести до найближчої вільної клітини»`; найновіша річ — першою.
- КОЛИ `custom: «жоден склад не приймає тип»` → ТО `custom: «річ лишається, де лежить; по неї ходять за потреби»`.
- КОЛИ `custom: «склад створено на клітині»` → ЯКЩО `occupied(cell, item)` → ТО `custom: «наявна рухома річ стає частиною складу, навіть заборонена; клітина зайнята, доки не винесуть»`.
- КОЛИ `custom: «клітина містить лише заборонені (forbidden) речі»` → ТО `custom: «клітина вважається вільною»`.
- Лінки: ЯКЩО not `custom: «take from anywhere»` → ТО `custom: «склад бере лише з пролінкованих складів/майстерень»`; пряма двостороння звʼязка заборонена, цикл із ≥ 3 — можна; кожен лінк створює зворотний.
- КОЛИ `custom: «майстерня пролінкована зі складами»` → ТО `custom: «бере вхідні матеріали лише з них»` (бракує палива → стоп).
- Категорія `None`: нові речі не приймає; склад, що не дозволяє ні органіки, ні неорганіки, — ніколи нічого не отримає.
- КОЛИ `input(zone, rect)` → ТО `set_cell(cell, zone-type)`; ЯКЩО `state(zone, active)` → ТО `custom: «гноми виконують роботу зони»` (напр. Water Source — набрати воду; Garbage Dump — віднести позначене «на викид»).

Рідини (кожен тік, клітина з глибиною d ≥ 1):
- КОЛИ `tick` → ЯКЩО `free(below)` → ТО `fall(liquid)` (рух лише вниз або вбік — 9 напрямків; ніколи по діагоналі вгору/вниз).
- КОЛИ `tick` → ЯКЩО not `free(below)` and `custom: «d ≥ 2»` → ТО `custom: «частина рівня перетікає в сусідню клітину з меншою глибиною (8 напрямків)»`.
- КОЛИ `tick` → ЯКЩО `custom: «d = 1»` and not `free(below)` → ТО `block` (1/7 рухається лише вниз).
- КОЛИ `custom: «вода падає в повну клітину 7/7»` → ЯКЩО `custom: «повна клітина — частина звʼязного обʼєму»` → ТО `teleport(water, nearest non-full reachable cell)` — тиск: вода «спливає» на тому ж рівні навіть далеко; заповнює не вище, ніж на 1 z-рівень нижче джерела (річка — до свого рівня).
- КОЛИ `custom: «потік іде через діагональне зʼєднання»` → ТО `custom: «тиск далі не передається»`.
- Магма: ті ж правила, але без тиску; КОЛИ `custom: «насос качає»` → ТО `custom: «рідина піднімається до рівня виходу насоса»`.
- КОЛИ `tick` → ЯКЩО `custom: «d = 1, клітина Outside, звичайна температура»` and `prob(p)` → ТО `disappear(water)` (окрема 1/7 випаровується швидше, ніж біля річки); у пеклі — на будь-якій глибині; 1/7 поверх 7/7 не випаровується; підлога над водою (Inside) — не випаровується.
- КОЛИ `custom: «температура < 10000 °U»` → ТО `transform(water, ice)` миттєво; ЯКЩО `occupied(cell, swimmer)` → ТО `disappear(swimmer)` (замерзає всередині).
- КОЛИ `custom: «лід тане»` → ТО `transform(ice, water 7/7)`; ЯКЩО `occupied(cell, non-swimmer)` → ТО `custom: «тоне»`.
- КОЛИ `edge(liquid)` → ТО `disappear(liquid)` (дренаж за край; вертикальний стік швидший за горизонтальний).
- КОЛИ `contact(clean|salt water, stagnant)` → ТО `transform(stagnant, fresh)`; вода, що зʼявилась ортогонально поруч із застійною, — теж застійна.
- КОЛИ `contact(water, magma)` → ТО `spawn(obsidian, cell)` (?).
- Глибина → ефекти: 1 — без впливу на роботи; ≥ 2 — будівництво на клітині призупинено; 3 — душить водних істот; ≥ 4 — «Dangerous terrain», гноми не прокладають шлях і скасовують роботи, тренують плавання; мінімум для льодової стіни; 5 — вагонетки перескакують; 6 — над головою; 7 — гном без навички плавання `custom: «тоне»`.
- КОЛИ `custom: «сильна течія»` → ТО `push(creature|item)` (гноми, тварини, камені, зброя, трупи).
- КОЛИ `custom: «падіння в глибоку воду»` → ТО `custom: «травма менша»`.
- Перемога: — (нема) · Поразка: колонію знищено або фортецю покинуто · Рахунок: — («Losing is Fun»).

## Керування і ввід
- Курсор/миша по поточному z-рівню; клавіші/колесо — вгору-вниз по z.
- Режими малювання: прямокутник (клік-клік), несуміжні області, пензель по клітині, гумка; Accept → пресет або Custom.
- Редагування складу кліком по ньому (назва, межі, видалення, give/take, скрині/бочки/тачки) або через вкладку Places.
- Призначення (dig, chop, gather) малюються так само; гноми виконують, коли дійдуть руки.
- Пауза і швидкість симуляції; майже все робиться на паузі.

## Вікна, меню, HUD
- `game-screen`: мапа одного z-рівня, тулбари (Stockpile `p`, зони, призначення, будови), нижній тулбар режиму (пензель/гумка).
- `+window:stockpile-settings`: 18 категорій (Ammo, Animal, Armor, Bar/Block, Cloth, Coins, Corpses, Finished Goods, Food, Furniture, Gem, Leather, Refuse, Sheets, Stone, Weapons, Wood, None), підфільтри матеріалу і якості (Tattered…Masterwork), Additional Options (органіка/неорганіка), лічильники контейнерів.
- `+window:zone-panel`: тип зони, активна/неактивна, призначення мешканців.
- Places (`P`): список складів, зон, локацій.
- HUD: `+ui:z-level-indicator`, цифра глибини на рідині (`+ui:depth-digit`), `message-log` (оголошення), `tooltip` клітини.
- `map-window` — мапа світу перед висадкою; `main-menu`: створити світ / почати гру / продовжити; режими Fortress, Adventurer, Legends.

## Фічі поза полем
- Фортечний режим без перемоги (граєш, доки колонія жива); режими Fortress, Adventurer, Legends (`mode-select`).
- Генератор світу з налаштуваннями (розмір, дикість, мінерали, тривалість історії) — `seed-input` (?).
- `save-slots` / `autosave` (?), `pause`, `speed-control`.
- Legends mode — історія світу, експорт XML і мап для сторонніх інструментів (`export-import`).
- Steam-версія (Kitfox, 6.12.2022): піксельна графіка з перемиканням на ASCII (`theme-select`), `mouse-and-keyboard`, `mod-support` (?).

## Варіації й родичі
- У корпусі: Terraria (`terraria-liquids.md`) — рідина з рівнем, 2D, змішування в блоки; Oxygen Not Included (`oxygen-not-included-cells.md`) — маса в клітині, газ+рідина; Timberborn (`timberborn.md`) — вода з висотою для бобрів; Prison Architect (`prison-architect-rooms.md`) — зони/кімнати з вимогами; Minecraft (`minecraft-redstone.md`) — вода з рівнем потоку 1–7 (?).
- Поза корпусом: RimWorld (склади з фільтрами й пріоритетами), Going Medieval, Stonehearth; Gnomoria, Timber and Stone.
- Осі варіацій: **рідина** (біт «є/нема» / рівень 1–7 / маса float) · **тиск** (нема / телепорт через повний обʼєм / гідростатика) · **склад** (фільтр категорій / фільтр + пріоритет / лінки give-take) · **розмітка** (прямокутник / пензель / заливка кімнати).

## Цікавинки для курсу
- Рідина як ціле 0–7 на клітині: падіння + вирівнювання з сусідами — 📎 (класика клітинного автомата зі збереженням маси).
- Тиск: падіння в повну клітину → BFS по звʼязному обʼєму до найближчої неповної клітини не вище «рівень джерела − 1» — 🥇 (нетривіальний алгоритм, повно пасток).
- Таблиця «глибина → ефект» як дані (шлях, роботи, плавання, утоплення) — 🌱.
- Склад: фільтр категорій/матеріалу/якості + черга робіт «перенести до найближчої вільної клітини» — 🥉.
- Give/take-лінки складів і майстерень із забороною двосторонніх — 🥉 (граф потоку речей).
- Фазові переходи вода ↔ лід за порогом температури й наслідки для істот у клітині — 📎.
- Розмітка прямокутником + пензель + гумка з пропуском заборонених клітин — 🌱.

## Мапа на каталог
- Є: `cell-click` + `multi-select` + `editor-draw-tools` + `editor-erase` (малювання складів і зон у самій грі) · `hover-highlight` · `impassable-cells` (стіни, глибина ≥ 4 для шляху) · `floor-types` (вода, магма, лід) · `environment-death` (утоплення, замерзання) · `gravity-fall` (рідина) · `height-levels` (z-рівні) · `interaction-table` (вода × магма, вода × застійна) · `cell-transform` (вода → лід) · `dig-terrain` · `game-pause` + `game-loop` · `state-as-data` · `field-scaling` · `save-game` · `status-panel` · `message-log` · `map-window`.
- **Нема** → пропозиції карток:
  - `+zone-paint` (є в `prison-architect-rooms.md`) — фарбування призначень клітин.
  - `+stockpile-filter` «Склад із фільтром речей» · entities/state · 🥉 · слоти {categories, quality}.
  - `+hauling-jobs` / `+job-queue` — роботи з черги для агентів · game-logic · 🥉.
  - `+stockpile-links` «Лінки give/take» · game-logic · 🥉.
  - `+container-capacity` «Контейнер на клітині» · entities/state · 📎 · слот {capacity}.
  - `+liquid-volume`, `+liquid-flow`, `+evaporation` (є в `terraria-liquids.md`), `+phase-change-threshold` (є в ONI).
  - `+liquid-pressure` «Тиск через повний обʼєм» · game-logic · 🥇.
  - `+depth-effects-table` «Ефекти глибини» · entities/interact · 🌱.
  - `+map-edge-drain`, `+liquid-contamination`, `+pump-lift`, `+z-level-view` — одним рядком кожна (дренаж, застійна/брудна вода, насос, перегляд по z-рівнях).

## Пропозиції до словників
- `+role:liquid` — вміст клітини з рівнем, що тече (також Terraria, ONI).
- `+effect:flow` — рідина перетікає в сусідню клітину вирівнюючи рівень; `+effect:evaporate` — рівень спадає/зникає.
- `+cond:volume` — рівень рідини в клітині порівняно з N (глибина ≥ 4, 7/7).
- `+cond:temperature` — температура клітини проти порогу; `+effect:freeze` — рідина → твердий тайл.
- `+cond:accepts` — склад/контейнер приймає річ за фільтром.
- `+effect:haul` — агент переносить річ у ціль (робота); `+effect:designate` — гравець призначає клітині роль (склад/зона/копати).
- `+trigger:job_done` — агент завершив роботу (ланцюг майстерня → склад).
- `+ui:depth-digit` — цифра рівня рідини на клітині; `+ui:z-level-indicator` — поточний z-рівень.
- `+window:stockpile-settings`, `+window:zone-panel` — вікна налаштувань призначення.
- `+feature:link-graph` — лінки між складами й майстернями як граф.
- `+card:liquid-pressure`, `+card:stockpile-filter`, `+card:depth-effects-table` — див. «Мапа на каталог».

## Джерела
- ⭐ [DF Wiki: Water](https://dwarffortresswiki.org/index.php/Water) — глибина 0–7, таблиця глибин 1–7, 9 напрямків течії, 1/7 лише вниз, випаровування, 10000 °U, солона/застійна/брудна вода, дренаж.
- [DF Wiki: Stockpile](https://dwarffortresswiki.org/index.php/Stockpile) — малювання, Accept + пресет/Custom, пензель і гумка, перенесення до найближчої клітини, лінки, 18 категорій, бини 10 / бочки 60, звалище, нори, кімнати, локації.
- [DF Wiki: Pressure](https://dwarffortresswiki.org/index.php/Pressure) — у пошуку: вода стає на 1 рівень нижче джерела, річка — до свого рівня, діагональ гасить тиск, магма без тиску без насоса (сторінку не відкрив — 429).
- [DF Wiki: Zone](https://dwarffortresswiki.org/index.php/Zone) — типи зон (не відкрив — 429).
- [Wikipedia: Dwarf Fortress](https://en.wikipedia.org/wiki/Dwarf_Fortress) — режими, непряме керування, z-вісь з 2007, Steam 6.12.2022, «Losing is Fun».

## Непевне
- (?) Перелік зон активності (Meeting Area, Pen/Pasture, Pit/Pond, Water Source, Fishing, Gather Fruit, Sand, Clay, Animal Training, Barracks, Archery, Tomb, Dungeon) — з памʼяті; підтверджено лише Garbage Dump, нори, кімнати, локації, Water Source (тест солоності).
- (?) Вода + магма → обсидіан: сторінка Water про це мовчить; з власних знань.
- (?) Точний алгоритм розтікання (скільки рівня переходить за тік, порядок обходу) — на вікі нема.
- (?) Збереження й сейв-слоти, моди в Steam-версії, вода в Minecraft з рівнем 1–7 — не перевірено.
- (?) Тиск: деталі (пошук «вниз → убік → нагору», межі) — лише з пошукового фрагмента.
