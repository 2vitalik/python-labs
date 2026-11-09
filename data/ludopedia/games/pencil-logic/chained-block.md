---
title: Chained Block
slug: chained-block
aka: [チェンブロ, Chenburo, Chained Blocks, chainedb]
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
  - {kind: other, url: "https://www.nikoli.co.jp/en/puzzles/chained-block/", best: true, note: "Nikoli: правила EN, приклад, хід розвʼязання і відповідь картинками"}
  - {kind: other, url: "https://www.nikoli.co.jp/ja/puzzles/chained-block/", note: "Nikoli JA: правила チェンブロ"}
  - {kind: play, url: "https://puzz.link/rules.html?chainedb", note: "puzz.link: правила й плеєр (сторінка рендериться JS)"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/chainedb.js", note: "правила EN/JA, «Nikoli vol. 173», коди помилок"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/master/src/variety/chainedb.js", note: "pzprjs: блоки, ланцюги через 8-сусідство, чек-лист; там же Mirroring Tile і Archipelago"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/master/src/res/failcode.en.json", note: "тексти помилок bkNoChain.chainedb, bsSameShape.chainedb"}
  - {kind: other, url: "https://www.janko.at/Raetsel/Chained-Blocks/index.htm", note: "Janko: правила DE/EN, 80 пазлів, родинні жанри"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=chained+block+nikoli+puzzle", note: "пошук; розвʼязання"}
stage: v1
coverage: 60
mechanics: [markup-validity, completion-detection, satisfy-constraints, conflict-highlight, selection-highlight, cell-click, dot-mark, undo-redo, in-game-editor, import-open-formats, level-bank, +cell-shade-toggle, +one-clue-per-region, +region-size-check, +shape-identity-check, +diagonal-chain, +chain-unique-shapes]
proposes: ["+cond:region_has(block, clue, n)", "+cond:diag_touch(a, b)", "+card:diagonal-chain", "+card:chain-unique-shapes"]
author: opus
date: 2026-11-09
---

# Chained Block — зафарбуй блоки за числами так, щоб блоки, що торкаються кутами, складали ланцюги без двох однакових форм

## Суть
Гравець зафарбовує клітинки. Орто-звʼязна група чорних — «блок»; у кожному блоці рівно одна підказка: число (розмір блоку) або «?» (розмір невідомий). Блоки, що торкаються кутами, утворюють «ланцюг»; самотніх блоків бути не може, а в одному ланцюгу не може бути двох блоків однакового розміру й форми (повороти й дзеркала — та сама форма). Незвичне: обмеження живе на рівні графа «блок—блок через кут», а не клітинок.

## Поле і час
- Прямокутна сітка без регіонів; підказки — числа й «?» у клітинках.
- Два рівні сусідства: блок — по ребру (4-сусідство); ланцюг — компонента блоків, звʼязаних дотиком кутом (8-сусідство клітинок).
- Шари: підказки (незмінні) · зафарбовані клітинки · крапки «біле» гравця.
- Час статичний; хід = зафарбувати / позначити клітинку. Пазли авторські (`random: none`).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітинка | terrain | — | біла або чорна |
| Число | mark | N ≥ 1 | клітинка завжди чорна; її блок має рівно N клітинок |
| «?» | mark | — | клітинка чорна; блок має підказку, розмір довільний |
| Блок | zone | клітинки, форма | орто-звʼязна група чорних; рівно одна підказка |
| Ланцюг | zone | множина блоків | ≥ 2 блоки, звʼязані дотиком кутами; усі форми різні |
| Крапка | mark | — | нотатка «тут біле», не перевіряється |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left_click, cell)` → ЯКЩО `not occupied(cell, clue)` → ТО `paint(cell, black)`; повтор — `unmark(cell)` (цифрова версія, (?)).
- КОЛИ `input(right_click, cell)` → ТО `mark(cell, dot)` (цифрова версія, (?)).
- КОЛИ `input(unshade, clue_cell)` → ЯКЩО `occupied(cell, clue)` → ТО `block` — клітинку з підказкою не можна зробити білою (pzprjs).
- КОЛИ `input(info_blk, cell)` → ЯКЩО `mode(info-blk)` → ТО `custom: «підсвітити весь ланцюг, що містить цю чорну клітинку»`.
- КОЛИ `constraint_broken(multiple_numbers)` → ЯКЩО `custom: «у блоці дві або більше підказок»` → ТО `message(«A block has multiple numbers»)` · `flash(block)` — bkNumGe2.
- КОЛИ `constraint_broken(same_shape)` → ЯКЩО `same(block_a, block_b, shape)` і `custom: «обидва блоки в одному ланцюгу; повороти й дзеркала не розрізняються»` → ТО `message(«A chain contains two identical blocks»)` · `flash(block_a)` — bsSameShape.
- КОЛИ `constraint_broken(no_number)` → ЯКЩО `custom: «у блоці нема ні числа, ні «?»»` → ТО `message(«A block has no number»)` · `flash(block)` — bkNoNum.
- КОЛИ `constraint_broken(size)` → ЯКЩО `not region_size(block, N)` → ТО `message(«The size of the block is not equal to the number»)` · `flash(block)` — bkSizeNe.
- КОЛИ `constraint_broken(no_chain)` → ЯКЩО `custom: «блок не торкається кутом жодного іншого блоку»` → ТО `message(«A block is not diagonally adjacent to another block»)` · `flash(block)` — bkNoChain.
- КОЛИ `all_constraints_met` → ТО `win`.
- Порядок перевірок у pzprjs: bkNumGe2 → bsSameShape → bkNoNum → bkSizeNe → bkNoChain; показується перша знайдена помилка.
- Блоки не можуть торкатись ребром за визначенням: дві чорні клітинки поруч по ребру — це вже один блок.
- Перемога: кожен блок з однією підказкою й правильним розміром, кожен блок у ланцюгу, у ланцюгах нема двох однакових форм. Поразки й рахунку нема.
- Дедукція «дві підказки поруч»: клітинка між двома підказками в одному ряду, що злила б їхні блоки, — біла; дві підказки поруч по ребру в коректному пазлі неможливі.
- Дедукція «одиничка»: блок 1 — одна клітинка, чотири орто-сусіди білі, і хоч один діагональний сусід мусить бути чорним.
- Дедукція «ліміт форм»: у ланцюгу щонайбільше 1 блок розміру 1, 1 — розміру 2, 2 — розміру 3, 5 — розміру 4 (вільні поліоміно); тому два блоки «1» чи «2», що торкаються кутом, неможливі.

## Керування і ввід
- Папір: зафарбувати клітинки блоків, крапками позначати білі.
- puzz.link (play): режими shade / unshade та info-blk (клік підсвічує цілий ланцюг); клік по клітинці за замовчуванням малює (autoplay cell); undo/redo (?).
- puzz.link (edit): режими number (число, клітинка одразу стає чорною), «?», clear (прибрати підказку й зафарбування).

## Вікна, меню, HUD
- `game-screen` (цифрова версія): сітка, числа й «?», чорні клітинки, крапки; `check-button`, `undo-button`, `redo-button`; `conflict-highlight` — блок із помилкою підсвічується разом з текстом помилки.
- `selection-highlight` — режим info-blk: підсвітка ланцюга під курсором.
- `editor-window` (puzz.link edit): розмір, числа, «?», експорт у URL.
- `help-window` — правила (Nikoli з покроковими картинками, puzz.link, Janko).
- `puzzle-select` (Janko): 80 пазлів за номером, розміром, складністю.
- Переходи: список Janko → пазл → `game-screen` → перевірка.

## Фічі поза полем
- `auto-check` за кнопкою (puzz.link); `undo` / `redo`.
- `level-editor` + `share-code` (URL пазла puzz.link, формат pzprv3).
- `puzzle-bank` — Janko: 80 пазлів (5×5 … 18×18 і кілька великих); Nikoli — приклад із розвʼязанням.

## Варіації й родичі
- У тому самому модулі pzprjs: **Mirroring Tile** (ミラーリングタイル, Nikoli vol. 172) — дзеркальне правило: кожна «плитка» мусить торкатися кутом плитки тієї самої форми; **Archipelago** (アーキペラゴ) — ланцюг порівнює розміри, а не форми.
- Janko відносить до однієї родини Akiperago, Chiyotsui, Choco Banana, Chocona, Cocktail-Lampe, Norinori, Norinuri, Tetrochain.
- У корпусі: [LITS](lits.md) (однакові тетраміно не торкаються), [Statue Park](statue-park.md) (банк форм, кожна раз), [Double Choco](double-choco.md) (конгруентні половини), [Hinge](hinge.md), [Nurikabe](nurikabe.md) (число = розмір області).
- **Осі варіацій**: звʼязок блоків (кутом / ребром) · умова в ланцюгу (усі форми різні / кожна має двійника — Mirroring Tile / різні розміри — Archipelago) · підказки (розмір / «?» / дані чорні клітинки) · обовʼязковість ланцюга (так / ні).

## Цікавинки для курсу
- Два рівні компонент: блоки BFS по 4-сусідству, ланцюги — BFS по 8-сусідству поверх блоків — 🌱.
- Канонічна форма поліоміно (8 симетрій, зсув у нуль) і пошук дубля в ланцюгу — 📎.
- Підсвітка всього ланцюга за кліком — 🌱.
- Покрокова перевірка з першою помилкою і текстом (чек-лист pzprjs) — 📎.
- Розвʼязувач: розстановка блоків з бектрекінгом і відсіканням за лімітом форм — 🥈.
- Генератор з єдиним розвʼязком — 👑.

## Мапа на каталог
- Є: `markup-validity`, `completion-detection`, `satisfy-constraints` · `conflict-highlight` ↔ блок з помилкою · `selection-highlight` ↔ info-blk · `cell-click`, `dot-mark` · `undo-redo` · `in-game-editor`, `import-open-formats` ↔ редактор і URL puzz.link · `level-bank` ↔ Janko.
- **Нема** → пропозиції карток:
  - `+cell-shade-toggle`, `+one-clue-per-region`, `+region-size-check`, `+shape-identity-check` — уже пропоновані в корпусі.
  - `+diagonal-chain` «Групи, що торкаються кутом, утворюють ланцюг; самотня група — помилка» · game-logic/constraints · 🌱.
  - `+chain-unique-shapes` «У ланцюгу всі форми різні з точністю до поворотів і дзеркал» · game-logic/constraints · 📎.

## Пропозиції до словників
- `+cond:region_has(block, clue, n)` — у блоці/регіоні рівно N обʼєктів виду (повтор із корпусу).
- `+cond:diag_touch(a, b)` — дві групи мають спільну вершину клітинок, але не ребро.
- `+card:diagonal-chain`, `+card:chain-unique-shapes` — див. мапу.

## Джерела
- ⭐ [Nikoli: Chained Block](https://www.nikoli.co.jp/en/puzzles/chained-block/) — правила (блок, «?», ланцюг, однакові форми з поворотами й дзеркалами), приклад, хід розвʼязання і відповідь.
- [Nikoli JA: チェンブロ](https://www.nikoli.co.jp/ja/puzzles/chained-block/) — ті самі 5 правил японською.
- [puzz.link chainedb.js](https://puzz.link/js/pzpr-samples/chainedb.js) — правила EN/JA, «Puzzle Communication Nikoli vol. 173», коди bkNumGe2 / bkNoNum / bkSizeNe / bkNoChain / bsSameShape.
- [pzprjs chainedb.js](https://raw.githubusercontent.com/robx/pzprjs/master/src/variety/chainedb.js) — режими вводу, AreaShadeGraph / AreaShade8Graph, порядок перевірок, Mirroring Tile й Archipelago.
- [pzprjs failcode.en.json](https://raw.githubusercontent.com/robx/pzprjs/master/src/res/failcode.en.json) — тексти помилок.
- [Janko: Chained Blocks](https://www.janko.at/Raetsel/Chained-Blocks/index.htm) — правила DE/EN, назва Chenburo, 80 пазлів, родинні жанри.
- [puzz.link: Chained Block](https://puzz.link/rules.html?chainedb) — сторінка правил і плеєр (JS).

## Непевне
- (?) Рік першої публікації: відомо лише «Nikoli vol. 173»; дату номера не знайшов.
- (?) Розкладка кнопок миші в puzz.link (лівий — чорне, правий — крапка) — загальна поведінка pzpr, не перевірена для цього жанру.
- (?) Правила Archipelago прочитані лише з коду (сумісні розміри в ланцюгу, найбільший блок не більший за кількість блоків); сторінки правил не знайшов.
- (?) Дедукції «дві підказки поруч» і «ліміт форм» — загальна логіка, не з джерела.
