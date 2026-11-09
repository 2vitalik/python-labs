---
title: Card Hunter
slug: card-hunter
aka: []
family: tactics
also: [board-digital]
klass: figure
axes:
  field: square
  time: turn
  opponent: ai
  info: partial
  random: runtime
  goal: score
year: 2013
platforms: [web, PC, Mac]
links:
  - {kind: official, url: "https://www.cardhunter.com/how-to-play-card-hunter/", best: true, note: "офіційні правила: типи карт, keywords, структура раунду, терени, перемога, раси, міньйони"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Card_Hunter", note: "Gary-GM, колода з класу/раси/спорядження, модулі, лут, PvP/coop, монетизація"}
  - {kind: steam, url: "https://store.steampowered.com/app/293260/Card_Hunter/", note: "standalone-клієнт 2015"}
  - {kind: official, url: "https://www.cardhunter.com/", note: "форуми, FAQ, Discord"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Card+Hunter+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [hp-damage, line-of-sight-attack, melee-vs-ranged, impassable-cells, floor-types, status-effects, temporary-modes, multi-cell-size, inventory, inventory-items, unit-xp-skills, shop-window, shop-between-levels, shop-catalog, shop-buyback, destroy-all-enemies, event-points, time-out, pass-turn, ai-opponent, online-multiplayer, rating-system, difficulty-levels, sequential-levels, level-select, world-map, character-select, pocket, selection-highlight, reachable-highlight, game-screen, main-menu, end-screen, +deck-draw, +equipment-cards, +reactive-cards, +victory-squares, +armor-roll, +attachments-limit, +group-minions, +alternate-card-play]
proposes: ["+effect:draw_card", "+effect:discard", "+role:card", "+trigger:attacked", "+trigger:round_start", "+trigger:round_end", "+trigger:both_passed", "+effect:roll_dice", "+effect:attach_card", "+cond:from_behind", "+window:equip-window", "+window:loot-window", "+ui:hand-per-character", "+feature:loot-chests"]
author: opus
date: 2026-11-09
---

# Card Hunter — тактика, де спорядження = колода: кожен предмет кладе свої карти, а бій грається на картонному полі в «настолці» з невмілим майстром Гері

## Суть
Гравець збирає загін до трьох героїв і проходить модулі-пригоди, які веде гейм-майстер Gary (пародія на D&D-сесію). Колоду кожного героя не збирають руками: її складають клас, раса і **спорядження** — кожен предмет додає фіксований набір карт. Бій на прямокутній сітці з картонними фігурками: сторони по черзі грають **по одній карті** будь-якого героя, доки обидві не спасують. Перемога — набрати потрібну кількість зірок за вбивства й утримання клітин-цілей.

## Поле і час
- Прямокутне квадратне поле модуля (кімната, ліс, підземелля) з клітинами-тереном; фігури — стоячі картонки, деякі вороги 2×2.
- Типи тайлів: open (звичайний), difficult (зупиняє рух при вході), impassable (не ввійти, але лінія бачення проходить — провалля, глибока вода), blocked (не ввійти і блокує лінію; товста чорна рамка).
- На тайли й героїв можна «вішати» attachments — тривалі ефекти з лічильником раундів; terrain-ефекти спрацьовують на початку раунду.
- Час — **раунди**: добір → почергова гра по одній карті до двох пасів поспіль → скидання до 2 карт → підрахунок клітин-цілей.
- Інформація часткова: поле видно, руку суперника — ні; добір і броня — випадкові.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой | player | клас, раса, HP, слоти спорядження | має власну колоду і руку; діє лише картами |
| Клас (воїн / маг / жрець) | — | дозволені типи предметів | визначає, що можна вдягнути, отже які карти в колоді |
| Раса (human / elf / dwarf) | — | бойові бонуси, базова карта руху | Run 3 (human) · Dash 4 (elf) · Walk 2 (dwarf) щораунду |
| Предмет | container | слот, рівень | кладе в колоду свій набір карт; міняється лише між боями |
| Колода / рука / скидання | supply | рука після раунду ≤ 2 | добір щораунду; скидання перетасовується, коли колода порожня |
| Карта Attack | supply | дальність, шкода, ціль | шкода або шкідливий ефект; деякі цілять у клітини (Fireball) |
| Карта Move | supply | клітин | рух героя; зіграну не скасувати |
| Карта Armor | supply | поріг кубика, Keep | не грається: при атаці кидок ≥ порогу зменшує шкоду; зазвичай Keep |
| Карта Block | supply | — | не грається: скасовує атаку, коли героя обрано ціллю, і скидається; не діє проти атаки ззаду |
| Карта Assist | supply | — | користь союзникам (лікування) |
| Карта Utility | supply | — | рухає ворогів / знімає шкідливі attachments з тайлів |
| Карта Boost (Trait) | supply | — | бонус; Trait грається безкоштовно на початку раунду власника |
| Карта Handicap | supply | — | шкода собі; переважно Trait — грається на старті раунду, одразу добір заміни |
| Attachment | zone | тривалість у раундах; ≤ 3 на героя | тривалий ефект на героєві чи тайлі; четвертий витісняє найстаріший |
| Ворог-герой / монстр | enemy | HP, колода, зірки за вбивство | грає карти за Gary (AI) |
| Великий ворог 2×2 | enemy | 4 клітини | бере терен лише однієї клітини (першої, рахуючи від нижньої) |
| Група міньйонів | enemy | спільна рука | рухаються групою; кожен — одна не-move дія за раунд (потім сірий); добір падає, коли міньйони гинуть |
| Клітина-ціль (victory square) | zone | — | наприкінці раунду той, у кого більше фігур на цілях, отримує зірку |
| Difficult-тайл | terrain | — | рух зупиняється при вході |
| Impassable-тайл | static | — | не ввійти; лінію не блокує |
| Blocked-тайл | static | — | не ввійти; блокує лінію |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `level_start` → ТО `custom: «кожен герой добирає 4 карти»`.
- КОЛИ `custom: «початок раунду»` → ТО спрацьовують ефекти: карти в руці → attachments → терен; прострочені attachments `disappear`.
- КОЛИ `custom: «початок раунду»` → ТО кожен герой `custom: «добирає 2 карти»` і `give(hero, racial_move_card)` (базова карта руху раси; після використання знищується, а не скидається).
- КОЛИ `custom: «колода порожня, треба добрати»` → ТО `custom: «перетасувати скидання в колоду»`.
- КОЛИ `custom: «на початку раунду в руці Trait»` → ТО `custom: «Trait грається безкоштовно»`; ЯКЩО це Handicap → ТО ще й `custom: «добір заміни»`.
- КОЛИ `input(play_card, card, target)` → ЯКЩО `turn_of(side)` → ТО ефект карти, карта в скидання (passive-карти лишаються в грі), хід → `end_turn`.
- КОЛИ `input(pass)` → ТО `pass_turn`; КОЛИ `custom: «обидві сторони спасували поспіль»` → ТО кінець раунду; першим наступного раунду ходить той, хто спасував першим.
- КОЛИ `input(play_card, move)` → ТО `move(hero, to)` до N клітин; ЯКЩО `cell(next, difficult)` або `adjacent(hero, enemy)` → ТО `custom: «рух зупиняється»`.
- КОЛИ `input(play_card, move)` → ЯКЩО `not free(cell)` (impassable / blocked / фігура) → ТО `block`.
- КОЛИ `input(play_card, attack, target)` → ЯКЩО `line_of_sight(hero, target) and in_range(hero, target, r)` → ТО `custom: «атака»`; інакше `block`.
- КОЛИ `custom: «героя обрано ціллю атаки»` → ЯКЩО `has(target, block_card) and not custom: «атака ззаду»` → ТО атака скасована, Block-карта скидається.
- КОЛИ `custom: «атака влучила»` → ЯКЩО `has(target, armor_card)` → ТО `custom: «кидок кубика броні»`; ЯКЩО `custom: «кидок ≥ порогу»` → ТО `damage(n − armor)`; Keep → карта лишається в руці, інакше скидається.
- КОЛИ `custom: «атака Penetrating»` → ТО Armor не спрацьовує, `damage(n)`.
- КОЛИ `input(play_card, utility, enemy)` → ТО `move(enemy, to)` або `custom: «зняти attachment з тайла»`.
- КОЛИ `input(play_card, assist, ally)` → ТО `heal(ally, n)` або `set_state(ally, buff, rounds)`.
- КОЛИ `custom: «новий attachment на героя»` → ЯКЩО `count(attachments, =, 3)` → ТО `custom: «найстаріший attachment зникає»`.
- КОЛИ `hp_zero(unit)` → ТО `disappear(unit)`, `counter(stars, +1)` стороні-вбивці (деякі монстри дорожчі; у PvP вбивство героя = 2).
- КОЛИ `custom: «кінець раунду»` → ЯКЩО `custom: «у руці > 2 карт»` → ТО `custom: «скинути до 2»`.
- КОЛИ `custom: «кінець раунду»` → ЯКЩО `custom: «у сторони більше фігур на victory squares»` → ТО `counter(stars, +1)`; нічия — нічого.
- КОЛИ `counter(stars, >=, n)` → ТО `win` тієї сторони.
- КОЛИ `all_gone(enemy)` → ТО `win` (total annihilation).
- КОЛИ `timer(<=, 0)` → ЯКЩО `mode(timed)` (деякі бої, рейтинговий PvP) → ТО `lose`.
- КОЛИ `custom: «міньйон групи виконав не-move дію»` → ТО `set_state(minion, spent, 1 round)`; КОЛИ `died(minion)` → ТО `custom: «група добирає менше карт»`.
- КОЛИ `win` → ТО `window(loot-window)`: випадковий лут, XP; КОЛИ `custom: «рівень героя зріс»` → ТО `unlock(equipment_slot)`.
- Перемога: набрати зірки (вбивства + клітини-цілі) або знищити всіх · Поразка: суперник набрав першим / вичерпано час · Рахунок: зірки бою; поза боєм — лут, золото, XP.

## Керування і ввід
- Миша: клік по карті в руці героя → підсвітка допустимих клітин/цілей → клік по цілі; Attack за замовчуванням цілить у ворогів, Assist — у своїх; з Ctrl — навпаки.
- Будь-яка карта будь-якого героя загону в свій «хід» (одна карта = одна дія); кнопка Pass.
- Move-карту, раз зіграну, не скасувати.

## Вікна, меню, HUD
- `main-menu` (цифрова гра): кампанія · мультиплеєр (PvP) · магазин · вийти.
- `map-window` — мапа світу з модулями-пригодами; модулі мають рівні складності; пройдені можна переграти.
- `character-select` — склад загону з 3 героїв із ширшого ростеру; найм нових героїв.
- `custom-window` «екіпірування» — слоти героя за класом, предмети, перегляд колоди, яку вони дають.
- `game-screen`: поле-«настолка», фігурки; `pocket` — рука кожного героя; `hp-bar`; іконки attachments з лічильником раундів; `remaining-counter`/рахунок зірок обох сторін; `selection-highlight`, `reachable-highlight`; кнопка Pass; репліки Gary (`message`).
- `end-screen` + `custom-window` «loot» — скрині з лутом після бою.
- `shop-window` — купівля/продаж спорядження й скарбів; частина асортименту з обмеженим часом.
- `lobby-window` — PvP і кооп (2–3 гравці, кожен веде одного героя).

## Фічі поза полем
- Кампанія з модулів (`world-map`); складніший модуль — сильніші вороги, кращий лут, більше XP.
- Прогресія героя: XP → нові слоти спорядження (`xp-level`); предмети міняються лише між боями.
- Магазин зі змінним асортиментом; продаж назад.
- PvP з поточними героями або готовими наборами; кооп 2–3 гравці (на двох — кожен добирає додаткову карту замість третього героя).
- Монетизація: валюта «pizza» → косметичні фігурки, скрині, золото; підписка Card Hunters Club — +1 предмет луту після бою.
- Сюжетна рамка: Gary «ще вчиться», спершу дає сильніших героїв брата Melvin, потім той їх забирає (вбудований туторіал).

## Варіації й родичі
- Родичі в корпусі: [gloomhaven](gloomhaven.md) (карти = дії в тактиці), [fights-in-tight-spaces](fights-in-tight-spaces.md) (колода + сітка), [heroquest-space-hulk](heroquest-space-hulk.md) (настільна тактика з майстром), [mage-knight](mage-knight.md) (карти як рух/атака).
- Поза корпусом: Slay the Spire (декбілдинг без поля), D&D 4e (сітка й ролі).
- **Осі варіацій**: колода — збирається з карт (StS) / виводиться з предметів (Card Hunter) / фіксована на героя (Gloomhaven) · хід — по одній карті з пасом (Card Hunter) / вся рука за хід (FiTS) · захист — реактивні карти в руці (Armor, Block) / ресурс блоку · перемога — зірки за вбивства + клітини-цілі / знищити всіх.

## Цікавинки для курсу
- Колода як функція спорядження: предмет = список карт; зміна предмета перебудовує колоду — 📎 (дані → колода).
- Почергова гра по одній карті до двох пасів поспіль, перший, хто спасував, починає наступний раунд — 🥉 (нестандартна черговість).
- Реактивні карти, що лежать у руці: Armor (кидок ≥ порогу, Keep) і Block (не ззаду) — 🥉 (обробник події «на тебе напали»).
- Victory squares + зірки за вбивства як подвійна умова перемоги — 📎.
- Attachments з лічильником раундів і лімітом 3 (витісняє найстаріший) — 📎 поверх `status-effects`.
- Група міньйонів зі спільною рукою, добір падає з втратами — 🥉.
- Типи тайлів за двома осями «прохідність × лінія бачення» (open/difficult/impassable/blocked) — 🌱.

## Мапа на каталог
- Є: `hp-damage` · `line-of-sight-attack` ↔ лінія бачення й blocked-тайли · `melee-vs-ranged` · `impassable-cells` · `floor-types` ↔ difficult-тайл · `status-effects` / `temporary-modes` ↔ attachments · `multi-cell-size` ↔ вороги 2×2 · `inventory` / `inventory-items` ↔ спорядження · `unit-xp-skills` ↔ XP → слоти · `shop-window` / `shop-between-levels` / `shop-catalog` / `shop-buyback` · `destroy-all-enemies` · `event-points` ↔ зірки · `time-out` · `pass-turn` · `ai-opponent` (Gary) · `online-multiplayer` / `rating-system` (PvP) · `difficulty-levels` ↔ складність модуля · `world-map` / `level-select` ↔ модулі · `character-select` · `pocket` ↔ рука.
- **Нема** → пропозиції карток:
  - `+deck-draw` «Колода / рука / скидання з перетасовкою» · entities/state · 🥉 · слоти {draw_per_round, keep_limit}.
  - `+equipment-cards` «Предмет додає карти в колоду» · entities/state · 📎 · {item → cards}.
  - `+reactive-cards` «Карти, що спрацьовують з руки на подію» · game-logic/opponent · 🥉 · {trigger, keep}.
  - `+victory-squares` «Утримання клітин-цілей наприкінці раунду» · game-logic/win · 🌱.
  - `+armor-roll` «Кидок кубика проти порогу броні» · entities/combat · 🌱 · {threshold, reduce}.
  - `+attachments-limit` «Ліміт тривалих ефектів, найстаріший витісняється» · entities/state · 🌱 · {max: 3}.
  - `+group-minions` «Група юнітів зі спільною рукою/діями» · entities/combat · 📎.
  - `+alternate-card-play` «По одній дії по черзі до двох пасів» · game-logic/turns · 📎.

## Пропозиції до словників
- `+effect:draw_card` — добрати N карт у руку (не `draw` = нічия).
- `+effect:discard` — карта йде в скидання (скидання до ліміту наприкінці раунду).
- `+role:card` — карта як сутність поза полем (рука/колода).
- `+trigger:attacked` — сутність обрали ціллю атаки (Block/Armor).
- `+trigger:round_start` / `+trigger:round_end` — початок/кінець раунду, коли раунд ≠ хід сторони.
- `+trigger:both_passed` — усі сторони спасували поспіль (кінець раунду в «пасових» іграх).
- `+effect:roll_dice` — кинути кубик і порівняти з порогом (броня).
- `+effect:attach_card` — повісити тривалий ефект-картку на сутність/клітину з лічильником.
- `+cond:from_behind` — атака ззаду відносно орієнтації цілі.
- `+window:equip-window` — слоти спорядження героя з переглядом карт, які вони дають.
- `+window:loot-window` — скрині/лут після бою.
- `+ui:hand-per-character` — окрема рука для кожного героя загону.
- `+feature:loot-chests` — випадкові скрині предметів за валюту/підписку.

## Джерела
- ⭐ [How to play Card Hunter](https://www.cardhunter.com/how-to-play-card-hunter/) — типи карт, Keep/Penetrating/Trait, 7 кроків раунду, 4 типи тайлів, victory stars і squares, attachments, 2×2, раси й базові карти руху, міньйони.
- [Wikipedia](https://en.wikipedia.org/wiki/Card_Hunter) — Gary і Melvin, загін до 3, колода з класу/раси/предметів, 4 карти на старті бою, модулі й складність, лут, PvP, кооп 2015, pizza і клуб.
- [Steam](https://store.steampowered.com/app/293260/Card_Hunter/) — standalone-версія 13.07.2015.
- [Офіційний сайт](https://www.cardhunter.com/) — форуми, FAQ, Discord; вікі Cardhuntria не відкрилась.
- YouTube: пошук «Card Hunter gameplay».

## Непевне
- (?) Колода героя 36 карт — у Вікіпедії з позначкою «citation needed».
- (?) Wikipedia пише «typically three» карти на раунд, офіційні правила — 2 + базова карта руху; узгоджено як 2+1.
- (?) Як визначається орієнтація фігури (для «атаки ззаду») — не перевірено.
- (?) Кидок ініціативи на старті раунду (поза правилом «хто першим спасував») — не бачив у джерелах.
- (?) Точний перелік слотів спорядження за класами та кількість карт на предмет — не перевірено (вікі недоступна).
- (?) Номенклатура класів «воїн / маг / жрець» — з памʼяті, у відкритих джерелах класи не названо.
