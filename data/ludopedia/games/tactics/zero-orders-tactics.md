---
title: Zero Orders Tactics
slug: zero-orders-tactics
aka: [ZOT, "Zero Orders Tactics: Under"]
family: tactics
also: [roguelike]
klass: cursor
axes:
  field: hex
  time: turn
  opponent: ai
  info: partial
  random: both
  goal: state
year: 2024
platforms: [Windows, macOS, web (itch beta)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1877650/Zero_Orders_Tactics/", best: true, note: "офіційний опис: наказів нема, рельєф і класи як зброя, фіксований пошук шляху, без output-рандому, колода заклять і юнітів; реліз 04.11.2024"}
  - {kind: other, url: "https://steamcommunity.com/groups/TheIrregularGamer/discussions/0/592884025032506586", note: "найдокладніший огляд: дії за хід, мана, 5 типів терену, квести 3–9 ходів, Ironman, боси"}
  - {kind: other, url: "http://www.thegeeklygrind.com/all-posts/zero-order-tactics-intial-demo-imprssions", note: "демо: улюблений / неулюблений / непрохідний терен, рух зліва направо, превʼю ворога"}
  - {kind: itch, url: "https://pauloondra.itch.io/zero-orders-tactics", note: "бета 0.575 у браузері + девлоги (енергія-гекс, фаза розстановки, скрині)"}
  - {kind: steam, url: "https://store.steampowered.com/app/4116860/Zero_Orders_Tactics_Under/", note: "DLC Under (19.11.2025): 7-ма фракція, 3 герої, 3 боси"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Zero+Orders+Tactics+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [hp-damage, impassable-cells, floor-types, cursor-place, cell-click, telegraphed-intents, path-preview, undo-unlimited, spawn-points, unit-xp-skills, shop-between-levels, map-window, character-select, game-screen, main-menu, settings-window, tutorial-window, leaderboard, +indirect-control-tactics, +terrain-preference-pathing, +auto-march-units, +terraform, +one-action-per-kind, +mana-pool-spells, +deck-builder, +deployment-phase, +energy-extra-action, +deterministic-combat, +bonus-objectives, +turn-limit-objectives, +unit-recycle, +meta-progression]
proposes: ["+effect:auto_path(a, prefs)", "+card:indirect-control-tactics", "+card:terrain-preference-pathing", "+card:one-action-per-kind", "+feature:mode-ironman"]
author: opus
date: 2026-11-09
---

# Zero Orders Tactics — тактика без наказів: юніти йдуть самі, а ти змінюєш під ними рельєф

## Суть
Гравець — бог, а не генерал: юніти обох сторін **самі** йдуть через гекс-поле за фіксованим правилом пошуку шляху, а гравець за хід може замінити плитку терену, вивести юніта з резерву, замінити активного юніта або кинути закляття з руки. Кожен тип юніта має улюблений, неулюблений і непрохідний терен — тож поставлений ліс чи гора перенаправляє цілий загін. Бій детермінований, ціль — виконати квест за кілька ходів. Над боями — роглайт-забіг: колода юнітів і заклять, герої, скіл-дерева.

## Поле і час
- Гексагональне поле (тег Steam «Hex Grid», девлог 0.4 «hex overlay»), три розміри мап; п'ять типів терену (огляд Steam-групи).
- Свої юніти рухаються зліва направо, ворожі — справа наліво, «приблизно по прямій», відхиляючись за вподобаннями терену (Geekly Grind).
- Хід: фаза гравця (дії) → автоматичний рух і атаки всіх юнітів за ініціативою → поява ворожих підкріплень. Перед першим ходом — фаза розстановки (девлог 0.330).
- Квест триває 3–9 ходів (огляд); у беті бої скоротили до 8 ходів (девлог 0.405).
- Інформація часткова: превʼю «show all plans» показує, куди підуть юніти, але ініціатива може змінити послідовність; нові вороги зʼявляються позаду загону.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Юніт гравця | ally | раса героя; клас; любить / не любить / не проходить терен | щохід сам іде до протилежного краю на свою дальність, атакує поруч |
| Посилений юніт | ally | — | сильніша версія базового (нагорода квесту, торговець) |
| Юніт-підсилювач | ally | аура | підсилює сусідніх юнітів (девлог 0.4) |
| Ворожий юніт | enemy | ті самі вподобання | іде справа наліво, ціль атаки — детермінована (девлог 0.440) |
| Бос | boss | — | Eye Tyrant, родина орків і гоблінів, Drago Heroes (DLC Under) |
| Плитка терену ×5 | terrain | тип | гравець ставить замість іншої; міняє шлях і (?) клас юніта на ній |
| Скриня | pickup | — | юніт, що пройшов через неї, дає нагороду після бою |
| Ціль квесту | zone | — | виконати хоча б одну — перемога |
| Точка підкріплення | spawner | — | ШІ виводить ворогів позаду загону і біля цілей |
| Резерв / колода юнітів | supply | — | вивести на поле або замінити активного; загиблі й ті, що вийшли за край, повертаються в обіг |
| Рука заклять | supply | ціна в мані | nudge, розворот напрямку руху тощо |
| Мана | resource | — | накопичується з часом; кілька заклять за хід — лише з запасом |
| Енергія-гекс | resource | 6 трикутників (?) | заповнений гекс = додаткова дія (девлог 0.333) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(swap_terrain, cell)` → ЯКЩО `custom: «цього ходу терен ще не мінявся»` → ТО `set_cell(cell, terrain)` (можна і під юнітом чи скринею, девлог 0.484).
- КОЛИ `input(deploy, unit, cell)` → ЯКЩО `custom: «цього ходу ще не виводив»` → ТО `place(player, unit)`.
- КОЛИ `input(swap_unit, a, b)` → ЯКЩО `custom: «цього ходу ще не міняв»` → ТО `swap(a, b)` (активний ↔ резервний).
- КОЛИ `input(cast, spell, target)` → ЯКЩО `counter(mana, >=, cost)` → ТО `counter(mana, -cost)` і ефект: nudge — `move(unit, dir)`; розворот — `face(unit, reverse)`.
- КОЛИ `turn_start(player)` → ТО `counter(mana, +n)` (?).
- КОЛИ `counter(energy, ==, full_hex)` → ТО `extra_move`.
- КОЛИ `turn_end(player)` → ТО кожен юніт `custom: «auto-path: крок до протилежного краю за вподобаннями терену»`, у порядку ініціативи.
- КОЛИ `custom: «auto-path обирає клітину»` → ЯКЩО `cell(next, liked)` → ТО `move(unit, next)`; ЯКЩО `cell(next, impassable)` → ТО `custom: «обхід»`; неулюблений терен — лише коли інакше не можна (?).
- КОЛИ `adjacent(unit, enemy)` → ТО `damage(enemy, atk)`; ціль — `custom: «за фіксованим правилом, не випадково»`.
- КОЛИ `custom: «терен під юнітом змінено чарами»` → ТО `transform(unit, class)` (?) — Steam: «powers reshape terrain and can also change unit classes».
- КОЛИ `contact(unit, chest)` → ТО `pickup` → нагорода після бою.
- КОЛИ `edge(unit)` або `died(unit)` → ТО `disappear_a`, `custom: «повертається в резерв»`.
- КОЛИ `turn_end(enemy)` → ТО `spawn_at(enemy, behind_player|near_objective)` (smart enemy spawn).
- КОЛИ `custom: «ціль квесту виконана»` → ТО `win` (бій), нагорода (досвід героя, золото, колода).
- КОЛИ `input(undo)` → ЯКЩО `not mode(ironman)` → ТО `undo(1)` (без ліміту).
- Перемога: виконати ≥1 ціль квесту до кінця ліміту ходів; забіг — 3 акти з босами · Поразка: жодної цілі до кінця ходів (?) · Рахунок: Steam-лідерборди (?).

## Керування і ввід
- Лише миша (Steam: «Mouse Only Option»): клік по плитці терену в руці → клік по гексу; клік по юніту резерву → клік по клітині; клік по закляттю → ціль.
- Дія кожного виду — раз за хід; кнопка «show all plans» — превʼю маршрутів і атак усіх юнітів.
- Undo без ліміту поза Ironman; «Save Anytime».

## Вікна, меню, HUD
- `main-menu` → вибір героя (`character-select`: дев'ять героїв, кожен — раса й набір юнітів) → глобальна карта (`map-window`: квести, торговці, три акти; девлог 0.550).
- `shop-window` — торговці між квестами: колода, золото, досвід, плитки.
- `upgrade-window` — скіл-дерева героя (девлог 0.550).
- `custom-window` «Deploy» — розстановка перед першим ходом.
- `game-screen`: гекс-поле; рука заклять і плиток (`inventory-bar`); `energy-bar` (гекс з трикутників); мана; `turn-counter`; `objective-text` (цілі квесту); `path-preview` / `telegraph-marker` («show all plans»); `undo-button`; `end-turn-button`; `tooltip` (огляд: підказки потрібні).
- `tutorial-window` (за оглядом — не переграється), `settings-window` (звук, вікно/повний екран), `end-screen` з нагородами, `leaderboard`, `achievements-window`.

## Фічі поза полем
- Роглайт-забіг: колода юнітів і заклять росте за забіг (`meta-progression`: рівні героя дають стартові бонуси й навички назавжди; квести відкривають героїв, юнітів, заклять).
- Ironman — без undo; `difficulty-presets` (Steam: Adjustable Difficulty); `colorblind-palette` (Color Alternatives); `cloud-save`; `achievements`.
- DLC Under (2025): 7-ма фракція (31 юніт), 3 герої, 3 боси.

## Варіації й родичі
- Натхнення — [Into the Breach](into-the-breach.md) (детермінізм, превʼю), але інверсія: замість керування загоном — керування полем.
- Родичі «юніти йдуть самі»: Lemmings (ставиш роль, не ведеш), auto-battler-и й Wildfrost-подібні смуги (tower-lanes); терен-як-зброя — [Polytopia](polytopia.md) (лише економічно).
- **Осі варіацій**: контроль — прямий (FE, XCOM) / непрямий через поле (ZOT) / програма наперед (RoboRally) · шлях юніта — найкоротший / за вподобаннями терену / за наказом-закляттям.

## Цікавинки для курсу
- Пошук шляху з вагами «улюблений / неулюблений / непрохідний терен» для кожного типу юніта — 🥈 (Dijkstra з вагами за типом).
- Тактика без наказів: гравець лише міняє клітини, а превʼю показує новий маршрут усіх — 🥇 (симуляція на копії стану після кожної зміни).
- Одна дія кожного виду за хід (терен, вивід, заміна, закляття) — 🌱.
- Енергія-гекс з трикутників: заповнений — додаткова дія — 📎.
- Обіг юнітів: загиблий чи вийшов за край — назад у резерв — 📎.

## Мапа на каталог
- Є: `hp-damage` · `impassable-cells` · `floor-types` (5 терен) · `cursor-place` (плитка, юніт) · `telegraphed-intents` + `path-preview` (show all plans) · `undo-unlimited` · `spawn-points` · `unit-xp-skills` (герой) · `shop-between-levels` (торговці) · `map-window` · `character-select` · вікна.
- **Нема** → пропозиції карток:
  - `+indirect-control-tactics` «Тактика без наказів» · entities/move · 🥇 — юніти діють самі, гравець міняє поле.
  - `+terrain-preference-pathing` «Шлях за вподобаннями терену» · entities/move · 🥈 · слот {liked, disliked, impassable}.
  - `+one-action-per-kind` «Одна дія кожного виду за хід» · game-logic/opponent · 🌱.
  - `+energy-extra-action` «Шкала енергії → додаткова дія» · game-logic/economy · 📎.
  - `+unit-recycle` «Загиблий юніт повертається в резерв» · entities/spawn · 📎.

## Пропозиції до словників
- `+effect:auto_path(a, prefs)` — сутність сама робить крок за фіксованим правилом пошуку шляху з вагами клітин.
- `+card:indirect-control-tactics` — покрокова тактика, де гравець змінює поле, а не наказує юнітам.
- `+card:terrain-preference-pathing` — вподобання терену як вагова функція маршруту.
- `+card:one-action-per-kind` — ліміт «по одній дії кожного типу за хід».
- `+feature:mode-ironman` — режим без undo і переграшів (Ironman ZOT, Irondog Dog in the Machine).

## Джерела
- ⭐ [Steam: Zero Orders Tactics](https://store.steampowered.com/app/1877650/Zero_Orders_Tactics/) — опис, «100 % predictable», теги Hex Grid, дата.
- [The Irregular Gamer (Steam-група)](https://steamcommunity.com/groups/TheIrregularGamer/discussions/0/592884025032506586) — дії за хід, мана, терен, квести, Ironman, обіг юнітів, критика.
- [Geekly Grind: демо](http://www.thegeeklygrind.com/all-posts/zero-order-tactics-intial-demo-imprssions) — вподобання терену, напрями руху, превʼю ворога, закляття-розворот.
- [itch.io + девлоги](https://pauloondra.itch.io/zero-orders-tactics) — енергія-гекс, фаза розстановки, скрині, детерміновані цілі атак.
- [Steam: DLC Under](https://store.steampowered.com/app/4116860/Zero_Orders_Tactics_Under/) — склад доповнення.

## Непевне
- (?) Як саме терен змінює клас юніта — лише фраза з опису Steam.
- (?) Точні типи 5 терен і їхні ефекти; дальність руху й атаки юнітів; формула ініціативи.
- (?) Правило поразки в бою (ліміт ходів без виконаної цілі?) і чи гине герой.
- (?) Скільки мани приходить за хід; енергія-гекс із 6 трикутників — висновок з «filling by triangles».
- (?) Мобільна версія — лише згадка «зроблено під планшети» в огляді.
