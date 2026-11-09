---
title: Isaac and the Conservation of Momentum
slug: isaac-conservation-of-momentum
aka: [Isaac and the Conservation of Momentum, Momentum (PuzzleScript)]
family: thinky
also: [push-slide]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2021
platforms: [web]
links:
  - {kind: itch, url: "https://menderbug.itch.io/isaac-and-the-conservation-of-momentum", best: true, note: "грати в браузері; джем, версії, кредити, лінки на код"}
  - {kind: other, url: "https://github.com/broken-sign-games/thinky-puzzle-game-jam-2021", note: "репозиторій: momentum.puzzlescript, momentum-bonus, momentum-solver"}
  - {kind: other, url: "https://raw.githubusercontent.com/broken-sign-games/thinky-puzzle-game-jam-2021/main/momentum.puzzlescript", note: "сирий код: обʼєкти, правила імпульсу, 36 рівнів з коментарями"}
  - {kind: play, url: "https://broken-sign-games.github.io/PuzzleScript/play.html?p=f450ad190eeb08e6ee28702843868667", note: "джемова версія"}
  - {kind: itch, url: "https://menderbug.itch.io/isaac-and-the-conservation-of-mass", note: "наступник 2022: желейні блоки, Pattern:Script"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Isaac+and+the+Conservation+of+Momentum+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [move-4dir, move-by-input, push-object, inertia-slide, floor-types, environment-death, player-death, death-animation, all-on-targets, impassable-cells, undo-unlimited, restart-level, sequential-levels, skip-level, keyboard-controls, sound-effects, movement-animation, +momentum-transfer, +mass-threshold, +chain-push]
proposes: ["+card:momentum-transfer", "+card:mass-threshold", "+effect:transfer_momentum", "+window:title-screen"]
author: opus
date: 2026-11-09
---

# Isaac and the Conservation of Momentum — Sokoban з кулями, що котяться до упору й передають імпульс, як колиска Ньютона

## Суть
Ісаак штовхає кулі на цілі, але штовхнута куля не зупиняється за крок: вона котиться, доки її не спинить стіна, пісок або інша куля. Зіткнення з нерухомою кулею — як у колисці Ньютона: перша стає, друга котиться далі. Металева куля «важка»: їй потрібно дві одиниці імпульсу, тож дерев'яна її не зрушить, а сама металева бʼє далі. Ями ковтають кулі (і героя), пісок гасить рух.

## Поле і час
- Квадратна сітка, один екран на рівень; 36 рівнів у коді (+ закоментовані чорновий і обкладинка).
- Шари колізій (з коду): фон → пісок / яма (+ декор) → падіння / ціль → гравець, стіна, кулі → службові маркери імпульсу й декор стін.
- Хід = ввід гравця; далі світ «дограє» через `again`: правило `late [Momentum] -> [Momentum] again` повторює фазу, доки на полі лишається хоч один маркер імпульсу. Тобто вся прокатка — в межах одного ходу, з покадровою анімацією.
- Імпульс — невидимий маркер на кулі `Momentum1R/L/U/D` або `Momentum2…` (одна / дві одиниці + напрямок).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Ісаак (`Player`) | player | — | крок 4 напрямки; штовхає кулю (і ряд куль); падає в яму |
| Деревʼяна куля (`WoodenBall`) | object | імпульс 0/1 | штовхнута — отримує 1 одиницю й котиться до упору |
| Металева куля (`MetalBall`) | object | імпульс 0/1/2 | штовхнута героєм — 2 одиниці; з 1 одиницею стоїть (інерція); віддає 1 одиницю й зупиняється |
| Стіна (`Wall`) | static | — | непрохідна; гасить імпульс кулі, що вдарилась |
| Пісок (`Sand`) | terrain | — | по ньому ходять; куля, що в'їхала, втрачає весь імпульс |
| Яма (`Pit`) | hazard | — | куля чи герой, що опинились на ній, падають за 3 кадри й зникають; яма лишається |
| Ціль (`Target`) | static | контур кола | на кожній має лежати куля |
| Маркер імпульсу (`Momentum1/2 R/L/U/D`) | mark | одиниці, напрямок | службовий; без кулі знищується |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(cell_ahead)` → ТО `move(player, dir)`; на піску — `sound(sand_step)`.
- КОЛИ `contact(player, ball)` → ТО `push`; ряд куль попереду рушає разом («pushing multiple balls at once»), упор у стіну → `block`.
- КОЛИ `custom: «деревʼяна куля рушає в напрямку d»` → ТО `custom: «поставити маркер Momentum1 d»`.
- КОЛИ `custom: «металева куля рушає в напрямку d»` → ТО `custom: «поставити маркер Momentum2 d»`.
- КОЛИ `tick` → ЯКЩО `custom: «на кулі є маркер імпульсу d»` → ТО `move(ball, d)` — куля котиться далі (`again`).
- КОЛИ `custom: «куля з імпульсом 1 впирається в нерухому кулю»` → ТО `custom: «імпульс переходить до другої кулі, перша стає»` (колиска Ньютона; ряд куль — імпульс доходить до останньої).
- КОЛИ `custom: «металева куля з імпульсом 2 впирається в нерухому кулю»` → ТО `custom: «обидві отримують по 1 одиниці»`; деревʼяна котиться, металева з 1 одиницею далі стає.
- КОЛИ `custom: «металева куля з імпульсом 2 впирається в металеву, що отримала 1»` → ТО `custom: «друга отримує 2, перша лишається з 1»` — металева передає металевій повний удар.
- КОЛИ `custom: «на металевій кулі лише 1 одиниця»` → ТО `custom: «маркер знімається»` — деревʼяна не зрушить металеву.
- КОЛИ `custom: «куля з імпульсом упирається в стіну»` → ТО `custom: «імпульс знімається»`, `sound(wall_hit)`.
- КОЛИ `enter(ball, sand)` → ТО `custom: «імпульс знімається повністю»`, `sound(sand)`.
- КОЛИ `enter(ball, pit)` → ТО `animate(fall, 3)`, `disappear_a`; яма не засипається.
- КОЛИ `enter(player, pit)` → ТО `animate(fall, 3)`, `disappear_a` — герой зникає, лишається undo/restart.
- КОЛИ `settled` (імпульсу нема, жодна куля не падає) → ЯКЩО `all_on(ball, target)` → ТО `win`, `next_level` (умови коду: «All Target on Ball», «No Momentum», «No FallingBall»).
- Перемога: на кожній цілі куля, усе зупинилось · Поразки як стану нема (герой у ямі = глухий кут) · Рахунку нема.

## Керування і ввід
- Стрілки / WASD — крок і поштовх; `noaction` — кнопки дії нема.
- `Z` — undo, `R` — рестарт (стандарт PuzzleScript); пропуск рівня — є (за коментарем гравця), вибору рівня в релізі нема.

## Вікна, меню, HUD
- `title-screen` (custom, стандарт PuzzleScript): назва, автор Menderbug, start / continue.
- `game-screen`: поле з перспективними спрайтами (палітра Resurrect 64 + колір ям), без HUD.
- Переходи: title → рівні підряд → фінальний «Victory lap» → title (?).

## Фічі поза полем
- `undo` ∞, `restart-level`, `skip-level` (без ліміту?) — відповідь автора на складні рівні.
- `levels-sequential`: 36 рівнів; кожна нова ідея — окремий вступний рівень (коментарі коду: momentum → transfer → кілька куль → ями → зупинка над ямою → пісок → металеві кулі → металеві на піску → Victory lap).
- У репозиторії поруч — `momentum-solver.puzzlescript` (розвʼязувач/перевірка рівнів) і `momentum-bonus.puzzlescript`.
- Власний форк редактора PuzzleScript автора (легше працювати з перспективними спрайтами).

## Варіації й родичі
- Наступник: Isaac and the Conservation of Mass (2022, Thinky Puzzle Game Jam 2) — желейні блоки, рушій Pattern:Script.
- Родичі в корпусі: [Ice sliding puzzles](../push-slide/ice-sliding-puzzles.md) і [Pengo](../push-slide/pengo.md) (ковзання до упору), [Sokoban](../push-slide/sokoban.md), [Kwirk](../push-slide/kwirk.md) (ями), [Golf Peaks](golf-peaks.md) (кулька з заданим запасом руху).
- Осі варіацій: **що гасить рух** — стіна / тип підлоги (пісок) / інша куля; **маса** — одна / дві (метал потребує 2 одиниць) / довільна; **удар по кулі** — зупинка (колиска) / відскок / обидві котяться; **яма** — ковтає / засипається (Kwirk) / пропускає на швидкості.

## Цікавинки для курсу
- Імпульс як маркер «одиниці + напрямок» на обʼєкті й дограш світу до стабілізації в межах ходу — 🥉.
- Колиска Ньютона: передача імпульсу по ряду куль до останньої — 📎.
- Маса через поріг: металевій потрібно 2 одиниці, віддає 1 і стає — 🥉 (таблиця взаємодій 2×2 матеріалів).
- Пісок як підлога, що гасить рух, і яма як знищувач — 🌱.
- Умова перемоги «усе зупинилось» (No Momentum) — 🌱.
- Розвʼязувач з симуляцією прокатки на кожному кроці BFS — 🥇.

## Мапа на каталог
- Є: `move-4dir` · `move-by-input` · `push-object` · `inertia-slide` (кулі до упору) · `floor-types` (пісок) · `environment-death` + `player-death` + `death-animation` (яма, 3 кадри) · `all-on-targets` · `impassable-cells` · `undo-unlimited` · `restart-level` · `sequential-levels` · `skip-level` · `keyboard-controls` · `sound-effects` (окремі звуки дерево/метал/стіна/пісок/яма) · `movement-animation`.
- **Нема** → пропозиції карток:
  - `+momentum-transfer` «Удар передає імпульс (колиска Ньютона)» · entities/move · 🥉 · слоти {mode: stop|both_move, chain: bool}.
  - `+mass-threshold` «Обʼєкт рушає лише від імпульсу ≥ маси» · entities/move · 🥉 · слот {mass: 1..n}.
  - `+chain-push` (див. Heroes of Sokoban) — штовхання ряду куль.

## Пропозиції до словників
- `+effect:transfer_momentum` — передати одиниці імпульсу іншій сутності в напрямку удару.
- `+card:momentum-transfer`, `+card:mass-threshold` — див. вище.
- `+window:title-screen` — повтор (Mirror Isles).
- Слова словників, вжиті тут: `settled` (🔥), `input`, `tick`, `enter`, `free`, `move`, `animate`, `sound`, `all_on`, `next_level`, ролі `terrain`, `hazard`, `mark`.

## Джерела
- ⭐ [Сторінка на itch.io](https://menderbug.itch.io/isaac-and-the-conservation-of-momentum) — гра, Thinky Puzzle Game Jam (перший), версії 1.1/1.2 (5 і 9 липня 2021), кредити, лінки на код і форк редактора; матеріали з коментарів (дерево, пісок, ями, метал).
- [Репозиторій джему](https://github.com/broken-sign-games/thinky-puzzle-game-jam-2021) і [сирий momentum.puzzlescript](https://raw.githubusercontent.com/broken-sign-games/thinky-puzzle-game-jam-2021/main/momentum.puzzlescript) — обʼєкти, шари, правила імпульсу, передачі, піску, ям, умови перемоги, 36 рівнів з коментарями.
- [Isaac and the Conservation of Mass](https://menderbug.itch.io/isaac-and-the-conservation-of-mass) — наступник 2022.

## Непевне
- (?) «Stopping over a pit» (коментар рівня): як куля зупиняється над ямою й не падає — за правилами коду будь-яка куля на ямі падає; можливо, мова про кулю, що зупинилась на ямі й заповнила «прохід» на мить, — не перевірено в грі.
- (?) Правило ланцюгового поштовху ряду куль героєм у фетчі не процитоване дослівно — виведено з коментаря рівня.
- (?) Пропуск рівня: коментар гравця каже, що є skip без вибору; кредити згадують level selector Draknek — розбіжність.
- (?) Черга дала рік 2023 — сторінка і код кажуть 2021 (перший Thinky Puzzle Game Jam).
- (?) Імʼя героя «Isaac» (Ньютон) — з назви; у коді обʼєкт зветься `Player`.
