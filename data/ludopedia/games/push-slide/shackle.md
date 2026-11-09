---
title: Shackle
slug: shackle
aka: [Shackle (Steven Miller), Кайдани]
family: push-slide
also: [thinky]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2020
platforms: [PC, web]
links:
  - {kind: itch, url: "https://steven-miller.itch.io/shackle", best: true, note: "грати в браузері; опис «A ball and chain obstructs your movement», 45+ рівнів, керування, GameMaker"}
  - {kind: other, url: "https://steven-miller.itch.io/shackle/devlog/145134/update-1", note: "коментарі автора: rot13-підказки до +3 Cage (червона стіна, перемикачі, перевернуті сині стіни, ящик, «міст», відродження)"}
  - {kind: other, url: "https://itch.io/t/819809/stuck-on-second-to-last-level-anyone-have-a-hint-spoiler", note: "Preservation: «rigid/freezing tile», ящик на ланцюгу, «break your ball»"}
  - {kind: other, url: "https://itch.io/t/826041/need-help-for-the-final-puzzle-spoilers", note: "Eternity: зелені/червоні/сині перемикачі, ланцюг рветься лише на перевернутих синіх воротах, секретний вхід до бонусів"}
  - {kind: other, url: "https://www.bontegames.com/2020/05/shackle-browser.html?m=1", note: "огляд + коментарі гравців: куля штовхає ящик, freezing pad, «flung off» на кутах, 47 рівнів, 3 слоти збережень"}
  - {kind: itch, url: "https://steven-miller.itch.io/shack-o-lantern", note: "спін-оф 2025: світильник-гарбуз на ланцюгу, поза світлом не можна"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Shackle+Steven+Miller+puzzle", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [move-4dir, keyboard-controls, push-object, button-toggle, impassable-cells, reach-exit, environment-death, respawn, destructible-blocks, world-map, level-select, save-multi-slot, restart-level, +undo-redo, +undo-through-restart, +tether-tail, +auto-attach, +ghost-revive, +rigid-chain-tile, +inverted-gate, +crush-by-gate, +secret-bonus-levels]
proposes: ["+effect:attach", "+effect:detach", "+effect:drag", "+effect:revive", "+trigger:crushed", "+cond:unique_adjacent", "+role:tether", "+axis:actors", "+feature:undo-through-restart", "+feature:save-slots", "+card:tether-tail", "+card:auto-attach", "+card:inverted-gate", "+card:crush-by-gate"]
author: opus
date: 2026-11-09
---

# Shackle — Sokoban з ядром на ланцюгу: куля заважає ходити, але нею тиснуть перемикачі, штовхають ящики, а смерть — спосіб скинути кайдани

## Суть
Покрокова головоломка: герой прикутий ланцюгом до залізної кулі, яка волочиться за ним і обмежує, куди можна пройти. Та сама куля — інструмент: вона тисне кольорові перемикачі й штовхає ящики. Ланцюг можна втратити (його перебивають ворота, що зачиняються), а героя — «вбити» об червоні стіни чи двері; після смерті він стає привидом, а відродившись, знову має ланцюг і чіпляє найближчу кулю. Пізні рівні — про обмін куль і ящиків між частинами рівня, паритет і «що зберегти» (рівень Preservation).

## Поле і час
- Квадратна сітка, рівні з кількох кімнат-відсіків, зʼєднаних коридорами; вигляд згори, піксель-арт.
- Хід = крок героя (з можливим поштовхом і перетягуванням кулі); без вводу нічого не рухається.
- Ланцюг займає проміжні клітини між героєм і кулею (на скріншотах — 2–3 ланки між ними) (?).
- Світ — хаб «main hall» з групами рівнів (позначення 5.4 = рівень 26), рівень Exit і секретні бонусні рівні з «+» (+3 Cage, Eternity).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой | player | є / нема ланцюга | рух 4 напрямки; штовхає ящики; тягне кулю ланцюгом |
| Ланцюг | object | довжина (?) | звʼязує героя з кулею; ящик може застрягти на ньому; рветься під воротами, що зачиняються |
| Залізна куля (прикута) | object | — | волочиться за героєм; штовхає ящики; тисне перемикачі |
| Вільна куля | object | — | герой без кулі чіпляє її, підійшовши; не чіпляється, якщо поруч друга куля або ланцюг на її клітині |
| Ящик (crate) | object | — | штовхається героєм або кулею; тисне перемикачі; може «зачепитися» за ланцюг |
| Червоний / зелений / синій перемикач | switch | колір | натиснутий обʼєктом (куля, ящик) або героєм (?) — керує стінами свого кольору |
| Кольорова стіна / двері | gate | колір, відкрита/закрита | відкривається перемикачем; зачиняючись на герої — вбиває, на кулі/ящику/ланцюгу — руйнує |
| Перевернута стіна (inverted) | gate | колір | поводиться навпаки: піднята, коли перемикач натиснутий; сині перевернуті ворота — місце, де рветься ланцюг |
| Freezing pad («rigid/freezing tile») | terrain | — | ланцюг стає жорстким/складеним; так проводять ланцюг крізь ящик і повертають за кути |
| Кнопка (Exit, бонуси) | switch | — | натискається героєм або кулею; відкриває прохід до бонусних рівнів |
| Вихід / сходи | static | — | дійти й натиснути Space — рівень пройдено |
| Привид (мертвий герой) | player | — | рухається без ланцюга, може «ходити поверх» обʼєктів-мосту (?); відроджується з новим ланцюгом |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next_cell)` → ТО `move(player, dir)`, `custom: «куля тягнеться за героєм ланцюгом»` (?).
- КОЛИ `contact(player, crate)` → ЯКЩО `free(cell_behind)` → ТО `push`.
- КОЛИ `contact(ball, crate)` → ЯКЩО `free(cell_behind)` → ТО `push` (куля штовхає ящик на перемикач).
- КОЛИ `custom: «герой повертає за кут з предметом на ланцюгу»` → ТО `custom: «предмет злітає з ланцюга»` («flung off»).
- КОЛИ `enter(player, freezing_pad)` → ТО `set_state(chain, rigid)` — ланцюг складається, проходить кути й крізь ящик.
- КОЛИ `adjacent(player, loose_ball)` → ЯКЩО `not has(player, chain_ball)` і `custom: «поруч рівно одна вільна куля»` і `custom: «ланцюг не лежить на клітині кулі»` → ТО `attach(player, ball)`.
- КОЛИ `enter(object, switch)` → ТО `set_state(gates_of_color, open)`; інверсні стіни того ж кольору — `set_state(inverted, closed)`.
- КОЛИ `leave(object, switch)` → ТО `set_state(gates_of_color, closed)`.
- КОЛИ `custom: «ворота зачиняються на клітині героя»` або `contact(player, red_wall)` → ТО `died(player)` → `custom: «герой стає привидом»`, `detach(player, ball)`.
- КОЛИ `custom: «ворота зачиняються на ланцюгу»` → ТО `custom: «ланцюг рветься»`, `detach(player, ball)`.
- КОЛИ `custom: «ворота зачиняються на кулі чи ящику»` → ТО `disappear` (обʼєкт знищено).
- КОЛИ `custom: «привид відроджується»` → ТО `respawn(player, here)`, `custom: «ланцюг зʼявляється знову, навіть якщо був знищений»`; на freezing pad — ланцюг складений.
- КОЛИ `custom: «знищено кулю, коли на ланцюгу застряг ящик»` → ТО `custom: «ящик лишається на ланцюгу»` (ключ рівня Preservation) (?).
- КОЛИ `reach(player, exit)` → ЯКЩО `input(continue)` → ТО `win`, `next_level`.
- КОЛИ `custom: «пройдено всі рівні main hall»` → ТО `custom: «стіна в центрі рівня Exit опускається»`, `unlock(bonus_levels)`.
- КОЛИ `input(undo)` → ТО `undo(1)` (з 2025 — і крізь рестарт) · КОЛИ `input(reset)` → ТО `restart`.
- Перемога: дійти до виходу (у деяких рівнях — лише з ланцюгом). · Поразка: нема; глухий кут → undo/reset. · Рахунок: нема, лише відмітки пройдених рівнів.

## Керування і ввід
- WASD / стрілки — крок; Z / U / Shift / Backspace — undo; R — reset; Space / Enter — продовжити (зійти сходами); Escape — вихід; Tab — повний екран.
- Один аватар; керування кулею — лише непряме, через рух героя.

## Вікна, меню, HUD
- `main-menu` з підказкою-промптом (додано в Update #4); `save-slots` — 3 слоти збережень.
- `map-window` — хаб «main hall»: входи в групи рівнів, позначка завершеної області.
- `game-screen`: кімната; HUD — назва рівня (?) і мінімум інтерфейсу.
- `credits-window` (виправлений у Update #1).
- Переходи: меню → слот → хаб → рівень → сходи → хаб.

## Фічі поза полем
- `undo` без ліміту + `+feature:undo-through-restart` (з 5-ї річниці, 2025).
- `restart-level`, `levels-sequential` групами в хабі; секретний шар бонусних «+»-рівнів після рівня Exit.
- `+feature:save-slots` — три слоти прогресу.
- Безкоштовно / «name your own price», браузерна версія з травня 2020.

## Варіації й родичі
- **Shack-o'-Lantern** (2025, той самий автор) — спін-оф: замість кулі на ланцюгу світильник-гарбуз; поза світлом бути не можна; «плутані» обʼєкти автор хотів би бачити «як сегменти змійки»; квіти, які можна знищити. Автор: «перші 6 наборів Shackle покривають усі потрібні механіки».
- **Осі варіацій**:
  - **звʼязок з обʼєктом**: нема (`sokoban`) / тягнення поруч (`pull-object`) / ланцюг фіксованої довжини (тут) / змійка-тіло (Snakebird);
  - **як позбутися ноші**: ніяк / смерть і відродження (тут) / розрізати ланцюг воротами;
  - **хто тисне перемикач**: герой / ящик / куля на ланцюгу (тут — усе разом, звідси паритетні задачі).
- Родичі: `sokoban`, `kwirk`, `quell`; Baba Is You (правила-обʼєкти) — межа з `thinky`.

## Цікавинки для курсу
- Ланцюг фіксованої довжини: куля тягнеться, коли відстань перевищено; ланки на проміжних клітинах — 🥈.
- Автоприєднання до кулі з правилом неоднозначності (дві кулі поруч → нічого) — 📎.
- Смерть як механіка: привид без ланцюга, відродження з новим ланцюгом — 🥉.
- Ворота, що зачиняються на обʼєкті: вбивають / рвуть ланцюг / руйнують кулю — 🥉 (таблиця «що під воротами»).
- Freezing pad — зміна фізики ланцюга (жорсткий, проходить кути) — 🥈.
- Розвʼязувач для кімнат з кулями, ящиками й перемикачами (BFS по станах із ланцюгом) — 🥇.

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls`; `push-object` ↔ ящики (герой і куля); `button-toggle` ↔ кольорові перемикачі; `impassable-cells`; `reach-exit` ↔ сходи; `environment-death` ↔ смерть на червоному / під воротами; `respawn` ↔ відродження; `destructible-blocks` ↔ знищення куль і ящиків; `world-map` + `level-select` ↔ хаб; `save-multi-slot` ↔ 3 слоти; `restart-level`.
- **Нема** → пропозиції карток:
  - `+tether-tail` «Обʼєкт на ланцюгу фіксованої довжини тягнеться за аватаром» · entities/move · 🥈 · слот {length}.
  - `+auto-attach` «Аватар без ноші автоматично чіпляє сусідній обʼєкт, якщо вибір однозначний» · entities/interact · 📎.
  - `+ghost-revive` «Після смерті аватар стає привидом і згодом відроджується (зі скинутою ношею)» · entities/death · 🥉.
  - `+rigid-chain-tile` «Клітина робить ланцюг жорстким» · entities/interact · 🥉.
  - `+inverted-gate` «Стіна, що працює навпаки до перемикача» · entities/interact · 🌱.
  - `+crush-by-gate` «Ворота, що зачиняються, знищують/вбивають те, що під ними» · entities/death · 📎.
  - `+secret-bonus-levels`, `+undo-through-restart`, `+undo-redo`.

## Пропозиції до словників
- `+effect:attach` / `+effect:detach` — ⏳ підтверджую: приєднати/відʼєднати кулю.
- `+effect:drag` — обʼєкт тягнеться за аватаром на привʼязі (не крок поруч, як `pull`).
- `+effect:revive` — відродження з поверненням привʼязі (уже пропонували інші).
- `+trigger:crushed` — сутність опинилась під воротами, що зачинились.
- `+cond:unique_adjacent` — поруч рівно один обʼєкт виду (правило автоприєднання).
- `+role:tether` — ланцюг/мотузка як окрема сутність між двома.
- `+axis:actors` — `tethered`: аватар + привʼязаний обʼєкт.
- `+feature:undo-through-restart`, `+feature:save-slots`.
- `+card:tether-tail`, `+card:auto-attach`, `+card:inverted-gate`, `+card:crush-by-gate`.

## Джерела
- ⭐ [itch.io: Shackle](https://steven-miller.itch.io/shackle) — опис, 45+ рівнів, керування, HTML5/Windows, GameMaker, devlog-и (оновлення 2020, 5-та річниця 2025).
- [Devlog Update #1 + коментарі](https://steven-miller.itch.io/shackle/devlog/145134/update-1) — 6 rot13-підказок автора до +3 Cage (червона стіна, куля на перемикачі «повертається», зелена кнопка, перевернута синя стіна, «міст», відродження), «ланцюг завжди зʼявляється після смерті».
- [Тред Preservation](https://itch.io/t/819809/stuck-on-second-to-last-level-anyone-have-a-hint-spoiler) — «rigid/freezing tile», «три кулі», «break your ball while you have a box stuck on your chain», «chain doesn't attach if it is on the same tile as the ball».
- [Тред Eternity](https://itch.io/t/826041/need-help-for-the-final-puzzle-spoilers) — перемикачі трьох кольорів, «blue inverted gates… only place where you can break your chain», «opening and closing them to die», секрет: стіна в рівні Exit, кнопка кулею.
- [bontegames](https://www.bontegames.com/2020/05/shackle-browser.html?m=1) — коментарі: куля штовхає ящик, freezing pad, «flung off», червоний перемикач убиває героя, 47 рівнів, бонуси «+», 3 слоти, Space для сходів.
- [Shack-o'-Lantern](https://steven-miller.itch.io/shack-o-lantern) і тред Help Needed — спін-оф, світло на ланцюгу, «перші 6 наборів Shackle покривають усі механіки».

## Непевне
- (?) Точна довжина ланцюга і правило волочіння (куля тягнеться одразу чи лише при натягу; чи може куля проходити кути без freezing pad).
- (?) Чи натискає перемикач сам герой; що саме робить червоний перемикач (вбиває героя чи відчепляє кулю — у коментарях обидва).
- (?) Де відроджується привид і що запускає відродження («without reviving too early»); як привид ходить «поверх» обʼєктів.
- (?) За пошуковим описом Thinky Games, Shackle — початок лінії ігор автора про тягання обʼєктів; сторінку не відкрито (403).
- (?) Кількість рівнів: itch — «over 45», гравці — 47 основних + бонусні «+»; назви груп і HUD — з памʼяті коментарів.
