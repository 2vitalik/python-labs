---
title: Water Sort / Ball Sort Puzzle (сортування кольорів у пробірках)
slug: water-sort
aka: [Water Sort Puzzle, Ball Sort Puzzle, Color Sort, «сортування води», «сортування кульок»]
family: falling-match
also: [push-slide]
klass: cursor
axes:
  field: graph
  time: turn
  opponent: none
  info: full
  random: setup
  goal: state
year: 2020
platforms: [iOS, Android, web]
links:
  - {kind: other, url: "https://arxiv.org/abs/2202.09495", best: true, note: "Ito et al. 2022 «Sorting Balls and Water»: точні правила ball-move / water-move, мета, NP-повнота, межі кількості порожніх пробірок"}
  - {kind: other, url: "https://arxiv.org/html/2202.09495", note: "HTML-версія статті з формальними визначеннями"}
  - {kind: official, url: "https://apps.apple.com/us/app/id1571446860", note: "Water Sort Color Pouring Game (Rolling Panda, 2021): правила словами, Undo, Add Tube, 5 складностей, 1000 рівнів"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=water+sort+puzzle+gameplay", note: "пошук; геймплей"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=ball+sort+puzzle+gameplay", note: "пошук; варіант з кульками"}
stage: v1
coverage: 75
mechanics: [cell-click, selection-highlight, undo-redo, undo-step, restart-level, sequential-levels, level-unlock, difficulty-levels, level-solver, unsolvable-states, movement-animation, event-effects, sound-effects, game-screen, end-screen, +stack-sort, +pour-run, +extra-container-booster]
proposes: ["+effect:pour", "+card:stack-sort", "+card:pour-run", "+card:extra-container-booster"]
author: opus
date: 2026-11-09
---

# Water Sort / Ball Sort — переливай верхній шар з пробірки в пробірку, доки кожна не стане одного кольору

## Суть
Є n заповнених пробірок місткості h з перемішаними порціями кольорів і кілька порожніх. Хід — узяти верхню порцію з однієї пробірки й покласти в іншу, але лише на той самий колір або в порожню, і лише якщо там є місце. Мета — кожна пробірка порожня або повна одного кольору. Детермінований пазл стану: випадковість лише в генерації рівня, ядро — обмежений буфер (порожні пробірки) і планування на кілька ходів, як у «Ханойській вежі». Ball Sort — та сама гра з кульками: за хід рухається одна кулька, у Water Sort — увесь верхній однокольоровий відрізок.

## Поле і час
- Поле — не сітка, а набір стеків (пробірок) у рядах; позиція в стеку важлива лише зверху (`field: graph` — граф «будь-яка пробірка → будь-яка»).
- Кожна пробірка — стек висоти h (у статті — параметр; у застосунках зазвичай 4 (?)); n пробірок із кольорами + k порожніх (у статті — загальний випадок n + k).
- Покрокова, без таймера («No time limit to solve puzzle»); анімація переливання — лише косметика.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Пробірка | container | місткість h, стек порцій | приймає порцію, якщо порожня або верх того самого кольору і є місце |
| Порція води / кулька | tile | колір | рухається лише з верху стека; у воді сусідні однакові порції зливаються в один відрізок |
| Порожня пробірка | container | 0 / h | буфер: приймає будь-який колір |
| Вибрана пробірка | container (стан) | — | піднята / підсвічена, чекає цілі |
| Додаткова пробірка | container | бустер «Add Tube» | зʼявляється порожньою на вимогу гравця |
| Розвʼязана пробірка | container (стан) | повна, один колір | у частині застосунків закривається кришкою і більше не бере участі (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(tap tube A)` → ЯКЩО `count(units_in_A, >, 0)` → ТО `set_state(A, selected)`; повторний тап — `clear_state(A, selected)`.
- КОЛИ `input(tap tube B)` → ЯКЩО `state(A, selected) and count(units_in_B, <, h) and (count(units_in_B, ==, 0) or same(top_A, top_B, color))` → ТО `custom: «pour — верхній однокольоровий відрізок A переходить у B, скільки влізе; решта лишається в A»`, `clear_state(A, selected)`.
- Інакше → `block` (переливання не відбувається; анімація «не можна» (?)), `clear_state(A, selected)`.
- Ball Sort: те саме, але ТО `move(top_ball_A, B)` — рівно одна кулька за хід.
- КОЛИ `all_constraints_met` (кожна пробірка порожня або повна h порцій одного кольору) → ТО `win`, `next_level`.
- КОЛИ `no_moves(player)` → ТО `custom: «глухий кут — лише undo / рестарт / додаткова пробірка»`; поразки як події нема.
- КОЛИ `input(undo)` → ТО `undo(1)` (крок назад).
- КОЛИ `input(add_tube)` → ЯКЩО `has(player, booster)` → ТО `spawn(empty_tube)`, `take(player, booster)`.
- КОЛИ `input(restart)` → ТО `restart`.
- Теорія (Ito et al.): ball-move і water-move дають **однакову** розвʼязність; задача NP-повна; k ≥ ⌈(h−1)n/h⌉ порожніх пробірок вистачає завжди, деяким рівням потрібно k ≥ ⌊(19/64)·min{n,h}⌋; при h = 2 вистачає k = 2.
- Перемога: усі пробірки відсортовано · Поразка: нема (лише глухий кут) · Рахунок: нема; прогрес — номер рівня.

## Керування і ввід
- Один палець / миша: тап по пробірці-джерелу, тап по пробірці-цілі; повторний тап знімає вибір.
- Кнопки: Undo, Add Tube, Restart; у частині застосунків — Shuffle (?).

## Вікна, меню, HUD
- `game-screen`: ряди пробірок, `selection-highlight` вибраної, `level-number`, кнопки `undo-button`, `restart-button`, кнопка додаткової пробірки з лічильником (?).
- `end-screen`: «рівень пройдено» → наступний.
- `difficulty-select` / `mode-select`: Beginner · Advanced · Master · Expert · Challenge (Rolling Panda).
- `level-select` з номерами рівнів (?); `settings-window` (звук, вібрація) (?); `shop-window` теми/скіни пробірок (?).
- Переходи: main-menu → game-screen → (усі відсортовано) end-screen → наступний рівень.

## Фічі поза полем
- `levels-sequential` (1000 рівнів у Rolling Panda), рівні складності; `undo`; `restart-level`; бустер «Add Tube» (обмежений, часто за рекламу (?)).
- `autosave` прогресу рівнів (?); теми оформлення (?).

## Варіації й родичі
- Ball Sort Puzzle (за статтею — перший застосунок IEC Global Pty Ltd, січень 2020) → Water Sort (рух відрізками) → безліч клонів (Color Sort, Nuts Sort, Hexa Sort, сортування товарів на полицях).
- Родичі: Ханойська вежа (стеки з обмеженням на верх), Sokoban (детермінований пазл стану з глухими кутами), пасьянси типу FreeCell (буферні клітини).
- **Осі варіацій**: що рухається (1 кулька / весь однокольоровий відрізок / ціла пробірка) · місткість h (3 / 4 / 5+) · кількість порожніх k · приховані нижні шари («?»-порції, що відкриваються, коли стають верхніми (?)) · бустери (додаткова пробірка / undo-ліміт / shuffle) · закриття готової пробірки.

## Цікавинки для курсу
- Модель стеків і перевірка легальності ходу (порожньо або той самий верх, є місце) — 🌱.
- Water-move: перелити максимальний верхній відрізок у межах місткості — 📎.
- Undo через стек станів — 📎; детектор глухого кута (нема легальних нетривіальних ходів) — 📎.
- Генератор рівня з гарантією розвʼязності: перемішування зворотними ходами або перевірка розвʼязувачем — 🥈.
- Розвʼязувач BFS/A* з канонізацією стану (порядок пробірок неважливий) — 🥇 (задача NP-повна, без канонізації вибухає).

## Мапа на каталог
- Є: `cell-click` (тап по пробірці) · `selection-highlight` · `undo-redo` / `undo-step` · `restart-level` · `sequential-levels` · `level-unlock` · `difficulty-levels` · `level-solver` · `unsolvable-states` (глухий кут) · `movement-animation` (переливання) · `event-effects` · `sound-effects` · `game-screen` · `end-screen`.
- **Нема** → пропозиції карток:
  - `+stack-sort` «Сортування стеків за кольором» · entities/legality · 📎 · слоти {capacity: 4, empty: 2, unit: ball|run}.
  - `+pour-run` «Перелити верхній однокольоровий відрізок» · entities/interact · 📎.
  - `+extra-container-booster` «Додатковий порожній контейнер на вимогу» · game-logic/difficulty · 🌱 · слот {uses: n}.

## Пропозиції до словників
- `+effect:pour` — перенести верхній однокольоровий відрізок одного стека в інший у межах місткості (Water Sort; відрізняється від `move` кількістю одиниць).
- Вжито вже наявні `all_constraints_met`, `no_moves`, `same`, `count`, `undo`, `restart`, роль `container`.

## Джерела
- ⭐ [Ito et al., Sorting Balls and Water (arXiv 2202.09495)](https://arxiv.org/abs/2202.09495) — правила обох варіантів, мета, еквівалентність, NP-повнота, межі порожніх пробірок.
- [HTML-версія статті](https://arxiv.org/html/2202.09495) — формальні визначення ball-move / water-move, перший Ball Sort від IEC Global (01.2020).
- [App Store: Water Sort Color Pouring Game](https://apps.apple.com/us/app/id1571446860) — правила словами, Undo, Add Tube, 5 складностей, 1000 рівнів, без ліміту часу; Shuffle в історії версій.

## Непевне
- (?) Типова місткість 4 і «n кольорів + 2 порожні» у застосунках — з памʼяті; стаття дає загальні h і k.
- (?) Кришка на готовій пробірці, приховані «?»-шари, магазин скінів, Add Tube за рекламу, рівень-селектор — з памʼяті, різниться між клонами.
- (?) Рік: Ball Sort — січень 2020 за статтею; найраніший Water Sort — не перевірено.
- (?) Чи є в класичних застосунках ліміт undo (часто 5 за рівень (?)) — не звірено.
