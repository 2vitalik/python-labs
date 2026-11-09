---
title: N-queens і Knight's tour (задача ферзів, хід коня)
slug: n-queens-knights-tour
aka: [Eight queens puzzle, 8 ферзів, Задача про вісім ферзів, Knight's tour, Хід коня, Обхід конем, Тур коня]
family: pencil-logic
also: [chess-abstract]
klass: puzzle
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: none
  goal: constraints
year: 1848
platforms: [paper, PC, web]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Eight_queens_puzzle", best: true, note: "історія, 92/12 розвʼязків, n ферзів, споріднені задачі, алгоритми, ігри"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Knight%27s_tour", note: "відкритий/замкнений тур, теорема Швенка, кількість турів, правило Варнсдорфа"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=eight+queens+knight%27s+tour+puzzle", note: "пошук; пояснення й візуалізації"}
stage: v1
coverage: 60
mechanics: [piece-move-patterns, cursor-place, legal-move-highlight, markup-validity, completion-detection, satisfy-constraints, conflict-highlight, cell-click, field-size-picker, undo-redo, level-solver, visited-trail, no-moves-left, +attack-lines-overlay, +knight-tour-path, +hamiltonian-path-check, +backtracking-visualizer]
proposes: ["+cond:attacked(cell, by)", "+cond:visited", "+cond:knight_move(a, b)", "+card:attack-lines-overlay", "+card:knight-tour-path", "+card:hamiltonian-path-check", "+card:backtracking-visualizer"]
author: opus
date: 2026-11-09
---

# N-queens і Knight's tour — дві класичні шахові задачі: розставити ферзів без боїв і обійти дошку конем

## Суть
Дві задачі, де шахова дошка — просто сітка, а фігура — правило сусідства. **N ферзів**: поставити N ферзів на дошку N×N так, щоб жоден не бив іншого (рядок, стовпець, діагональ). **Тур коня**: провести коня ходами коня так, щоб він побував у кожній клітинці рівно раз; замкнений тур закінчується за хід коня від старту. Обидві — канонічні вправи на перебір з поверненням і граф (Гамільтонів шлях); у цифровій формі це пазл із курсором і підсвіткою боїв.

## Поле і час
- Квадратна дошка N×N (класично 8×8); тур коня — також m×n і нерегулярні дошки; ферзі — і тор (Pólya).
- Шари: клітинки · фігури (ферзі) або номери ходів коня (1…N²) · підсвітка атак / доступних ходів.
- Час статичний; хід = поставити/зняти ферзя або зробити наступний хід конем.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітинка дошки | terrain | колір, координата | вільна, під боєм або зайнята |
| Ферзь | piece | позиція | бʼє рядок, стовпець і обидві діагоналі на всю довжину |
| Кінь | piece | позиція | ходить буквою Г (±1, ±2); не бʼє — лише рухається |
| Відвідана клітинка | mark | номер ходу k | у турі коня — більше не можна стати |
| Лінія атаки | mark | напрямок | підсвітка клітинок, які бʼє ферзь (цифрова версія) |
| Інші фігури | piece | тура, слон, король, кінь | у споріднених задачах незалежності/домінування |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(click, cell)` → ЯКЩО `free(cell)` → ТО `place(queen, cell)`; клік по ферзю — `disappear_a` (зняти).
- КОЛИ `input(click, cell)` → ЯКЩО `custom: «клітинку бʼє інший ферзь»` (`+cond:attacked`) → ТО `set_state(queens, conflict)` або `block` (режим «тільки легальні») (?).
- КОЛИ `constraint_broken(attack)` → ЯКЩО `custom: «два ферзі на одному рядку, стовпці чи діагоналі»` → ТО `set_state(pair, error)`.
- КОЛИ `counter(queens, eq, N)` → ЯКЩО `not constraint_broken(attack)` → ТО `win`.
- КОЛИ `input(click, cell)` → ЯКЩО `custom: «клітинка за хід коня від поточної»` (`+cond:knight_move`) and `not custom: «клітинку вже відвідано»` (`+cond:visited`) → ТО `move(knight, cell)` + `mark(cell, k)`.
- КОЛИ `input(click, cell)` → ЯКЩО `custom: «не хід коня або вже відвідано»` → ТО `block`.
- КОЛИ `no_moves(knight)` → ЯКЩО `count(visited, lt, N*N)` → ТО `lose` (глухий кут; у цифровій версії — `undo`).
- КОЛИ `counter(visited, eq, N*N)` → ТО `win`; ЯКЩО `custom: «остання клітинка за хід коня від першої»` → ТО `custom: «замкнений тур»`.
- Евристика Варнсдорфа (1823): ходити в клітинку з найменшою кількістю подальших ходів — `custom: «підказка-клітинка»` як `hint`.
- Існування: ферзі — розвʼязок є для всіх N, крім 2 і 3; для 8 — 92 розвʼязки, 12 з точністю до симетрій.
- Існування туру (теорема Швенка): замкненого нема, якщо обидві сторони непарні, менша сторона 1, 2 чи 4, або 3×4, 3×6, 3×8; відкритий є на будь-якій дошці з меншою стороною ≥ 5.
- Перемога: N ферзів без взаємних боїв · усі клітинки відвідані конем рівно раз. Рахунку нема; поразка — лише глухий кут туру.

## Керування і ввід
- Ферзі: клік по клітинці ставить/знімає; drag ферзя — перенести (`drag-drop-piece`) (?).
- Тур: клік по одній з підсвічених клітинок — наступний хід; undo — повернути коня на крок.
- Папір: ферзі — хрестиками на дошці; тур — номери ходів у клітинках.

## Вікна, меню, HUD
- `game-screen` (цифрова версія): дошка, фігури, `legal-move-highlight` (ходи коня), підсвітка боїв ферзів, `remaining-counter` (лишилось поставити / відвідати), `move-counter`.
- `settings-window`: розмір дошки N, тип задачі, «показувати атаки», «замкнений тур».
- `solutions-window` — галерея знайдених розвʼязків (92 для 8 ферзів) (цифрова версія).
- `end-screen` — «розвʼязано»; для туру — відкритий/замкнений.
- Переходи: settings → нова дошка; game-screen → end-screen.

## Фічі поза полем
- `custom-difficulty`: розмір дошки N / m×n; `undo` ∞; `hint` (Варнсдорф); `auto-solve` (перебір з поверненням з анімацією); `stats` — скільки розвʼязків знайдено.
- У відеоіграх: «Queen's Dilemma» у The 7th Guest, головоломка 130 «Too Many Queens 5» у Professor Layton and the Curious Village.

## Варіації й родичі
- Ферзі: інші фігури на 8×8 — 32 коні, 14 слонів, 16 королів, 8 тур без боїв; домінування (5 ферзів тримають усю 8×8); доповнення часткової розстановки — NP-повне; тор; шогі-«драконові королі», змішані фігури, латинські квадрати.
- Тур: магічний тур (на 8×8 повністю магічного нема), нерегулярні дошки, вірші й романи (Rudrata, Perec «Життя: інструкція з використання», 10×10).
- У сімʼї: [Star Battle](star-battle.md) (одна зірка на рядок/стовпець/область, без дотику — «ферзі з регіонами»), [Hidato](hidato.md) і [Signpost](signpost.md) (номерований Гамільтонів шлях), [Sudoku variants](sudoku-variants.md) (anti-knight / anti-king), [Takuzu](takuzu.md).
- Поза сімʼєю: [Chess](../chess-abstract/chess.md) (патерни ходу), [Chess rule twists](../chess-abstract/chess-rule-twists.md).
- **Осі варіацій**: фігура (ферзь / тура / слон / кінь / фея) · мета (незалежність / домінування / обхід) · дошка (N×N / m×n / тор / нерегулярна) · тур (відкритий / замкнений / магічний).

## Цікавинки для курсу
- Перевірка «ніхто не бʼє»: множини рядків, стовпців, діагоналей r−c і r+c — 🌱.
- Перебір з поверненням для N ферзів (по ферзю на рядок) з анімацією кроків — 📎.
- Підсвітка ходів коня і заборона повторних клітинок — 🌱.
- Тур коня за Варнсдорфом + підказка «найменше виходів» — 📎.
- Min-conflicts для 1 000 000 ферзів / підрахунок усіх розвʼязків бітовими масками — 🥈.
- Генератор «доповни розстановку» з єдиним розвʼязком (NP-повна задача) — 🥇.

## Мапа на каталог
- Є: `piece-move-patterns` ↔ біг ферзя / стрибок коня · `cursor-place` ↔ поставити ферзя · `legal-move-highlight` ↔ ходи коня · `markup-validity`, `conflict-highlight`, `completion-detection`, `satisfy-constraints` · `visited-trail` ↔ номери ходів туру · `no-moves-left` ↔ глухий кут · `level-solver` ↔ перебір · `field-size-picker`, `undo-redo`, `cell-click`.
- **Нема** → пропозиції карток:
  - `+attack-lines-overlay` «Підсвітка клітинок під боєм фігур» · interface/hud · 🌱.
  - `+knight-tour-path` «Шлях фігурним ходом через усі клітинки рівно раз» · game-logic/win · 📎 · слот {closed: yes|no}.
  - `+hamiltonian-path-check` «Шлях відвідує кожну вершину рівно раз» · game-logic/constraints · 🌱.
  - `+backtracking-visualizer` «Покрокова анімація перебору з поверненням» · levels/solvability · 📎.

## Пропозиції до словників
- `+cond:attacked(cell, by)`, `+cond:visited` — повтори (Chess, Icebarn).
- `+cond:knight_move(a, b)` — між клітинками хід коня (|dx|,|dy|) = (1,2)/(2,1); узагальнення — `+cond:leaper(a, b, m, n)`.
- `+card:attack-lines-overlay`, `+card:knight-tour-path`, `+card:hamiltonian-path-check`, `+card:backtracking-visualizer` — див. мапу.

## Джерела
- ⭐ [Wikipedia: Eight queens puzzle](https://en.wikipedia.org/wiki/Eight_queens_puzzle) — Bezzel 1848, Nauck 1850 (узагальнення до n), Dijkstra 1972, 92/12 розвʼязків, N≠2,3, споріднені задачі, backtracking і min-conflicts, 7th Guest і Layton.
- [Wikipedia: Knight's tour](https://en.wikipedia.org/wiki/Knight%27s_tour) — означення, Rudrata (IX ст.), Euler 1759, Warnsdorff 1823, теорема Швенка, кількість турів на 8×8, магічні тури.
- YouTube: пошук «eight queens knight's tour puzzle».

## Непевне
- (?) `year: 1848` — рік задачі ферзів; тур коня значно старший (IX ст.), одне поле на два твори.
- (?) Вікна й режими (галерея розвʼязків, «тільки легальні ходи») — типові для цифрових реалізацій, конкретної еталонної програми не перевіряв.
- (?) Як саме подано задачі в The 7th Guest і Professor Layton (ввід, підсвітка) — лише згадка у Вікіпедії.
- (?) `lose` у глухому куті туру — моя формалізація; у задачі на папері поразки нема, лише стерти й почати знову.
