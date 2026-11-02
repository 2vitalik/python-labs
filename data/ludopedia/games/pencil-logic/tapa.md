---
title: Tapa (Тапа, T-Paint)
slug: tapa
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
year: 2007
platforms: [paper, web, mobile]
links:
  - {kind: other, url: "https://www.gmpuzzles.com/blog/tapa-rules-and-info/", best: true, note: "GMPuzzles: правила з прикладом, історія (Serkan Yürekli, IPST 2007, WPC 2009)"}
  - {kind: other, url: "https://wpcunofficial.miraheze.org/wiki/Tapa", note: "WPC-вікі: правила, «?» і «0», T-Paint → Tapa, 23 раунди WPC"}
  - {kind: other, url: "https://wpcunofficial.miraheze.org/wiki/List_of_Tapa_variants", note: "WPC-вікі: десятки варіантів (Pata, Tapa Islands, Hexa, Toroidal…)"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/tapa.js", note: "puzz.link: правила з «?», 4 коди помилок, тести вводу чисел"}
  - {kind: other, url: "https://puzz.link/rules.html?tapa", note: "puzz.link: сторінка правил (текст рендериться JS)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=tapa+puzzle+how+to+solve", note: "пошук; розвʼязання"}
stage: v1
coverage: 75
mechanics: [markup-validity, completion-detection, satisfy-constraints, cell-click, keyboard-controls, reachability-check, level-solver, unique-puzzle-generation, level-bank, import-open-formats, in-game-editor, +undo-redo, +cell-shade-toggle, +dot-mark, +no-2x2-check, +global-connectivity, +ring-run-clue]
proposes: ["+cond:ring_runs", "+ui:multi-number-clue", "+card:ring-run-clue", "+card:pattern-lookup-table"]
author: opus
date: 2026-11-02
---

# Tapa — числа в клітинці описують серії чорних у кільці з 8 сусідів

## Суть
Гравець зафарбовує клітинки так, щоб усі чорні утворили одну звʼязну «стіну» без квадратів 2×2. Підказки — клітинки з одним або кількома числами: це довжини серій зафарбованих клітинок серед 8 сусідів (по колу), у будь-якому порядку; різні серії розділені хоча б однією білою. Незвичне: **підказка-кільце** — Nonogram-подібний опис серій, але на замкненому циклі з 8 клітинок довкола числа, а не в рядку; одна клітинка несе кілька чисел.

## Поле і час
- Прямокутна сітка; клітинки: підказка (1–4 числа або «?») · порожня.
- Кільце підказки — 8 сусідів (ортогональні + діагональні) по колу; на краю/в куті поля кільце коротше і розірване (не замкнене).
- Звʼязність стіни й заборона 2×2 — ортогональне сусідство; дотик лише кутами не зʼєднує.
- Шари: підказки (незмінні) · стан клітинки: невідомо / зафарбовано / крапка.
- Час статичний; хід = зміна стану однієї клітинки.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітинка-підказка | static | мультимножина чисел {a, b, …} | не фарбується; серії чорних у її кільці = числа (порядок неважливий) |
| Число «0» | static | — | жодної чорної в кільці |
| «?» | static | — | будь-яке додатне число; самотній «?» може означати 0 |
| Кільце сусідів | zone | ≤ 8 клітинок по колу | серії рахуються циклічно (перехід через «шов» кільця) |
| Порожня клітинка | mark | стан unknown / shaded / dot | клік змінює стан |
| Зафарбована клітинка | mark | — | частина стіни |
| Стіна | zone | кількість компонент | усі чорні — одна 4-звʼязна компонента без 2×2 |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left_click, cell)` → ЯКЩО `cell(x, empty)` → ТО `mark(cell, shaded)`; повтор → `unmark(cell)` (?).
- КОЛИ `input(right_click, cell)` → ТО `mark(cell, dot)` (?).
- КОЛИ `constraint_broken(tapa_clue)` — ЯКЩО `not ring_runs(clue) == {a, b, …}` → ТО підказка підсвічена (puzz.link `ceTapaNe`).
- КОЛИ `pattern(block2x2)` — 4 чорні квадратом → ТО `constraint_broken(no_2x2)` (`cs2x2`).
- КОЛИ `constraint_broken(wall_connected)` — ЯКЩО `not connected(shaded)` → ТО конфлікт (`csDivide`).
- КОЛИ `constraint_broken(board_not_empty)` — нічого не зафарбовано → ТО конфлікт (`brNoShade`).
- КОЛИ `all_constraints_met` → ТО `win`.
- Обчислення `ring_runs`: обійти 8 сусідів за годинниковою стрілкою, розбити на серії чорних; якщо кільце повне і перша й остання клітинки чорні — це одна серія; клітинка поза полем = біла.
- Дедукції: «0» → усі сусіди білі; «8» → усе кільце чорне; сума чисел + мінімум розривів = довжина кільця → шаблон відомий з точністю до зсуву по колу («3 3» у центрі: 3+1+3+1), а на краю поля, де кільце розірване, — повністю («2 2» біля краю: 2+1+2 = 5); «1 1 1 1» у центрі — чорні лише в кутах або лише ортогональні (дві розбивки); три чорні кутиком → четверта клітинка квадрата біла; чорна, що могла б лишитись ізольованою, мусить мати вихід до решти стіни. Білі клітинки звʼязними бути не мусять.
- Перемога: усі підказки виконані, стіна звʼязна, нема 2×2. Поразки й рахунку нема.

## Керування і ввід
- puzz.link play: ліва — фарба, права — крапка, drag протягує (?).
- puzz.link edit: клітинка-підказка набирає **кілька чисел** з клавіатури послідовно (тести `tapa.js` на полях 5×1…9×1 перевіряють, які набори допустимі для кільця з 3 або 5 клітинок) (?); «?» — окремий символ.
- Undo/redo, Check (код першого порушення), Clear answer.
- Тач (цифрова версія): тап — цикл unknown → shaded → dot.

## Вікна, меню, HUD
- `game-screen`: сітка, підказки з 1–4 числами в компоновці всередині клітинки, `conflict-highlight` (неправильна підказка, 2×2, розірвана стіна).
- Кнопки: Check, Undo, Redo, Clear answer.
- `editor-window` — puzz.link edit mode: введення мультичисел, експорт URL.
- `help-window` — правила (GMPuzzles, приклад з розвʼязком).
- `puzzle-select` — книги «Tapa and Variations», банки сайтів (цифрова версія).
- `end-screen` — розвʼязано.

## Фічі поза полем
- `auto-check` за кнопкою; `undo`/`redo`.
- `level-editor` + `share-code` (puzz.link URL).
- `puzzle-bank` (IPST, Akil Oyunlari, змагання WPC/OAPC; на WPC — один із найчастіших жанрів, ≥ 23 класичних появи).
- Перевірка підказки в редакторі: не кожна мультимножина реалізовна в кільці (напр. «4 4» неможлива — потрібно ≥ 10 клітинок) — валідація введення (?).

## Варіації й родичі
- **Pata** — числа описують білі серії, а не чорні.
- **Tapa Islands** — гібрид з Nurikabe: біла область містить ≤ 1 підказку, цифра = розмір області.
- **Hexa Tapa** (гекс-сітка: кільце з 6), **Toroidal / Cylindrical Tapa** (поле-тор/циліндр).
- **Tapa Line** (заборона 4 чорних поспіль), **Tapa Trimino**, **Thermometer Tapa**, **Color Tapa** (3 кольори, змішування).
- **Easy as Tapa** — підказки треба спершу розставити; **Twilight Tapa** — підказка може бути чорною.
- Родичі: Nurikabe і LITS (звʼязна стіна без 2×2), Nonogram (серії в лінії), Minesweeper (кільце з 8 сусідів, але лише сума).
- **Осі варіацій**: що описує підказка (довжини серій / сума / білі серії) · форма кільця (8 / 6 гекс / 4) · топологія поля (площина / тор / циліндр) · додаткові заборони (2×2, серії в лінії).

## Цікавинки для курсу
- Обхід кільця 8 сусідів по колу з урахуванням краю поля — 🌱.
- Довжини циклічних серій і порівняння мультимножин — 📎 (головна пастка — серія через «шов» кільця).
- Таблиця шаблонів: усі 256 станів кільця → мультимножина серій; підказка = множина допустимих шаблонів — 🥉 (класичний трюк розвʼязувачів).
- Заборона 2×2 + звʼязність стіни — 🌱 + 📎 (спільний код із Nurikabe/LITS).
- Розвʼязувач: перетин допустимих шаблонів кожної підказки + звʼязність — 🥇.
- Генератор: випадкова звʼязна стіна без 2×2 → підказки в білих клітинках → прибирання до унікальності — 👑.

## Мапа на каталог
- Є: `markup-validity` ↔ коди помилок · `completion-detection`, `satisfy-constraints` · `cell-click` · `keyboard-controls` ↔ введення мультичисел · `reachability-check` ↔ звʼязність стіни · `level-solver`, `unique-puzzle-generation` · `level-bank` · `import-open-formats` · `in-game-editor`.
- Перевикористано: `+undo-redo`, `+cell-shade-toggle`, `+dot-mark`, `+no-2x2-check` (Nurikabe), `+global-connectivity`; родич `+run-length-clues` (Nonogram) — серії в лінії, тут у кільці.
- **Нема** → пропозиції карток:
  - `+ring-run-clue` «Підказка: довжини серій у кільці сусідів» · game-logic/constraints · 📎 · слот {ring: 8|6, counts: shaded|unshaded}.
  - `+pattern-lookup-table` «Передобчислена таблиця шаблонів сусідства» · game-logic/constraints · 🥉 — 256 станів → значення; корисно й для автотайлінгу.

## Пропозиції до словників
- `+cond:ring_runs` — мультимножина довжин серій чорних у кільці сусідів клітинки.
- `+ui:multi-number-clue` — кілька чисел в одній клітинці з автокомпоновкою (1–4 числа).
- `+card:ring-run-clue`, `+card:pattern-lookup-table` — див. мапу.

## Джерела
- ⭐ [GMPuzzles: Tapa Rules and Info](https://www.gmpuzzles.com/blog/tapa-rules-and-info/) — правила з прикладом, автор Serkan Yürekli, IPST 2007, Akil Oyunlari, WPC 2009 в Анталії.
- [WPC unofficial wiki: Tapa](https://wpcunofficial.miraheze.org/wiki/Tapa) — правила з «0» і «?», T-Paint → Tapa («Turkish Art Paint», OAPC 2009), раунди WPC 2015–2024.
- [WPC unofficial wiki: List of Tapa variants](https://wpcunofficial.miraheze.org/wiki/List_of_Tapa_variants) — Pata, Tapa Islands, Easy as Tapa, Twilight, Line, Trimino, Thermometer, Color Tapa тощо.
- [puzz.link tapa.js](https://puzz.link/js/pzpr-samples/tapa.js) — правила, коди `brNoShade`, `cs2x2`, `ceTapaNe`, `csDivide`, тести вводу.
- [puzz.link rules](https://puzz.link/rules.html?tapa) — сторінка правил (без JS порожня).
- YouTube: пошук «tapa puzzle how to solve».

## Непевне
- (?) Статті Wikipedia про Tapa нема (`Tapa_(puzzle)` — 404), тому ⭐ — GMPuzzles.
- (?) Що саме перевіряють тести вводу в `tapa.js` — бачив лише опис, не очікувані значення.
- (?) Валідація неможливих мультимножин у редакторах — логічно, але в конкретному плеєрі не бачив.
- (?) Hexa / Toroidal / Cylindrical — лише назви зі сторінки Tapa, правил не читав.
