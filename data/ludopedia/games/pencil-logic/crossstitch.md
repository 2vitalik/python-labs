---
title: Crossstitch
slug: crossstitch
aka: [Cross Stitch, Вишивка хрестиком]
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
platforms: [paper, web]
links:
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/crossstitch.js", best: true, note: "puzz.link: правила EN/JA (6 пунктів), автор Arvi Teikari (Hempuli), тестові поля з кодами помилок, тести вводу"}
  - {kind: play, url: "https://puzz.link/rules.html?crossstitch", note: "puzz.link: сторінка правил і плеєр (рендериться JS)"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/main/src/variety/crossstitch.js", note: "pzprjs: ввід, дві графи ліній за парністю, порядок перевірок"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/main/src/res/failcode.en.json", note: "pzprjs: тексти помилок (cxAdjacent, lnPlLoop.crossstitch, nmCircleNe…)"}
  - {kind: other, url: "https://api.github.com/repos/robx/pzprjs/commits?path=src/variety/crossstitch.js", note: "історія файла: жанр додано в pzprjs 2021-01-30"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=crossstitch+puzzle+hempuli", note: "пошук; відео не шукав"}
stage: v1
coverage: 60
mechanics: [markup-validity, completion-detection, satisfy-constraints, cell-click, dot-mark, conflict-highlight, in-game-editor, import-open-formats, undo-redo, +loop-detection, +crossing-detection, +arrow-count-clue, +two-loops, +parity-sublattice, +corner-touch-clue, +clue-done-mark]
proposes: ["+cond:lines_at(vertex, n)", "+cond:count_in", "+cond:corners_touched(cell, n)", "+cond:loop_count(n)", "+ui:loop-color-coding", "+card:two-loops", "+card:parity-sublattice", "+card:corner-touch-clue"]
author: opus
date: 2026-11-09
---

# Crossstitch — дві петлі з діагоналей клітинок, які можуть перетинати одна одну хрестиком

## Суть
Гравець малює в клітинках діагоналі так, щоб вийшли рівно дві замкнені петлі. Петля не розгалужується й не перетинає себе, але дві петлі можуть перетнутись — тоді в клітинці стоїть «X» з обох діагоналей. Підказки: число в колі — скільки кутів клітинки торкається петля; число зі стрілкою — скільки X у тому напрямку; клітинки-перетини не сусідять по стороні. Жанр вигадав Arvi Teikari (Hempuli).

## Поле і час
- Прямокутна сітка; лінії йдуть діагоналями клітинок від вершини до вершини.
- Стан клітинки: порожня, «\», «/» або X (обидві діагоналі).
- Клітинки-підказки затінені: лінії через них не йдуть, і на них обривається лічба стрілок.
- Шари: підказки · діагоналі гравця · позначки (крапки у вершинах, кола в клітинках, хрестики на діагоналях, «готово» на підказках).
- Час статичний; пазли авторські (редактор puzz.link).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітинка | terrain | порожня / «\» / «/» / X | X = перетин двох петель |
| Вершина сітки | mark | клас парності (шахове розфарбування вершин) | має 0 або 2 лінії; 3 — розгалуження, 4 — самоперетин |
| Петля | zone | замкнена ламана з діагоналей | рівно дві на полі |
| Перетин X | mark | — | не сусідить по стороні з іншим X |
| Затінена клітинка | static | — | без ліній; кінець лічби стрілки |
| Число в колі | static | 0–4 | скільки з 4 кутів клітинки торкається петля |
| Число зі стрілкою | static | n, напрямок | скільки X у напрямку до наступної затіненої клітинки чи краю |
| «?» | static | у колі або зі стрілкою | будь-яке число, крім 0 |
| Позначки гравця | mark | крапка, коло, хрестик, «готово» | на перевірку не впливають |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag_diagonal, cell)` → ЯКЩО `free(cell)` → ТО `mark(cell, «\» або «/»)`; ЯКЩО `occupied(cell, other_diagonal)` → ТО `mark(cell, X)`; drag по наявній лінії → `unmark(cell)` (pzprjs `inputslash`).
- КОЛИ `input(click, cell)` → ТО `custom: «цикл \ → / → X → порожньо або перемикач — за налаштуванням use»`.
- КОЛИ `input(right_drag, cell)` → ТО `mark(cell, «хрестик на діагоналі»)` («Drag pekes»).
- КОЛИ `input(click, vertex)` → ТО `mark(vertex, dot)`; `input(click, clue)` → `set_state(clue, done)`; `input(click, empty_cell)` → `mark(cell, circle)`.
- Затінення: ЯКЩО `occupied(shaded_cell, line)` → ТО `constraint_broken(custom: «лінія на затіненій клітинці»)`.
- Розгалуження: ЯКЩО `custom: «у вершині 3 лінії»` (`+cond:lines_at`) → `constraint_broken(custom: «гілка»)`.
- Самоперетин: ЯКЩО `custom: «у вершині 4 лінії»` → `constraint_broken(custom: «петля перетинає себе»)`.
- Перетини: ЯКЩО `no_adjacent(X)` → ок; інакше `constraint_broken(custom: «перетини сусідять»)`.
- Коло: ЯКЩО `custom: «к-сть кутів клітинки з лінією = n»` (`+cond:corners_touched`) → підказка задоволена; «?» у колі — щонайменше 1.
- Стрілка: ЯКЩО `custom: «к-сть X у напрямку до затіненої клітинки чи краю = n»` (`+cond:count_in`) → задоволена; «?» зі стрілкою — щонайменше 1.
- Кінці: ЯКЩО `custom: «лінія обривається у вершині»` → `constraint_broken(custom: «глухий кінець»)`.
- Петлі: ЯКЩО `custom: «компонент ліній рівно 2»` (`+cond:loop_count`) → ок; інакше «There aren't exactly two loops».
- Редактор: ЯКЩО `custom: «число > 4 без стрілки»` → `constraint_broken(custom: «A number has no arrow»)`.
- КОЛИ `all_constraints_met` → ТО `win`.
- Дедукція «парність»: діагональ завжди зʼєднує вершини одного кольору шахового розфарбування вершин; «\» і «/» однієї клітинки — різних кольорів. Тож X — завжди перетин двох різних петель, а за наявності X петлі лежать по одній у кожному класі (pzprjs веде дві окремі графи ліній).
- Дедукція «самоперетин лише у вершині»: у клітинці петля сама себе перетнути не може — заборона стосується вершин з 4 лініями.
- Дедукція «коло 0 / коло 4»: при 0 усі діагоналі сусідніх клітинок, що ведуть у кути, заборонені; при 4 кожен кут має дві лінії.
- Дедукція «стрілка 0»: у напрямку жодного X — кожна клітинка має щонайбільше одну діагональ.
- Дедукція «сусід X»: біля X по стороні клітинки мають не більше однієї діагоналі.
- Перемога: рівно дві петлі, без гілок і самоперетинів, перетини не сусідять, усі числа збіглися. Поразки й рахунку нема.

## Керування і ввід
- puzz.link play: drag по діагоналі клітинки — лінія; другий drag іншою діагоналлю — X; повторний drag по лінії — стерти.
- Клік по клітинці — перемикання/цикл діагоналей (налаштування `use`); права кнопка з drag — хрестик «тут лінії нема».
- Клік біля вершини — крапка; клік по порожній клітинці — коло; клік по підказці — «готово».
- Режими вводу: line, completion, peke, dot, subcircle, info-line (код `inputModes`).
- puzz.link edit: клік — число (цикл включає «?» і затінення); drag із клітинки — стрілка; спливна панель цифр (KeyPopup).

## Вікна, меню, HUD
- `game-screen`: світла сітка, затінені клітинки з числами в колі або зі стрілкою, діагоналі, X, позначки; петлі можна розфарбувати різними кольорами (`irowake`, `+ui:loop-color-coding`); `conflict-highlight` — лінії/клітинки з помилкою.
- `editor-window` (edit): числа, затінення, стрілки, розмір.
- `settings-window`: спосіб вводу ліній (`use`).
- `help-window` — правила EN/JA.
- Решта — оболонка [puzz.link](puzz-link.md): Check, Undo/Redo, Trial, URL, таймер.

## Фічі поза полем
- `auto-check` за кнопкою з текстом першої помилки (порядок: затінення, стрілка, гілка, самоперетин, сусідні X, кола, стрілки, кінці, «дві петлі»).
- `undo` / `redo`; trial-режим оболонки.
- `level-editor` + `share-code` (URL puzz.link); `export-import` (файл pzprv3).
- Поворот і віддзеркалення поля в редакторі міняють «\» ↔ «/» і повертають стрілки (`adjustBoardData`).

## Варіації й родичі
- У сімʼї: [Slant](slant.md) (діагональ у кожній клітинці, числа у вершинах), [Masyu](masyu.md) і [Slitherlink](slitherlink.md) (одна петля), [Tracks](tracks.md), [Meander](meander.md) (шлях з діагоналей), [Yajilin](yajilin.md) (стрілки-лічильники), [puzz.link](puzz-link.md) (оболонка).
- Автор — Hempuli, той самий, що зробив [Baba Is You](../thinky/baba-is-you.md) (?).
- **Осі варіацій**: кількість петель (1 / 2 / k за кольорами) · що рахують підказки (кути, перетини, лінії) · чи дозволено перетин (між петлями / ніде) · заборона сусідніх X.

## Цікавинки для курсу
- Модель «вершини двох класів парності + діагоналі як ребра двох окремих графів» — 📎.
- Перевірка: степені вершин (0/2), компоненти зʼєднаності, рівно дві петлі — 📎.
- Лічба X уздовж стрілки до затіненої клітинки — 🌱.
- Ввід діагоналі drag-ом з напрямком жесту і X другим жестом — 📎.
- Розфарбування петель різними кольорами за компонентами — 🌱.
- Розвʼязувач з SAT/backtracking за станами клітинок і умовою «дві петлі» — 🥇.

## Мапа на каталог
- Є: `markup-validity`, `completion-detection`, `satisfy-constraints` · `cell-click`, `dot-mark` ↔ крапки й кола, `conflict-highlight` · `in-game-editor`, `import-open-formats`, `undo-redo`.
- Перевикористано: `+loop-detection`, `+crossing-detection`, `+arrow-count-clue` (Yajilin та ін.), `+clue-done-mark` ↔ «готово» на підказці.
- **Нема** → пропозиції карток:
  - `+two-loops` «Рівно k петель на полі, а не одна» · game-logic/constraints · 📎 · слот {k}.
  - `+parity-sublattice` «Вершини двох класів шахової парності; діагоналі — ребра двох окремих графів» · game-logic/constraints · 📎.
  - `+corner-touch-clue` «Число в клітинці = скільки її кутів торкається лінія» · game-logic/constraints · 🌱.

## Пропозиції до словників
- `+cond:lines_at(vertex, n)` — повтор (Slant): у вершині n ліній.
- `+cond:count_in` — повтор (Compass, Doppelblock): лічба в напрямку.
- `+cond:corners_touched(cell, n)` — n кутів клітинки належать лінії.
- `+cond:loop_count(n)` — на полі рівно n петель.
- `+ui:loop-color-coding` — розфарбування ліній за компонентами.
- `+card:two-loops`, `+card:parity-sublattice`, `+card:corner-touch-clue` — див. мапу.

## Джерела
- ⭐ [puzz.link: crossstitch.js](https://puzz.link/js/pzpr-samples/crossstitch.js) — 6 правил EN/JA, «invented by Arvi Teikari a.k.a. Hempuli», тестові поля для кожного коду помилки, назви тестів вводу.
- [puzz.link: rules.html?crossstitch](https://puzz.link/rules.html?crossstitch) — сторінка правил (без JS — порожня).
- [pzprjs: crossstitch.js](https://raw.githubusercontent.com/robx/pzprjs/main/src/variety/crossstitch.js) — режими вводу, `parity()`, `LineGraph`/`Line2Graph`, `checkTwoLoops`, `checkCircledNumber`, `countCrossing`.
- [pzprjs: failcode.en.json](https://raw.githubusercontent.com/robx/pzprjs/main/src/res/failcode.en.json) — тексти помилок.
- [GitHub API: історія файла](https://api.github.com/repos/robx/pzprjs/commits?path=src/variety/crossstitch.js) — «Add Crossstitch», 2021-01-30.
- YouTube: пошук «crossstitch puzzle hempuli».

## Непевне
- (?) Рік винаходу — невідомо; у pzprjs жанр зʼявився 2021-01-30 (`year: null`).
- (?) Що Hempuli — автор Baba Is You, знаю не з відкритих тут джерел.
- (?) Код рахує лише сумарно 2 компоненти в обох класах; без жодного X обидві петлі теоретично можуть лежати в одному класі.
- (?) Режим `info-line` і точна розкладка кнопок миші — лише з коду й назв тестів.
- (?) Де ще публікувались пазли (блог Hempuli, збірки) — не перевіряв.
