---
title: Frostbite
slug: frostbite
aka: [Frostbite Bailey]
family: maze-arcade
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: none
  goal: state
year: 1983
platforms: [Atari 2600, Activision Anthology (2002)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Frostbite_(video_game)", best: true, note: "суть, вороги, риба 200, температура, життя кожні 5000, режими"}
  - {kind: other, url: "https://www.atariprotos.com/2600/software/frostbite/frostbite.htm", note: "16 блоків іглу, 4 ряди біле/синє, розворот за блок, крижини, що розходяться, ліміт 12 риб, день/ніч"}
  - {kind: other, url: "https://orphanedgames.com/articles/Bookcast_Articles/frostbite.html", note: "розбір гравця: дальність стрибка, ходьба по крижині, ведмідь і безпечна точка"}
  - {kind: other, url: "https://www.oldschoolgamermagazine.com/atari-2600-encyclopedia-do-you-know-frostbite", note: "ряд фарбується цілком, сусідні ряди пливуть назустріч"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Frostbite+Atari+2600", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [move-4dir, row-conveyor, carrier-platform, environment-death, touch-death, player-death, chase-player, time-out, time-bonus, event-points, extra-life-threshold, item-pickup, sequential-levels, progress-acceleration, difficulty-levels, hot-seat, status-panel, game-screen, +paint-cell, +paint-cycle-rules, +reverse-lane-cost, +build-to-exit, +splitting-platform, +push-off-platform, +pickup-cap, +approach-pacify, +day-night-cycle]
proposes: ["+card:reverse-lane-cost", "+card:build-to-exit", "+card:splitting-platform", "+card:push-off-platform", "+card:approach-pacify", "+card:day-night-cycle", "+cond:on_top"]
author: opus
date: 2026-11-09
---

# Frostbite — Frogger × Q*bert: стрибай по рядах крижин, перефарбовуй їх і будуй іглу, доки не замерз

## Суть
Ескімос Frostbite Bailey стрибає вгору-вниз по чотирьох рядах крижин, що пливуть горизонтально, як колоди у Frogger. Приземлення на **білий** ряд фарбує його в синій і додає блок до іглу на березі; коли всі чотири ряди сині — вони знову біліють. Зібрав 16 блоків — у іглу зʼявляються двері, зайшов — рівень пройдено, залишок «температури» йде в бонус. Незвичне: **розворот ряду кнопкою коштує блок іглу** — ціна дії, яка зникає, щойно іглу добудоване.

## Поле і час
- Один екран: берег з іглу вгорі, під ним море з 4 рядами крижин. Рух по вертикалі — дискретними стрибками між рядами (і на берег); по горизонталі — вільно в межах крижини.
- Сусідні ряди пливуть у протилежні боки; екран **не загортається** (тор нема), тож розворот ряду — головний інструмент.
- Real-time; «температура» спадає безперервно, навіть удень. З рівнем росте швидкість гри й дальність стрибка.
- Кожні 4 рівні день змінюється ніччю й назад (кольори, північне сяйво); на пізніх рівнях крижини розходяться й сходяться.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Frostbite Bailey | player | 1 активний + 3 у запасі | стрибок на сусідній ряд; ходьба вздовж крижини; кнопка — розворот ряду |
| Ряд крижин ×4 | platform | колір білий/синій; напрям | пливе горизонтально й везе Бейлі; стрибок на білий → синій |
| Крижини, що «дихають» | platform | фаза | на пізніх рівнях шматки ряду розходяться й сходяться; у щілині — вода |
| Вода | hazard | — | впав — життя −1 |
| Берег | terrain | — | безпечна земля; тут стоїть іглу; з рівня 4 — ведмідь |
| Іглу | container | 16 блоків | росте з кожним пофарбованим рядом; повне → двері |
| Двері іглу | gate | лише в повному іглу | увійшов — рівень пройдено |
| Сніжна гуска | enemy | — | летить прямо вздовж ряду |
| Королівський краб · клацаюча мушля | enemy | — | пливуть рядом, зупиняються й погойдуються |
| Риба | pickup | 200 очок | інколи пливе замість ворога; після 12 за рівень — більше не зʼявляється |
| Білий ведмідь | enemy | з рівня 4; швидшає з рівнями | патрулює берег і женеться; дотик — виштовхує Бейлі з екрана |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(up|down)` → ТО `move(bailey, row±1)`; з діагоналлю — `custom: «горизонтальна дальність стрибка = скільки тримаєш діагональ»`.
- КОЛИ `input(left|right)` → ЯКЩО `custom: «Бейлі на крижині»` → ТО `move(bailey, dir)`.
- КОЛИ `tick` → ТО `shift(row, dir)`, `carry(row, bailey)` — сусідні ряди пливуть назустріч.
- КОЛИ `enter(bailey, floe_row)` → ЯКЩО `state(row, white)` → ТО `paint(row, blue)`, `counter(igloo_blocks, +1)`.
- КОЛИ `counter(blue_rows, ==, 4)` → ТО `paint(all_rows, white)`.
- КОЛИ `enter(bailey, water)` → ТО `lives(-1)`.
- КОЛИ `input(fire)` → ЯКЩО `not state(igloo, complete)` → ТО `face(row, reverse)`, `counter(igloo_blocks, -1)`.
- КОЛИ `input(fire)` → ЯКЩО `state(igloo, complete)` → ТО `face(row, reverse)` — безкоштовно.
- КОЛИ `counter(igloo_blocks, ==, 16)` → ТО `set_state(igloo, complete)`, `spawn(door)`.
- КОЛИ `enter(bailey, door)` → ТО `score(bonus(temperature_left, level))`, `next_level`.
- КОЛИ `timer(every)` → ТО `counter(temperature, -1)`.
- КОЛИ `counter(temperature, ==, 0)` → ТО `lives(-1)`.
- КОЛИ `contact(bailey, goose|crab|clam)` → ТО `push(bailey)` — зіштовхує з крижини у воду; інколи одразу `lives(-1)` (?).
- КОЛИ `contact(bailey, fish)` → ТО `pickup`, `score(200)`, `counter(fish, +1)`.
- КОЛИ `counter(fish, ==, 12)` → ТО `custom: «риба до кінця рівня не зʼявляється»`.
- КОЛИ `timer(breath)` → ТО `custom: «шматки ряду розходяться й сходяться»`.
- КОЛИ `enter(bailey, gap)` → ТО `lives(-1)` — щілина між шматками = вода.
- КОЛИ `enter(bailey, shore)` → ЯКЩО `level(>=, 4) and custom: «не прямо з півдня на крайній захід»` → ТО `set_state(bear, hostile)`; інакше `set_state(bear, idle)` — ведмідь зупиняється й дивиться.
- КОЛИ `contact(bear, bailey)` → ТО `custom: «ведмідь виганяє Бейлі за край екрана»`, `lives(-1)`.
- КОЛИ `counter(score, %, 5000)` → ТО `lives(+1)`.
- КОЛИ `level_end` → ТО `speed(rows, +n)`, `custom: «дальність стрибка росте»`; кожні 4 рівні — день ↔ ніч.
- КОЛИ `counter(lives, ==, 0)` → ТО `game_over`.
- Перемога рівня: 16 блоків + увійти в двері. Поразка: життя вичерпано. Рахунок: риба 200 · бонус іглу за залишок температури й номер рівня · пофарбований ряд (?).

## Керування і ввід
- Джойстик: вгору/вниз — стрибок між рядами (утримання — стрибає далі без окремих натискань); діагональ — стрибок зі зсувом; ліво/право — ходьба по крижині (зійшов за край — у воду).
- Кнопка — розвернути ряд крижин (коштує блок, доки іглу не готове).
- Консольні перемикачі Atari 2600: Game Select — варіант гри (звичайний з рівня 1 / просунутий з рівня 5; 1 або 2 гравці), Game Reset — старт.

## Вікна, меню, HUD
- `game-screen`: берег з іглу, що добудовується блоками (візуальний `progress-bar`), 4 ряди крижин; угорі `score`; під ним `timer-countdown` у градусах (термометр з цифрами) і `lives` у запасі.
- Вибору меню нема — варіант гри перемикається консоллю (`mode-select` через Game Select) (?) щодо відображення номера варіанта.
- Кінець гри — окремого екрана й таблиці рекордів, найпевніше, нема (картридж 2600) (?).
- Переходи: Reset → рівень 1 (або 5) → (двері іглу) підрахунок бонусу → наступний рівень; смерть → той самий рівень.

## Фічі поза полем
- `difficulty-presets` — старт з рівня 1 або 5; `hotseat` — 2 гравці по черзі.
- `levels-sequential` без кінця; косметика за рахунок: рибка-улюбленець біля рахунку (110 000 за orphanedgames; після 20 рівнів за atariprotos) (?).
- Мануал Activision пропонував «нашивку Arctic Architect» за 40 000+ очок — позаігрова прогресія тих часів.

## Варіації й родичі
- [`frogger`](frogger.md) — смуги, що везуть гравця, вода = смерть; Frostbite додає фарбування рядів, будівництво і розворот смуги.
- [`qbert`](qbert.md) — фарбування стрибком; тут фарбується **цілий ряд**, а «правило кольору» — цикл біле → синє → (усі сині) → біле.
- [`flip-and-flop`](flip-and-flop.md) — інший гібрид Q*bert-а того ж 1983 року.
- **Осі варіацій**: смуга — «везе завжди / тоне періодично (Frogger-черепахи) / розходиться на шматки (Frostbite)»; керування смугою — «нема / розворот за ціну / розворот безкоштовно після мети»; вихід — «є з початку / будується зібраним».

## Цікавинки для курсу
- Ряд фарбується стрибком; усі 4 сині → скидання в білі (цикл кольору з глобальним ресетом) — 🌱.
- Розворот смуги кнопкою за ціну ресурсу; ціна зникає після мети — 📎.
- Вихід, що будується з прогресу (16 блоків → двері) — 🌱.
- Температура-таймер, залишок якої конвертується в бонус — 🌱.
- Крижини, що розходяться й сходяться (платформа з фазою й щілинами) — 📎.
- Ведмідь, чий стан залежить від того, **як** гравець вийшов на берег — 📎.
- Ліміт риби на рівень (12) — 🌱.

## Мапа на каталог
- Є: `move-4dir` · `row-conveyor` (ряди крижин) · `carrier-platform` · `environment-death` (вода) · `touch-death` · `player-death` · `chase-player` (ведмідь) · `time-out` (температура) · `time-bonus` · `event-points` · `extra-life-threshold` (кожні 5000) · `item-pickup` (риба) · `sequential-levels` · `progress-acceleration` · `difficulty-levels` · `hot-seat` · `status-panel` · `game-screen`.
- **Нема** → пропозиції карток:
  - `+reverse-lane-cost` «Розворот смуги за ресурс» · entities/move · 📎 · слот {cost}.
  - `+build-to-exit` «Вихід будується з зібраного» · game-logic/win · 🌱 · слот {blocks}.
  - `+splitting-platform` «Платформа розходиться на шматки» · entities/interact · 📎 (сімʼя з `periodic-sink`).
  - `+push-off-platform` «Ворог зіштовхує з платформи» · entities/interact · 🌱.
  - `+approach-pacify` «Ворог мирний, якщо підійти певним шляхом» · entities/state · 📎.
  - `+day-night-cycle` «Зміна дня й ночі між рівнями» · interface/render · 🌱.
  - Повтори: `+paint-cell`, `+paint-cycle-rules` (`qbert`), `+pickup-cap` «Ліміт предмета на рівень» · 🌱.

## Пропозиції до словників
- `+cond:on_top` — сутність стоїть на платформі (Бейлі на крижині — ходьба можлива, інакше вода); повтор з `frogger`.

## Джерела
- ⭐ [Wikipedia: Frostbite](https://en.wikipedia.org/wiki/Frostbite_(video_game)) — білий → синій, іглу, температура, гуски/краби/мушлі/ведмеді, риба 200, життя кожні 5000, звичайний (рівень 1) і просунутий (рівень 5) режими, 2 гравці по черзі.
- [AtariProtos: Frostbite](https://www.atariprotos.com/2600/software/frostbite/frostbite.htm) — 4 ряди й ресет у білі, 16 блоків, розворот коштує блок, «дихаючі» крижини, 12 риб на рівень, ведмідь з рівня 4, день/ніч по 4 рівні.
- [Orphaned Games: Frostbite](https://orphanedgames.com/articles/Bookcast_Articles/frostbite.html) — дальність стрибка від утримання діагоналі, ходьба по крижині, двері іглу, безпечна точка від ведмедя.
- [Old School Gamer: Frostbite](https://www.oldschoolgamermagazine.com/atari-2600-encyclopedia-do-you-know-frostbite) — ряд фарбується цілком, сусідні ряди пливуть назустріч, ведмідь стереже іглу.
- YouTube: пошук «Frostbite Atari 2600».

## Непевне
- (?) Розворот: orphanedgames — лише ряд під Бейлі, atariprotos — усі ряди (утримання кнопки).
- (?) Гуска/краб/мушля: зіштовхують у воду чи вбивають одразу — джерела розходяться.
- (?) Очки за пофарбований ряд і точна формула бонусу іглу; стартова температура.
- (?) Що буде, коли крижина винесе Бейлі до краю екрана.
- (?) З якого рівня крижини «дихають»; коли зʼявляється рибка-улюбленець (110 000 очок чи 20 рівнів).
- (?) Порт на C64 згадано в одному огляді — не перевірено; WebSearch — 1 запит.
