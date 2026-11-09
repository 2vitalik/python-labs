---
title: Slant (Gokigen Naname)
slug: slant
aka: [Gokigen Naname, Gokigen, 斜線, ごきげんななめ, Косі лінії]
family: pencil-logic
also: []
klass: puzzle
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: setup
  goal: constraints
year: null
platforms: [paper, PC, web, mobile]
links:
  - {kind: other, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/slant.html", best: true, note: "мануал Tatham: правила, керування циклом \\ / порожньо, Custom, Preferences"}
  - {kind: play, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/slant.html", note: "грати в браузері (WASM), коротка інструкція"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Gokigen_Naname", note: "правила Nikoli, «одна мережа не потрібна»"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/gokigen.js", note: "pzpr.js: правила EN/JA, Nikoli vol. 104, коди помилок slLoop/crConnSlNe/ceNoSlash"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=gokigen+naname+slant+puzzle", note: "пошук; розвʼязання"}
stage: v1
coverage: 65
mechanics: [markup-validity, completion-detection, satisfy-constraints, cell-click, keyboard-controls, unique-puzzle-generation, difficulty-levels, level-solver, field-size-picker, game-settings, controls-remap, seed-share, save-game, undo-redo, import-open-formats, +neighbor-count-clue, +loop-detection, +half-cell-triangles, +vertex-clue, +solve-into-undo, +tri-state-click-cycle]
proposes: ["+cond:no_loop(lines)", "+cond:lines_at(vertex, n)", "+card:vertex-clue", "+card:tri-state-click-cycle", "+window:params-dialog", "+window:game-id-dialog"]
author: opus
date: 2026-11-09
---

# Slant (Gokigen Naname) — у кожну клітинку діагональ \ чи /, без петель; число у вершині = скільки діагоналей у ній сходиться

## Суть
Прямокутна сітка; на деяких **вершинах** (перетинах ліній сітки) стоять числа в кружечках 0–4. Гравець у кожну клітинку ставить одну діагональ — `\` або `/`. Число на вершині каже, скільки діагоналей торкаються цієї точки; діагоналі ніде не мають утворити замкнену петлю. Незвичне: підказки не в клітинках, а на вершинах, а стан клітинки — бінарний (лише нахил), тому це «binary-determination» пазл (Wikipedia).

## Поле і час
- Сітка W×H клітинок, (W+1)×(H+1) вершин; підказки — на вершинах, зокрема на краях і в кутах.
- Внутрішня вершина має 4 сусідні клітинки → число 0…4; на краю — до 2, у куті — до 1.
- 0 усередині поля неможливий: він змусив би петлю (Tatham).
- Шари: вершини з підказками (незмінні) · діагоналі гравця.
- Граф: діагоналі — ребра між вершинами; умова «без петель» = граф діагоналей є лісом. Одна звʼязна мережа **не** вимагається (Wikipedia).
- Час статичний; хід = змінити стан клітинки. Пазл генерується (`random: setup`).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітинка | mark | стан: порожньо · `\` · `/` | діагональ зʼєднує дві протилежні вершини |
| Діагональ `\` | mark | — | зʼєднує лівий верхній і правий нижній кути |
| Діагональ `/` | mark | — | зʼєднує правий верхній і лівий нижній кути |
| Вершина | static | — | вузол графа діагоналей |
| Підказка на вершині | mark | n = 0…4 | рівно n діагоналей торкаються вершини |
| Мережа діагоналей | zone | — | компонента звʼязності графа; не має містити циклу |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left_click, cell)` → ТО `custom: «стан клітинки по колу: порожньо → \ → / → порожньо»` (Tatham).
- КОЛИ `input(right_click, cell)` → ТО `custom: «той самий цикл у зворотному порядку: порожньо → / → \ → порожньо»` (Tatham; одна кнопка достатня).
- КОЛИ `input(key_return)` → ТО `custom: «цикл як лівий клік»`; КОЛИ `input(key_space)` → ТО `custom: «цикл як правий клік»` (Tatham).
- КОЛИ `input(key_slash)` / `input(key_backslash)` → ТО `mark(cell, / | \)` напряму, незалежно від поточного стану (Tatham).
- КОЛИ `input(key_backspace)` → ТО `unmark(cell)` (Tatham).
- Підказка: ЯКЩО `custom: «кількість діагоналей, що торкаються вершини, = n»` (`+cond:lines_at`) → вершина задоволена.
- КОЛИ `constraint_broken(vertex)` → ЯКЩО `custom: «діагоналей у вершині більше n або вільних клітинок замало»` → ТО конфлікт (pzpr: `crConnSlNe`).
- КОЛИ `constraint_broken(loop)` → ЯКЩО `custom: «діагоналі утворили замкнену петлю»` (`+cond:no_loop`) → ТО конфлікт (pzpr: `slLoop`).
- КОЛИ `constraint_broken(cell)` → ЯКЩО `custom: «клітинка без діагоналі»` → ТО пазл не завершено (pzpr: `ceNoSlash`).
- КОЛИ `all_constraints_met` → ЯКЩО `cover_all(diagonals)` → ТО `win`.
- Дедукція «4 і 0»: 4 — усі чотири клітинки дивляться на вершину; 0 на краю — дві клітинки від неї; 1 у куті — діагональ у кут.
- Дедукція «пара 1–1 / 3–3»: сусідні по ребру 1 і 1 або 3 і 3 фіксують дві клітинки між ними (стандартна техніка, ?).
- Дедукція «петля»: якщо одна з орієнтацій закриває цикл, клітинка мусить мати іншу.
- Дедукція рівня Hard (Tatham): міркування про звʼязки між клітинками; навіть на Hard перебір не потрібен.
- Перемога: усі клітинки мають діагональ, усі числа виконані, петель нема. Поразки й рахунку нема.

## Керування і ввід
- Миша: лівий клік — `\`, правий — `/`; повторні кліки — цикл трьох станів; лівий і правий — у протилежних напрямках.
- Клавіатура: стрілки — курсор; Return — як лівий клік, Space — як правий; клавіші `/` і `\` — пряма постановка; Backspace — стерти.
- Preferences — поміняти ролі кнопок миші.
- Спільні дії Tatham: New, Restart, Undo, Redo, Solve; Enter game ID / random seed; Download / Upload save file.

## Вікна, меню, HUD
- `game-screen`: сітка, кружечки-підказки на вершинах, діагоналі; веб-версія — drag для зміни розміру, правий клік — розмір за замовчуванням.
- Меню Game: Enter game ID… · Enter random seed… · Download save file… · Upload save file… · Preferences…; кнопки New game · Restart game · Undo move · Redo move · Solve game.
- Меню Type → Custom… → `params-dialog`: Width, Height, Difficulty.
- `settings-window` (Preferences): порядок кнопок миші.
- `game-id-dialog`; `help-window` — «Full instructions».
- `conflict-highlight` для петлі та переповнених вершин — у pzpr є перевірки, у Tatham не описано (?).

## Фічі поза полем
- Генератор з рівнями складності; Hard без перебору (Tatham).
- `undo` ∞ + `redo`, `restart-level`, `auto-solve`; `seed-input`, `share-code`, збереження у файл.
- `remap-controls` — порядок кнопок миші.
- puzz.link (pzpr): редактор і перевірка відповіді з кодами помилок; URL-код пазла.

## Варіації й родичі
- У сімʼї: [Shakashaka](shakashaka.md) (половинки клітинок діагоналлю), [Slitherlink](slitherlink.md) (лінії й числа, але петля **потрібна**), [Hashiwokakero](hashiwokakero.md) (графові звʼязки, там одна мережа обовʼязкова), [Tatham collection](tatham-collection.md) (оболонка), [puzz.link](puzz-link.md).
- pzpr тести мають `setconfig,use,1/2` — два режими вводу (?).
- **Осі варіацій**: де підказки (вершини / клітинки) · заборона петель (так / ні) · вимога однієї мережі (ні в Slant / так) · кількість станів клітинки (2 нахили / 3 з порожнім).

## Цікавинки для курсу
- Клітинка з трьома станами по колу і зворотний цикл другою кнопкою — 🌱.
- Рендер діагоналей і підказок на вершинах (координати вершин ≠ координати клітинок) — 📎.
- Перевірка підказок: для кожної вершини порахувати діагоналі 4 сусідніх клітинок, що в неї впираються — 🌱.
- Перевірка «без петель» через union-find по вершинах: діагональ, що зʼєднує вже звʼязані вершини, дає цикл — 🥉.
- Розвʼязувач з пропагацією (числа + union-find «ця орієнтація замкне петлю») без перебору — 🥇.
- Генератор: випадковий ліс діагоналей → усі числа → мінімізація з перевіркою єдиності — 🥇.

## Мапа на каталог
- Є: `markup-validity`, `completion-detection`, `satisfy-constraints` · `cell-click`, `keyboard-controls` · `unique-puzzle-generation`, `difficulty-levels`, `level-solver` · `field-size-picker`, `game-settings`, `controls-remap` ↔ Preferences · `seed-share`, `save-game`, `undo-redo`, `import-open-formats` ↔ game ID.
- Перевикористано: `+neighbor-count-clue` ↔ число на вершині · `+loop-detection` ↔ заборона петель · `+half-cell-triangles` (Shakashaka) ↔ діагональ як стан клітинки · `+solve-into-undo`.
- **Нема** → пропозиції карток:
  - `+vertex-clue` «Підказки на вершинах сітки, не в клітинках» · field/render · 📎 — Slant, Tentai Show (центри), Slitherlink-варіанти.
  - `+tri-state-click-cycle` «Клік по колу через три стани, правий — назад» · interface/input · 🌱 (ширше за `flag-cycle`).

## Пропозиції до словників
- `+cond:no_loop(lines)` — граф ліній не містить циклу (протилежність `single_loop`).
- `+cond:lines_at(vertex, n)` — у вершині сходиться рівно n ліній.
- `+card:vertex-clue`, `+card:tri-state-click-cycle` — див. мапу.
- `+window:params-dialog`, `+window:game-id-dialog` — повтор Tatham-вікон.

## Джерела
- ⭐ [Tatham: Slant](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/slant.html) — правила, «zero can't appear in the interior», керування (цикл трьох станів, Return/Space, `/` і `\`, Backspace), Custom (Width, Height, Difficulty), «Hard… guesswork and backtracking should never be necessary», Preferences (кнопки миші), «Credit… Nikoli».
- [Tatham: Slant (грати)](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/slant.html) — меню Game, кнопки, коротка інструкція, drag-ресайз.
- [Wikipedia: Gokigen Naname](https://en.wikipedia.org/wiki/Gokigen_Naname) — правила, «single network of lines is not required», «binary-determination».
- [pzpr.js: gokigen](https://puzz.link/js/pzpr-samples/gokigen.js) — правила EN/JA, «Puzzle Communication Nikoli vol. 104», коди помилок.
- YouTube: пошук «gokigen naname slant puzzle».

## Непевне
- (?) Рік появи: pzpr каже Nikoli vol. 104, дати випуску не бачив (`year: null`).
- (?) Повний список рівнів складності Tatham (у мануалі описано лише Hard; ймовірно Easy/Hard).
- (?) Чи підсвічує Tatham петлі й переповнені вершини — не описано.
- (?) Техніка «1–1 / 3–3 по ребру» — з памʼяті, у джерелах не бачив.
- (?) Що означають режими `use,1` / `use,2` у pzpr — з тестів не зрозуміло.
