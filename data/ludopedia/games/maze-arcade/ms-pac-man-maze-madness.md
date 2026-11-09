---
title: Ms. Pac-Man Maze Madness
slug: ms-pac-man-maze-madness
aka: [Maze Madness]
family: maze-arcade
also: [push-slide]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: full
  random: runtime
  goal: collect
year: 2000
platforms: [PlayStation, Nintendo 64, Dreamcast, Game Boy Advance]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Ms._Pac-Man_Maze_Madness", best: true, note: "рухомі блоки, вибухові ящики, двері; пружини через стіни; двері за кількість точок; Pac-Dot Radar; Gold Star, Time Trial, боси, Witch's Key, класична Ms. Pac-Man у меню"}
  - {kind: other, url: "https://gamingtarget.com/article.php?artid=1131", note: "рецензія: жодної кнопки, лише рух; блоки, TNT, варпи, ключі, чекпоінти, перемикачі в правильному порядку; до 4 зірок; Ghost Tag, Dot Mania, бомба-«гаряча картопля»"}
  - {kind: other, url: "https://www.gameswelt.de/ms-pacman-paze-madness/test/ms-pacman-paze-madness-3044", note: "рецензія DE: блоки в ями як місток, TNT, рухомі платформи, енергія і чекпоінти, 4 зірки — вихід / 7 фруктів / усі точки / час"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Ms+Pac-Man+Maze+Madness", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [move-by-input, collect-quota, collect-all, reach-exit, item-pickup, temporary-modes, hp-damage, push-object, fill-hole, key-and-door, button-toggle, destructible-blocks, explode-area, teleport, carrier-platform, checkpoint, respawn, minimap-radar, event-points, extra-life-threshold, sequential-levels, level-unlock, main-menu, mode-select, game-screen, ai-opponent, realtime-ai, +spring-over-wall, +dot-count-gate, +stars-per-goal, +hot-potato-bomb, +ghost-tag, +backtrack-key, +bundled-original, +collapsing-bridge, +switch-order-puzzle]
proposes: ["+card:spring-over-wall", "+card:dot-count-gate", "+card:hot-potato-bomb", "+card:backtrack-key", "+feature:bundled-original"]
author: opus
date: 2026-11-09
---

# Ms. Pac-Man Maze Madness — лабіринт Pac-Man як пазл-кімната: блоки в ями, пружини через стіни, двері за кількість точок

## Суть
3D-продовження Ms. Pac-Man, де лабіринт став пазлом: щоб пройти ділянку, треба зʼїсти **достатньо** точок (не всі) — тоді відчиняються двері до наступної частини, а далі дійти до виходу. Дорогу перекривають рухомі блоки (штовхати в ями — вийде місток), вибухові ящики, замкнені двері з ключами, перемикачі в певному порядку, пружини, що перекидають через стіни. Привиди лишились: енерджайзер синить їх, як в аркаді, але дотик не вбиває одразу — знімає енергію. Повний збір (усі точки, усі фрукти, час) дає зірки, якими відкриваються нові рівні.

## Поле і час
- Рівні — великі 3D-лабіринти в чотирьох краях Pac-Land, кожен закритий силовим полем; у кожному — один із чотирьох Gems of Virtue. Рівень ділиться на секції дверима, що відчиняються кількістю зʼїдених точок.
- Пружини перекидають через стіни і часом садять **на верх стіни** — висота є, але рух лабіринтом лишається площинним (?).
- Real-time; камера йде за героїнею; кілька чекпоінтів на рівень.
- Боси: зелений Gobblin і фінальна відьма Mesmerelda; щоб побачити фінал, обох треба перемогти двічі.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Ms. Pac-Man | player | енергія, життя | рух лабіринтом стиком/D-pad; їсть точки, фрукти, привидів під енерджайзером |
| Точка (Pac-Dot) | pickup | — | зʼїдена — +1 до лічильника секції |
| Двері за точки | gate | потрібна кількість | відчиняються, коли зʼїдено досить жовтих точок |
| Енерджайзер (Power Pellet) | pickup | тривалість | вороги синіють — їх можна їсти обмежений час |
| Привид / ворог | enemy | — | дотик знімає енергію; під енерджайзером — зʼїдається |
| Бос (Gobblin, Mesmerelda) | boss | — | окремий бій; перемога дає Witch's Key (?) |
| Рухомий блок | object | — | штовхається; в яму — стає містком |
| Яма | terrain | — | непрохідна; блок у ній — перехід |
| Вибуховий ящик (TNT) | object | — | вибухає і руйнує блоки-перешкоди поруч |
| Руйнівний блок | static | — | зникає від вибуху TNT |
| Двері під ключ і ключ | gate / pickup | — | ключ відчиняє двері |
| Перемикач | switch | порядок | змінює стан лабіринту; часом треба натиснути в правильному порядку |
| Пружина | terrain | напрям | підкидає через стіну, інколи на верх стіни; деякі — на інший рівень лабіринту (?) |
| Варп | terrain | пара | переносить в інше місце |
| Рухома платформа | terrain | маршрут | везе через прірву |
| Міст, що обвалюється; сталактит; камінь, що котиться | hazard | — | шкодять або скидають у прірву (?) |
| Серце | pickup | — | відновлює енергію; інші предмети — +життя, +макс. енергія |
| Фрукти й снеки (7 видів, зокрема крендель) | pickup | — | усі види → зірка |
| Чекпоінт | static | — | точка відродження після смерті |
| Вихід | static | — | кінець рівня, перша зірка |
| Witch's Key | pickup | — | відчиняє місця в уже пройдених краях |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next_cell)` → ТО `move(ms_pac, dir)`.
- КОЛИ `contact(ms_pac, dot)` → ТО `disappear(dot)`, `counter(dots, +1)`, `score(n)`.
- КОЛИ `counter(dots, >=, gate_quota)` → ТО `disappear(dot_gate)` — секція відкрита.
- КОЛИ `contact(ms_pac, power_pellet)` → ТО `set_state(enemy, blue, dur)`.
- КОЛИ `contact(ms_pac, enemy)` → ЯКЩО `state(enemy, blue)` → ТО `disappear(enemy)`, `score(n)`; інакше `damage(ms_pac, n)`.
- КОЛИ `hp_zero(ms_pac)` → ТО `lives(-1)`, `respawn(ms_pac, checkpoint)`.
- КОЛИ `contact(ms_pac, block)` → ЯКЩО `free(cell_behind)` → ТО `push`; інакше `block`.
- КОЛИ `enter(block, hole)` → ТО `disappear(block)`, `set_cell(hole, bridge)`.
- КОЛИ `custom: «TNT вибухає»` → ТО `explode(area, n, empty)` — руйнівні блоки поруч зникають.
- КОЛИ `contact(ms_pac, key)` → ТО `pickup`; КОЛИ `contact(ms_pac, locked_door)` → ЯКЩО `has(ms_pac, key)` → ТО `disappear(locked_door)`, `take(ms_pac, key)` (?); інакше `block`.
- КОЛИ `contact(ms_pac, switch)` → ТО `custom: «змінити стан цілей (двері, платформи)»`; ЯКЩО `custom: «порядок натискань хибний»` → ТО `custom: «скидання»` (?).
- КОЛИ `enter(ms_pac, spring)` → ТО `custom: «стрибок через стіну в напрямку пружини, приземлення за стіною або на ній»`.
- КОЛИ `enter(ms_pac, warp)` → ТО `teleport(ms_pac, pair)`.
- КОЛИ `enter(ms_pac, moving_platform)` → ТО `custom: «їде разом із платформою»`.
- КОЛИ `contact(ms_pac, heart)` → ТО `heal(ms_pac, n)`.
- КОЛИ `reach(ms_pac, exit)` → ТО `custom: «зірка за вихід»`, `next_level`; бонусні зірки — `counter(fruit_types, ==, 7)`, `all_gone(dot)`, Time Trial у ліміт часу.
- КОЛИ `counter(stars, >=, n)` → ТО `custom: «відкрито рівень / бонус-раунд / Movie Player»`.
- КОЛИ `counter(score, step, n)` → ТО `lives(+1)` (очки дають життя (?)).
- КОЛИ `picked(ms_pac, witch_key)` → ТО `custom: «відкриваються закриті місця в попередніх краях»`.
- Мультиплеєр «бомба»: КОЛИ `contact(holder, rival)` → ТО `custom: «бомба переходить до суперника»`; КОЛИ `counter(time, ==, 0)` → ТО `disappear(holder)` — вибуває.
- Мультиплеєр Ghost Tag: `custom: «один гравець — привид, ловить інших»`; Dot Mania: `custom: «хто зʼїв найбільше точок»`.
- Перемога: зібрати 4 Gems of Virtue і двічі перемогти босів. · Поразка: енергія → 0 → мінус життя; життя → 0 → кінець (?). · Рахунок: точки, вороги, предмети; зірки (до 4 на рівень).

## Керування і ввід
- Лише рух: D-pad або аналоговий стик; рецензія наголошує — «жодна кнопка для гри не потрібна» (стрибки — лише пружинами).
- Мультиплеєр: до 4 гравців (multitap); один гравець — проти трьох AI.

## Вікна, меню, HUD
- `main-menu` — три пункти: квест · мультиплеєр · класична Ms. Pac-Man (на GBA класики нема).
- `level-select` / `map-window` — чотири краї з рівнями, частина закрита зірками (?).
- `game-screen` — 3D-лабіринт; HUD: `energy-bar`, `lives`, `score`, `custom: «Pac-Dot Radar»` (куди йти по точки, що лишились), лічильник точок до дверей (?), фрукти.
- `end-screen` рівня — отримані зірки (до 4) (?).
- `custom-window`: бонус-раунди між рівнями; Movie Player (відкривається зірками).
- `mode-select` мультиплеєра: Dot Mania · Ghost Tag · бомба · дуель (?); карти відкриваються проходженням соло.
- `dialogue-window` — відеоповідомлення й голограми Professor Pac (?).
- Переходи: main-menu → квест → вибір рівня → game-screen → вихід → зірки → вибір рівня; main-menu → мультиплеєр → вибір режиму/карти → матч; main-menu → класика → аркадна Ms. Pac-Man.

## Фічі поза полем
- `stars-rating` — до 4 зірок за рівень: вихід, усі 7 фруктів, усі точки, Time Trial; Gold Star за все, Gold Clock за Time Trial.
- `level-unlock` зірками; `mode-time-attack` — Time Trial на пройдених рівнях.
- `collectibles` — фрукти за дверима, які відчиняються пізніше (Witch's Key) → повернення в старі рівні.
- `unlockables` — бонус-раунди, Movie Player, мультиплеєрні карти.
- `mode-versus` / `local-multiplayer` до 4 + `ai-opponent-levels` (три AI-суперники) (?).
- Класична аркадна Ms. Pac-Man як окремий режим — `+feature:bundled-original`.
- Чекпоінти; збереження прогресу (?).

## Варіації й родичі
- `ms-pac-man` — база (аркада вкладена в гру цілком); `pac-man` — енерджайзер і сині привиди.
- Pac-Man World (1999) — 3D-платформер, у головному меню якого так само вкладено аркадний Pac-Man; Maze Madness на відміну від нього лишає лабіринт (окремого файла нема).
- `pac-man-spinoffs` — інші відгалуження «що змінити в Pac-Man»; `super-pac-man` — двері й ключі замість суцільного збору.
- `chips-challenge`, `adventures-of-lolo` — лабіринт-пазл з блоками, ключами й перемикачами; `sokoban`, `kwirk` — блок у дірку як місток.
- **Осі варіацій «Pac-Man як пазл»:** скільки точок треба (усі / квота на двері); як долати стіни (ніяк / пружини / блоки-містки); дотик привида (смерть / мінус енергія); прогрес (рівні підряд / зірки відкривають рівні); повернення в пройдене (нема / ключ відкриває старі місця).

## Цікавинки для курсу
- Двері, що відчиняються лічильником зʼїдених точок секції, — 🌱.
- Блок у яму → місток: `push` + `set_cell` — 📎 (картка `fill-hole`).
- Пружина через стіну з приземленням на стіну — другий шар висоти поверх сітки — 🥉.
- Перемикачі в правильному порядку — послідовність-замок — 📎.
- Енергія замість миттєвої смерті + чекпоінти — 🌱.
- Зірки за різні цілі рівня і відкриття рівнів зірками — 📎.
- «Гаряча картопля»: бомба переходить при дотику, вибухає за таймером — 📎.

## Мапа на каталог
- Є: `move-by-input`; `collect-quota` ↔ точки на двері; `collect-all` ↔ зірка за всі точки/фрукти; `reach-exit`; `temporary-modes` ↔ енерджайзер; `hp-damage` ↔ енергія; `push-object` + `fill-hole` ↔ блоки в ями; `key-and-door`; `button-toggle` ↔ перемикачі; `destructible-blocks` + `explode-area` ↔ TNT; `teleport` ↔ варпи; `carrier-platform` ↔ рухомі платформи; `checkpoint` + `respawn`; `minimap-radar` ↔ Pac-Dot Radar; `level-unlock` ↔ зірки; `ai-opponent` + `realtime-ai` ↔ AI в мультиплеєрі.
- **Нема** → пропозиції карток:
  - `+spring-over-wall` «Пружина перекидає через стіну» · entities/move · 📎 · слот {land_on_wall: bool}.
  - `+dot-count-gate` «Двері за кількістю зібраного» · entities/interact · 🌱 · слот {quota}.
  - `+stars-per-goal` «Зірки за окремі цілі рівня» · progression · 🌱.
  - `+hot-potato-bomb` «Бомба переходить дотиком, вибухає за таймером» · multiplayer · 📎.
  - `+ghost-tag` «Гравець за ворога ловить інших» · multiplayer · 📎.
  - `+backtrack-key` «Пізній ключ відкриває місця в пройдених рівнях» · progression · 🥉.
  - `+collapsing-bridge` «Міст обвалюється» · entities/legality · 📎.
  - `+switch-order-puzzle` «Перемикачі в заданому порядку» · entities/interact · 📎.

## Пропозиції до словників
- `+card:spring-over-wall` — стрибок пружиною через непрохідну клітину.
- `+card:dot-count-gate` — gate, що відчиняється лічильником зібраного (не ключем).
- `+card:hot-potato-bomb` — мультиплеєрна бомба-естафета.
- `+card:backtrack-key` — ключ, що відкриває зони в уже пройдених рівнях (метроїдванія-петля).
- `+feature:bundled-original` — оригінальна аркада як режим усередині ремейку.

## Джерела
- ⭐ [Wikipedia](https://en.wikipedia.org/wiki/Ms._Pac-Man_Maze_Madness) — елементи лабіринтів, Pac-Dot Radar, Gold Star / Time Trial / Gold Clock, боси, Witch's Key, мультиплеєр до 4, класика в меню, платформи й дати.
- [GamingTarget: рецензія](https://gamingtarget.com/article.php?artid=1131) — керування без кнопок, блоки, TNT, варпи, ключі, чекпоінти, порядок перемикачів, до 4 зірок, Ghost Tag, Dot Mania, бомба.
- [Gameswelt: рецензія (DE)](https://www.gameswelt.de/ms-pacman-paze-madness/test/ms-pacman-paze-madness-3044) — блоки в ями як мости, TNT, рухомі платформи, обвали, сталактити, камені, енергія, чекпоінти, чотири зірки, мультиплеєр.
- YouTube: пошук «Ms Pac-Man Maze Madness».

## Непевне
- (?) Чи рух прив'язаний до клітинної сітки (як у Pac-Man World), чи вільний у коридорах — поле записано `square` за логікою блоків-у-ями.
- (?) Пружина «на інший рівень» (GamingTarget) — інший поверх лабіринту чи інший рівень гри.
- (?) Чи двері витрачають ключ; що стається при хибному порядку перемикачів.
- (?) Кількість зірок, потрібних для рівнів; пороги очок за життя; чи є збереження/паролі.
- (?) Назви й точні правила мультиплеєрних режимів розходяться між рецензіями (Ghost Tag / Dot Mania / бомба; Gameswelt згадує ще дуель).
- (?) Чи Witch's Key видає саме перемога над босами (Wikipedia) і що саме він відкриває.
