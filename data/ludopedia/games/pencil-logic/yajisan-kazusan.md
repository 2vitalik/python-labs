---
title: Yajisan-Kazusan (やじさんかずさん)
slug: yajisan-kazusan
aka: [Yajikazu, やじさんかずさん, Prev Arrow Cation, Яджісан-Казусан]
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
year: 1998
platforms: [paper, web]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Yajisan-Kazusan", best: true, note: "правила, хибні підказки мусять бути зафарбовані, порада про «неможливі значення»"}
  - {kind: official, url: "https://www.nikoli.co.jp/ja/puzzles/yajisan_kazusan/", note: "Nikoli JA: 3 правила, картинки 例題 → 途中経過 → 答え"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/yajikazu.js", note: "puzz.link: правила EN/JA, історія (Nikoli vol.74), коди помилок"}
  - {kind: other, url: "https://puzz.link/rules.html?yajikazu", note: "puzz.link: сторінка правил (рендериться JS)"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/main/src/variety/yajikazu.js", note: "pzprjs: код — перевірка стрілок до краю, спільний файл з Out of Sight"}
  - {kind: other, url: "https://www.janko.at/Raetsel/Yajisan-Kazusan/index.htm", note: "Janko: правила DE/EN, №74 червень 1998, 10 варіантів, 230 пазлів"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=yajisan+kazusan+puzzle", note: "пошук; розвʼязання"}
stage: v1
coverage: 70
mechanics: [cell-click, dot-mark, line-sum-clue, connectivity-check, markup-validity, completion-detection, satisfy-constraints, conflict-highlight, undo-redo, in-game-editor, import-open-formats, level-bank, level-solver, unique-puzzle-generation, +cell-shade-toggle, +no-adjacent-check, +arrow-count-clue, +clue-void-when-covered, +liar-clue]
proposes: ["+cond:count_dir", "+cond:clue_covered", "+card:clue-void-when-covered", "+card:arrow-count-clue"]
author: opus
date: 2026-11-09
---

# Yajisan-Kazusan — стрілки рахують чорні клітинки, але будь-яку стрілку можна «вимкнути», зафарбувавши її саму

## Суть
На сітці стоять підказки «число + стрілка»: число — скільки чорних клітинок у напрямку стрілки до краю поля. Гравець зафарбовує клітинки: чорні не торкаються сторонами, білі звʼязні. Головне: **клітинку з підказкою теж можна зафарбувати — тоді її число не діє** (може бути і правдою, і брехнею). Отже кожна хибна підказка мусить стояти на чорній клітинці; частина роботи — знайти, які підказки брешуть.

## Поле і час
- Прямокутна сітка, як у Yajilin; сусідство ортогональне (4) для заборони дотику й звʼязності.
- Промінь стрілки — усі клітинки в одному з 4 напрямків до краю поля, зокрема крізь інші підказки (і вони рахуються, якщо чорні).
- Шари: підказки (незмінні) · стан клітинки: невідомо / чорна / крапка; зафарбована підказка лишається видимою (сірий шрифт).
- Час статичний; хід = зміна стану однієї клітинки.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Підказка | static | число n, стрілка ↑↓←→ | біла → у промені рівно n чорних |
| Зафарбована підказка | mark | — | число не діє; клітинка рахується як чорна для інших променів |
| Хибна підказка | static | — | мусить бути зафарбована (Wikipedia) |
| Клітинка | mark | unknown / shaded / dot | клік змінює стан |
| Чорна клітинка | mark | — | не торкається іншої чорної сторонами |
| Крапка | mark | — | позначка «тут біле» |
| Промінь стрілки | zone | клітинки до краю | множина, яку рахує число |
| Біла область | zone | компоненти | усі білі — одна 4-звʼязна компонента |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left_click, cell)` → ТО `mark(cell, shaded)`; права кнопка → `mark(cell, dot)` (?).
- Edit: КОЛИ `input(drag, clue)` → ТО `custom: «напрямок drag задає стрілку»`; КОЛИ `input(click, clue)` → ТО `set_value(clue, n)`.
- КОЛИ `constraint_broken(no_shade)` → ЯКЩО `count(shaded, ==, 0)` → ТО `message(brNoShade)`.
- КОЛИ `constraint_broken(adjacent)` → ЯКЩО `not no_adjacent(shaded)` → ТО `message(csAdjacent)`.
- КОЛИ `constraint_broken(connect)` → ЯКЩО `not connected(unshaded)` → ТО `message(cuDivideRB)`.
- КОЛИ `constraint_broken(clue)` → ЯКЩО `not state(clue, shaded)` and `custom: «чорних у промені стрілки до краю ≠ n»` (`+cond:count_dir`) → ТО `message(anShadeNe)`.
- КОЛИ `state_on(clue, shaded)` → ТО `custom: «число підказки не діє»` (`+cond:clue_covered`).
- КОЛИ `all_constraints_met` → ТО `win`.
- Наслідок: КОЛИ `custom: «підказка хибна»` → ТО `paint(clue, shaded)` — інакше розвʼязку нема.
- Дедукція «неможливе значення» (Wikipedia): чорні не торкаються, тож у промені з k клітинок вміщається не більше ⌈k/2⌉ чорних — більше число одразу хибне → його клітинка чорна → її 4 сусіди білі.
- Дедукція «суперечність»: дві підказки, що рахують перетинні промені, не можуть бути правдивими одночасно → одна з них чорна; часто звʼязність білих вирішує, яка.
- Дедукція «нуль»: біла «0» робить білим увесь промінь — але «0» може бути й зафарбована, тож спершу треба виключити чорну.
- Перемога: чорні не торкаються, білі звʼязні, кожна біла підказка правдива. Поразки й рахунку нема.

## Керування і ввід
- puzz.link play mode: режими `shade`, `unshade`, `peke`, `info-blk`; drag протягує стан.
- Edit mode: drag із клітинки — стрілка в тому напрямку, клік без руху — число; клавіатура: Shift + стрілки — напрямок (?).
- Undo/redo, Check (перша помилка з кодом), Clear.
- Janko (інтерактивно): клітинки фарбуються в чорне або біле.

## Вікна, меню, HUD
- `game-screen`: сітка, підказки зі стрілками (на чорних — сірим), чорні клітинки, крапки + `conflict-highlight` (підказка й увесь її промінь, сусідні чорні, розрізані білі).
- Кнопки: Check, Undo, Redo, Clear answer.
- `editor-window` — puzz.link edit mode: стрілки, числа, експорт URL.
- `help-window` — правила (Nikoli, puzz.link).
- `puzzle-select` — архів Janko (230 пазлів), книги Nikoli (цифрова версія).
- `end-screen` — повідомлення «розвʼязано».
- Переходи: puzzle-select → game-screen → Check → помилка / end-screen.

## Фічі поза полем
- `auto-check` за кнопкою з кодом порушення; `undo` / `redo`.
- `level-editor` + `share-code` (URL puzz.link).
- `puzzle-bank`: журнал Nikoli з 1998, Janko (230 пазлів і варіанти).

## Варіації й родичі
- Варіанти Janko: **Multi** (кілька стрілок на підказці, сума) · **Diagonal** (діагональні стрілки) · **Cipher** (літери замість чисел) · **Inverted** (на чорних числа мусять бути хибними) · **Liar** (рівно одна хибна на рядок і стовпець) · **Liar Arrows** (рівно одна стрілка на рядок і стовпець вказує не туди) · **No 2x2** (нема білих 2×2) · **Off by One** (кожне біле число відхиляється на 1) · **Windows** (парні «вікна» протилежних кольорів) · **Odd** (непарна кількість чорних у кожному рядку й стовпці).
- Out of Sight — жанр у тому самому файлі коду pzprjs: стрілка не мусить «бачити» число того ж кольору (?, правил не відкрив).
- [Yajisan-Sokoban](yajisan-sokoban.md) — запозичила правило «накрита підказка не діє», але накриває ящик.
- [Yajilin](yajilin.md) — ті самі стрілки, але підказки не зафарбовуються, плюс петля.
- [Usowan](usowan.md) — брехня за квотою «одна на кімнату».
- Родичі за двигуном: [Hitori](hitori.md), [Heyawake](heyawake.md), [Kuromasu](kuromasu.md).
- **Осі варіацій**: хто «вимикає» підказку (зафарбування / ящик / нічого) · квота брехунів (вільна / 1 на рядок і стовпець) · напрям стрілок (4 / діагоналі / кілька) · що рахує (чорні / білі / сума).

## Цікавинки для курсу
- Промінь стрілки до краю й підрахунок чорних — 🌱.
- Правило «зафарбована підказка не діє» як умова у валідаторі — 🌱.
- Звʼязність білих + заборона дотику чорних — 📎 (спільний двигун Hitori-родини).
- Підсвітка порушеної підказки разом з усім її променем — 🌱.
- Розвʼязувач: для кожної підказки дві гілки «чорна / правдива» + CSP — 🥇.
- Конструктор варіантів Janko (Multi, Diagonal, Liar, Off by One…) перемикачами — 🥉.

## Мапа на каталог
- Є: `cell-click`, `dot-mark` · `line-sum-clue` ↔ кількість чорних у промені · `connectivity-check` ↔ білі звʼязні · `markup-validity`, `completion-detection`, `satisfy-constraints`, `conflict-highlight` · `undo-redo` · `in-game-editor`, `import-open-formats`, `level-bank`, `level-solver`, `unique-puzzle-generation`.
- Перевикористано: `+cell-shade-toggle`, `+no-adjacent-check` (Hitori, Heyawake) · `+arrow-count-clue` (Yajilin, Yajisan-Sokoban) · `+clue-void-when-covered` (Yajisan-Sokoban; тут «накриття» = зафарбування) · `+liar-clue` (Usowan, 14 Minesweeper Variants).
- **Нема** → пропозиції карток:
  - `+clue-void-when-covered` «Накрита / зафарбована підказка не діє» · game-logic/constraints · 🌱 · слот {cover: shade|object}.
  - `+arrow-count-clue` «Число зі стрілкою рахує клітинки виду в промені до краю» · game-logic/constraints · 🌱 · слоти {dirs: 4|8|multi, kind: shaded|object}.

## Пропозиції до словників
- `+cond:count_dir` — кількість сутностей у напрямку від клітинки (повтор з Yajilin, Yajisan-Sokoban).
- `+cond:clue_covered` — підказку накрито / зафарбовано (повтор з Yajisan-Sokoban).
- `+card:clue-void-when-covered`, `+card:arrow-count-clue` — див. мапу.

## Джерела
- ⭐ [Wikipedia: Yajisan-Kazusan](https://en.wikipedia.org/wiki/Yajisan-Kazusan) — правила, «a shaded cell's clue need not be false», порада про неможливі значення.
- [Nikoli JA: やじさんかずさん](https://www.nikoli.co.jp/ja/puzzles/yajisan_kazusan/) — 3 офіційні правила, зокрема «数字の入ったマスが黒マスになることもあります。その場合、そのマスの数字の情報は無効».
- [puzz.link: yajikazu.js](https://puzz.link/js/pzpr-samples/yajikazu.js) — правила EN/JA, «first appeared in Puzzle Communication Nikoli vol. 74», коди `brNoShade`, `csAdjacent`, `cuDivideRB`, `anShadeNe`.
- [pzprjs: yajikazu.js](https://raw.githubusercontent.com/robx/pzprjs/main/src/variety/yajikazu.js) — `checkArrowNumber` (промінь до краю, пропуск зафарбованих підказок), ввід стрілки drag-ом.
- [Janko: Yajisan-Kazusan](https://www.janko.at/Raetsel/Yajisan-Kazusan/index.htm) — правила DE/EN, перша публікація «Puzzle Communication Nikoli Nr. 74, Juni 1998», 10 варіантів, назва Grant Fikes «Prev Arrow Cation».

## Непевне
- (?) Назва: «yaji» від やじるし (стрілка), «kazu» — число; ймовірно гра слів з парою героїв «Яджі-сан і Кіта-сан» (Tōkaidōchū Hizakurige); Janko перекладає інакше — не перевірено.
- (?) Підказка без стрілки в pzprjs не перевіряється взагалі (`qdir === 0` пропускається) — у паперових пазлах таких, схоже, нема.
- (?) Правила Out of Sight — лише текст помилки «An arrow points to a symbol with the same color».
- (?) Розкладка мишею й клавіатурою в puzz.link — за кодом, у живому інтерфейсі не перевірена.
