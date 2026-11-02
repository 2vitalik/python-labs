---
title: Q*bert
slug: qbert
family: maze-arcade
also: []
klass: avatar
axes:
  field: iso
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: state
year: 1982
platforms: [arcade, Atari 2600, Atari 5200, ColecoVision, C64, NES]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Q*bert", best: true, note: "сутності, очки, бонуси, історія, порти"}
  - {kind: play, url: "https://archive.org/details/arcade_qbert", note: "Internet Arcade — емуляція аркади в браузері"}
  - {kind: official, url: "https://archive.org/stream/Atari5200Manuals_201812/Q-bert%20%28USA%29_djvu.txt", note: "мануал Atari 5200: правила фарбування по рівнях, очки, життя"}
  - {kind: wiki, url: "https://c64-wiki.com/wiki/Q*bert", note: "C64-порт: раунди, вороги, freeze-куля"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=q*bert+arcade+gameplay", note: "пошук; геймплей аркади"}
stage: v1
coverage: 75
mechanics: [move-4dir, touch-death, environment-death, player-death, chase-greedy, random-walk, spawn-points, spawn-schedule, teleport-one-way, temporary-modes, event-points, time-bonus, sequential-levels, progress-acceleration, status-panel, goal-counter, score-records, leaderboard, +paint-cell, +paint-cycle-rules, +paint-revert-enemy, +lure-off-edge, +edge-walker, +freeze-all-enemies, +iso-field]
proposes: ["+effect:paint_step", "+trigger:all_cells", "+trigger:land", "+role:painter", "+ui:target-color", "+window:attract-demo", "+feature:operator-settings", "+card:paint-cycle-rules"]
author: opus
date: 2026-11-02
---

# Q*bert — стрибай по кубах піраміди й перефарбуй усі верхи, тікаючи від змія

## Суть
Q*bert стрибає по діагоналі з куба на куб ізометричної піраміди з 28 кубів; кожне приземлення змінює колір верхньої грані. Раунд виграно, коли всі 28 верхів мають цільовий колір. Ядро — **правило фарбування змінюється по рівнях**: від «один стрибок — готово» до циклу з трьох кольорів, де зайвий стрибок псує вже зроблене. Вороги додають тиск: змій Coily переслідує, кулі котяться згори, Slick і Sam перефарбовують назад, Ugg і Wrongway біжать по бічних гранях.

## Поле і час
- Поле — піраміда з 7 рядів (1+2+…+7 = 28 кубів) в ізометрії; кожен куб має сусідів по 4 діагоналях (вгору-вліво, вгору-вправо, вниз-вліво, вниз-вправо). Стрибок за край піраміди — падіння і смерть.
- Логічно це трикутна сітка: куб (r, c), 0 ≤ c ≤ r; ходи `(r±1, c)` і `(r±1, c±1)` у відповідних парах.
- Поза пірамідою, збоку на рівні певних рядів, висять **летючі диски** — «клітини-виходи» за межею поля.
- Ugg і Wrongway ходять не по верхах, а по **бічних гранях** кубів — окремий «шар» тієї ж піраміди, що перетинає траєкторію Q*bert-а.
- Real-time: Q*bert і вороги стрибають тіками; темп росте з рівнем. Структура: рівень = 4 раунди; рівнів 9, після 9-го повтор найшвидшого (Atari 5200: рівні 6–9 = правило рівня 5, швидше).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Q*bert | player | життя | стрибок по 4 діагоналях; приземлення фарбує куб |
| Куб (верх) | terrain | колір S / I / D | змінює колір при приземленні Q*bert-а за правилом рівня |
| Летючий диск | object | бік, ряд; одноразовий | Q*bert стрибає на нього → летить на вершину; невикористаний = бонус |
| Червона куля | enemy | — | зʼявляється на 2-му ряду, скаче вниз випадково ліво/право, падає з низу |
| Фіолетова куля (яйце) | enemy | — | як червона, але на нижньому ряду вилуплюється в Coily |
| Coily | enemy | — | змій; щострибка — у бік Q*bert-а; стрибає за ним на диск і падає |
| Ugg | enemy | старт справа знизу | біжить по бічних гранях кубів «вбік і вгору», зникає за краєм |
| Wrongway | enemy | старт зліва знизу | дзеркально до Ugg |
| Slick / Sam | enemy | не вбивають | скачуть вниз і повертають кубам вихідний колір; спіймати = очки |
| Зелена куля (freeze) | pickup | — | скаче вниз; спіймав → усі вороги завмирають на кілька секунд |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `cell(target, cube)` → ТО `move(qbert, dir)`; інакше (за краєм і не диск) → `custom: «падіння з піраміди»`, `lose`.
- КОЛИ `enter(qbert, cube)` → ТО `paint(cube, next_color(rule))`, `score(15|25)`:
  - рівень 1: S → D; D лишається D.
  - рівень 2: S → I → D; D лишається D.
  - рівень 3: S → D; **D → S** (повторний стрибок знімає фарбу).
  - рівень 4: S → I → D; **D → I**.
  - рівень 5+: S → I → D; **D → S** (цикл з трьох).
- КОЛИ `custom: «усі 28 верхів мають колір D»` → ТО `win` раунду, `score(round_bonus)`, `score(50 × unused_discs)`, `next_level`.
- КОЛИ `enter(qbert, disc)` → ТО `teleport(qbert, top)`, `disappear_b`.
- КОЛИ `enter(qbert, disc)` → ЯКЩО `in_range(coily, qbert, 1)` → ТО `custom: «Coily стрибає слідом за край»`, `disappear(coily)`, `score(500)`, `custom: «зникають усі вороги й кулі на екрані»`.
- КОЛИ `contact(qbert, red_ball|purple_ball|coily|ugg|wrongway)` → ТО `lose` (життя −1, `message(«@!#?@!»)`), раунд триває з тим самим фарбуванням.
- КОЛИ `contact(qbert, slick|sam)` → ТО `disappear_b`, `score(300)`.
- КОЛИ `enter(slick|sam, cube)` → ТО `paint(cube, S)` (повністю відкочує фарбу).
- КОЛИ `contact(qbert, green_ball)` → ТО `disappear_b`, `score(100)`, `freeze(all_enemies, n)`; на час заморозки дотик безпечний.
- КОЛИ `reach(purple_ball, bottom_row)` → ТО `transform(coily)`.
- КОЛИ `reach(ball|slick|sam, bottom_edge)` → ТО `disappear_a` (зістрибує з піраміди).
- Coily щотік: `chase-greedy` — діагональний крок, що зменшує відстань до Q*bert-а; не обходить край, тому пастка «диск» працює.
- Кулі: `random-walk` вниз — на кожному стрибку випадково ліво/право-вниз.
- Ugg/Wrongway: `custom: «рух по бічних гранях: вбік-вгору від свого кута до протилежного краю»`.
- Перемога: нема (нескінченна аркада), лише раунди. Поразка: 0 життів. Рахунок: 15 за проміжний колір, 25 за цільовий, 300 Slick/Sam, 100 зелена куля, 500 Coily за край, 50 за диск, бонус раунду 1000 + 250 за кожен наступний раунд, стеля 5000.
- Додаткові життя — за порогами очок (налаштування оператора; Atari 5200: 8000, далі кожні 14 000).

## Керування і ввід
- Один 4-позиційний джойстик, **повернутий на 45°** — кожен напрям = діагональ піраміди. Кнопок дії нема.
- Ввід приймається між стрибками: утримання — серія стрибків; помилка напрямку біля краю = смерть (головне джерело втрат).
- Start 1P / 2P — по черзі (альтернативні гравці).

## Вікна, меню, HUD
- `splash-screen` / атракт-режим: демо-гра, таблиця очок за сутності (`custom-window` «хто є хто»), рекорди.
- `game-screen` — піраміда в центрі; HUD: `score` (обох гравців), `level-number` і номер раунду, **цільовий колір** у кутку (`custom: «target-color»`), `lives` (іконки Q*bert-ів), `hi-score`.
- Перед кожним рівнем — інтро-екран з демонстрацією правила: скільки стрибків до цільового кольору (`custom-window` «правило рівня»).
- `end-screen` раунду: миготіння піраміди, нарахування бонусу.
- `leaderboard` — таблиця рекордів з ініціалами.
- Переходи: атракт → (монета, Start) → інтро рівня → game-screen → (раунд) бонус → наступний раунд → … → (0 життів) введення ініціалів → атракт.

## Фічі поза полем
- `levels-sequential` без вибору; `progress-acceleration` — швидкість і кількість ворогів зростають.
- `leaderboard-local` з ініціалами; `hotseat` — 2 гравці по черзі.
- Налаштування оператора (DIP-перемикачі): кількість життів, пороги extra life, складність — `custom: «operator settings»`.
- Нема паузи, збережень, редактора.

## Варіації й родичі
- Порти: Atari 2600 — піраміда на ряд менша; Atari 5200 / ColecoVision — 5 «Games» зі своїм стартом життів; NES — свої раунди. Правила фарбування в портах загалом ті самі.
- Q*bert's Qubes (1983) — куби повертаються, ціль — візерунок граней; Q*bert 3 (SNES), Q*bert Rebooted (2014) — гекс-поле.
- Родичі за механікою «фарбуй клітини»: Amidar, Crush Roller, Xonix (територія), Splatoon. Вісь варіацій **«що робить повторний візит»**: нічого / просуває далі / відкочує на крок / відкочує в нуль / цикл по N кольорах.
- Вісь «хто розфарбовує назад»: ворог-маляр (Slick/Sam), час, сам гравець.

## Цікавинки для курсу
- Ізометрична трикутна сітка 28 кубів і діагональні ходи як 4 напрямки — 📎: координати (r, c), перевірка «чи на піраміді».
- Правило фарбування як параметр рівня (1-крок / 2-крок / toggle / відкат на I / цикл з 3) — 🥉: одна функція `next_color(color, rule)`, 5 таблиць переходів.
- Coily + диск: жадібна погоня, яку можна виманити за край — 🥉: показує, чому жадібний переслідувач вразливий.
- Ворог-«антималяр» Slick/Sam: перевірка завершення стає динамічною — 📎.
- Ugg/Wrongway на бічних гранях — другий шар позицій на тій самій піраміді, зіткнення між шарами — 🥈.
- Freeze-куля: глобальний тимчасовий стан усіх ворогів — 📎 (`temporary-modes`).

## Мапа на каталог
- Є: `move-4dir` (діагоналі) · `touch-death` · `environment-death` (падіння з піраміди) · `player-death` · `chase-greedy` (Coily) · `random-walk` (кулі) · `spawn-points` (2-й ряд) · `spawn-schedule` · `teleport-one-way` (диск → вершина) · `temporary-modes` (freeze) · `event-points` · `time-bonus` (бонус раунду — радше «бонус за раунд») · `sequential-levels` · `progress-acceleration` · `status-panel` · `goal-counter` (цільовий колір) · `score-records` · `leaderboard` · `game-screen`.
- **Нема** → пропозиції карток:
  - `+paint-cell` «Фарбування клітини відвідуванням» · entities/interact · 📎 — Q*bert, Amidar.
  - `+paint-cycle-rules` «Правило зміни кольору як параметр» · entities/interact · 🥉 · слот {rule: once|twice|toggle|back-one|cycle3}.
  - `+paint-revert-enemy` «Ворог стирає прогрес» · entities/interact · 📎.
  - `+lure-off-edge` «Виманити переслідувача за край» · entities/move · 🥉 — Coily і диск.
  - `+edge-walker` «Ворог по іншому шару/грані» · entities/move · 🥈.
  - `+freeze-all-enemies` «Заморозка всіх ворогів предметом» · entities/state · 📎 (дитина `temporary-modes`).
  - `+iso-field` «Ізометричне/трикутне поле» · interface/render · 🥉.

## Пропозиції до словників
- `+effect:paint_step` — просунути колір клітини за правилом (не задати колір, а «наступний»); `paint(cell, color)` не передає цикл.
- `+trigger:all_cells(state)` — усі клітини поля в стані (усі верхи цільового кольору); `all_on` про сутності, не про клітини.
- `+trigger:land(a, cell)` — приземлення після стрибка (на відміну від `enter`, проміжні клітини не рахуються) — Q*bert, платформери.
- `+role:painter` — ворог, що змінює клітини, а не шкодить гравцю (Slick/Sam).
- `+ui:target-color` — зразок мети в куті HUD.
- `+window:attract-demo` — атракт-режим аркади: демо + таблиця очок + рекорди по колу.
- `+feature:operator-settings` — налаштування власника автомата (життя, пороги бонусів).
- `+card:paint-cycle-rules` — див. вище.

## Джерела
- ⭐ [Wikipedia: Q*bert](https://en.wikipedia.org/wiki/Q*bert) — піраміда 28 кубів, вороги, диски, таблиця очок і бонусів, порти.
- [Internet Arcade: Q*bert](https://archive.org/details/arcade_qbert) — грати аркаду в браузері.
- [Мануал Atari 5200](https://archive.org/stream/Atari5200Manuals_201812/Q-bert%20%28USA%29_djvu.txt) — таблиця S/I/D для рівнів 1–5, очки, життя, extra life.
- [C64-Wiki: Q*bert](https://c64-wiki.com/wiki/Q*bert) — раунди по 4, freeze-куля, Coily з фіолетової кулі.
- YouTube: пошук «q*bert arcade gameplay».

## Непевне
- (?) Таблиця S/I/D по рівнях узята з мануалу Atari 5200; для аркади збігається з описами (рівень 4: D → I; 5+: цикл), але покроково не звірено з ROM.
- (?) Стартова кількість життів в аркаді — налаштування оператора (звично 3); у порті 5200 — 3–5 залежно від «Game».
- (?) Точні рівні, з яких зʼявляються Ugg/Wrongway, Slick, зелена куля, та траєкторія Ugg/Wrongway по гранях — описи розходяться.
- (?) Чи Coily при дотику з кулею/Slick щось робить — не знайдено.
