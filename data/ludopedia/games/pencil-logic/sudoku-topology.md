---
title: Sudoku Topology
slug: sudoku-topology
aka: [Судоку-топологія]
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
year: 2024
platforms: [PC, Mac, Linux]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/3051910/Sudoku_Topology/", best: true, note: "опис, список поверхонь і правил, 5 скриншотів (панель Rules, підказки, кнопки вводу)"}
  - {kind: other, url: "https://steamcommunity.com/workshop/browse/?appid=3051910", note: "Workshop: шаблони розробника (torus9x9, cylinder6x8, octahedron4, tetrahedron5 …), фільтри правил і кількості цифр"}
  - {kind: other, url: "https://steamcommunity.com/app/3051910/discussions/", note: "обговорення: corner/centre notes, стрілка з відповіддю розробника, undo, QoL"}
  - {kind: other, url: "https://smartaigames.itch.io/minesweeper-topology", note: "той самий розробник: Minesweeper Topology"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Sudoku+Topology+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [markup-validity, completion-detection, satisfy-constraints, pencil-marks, cell-click, multi-select, undo-redo, redo, game-pause, in-game-editor, level-solver, level-exchange, level-bank, achievements-window, settings-window, +node-graph-field, +surface-topology, +graph-coloring-houses, +step-hints, +line-constraints, +dot-constraints, +killer-cage, +camera-orbit, +cell-coloring, +rules-panel]
proposes: ["+cond:increasing", "+cond:consecutive_set", "+cond:diff", "+cond:ratio", "+role:node", "+ui:rules-panel", "+ui:node-labels", "+feature:step-hints", "+feature:workshop", "+axis:field=surface", "+card:surface-topology", "+card:graph-coloring-houses", "+card:camera-orbit"]
author: opus
date: 2026-11-09
---

# Sudoku Topology — судоку на графі вузлів, натягнутому на сферу, тор, стрічку Мебіуса, пляшку Клейна й багатогранники

## Суть
Smart AI Games (листопад 2024): понад 60 ручних судоку, де клітинки — кульки-вузли у 3D, а «доми» (Boxes) — групи вузлів, розкладені по поверхні: циліндр і тор замикають рядки в кільця, Мебіус і Клейн — з перекрученням, тетраедр/октаедр/додекаедр — вершини як клітинки. Поверх — звичні модулі варіантного судоку: стрілки, термометри, клітки, X/V, білі й чорні крапки, Odd, German Whispers, Renban. Усе розвʼязується логікою без вгадування; кожен пазл має ланцюжок текстових підказок. У грі є 3D-редактор із розвʼязувачем і Steam Workshop.

## Поле і час
- Поле — граф: вузли (клітинки) у 3D, сині лінії-ребра показують форму поверхні. Розміри — від 4 цифр (тетраедр, «Digits 1-4») до 9 (plain9x9, torus9x9); шаблони розробника: plain9x9, circleplain8, hexplain4, cylinder 6×6 / 6×8 / 9×9, torus 6×6 / 9×9, torusskewed8, octahedron4, tetrahedron5, eight7; у відгуках — «тесеракт».
- Колір вузла = належність до дому; рядок «Boxes» у панелі правил перелічує доми ромбиками-кольорами, буває кілька сімейств домів (2–4 рядки «Boxes»).
- Камера 3D: огляд фігури з різних боків; лінії, що перетинаються в проєкції, легко сплутати з тими, що зʼєднують (скарга в обговоренні).
- Час статичний; на екрані — таймер, пауза.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Вузол | mark | цифра 1…N · кутові й центральні олівці · колір · номер у підказках | приймає цифру; належить кільком домам |
| Дім (Box) | zone | множина з N вузлів; колір | кожна цифра 1…N рівно раз |
| Ребро поверхні | static | — | показує форму (кільце, тор, грань) і сусідство |
| Killer-клітка | zone | число суми (напр. 11) | сума цифр = числу, без повторів |
| Термометр | mark | колба + лінія по вузлах | строго зростає від колби |
| Стрілка | mark | кружок + стрілка; довжина у вузлах | кружок = сума вузлів на стрілці; повтори можливі (1+6+1 = 8) |
| X / V | mark | на ребрі між 2 вузлами | сума 10 / 5 |
| Біла / чорна крапка | mark | на ребрі | різниця 1 / відношення 1:2 |
| Odd (Even) | mark | на вузлі | непарна (парна) цифра |
| German Whispers | mark | лінія | сусіди різняться ≥ 5 |
| Renban | mark | лінія | набір послідовних цифр у будь-якому порядку |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(digit d)` → ЯКЩО `not unique(box)` для будь-якого дому вузла → ТО `constraint_broken(box)`.
- КОЛИ `input(digit d)` → ЯКЩО `custom: «d > N пазла»` → ТО `block` (на панелі лише кнопки 1…N).
- Killer: КОЛИ `input(digit)` у клітці → ЯКЩО `not sum(cage, n)` or `not unique(cage)` → ТО `constraint_broken(cage)`.
- Стрілка: КОЛИ `input(digit)` на стрілці → ЯКЩО `not sum(arrow, circle)` → ТО `constraint_broken(arrow)`.
- Термометр: КОЛИ `input(digit)` → ЯКЩО `not custom: «строго більша за попередню від колби»` → ТО `constraint_broken(thermo)`.
- X / V: КОЛИ `input(digit)` → ЯКЩО `not sum(pair, 10)` / `not sum(pair, 5)` → ТО `constraint_broken(xv)`.
- Біла крапка: ЯКЩО `custom: «|a − b| ≠ 1»` → ТО `constraint_broken(white_dot)`; чорна: ЯКЩО `custom: «a ≠ 2b і b ≠ 2a»` → ТО `constraint_broken(black_dot)`.
- Odd: ЯКЩО `custom: «цифра парна»` → ТО `constraint_broken(odd)`.
- German Whispers: ЯКЩО `custom: «сусіди на лінії різняться < 5»` → ТО `constraint_broken(whisper)`.
- Renban: ЯКЩО `custom: «цифри лінії не утворюють відрізок послідовних чисел»` or `not unique(line)` → ТО `constraint_broken(renban)`.
- КОЛИ `input(hint)` → ТО `window(hints-window)` з кроком №k: текст з номерами вузлів + `custom: «підсвітити вузли»`; Prev / Next гортають кроки.
- КОЛИ `all_constraints_met` → ТО `win`, `timer(stop)` (?).
- Перемога: усі вузли заповнені без порушень. Поразки нема; таймер — лише інформація.

## Керування і ввід
- Лише миша або миша + клавіатура; без вимог до швидкості. Клік по вузлу — вибір; інструмент рамки — `multi-select`.
- Екранна панель: цифри 1…N, кутові нотатки («1 2 3»), центральні нотатки («12»), колесо кольорів, undo, redo, стерти; кнопка «Ed» — відкрити пазл у редакторі (?) .
- Камера обертається навколо фігури (?) — точних клавіш джерела не дають; переміщення вибору клавіатурою нема (QoL-тред).
- Конвенція гравців (Snyder): центральні нотатки — «вузол один з xyz», кутові — «x в одному з цих вузлів».

## Вікна, меню, HUD
- `game-screen`: 3D-фігура, `+ui:rules-panel` («Rules»/«Clues»: Digits 1-N, Boxes, Cages, Thermos, X, V, White/Black dots, Arrows, Whispers, Renbans, Odds — з перемикачами показу), `timer-elapsed`, `pause-button`, панель вводу, кнопка «Hints», кнопка «How to play», `+ui:node-labels` (номери вузлів у кольорових кружках у підказках).
- `hints-window`: «Hint #k» з текстом, кнопки Prev / X / Next і «око» (показати вузли).
- `help-window` («How to play»; попапи правил з прикладами — у треді про стрілки).
- `pause-menu`; `level-select` / `puzzle-select` (?) ; `editor-window` (3D-редактор із розвʼязувачем); Workshop-браузер Steam.
- `settings-window`: якість графіки (знижує лаги на 4K), низькоконтрастні режими й вимкнення світіння (Eye Ease Update), колірна доступність.
- `achievements-window` (Steam).

## Фічі поза полем
- `level-editor` + `auto-solve`-перевірка (розвʼязувач у редакторі) + `level-sharing` через Steam Workshop і `user-levels-browser` («top-rated puzzles»).
- `+feature:step-hints` — у кожного пазла послідовність підказок-кроків.
- `undo` / `redo`; `pause`; `colorblind-palette`, `high-contrast` (low-contrast modes), `animation-toggle` (glow), `volume-sliders`.
- `achievements`, `cloud-save`.

## Варіації й родичі
- [sudoku](sudoku.md) — площинний предок; [sudoku-variants](sudoku-variants.md), [sudoku-line-dot-variants](sudoku-line-dot-variants.md) — ті самі модулі на звичайній сітці.
- [minesweeper-dimensions](../hidden-deduction/minesweeper-dimensions.md) — інший сапер у вимірах; Minesweeper Topology від того ж розробника — сапер на торі, тетраедрі, циліндрах.
- «Miracle Sudoku on the torus» (стаття nklein) — тор як зміна того, хто кого «бачить».
- Осі варіацій: **топологія домів** (площина → циліндр: рядки-кільця → тор: кільця в обидва боки → Мебіус/Клейн: склеювання з перекрученням → багатогранник: вершини й грані) · **розмір алфавіту** (4…9) · **модулі поверх** (клітки, лінії, крапки, парність).

## Цікавинки для курсу
- Судоку як розфарбування графа: вузли + доми-кліки; будь-яка поверхня — це лише інша таблиця «вузол → доми» — 🥉 (валідатор не знає про геометрію).
- Генерація домів на торі / Мебіусі / Клейні з сітки N×M склеюванням країв — 🥈.
- 3D-рендер вузлів з камерою-орбітою і вибором кліком (raycast) — 🥈.
- Ланцюжок підказок-кроків, що посилається на номери вузлів — 📎 (дані рівня + вікно).
- Редактор із розвʼязувачем, що не дає опублікувати пазл без єдиного розвʼязку — 🥇.

## Мапа на каталог
- Є: `markup-validity` · `completion-detection` · `satisfy-constraints` · `pencil-marks` (кути + центр) · `cell-click` · `multi-select` · `undo-redo` + `redo` · `game-pause` · `in-game-editor` · `level-solver` · `level-exchange` (Workshop) · `level-bank` · `achievements-window` · `settings-window`.
- **Нема** → пропозиції карток:
  - `+node-graph-field` «Поле — граф вузлів» (повтор із Hitman GO / Kouchoku).
  - `+surface-topology` «Поле на поверхні: циліндр, тор, Мебіус, Клейн, багатогранник» · game-logic/constraints · 🥈 · слот {surface}.
  - `+graph-coloring-houses` «Доми як довільні множини вузлів» · game-logic/constraints · 🥉.
  - `+step-hints` «Ланцюжок підказок-кроків до пазла» · interface/hud · 📎.
  - `+camera-orbit` «Обертання 3D-камери навколо поля» · interface/render · 🥈.
  - `+line-constraints` · `+dot-constraints` · `+killer-cage` · `+cell-coloring` · `+rules-panel` — повтор із sudoku-variants.

## Пропозиції до словників
- `+cond:increasing` (Thermo), `+cond:diff` / `+cond:ratio` (крапки) — повтор із sudoku-line-dot-variants; `+cond:consecutive_set` — набір послідовних чисел (Renban).
- `+role:node` — вузол графа як клітинка (повтор).
- `+ui:rules-panel` (повтор), `+ui:node-labels` — номери вузлів у тексті підказок.
- `+feature:step-hints`, `+feature:workshop` (публікація і рейтинг рівнів через платформу).
- `+axis:field=surface` — поле на замкненій поверхні (тор/Мебіус/Клейн); зараз — `graph`.
- `+card:surface-topology` · `+card:graph-coloring-houses` · `+card:camera-orbit` — див. мапу.

## Джерела
- ⭐ [Steam: Sudoku Topology](https://store.steampowered.com/app/3051910/Sudoku_Topology/) — опис, поверхні, перелік модулів, 60+ пазлів, підказки, редактор із розвʼязувачем; скриншоти з панеллю Rules і вікном підказок.
- [Steam Workshop](https://steamcommunity.com/workshop/browse/?appid=3051910) — назви шаблонів поверхонь, фільтри Cage/Renban/Thermometer/Whispers і 4…9 цифр.
- [Steam-обговорення](https://steamcommunity.com/app/3051910/discussions/) — стрілка 1+6+1 = 8 (відповідь розробника), corner/centre notes, undo, «show seen cells».
- [Minesweeper Topology](https://smartaigames.itch.io/minesweeper-topology) — сапер того ж розробника.
- YouTube: [пошук](https://www.youtube.com/results?search_query=Sudoku+Topology+gameplay).

## Непевне
- (?) Як саме задано доми на кожній поверхні (кільця, грані, кольори) — тексту правил на сторінці нема; висновок зі скриншотів і назв шаблонів.
- (?) Even-клітинки: в описі «odd and even clues», на скриншотах бачив лише Odds.
- (?) X і V — стандартне значення XV (сума 10 / 5); формулювання гри не бачив.
- (?) Керування камерою (мишею / клавішами), екран вибору пазлів і зупинка таймера при перемозі.
- (?) Кнопка «Ed» на скриншотах — найімовірніше перехід у редактор.
