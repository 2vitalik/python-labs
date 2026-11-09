---
title: Civilization (бойовий шар юнітів, I–VI)
slug: civilization
aka: [Sid Meier's Civilization, Civ, Civ V, Civ 5, Цивілізація, 1UPT]
family: tactics
also: [build-sim]
klass: figure
axes:
  field: hex
  time: turn
  opponent: ai
  info: hidden
  random: both
  goal: state
year: 1991
platforms: [PC, Mac, Linux, iOS, Android, Switch, PS4, Xbox One]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Civilization_V", best: true, note: "гекс замість квадрата (від Panzer General), один військовий юніт на клітину, дальній бій без відповіді, міста-стрільці на 2 клітини, embark, промоції, умови перемоги"}
  - {kind: other, url: "https://forums.civfanatics.com/resources/understanding-the-zone-of-control-vanilla.25582/", note: "CivFanatics: точне правило ZOC у Civ V з цитатою мануала, винятки (міста, кораблі, embarked, авіація), рисунки"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Civilization_(video_game)", note: "Civ I: квадратна сітка, поселенці, ветерани, «stacks of doom» замість ZOC, фаланга проти лінкора"}
  - {kind: other, url: "https://drwjf.github.io/bc4/civ/civ2civ3/zoc.html", note: "класичне правило ZOC (Civ II/III-стиль): не можна з клітини біля ворога в іншу клітину біля ворога, винятки"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=Civilization", note: "пошук"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Civilization+V+combat+gameplay", note: "пошук; бій у Civ V"}
stage: v1
coverage: 60
mechanics: [hp-damage, melee-vs-ranged, unit-xp-skills, fog-of-war, impassable-cells, ai-opponent, hot-seat, online-multiplayer, destroy-all-enemies, reachable-highlight, path-preview, hover-highlight, minimap-radar, field-scaling, player-camera, save-game, save-autosave, difficulty-levels, round-currency, map-window, +zone-of-control, +movement-points, +terrain-move-cost, +one-unit-per-tile, +stack-kill, +city-ranged-attack, +embark, +unit-swap, +combat-preview, +fortify, +city-capture-choice, +flanking, +map-generation]
proposes: ["+cond:in_enemy_zoc", "+effect:end_moves", "+effect:capture", "+role:city", "+ui:combat-preview", "+window:city-screen", "+window:tech-tree", "+feature:victory-toggles", "+axis:stacking", "+card:one-unit-per-tile", "+card:stack-kill", "+card:city-ranged-attack", "+card:embark"]
author: opus
date: 2026-11-09
---

# Civilization (юніти) — від «стопки загибелі» на квадратах до одного юніта на гекс: армія розкладається по мапі, і бій стає тактикою

## Суть
Описано **лише бойовий/юнітовий шар** серії; райони й суміжність Civ VI — у [civ6-districts](../build-sim/civ6-districts.md). Гравець веде цивілізацію з давнини до космосу; військові юніти ходять мапою, захоплюють міста й обороняються. Поворот серії — **Civ V (2010)**: квадрат → гекс і **один військовий юніт на клітину** (1UPT, плюс один цивільний), тож армія стає лінією фронту, а не стопкою. Разом із **зоною контролю** (ZOC), дальнім боєм без відповіді та містами, що самі стріляють, глобальна стратегія отримала тактичну битву на тій самій мапі.

## Поле і час
- Civ I–IV: квадратна сітка (8 сусідів); Civ V–VI: гекси (6 сусідів). Мапа процедурна (материки, острови тощо), туман війни; одна мапа і для економіки, і для бою.
- Шари клітини: рельєф (рівнина, пагорб, гора), фіча (ліс, джунглі, болото), ресурс, покращення (дорога, шахта), місто; ріки (у V — по ребрах гексів) (?).
- Хід — усі юніти й міста гравця діють у будь-якому порядку, потім ходять інші цивілізації (у мультиплеєрі V — одночасні ходи за замовчуванням (?)).
- Кожен юніт має **очки руху** (MP); клітини мають вартість входу; дороги й залізниці (у Civ I — необмежений рух по залізниці) зменшують вартість.
- Стек: I–IV — скільки завгодно юнітів у клітині; V — **1 військовий + 1 цивільний/Великий діяч**; VI — 1UPT із формуваннями (корпус/армія) (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Військовий юніт ближнього бою | piece | сила, MP, HP, досвід, промоції | атакує сусідню клітину, отримує відповідь; при перемозі може зайти в клітину (?) |
| Дальній юніт (лучник, артилерія) | piece | дальня сила, дальність | бʼє здалеку **без відповіді**; у ближньому бою слабкий — «ближній зазвичай знищує дальнього» |
| Облоговий юніт | piece | бонус проти міст | у V — потребує розгортання перед пострілом (?) |
| Кіннота / броня | piece | багато MP | може рухатися після атаки; пробиває ZOC маневром |
| Корабель | piece | MP по воді | має ZOC і на морські, і на сухопутні юніти; сухопутні на кораблі ZOC не накладають |
| Сухопутний юніт на воді (embarked) | piece | вразливий | у V сам «сідає на воду» (замість транспортів); власної ZOC нема |
| Поселенець / робітник | ally | цивільний, без бою | закладає місто / будує покращення; захоплюється ворогом при контакті (?) |
| Великий генерал | ally | аура | бонус сусіднім юнітам; будує Цитадель, що шкодить сусіднім ворогам |
| Місто | static | HP, сила оборони, стіни | **стріляє** по ворогах у радіусі 2 клітин; ZOC навіть без гарнізону; HP 0 → захоплення |
| Місто-держава | neutral | тип (морська, культурна, військова…) | не може перемогти; дає бонуси союзнику; захоплюється |
| Варвари | enemy | — | зʼявляються з таборів / незайнятої землі / моря |
| Клітина рельєфу | terrain | вартість руху, бонус оборони | пагорб/ліс — обороні краще (?); гора — непрохідна в V |
| Ріка | terrain | ребро | штраф атакуючому через ріку (?) |
| Укріплення / форт / цитадель | static | бонус оборони | у Civ I–II фортеця рятує стек від загибелі цілком |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(move, u, cell)` → ЯКЩО `custom: «MP юніта ≥ вартість клітини»` → ТО `move(u, cell)`, MP −вартість; інакше `custom: «юніт завжди може зробити хоча б один крок, якщо не оточений»`.
- КОЛИ `input(move, u, cell)` → ЯКЩО `occupied(cell, military)` and `custom: «це свій військовий юніт»` → ТО `swap(u, other)` (Civ V: юніти міняються місцями) ; інакше `block`.
- Стек (I–IV): КОЛИ `input(move, u, cell)` → ЯКЩО `occupied(cell, own)` → ТО `move` — юніти складаються в стопку без ліміту.
- 1UPT (V): КОЛИ `input(move, u, cell)` → ЯКЩО `count(military, >=, 1)` у клітині → ТО `block`; ЯКЩО `custom: «u — цивільний і цивільного в клітині нема»` → ТО `move`.
- ZOC (V): КОЛИ `input(move, u, cell)` → ЯКЩО `custom: «і стартова, і цільова клітини поруч з одним і тим самим ворожим бойовим юнітом/містом»` → ТО `move` і `custom: «MP = 0»` (вхід у ZOC, вихід з неї, перехід з однієї ZOC в іншу — без штрафу).
- ZOC (класична, Civ I–III-стиль): КОЛИ `input(move, u, cell)` → ЯКЩО `custom: «u стоїть поруч з ворогом і cell теж поруч з ворогом»` and not `custom: «cell — місто або клітина зі своїм юнітом»` → ТО `block`.
- КОЛИ `input(attack, u, t)` → ЯКЩО `adjacent(u, t)` and `custom: «u — ближній»` → ТО `damage` обом за співвідношенням сил (атакувальник теж отримує шкоду).
- КОЛИ `input(attack, u, t)` → ЯКЩО `custom: «u — дальній»` and `in_range(u, t, range)` and `line_of_sight(u, t)` → ТО `damage(t)`; відповіді нема.
- КОЛИ `hp_zero(t)` → ЯКЩО `custom: «атакував ближній юніт»` → ТО `disappear_b`, `custom: «атакувальник займає клітину (?)»`.
- Стек-загибель (Civ I–II): КОЛИ `custom: «захисник стеку програв бій»` → ЯКЩО not `cell(stack, city)` and not `cell(stack, fortress)` → ТО `custom: «гине вся стопка»` (?).
- Вибір захисника (I–IV): КОЛИ `input(attack, u, stack)` → ТО `custom: «бій веде найсильніший захисник стопки»`.
- КОЛИ `turn_end(side)` → ЯКЩО `custom: «ворог у радіусі 2 від міста»` → ТО `custom: «місто може вистрілити раз за хід»` (`damage`).
- КОЛИ `input(attack, melee, city)` → ТО `damage` місту і атакувальнику (сила міста росте від гарнізону й стін); фланговий бонус від сусідніх своїх юнітів.
- КОЛИ `hp_zero(city)` → ЯКЩО `custom: «ближній юніт входить у місто»` → ТО `set_side(city, attacker)`, `choose([annex, puppet, raze])`.
- КОЛИ `turn_start(side)` → ЯКЩО `custom: «місто не захоплене»` → ТО `heal(city, ~15 %)`; юніти лікуються за типом, місцем (своя територія, місто) і промоціями.
- КОЛИ `input(fortify, u)` → ТО `set_state(u, fortified)` — бонус оборони, доки стоїть (?).
- КОЛИ `died(enemy)` → ТО `counter(xp, +n)`; КОЛИ `counter(xp, >=, threshold)` → ТО `choose(promotions)` або значне лікування замість промоції.
- КОЛИ `enter(land_unit, water)` → ЯКЩО `custom: «відкрита технологія embark»` → ТО `set_state(u, embarked)` — слабка оборона, без ZOC.
- КОЛИ `contact(military, enemy_civilian)` → ТО `set_side(civilian, attacker)` (Великий діяч при захопленні гине, крім пророків у доповненнях).
- Перемога (V): космос (корабель-колонія) · дипломатія (голосування ООН) · культура (5 гілок політик + Утопія; у BNW — туризм) · домінування (тримати всі столиці) · очки (найбільший рахунок у 2050 р.); кожну можна вимкнути. Civ I: завоювання всіх або космос до Альфи Центавра.
- Поразка: втрата всіх міст / іншу цивілізацію досягла перемоги.

## Керування і ввід
- Клік по юніту → підсвітка досяжних клітин (з урахуванням MP), наведення на клітину → шлях і кількість ходів; ПКМ — наказ руху (кілька ходів — маршрут зберігається).
- Наведення курсора на ворога → вікно прогнозу бою (сила, модифікатори, очікувана шкода обом); клік — атака. Дальній бій — окремий режим «Ranged Attack» з підсвіткою цілей у радіусі.
- Кнопки наказів юніта: Fortify, Sleep/Sentry, Alert, Skip Turn, Pillage, Embark, Set Up (облога), Upgrade, Delete; клавіша «наступний юніт», що чекає наказу.
- Кнопка «Next Turn» — активна, коли всі юніти мають накази або явно пропущені.

## Вікна, меню, HUD
- `main-menu`: Single Player (Play Now / Setup Game), Multiplayer (Internet, LAN, Hotseat), Mods, Options, Exit.
- `match-setup`: цивілізація, розмір і тип мапи, складність (8 рівнів у V (?)), швидкість гри, увімкнені умови перемоги.
- `game-screen`: мапа з гексами, `minimap`, верхня смуга ресурсів (золото, наука, культура, щастя), панель вибраного юніта (сила, MP, HP, промоції, кнопки наказів), `turn-counter`/рік, кнопка Next Turn; на мапі — `reachable-highlight`, `path-preview`, HP-смуги над юнітами, межі культури.
- `combat-preview` — спливна панель прогнозу бою.
- `city-screen` — місто: виробництво, громадяни на клітинах, будівлі, купівля клітин за золото.
- `tech-tree` — дерево технологій (одна досліджується за раз).
- `map-window` / оверлеї мапи; `log-window` (журнал подій), `stats-window` (демографія, рейтинги), дипломатичний екран з лідером.
- `end-screen` — перемога/поразка, графік рахунку за історію.
- `pause-menu` (Esc): Save, Load, Options, Retire, Exit.

## Фічі поза полем
- `save-slots`, `autosave`; `hotseat`, `online-multiplayer` (V), `mod-support`.
- `difficulty-presets`; `custom-rules` — опції партії (умови перемоги, розмір мапи, швидкість).
- Прогресія всередині партії: технології відкривають юніти, промоції — досвід юніта; апгрейд застарілого юніта за золото.

## Варіації й родичі
- Сусіди в корпусі: [polytopia](polytopia.md) (той самий 4X-бій на квадраті, спрощений), [panzer-general](panzer-general.md) (звідки взято гекс 1UPT), [battle-for-wesnoth](battle-for-wesnoth.md) (ZOC + гекси), [advance-wars](advance-wars.md) (захоплення будівель), [heroes-of-might-and-magic-3](heroes-of-might-and-magic-3.md) (стратегічна мапа + окреме бойове поле — протилежне рішення).
- **Осі варіацій:**
  - **стек**: необмежений + загибель усієї стопки (I–II) / найсильніший захисник, колатераль від облоги (III–IV) (?) / 1UPT (V) / 1UPT + обʼєднання в корпус-армію (VI) (?);
  - **ZOC**: заборона «з ZOC у ZOC» (I–III) / штраф «всі MP» між клітинами однієї ZOC (V) / вхід у ZOC зупиняє (VI) (?);
  - **поле**: квадрат (I–IV) / гекс (V–VI);
  - **бій**: кидок ймовірності на перемогу (I) / HP і часткова шкода (II+) / детермінована формула з розкидом (V) (?).

## Цікавинки для курсу
- 1UPT + обмін місцями зі своїм — 🌱: одна перевірка заповненості й swap.
- ZOC за правилом Civ V (штраф лише «між двома клітинами однієї ZOC») — 📎: для кожного кроку перетнути множини сусідніх ворогів.
- Очки руху з вартістю рельєфу + «завжди один крок» — 🥉: Дейкстра з обмеженням, плюс виняток.
- Дальній бій без відповіді проти ближнього з відповіддю — 📎: дві гілки атаки й `in_range` на гексах.
- Місто-стрілець і HP міста з регенерацією — 📎.
- Загибель усієї стопки vs вибір найкращого захисника — 🌱/📎: дві версії одного правила, зручно порівнювати.
- Гексові координати (кубічні/осьові), відстань і сусіди — 🥉.

## Мапа на каталог
- Є: `hp-damage` · `melee-vs-ranged` ↔ ближній/дальній · `unit-xp-skills` ↔ промоції · `fog-of-war` · `impassable-cells` ↔ гори · `ai-opponent` · `hot-seat` / `online-multiplayer` · `destroy-all-enemies` ↔ домінування · `reachable-highlight` / `path-preview` / `hover-highlight` · `minimap-radar` · `field-scaling` / `player-camera` · `save-game` / `save-autosave` · `difficulty-levels` · `round-currency` ↔ золото · `map-window`.
- **Нема** → пропозиції карток:
  - `+zone-of-control` (вже в чергах інших ігор) — тут варіант Civ V зі штрафом «усі MP»; слот {mode: block | drain}.
  - `+movement-points` / `+terrain-move-cost` (з Wesnoth/Advance Wars) — MP і вартість клітин.
  - `+one-unit-per-tile` «Один військовий юніт на клітину» · entities/legality · 🌱 · слот {civilian_slot: true}.
  - `+stack-kill` «Програв захисник — гине стопка» · entities/combat · 🌱 · слот {safe: [city, fortress]}.
  - `+city-ranged-attack` «Будівля-стрілець з HP» · entities/combat · 📎 · слот {range: 2}.
  - `+embark` «Юніт сам переходить на воду» · entities/state · 📎.
  - `+unit-swap` «Обмін місцями зі своїм» · entities/move · 🌱.
  - `+combat-preview` (з Wesnoth `+damage-forecast`) — прогноз бою під курсором.
  - `+fortify` «Окопатись: бонус оборони, доки не рушив» · entities/state · 🌱.
  - `+city-capture-choice` «Захоплене місто: анексувати / маріонетка / зруйнувати» · game-logic/win · 🌱.
  - `+flanking` (з XCOM) — тут бонус за сусідніх своїх при атаці міста.
  - `+map-generation` «Генерація материків» · levels/generation · 🥇.

## Пропозиції до словників
- `+cond:in_enemy_zoc(a, from, to)` — обидві клітини ходу в ZOC того самого ворога (Civ V; Wesnoth — інша семантика).
- `+effect:end_moves(a)` — обнулити очки руху без завершення ходу сторони (≠ `end_turn`).
- `+effect:capture(city)` — захопити будівлю/місто з вибором долі (поряд із ⏳ `set_side`).
- `+role:city` — статична будівля з HP, власною атакою й ZOC.
- `+ui:combat-preview` — прогноз бою під курсором.
- `+window:city-screen` — екран міста; `+window:tech-tree` — дерево технологій.
- `+feature:victory-toggles` — увімкнення/вимкнення окремих умов перемоги.
- `+axis:stacking` = `unlimited` | `one-per-tile` | `formations`.
- `+card:one-unit-per-tile`, `+card:stack-kill`, `+card:city-ranged-attack`, `+card:embark` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Civilization V](https://en.wikipedia.org/wiki/Civilization_V) — гекс від Panzer General, 1 військовий + 1 цивільний на клітину, дальній бій без відповіді, міста стріляють на 2 клітини й регенерують ~15 %, embark, промоції, анексія/маріонетка/руйнування, 5 умов перемоги.
- [CivFanatics: Understanding the Zone of Control (vanilla)](https://forums.civfanatics.com/resources/understanding-the-zone-of-control-vanilla.25582/) — цитата мануала, хто накладає ZOC, винятки й рисунки.
- [Wikipedia: Civilization (1991)](https://en.wikipedia.org/wiki/Civilization_(video_game)) — поселенці, ветерани, «stacks of doom» замість ZOC, умови перемоги Civ I.
- [ZOC (Civ II/III-стиль)](https://drwjf.github.io/bc4/civ/civ2civ3/zoc.html) — правило «не з ZOC у ZOC» і винятки (місто, клітина зі своїм юнітом, дипломати).
- YouTube: пошук «Civilization V combat gameplay».

## Непевне
- (?) Загибель усієї стопки поза містом/фортецею — Civ I–II; у III–IV — інакше (колатеральна шкода облогою). Не перевірено першоджерелом.
- (?) ZOC у Civ VI («вхід зупиняє») і формування корпус/армія — з памʼяті.
- (?) HP юнітів (10 у ранньому V, 100 після G&K), формула шкоди, бонуси пагорба/лісу/ріки — у відкритих джерелах цифр не було.
- (?) Займання клітини переможцем ближнього бою, розгортання облоги, захоплення цивільних — з памʼяті.
- (?) Кількість рівнів складності в V (8) і одночасні ходи в мультиплеєрі.
