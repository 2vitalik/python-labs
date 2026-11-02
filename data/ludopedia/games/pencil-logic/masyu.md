---
title: Masyu (Pearl, «Перлини»)
slug: masyu
family: pencil-logic
also: [connect-rotate]
klass: puzzle
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: none
  goal: constraints
year: 1999
platforms: [paper, PC, web, mobile, Switch]
links:
  - {kind: official, url: "https://www.nikoli.co.jp/en/puzzles/masyu/", best: true, note: "Nikoli: чотири правила з картинками-прикладами"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Masyu", note: "історія назв, техніки, NP-повнота, варіанти (сірі перлини, тор, гекс)"}
  - {kind: official, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/pearl.html", note: "Tatham Pearl: керування drag/хрестики, Allow unsoluble, Loopy-style"}
  - {kind: play, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/pearl.html", note: "грати в браузері (Tatham)"}
  - {kind: play, url: "https://www.puzzle-masyu.com/", note: "онлайн 6×6…25×25, daily, таймер"}
  - {kind: other, url: "https://www.gmpuzzles.com/blog/?p=483", note: "Grandmaster Puzzles: правила й історія Masyu"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=masyu+puzzle+solve", note: "пошук; розвʼязання"}
stage: v1
coverage: 75
mechanics: [satisfy-constraints, markup-validity, completion-detection, cell-click, keyboard-controls, hover-highlight, unique-puzzle-generation, difficulty-levels, difficulty-rating, level-solver, field-size-picker, daily-puzzle, +undo-redo, +edge-marking, +single-loop-check, +turn-straight-clue, +drag-draw-path, +seed-share]
proposes: ["+trigger:input", "+trigger:constraint_broken", "+trigger:all_constraints_met", "+trigger:pattern", "+effect:mark", "+effect:unmark", "+cond:turns", "+cond:connected", "+role:mark", "+ui:conflict-highlight", "+ui:path-preview", "+feature:auto-check", "+feature:theme-select"]
author: opus
date: 2026-11-02
---

# Masyu — одна петля крізь усі перлини: на білій — прямо, на чорній — поворот

## Суть
На сітці стоять білі й чорні кола-«перлини». Треба провести одну замкнену петлю через центри клітин (лише по горизонталі/вертикалі), без самоперетинів і розгалужень, що проходить крізь усі перлини. Біла: петля йде через неї прямо і повертає хоча б в одній сусідній по петлі клітині; чорна: петля повертає на ній і йде прямо щонайменше одну клітину в обидва боки. Усе розвʼязання — локальна геометрія поворотів плюс глобальне «петля одна».

## Поле і час
- Прямокутна сітка; петля — набір ребер між центрами сусідніх клітин; кожна клітина має степінь 0 (не відвідана) або 2 (прямо / кут).
- Петля не мусить відвідати всі клітини — лише всі перлини.
- Tatham: альтернативний вигляд «Loopy-style» — петля по вершинах сітки, перлини на вершинах (те саме з точністю до дуальності).
- Час статичний; хід = провести/стерти сегмент або поставити хрестик «тут петлі нема».

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Біла перлина | static | — | петля проходить прямо; поворот у ≥1 з двох сусідніх по петлі клітин |
| Чорна перлина | static | — | петля повертає на 90°; обидва сусіди по петлі — прямі (2 клітини прямо в кожну гілку) |
| Сегмент петлі | mark | ребро між двома клітинами | частина єдиної петлі; у клітині сходяться 0 або 2 сегменти |
| Хрестик | mark | ребро | гравець фіксує «тут петлі нема» (правий клік) |
| Клітина | static | тип: порожня / пряма / кут | визначається сегментами, що в неї входять |
| Петля | zone | довжина | одна замкнена, без розгалужень і перетинів |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(click, edge)` → ТО `mark(edge, segment)` toggle; КОЛИ `input(right_click, edge)` → ТО `mark(edge, cross)` toggle.
- КОЛИ `input(drag, cells…)` → ТО `mark(edge, segment)` уздовж шляху; drag по вже наявній петлі стирає її або відгалужує в новий бік.
- КОЛИ `constraint_broken(degree(cell) > 2)` → ТО клітина/сегменти підсвічуються (розгалуження).
- КОЛИ `constraint_broken(white)` → ЯКЩО `turns(white)` або `custom: «обидва сусіди по петлі прямі»` → ТО перлина червона.
- КОЛИ `constraint_broken(black)` → ЯКЩО `not turns(black)` або `custom: «сусід по петлі сам є кутом»` → ТО перлина червона.
- КОЛИ `pattern(loop_closed)` → ЯКЩО `custom: «лишились сегменти поза петлею або перлини не на петлі»` → ТО `custom: «передчасне коротке замикання — помилка»`.
- КОЛИ `all_constraints_met` (одна петля, усі перлини на ній, усі умови кіл виконано) → ТО `win`, `flash(completion)`.
- Уточнення Tatham: умова перлини стосується лише двох клітин, з якими петля реально зʼєднує перлину, а не всіх сусідів по сітці.
- Перемога: одна замкнена петля через усі перлини з виконаними умовами. Поразки нема. Рахунок нема (онлайн — час).
- Дедукції: чорна біля краю/іншої чорної — гілка йде від краю; біла на краю — петля йде паралельно краю; три білі в ряд — петля перетинає їх перпендикулярно; дві чорні поруч — гілки розходяться назовні; парність: розріз сітки петля перетинає парну кількість разів (теорема Жордана); заборона передчасного замикання.

## Керування і ввід
- Tatham: лівий клік по ребру — сегмент вкл/викл; лівий drag крізь клітини — малювати кілька сегментів (по старій петлі — стирати/перенаправляти); правий клік — хрестик.
- Tatham (клавіатура): стрілки — курсор; Enter — почати/закінчити drag; Space/Escape/Backspace — скасувати drag; Ctrl+стрілки — малювати по ходу; Shift+стрілка — хрестик на ребрі; Ctrl+Shift+стрілка — сегмент.
- puzzle-masyu.com: лівий клік між точками — зʼєднати; правий — X у клітині; опція «ghost lines».
- Папір: олівцем лінії, хрестиками — заборонені ребра.

## Вікна, меню, HUD
- `game-screen`: поле з перлинами, сегменти, хрестики, `conflict-highlight` (порушені перлини, розгалуження), `path-preview` під час drag.
- Tatham: Type/Custom (`params-dialog`: Width, Height, Difficulty, Allow unsoluble), Preferences (`settings-window`: Traditional / Loopy-style — `theme-select` для геометрії), Specific/Random Seed.
- puzzle-masyu.com: `timer-elapsed` (можна сховати/особистий), Done, Start Over, розміри 6×6…25×25 × Easy/Normal/Hard, Special Daily/Weekly/Monthly, Hall of Fame, `stats-window`, опції: сітка, координати, checkpoints, підсвітка останньої зміни, підсвітка хибних ходів, нічний режим.
- Переходи: вибір розміру → game-screen → Done/автосабміт → результат (онлайн) або спалах (Tatham).

## Фічі поза полем
- `difficulty-presets` + `custom-difficulty`; Tatham «Allow unsoluble» — швидка генерація великих полів без гарантії єдиності.
- `undo`/`redo`, `auto-solve`, `seed-input`/`share-code` (Tatham); `checkpoint`-и й «підсвітка хибних ходів» (`auto-check`) онлайн.
- `daily-puzzle`, `leaderboard-online`, `stats`, друк, permalink прогресу (puzzle-masyu.com).
- «Puzzle by Nikoli S Masyu» — комерційна версія для Nintendo Switch (банк пазлів від Nikoli) (?).

## Варіації й родичі
- Історія: Puzzle Communication Nikoli #84 «Shinju no Kubikazari» («перлинове намисто») — лише білі (1999, Ryou Yano за Atlas Obscura); #90 додано чорні — «Shiroshinju Kuroshinju» (2000); #103 — назва Masyu (перекручене прочитання 真珠 «shinju»).
- Варіанти: **сірі перлини** (гравець вирішує, біла вона чи чорна) · **тор** (краї склеєні) · **регіони** (петля повертає хоч раз у кожному регіоні) · **гекс** (повороти 60°/120°).
- Родичі «одна петля»: Slitherlink (Loopy) — петля по ребрах за числами; Tracks; Yajilin; Pearl = Tatham-реалізація.
- **Осі варіацій**: де живе петля (центри клітин / вершини) · що задає підказка (поворот / прямо / кількість ребер / напрямок) · мусить відвідати (усі підказки / усі клітини / регіони) · топологія (прямокутник / тор / гекс).

## Цікавинки для курсу
- Перевірка «одна замкнена петля»: степені вершин 0/2 + одна компонента обходом — 🥉.
- Локальні умови білої/чорної перлини через типи клітин (пряма/кут) — 📎 кожна.
- Drag-малювання шляху, де повторний прохід стирає або перенаправляє, + хрестики правим кліком — 🥉 (ввід на ребрах).
- Детектор передчасного замикання й парність розрізу як підказки — 🥈.
- Солвер: поширення локальних дедукцій + глобальна заборона малих циклів + бектрекінг — 🥇; генератор з гарантією єдиності — 👑.
- Перемикач геометрії (центри ↔ вершини) як тема відображення без зміни логіки — 📎 (`logic-render-split`).

## Мапа на каталог
- Є: `satisfy-constraints` · `markup-validity` · `completion-detection` · `cell-click` · `keyboard-controls` · `hover-highlight` · `unique-puzzle-generation` · `difficulty-levels` · `difficulty-rating` · `level-solver` · `field-size-picker` · `daily-puzzle`.
- **Нема** → пропозиції карток:
  - `+undo-redo` (уже є в корпусі).
  - `+edge-marking` (є в slitherlink) — сегмент / хрестик.
  - `+single-loop-check` (є в slitherlink) — одна замкнена петля.
  - `+turn-straight-clue` «Підказка повороту/прямоти на клітині» · game-logic/constraints · 📎 · слот {kind: white|black|gray}.
  - `+drag-draw-path` «Малювання шляху протягуванням (зі стиранням зворотним ходом)» · interface/input · 🥉 — Masyu, Flow Free, Tracks.
  - `+seed-share` (пропоновано).

## Пропозиції до словників
- `+trigger:input`, `+trigger:constraint_broken`, `+trigger:all_constraints_met`; `+trigger:pattern` з `loop_closed` — уже ⏳, тут потрібен.
- `+effect:mark` / `+effect:unmark` — на ребрі.
- `+cond:turns(cell)` — петля в клітині повертає (кут), а не йде прямо; `+cond:connected(set)` — одна компонента.
- `+role:mark` — сегмент, хрестик.
- `+ui:conflict-highlight`, `+ui:path-preview` — лінія під час drag.
- `+feature:auto-check`, `+feature:theme-select` — Traditional / Loopy-style.

## Джерела
- ⭐ [Nikoli: Masyu](https://www.nikoli.co.jp/en/puzzles/masyu/) — чотири правила з прикладами від автора жанру.
- [Wikipedia: Masyu](https://en.wikipedia.org/wiki/Masyu) — історія назв (#84/#90/#103), техніки, NP-повнота (Friedman), варіанти.
- [Tatham: Pearl](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/pearl.html) — керування, параметри, Loopy-style; [грати](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/pearl.html).
- [puzzle-masyu.com](https://www.puzzle-masyu.com/) — онлайн-версія: розміри, опції підсвіток, daily, Hall of Fame.
- [Grandmaster Puzzles: Masyu Rules and Info](https://www.gmpuzzles.com/blog/?p=483) — правила й дата 2000 (Communication 90).
- YouTube: [пошук «masyu puzzle solve»](https://www.youtube.com/results?search_query=masyu+puzzle+solve).

## Непевне
- (?) Рік: 1999 (#84, лише білі) чи 2000 (#90, з чорними) — джерела розходяться; взято 1999.
- (?) Nintendo Switch «Puzzle by Nikoli S Masyu» — бачив лише в результатах пошуку, сторінку не відкривав.
- (?) GMPuzzles-сторінку не відкривав — лише заголовок у пошуку.
