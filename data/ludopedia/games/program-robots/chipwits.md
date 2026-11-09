---
title: ChipWits
slug: chipwits
aka: [IBOL, ChipWits II, ChipWits (2025)]
family: program-robots
also: []
klass: avatar
axes:
  field: square
  time: programmed
  opponent: none
  info: partial
  random: both
  goal: score
year: 1984
platforms: [Macintosh, Apple II, C64, PC (Steam 2025)]
links:
  - {kind: other, url: "https://github.com/chipwits/chipwits-forth", best: true, note: "вихідний код Forth і оригінальні мануали Mac / C64 / Apple II (docs/*.pdf): усі оператори, середовища, ціни, шкода"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/ChipWits", note: "історія: Sharp і Johnston, порти Epyx, ChipWits II, ребут на Unity"}
  - {kind: steam, url: "https://store.steampowered.com/app/2330720/ChipWits/", note: "ремейк 2025: фабрика, рахунок / мінімум чипів / мінімум циклів, лідерборди"}
  - {kind: official, url: "https://chipwits.com/docs/", note: "документація ремейку: чипи дій, сенсорів, стеків; місії-пазли"}
  - {kind: play, url: "https://chipwits.com/retro/", note: "оригінал в емуляторі"}
  - {kind: steam, url: "https://store.steampowered.com/app/4960100/ChipWits_Worlds/", note: "ChipWits Worlds (анонс): колонія роботів на 65C02"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=chipwits+1984+gameplay", note: "пошук; геймплей оригіналу й ремейку"}
stage: v1
coverage: 70
mechanics: [command-program, user-procedures, sensor-predicates, step-execution, code-editor-window, drag-drop-piece, impassable-cells, orientation-state, move-8dir, item-pickup, event-points, hunger-clock, hp-damage, touch-death, keyboard-controls, level-select, save-multi-slot, stats-window, score-records, sound-effects, leaderboard, +flowchart-chip-grid, +true-false-wires, +typed-stacks, +cycle-budget, +action-energy-cost, +series-average-score, +room-by-room-view, +signpost-arrow-pattern, +regenerating-pickup, +keypress-override, +range-finder-register, +value-wrap-0-7, +negative-points-for-killing]
proposes: ["+effect:jump(to)", "+effect:call(fn)", "+effect:return", "+effect:stack_push(v)", "+effect:stack_pop(s)", "+cond:stack_top(s, op, v)", "+cond:key_pressed(k)", "+ui:status-beakers", "+ui:stack-registers", "+window:warehouse", "+feature:series-mode", "+feature:solution-metrics", "+feature:print-program"]
author: opus
date: 2026-11-09
---

# ChipWits — робот за мовою іконок IBOL: панель з 60 чипів, дроти «так/ні», три стеки, і місії в кімнатах із пирогами, кавою, дисками, електрокрабами й бомбами

## Суть
Освітня гра 1984 року (Doug Sharp, Mike Johnston; Mac, 1985 — Apple II і C64 від Epyx). Гравець у Майстерні викладає програму робота-ЧіпВіта з **чипів-іконок** на панелі: кожен чип — оператор (дієслово: LOOK, FEEL, MOVE, ZAP…) і аргумент (предмет: пиріг, стіна, напрям), а виконання тече дротами **T/F** від чипа до чипа. Потім робот іде на місію в одне з 8 середовищ — кімнати з дверима, де він сам шукає їжу (пальне), підбирає диски й оливу (очки), стріляє в електрокрабів і обходить бомби, доки не скінчаться цикли, пальне чи здоровʼя. Мета — найвищий рахунок; ремейк 2025 року на Unity додав місії-пазли з рахунком за кількість чипів і циклів.

## Поле і час
- Середовище — набір кімнат; кімната — сітка плиток підлоги в рамці стін, проходи в зовнішніх стінах — двері; усередині деяких кімнат — внутрішні стіни.
- Видно лише поточну кімнату: пройшов у двері → показується наступна (C64: кімната змінюється, коли робот на дверях подивився, помацав, схопив чи вистрілив уперед).
- Робот стоїть на плитці й дивиться в напрямок; MOVE — крок уперед/назад на плитку або поворот на 45° на місці.
- Час програмний: кожен виконаний чип забирає **цикли** (бюджет місії) і **пальне**; швидкість показу — від повної до «чип за клік».
- Кількість кімнат і бюджет циклів — за середовищем (нижче).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| ЧіпВіт | player | пальне 7000, шкода 0…1400, цикли, напрям | виконує програму; 4 сенсори, руки, плазмовий промінь |
| Стіна | static | — | непрохідна; врізатись −50 здоровʼя; взяти −50 |
| Підлога | terrain | — | порожня плитка; її теж можна «побачити» чи «помацати» |
| Двері | static | — | прохід у сусідню кімнату |
| Пиріг | pickup | +1200 пального | PICK UP — заправка, очок не дає |
| Кава | pickup | +1200 пального | те саме |
| Каністра оливи | pickup | очки за середовищем | PICK UP → очки |
| Диск | pickup | очки за середовищем | PICK UP → очки; у Memory Lanes відроджується |
| Електрокраб | enemy | очки за ZAP | атакує: −200 пального; врізатись −100; взяти −150 |
| Баунсер (bouncer) | enemy | очки за ZAP | врізатись −100; взяти −150 (C64: висмоктує енергію) |
| Бомба | hazard | — | взяти, вистрілити чи врізатись → 1400 шкоди, кінець |
| Знак-стрілка (Mystery Matrix) | zone | 3 обʼєкти в ряд | два однакові — древко, третій — вістря: вказує вигідний шлях |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `exec(LOOK thing)` → ЯКЩО `line_of_sight(chipwit, thing)` → ТО `custom: «гілка T»`, `counter(range, =distance)`; інакше гілка F.
- КОЛИ `exec(SMELL thing)` → ЯКЩО `count(thing_in_room, >=, 1)` → ТО гілка T; інакше F.
- КОЛИ `exec(FEEL thing)` → ЯКЩО `occupied(front_cell, thing)` → ТО гілка T; інакше F.
- КОЛИ `exec(PICK UP)` → ЯКЩО `occupied(front_cell, pie|coffee)` → ТО `pickup`, `counter(fuel, +1200)`.
- КОЛИ `exec(PICK UP)` → ЯКЩО `occupied(front_cell, oil|disk)` → ТО `pickup`, `score(env_value)`.
- КОЛИ `exec(PICK UP)` → ЯКЩО `occupied(front_cell, wall)` → ТО `damage(50)`; crab|bouncer → `damage(150)`; bomb → `damage(1400)`.
- КОЛИ `exec(ZAP)` → ЯКЩО `occupied(front_cell, crab|bouncer)` → ТО `disappear_b`, `score(env_value)` (у Peace Paths — від'ємні).
- КОЛИ `exec(ZAP)` → ЯКЩО `occupied(front_cell, pie|coffee|oil|disk)` → ТО `disappear_b` без пального й очок; bomb → `damage(1400)`; стіни й підлога не знищуються.
- КОЛИ `exec(MOVE forward|back)` → ЯКЩО `free(target)` → ТО `move(chipwit, dir)`; інакше `block`, `damage(100)` за краба/баунсера або `damage(50)` за інше.
- КОЛИ `exec(MOVE turn)` → ТО `rotate(chipwit, ±45)`.
- КОЛИ `exec(MOVE stack)` → ТО `custom: «виконати хід з вершини Move-стеку»`.
- КОЛИ `contact(crab, chipwit)` → ТО `counter(fuel, −200)`.
- КОЛИ `exec(op)` → ТО `counter(cycles, −cost(op))`, `counter(fuel, −fuel_cost(op))` — з таблиці мануала (JUNCTION — 0/0, MOVE — 3 цикли й 5 пального).
- КОЛИ `exec(COIN FLIP)` → ЯКЩО `prob(1/2)` → ТО гілка T; інакше F.
- КОЛИ `exec(KEYPRESS key)` → ЯКЩО `custom: «клавіша (або будь-яка для порожнього аргументу) натиснута саме зараз»` → ТО гілка T.
- КОЛИ `exec(SUB-PANEL X)` → ТО `custom: «перехід на світлофор підпанелі X (A–G), лише з головної»`; `exec(BOOMERANG)` → `custom: «повернення на головну, до чипа після виклику»`; `exec(LOOP)` → `custom: «на світлофор поточної панелі»`; `exec(JUNCTION)` — лише зʼєднує.
- КОЛИ `exec(SAVE MOVE|THING|NUMBER v)` → ТО `custom: «push v у свій стек (≤ 256; 257-й витісняє найстаріший)»`; `exec(POP s)` → `custom: «зняти вершину стеку s»`.
- КОЛИ `exec(COMPARE MOVE|THING v)` → ЯКЩО `same(stack_top, v, value)` → ТО гілка T; аргумент «порожній квадрат» = стек порожній.
- КОЛИ `exec(COMPARE NUMBER: EQUAL?|LESS THAN? v)` → ЯКЩО `custom: «вершина Number-стеку = v / < v»` → ТО гілка T; v — 0…7, пальне, шкода, далекомір.
- КОЛИ `exec(INCREMENT|DECREMENT)` → ТО `custom: «вершина Number-стеку ±1 по колу 0…7»`.
- КОЛИ `exec(SING v)` → ТО `sound(note v)` — нота 0…7 (октава), зі стеку чи з показника.
- КОЛИ `enter(chipwit, door)` → ТО `custom: «показується сусідня кімната»`.
- КОЛИ `custom: «у Memory Lanes робот на протилежному кінці лабіринту»` → ТО `spawn_at(disk, other_end)`.
- КОЛИ `counter(cycles, ==, 0)` або `counter(fuel, ==, 0)` → ТО `game_over`; КОЛИ `counter(damage, >=, 1400)` → ТО `lose`.
- Перемога: нема — рекорд і середній рахунок ЧіпВіта в середовищі · Поразка: шкода 1400 (бомба, удари) · Рахунок: очки за диски, оливу й ZAP за таблицею середовища.

## Керування і ввід
- Майстерня: клік по порожньому чипу → клік по іконці оператора (рядок Operators) → клік по аргументу (меню Arguments підлаштовується під оператор).
- Дроти T і F: клік по дроту, потім по іншій стороні чипа — дріт переїжджає; без дротів (MOVE, PICK UP) потік іде далі за розташуванням.
- Чип перетягується мишею (на зайнятий — замінює); видалення — кошик; Cut / Copy / Paste цілої панелі, Clear Panel.
- Панель — 60 чипів, головна + 7 підпанелей A–G; виконання починається зі «світлофора» в рядку 1, стовпці 1.
- Під час місії: швидкість — колібрі (повна), равлик (повільно), черевик (чип за клік); KEYPRESS дає вручну «підказати» роботу гілку (ручний обхід ще не написаної логіки).
- C64: керування джойстиком у тих самих меню.

## Вікна, меню, HUD
- `splash-screen` BrainPower → заставка «Ready when you are».
- Рядок меню: **Warehouse** (16 слотів ЧіпВітів; Greedy і Mr. C.W. — готові; позначка «призначений для поточного середовища»), **Workshop** (Enter, Save ChipWit з назвою й позначками середовищ, Cut / Copy / Paste / Clear Panel), **Environments** (Start / End Mission, Series / Last Mission, 8 середовищ), **Options** (Print Screen, Print Panel, Sound Off/On, Debug On / Show Stats, Quit).
- `code-editor` (Майстерня): панель чипів, Operators, Arguments, кошик, перемикач головна / A–G.
- `game-screen` (Environment): кімната; `score` зліва вгорі, цикли справа вгорі; панель Status — мензурки шкоди, пального, останньої клавіші, далекоміра (0–7); Memory — верхні 3 елементи кожного з трьох стеків; вікно Debug — чверть панелі з підсвіченим поточним чипом (`instruction-highlight`), мінісхема, яка чверть і яка панель.
- `stats-window`: рекорд, середній рахунок і кількість місій цього ЧіпВіта в цьому середовищі (змінив програму — статистика з нуля).
- `confirm-dialog`: зберегти ЧіпВіта (імʼя, середовища).

## Фічі поза полем
- 8 середовищ (Mac; очки диск / олива / краб / баунсер; цикли):
  - Greedville — 4 кімнати, лише добро; 100 / 50; 6000.
  - ChipWit Caves — 8 кімнат складають слово «CHIPWITS»; 100 / 50 / 50; 10 000.
  - Doom Rooms — 13 кімнат (C64: 12), лише краби й баунсери; краб 100, баунсер 250; 10 000.
  - Peace Paths — 54 кімнати, краб −30 (C64: баунсер −60), диск 150, олива 20; 16 000.
  - Memory Lanes — 10 кімнат «підковою», диск-відроджувач на кожному кінці; 250 / 30 / 30 / 60; 20 000.
  - Octopus Garden — 8 коридорів, 44 кімнати; 250 / — / 10 / 20; 20 000.
  - Mystery Matrix — 100 однакових кімнат, знаки-стрілки; 250 / 150 / 20 / 40; 30 000 (C64: 20 000).
  - Boomtown — 9 кімнат з бомбами за візерунком; диск 250, краб 40; 12 000.
- `series-mode`: безкінечна серія місій для чесного середнього; `print-program` (Print Panel на Imagewriter).
- Ремейк 2025 (ChipWits, Inc.): робот CW-03.24 на фабриці Professor Chip; чипи Skate / Pickup / Zap / Sing, If Feel / If Smell / If See, стекові push / pop / порівняння; місії-пазли з обмеженим набором чипів і циклів; оцінка за рахунком, кількістю чипів і циклів, глобальні лідерборди, досягнення, Steam Workshop, коди IBOL для обміну.

## Варіації й родичі
- [robot-odyssey](robot-odyssey.md) — сучасник 1984 року, з яким порівнював Computer Gaming World (схеми замість іконок); [karel](karel.md) — текстовий робот того ж часу; [robozzle](robozzle.md), [lightbot](lightbot.md) — короткі програми з функціями.
- ChipWits II (2006–2008, Adobe AIR): ізометрія й 3D, туторіал, нові чипи й місії; C64-ремейк 2025 («Back to 1985»); ChipWits Worlds (анонс) — колонія роботів, кожен на справжньому 65C02, програми — асемблер, як у [tis-100](tis-100.md) / [exapunks](exapunks.md).
- Осі варіацій: **мова** (іконки з дротами / список команд / асемблер) · **сенсори** (промінь / уся кімната / сусідня клітина) · **памʼять** (нема / типізовані стеки / RAM) · **бюджет** (цикли + пальне / ліміт чипів) · **оцінка** (очки / чипи й цикли).

## Цікавинки для курсу
- Інтерпретатор IBOL: панель-сітка з 60 чипів, у кожного оператор, аргумент і дроти T/F, світлофор і LOOP — 🥈.
- Три сенсори різного радіуса: LOOK по променю з далекоміром, SMELL — уся кімната, FEEL — сусідня клітина — 🥉.
- Три типізовані стеки з обмеженням 256 і числами по колу 0…7 — 📎.
- Бюджет циклів і пального за таблицею вартостей операторів; ZAP vs PICK UP як економічний вибір — 📎.
- Серія місій і середній рахунок як «юніт-тести» програми робота — 🌱.
- Розпізнавання знака-стрілки з трьох обʼєктів у ряд (Mystery Matrix) — 🥉.
- Повернення в Octopus Garden через Move-стек (записати шлях, пройти навпаки) — 🥈.

## Мапа на каталог
- Є: `command-program` · `user-procedures` (підпанелі A–G) · `sensor-predicates` (LOOK / SMELL / FEEL) · `step-execution` (Debug, черевик) · `code-editor-window` (Майстерня) · `drag-drop-piece` (чипи) · `impassable-cells` · `orientation-state` · `move-8dir` (поворот на 45°) · `item-pickup` · `event-points` (таблиця за середовищем) · `hunger-clock` (пальне, пиріг і кава) · `hp-damage` (шкода 1400) · `touch-death` (бомба) · `keyboard-controls` (KEYPRESS) · `level-select` (меню середовищ) · `save-multi-slot` (16 ЧіпВітів) · `stats-window` · `score-records` · `sound-effects` · `leaderboard` (ремейк).
- **Нема** → пропозиції карток:
  - `+flowchart-chip-grid` «Програма — сітка чипів, потік — розташуванням і дротами» · game-logic/program · 🥈.
  - `+true-false-wires` «Кожна перевірка має два виходи T/F» · game-logic/program · 📎.
  - `+typed-stacks` «Окремі стеки для ходів, речей і чисел» · game-logic/program · 📎.
  - `+cycle-budget` «Місія триває N циклів, оператори коштують цикли» · game-logic/program · 🌱.
  - `+action-energy-cost` «Кожна дія витрачає пальне» · entities/state · 🌱.
  - `+series-average-score` «Серія запусків і середній рахунок» · game-logic/score · 🌱.
  - `+room-by-room-view` «Показ поточної кімнати, перехід дверима» · interface/render · 📎.
  - `+signpost-arrow-pattern` «Три обʼєкти в ряд вказують шлях» · levels/design · 📎.
  - `+regenerating-pickup` «Предмет відроджується, коли гравець далеко» · entities/spawn · 🌱.
  - `+keypress-override` «Програма питає людину: натиснута клавіша?» · game-logic/program · 🌱.
  - `+range-finder-register` «Сенсор пише відстань у регістр для програми» · game-logic/program · 🌱.
  - `+value-wrap-0-7` «Числа програми — 3 біти по колу» · game-logic/program · 🌱.
  - `+negative-points-for-killing` «Середовище карає за атаку» · game-logic/score · 🌱.

## Пропозиції до словників
- `+effect:jump(to)` — перехід дротом T/F на інший чип (підтвердження з family).
- `+effect:call(fn)` / `+effect:return` — SUB-PANEL і BOOMERANG.
- `+effect:stack_push(v)` — підтвердження; `+effect:stack_pop(s)` — POP.
- `+cond:stack_top(s, op, v)` — вершина стеку порівняно з v (COMPARE …; порожній = дно).
- `+cond:key_pressed(k)` — людина тримає клавішу в мить виконання.
- `+ui:status-beakers` — показники мензурками 0…7; `+ui:stack-registers` — верхні елементи стеків.
- `+window:warehouse` — склад збережених роботів зі слотами.
- `+feature:series-mode` — серія місій для статистики; `+feature:solution-metrics` — підтвердження (ремейк: чипи й цикли); `+feature:print-program`.

## Джерела
- ⭐ [chipwits/chipwits-forth](https://github.com/chipwits/chipwits-forth) — `docs/ChipWits_Mac_Manual.pdf` (усі оператори з аргументами, меню, середовища з очками й циклами, пальне 7000 / +1200 / −200, шкода 1400 / 50 / 100 / 150, стеки по 256), `docs/ChipWits_C64_Manual.pdf` (символи речей, поворот на 45°, знаки-стрілки, розбіжні числа), скриншот Mac.
- [Wikipedia: ChipWits](https://en.wikipedia.org/wiki/ChipWits) — автори, порти, ChipWits II, ребут, відкриття коду 2024.
- [Steam: ChipWits (2025)](https://store.steampowered.com/app/2330720/ChipWits/) — реліз 11.07.2025, оцінка за рахунком / чипами / циклами, Workshop, лідерборди.
- [chipwits.com/docs](https://chipwits.com/docs/) — назви чипів ремейку, місії-пазли.
- [Steam: ChipWits Worlds](https://store.steampowered.com/app/4960100/ChipWits_Worlds/) — анонс: 65C02, 64 КБ RAM, батарея, електрокраби вночі.

## Непевне
- (?) Розмір кімнати в плитках і розкладка панелі (60 чипів — 6×10 чи інакше) — у тексті мануала не сказано; далекомір «повна мензурка = 7 плиток».
- (?) Чи хід по діагоналі можливий після повороту на 45° (тег `move-8dir` — за описом повороту).
- (?) Чи рухаються електрокраби й баунсери і як саме «атакує» краб — мануал не описує поведінку.
- (?) Таблиця циклів / пального з PDF прочитана частково: Loop, Sub-Panel, Boomerang 1/1; Junction 0/0; Move 3/5; Pick up 1/5; Zap 1/7; Sing 2/2; Feel 4/4; Look 4/2 — решту (Smell, Coin Flip, стекові) витягти не вдалось, можливе зміщення колонок.
- (?) ZAP бʼє «anything directly ahead in the room» — лише сусідню клітину чи весь промінь, з мануала неясно.
- (?) Розбіжності версій: Doom Rooms 13 / 12 кімнат, Mystery Matrix 30 000 / 20 000 циклів (Mac / C64).
