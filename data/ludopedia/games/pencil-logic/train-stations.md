---
title: Train Stations
slug: train-stations
aka: [trainstations, Залізничні станції, Станції]
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
year: null
platforms: [web]
links:
  - {kind: play, url: "https://puzz.link/rules.html?trainstations", best: true, note: "puzz.link: правила EN і вхід у плеєр/редактор (сторінка рендериться JS)"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/trainstations.js", note: "4 правила EN, «invented by Craig Kasper», приклад 6×6, 14 тест-дошок і 3 сценарії вводу"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/main/src/variety/trainstations.js", note: "код pzprjs: хрести, станції «?», порожні клітинки, обхід петлі з перевіркою порядку; спільний скрипт з Turn and Run"}
  - {kind: other, url: "https://api.github.com/repos/robx/pzprjs/commits?path=src/variety/trainstations.js", note: "історія файла: Add Train Stations 2023-02-21, порожні клітинки 2023-02-24, «?» 2023-02-25, Turn and Run 2025-01-20"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/main/src/res/failcode.en.json", note: "тексти помилок: lnCurveOnNum, nmNotConseq, lnNotCrossMk…"}
  - {kind: other, url: "https://www.gmpuzzles.com/blog/2014/10/round-trip-craig-kasper/", note: "інший жанр того ж автора: Round Trip — петля з прямими самоперетинами (GM Puzzles, 2014)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=train+stations+puzzle+loop", note: "пошук"}
stage: v1
coverage: 65
mechanics: [path-drawing, edge-marking, single-loop-check, satisfy-constraints, markup-validity, completion-detection, conflict-highlight, keyboard-controls, in-game-editor, editor-window, import-open-formats, undo-redo, help-window, fixture-level-tests, level-solver, +forced-crossing-cell, +ordered-checkpoints, +turn-straight-clue, +wildcard-clue, +fill-all-cells, +obstacle-cells, +aux-direction-marks, +crossing-detection, +trial-mode]
proposes: ["+cond:turns", "+cond:crosses", "+cond:degree", "+cond:order_next", "+ui:loop-color-coding"]
author: opus
date: 2026-11-19
---

# Train Stations — петля крізь усі клітинки, що перетинає себе лише на хрестах і обʼїжджає станції за номерами

## Суть
Гравець малює одну замкнену лінію-«колію» через центри клітинок так, щоб вона пройшла кожну клітинку. Перетинати себе петля може лише в клітинках-хрестах, і в кожному хресті мусить перетнутися; більше ніде. Кружечки з числами — станції: їхати через них треба навпростець, а самі станції петля має проїжджати по черзі 1 → 2 → … → N і знову 1. Незвичне: порядок на **циклі** (напрям обходу петля обирає сама, «?»-станція бере будь-який потрібний номер), а самоперетини задано наперед.

## Поле і час
- Квадратна сітка; приклад puzz.link — 6×6 з 4 станціями й 2 хрестами, тести — 3×3 і 4×4.
- Клітинка: звичайна · станція (номер або «?») · хрест «+» · порожня (чорна, поза петлею; з 2023-02-24).
- Лінія йде по центрах клітинок між ортогональними сусідами; на хресті — прямо в обидва боки, тобто клітинку проходять двічі.
- Шари: умова (станції, хрести, порожні) · лінії гравця · допоміжні хрестики × і стрілки напрямку на межах.
- Час статичний; хід = провести або стерти відрізок лінії.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Станція | static | номер 1…N (N — кількість станцій) або «?» | лінія йде через неї прямо; номери йдуть по петлі поспіль |
| Станція «?» | static | — | займає в черзі той номер, що потрібен |
| Хрест «+» | static | — | лінія тут обовʼязково перетинає себе (4 виходи) |
| Порожня клітинка | static | чорна | лінія сюди не заходить і не покриває її |
| Звичайна клітинка | terrain | — | рівно 2 виходи лінії |
| Лінія | mark | — | одна петля без розгалужень і тупиків |
| Хрестик × | mark | на межі | «тут лінії нема», допоміжний |
| Стрілка напрямку | mark | на межі | допоміжна позначка руху; перевірка її не бачить |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag, cells)` → ЯКЩО `not cell(x, empty)` → ТО `mark(edges, line)`; протяжка по наявній лінії → `unmark(edges)`.
- КОЛИ `input(right_drag, edge)` → ТО `mark(edge, cross)` або `mark(edge, arrow)` — залежно від того, де почато протяжку (допоміжні, не перевіряються).
- КОЛИ `constraint_broken(range)` → ЯКЩО `custom: «номер станції більший за кількість станцій»` → ТО `set_state(station, error)`, `message(«A number is out of range.»)` (код nmRange).
- КОЛИ `constraint_broken(branch)` → ЯКЩО `custom: «у клітинці 3 лінії»` (`+cond:degree`) → ТО `set_state(cell, error)`, `message(«There is a branch line.»)` (lnBranch).
- КОЛИ `constraint_broken(cross_outside)` → ЯКЩО `custom: «4 лінії в клітинці без хреста»` (`+cond:crosses`) → ТО `set_state(cell, error)`, `message(«There is a crossing outside given crosses.»)` (lnCrossExMk).
- КОЛИ `constraint_broken(curve_on_station)` → ЯКЩО `occupied(cell, station)` and `custom: «лінія в ній повертає»` (`+cond:turns`) → ТО `set_state(station, error)`, `message(«A line turns on a station.»)` (lnCurveOnNum).
- КОЛИ `constraint_broken(order)` → ЯКЩО `custom: «дві сусідні по лінії станції різняться не на 1 і не як N → 1»` (`+cond:order_next`) → ТО `set_state(path, error)`, `message(«A number doesn't connect to the next consecutive number.»)` (nmNotConseq; «?» тут пропускається).
- КОЛИ `constraint_broken(cross_mark)` → ЯКЩО `occupied(cell, cross)` and `custom: «у хресті не 4 лінії»` → ТО `set_state(cell, error)`, `message(«A cross-joint cell doesn't have four-way lines.»)` (lnNotCrossMk).
- КОЛИ `constraint_broken(dead_end)` → ЯКЩО `custom: «у клітинці 1 лінія»` (`+cond:degree`) → ТО `set_state(cell, error)`, `message(«There is a dead-end line.»)` (lnDeadEnd).
- КОЛИ `constraint_broken(multi_loop)` → ЯКЩО `not single_loop` → ТО `set_state(other_loop, error)`, `message(«There are multiple loops.»)` (lnPlLoop).
- КОЛИ `constraint_broken(order_full)` → ЯКЩО `custom: «обхід петлі від найменшої станції дає не 1, 2, 3… (кожна «?» бере наступний номер)»` (`+cond:order_next`) → ТО `set_state(shorter_arc, error)`, `message(«A number doesn't connect to the next consecutive number.»)` (nmNotConseqFull).
- КОЛИ `constraint_broken(empty_cell)` → ЯКЩО `not cover_all(cell)` → ТО `set_state(cell, error)`, `message(«There is an empty cell.»)` (ceNoLine; порожні чорні не рахуються).
- КОЛИ `all_constraints_met` → ТО `win`.
- Обхід петлі в коді: від найменшої станції в обидва боки; на хресті — прямо, деінде — у єдиний інший вихід; тому петля з перетинами лишається одним циклом.
- Перемога: одна петля покриває всі непорожні клітинки, перетинається рівно на хрестах, на станціях не повертає, станції йдуть по колу 1 → … → N → 1. · Поразки й рахунку нема.
- Наслідки правил (дедукції): у кутовій клітинці лінія завжди повертає, тож станції в куті бути не може; станція на краю поля йде вздовж краю; усі 4 сусіди хреста зʼєднані з ним; клітинка поруч із порожньою має на один варіант менше.

## Керування і ввід
- puzz.link play: протяжка лівою — лінія через центри клітинок; клік лівою без руху — стрілка напрямку на межі; права кнопка — хрестики × або стрілки протяжкою; режими `line` · `peke` · `diraux` · `clear` · `info-line` (підсвітити звʼязану лінію).
- puzz.link edit: клік по клітинці перебирає «нічого → ? → хрест → 1 → 2 → …», права кнопка — назад (тест вводу); клавіша `q` — хрест; режим `empty` — порожня клітинка; цифри — номер станції.
- Кольори петлі (`irowake`) — кожна компонента лінії своїм кольором.

## Вікна, меню, HUD
- `game-screen` (puzz.link): сітка, станції — білі кружки з номером або «?», хрести — товстий знак «+», порожні клітинки чорні з рамкою; лінії, хрестики, стрілки; кнопки Check · Undo · Redo · Erase answer · Erase marks · Colour all · Trial (оболонка — [puzz.link](puzz-link.md)); `conflict-highlight` — клітинка з помилкою або коротша дуга петлі з порушеним порядком.
- `editor-window` — той самий екран у режимі Edit: number · undef · empty · clear, вивід URL.
- `help-window` — rules.html?trainstations (правила лише англійською).
- Переходи: rules → плеєр за URL → Check → «розвʼязано» або текст першої помилки.

## Фічі поза полем
- `auto-check` і Check з текстом першої помилки; `undo` ∞ / `redo`; `+feature:trial-mode` (puzz.link).
- `+ui:loop-color-coding` (irowake) і підсвітка звʼязаної лінії (`info-line`).
- `level-editor` + `share-code` (URL `p?trainstations/6/6/…`), файли pzprv3.
- Нема генератора, банку рівнів у жанрі, підказок.

## Варіації й родичі
- Turn and Run (トツゲキループ, `turnrun`, у puzz.link з 2025-01-20) — той самий скрипт: на клітинці з числом петля мусить повернути, а число — довжина прямого відрізка, яким вона виходить із клітинки (за кодом перевірки); хрести — як тут; покриття всіх клітинок — лише у варіанті `loop_full`.
- [Suraromu](suraromu.md) — нумеровані ворота в заданому порядку від старту; тут — станції-клітинки по колу 1 → N → 1.
- [Masyu](masyu.md) — біла перлина «їдь прямо»; тут кожна станція — така перлина з номером.
- [Reflect Link](reflect-link.md) — самоперетин лише на заданих хрестах; [Icebarn](icebarn.md) — перетини лише на льоду.
- Round Trip (Craig Kasper, GM Puzzles, 2014) — інший жанр автора: петля, що перетинає себе під прямим кутом, з числами по краях.
- [Hidato](hidato.md), [Signpost](signpost.md) — порядок 1…N як нумерація клітинок, а не станції на петлі.
- **Осі варіацій**: покриття (усі клітинки / ні) · самоперетини (заборонені / лише на хрестах / будь-де під 90°) · порядок (нема / чекпоінти від старту / по колу з «?») · поведінка на числі (прямо — Train Stations / поворот із довжиною — Turn and Run).

## Цікавинки для курсу
- Ступені клітинок як перевірка: 2 скрізь, 4 лише на хресті, 0 лише в порожніх — 🌱.
- Обхід петлі з самоперетинами (на хресті — прямо, інакше — у єдиний інший вихід) — 📎.
- Порядок станцій на циклі: старт із найменшої, обидва напрямки, «?» як наступний номер, перехід N → 1 — 📎.
- Допоміжні стрілки напрямку на межах — шар розмітки, який перевірка ігнорує — 🌱.
- Розвʼязувач: гамільтонів цикл на сітці з фіксованими хрестами, прямими станціями й порядком — 🥇.
- Генератор з унікальним розвʼязком — 👑.

## Мапа на каталог
- Є: `path-drawing` ↔ лінія протяжкою · `edge-marking` ↔ хрестики × · `single-loop-check` ↔ одна петля · `satisfy-constraints`, `markup-validity`, `completion-detection`, `conflict-highlight` ↔ Check з кодами · `keyboard-controls` ↔ `q` і цифри · `in-game-editor`, `editor-window`, `import-open-formats` ↔ edit-режим, URL · `undo-redo` · `help-window` · `fixture-level-tests` ↔ тест-дошки · `level-solver`.
- Перевикористано: `+forced-crossing-cell` (Reflect Link; слот cross: given) · `+ordered-checkpoints` (Suraromu; слот {numbered: some, cyclic: true}) · `+turn-straight-clue` (Masyu; kind: straight) · `+wildcard-clue` («?»-станція) · `+fill-all-cells` · `+obstacle-cells` (порожні клітинки) · `+aux-direction-marks` (Arofuro) · `+crossing-detection` · `+trial-mode`.
- **Нема** → нових карток не треба: жанр складено з наявних механік.

## Пропозиції до словників
- `+cond:turns` — повтор: лінія повертає в клітинці.
- `+cond:crosses` — повтор: лінія перетинає себе в клітинці.
- `+cond:degree` — повтор: скільки ліній сходиться в клітинці.
- `+cond:order_next` — повтор (Railbound): наступна станція має очікуваний номер; тут по колу N → 1, «?» — будь-який.
- `+ui:loop-color-coding` — повтор: irowake фарбує лінії за компонентами.

## Джерела
- ⭐ [puzz.link: Train Stations](https://puzz.link/rules.html?trainstations) — правила й плеєр (текст рендериться JS).
- [pzpr-samples/trainstations.js](https://puzz.link/js/pzpr-samples/trainstations.js) — «Draw a loop that goes through every cell», «All cells where the loop crosses itself are given», «The stations must be visited in ascending order», «The loop cannot turn while visiting a station»; «This genre was invented by Craig Kasper»; тести lnBranch · lnCrossExMk · lnNotCrossMk · lnCurveOnNum · nmNotConseq · lnPlLoop · lnDeadEnd · ceNoLine · nmNotConseqFull · nmRange і сценарії вводу.
- [pzprjs trainstations.js](https://raw.githubusercontent.com/robx/pzprjs/main/src/variety/trainstations.js) — checklist, `trainstations_walkLine`, клавіша `q`, режими вводу, спільний код із `turnrun`.
- [Історія trainstations.js](https://api.github.com/repos/robx/pzprjs/commits?path=src/variety/trainstations.js) — дати додавання жанру, порожніх клітинок, «?» і Turn and Run (Lennard Sprong).
- [failcode.en.json](https://raw.githubusercontent.com/robx/pzprjs/main/src/res/failcode.en.json) — тексти помилок.
- [GM Puzzles: Round Trip by Craig Kasper](https://www.gmpuzzles.com/blog/2014/10/round-trip-craig-kasper/) — автор як гостьовий укладач GM Puzzles.
- YouTube: [пошук «train stations puzzle loop»](https://www.youtube.com/results?search_query=train+stations+puzzle+loop).

## Непевне
- (?) Автор — Craig Kasper лише за рядком історії puzz.link; першої публікації (рік, місце) два пошуки не знайшли → `year: null`; у puzz.link жанр з 2023-02-21.
- (?) «?»-станція за кодом лічиться як наступний номер обходу — тобто «будь-який номер, що пасує порядку»; окремого правила в тексті нема.
- (?) Послідовність кліків у редакторі виведено з тесту вводу (перший клік, схоже, лише ставить курсор); що саме дає права кнопка в play — з коду (`inputdiraux_mousedown` / `inputpeke`).
- (?) Правила Turn and Run — лише з коду перевірки (ceDirection «A line that exits a cell turns at the wrong position», lnStraightOnNum); pzpr-samples/turnrun.js віддає 404.
