---
title: Usowan (ウソワン)
slug: usowan
aka: [Usoone, Uso-one, ウソワン, Одна брехня]
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
  - {kind: official, url: "https://www.nikoli.co.jp/en/puzzles/usowan/", best: true, note: "Nikoli: 4 правила EN, картинки Sample → Progressing → Solution"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/usoone.js", note: "puzz.link: правила EN/JA, історія (Nikoli vol.151), коди помилок, тести вводу"}
  - {kind: other, url: "https://puzz.link/rules.html?usoone", note: "puzz.link: сторінка правил (рендериться JS)"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/main/src/variety/usoone.js", note: "pzprjs: код — визначення брехуна, позначки ○/× на числах, перевірка «рівно один брехун у кімнаті»"}
  - {kind: other, url: "https://www.janko.at/Raetsel/Usoone/index.htm", note: "Janko: правила DE/EN, 130 пазлів для гри в браузері"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=usowan+puzzle+nikoli", note: "пошук; розвʼязання"}
stage: v1
coverage: 65
mechanics: [cell-click, dot-mark, neighbor-count-clue, connectivity-check, markup-validity, completion-detection, satisfy-constraints, conflict-highlight, undo-redo, in-game-editor, import-open-formats, level-bank, level-solver, unique-puzzle-generation, +cell-shade-toggle, +no-adjacent-check, +irregular-regions, +liar-clue, +clue-done-mark]
proposes: ["+cond:liar_count", "+ui:clue-truth-mark", "+card:liar-clue"]
author: opus
date: 2026-11-09
---

# Usowan — зафарбовування з числами-сусідами, де в кожній кімнаті рівно одне число бреше

## Суть
Сітка поділена товстими лініями на кімнати; у клітинках стоять числа — скільки чорних серед 4 сусідів. Гравець зафарбовує клітинки за правилами Hitori-родини: чорні не торкаються сторонами, білі звʼязні, числа завжди білі. Головне: **у кожній кімнаті рівно одне число неправильне** — показує хибну кількість. Незвичне: розвʼязувач паралельно вирішує, *яке* число бреше, — брехня тут не шум, а обмеження «рівно один на регіон».

## Поле і час
- Прямокутна сітка; кімнати — у Nikoli прямокутники в товстих рамках, puzz.link дозволяє будь-яку форму.
- Сусідство ортогональне (4): для лічильника числа, заборони дотику чорних і звʼязності білих.
- Шари: межі кімнат і числа (незмінні) · стан клітинки: невідомо / чорна / крапка · позначка на числі: ○ «правда» / × «брехня».
- Час статичний; хід = зміна стану клітинки або позначки числа.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Кімната | zone | клітинки в товстій рамці | рівно одне число в ній хибне → у кімнаті ≥ 1 число |
| Число | static | 0…4 | біла клітинка; правдиве = кількість чорних серед 4 сусідів |
| Число-брехун | static | — | кількість чорних сусідів ≠ числу; рівно одне на кімнату |
| Клітинка | mark | unknown / shaded / dot | клік змінює стан |
| Чорна клітинка | mark | — | не торкається іншої чорної сторонами |
| Крапка | mark | — | позначка «тут біле», на перевірку не впливає |
| Позначка ○ / × | mark | на числі | нотатка гравця «правда / брехня», на перевірку не впливає |
| Біла область | zone | компоненти | усі білі — одна 4-звʼязна компонента |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left_click, cell)` → ТО `mark(cell, shaded)`; права кнопка → `mark(cell, dot)` (?).
- КОЛИ `input(left_click, clue)` → ТО `mark(clue, ×)` → повтор `mark(clue, ○)` → повтор `unmark(clue)`; права кнопка — у зворотному порядку (код `[2,0,1]` / `[1,2,0]`).
- КОЛИ `input(click, clue)` → ТО `custom: «число не зафарбовується»` (`numberRemainsUnshaded`).
- КОЛИ `constraint_broken(adjacent)` → ЯКЩО `not no_adjacent(shaded)` → ТО `message(csAdjacent)`.
- КОЛИ `constraint_broken(connect)` → ЯКЩО `not connected(unshaded)` → ТО `message(cuDivideRB)`.
- Брехун: ЯКЩО `not adjacent_count(clue, shaded, ==, n)` → ТО `custom: «число — брехун»` (`isLiar`).
- КОЛИ `constraint_broken(liars)` → ЯКЩО `custom: «брехунів у кімнаті ≠ 1»` (`+cond:liar_count`) → ТО `message(bkLiarNe1)` («The number of liars in a room is not one»).
- КОЛИ `all_constraints_met` → ТО `win`.
- Дедукція «одне число в кімнаті»: воно і є брехуном — його значення точно хибне (напр., «0» → хоча б один сусід чорний).
- Дедукція «неможливе значення»: «4» біля краю чи «3» в куті не може бути правдою → це брехун своєї кімнати, решта чисел кімнати правдиві.
- Дедукція «два числа»: рівно одне з двох правдиве — розгалуження на два випадки, часто одне з них ламає звʼязність білих.
- Дедукція з Hitori-родини: біля чорної всі 4 сусіди білі; чорні не можуть «відрізати» білу область.
- Перемога: чорні не торкаються, білі звʼязні, у кожній кімнаті рівно одне число не збігається з кількістю чорних сусідів. Поразки й рахунку нема.

## Керування і ввід
- puzz.link play mode: режими `shade`, `unshade`, `submark` (цикл ○/×), `subcircle`, `subcross`, `peke`, `info-blk`; Alt + drag — хрестики (?).
- Drag протягує стан зафарбовування по клітинках.
- Edit mode: межі кімнат — drag по ребрах, числа — клік і клавіатура.
- Undo/redo, Check (перша помилка з кодом), Clear.
- Janko (інтерактивно): клітинки фарбуються в чорне або біле.

## Вікна, меню, HUD
- `game-screen`: сітка з товстими межами кімнат, числа, чорні клітинки, крапки, зелені ○/× на числах + `conflict-highlight` (кімната з неправильною кількістю брехунів, сусідні чорні, розрізані білі).
- Кнопки: Check, Undo, Redo, Clear answer.
- `editor-window` — puzz.link edit mode: межі, числа, експорт URL.
- `help-window` — правила (Nikoli: Sample / Progressing / Solution).
- `puzzle-select` — архів Janko, банк puzz.link (цифрова версія).
- `end-screen` — повідомлення «розвʼязано».
- Переходи: puzzle-select → game-screen → Check → помилка / end-screen.

## Фічі поза полем
- `auto-check` за кнопкою з кодом порушення; `undo` / `redo`.
- `level-editor` + `share-code` (URL puzz.link).
- `puzzle-bank`: журнал Nikoli, Janko (130 пазлів).

## Варіації й родичі
- [Yajisan-Kazusan](yajisan-kazusan.md) — інша Nikoli-брехня: хибна стрілка мусить стояти на чорній клітинці.
- Janko-варіант Yajisan-Kazusan «Liar» — рівно одне хибне число на рядок і стовпець.
- [14 Minesweeper Variants](../hidden-deduction/14-minesweeper-variants.md) — брехун «±1» у сапері.
- Uso-tatami — ще один Nikoli-жанр з «uso» у назві (у черзі сімʼї, правил не перевіряв) (?).
- Родичі за двигуном: [Heyawake](heyawake.md) (кімнати + чорні не торкаються + білі звʼязні), [Hitori](hitori.md), [Kuromasu](kuromasu.md), [Light Up](light-up.md) (число рахує 4 сусідів).
- Janko відносить до родини Kuroshuto, Heyawake, AYE-Heya.
- **Осі брехні**: скільки брехунів (1 на кімнату / 1 на рядок і стовпець / усі) · як бреше (будь-яке хибне / рівно ±1) · що з брехуном (лише позначити / мусить бути зафарбований) · позначка брехуна (нотатка / частина відповіді).

## Цікавинки для курсу
- Лічильник 4 сусідів і визначення «брехун» — 🌱.
- Перевірка «рівно один брехун на кімнату» через мапу клітинка → кімната — 🌱.
- Звʼязність білих (flood fill) + заборона дотику чорних — 📎 (спільний двигун Hitori/Heyawake).
- Позначки ○/× на числах як окремий шар нотаток гравця з циклом лівою/правою кнопкою — 🌱.
- Розвʼязувач: CSP з додатковою змінною «хто брехун» на кімнату — 🥇.
- Генератор, де брехун не очевидний, з єдиним розвʼязком — 👑.

## Мапа на каталог
- Є: `cell-click`, `dot-mark` · `neighbor-count-clue` ↔ число рахує 4 сусідів · `connectivity-check` ↔ білі звʼязні · `markup-validity`, `completion-detection`, `satisfy-constraints`, `conflict-highlight` · `undo-redo` · `in-game-editor`, `import-open-formats`, `level-bank`, `level-solver`, `unique-puzzle-generation`.
- Перевикористано: `+cell-shade-toggle`, `+no-adjacent-check` (Hitori, Heyawake) · `+irregular-regions` (puzz.link-кімнати) · `+liar-clue` (14 Minesweeper Variants) · `+clue-done-mark` ↔ ○/× на числах.
- **Нема** → пропозиції карток:
  - `+liar-clue` «Частина підказок хибна за правилом-квотою» · game-logic/constraints · 📎 · слоти {liars_per: region|row-col|all, lie: any|±1, liar_cell: free|shaded}.

## Пропозиції до словників
- `+cond:liar_count` — кількість хибних підказок у регіоні / рядку порівняно з N.
- `+ui:clue-truth-mark` — позначка ○/× «правда / брехня» на клітинці-підказці.
- `+card:liar-clue` — див. мапу (повтор з 14 Minesweeper Variants).

## Джерела
- ⭐ [Nikoli: Usowan](https://www.nikoli.co.jp/en/puzzles/usowan/) — офіційні правила («in each rectangle bordered by bold lines, there is one (and only one) wrong number»), картинки прикладу.
- [puzz.link: usoone.js](https://puzz.link/js/pzpr-samples/usoone.js) — правила EN/JA, «first appeared in Puzzle Communication Nikoli vol. 151», коди `csAdjacent`, `cuDivideRB`, `bkLiarNe1`.
- [pzprjs: usoone.js](https://raw.githubusercontent.com/robx/pzprjs/main/src/variety/usoone.js) — `isLiar`, цикл ○/×, чекліст перевірок.
- [Janko: Usoone](https://www.janko.at/Raetsel/Usoone/index.htm) — правила DE/EN, «автор невідомий», 130 пазлів.
- [puzz.link rules](https://puzz.link/rules.html?usoone) — сторінка правил (без JS порожня).

## Непевне
- (?) Рік: Nikoli vol.151 — за датуванням номерів у JA-Вікіпедії (№150 — весна 2015, журнал квартальний) це приблизно літо 2015; прямої дати не бачив.
- (?) Назва: ウソ = «брехня» (嘘), ワン = англ. «one» — «одна брехня»; Janko тлумачить інакше. `aka` «Одна брехня» — описова.
- (?) Розкладка мишею (права кнопка — крапка чи чорна, `RBShadeCell`) не перевірена в живому інтерфейсі.
- (?) Чи може кімната в Nikoli бути непрямокутною — офіційні правила кажуть «rectangle».
