---
title: Quoridor (Кворидор)
slug: quoridor
family: chess-abstract
also: [board-digital]
klass: figure
axes:
  field: square
  time: turn
  opponent: hotseat
  info: full
  random: none
  goal: race
year: 1997
platforms: [board, web]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Quoridor", best: true, note: "правила 2/4 гравці, стрибок, стіни, заборона повністю перекрити шлях, AI-дослідження"}
  - {kind: official, url: "https://en.gigamic.com/game/quoridor", note: "Gigamic: склад коробки (20 стін, 4 пішаки), правила PDF"}
  - {kind: official, url: "https://en.gigamic.com/index.php?controller=attachment&id_attachment=467", note: "офіційна книжка правил (PDF, лінк зі сторінки Gigamic)"}
  - {kind: play, url: "https://en.boardgamearena.com/gamepanel?game=quoridor", note: "Board Game Arena — 2 або 4 гравці, 10/5 стін"}
  - {kind: other, url: "http://modelai.gettysburg.edu/2014/mpgames/website.html", note: "навчальний проєкт: студенти пишуть AI-гравця Quoridor; правила з L-стрибком"}
  - {kind: other, url: "https://upcommons.upc.edu/bitstream/handle/2117/127676/131875.pdf", note: "Respall 2018: MCTS для Quoridor (лінк зі статті Wikipedia)"}
  - {kind: other, url: "https://boardgamegeek.com/boardgame/624/quoridor", note: "BGG (з черги куратора)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=quoridor+how+to+play", note: "пошук; правила"}
stage: v1
coverage: 85
mechanics: [move-4dir, reachability-check, chase-bfs, hot-seat, turn-enforcement, move-timer, ai-opponent, ai-greedy, ai-minimax, cell-click, hover-highlight, legal-move-highlight, drag-drop-piece, game-screen, main-menu, end-screen, help-window, settings-window, difficulty-levels, replay, +edge-walls, +wall-supply, +pawn-jump, +reach-row-win, +move-or-build, +move-notation]
proposes: ["+cond:path_exists", "+cond:wall_between", "+effect:place_wall", "+ui:wall-counter", "+ui:wall-ghost", "+ui:path-length", "+window:player-count-select", "+axis:field-edges", "+card:edge-walls", "+card:pawn-jump", "+card:move-or-build"]
author: opus
date: 2026-11-02
---

# Quoridor — біжи пішаком на протилежний край або постав стіну на шляху суперника

## Суть
На полі 9×9 кожен гравець має пішака і запас стін завдовжки дві клітини. Хід — **або** крок пішаком, **або** стіна в паз між клітинами; стіни вічні й не можуть повністю відрізати жодного пішака від його цільового краю. Хто першим дійде до протилежного ряду — виграв. Гра — це перегони найкоротших шляхів, які обидва постійно переписують стінами.

## Поле і час
- Квадратне поле 9×9 (81 клітина). Між клітинами — **пази**: стіни лежать на ребрах, а не в клітинах (поле = клітини + сітка ребер, 8×8 точок перетину).
- Стіна займає 2 сусідні ребра і точку між ними; стіни не перетинаються й не накладаються (у т. ч. хрест у спільній точці).
- Старт на двох: пішаки в центрі своїх крайніх рядів (e1 і e9); на чотирьох — центри всіх чотирьох сторін (e1, a5, e9, i5). Ціль — будь-яка клітина протилежного краю.
- Запас: 20 стін ділять порівну — 10 на двох, 5 на чотирьох.
- Покроково; на змаганнях — годинник, вийшов час = поразка.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Пішак | piece | сторона, цільовий край | крок на 1 ортогонально; стрибок через сусіднього пішака; не проходить крізь стіни |
| Стіна | static | орієнтація H/V, точка центру; на ребрах | блокує рух через 2 ребра; ставиться назавжди |
| Запас стін | resource | 10 (2 гравці) / 5 (4 гравці) | зменшується при кожній стіні; 0 → лише ходи пішаком |
| Цільовий край | zone | ряд/стовпець 9 клітин | пішак власника, що став на будь-яку клітину, виграє |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(side)` → ТО гравець обирає одне: рух пішака **або** стіна (`custom: «move-or-build»`).
- КОЛИ `input(move, pawn, dir)` → ЯКЩО `free(cell)` і `not wall_between(pawn, cell)` → ТО `move(pawn, cell)` (лише ортогонально).
- КОЛИ `input(move, pawn, dir)` → ЯКЩО `occupied(cell, pawn2)` і `not wall_between` → ТО ЯКЩО клітина за pawn2 вільна і без стіни → `move(pawn, cell+2)` (стрибок по прямій); інакше `custom: «L-стрибок: клітина ліворуч або праворуч від pawn2»`.
- Через двох пішаків поспіль і через стіну стрибати не можна (на чотирьох — не більше одного суперника).
- КОЛИ `input(place_wall, edge_pair)` → ЯКЩО `has(side, wall)` і `custom: «пази вільні, нема перетину з іншою стіною»` і `path_exists(every_pawn, its_goal_edge)` після встановлення → ТО `custom: «поставити стіну»`, `counter(walls[side], -1)`; інакше `block`.
- Стіни не рухаються й не знімаються до кінця партії.
- КОЛИ `reach(pawn, goal_edge)` → ТО `win`.
- КОЛИ `timer(clock[side]) == 0` → ТО `lose`.
- Пасу нема: хід пішаком майже завжди можливий, бо шлях до цілі гарантовано існує (?).
- Перемога: першим на протилежний край · Поразка: суперник раніше / час · Рахунок: нема.

## Керування і ввід
- Настільна: пересунути пішака або вставити планку-стіну в паз.
- (цифрова версія) Два режими вводу: клік/drag пішака на підсвічену клітину (вкл. клітини стрибка) **або** наведення між клітинами показує `wall-ghost` (H/V перемикається клавішею, колесом чи позицією курсора), клік ставить; нелегальна стіна — червоний привид.
- Черга: 2 гравці по черзі; 4 — за годинниковою стрілкою.

## Вікна, меню, HUD
- (цифрова версія) `main-menu`: Грати → `player-count-select` (2/4) → суперники (людина / AI з рівнем); Онлайн → `lobby-window` (BGA); Правила → `help-window`.
- (цифрова версія) `game-screen`: поле 9×9 з пазами, пішаки, `wall-counter` кожного гравця (скільки стін лишилось), `turn-indicator`, `legal-move-highlight` для пішака, `wall-ghost`, `path-length` (довжина найкоротшого шляху кожного — підказка (?)), `move-list` у нотації (e2, e3h…), `undo-button` проти AI, `player-clock`.
- (цифрова версія) `end-screen`: хто дійшов, кількість ходів, реванш.
- (цифрова версія) `settings-window`: кількість гравців, рівень AI, показ шляхів/підсвіток.
- Переходи: main-menu → player-count-select → game-screen → end-screen.

## Фічі поза полем
- `hotseat` / `local-multiplayer` на 2 або 4; `online-multiplayer` (BGA: 2 або 4, 10/5 стін); `turn-timer`.
- `ai-opponent-levels`: Quoridor — популярна ціль студентських AI (minimax з евристикою «різниця найкоротших шляхів», MCTS у дипломних роботах).
- `undo`, `replay`, `history`, `export-import` партій у нотації.
- `tutorial`, `rules-page`.

## Варіації й родичі
- Quoridor Kid (2004) — кругле поле 7×7, 16 стін (8/4), тема мишей і сиру.
- Попередник Marchesi — Pinko Pallino (?); старший родич — Blockade (1975) з пішаками й стінами (?).
- Онлайн-ігри для ботів: CodinGame «The Great Escape» — Quoridor на 3–4 ботів (з черги корпусу).
- Осі варіацій: **кількість гравців** (2 / 4, запас ділиться) · **розмір поля** (9×9 / 7×7) · **стрибок** (лише прямо / L-стрибок / через кількох) · **заборона повного перекриття** (є / нема — тоді гра може зайти в глухий кут) · **довжина стіни** (2 / 3).
- Родичі: Hex (будуєш зʼєднання й водночас блокуєш), Labyrinth (змінне поле лабіринту), Ricochet Robots (стіни на ребрах).

## Цікавинки для курсу
- Стіни на **ребрах** клітин (окремий масив горизонтальних/вертикальних пазів + перевірка перетину в точці) — 🥉.
- Легальність стіни через BFS «чи дійде кожен пішак до свого краю» — 🥈 (BFS на кожну спробу; оптимізація — перевіряти лише стіни, що зачіпають поточний найкоротший шлях — 🥇).
- Стрибок через пішака з L-відступом, якщо за ним стіна/край — 📎 (багато крайових випадків).
- Вибір ходу «рух або будівництво» з обмеженим запасом — 🌱.
- AI: жадібний «крок по найкоротшому шляху» — 🥉; minimax з оцінкою `dist(суперник) − dist(я)` і генерацією ~130 стін — 🥇.
- Режим на 4 гравців з 4 різними цілями — 📎.

## Мапа на каталог
- Є: `move-4dir` ↔ крок пішака · `reachability-check` ↔ заборона перекрити шлях · `chase-bfs` ↔ найкоротший шлях для AI · `hot-seat` + `turn-enforcement` · `move-timer` · `ai-opponent` / `ai-greedy` / `ai-minimax` · `cell-click` + `hover-highlight` + `legal-move-highlight` + `drag-drop-piece` · `game-screen`, `main-menu`, `end-screen`, `help-window`, `settings-window` · `difficulty-levels` · `replay`.
- **Нема** → пропозиції карток:
  - `+edge-walls` «Стіни на ребрах клітин» · entities/legality · 🥉 · слот {length: 2} — перешкода між клітинами, не в клітині (Quoridor, Ricochet Robots, тонкі стіни Chip's Challenge).
  - `+wall-supply` «Обмежений запас будівель» · game-logic/economy · 🌱 · слот {count: 10} — лічильник предметів, які можна виставити.
  - `+pawn-jump` «Стрибок через фігуру» · entities/move · 📎 · слот {side_step: bool} — прямо через сусіда, з бічним відступом, коли за ним перешкода.
  - `+reach-row-win` «Дійти до протилежного краю» · game-logic/win · 🌱 — ціль-зона, а не одна клітина (дитина `reach-exit`).
  - `+move-or-build` «Хід: рух або будівництво» · game-logic/opponent · 🌱 — вибір типу дії в межах ходу.

## Пропозиції до словників
- `+cond:path_exists` — існує шлях від сутності до зони (легальність стіни; спільне з Hex).
- `+cond:wall_between` — між двома сусідніми клітинами стоїть стіна на ребрі.
- `+effect:place_wall` — поставити перешкоду на ребро/ребра (не `set_cell`, бо клітини не змінюються).
- `+ui:wall-counter` — лишилось стін у кожного; `+ui:wall-ghost` — привид стіни, що показує легальність; `+ui:path-length` — довжина найкоротшого шляху.
- `+window:player-count-select` — вибір 2/4 гравців і хто з них AI.
- `+axis:field-edges` — поле з окремим шаром ребер (стіни між клітинами): Quoridor, Ricochet Robots, тонкі стіни.
- `+card:edge-walls`, `+card:pawn-jump`, `+card:move-or-build` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Quoridor](https://en.wikipedia.org/wiki/Quoridor) — поле, старт на 2/4, хід пішаком або стіною, стрибок і бічний відступ, заборона відрізати шлях, перемога, годинник, Quoridor Kid, AI-тези.
- [Gigamic: Quoridor](https://en.gigamic.com/game/quoridor) — офіційна сторінка: 2–4 гравці, 20 стін, 4 пішаки.
- [Gigamic: Rulebook PDF](https://en.gigamic.com/index.php?controller=attachment&id_attachment=467) — офіційні правила (лінк бачив, не відкривав).
- [Board Game Arena: Quoridor](https://en.boardgamearena.com/gamepanel?game=quoridor) — онлайн на 2 або 4; 10 і 5 стін.
- [Gettysburg Model AI: Quoridor](http://modelai.gettysburg.edu/2014/mpgames/website.html) — навчальний проєкт «напиши гравця»: правила з L-стрибком, «доступ до цілі завжди відкритий».
- [Respall 2018 (UPC)](https://upcommons.upc.edu/bitstream/handle/2117/127676/131875.pdf) — MCTS-агент (лінк зі статті Wikipedia).
- [BoardGameGeek: Quoridor](https://boardgamegeek.com/boardgame/624/quoridor) — картка гри (з черги куратора).
- YouTube: пошук «quoridor how to play».

## Непевне
- (?) Чи може статися, що пішак не має жодного легального кроку (оточений пішаками і стінами) — правила про пас не знайшов.
- (?) Pinko Pallino як попередник (BGG 7581 у лінках Wikipedia) і Blockade (1975) як родич — з памʼяті.
- (?) Показ довжини найкоротшого шляху в HUD — є в деяких цифрових версіях, конкретну не перевіряв.
- (?) На чотирьох — чи можна стрибати лише через суперника чи через будь-якого пішака: джерела кажуть «не більше одного».
