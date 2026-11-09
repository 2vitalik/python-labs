---
title: Reflect Link (リフレクトリンク)
slug: reflect-link
aka: [Reflect, リフレクトリンク, Рефлект-лінк]
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
year: null
platforms: [paper, web]
links:
  - {kind: other, url: "https://www.janko.at/Raetsel/Reflect/index.htm", best: true, note: "Janko: правила DE/EN, 230 пазлів грати в браузері"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/reflect.js", note: "puzz.link/pzpr: правила EN/JP, Nikoli vol. 106, тести вводу, коди помилок"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/master/src/res/failcode.en.json", note: "тексти кодів помилок pzprjs (lnExTri.reflect, lnLenGt.reflect…)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=reflect+link+puzzle", note: "пошук; розвʼязання"}
stage: v1
coverage: 65
mechanics: [markup-validity, completion-detection, satisfy-constraints, single-loop-check, path-drawing, path-cut, edge-marking, mirror-reflect, conflict-highlight, in-game-editor, editor-palette, import-open-formats, level-bank, undo-redo, +crossing-detection, +forced-crossing-cell, +segment-length-clue, +fixed-corner-cell]
proposes: ["+cond:turns", "+cond:crosses", "+cond:straight_len", "+trigger:pattern(loop_branch)", "+card:forced-crossing-cell", "+card:segment-length-clue", "+card:fixed-corner-cell"]
author: opus
date: 2026-11-09
---

# Reflect Link — одна петля, що відбивається від чорних трикутників і перетинає себе лише на позначених хрестах

## Суть
Гравець малює одну замкнену петлю через центри клітинок. Чорні трикутники займають половину клітинки по діагоналі: петля мусить пройти через кожен і повернути на 90° об його гіпотенузу, як промінь об дзеркало. Перетинати себе петля може лише в заданих клітинках-хрестах (і там мусить перетнути), а число в трикутнику каже сумарну довжину двох прямих відрізків, що від нього виходять. Незвичне: «дзеркало» з лазерних ігор (`connect-rotate`) стало обмеженням на петлю.

## Поле і час
- Прямокутна сітка; клітинки порожні, з трикутником (4 орієнтації, може мати число) або з хрестом `+`.
- У версії Janko частина відрізків петлі може бути наперед намальована.
- Шари: підказки (трикутники, числа, хрести — незмінні) · петля гравця (сегменти між центрами сусідніх клітинок) · хрестики «тут нема лінії».
- Час статичний; хід = додати/стерти сегмент.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Порожня клітинка | terrain | — | петля може пройти прямо, повернути або не пройти; перетин заборонено |
| Трикутник | static | орієнтація (4), число? | петля обовʼязково проходить; вхід і вихід — дві сторони навпроти гіпотенузи, тобто фіксований кут |
| Число в трикутнику | mark | N | довжина обох прямих відрізків від трикутника до першого повороту, разом з клітинкою трикутника |
| Хрест `+` | static | — | петля проходить у всіх 4 напрямках і перетинає себе |
| Петля | mark | сегменти | одна, замкнена, без розгалужень |
| Наперед даний відрізок | mark | — | належить петлі (Janko) |
| Мітка «нема лінії» | mark | — | допоміжний хрестик гравця |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left_drag, cells)` → ТО `custom: «додати сегменти петлі між сусідніми центрами»`; drag назад по наявному — стерти.
- КОЛИ `input(right_click, edge)` → ТО `mark(edge, no_line)` (?).
- КОЛИ `constraint_broken(no_line)` → ЯКЩО `count(segment, =, 0)` → ТО `set_state(board, error)` (pzpr `brNoLine`).
- КОЛИ `pattern(loop_branch)` → ЯКЩО `custom: «з клітинки виходить 3 сегменти»` → ТО `set_state(cell, error)` (`lnBranch`).
- КОЛИ `constraint_broken(crossing)` → ЯКЩО `custom: «петля перетинає себе»` (`+cond:crosses`) and `not cell(x, cross)` → ТО `set_state(cell, error)` (`lnCrossExMk`).
- КОЛИ `constraint_broken(cross)` → ЯКЩО `cell(x, cross)` and `custom: «у клітинці не 4 сегменти»` → ТО `set_state(cell, error)` (`lnNotCrossMk`).
- КОЛИ `constraint_broken(triangle)` → ЯКЩО `cell(x, triangle)` and `custom: «петля не проходить через трикутник»` → ТО `set_state(cell, error)` (`lnExTri`: «A line doesn't goes through a triangle»).
- КОЛИ `input(left_drag, cells)` → ЯКЩО `cell(x, triangle)` → ТО `custom: «сегменти лише з двох сторін навпроти гіпотенузи; петля повертає на 90° (відбиття)»` (`+cond:turns`).
- КОЛИ `constraint_broken(length)` → ЯКЩО `custom: «сума двох прямих відрізків від трикутника > N»` (`+cond:straight_len`) → ТО `set_state(clue, error)` (`lnLenGt`).
- КОЛИ `constraint_broken(length)` → ЯКЩО `custom: «сума < N»` → ТО `set_state(clue, error)` (`lnLenLt`).
- КОЛИ `constraint_broken(dead_end)` → ЯКЩО `custom: «у клітинці рівно 1 сегмент»` → ТО `set_state(cell, error)` (`lnDeadEnd`).
- КОЛИ `constraint_broken(loops)` → ЯКЩО `not single_loop` → ТО `set_state(board, error)` (`lnPlLoop`: «There are multiple loops»).
- КОЛИ `all_constraints_met` → ТО `win`.
- Дедукція «кут-трикутник»: орієнтація трикутника вже задає обидва сегменти в його клітинці — розвʼязок стартує з них.
- Дедукція «довжина»: число N з одним уже відомим відрізком довжини k дає другий рівно N − k (з урахуванням спільної клітинки); на хресті петля йде прямо, тож хрест не обриває відрізок (?).
- Перемога: одна петля, усі трикутники пройдені з відбиттям, усі числа збігаються, перетини рівно на хрестах. Поразки й рахунку нема.

## Керування і ввід
- puzz.link play: ліва кнопка + drag по клітинках малює петлю (тест `mouse,left, 1,3, 9,3, 9,7, 1,7, 1,3` — прямокутник); права — допоміжні мітки (?).
- puzz.link edit: клавіші `q` `w` `e` `r` — чотири орієнтації трикутника, `t` — хрест; цифри — число в трикутнику; повторні кліки по клітинці (`leftx2…x7`, `rightx2…x7`) перебирають типи вперед/назад.
- Janko: власний браузерний інтерфейс (?).
- Цифрова версія: undo/redo, перевірка за кнопкою.

## Вікна, меню, HUD
- `game-screen`: сітка, чорні трикутники з білими числами, хрести, петля, `conflict-highlight` для помилкових клітинок.
- puzz.link: перемикач play/edit, кнопка перевірки з текстом першої помилки, `settings-window`.
- `help-window` — правила (puzz.link, Janko).
- `puzzle-select` — список 230 пазлів Janko (дата, розмір, складність).
- Переходи: edit → play; check → повідомлення; список Janko → пазл.

## Фічі поза полем
- `auto-check` за кнопкою з кодами помилок pzpr.
- `undo` / `redo`; `level-editor` + `share-code` (URL пазла puzz.link).
- `puzzle-bank` Janko; генератора не бачив (?).

## Варіації й родичі
- У сімʼї: [Masyu](masyu.md) (петля з правилами поворотів у клітинках), [Icebarn](icebarn.md) (перетин дозволено лише на льоду), [Slitherlink](slitherlink.md), [Yajilin](yajilin.md); дзеркала як обʼєкти — [Kin-Kon-Kan](kin-kon-kan.md), [Undead](undead.md).
- Поза сімʼєю: Deflektor / Laser Tank (`connect-rotate`) — справжні промені й дзеркала.
- **Осі варіацій**: де дозволено перетин (задані хрести / ніде / лід) · що каже число (довжина відрізків / кількість відбиттів) · трикутник як кут петлі / як дзеркало променя · петля / шлях.

## Цікавинки для курсу
- Трикутник як «фіксований кут»: орієнтація → пара напрямків сегментів — 🌱.
- Перевірка ступенів клітинок: 0 або 2 скрізь, рівно 4 на хресті, кут на трикутнику — 📎.
- Обчислення довжини прямих відрізків від трикутника до першого повороту (прохід через хрест — прямо) — 📎.
- Перевірка однієї петлі з перетинами (обхід графа, де хрест — дві незалежні проходки) — 🥉.
- Валідатор з кодами помилок як у pzpr — 🥉; розвʼязувач — 🥇.

## Мапа на каталог
- Є: `markup-validity`, `completion-detection`, `satisfy-constraints`, `single-loop-check` · `path-drawing`, `path-cut`, `edge-marking` ↔ ввід петлі · `mirror-reflect` ↔ відбиття об гіпотенузу (аналогія) · `conflict-highlight` · `in-game-editor`, `editor-palette`, `import-open-formats` (puzz.link) · `level-bank` (Janko) · `undo-redo`.
- **Нема** → пропозиції карток:
  - `+crossing-detection` — повтор: виявлення самоперетину лінії.
  - `+forced-crossing-cell` «Клітинка-хрест: перетин тут обовʼязковий, деінде заборонений» · game-logic/constraints · 🌱 · слот {cross: given|ice|none}.
  - `+segment-length-clue` «Число = довжина прямих відрізків від клітинки до першого повороту» · game-logic/constraints · 📎 · слот {count: both|each}.
  - `+fixed-corner-cell` «Клітинка, що задає кут лінії (дзеркало-трикутник)» · game-logic/constraints · 🌱.

## Пропозиції до словників
- `+cond:turns` — лінія повертає в клітинці (повтор з Masyu/Icebarn).
- `+cond:crosses` — лінія перетинає себе в клітинці (повтор).
- `+cond:straight_len` — довжина прямого відрізка лінії від клітинки до першого повороту.
- `+trigger:pattern(loop_branch)` — розгалуження лінії (повтор).
- `+card:forced-crossing-cell`, `+card:segment-length-clue`, `+card:fixed-corner-cell` — див. мапу.

## Джерела
- ⭐ [Janko: Reflect](https://www.janko.at/Raetsel/Reflect/index.htm) — правила DE/EN (наперед дані відрізки, перетин лише на хрестах, відбиття 90°), японська назва リフレクトリンク, 230 пазлів; винахідник невідомий.
- [puzz.link reflect.js](https://puzz.link/js/pzpr-samples/reflect.js) — правила EN/JP: «loop reflects at a right angle off a triangle's hypotenuse», число — «total cell count of the two line segments leaving it, up to their first turn»; Nikoli vol. 106; тести вводу; коди `brNoLine`, `lnBranch`, `lnCrossExMk`, `lnLenGt`, `lnExTri`, `lnLenLt`, `lnNotCrossMk`, `lnDeadEnd`, `lnPlLoop`.
- [pzprjs failcode.en.json](https://raw.githubusercontent.com/robx/pzprjs/master/src/res/failcode.en.json) — тексти помилок.
- YouTube: пошук «reflect link puzzle».

## Непевне
- (?) Рік: перша поява — Puzzle Communication Nikoli vol. 106; рік номера не перевірено (`year: null`).
- (?) Чи переривається відрізок на хресті — з тексту «up to their first turn» випливає, що ні (на хресті петля йде прямо), але явно не сказано.
- (?) Призначення правої кнопки в play-режимі puzz.link та інтерфейс Janko — не бачив.
- (?) Наперед дані відрізки — є в правилах Janko, у puzz.link-правилах не згадані.
