---
title: Mr. Driller
slug: mr-driller
family: dig-gravity
also: [falling-match]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: setup
  goal: state
year: 1999
platforms: [arcade, PlayStation, Dreamcast, Game Boy Color, WonderSwan Color, PC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Mr._Driller", best: true, note: "серія: кольорові блоки, 4 однакові зникають, повітря, X-блоки, перелік ігор"}
  - {kind: other, url: "https://planetdc.segaretro.org/games/reviews/mrdriller/", note: "огляд DC: X-блок 5 ударів і −20 повітря, капсула +20, 5 футів на шар, 500-футові секції, режими, очки"}
  - {kind: other, url: "https://www.arcade-museum.com/Videogame/mr-driller", note: "KLOV: аркада, 2500/5000 ft, джойстик + кнопка Drill"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Mr._Driller_Online", note: "Xbox 360: онлайн-версія"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=Mr.+Driller", note: "пошук; Mr. Driller DrillLand (2020)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Mr+Driller+arcade+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 75
mechanics: [move-4dir, gravity-fall, environment-death, player-death, item-pickup, event-points, time-bonus, score-records, progress-acceleration, infinite-field, player-camera, difficulty-levels, status-panel, +dig-terrain, +dig-wall, +connected-group-pop, +cascade-gravity, +chain-reaction, +delayed-fall, +hunger-clock, +group-support, +depth-goal]
proposes: ["+trigger:settled", "+cond:supported", "+cond:connected", "+effect:collapse", "+effect:wobble", "+ui:depth-meter", "+ui:air-gauge", "+card:group-support", "+card:depth-goal"]
author: opus
date: 2026-11-02
---

# Mr. Driller — бури вниз крізь кольорові блоки, доки не скінчилось повітря і не придавило згори

## Суть
Сусуму Хорі буром руйнує блоки під собою і спускається в колодязь до цільової глибини. Блоки однакового кольору злипаються в групи; група без опори хитається й падає, а коли падіння зʼєднує **4+ блоки одного кольору**, вони зникають — можливі ланцюги. Небезпек дві: впасти під блок, що падає згори, і вичерпати повітря, яке постійно тече і поповнюється лише капсулами. Це «падаючі блоки навпаки»: гравець не скидає блоки, а риє під ними.

## Поле і час
- Вертикальна шахта ~7–9 колонок завширшки (?), нескінченна вниз; камера йде за гравцем, видно кілька екранів шарів над ним (звідти падає загроза).
- Шар (рядок) = 5 футів; гра ділиться на секції по 500 футів, кожна складніша (більше X-блоків, швидший темп).
- Real-time; блоки після втрати опори хитаються коротку паузу й падають; повітря зменшується щосекунди.
- Розкладка кольорів випадкова (Arcade); у Time Attack — фіксовані рівні.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Містер Дриллер | player | повітря 100, 3 життя (1–5 у DC) | ходить ліворуч/праворуч, бурить у 4 сторони, залазить на 1 блок угору |
| Кольоровий блок ×4 | tile | колір | 1 удар буром — зникає вся звʼязна група того ж кольору (?); падає, якщо група без опори |
| X-блок (коричневий) | tile | 5 ударів | зникнення коштує −20 повітря; 4+ звʼязаних X теж зникають |
| Повітряна капсула | pickup | +20 повітря | лежить у клітині; бере дотиком |
| Падаючий блок | object | — | хитається, потім падає; приземлився на гравця → смерть |
| Цільова глибина | static | 2500 / 5000 ft | досягнення — перемога забігу |
| Годинник (Time Attack) | pickup | номінал секунд | замінює капсулу; віднімає час від таймера |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drill, dir)` → ЯКЩО `cell(target, color_block)` → ТО `clear(group(target))`, `score(10 × n)` (?).
- КОЛИ `input(drill, dir)` → ЯКЩО `cell(target, x_block)` → ТО `damage(1)`; 5-й удар → `disappear_b`, `counter(air, -20)`.
- КОЛИ `input(move, dir)` → ЯКЩО `free(target)` → ТО `move`; ЯКЩО висота 1 → `custom: «залізти на блок»`.
- КОЛИ `not supported(player)` → ТО `fall(player)` (вільне падіння шахтою вниз, глибина росте).
- КОЛИ `not supported(group)` → ТО `wobble(group)` → `fall(group)` як одне ціле: `custom: «група того ж кольору тримається, якщо хоч один її блок має опору»`.
- КОЛИ `settled(group)` → ЯКЩО `connected(same_color) ≥ 4` → ТО `clear(group)`, `after` → нові групи без опори → `chain`.
- КОЛИ `settled(falling)` → ТО `custom: «блок прилипає до сусідів того ж кольору»`.
- КОЛИ `contact(falling_block, player)` згори → ТО `lose` (розчавлено), `lives(-1)`.
- КОЛИ `timer(1 s)` → ТО `counter(air, -1)`; КОЛИ `counter(air, ==, 0)` → ТО `lose`, `lives(-1)`.
- КОЛИ `contact(player, air_capsule)` → ТО `pickup`, `counter(air, +20)`, `score(n)`.
- КОЛИ `counter(depth, %, 500)` → ТО `progress-acceleration`: більше X-блоків, нова палітра секції.
- КОЛИ `counter(depth, >=, goal)` → ТО `win`.
- КОЛИ `lives == 0` → ТО `game_over`.
- Перемога: дійти до 2500/5000 ft (Arcade) або до дна рівня (Time Attack, на час). Поразка: розчавлення або нуль повітря при 0 життів. Рахунок: блоки (групи вигідніші за поштучні), капсули, глибина; ланцюги підвищують очки.

## Керування і ввід
- Джойстик 4 напрямки + одна кнопка Drill (аркада). Напрямок джойстика задає, куди бурити: ліворуч, праворуч, вниз, вгору.
- Головна навичка — не стояти під щойно підрізаною групою і стежити за кольорами над головою.

## Вікна, меню, HUD
- `splash-screen` / `attract-demo`.
- `mode-select` (домашні версії): Arcade (2500 ft / 5000 ft), Time Attack, Survival (?).
- `game-screen`: шахта, справа панель — `score`, `depth-meter` (фути), `air-gauge` (відсоток повітря), `lives`, `level-number` (секція).
- `end-screen`: досягнута глибина й очки; `leaderboard` з ініціалами.
- `settings-window` (DC): кількість життів 1–5, складність.

## Фічі поза полем
- `mode-classic` (Arcade 2500/5000), `mode-time-attack` (10 стадій з фіксованими блоками; спершу відкриті 4, далі — за рекорд), `mode-endless` / Survival (?).
- `leaderboard-local`, рекорди часу в Time Attack (`speedsolve`-подібно).
- `difficulty-presets`: 2500 ft — новачки, 5000 ft — експерти.

## Варіації й родичі
- Mr. Driller 2 (швидше, кооп на двох, нові режими), G (сюжет і персонажі з різними атрибутами: менше повітря / швидший рух), A (RPG-елементи), Drill Land (парк режимів), Drill Spirits (боси, магазин), Drill Till You Drop (кристали-ефекти), DrillLand (2020, Switch/PC).
- Пізніші блоки: зіркові (зникають через час), прозорі/кристальні.
- Родичі: Dig Dug (сімейство Хорі), Puyo Puyo (група з 4+ кольору, каскад), Boulder Dash (копання + падіння), Meteos.
- **Осі варіацій**: хто рухає блоки — «гравець скидає (Tetris/Puyo) / гравець прибирає опору (Driller)»; ресурс-годинник — «повітря / час / голод»; що робить найтвердіший блок — «кілька ударів / ціна ресурсом / обидва».

## Цікавинки для курсу
- Звʼязні групи кольору як тіла: опора групи = опора будь-якого її блока, падіння всією групою — 🥇 (flood fill за кольором + перевірка опори + рух групи + злипання після приземлення).
- Ланцюги «впало → склалось 4+ → зникло → щось ще впало» — 🥈 (каскадний цикл до стабілізації).
- Повітря як годинник, що поповнюється капсулами й штрафується X-блоком — 🌱.
- Затримка-хитання перед падінням — дає гравцю шанс утекти — 📎.
- Блок з HP (5 ударів) і ціною ресурсу — 🌱.
- Нескінченна шахта вниз з камерою і секціями складності — 🥈 (генерація шарів на льоту).

## Мапа на каталог
- Є: `move-4dir` · `gravity-fall` · `environment-death` ↔ розчавлення · `player-death` · `item-pickup` ↔ капсули · `event-points` · `time-bonus` (Time Attack) · `score-records` · `progress-acceleration` ↔ 500-футові секції · `infinite-field` ↔ шахта вниз · `player-camera` · `difficulty-levels` · `status-panel`.
- **Нема** → пропозиції карток:
  - `+group-support` «Звʼязна група одного кольору падає як ціле» · entities/move · 🥇 · слоти {adjacency: 4, stick_on_land: bool}.
  - `+depth-goal` «Мета — глибина спуску» · game-logic/win · 🌱 · слот {goal: 2500ft}.
  - Повтори: `+dig-terrain`, `+dig-wall` (X-блок: міцність 5), `+connected-group-pop` (слоти {min: 4, adjacency: 4}), `+cascade-gravity`, `+chain-reaction`, `+delayed-fall` (хитання, без руйнування), `+hunger-clock` (повітря: max 100, rate 1/с, штраф X −20).

## Пропозиції до словників
- `+trigger:settled` ⏳ — група приземлилась (перевірка збігу після падіння).
- `+cond:supported` ⏳ — є опора знизу; `+cond:connected` ⏳ — звʼязна група того ж кольору.
- `+effect:collapse` — падіння групи як цілого (на відміну від `fall` однієї сутності); `+effect:wobble` — стан «хитається N тіків» перед падінням (можна як `set_state(wobble, n)` — слабка пропозиція).
- `+ui:depth-meter` — лічильник глибини (Mr. Driller, SteamWorld Dig, Dome Keeper); `+ui:air-gauge` — шкала ресурсу-годинника (близько до ⏳ `energy-bar`).

## Джерела
- ⭐ [Wikipedia: Mr. Driller](https://en.wikipedia.org/wiki/Mr._Driller) — ядро серії: 4 однакові зникають, ланцюги, повітря й капсули, X-блоки з 5 ударів, перелік ігор і платформ.
- [Planet Dreamcast review](https://planetdc.segaretro.org/games/reviews/mrdriller/) — 4 кольори, злипання, хитання перед падінням, X = −20 повітря, капсула +20, 100 повітря, 5 ft на шар, режими Arcade/Time Attack, життя 1–5, 10 очок за блок.
- [KLOV: Mr. Driller](https://www.arcade-museum.com/Videogame/mr-driller) — аркада Namco 1999, 2500/5000 ft, джойстик + Drill, 4+ X-блоки теж зникають.
- [Wikipedia: Mr. Driller Online](https://en.wikipedia.org/wiki/Mr._Driller_Online) — онлайн-версія Xbox 360.
- YouTube: пошук «Mr Driller arcade gameplay».

## Непевне
- (?) Чи удар по кольоровому блоку прибирає всю звʼязну групу, чи лише один блок — у памʼяті вся група; джерела кажуть «руйнувати формації».
- (?) Ширина шахти (7 чи 9 колонок) і темп спадання повітря (1/с).
- (?) Множник очок за групу (×3 у огляді DC) і зростання очок за капсули (100, 200, 300… — лише з пошукового сніпета).
- (?) Survival-режим у PS/DC версії — згаданий без правил.
- (?) Що відбувається після смерті (розчищення стовпа над гравцем) — не перевірено.
