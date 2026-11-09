---
title: RoboMind
slug: robomind
aka: [ROBO, RoboMind Academy]
family: program-robots
also: []
klass: avatar
axes:
  field: square
  time: programmed
  opponent: none
  info: full
  random: runtime
  goal: state
year: 2005
platforms: [PC, Mac, Linux, web]
links:
  - {kind: official, url: "https://www.robomind.net/en/docBasicInstructions.htm", best: true, note: "усі базові команди: рух, фарба, маяки, сенсори «бачити», flipCoin"}
  - {kind: official, url: "https://www.robomind.net/en/docProgrammingStructures.htm", note: "repeat / repeatWhile / if / procedure / return / змінні й оператори"}
  - {kind: official, url: "https://www.robomind.net/en/docExamples.htm", note: "приклади: написати імʼя, знайти білу пляму, line follower, лабіринт з маяком"}
  - {kind: official, url: "https://www.robomind.net/en/robomind.htm", note: "IDE: редактор, монітор, швидкість, покроково"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/RoboMind", note: "історія, версії, 22 мови ключових слів, LEGO NXT"}
  - {kind: official, url: "https://www.robomind.net/", note: "Academy (онлайн-курси) і Desktop"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=robomind+programming+robot", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [command-program, user-procedures, sensor-predicates, step-execution, code-editor-window, impassable-cells, item-pickup, visited-trail, reach-exit, in-game-editor, level-select, game-screen, help-window, settings-window, +runtime-error-stop, +paint-trail-brush, +color-sensors, +coin-flip-predicate, +real-robot-export, +localized-keywords, +camera-follow-robot]
proposes: ["+feature:real-robot-export", "+feature:localized-keywords", "+ui:remote-control-pad", "+ui:camera-follow", "+cond:returns(value)"]
author: opus
date: 2026-11-09
---

# RoboMind — Karel-подібний робот, що малює фарбою слід і читає кольори клітин сенсорами

## Суть
Гравець пише скрипт власною мовою RoboMind (ROBO) і запускає робота на клітинній карті. Робот ходить, повертає, опускає пензель з білою чи чорною фарбою (і лишає слід, поки пензель внизу), бере, кладе і «зʼїдає» маяки. Головна відмінність від Karel — **фарба як памʼять**: робот бачить колір сусідніх клітин (`leftIsWhite`, `frontIsBlack`), тож може йти по лінії або сам собі розмічати шлях. Є `flipCoin` — випадкова умова, отже програма може бути недетермінованою.

## Поле і час
- Квадратна сітка (карта `.map`); робот займає клітину й має напрям N/E/S/W.
- Шари клітини: тло (порожньо / стіна-перешкода) + фарба (біла або чорна лінія на підлозі) + обʼєкт-маяк.
- Сенсори бачать **лише три сусідні клітини** — ліворуч, попереду, праворуч; гравець бачить усю карту.
- Час `programmed`: тік = одна виконана команда руху/дії; швидкість регулюється слайдером, є покрокове виконання.
- Камера: перетягування карти мишею, зум, автостеження за роботом.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Робот | player | позиція, напрям, стан пензля (off / white / black), руки (маяк або нічого) (?) | виконує команди скрипта |
| Перешкода (стіна) | static | — | непрохідна; `forward` в неї — упор |
| Вільна клітина | terrain | — | `xIsClear` = true |
| Біла фарба | mark | колір white | лишається під роботом, поки опущено `paintWhite`; сенсор `xIsWhite` |
| Чорна фарба | mark | колір black | те саме для `paintBlack`; сенсор `xIsBlack` |
| Маяк (beacon) | object | — | `pickUp` бере перед собою, `putDown` кладе перед собою, `eatUp` бере й знищує; заважає руху (?) |
| Карта прикладу (white spot, лінія, лабіринт) | zone | файл `.map` | задає задачу: знайти пляму, пройти по лінії, дістатися маяка |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `exec(forward(n))` → ЯКЩО `free(front)` → ТО `move(robot, facing)` n разів; повертає кількість кроків до упору (`custom: «forward повертає зроблені кроки»`).
- КОЛИ `exec(forward)` → ЯКЩО `not free(front)` → ТО `block` (робот «вдаряється»; скрипт іде далі (?) або зупиняється з помилкою (?)).
- КОЛИ `exec(backward(n))` → ТО `move(robot, back)` n разів без повороту.
- КОЛИ `exec(left|right)` → ТО `face(robot, ±90°)`.
- КОЛИ `exec(north|south|east|west(n))` → ТО `face(robot, dir)`, потім `move(robot, dir)` n разів.
- КОЛИ `exec(paintWhite|paintBlack)` → ТО `set_state(robot, brush_white|brush_black)`.
- КОЛИ `exec(stopPainting)` → ТО `clear_state(robot, brush)`.
- КОЛИ `enter(robot, cell)` → ЯКЩО `state(robot, brush_white|brush_black)` → ТО `paint(cell, color)` — слід фарби.
- КОЛИ `exec(pickUp)` → ЯКЩО `occupied(front, beacon)` → ТО `pickup` (маяк у робота).
- КОЛИ `exec(putDown)` → ЯКЩО `has(robot, beacon)` and `free(front)` → ТО `place(beacon, front)`.
- КОЛИ `exec(eatUp)` → ЯКЩО `occupied(front, beacon)` → ТО `disappear_b`.
- Сенсори (чисті, без ефекту) для `left/front/right`: `xIsObstacle` ↔ `cell(x, wall)`; `xIsClear` ↔ `free(x)`; `xIsBeacon` ↔ `occupied(x, beacon)`; `xIsWhite`/`xIsBlack` ↔ `cell(x, white|black)`.
- `flipCoin()` ↔ `prob(0.5)` — випадкова гілка (блукання, обхід «на щастя»).
- Потік: `repeat(n){}`, `repeat{}` (вічно), `repeatWhile(cond){}`, `break`, `if(cond){} else{}`, `procedure name(params){}` з рекурсією, `return(expr)` (`custom: «процедура повертає значення, за замовчуванням 0»`), змінні `x = …`, оператори `not and or`, `== ~= < <= > >=`, `+ − * /` (цілі).
- КОЛИ `exec(end)` → ТО `custom: «зупинити всю програму»`.
- КОЛИ `custom: «синтаксична помилка»` → ТО `crash` ще до запуску, повідомлення на полях редактора.
- КОЛИ `program_end` → ТО `custom: «автоперевірки цілі нема — гравець сам дивиться, чи досягнуто задачу (Desktop)»` (?).
- Перемога: задача карти виконана (пляма знайдена, лінія пройдена, маяк узято) · Поразка: нема; помилка чи нескінченний цикл — правиш скрипт · Рахунок: нема (Desktop).

## Керування і ввід
- Ввід — текст скрипта в редакторі з підсвіткою, автодоповненням (Ctrl+Space), номерами рядків, необмеженим undo, пошуком/заміною з regex.
- Ключові слова локалізовані: та сама мова доступна ~22 мовами (укр. теж), скрипт пишеш рідною.
- Запуск одним кліком без компіляції; слайдер швидкості; покрокове виконання; стрілка біля рядка, що виконується.
- Пульт ручного керування (remote control) — рух робота кнопками без скрипта (?).
- Карта: перетягування мишею, зум, знімок екрана в JPG.

## Вікна, меню, HUD
- `game-screen` = редактор скрипта (ліворуч) + монітор карти (праворуч) + панель запуску (Run / Pause / Stop (?) / Step, `speed-slider`) + рядок повідомлень унизу.
- HUD: `instruction-highlight` (стрілка поточної команди), позначки помилок на полях, `zoom-control`, `camera-follow`.
- `level-select`: «Відкрити карту» — вибір `.map` зі збірки (default, findSpot, maze, open area…).
- `editor-window`: редактор карт (окремий інструмент з меню Robo).
- `settings-window`: мова інтерфейсу й ключових слів, скін, тека для знімків.
- `help-window`: вбудована документація команд.
- Переходи: відкрити карту → написати скрипт → Run → спостерігати → правити.

## Фічі поза полем
- `level-editor` — свої карти, обмін файлами `.map` (`level-sharing`).
- `step-mode`, `speed-control`.
- `real-robot-export` — експорт скрипта на LEGO Mindstorms NXT (з v4.0), EV3 і Sparki.
- `localized-keywords` — переклад усіх ключових слів мови.
- `theme-select` — скіни монітора.
- RoboMind Academy — онлайн-курси з учительським кабінетом і змаганнями (окремий продукт).

## Варіації й родичі
- Прямий предок — [karel](karel.md) (сенсори з трьох боків, процедури, «стан світу» як ціль); RoboMind додає фарбу як памʼять і `flipCoin`.
- [kara](kara.md) — теж з «листками» як памʼяттю, але програма — автомат; [robot-turtles](robot-turtles.md) і Logo-черепаха — пензель-слід як у RoboMind.
- [lightbot](lightbot.md) — «увімкнути світло» на клітині як аналог фарби-цілі.
- Осі варіацій: **памʼять у світі** (біпери / фарба / листки / нічого); **сенсори** (лише фронт / три сторони / колір); **детермінізм** (без випадковості / `flipCoin`); **мова** (свій мінімум / Python / блоки); **реальний робот** (лише симуляція / експорт на LEGO).

## Цікавинки для курсу
- Пензель як стан робота + слід фарби на клітинах, який робот сам же читає сенсорами — 📎.
- Line follower: сенсори кольору ліворуч/попереду/праворуч і рекурсивна процедура `follow()` — 🥉.
- Інтерпретатор ROBO з `repeat/repeatWhile/if/procedure/return` і змінними — 🥇.
- Локалізація ключових слів мови (таблиця синонімів на кожну мову) — 📎.
- `flipCoin` і випадкове блукання до цілі — 🌱.
- Експорт тієї ж програми в інший «рантайм» (симуляція → справжній робот) — 🥈.

## Мапа на каталог
- Є: `command-program` · `user-procedures` · `sensor-predicates` · `step-execution` · `code-editor-window` · `impassable-cells` · `item-pickup` (маяк) · `visited-trail` (слід фарби) · `reach-exit` (дійти до плями/маяка) · `in-game-editor` (редактор карт) · `level-select` · `game-screen` · `help-window` · `settings-window`.
- **Нема** → пропозиції карток:
  - `+runtime-error-stop` (вже пропоновано в Karel).
  - `+paint-trail-brush` «Пензель: робот лишає слід кольором, поки пензель опущено» · entities/move · 📎.
  - `+color-sensors` «Сенсори кольору сусідніх клітин» · game-logic/program · 📎.
  - `+coin-flip-predicate` «Випадкова умова в програмі» · game-logic/program · 🌱.
  - `+real-robot-export` «Експорт програми на фізичного робота» · code/architecture · 🥈.
  - `+localized-keywords` «Ключові слова мови кількома мовами» · interface/input · 📎.
  - `+camera-follow-robot` «Камера стежить за актором, карта тягається мишею» · interface/render · 🌱.

## Пропозиції до словників
- `+feature:real-robot-export` — перенести програму з симуляції на реальний пристрій (LEGO NXT/EV3, Sparki).
- `+feature:localized-keywords` — мова програмування з перекладеними ключовими словами.
- `+ui:remote-control-pad` — панель ручного керування роботом поза програмою.
- `+ui:camera-follow` — перемикач «камера стежить за роботом».
- `+cond:returns(value)` — умова як значення процедури користувача (`return(true)`), ширше за сенсор.

## Джерела
- ⭐ [RoboMind: Basic instructions](https://www.robomind.net/en/docBasicInstructions.htm) — forward/backward/left/right/north…west, paintWhite/paintBlack/stopPainting, pickUp/putDown/eatUp, 15 сенсорів «бачити», flipCoin 50/50.
- [RoboMind: Programming structures](https://www.robomind.net/en/docProgrammingStructures.htm) — repeat, repeatWhile, break, if/else, procedure, return, рекурсія, змінні, оператори, цілочисельне ділення.
- [RoboMind: Example programs](https://www.robomind.net/en/docExamples.htm) — написати літеру, знайти білу пляму, line follower (рекурсивно), лабіринт за правою рукою до маяка.
- [RoboMind: Development environment](https://www.robomind.net/en/robomind.htm) — редактор з автодоповненням і undo, монітор із зумом і стеженням, слайдер швидкості, покроково, стрілка поточного рядка.
- [Wikipedia: RoboMind](https://en.wikipedia.org/wiki/RoboMind) — 2005, Arvid Halma (UvA), Research Kitchen з 2011, v4.0 LEGO NXT, v5.0 змінні й функції, 22 мови.
- [RoboMind](https://www.robomind.net/) — Academy (онлайн) і Desktop (v7.0, Windows/Mac/Linux).
- YouTube: пошук «robomind programming robot».

## Непевне
- (?) Що саме стається при `forward` у стіну — лише зупинка кроку чи помилка виконання; документація каже тільки, що повертається кількість кроків «до удару».
- (?) Чи маяк є перешкодою для руху і чи робот може нести більше одного.
- (?) Ручний пульт (remote control), кнопки Pause/Stop і окремий редактор карт — бачив лише посилання «Map editor», деталі з памʼяті.
- (?) Автоперевірки цілі в Desktop нема (з памʼяті); в Academy завдання, імовірно, перевіряються автоматично.
- (?) Актуальна версія: Wikipedia — 5.3 (2014), сайт — 7.0 (© 2005–2016).
