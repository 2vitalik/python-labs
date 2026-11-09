---
title: Ququ
slug: ququ
aka: []
family: pencil-logic
also: []
klass: puzzle
axes:
  field: graph
  time: static
  opponent: none
  info: full
  random: none
  goal: constraints
year: null
platforms: [paper, web]
links:
  - {kind: other, url: "https://puzz.link/rules.html?ququ", best: true, note: "puzz.link: сторінка правил і плеєр (рендериться JS)"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/ququ.js", note: "puzz.link: правила EN/JA, «Puzzle Communication Nikoli vol. 171», коди помилок"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/master/src/variety/ququ.js", note: "pzprjs: геометрія 4 трикутники на клітинку, сусідство по ребру й по точці, порядок перевірок"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/master/src/res/failcode.en.json", note: "pzprjs: тексти помилок bkNoNum, bkNumGe2, bkSizeNe, bsSameShape"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=ququ+puzzle+nikoli", note: "пошук; розвʼязання"}
stage: v1
coverage: 65
mechanics: [markup-validity, completion-detection, satisfy-constraints, conflict-highlight, cell-click, keyboard-controls, dot-mark, undo-redo, in-game-editor, import-open-formats, +cell-shade-toggle, +triangle-subgrid, +shape-identity-check, +region-size-check, +one-clue-per-region]
proposes: ["+cond:same_shape", "+cond:touch_corner", "+axis:field=triangles", "+card:triangle-subgrid", "+card:one-clue-per-region"]
author: opus
date: 2026-11-09
---

# Ququ — квадрати, розрізані діагоналями на 4 трикутники: білі ділянки з одним числом-розміром, сусідні по куту чорні блоки різної форми

## Суть
Кожна клітинка квадратної сітки розрізана обома діагоналями на чотири трикутники. Гравець зафарбовує трикутники так, щоб незафарбовані, зʼєднані ребрами, склали ділянки з рівно одним числом (або «?»), і число дорівнювало розміру ділянки в трикутниках. Зафарбовані трикутники утворюють блоки; два блоки, що торкаються лише кутом, мусять мати різну форму (з точністю до поворотів і віддзеркалень). Незвичне: поле — граф трикутників, і «форма блоку» рахується на ньому, а не на квадратах.

## Поле і час
- Квадратна сітка, кожна клітинка = 4 трикутники Up/Left/Right/Down з вершиною в центрі клітинки (обидві діагоналі в кожній клітинці, напрям не чергується).
- Сусідство по ребру: два трикутники своєї клітинки (по діагоналях) + трикутник сусідньої клітинки через зовнішню сторону — разом 3 сусіди.
- Сусідство по точці (для правила форм): трикутники навколо спільних вершин — і в центрі клітинки, і в кутах сітки.
- Шари: підказка (число / «?» / порожньо) · стан гравця (зафарбований / білий / крапка).
- Час статичний; хід = змінити стан трикутника.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Трикутник | mark | позиція U/L/R/D у клітинці | зафарбований або білий; 3 сусіди по ребру |
| Число | static | N | стоїть у трикутнику, той не можна зафарбувати; ділянка з ним має N трикутників |
| «?» | static | — | як число невідомого розміру: займає ділянку, але розмір не задає |
| Біла ділянка | zone | розмір | звʼязна по ребрах; рівно одна підказка (число або «?») |
| Чорний блок | zone | форма | звʼязний по ребрах; з блоками, що торкаються кутом, — різна форма |
| Крапка | mark | — | допоміжна позначка «білий» |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(click, triangle)` → ТО `mark(triangle, shaded)` toggle; ЯКЩО `occupied(triangle, clue)` → ТО `block`.
- КОЛИ `input(right_click, triangle)` → ТО `mark(triangle, dot)` (?).
- КОЛИ `custom: «біла ділянка без підказки»` → ТО `constraint_broken(no_number)` (`bkNoNum`).
- КОЛИ `custom: «у білій ділянці ≥2 підказки»` → ТО `constraint_broken(many_numbers)` (`bkNumGe2`).
- КОЛИ `custom: «перевірка розміру»` → ЯКЩО `not region_size(white, N)` → ТО `constraint_broken(size)` (`bkSizeNe`); для «?» перевірки розміру нема.
- КОЛИ `custom: «два чорні блоки торкаються по точці»` → ЯКЩО `custom: «однакова форма з точністю до повороту й віддзеркалення»` → ТО `constraint_broken(same_shape)` (`bsSameShape`; `+cond:same_shape`, `+cond:touch_corner`).
- КОЛИ `custom: «лишились невирішені трикутники»` → ТО `constraint_broken(undecided)` (`doneShadingDecided` у pzprjs).
- КОЛИ `all_constraints_met` → ТО `win`.
- Порядок перевірок pzprjs: ділянка без числа → однакові форми по куту → кілька чисел → розмір → усе вирішено.
- Перемога: усі обмеження виконані. Поразки й рахунку нема.
- Обмежень на звʼязність чорних і на дотик чорних ребром нема: ребром торкаються — значить, це вже один блок.

## Керування і ввід
- puzz.link (play): режими `shade`, `unshade`, `info-blk` (показати блок під курсором); клік вибирає найближчий трикутник за положенням курсора в клітинці (`getpos` порівнює |dx| і |dy|).
- puzz.link (edit): режими `number`, `undef` («?»), `clear`; числа з клавіатури.
- Папір: зафарбувати олівцем трикутник.

## Вікна, меню, HUD
- `game-screen` (puzz.link): сітка з діагоналями, числа, зафарбування; `check-button`, `undo-button`, `redo-button`; `conflict-highlight` після перевірки (?); режим `info-blk` підсвічує блок/ділянку — `selection-highlight`.
- `editor-window` (puzz.link edit mode): числа, «?», розмір поля, експорт у URL.
- `help-window` — сторінка правил puzz.link.
- Переходи: rules → URL пазла → game-screen → Check → «правильно / помилка».

## Фічі поза полем
- `auto-check` за кнопкою (перший код помилки); `undo`/`redo`.
- `level-editor` + `share-code` — пазл як URL puzz.link.

## Варіації й родичі
- [lits](lits.md) — та сама ідея «сусідні блоки різної форми», але для тетроміно по ребру в кімнатах; [fillomino](fillomino.md), [nurikabe](nurikabe.md) — «ділянка з числом = розмір».
- [shakashaka](shakashaka.md), [tatham-collection](tatham-collection.md) — інші пазли з трикутниками/діагоналями на квадратній сітці.
- **Осі варіацій**: поділ клітинки (2 трикутники / 4 трикутники / квадрати) · сусідство для правила форм (ребро / кут) · еквівалентність форм (з поворотом / з віддзеркаленням / дослівно) · що задає число (розмір ділянки / розмір блоку).

## Цікавинки для курсу
- Поле-граф: id трикутника `cell*4 + pos`, таблиця сусідів по ребру й по точці — 📎; гарна вправа на «сітка ≠ масив».
- Канонічна форма блоку на трикутній підсітці під 8 симетріями квадрата — 🥉 (на квадратах — 📎).
- Перевірка ділянок: BFS по ребрах, рахунок підказок і розміру — 🌱.
- Розвʼязувач: розбиття білих на ділянки + заборона однакових форм по куту — 🥇; генератор з єдиним розвʼязком — 👑.

## Мапа на каталог
- Є: `markup-validity`, `conflict-highlight`, `completion-detection`, `satisfy-constraints` · `cell-click`, `dot-mark`, `keyboard-controls` · `in-game-editor`, `import-open-formats` ↔ URL puzz.link · `undo-redo`.
- **Нема** → пропозиції карток:
  - `+cell-shade-toggle`, `+shape-identity-check` (LITS), `+region-size-check` — уже пропоновані в корпусі.
  - `+triangle-subgrid` «Клітинка, поділена на 4 трикутники; сусідство по ребру й по точці» · entities/legality · 📎 · слот {split: 2|4}.
  - `+one-clue-per-region` «Кожна ділянка містить рівно одну підказку» · game-logic/constraints · 🌱.

## Пропозиції до словників
- `+cond:same_shape` — два блоки конгруентні з поворотом і віддзеркаленням (повтор з LITS).
- `+cond:touch_corner` — дві множини клітинок торкаються лише вершиною, не ребром.
- `+axis:field=triangles` — значення осі `field` для трикутної підсітки всередині квадратів (тут поки `graph`).
- `+card:triangle-subgrid`, `+card:one-clue-per-region` — див. мапу.

## Джерела
- ⭐ [puzz.link: Ququ](https://puzz.link/rules.html?ququ) — сторінка правил і плеєр (текст рендериться JS).
- [puzz.link ququ.js](https://puzz.link/js/pzpr-samples/ququ.js) — 5 правил EN/JA, «Puzzle Communication Nikoli vol. 171», коди помилок.
- [pzprjs variety/ququ.js](https://raw.githubusercontent.com/robx/pzprjs/master/src/variety/ququ.js) — геометрія U/L/R/D, `getPointAdjacent`, режими вводу, порядок перевірок.
- [pzprjs failcode.en.json](https://raw.githubusercontent.com/robx/pzprjs/master/src/res/failcode.en.json) — тексти `bsSameShape` тощо.
- YouTube: пошук «ququ puzzle nikoli».

## Непевне
- (?) Японську назву не бачив; рік — лише «Nikoli vol. 171», дату тому не перевіряв.
- (?) Чи «?» може бути у трикутнику, а чи зафарбований трикутник може бути поруч з числом — у правилах лише «з числом/«?» не зафарбовуються».
- (?) Кліки миші (ліва — зафарбувати, права — крапка) — загальна поведінка pzpr, у ququ.js не визначені.
- (?) WebSearch за «Ququ» нічого не дав — жанр рідкісний; інших джерел, крім pzprjs, не знайшов.
