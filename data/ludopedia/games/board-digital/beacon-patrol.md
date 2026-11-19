---
title: Beacon Patrol
slug: beacon-patrol
aka: []
family: board-digital
also: []
klass: hybrid
axes:
  field: square
  time: turn
  opponent: coop
  info: partial
  random: runtime
  goal: score
year: 2025
platforms: [board, PC (Steam), macOS, Linux]
links:
  - {kind: other, url: "https://rulespal.com/beacon-patrol/rulebook", best: true, note: "повні правила базової гри: 54 плитки + HQ, рука й жетони руху за кількістю гравців, розміщення за ребрами, «досліджена» плитка, очки 3/2/1, звання, міні-доповнення вітряки й пірси, соло"}
  - {kind: other, url: "https://rulespal.com/beacon-patrol-ships-shores/rulebook", note: "доповнення Ships & Shores: 7 кораблів зі здібностями й своїми плитками, −10 очок за гравця"}
  - {kind: steam, url: "https://store.steampowered.com/app/2273850/Beacon_Patrol/", note: "цифрова версія 17.09.2025 (Shapes and Dreams, BrutalHack; видавці Assemble Entertainment, Shapes and Dreams): режими Exploration / Board Game / Creative, кооп до 4, 49 досягнень"}
  - {kind: other, url: "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=2273850&count=20&maxlength=3000", note: "новини й патчноути Steam: Treasury, автосейв на початку ходу, 3 слоти на режим, drag & drop, підказки «чому сюди не можна», рахунок пірсів і seal bank наживо"}
  - {kind: other, url: "https://bleedingcool.com/games/beacon-patrol-announces-first-expansion-ships-shores", note: "анонс Ships & Shores (Pandasaurus Games, червень 2024, 7 кораблів)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Beacon+Patrol+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 75
mechanics: [drag-drop-piece, conflict-highlight, move-4dir, impassable-cells, turn-enforcement, event-effects, field-scaling, save-autosave, save-multi-slot, main-menu, mode-select, tutorial-window, achievements-window, game-screen, +tile-exploration, +edge-matching, +fixed-orientation-tiles, +hand-of-tiles, +tile-bag-draw, +tile-exchange, +discard-unplayable, +hold-piece, +action-points, +place-then-enter, +discard-for-move, +surround-reward, +shared-field-coop, +local-coop, +variable-player-powers, +expansion-modules, +solo-rank-table, +score-refills-supply, +sandbox-mode, +meta-unlocks, +mission-goals]
proposes: ["+trigger:surrounded", "+cond:edges_match", "+window:treasury", "+ui:movement-tokens", "+card:place-then-enter", "+card:discard-for-move", "+card:score-refills-supply"]
author: opus
date: 2026-11-19
---

# Beacon Patrol — кооперативна мапа Північного моря: клади плитки поруч зі своїм кораблем, заходь на них і оточуй, щоб «дослідити»

## Суть
Кооперативна настільна гра про берегову охорону (у США — Pandasaurus Games) і її цифрова версія 2025 року. Гравці по черзі кладуть квадратні плитки моря поруч із плиткою, де стоїть їхній корабель: ребра мусять збігатися (вода до води, суша до суші), а корабель **одразу заходить** на нову плитку. Додатково корабель плаває водою за жетони руху. Очки дає лише **досліджена** плитка — оточена іншими з усіх чотирьох боків; маяки й буї коштують більше. Клас — `hybrid`: аватар-корабель (`avatar`) + викладання плиток курсором (`cursor`).

## Поле і час
- Необмежена квадратна сітка плиток, що росте від штабу (HQ) в центрі. Плитка має 4 ребра типу «вода» або «суша»; стрілка в правому верхньому куті задає єдину орієнтацію — плитки не повертають.
- Корабель стоїть на плитці; крок — на ортогонального сусіда через спільне водне ребро. Суша непрохідна.
- Хід гравця (за годинниковою стрілкою): у будь-якому порядку — покласти до 3 плиток (4 гравці — до 2), рухатись за жетони, раз помінятись плиткою з іншим гравцем. Кінець ходу — скидання й добір.
- Гра закінчується, коли всі плитки покладено або скинуто; рахунок спільний.
- Цифрова версія: та сама сітка з камерою (масштаб і напрям налаштовуються), режими з нескінченним запасом плиток (Exploration) і без обмежень (Creative).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Корабель | player | 1 на гравця; у Ships & Shores — тип зі здібністю | заходить на щойно покладену плитку; плаває водою за жетони |
| Штаб берегової охорони (HQ) | static | стартова плитка, задає орієнтацію | центр мапи; досліджений — 3 очки, як маяк |
| Плитка моря | tile | 4 ребра вода/суша, стрілка орієнтації | кладеться поруч із кораблем; оточена з 4 боків — досліджена, 1 очко |
| Плитка з маяком | tile | — | досліджена — 3 очки |
| Плитка з буєм | tile | — | досліджена — 2 очки; рахується як відкритий океан |
| Відкритий океан | tile | без суші | для вітряка — сусід, що дає очко |
| Острів | zone | звʼязна суша через кілька плиток, будинки | непрохідний; пірс і seal bank рахують його будинки/плитки |
| Жетон руху | resource | синій/червоний бік; соло 4, 2–3 гравці по 3, 4 гравці по 2 | 1 жетон = 1 крок; наприкінці ходу всі знову сині |
| Рука плиток | supply | 3 (4 гравці — 2), лицем догори | звідси кладуть і міняються; незіграні йдуть зі гри |
| Стос плиток | supply | 54 базові + 9 міні-доповнень + 20 Ships & Shores | добір наприкінці ходу; кінець стосу й рук — кінець гри |
| Скид | supply | поза грою | Submarine бере верхню плитку; там лежать Wreck |
| Вітряк | tile | міні-доповнення / Construction Ship | 1 + 1 за кожного ортогонального сусіда — відкритий океан |
| Пірс | tile | міні-доповнення / Ferry | 1 + 1 за кожен будинок на звʼязаному острові |
| Outpost | tile | Coast Guard Ship | 2 очки; ціль телепорту корабля |
| Lake | tile | Hover Craft | оточене сушею; 2 очки |
| Rocky Bay | tile | Pilot Ship | 2 очки |
| Seal Bank Shore | tile | Research Vessel | 1 + 1 за кожну плитку звʼязаного острова без будинку |
| Wreck | tile | Submarine, 4 шт. у скиді | 1 + 1 за кожну сусідню плитку з буєм |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `game_start` → ТО `place(HQ, centre)`, усі кораблі на HQ, `custom: «кожен бере руку й жетони руху за кількістю гравців»`.
- КОЛИ `input(place(tile, cell))` → ЯКЩО `free(cell)` і `custom: «cell ортогонально поруч із плиткою мого корабля»` і `custom: «ребра збігаються з усіма сусідами: вода до води, суша до суші»` і `custom: «з поточною плиткою — водним ребром»` і `counter(placed_this_turn, <, 3)` (4 гравці — 2) → ТО `place(player, tile)`, `move(ship, cell)` без жетона; інакше `block`.
- Плитку не можна повернути: стрілка завжди як у HQ.
- КОЛИ `input(move(ship, dir))` → ЯКЩО `has(player, movement_token)` і `custom: «сусідня плитка звʼязана водним ребром»` → ТО `move(ship, dir)`, `set_state(token, spent)`; через сушу — `block`.
- КОЛИ `input(discard(tile))` → ТО `disappear(tile)` (зі гри), `custom: «+1 безкоштовний крок без жетона»`.
- КОЛИ `input(swap(my_tile, their_tile))` → ЯКЩО `custom: «≥ 2 гравці і цього ходу ще не мінявся»` → ТО `swap(my_tile, their_tile)`; отриману можна одразу зіграти, незіграну — скинути наприкінці ходу.
- КОЛИ `turn_end(player)` → ТО `custom: «незіграні плитки — зі гри (соло: одну можна лишити)»`, `custom: «добрати до 3 (4 гравці — 2; соло з лишеною — 2)»`, `clear_state(tokens, spent)`, `end_turn`.
- КОЛИ `after(place)` → ЯКЩО `adjacent_count(tile, ==, 4)` (плитка оточена з усіх боків) → ТО `set_state(tile, explored)`; рахуються лише досліджені.
- КОЛИ `custom: «усі плитки покладено або скинуто»` → ТО `game_over`; `score(+3)` за досліджений маяк і HQ, `score(+2)` за буй, `score(+1)` за іншу; звання: Novices 0–25 · Sailors 26–35 · Captains 36–45 · Navigators 46–55 · Cartographers 56+ (з кожним міні-доповненням пороги +10).
- Вітряк: ЯКЩО `state(windmill, explored)` → ТО `score(+1)` і `score(+1)` за кожного ортогонального сусіда без суші (вітряки, буї й HQ теж рахуються).
- Пірс: ЯКЩО `state(pier, explored)` → ТО `score(+1)` і `score(+1)` за кожен будинок на звʼязаному острові; сам острів не мусить бути дослідженим.
- Ships & Shores: ЯКЩО `turn_of(owner)` → ТО `custom: «діє здібність лише свого корабля»`; плитки доповнення рахуються за картками кораблів у партії; наприкінці `score(-10 × кількість гравців)`.
- Construction Ship (★1, +5 вітряків): КОЛИ `after(place)` → ТО `clear_state(1 token, spent)`.
- Research Vessel (★1, +4 Seal Bank Shore): 1 жетон → ще один обмін за хід; соло — 1 жетон → лишити ще одну плитку.
- Coast Guard Ship (★2, +4 Outpost): 1 жетон → `teleport(ship, outpost|HQ)`.
- Hover Craft (★2, +4 Lake): 1 жетон → покласти плитку, звʼязану сушею, і заїхати на неї; 2 жетони → 1 крок через сушу. Lake оточене сушею, тож класти його можуть лише Hover Craft і Pilot Ship.
- Pilot Ship (★3, +4 Rocky Bay): заїзд на щойно покладену плитку коштує 1 жетон, зате можна класти плитки, звʼязані сушею.
- Ferry (★3, +4 пірси, +1 жетон): 1 жетон → до 3 плиток по прямій; не міняється плитками, соло не лишає плитку.
- Submarine (★3, +4 Wreck у скид лицем догори): 2 жетони → `give(player, top_of_discard)`.
- Цифровий Exploration Mode: КОЛИ `custom: «плитки досліджено, очки нараховано»` → ТО `give(team, new_tiles)`; гра триває, «доки рахуєш» (скільки плиток за очко — (?)).
- Creative Mode: `custom: «необмежені плитки й рух, без рахунку-мети»`.
- Перемога/поразка: нема, спільний рахунок і звання · Рахунок: лише досліджені плитки за таблицею.

## Керування і ввід
- Настільна: свої плитки лицем догори перед собою, жетони під ними; хід по черзі.
- Цифрова: миша (є Mouse Only Option) або геймпад (повна підтримка: Xbox, DualShock 4, DualSense, Switch Pro, Steam Deck); плитку можна перетягнути drag & drop; з травня 2025 нема окремих режимів «рух / викладання».
- Локальний кооп до 4 на одному екрані (вікно призначення контролерів гравцям); онлайн — лише через Steam Remote Play Together.
- Камера: масштаб, напрям і чутливість налаштовуються.

## Вікна, меню, HUD
(цифрова версія)
- `main-menu` → `mode-select`: Exploration · Board Game (з Ships & Shores) · Creative; у кожного режиму 3 слоти збережень (`save-slots`).
- `treasury` (`custom-window`): усе відкриване — кораблі й плитки (лише для Exploration), чайки-супутники, прапори, мапи, фони; більшість відкривається звичайною грою й місіями.
- `character-select` (?): вибір корабля; вікно призначення контролерів у локальному коопі.
- `tutorial-window`: покрокове навчання; уроки плиток фільтруються за соло/мультиплеєром і ввімкненими доповненнями.
- `game-screen`: мапа плиток із кораблями; `pocket` — рука плиток; `movement-tokens` — жетони руху; рахунок; візуальні підказки, чому плитку не можна покласти (`conflict-highlight`); у мультиплеєрі — підказка «discard all tiles to end turn»; звук і анімація, коли нараховано очки чи прийшли нові плитки; рахунок пірсів і seal bank оновлюється наживо.
- `settings-window`: камера, гучність, Color Alternatives, 8 мов; `achievements-window` (Steam, 49).
- Переходи: main-menu → mode-select → слот → game-screen (автосейв на початку кожного ходу) → кінець партії (рахунок і звання — (?)).

## Фічі поза полем
- `mode-coop` + `local-multiplayer` до 4; онлайн — Remote Play Together.
- `mode-classic` (Board Game — вірна адаптація), `mode-endless` (Exploration: очки поповнюють запас плиток, відкриваються нові плитки й кораблі), `mode-sandbox` (Creative).
- `autosave` на початку кожного ходу, `save-slots` (3 на режим), `cloud-save`.
- `unlockables` + місії (`meta-progression`): кораблі з навичками (рибальський човен і плитки з рибальськими прапорцями — (?)), плитки, чайки, прапори, мапи; святкова косметика.
- `tutorial`, `colorblind-palette` (Color Alternatives), `gamepad-support`, `mouse-and-keyboard`, `localization` (8 мов, французька з 1.6.1).
- `custom-rules`: міні-доповнення вітряки й пірси та Ships & Shores вмикаються окремо.

## Варіації й родичі
- Настільна база (54 плитки + HQ) з двома міні-доповненнями в коробці (вітряки, пірси — червона стрілка); Ships & Shores (червень 2024) — 7 кораблів і 20 плиток; ще згадано доповнення Discovery Tiles (правил не бачили).
- Родичі в корпусі: `carcassonne.md` (збіг ребер, відкрита мапа, очки за завершене), `magic-maze.md` (кооп, мапа відкривається плитками), `forbidden-island.md` (кооп на плитках), `cartographers.md` (оточена гора дає нагороду), `kingdomino.md`, `isle-of-skye.md`; `build-sim/dorfromantik.md` — теж «очки поповнюють запас плиток».
- **Осі варіацій**: що рахується (оточена плитка — Beacon Patrol / завершена фіча — Carcassonne / оточена клітина — Cartographers) · як рухається аватар (заходить на покладене / кроки за жетони / телепорт до аванпосту / по прямій до 3) · запас (скінченний стос / поповнюється очками / нескінченний) · рука (3 / 2 / тримати одну соло) · спілкування в коопі (вільне — тут / заборонене — Magic Maze).

## Цікавинки для курсу
- Легальність плитки: 4 ребра «вода/суша» проти всіх сусідів + водне ребро до поточної + сусідство з кораблем — 📎.
- «Досліджена» = 4 сусіди; підсумковий рахунок за типами плиток і таблиця звань — 🌱.
- Досяжність корабля водою за N жетонів (BFS по водних ребрах, підсвітка досяжних плиток) — 📎.
- Рука, скидання = безкоштовний крок, обмін раз за хід, соло-«hold» однієї плитки — 🌱.
- 7 кораблів як модифікатори правил (лише власник і лише на своєму ході): телепорт, крок через сушу, рух по прямій, взяти зі скиду — 🥈 (система здібностей, що змінює легальність ходу й рахунок).
- Пірс і seal bank: очки за будинки/плитки звʼязаного острова — flood fill по суші через кілька плиток — 🥉.
- Exploration: очки поповнюють запас — нескінченна гра «поки рахуєш» — 📎.

## Мапа на каталог
- Є: `drag-drop-piece` ↔ перетягування плитки; `conflict-highlight` ↔ пояснення, чому сюди не можна; `move-4dir` + `impassable-cells` ↔ корабель водою, суша непрохідна; `turn-enforcement` ↔ хід по черзі; `event-effects` ↔ звук і анімація очок; `field-scaling` ↔ масштаб камери; `save-autosave` + `save-multi-slot`; `main-menu`, `mode-select`, `tutorial-window`, `achievements-window`, `game-screen`.
- **Нема** → пропозиції карток:
  - `+place-then-enter` «Покладена плитка одразу переносить аватар» · entities/move · 🌱.
  - `+discard-for-move` «Скинути карту/плитку → безкоштовний крок» · game-logic/economy · 🌱.
  - `+score-refills-supply` «Очки поповнюють запас — гра, доки рахуєш» · game-logic/win · 📎 (родич Dorfromantik).
  - `+fixed-orientation-tiles` «Плитки без повороту, єдина стрілка» · entities/legality · 🌱.
  - `+surround-reward`, `+edge-matching`, `+tile-exploration`, `+hand-of-tiles`, `+tile-exchange`, `+action-points`, `+variable-player-powers`, `+solo-rank-table` — уже в корпусі.

## Пропозиції до словників
- `+trigger:surrounded` — клітина/плитка отримала сусідів з усіх боків (досліджена плитка, оточена гора Cartographers).
- `+cond:edges_match` — типи ребер плитки збігаються з усіма сусідами (вода/суша, дороги Carcassonne).
- `+window:treasury` — галерея відкриваного контенту з умовами відкриття.
- `+ui:movement-tokens` — ряд жетонів руху з двома боками (доступний / витрачений).
- `+card:place-then-enter`, `+card:discard-for-move`, `+card:score-refills-supply` — див. «Мапа на каталог».

## Джерела
- ⭐ [RulesPal: Beacon Patrol rulebook](https://rulespal.com/beacon-patrol/rulebook) — компоненти, підготовка й таблиця рук/жетонів, хід, правила розміщення й руху, обмін, кінець ходу, «explored», очки 3/2/1 з прикладом, звання, вітряки й пірси, соло.
- [RulesPal: Ships & Shores](https://rulespal.com/beacon-patrol-ships-shores/rulebook) — 7 кораблів (зірки, плитки, здібності, рахунок), −10 очок за гравця, Lake лише для Hover Craft і Pilot Ship.
- [Steam: Beacon Patrol](https://store.steampowered.com/app/2273850/Beacon_Patrol/) — опис цифрової версії, три режими, «Your ship immediately moves onto the newly placed tiles», категорії (кооп на одному екрані, геймпад, Color Alternatives), 49 досягнень.
- [Steam News API](https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=2273850&count=20&maxlength=3000) — плейтест і демо (перші 4 кораблі, місії, Treasury, 3 слоти, автосейв, контролери), патчі 1.5.9–1.6.4 (пірси, вітряки, seal bank, субмарина, рибальський човен).
- [Bleeding Cool](https://bleedingcool.com/games/beacon-patrol-announces-first-expansion-ships-shores) — Pandasaurus Games анонсує Ships & Shores: 7 кораблів, червень 2024, $15.

## Непевне
- (?) Автор настільної гри (Torben Ratzlaff?), оригінальний видавець (Pegasus Spiele?) і рік першого видання (2022–2023?) — з памʼяті, у прочитаних джерелах не названі.
- (?) Скільки нових плиток дає Exploration Mode за досліджене і коли гра там закінчується.
- (?) Цифрові кораблі Exploration (рибальський човен, «навички», плитки рибальських прапорців) — у патчноутах лише згадки; чи збігаються вони з кораблями Ships & Shores.
- (?) Чи є окремий екран кінця партії зі званням у цифровій версії і як саме вибирається корабель.
- (?) Доповнення Discovery Tiles — лише назва.
