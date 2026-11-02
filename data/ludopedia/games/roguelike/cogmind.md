---
title: Cogmind
slug: cogmind
family: roguelike
also: [build-sim]
klass: avatar
axes:
  field: square
  time: turn
  opponent: ai
  info: hidden
  random: both
  goal: state
year: 2017
platforms: [PC (Windows, Steam)]
links:
  - {kind: other, url: "https://www.gridsagegames.com/cogmind/manual.txt", best: true, note: "офіційний мануал: слоти, покриття (coverage), енергія/матерія/тепло, маса, salvage, хакінг, час, HUD — найщільніший вхід"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Cogmind", note: "історія: 7DRL 2012 → альфа 2015 → Steam EA 2017"}
  - {kind: official, url: "https://www.gridsagegames.com/cogmind/", note: "сайт гри, блог розробника про дизайн"}
  - {kind: other, url: "https://www.pcgamer.com/uk/cogmind-is-a-sci-fi-roguelike-about-building-yourself-from-salvaged-parts", note: "PC Gamer: «будуєш себе з підібраних частин»"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=cogmind", note: "пошук Steam"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=cogmind+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [move-8dir, dungeon-generation, hp-damage, inventory, inventory-items, inventory-limit, item-pickup, projectile-shot, melee-vs-ranged, blast-wave, chase-bfs, enemy-patrol, sequential-levels, player-death, speed-per-type, cell-transform, impassable-cells, console-render, gui-render, status-panel, keyboard-controls, cell-click, minimap-radar, +parts-on-body, +slot-categories, +coverage-hit-table, +part-destroyed-overflow, +salvage-drop, +core-evolution, +heat-budget, +mass-vs-propulsion, +energy-matter, +terminal-hacking, +trace-detection, +ally-orders, +robot-ecosystem, +destructible-terrain, +system-corruption, +item-labels, +permadeath]
proposes: ["+trigger:part_destroyed", "+trigger:evolve", "+trigger:detected", "+cond:slot_free", "+cond:overweight", "+cond:heat", "+cond:energy", "+effect:attach", "+effect:detach", "+effect:salvage", "+effect:corrupt", "+effect:hack", "+effect:alert", "+role:machine", "+role:ally", "+window:evolution-window", "+window:hack-window", "+window:score-sheet", "+window:lore-window", "+ui:parts-list", "+ui:scan-window", "+ui:resource-bars", "+ui:volley-window", "+ui:item-labels", "+feature:keyboard-mode", "+feature:permadeath", "+axis:session=run"]
author: opus
date: 2026-11-02
---

# Cogmind — робот, зібраний із чужих частин: інвентар — це тіло, кожен постріл по тобі відбиває якусь деталь

## Суть
Cogmind — ядро-робот, що піднімається з глибин Комплексу (поверхи від −10 до −1) на поверхню. Сили не дає досвід: ти чіпляєш до тіла деталі чотирьох категорій — живлення, рух, утиліти, зброя — у обмежені слоти, а ворожі постріли влучають **у деталі пропорційно їх покриттю**, ламаючи їх. Знищені роботи кидають уламки (salvage), з яких ти береш нові частини; тож гра — безперервна перебудова себе під енергію, тепло й масу. Довкола — «екосистема» роботів (робітники, збирачі сміття, патрулі), термінали для хакінгу й стелс як альтернатива бою.

## Поле і час
- Квадратна сітка, поверх великий (більший за екран) — камера за гравцем, мінімапа; поверхи одноразові: виходи ведуть угору (по головній гілці −10 Materials → Factory → Research → −1 Access) або в бічні гілки (шахти, сховища, печери).
- Шари: стіни (руйнівні!), підлога, машини (термінали, фабрикатори, ремонтні станції), предмети, роботи. Поле зору 16 клітин (базово); дрони й союзники передають бачене; памʼять мапи.
- Час дискретний: абсолютний хід = 100 одиниць часу; кожна дія коштує свої (рух ~100 залежно від шасі, постріл 200, підібрати/причепити 100, зняти 50); черга ходів — за накопиченим часом.
- Тиск часу — рівень тривоги: бій, руйнування й злами піднімають її → більше патрулів і загонів-перехоплювачів.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Cogmind (ядро) | player | Integrity 250 (+150/еволюція), експозиція 100, енергія 100, матерія 300, відведення тепла 25 | рух, стрільба всією зброєю залпом, чіпляє/знімає деталі; без деталей ядро рухається саме (50 од. часу) |
| Деталь: живлення (Power) | object | енергія/хід, ємність, маса, покриття, integrity | генерує енергію; може перегріватись |
| Деталь: рух (Propulsion) | object | тип (гусениці/ноги/колеса/ховер/політ), підтримувана маса, швидкість | активний лише один тип; більше маси → повільніше |
| Деталь: утиліта (Utility) | object | вид (броня, сховище, сенсор, хакерське ПЗ, охолодження…) | пасивні/активні бонуси; часто споживають енергію |
| Деталь: зброя (Weapon) | object | тип (балістична, енергетична, ракетна/вибухова, ближній бій), шкода, тепло, енергія/матерія за постріл | стріляють залпом |
| Уламки (salvage) | pickup | шанс уціліти деталі, матерія | падають зі знищених роботів |
| Матерія | pickup / resource | кількість | будує деталі, живить балістику |
| Grunt / Sentry / Hunter / Swarmer | enemy | клас, набір деталей | бойові патрулі й загони |
| Programmer | enemy | — | хакає Cogmind → корупція системи |
| Watcher / Operator | enemy | — | спостерігає/кличе підкріплення, піднімає тривогу |
| Worker / Engineer | neutral | — | прибирає уламки / відбудовує зруйновані стіни |
| Recycler | neutral | — | збирає деталі, що лежать на підлозі |
| Hauler | neutral | несе предмети | вантаж падає при знищенні |
| Союзник (дрон, найманець, перепрограмований робот) | ally | накази | виконує STAY/FOLLOW/GUARD/EXPLORE… |
| Термінал | static (machine) | безпека 1–3 | хакінг: карти, тривога, запити |
| Фабрикатор | spawner | схема + матерія | будує деталь/робота за схемою |
| Ремонтна станція / Recycling Unit / Scanalyzer | static (machine) | — | ремонт деталей / переробка / отримання схеми |
| Вибухова машина | hazard | — | вибухає від влучання |
| Пастка | hazard | вид | шанс спрацювання за типом руху (гусениці 100 % … політ 20 %) |
| Стіна / двері | static / gate | руйнівна | стіну можна пробити; двері відчиняються |
| Вихід (access) | static | куди веде | перехід на інший поверх → еволюція |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(attach part)` → ЯКЩО `slot_free(category)` → ТО `attach(part)`, `custom: «−20 енергії, −10 матерії, 100 од. часу»`; `detach` — 10 енергії, 50 од. часу.
- КОЛИ `input(move dir)` → ТО `move(cogmind, dir)`, `custom: «час = f(тип руху, маса/підтримка)»`; ЯКЩО `overweight` → ТО повільніше, пастки спрацьовують завжди.
- КОЛИ `turn_start(cogmind)` → ТО `counter(energy, +sum(power))`, `counter(energy, -upkeep)`, `counter(heat, -dissipation)`.
- КОЛИ `input(fire at target)` → ЯКЩО `has(energy|matter, cost)` → ТО `custom: «залп усіма активними зброями; шанс влучання 60 % ± модифікатори, 10–95 %»`, `counter(heat, +n)`.
- КОЛИ `contact(projectile, robot)` → ТО `custom: «ціль — ядро або деталь, зважено за покриттям (ядро — експозиція)»`, `damage(n)` по ній.
- КОЛИ `hp_zero(part)` → ТО `disappear(part)`, `counter(matter, +5)`; ЯКЩО `custom: «шкода > integrity деталі»` → ТО надлишок переходить на ядро/іншу деталь (крім куль-гармат).
- КОЛИ `custom: «рубляча зброя»` → ТО `detach(part)` — деталь відлітає на підлогу цілою.
- КОЛИ `hp_zero(core)` → ТО `lose`; КОЛИ `counter(corruption, >=, 100%)` → ТО `lose`.
- КОЛИ `counter(heat, >, 200)` → ТО `custom: «утиліти/зброя можуть вимкнутись»`; `> 300` → `custom: «живлення ймовірно вимикається»`, деталі можуть плавитись (?).
- КОЛИ `destroyed(robot)` → ТО `spawn_at(salvage, cell)`: кожна деталь уціліє з p ≈ (integrity% / 2) + salvage-модифікатор зброї; інвентар падає завжди; фабричні роботи — без уламків.
- КОЛИ `contact(em_shot, robot)` → ТО `custom: «корупція системи»`; корупція → випадкові збої (скидання деталі, хибні дані).
- КОЛИ `input(hack terminal, command)` → ТО `custom: «успіх % = хакерське ПЗ − безпека − корупція/3»`; кожна дія може бути `detected` → trace росте; повний trace → `custom: «замок + контратака»`.
- КОЛИ `input(order ally, cmd)` → ТО `custom: «союзник виконує STAY/ROAM/FOLLOW/GUARD/AID/TUNNEL/DROP/PICKUP/COLLECT/EXPLORE/RETURN»`.
- КОЛИ `enter(cogmind, exit)` → ТО `next_level`; ЯКЩО `custom: «нова глибина»` → ТО `window(evolution)`: +2 слоти, гравець обирає категорію; integrity ядра +150; корупція скидається.
- КОЛИ `custom: «бій/руйнування/вдалий хак»` → ТО `counter(alert, +n)`; з часом тривога спадає.
- КОЛИ `rng(trap by propulsion)` при `enter(cogmind, trap)` → ТО ефект пастки (стазис-пастка — навпаки).
- Перемога: вийти на поверхню (кілька кінцівок за гілками). Поразка: integrity ядра 0 або корупція 100 %. Рахунок: детальний score sheet (глибина, вбивства, хакінг, знахідки, еволюції).

## Керування і ввід
- Два повноцінні режими: **миша** (клік — шлях до клітини, клік по ворогу — ціль, перетягування деталей між інвентарем і слотами) і **клавіатурний режим** (F2: vi/numpad, біг з модифікатором, курсор з кроком).
- Буквені клавіші вмикають/вимикають деталі зі списку; `f` — режим стрільби з превʼю влучань і траєкторії (?).
- Хакінг — меню команд термінала або ручний ввід команди текстом.
- Накази союзникам — меню команд на вибраному союзнику.
- Мітки: цифрові клавіші підсвічують ворогів/союзників/предмети/виходи на мапі (`+ui:item-labels`).

## Вікна, меню, HUD
- `game-screen`: мапа (ASCII або тайли) + **права колонка** `+ui:parts-list` — деталі за категоріями з integrity-барами, станом увімк/вимк і, за опцією, покриттям; під нею `inventory-bar` з місткістю; вгорі — `+ui:resource-bars`: Core integrity, енергія, матерія, тепло, рух (тип, швидкість, маса/підтримка); `message-log`; `minimap`.
- `+ui:scan-window` — наведення на робота/деталь/машину: integrity, тепло, ставлення (червоний ворог, сірий нейтрал, зелений друг), «!» — помітив тебе.
- `+ui:volley-window` у режимі стрільби — дальність, час, витрати залпу; поза ним — вікно ухилення (evasion).
- `+window:hack-window` — термінал: список команд з % успіху, рівень trace.
- `+window:evolution-window` — розподіл двох нових слотів між категоріями.
- `map-window` — карта Комплексу/поверху, пошук предметів, коментарі на мапі, експорт PNG.
- `+window:lore-window` — колекція лору, галерея предметів; `achievements-window`.
- `+window:score-sheet` (`end-screen`) — величезна статистика партії.
- `main-menu`, `settings-window` (клавіатурний режим, тайли/ASCII, підтвердження виходу, мітки), `help-window` / туторіал (?).
- Переходи: main-menu → game-screen; вихід з поверху → evolution-window → новий поверх; смерть/вихід → score-sheet → main-menu.

## Фічі поза полем
- `permadeath`; збереження при виході.
- Режими складності (Explorer / Adventurer / Rogue) (?) і `seed-input` (?).
- `keyboard-mode` як окремий повноцінний режим інтерфейсу; `colorblind`/масштаб шрифту — гнучкі налаштування (?).
- Колекції поза партіями: лор, галерея деталей, досягнення — `meta-progression` лише знаннями, без сили.
- Лишається в Early Access навмисно — безкоштовні розширення (нові гілки й кінцівки).

## Варіації й родичі
- Попередники: X@COM (рушій автора), 7DRL-версія 2012. Родичі: Brogue і DCSS (класика), Caves of Qud (органи як частини тіла), Robotron/Mech-ігри (збірка робота), Backpack Hero (інвентар як поле).
- Осі варіацій: **інвентар** (рюкзак / тіло зі слотами / сітка-рюкзак) · **шкода** (HP одним числом / по частинах за покриттям) · **прогресія** (XP / предмети / еволюція слотів) · **ресурси** (нема / енергія / енергія+матерія+тепло+маса) · **вороги** (усі ворожі / екосистема з нейтралами).

## Цікавинки для курсу
- Тіло як інвентар: 4 категорії слотів, attach/detach з ціною часу і ресурсів — 🥉.
- Влучання у деталь, зважене за покриттям, з переливом надлишку шкоди — 🥈 (зважений випадковий вибір + ланцюг шкоди).
- Бюджет енергія/тепло/маса за хід: генерація, upkeep, відведення, перевантаження — 🥈.
- Salvage: шанс уцілілих деталей залежить від стану й типу зброї — 📎.
- Хакінг термінала з % успіху і trace-лічильником виявлення — 🥉 (мінігра-автомат станів).
- Екосистема нейтральних роботів (прибиральник, збирач деталей, відбудовник стін) — 🥇 (кілька ШІ з власними цілями на одному полі).
- Еволюція: +2 слоти на поверх з вибором категорії — 🌱.

## Мапа на каталог
- Є: `move-8dir` · `move-by-input` · `dungeon-generation` · `hp-damage` (integrity ядра й деталей) · `inventory` + `inventory-items` + `inventory-limit` · `item-pickup` · `projectile-shot` · `melee-vs-ranged` · `blast-wave` (вибухи) · `chase-bfs` · `enemy-patrol` · `sequential-levels` · `player-death` · `speed-per-type` (тип шасі) · `cell-transform` (руйнування стін) · `impassable-cells` · `console-render` + `gui-render` · `status-panel` · `keyboard-controls` · `cell-click` · `hover-highlight` · `minimap-radar` · `game-screen` · `settings-window` · `help-window`.
- **Нема** → пропозиції карток:
  - `+parts-on-body` «Деталі на тілі як інвентар і HP» · entities/state · 🥈.
  - `+slot-categories` «Слоти за категоріями (живлення/рух/утиліта/зброя)» · entities/state · 🥉 · слот {counts}.
  - `+coverage-hit-table` «Ціль удару зважено за покриттям частин» · entities/combat · 🥈.
  - `+part-destroyed-overflow` «Надлишок шкоди переходить на інші частини» · entities/combat · 📎.
  - `+salvage-drop` «Уламки ворога: шанс уцілілих деталей» · entities/death · 📎 · слот {modifier}.
  - `+core-evolution` «Еволюція: нові слоти на кожному поверсі» · levels/progression · 🌱.
  - `+heat-budget` «Тепло: генерація, відведення, пороги збоїв» · entities/state · 🥉.
  - `+mass-vs-propulsion` «Маса проти підтримки шасі → швидкість» · entities/move · 📎.
  - `+energy-matter` «Два ресурси за хід: енергія й матерія» · game-logic/economy · 📎.
  - `+terminal-hacking` «Хакінг термінала з % успіху» · entities/interact · 🥉.
  - `+trace-detection` «Лічильник виявлення під час дії» · game-logic/lose · 📎.
  - `+ally-orders` «Накази союзникам» · entities/move · 🥉.
  - `+robot-ecosystem` «Нейтральні роботи з власними завданнями» · entities/move · 🥇.
  - `+destructible-terrain` «Руйнівні стіни, відбудова» · entities/interact · 📎.
  - `+system-corruption` «Корупція → випадкові збої» · entities/state · 📎.
  - `+item-labels` «Мітки на мапі за клавішею» · interface/hud · 🌱.
  - `+permadeath` (з Rogue).

## Пропозиції до словників
- `+trigger:part_destroyed` — частина сутності знищена (не вся сутність); `+trigger:evolve` — перехід на нову глибину; `+trigger:detected` — дію гравця виявлено (хакінг, стелс).
- `+cond:slot_free` — є вільний слот категорії; `+cond:overweight` — маса > підтримки; `+cond:heat` — тепло понад поріг; `+cond:energy` — вистачає ресурсу на дію.
- `+effect:attach` / `+effect:detach` (є ⏳, тут — у сенсі «частина тіла»); `+effect:salvage` — розкидати вцілілі частини; `+effect:corrupt` — +корупція; `+effect:hack` — дія над машиною з шансом; `+effect:alert` — підняти тривогу поверху.
- `+role:machine` — інтерактивна машина-обʼєкт (термінал, фабрикатор); `ally` вже ⏳ — тут вживається з наказами.
- `+window:evolution-window`, `+window:hack-window`, `+window:score-sheet` (детальна статистика партії), `+window:lore-window`.
- `+ui:parts-list`, `+ui:scan-window`, `+ui:resource-bars`, `+ui:volley-window`, `+ui:item-labels`.
- `+feature:keyboard-mode` (повноцінна альтернатива миші), `+feature:permadeath`; `+axis:session=run`.

## Джерела
- ⭐ [Cogmind manual](https://www.gridsagegames.com/cogmind/manual.txt) — стати ядра, ціни attach/detach, покриття, перелив шкоди, енергія/матерія, тепло 200/300, маса, типи руху й пастки, salvage, хакінг і trace, накази союзникам, час дій, HUD-вікна.
- [Wikipedia: Cogmind](https://en.wikipedia.org/wiki/Cogmind) — історія, понад 1000 деталей, стелс, Early Access.
- [Grid Sage Games](https://www.gridsagegames.com/cogmind/) — офіційний сайт і блог.
- [PC Gamer](https://www.pcgamer.com/uk/cogmind-is-a-sci-fi-roguelike-about-building-yourself-from-salvaged-parts) — огляд ідеї «збери себе з уламків».
- [Game Developer: інтервʼю з Josh Ge](https://gamedeveloper.com/design/-play-87-interview-with-josh-ge-creator-of-cogmind) — стартові слоти «по 2, живлення 1».
- YouTube: пошук «cogmind gameplay».

## Непевне
- (?) Мануал з сайту — старої бети; числа (integrity 250, тепло 200/300, ціни часу) могли змінитись.
- (?) Стартові слоти (живлення 1, інші по 2) і «+2 слоти за еволюцію з вибором» — з інтервʼю/огляду в пошуку, не з мануалу.
- (?) Режими складності, seed-input, туторіал, клавіша стрільби `f` — з памʼяті.
- (?) Плавлення деталей від тепла понад 300 — у мануалі лише «залишкове тепло плавить уламки».
- (?) Назви гілок Комплексу й відповідність глибин (Materials −10…, Access −1) — частково з мануалу, решта з памʼяті.
- (?) Steam-сторінку прямо не бачив — дано пошук.
