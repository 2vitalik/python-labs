---
title: Robot Turtles
slug: robot-turtles
aka: []
family: program-robots
also: [board-digital]
klass: avatar
axes:
  field: square
  time: turn
  opponent: hotseat
  info: full
  random: none
  goal: state
year: 2013
platforms: [board]
links:
  - {kind: other, url: "https://ultraboardgames.com/robot-turtles/game-rules.php", best: true, note: "повні правила: карти, плитки, 4 рівні гри, Function Frog, «Bug!»"}
  - {kind: other, url: "https://dicetower.com/board-game/147370", note: "дизайнер Dan Shapiro, 2013, ThinkFun, 2–5 гравців, 4+"}
  - {kind: other, url: "https://rulespal.com/robot-turtles/rulebook", note: "правила (з пошуку)"}
  - {kind: official, url: "https://thinkfun.com/robot-turtles/turtlemover.php", note: "ThinkFun: сторінка для дорослого Turtle Mover (з пошуку)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=robot+turtles+board+game", note: "пошук; партії й пояснення правил"}
stage: v1
coverage: 75
mechanics: [command-program, user-procedures, push-object, impassable-cells, destructible-blocks, orientation-state, reach-exit, undo-redo, undo-step, restart-level, hot-seat, turn-enforcement, in-game-editor, rule-variants, game-screen, end-screen, +card-program, +human-interpreter, +staged-rules-unlock, +program-ahead-mode, +reverse-whole-program, +own-color-target]
proposes: ["+feature:human-interpreter", "+feature:staged-rules", "+feature:program-ahead", "+ui:card-program-row", "+effect:melt(cell)", "+window:frog-program"]
author: opus
date: 2026-11-09
---

# Robot Turtles — настолка для дошкільнят: діти кладуть карти-команди, дорослий виконує їх черепашкою, щоб дійти до свого самоцвіта

## Суть
Кожна дитина («Turtle Master») має черепашку свого кольору й колоду карт: крок уперед, поворот ліворуч, поворот праворуч, лазер, Function Frog. На свій хід дитина кладе карту в ряд за попередніми — ряд карт і є **програмою**; дорослий («Turtle Mover») єдиний торкається поля й виконує карту черепашкою, зі звуками. Мета — дійти до самоцвіта свого кольору в центрі поля; виграють усі, хто дійшов. Незвичне: «процесор» — жива людина, а кнопка «Bug!» (плитка-жучок) — **undo** поточного ходу; правила відкриваються поступово (лід → лазер → камінь → ящики → програма наперед → функція).

## Поле і час
- Квадратне поле-дошка (розмір не вказано в джерелах — (?)); черепашки стартують у кутах, самоцвіти — в центрі; кожен гравець сидить зі «свого» боку.
- Клітина: порожня / стіна (камінь, лід) / калюжа / ящик / черепашка / самоцвіт.
- Час `turn`: по черзі за годинниковою стрілкою, починає наймолодший; хід = одна карта (базова гра), ~3 карти (перехідний етап) або вся програма (режим Write Program).
- Інформація повна; випадковості нема — розстановку перешкод робить дорослий.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Черепашка | player | колір, напрямок | виконує карти: крок / поворот на 90° / лазер |
| Самоцвіт | pickup | колір | ціль; лише свого кольору — «підбирає» |
| Кам'яна стіна | static | — | непрохідна, лазер не діє |
| Крижана стіна | static | — | непрохідна; лазер розтоплює → калюжа |
| Калюжа | terrain | — | прохідна; сюди можна заштовхнути ящик |
| Ящик | object | — | штовхається на 1, якщо за ним порожньо або калюжа |
| Плитка-жучок (Bug) | switch | одна на гравця | «Bug!» — скасувати свій поточний хід |
| Карта «крок» / «ліворуч» / «праворуч» | — (команда) | колір квітки | одна команда програми |
| Карта «лазер» | — (команда) | — | розтоплює крижану стіну прямо перед черепашкою |
| Карта Function Frog | — (команда) | — | виклик окремої програми-«жаби» |
| Turtle Mover (дорослий) | — (виконавець) | — | інтерпретатор: виконує карти, озвучує, відкочує |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `exec(step)` → ЯКЩО `free(front)` → ТО `move(turtle, forward)`.
- КОЛИ `exec(step)` → ЯКЩО `occupied(front, wall)` or `occupied(front, turtle)` → ТО `block`, `custom: «дорослий хитає черепашку й видає звук»` — дитина виправляє через Bug.
- КОЛИ `exec(step)` → ЯКЩО `occupied(front, crate)` and `free(behind_crate)` → ТО `push(crate)`, `move(turtle, forward)`.
- КОЛИ `exec(step)` → ЯКЩО `occupied(front, crate)` and `occupied(behind_crate, wall|crate|turtle)` → ТО `block`.
- КОЛИ `exec(step)` → ЯКЩО `occupied(front, crate)` and `custom: «за ящиком край поля»` → ТО `block` (за край штовхати не можна).
- КОЛИ `exec(step)` → ЯКЩО `occupied(front, crate)` and `occupied(behind_crate, puddle)` → ТО `push(crate)` (ящик стає на калюжу).
- КОЛИ `exec(turn_left)` / `exec(turn_right)` → ТО `face(turtle, ∓90°)` (без кроку).
- КОЛИ `exec(laser)` → ЯКЩО `occupied(front, ice_wall)` → ТО `transform(puddle)`.
- КОЛИ `exec(laser)` → ЯКЩО `not occupied(front, ice_wall)` → ТО `custom: «нічого не стається»` (камінь, самоцвіт, порожнеча).
- КОЛИ `exec(frog)` → ТО `custom: «виконати всю окрему програму-жабу»`.
- КОЛИ `enter(turtle, jewel)` → ЯКЩО `same(turtle, jewel, color)` → ТО `pickup`, `win` (для цього гравця).
- КОЛИ `input(bug)` → ЯКЩО `turn_of(self)` and `custom: «наступний гравець ще не почав хід»` → ТО `undo` (скільки завгодно разів у межах ходу).
- КОЛИ `input(run_program)` (режим Write Program) → ТО `custom: «дорослий виконує всю програму з початку, карта за картою»`.
- КОЛИ `program_end` → ЯКЩО `not custom: «черепашка на своєму самоцвіті»` → ТО `restart` — дорослий відкочує кожен рух у зворотному порядку, включно з «заморожуванням» калюж і поверненням ящиків; спроба наступного ходу.
- КОЛИ `turn_end(side)` → ТО `end_turn`.
- КОЛИ `custom: «у гравця скінчились карти виду»` → ТО `custom: «базова гра: можна повторно взяти свої вже зіграні карти; при <4 гравців — з колоди невикористаного кольору»`.
- КОЛИ `custom: «гравець дійшов»` → ТО `custom: «прибрати черепашку й самоцвіт або лишити — розтоплювати лід іншим»`.
- Перемога: черепашка на самоцвіті свого кольору; виграти можуть усі · Поразка: нема · Рахунок: у режимі Function Frog — дійти найменшою кількістю карт.

## Керування і ввід
- Дитина кладе карту-команду з руки (колода свого кольору, відкрита) в ряд-програму перед собою; поля не торкається.
- Дорослий («Turtle Mover») переносить карту в дію: рухає черепашку, озвучує; дитина може стати Mover-ом, коли добре грає; одна людина не може бути обома ролями.
- «Bug!» — торкнутися своєї плитки-жучка й крикнути; Mover скасовує хід.
- Function Frog: окремий ряд-програма жаби; кожна карта жаби в основній програмі = виконати весь ряд.

## Вікна, меню, HUD
- (цифрова версія) `main-menu`: Грати → `match-setup` (кількість гравців 1–4, які правила ввімкнено: лід, лазер, камінь, ящики, програма наперед, жаба).
- (цифрова версія) `editor-window` — розставити перешкоди на полі (оригінал заохочує власні розкладки, якщо черепашка й самоцвіт не замкнені).
- (цифрова версія) `game-screen`: поле; `card-program-row` кожного гравця; `pocket` — рука карт; `turn-indicator`; `undo-button` = Bug; кнопка «Run Program!» у режимі III.
- (цифрова версія) `frog-program` — окремий ряд для функції-жаби.
- (цифрова версія) `end-screen` — хто дійшов, кількість карт у програмі.
- Переходи: setup → гра → (усі дійшли) end-screen → нова розкладка.

## Фічі поза полем
- `staged-rules` — рівні гри: I Basic (одна карта за хід) → II Unlockables (лід → лазер → камінь → ящики, по одному) → III Write Program (спершу ~3 карти, потім уся програма й «Run Program!») → IV Function Frog.
- `undo` (Bug) необмежено в межах свого ходу; `restart-level` з повним відкотом програми в режимі III.
- `level-editor` — власні розкладки поля після вивчення всіх перешкод.
- `hotseat` на 1–4 дітей + дорослий; підтримка повільніших («їх не квапити»).
- Без змагального рахунку; режим IV додає мету «менше карт».

## Варіації й родичі
- Родичі в корпусі: [RoboRally](roborally.md) (карти-програма, але одночасно й зі зіткненнями), [Lightbot](lightbot.md) (процедура = Function Frog), [Karel](karel.md), [Block maze games](block-maze-games.md) (той самий «поворот + крок» на клітинах); фізичні програмовані іграшки-«черепахи» Logo (?).
- **Осі варіацій**: хто виконує (людина / комп'ютер) · коли виконується (після кожної карти / усю програму наперед) · відкат (undo ходу / повний реверс програми) · перешкоди (камінь / розтоплюваний лід / штовхальний ящик) · виграш (кожен свій / перший).

## Цікавинки для курсу
- Ряд карт як програма + інтерпретатор карт (крок, поворот, лазер) — 🌱.
- Ящик, що штовхається лише в порожнечу/калюжу і не за край — 🌱.
- Лазер, що перетворює крижану стіну на калюжу (`transform`) — 🌱.
- Режим «уся програма наперед» з повним реверсом усіх ефектів (undo-стек ефектів) — 🥉.
- Function Frog: виклик підпрограми й підрахунок довжини програми — 📎.
- Поступове відкривання правил (прапорці правил у налаштуванні партії) — 📎.
- Hot-seat на 4 гравців зі своїми кольорами самоцвітів — 📎.

## Мапа на каталог
- Є в каталозі: `command-program` ↔ ряд карт; `user-procedures` ↔ Function Frog; `push-object` ↔ ящики; `impassable-cells` ↔ стіни; `destructible-blocks` ↔ лід під лазером; `orientation-state` ↔ напрямок черепашки; `reach-exit` ↔ дійти до самоцвіта; `undo-redo` / `undo-step` ↔ Bug; `restart-level` ↔ реверс програми; `hot-seat`, `turn-enforcement`; `in-game-editor` ↔ власні розкладки; `rule-variants` ↔ рівні гри; `game-screen`, `end-screen`.
- **Нема** → пропозиції карток:
  - `+card-program` «Програма з карт у руці» · game-logic/program · 🌱.
  - `+human-interpreter` «Виконавець програми — інший гравець» · game-logic/opponent · 🌱 (для цифрової версії — режим «друг виконує»).
  - `+staged-rules-unlock` «Правила вмикаються поступово» · levels/progression · 📎.
  - `+program-ahead-mode` «Скласти всю програму, потім запуск» · game-logic/program · 📎.
  - `+reverse-whole-program` «Відкат усіх ефектів програми» · game-logic/history · 🥉.
  - `+own-color-target` «Кожен гравець має ціль свого кольору» · game-logic/win · 🌱.

## Пропозиції до словників
- `+feature:human-interpreter` — роль «виконавця» програми (Turtle Mover).
- `+feature:staged-rules` — відкривання правил по одному.
- `+feature:program-ahead` — перемикач «по карті / уся програма».
- `+ui:card-program-row` — ряд карт-команд гравця.
- `+effect:melt(cell)` — лазер розтоплює крижану стіну (зараз записано як `transform(puddle)`; окреме слово — якщо зустрінеться ще).
- `+window:frog-program` — окрема панель підпрограми.

## Джерела
- ⭐ [UltraBoardGames: Robot Turtles rules](https://ultraboardgames.com/robot-turtles/game-rules.php) — компоненти (20 кам'яних, 12 крижаних стін, 4 ящики), ролі, карти, Bug, чотири рівні гри, Function Frog.
- [Dice Tower: Robot Turtles](https://dicetower.com/board-game/147370) — Dan Shapiro, 2013, ThinkFun, 2–5 гравців (з дорослим), 4+, 15 хв.
- [RulesPal](https://rulespal.com/robot-turtles/rulebook) — правила (з результатів пошуку, не відкривав).
- [ThinkFun: Turtle Mover](https://thinkfun.com/robot-turtles/turtlemover.php) — сторінка для дорослого (з результатів пошуку, не відкривав).
- YouTube: пошук «robot turtles board game».

## Непевне
- (?) Розмір поля (8×8 — з памʼяті) і точна стартова розстановка.
- (?) Kickstarter-історія (2013) — з памʼяті, у відкритих джерелах не підтверджено.
- (?) Статті Wikipedia «Robot_Turtles» нема (404) — ⭐ поставлено на сторінку правил.
- (?) Чи лазер діє лише на сусідню клітину, чи вздовж лінії до першої перешкоди: правила кажуть «прямо перед черепашкою», трактую як сусідню.
- (?) Чи є офіційна цифрова версія.
