---
title: Unmatched
slug: unmatched
aka: ["Unmatched: Battle of Legends", "Unmatched: Digital Edition"]
family: tactics
also: []
klass: figure
axes:
  field: graph
  time: turn
  opponent: hotseat
  info: hidden
  random: runtime
  goal: state
year: 2019
platforms: [board, PC]
links:
  - {kind: other, url: "https://rulespal.com/unmatched-battle-of-legends-volume-one/rulebook", best: true, note: "правила Battle of Legends Vol. 1: поле-граф, зони, 2 дії, маневр/схема/атака, бій таємними картами, виснаження колоди, команди"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Unmatched_(board_game)", note: "Restoration Games 2019, кольорові зони = видимість для дальніх атак, набори"}
  - {kind: steam, url: "https://store.steampowered.com/app/1677980", note: "Unmatched: Digital Edition (2023); бачив у пошуку Steam, сторінку не відкривав"}
  - {kind: other, url: "https://www.the-unmatched.club/rules/glossary", note: "фанатський глосарій правил (бачив у результатах пошуку)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Unmatched+board+game+how+to+play", note: "пошук; як грати"}
stage: v1
coverage: 60
mechanics: [melee-vs-ranged, hp-damage, hot-seat, character-select, pocket, +zone-graph-board, +zone-line-of-sight, +hidden-combat-cards, +card-dual-use, +boost-discard, +two-actions-per-turn, +move-through-allies, +deck-exhaustion-damage, +hand-limit, +group-minions, +variable-player-powers, +ability-timing-windows, +leader-death-lose, +asymmetric-sides, +team-play]
proposes: ["+trigger:deck_empty", "+cond:same_zone", "+effect:draw_card", "+effect:discard", "+effect:boost", "+ui:health-dial", "+card:zone-graph-board"]
author: opus
date: 2026-11-09
---

# Unmatched — дуель легенд на полі-графі: дві дії за хід, рух з карт, бій таємними картами атаки й захисту

## Суть
Асиметрична дуель Restoration Games (2019): кожен гравець веде **героя** (Медуза, Король Артур, Аліса, Синдбад, Робін Гуд, Бігфут…) і його **помічників**, а вся сила бійця — його власна колода з 30 карт. За хід — **2 дії** з трьох: маневр (добрати карту й рухатись), схема (зіграти особливу карту) або атака. Бій — **таємні карти**: атакер кладе карту атаки лицем донизу, захисник може покласти карту захисту, обидві відкривають, шкода = різниця. Поле — не сітка, а **граф кружечків**, розфарбованих у **зони**: дальня атака дістає будь-кого у своїй зоні. Гра межова для сімʼї: тактичний рух є, але клітин нема (родич на сітці — [BattleCON](battlecon.md), карти бою на 1D-полі).

## Поле і час
- Поле — кружечки-простори, зʼєднані лініями: сусідство лише по лініях.
- Простори розфарбовані візерунками-**зонами**; простори одного кольору — одна зона, навіть у різних кінцях поля; простір кількох кольорів належить кільком зонам.
- Двостороннє поле — два бойовища; для гри вдвох на двох — окрема мапа на 4 стартові простори.
- Хід — гравці по черзі; молодший ходить першим. Часу на хід нема.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой | player | здоровʼя (диск), рух, ближній / дальній бій, особлива здібність | рухається, атакує, захищається; поразка героя — поразка гравця |
| Помічник | ally | здоровʼя (диск або 1), рух і тип атаки як у героя | рухається, атакує, захищається; переможений — знімається |
| Карта атаки | supply | значення, BOOST, хто може грати, ефект | грається лицем донизу в атаці |
| Карта захисту | supply | значення, BOOST, хто може, ефект | грається лицем донизу в захисті |
| Універсальна карта (versatile) | supply | значення | атака або захист |
| Карта схеми | supply | ефект, хто може | дія «схема» поза боєм |
| Простір | terrain | номер старту (1, 2…) | клітина графа; на ньому одна фігура |
| Зона | zone | колір | дальня атака дістає будь-кого в спільній зоні |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `game_start` → ТО `custom: «кожен тасує 30 карт і бере 5; молодший ставить героя в простір 1, помічників — у ту саму зону; старший — у простір 2»`.
- КОЛИ `turn_start(player)` → ТО `custom: «2 дії з трьох: маневр, схема, атака; повтор дозволено»`.
- КОЛИ `input(maneuver)` → ТО `custom: «обовʼязково добрати 1 карту»`, потім кожен боєць по черзі `move(fighter, adjacent)` до свого значення руху.
- КОЛИ `input(maneuver)` → ЯКЩО `custom: «колода порожня»` → ТО `damage(each_own_fighter, 2)`; скид не перетасовується.
- КОЛИ `input(boost, card)` → ТО `custom: «скинути карту й додати її BOOST до руху, ефект ігнорується»` (так скидають і карти переможених бійців).
- КОЛИ `input(maneuver)` → ЯКЩО `occupied(next_space, ally)` → ТО `custom: «можна пройти, але не зупинитись»`.
- КОЛИ `input(maneuver)` → ЯКЩО `occupied(next_space, enemy)` → ТО `block`.
- КОЛИ `input(scheme, card, fighter)` → ЯКЩО `custom: «боєць, вказаний на карті, ще живий»` → ТО `custom: «розіграти ефект і скинути»`.
- КОЛИ `input(attack, fighter, target)` → ЯКЩО `custom: «ближній бій: ціль у сусідньому просторі»` або `custom: «дальній: ціль у сусідньому просторі чи в спільній зоні»` → ТО `custom: «атакер кладе карту атаки лицем донизу, захисник може — карту захисту, відкривають разом»`.
- КОЛИ `custom: «карти відкрито»` → ТО `custom: «ефекти НЕГАЙНО, потім ПІД ЧАС БОЮ; при конфлікті — спершу захисника»`, `damage(target, attack − defense)`, `custom: «ефекти ПІСЛЯ БОЮ, здібності героїв, скинути карти»`.
- КОЛИ `custom: «атака сама завдала ≥ 1 шкоди»` → ТО `custom: «бій виграв атакер»`; інакше виграв захисник (навіть якщо ефекти завдали шкоди).
- КОЛИ `hp_zero(sidekick)` → ТО `disappear(sidekick)`.
- КОЛИ `hp_zero(hero)` → ТО `lose` (власник), `win` (суперник).
- КОЛИ `turn_end(player)` → ЯКЩО `custom: «у руці > 7 карт»` → ТО `custom: «скинути до 7»`.
- Команди 2 × 2: черга чергується між командами; переможений герой знімається, але гравець ходить, доки живий хоч один помічник; команда програє, коли переможені обидва герої. Утрьох — один гравець веде обох героїв однієї команди.
- Перемога: перемогти героя суперника · Поразка: свій герой на 0 · Рахунок: нема.

## Керування і ввід
- Настільна: диски здоровʼя, міні-фігура героя, жетони помічників, рука карт; таємність — лише в бою (дві карти лицем донизу).
- Цифрова версія (Steam, 2023): ті самі дії; інтерфейс не бачив.

## Вікна, меню, HUD
- `character-select`: вибір героя з наборів і бойовища.
- `game-screen`: поле-граф із зонами; `hp-bar` (диски здоровʼя) героя й помічників; `pocket` — рука карт; лічильник колоди (`remaining-counter`); `legal-move-highlight` простору для руху; підсвітка зони дальньої атаки (`threat-range`).
- `custom-window` бою: дві карти лицем донизу → відкриття → шкода.
- `end-screen` (цифрова версія): переможець.

## Фічі поза полем
- Набори сумісні: героїв і поля різних коробок можна змішувати (`custom-rules`).
- Режими: 1 на 1, 2 на 2, кожен сам за себе (з 3–4 гравцями).
- `online-multiplayer` у цифровій версії — (?).

## Варіації й родичі
- Набори: Battle of Legends Vol. 1 (2019), Robin Hood vs Bigfoot (2019), Jurassic Park: InGen vs Raptors (2020), Marvel (Deadpool 2021, Hell's Kitchen, Teen Spirit…), Cobble & Fog, Houdini vs The Genie; цифрові DLC — Cobble and Fog, Robin Hood vs Bigfoot.
- Родичі: [BattleCON](battlecon.md) (дуель картами на 7 клітинах), [Summoner Wars](summoner-wars.md) (колода фракції як ресурс), [Mage Wars](mage-wars.md) (арена із зон), [Zombicide](zombicide.md) (поле-граф із зонами).
- Осі варіацій:
  - **поле**: сітка / **граф просторів з кольоровими зонами** / 1D-смуга (BattleCON);
  - **видимість**: лінія по клітинах / **спільна зона** / радіус;
  - **бій**: кубики / **таємні карти атаки й захисту** / одночасний вибір пари (BattleCON);
  - **ресурс руху**: фіксований / **буст скинутою картою**.

## Цікавинки для курсу
- Поле-граф із зонами: сусідство по ребрах + перетин множин зон для дальньої атаки — 📎.
- Бій двома таємними картами з таймінгом ефектів (негайно → під час → після) і пріоритетом захисника — 🥉.
- Колода як годинник: виснаження → 2 шкоди кожному бійцю за кожен маневр — 🌱.
- Буст: будь-яка карта — пальне для руху — 🌱.
- Рух крізь своїх, але не крізь ворогів, BFS з обмеженням кроків — 📎.

## Мапа на каталог
- Є: `melee-vs-ranged` ↔ ближні проти дальніх бійців · `hp-damage` ↔ диски здоровʼя · `hot-seat` · `character-select` ↔ вибір героя · `pocket` ↔ рука карт.
- **Нема** → пропозиції карток:
  - `+zone-graph-board` (Zombicide) «Поле — граф просторів, зони за кольором» · entities/legality · 📎.
  - `+zone-line-of-sight` «Видимість = спільна зона» · entities/combat · 🌱.
  - `+hidden-combat-cards` «Атака й захист — карти лицем донизу» · entities/combat · 📎.
  - `+card-dual-use` (Mage Knight) — універсальні карти й буст; `+boost-discard`.
  - `+two-actions-per-turn`, `+move-through-allies`, `+deck-exhaustion-damage`, `+hand-limit`, `+group-minions` (помічники), `+variable-player-powers`, `+ability-timing-windows`, `+leader-death-lose`, `+asymmetric-sides`, `+team-play`.

## Пропозиції до словників
- `+trigger:deck_empty` — колода скінчилась (виснаження).
- `+cond:same_zone` — A і B мають спільну зону поля.
- `+effect:draw_card` · `+effect:discard` · `+effect:boost` — добрати, скинути, скинути заради бонусу руху.
- `+ui:health-dial` — диск здоровʼя на кожного бійця.
- `+card:zone-graph-board` — поля-графа із зонами-видимістю в каталозі нема.

## Джерела
- ⭐ [RulesPal: Unmatched: Battle of Legends, Volume One rulebook](https://rulespal.com/unmatched-battle-of-legends-volume-one/rulebook) — поле-граф і зони, розстановка, 2 дії, маневр і буст, рух крізь своїх, схема, атака, порядок ефектів, перемога в бою, виснаження (2 шкоди), ліміт 7 карт, 30 карт на героя, команди.
- [Wikipedia: Unmatched (board game)](https://en.wikipedia.org/wiki/Unmatched_(board_game)) — видавець, рік, зони як видимість для дальніх атак, таємні карти, шкода = різниця, помічники, набори.
- [Steam: Unmatched: Digital Edition](https://store.steampowered.com/app/1677980) — цифрова версія 2023 (лише з результатів пошуку Steam).
- [the-unmatched.club: глосарій](https://www.the-unmatched.club/rules/glossary) — фанатський довідник термінів (бачив у пошуку, не відкривав).
- YouTube: пошук «Unmatched board game how to play».

## Непевне
- (?) Правило виснаження (2 шкоди без перетасування) у різних наборах може відрізнятись — пошук показав формулювання з окремого набору.
- (?) Режими й мультиплеєр цифрової версії — сторінку Steam не відкривав.
- (?) Особливі здібності героїв (Медуза, Аліса, Артур, Синдбад) — на картках персонажів, у тексті правил не наведено.
