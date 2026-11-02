---
title: Flow Free
slug: flow-free
family: connect-rotate
also: [pencil-logic]
klass: puzzle
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: none
  goal: constraints
year: 2012
platforms: [iOS, Android, Windows Phone, Apple Arcade, Microsoft Store]
links:
  - {kind: official, url: "https://www.bigduckgames.com/flowfree", best: true, note: "офіційна сторінка: правила в 3 рядки, режими"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Flow_Free", note: "розміри полів, perfect-зірка, Bridges/Hexes/Warps/Shapes, дати"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Numberlink", note: "паперовий предок, варіанти правил, NP-повнота"}
  - {kind: official, url: "https://www.bigduckgames.com/bridges", note: "Flow Free: Bridges"}
  - {kind: official, url: "https://www.bigduckgames.com/hexes", note: "Flow Free: Hexes"}
  - {kind: official, url: "https://www.bigduckgames.com/warps", note: "Flow Free: Warps"}
  - {kind: official, url: "https://www.bigduckgames.com/shapes", note: "Flow Free: Shapes"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Flow+Free+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [drag-drop-piece, swipe-gestures, hover-highlight, satisfy-constraints, completion-detection, level-bank, level-select, level-unlock, time-out, difficulty-levels, game-screen, end-screen, +path-drawing, +path-cut, +fill-all-cells, +perfect-rating, +hint-reveal, +bridge-cell, +wrap-edges, +undo-redo, +time-trial]
proposes: ["+role:terminal", "+trigger:input(drag)", "+trigger:all_constraints_met", "+cond:same", "+effect:extend_path", "+effect:cut_path", "+ui:flows-counter", "+ui:pipe-percent", "+ui:move-counter", "+window:pack-select", "+feature:hint", "+card:path-drawing", "+card:path-cut"]
author: opus
date: 2026-11-02
---

# Flow Free — зʼєднай пари однакових кольорів трубами, що заповнюють усе поле

## Суть
На сітці — пари кольорових точок. Гравець пальцем тягне трубу від точки до її пари; труби не перетинаються, а в розвʼязку мусять покрити **кожну** клітину. Це цифрова версія паперової Numberlink, але з живим вводом: нова труба «розрізає» чужу, яку перетнула, тож можна пробувати й відкочувати шляхи жестом. Оцінка — не лише «розвʼязано», а й «perfect»: без зайвих переробок.

## Поле і час
- Квадратна сітка від 5×5 (3 кольори) до 15×15 (до 16 кольорів); частина полів має внутрішні стіни, які треба обходити.
- Один шар клітин; кожна клітина — порожня, точка-термінал або сегмент труби кольору c з напрямами входу/виходу.
- Час статичний (хід = жест); у Time Trial — відлік часу на серію полів.
- Спін-офи міняють топологію: Bridges — клітина-міст (два шари), Hexes — гекси, Warps — обгортання країв, Shapes — клітини довільної форми.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Точка (dot) | terminal (custom) | колір | кінець труби; рівно 2 на колір; пройти крізь неї не можна |
| Труба (flow) | mark | колір, шлях клітин | тягнеться від точки; не розгалужується; без перетинів |
| Порожня клітина | static | — | має бути покрита в розвʼязку |
| Стіна (у частині паків) | static | ребро/клітина | труба не проходить |
| Міст (Bridges) | terrain | 2 канали: ─ і │ | дві різні труби можуть перетнутися лише тут, перпендикулярно |
| Гекс-клітина (Hexes) | static | 6 сусідів | труба може йти в 6 напрямках |
| Отвір на краю (Warps) | terrain | пара країв | труба виходить з одного краю й заходить з протилежного |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag_start, dot|pipe_end)` → ТО `custom: «активна труба цього кольору»`; почати з точки — стара труба цього кольору стирається.
- КОЛИ `input(drag, cell)` → ЯКЩО `free(cell)` → ТО `extend_path(c, cell)`.
- КОЛИ `input(drag, cell)` → ЯКЩО `occupied(cell, pipe[c])` (свій же шлях) → ТО `custom: «обрізати власну трубу до цієї клітини»` (відкат).
- КОЛИ `input(drag, cell)` → ЯКЩО `occupied(cell, pipe[other])` → ТО `cut_path(other, cell)` — чужа труба «ламається» від місця перетину; `extend_path(c, cell)`. Відпустиш палець — розрізана чужа лишається короткою (?).
- КОЛИ `input(drag, cell)` → ЯКЩО `occupied(cell, dot) and not same(dot, c, color)` → ТО `block`.
- КОЛИ `input(drag, dot)` → ЯКЩО `same(dot, c, color)` → ТО `custom: «flow зʼєднано»`, `counter(flows, +1)`, `sound`.
- КОЛИ `input(drag, bridge)` → ЯКЩО `custom: «рух прямо через міст і відповідний канал вільний»` → ТО `extend_path`; повернути на мосту не можна (Bridges).
- КОЛИ `edge(path)` → ЯКЩО `cell(edge, warp)` → ТО `wrap(path)` (Warps).
- КОЛИ `input(drag_start)` → ЯКЩО `not same(color, last_moved)` → ТО `counter(moves, +1)`.
- КОЛИ `all_constraints_met` = усі пари зʼєднані **і** `pipe% = 100` → ТО `win`, `window(end-screen)`; ЯКЩО `counter(moves, ==, flows)` → ТО `custom: «⭐ perfect»`, інакше `custom: «✓»`.
- КОЛИ всі пари зʼєднані, але `pipe% < 100` → ТО `message(«заповни все поле»)` (?) — рівень не зараховано.
- КОЛИ `input(hint)` → ЯКЩО `has(player, hints)` → ТО `custom: «показати один правильний flow повністю»`, `take(hint)`.
- Time Trial: КОЛИ `timer(op, ==, 0)` → ТО `game_over`, `score(puzzles_solved)`.
- Поразки в звичайному режимі нема; рахунок — кількість розвʼязаних, зірки perfect.

## Керування і ввід
- Drag пальцем/мишею від точки або від кінця наявної труби; повернути пальцем назад — скоротити свою трубу; перетнути чужу — розрізати її.
- Кнопки: undo останнього жесту, restart поля, hint, перехід prev/next рівень.
- Гравцеві не треба точно «вести» по центрах: ввід квантується до сусідньої клітини.

## Вікна, меню, HUD
- `main-menu`: Play (Free Play), Time Trial, Daily (?), магазин паків/підказок, налаштування.
- `pack-select` → `puzzle-select`: сітка рівнів пака (за розміром поля) з позначками ✓ / ⭐.
- `game-screen`: поле; зверху — `flows-counter` (зʼєднано x/y), `move-counter` (moves / best), `pipe-percent` (% покриття); знизу — `undo-button`, `restart-button`, `hint-button` з кількістю, стрілки рівнів.
- `end-screen`: «Level complete» / «Perfect!», кнопка Next.
- Time Trial: `mode-select` тривалості (?) і розміру поля → гра з `timer-countdown` → результат з рекордом.
- `settings-window`: звук, кольорові мітки для дальтоніків (?), теми.
- `shop-window`: паки рівнів, підказки, вимкнення реклами.

## Фічі поза полем
- `puzzle-bank` паків (2000+ безкоштовних, платні паки), `stars-rating` (✓/⭐), `level-unlock` всередині пака (?).
- `hint` з обмеженим запасом (покупні); `undo` останнього жесту; `restart-level`.
- `mode-time-attack` (Time Trial), `mode-daily` (щоденні пазли, ?), `stats` — кількість ⭐ по паку.
- `colorblind-palette` (?) — літери на точках для дальтоніків.
- Спін-офи як окремі застосунки: Bridges (2012), Hexes (2016), Warps (2017), Shapes (2024).

## Варіації й родичі
- Numberlink / Arukone (Nikoli) — паперовий предок; Sam Loyd (1897), Dudeney (1917).
- Варіанти Numberlink: лише зʼєднати пари / покрити всі клітини без U-поворотів / покрити всі з U-поворотами.
- Родичі за жестом: Two Dots (лінія через однакові точки), LYNE (один шлях через однакові вузли), The Witness (шлях на панелі).
- Осі варіацій: **покриття: все поле / не обовʼязково** · **перетин: заборонено / мости / на гексах** · **топологія: квадрат / гекс / тор (Warps) / довільні клітини** · **перетин чужої труби: блок / розрізає**.

## Цікавинки для курсу
- Малювання шляху drag-ом з квантуванням до клітин і відкатом назад по своєму шляху — 📎.
- Розрізання чужої труби при перетині (стан кожного кольору — список клітин) — 📎.
- Перевірка розвʼязку: усі пари зʼєднані + 100 % покриття + лічильники flows/moves/pipe% — 🌱.
- Мости як клітина з двома незалежними каналами — 🥉 (два шари в одній клітині).
- Розвʼязувач Numberlink (backtracking з відсіканням «мертвих» областей) — 🥇; генерація з єдиним розвʼязком — 👑.
- Time Trial: серія згенерованих/банкових полів на таймер — 🌱.

## Мапа на каталог
- Є: `drag-drop-piece` (найближче до drag-вводу) · `swipe-gestures` · `hover-highlight` · `satisfy-constraints` · `completion-detection` · `level-bank` · `level-select` · `level-unlock` · `time-out` (Time Trial) · `difficulty-levels` (розмір поля) · `game-screen` · `end-screen`.
- **Нема** → пропозиції карток:
  - `+path-drawing` «Малювання шляху drag-ом по клітинах» · interface/input · 📎 · слоти {backtrack: true, diagonal: false}.
  - `+path-cut` «Новий шлях розрізає чужий» · entities/legality · 📎.
  - `+fill-all-cells` «Покрити всі клітини» · game-logic/win · 🌱.
  - `+perfect-rating` «Оцінка perfect за мінімум ходів» · game-logic/score · 🌱 — ⭐, коли moves = flows.
  - `+hint-reveal` «Підказка відкриває частину розвʼязку» · game-logic/difficulty · 📎 · слот {reveal: one_flow}.
  - `+bridge-cell` «Клітина-міст з двома каналами» · entities/interact · 🥉.
  - `+wrap-edges` «Обгортання країв (тор)» · entities/move · 📎.
  - `+undo-redo` «Undo ходів гравця» · game-logic · 📎.
  - `+time-trial` «Серія пазлів на таймер» · game-logic/difficulty · 🌱.

## Пропозиції до словників
- `+role:terminal` — фіксований кінець шляху (точка Flow, вузол LYNE); від `source` відрізняється тим, що симетричний.
- `+trigger:input(drag)` — ⏳ `input` з аргументом drag: подія по кожній клітині під пальцем.
- `+trigger:all_constraints_met` — підтверджується.
- `+cond:same` ⏳ — однаковий колір точки й труби.
- `+effect:extend_path(c, cell)` — додати клітину до шляху; `+effect:cut_path(c, cell)` — обрізати шлях від клітини.
- `+ui:flows-counter` (зʼєднано x/y), `+ui:pipe-percent` (% покриття); `move-counter` уже ⏳.
- `+window:pack-select` — вибір пака рівнів перед `puzzle-select`.
- `+feature:hint` ⏳ підтверджується (обмежений запас, купівля).

## Джерела
- ⭐ [Flow Free — Big Duck Games](https://www.bigduckgames.com/flowfree) — правила («pipes break if they cross»), Free Play, Time Trial, 2000+ пазлів.
- [Wikipedia: Flow Free](https://en.wikipedia.org/wiki/Flow_Free) — розміри 5×5…15×15, до 16 кольорів, стіни, ✓/⭐ perfect, дати спін-офів.
- [Wikipedia: Numberlink](https://en.wikipedia.org/wiki/Numberlink) — варіанти правил, NP-повнота, історія.
- [Bridges](https://www.bigduckgames.com/bridges) · [Hexes](https://www.bigduckgames.com/hexes) · [Warps](https://www.bigduckgames.com/warps) · [Shapes](https://www.bigduckgames.com/shapes) — офіційні сторінки спін-офів.
- YouTube: пошук «Flow Free gameplay».

## Непевне
- (?) Лічильник moves: «+1, коли береш інший колір, ніж минулого разу» — з памʼяті; Wikipedia каже лише «fewest possible moves».
- (?) Чи лишається розрізана чужа труба короткою після відпускання, чи відновлюється, якщо жест повернувся назад — у грі є відновлення в межах одного жесту (?).
- (?) Повідомлення «заповни все поле», тривалості Time Trial, щоденні пазли, кольорові мітки для дальтоніків, undo — з памʼяті, офіційні сторінки цього не описують.
- (?) Hint показує цілий flow одного кольору — з памʼяті.
