---
title: Tents (Tatham)
slug: tents
aka: [Tents and Trees, Tents & Trees, Намети]
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
platforms: [PC, web, mobile, print]
links:
  - {kind: other, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/tents.html", best: true, note: "мануал Tatham: правила, миша й клавіатура, параметри Custom"}
  - {kind: play, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/tents.html", note: "грати в браузері (JS-версія колекції)"}
  - {kind: other, url: "https://www.brainbashers.com/tentshelp.asp", note: "BrainBashers: правила, «дерево може торкатись двох наметів, але повʼязане з одним»"}
  - {kind: other, url: "https://puzz.link/rules.html?tents", note: "puzz.link: правила (сторінка рендериться JS)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=tents+and+trees+puzzle", note: "пошук; розвʼязання"}
stage: v1
coverage: 65
mechanics: [markup-validity, completion-detection, satisfy-constraints, line-sum-clue, cell-click, keyboard-controls, unique-puzzle-generation, no-guess-generation, difficulty-levels, difficulty-rating, level-solver, field-size-picker, game-settings, seed-share, save-game, undo-redo, +tree-tent-matching, +no-touch-8, +drag-line-fill]
proposes: ["+cond:count_in(line, kind, op, n)", "+cond:perfect_matching(a, b)", "+window:params-dialog", "+window:game-id-dialog", "+card:tree-tent-matching", "+card:no-touch-8"]
author: opus
date: 2026-11-09
---

# Tents — постав біля кожного дерева свій намет так, щоб намети не торкались і збігались лічильники рядків

## Суть
На сітці стоять дерева. Гравець ставить намети в порожні клітинки: наметів стільки ж, скільки дерев, і їх можна попарно звʼязати «дерево — намет» по ортогональному сусідству. Намети не торкаються один одного навіть по діагоналі, а числа на краях кажуть, скільки наметів у кожному рядку й стовпці. Незвичне: прихована умова — існування паросполучення 1:1 між деревами й наметами, яке гравцеві не треба малювати, але вона відсікає багато розстановок.

## Поле і час
- Прямокутна сітка W×H; числа над стовпцями й біля рядків.
- Сусідство різне для різних правил: намет — дерево лише ортогонально (4), намет — намет заборонено в усіх 8 напрямках.
- Шари: дерева (незмінні) · намети гравця · «трава» — зелена мітка «тут намету нема».
- Час статичний; хід = поставити / зняти намет чи мітку. Пазл генерується (`random: setup`).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Порожня клітинка | terrain | — | може стати наметом або травою |
| Дерево | static | — | потребує рівно одного свого намету по ортогоналі |
| Намет | mark | — | ставить гравець; привʼязаний рівно до одного сусіднього дерева |
| Трава | mark | зелений колір | мітка «тут намету нема» |
| Число рядка / стовпця | mark | N | кількість наметів у лінії |
| Пара дерево–намет | zone | 2 клітинки | неявне паросполучення; гравець його не малює |
| Курсор | mark | клітинка | керування з клавіатури |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left_click, cell)` → ЯКЩО `free(cell)` → ТО `mark(cell, tent)`.
- КОЛИ `input(right_click, cell)` → ЯКЩО `free(cell)` → ТО `mark(cell, grass)`.
- КОЛИ `input(any_click, cell)` → ЯКЩО `custom: «у клітинці намет або трава»` → ТО `unmark(cell)`.
- КОЛИ `input(right_drag, line)` → ТО `custom: «усі порожні клітинки відрізка рядка/стовпця стають травою»`.
- КОЛИ `input(shift_arrow)` → ТО `mark(cell, grass)` (лише порожні); КОЛИ `input(ctrl_arrow)` → ТО `mark(cell, grass)` (і порожні, і намети).
- КОЛИ `constraint_broken(tent_touch)` → ЯКЩО `adjacent_count(tent, tent, >=, 1)` and `custom: «рахувати 8 сусідів, з діагоналями»` → ТО `custom: «пазл не розвʼязано»`.
- КОЛИ `constraint_broken(line_count)` → ЯКЩО `custom: «наметів у рядку/стовпці ≠ числу»` (`+cond:count_in`) → ТО `custom: «пазл не розвʼязано»`.
- КОЛИ `constraint_broken(pairing)` → ЯКЩО `custom: «нема паросполучення 1:1 дерево↔намет по ортогональних сусідах»` (`+cond:perfect_matching`) → ТО `custom: «пазл не розвʼязано»`.
- Дерево може торкатися двох і більше наметів, але «своїм» вважається лише один; намет теж може торкатися кількох дерев.
- КОЛИ `all_constraints_met` → ЯКЩО `count(tent, =, count(tree))` → ТО `win`.
- Дедукція «далеко від дерев»: клітинка без дерева серед 4 сусідів — трава.
- Дедукція «нуль і повна лінія»: число 0 — уся лінія трава; число = кількості можливих клітинок — усі вони намети.
- Дедукція «кільце»: навколо поставленого намету всі 8 клітинок — трава.
- Дедукція «одинак»: дерево, у якого лишилась одна можлива клітинка (і вона не забрана іншим деревом), отримує там намет.
- Перемога: наметів = дерев, усі в парах, не торкаються, лічильники збігаються. Поразки й рахунку нема.

## Керування і ввід
- Ліва кнопка по порожній клітинці — намет; права — трава; будь-яка кнопка по зайнятій — очистити.
- Права кнопка з drag по рядку чи стовпцю — трава на всі порожні клітинки відрізка.
- Клавіатура: стрілки — курсор; Return — намет / очистити; Space — трава / очистити; Shift+стрілка — трава на порожні клітинки по ходу; Ctrl+стрілка — трава і на намети теж.
- Спільні дії колекції Tatham (розд. 2.1): undo/redo, нова гра, рестарт, solve.

## Вікна, меню, HUD
- `game-screen`: сітка з деревами, намети, зелені клітинки трави, числа на краях, курсор.
- Веб-версія: кнопки New game · Restart game · Undo move · Redo move · Solve game; меню Game: Enter game ID… · Enter random seed… · Download / Upload save file… · Preferences….
- Меню Type: пресети; Custom… → `params-dialog` (Width, Height, Difficulty).
- `game-id-dialog` — Specific / Random Seed; `help-window` — розділ мануалу.
- Переходи: game-screen → Type → Custom → params-dialog → новий пазл.

## Фічі поза полем
- Генератор з єдиним розвʼязком; складність визначає глибину дедукцій, жоден рівень не вимагає вгадування (`no-guess-generation`).
- `undo` ∞ + `redo`, `restart-level`, `auto-solve`, `seed-display` / `seed-input` / `share-code`, збереження у файл.
- `custom-difficulty`: ширина й висота окремо.

## Варіації й родичі
- У сімʼї: [Tatham collection](tatham-collection.md) (оболонка), [Star Battle](star-battle.md) (обʼєкти не торкаються по діагоналі), [Light Up](light-up.md), [Tracks](tracks.md) і [Kakuro](kakuro.md) (лічильники рядків і стовпців), [Undead](undead.md).
- Жанр широко відомий як Tents and Trees (газети, BrainBashers, мобільні застосунки); Tatham пише, що автор жанру йому невідомий.
- **Осі варіацій**: заборона дотику (8 / лише 4 напрямки) · лічильники (усі лінії / частина прибрана) · пара дерево–намет (ортогональна / з діагоналлю) · поле (квадрат / гекс) · додаткові підказки в регіонах.

## Цікавинки для курсу
- Перевірка «намети не торкаються по 8 напрямках» і лічильники ліній — 🌱.
- Drag-заповнення травою і клавіатурні Shift/Ctrl-стрілки — 📎.
- Перевірка паросполучення дерев і наметів (алгоритм Куна / Hopcroft–Karp на двочастковому графі) — 🥉.
- Розвʼязувач на дедукціях «одинак», «кільце», «нуль» без перебору — 🥈.
- Генератор: розставити пари, порахувати лічильники, перевірити єдиність розвʼязувачем — 🥇.

## Мапа на каталог
- Є: `markup-validity`, `completion-detection`, `satisfy-constraints` · `line-sum-clue` ↔ числа рядків/стовпців · `cell-click`, `keyboard-controls` · `unique-puzzle-generation`, `no-guess-generation`, `difficulty-levels`, `difficulty-rating`, `level-solver` · `field-size-picker`, `game-settings` · `seed-share`, `save-game`, `undo-redo`.
- **Нема** → пропозиції карток:
  - `+tree-tent-matching` «Обʼєкти двох видів мають утворити паросполучення 1:1 по сусідству» · game-logic/constraints · 🥉 · слот {adjacency: 4|8}.
  - `+no-touch-8` «Однакові обʼєкти не торкаються навіть по діагоналі» · game-logic/constraints · 🌱 (спільна з Star Battle).
  - `+drag-line-fill` — повтор з Tracks: drag ставить однакові мітки на відрізок лінії.

## Пропозиції до словників
- `+cond:count_in(line, kind, op, n)` — кількість обʼєктів виду в рядку/стовпці/регіоні (повтор з інших пазлів сімʼї).
- `+cond:perfect_matching(a, b)` — існує паросполучення 1:1 між сутностями A і B по сусідству.
- `+window:params-dialog`, `+window:game-id-dialog` — повтори з Tatham collection.
- `+card:tree-tent-matching`, `+card:no-touch-8` — див. мапу.

## Джерела
- ⭐ [Tatham: Tents (мануал)](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/tents.html) — правила («No two tents are adjacent horizontally, vertically or diagonally»), миша, клавіатура з Shift/Ctrl-стрілками, параметри, примітка про невідомого автора.
- [Tatham: Tents (грати)](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/tents.html) — коротка інструкція, меню Game, кнопки.
- [BrainBashers: Tents help](https://www.brainbashers.com/tentshelp.asp) — ті самі правила; дерево може торкатися двох наметів, але повʼязане з одним.
- [puzz.link: Tents](https://puzz.link/rules.html?tents) — сторінка правил; текст рендериться JS і через WebFetch не читається.
- YouTube: пошук «tents and trees puzzle».

## Непевне
- (?) Назви рівнів складності (Easy / Tricky?) і пресети меню Type не бачив.
- (?) Підсвітка помилок (дерево без можливого намету, намети поруч) — у мануалі не описана.
- (?) Хто й коли придумав жанр — невідомо навіть Tatham; рік додавання в колекцію не перевірено (`year: null`).
- (?) Правила puzz.link-версії не прочитані (JS-сторінка); можливі відмінності в розмітці пар.
