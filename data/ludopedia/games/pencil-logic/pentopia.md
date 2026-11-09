---
title: Pentopia
slug: pentopia
aka: [Пентопія]
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
year: 2011
platforms: [paper, web]
links:
  - {kind: other, url: "https://www.gmpuzzles.com/blog/?p=22920", best: true, note: "GM Puzzles: правила, походження (Bram de Laat, LMI 2011), варіант «не всі фігури»"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/pentopia.js", note: "puzz.link: правила EN/JP, коди помилок, тести вводу, пазл-приклад"}
  - {kind: other, url: "https://puzz.link/rules.html?pentopia", note: "puzz.link: сторінка правил (рендериться JS)"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/main/src/res/failcode.en.json", note: "pzprjs: тексти помилок pentopia"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=pentopia+puzzle", note: "пошук; розвʼязання"}
stage: v1
coverage: 60
mechanics: [polyomino-placement, markup-validity, completion-detection, satisfy-constraints, conflict-highlight, cell-click, keyboard-controls, in-game-editor, undo-redo, level-bank, +shape-identity-check, +shape-bank, +nearest-in-direction-clue, +multi-arrow-clue]
proposes: ["+cond:nearest_dist(cell, dir, kind)", "+cond:touches8(a, b)", "+ui:shape-bank", "+card:shape-bank", "+card:nearest-in-direction-clue", "+card:multi-arrow-clue"]
author: opus
date: 2026-11-09
---

# Pentopia — розстав фігури з банку так, щоб стрілки вказували на найближчу

## Суть
Поруч із сіткою лежить банк фігур (класично — пентаміно). Гравець зафарбовує клітинки, викладаючи частину фігур банку, кожну не більше разу; повороти й дзеркала дозволені. Фігури не торкаються ні стороною, ні кутом. Клітинки-підказки зі стрілками кажуть, у яких напрямках лежить найближча фігура. Незвичне: підказка описує не сусідство, а «що я бачу першим» у чотирьох напрямках, і рівновіддаленість усіх позначених напрямків.

## Поле і час
- Прямокутна сітка; GM Puzzles радить 10×10–12×12, інші розміри можливі.
- Шари: клітинки-підказки зі стрілками (незмінні) · зафарбування гравця · крапки «тут порожньо».
- Банк фігур — поза полем, поруч (у puzz.link — набір форм, заданий автором пазла).
- Час статичний; хід = зафарбувати/очистити клітинку.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітинка | terrain | — | порожня або частина фігури |
| Підказка-стрілки | mark | набір напрямків (1–4), значення-бітова маска 1–15 | не може бути зафарбована; найближча фігура — у позначених напрямках |
| Фігура банку | supply | форма (пентаміно), до 1 разу | кладеться як звʼязна група зафарбованих клітинок |
| Зафарбована клітинка | mark | — | частина однієї фігури |
| Крапка | mark | — | «порожньо», на перевірку не впливає |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(click, cell)` → ЯКЩО `not occupied(cell, clue)` → ТО `mark(cell, shaded)`; повтор — `unmark(cell)` або крапка.
- КОЛИ `input(click, clue)` → ЯКЩО `mode(play)` → ТО `block` (стрілку не зафарбувати; налаштування `pentopia_transparent` дозволяє).
- КОЛИ `constraint_broken(shape)` → ЯКЩО `custom: «звʼязна група зафарбованих не збігається з жодною фігурою банку з точністю до поворотів і дзеркал»` → ТО `set_state(group, error)` («The board contains an invalid piece»).
- КОЛИ `constraint_broken(bank)` → ЯКЩО `custom: «одна фігура банку викладена двічі»` → ТО `set_state(group, error)` («A piece appears too many times»).
- КОЛИ `constraint_broken(touch)` → ЯКЩО `custom: «дві фігури торкаються кутом»` (`+cond:touches8`) → ТО `set_state(group, error)` («Two pieces are diagonally adjacent»); дотик стороною зливає їх в одну неправильну групу.
- КОЛИ `constraint_broken(clue)` → ЯКЩО `custom: «клітинка з підказкою зафарбована»` → ТО `set_state(clue, error)`.
- КОЛИ `constraint_broken(arrow)` → ЯКЩО `custom: «у напрямку стрілки нема жодної зафарбованої клітинки»` → ТО `set_state(clue, error)`.
- КОЛИ `constraint_broken(arrow)` → ЯКЩО `custom: «відстані до першої фігури в різних позначених напрямках різні»` (`+cond:nearest_dist`) → ТО `set_state(clue, error)`.
- КОЛИ `constraint_broken(arrow)` → ЯКЩО `custom: «у непозначеному напрямку фігура ближча, ніж у позначених»` → ТО `set_state(clue, error)`.
- КОЛИ `all_constraints_met` → ТО `win`.
- Дедукція «рівна відстань»: дві протилежні стрілки — фігури на однаковій відстані з обох боків; непозначені напрямки до тієї ж відстані — вільні.
- Дедукція «зона заборони»: навколо кожної фігури рамка 8-сусідів порожня — це швидко ріже простір для решти банку.
- Перемога: усі фігури — з банку без повторів, не торкаються, усі стрілки правдиві. Поразки й рахунку нема.

## Керування і ввід
- puzz.link, play mode: ліва кнопка / drag — зафарбування клітинок; повторний клік — крапка або очищення (?).
- Edit mode: клік/drag ставить стрілки; курсор + цифри або Shift+стрілки — змінити набір напрямків як число 1–15 (тести `key,shift+left`).
- Цифрова версія: undo/redo, кнопка перевірки, що підсвічує першу помилку.

## Вікна, меню, HUD
- `game-screen`: сітка зі стрілками, банк фігур поруч, `conflict-highlight` після перевірки.
- puzz.link: перемикач play/edit, кнопка перевірки, `settings-window` (зокрема прозорість стрілок).
- `help-window` — правила жанру.
- Переходи: edit → play; check → повідомлення з текстом помилки.

## Фічі поза полем
- `auto-check` за кнопкою (тексти помилок pzprjs).
- `undo` / `redo`; `level-editor` + `share-code` (URL пазла з банком).
- `custom-rules`: «прозорі стрілки» (дозвіл зафарбовувати підказки) — налаштування puzz.link.
- Банк авторських пазлів (GM Puzzles — категорія Pentopia, 29 пазлів на сторінці; GMPQ Vol. 5).

## Варіації й родичі
- Підказки взято з Myopia (стрілки «що найближче»), розміщення — з пентаміно-жанрів; у сімʼї: [Statue Park](statue-park.md), [Pentominous](pentominous.md), [LITS](lits.md), [Star Battle](star-battle.md) (заборона дотику кутом).
- Grant Fikes «Single Vision» — лише однонапрямні стрілки; Bryce Herdt — лише двонапрямні (за видачею пошуку).
- **Осі варіацій**: усі фігури банку / частина · банк пентаміно / тетраміно / довільний · дотик кутом заборонено / дозволено · стрілки «найближча» / «рахує клітинки до фігури».

## Цікавинки для курсу
- Перевірка стрілки: промінь у 4 напрямки до першої зафарбованої клітинки + порівняння відстаней — 🌱.
- Нормалізація форми під 8 симетрій (повороти + дзеркала) і пошук у банку — 📎.
- Заборона дотику кутом через 8-сусідство між різними групами — 🌱.
- Редактор стрілок: набір напрямків як бітова маска 1–15 — 🌱.
- Розвʼязувач: перебір розміщень фігур банку з відсіканням за стрілками — 🥇.

## Мапа на каталог
- Є: `polyomino-placement` ↔ викладання пентаміно · `markup-validity`, `completion-detection`, `satisfy-constraints`, `conflict-highlight` · `cell-click`, `keyboard-controls` · `in-game-editor`, `level-bank`, `undo-redo`.
- **Нема** → пропозиції карток:
  - `+shape-bank` «Банк фігур поза полем, кожна до N разів» · entities/legality · 📎 · слот {uses: once|all}.
  - `+nearest-in-direction-clue` «Підказка-стрілка: найближчий обʼєкт у напрямку» · game-logic/constraints · 🌱.
  - `+multi-arrow-clue` «Кілька стрілок однієї підказки — рівні відстані, решта далі» · game-logic/constraints · 📎.
  - `+shape-identity-check` — повтор з LITS.

## Пропозиції до словників
- `+cond:nearest_dist(cell, dir, kind)` — відстань до першої сутності виду в напрямку (Pentopia, Myopia, Kuromasu-подібні промені).
- `+cond:touches8(a, b)` — дві групи торкаються хоча б кутом.
- `+ui:shape-bank` — панель фігур поруч із полем з позначкою «використано».
- `+card:shape-bank`, `+card:nearest-in-direction-clue`, `+card:multi-arrow-clue` — див. мапу.

## Джерела
- ⭐ [GM Puzzles: Pentopia Rules and Info](https://www.gmpuzzles.com/blog/?p=22920) — правила, автор Bram de Laat («Hybrids – LMI March 2011»), гібрид Myopia-підказок і пентаміно, варіант без вимоги «використати всі», 10×10–12×12.
- [puzz.link: pentopia.js](https://puzz.link/js/pzpr-samples/pentopia.js) — правила (банк, повороти/дзеркала, до 1 разу, без дотику, рівні відстані, непозначені напрямки далі), коди csOnArrow/arNoShade/bankInvalid/shDiag/bankGt/arDistanceGt/arDistanceNe, тести вводу.
- [pzprjs: failcode.en.json](https://raw.githubusercontent.com/robx/pzprjs/main/src/res/failcode.en.json) — тексти помилок.
- YouTube: пошук «pentopia puzzle».

## Непевне
- (?) Точна поведінка повторного кліку (крапка/очищення) у puzz.link — не бачив, лише тести зафарбування drag-ом.
- (?) Код `bankGt` у puzz.link — «фігура зустрічається забагато разів»; чи банк може задавати кратність >1 — не перевірено.
- (?) GMP формулює «повороти й дзеркала — та сама фігура», puzz.link — «можна повертати й віддзеркалювати»; зміст однаковий, але чи банк puzz.link буває не пентаміно (тетраміно тощо) — з тексту «shapes» лише припускаю.
- (?) Варіанти Fikes/Herdt — зі сніпетів пошуку, сторінок не відкривав.
