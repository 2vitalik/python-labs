---
title: Shikaku (Шікаку, Rectangles, Divide by Box)
slug: shikaku
family: pencil-logic
also: []
klass: puzzle
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: none
  goal: constraints
year: 1989
platforms: [paper, web, mobile, PC]
links:
  - {kind: official, url: "https://www.nikoli.co.jp/en/puzzles/shikaku/", best: true, note: "Nikoli: 2 правила, Sample → Progressing → Solution, «тренування таблиці множення»"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Shikaku", note: "Yoshinao Anpuku (1989), назви, NP-повнота (Takenaga та ін., 2013)"}
  - {kind: official, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/rect.html", note: "Tatham Rectangles: drag-прямокутники, клавіатура, Expansion factor, Ensure unique"}
  - {kind: play, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/rect.html", note: "Rectangles у браузері (WebAssembly)"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/shikaku.js", note: "puzz.link: правила, тести вводу меж, коди помилок"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=shikaku+puzzle+how+to+solve", note: "пошук; розвʼязання"}
stage: v1
coverage: 75
mechanics: [markup-validity, completion-detection, satisfy-constraints, cell-click, keyboard-controls, unique-puzzle-generation, difficulty-levels, level-solver, field-size-picker, game-settings, import-open-formats, editor-draw-tools, +undo-redo, +seed-share, +edge-marking, +region-size-check, +solve-into-undo, +drag-rectangle, +rect-shape-check, +region-done-shade, +grid-expansion-generation]
proposes: ["+cond:is_rectangle", "+cond:region_size", "+effect:draw_rect", "+ui:drag-rect-preview", "+ui:region-done-shade", "+feature:non-unique-mode", "+window:params-dialog", "+card:drag-rectangle", "+card:rect-shape-check"]
author: opus
date: 2026-11-02
---

# Shikaku — розріж сітку на прямокутники, кожен з одним числом, що дорівнює його площі

## Суть
У деяких клітинках сітки стоять числа. Гравець ділить усю сітку на прямокутники (квадрати теж) так, щоб кожен містив рівно одне число і площа дорівнювала цьому числу. Розмітка — не клітинки, а **межі** між ними; у цифрових версіях — перетягування прямокутника мишею. Незвичне: кожна підказка дає скінченний список кандидатів (12 = 1×12, 2×6, 3×4 у різних позиціях), і пазл — це задача точного покриття поля вибраними кандидатами.

## Поле і час
- Прямокутна сітка; клітинки з числом N ≥ 1 або порожні.
- Розмітка на ребрах між клітинками (puzz.link: «draw lines over the dotted lines»); зовнішня рамка — завжди межа.
- Шари: число (незмінне) · стан кожного внутрішнього ребра: невідомо / межа / «точно не межа» (puzz.link, хрестик правою кнопкою) · похідне: області.
- Час статичний; хід = провести/стерти ребро або весь прямокутник drag-ом.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітинка з числом | static | N | рівно одна в своєму прямокутнику; N = площа |
| Порожня клітинка | mark | належність до області | покривається рівно одним прямокутником |
| Ребро | mark | стан none / border / no-border | перемикається кліком; межі формують області |
| Прямокутник (область) | zone | ширина × висота, кількість чисел | 4-звʼязна область, обмежена межами; має бути прямокутною |
| Завершений прямокутник | zone | — | Tatham: правильний прямокутник зафарбовується |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left_click, edge)` → ТО `custom: «перемкнути ребро межа/нічого»` (Tatham).
- КОЛИ `input(left_drag, from, to)` → ТО `custom: «намалювати прямокутник між кутами/центрами; внутрішні ребра стерти»` (`+effect:draw_rect`); drag уздовж лінії сітки → лінія.
- КОЛИ `input(right_drag, rect)` → ТО `custom: «стерти вміст прямокутника, не чіпаючи його межі»` (Tatham); puzz.link — права кнопка ставить на ребра позначку «не межа».
- КОЛИ `after(edges_changed)` → ЯКЩО `is_rectangle(region)` and `count_in(region, number, ==, 1)` and `region_size(region) == N` → ТО `custom: «зафарбувати прямокутник як готовий»` (Tatham).
- КОЛИ `constraint_broken(no_number)` — область без числа → ТО конфлікт (puzz.link `bkNoNum`).
- КОЛИ `constraint_broken(one_number)` — у області ≥ 2 числа → ТО конфлікт (`bkNumGe2`).
- КОЛИ `constraint_broken(rectangular)` — ЯКЩО `not is_rectangle(region)` → ТО конфлікт (`bkNotRect`).
- КОЛИ `constraint_broken(area)` — ЯКЩО `region_size(region) != N` → ТО конфлікт (`bkSizeNe`).
- КОЛИ `constraint_broken(dead_end_border)` — відрізок межі обривається всередині поля → ТО конфлікт (`bdDeadEnd`).
- КОЛИ `all_constraints_met` → ТО `win`, `flash` (Tatham).
- Дедукції: перелічити для кожного числа всі прямокутники-кандидати, що не накривають інше число; клітинку, яку може покрити лише один кандидат, віддати йому; «1» — одразу квадрат 1×1; просте N біля краю — лише смуга.
- Перемога: поле повністю розбите на прямокутники, у кожному одне число = площа. Поразки й рахунку нема.

## Керування і ввід
- Tatham, миша: клік по ребру — вкл/викл; ліва з протягуванням — прямокутник (з `+ui:drag-rect-preview`) або лінія; права з протягуванням — стерти вміст.
- Tatham, клавіатура: стрілки — курсор; Return — почати прямокутник, стрілки — розтягнути, Return — завершити; Space замість Return — стерти; Escape — скасувати drag.
- puzz.link: ліва з протягуванням по точкових лініях — межі (повтор стирає); права — хрестики «не межа».
- Спільні дії Tatham: N, U/Ctrl+Z, R/Ctrl+R, Restart, Solve.

## Вікна, меню, HUD
- `game-screen`: сітка з числами, межі, `+ui:region-done-shade` (готові прямокутники зафарбовані), `drag-ghost` під час протягування, `cursor`.
- Tatham: Game (New, Restart, Undo, Redo, Solve, Enter game ID, Enter random seed, Download/Upload save file, Preferences) · Type (пресети + Custom…).
- `+window:params-dialog` (Custom…): Width, Height, Expansion factor, Ensure unique solution.
- `+window:game-id-dialog` — ID / seed.
- `help-window` — правила (Nikoli, Tatham doc).
- puzz.link: Check з текстом коду помилки, `editor-window` для чисел.
- Переходи: Type → params-dialog → генерація → game-screen; розвʼязання → спалах → New game.

## Фічі поза полем
- `auto-check`: Tatham — зафарбовує кожен правильний прямокутник одразу (позитивний зворотний звʼязок замість червоних помилок); puzz.link — Check.
- `undo`/`redo`, `auto-solve` в історії undo, `seed-input`, `share-code`, збереження у файл.
- `custom-difficulty`: **Expansion factor** — генерувати меншу сітку й додавати рядки/стовпці (≈0.5 складніше, завелике — тривіально); **Ensure unique solution** — вимкнення дає неоднозначні пазли (складніше, «знайди всі розвʼязки», швидша генерація).
- `level-editor` + `share-code` (puzz.link).

## Варіації й родичі
- Tatham **Rectangles** — та сама гра; Tatham генерує сітки будь-якого розміру (на відміну від Palm-версії Puzzle Palace).
- Родичі: Fillomino (області за розміром, будь-якої форми), Sashigane (L-подібні області), Tentai Show/Galaxies (симетричні області), Nurikabe (острови з числом = розмір).
- **Осі варіацій**: форма області (прямокутник / L / будь-яка / симетрична) · що несе число (площа / периметр / кількість) · скільки чисел на область (рівно 1 / ≥1) · ввід (межі / drag-прямокутник / заливка).

## Цікавинки для курсу
- Ввід «перетягни прямокутник» з превʼю й очищенням внутрішніх меж — 📎 (картка `editor-draw-tools` — близький родич).
- Перевірка «область — прямокутник» (bounding box = розмір компоненти) — 🌱.
- Області з ребер через flood fill + «одне число, площа = N» — 📎 (є пропозиція `+region-size-check`).
- Автозафарбування готового прямокутника — 🌱, гарний приклад позитивного фідбеку.
- Розвʼязувач: кандидати для кожного числа + точне покриття (Algorithm X) — 🥇.
- Генератор: випадково розрізати поле на прямокутники → поставити числа → перевірити унікальність; плюс Expansion factor — 👑.

## Мапа на каталог
- Є: `markup-validity` ↔ коди помилок · `completion-detection`, `satisfy-constraints` · `cell-click` ↔ клік по ребру · `keyboard-controls` ↔ Return/Space/Escape · `editor-draw-tools` ↔ прямокутник drag-ом (той самий інструмент, але в грі) · `unique-puzzle-generation`, `level-solver`, `difficulty-levels`, `field-size-picker`, `game-settings` ↔ Custom · `import-open-formats` ↔ puzz.link URL.
- Перевикористано: `+undo-redo`, `+seed-share`, `+edge-marking`, `+region-size-check`, `+solve-into-undo`.
- **Нема** → пропозиції карток:
  - `+drag-rectangle` «Ввід прямокутника перетягуванням» · interface/input · 📎 · слот {snap: corners|centres}.
  - `+rect-shape-check` «Область має бути прямокутником» · game-logic/constraints · 🌱 · слот {shape: rect|square}.
  - `+region-done-shade` «Зафарбувати правильно завершену область» · interface/hud · 🌱.
  - `+grid-expansion-generation` «Генерація меншого поля з розтягуванням» · levels/generation · 🥈 · слот {factor}.

## Пропозиції до словників
- `+cond:is_rectangle` — область збігається зі своїм обмежувальним прямокутником.
- `+cond:region_size` — розмір області порівняно з числом (повтор із Nurikabe/Fillomino).
- `+effect:draw_rect` — встановити межі прямокутника й стерти внутрішні.
- `+ui:drag-rect-preview` — контур прямокутника під час протягування; `+ui:region-done-shade` — фарба готової області.
- `+feature:non-unique-mode` — дозвіл неоднозначних пазлів (Tatham «Ensure unique solution» = off).
- `+window:params-dialog` — повтор (Tatham Custom).
- `+card:drag-rectangle`, `+card:rect-shape-check` — див. мапу.

## Джерела
- ⭐ [Nikoli: Shikaku](https://www.nikoli.co.jp/en/puzzles/shikaku/) — 2 правила, ілюстрації, приклад 12 = 1×12 / 2×6 / 3×4.
- [Wikipedia: Shikaku](https://en.wikipedia.org/wiki/Shikaku) — Yoshinao Anpuku (Кіотський університет, 1989), назви Shikaku ni Kire / Divide by Box / Rectangles, NP-повнота (2013).
- [Tatham: Rectangles](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/rect.html) — миша, клавіатура, Expansion factor, Ensure unique solution.
- [Rectangles у браузері](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/rect.html) — меню й підказка з керування.
- [Tatham: common actions](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/common.html) — спільні клавіші, Solve в undo.
- [puzz.link shikaku.js](https://puzz.link/js/pzpr-samples/shikaku.js) — правила, тести вводу меж, коди `bkNoNum`, `bkNumGe2`, `bkNotRect`, `bkSizeNe`, `bdDeadEnd`.
- YouTube: пошук «shikaku puzzle how to solve».

## Непевне
- (?) Назви відеоігор-адаптацій — Wikipedia лише згадує факт адаптації.
- (?) Пресети Type у Tatham Rectangles — сторінка не перелічує.
- (?) Значення «-1» на ребрах у тестах puzz.link трактую як хрестик «не межа» — виведено з тестів.
