---
title: Advent of Code — сіткові пазли (збірка)
slug: advent-of-code-grids
family: program-robots
also: [push-slide, dig-gravity, connect-rotate, build-sim, falling-match]
klass: hybrid
axes:
  field: square
  time: programmed
  opponent: none
  info: full
  random: setup
  goal: state
year: 2015
platforms: [web]
links:
  - {kind: play, url: "https://adventofcode.com/2024/day/15", best: true, note: "Warehouse Woes: Sokoban-склад з текстовою мапою й рядком ходів — найшвидший вхід у формат AoC"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Advent_of_Code", note: "формат події: дві частини, зірки, персональний ввід; з 2025 — 12 днів і без глобального лідерборду"}
  - {kind: official, url: "https://adventofcode.com/2024/about", note: "про подію: Eric Wastl, будь-яка мова, приклади в умові"}
  - {kind: play, url: "https://adventofcode.com/2018/day/15", note: "Beverage Bandits: гобліни vs ельфи, порядок читання, BFS"}
  - {kind: play, url: "https://adventofcode.com/2018/day/13", note: "Mine Cart Madness: вагонетки, перехрестя ліво-прямо-право"}
  - {kind: play, url: "https://adventofcode.com/2019/day/24", note: "Planet of Discord: Life 5×5, у другій частині — рекурсивні сітки"}
  - {kind: play, url: "https://adventofcode.com/2022/day/14", note: "Regolith Reservoir: падаючий пісок"}
  - {kind: play, url: "https://adventofcode.com/2022/day/17", note: "Pyroclastic Flow: тетріс із вітром"}
  - {kind: play, url: "https://adventofcode.com/2022/day/22", note: "Monkey Map: обгортання краю → розгортка куба"}
  - {kind: play, url: "https://adventofcode.com/2023/day/16", note: "The Floor Will Be Lava: промені, дзеркала, розщеплювачі"}
  - {kind: play, url: "https://adventofcode.com/2024/day/6", note: "Guard Gallivant: патруль «впершись — праворуч»"}
  - {kind: play, url: "https://adventofcode.com/2024/day/14", note: "Restroom Redoubt: роботи зі швидкістю на торі"}
  - {kind: play, url: "https://adventofcode.com/2024/day/21", note: "Keypad Conundrum: роботи натискають клавіатури роботів"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=advent+of+code+visualization+grid", note: "пошук; візуалізації розвʼязків"}
stage: v1
coverage: 70
mechanics: [level-from-txt, push-object, multi-cell-size, gravity-fall, inertia-slide, impassable-cells, enemy-patrol, chase-bfs, hp-damage, piece-capture, teleport, unsolvable-states, state-as-data, game-loop, unit-tests, fixture-level-tests, console-render, +reading-order-tiebreak, +turn-when-blocked, +intersection-turn-cycle, +collision-detect, +cellular-automaton-rule, +recursive-grid, +falling-sand, +jet-push, +cycle-detection, +cube-net-wrap, +torus-wrap, +beam-tracing, +mirror-reflect, +beam-split, +loop-detection, +velocity-wrap, +emergent-picture, +chain-push-wide, +control-chain-keypads, +answer-checksum, +two-part-puzzle]
proposes: ["+trigger:tick", "+trigger:turn_start(side)", "+trigger:blocked", "+trigger:repetition", "+trigger:beam_hit", "+cond:free", "+cond:facing", "+cond:adjacent_count", "+cond:reading_order", "+effect:move", "+effect:face", "+effect:fall", "+effect:wrap", "+effect:split_beam", "+effect:reflect", "+effect:push_chain", "+effect:press(key)", "+role:terrain", "+role:projectile", "+window:puzzle-page", "+window:answer-form", "+ui:star-calendar", "+feature:personal-input", "+feature:two-part-reveal", "+feature:private-leaderboard", "+axis:control", "+axis:session"]
author: opus
date: 2026-11-02
---

# Advent of Code: сіткові пазли — щоденні симуляції клітинних світів, розвʼязувані програмою

## Суть
Advent of Code (Eric Wastl, з 2015) — адвент-календар програмістських задач: щодня задача з двох частин, персональний текстовий ввід, відповідь — одне число чи рядок, за кожну частину — зірка. Чимала частка задач — **клітинні ігри без інтерфейсу**: умова описує правила світу (бій гоблінів і ельфів, вагонетки, падаючий пісок, тетріс із вітром, склад-Sokoban), ввід — рівень у ASCII, а «гра» — твоя програма-симулятор. Цей файл — парасолька: кожна задача — рядок таблиці сутностей і блок правил. Друга частина зазвичай ламає «наївну» симуляцію (мільярд кроків, рекурсивні сітки, куб) і вимагає алгоритму.

## Поле і час
- Поле — ASCII-сітка з входу (`#` стіна, `.` пусто, літери/стрілки — сутності); координати — від лівого верхнього кута, y вниз.
- Топології: прямокутник з краєм-виходом (2024 D6), тор (2024 D14), нерегулярна мапа з обгортанням (2022 D22 ч.1) і розгорткою куба (ч.2), рекурсивні вкладені сітки (2019 D24 ч.2), вузька шахта ширини 7 (2022 D17).
- Час `programmed`: гравець пише програму; всередині задачі — тік/раунд/секунда, у кожної задачі свій порядок оновлень (одночасно / в порядку читання / по черзі).
- Видимість повна; випадковості в правилах нема — варіативність лише у персональному вводі (`random: setup`).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| 2018 D15 Beverage Bandits — гоблін `G` / ельф `E` | enemy | 200 HP, атака 3 | раунд: ходи в порядку читання; крок найкоротшим шляхом до клітини поряд з ворогом; удар по сусіду з найменшим HP |
| 2018 D15 — стіна `#`, печера `.` | static | — | стіна непрохідна; загиблий юніт → `.` |
| 2018 D13 Mine Cart Madness — вагонетка `^v<>` | object | напрямок, лічильник перехресть | їде колією; на `+` по колу: ліво → прямо → право |
| 2018 D13 — колія `| - / \ +` | terrain | тип | пряма / поворот / перехрестя |
| 2019 D24 Planet of Discord — жук `#` | tile | — | Life 5×5: виживає з рівно 1 сусідом; народжується з 1–2 |
| 2019 D24 ч.2 — центральна клітина `?` | zone | рівень вкладеності | містить внутрішню сітку 5×5; краї — сусіди зовнішнього рівня |
| 2022 D14 Regolith Reservoir — пісок | object | — | падає вниз → вниз-ліво → вниз-право, інакше спочиває |
| 2022 D14 — скеля (ламані з вводу), джерело `500,0`, прірва/підлога | static | — | скеля непрохідна; ч.1 — прірва під найнижчою скелею; ч.2 — підлога на y_max+2 |
| 2022 D17 Pyroclastic Flow — камінь (5 фігур по колу) | object | форма | спавн: 2 від лівої стіни, 3 над вершиною; поштовх вітру → падіння на 1 |
| 2022 D17 — струмінь `<` `>` | terrain | цикл символів вводу | штовхає камінь вліво/вправо на кожному кроці |
| 2022 D22 Monkey Map — ти | player | позиція, напрямок (0 → 1 ↓ 2 ← 3 ↑) | рух N кроків до стіни, поворот L/R |
| 2022 D22 — `.` / `#` / пробіл-порожнеча | terrain | — | відкрито / стіна / за краєм: обгортання (ч.1) або перехід на сусідню грань куба (ч.2) |
| 2023 D16 The Floor Will Be Lava — промінь | projectile | напрямок | летить прямо; дзеркало повертає на 90°; розщеплювач з пласкої сторони ділить на два |
| 2023 D16 — дзеркала `/ \`, розщеплювачі `| -` | static | орієнтація | відбивають / ділять промінь; з гострого кінця — прохід |
| 2024 D6 Guard Gallivant — вартова `^` | enemy | напрямок | перешкода попереду → поворот праворуч на 90°, інакше крок; виходить за край |
| 2024 D6 — перешкода `#` | static | — | непрохідна; ч.2 — гравець додає одну, щоб зациклити вартову |
| 2024 D14 Restroom Redoubt — робот | object | `p=x,y v=dx,dy` | рух зі сталою швидкістю на торі 101×103; роботи не взаємодіють |
| 2024 D15 Warehouse Woes — робот `@` | player | — | ходи `<^>v` з вводу; штовхає ланцюг ящиків |
| 2024 D15 — ящик `O` (ч.2: `[]` подвійної ширини) | object | ширина 1 / 2 | ланцюг зсувається, якщо за ним вільно; широкий ящик вертикально штовхає «дерево» ящиків |
| 2024 D21 Keypad Conundrum — рука робота | player | клавіатура, позиція (старт на `A`) | стрілки рухають руку, `A` натискає клавішу; наведення на дірку — паніка |
| 2024 D21 — цифрова (789/456/123/_0A) і напрямна (_^A/<v>) клавіатури | static | розкладка з діркою | ланцюг: ти → робот → робот → робот біля дверей (ч.2: 25 роботів) |

## Правила (КОЛИ → ЯКЩО → ТО)
- **2018 D15:** КОЛИ `turn_start(unit)` (порядок читання позицій на початок раунду) → ЯКЩО `count(enemies, ==, 0)` → ТО `game_over`; ЯКЩО `not adjacent(unit, enemy)` → ТО `move(unit, step)` за `custom: «BFS до найближчої клітини поряд з ворогом; рівні — за порядком читання цілі, потім першого кроку»`; ПОТІМ ЯКЩО `adjacent(unit, enemy)` → ТО `damage(3)` по сусіду з найменшим HP (рівні — порядок читання). КОЛИ `hp_zero(u)` → ТО `disappear_a`. Відповідь: повні раунди × сума HP вцілілих. Ч.2: мінімальна атака ельфів, за якої не гине жоден ельф.
- **2018 D13:** КОЛИ `tick` → ТО вагонетки ходять по черзі за порядком читання; КОЛИ `enter(cart, curve)` → ТО `face(cart, turn)`; КОЛИ `enter(cart, intersection)` → ТО `face(cart, cycle[left, straight, right])`, лічильник +1. КОЛИ `contact(cart, cart)` → ТО `custom: «аварія — відповідь X,Y»`; ч.2: `disappear_both`, відповідь — позиція останньої.
- **2019 D24:** КОЛИ `tick` → ТО усі клітини одночасно: жук з `adjacent_count ≠ 1` → `set_cell(empty)`; порожня з `adjacent_count ∈ {1,2}` → `set_cell(bug)`. КОЛИ `repetition(layout)` → ТО відповідь = біорізноманіття Σ 2^(n−1). Ч.2: `custom: «рекурсивні сітки: центр — внутрішній рівень, край — зовнішній»`, рахунок жуків через 200 хвилин.
- **2022 D14:** КОЛИ `custom: «попередня піщинка спочила»` → ТО `spawn_at(sand, 500,0)`; КОЛИ `tick` → ЯКЩО `free(down)` → `move(down)`, інакше `free(down-left)` → `move`, інакше `free(down-right)` → `move`, інакше `set_state(rest)`. КОЛИ `reach(sand, below_lowest_rock)` → ТО кінець (ч.1); ч.2 — КОЛИ `occupied(source, sand)` → ТО кінець.
- **2022 D17:** КОЛИ `spawned(rock)` → ТО позиція (x=2, y=top+3), наступна з 5 форм; КОЛИ `tick` → ТО `move(rock, jet[i++ mod n])` ЯКЩО `free`; потім `fall(rock, 1)`; ЯКЩО `blocked(rock)` знизу → ТО `set_state(rest)`, наступний камінь. Відповідь: висота вежі після 2022 каменів; ч.2 — після 10¹² → `custom: «виявлення циклу (форма, індекс струменя, профіль верху)»`.
- **2022 D22:** КОЛИ `exec(N)` → ТО N разів: ЯКЩО `cell(ahead, wall)` → `block` (стоп), інакше `move`; ЯКЩО `cell(ahead, void)` → ТО `wrap` (ч.1: на протилежний край ряду/стовпця; ч.2: на сусідню грань розгортки куба 50×50 з поворотом напрямку). КОЛИ `exec(L|R)` → ТО `face(±90°)`. Пароль = 1000·рядок + 4·стовпець + напрямок.
- **2023 D16:** КОЛИ `beam_hit(mirror)` → ТО `reflect(beam, 90°)`; КОЛИ `beam_hit(splitter_flat)` → ТО `split_beam(two, along_axis)`; гострий кінець → прохід. Промінь на клітині → `mark(energized)`; відповідь — кількість енергізованих; цикли променів відсікати за (клітина, напрямок). Ч.2: найкращий вхід з будь-якого краю.
- **2024 D6:** КОЛИ `tick` → ЯКЩО `cell(ahead, obstacle)` → ТО `face(guard, right)`, інакше `move(guard)`; КОЛИ `edge(guard)` → ТО кінець; відповідь — кількість різних відвіданих клітин. Ч.2: КОЛИ `repetition(cell, dir)` → ТО цикл — порахувати позиції однієї нової перешкоди, що зациклюють вартову.
- **2024 D14:** КОЛИ `tick` (секунда) → ТО `move(robot, v)`, `wrap(robot)` по обох осях; після 100 с — добуток кількостей у 4 квадрантах (середні ряд і стовпець не рахуються). Ч.2: `custom: «знайти секунду, коли роботи складаються в ялинку»` — без формальної умови.
- **2024 D15:** КОЛИ `input(dir)` → ЯКЩО `free(ahead)` → `move(robot)`; ЯКЩО `occupied(ahead, box)` → ТО `custom: «зібрати ланцюг ящиків у напрямку»`; ЯКЩО за ланцюгом стіна → `block` для всіх, інакше `push_chain` + `move(robot)`. Ч.2: мапа подвоєна вшир, ящики `[]` — вертикальний поштовх зачіпає обидві половини й розгалужується деревом. Відповідь: Σ(100·рядок + стовпець) ящиків (GPS).
- **2024 D21:** КОЛИ `input(dir)` на своїй клавіатурі → ТО `move(arm_next, dir)`; КОЛИ `input(A)` → ТО `press(key_under_arm_next)` — каскадом униз ланцюга. КОЛИ `custom: «рука над діркою»` → ТО `lose` (паніка). Відповідь: Σ довжина найкоротшої послідовності × число коду; ч.2 — 25 проміжних роботів → `custom: «DP/мемоізація за парами клавіш на кожному рівні»`.
- Загальне: перемога = правильна відповідь у формі на сайті (зірка); неправильна — повідомлення «too high/too low» (?) і затримка перед наступною спробою; рахунок — зірки (50 за рік до 2024).

## Керування і ввід
- Гравець не керує сутностями: пише програму будь-якою мовою, читає свій ввід, друкує число.
- **Формат рівня = ввід:** ASCII-сітка (D6, D13, D15, D16, D22, D24), список відрізків `x,y -> x,y -> …` (2022 D14), рядок символів `<>` (2022 D17), рядки `p=x,y v=dx,dy` (2024 D14), сітка + порожній рядок + програма руху (`<^v>` на кількох рядках у 2024 D15; `10R5L5…` у 2022 D22), коди `029A` (2024 D21).
- Кожна умова має маленький приклад з відповіддю — природні тест-фікстури.
- Відповідь вводиться в текстове поле на сторінці задачі; ввід кожного гравця свій.

## Вікна, меню, HUD
- `puzzle-page` (custom): текст умови, приклади, поле відповіді, посилання «get your puzzle input»; після першої зірки зʼявляється друга частина.
- `answer-form`: «That's the right answer!» / «That's not the right answer» з таймаутом перед повтором.
- `level-select` — календар-ASCII-картинка року (`star-calendar`), що «оживає» з кожним розвʼязаним днем; архів років 2015+.
- `leaderboard`: приватні лідерборди (глобальний — до 2024 включно); `stats-window` — скільки людей розвʼязали обидві/одну частину.
- `settings-window`: імʼя, анонімність, привʼязка акаунта (GitHub/Google/Reddit…) (?).
- Переходи: календар → день → ч.1 → (зірка) ч.2 → (зірка) календар.

## Фічі поза полем
- `personal-input` — у кожного свій ввід і своя відповідь (антиплагіат, «рівень» генерується).
- `two-part-reveal` — друга частина відкривається лише після першої, часто змінює правила світу.
- `daily-puzzle` (1–25 грудня; з 2025 — 12 днів), `streaks`, архів (`puzzle-bank`).
- `private-leaderboard`; глобальний лідерборд на швидкість прибрано з 2025.
- Спільнота: візуалізації розвʼязків, мемоізація/цикли як «фольклор».

## Варіації й родичі
- Класичні ігри всередині задач: Sokoban (2024 D15), Tetris (2022 D17), falling sand (2022 D14), Game of Life (2019 D24), Deflektor/лазери (2023 D16), Langton-подібний патруль (2024 D6), тактика-роглайк (2018 D15), залізниця (2018 D13).
- Родичі: Project Euler (чиста математика), everybody.codes (?), Synacor Challenge (той самий автор).
- Осі варіацій: **порядок оновлень** (одночасно / в порядку читання / послідовно від джерела); **топологія** (край-вихід / тор / обгортання / куб / рекурсія); **друга частина** (масштаб → цикл / нова фізика / пошук параметра); **що є ввід** (мапа / програма ходів / список тіл).

## Цікавинки для курсу
- 2024 D15: Sokoban з ланцюгом ящиків і широкими ящиками (рекурсивна перевірка «дерева» поштовху) — 🥈.
- 2018 D15: бій з BFS і tie-break за порядком читання — 🥇 (класична пастка на дрібниці).
- 2022 D17: тетріс із вітром + виявлення циклу для 10¹² каменів — 🥇.
- 2022 D22: перехід через ребро розгортки куба з поворотом напрямку — 🥇.
- 2023 D16: промені з розщепленням і відсіканням циклів — 🥉.
- 2024 D6: патруль «впершись — праворуч» + пошук перешкоди, що зациклює — 🥉 / 🥈.
- 2022 D14: падаючий пісок трьома правилами — 📎; 2019 D24 рекурсивний Life — 🥈.
- 2024 D21: ланцюг роботів, що натискають клавіатури один одного (DP за рівнями) — 👑 як курсова «гра в гру».

## Мапа на каталог
- Є: `level-from-txt` (усі вводи) · `push-object` (D15) · `multi-cell-size` (широкі ящики, фігури D17) · `gravity-fall` (пісок, камені) · `inertia-slide` (рух до стіни в D22) · `impassable-cells` · `enemy-patrol` (D6) · `chase-bfs` (D15 2018) · `hp-damage` + `piece-capture` (бій) · `teleport` (обгортання) · `unsolvable-states` (цикли) · `state-as-data` · `game-loop` · `unit-tests` / `fixture-level-tests` (приклади з умови) · `console-render`.
- **Нема** → пропозиції карток:
  - `+reading-order-tiebreak` «Порядок читання для ходів і рівних варіантів» · game-logic · 📎.
  - `+turn-when-blocked` (з Chip's Challenge) · entities/move · 📎.
  - `+intersection-turn-cycle` «Циклічний вибір повороту на перехресті» · entities/move · 📎.
  - `+collision-detect` «Виявлення зіткнення рухомих» · entities/interact · 📎.
  - `+cellular-automaton-rule` (з Game of Life) · 🥉; `+recursive-grid` «Вкладені сітки з межами-сусідами» · 🥈.
  - `+falling-sand` · entities/move · 📎; `+jet-push` «Поштовх за циклічною програмою» · entities/move · 🌱.
  - `+cycle-detection` «Виявлення циклу стану для великих N» · game-logic · 🥇.
  - `+cube-net-wrap` «Обгортання по розгортці куба» · entities/move · 🥇; `+torus-wrap` · 🌱; `+velocity-wrap` · 🌱.
  - `+beam-tracing`, `+mirror-reflect` (з Deflektor/Laser Tank); `+beam-split` «Розщеплення променя» · 🥉.
  - `+loop-detection` «Зациклення актора за (клітина, напрямок)» · 📎.
  - `+emergent-picture` «Ціль — картинка, а не число» · 🥉.
  - `+chain-push-wide` «Ланцюгове штовхання широких обʼєктів» · entities/legality · 🥈.
  - `+control-chain-keypads` «Актор керує актором через інтерфейс» · 👑.
  - `+answer-checksum` «Стан → контрольне число (GPS, біорізноманіття, пароль)» · game-logic/score · 🌱; `+two-part-puzzle` · levels · 📎.

## Пропозиції до словників
- `+trigger:tick`, `+trigger:turn_start(side)`, `+trigger:blocked`, `+trigger:repetition` (повтор стану — 2019 D24, цикли), `+trigger:beam_hit`.
- `+cond:free`, `+cond:facing`, `+cond:adjacent_count` (⏳ є — вживати); `+cond:reading_order` — пріоритет за порядком читання.
- `+effect:move`, `+effect:face`, `+effect:fall`, `+effect:wrap` (⏳ є); `+effect:split_beam`, `+effect:reflect`, `+effect:push_chain`, `+effect:press(key)`.
- `+role:terrain` (колія, струмінь), `+role:projectile` (промінь).
- `+window:puzzle-page`, `+window:answer-form`; `+ui:star-calendar`.
- `+feature:personal-input`, `+feature:two-part-reveal`, `+feature:private-leaderboard`.
- `+axis:control` = `programmed` (гравець пише симулятор); `+axis:session` = `daily`.

## Джерела
- ⭐ [2024 Day 15: Warehouse Woes](https://adventofcode.com/2024/day/15) — мапа `@ O # .`, ходи `<^>v` на кількох рядках, ланцюг ящиків, GPS.
- [Wikipedia: Advent of Code](https://en.wikipedia.org/wiki/Advent_of_Code) — Eric Wastl, 2015, дві частини, персональний ввід, зміни 2025.
- [About](https://adventofcode.com/2024/about) — формат події, приватні лідерборди.
- [2018 D15 Beverage Bandits](https://adventofcode.com/2018/day/15) — 200 HP, атака 3, порядок читання, BFS, формула результату.
- [2018 D13 Mine Cart Madness](https://adventofcode.com/2018/day/13) — колія, цикл ліво/прямо/право, порядок ходів.
- [2019 D24 Planet of Discord](https://adventofcode.com/2019/day/24) — правило 1 / 1–2 сусіди, біорізноманіття.
- [2022 D14 Regolith Reservoir](https://adventofcode.com/2022/day/14) — джерело 500,0, три кроки падіння, прірва.
- [2022 D17 Pyroclastic Flow](https://adventofcode.com/2022/day/17) — ширина 7, 5 форм, спавн 2/3, струмінь → падіння.
- [2022 D22 Monkey Map](https://adventofcode.com/2022/day/22) — мапа + шлях `10R5L5…`, обгортання, пароль.
- [2023 D16 The Floor Will Be Lava](https://adventofcode.com/2023/day/16) — дзеркала, розщеплювачі, енергізовані клітини.
- [2024 D6 Guard Gallivant](https://adventofcode.com/2024/day/6) — поворот праворуч при перешкоді.
- [2024 D14 Restroom Redoubt](https://adventofcode.com/2024/day/14) — `p=… v=…`, тор 101×103, квадранти.
- [2024 D21 Keypad Conundrum](https://adventofcode.com/2024/day/21) — розкладки, дірки, ланцюг роботів, складність.

## Непевне
- (?) Другі частини (2018 D13/D15, 2019 D24 рекурсія, 2022 D14 підлога, 2022 D17 10¹², 2022 D22 куб 50×50, 2023 D16, 2024 D6/D14/D15/D21 з 25 роботами) — з памʼяті: без входу на сайт видно лише першу частину.
- (?) Тексти відповіді форми («too high/too low») і таймаут між спробами — з памʼяті.
- (?) «50 зірок за рік» — до 2024; у 2025 днів 12.
- (?) everybody.codes як родич — з памʼяті, не перевірено.
