---
title: Cubetto
slug: cubetto
aka: [Cubetto Playset, Cubetto+, Primo]
family: program-robots
also: [board-digital]
klass: avatar
axes:
  field: square
  time: programmed
  opponent: none
  info: full
  random: runtime
  goal: state
year: 2016
platforms: [toy (деревʼяний робот + дошка)]
links:
  - {kind: official, url: "https://primotoys.com/cubetto-user-manual/", best: true, note: "інструкція: дошка 12 + 4 слоти, LED, кнопка, крок 15 см, поворот 90°, порожній слот, карта 6×6"}
  - {kind: official, url: "https://www.primotoys.com/", note: "Primo Toys: Cubetto+ і Cubetto, блоки Forward, Left, Right, Function, Backward, Negation, Random"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Primo_Toys", note: "історія: прототип Primo (2012), Kickstarter-и, вік 3+, тональні звуки для незрячих"}
  - {kind: other, url: "https://primotoys.com/shop/cubetto-plus-playset/", note: "Cubetto+: 24 блоки, 18 кроків + 4 функції, програма зліва направо"}
  - {kind: other, url: "https://primotoys.com/shop/logic-blocks/", note: "Logic Blocks: 4× Negation, 4× Random, 4× Function"}
  - {kind: other, url: "https://www.primotoys.com/faq/", note: "FAQ: вік 3–6, офлайн, Bluetooth-пара, групи 3–4, поняття курсу"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=cubetto+coding+robot", note: "пошук; як діти програмують робота"}
stage: v1
coverage: 55
mechanics: [command-program, user-procedures, step-execution, drag-drop-piece, sound-effects, reach-exit, game-screen, +relative-turn-controls, +command-slots-limit, +recursion-loop, +tangible-program-board, +empty-slot-terminates, +random-command-block, +negation-block, +audio-cue-per-command, +device-pairing]
proposes: ["+window:program-board", "+feature:tangible-programming", "+feature:audio-cues", "+feature:device-pairing", "+axis:control", "+card:tangible-program-board"]
author: opus
date: 2026-11-19
---

# Cubetto — деревʼяний робот для дошкільнят: програма — кольорові бруски в слотах дошки, кнопка — і робот їде картою

## Суть
Дитина 3–6 років складає програму з деревʼяних брусків у слотах дошки (Interface Board): зелений — уперед, жовтий — ліворуч, червоний — праворуч, синій — виклик функції. Кнопка надсилає програму бездротово, і Cubetto виконує команди по одній на тканинній карті з клітинами 15 см, а під поточним слотом блимає світлодіод і грає мелодія.

Екрана нема зовсім: програма — фізичний ряд брусків, функція — окремий короткий ряд на тій самій дошці, налагодження — порівняти шлях робота з задумом. Набір розширюють блоками Backward, Negation і Random, картами-пригодами й книжками; натхнення — Logo Сеймура Пейперта й Монтессорі.

## Поле і час
- Карта Cubetto's World — 1 × 1 м, сітка 6×6 клітин по 15 см; крок робота = одна клітина. Є карти-пригоди (Ancient Egypt, Big City, Blue Ocean, Deep Space) і прозора карта з кишенями для карток-літер і цифр.
- Робот має напрямок і повертає на місці на 90°; кут повороту в кожного робота трохи свій — виробник вважає це нормою.
- Дошка оригінального Cubetto: 12 слотів основної послідовності, зʼєднаних вигравіюваною «ниткою» від лівого верхнього, + 4 слоти функційної лінії; під кожним слотом — LED. Cubetto+: 18 кроків + 4 функції, черга зліва направо.
- Час `programmed`: спершу вся програма, потім кнопка; зміни на дошці під час виконання не діють.
- Карта — лише малюнок: стін і меж робот фізично не бачить (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Cubetto | player | напрямок; крок 15 см | виконує команди з дошки по одній; мелодія після кожної, довша — в кінці програми |
| Дошка (Interface Board) | container | 12 + 4 слоти (Cubetto+: 18 + 4); LED під слотом; кнопка | зчитує бруски (у V2 — магніти й датчики Холла) і надсилає програму роботу |
| Блок Forward (зелений) | supply | — | крок уперед на 15 см |
| Блок Left (жовтий) | supply | — | поворот на 90° проти годинникової |
| Блок Right (червоний) | supply | — | поворот на 90° за годинниковою |
| Блок Function (синій) | supply | — | виконати функційну лінію |
| Блок Backward | supply | у наборі Direction Blocks (?) | крок назад (?) |
| Блок Negation | supply | 4 у наборі Logic Blocks | «заперечення» наступної дії (?) |
| Блок Random | supply | 4 у наборі Logic Blocks | випадкова дія (?) |
| Порожній слот | — | — | блоки після нього не розпізнаються й не виконуються |
| Карта | terrain | 6×6, тематичні малюнки | орієнтири для завдань та історій; власних правил не має |
| Кнопка дії | switch | — | старт програми; також спарювання з роботом |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(go)` → ТО `custom: «дошка зчитує слоти вздовж нитки й надсилає програму роботу»`.
- КОЛИ `custom: «бруски переставили під час виконання»` → ТО `custom: «нічого — діє вже надіслана програма»`.
- КОЛИ `exec(slot)` → ЯКЩО `custom: «слот порожній»` → ТО `custom: «кінець програми: блоки далі не виконуються»`.
- КОЛИ `exec(forward)` → ТО `move(cubetto, forward)` — 15 см, одна клітина.
- КОЛИ `exec(left)` → ТО `rotate(cubetto, -90)`.
- КОЛИ `exec(right)` → ТО `rotate(cubetto, 90)`.
- КОЛИ `exec(function)` → ТО `custom: «виконати слоти функційної лінії й повернутись у головну послідовність»`.
- КОЛИ `exec(function)` → ЯКЩО `custom: «синій блок стоїть і в самій функційній лінії»` → ТО `custom: «рекурсія — повтор без кінця (?)»`.
- КОЛИ `exec(block)` → ТО `custom: «LED під слотом блимає»`, `sound(«мелодія команди»)`.
- КОЛИ `program_end` → ТО `sound(«довша фінальна мелодія»)`.
- КОЛИ `exec(backward)` → ТО `move(cubetto, back)` (?).
- КОЛИ `exec(random)` → ТО `custom: «випадкова дія (?)»`.
- КОЛИ `exec(negation)` → ТО `custom: «протилежна дія (?)»`.
- КОЛИ `input(pair)` → ЯКЩО `custom: «спершу ввімкнено дошку, потім робота; у першому слоті блок напрямку»` → ТО `custom: «пара тримається, доки обидва ввімкнені»`.
- Кілька роботів у класі спаровують з дошками по одному; робот слухає найближчу дошку.
- Перемоги й поразки в наборі нема: мету задає дорослий, карта чи книжка (довезти до клітини, обминути малюнок-перешкоду); помилку видно одразу — робот приїхав не туди.

## Керування і ввід
- Дитина вставляє бруски в слоти вздовж нитки (оригінал — змійкою від лівого верхнього слота, Cubetto+ — зліва направо); функція — окремий короткий ряд.
- Кнопка дії — запуск; нову програму можна запустити лише після кінця попередньої.
- Налагодження: побачити, де робот збився, переставити брусок, запустити знову (FAQ: «debugging»).
- Гра в парах або групах 3–4 дітей на одного робота; бездротовий звʼязок дошки й робота — до ≈10 м у приміщенні.

## Вікна, меню, HUD
(цифрова версія — так виглядав би Cubetto на екрані)
- `game-screen`: карта 6×6 з роботом і стрілкою напрямку; дошка-програма — 12 (18) слотів + 4 функції; `instruction-highlight` — «LED» поточного слота; кнопка Go.
- `tool-palette`: запас брусків чотирьох кольорів (+ Backward, Negation, Random) для перетягування в слоти.
- `level-select` — вибір карти-пригоди й історії; `end-screen` — «доїхав / не туди».
- Звук: мелодія кожної команди й фінальна; тональні звуки допомагають незрячим дітям.
- Переходи: вибір карти → складання програми → Go → виконання → правка програми.

## Фічі поза полем
- Розширення: Logic Blocks (4 Negation, 4 Random, 4 Function), Direction Blocks, чотири карти-пригоди з книжками, Logic Pack (книжки й флеш-картки), прозора карта з картками літер і цифр.
- Освіта: уроки для 4–5 і 5–6 років (по 4 юніти), Coding Guide і Teaching Guides; поняття за FAQ — algorithms, the queue, debugging, recursions.
- Доступність: тональні звуки команд роблять набір придатним для незрячих учнів (Вікіпедія).
- Усе працює офлайн; Cubetto+ — акумулятор USB-C (≈2 год робот, ≈10 год дошка), оригінал — батарейки AA.

## Варіації й родичі
- Primo (прототип Matteo Loglio, 2012) → перший Kickstarter (£56 666, 651 бекер) → Cubetto Playset (Kickstarter 8 березня 2016, $1 596 457 від 6553 бекерів) → Cubetto+ (18 кроків, зліва направо, USB-C).
- Родичі в корпусі: [Robot Turtles](robot-turtles.md) (карти-команди, виконавець — дорослий; Function Frog ≈ синій блок), [Lightbot](lightbot.md) (процедури й рекурсія), [Robot Karol](robot-karol.md), [Karel](karel.md), [RoboRally](roborally.md).
- **Осі варіацій**: носій програми (бруски в слотах / карти / екран) · виконавець (робот / людина / спрайт) · довжина черги (12 / 18) і функції (4) · рух (абсолютні напрямки / відносні «крок + поворот») · логіка (нема / Negation і Random) · зворотний звʼязок (LED + мелодія / лише рух).

## Цікавинки для курсу
- Дошка-черга з обмеженою кількістю слотів і функційною лінією; виконання до першого порожнього слота — 🌱.
- Відносний рух «крок + поворот на 90°» з напрямком робота на сітці 6×6 — 🌱.
- Виклик функції з поверненням і захист від нескінченної рекурсії (синій блок у самій функції) — 📎.
- Підсвітка поточного слота + звук на кожну команду як покрокова візуалізація — 📎.
- Блоки Random і Negation як «логічні» модифікатори — 📎 (семантику треба обрати й описати самому).
- Карта-пригода із завданням «довези до клітини» й перевіркою кінцевої позиції — 🌱.

## Мапа на каталог
- Є: `command-program` ↔ ряд брусків; `user-procedures` ↔ функційна лінія; `step-execution` ↔ LED поточного слота; `drag-drop-piece` ↔ цифровий аналог вставляння брусків; `sound-effects` ↔ мелодії команд; `reach-exit` ↔ завдання «доїхати до місця»; `game-screen`.
- **Нема** → пропозиції карток:
  - `+tangible-program-board` «Програма з фізичних блоків у слотах дошки» · game-logic/program · 📎.
  - `+empty-slot-terminates` «Програма закінчується на першому порожньому слоті» · game-logic/program · 🌱.
  - `+random-command-block` «Блок випадкової дії» · game-logic/program · 🌱 (?).
  - `+negation-block` «Блок-заперечення наступної дії» · game-logic/program · 🌱 (?).
  - `+audio-cue-per-command` «Звук на кожну команду (доступність)» · interface/sound · 🌱.
  - `+device-pairing` «Спарювання виконавця з пультом» · interface/settings · 🌱.
  - Уже пропоновані іншими: `+relative-turn-controls`, `+command-slots-limit`, `+recursion-loop`.

## Пропозиції до словників
- `+window:program-board` — дошка-черга зі слотами й функційною лінією.
- `+feature:tangible-programming` — програма складається з фізичних предметів.
- `+feature:audio-cues` — звук на кожну команду як засіб доступності.
- `+feature:device-pairing` — спарювання робота з дошкою (клас із кількома роботами).
- `+axis:control` — `programmed`: уся програма наперед, потім кнопка.
- `+card:tangible-program-board`.

## Джерела
- ⭐ [Cubetto User Manual](https://primotoys.com/cubetto-user-manual/) — 12 + 4 слоти, LED, кнопка дії, Forward 15 см, Left / Right 90°, Function, порожній слот, спарювання, карта 1 × 1 м 6×6.
- [Primo Toys](https://www.primotoys.com/) — Cubetto+ і Cubetto, кольори блоків, перелік Backward, Negation, Random, «Hit the blue button».
- [Wikipedia: Primo Toys](https://en.wikipedia.org/wiki/Primo_Toys) — засновники, прототип Primo, обидва Kickstarter-и, нагороди, натхнення (Монтессорі, Logo), звуки для незрячих.
- [Cubetto+ Playset](https://primotoys.com/shop/cubetto-plus-playset/) — 24 блоки, 18 + 4 кроки, програма зліва направо.
- [Logic Blocks](https://primotoys.com/shop/logic-blocks/) — 4× Negation, 4× Random, 4× Function.
- [FAQ](https://www.primotoys.com/faq/) — вік 3–6, офлайн, Bluetooth, групи 3–4, поняття курсу, кут повороту.
- [Learning in Hand: Cubetto](https://learninginhand.com/blog/cubetto) — карта з 36 клітин, 16 блоків у наборі, 4 слоти функції праворуч.
- [Experiential Learning of Robotics: Cubetto](https://davidrihtarsic.github.io/Experiental_Learning_of_Robotics/Learning_Activities/Early_Robotics/Cubetto/00_CUBETTO_INTRO_AND_SETUP.html) — V1: 16 місць (12 програма + 4 підпрограма); V2: блоки з магнітами, три датчики Холла під кожним місцем.
- YouTube: пошук «cubetto coding robot».

## Непевне
- (?) Що саме роблять Negation і Random: офіційні сторінки лише називають блоки; «протилежна» й «випадкова» дія — здогад з назв.
- (?) Блок Backward: колір (фіолетовий — з видачі пошуку, сторінку не відкривав) і в якому наборі він іде.
- (?) Синій блок у самій функційній лінії: нескінченна рекурсія чи інша поведінка — FAQ лише згадує «recursions».
- (?) Живлення оригіналу: інструкція пише 3 AA на кожен пристрій, FAQ — 6 AA для робота.
- (?) Рік першого Kickstarter (Primo) стаття не називає; у шапці — Kickstarter Cubetto Playset (2016).
- (?) Чи є офіційна екранна версія (застосунок) — не знайшов; вікна вище — уявна цифрова версія.
