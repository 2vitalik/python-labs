---
title: Hinge (Chōtsugai, ちょうつがい)
slug: hinge
aka: [Chōtsugai, Chiyotsui, ちょうつがい, ちようつがい, Шарнір]
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
  - {kind: other, url: "https://puzz.link/rules.html?hinge", best: true, note: "puzz.link: правила EN/JA і поле-приклад (сторінка рендериться JS)"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/hinge.js", note: "puzz.link: правила EN/JA, історія (Nikoli vol.159), 9 тестових полів 5×5 з кодами помилок"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/main/src/variety/shimaguni.js", note: "pzprjs: код Hinge у спільному файлі з Shimaguni, Chocona, Sto-Stone — пошук «шарнірної» межі й перевірка дзеркала"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/main/src/res/failcode.en.json", note: "pzprjs: тексти помилок bkHinge*"}
  - {kind: other, url: "https://www.janko.at/Raetsel/Chiyotsui/index.htm", note: "Janko: правила DE/EN, значення назви, 60 пазлів 6×6…12×12"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=hinge+chotsugai+puzzle", note: "пошук; розвʼязання"}
stage: v1
coverage: 55
mechanics: [cell-click, dot-mark, markup-validity, completion-detection, satisfy-constraints, conflict-highlight, undo-redo, in-game-editor, import-open-formats, level-bank, level-solver, unique-puzzle-generation, +cell-shade-toggle, +region-quota, +irregular-regions, +block-components, +mirror-across-border]
proposes: ["+cond:mirror_symmetric", "+cond:borders_crossed", "+card:mirror-across-border", "+card:block-components"]
author: opus
date: 2026-11-09
---

# Hinge — зафарбуй блоки, кожен з яких розтинає рівно одна пряма межа кімнат, і відносно неї блок дзеркальний, як дві стулки на шарнірі

## Суть
Сітка поділена товстими лініями на кімнати, частина кімнат має число — скільки в ній чорних клітинок. Гравець зафарбовує клітинки; кожен блок (4-звʼязна група чорних) мусить перетинати рівно одну пряму суцільну ділянку межі кімнат і бути дзеркально симетричним відносно неї. Назва — «шарнір, дверна петля»: межа кімнат — вісь, дві половини блоку — стулки. Незвичне: **симетрія відносно межі регіонів** — розмітка кімнат стає набором можливих осей дзеркала.

## Поле і час
- Прямокутна сітка (тести puzz.link — 5×5; Janko — 6×6, 8×8, 10×10, 12×12); кімнати — довільні поліоміно.
- Сусідство ортогональне (4) для блоків; діагональний дотик блоків правилами не заборонено (?).
- Вісь симетрії лежить **між** клітинками (по ребрах межі), тож жодна клітинка блоку не стоїть на осі.
- Шари: межі кімнат і числа (незмінні) · стан клітинки: невідомо / чорна / крапка.
- Час статичний; хід = зміна стану однієї клітинки.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Кімната | zone | поліоміно, число N або без числа | рівно N чорних; без числа — будь-яка кількість |
| Число кімнати | static | N ≥ 0 | лічильник чорних у кімнаті |
| Межа кімнат | static | ребро сітки | кандидат у вісь дзеркала |
| Шарнір | zone | пряма суцільна ділянка межі всередині блоку | рівно один на блок; вісь симетрії |
| Блок | zone | 4-звʼязні чорні | перетинає рівно один шарнір, дзеркальний відносно нього → ≥ 2 клітинки, парна кількість |
| Клітинка | mark | unknown / shaded / dot | клік змінює стан |
| Крапка | mark | — | позначка «тут біле» |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left_click, cell)` → ТО `mark(cell, shaded)`; права кнопка → `mark(cell, dot)` (?).
- КОЛИ `constraint_broken(no_shade)` → ЯКЩО `count(shaded, ==, 0)` → ТО `message(brNoShade)`.
- КОЛИ `constraint_broken(hinge)` → ЯКЩО `custom: «блок перетинає межі кімнат на двох і більше різних прямих»` (`+cond:borders_crossed`) → ТО `message(bkHingeGt)` («A block goes through multiple borders»).
- КОЛИ `constraint_broken(hinge)` → ЯКЩО `custom: «ділянка межі під блоком не суцільна»` → ТО `message(bkHingeSplit)` («The region border which separates a block is not continuous»).
- КОЛИ `constraint_broken(hinge)` → ЯКЩО `not custom: «блок дзеркальний відносно шарніра»` (`+cond:mirror_symmetric`) → ТО `message(bkHingeMirror)`.
- Перевірка дзеркала в коді: вісь мусить іти через центр обмежувального прямокутника блоку; кожна чорна клітинка має чорну пару навпроти; кожна пара чорних, що стоять поруч через вісь, розділена ребром межі (вісь не «обривається» всередині блоку).
- КОЛИ `constraint_broken(hinge)` → ЯКЩО `custom: «блок не перетинає жодної межі кімнат»` → ТО `message(bkHingeLt)` («A block does not go through any borders»).
- КОЛИ `constraint_broken(room_count)` → ЯКЩО `not count(shaded in room, ==, N)` → ТО `message(bkShadeNe)`.
- КОЛИ `all_constraints_met` → ТО `win`.
- Дедукція «парність»: блок дзеркальний відносно ребра → кількість його клітинок парна, по половині з кожного боку.
- Дедукція «дві кімнати порівну»: кожна половина блоку звʼязна й не перетинає меж, тож блок займає рівно дві кімнати (Janko) і кладе в кожну однакову кількість клітинок → кімната з числом 1 мусить мати доміно 1+1 через свою межу з сусідньою.
- Дедукція «половина торкається межі»: кожна чорна клітинка належить половині, що прилягає до межі своєї кімнати; одинока чорна клітинка неможлива (`bkHingeLt`).
- Дедукція «одна вісь»: якщо дві чорні блоку вже стоять навпроти через вертикальну межу, жодна інша пара чорних цього блоку не може стояти через горизонтальну.
- Перемога: числа кімнат виконані; кожен блок — рівно один суцільний прямий шарнір і дзеркальна симетрія відносно нього. Поразки й рахунку нема.

## Керування і ввід
- puzz.link play mode: зафарбування / крапка, drag протягує стан (типова схема shading-жанрів) (?).
- Edit mode: межі кімнат — drag по ребрах, числа — клік і клавіатура.
- Undo/redo, Check (перша помилка з кодом), Clear.
- Janko (інтерактивно): сірі клітинки фарбуються в чорне або біле.

## Вікна, меню, HUD
- `game-screen`: сітка з товстими межами кімнат і числами, чорні блоки, крапки + `conflict-highlight` (увесь блок з порушеним шарніром чи симетрією, кімната з неправильною кількістю).
- Кнопки: Check, Undo, Redo, Clear answer.
- `editor-window` — puzz.link edit mode: межі, числа, експорт URL.
- `help-window` — правила (puzz.link, Janko).
- `puzzle-select` — архів Janko за розміром (цифрова версія).
- `end-screen` — повідомлення «розвʼязано».
- Переходи: puzzle-select → game-screen → Check → помилка / end-screen.

## Фічі поза полем
- `auto-check` за кнопкою з кодом порушення; `undo` / `redo`.
- `level-editor` + `share-code` (URL puzz.link).
- `puzzle-bank`: журнал Nikoli, Janko (60 пазлів: 14 — 6×6, 17 — 8×8, 19 — 10×10, 10 — 12×12).

## Варіації й родичі
- Код-родина pzprjs (один файл, двигун «блоки чорних + кімнати»): Shimaguni, Chocona, [Sto-Stone](sto-stone.md), Heyablock, Cocktail, Martini, Nuritwin та ін.
- Janko відносить до родини Akiperago, Chained Blocks, Choco Banana, Chocona, Cocktail-Lampe, Norinori, Norinuri, Tetrochain.
- [Tentai Show](tentai-show.md) — симетрія регіону, але центральна (поворот на 180°) відносно точки.
- [LITS](lits.md), [Double Choco](double-choco.md) (дві половини однакової форми), [Heyawake](heyawake.md) (квота чорних у кімнаті).
- **Осі варіацій**: тип симетрії (дзеркало відносно межі / центральна / копія без дзеркала) · скільки меж перетинає блок (рівно 1 / ≥ 1 / 0) · що рахує число (клітинки / блоки) · вісь (лише межа кімнат / будь-яка лінія сітки).

## Цікавинки для курсу
- Модель кімнат з ребер і блоків як компонент звʼязності (flood fill) — 📎.
- Пошук шарніра: зібрати ребра межі, що розділяють дві чорні клітинки одного блоку, перевірити «одна пряма, суцільна» — 📎.
- Перевірка дзеркала відносно вертикальної/горизонтальної осі через обмежувальний прямокутник — 🌱.
- Підсвітка блоку цілком із кодом причини (Gt / Lt / Split / Mirror) — 🌱.
- Розвʼязувач: перелік кандидатів-шарнірів на кожній межі + квоти кімнат — 🥇.
- Генератор з єдиним розвʼязком — 👑.

## Мапа на каталог
- Є: `cell-click`, `dot-mark` · `markup-validity`, `completion-detection`, `satisfy-constraints`, `conflict-highlight` · `undo-redo` · `in-game-editor`, `import-open-formats`, `level-bank`, `level-solver`, `unique-puzzle-generation`.
- Перевикористано: `+cell-shade-toggle` (Hitori, Heyawake) · `+region-quota` (Heyawake, Star Battle) · `+irregular-regions`.
- **Нема** → пропозиції карток:
  - `+mirror-across-border` «Група клітинок дзеркальна відносно однієї прямої ділянки межі регіонів» · game-logic/constraints · 📎 · слоти {axis: region-border|grid-line, borders: exactly1}.
  - `+block-components` «Розбити розмічені клітинки на 4-звʼязні блоки й перевіряти кожен окремо» · game-logic/constraints · 🌱 — спільний крок Hinge, Chocona, LITS, Statue Park.

## Пропозиції до словників
- `+cond:mirror_symmetric` — група дзеркальна відносно осі (повтор з Epaminondas).
- `+cond:borders_crossed` — скільки різних прямих меж регіонів перетинає група.
- `+card:mirror-across-border`, `+card:block-components` — див. мапу.

## Джерела
- ⭐ [puzz.link: Hinge](https://puzz.link/rules.html?hinge) — сторінка правил і приклад (текст рендериться JS).
- [puzz.link: hinge.js](https://puzz.link/js/pzpr-samples/hinge.js) — правила EN/JA («Each block is cut exactly once by a single straight segment of region borders, across which it must have reflectional symmetry»), «first appeared in Puzzle Communication Nikoli vol. 159», тестові поля.
- [pzprjs: shimaguni.js](https://raw.githubusercontent.com/robx/pzprjs/main/src/variety/shimaguni.js) — `getHingeData`: збір шарнірних ребер, Gt / Split / Mirror / Lt.
- [pzprjs: failcode.en.json](https://raw.githubusercontent.com/robx/pzprjs/main/src/res/failcode.en.json) — тексти `bkHingeGt`, `bkHingeLt`, `bkHingeMirror`, `bkHingeSplit`.
- [Janko: Chiyotsui](https://www.janko.at/Raetsel/Chiyotsui/index.htm) — правила DE/EN («genau zwei Gebiete … symmetrisch bezüglich der gemeinsamen Gebietsgrenze»), назва = «шарніри, стулки дверей», 60 пазлів.

## Непевне
- (?) Рік: Nikoli vol.159 — за датуванням номерів у JA-Вікіпедії (№150 — весна 2015, журнал квартальний) це приблизно літо 2017; прямої дати не бачив.
- (?) Чи дозволено блокам торкатися по діагоналі — правила мовчать; Janko пише «блоки не сусідять ортогонально», що випливає з означення блоку.
- (?) Межовий випадок: блок, що двічі перетинає одну й ту саму пряму межу в різних місцях, — код дає `bkHingeSplit`, правила словами не уточнюють.
- (?) Розкладка мишею в puzz.link — за загальною схемою зафарбовувань; тести вводу у файлі порожні.
