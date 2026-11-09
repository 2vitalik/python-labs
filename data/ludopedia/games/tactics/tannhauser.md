---
title: Tannhäuser
slug: tannhauser
aka: [Tannhauser, Тангейзер]
family: tactics
also: []
klass: figure
axes:
  field: graph
  time: turn
  opponent: hotseat
  info: partial
  random: runtime
  goal: state
year: 2007
platforms: [board]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Tannh%C3%A4user_(board_game)", best: true, note: "поле з кіл і кольорових стежок, лінія бачення = спільний колір, загін 3+2, режими, фракції, розширення"}
  - {kind: other, url: "https://rulespal.com/tannhauser/rulebook", note: "правила: кола-модифікатори, рух, ініціатива, дуелі d10, Combat/Shock Roll, трек здоровʼя, VP, паки, токени, зброя за дальністю, умови перемоги"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Tannhauser+board+game+how+to+play", note: "пошук; як грати"}
stage: v1
coverage: 60
mechanics: [hp-damage, melee-vs-ranged, impassable-cells, floor-types, inventory-items, item-pickup, explode-area, spawn-points, respawn, destroy-all-enemies, difficulty-levels, hot-seat, turn-enforcement, mode-select, match-setup, reachable-highlight, selection-highlight, +node-graph-board, +color-path-sight, +wound-track-stats, +dice-pool-successes, +opposed-dice-duel, +initiative-roll, +catch-up-initiative, +alternating-activation, +bull-rush, +victory-point-spend, +retaliation, +equipment-packs, +search-crate, +skill-objectives, +capture-the-flag, +domination-points, +smoke-zone, +weapon-range-bands, +squad-builder]
proposes: ["+effect:roll_dice", "+trigger:attacked", "+trigger:round_start", "+cond:same_path(a, b)", "+cond:distance(a, b, op, n)", "+effect:wound(a, n)", "+role:objective", "+ui:health-track", "+ui:dice-tray", "+ui:path-overlay", "+window:squad-builder", "+feature:custom-pack", "+axis:turn-structure:alternating-activation", "+card:color-path-sight"]
author: opus
date: 2026-11-09
---

# Tannhäuser — тактика загонів на полі-графі кіл, де бачиш і стріляєш лише вздовж стежки свого кольору

## Суть
Альтернативна Перша світова з окультизмом: два загони по 5 персонажів (герої й солдати) бʼються на друкованій карті замку, крипти чи міста. Поле — не сітка, а **граф кіл**, зʼєднаних кольоровими стежками: персонаж бачить і стріляє лише в тих, хто стоїть на колі **того самого кольору** (кола-перехрестя й двері мають кілька кольорів). Бій — пули d10 проти поточних характеристик, а кожна рана зсуває «повзунок» здоровʼя на рядок униз, і разом з ним падають усі характеристики. Окремий ресурс — **очки перемоги (VP)**, які витрачаються на рух, лікування, контратаку чи тимчасову навичку.

## Поле і час
- Поле — друкована карта (вид згори) з колами, куди можна ставати; сусідні кола одного кольору утворюють **Pathfinding Path** (стежку). Коло з кількома кольорами належить кільком стежкам — зазвичай на перехрестях і у дверях.
- Рух — по ребрах графа (сусіднє коло = 1 очко руху); лінія бачення — не геометрія, а **членство в стежці**: персонаж бачить усе на своїй стежці на 360°, союзники й вороги не заступають.
- Чорні кола (Objective Circles, Action Circles) не належать жодній стежці; в них не можна входити й крізь них проходити — на них лежать токени цілей і ящики.
- Кола-модифікатори: зелений символ характеристики дає +1 до поточного значення, червоний — −1; червоний символ руху коштує +1 очко руху на вихід.
- Час — **ігрові ходи**: на початку кидок ініціативи, далі гравці по черзі активують **по одному персонажу**; хід закінчується, коли кожен персонаж обох загонів активувався раз.
- Інформація: поле відкрите, вміст ящиків прихований до обшуку. Випадковість — d10.
- Гравців 2–10: двоє ведуть по загону, або кожен гравець — одного персонажа.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой (Hero) | piece | Combat, Stamina, Movement, Mental × рядки треку здоровʼя; навички Main/Secondary | активується раз за хід; може витратити до 2 VP за активацію; пак Combat/Stamina/Mental |
| Солдат (Trooper) | piece | ті самі 4 характеристики, слабші | до 1 VP за активацію; пак Combat/Stamina; може повернутись підкріпленням |
| Епічний герой (розширення) | piece | займає слот героя + солдата | значно сильніший; загін скорочується до 4 |
| Кольорове коло | terrain | колір(и) стежки | вузол графа: рух сюди, видимість по стежці |
| Багатокольорове коло | terrain | ≥2 кольори | належить кільком стежкам — точка, звідки видно в кілька коридорів |
| Коло-модифікатор | terrain | символ характеристики, зелений/червоний | ±1 до поточної характеристики, поки стоїш; червоний рух — +1 на вихід |
| Коло цілі / дії (чорне) | static | токен цілі або ящика | непрохідне, поза стежками; працюють із сусіднього кола |
| Точка входу (Entry Point) | spawner | обирається кидком розгортання | вхід коштує 1 очко руху; закінчити рух на ній не можна; сюди приходять підкріплення |
| Ящик (Crate) | container | лицем донизу | обшук із сусіднього кола без сусіднього ворога → спорядження або VP |
| Спорядження (токен) | pickup | одноразове — штрихова рамка | можна кинути, передати, підняти; падає на коло при смерті власника |
| Ціль Main / Secondary | zone | золота — 2 навички, срібна — 1 | виконується персонажем з потрібними навичками (Story mode) |
| Прапор | object | — | захопити й донести (CTF) / поставити на коло цілі (Domination) |
| Уламки (Debris) | terrain | +1 штраф руху | лишає граната або TNT |
| Димова завіса | hazard | −5 Combat/Stamina у своєму колі, −3 на інших колах стежки | значення не падає нижче 1 |
| Hermetica | hazard | ставиться на порожнє коло стежки | окультний ефект зони (?) |
| Граната | projectile | на порожнє коло ≥4 кіл по стежці | бʼє кожного в сусідніх колах автоматичною раною |
| Очко перемоги (VP) | resource | старт 2 на сторону | валюта дій: +рух, лікування, контратака, перекид ініціативи, навичка |
| d10 | object | пул = поточна характеристика | успіх — грань ≥ складності; натуральні 10 і 1 особливі |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `custom: «початок ігрового ходу»` → ТО кожен гравець `custom: «кидає d10 +1 за кожного свого загиблого персонажа»`; вищий починає, нічия — перекид.
- КОЛИ `input(activate, character)` → ЯКЩО `turn_of(player)` and `not state(character, activated)` → ТО `set_state(character, activated)`, після активації `end_turn` — ходить суперник.
- КОЛИ `custom: «усі персонажі обох загонів активувались»` → ТО `custom: «кінець ігрового ходу, нова ініціатива»`.
- КОЛИ `input(move, a, circle)` → ЯКЩО `custom: «коло сусіднє за графом»` and `counter(movement_points, >, 0)` → ТО `move(a, circle)`, `counter(movement_points, -1)`; очок руху = поточна Movement.
- КОЛИ `leave(a, red_movement_circle)` → ТО `counter(movement_points, -1)` додатково; кілька штрафів руху не складаються — діє найбільший.
- КОЛИ `enter(a, modifier_circle)` → ТО `set_state(a, stat_mod)` — ±1 до характеристики за символом; КОЛИ `leave(a, modifier_circle)` → ТО `clear_state(a, modifier)`.
- КОЛИ `input(move, a, circle)` → ЯКЩО `cell(circle, objective_circle | action_circle)` → ТО `block`.
- КОЛИ `input(move, a, circle)` → ЯКЩО `occupied(circle, ally)` → ТО `move(a, circle)` транзитом; закінчити рух на зайнятому колі не можна.
- КОЛИ `input(move, a, circle)` → ЯКЩО `occupied(circle, enemy)` → ТО `custom: «Bull Rush — дуель Stamina; переміг — проходить; витрачає фазу дії»`.
- КОЛИ `enter(a, entry_point)` → ТО `counter(movement_points, -1)`; `custom: «закінчити рух на точці входу не можна»`.
- КОЛИ `input(action, a)` → ТО `custom: «фаза дії — рівно одна: дія, Bull Rush, спорядження, кинути/передати/підняти, обшук або атака»`; рух можна перервати фазою дії й доходити рештою очок.
- КОЛИ `input(attack, a, b)` → ЯКЩО `custom: «a і b на спільній кольоровій стежці»` and `custom: «відстань відповідає типу зброї»` → ТО `custom: «Combat Roll: пул d10 = Combat(a), складність = Combat(b); кожен успіх — влучання»`.
- КОЛИ `custom: «є влучання»` → ТО `custom: «Shock Roll захисника: пул = Stamina(b), складність = використаний Combat(a); кожен успіх скасовує одне влучання»`.
- КОЛИ `custom: «влучання не скасоване»` → ТО `damage(b, 1)`, `custom: «індикатор здоровʼя на рядок униз — поточні характеристики беруться з нового рядка»`.
- КОЛИ `custom: «індикатор опустився нижче останнього рядка»` → ТО `disappear(b)`, `spawn_at(disposable_equipment, circle_of_b)`.
- КОЛИ `input(attack, a, b)` → ЯКЩО `adjacent(a, b)` and `not has(a, weapon)` → ТО `custom: «рукопашна: обидва беруть найнижчий рядок Combat»`.
- КОЛИ `custom: «на кубику натуральна 10»` → ТО `custom: «успіх, штрафи не діють»`; КОЛИ `custom: «натуральна 1»` → ТО `custom: «бонуси не діють»`.
- КОЛИ `custom: «дуель Stamina або Mental»` → ТО `custom: «пул нападника = його поточне значення, складність = значення захисника; більше успіхів перемагає, нічия — захиснику»`.
- КОЛИ `input(attack, heavy_weapon)` → ТО `custom: «влучання = автоматичні рани»`; контратака й додаткові набої неможливі; без навички Athletics носій рухається за найнижчим Movement.
- КОЛИ `input(throw, grenade, circle)` → ЯКЩО `free(circle)` and `custom: «на тій самій стежці, ≥4 кіл»` → ТО `custom: «окремий Combat Roll кожному в сусідніх колах + автоматична рана, яку Shock не скасовує»`, `spawn_at(debris, circle)`.
- КОЛИ `custom: «на колі стежки стоїть дим»` → ТО `custom: «−5 Combat і Stamina у колі диму, −3 на інших колах тієї стежки, не нижче 1»`.
- КОЛИ `input(search, a, crate)` → ЯКЩО `adjacent(a, crate)` and `adjacent_count(a, enemy, ==, 0)` → ТО `reveal(crate)`, `give(a, equipment)` або `currency(+n)`.
- КОЛИ `input(spend_vp, a)` → ЯКЩО `custom: «витрачено цієї активації < 2 (герой) або < 1 (солдат)»` → ТО `currency(-1)` і одне з: `speed(a, +1)` · `heal(a, 1)` (рядок треку) · перекид меншого кубика ініціативи (раз за хід) · `custom: «купити навичку на активацію: 1 VP Secondary, 2 VP Main»`.
- КОЛИ `custom: «ворог атакував, ціль вижила»` → ЯКЩО `custom: «є 1 VP»` → ТО `currency(-1)`, `custom: «контратака одразу»`.
- КОЛИ `all_gone(enemy_heroes)` → ТО `currency(+2)`; КОЛИ `counter(enemy_troopers_killed, ==, 2)` → ТО `currency(+1)` (на Easy — ще раз після четвертого).
- КОЛИ `died(trooper)` → ЯКЩО `counter(reinforcements, >, 0)` → ТО `respawn(trooper, entry_point)`; підкріплень: Easy 2, Normal 1, Hard 0.
- КОЛИ `input(action, a, objective)` → ЯКЩО `adjacent(a, objective)` and `has(a, skill)` (1 — Secondary, 2 — Main) → ТО `custom: «ціль виконано»`, `score(+vp)`.
- Перемога: Deathmatch — КОЛИ `all_gone(enemy_characters)` → ТО `win` · Story — КОЛИ `custom: «виконано 2 Main або 1 Main + 2 Secondary»` → ТО `custom: «кінець, більше VP перемагає»` · CTF — КОЛИ `custom: «2 ворожі прапори донесено до своєї точки входу / кіл цілей»` → ТО `win` · Domination — КОЛИ `custom: «четвертий прапор поставлено на четверте різне коло цілі»` → ТО `win` · King of the Hill — VP лише за вбивство лідера. Будь-який режим — нічия за згодою або пат.

## Керування і ввід
- Настільна гра: гравець обирає персонажа для активації, переставляє фігурку по колах, оголошує фазу дії, кидає пул d10. Трек здоровʼя — повзунок на карті персонажа.
- (цифрова версія) клік по фігурці → підсвітка досяжних кіл за очками руху (`reachable-highlight`) і стежок, на яких вона «бачить»; клік по ворогу на тій самій стежці → атака обраною зброєю; кнопки витрати VP, обшуку, гранати; ворог поза стежкою не клікабельний.
- Порядок: чергування активацій по одному персонажу (не «весь загін за хід»).

## Вікна, меню, HUD
- (цифрова версія) `main-menu` → `mode-select` (Deathmatch · Story · CTF · Domination · King of the Hill · сюжетні місії) → `match-setup` (мапа й бік поля, складність Easy/Normal/Hard = кількість підкріплень) → `+window:squad-builder` (5 персонажів однієї приналежності: 3 герої + 2 солдати або 2 + 3; пак кожному — стандартний з особливим предметом або власний з 3 токенів) → кидок розгортання й вибір точки входу → `game-screen`.
- `game-screen`: граф кіл на карті; `+ui:path-overlay` — підсвітка кольору стежки вибраного персонажа; карти персонажів з `+ui:health-track`; `turn-indicator` / порядок активацій; лічильник VP обох сторін; `+ui:dice-tray` (пул d10, успіхи, натуральні 10/1); `remaining-counter` підкріплень; іконки спорядження (`inventory-bar`).
- `confirm-dialog` перед витратою VP; `end-screen` з переможцем і VP.
- `help-window` / `codex-window` персонажів і спорядження.

## Фічі поза полем
- Режими: Deathmatch (базовий), Story (VP + цілі + відродження), сюжетні місії з наперед заданими персонажами, Capture the Flag, Domination, King of the Hill.
- Складність = кількість підкріплень солдатів (2 / 1 / 0).
- Побудова загону: приналежність (Union, Reich, Matriarchy, Shogunate), альянси двох фракцій (Nippon Accords, UMTOMA); паки спорядження, пізніше — Equipment Cards.
- Двостороння дошка в базі (Castle Ksiaz / крипта), нові мапи з розширеннями (Operation Novogrod, Daedalus, Hinansho, Frankenstahl).
- Мультиплеєр: 2 загони або до 10 гравців по персонажу (`hotseat` за столом).

## Варіації й родичі
- Родичі в корпусі: [Heroscape](heroscape.md) (мініатюри + карти статів), [Zombicide](zombicide.md) (зони замість клітин, спільна видимість), [HeroQuest / Space Hulk](heroquest-space-hulk.md) (коридори й лінія бачення), [Summoner Wars](summoner-wars.md) (карти як фігури), [HeroClix](heroclix.md) (стати падають з пораненням).
- **Осі варіацій**:
  - **поле**: квадрати / гекси / **граф кіл** (Tannhäuser) / зони ([Zombicide](zombicide.md));
  - **лінія бачення**: геометрична (трасування через клітини) / **членство в кольоровій стежці** / зона;
  - **поранення**: HP-лічильник / **трек, що знижує всі стати** (Tannhäuser, [HeroClix](heroclix.md)) / маркери ран;
  - **порядок**: увесь загін за хід / **чергування по одній фігурі** / маркери наказів ([Heroscape](heroscape.md));
  - **ресурс дій**: нема / VP як валюта бонусів (Tannhäuser) / очки дій.

## Цікавинки для курсу
- Поле-граф із кольоровими стежками: суміжність = ребра, видимість = спільний колір — 📎 (два словники над одним графом, без трасування променів).
- Трек здоровʼя, де кожна рана міняє всі чотири характеристики (таблиця рядків) — 🌱.
- Пул d10 проти поточного значення суперника + Shock Roll, що скасовує влучання, — 🌱 (дві фази кидка, натуральні 10/1).
- Дим як аура на стежці: −5 у своєму колі, −3 на всій стежці, мінімум 1 — 📎.
- VP як валюта з лімітом витрати на активацію (2 герой / 1 солдат) і меню з 5 витрат — 📎.
- Чергування активацій по одному персонажу + ініціатива з бонусом відстаючому — 🌱.
- Цілі, що потребують 1–2 навичок, і купівля відсутньої навички за VP — 📎.

## Мапа на каталог
- Є: `hp-damage` ↔ трек здоровʼя · `melee-vs-ranged` ↔ рукопашна проти вогнепальної · `impassable-cells` ↔ чорні кола · `floor-types` ↔ кола-модифікатори · `inventory-items` + `item-pickup` ↔ спорядження, кинути/передати/підняти · `explode-area` ↔ граната по сусідніх колах · `spawn-points` + `respawn` ↔ точки входу й підкріплення · `destroy-all-enemies` ↔ Deathmatch · `difficulty-levels` ↔ Easy/Normal/Hard · `hot-seat`, `turn-enforcement`, `mode-select`, `match-setup`, `reachable-highlight`, `selection-highlight`.
- **Нема** → пропозиції карток:
  - `+node-graph-board` «Поле-граф вузлів» · entities/legality · 📎 · слот {nodes, edges} — рух по ребрах, не по клітинах.
  - `+color-path-sight` «Видимість по кольорових стежках» · entities/combat · 📎 · слот {colors_per_node} — атака лише в межах спільного кольору.
  - `+wound-track-stats` «Трек ран змінює всі стати» · entities/state · 🌱 · слот {rows}.
  - `+dice-pool-successes` «Пул кубиків, успіх ≥ порогу» · entities/combat · 🌱 · слот {die: d10, natural_rules}.
  - `+opposed-dice-duel` «Дуель пулів, нічия — захиснику» · entities/combat · 🌱.
  - `+initiative-roll` / `+catch-up-initiative` «Ініціатива кидком; +1 за кожного свого загиблого» · game-logic/opponent · 🌱.
  - `+alternating-activation` «Чергування активацій по одній фігурі» · game-logic/opponent · 🌱.
  - `+bull-rush` «Прорив крізь ворога дуеллю» · entities/combat · 📎.
  - `+victory-point-spend` «VP як валюта бонусів з лімітом на активацію» · game-logic/economy · 📎.
  - `+retaliation` (контратака за 1 VP) · `+equipment-packs` · `+search-crate` · `+skill-objectives` · `+capture-the-flag` · `+domination-points` · `+smoke-zone` · `+weapon-range-bands` «тип зброї задає мінімальну дальність» · `+squad-builder`.

## Пропозиції до словників
- `+effect:roll_dice` — кинути пул кубиків як ефект (Combat Roll, Shock Roll, ініціатива).
- `+trigger:attacked` — сутність стала ціллю атаки (контратака, Shock Roll).
- `+trigger:round_start` — початок ігрового ходу/раунду (кидок ініціативи).
- `+cond:same_path(a, b)` — дві сутності на спільній кольоровій стежці графа; основна умова атаки.
- `+cond:distance(a, b, op, n)` — відстань у вузлах графа з мінімумом (граната ≥4, зброя з мінімальною дальністю); `in_range` має лише «≤».
- `+effect:wound(a, n)` — рана, що зсуває трек стану, а не віднімає HP.
- `+role:objective` — токен цілі, з яким взаємодіють навичкою (Main/Secondary).
- `+ui:health-track` — повзунок по рядках характеристик; `+ui:dice-tray` — результат пулу; `+ui:path-overlay` — підсвітка стежки, видимої персонажу.
- `+window:squad-builder` — складання загону з паками; `+feature:custom-pack` — власний пак з 3 токенів без особливого предмета.
- `+axis:turn-structure:alternating-activation` — по одній фігурі від кожної сторони по черзі.
- `+card:color-path-sight` — видимість як членство в кольоровій підмножині графа.

## Джерела
- ⭐ [Wikipedia: Tannhäuser (board game)](https://en.wikipedia.org/wiki/Tannh%C3%A4user_(board_game)) — pathfinding-стежки й лінія бачення через спільний колір, загін 3 герої + 2 солдати, епічні герої, режими, фракції й альянси, склад базової коробки (6 d10, 160 токенів), розширення.
- [RulesPal: Tannhäuser rulebook](https://rulespal.com/tannhauser/rulebook) — повні правила: кола-модифікатори, рух, Bull Rush, ініціатива, дуелі, Combat/Shock Roll, трек здоровʼя, VP, паки, ящики, дим, гранати, типи зброї, умови перемоги режимів.
- YouTube: пошук «Tannhauser board game how to play».

## Непевне
- (?) Типи зброї: RulesPal пише «minimum range 2 / 3 / 4» для Close Combat / Automatic / Heavy — чи це мінімальна відстань, чи дальність типу, з уривка не ясно.
- (?) Розбіжність складу загону: Wikipedia — 3 герої + 2 солдати; RulesPal — також 2 + 3.
- (?) Ефект токена Hermetica — у прочитаному уривку лише разом з димом; точна дія не перевірена.
- (?) Story mode: відродження вибулих — за Wikipedia; механіку відродження в правилах не дочитав.
- (?) Офіційної цифрової версії не знайшов; вікна описані як «цифрова версія».
- (?) Дизайнери (William Grosselin, Didier Poli) — з памʼяті, у статті не названі.
