---
title: Turing Tumble
slug: turing-tumble
aka: [TT, Тюрінг Тамбл]
family: program-robots
also: [connect-rotate, board-digital]
klass: cursor
axes:
  field: square
  time: programmed
  opponent: none
  info: full
  random: none
  goal: state
year: 2017
platforms: [board, web]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Turing_Tumble", best: true, note: "що це, деталі (рампа, кросовер, біт, перехоплювач, гір-біт, шестерня), 60 задач у коміксі, P/PSPACE-повнота, Тюрінг-повнота"}
  - {kind: other, url: "https://upperstory.com/turingtumble/assets/educator-guide-english.pdf", note: "Educator's Guide 2.8: як працює дошка (важелі внизу → кулька згори), 6 видів деталей, формат задачі, правило «кулька не падає вільно», задачі 1–30"}
  - {kind: other, url: "https://upperstory.com/turingtumble/assets/practice-guide-2021.pdf", note: "Practice Guide: 30 додаткових практичних задач з цілями й required output"}
  - {kind: other, url: "https://arxiv.org/abs/2110.09343", note: "L. Pitt, «Turing Tumble is Turing-Complete»: точна поведінка кожної деталі, тригер/бункер, гаджети read / write-0 / write-1 на гір-бітах"}
  - {kind: play, url: "https://jessecrossen.github.io/ttsim/", note: "симулятор Jesse Crossen: фізика matter.js, розміри дошки, стан у URL, турнікет і бункери будь-де"}
  - {kind: other, url: "https://jessecrossen.github.io/ttsim/usage", note: "довідка симулятора: усі інструменти й дії"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Turing+Tumble+puzzle", note: "пошук; розвʼязки задач"}
stage: v1
coverage: 65
mechanics: [gravity-fall, cell-click, drag-drop-piece, button-toggle, sequential-levels, level-unlock, level-bank, tutorial-window, game-screen, field-scaling, state-string, restart-level, +marble-logic-board, +bit-toggle-on-pass, +gear-linked-bits, +ramp-direction-piece, +crossover-piece, +interceptor-halt, +trigger-hopper-loop, +required-output-sequence, +starting-setup-and-parts, +part-unlock-progression, +no-free-fall-rule, +fewer-parts-challenge, +schematic-physical-view]
proposes: ["+role:token", "+effect:release(hopper)", "+trigger:reach_bottom(a)", "+cond:part_budget(kind, n)", "+window:puzzle-card", "+ui:output-tray", "+feature:part-budget", "+axis:signal"]
author: opus
date: 2026-11-09
---

# Turing Tumble — механічний компʼютер на кульках: рампи, біти й шестерні на похилій дошці, а кулька внизу запускає наступну

## Суть
Настільна іграшка-головоломка Paul і Alyssa Boswell (навіяна Digi-Comp II): на похилу дошку з кілочками гравець чіпляє деталі — рампи, кросовери, біти, гір-біти з шестернями, перехоплювач. Згори по одній скочуються сині й червоні кульки; дійшовши донизу, кулька натискає лівий або правий важіль і цим випускає наступну синю або червону. Задача з книжки-коміксу (60 штук, інженерка Alia на безлюдній планеті) задає стартову розстановку, набір доступних деталей і потрібну послідовність кольорів на виході — гравець «програмує» розстановкою, потім запускає й не торкається. Біти зберігають стан, гір-біти звʼязують кілька бітів — звідси лічильники, суматори і Тюрінг-повнота на нескінченній дошці.

## Поле і час
- Похила дошка-сітка з кілочками; деталь висить на кілочку й займає позицію сітки, кулька з деталі переходить по діагоналі вниз-ліворуч або вниз-праворуч на наступну деталь.
- Згори — два бункери: лівий з синіми, правий з червоними кульками; знизу — два важелі (тригери), повʼязані з бункерами через задню частину дошки; нижче — лоток виходу, де кульки лягають по порядку.
- Деякі позиції особливі: спеціальні кілочки для шестерень (?) — шестерня може стояти на будь-якій клітині (у симуляторі).
- Час `programmed`: розстановка → натиснути старт (випускає першу кульку) → машина працює сама, доки кулька не впіймана перехоплювачем або не закінчились кульки. В один момент на дошці одна кулька.
- Детерміновано; цифрові симулятори мають більші дошки й режим «схема».

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Синя / червона кулька | object | колір | падає згори, котиться деталями, внизу натискає важіль |
| Бункер (ball drop) | spawner | колір, запас кульок | випускає одну кульку на сигнал важеля |
| Важіль (trigger) | switch | лівий → синій, правий → червоний | кулька натискає → бункер випускає наступну |
| Кнопка старту | switch | — | випускає першу кульку (зазвичай синю) |
| Рампа | conduit | напрям вправо/вліво, противага | приймає кульку з будь-якого боку, скидає в один бік; повертається у вихідне положення |
| Кросовер | conduit | — | з лівого верху → у правий низ, з правого верху → у лівий низ; «міст» для перетину шляхів |
| Біт | switch | стан 0 (вліво) / 1 (вправо) | кулька проходить і **перемикає** біт; вихід — у бік нового стану |
| Гір-біт | switch | стан 0/1, звʼязок із шестернями | як біт, але повертає всі зчеплені гір-біти разом |
| Шестерня | conduit | — | з кульками не взаємодіє; передає поворот між гір-бітами |
| Перехоплювач | sink | — | ловить кульку — машина зупиняється («обчислення завершено») |
| Лоток виходу | sink | — | збирає кульки в порядку надходження; порівнюється з required output |
| Порожнє місце (без деталі) | static | — | кулька не повинна падати вільно — це заборонено правилами |
| Турнікет (симулятор) | switch | колір найближчого бункера | ttsim: тригер, який можна поставити будь-де |
| Стінка / схил (симулятор) | static | ліво/право; лінія до 6 | ttsim: блокує горизонтальний рух / веде кульку вбік |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(place, part)` → ЯКЩО `custom: «деталь є в Available parts задачі»` → ТО `place(player, part)` на кілочок; стартові деталі задачі вже стоять.
- КОЛИ `input(start)` → ТО `spawn_at(blue_ball, left_hopper)` (зазвичай синя; задача може починати з червоної).
- КОЛИ `tick` → ТО `fall(ball)` на деталь під нею; `custom: «кулька має одразу потрапити на наступну деталь — вільне падіння заборонене»`.
- КОЛИ `enter(ball, ramp)` → ТО `move(ball, ramp_dir)` (вниз-праворуч або вниз-ліворуч); рампа повертається противагою.
- КОЛИ `enter(ball, crossover)` → ЯКЩО `moving(ball, right)` → ТО `move(ball, down_right)`; ЯКЩО `moving(ball, left)` → ТО `move(ball, down_left)`.
- КОЛИ `enter(ball, bit)` → ЯКЩО `state(bit, 0)` → ТО `set_state(bit, 1)`, `move(ball, down_right)`; ЯКЩО `state(bit, 1)` → ТО `set_state(bit, 0)`, `move(ball, down_left)`.
- КОЛИ `enter(ball, gear_bit)` → ТО як біт, і `custom: «усі гір-біти, зчеплені шестернями, стають у той самий стан»`.
- КОЛИ `enter(ball, interceptor)` → ТО `custom: «кулька зупиняється»`, `game_over` (машина стоїть).
- КОЛИ `reach(ball, bottom)` → ТО `custom: «кулька лягає в лоток»`; ЯКЩО `custom: «натиснуто лівий важіль»` → ТО `spawn_at(blue_ball, left_hopper)`; ЯКЩО правий → ТО `spawn_at(red_ball, right_hopper)`.
- КОЛИ `custom: «бункер порожній»` → ТО `custom: «нова кулька не випадає — машина зупиняється»`.
- КОЛИ `custom: «машина зупинилась»` → ЯКЩО `custom: «послідовність у лотку = required output (напр. синя-червона-синя-червона…, 8 синіх)»` → ТО `win`; інакше — `restart` з іншою розстановкою.
- КОЛИ `custom: «машина в русі»` → ТО `custom: «гравець не торкається дошки»` (аварійна зупинка — підняти важелі).
- КОЛИ `custom: «задача розвʼязана меншою кількістю деталей, ніж у Available parts»` → ТО `custom: «додатковий виклик (challenge)»`.
- КОЛИ `custom: «пройдено кілька задач»` → ТО `unlock(new_part)` (напр. кросовер після 4-ї задачі).
- Перемога: лоток збігається з required output або біти в потрібному стані (?) · Поразка: нема (переставляєш) · Рахунок: нема; «менше деталей» — неформальний виклик.

## Керування і ввід
- Фізично: повісити деталь на кілочок (рампи — оборотні, напрям обираєш, вішаючи); задати початковий стан біта; натиснути кнопку старту; не торкатись до зупинки.
- Симулятор ttsim: інструмент «рука» (клік — перевернути/повернути, drag — перенести деталь чи кульку, Ctrl+drag — панорама, тягнути край — розмір дошки), гумка, палітра деталей (рампа, кросовер, перехоплювач, біт, гір-біт, шестерня, кулька, бункер, турнікет, стінка, схил).
- Дії ttsim: схема/фізика, зум, швидкість, «повернути кульки», очистити, шухляда рідких дій.

## Вікна, меню, HUD
- Книжка (паперова): сторінка задачі (`puzzle-card` custom) — Objective, Required output (кольорові кульки з кількостями), Starting setup, Available parts; комікс між задачами; уроки «Computer Logic Lesson» у посібнику вчителя.
- (цифрова версія, ttsim) `game-screen`: дошка + панель інструментів; кнопки розміру дошки (мала/середня/велика), завантаження/вивантаження PNG (піксель = деталь), стан у URL.
- (цифрова версія, Tumble Together) `level-select` перших 30 задач, спільні кімнати для дистанційної роботи (?).
- HUD: кількість кульок у бункері (наведення на бункер у ttsim); `output-tray` (custom) — лоток з порядком кольорів.
- Переходи (цифрова): вибір задачі → дошка з розстановкою → запуск → перевірка лотка → наступна задача.

## Фічі поза полем
- 60 задач у книжці-коміксі з поступовим відкриттям деталей; Practice Guide — ще 30 практичних між основними; Educator's Guide з розборами 1–30.
- Неформальні виклики: розвʼязати меншою кількістю деталей.
- Симулятори: Tumble Together (Rich Twilton, 30 задач, кімнати), ttsim (Jesse Crossen, фізика, великі дошки, обмін через URL/PNG), js-tumble (Lode Vandevenne).
- Спільнота Turing Tumble Community — свої задачі й конструкції.

## Варіації й родичі
- Предки: Digi-Comp II (1960-ті), Dr. Nim — кулькові компʼютери з бітами-перемикачами.
- Корпус: [marble-drop](../connect-rotate/marble-drop.md) і [gravitrax](../connect-rotate/gravitrax.md) (маршрутизація кульок), [manufactoria](manufactoria.md) (обробка стрічки), [kohctpyktop](kohctpyktop.md) і [turing-complete](turing-complete.md) (від ключів до процесора), [compressure](compressure.md) (аналоговий аналог «логіки на потоці»).
- Осі варіацій: **запуск** (кулька внизу запускає наступну — тригер / усі кульки разом); **памʼять** (біт, що перемикається читанням / гір-біти з неруйнівним читанням); **межі** (фізична дошка й запас деталей / нескінченна дошка — Тюрінг-повнота); **оцінка** (послідовність на виході / стан бітів).

## Цікавинки для курсу
- Біт, що перемикається кожною кулькою, + рампи як «дроти» — 🥉 (лічильник/дільник частоти).
- Гір-біти, зчеплені шестернями: неруйнівне читання, write-0 / write-1 з гаджета з трьох гір-бітів — 🥈.
- Тригер-бункер як цикл: результат унизу керує тим, що випаде згори — 🥉.
- Формат задачі «стартова розстановка + доступні деталі + required output» і перевірка лотка — 📎.
- Симулятор дошки: падіння по діагоналі, стани деталей, лоток — 🥉; з фізикою (matter.js) — 🥈.
- Доведення Тюрінг-повноти на нескінченній дошці (Pitt 2021) — 👑.

## Мапа на каталог
- Є: `gravity-fall` (кульки падають) · `cell-click` / `drag-drop-piece` (розстановка в симуляторі) · `button-toggle` (біт/гір-біт як перемикач стану) · `sequential-levels` / `level-unlock` / `level-bank` (книжка задач) · `tutorial-window` (уроки) · `game-screen` · `field-scaling` (розміри дошки ttsim) · `state-string` (стан у URL) · `restart-level`.
- **Нема** → пропозиції карток:
  - `+marble-logic-board` «Кулькова логіка на похилій дошці» · game-logic/program · 🥈.
  - `+bit-toggle-on-pass` «Біт перемикається кожним проходом» · entities/state · 📎; `+gear-linked-bits` «Зчеплені біти одного стану» · entities/state · 🥉.
  - `+ramp-direction-piece` · `+crossover-piece` · `+interceptor-halt` — деталі маршруту й зупинки · entities/interact · 🌱 кожна.
  - `+trigger-hopper-loop` «Вихід унизу запускає наступну кульку згори» · game-logic/program · 🥉.
  - `+required-output-sequence` «Ціль — послідовність кольорів на виході» · game-logic/win · 📎; `+starting-setup-and-parts` «Стартова розстановка й запас деталей» · levels/format · 📎.
  - `+part-unlock-progression` · levels/progression · 🌱; `+no-free-fall-rule` · entities/legality · 🌱; `+fewer-parts-challenge` · game-logic/score · 🌱; `+schematic-physical-view` · interface/render · 📎.

## Пропозиції до словників
- `+role:token` — кулька/токен як носій даних у машині (≠ `object`).
- `+effect:release(hopper)` — випустити наступну одиницю із запасу (бункер кульок).
- `+trigger:reach_bottom(a)` — дійшов до низу дошки (окремо від загального `reach`, бо запускає цикл).
- `+cond:part_budget(kind, n)` — у запасі задачі лишилось ≥ n деталей виду.
- `+window:puzzle-card` — сторінка задачі: ціль, required output, стартова розстановка, доступні деталі.
- `+ui:output-tray` — лоток з порядком результатів.
- `+feature:part-budget` — обмежений набір деталей на задачу.
- `+axis:signal` — тут `bit` (механічний).

## Джерела
- ⭐ [Wikipedia: Turing Tumble](https://en.wikipedia.org/wiki/Turing_Tumble) — деталі, 60 задач, Boswell, Digi-Comp II, P/PSPACE, Тюрінг-повнота, нагороди.
- [Educator's Guide 2.8 (PDF)](https://upperstory.com/turingtumble/assets/educator-guide-english.pdf) — механіка дошки й важелів, 6 видів деталей, формат задачі, правила запуску, симулятори.
- [Practice Guide (PDF)](https://upperstory.com/turingtumble/assets/practice-guide-2021.pdf) — цілі практичних задач («Release one blue ball and then all of the red balls», «blue, red, blue, red…»).
- [arXiv 2110.09343 — L. Pitt](https://arxiv.org/abs/2110.09343) — формальний опис деталей і гаджетів, тригер/бункер.
- [ttsim](https://jessecrossen.github.io/ttsim/) + [довідка](https://jessecrossen.github.io/ttsim/usage) — цифрова версія; README репо jessecrossen/ttsim.
- YouTube: пошук «Turing Tumble puzzle».

## Непевне
- (?) Рік: Wikipedia відносить до 2017 (Kickstarter), стаття Pitt — «introduced in 2018»; у черзі 2017.
- (?) Склад коробки (20 синіх + 20 червоних кульок, 30 рамп, 3 перехоплювачі) — лише зі сніпета пошуку, сторінку не відкривав.
- (?) Чи бувають у книжці задачі з ціллю «стан бітів», а не послідовність кульок (лічильники, двійкові числа) — у посібнику бачив лише задачі 1–30.
- (?) Геометрія кілочків (окремі позиції для шестерень у фізичній дошці) — не перевірено; у ttsim шестерня ставиться будь-де.
- (?) Офіційний сайт (upperstory.com/turingtumble) агенту віддав 403 — у шапку не кладу.
