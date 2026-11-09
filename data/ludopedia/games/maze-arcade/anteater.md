---
title: Anteater (Мурахоїд)
slug: anteater
aka: [Мурахоїд, Ardy the Aardvark]
family: maze-arcade
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: full
  random: runtime
  goal: collect
year: 1982
platforms: [arcade (Tago Electronics)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Anteater_(video_game)", best: true, note: "язик, удар лише кінчиком, черв'яки ззаду, павук уночі, королева, очки й бонус ants×worms"}
  - {kind: other, url: "https://www.arcade-museum.com/Videogame/anteater", note: "KLOV: джойстик + кнопка втягування, дні коротшають, життя кожні 20 000"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Oil%27s_Well", note: "Oil's Well (Sierra, 1983) — переосмислений клон: бур і труба"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=anteater+1982+arcade+gameplay", note: "пошук; геймплей аркади"}
stage: v1
coverage: 65
mechanics: [move-4dir, impassable-cells, collect-all, touch-death, player-death, event-points, extra-life-threshold, progress-acceleration, random-walk, spawn-points, status-panel, game-screen, +anchored-tether-body, +tip-only-attack, +fast-retract, +attack-from-behind, +day-night-hazard, +screen-clear-pickup, +product-bonus]
proposes: ["+effect:retract", "+trigger:night_start", "+cond:from_behind", "+card:anchored-tether-body", "+card:tip-only-attack", "+card:day-night-hazard", "+card:product-bonus", "+role:tether"]
author: opus
date: 2026-11-09
---

# Anteater — мурахоїд просуває язик лабіринтом мурашника: їсть лише кінчик, а тіло язика вразливе

## Суть
Мурахоїд сидить на поверхні, а гравець веде кінчик його язика тунелями мурашника, з'їдаючи личинок (червоні точки). Язик — це шлях від морди до кінчика: їсти може лише кінчик, а мураха, що торкнулася будь-якої іншої частини язика, забирає життя. Кнопка швидко втягує язик назад — головний спосіб рятуватися. Уночі по язику спускається павук; позбутися його можна, лише з'ївши королеву на дні.

## Поле і час
- Поле — вертикальний розріз мурашника: тунелі-коридори на клітинній сітці, мурахоїд — нерухомо нагорі, звідти починається язик.
- Real-time: мурахи й черв'яки повзуть коридорами, кінчик язика рухається під джойстиком.
- Над поверхнею сонце перетинає екран — це таймер дня; після заходу настає ніч і з'являється павук. З кожним рівнем дні коротші (?).
- Шари: тунелі → личинки → язик (лінія клітин від морди до кінчика) → істоти.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Кінчик язика | player | 4 напрямки | веде язик тунелем, їсть усе, на що наступає (крім голови черв'яка (?)) |
| Тіло язика | object (`+role:tether`) | довжина = пройдений шлях | вразливе: дотик мурахи = втрата життя; по ньому лізе павук |
| Мурахоїд | static | — | точка кріплення язика нагорі |
| Личинка | pickup | 10 очок | мета рівня: з'їсти всі |
| Мураха | enemy | 100 очок | повзає тунелями; кінчик її з'їдає, тіло — гине від неї |
| Черв'як | enemy | 200 очок | повзає тунелями; їсти лише ззаду, голова небезпечна |
| Павук | enemy | — | з'являється вночі, повзе по язику до кінчика |
| Королева мурах | pickup | 1000 очок | на дні мурашника; з'їдена — очищає поле від павука, мурах і черв'яків |
| Сонце | — | швидкість росте з рівнем | таймер дня над поверхнею |
| Тунелі / ґрунт | static | — | язик іде лише коридорами |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(cell_ahead)` → ТО `move(tip, dir)`, `grow(tongue, 1)`.
- КОЛИ `input(dir)` → ЯКЩО `custom: «напрямок назад уздовж власного язика»` → ТО `grow(tongue, -1)` (?).
- КОЛИ `input(retract)` → ТО `custom: «язик швидко змотується до морди»` (`+effect:retract`).
- КОЛИ `contact(tip, larva)` → ТО `disappear_b`, `score(10)`.
- КОЛИ `contact(tip, ant)` → ТО `disappear_b`, `score(100)`, `counter(ants_eaten, 1)`.
- КОЛИ `contact(ant, tongue_body)` → ТО `lives(-1)`.
- КОЛИ `contact(tip, worm)` → ЯКЩО `custom: «кінчик позаду голови черв'яка»` (`+cond:from_behind`) → ТО `disappear_b`, `score(200)`, `counter(worms_eaten, 1)`.
- КОЛИ `contact(tip, worm)` → ЯКЩО `not custom: «ззаду»` → ТО `lives(-1)` (?).
- КОЛИ `custom: «сонце зайшло»` (`+trigger:night_start`) → ТО `spawn(spider)`.
- КОЛИ `tick` → ЯКЩО `count(spider, >, 0)` → ТО `custom: «павук сповзає по язику на клітину ближче до кінчика»`.
- КОЛИ `reach(spider, tip)` → ТО `lives(-1)`.
- КОЛИ `contact(tip, queen)` → ТО `score(1000)`, `custom: «зникають павук, усі мурахи й черв'яки»`.
- КОЛИ `all_gone(larva)` → ТО `next_level`.
- КОЛИ `level_end` або `died(player)` → ТО `score(10 × ants_eaten × worms_eaten)` — бонус-добуток.
- КОЛИ `counter(score, >=, 20000·k)` → ТО `lives(+1)`.
- КОЛИ `level_start` → ТО `custom: «день коротший, ніж на попередньому рівні»`.
- Перемога: з'їсти всі личинки рівня · Поразка: 0 життів · Рахунок: личинки, мурахи, черв'яки, королева + бонус-добуток.

## Керування і ввід
- 4-напрямний джойстик веде кінчик язика тунелями.
- Одна кнопка — швидке втягування язика (рятує від мурахи, що наближається до тіла, і від павука).
- 1–2 гравці по черзі (alternating).

## Вікна, меню, HUD
- `attract-demo` — автомат у режимі очікування (?).
- `game-screen`: розріз мурашника, мурахоїд і сонце нагорі; `score`, `hi-score`, `lives` (?).
- `custom-window` — підрахунок бонусу ants × worms після рівня чи смерті (?).
- `end-screen` — GAME OVER (?).

## Фічі поза полем
- `levels-sequential` з наростанням темпу (коротші дні).
- Додаткове життя кожні 20 000 очок.
- 2 гравці по черзі; домашніх портів не було (порт на Atari 2600 скасовано).

## Варіації й родичі
- Ardy the Aardvark (Datamost, 1983, Apple II → C64/Atari 8-bit) — майже точна копія.
- Oil's Well (Sierra, 1983) — бур замість язика, труба тягнеться до бази, кнопка швидко втягує бур; 8 рівнів. Клони: Pipeline Run, Oilmania, Aardvark (Bug-Byte), Jack the Digger, Diamond Mine I–II.
- Родичі: `snake` (тіло як шлях, але рухоме), `pac-man` (точки в лабіринті), `tron-light-cycles` (слід як вразлива/небезпечна стіна).
- **Осі варіацій:** тіло-шлях прив'язане до бази / вільне (змійка) · втягування лише назад-кроком / кнопкою · вразливість тіла: смерть / розрив / нема · атака кінчиком: усіх / лише ззаду · нічна загроза: павук по тілу / нема.

## Цікавинки для курсу
- Язик як стек клітин від бази до кінчика: крок назад = pop, кнопка = швидкий pop усіх — 🌱: найпростіша структура з цікавою грою.
- Вразливе тіло й атакуючий кінчик: колізії розрізняють «голову» і «тіло» тієї самої сутності — 📎.
- «Їсти лише ззаду» — перевірка напрямку руху цілі відносно атакувальника — 📎.
- Павук, що повзе по тілу-шляху гравця (рух графом, який будує сам гравець) — 🥉.
- Бонус-добуток ants × worms: заохочує ризикувати з обома видами — 🌱.
- День-ніч як таймер, що не вбиває, а випускає нову загрозу — 📎.

## Мапа на каталог
- Є: `move-4dir` · `impassable-cells` · `collect-all` (личинки) · `touch-death` · `player-death` · `event-points` · `extra-life-threshold` · `progress-acceleration` (дні коротшають) · `random-walk` (мурахи (?)) · `spawn-points` · `status-panel`.
- **Нема** → пропозиції карток:
  - `+anchored-tether-body` «Тіло-шлях від бази» · entities/move · 📎 · слот {retract: step|button} — довжина = шлях від точки кріплення.
  - `+tip-only-attack` «Атакує лише голова» · entities/combat · 🌱 — тіло вразливе, кінчик їсть.
  - `+fast-retract` «Швидке втягування» · entities/move · 🌱 — кнопка змотує тіло до бази.
  - `+attack-from-behind` «Бити лише ззаду» · entities/combat · 📎.
  - `+day-night-hazard` «Ніч випускає загрозу» · game-logic/waves · 📎 · слот {day_length}.
  - `+screen-clear-pickup` «Предмет очищає поле від ворогів» · entities/interact · 🌱 (королева).
  - `+product-bonus` «Бонус-добуток двох лічильників» · game-logic/score · 🌱.

## Пропозиції до словників
- `+effect:retract` — змотати тіло-шлях до точки кріплення (є в іншій грі корпусу; підтверджую).
- `+trigger:night_start` — настала ніч / фаза доби змінилась.
- `+cond:from_behind` — A торкається B з боку, протилежного напрямку руху B.
- `+role:tether` — тіло-шлях, прив'язане до бази (язик, труба, мотузка).
- `+card:anchored-tether-body`, `+card:tip-only-attack`, `+card:day-night-hazard`, `+card:product-bonus` — див. «Мапу на каталог».

## Джерела
- ⭐ [Wikipedia: Anteater (video game)](https://en.wikipedia.org/wiki/Anteater_(video_game)) — механіка язика, вороги, королева, очки (10/100/200/1000), бонус 10 × ants × worms, клони.
- [KLOV: Anteater](https://www.arcade-museum.com/Videogame/anteater) — джойстик 4-way + кнопка втягування, 2 гравці по черзі, дні коротшають, extra life кожні 20 000.
- [Wikipedia: Oil's Well](https://en.wikipedia.org/wiki/Oil%27s_Well) — найвідоміший клон, 8 рівнів, кнопка втягування.
- YouTube: пошук «anteater 1982 arcade gameplay».

## Непевне
- (?) Чи рух кінчика назад уздовж язика втягує його покроково, чи язик змотується лише кнопкою.
- (?) Що буває, коли голова черв'яка торкається кінчика чи тіла язика: KLOV — «не торкатися голови», Wikipedia — «їсти лише ззаду».
- (?) Чи королева зникає після поїдання (Wikipedia: «королеви виживають»; KLOV: «очищає всіх істот»).
- (?) Чи кінець дня/часу щось забирає, крім появи павука; яка тривалість дня.
- (?) Як рухаються мурахи (випадково чи до язика), звідки з'являються.
- (?) Склад HUD, attract-режим, екран бонусу — джерел нема.
