---
title: Sto-stone (ストストーン)
slug: sto-stone
aka: [Stostone, ストストーン]
family: pencil-logic
also: [dig-gravity]
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
  - {kind: official, url: "https://www.nikoli.co.jp/en/puzzles/sto_stone/", best: true, note: "Nikoli: правила кімнат і «скинь камені вниз», Sample → Progressing ×2 → Solution"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/stostone.js", note: "puzz.link: правила EN/JP, «Nikoli vol. 156», коди помилок"}
  - {kind: other, url: "https://puzz.link/rules.html?stostone", note: "puzz.link: сторінка правил (рендериться JS)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=sto-stone+puzzle+nikoli", note: "пошук; розвʼязання"}
stage: v1
coverage: 60
mechanics: [markup-validity, completion-detection, satisfy-constraints, cell-click, gravity-fall, connectivity-check, in-game-editor, import-open-formats, undo-redo, dot-mark, +cell-shade-toggle, +region-size-check, +virtual-gravity-check]
proposes: ["+cond:region_size", "+cond:touch_across_border", "+cond:fills_bottom_half", "+card:virtual-gravity-check"]
author: opus
date: 2026-11-09
---

# Sto-stone — зафарбуй по одному блоку в кімнаті так, щоб після «падіння» вони заповнили нижню половину

## Суть
Сітка поділена жирними межами на кімнати; у частині кімнат стоїть число. Гравець зафарбовує клітинки: у кожній кімнаті — рівно один ортогонально звʼязний блок, число задає його розмір, а блоки з різних кімнат не торкаються через межу. Головне правило — уявна гравітація: якщо всі блоки впадуть прямо вниз, не змінюючи форми, вони мають точно заповнити нижню половину поля. Незвичне: перевірка розвʼязку — **симуляція фізики** (Tetris-падіння), а не статичне обмеження.

## Поле і час
- Прямокутна сітка з парною висотою (інакше «нижня половина» не ділиться) (?); кімнати — довільні поліоміно, задані жирними межами.
- Шари: кімнати й числа (незмінні) · стан клітинки: порожньо / зафарбовано (камінь) / мітка «не камінь».
- Уявний шар перевірки: позиції блоків після падіння.
- Час статичний; хід = зафарбувати/зняти/позначити.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітинка | mark | стан empty / shaded / dot | зафарбована = частина каменя |
| Кімната | zone | число N або без числа | містить рівно один блок; з числом — розміру N |
| Блок (камінь) | object | форма, розмір | звʼязна група зафарбованих у кімнаті; при падінні — тверда фігура |
| Межа кімнати | static | — | зафарбовані клітинки по різні боки межі не можуть бути сусідами |
| Нижня половина | zone | H/2 рядків | після падіння має бути заповнена без дірок |
| Мітка «не камінь» | mark | — | позначка гравця, на перевірку не впливає |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left_click, cell)` → ТО `mark(cell, shaded)`; повтор → `unmark(cell)` (типова схема pzpr) (?).
- КОЛИ `input(right_click, cell)` → ТО `mark(cell, dot)` (?).
- КОЛИ `constraint_broken(one_block)` → ЯКЩО `not connected(shaded in room)` → ТО кімната конфліктна (puzz.link `bkShadeDivide`).
- КОЛИ `constraint_broken(one_block)` → ЯКЩО `count(shaded in room, ==, 0)` → ТО кімната конфліктна (puzz.link `bkNoShade`).
- КОЛИ `constraint_broken(size)` → ЯКЩО `custom: «розмір блоку ≠ числу кімнати»` (`+cond:region_size`) → ТО конфлікт (puzz.link `bkShadeNe`).
- КОЛИ `constraint_broken(border)` → ЯКЩО `custom: «два камені сусідять через межу кімнат»` (`+cond:touch_across_border`) → ТО конфлікт (puzz.link `cbShade`).
- КОЛИ `custom: «перевірка розвʼязку»` → ТО `fall(block)` для кожного блоку як твердої фігури, знизу вгору, доки не впреться в дно чи інший блок.
- КОЛИ `settled` → ЯКЩО `custom: «камінь лишився у верхній половині»` → ТО конфлікт (puzz.link `csUpper`).
- КОЛИ `settled` → ЯКЩО `custom: «у нижній половині лишилась порожня клітинка»` (`+cond:fills_bottom_half`) → ТО конфлікт (puzz.link `cuLower`).
- КОЛИ `all_constraints_met` → ТО `win`.
- Дедукція «стовпець»: падіння прямо вниз не міняє кількість каменів у стовпці → у кожному стовпці рівно H/2 зафарбованих.
- Дедукція «площа»: сума розмірів усіх блоків = половина площі поля; кімнати без числа беруть залишок.
- Дедукція «межа»: клітинки по обидва боки межі поруч із каменем — не камені.
- Після падіння блоки можуть торкатися через межі кімнат (Nikoli) — це дозволено.
- Перемога: усі кімнати мають по одному блоку правильного розміру, межі чисті, падіння заповнює нижню половину. Поразки й рахунку нема.

## Керування і ввід
- Папір: зафарбувати клітинки, крапки — «не камінь».
- puzz.link: тестів вводу у файлі нема (`inputs: []`); ввід, імовірно, стандартний для shade-жанрів: ліва — зафарбувати, права — крапка, drag — серія (?).
- Цифрова версія: undo/redo, перевірка за кнопкою.

## Вікна, меню, HUD
- `game-screen`: сітка з жирними межами кімнат, числа в кутках кімнат, зафарбовані клітинки, `conflict-highlight`.
- (цифрова версія) превʼю «після падіння» — `+ui` не пропоную, бо в джерелах не бачив (?).
- puzz.link: play/edit, кнопка перевірки з повідомленням першої помилки, `settings-window`.
- `help-window` — правила (Nikoli, puzz.link rules).
- Переходи: edit → play; check → повідомлення.

## Фічі поза полем
- `auto-check` за кнопкою (puzz.link коди помилок).
- `undo` / `redo`; `level-editor` + `share-code` (puzz.link URL).
- Банк — журнал і книги Nikoli; генератора не бачив (?).

## Варіації й родичі
- Родичі: [LITS](lits.md) (одна фігура в кожній кімнаті + глобальне обмеження), [Fillomino](fillomino.md) (розмір блоку = число), [Heyawake](heyawake.md) (кімнати з числом зафарбованих), Tetris (`falling-match`) і Boulder Dash (`dig-gravity`) — справжня гравітація замість уявної.
- **Осі варіацій**: напрямок падіння (вниз / до центру / вбік) · яку частину поля треба заповнити (нижню половину / задану фігуру) · блоки при падінні тверді чи «пісок» (кожна клітинка падає окремо) · кімнати з числом / без.

## Цікавинки для курсу
- Падіння твердих поліоміно: сортувати блоки за нижньою клітинкою, кожен опускати до упору — 📎; з урахуванням того, що блок може лежати на кількох — 🥉.
- Перевірка «нижня половина заповнена без дірок» після симуляції — 🌱.
- Один звʼязний блок у кімнаті (flood fill по кімнаті) — 🌱.
- Заборона дотику через межу кімнат — 🌱 (перевірка пар сусідів з різними room-id).
- Дедукція «рівно H/2 у кожному стовпці» як швидкий відсів — 🌱; повний розвʼязувач — 🥇.

## Мапа на каталог
- Є: `markup-validity`, `completion-detection`, `satisfy-constraints` · `cell-click` · `gravity-fall` ↔ уявне падіння · `connectivity-check` ↔ один блок у кімнаті · `in-game-editor`, `import-open-formats` (puzz.link) · `undo-redo`, `dot-mark`.
- Перевикористано: `+cell-shade-toggle`, `+region-size-check` (з Fillomino/LITS).
- **Нема** → пропозиції карток:
  - `+virtual-gravity-check` «Перевірка розвʼязку уявним падінням» · game-logic/constraints · 🥉 · слот {dir: down, body: rigid|sand, target: bottom-half|shape}.

## Пропозиції до словників
- `+cond:region_size` — розмір групи/блоку дорівнює числу (повтор з Fillomino).
- `+cond:touch_across_border` — дві зафарбовані клітинки сусідять через межу кімнат.
- `+cond:fills_bottom_half` — після падіння нижня половина поля заповнена повністю.
- `+card:virtual-gravity-check` — див. мапу.

## Джерела
- ⭐ [Nikoli: Sto-stone](https://www.nikoli.co.jp/en/puzzles/sto_stone/) — 4 правила (кімнати, число = довжина блоку, нема дотику через межу, падіння заповнює нижню половину), 4 ілюстрації.
- [puzz.link stostone.js](https://puzz.link/js/pzpr-samples/stostone.js) — «All regions contain exactly one block», «fall straight down without changing shape», Nikoli vol. 156; коди `cbShade`, `bkShadeDivide`, `csUpper`, `bkShadeNe`, `cuLower`, `bkNoShade`.
- [puzz.link rules](https://puzz.link/rules.html?stostone) — сторінка правил (через WebFetch текст не рендериться).
- YouTube: пошук «sto-stone puzzle nikoli».

## Непевне
- (?) Рік: перша поява — Puzzle Communication Nikoli vol. 156; рік номера не перевірено (`year: null`).
- (?) Розходження: переказ Nikoli — «кімнати без числа можуть мати будь-яку кількість чорних»; puzz.link — «у кожній кімнаті рівно один блок». Імовірно, «будь-якого розміру», але один блок.
- (?) Розшифровка кодів помилок puzz.link — моя, за назвами (`cs` = shaded cell, `cu` = unshaded cell, `bk` = block/room).
- (?) Ввід у puzz.link не перевірено (тестів вводу нема).
- (?) Чи гарантовано парна висота поля — випливає з правила, у джерелах прямо не сказано.
