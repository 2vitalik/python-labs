---
title: JezzBall
slug: jezzball
aka: [Jezz Ball]
family: maze-arcade
also: []
klass: cursor
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: setup
  goal: territory
year: 1992
platforms: [Windows 3.x (Microsoft Entertainment Pack), The Best of Microsoft Entertainment Pack]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/JezzBall", best: true, note: "атоми, стіна з точки курсора в обидва боки, мʼяч у недобудовану стіну — життя, 75 %, життів = атомів, +1 атом за рівень"}
  - {kind: other, url: "https://jeffpar.github.io/kbarchive/kb/098/Q98938", note: "Microsoft KB Q98938: половина стіни, час за кількістю атомів, очки за клітину, бонуси за % понад 80 і 90, повільні атоми = ½ очок"}
  - {kind: itch, url: "https://winterdust.itch.io/jezzball-classic", note: "JezzBall Classic — фан-ремейк, що відтворює оригінал; моди й пресети"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=JezzBall+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [cell-click, player-death, time-out, time-bonus, event-points, sequential-levels, progress-acceleration, status-panel, game-screen, +region-fill, +territory-capture, +percent-goal, +trail-vulnerable, +bounce-move, +wall-builder-two-ends, +lives-per-enemy, +tiered-overshoot-bonus, +speed-score-tradeoff]
proposes: ["+card:wall-builder-two-ends", "+card:lives-per-enemy", "+card:tiered-overshoot-bonus", "+card:speed-score-tradeoff", "+ui:territory-percent"]
author: opus
date: 2026-11-09
---

# JezzBall — клік ставить стіну, що росте в обидва боки й ділить кімнату; атом у недобудовану половину — мінус життя

## Суть
У прямокутній кімнаті відбиваються атоми; гравець кліком запускає стіну, яка від точки курсора росте двома половинами в протилежні боки. Половина, що дійшла до стіни без дотику атома, стає частиною поля; області без атомів зафарбовуються й зараховуються. Треба відрізати щонайменше 75 % кімнати до кінця часу. Аватара нема: гравець — курсор, а ризик — у моменті й місці запуску (Qix/Xonix без бігуна).

## Поле і час
- Кімната — сітка клітин; очки рахуються «за клітину». З чисел KB (3.5 очка за клітину, 70 за вертикальний і 98 за горизонтальний прохід) — 20 × 28 клітин (вивід (?)).
- Атоми рухаються по діагоналі й відбиваються від стін і захопленого.
- Real-time з таймером рівня; що більше атомів, то більше часу. Годинник — у правому верхньому куті.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Курсор-будівник | — | орієнтація: горизонт / вертикаль | лівий клік — запуск стіни, правий — зміна орієнтації |
| Половина стіни (червона / синя) | hazard | росте з точки запуску | вразлива, доки не дійшла до стіни; атом у неї — життя мінус |
| Стіна (добудована) | static | — | межа; атоми від неї відбиваються |
| Атом (червоно-білий мʼяч) | enemy | 2 на 1-му рівні, +1 щорівня, з 49-го — 50 | рух по діагоналі, відбивання |
| Вільна кімната | zone | площа | тут літають атоми |
| Захоплена область | zone | частка поля, % | зафарбована, атомів у ній нема |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(right_click)` → ТО `rotate(builder, 90)` — горизонтально ↔ вертикально.
- КОЛИ `input(left_click, cell)` → ЯКЩО `free(cell)` → ТО `spawn(wall_half_red)`, `spawn(wall_half_blue)` у протилежні боки.
- КОЛИ `tick` → ТО `grow(wall_half, 1)` у своєму напрямку.
- КОЛИ `reach(wall_half, wall)` → ТО `transform(wall_half, wall)`.
- КОЛИ `contact(atom, wall_half)` → ТО `disappear(wall_half)`, `lives(-1)`; друга половина росте далі й може добудуватись.
- КОЛИ `pattern(region_closed)` → ЯКЩО `count(atom_in_region, ==, 0)` → ТО `fill(region)`, `score(+cells × rate)`.
- КОЛИ `tick` → ТО `move(atom, diag)`; ЯКЩО `not free(cell_ahead)` → ТО `bounce(atom)`.
- КОЛИ `counter(cleared, >=, 75%)` → ТО `next_level`, `score(bonus)` — бонус за кожен % понад 80 і другий рівень бонусу за кожен % понад 90; обидва ростуть з кількістю атомів.
- КОЛИ `level_start` → ТО `spawn(atom × (level + 1))` (з 49-го рівня — 50), `custom: «життів = кількість атомів»`, `timer(start, by_atoms)`.
- КОЛИ `counter(lives, ==, 0)` → ТО `game_over`.
- КОЛИ `counter(time_left, ==, 0)` → ТО `custom: «рівень не пройдено»` (?).
- КОЛИ `custom: «атоми сповільнено в налаштуваннях»` → ТО `multiplier(×0.5)`; швидкі атоми — очки ×2 до повільних.
- Перемога: рівнів нескінченно. Поразка: життя вичерпано. Рахунок: клітини захоплених областей (ціна клітини росте з атомами), бонус за % понад 80 / 90, у ремейку — ще за час і життя.

## Керування і ввід
- Лише миша: лівий клік — запуск стіни в клітині під курсором, правий — перемкнути орієнтацію.
- Запуск можливий лише у вільній частині кімнати; одночасно будується одна стіна (?).

## Вікна, меню, HUD
- `game-screen`: кімната; статус-рядок — рівень, життя, захоплено %, очки (?); `timer-countdown` у правому верхньому куті.
- Меню-бар Windows: Game (New, Pause, High Scores…) · Options (звук, повільні атоми) · Help (?).
- `end-screen`-діалог рівня з бонусом (?); `leaderboard` рекордів (?); `help-window` — довідка Windows (?).
- Переходи: game-screen → (≥ 75 %) діалог бонусу → наступний рівень; (0 життів) → кінець гри.

## Фічі поза полем
- `levels-sequential` нескінченно: +1 атом щорівня, 50 атомів з 49-го.
- Повільні / швидкі атоми — компроміс швидкість ↔ очки (`difficulty-presets` з ціною).
- Нема збережень, undo, редактора (?).

## Варіації й родичі
- `xonix` / Qix — те саме відрізання областей без ворогів, але слідом бігуна; `gals-panic` — відкриття картинки.
- JezzBall Classic (фан-ремейк): особливі атоми (аптечка — +1 життя, заморозка, бонус, генерал телепортує атоми, ракети по кінцях стіни), 83 моди й пресети — Prison (кожен атом в окрему клітку), Divisor (розвести червоні й сині), Artist (малювати стіни), Worker (будівник-повзун).
- **Осі варіацій:** будівник — курсор / бігун зі слідом · стіна — дві половини / одна / малюється · кара — життя / смерть / нічого (Planner у ремейку) · ціль — % поля / кожен атом окремо / розвести кольори.

## Цікавинки для курсу
- Стіна з двох незалежних половин, що ростуть від точки кліку: кожна вразлива окремо — 📎.
- Заливка областей без атомів (flood fill від кожного атома) — 🥈, той самий алгоритм, що в Xonix.
- Діагональне відбивання з окремим розворотом по x і y — 📎.
- Життів стільки, скільки атомів: складність і запас помилок ростуть разом — 🌱.
- Бонус за перевиконання з двома порогами (80 / 90 %) — 🌱.
- Налаштування швидкості як множник очок (повільно = ½) — 🌱.

## Мапа на каталог
- Є: `cell-click` · `player-death` (життя) · `time-out` · `time-bonus` (ремейк) · `event-points` · `sequential-levels` + `progress-acceleration` (+1 атом) · `status-panel` · `game-screen`.
- **Нема** → пропозиції карток:
  - `+region-fill`, `+territory-capture`, `+percent-goal`, `+trail-vulnerable` (є пропозиції з Xonix) — тут вразлива недобудована стіна; `+bounce-move` (є пропозиція з Chip's Challenge) — діагональне відбивання атомів.
  - `+wall-builder-two-ends` «Стіна росте від точки двома половинами» · entities/spawn · 📎 · слот {axis: h|v}.
  - `+lives-per-enemy` «Життів стільки, скільки ворогів» · game-logic/difficulty · 🌱.
  - `+tiered-overshoot-bonus` «Бонус за перевиконання з порогами» · game-logic/score · 🌱 · слот {tiers: [80, 90]}.
  - `+speed-score-tradeoff` «Повільніше — дешевше» · game-logic/difficulty · 🌱 · слот {slow: 0.5}.

## Пропозиції до словників
- `+ui:territory-percent` — частка захопленого (є пропозиція з Xonix; підтверджую).
- `+card:wall-builder-two-ends`, `+card:lives-per-enemy`, `+card:tiered-overshoot-bonus`, `+card:speed-score-tradeoff` — див. «Мапу на каталог».

## Джерела
- ⭐ [Wikipedia: JezzBall](https://en.wikipedia.org/wiki/JezzBall) — правила, життя = атоми, +1 атом, 50 з 49-го рівня, керування мишею, Dima Pavlovsky.
- [Microsoft KB Q98938](https://jeffpar.github.io/kbarchive/kb/098/Q98938) — половина стіни, час за атомами, годинник угорі праворуч, 75 %, очки за клітину, бонуси > 80 / > 90 %, повільні атоми = ½.
- [JezzBall Classic (itch.io)](https://winterdust.itch.io/jezzball-classic) — фан-ремейк: дві половини незалежні, бонус за час і життя, моди й пресети.
- YouTube: пошук «JezzBall gameplay».

## Непевне
- (?) Розмір поля 20 × 28 — виведено з очок KB, не названо прямо.
- (?) Що буває, коли час вичерпано (кінець гри чи втрата життя); чи атоми відбиваються один від одного.
- (?) Меню, статус-рядок, таблиця рекордів, діалог бонусу — з памʼяті, у відкритих джерелах не перевірено.
- (?) Номер Entertainment Pack (пошуковий сніпет каже 4).
- (?) Бонус за час і життя — так у ремейку, що «відтворює оригінальне рахування»; в KB не згадано.
- (?) Чи стартові позиції атомів випадкові (`random: setup`).
