---
title: Alien Cartographer
slug: alien-cartographer
aka: []
family: hidden-deduction
also: [pencil-logic]
klass: puzzle
axes:
  field: hex
  time: static
  opponent: none
  info: hidden
  random: setup
  goal: state
year: 2026
platforms: [PC (Windows)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/3134580/Alien_Cartographer/", best: true, note: "опис, трейлер: «Minesweeper-like» гекс-дедукція будівель за правилами архітектури; 90 рівнів, челенджі, редактор + Workshop; 22.01.2026"}
  - {kind: other, url: "https://steamcommunity.com/sharedfiles/filedetails/?id=3660033289", note: "посібник гравця (JA): переклад туторіалів рівнів 1–76 — усі правила будівель, кольорів і підказок"}
  - {kind: other, url: "https://steamcommunity.com/app/3134580/reviews/?browsefilter=toprated", note: "рецензії: 4-та помилка — рестарт, малювання на полі, кодекс, режим для дальтоніків, миша/тач"}
  - {kind: other, url: "https://store.steampowered.com/api/appdetails?appids=3134580", note: "Steam API: категорії (Workshop, Leaderboards, Cloud, Mouse/Touch Only), 18 досягнень"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Alien+Cartographer+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [cell-click, hover-highlight, selection-highlight, satisfy-constraints, completion-detection, neighbor-count-clue, connectivity-check, restart-level, sequential-levels, level-select, unique-puzzle-generation, in-game-editor, level-exchange, codex-window, tutorial-window, help-window, achievements-window, leaderboard, settings-window, game-screen, volume-control, background-music, +hex-grid-render, +mistake-counter, +mistake-limit, +per-color-neighbourhood, +asymmetric-adjacency, +settlement-groups, +two-attribute-cell, +reveal-number-on-correct, +free-draw-notes, +radial-quick-select, +distinct-distance-clue, +between-pair-clue, +line-same-color-clue, +exclusion-radius-clue, +all-kinds-present, +colorblind-palette, +perfect-run]
proposes: ["+axis:neighbourhood", "+cond:matches_solution", "+cond:between", "+cond:neighbour_of_color", "+ui:quick-wheel", "+ui:draw-layer", "+ui:confirm-panel", "+feature:perfect-run", "+card:per-color-neighbourhood", "+card:settlement-groups", "+card:two-attribute-cell", "+card:distinct-distance-clue", "+card:between-pair-clue"]
author: opus
date: 2026-11-09
---

# Alien Cartographer — гекс-сапер про інопланетне місто: вгадай колір (расу) і тип будівлі кожної клітини за правилами архітектури

## Суть
На гекс-полі частина клітин — будівельні «?»: у кожній стоїть будівля одного з трьох типів (енергоядро, дім, вежа) й одного з трьох кольорів (синя, червона, зелена раса). Гравець підтверджує для клітини пару «будівля + колір»; правильна відповідь відкриває число-підказку, хибна — рахується як помилка, четверта перезапускає рівень. Головна незвичність — **кожна раса має своє сусідство** (синя — 6 прямих сусідів, червона — 6 «діагональних» через кути, зелена — 6 клітин через одну по прямій), тому поселення, числа й правила будівель читаються по-різному залежно від кольору. Правила ніколи не змінюються: 90 ручних рівнів лише поступово відкривають нові.

## Поле і час
- Гексагональне поле довільної форми; найбільші рівні — приблизно гекс зі стороною 4 (за JA-рецензентом, (?)).
- Три види клітин: **будівельна** (будівля там є завжди), **підказкова** (золота копальня, ринок, парк, фабрика, телепорт) і **порожня** (будувати не можна).
- Прихований шар на будівельній клітині — дві ознаки: тип будівлі та колір; відкритий шар — число після правильного визначення; окремий шар малювання гравця.
- Сусідство за кольором (поле `+axis:neighbourhood`):
  - синій — 6 клітин зі спільним ребром;
  - червоний — 6 «діагональних» клітин через кути гекса (відстань 2), прямі сусіди червоному **не** сусіди;
  - зелений — 6 клітин на відстані 2 по прямих осях.
- Сусідство несиметричне: синій і червоний доми поруч — для синього червоний сусід, для червоного синій ні.
- Статичний пазл (`time: static`): без таймера, «Playable without Timed Input».

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Будівельна клітина «?» | static | прихований тип + колір | після правильного Confirm відкриває будівлю й число |
| Енергоядро (Energy Core) | mark | колір; число = інші будівлі поселення | рівно одне на поселення; живить його |
| Дім (House) | mark | колір; число = сусідні доми | мусить мати сусідній дім (будь-якого кольору) |
| Вежа (Tower) | mark | колір; число = сусідні будівлі іншого кольору | лише поруч із ядром свого поселення **і** з будівлею іншого кольору; зʼявляється з 2+ рас |
| Поселення | zone | ≥ 2 будівлі | звʼязна група будівель за сусідством кольору; 1 ядро + ≥ 1 дім або вежа |
| Золота копальня (Gold Mine) | mark | — | серед 6 прямих сусідів ≥ 1 ядро (будь-якої раси) |
| Ринок (Market) | mark | — | стоїть між двома вежами різних кольорів; між ними лише порожні клітини |
| Парк (Park) | mark | — | у радіусі 2 нема жодної вежі |
| Фабрика (Factory) | mark | — | усі ядра поля — на попарно різних відстанях від неї |
| Телепорт (Teleporter) | mark | пари | будівлі на прямій між двома телепортами — одного кольору |
| Порожня клітина | static | — | будівлі нема; ринку й телепорту не заважає |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `level_start` → ТО `custom: «показано поле, доступні раси й типи; на першому проході рівня — сторінки туторіалу з новим правилом»`.
- КОЛИ `input(click, building_tile)` → ТО `custom: «підсвітити поселення клітини і обвести її сусідів за її кольором»`.
- КОЛИ `input(click, hint_tile)` → ТО `custom: «показати правило підказки»` (вхід у кодекс).
- КОЛИ `input(confirm, tile, building, color)` → ЯКЩО `custom: «пара збігається з розвʼязком»` → ТО `reveal(tile)`, `set_value(tile, n)`; інакше `counter(mistakes, +1)`.
- КОЛИ `counter(mistakes, >=, 4)` → ТО `restart` (до 3 помилок рівень триває).
- КОЛИ `all_constraints_met` (усі «?» визначено) → ТО `win`, `next_level`.
- Поселення: `custom: «будівля належить рівно одному поселенню — звʼязній групі будівель свого кольору за сусідством цього кольору»` (`connected`); прямі сусіди-червоні — різні поселення.
- Розмір поселення: `count(settlement_buildings, >=, 2)`.
- Ядро: `count(core_in_settlement, ==, 1)`; і `count(house_or_tower_in_settlement, >=, 1)` — поселення без домів або без веж допустиме.
- Дім: `adjacent_count(house, house, >=, 1)` — сусідство за кольором дому, колір сусіднього дому будь-який.
- Вежа: `adjacent_count(tower, own_core, >=, 1)` **and** `custom: «серед сусідів є будівля іншого кольору»` (`+cond:neighbour_of_color`); кілька веж в одному поселенні можна.
- Числа: ядро — `set_value(core, count(settlement) − 1)`; дім — `set_value(house, adjacent_count(house))`; вежа — `set_value(tower, кількість сусідніх будівель іншого кольору)`; рахуються за сусідством кольору будівлі.
- Золота копальня: `adjacent_count(mine, core, >=, 1)` завжди по 6 прямих сусідах, незалежно від раси; не кожне ядро стоїть біля копальні, кілька копалень можуть вказувати на одне ядро.
- Ринок (з рівня 21): `custom: «на одній лінії між двома вежами різних кольорів, між ними лише порожні клітини»` (`+cond:between`); одна вежа може обслуговувати кілька ринків, вежі без ринку дозволені.
- Парк (з рівня 51): `not in_range(park, tower, 2)`.
- Фабрика (з рівня 61): `unique(distance(factory, core))` для всіх ядер поля; кожна фабрика перевіряється окремо.
- Телепорт (з рівня 76): `same(buildings_on_line(tp_a, tp_b), color)` **and** `custom: «між ними нема іншого телепорта»`; один телепорт може мати кілька ліній різного кольору.
- Усі раси (з рівня 46): ЯКЩО `custom: «на рівні доступно кілька рас»` → `count(color_k, >=, 1)` для кожної.
- Перемога: усі будівельні клітини визначено. · Поразка: 4 помилки → рестарт рівня. · Рахунок: помилки; досягнення вимагають проходження без помилок.

## Керування і ввід
- Клік по будівельній клітині — вибір і підсвітка; підтвердження будівлі й кольору — у меню праворуч (Confirm).
- Quick-Guessing Wheel: утримання лівої кнопки на клітині — колесо типів будівлі, правої — колесо кольорів; вимикається в налаштуваннях.
- Шар малювання (меню праворуч унизу): позначки й нотатки поверх поля; вмикається іконкою ока, Space або утриманням Shift.
- Клік по підказці — правило; кодекс з гіпертекстом між правилами.
- Повна гра мишею або тачем («Mouse Only», «Touch Only»).

## Вікна, меню, HUD
- `game-screen`: гекс-поле; `mistake-counter` угорі ліворуч; `+ui:confirm-panel` праворуч (вибір будівлі й кольору, Confirm); `+ui:draw-layer` праворуч унизу; `selection-highlight` поселення і контур сусідів; `+ui:quick-wheel`.
- `tutorial-window`: багатосторінковий текст нового правила на старті рівня (рівень 1 — 6 сторінок, за JA-рецензентом).
- `codex-window`: усі правила з гіперпосиланнями; доступний будь-коли.
- `level-select`: кампанія з 90 рівнів (?) — вигляд меню не бачив.
- `mode-select` (?): кампанія / 5 процедурних челенджів / рівні Workshop / редактор.
- `editor-window`: внутрішній редактор рівнів із публікацією у Steam Workshop.
- `leaderboard`: Steam Leaderboards (імовірно для челенджів (?)).
- `settings-window`: гучність окремими повзунками, вимикач Quick-Guessing Wheel, режим для дальтоніків.
- `achievements-window`: 18 досягнень Steam.
- `end-screen` (?) рівня — не бачив.

## Фічі поза полем
- `levels-sequential`: 90 ручних рівнів, правила вводяться поступово (кольори 6/11/31, вежа 12, ринок 21, «усі раси» 46, парк 51, фабрика 61, телепорт 76).
- Челенджі: 5 видів процедурно згенерованих рівнів; `leaderboard-online` (?).
- `level-editor` + `level-sharing` через Steam Workshop.
- `mistake-limit`: 3 помилки прощаються, 4-та — рестарт; `+feature:perfect-run` — досягнення лише за рівні без помилок.
- `codex` з гіпертекстом; `colorblind-palette`; `touch-controls`; `volume-sliders`; `cloud-save`; мови EN і DE.
- Демо до релізу; у релізі додано розмітку (малювання).

## Варіації й родичі
- Родичі: [hexcells.md](hexcells.md) (гекс, числа сусідів, помилки лише рахуються), [tametsi.md](tametsi.md), [14-minesweeper-variants.md](14-minesweeper-variants.md) (набір правил-модифікаторів), [patterna.md](patterna.md); паперові «Towers»/«Star Battle» — згадані рецензентом як схожі на правило ринку.
- **Осі варіацій**:
  - сусідство: одне на всіх (сапер) / своє для кожного кольору (тут) / несиметричне;
  - що в клітині: так/ні (міна) / число / дві ознаки — тип і колір (тут);
  - підказки: число сусідів / глобальні обмеження (фабрика: різні відстані; телепорт: лінія одного кольору);
  - помилка: смерть / лічильник / ліміт із рестартом (тут — 4).

## Цікавинки для курсу
- Три сусідства на гекс-сітці (кільце 1, діагоналі, «через одну») і несиметрична перевірка «сусід з погляду кольору» — 🥉.
- Поселення як звʼязні компоненти за кольоровим сусідством + перевірка «рівно одне ядро, ≥ 2 будівлі» — 🥉.
- Валідатор розвʼязку: усі правила (дім, вежа, копальня, ринок, парк, фабрика, телепорт) як предикати над розміткою — 🥈.
- Відкриття числа після правильної відповіді й лічильник помилок з рестартом на 4-й — 🌱.
- Quick-wheel: утримання кнопки → радіальне меню вибору — 📎.
- Розвʼязувач/генератор челенджів з єдиним розвʼязком (CSP із двома змінними на клітину) — 👑.

## Мапа на каталог
- Є: `cell-click` · `hover-highlight` / `selection-highlight` ↔ підсвітка поселення · `satisfy-constraints` + `completion-detection` · `neighbor-count-clue` ↔ числа дому/вежі · `connectivity-check` ↔ поселення · `restart-level` ↔ рестарт на 4-й помилці · `sequential-levels` + `level-select` ↔ кампанія · `unique-puzzle-generation` ↔ челенджі (?) · `in-game-editor` + `level-exchange` ↔ редактор і Workshop · `codex-window` · `tutorial-window` · `help-window` · `achievements-window` · `leaderboard` · `settings-window` · `volume-control` · `background-music`.
- **Нема** → пропозиції карток:
  - `+per-color-neighbourhood` «Сусідство залежить від типу клітини» · game-logic/constraints · 🥉 · слоти {ring1, diag, jump2}.
  - `+asymmetric-adjacency` «Несиметричне сусідство» · game-logic/constraints · 📎.
  - `+settlement-groups` «Групи-поселення з квотою типів (рівно 1 ядро)» · game-logic/constraints · 🥉.
  - `+two-attribute-cell` «Клітина з двома прихованими ознаками (тип + колір)» · entities/state · 📎.
  - `+reveal-number-on-correct` «Правильна відповідь відкриває число» · game-logic/constraints · 🌱.
  - `+distinct-distance-clue` «Усі цілі на різних відстанях від підказки» · game-logic/constraints · 📎.
  - `+between-pair-clue` «Підказка між парою різних цілей на лінії» · game-logic/constraints · 📎.
  - `+line-same-color-clue` «Лінія між парою — один колір» · game-logic/constraints · 📎.
  - `+exclusion-radius-clue` «У радіусі N нема цілей виду» · game-logic/constraints · 🌱.
  - `+all-kinds-present` «Кожен вид мусить бути на полі» · game-logic/constraints · 🌱.
  - Також: `+mistake-counter`, `+mistake-limit`, `+free-draw-notes`, `+radial-quick-select`, `+hex-grid-render`, `+colorblind-palette`, `+perfect-run`.

## Пропозиції до словників
- `+axis:neighbourhood` — сусідство як поле осі: `ring1` / `diag` / `jump2` / `per-kind`.
- `+cond:matches_solution` — відповідь гравця збігається з прихованим розвʼязком (Confirm, Hexcells, Voltorb).
- `+cond:between` — клітина лежить на відрізку між двома сутностями однієї лінії (ринок, телепорт).
- `+cond:neighbour_of_color` — серед сусідів (за сусідством сутності) є сутність іншого кольору.
- `+ui:quick-wheel` — радіальне меню під утриманою кнопкою.
- `+ui:draw-layer` — вільне малювання поверх поля, не впливає на перевірку.
- `+ui:confirm-panel` — бічна панель вибору ознак клітини з кнопкою Confirm.
- `+feature:perfect-run` — окремий статус/досягнення за рівень без помилок.
- `+card:per-color-neighbourhood`, `+card:settlement-groups`, `+card:two-attribute-cell`, `+card:distinct-distance-clue`, `+card:between-pair-clue`.

## Джерела
- ⭐ [Steam: Alien Cartographer](https://store.steampowered.com/app/3134580/Alien_Cartographer/) — опис («identify various buildings on a hexagonal grid using environmental hints and the strict rules of their architecture»), 90 рівнів, челенджі, редактор + Workshop, FachchefGames, 22.01.2026.
- [Steam API appdetails](https://store.steampowered.com/api/appdetails?appids=3134580) — категорії: Workshop, Leaderboards, Cloud, Custom Volume, Mouse/Touch Only, 18 досягнень.
- [Посібник (JA) — переклад туторіалів](https://steamcommunity.com/sharedfiles/filedetails/?id=3660033289) — типи клітин, поселення, ядро/дім/вежа, числа, копальня, ринок, парк, фабрика, телепорт, сусідства трьох рас, Confirm, 3 помилки + рестарт на 4-й, шар малювання, Quick-Guessing Wheel.
- [Steam: рецензії](https://steamcommunity.com/app/3134580/reviews/?browsefilter=toprated) — «four strikes, and you're out», кодекс з гіпертекстом, малювання, режим для дальтоніків, 5 челенджів, досягнення за ідеальні рівні, гекс до ~4×4×4.
- YouTube: пошук «Alien Cartographer gameplay».

## Непевне
- (?) Чи поселення завжди одноколірне: туторіал каже «будівлі поселення сусідять за сусідством кольору», рецензент зве визначення «тієї ж області» підступним.
- (?) Ринок і телепорт — «на одній прямій» виведено з «між двома вежами» / «пряма між телепортами»; чи ринок може стояти не на прямій — не перевірено.
- (?) Чи челенджі гарантують єдиний розвʼязок без вгадувань і на що саме лідерборди — не бачив.
- (?) Вигляд меню, вибору рівнів, екрана кінця рівня — не бачив; `mode-select` припущено.
- (?) Розмір найбільшого поля «4×4×4» — оцінка рецензента.
