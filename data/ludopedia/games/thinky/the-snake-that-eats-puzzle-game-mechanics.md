---
title: The Snake That Eats Puzzle Game Mechanics (Thinky Collective)
slug: the-snake-that-eats-puzzle-game-mechanics
aka: [The Snake, The Chain, Metal Gear Liquid 3 Snake Feeder]
family: thinky
also: [maze-arcade, push-slide]
klass: avatar
axes:
  field: square
  time: turn
  opponent: ai
  info: full
  random: none
  goal: state
year: 2026
platforms: [web]
links:
  - {kind: itch, url: "https://thinkycollective.itch.io/the-snake", best: true, note: "грати в браузері; 19 PuzzleScript-пазлів ланцюжком від 17 авторів; керування; коментарі про змію"}
  - {kind: official, url: "https://thinkypuzzlegames.com", note: "Discord-спільнота Thinky Puzzle Games, звідки колектив"}
  - {kind: other, url: "https://tetramouse.itch.io", note: "автор пазла Snake Feeder (Tetramouse)"}
  - {kind: other, url: "https://www.clickmazes.com", note: "автор пазла Disorientation (clickmazes)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=The+Snake+That+Eats+Puzzle+Game+Mechanics+puzzlescript", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [move-4dir, move-by-input, keyboard-controls, swipe-gestures, push-object, fill-hole, chase-bfs, chase-player, body-queue, impassable-cells, touch-death, player-death, undo-unlimited, restart-level, level-select, level-bank, save-progress, collect-all, reach-exit, gravity-fall, ladder-climb, chain-detonation, explode-area, +grow-by-eating, +eat-delay-turn, +sleep-when-no-path, +chain-jam-collection, +eat-to-win]
proposes: ["+effect:step_toward", "+cond:no_path", "+trigger:eaten", "+feature:chain-jam", "+card:eat-delay-turn", "+card:sleep-when-no-path", "+card:chain-jam-collection"]
author: opus
date: 2026-11-09
---

# The Snake That Eats Puzzle Game Mechanics — збірка-ланцюжок PuzzleScript-пазлів; у головному змія після кожного ходу крокує до героя найкоротшим шляхом

## Суть
Колективна збірка спільноти Thinky Puzzle Games (січень–липень 2026): 17 учасників по черзі робили по одноекранному PuzzleScript-пазлу, і кожен отримував шматок попереднього — спрайти або форму рівня; два пазли (Mining Caverns, Closed Circuit) успадкували й механіку. Рамка — велетенська змія, що «їсть механіки»: у вступі гравець згодовує їй предмети-іконки, у фіналі вона їх випльовує. Ядро для корпусу — перший пазл **Metal Gear Liquid 3: Snake Feeder** (Tetramouse): змія після кожного ходу героя робить крок найкоротшим шляхом до нього, яблука її затримують, а герой має засипати бочками всі ями, поки його не зʼїли. Файл описує це ядро повністю, решту пазлів — рядком.

## Поле і час
- Кожен пазл — один рівень на квадратній сітці; Snake Feeder — кімната 13×15 зі стінами-перегородками (з коду).
- Покроково: хід = крок героя; змія рахує шлях і ходить у `late`-фазі того самого ходу, тобто «туди, куди ти щойно став».
- Пазли йдуть у порядку створення, не складності — гра так і каже на старті.

## Сутності
Snake Feeder:
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой | player | — | рух 4 напрямки; штовхає одну бочку; не може стати на яблуко |
| Змія — голова | enemy | рот відкритий / закритий | з відкритим ротом робить крок першою клітиною найкоротшого шляху до героя |
| Змія — тіло й хвіст | enemy | довжина | тіло-черга: хвіст підтягується за головою; уся змія — перешкода |
| Бочка | object | — | штовхається, якщо попереду нема стіни, змії, бочки чи яблука; перешкода для змії |
| Яма (кнопка) | terrain | — | бочка, що стала на яму, зникає разом з ямою |
| Яблуко | pickup | — | непрохідне для героя й бочки; змія його зʼїдає: росте на 1 і пропускає наступний хід |
| Стіна | static | — | непрохідна для всіх |

## Правила (КОЛИ → ЯКЩО → ТО)
Snake Feeder (з коду):
- КОЛИ `input(dir)` → ЯКЩО `occupied(next_cell, apple)` → ТО `block`.
- КОЛИ `contact(player, barrel)` → ЯКЩО `free(cell_behind)` and `not occupied(cell_behind, apple)` → ТО `push`, `move(player, dir)`; інакше `block`.
- КОЛИ `turn_end(player)` → ЯКЩО `state(head, mouth_open)` and `path_exists(head, player)` → ТО `custom: «BFS від голови по клітинах без стін, бочок і змії; крок на першу клітину знайденого шляху»`; яблука для BFS — прохідні, герой — ціль.
- КОЛИ `custom: «голова стала на клітину без яблука»` → ТО `custom: «хвіст підтягується на 1»` (довжина не змінюється).
- КОЛИ `enter(head, apple)` → ТО `disappear(apple)`, `grow(snake, 1)` (хвіст лишається), `set_state(head, mouth_closed, 1)` — наступного ходу змія стоїть.
- КОЛИ `turn_end(player)` → ЯКЩО `custom: «перша клітина шляху — сам герой»` → ТО `disappear(player)`, `set_state(head, mouth_closed)`; без героя перемога неможлива → undo/рестарт.
- КОЛИ `turn_end(player)` → ЯКЩО `not path_exists(head, player)` → ТО `set_state(snake, asleep)` — змія закриває рот і не рухається.
- КОЛИ `adjacent(player, head)` → ЯКЩО `state(snake, asleep)` → ТО `clear_state(snake, asleep)` — прокидається.
- КОЛИ `enter(barrel, hole)` → ТО `disappear(barrel)`, `set_cell(hole, floor)`.
- КОЛИ `all_gone(barrel)` → ЯКЩО `count(player, =, 1)` → ТО `win`.
- КОЛИ `input(Z)` → ТО `undo(1)`; КОЛИ `input(R)` → ТО `restart`; КОЛИ `input(Esc)` → ТО `window(level-select)`.
- Перемога: усі ями засипані, герой живий · Поразка: змія зʼїла героя (мʼяка — undo) · Рахунку нема.

Вступ і фінал (рамка):
- Вступ: КОЛИ `contact(player, food)` → ТО `push` ланцюгом (їжа штовхає їжу); КОЛИ `adjacent(food, head)` → ТО `set_state(head, mouth_open)`; КОЛИ `custom: «їжу заштовхнуто в роззявлений рот»` → ТО `disappear(food)`, `custom: «кулька біжить тілом змії до хвоста»`.
- Вступ: КОЛИ `all_gone(food)` → ЯКЩО `adjacent(player, head)` → ТО `set_state(head, mouth_open)`; КОЛИ `custom: «змія ковтнула героя і кулька дійшла до хвоста»` → ТО `win` («No Player, No Circle»).
- Фінал …And Spits Them Back Out: КОЛИ `input(dir)` → ТО `custom: «рухається кулька всередині тіла змії; рух поперек тіла скасовується»` (?).

## Керування і ввід
- WASD / стрілки — рух (на мобільному — свайп); X / пробіл — дія (тап), потрібна в частині пазлів; Z — undo; R — рестарт; Esc — до вибору пазла.
- У Snake Feeder дії X нема: лише кроки; «чекати» не можна (кожен хід — крок).

## Вікна, меню, HUD
- `puzzle-select` (власна HTML-оболонка «The Chain»): назва пазла, «by автор» з посиланням на його сторінку, превʼю рівня, ряд крапок-прогресу (по одній на пазл, пройдені позначені); гортання вліво/вправо.
- `game-screen`: поле PuzzleScript; HUD нема; кнопки mute/unmute.
- `custom-window` — повідомлення PuzzleScript перед і після пазлів («Fill all the holes with barrels before the snake eats you!»).
- `end-screen` (фінал): «Thank you for playing!» і подяка всім учасникам.
- Переходи: puzzle-select → пазл → (перемога) наступний пазл; Esc → puzzle-select.

## Фічі поза полем
- `puzzle-bank`: 19 пазлів (вступ + 17 авторських + фінал), будь-який порядок.
- Прогрес «пройдено» — у `localStorage` браузера по пазлу; власні збереження PuzzleScript вимкнені.
- `undo` ∞, `restart-level`; `touch-controls` (свайпи, тап).
- Формат створення: chain-jam — кожен учасник успадковує шматок попереднього пазла.

## Варіації й родичі
Пазли збірки (за порядком; ядро — з коду, коротко):
| # | Пазл | Автор | Ядро |
|---|---|---|---|
| 0 | The Snake That Eats Puzzle Game Mechanics… | колектив | вступ: заштовхати «їжу» (яблука, бочки, кнопку, кайло) у пащу змії, потім себе |
| 1 | Metal Gear Liquid 3: Snake Feeder | Tetramouse | ядро файла: змія з BFS, бочки в ями, яблука-затримки |
| 2 | Are Those Power-ups? | xxuurruuii | два режими героя: Down (гравітація, драбини) і Fly (штовхає ящики, удар ящика вибухає); пауер-апи перемикають, драбини ↔ ящики |
| 3 | Snakey Escape | HKMG | герой — змійка-тіло, штовхає ящики ланцюгом; LengthUp / LengthDown міняють довжину; вийти |
| 4 | Mag Trek | maia s ravn | герой-магніт, X міняє полярність; «сильніша сила перемагає, ти трохи сильніший»; магніти на цілі |
| 5 | Screw photosynthesis — HIGH VOLTAGE! | Osi Fisher | батареї + і −: між ними на одній лінії йде промінь; живити всі квіти |
| 6 | Heist at the Crate and [Exploding] Barrel | Aspeon | блок-ґніт, заштовхнутий у блок, вибухає ланцюгом по сусідніх блоках; зібрати самоцвіти |
| 7 | Mining Caverns | Slabdrill | механіка №6, новий рівень |
| 8 | Canary | configurations | гак: X вистрілює мотузку, тягнути стіни за мотузку; яйце в героя |
| 9 | save your Egg and save the Birds! | Monakrom | здібності, крихкі стіни, птахи гинуть від шкоди, яйце крихке |
| 10 | Untitled Circuitry Puzzle | pluf & configurations | дроти й кнопки живлять двері; штовхання й злипання |
| 11 | Closed Circuit | CHz | механіка №10, новий рівень |
| 12 | Disorientation | clickmazes | зібрати монети; хід залежить від орієнтації героя (?) |
| 13 | Turning Older | Pastimeshark | герой обертається, лишаючись керованим; штовхання кількох; кілька типів цілей |
| 14 | My Broken Phaser | Mistafixxa | фазер штовхає й тягне ящики; повернути червоні речі на телепорти |
| 15 | one gun level | bird | постріл «ховає» ящик у рушницю, другий — випускає; падіння |
| 16 | Bul le poisson | dead0ne | риба на суші; X перед лататтям кличе інших риб; бульбашки |
| 17 | Bubble Pond | knexator | бульбашки хапають рибу, лопаються, зникають за краєм |
| 18 | …And Spits Them Back Out | колектив | фінал: кулька всередині змії, змія випльовує «сміття» (?) |

- Родичі ядра: Snake (тіло-черга, ріст від їжі), Theseus and the Minotaur (покроковий переслідувач), Pac-Man (`chase-bfs`), Snakebird (змія в thinky), Sokoban (бочки).
- Осі варіацій переслідувача: **алгоритм** — жадібний / BFS (тут) / A*; **темп** — кожен хід / через хід / подвійний; **що його затримує** — їжа (тут), пастки, двері; **без шляху** — стоїть і чекає (тут) / блукає.

## Цікавинки для курсу
- Покроковий переслідувач з BFS по сітці з перешкодами й відновленням першого кроку — 🥈.
- Змія як тіло-черга, що росте лише при поїданні яблука — 📎.
- Яблуко-затримка: зʼїв → пропускає хід (стан на 1 тік) — 🌱.
- «Сон» без шляху й пробудження, коли герой поруч, — 🌱.
- Бочки як знаряддя: засипати яму або перегородити шлях змії — 📎.
- Оболонка-збірка: список пазлів, автори, прогрес у `localStorage` — 📎.
- Формат chain-jam: успадкувати спрайти / форму рівня попередника — 🌱 (ідея для групового проєкту курсу).

## Мапа на каталог
- Є: `move-4dir` · `move-by-input` · `keyboard-controls` · `swipe-gestures` ↔ ввід; `push-object` ↔ бочки; `fill-hole` ↔ бочка в яму; `chase-bfs` (дитина `chase-player`) ↔ змія; `body-queue` ↔ тіло; `impassable-cells`; `touch-death` · `player-death` ↔ зʼїдено; `undo-unlimited` · `restart-level`; `level-select` · `level-bank` · `save-progress` ↔ оболонка; `collect-all`, `reach-exit`, `gravity-fall`, `ladder-climb`, `chain-detonation`, `explode-area` ↔ інші пазли збірки.
- **Нема** → пропозиції карток:
  - `+grow-by-eating` (уже в корпусі, Can of Wormholes) — змія росте від яблука.
  - `+eat-delay-turn` «Поїдання зупиняє ворога на хід» · entities/state · 🌱.
  - `+sleep-when-no-path` «Переслідувач без шляху засинає до наближення» · entities/move · 🌱.
  - `+chain-jam-collection` «Збірка пазлів з успадкуванням від попередника» · levels/bank · 📎.
  - `+eat-to-win` «Перемога — коли героя зʼїли» (вступ) · game-logic/win · 🌱.

## Пропозиції до словників
- `+effect:step_toward` — сутність робить один крок найкоротшим шляхом до цілі (тут — `custom` з BFS).
- `+cond:no_path` — шляху до цілі нема (зараз `not path_exists`).
- `+trigger:eaten` — сутність проковтнута іншою (зараз `disappear` у правилі змії).
- `+feature:chain-jam` — формат колективної збірки ланцюжком.
- `+card:eat-delay-turn`, `+card:sleep-when-no-path`, `+card:chain-jam-collection` — див. вище.
- ⏳-слова, вжиті тут: `input`, `turn_end`, `enter`, `adjacent`, `all_gone`, `free`, `occupied`, `path_exists`, `state`, `count`, `move`, `grow`, `set_state`, `clear_state`, `set_cell`, `undo`, `restart`, `window`.

## Джерела
- ⭐ [itch: The Snake That Eats Puzzle Game Mechanics](https://thinkycollective.itch.io/the-snake) — опис збірки (Thinky Puzzle Games Discord, січень–липень 2026, порядок створення, успадкування спрайтів / форми рівня), керування, список учасників; коментар M0liusX: «the snake will always take a step towards a shortest path to where you land after you move».
- Код гри — з кадру itch (`html-classic.itch.zone/html/19053177/`, файл `games.js` з `sourceCode` усіх 19 пазлів і оболонкою вибору): правила Snake Feeder (BFS, хвіст, яблука, сон, бочки), вступу й фіналу, умови перемоги всіх пазлів.
- [Thinky Puzzle Games](https://thinkypuzzlegames.com) — спільнота-організатор.

## Непевне
- (?) Однолінійні описи пазлів №2, 8–18 — з коментарів і перших правил коду, без проходження; деталі (особливо Disorientation, Canary, фінал) можуть бути неточні.
- (?) Порядок кроків BFS при рівних шляхах — за порядком правил left → right → up → down; які саме клітини змія обирає в нічиїх, не перевірено в грі.
- (?) Коментатор каже, що в іншому пазлі змія «не вважає бомби перешкодою» — до якого пазла це стосується, не зрозуміло.
- (?) Рік 2026 — за описом (пазли зроблено січень–липень 2026); точна дата публікації невідома.
