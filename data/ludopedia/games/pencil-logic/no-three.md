---
title: No Three (ノースリー)
slug: no-three
aka: [ノースリー, Nothree, Nōsuriichi, «Без трійок»]
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
  - {kind: other, url: "https://puzz.link/rules.html?nothree", best: true, note: "puzz.link: правила з прикладом (рендер JS)"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/nothree.js", note: "правила EN/JA, Nikoli vol. 158, 6 кодів помилок, тести вводу кружків"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/master/src/variety/nothree.js", note: "код pzprjs: кружки в клітинці/на ребрі/у вузлі, перевірка рівних проміжків"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/master/src/res/failcode.en.json", note: "тексти помилок pzpr"}
  - {kind: other, url: "https://www.janko.at/Raetsel/Nikoli/158.htm", note: "Janko: огляд Nikoli № 158, правила EN/DE/JA під назвою Nōsuriichi"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=no+three+nikoli+puzzle", note: "пошук; розвʼязання"}
stage: v1
coverage: 70
mechanics: [markup-validity, completion-detection, satisfy-constraints, cell-click, connectivity-check, conflict-highlight, keyboard-controls, edge-marking, in-game-editor, import-open-formats, undo-redo, +cell-shade-toggle, +no-adjacent-check, +global-connectivity, +vertex-clue, +input-scheme-toggle, +no-equal-spacing]
proposes: ["+cond:equal_spacing", "+trigger:pattern(equal_spacing3)", "+card:no-equal-spacing"]
author: opus
date: 2026-11-09
---

# No Three — зафарбуй клітинки так, щоб жодні три чорні поспіль у рядку не стояли на рівних відстанях

## Суть
Гравець зафарбовує клітинки за чотирма правилами: чорні не торкаються сторонами, білі звʼязні, кожен маленький кружок торкається рівно однієї чорної, і в кожному рядку та стовпці три послідовні чорні клітинки не можуть мати однакові проміжки. Незвичне: головне обмеження — **арифметичне** (заборона рівномірного кроку), а кружки стоять не лише в клітинках, а й на ребрах та у вузлах сітки.

## Поле і час
- Прямокутна сітка; кружок можна поставити в центр клітинки (торкається 1 клітинки), на ребро (2) або у вузол (4) — JA: «接している最大4マス».
- «Послідовні» чорні — сусідні серед чорних цього рядка/стовпця; білі між ними не рахуються.
- Шари: кружки (незмінні) · стан клітинки: невідома / чорна / біла (крапка) · допоміжні хрестики на ребрах (на ребрі з кружком — заборонені).
- Час статичний; хід = зафарбувати / позначити / стерти.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітинка | mark | невідома / чорна / біла | гравець перемикає стан |
| Кружок у клітинці | static | 1 клітинка | ця клітинка чорна |
| Кружок на ребрі | static | 2 клітинки | рівно одна з двох чорна |
| Кружок у вузлі | static | 4 клітинки | рівно одна з чотирьох чорна |
| Чорна клітинка | mark | — | без чорних сусідів по сторонах |
| Трійка послідовних чорних | zone | проміжки d1, d2 | d1 ≠ d2 |
| Біла область | zone | — | одна 4-звʼязна компонента |
| Хрестик на ребрі | mark | — | допоміжна позначка, не перевіряється |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left_click, cell)` → ТО `mark(cell, shaded)`; права кнопка — `mark(cell, white)`; біля ребра — `mark(edge, cross)` (pzpr `cellpeke`) (?).
- КОЛИ `constraint_broken(no_shade)` → ЯКЩО `count(shaded, ==, 0)` → ТО помилка (`brNoShade`).
- КОЛИ `constraint_broken(adjacent)` → ЯКЩО `not no_adjacent(shaded)` → ТО `set_state(cells, error)` (`csAdjacent`: «Some shaded cells are adjacent»).
- КОЛИ `constraint_broken(dot_over)` → ЯКЩО `count(shaded touching dot, >, 1)` → ТО `set_state(dot, error)` (`csGt1`: «A dot overlaps more than one shaded cell»).
- КОЛИ `constraint_broken(white_connected)` → ЯКЩО `not connected(white)` → ТО `set_state(board, error)` (`cuDivideRB`: «The unshaded cells are divided»).
- КОЛИ `pattern(equal_spacing3)` → ЯКЩО `custom: «три послідовні чорні в рядку/стовпці мають рівні проміжки»` (`+cond:equal_spacing`) → ТО `set_state(cells, error)` (`csDistance`: «Three consecutive cells in the same row have the same distance»).
- КОЛИ `constraint_broken(dot_under)` → ЯКЩО `count(shaded touching dot, ==, 0)` → ТО `set_state(dot, error)` (`csLt1`: «A dot doesn't overlap a shaded cell»).
- КОЛИ `all_constraints_met` → ТО `win`.
- Дедукція «центр»: кружок у клітинці → вона чорна, чотири сусіди білі.
- Дедукція «ребро»: кружок на ребрі → одна з двох чорна; щойно одна визначилась, друга — протилежна.
- Дедукція «крок»: чорні в позиціях x1 < x2 поспіль → клітинка x2 + (x2 − x1) може бути чорною, лише якщо між нею й x2 є ще чорна; тож шаблон «Ч·Ч·Ч» (крок 2, 2) заборонений.
- Дедукція «розріз»: діагональний ланцюжок чорних не може відрізати частину білих (як у Hitori).
- Перемога: усі обмеження виконані. Поразки й рахунку нема.

## Керування і ввід
- Play (puzz.link): режими `shade`, `unshade`, `peke`, `info-blk`; схема кнопок `use`.
- Edit: клік у точці з точністю чверть клітинки ставить/знімає кружок у центрі, на ребрі чи у вузлі; режим `circle-unshade` — протяжкою ставить кружки в ряд (тест «Input multiple dots»).
- Клавіатура в редакторі: курсор ходить півклітинками (`moveTBorder`), `1` — кружок, пробіл/`-`/`0` — стерти.
- Папір: зафарбувати клітинку, крапкою — «точно біла».

## Вікна, меню, HUD
- `game-screen`: світла сітка, маленькі кружки, чорні клітинки, крапки, хрестики, `conflict-highlight` — трійка з рівним кроком (уся смуга від першої до третьої), кружок разом із його клітинками.
- puzz.link — спільний інтерфейс ([puzz-link](puzz-link.md)): Check, Undo/Redo, Edit/Play, `help-window`, URL input/output, `settings-window` (схема вводу).
- Переходи: rules.html → p?nothree → Check → текст помилки.

## Фічі поза полем
- `auto-check` з кодами pzpr; `undo` / `redo`.
- `level-editor` + `share-code` (URL).
- Банку пазлів окрім журналу Nikoli й прикладу puzz.link не бачив (?).

## Варіації й родичі
- Двигун «чорні не торкаються + білі звʼязні» — [Hitori](hitori.md), [Heyawake](heyawake.md), [Kuromasu](kuromasu.md), [One Room One Door](one-room-one-door.md).
- Кружок на ребрі/у вузлі, що рахує дотичні клітинки, — [Kuralin](kuralin.md) (більшість кольору), [Slant](slant.md) (числа у вузлах); у pzpr схожу умову «кружок перекриває рівно одну чорну» має Sumiwake (кружки у вузлах).
- Заборона рівного кроку — далекий родич задач про множини без 3-членних арифметичних прогресій (тут лише для сусідніх серед чорних).
- **Осі варіацій**: де стоїть підказка (клітинка / ребро / вузол) · скільки чорних торкається кружка (рівно 1 / ≥ 1) · заборона кроку (лише послідовні / будь-які три) · звʼязність білих.

## Цікавинки для курсу
- Перевірка рівного кроку: ковзне вікно з 3 по списку чорних у рядку — 🌱.
- Подвоєні координати pzpr: клітинки на непарних, вузли на парних, ребра — змішані; одна функція «які клітинки торкається кружок» для трьох місць — 📎.
- Заборона сусідства + звʼязність білих (BFS) — 🌱 + 📎.
- Повний валідатор з підсвіткою смуги трійки — 🥉; розвʼязувач — 🥇.

## Мапа на каталог
- Є: `markup-validity`, `completion-detection`, `satisfy-constraints` · `cell-click` · `connectivity-check` ↔ білі · `conflict-highlight` · `keyboard-controls` · `edge-marking` ↔ хрестики на ребрах · `in-game-editor`, `import-open-formats` · `undo-redo`.
- Перевикористано: `+cell-shade-toggle`, `+no-adjacent-check`, `+global-connectivity` (Hitori, Heyawake), `+vertex-clue` (Slant; тут ще й ребра й центри), `+input-scheme-toggle`.
- **Нема** → пропозиції карток:
  - `+no-equal-spacing` «Три послідовні позначені в лінії не на рівних відстанях» · game-logic/constraints · 🌱 · слот {scope: consecutive|any}.

## Пропозиції до словників
- `+cond:equal_spacing` — три сутності в лінії стоять із рівним кроком.
- `+trigger:pattern(equal_spacing3)` — значення для `pattern(shape)`: трійка з рівним кроком.
- `+card:no-equal-spacing` — див. мапу.

## Джерела
- ⭐ [puzz.link rules: nothree](https://puzz.link/rules.html?nothree) — правила з прикладом (рендер JS).
- [pzpr-samples nothree.js](https://puzz.link/js/pzpr-samples/nothree.js) — правила EN/JA, «first appeared in Puzzle Communication Nikoli vol. 158», коди `brNoShade`, `csAdjacent`, `cuDivideRB`, `csLt1`, `csGt1`, `csDistance`.
- [pzprjs nothree.js](https://raw.githubusercontent.com/robx/pzprjs/master/src/variety/nothree.js) — `dotCells` для клітинки, ребра й вузла; `checkThreeRow`; режими вводу.
- [failcode.en.json](https://raw.githubusercontent.com/robx/pzprjs/master/src/res/failcode.en.json) — тексти `csGt1.nothree`, `csLt1.nothree`, `csDistance.nothree`.
- [Janko: Nikoli № 158](https://www.janko.at/Raetsel/Nikoli/158.htm) — правила EN/DE/JA («the distance from the middle one to the two other must not be the same»).

## Непевне
- (?) Рік: Nikoli vol. 158; за квартальним виходом (Janko: № 163 — червень 2018) ≈ березень 2017 — дати не бачив.
- (?) Назва Janko «Nōsuriichi» схоже на хибне прочитання ノースリー; у pzpr — «No Three».
- (?) Призначення кнопок миші (`use`, `cellpeke`) у play-режимі; перевірка `doneShadingDecided` у кінці списку не прочитана.
- (?) Онлайн-банку пазлів (Janko, GM Puzzles) не знайшов.
