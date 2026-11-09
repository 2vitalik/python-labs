---
title: SimAnt
slug: simant
aka: [SimAnt: The Electronic Ant Colony, СімАнт]
family: build-sim
also: [tactics]
klass: hybrid
axes:
  field: layers
  time: realtime
  opponent: ai
  info: full
  random: runtime
  goal: territory
year: 1991
platforms: [Mac, DOS, Windows, Amiga, SNES, FM Towns, PC-98, X68000]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/SimAnt", note: "режими, жовта мураха, небезпеки, платформи й дати"}
  - {kind: other, url: "https://oldergeeks.com/downloads/files/SimAnt-The-Electronic-Ant-Colony_Manual_DOS_EN.pdf", best: true, note: "оригінальний мануал DOS: вікна, меню, феромони, касти, таблиця битв, спарювання"}
  - {kind: strategywiki, url: "https://strategywiki.org/wiki/SimAnt:_The_Electronic_Ant_Colony", note: "гайд (фетчер отримав 403; бачив у пошуку)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=simant+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [party-switch, move-auto, random-walk, chase-greedy, item-pickup, hp-damage, hunger-clock, dig-terrain, impassable-cells, realtime-ai, respawn, spawn-random-cell, map-window, minimap-radar, status-panel, stats-window, help-window, tutorial-window, mode-select, game-pause, save-game, sound-effects, music-toggle, field-scaling, game-loop, state-as-data, +pheromone-field, +scent-decay, +recruit-followers, +ratio-triangle-control, +behavior-allocation, +caste-allocation, +battle-odds-table, +side-view-nest, +linked-views, +macro-map-of-patches, +background-sim, +colony-spread, +area-hazard-sweep, +flood-lower-layers]
proposes: ["+role:scent", "+trigger:smell", "+cond:scent_level", "+effect:deposit_scent", "+effect:decay", "+effect:recruit", "+effect:release", "+effect:possess", "+ui:ratio-triangle", "+ui:warning-threshold", "+ui:scent-overlay", "+window:behavior-control", "+window:caste-control", "+window:history-graph", "+window:strategic-map", "+feature:presets", "+feature:auto-manager", "+feature:background-sim", "+card:pheromone-field", "+card:ratio-triangle-control"]
author: opus
date: 2026-11-09
---

# SimAnt — ти «розум колонії»: вселяєшся в одну мураху, малюєш феромонами сліди на клітинах і крутиш трикутники каст і поведінки

## Суть
Maxis-симуляція мурашника: чорна колонія проти червоної за ту саму ділянку двору. Гравець керує **одною** жовтою мурахою напряму (ходить, носить, копає, бʼється, вербує 5/10 сусідів, лишає сигнал тривоги), а рештою — **непрямо**: двома «трикутними джойстиками» (поведінка: їжа/копання/догляд; касти: робітники/солдати/розплідники). Мурахи орієнтуються за трьома полями запахів на клітинах — гніздо, слід до їжі, тривога; запахи вигасають і змиваються дощем. Клас `hybrid`: `avatar` (жовта мураха) + непряме керування роєм; Full Game додає макрорівень — мапу з 192 ділянок, спарювання й заселення нових ділянок.

## Поле і час
- **Ділянка (Patch)** — ігрове поле: поверхня (вид згори) + два підземні гнізда (вид збоку: чорне й червоне). Поверхня й нори — окремі шари; вхід — мурашники (anthill), їх може бути кілька.
- Вікна Edit (зблизька, частина ділянки) і Map (уся ділянка точками-квадратами) звʼязані: зміна виду в одному міняє інше; прямокутник Edit на мапі тягається.
- **Двір (Yard Level)** — макросітка з 192 ділянок (двір + будинок з кімнатами); активна одна ділянка, решта колоній «симулюються у фоні», поки туди не ввійдеш.
- Real-time з керованою швидкістю: Pause (single-step: сим іде лише поки рухається жовта), Slow, Normal, Fast, Ultra (рідше перемальовує).
- Їжа «зʼявляється» на поверхні сама (крім Experimental).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Жовта мураха | player | каста, здоровʼя, вантаж | ходить у клітину кліку найпрямішим шляхом; копає, носить, бʼється, вербує, лишає тривогу; після смерті — з наступного яйця |
| Робітник | ally | здоровʼя, поведінка | їжа / копання / догляд за ратіо трикутника; найдешевший |
| Солдат | ally | здоровʼя | як робітник без догляду; сильніший у бою, їсть більше |
| Королева | ally | одна на колонію | лише несе яйця; смерть чорної = поразка (Quick) |
| Нова королева, самець (Breeders) | ally | — | дорогі, не працюють; потрібні для спарювання (Full) |
| Яйце, личинка, лялечка (brood) | object | здоровʼя | дозрівають, лише якщо досить нянь; жовта може переносити |
| Червона мураха | enemy | каста, здоровʼя | дзеркало чорних; при перевазі — тотальна атака |
| Red Terminator | enemy | один завжди | ініціатор червоних: шукає їжу й вербує проти чорних; загинув — випадкова червона займає місце |
| Павук | enemy | один на мапі | блукає поверхнею, їсть будь-яких мурах; під землю не ходить; вбитий → їжа |
| Мурашиний лев | hazard | нерухомий | яма-пастка; вбитий зʼїдається одразу (не стає їжею) |
| Гусінь | neutral | одна на мапі | блукає; оточена гуртом — гине → зелені кульки їжі |
| Мокриця (sow bug) | neutral | — | блукає, заважає, нікого не їсть |
| Їжа (зелена кулька) | resource | — | беруть, несуть у гніздо, ділять трофалаксисом |
| Камінь | static | малий / великий | барʼєр; малий можна нести (барикада входу) |
| Земля підземна | terrain | — | копається в тунелі й камери |
| Феромон гнізда | terrain | колонія | веде додому; чужий = небезпека |
| Слід до їжі | terrain | інтенсивність | лишає мураха з їжею; ненапрямлений; вигасає без використання, змивається дощем |
| Тривога | terrain | інтенсивність | мурахи товчуться поруч і захищають; більше крапель — сильніше й довше; змивається дощем |
| Нога людини | hazard | раптова | давить мурах під собою «за 2 секунди» |
| Газонокосарка | hazard | прохід | здуває всіх на поверхні назавжди |
| Інсектицид | hazard | лише в будинку | вбиває більшість мурах ділянки на поверхні |
| Дощ | hazard | подія | затоплює нижні камери гнізда, змиває сліди й тривогу |
| Птах | enemy | на мапі двору | їсть королев під час шлюбного льоту |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(click cell)` → ТО `custom: «жовта йде до клітини найпрямішим шляхом»`; ЯКЩО `blocked(yellow)` під землею → `custom: «треба копати»`.
- КОЛИ `input(double-click underground)` → ТО `set_cell(cell, tunnel)` (копання до точки).
- КОЛИ `input(double-click object)` → ЯКЩО `custom: «їжа, brood або малий камінь»` → ТО `pickup(yellow, object)`; повторний double-click → `place(yellow, object)`.
- КОЛИ `input(Recruit 5|10)` → ТО `custom: «5/10 найближчих чорних біжать до жовтої й ходять за нею збудженими»`; КОЛИ `input(Release 1/2|all)` або `died(yellow)` → ТО `custom: «завербовані повертаються до своєї поведінки»`.
- КОЛИ `input(Exchange)` + клік по мурасі → ТО `custom: «жовта вселяється в ту мураху і бере її касту»` (лише жива доросла чорна, зокрема королева).
- КОЛИ `input(key 0)` → ТО `set_state(yellow, alarm-mode)`; КОЛИ `tick` → ЯКЩО `state(yellow, alarm-mode)` → ТО `custom: «лишає тривогу в клітині позаду; повтор в одній клітині підсилює й уповільнює згасання»`.
- КОЛИ `reach(ant-with-food, nest)` → ТО `custom: «шлях позаду мітиться слідом до їжі»`.
- КОЛИ `contact(ant, trail)` → ТО `custom: «мураха йде слідом у випадковому напрямку; дійшла до дому — розвертається»`.
- КОЛИ `contact(black, alarm)` → ТО `set_state(black, alarmed)`; КОЛИ `custom: «тривога в клітині згасла або змита»` → ТО `clear_state(black, alarmed)`.
- КОЛИ `tick` → ТО `custom: «сліди й тривога згасають; невживаний слід зникає»`.
- КОЛИ `custom: «почався дощ»` → ТО `custom: «стерти сліди й тривогу; затопити нижні камери»` → ЯКЩО `custom: «brood/мураха в затопленій камері»` → ТО `disappear(ant)`.
- КОЛИ `tick` → ЯКЩО not `custom: «завербована, стривожена, у бою»` → ТО `custom: «мураха виконує forage/dig/nurse за ратіо трикутника поведінки»`.
- КОЛИ `custom: «королева знесла яйце»` → ТО `custom: «каста майбутньої мурахи — за ратіо трикутника каст»`; ЯКЩО not `custom: «досить нянь»` → `custom: «brood не дозріває»`.
- КОЛИ `adjacent(black, red)` → ТО `custom: «бій 1:1; шанс з таблиці каст (робітник проти солдата 20/80, солдат проти розплідника 90/10…), ±10 % тому, в кого здоровʼя вище»` → `disappear(loser)`.
- КОЛИ `custom: «гурт оточив гусінь/павука»` → ТО `disappear(prey)` + `spawn(food, cell)`.
- КОЛИ `contact(ant, antlion-pit)` → ТО `disappear(ant)`.
- КОЛИ `contact(foot|mower, ant)` → ЯКЩО `custom: «мураха на поверхні»` → ТО `disappear(ant)`.
- КОЛИ `custom: «здоровʼя жовтої нижче порогу-лінії»` → ТО `custom: «сусідня чорна приходить і годує»`; КОЛИ `custom: «здоровʼя колонії нижче порогу»` → ТО `message(шукай їжу)`.
- КОЛИ `custom: «рух, копання, ношення»` → ТО `custom: «здоровʼя жовтої падає»` (голод); бере їжу голодною → `heal(yellow, n)`.
- КОЛИ `died(yellow)` → ТО `respawn(yellow, next-egg)` — штраф лише час.
- КОЛИ `input(Mate)` → ЯКЩО `custom: «є breeders»` → ТО `custom: «шлюбний літ: N запліднених королев»`; КОЛИ `input(Place + patch)` → ЯКЩО `custom: «≤ 3 ділянки від рідної, там нема чорної колонії»` → ТО `spawn_at(colony, patch)`; нерозміщених поступово їдять птахи, при переході на іншу ділянку вони гинуть.
- Перемога (Quick): `died(red-queen)` → `win`; поразка: `died(black-queen)` → `lose`.
- Перемога (Full): `all_gone(red)` and `custom: «чорні тримають > 70 % ділянок будинку»` → `win` (люди виїжджають); поразка: `all_gone(black-queen)` → `lose`.
- Experimental: перемоги нема; їжа сама не зʼявляється.

## Керування і ввід
- Миша: клік — іти; double-click — копати / взяти / покласти / атакувати; click-and-hold на жовтій — меню Recruit 5/10, Release 1/2/all, Exchange, `?`. У Map-вікні те саме із Shift.
- Click-and-hold на будь-якій мурасі чи brood — інфо-віконце (каста, поведінка, вантаж, здоровʼя).
- `0` — режим тривоги; клавіатурні скорочення для всіх команд, гра можлива без миші.
- Трикутні джойстики: тягни точку — ратіо трьох поведінок/каст; кнопки Auto/Manual; три пресети Set.
- Пороги здоровʼя — тягни горизонтальну лінію в барі.

## Вікна, меню, HUD
- `main-menu` ≈ «Select a Game»: Quick, Full, Experimental, Load, Tutorial, Cancel.
- `game-screen` = **Edit Window**: поверхня або нора; панель — Map-кнопка з мінімапою, Help, Experiment, Surface / Black Nest / Red Nest, Yellow Ant, Spider (центрування), Pause, Scent (показ запахів), Health Graph (жовта, чорні, червоні + пороги).
- `map-window` = **Map Window**: Patch Level (уся ділянка, кольорові точки: жовтий/чорний/зелений-з-їжею/червоний/помаранчевий…; перемикачі Nest/Trail/Alarm, Trails-візуалізація шляхів) і Yard Level (House / Strategic / Graphic views; Mating Controls: Mate, Automatic/Manual, Place; Colony Tally).
- `+window:behavior-control` — трикутник Forage/Dig/Nurse, відсотки або числа, бар-графік, Auto/Manual, 3 пресети.
- `+window:caste-control` — трикутник Workers/Soldiers/Breeders, ті самі контроли.
- `+window:history-graph` — графіки: популяція чорних/червоних, запас їжі, здоровʼя колоній 0–100, їжа на поверхні.
- `stats-window` ≈ Status Window — оцінка гравця як мурахи й загальний рахунок.
- `codex-window` ≈ Info Window — навчальна енциклопедія про справжніх мурах.
- `help-window` — довідка з кожної панелі; `tutorial-window` — Tutorial «Going for a Buggy Ride».
- Меню: File (About, New, Open, Save, Save As, Quit) · Window (Edit, Map, Behavior, Caste, History, Info, Status) · View (Yard, House, Strategic, Graphic, Surface, Black Nest, Red Nest) · Options (Auto Track, Music, Sound Effects, Events, Messages, Silly) · Speed (Pause, Slow, Normal, Fast, Ultra).
- HUD: `message-log` ≈ Message Bar, `popup-text` ≈ події у спливних віконцях, `+ui:warning-threshold`, `+ui:scent-overlay`, `remaining-counter` ≈ лічильники популяцій.

## Фічі поза полем
- Режими: `mode-classic` (Quick, одна ділянка), кампанія Full (усі 192 ділянки), `mode-sandbox` (Experimental: стіни/камені, dig/fill, додати чорних/червоних мурах, їжу 1 або 20, сліди й тривога, інсектицид).
- `save-slots`/збереження у файл, `pause`, `speed-control`, `tutorial`, `codex`, `sound-toggle`, `music-toggle`.
- `+feature:auto-manager` — Auto-режим трикутників (сим сам розподіляє); `+feature:presets` — три збережені ратіо.
- `+feature:background-sim` — колонії на неактивних ділянках ростуть самі.
- Перемикачі подачі: Events, Messages, Silly (жарти мурах), Auto Track камери.
- SNES-версія: вісім сценаріїв з різними локаціями й небезпеками.

## Варіації й родичі
- Empires of the Undergrowth (сучасний RTS-мурашник), Ant Simulator-и, NetLogo Ants (класична модель феромонів).
- У корпусі: Langton's Ant (`langtons-ant.md`) — одна «мураха» з правилом, без феромонів; Prison Architect (`prison-architect-rooms.md`) і Fallout Shelter (`fallout-shelter.md`) — непряме керування агентами; Populous (`populous.md`) — бог над юрбою; Oxygen Not Included (`oxygen-not-included-cells.md`) — колонія в розрізі.
- Осі варіацій: **керування роєм** (лише ратіо / ратіо + аватар-ініціатор / пряме виділення RTS) · **сигнали** (поле запахів з вигасанням / прапорці-накази) · **вид** (згори / розріз / обидва звʼязані) · **масштаб** (одна ділянка / мета-мапа з фоновою симуляцією).

## Цікавинки для курсу
- Поле феромонів: float-шар на клітинах, депозит, вигасання, змив подією — 📎 (класика ACO, видно на мапі).
- Мураха-агент: блукання → знайшла їжу → несе додому, лишаючи слід → інші йдуть слідом — 🥉 (емерджентна стежка з 3 правил).
- Трикутний джойстик ратіо (барицентричні координати → три частки) + Auto/пресети — 📎.
- Вербування 5/10 найближчих і «ходити за лідером» — 🌱.
- Таблиця шансів боїв каст + модифікатор здоровʼя — 🌱 (дані, а не if-и).
- Два звʼязані види (поверхня згори + нора збоку) і мінімапа з прямокутником вʼюпорта — 🥉.
- Мета-мапа з фоновою симуляцією неактивних ділянок — 🥈 (спрощена модель для «не на екрані»).

## Мапа на каталог
- Є: `party-switch` (Exchange — вселитись у будь-яку) · `move-auto` + `random-walk` (мурахи блукають) · `chase-greedy` (жовта йде найпрямішим шляхом) · `item-pickup` · `hp-damage` + `hunger-clock` (здоровʼя падає від праці) · `dig-terrain` · `impassable-cells` (камені) · `realtime-ai` (червоні, Terminator) · `respawn` (жовта з яйця) · `spawn-random-cell` (їжа) · `map-window` + `minimap-radar` · `status-panel` · `stats-window` · `help-window` · `tutorial-window` · `mode-select` · `game-pause` · `save-game` · `sound-effects` · `music-toggle` · `field-scaling` · `game-loop` · `state-as-data`.
- **Нема** → пропозиції карток:
  - `+pheromone-field` «Поле запахів на клітинах» · entities/state · 📎 · слоти {kinds, decay} — депозит/читання/вигасання.
  - `+scent-decay` «Вигасання й змив» · game-logic · 🌱.
  - `+recruit-followers` «Вербування за лідером» · entities/move · 🌱 · слот {n}.
  - `+ratio-triangle-control` «Трикутник ратіо» · interface/input · 📎.
  - `+behavior-allocation` / `+caste-allocation` — розподіл ролей роєм за ратіо · game-logic · 🥉.
  - `+battle-odds-table` «Таблиця шансів бою» · entities/combat · 🌱.
  - `+side-view-nest`, `+linked-views` — розріз нори і звʼязані вікна · interface/render · 🥉.
  - `+macro-map-of-patches`, `+background-sim`, `+colony-spread` — мета-мапа ділянок · levels · 🥈.
  - `+area-hazard-sweep` (нога, косарка), `+flood-lower-layers` (дощ) · entities/death · 📎.

## Пропозиції до словників
- `+role:scent` — невидима мітка на клітині з інтенсивністю й вигасанням (феромон, запах, шум).
- `+trigger:smell` — сутність відчула мітку-запах у своїй клітині/поруч (замість `contact` з невидимим).
- `+cond:scent_level` — інтенсивність мітки в клітині порівняно з N.
- `+effect:deposit_scent` — лишити/підсилити мітку; `+effect:decay` — інтенсивність спадає щотіку.
- `+effect:recruit` / `+effect:release` — N сусідів починають / перестають ходити за лідером.
- `+effect:possess` — гравець вселяється в іншу сутність (бере її тип і параметри).
- `+ui:ratio-triangle` — трикутний повзунок трьох часток; `+ui:warning-threshold` — тягнений поріг у барі; `+ui:scent-overlay` — показ невидимого шару.
- `+window:behavior-control`, `+window:caste-control`, `+window:history-graph`, `+window:strategic-map` — вікна SimAnt.
- `+feature:presets`, `+feature:auto-manager`, `+feature:background-sim`.
- `+card:pheromone-field`, `+card:ratio-triangle-control` — див. «Мапа на каталог».

## Джерела
- ⭐ [Мануал SimAnt (DOS)](https://oldergeeks.com/downloads/files/SimAnt-The-Electronic-Ant-Colony_Manual_DOS_EN.pdf) — повний Reference: 192 ділянки, касти, три поведінки, три запахи, Recruit 5/10, таблиця битв, усі вікна й меню, Experimental-інструменти, спарювання (≤ 3 ділянки).
- [Wikipedia: SimAnt](https://en.wikipedia.org/wiki/SimAnt) — режими, керування жовтою, небезпеки, платформи й дати, SNES-сценарії.
- [StrategyWiki](https://strategywiki.org/wiki/SimAnt:_The_Electronic_Ant_Colony) — гайд (бачив у пошуку, фетчер 403).

## Непевне
- (?) Чи поле ділянки — справжня клітинна сітка і якого розміру: мануал показує обʼєкти на мапі «квадратами», але розмір не дає.
- (?) Розкладка 192 ділянок (напр. 16×12) — не підтверджено.
- (?) Швидкість вигасання запахів і поріг «досить нянь» — числа в мануалі не наведені.
- (?) Точний склад SNES-сценаріїв — лише «вісім».
