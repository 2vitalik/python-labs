---
title: Nurimisaki (ぬりみさき)
slug: nurimisaki
aka: [ぬりみさき, Нурімісакі, Promontory]
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
year: 2018
platforms: [paper, web]
links:
  - {kind: official, url: "https://www.nikoli.co.jp/en/puzzles/nurimisaki/", best: true, note: "Nikoli: правила EN, картинки Sample / Progressing / Solution"}
  - {kind: other, url: "https://www.janko.at/Raetsel/Nurimisaki/index.htm", note: "Janko: правила DE/EN, Nikoli № 163 (червень 2018), автор umaya tengoku, 100 пазлів"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/nurimisaki.js", note: "puzz.link/pzpr: правила EN/JP, коди помилок, тести вводу"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/master/src/res/failcode.en.json", note: "тексти помилок pzpr"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=nurimisaki+puzzle", note: "пошук; розвʼязання"}
stage: v1
coverage: 70
mechanics: [markup-validity, completion-detection, satisfy-constraints, connectivity-check, cell-click, conflict-highlight, level-bank, in-game-editor, import-open-formats, +cell-shade-toggle, +no-2x2-check, +dot-mark, +input-scheme-toggle, +undo-redo, +visibility-count-clue, +dead-end-clue]
proposes: ["+trigger:pattern(block2x2)", "+cond:view_count", "+cond:dead_end", "+card:dead-end-clue"]
author: opus
date: 2026-11-09
---

# Nurimisaki — зафарбуй клітинки так, щоб білі утворили одну мережу стежок, а кружечки були рівно її тупиками-«мисами»

## Суть
Гравець зафарбовує частину клітинок сітки. Білі клітинки мають бути однією звʼязною мережею без квадратів 2×2 (і чорні теж без 2×2) — тож біле поле стає «стежками» шириною в одну клітинку. Кружечок — це «мис» (тупик): біла клітинка рівно з одним білим сусідом; і навпаки, кожен тупик білої мережі мусить бути кружечком. Число в кружечку — скільки білих клітинок видно з мису по прямій у бік його єдиного сусіда.

## Поле і час
- Прямокутна сітка; підказки — кружечки (порожні або з числом) у частині клітинок.
- Стан клітинки: невідома · чорна · біла (допоміжна крапка гравця).
- Шари: кружечки й числа (незмінні) · зафарбування · допоміжні крапки.
- Час статичний; хід = зафарбувати / позначити / стерти клітинку.
- Janko: заборона 2×2 для обох кольорів робить білі клітинки «шляхом завширшки одна клітинка».

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітинка | mark | невідома / чорна / біла | гравець перемикає стан |
| Кружечок (мис) | static | — | завжди білий; рівно один білий сусід по стороні |
| Кружечок з числом | static | N | з мису по прямій у бік білого сусіда видно N білих клітинок (до чорної чи краю) |
| Біла мережа | zone | — | одна компонента за 4-звʼязністю; без 2×2 |
| Чорна область | zone | — | без 2×2; звʼязність не вимагається |
| Тупик без кружечка | mark | — | заборонений: «білу клітинку без кружечка не можна робити мисом» |
| Допоміжна крапка | mark | — | «тут біле», не перевіряється (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left_click, cell)` → ТО `mark(cell, black)`; повтор — зняти; правий клік — `mark(cell, dot)` (puzz.link, схема `use`) (?).
- КОЛИ `pattern(block2x2)` → ЯКЩО `same(cells, black)` → ТО `set_state(block, error)` (pzpr `cs2x2`: «There is a 2x2 block of shaded cells»).
- КОЛИ `pattern(block2x2)` → ЯКЩО `same(cells, white)` → ТО `set_state(block, error)` (`cu2x2`).
- КОЛИ `constraint_broken(white_connected)` → ЯКЩО `not connected(white)` → ТО `set_state(board, error)` (`cuDivide`: «The unshaded cells are divided»).
- КОЛИ `constraint_broken(promontory)` → ЯКЩО `occupied(cell, circle)` and `not adjacent_count(cell, white, ==, 1)` → ТО `set_state(cell, error)` («A circle is not adjacent to exactly one unshaded cell»).
- КОЛИ `constraint_broken(false_promontory)` → ЯКЩО `not occupied(cell, circle)` and `adjacent_count(cell, white, ==, 1)` → ТО `set_state(cell, error)` (`nonCirclePromontory`: «A dead end has no circle») (`+cond:dead_end`).
- КОЛИ `constraint_broken(view)` → ЯКЩО `custom: «кількість білих клітинок по прямій від мису ≠ N»` (`+cond:view_count`) → ТО `set_state(cell, error)` (`nmSumViewNe`).
- КОЛИ `constraint_broken(empty_board)` → ЯКЩО `count(black, ==, 0)` → ТО помилка (`brNoShade`).
- Кружечок завжди білий: ЯКЩО `occupied(cell, circle)` → ТО `block` на `mark(cell, black)` (?).
- КОЛИ `all_constraints_met` → ТО `win`.
- Дедукція «мис»: у кружечка три з чотирьох сусідів чорні — щойно один сусід став білим, решта стає чорною.
- Дедукція «довжина»: кружечок N біля краю чи чорної клітинки — напрямок білого сусіда визначається тим, де вміщається N клітинок поспіль.
- Дедукція «кінець погляду»: клітинка за N-ою білою по прямій — чорна (або край).
- Дедукція «без 2×2»: три білі клітинки квадрата → четверта чорна; так само для чорних.
- Дедукція «гілки»: тупики білої мережі бувають тільки в кружечках, тож кожна гілка закінчується мисом.
- Перемога: усі обмеження виконані. Поразки й рахунку нема.

## Керування і ввід
- Папір: зафарбувати клітинку, крапкою позначити «білу».
- puzz.link play: клік по клітинці — чорна / біла крапка; налаштування `use` (1 / 2) міняє схему кнопок миші (тести pzpr).
- puzz.link edit: клік — поставити кружечок, цифри — число.
- Цифрова версія: undo/redo, перевірка за кнопкою з текстом першої помилки.

## Вікна, меню, HUD
- `game-screen`: сітка, кружечки з числами, зафарбування, крапки, `conflict-highlight` на клітинці чи квадраті з помилкою.
- puzz.link: перемикач play/edit, кнопка перевірки, `settings-window` (схема вводу).
- `help-window` — правила (Nikoli з картинками; Janko; pzpr).
- `puzzle-select` — 100 пазлів Janko.
- Переходи: edit → play; check → повідомлення помилки.

## Фічі поза полем
- `auto-check` за кнопкою з кодами pzpr.
- `undo` / `redo`; `level-editor` + `share-code` (URL puzz.link).
- `puzzle-bank` Janko; генератора не бачив (?).

## Варіації й родичі
- Сімʼя «нурі»: [Nurikabe](nurikabe.md) (чорна стіна звʼязна, білі острови), [Nuri-maze](nuri-maze.md), [Kuromasu](kuromasu.md) (число = скільки білих видно в чотири боки), [Heyawake](heyawake.md).
- pzpr має варіант **Heyajiri-misaki** (кімнати + миси) — за кодом `circleNotPromontory.heyajirimisaki` (?).
- Janko називає родичів Nuribou і Nurimaze.
- **Осі варіацій**: що означає кружечок (тупик / розгалуження) · рахунок погляду (в один бік / в чотири, як Kuromasu) · заборона 2×2 (обидва кольори / лише один) · чи потрібна звʼязність білих.

## Цікавинки для курсу
- Перевірка 2×2 для обох кольорів і звʼязності (BFS) — 🌱.
- Ступінь вершини в білій мережі: «тупик ⇔ кружечок» — 📎; одна функція `white_neighbors(cell)` для двох правил.
- Підрахунок погляду з мису в напрямку єдиного сусіда — 🌱.
- Повний валідатор з кодами pzpr — 🥉; розвʼязувач (пропагація 2×2 + мис + BFS-звʼязність з відкатом) — 🥇.

## Мапа на каталог
- Є: `markup-validity`, `completion-detection`, `satisfy-constraints`, `connectivity-check` ↔ біла мережа · `cell-click`, `conflict-highlight` · `level-bank` (Janko) · `in-game-editor`, `import-open-formats` (puzz.link).
- Перевикористано: `+cell-shade-toggle`, `+no-2x2-check` (Nurikabe), `+dot-mark`, `+input-scheme-toggle`, `+undo-redo`, `+visibility-count-clue` (Kuromasu; слот direction: one).
- **Нема** → пропозиції карток:
  - `+dead-end-clue` «Підказка = тупик мережі» · game-logic/constraints · 📎 · слот {where: circles-only|exact} — Nurimisaki, Kurodoko-варіанти pzpr.

## Пропозиції до словників
- `+trigger:pattern(block2x2)` — повтор з Nurikabe.
- `+cond:view_count` — повтор з Kuromasu: скільки клітинок видно по прямій.
- `+cond:dead_end` — клітинка мережі має рівно одного сусіда своєї мережі.
- `+card:dead-end-clue` — див. мапу.

## Джерела
- ⭐ [Nikoli: Nurimisaki](https://www.nikoli.co.jp/en/puzzles/nurimisaki/) — 5 правил: кружечок = мис, «only one of the cells next to it remaining white», число = довжина білої прямої, звʼязність, без 2×2 обох кольорів.
- [Janko: Nurimisaki](https://www.janko.at/Raetsel/Nurimisaki/index.htm) — Nikoli № 163, червень 2018, umaya tengoku; «шлях завширшки одна клітинка»; 100 пазлів.
- [puzz.link nurimisaki.js](https://puzz.link/js/pzpr-samples/nurimisaki.js) — правила, коди `brNoShade`, `cs2x2`, `cu2x2`, `cuDivide`, `nmSumViewNe`, `circleNotPromontory`, `nonCirclePromontory`.
- [pzprjs failcode.en.json](https://raw.githubusercontent.com/robx/pzprjs/master/src/res/failcode.en.json) — тексти помилок.

## Непевне
- (?) Чи рахується сам кружечок у числі: pzpr — «including the clue cell», Nikoli — «white cells form a straight line from the Misaki cell»; формулювання розходяться.
- (?) Тексти `circleNotPromontory` / `nonCirclePromontory` у failcode.en.json є лише з суфіксами `.heyajirimisaki` / `.kurodoko` — що бачить гравець саме в Nurimisaki, не перевірено.
- (?) Призначення кнопок миші в play-режимі puzz.link (схеми `use` 1/2).
- (?) Чи може біла мережа мати цикл — правила не забороняють, але на прикладах не перевірено.
