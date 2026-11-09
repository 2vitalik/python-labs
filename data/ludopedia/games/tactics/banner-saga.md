---
title: The Banner Saga
slug: banner-saga
aka: [Banner Saga, TBS, "The Banner Saga: Factions"]
family: tactics
also: []
klass: figure
axes:
  field: square
  time: turn
  opponent: ai
  info: full
  random: runtime
  goal: state
year: 2014
platforms: [PC, Mac, Linux, iOS, Android, PS4, Xbox One, Switch]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/The_Banner_Saga", best: true, note: "покроковий бій, рішення в подорожі, без луту й перезавантаження, Factions як мультиплеєр"}
  - {kind: other, url: "https://www.matchstickeyes.com/2014/02/02/the-banner-saga-turn-based-tactics-with-a-twist/", note: "черговість сторін H1-D1-H2-D2, Strength = HP і сила, формула шкоди, варли 2×2, KO і травми"}
  - {kind: other, url: "https://www.gamedeveloper.com/design/the-banner-saga-on-willpower", note: "дизайнер про Willpower: не відновлюється, +1 за вбивство до 5, «health is damage»"}
  - {kind: other, url: "https://www.gamepressure.com/thebannersaga/moving-around-the-battlefield-and-order-of-turns/z15d08", note: "сині/жовті клітини руху, Turn Order, Pillage"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=The+Banner+Saga"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=The+Banner+Saga+combat+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [hp-damage, melee-vs-ranged, multi-cell-size, legal-move-highlight, reachable-highlight, hover-highlight, unit-xp-skills, inventory-items, ai-opponent, destroy-all-enemies, round-currency, shop-between-levels, world-map, sequential-levels, save-progress, online-multiplayer, difficulty-levels, placement-screen, character-select, +strength-is-hp, +armor-break, +willpower-boost, +alternating-side-turns, +pillage-mode, +kill-reward-pool, +injury-days, +caravan-supplies, +story-choices]
proposes: ["+effect:break_armor", "+effect:spend", "+cond:sides_count", "+ui:turn-order-bar", "+ui:willpower-pips", "+ui:horn-meter", "+window:caravan-travel", "+window:camp-screen", "+window:decision-dialog", "+window:hero-roster", "+feature:no-reload-consequences", "+axis:turn-structure=alternating-unit"]
author: opus
date: 2026-11-09
---

# The Banner Saga — тактика, де HP = сила удару: ламай броню або різь силу, ходи сторін чергуються по одному юніту

## Суть
Загін вікінгів-людей і велетнів-варлів б'ється з камʼяними Dredge на квадратній сітці. Головний трюк — **Strength одночасно і HP, і сила атаки**: поранений воїн бʼє слабше, тож кожен удар — вибір: зняти броню (Armor) цілі чи її силу. Ходи **чергуються по одному юніту** незалежно від кількості, доки одна зі сторін не лишиться з одним бійцем (Pillage). Між боями — подорож каравану з припасами, моралем і рішеннями без права перезавантажитись.

## Поле і час
- Поле — квадратна сітка, вигляд у ізометричному ракурсі; перешкоди займають клітини.
- Люди займають 1 клітину, **варли — 2×2** (4 клітини).
- Час — покроковий: черга юнітів кожної сторони задана наперед, сторони чергуються 1 на 1 (H1, D1, H2, D2, H1, D3…). Сторона з меншою кількістю бійців ходить кожним частіше.
- Випадковість: шанс пробити броню, коли сила нижча (?), криті від предметів (Tryggvi — «вищий шанс подвійної шкоди»).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой-людина (лучник, щитоносець, спис) | piece | Armor, Strength, Willpower, Exertion, Armor Break, 1 клітина | рух, атака по броні або силі, активна навичка за Willpower |
| Варл (велетень) | piece | ті самі, 2×2 | високі Armor/Strength, займає 4 клітини, бʼє сусідів |
| Лучник | piece | дальність | бонус до атаки, якщо не рухався в цей хід |
| Списоносець | piece | — | атакує також по діагоналі, не впритул (?) |
| Dredge (воїн, лучник, стоунгард) | enemy | ті самі стати | AI: обирає ціль, ламає броню / ріже силу |
| Важкий Dredge / велетень | boss | великий Armor | у деяких боях — ціль бою |
| Перешкода (камінь, віз) | static | — | займає клітини, блокує рух |
| Ріг (Horn) | resource | до 5 зірок | наповнюється вбивствами, зірки віддаються будь-якому герою як Willpower |
| Предмет героя | pickup | 1 слот (?) | пасивний бонус до статів |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_end(side)` → ТО `custom: «хід переходить до наступного юніта іншої сторони за її чергою»`.
- КОЛИ `input(move, unit, cell)` → ЯКЩО `custom: «синя клітина (базовий рух)»` → ТО `move(unit, cell)`; ЯКЩО `custom: «жовта клітина»` and `counter(willpower, >, 0)` → ТО `move(unit, cell)`, `counter(willpower, −k)` (+1 клітина за 1 Willpower, ≤ Exertion).
- Атака по силі: КОЛИ `input(attack_strength, a, t)` → ЯКЩО `adjacent(a, t)` або `in_range(a, t, range)` → ТО `damage(t, a.strength + wp − t.armor)` (формула за оглядом: «(strength + 1) − armor», ?).
- КОЛИ `input(attack_strength, a, t)` → ЯКЩО `custom: «сила атакувальника ≤ броні цілі»` → ТО `prob(p)` → `damage(t, 1)` (?), інакше `custom: «удар відскакує»`.
- Атака по броні: КОЛИ `input(attack_armor, a, t)` → ТО `custom: «Armor цілі −(Armor Break + Willpower)»`; від сили атакувальника не залежить.
- КОЛИ `input(boost, a)` → ЯКЩО `counter(willpower, >=, n)` and `custom: «n ≤ Exertion»` → ТО `counter(willpower, −n)`, `custom: «+n до шкоди / руху»`.
- КОЛИ `input(ability, a)` → ЯКЩО `counter(willpower, >=, cost)` → ТО `counter(willpower, −cost)`, `custom: «ефект навички класу»` (наприклад, примусити сусідів бити себе — провокація варла).
- КОЛИ `input(rest, a)` → ТО `end_turn`, `custom: «юніт не діє»` (+1 Willpower, ?).
- Willpower: КОЛИ `level_start` → ТО `set_value(unit.willpower, max)` — під час бою сам не відновлюється; морал каравану змінює стартовий Willpower.
- Ріг: КОЛИ `died(enemy)` → ТО `counter(horn, +1)` (≤ 5); КОЛИ `input(horn, hero)` → ТО `custom: «зірка з рогу стає Willpower героя»`.
- КОЛИ `hp_zero(unit)` → ТО `disappear(unit)` з поля; герой — KO, `custom: «травма: штраф до статів на кілька днів подорожі»`, без перманентної смерті.
- Pillage: КОЛИ `custom: «в однієї сторони лишився 1 юніт, в іншої ≥ 2»` → ТО `custom: «більша сторона ходить усіма юнітами підряд, потім одиночка»`.
- Лучник: КОЛИ `input(attack, archer, t)` → ЯКЩО `custom: «не рухався цей хід»` → ТО `custom: «бонус до атаки»`.
- Перемога: `all_gone(enemy)` → ТО `win`, `currency(renown, +n)` за вбивства. Поразка: `all_gone(hero)` → ТО `custom: «наслідки в сюжеті (гра продовжується), або lose у ключових боях»` (?).
- Підвищення: КОЛИ `input(promote, hero)` → ЯКЩО `counter(kills, >=, need)` and `counter(renown, >=, cost)` → ТО `custom: «+рівень, очки статів»`.
- Караван: КОЛИ `tick` (день подорожі) → ТО `counter(supplies, −clansmen)`; ЯКЩО `counter(supplies, ==, 0)` → ТО `custom: «гинуть люди, падає морал»`.

## Керування і ввід
- Миша/тач/геймпад по клітинах: вибір юніта в його хід → сині й жовті клітини руху → клітина → ціль атаки.
- На цілі — вибір: бити броню (синя смуга) чи силу (червона); слайдер/кнопки «+Willpower» до межі Exertion; прогноз результату.
- Кнопки: навичка, Rest / End Turn; перегляд статів будь-якого юніта.
- Перед боєм — розстановка в зоні старту й порядок ходів своїх героїв (Turn Order) на екрані героїв.

## Вікна, меню, HUD
- `main-menu`: New Game, Continue, Options, Exit; вибір складності.
- `game-screen`: сітка, `reachable-highlight` синя (база) і жовта (за Willpower) зони; над юнітом дві смуги — броня і сила; `willpower-pips`; `turn-order-bar` з чергою обох сторін; `horn-meter`; кнопки навички й завершення ходу; попередній прогноз шкоди.
- `placement-screen` — розстановка перед боєм; `hero-roster` — герої, стати, Turn Order, підвищення за Renown, предмети.
- `caravan-travel` — бічний вид каравану на мапі: дні, припаси, морал, кількість кланових, бійців, варлів, Renown.
- `decision-dialog` — події подорожі з варіантами відповіді; `map-window` — карта світу з маршрутом.
- `camp-screen` — табір: відпочинок (лікування травм, витрата припасів), торговець (`shop-window`) за Renown, тренувальний бій (?).
- `end-screen` — результат бою; `pause-menu`; `settings-window`.

## Фічі поза полем
- Renown — одна валюта на все: підвищення героїв, купівля припасів і предметів.
- Без луту, без «переграти поразку»: поразка й смерть персонажів у сюжеті — наслідки, які несеш далі (`no-reload-consequences`).
- `autosave` за подіями; перенос збереження між частинами трилогії (TBS 2, 3) (?).
- The Banner Saga: Factions — безкоштовний онлайн-PvP на тій самій бойовій системі (`online-multiplayer`).
- `difficulty-presets`; у TBS 3 — бої хвилями з вибором «продовжувати чи відійти» (?).

## Варіації й родичі
- Сиквели: The Banner Saga 2 (2016), 3 (2018) — нові класи, таланти; Factions (2013) — PvP.
- Родичі: Final Fantasy Tactics (натхнення — [final-fantasy-tactics](final-fantasy-tactics.md)), Shining Force; Battle Brothers (загін найманців на мапі — [battle-brothers](battle-brothers.md)), Darkest Dungeon (стрес і припаси, не клітинна).
- Осі варіацій:
  - **HP і сила**: окремо (FE, FFT) / одне число (TBS, частково Langrisser — [langrisser](langrisser.md): менше солдатів — слабша атака);
  - **черга ходів**: фази сторін ([fire-emblem](fire-emblem.md)) / за швидкістю ([triangle-strategy](triangle-strategy.md)) / по одному юніту сторін почергово (TBS, [xcom-chimera-squad](xcom-chimera-squad.md));
  - **ресурс підсилення**: TP, що росте (Triangle Strategy) / Willpower, що лише витрачається й повертається вбивствами (TBS).

## Цікавинки для курсу
- Strength = HP = шкода: дві смуги, два види атаки, вибір «броня чи сила» — 📎.
- Почергові ходи сторін по одному юніту з кільцевими чергами різної довжини + Pillage — 📎.
- Willpower з межею Exertion на одну дію (і на шкоду, і на рух) — 🌱.
- Ріг: спільний пул за вбивства, що роздається будь-кому — 🌱.
- Варл 2×2: рух, суміжність і досяжність для багатоклітинного юніта — 🥉.
- Караван: щоденне споживання припасів, морал → стартовий Willpower у бою — 📎.

## Мапа на каталог
- Є: `hp-damage` · `melee-vs-ranged` · `multi-cell-size` ↔ варл 2×2 · `legal-move-highlight` + `reachable-highlight` ↔ сині/жовті клітини · `hover-highlight` · `unit-xp-skills` ↔ підвищення за вбивства й Renown · `inventory-items` ↔ предмет героя · `ai-opponent` · `destroy-all-enemies` · `round-currency` + `shop-between-levels` ↔ Renown і торговець · `world-map` · `sequential-levels` ↔ глави · `save-progress` · `online-multiplayer` ↔ Factions · `difficulty-levels` · `placement-screen` · `character-select`.
- **Нема** → пропозиції карток:
  - `+strength-is-hp` «HP = сила атаки» · entities/combat · 📎 · слот {formula: str − armor}.
  - `+armor-break` «Атака по броні окремо від HP» · entities/combat · 📎.
  - `+willpower-boost` «Ресурс підсилення з межею на дію» · entities/combat · 🌱 · слот {cap: exertion}.
  - `+alternating-side-turns` «Сторони ходять по одному юніту почергово» · game-logic/opponent · 📎.
  - `+pillage-mode` «Останній юніт сторони — суперник ходить усіма» · game-logic/opponent · 🌱.
  - `+kill-reward-pool` «Спільний пул за вбивства (ріг)» · entities/combat · 🌱.
  - `+injury-days` «Травма на кілька днів кампанії замість смерті» · progression · 🌱.
  - `+caravan-supplies` «Караван: припаси, морал, люди» · progression · 🥉.
  - `+story-choices` «Рішення в подіях змінюють ресурси й сюжет» · interface/menus · 📎.

## Пропозиції до словників
- `+effect:break_armor(t, n)` — зменшити броню цілі на N, не чіпаючи HP.
- `+effect:spend(a, resource, n)` — витратити ресурс юніта (Willpower, TP) на підсилення.
- `+cond:sides_count(side, op, n)` — у сторони лишилось N юнітів (Pillage).
- `+ui:turn-order-bar` — черга ходів обох сторін; `+ui:willpower-pips` — зірки Willpower над юнітом; `+ui:horn-meter` — ріг з накопиченими зірками.
- `+window:caravan-travel` — подорож каравану з ресурсами; `+window:camp-screen` — табір; `+window:decision-dialog` — подія з варіантами; `+window:hero-roster` — герої, черга, підвищення.
- `+feature:no-reload-consequences` — поразка не скасовується, гра йде далі з наслідками.
- `+axis:turn-structure=alternating-unit` — сторони чергуються по одному юніту (TBS, Chimera Squad).

## Джерела
- ⭐ [Wikipedia: The Banner Saga](https://en.wikipedia.org/wiki/The_Banner_Saga) — покроковий бій, рішення в подорожі, без луту й перезавантаження, Factions, платформи й дати.
- [Matchstick Eyes: turn-based tactics with a twist](https://www.matchstickeyes.com/2014/02/02/the-banner-saga-turn-based-tactics-with-a-twist/) — приклад черги H1-D1-H2-D2, Strength = HP і сила, «(strength + 1) − armour», варли на 4 клітини, KO → травми на дні, підвищення за вбивства.
- [Game Developer: On Willpower](https://www.gamedeveloper.com/design/the-banner-saga-on-willpower) — Willpower не відновлюється, +1 за вбивство до 5, «health is damage».
- [Gamepressure: рух і черга ходів](https://www.gamepressure.com/thebannersaga/moving-around-the-battlefield-and-order-of-turns/z15d08) — сині/жовті клітини, Turn Order, Pillage, бонус лучника за нерух, діагональ списа.
- YouTube: пошук «The Banner Saga combat gameplay».

## Непевне
- (?) Точна формула шкоди по силі: «сила − броня» чи «сила + 1 − броня»; шанс «пробити» 1 шкоди, коли броня вища.
- (?) Rest дає +1 Willpower; бонус лучника за нерух — розмір.
- (?) Ріг (Horn): чи це те саме, що «+1 за вбивство до 5» з тексту дизайнера.
- (?) Pillage: хто саме ходить першим у режимі; спрацьовує для обох сторін (джерела розходяться).
- (?) Наслідки поразки в бою (сюжет іде далі чи game over у ключових битвах); перенос сейва між частинами.
- (?) Кількість слотів предметів на героя, бої хвилями в TBS 3.
