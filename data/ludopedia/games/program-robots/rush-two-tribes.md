---
title: RUSH (Two Tribes)
slug: rush-two-tribes
aka: ["Rubik's Puzzle Galaxy: RUSH", Rush]
family: program-robots
also: [connect-rotate]
klass: cursor
axes:
  field: 3d
  time: programmed
  opponent: none
  info: full
  random: none
  goal: state
year: 2009
platforms: [Wii (WiiWare), PC (Windows), macOS, Linux, Wii U]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/38720/RUSH/", best: true, note: "опис, трейлер, 70+ рівнів, підказки, drag-and-drop мишею"}
  - {kind: other, url: "https://lameazoid.com/review-rush-pc", note: "огляд PC: стрілки, роздільники, конвеєри, стоп-знаки, стіни, падіння, зіткнення, дві підказки"}
  - {kind: other, url: "https://indiegamereviewer.com/?p=2870", note: "огляд 2010: телепорти, роздільники, диспенсери, Easy / Medium / Hard + бонус, без рахунку й ліміту часу"}
  - {kind: other, url: "https://www.tportal.hr/vijesti/clanak/rush-20101220", note: "огляд (HR): стіна → поворот праворуч, телепорти — частина рівня, запас плиток рівно під розвʼязок"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Two_Tribes_(company)", note: "платформи й роки: WiiWare 2009, Windows 2010, Mac/Linux 2011, Wii U 2013"}
  - {kind: other, url: "https://opencritic.com/game/1136/rush/reviews?order=asc", note: "уривки оглядів (Destructoid Wii U: тач, зум тригерами; IGN, Eurogamer, Nintendo Life)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=RUSH+Two+Tribes+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [move-auto, turn-when-blocked, cursor-place, drag-drop-piece, spawn-points, environment-death, all-on-targets, teleport, height-levels, gravity-fall, sequential-levels, level-unlock, level-select, difficulty-levels, restart-level, game-screen, +direction-arrow-tile, +place-then-run, +conveyor-push, +junction-toggle, +stop-sign-delay, +collision-fail, +color-matched-exit, +starting-setup-and-parts, +hint-placement-only, +hint-check-placed, +camera-orbit, +rotate-view-to-solve]
proposes: ["+effect:toggle_junction", "+ui:run-button", "+feature:multiple-profiles", "+feature:bonus-level-set", "+card:stop-sign-delay", "+card:color-matched-exit", "+card:hint-check-placed"]
author: opus
date: 2026-11-19
---

# RUSH — розстав стрілки, конвеєри й роздільники на 3D-рівні, щоб потоки кубів докотились до виходів свого кольору й ніде не зіткнулись

## Суть
Головоломка Two Tribes (автори Toki Tori): зі спавнерів 3D-рівня викочуються кольорові куби й котяться прямо, а гравець наперед розставляє з обмеженого запасу плитки — стрілки, конвеєри, стоп-знаки, роздільники, — щоб кожен куб дійшов до виходу свого кольору. Потім тисне «старт» і дивиться: жоден куб не має випасти за край світу чи хоч раз торкнутися іншого.

Упершись у стіну, куб сам повертає праворуч — це «фізика» рівня, яку гравець використовує нарівні з плитками. Ядро — непряме керування потоком, як у Puzzle-режимі ChuChu Rocket!, але на рівнях із висотами й уступами, де камеру доводиться обертати.

## Поле і час
- Рівень — 3D-конструкція з блоків-клітин: платформи на кількох висотах; куби котяться верхніми гранями клітин.
- З уступу на нижчу платформу падати можна (деякі виходи досяжні лише стрибком згори); з краю світу — куб утрачено.
- Шари: геометрія рівня (стіни, уступи, телепорти, спавнери, виходи) + плитки гравця на вільних клітинах + рухомі куби.
- Час `programmed`: розстановка без часу → запуск (галочка) → куби рухаються в реальному часі; прискорення в PC-версії нема.
- Пізні рівні — більше висот, спавнерів і виходів, до 20+ кубів на полі одночасно (tportal).
- Камеру обертають, щоб бачити всі боки рівня; «печерні» рівні на Wii U тісні для розстановки (Destructoid, уривок).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Куб | object | колір | котиться прямо; слухається плиток; упершись у стіну — повертає праворуч |
| Спавнер (отвір) | spawner | колір, напрям виходу | випускає куби на маршрут (?) з інтервалом |
| Вихід (колектор, «база») | sink | колір | приймає куби свого кольору |
| Стрілка (direction sign) | terrain | напрям | розвертає куб у свій напрям, і він їде далі прямо |
| Конвеєр | terrain | напрям | зсуває куб на одну клітину вбік; курс куба не змінюється |
| Стоп-знак | terrain | — | коротко тримає куб — інструмент таймінгу |
| Роздільник (split, separator) | switch | поточний напрям | шле куби по черзі в один із двох напрямів |
| Варп (телепорт) | terrain | пара точок | переносить куб в іншу частину рівня, зокрема між висотами |
| Стіна, блок рівня | static | — | упор: куб повертає праворуч, поворот коштує короткої затримки |
| Уступ, край платформи | terrain | висота | з уступу куб падає на нижчу платформу; з краю світу — втрачено |
| Запас плиток | supply | кількість кожного виду | рівно стільки, скільки потрібно для розвʼязку |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag, tile → cell)` → ЯКЩО `free(cell)` and `has(supply, tile)` → ТО `place(player, tile)`, `take(supply, tile)`.
- КОЛИ `input(go)` → ТО `custom: «запуск: спавнери починають випускати куби»`.
- КОЛИ `timer(every)` → ТО `spawn_at(cube[c], spawner[c])` (?) — інтервал і кількість кубів на спавнер не перевірено.
- КОЛИ `tick` → ТО `move(cube, facing)`.
- КОЛИ `blocked(cube)` (стіна) → ТО `face(cube, right)`, `stun(cube, 1)` — поворот із короткою затримкою.
- КОЛИ `enter(cube, arrow)` → ТО `face(cube, arrow_dir)`.
- КОЛИ `enter(cube, conveyor)` → ТО `move(cube, conveyor_dir)`; `custom: «курс куба лишається попереднім»`.
- КОЛИ `enter(cube, stop_sign)` → ТО `stun(cube, n)` — куб стоїть кілька тіків, потім їде далі.
- КОЛИ `enter(cube, splitter)` → ТО `face(cube, splitter_dir)`; `after` → `set_state(splitter, other_dir)` — наступний куб піде іншим напрямом.
- КОЛИ `enter(cube, warp)` → ТО `teleport(cube, warp_exit)`.
- КОЛИ `custom: «під кубом порожньо»` → ЯКЩО `custom: «нижче є платформа»` → ТО `fall(cube)`; інакше `lose` — куб випав зі світу.
- КОЛИ `contact(cube, cube)` → ТО `lose` — будь-який дотик двох кубів, навіть на мить.
- КОЛИ `enter(cube, exit)` → ЯКЩО `same(cube, exit, color)` → ТО `disappear_a`, `counter(cubes_left, -1)`; чужий колір — (?).
- КОЛИ `counter(cubes_left, ==, 0)` → ТО `win`, `unlock(next_levels)` — відкривається пачка рівнів, «більше ніж один за раз».
- КОЛИ `custom: «запуск провалено (зіткнення чи падіння)»` → ТО `restart` — розстановку правиш і запускаєш знову; спроб без ліку.
- КОЛИ `input(hint_1)` → ТО `mark(placed_tiles, correct)` — підсвічує, які з поставлених плиток стоять правильно.
- КОЛИ `input(hint_2)` → ТО `reveal(cells)` — показує клітини, де мають стояти плитки; готового розвʼязку не дає.
- КОЛИ `input(rotate_view)` → ТО `camera(rotate)`; на Wii U — `camera(zoom)` тригерами.
- Перемога: усі куби у виходах свого кольору · Поразка: зіткнення кубів або падіння за край — запуск зупиняється · Рахунок: нема; ні таймера, ні ліміту спроб.

## Керування і ввід
- PC: лише миша — перетягнути плитку з панелі запасу на клітину (drag-and-drop), клік по галочці — запуск, обертання камери (?) мишею.
- Wii (WiiWare): вказівник Wii Remote «заганяє» куби знаками (?).
- Wii U: тач GamePad — обертати рівень і ставити знаки; дотик унизу екрана — запуск («куби мчать додому»); зум — тригерами; можна грати без ТВ.
- Плитки ставляться до запуску; після провалу — правиш і запускаєш знову.

## Вікна, меню, HUD
- `main-menu` + `profile-window` — кілька профілів гравців (Steam).
- `level-select`: набори Easy / Medium / Hard + бонусний; рівні відкриваються пачками.
- `game-screen`: 3D-рівень; `inventory-bar` — запас плиток із кількістю; кнопка-галочка запуску; `hint-button` (два рівні підказки); керування камерою.
- `end-screen` — рівень пройдено (?).
- Переходи: level-select → game-screen (розстановка) → галочка (запуск) → (провал) назад до розстановки / (усі куби вдома) → наступний рівень.

## Фічі поза полем
- `levels-sequential` + `level-unlock`: 70+ рівнів у трьох наборах складності + бонусний набір (за вступ до Steam-групи; «регулярно оновлювані» бонусні рівні).
- `hint` двох рівнів: що з поставленого правильне / де мають стояти плитки; використання підказки «знижує успіх» рівня (?).
- `achievements` (Steam, 25), `cloud-save` (Steam Cloud), кілька профілів.
- Нема рахунку, таймера й ліміту спроб; нема прискорення симуляції (PC).
- `localization`: англійська, нідерландська, французька, німецька, італійська, іспанська.

## Варіації й родичі
- Rubik's Puzzle Galaxy: RUSH (WiiWare, 2009) — оригінал під ліцензією Rubik's; RUSH — порт на Windows (2010), Mac/Linux (2011) і Wii U (2013, тач-керування).
- У корпусі: [ChuChu Rocket!](../maze-arcade/chuchu-rocket.md) — той самий принцип «прямо, біля стіни праворуч, стрілка розвертає», Puzzle-режим «розстав і запусти»; [Trainyard](../connect-rotate/trainyard.md) — стрілки, що перемикаються проїздом, як роздільник; [Manufactoria](manufactoria.md) — конвеєри й розгалуження; [Lemmings](../dig-gravity/lemmings.md) — непряме керування натовпом (порівняння IGN); [Upalu Mundi](upalu-mundi.md) — стрілки за станом потяга.
- Осі варіацій: плитка-напрямок «вічна (RUSH) / тане (ChuChu Battle) / ламається»; запас «рівно під розвʼязок (RUSH) / з надлишком / безліч»; конвеєр «змінює курс / лише зсуває (RUSH)»; роздільник «по черзі (RUSH) / за кольором (Manufactoria) / за станом (Upalu Mundi)»; поле «2D (ChuChu) / 3D з уступами (RUSH)».

## Цікавинки для курсу
- Автономні куби «прямо; стіна — праворуч» + плитки-напрямки на 3D-полі з уступами й падінням — 🥉.
- Роздільник із памʼяттю: по черзі в два боки — 📎.
- Конвеєр, що зсуває на клітину без зміни курсу — 🌱.
- Перевірка «куби ніколи не торкаються»: зіткнення в одній клітині, зустрічні й навхрест — 🥉.
- Дві підказки: «що з поставленого правильне» (порівняння з еталоном) і «де мають стояти плитки» — 📎.
- Розвʼязувач: перебір розстановок із точного запасу плиток + симуляція до успіху — 🥇.

## Мапа на каталог
- Є: `move-auto` ↔ куби котяться самі, плитки змінюють напрям · `turn-when-blocked` ↔ стіна → праворуч (слот turn: right) · `cursor-place` + `drag-drop-piece` ↔ плитка з запасу на клітину · `spawn-points` ↔ спавнери · `environment-death` ↔ куб випав за край · `all-on-targets` ↔ усі куби у виходах · `teleport` ↔ варпи · `height-levels` + `gravity-fall` ↔ уступи й падіння на нижчу платформу · `sequential-levels` + `level-unlock` + `level-select` ↔ набори рівнів · `difficulty-levels` ↔ Easy / Medium / Hard · `restart-level` ↔ повтор після провалу · `game-screen`.
- **Нема** → пропозиції карток:
  - `+direction-arrow-tile` (повтор, ChuChu) · слот {lifetime: forever}.
  - `+place-then-run` (повтор).
  - `+conveyor-push` (повтор) · слот {keeps_heading: yes}.
  - `+junction-toggle` (повтор) — роздільник по черзі.
  - `+stop-sign-delay` «Плитка тримає того, хто став, N тіків» · entities/interact · 🌱 · слот {n}.
  - `+collision-fail` (повтор) — будь-який дотик кубів.
  - `+color-matched-exit` «Вихід приймає лише свій колір» · game-logic/win · 🌱.
  - `+starting-setup-and-parts` (повтор, Turing Tumble) — запас плиток рівно під розвʼязок.
  - `+hint-placement-only` (повтор) — «де мають стояти плитки».
  - `+hint-check-placed` «Підказка: які поставлені деталі правильні» · game-logic/difficulty · 📎.
  - `+camera-orbit` / `+rotate-view-to-solve` (повтори).

## Пропозиції до словників
- `+effect:toggle_junction` — роздільник перемикається після кожного куба.
- `+ui:run-button` — галочка запуску симуляції.
- `+feature:multiple-profiles` — кілька профілів гравців на одній копії; `+feature:bonus-level-set` — окремий набір бонусних рівнів поза основними.
- `+card:stop-sign-delay`, `+card:color-matched-exit`, `+card:hint-check-placed` — див. «Мапу на каталог».

## Джерела
- ⭐ [Steam: RUSH](https://store.steampowered.com/app/38720/RUSH/) — опис (куби до виходів свого кольору, конвеєри, варпи, стоп-знаки, роздільники), 70+ рівнів, підказки, drag-and-drop, профілі; трейлер.
- [Lameazoid: Review – Rush (PC)](https://lameazoid.com/review-rush-pc) — спавнери й колектори, запас плиток рівно під розвʼязок, стрілки / роздільники / конвеєри / стоп-знаки / стіни, падіння на нижчий рівень, зіткнення, дві підказки, нема прискорення.
- [Indie Game Reviewer](https://indiegamereviewer.com/?p=2870) — «collisions are fatal», телепорти, роздільники, диспенсери, виходи, до яких треба падати згори, Easy / Medium / Hard + бонус, галочка запуску, без рахунку й ліміту часу.
- [tportal.hr](https://www.tportal.hr/vijesti/clanak/rush-20101220) — стіна завжди повертає куб праворуч, телепорти — частина рівня, куби не мають торкатись ніколи, підказка знижує успіх.
- [Wikipedia: Two Tribes](https://en.wikipedia.org/wiki/Two_Tribes_(company)) — WiiWare 2009, Windows 2010, Mac/Linux 2011, Wii U 2013.
- [OpenCritic: огляди](https://opencritic.com/game/1136/rush/reviews?order=asc) — уривки Destructoid (Wii U: тач, зум тригерами), IGN (Lemmings + ChuChu Rocket), Eurogamer, Nintendo Life.
- [Nintendo Life: Rubik's Puzzle Galaxy: RUSH](https://www.nintendolife.com/reviews/2009/12/rubiks_puzzle_galaxy_rush) — огляд WiiWare (у фетчі 403; бачено в пошуку: роздільник по черзі, конвеєр лише зсуває, стоп-знак тримає коротко).
- YouTube: пошук «RUSH Two Tribes gameplay».

## Непевне
- (?) Напрям стрілки: заданий у запасі рівня чи гравець обирає й повертає (уривок Giant Bomb у пошуку — «pieces can't be rotated»; сторінка не відкрилась).
- (?) Інтервал і кількість кубів зі спавнера; «диспенсери, що пускають куби в кількох напрямках» (IGR) — як саме.
- (?) Що буває з кубом у виході чужого кольору — провал чи упор.
- (?) Варпи: лише частина рівня (tportal) чи бувають і в запасі (Steam перелічує їх серед засобів гравця).
- (?) Роздільник: які саме два напрями (ліворуч / праворуч від курсу?); «ротори пришвидшують куби» (tportal) — не підтверджено.
- (?) Стіна: поворот «миттєво» (tportal) проти «з короткою затримкою» (Lameazoid).
- (?) «Деякі куби швидші за інші» (IGR) — окремий тип куба чи частіший спавн.
- (?) Чи можна правити плитки під час запуску; чи провал скидає запуск одразу.
- (?) Віртуальний кубик Рубіка у WiiWare-версії згадано лише в пошуковому уривку; tportal каже, що в PC-версії такого режиму нема.
- (?) «Підказка знижує успіх» — чи є позначка «пройдено без підказок».
- Помилка черги: рік 2010 — це PC-порт; оригінал — Rubik's Puzzle Galaxy: RUSH (WiiWare, 2009).
