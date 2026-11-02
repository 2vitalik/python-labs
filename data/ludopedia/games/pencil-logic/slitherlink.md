---
title: Slitherlink (Слізерлінк, Loopy, Fences)
slug: slitherlink
family: pencil-logic
also: [connect-rotate]
klass: puzzle
axes:
  field: graph
  time: static
  opponent: none
  info: full
  random: setup
  goal: constraints
year: 1989
platforms: [paper, web, mobile, WonderSwan, Game Boy, Nintendo DS]
links:
  - {kind: play, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/loopy.html", best: true, note: "Tatham Loopy: грати в браузері, правила під полем, меню Type — інші плитки"}
  - {kind: official, url: "https://www.nikoli.co.jp/en/puzzles/slitherlink/", note: "Nikoli: 3 правила, числа 0–3, приклад"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Slitherlink", note: "правила, Nikoli №26 (1989), назви, відеоігри, інші графи"}
  - {kind: official, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/loopy.html", note: "Loopy: керування, типи сіток, складність"}
  - {kind: official, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/common.html", note: "спільні дії Tatham: undo/redo, solve, Game ID, seed"}
  - {kind: play, url: "https://puzz.link/rules.html?slither", note: "puzz.link: плеєр з автоперевіркою"}
  - {kind: official, url: "https://puzz.link/js/pzpr-samples/slither.js", note: "текст правил і тест вводу (лінія/хрестик)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=slitherlink+how+to+solve", note: "пошук; техніки"}
stage: v1
coverage: 80
mechanics: [markup-validity, completion-detection, satisfy-constraints, cell-click, unique-puzzle-generation, difficulty-rating, level-solver, import-open-formats, +edge-marking, +single-loop-check, +grid-tilings, +inside-outside-coloring]
proposes: ["+role:edge", "+trigger:pattern(loop_closed)", "+effect:mark_edge", "+ui:edge-cross", "+axis:field-edges"]
author: opus
date: 2026-11-02
---

# Slitherlink — одна замкнена петля по ребрах сітки; число = скільки ребер клітинки на петлі

## Суть
Сітка точок; у частині клітинок — числа 0–3. Гравець малює лінії між сусідніми точками так, щоб вийшла **одна** замкнена петля без розгалужень і самоперетинів, а кожне число дорівнювало кількості сторін своєї клітинки, що лежать на петлі. Незвичне для корпусу: розмічаються **ребра**, а не клітинки — поле фактично граф (вершини-точки, ребра-кандидати), і тому гра легко переноситься на трикутні, гексагональні й апериодичні плитки (Tatham Loopy).

## Поле і час
- Квадратна сітка точок (класика Nikoli); клітинки — грані графа, ребра — кандидати лінії. Wikipedia: замість квадратної — інші планарні графи (snowflake, Penrose, Laves, Altair).
- Tatham Loopy: square (default), triangular, honeycomb, Cairo, Kites, Great Hexagonal та інші «екзотичні» плитки в меню Type.
- Стан ребра: unknown / line / cross («точно не лінія»). Число в клітинці — 0…3 для квадрата (на інших плитках — до кількості сторін грані).
- Час статичний; хід = зміна стану одного ребра.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Точка (вершина) | static | ступінь у петлі 0 або 2 | у розвʼязку має 0 або 2 лінії; 1 або 3+ — порушення |
| Ребро | mark | unknown / line / cross | ліва кнопка — line, права — cross; повтор повертає unknown |
| Клітинка з числом | static | N ∈ 0..sides | рівно N її ребер — line |
| Порожня клітинка | static | — | будь-яка кількість ребер |
| Петля | zone | довжина | усі line-ребра = один простий цикл |
| Внутрішня/зовнішня область | zone | колір in/out | клітинки по різні боки петлі; техніка розвʼязання (Jordan) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left_click, edge)` → ТО `mark(edge, line)`; повтор → `unmark(edge)`.
- КОЛИ `input(right_click, edge)` → ТО `mark(edge, cross)`; повтор → `unmark(edge)` (Tatham, puzz.link).
- КОЛИ `constraint_broken(clue_count)` — `custom: «line-ребер навколо числа > N, або line + unknown < N»` → ТО `custom: «число підсвічується помилкою»` (?).
- КОЛИ `constraint_broken(vertex_degree)` — вершина з 3–4 лініями (розгалуження) → ТО конфлікт.
- КОЛИ `pattern(loop_closed)` → ЯКЩО `custom: «є line-ребра поза цим циклом»` → ТО `constraint_broken(single_loop)`; закрита мала петля — помилка, навіть якщо локально все ок.
- КОЛИ `input(check)` (puzz.link) → ТО `message(перше порушене правило)`.
- КОЛИ `all_constraints_met` — одна петля, усі ступені 0/2, усі числа точні → ТО `win`, `flash` (Tatham — спалах поля при розвʼязанні (?)).
- Перемога: петля єдина й усі числа виконано. Поразки й рахунку нема; у DS-версіях — час (?).

## Керування і ввід
- Мишка: ліва кнопка по ребру — лінія, права — хрестик (X); повтор — знову невідомо. Хрестик — «олівець» Slitherlink: заборона ребра без впливу на перевірку.
- puzz.link: drag малює лінію по ланцюжку точок (`mouse,left, x1,y1, x2,y2…`), права з drag — хрестики на шляху.
- Клавіатура (puzz.link edit): курсор + цифра ставлять підказки — редактор того ж жанру.
- Tatham: Undo/Redo, Restart, Solve, Game ID / seed; на тачі довге натискання = права кнопка (?).

## Вікна, меню, HUD
- `game-screen`: сітка точок, ребра трьох станів, числа; помилкові числа/вершини підсвічуються (Loopy: «червоні» перевантажені числа (?)).
- Меню Tatham (HTML-сторінка): Game — Enter game ID, Enter random seed, Download/Upload save file, Preferences; Type — розміри й плитки + Custom; кнопки New game · Restart · Undo · Redo · Solve.
- `difficulty-select` — у Custom-параметрах Loopy (Difficulty) + тип плитки (меню Type).
- `help-window` — правила під полем (Tatham) / сторінка правил (Nikoli, puzz.link).
- `end-screen` — нема окремого: спалах і стан «solved» (Tatham).

## Фічі поза полем
- `seed-input`, `seed-display`, `share-code` (Game ID Tatham, URL puzz.link), `export-import` (save file з повною історією undo).
- `undo`/`redo` необмежені, `show-solution` (Solve додається в історію — можна скасувати).
- `custom-difficulty`: розмір, тип плитки, складність генерації.
- `puzzle-bank` (Nikoli, Conceptis), `level-editor` (puzz.link edit mode).

## Варіації й родичі
- Плитки: квадрат / трикутник / гекс / Cairo / Kites / Great Hexagonal / Penrose (Loopy, Wikipedia).
- Ранній вигляд: у першому пазлі Nikoli №26 числа були в кожній клітинці і петля не вимагалась — редактор злив два пазли в один.
- Родичі «петлі»: Masyu, Yajilin, Country Road, Castle Wall — інша підказка, та сама перевірка «одна петля».
- Відеоігри: Slither Link (Bandai, WonderSwan, 2000), Kangaeru Puzzle (Game Boy, 2001), Puzzle Series Vol. 5 (DS, 2006), Brain Buster Puzzle Pak (DS, 2007).
- **Осі варіацій**: що розмічається (клітинки / ребра / лінії між центрами) · топологія (квадрат / гекс / апериодична) · глобальна умова (одна петля / шлях / кілька петель).

## Цікавинки для курсу
- Модель «граф ребер» замість клітинок: зберігання ребер, рендер ліній між точками — 📎 (консоль: `+`, `-`, `|`, `x`).
- Перевірка «рівно одна петля»: ступені вершин + обхід компоненти — 🥉.
- Ліва/права кнопка по ребру (лінія/хрестик) з вибором найближчого ребра до курсора — 🥉.
- Інші плитки (трикутна, гекс) з тим самим двіжком — 🥈 (абстракція графа замість масиву).
- Розвʼязувач локальними шаблонами (0, кутові 3, суміжні 3) + розфарбування in/out — 🥇.
- Генерація: випадкова петля → підказки → прибирання до єдиного розвʼязку — 👑.

## Мапа на каталог
- Є: `markup-validity` ↔ перевантажені числа й розгалуження · `completion-detection`, `satisfy-constraints` · `cell-click` (по ребру) · `unique-puzzle-generation`, `difficulty-rating`, `level-solver` ↔ Tatham · `import-open-formats` ↔ Game ID, pzprv3.
- **Нема** → пропозиції карток:
  - `+edge-marking` «Розмітка ребер (лінія / хрестик)» · interface/input · 🥉.
  - `+single-loop-check` «Одна петля: ступені вершин і звʼязність» · game-logic/constraints · 🥉.
  - `+grid-tilings` «Те саме правило на інших плитках» · levels/format · 🥈 · слот {tiling}.
  - `+inside-outside-coloring` «Розфарбування всередині/зовні петлі» · interface/input · 📎.

## Пропозиції до словників
- `+role:edge` — ребро між клітинками як сутність розмітки (Slitherlink, Bridges, тонкі стіни).
- `+trigger:pattern(loop_closed)` — уже є в прикладах `pattern`; тут — головна умова гри.
- `+effect:mark_edge` — розмітка ребра (`mark(cell, …)` не покриває ребра).
- `+ui:edge-cross` — хрестик «тут не лінія».
- `+axis:field-edges` — значення осі `field` або окрема вісь: гра розмічає ребра, а не клітинки.

## Джерела
- ⭐ [Tatham Loopy (грати)](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/loopy.html) — гра в браузері, правила під полем, меню Type з плитками.
- [Nikoli: Slitherlink](https://www.nikoli.co.jp/en/puzzles/slitherlink/) — правила, числа 0–3, «Sli-Lin».
- [Wikipedia: Slitherlink](https://en.wikipedia.org/wiki/Slitherlink) — історія №26 (червень 1989), назви, графи, відеоігри, NP-повнота.
- [Tatham Loopy doc](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/loopy.html) і [спільні дії](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/common.html).
- [puzz.link](https://puzz.link/rules.html?slither) і [slither.js](https://puzz.link/js/pzpr-samples/slither.js) — правила, тести вводу.
- YouTube: пошук «slitherlink how to solve».

## Непевне
- (?) Повний список плиток Loopy (snub square, octagonal, Floret, dodecagonal, Penrose, hats…) — doc називає лише 6, решту «exotic».
- (?) Як Loopy підсвічує помилки (червоні числа, точки з 3 лініями) і спалах при розвʼязанні — з памʼяті.
- (?) Довге натискання = права кнопка на тачі; таймер у DS-версіях.
