---
title: DVONN
slug: dvonn
aka: [Двонн, Dvonn]
family: chess-abstract
also: []
klass: figure
axes:
  field: hex
  time: turn
  opponent: hotseat
  info: full
  random: none
  goal: score
year: 2001
platforms: [board, web]
links:
  - {kind: other, url: "https://www.gipf.com/dvonn/rules/rules.html", best: true, note: "офіційні правила: дві фази, рух на висоту стосу, відрізання від DVONN-фішок, підрахунок"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/DVONN", note: "49 полів, 23+23+3 фішки, 97 ходів максимум, нагороди, програми (CodeCup 2011)"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/GIPF_project", note: "четверта гра серії; DVONN-potential у GIPF"}
  - {kind: bgg, url: "https://boardgamegeek.com/geeksearch.php?action=search&q=DVONN", note: "пошук BGG"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=DVONN+board+game+how+to+play", note: "пошук; як грати"}
stage: v1
coverage: 75
mechanics: [piece-move-patterns, connectivity-check, pass-turn, no-moves-left, legal-move-highlight, selection-highlight, last-move-highlight, hot-seat, turn-enforcement, move-timer, ai-opponent, ai-minimax, cell-click, hover-highlight, drag-drop-piece, online-multiplayer, move-notation, replay, game-screen, main-menu, end-screen, help-window, settings-window, state-as-data, unit-tests, +hex-grid-render, +placement-phase, +stack-control, +stack-height-move, +disconnect-removal, +stack-height-score]
proposes: ["+cond:top_side", "+cond:surrounded", "+cond:stack_height", "+effect:stack_onto", "+effect:remove_disconnected", "+trigger:phase_end", "+ui:stack-view", "+ui:stack-height-label", "+ui:dvonn-link-overlay", "+card:stack-height-move", "+card:disconnect-removal", "+card:placement-phase", "+card:stack-height-score"]
author: opus
date: 2026-11-09
---

# DVONN — стос ходить рівно на свою висоту; усе, що відірвалось від червоних DVONN-фішок, зникає

## Суть
Спершу двоє по черзі заповнюють усе поле: три нейтральні червоні DVONN-фішки й по 23 своїх. Потім по черзі переносять стоси, якими керують (свій колір зверху): стос летить прямою **рівно на стільки полів, скільки в ньому фішок** і мусить сісти на інший стос. Після кожного ходу всі стоси, не повʼязані ланцюжком сусідів із жодною DVONN-фішкою, знімаються з гри. Коли ходів нема ні в кого, виграє той, у чиїх стосах більше фішок. Четверта гра GIPF Project (Kris Burm), International Gamers Award 2002.

## Поле і час
- 49 полів у видовженому гекс-розкладі, 5 рядів (`field: hex`, трикутна сітка точок, 6 напрямків).
- Поле поступово «розсипається»: порожніх полів більшає, острови без DVONN-фішки зникають.
- Дві фази: розстановка (49 ходів до повного поля) і рух (≤ 48 ходів, без пасів) — максимум 97 ходів. Турнірний годинник — 15 хв на гравця наживо, 10 хв онлайн.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Фішка гравця | piece | white ×23 / black ×23 | ставиться на порожнє поле у фазі 1; у фазі 2 — частина стосу |
| DVONN-фішка | neutral | red ×3, нікому не належить | сама не ходить; на неї можна ставити стоси; «якір» звʼязності, лишається в грі до кінця |
| Стос | piece | висота h ≥ 1, власник = колір верху | ходить прямою рівно на h полів; може містити DVONN-фішку — тоді він теж якір |
| Поле | terrain | 49, порожнє / зайняте | порожні поля можна перелітати, але не на них приземлятись |
| Острів | zone | звʼязна компонента зайнятих полів | без DVONN-фішки — знімається цілком |
| Зняті фішки | zone | — | вибули з гри, не рахуються нікому |

## Правила (КОЛИ → ЯКЩО → ТО)
- Фаза 1: КОЛИ `input(place, cell)` → ЯКЩО `free(cell)` → ТО `place(piece, cell)`; перші три ходи — DVONN-фішки (білі, чорні, білі), далі — свої фішки, починають чорні.
- КОЛИ `custom: «поле заповнене»` (`+trigger:phase_end`) → ТО фаза 2; першими ходять білі.
- КОЛИ `input(move, stack, dir)` → ЯКЩО `custom: «колір верху стосу — мій»` (`+cond:top_side`) → ТО продовжити перевірку; інакше `block`.
- КОЛИ `input(move, stack, dir)` → ЯКЩО `adjacent_count(stack, occupied, ==, 6)` (`+cond:surrounded`) → ТО `block` — оточений з усіх 6 боків не ходить.
- КОЛИ `input(move, stack, dir)` → ЯКЩО `custom: «одиночна DVONN-фішка»` → ТО `block`.
- КОЛИ `input(move, stack, dir)` → ЯКЩО `custom: «через h полів прямою (порожні рахуються) — зайняте поле»` (`+cond:stack_height`) → ТО `custom: «поставити весь стос зверху цільового»` (`+effect:stack_onto`); інакше `block` (на порожнє не сідають, за край не виходять).
- Ціль може бути будь-якого кольору, зокрема стос з DVONN-фішкою; новий власник — колір нового верху.
- КОЛИ `after(stack_onto)` → ЯКЩО `not connected(stack, dvonn)` — стос не повʼязаний ланцюжком сусідів з DVONN-фішкою → ТО `disappear(stack)` (`+effect:remove_disconnected`), байдуже, чий хід це спричинив.
- КОЛИ `no_moves(side)` → ТО `pass_turn`; пасувати, маючи хід, не можна.
- КОЛИ `no_moves(both)` → ТО `custom: «кожен складає свої стоси; рахуються всі фішки під своїм верхом, незалежно від кольору»` → більше — `win`, рівно — `draw`.
- Перемога: більше фішок у стосах, які контролюєш наприкінці · Поразка: менше · Рахунок: сума висот своїх стосів.

## Керування і ввід
- Настільна: фаза 1 — ставиш фішку на порожнє поле; фаза 2 — береш стос цілком і переносиш.
- (цифрова версія) Клік по своєму стосу → підсвітка до 6 цільових полів рівно на висоті h → клік/drag. Після ходу анімовано зникають відрізані острови.
- Позиція має бути добре читабельною: висота й колір верху кожного стосу — цифрою або профілем.

## Вікна, меню, HUD
- `main-menu` (цифрова версія): Грати проти людини / робота → `match-setup` (колір, годинник).
- `game-screen`: гекс-поле, `turn-indicator` з фазою (розстановка / рух), `stack-height-label` на кожному стосі, `stack-view` (склад стосу при наведенні), `legal-move-highlight`, `dvonn-link-overlay` (які стоси живуть від якої DVONN-фішки), `score` (поточна сума контрольованих фішок), `last-move-highlight`, `move-list`, `player-clock`.
- `end-screen`: дві «вежі» з підсумком висот, перемога / нічия.
- `help-window`: правила і приклад відрізання острова.
- Переходи: main-menu → match-setup → game-screen (фаза 1 → фаза 2) → end-screen.

## Фічі поза полем
- `online-multiplayer` і `ai-opponent-levels` — Boardspace.net (людина або робот), LittleGolem (раніше — роботи RoRoRo, Jan's program).
- `turn-timer`: 15 / 10 хв на гравця.
- Програми: dDvonn, Dvonner, Holtz (кілька ігор), PrimaDvonna — переможець CodeCup 2011 (змагання ботів).

## Варіації й родичі
- У GIPF — DVONN-potential: поставити potential на звичайну фішку суперника й перефарбувати її.
- Серія GIPF Project: [gipf](gipf.md) (вштовхування), [zertz](zertz.md) (поле теж зменшується, ізоляція островів), [yinsh](yinsh.md); TZAAR — інша гра серії зі стосами (?).
- Стоси в корпусі: [tak](tak.md) (стос розкладається слідом), [lasca](lasca.md) (колона з полоненими), [hive](hive.md) (жук на вулику), [checkers-variants](checkers-variants.md).
- «Відрізане зникає» — як «один вулик» у [hive](hive.md) і острови в [zertz](zertz.md); рух «рівно на N» — LOA у [breakthrough-loa](breakthrough-loa.md) (там N — кількість фішок на лінії).
- Осі варіацій: **дальність руху** (= висота / ≤ висоти / = кількість на лінії) · **куди можна сісти** (лише на зайняте / будь-куди) · **якір звʼязності** (нейтральні фішки / свої) · **підсумок** (сума фішок / найвищий стос).

## Цікавинки для курсу
- Фаза розстановки + фаза руху з різними правилами в одному двіжку — 🌱.
- Генерація ходів «рівно на h полів, приземлитись на зайняте, не з оточення» — 📎.
- Відрізання островів: BFS від усіх DVONN-фішок після кожного ходу, зняття решти — 🥉.
- Стос як список з власником = верх, переливання стосу на стос — 🌱.
- Підрахунок наприкінці і пас лише без ходів (гра до повного виснаження обох) — 🌱.
- AI: розгалуження падає з кожним ходом — minimax з оцінкою «контроль висот + близькість до DVONN» — 🥇.

## Мапа на каталог
- Є: `piece-move-patterns` ↔ рух на h · `connectivity-check` ↔ звʼязок із DVONN · `pass-turn`, `no-moves-left` ↔ пас і кінець гри · `legal-move-highlight`, `selection-highlight`, `last-move-highlight` · `hot-seat`, `turn-enforcement`, `move-timer`, `online-multiplayer` · `ai-opponent`, `ai-minimax` · `cell-click`, `hover-highlight`, `drag-drop-piece` · `move-notation`, `replay`, `state-as-data`, `unit-tests` · `game-screen`, `main-menu`, `end-screen`, `help-window`, `settings-window`.
- **Нема** → пропозиції карток:
  - `+hex-grid-render` (див. hex.md).
  - `+placement-phase` «Фаза розстановки на полі перед рухом» · game-logic/opponent · 🌱 — DVONN, YINSH, млин.
  - `+stack-control` (див. tak.md) — власник стосу = верх.
  - `+stack-height-move` «Рух рівно на висоту стосу» · entities/move · 📎.
  - `+disconnect-removal` «Відрізане від якоря зникає» · entities/interact · 🥉 · слоти {anchor: neutral|own}.
  - `+stack-height-score` «Перемога за сумою висот стосів» · game-logic/win · 🌱.

## Пропозиції до словників
- `+cond:top_side` — верхня фішка стосу належить стороні (Tak, Lasca, DVONN).
- `+cond:surrounded` — усі сусідні клітини зайняті (Hive, DVONN).
- `+cond:stack_height` — ціль рівно на відстані висоти стосу.
- `+effect:stack_onto` — перенести стос цілком на інший стос.
- `+effect:remove_disconnected` — зняти всі сутності, не звʼязані з якорем.
- `+trigger:phase_end` — завершилась фаза партії (розстановка → рух).
- `+ui:stack-view`, `+ui:stack-height-label`, `+ui:dvonn-link-overlay` — склад стосу, висота цифрою, підсвітка звʼязку з якорем.
- `+card:stack-height-move`, `+card:disconnect-removal`, `+card:placement-phase`, `+card:stack-height-score` — див. «Мапа на каталог».

## Джерела
- ⭐ [gipf.com: правила DVONN](https://www.gipf.com/dvonn/rules/rules.html) — дві фази, порядок розстановки, рух, оточення, відрізання, пас, підрахунок і правило «різниця в 1 — рахуйте фішки».
- [Wikipedia: DVONN](https://en.wikipedia.org/wiki/DVONN) — 49 полів, 23+23+3, максимум 97 ходів, годинник, нагороди (IGA 2002, Games 2003), програми і CodeCup.
- [Wikipedia: GIPF project](https://en.wikipedia.org/wiki/GIPF_project) — місце в серії, DVONN-potential.

## Непевне
- (?) Хто ставить першу фішку свого кольору: офіційні правила — чорні після трьох DVONN-фішок; Wikipedia — «білі першими» (мабуть, про першу DVONN-фішку).
- (?) Точна форма поля — ряди 9-10-11-10-9 (з памʼяті; джерела кажуть лише «49 полів, 5 рядів»).
- (?) Wikipedia: «білі першим ходом мусять рухати фішку з периметра» — це наслідок правила оточення, а не окреме правило.
- (?) TZAAR як гра зі стосами — з назви «capture and stacking game», правил не читав.
- (?) BoardSpace-сторінку DVONN не відкривав (згадка — зі статті Wikipedia).
