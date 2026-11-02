---
title: LITS (Nuruomino)
slug: lits
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
year: 2004
platforms: [paper, web, mobile]
links:
  - {kind: official, url: "https://www.nikoli.co.jp/en/puzzles/lits/", best: true, note: "Nikoli: 4 правила, Sample → Progressing → Solution, історія назви"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/LITS", note: "правила, Nuruomino → LITS, NP-повнота (Biro, Schmidt 2017)"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/lits.js", note: "puzz.link: правила, 7 кодів помилок, тест вводу меж регіонів"}
  - {kind: other, url: "https://puzz.link/rules.html?lits", note: "puzz.link: сторінка правил (текст рендериться JS)"}
  - {kind: other, url: "https://wpcunofficial.miraheze.org/wiki/LITS", note: "WPC-вікі: автор Naoki Inaba, LITS+, Inverse LITSO, раунди WPC"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=LITS+puzzle+how+to+solve", note: "пошук; розвʼязання"}
stage: v1
coverage: 75
mechanics: [markup-validity, completion-detection, satisfy-constraints, cell-click, reachability-check, level-solver, unique-puzzle-generation, level-bank, import-open-formats, in-game-editor, +undo-redo, +cell-shade-toggle, +dot-mark, +region-quota, +no-2x2-check, +global-connectivity, +irregular-regions, +shape-identity-check]
proposes: ["+cond:same_shape", "+trigger:pattern(same_shape_touch)", "+card:shape-identity-check", "+card:region-polyomino-shading"]
author: opus
date: 2026-11-02
---

# LITS — у кожному регіоні тетроміно; однакові не торкаються, усі разом — одна «стіна» без квадратів 2×2

## Суть
Сітка поділена на регіони (поліоміно з ≥ 4 клітинок). Гравець зафарбовує в кожному регіоні рівно 4 звʼязні клітинки — тетроміно. Усі зафарбовані разом утворюють одну звʼязну «стіну» без квадратів 2×2 (як у Nurikabe), а два **однакові** тетроміно (з урахуванням поворотів і відбиттів) не можуть торкатися стороною через межу регіонів. Незвичне: обмеження на **тотожність форм** — клітинки порівнюються не за значенням, а за геометричним класом фігури, якої вони частина. Квадрат O неможливий через заборону 2×2, звідси назва — чотири літери L, I, T, S.

## Поле і час
- Прямокутна сітка (типово 10×10), поділена товстими межами на регіони довільної форми; у WPC-версіях бувають клітинки «X» поза регіонами.
- Сусідство ортогональне для звʼязності, для дотику фігур і всередині тетроміно; дотик кутами між однаковими фігурами дозволено.
- Шари: межі регіонів (незмінні) · стан клітинки: невідомо / зафарбовано / крапка.
- Час статичний; хід = зміна стану однієї клітинки.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Регіон | zone | поліоміно, ≥ 4 клітинки | містить рівно 4 зафарбовані, звʼязні між собою |
| Клітинка | mark | стан unknown / shaded / dot | клік змінює стан |
| Зафарбована клітинка | mark | — | частина тетроміно свого регіону і загальної «стіни» |
| Тетроміно | zone | форма L / I / T / S (O неможлива) | похідна сутність: 4 зафарбовані клітинки регіону; форма — клас за поворотами й відбиттями |
| Межа регіонів | static | ребро сітки | через неї однакові тетроміно не можуть сусідити |
| Стіна | zone | кількість компонент | усі зафарбовані — одна 4-звʼязна компонента |
| Клітинка X (WPC) | static | — | не належить жодному регіону, не фарбується (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left_click, cell)` → ТО `mark(cell, shaded)`; повтор → `unmark(cell)` (?).
- КОЛИ `input(right_click, cell)` → ТО `mark(cell, dot)` (?).
- КОЛИ `constraint_broken(region_count)` — ЯКЩО `count(shaded in region, >, 4)` → ТО конфлікт (`bkShadeGt4`); `< 4` — `bkShadeLt4`; `== 0` — `bkNoShade`.
- КОЛИ `constraint_broken(tetromino_connected)` — ЯКЩО `not connected(shaded in region)` → ТО конфлікт (`bkShadeDivide`).
- КОЛИ `pattern(block2x2)` — 4 зафарбовані квадратом → ТО `constraint_broken(no_2x2)` (`cs2x2`).
- КОЛИ `pattern(same_shape_touch)` — ЯКЩО `adjacent(t1, t2) and same(t1, t2, shape)` (форма з точністю до поворотів і відбиттів) → ТО обидва підсвічені (`bsSameShape`).
- КОЛИ `constraint_broken(wall_connected)` — ЯКЩО `not connected(shaded)` → ТО конфлікт (`csDivide`).
- КОЛИ `all_constraints_met` → ТО `win`.
- Дедукції: регіон рівно з 4 клітинок зафарбований цілком; клітинки, що не входять у жодне розміщення тетроміно в регіоні, — білі; спільні для всіх розміщень — чорні; якщо всі розміщення регіону — I, сусідній регіон не може бути I на тій самій межі; три зафарбовані кутиком → четверта клітинка квадрата біла.
- Не всі 4 форми мусять зʼявитись (WPC-вікі).
- Перемога: 4 звʼязні клітинки в кожному регіоні, стіна звʼязна, нема 2×2, однакові не торкаються. Поразки й рахунку нема.

## Керування і ввід
- puzz.link play: ліва — фарба, права — крапка, drag протягує (?).
- puzz.link edit: межі регіонів — drag лівою по вузлах сітки; повторне протягування тим самим шляхом прибирає межу (з тестів `lits.js`: двічі той самий ввід → порожня розмітка).
- Undo/redo, Check (код першого порушення), Clear answer.

## Вікна, меню, HUD
- `game-screen`: сітка з товстими межами регіонів + `conflict-highlight` (регіон з ≠ 4, розірване тетроміно, квадрат 2×2, пара однакових фігур).
- Кнопки: Check, Undo, Redo, Clear answer.
- `editor-window` — puzz.link edit mode: малювання меж, експорт URL.
- `help-window` — правила (Nikoli: Sample / Progressing / Solution).
- `puzzle-select` — книги Nikoli (перша книга LITS — листопад 2007), банки сайтів (цифрова версія).
- `end-screen` — розвʼязано.

## Фічі поза полем
- `auto-check` за кнопкою; `undo`/`redo`.
- `level-editor` + `share-code` (puzz.link URL / pzprv3 — регіони кодуються як матриця id).
- `puzzle-bank` (Nikoli, змагання WPC 2014–2023).
- Корисна HUD-фіча цифрової версії: розфарбувати кожне завершене тетроміно кольором його форми (L/I/T/S) — однакові сусіди видно одразу (?).

## Варіації й родичі
- **LITS+** (Robert Vollmert, 2014): регіон або порожній, або тетроміно; заборонено 2×2 і чорних, і білих.
- **Inverse LITSO** (Bram de Laat, 2012): у кожному регіоні 4 **білі** клітинки утворюють L/I/T/S/O; решта чорних звʼязна без 2×2.
- Inverted LITS (WPC 2014) (?).
- Родичі: Nurikabe (звʼязна стіна без 2×2), Statue Park, Norinori (доміно в регіонах) (?), Tetris/Blokus (форми тетроміно).
- **Осі варіацій**: розмір фігури (доміно / тріміно / тетроміно / пентаміно) · що зафарбовано (фігура / доповнення) · заборона дотику (однакові форми / будь-які) · звʼязність (чорні / обидва) · 2×2 (лише чорні / обидва кольори).

## Цікавинки для курсу
- Квота 4 клітинки на регіон + звʼязність усередині — 🌱.
- Розпізнавання форми тетроміно: нормалізувати координати, перебрати 8 симетрій (D4), взяти мінімальний ключ — 📎; знадобиться і в Tetris/Blokus.
- Заборона однакових сусідів: побудувати граф регіонів (сусідні клітинки через межу) і порівняти ключі форм — 📎.
- Заборона 2×2 + глобальна звʼязність — 🌱 + 📎 (той самий код, що в Nurikabe/Tapa).
- Розвʼязувач: перелік усіх розміщень тетроміно в кожному регіоні + поширення обмежень (перетин/обʼєднання розміщень) — 🥇; це майже exact-cover.
- Генератор з унікальним розвʼязком (NP-повна задача, Biro, Schmidt 2017) — 👑.

## Мапа на каталог
- Є: `markup-validity` ↔ коди помилок · `completion-detection`, `satisfy-constraints` · `cell-click` · `reachability-check` ↔ звʼязність стіни · `level-solver`, `unique-puzzle-generation` · `level-bank` · `import-open-formats` ↔ puzz.link URL · `in-game-editor` ↔ edit mode.
- Перевикористано: `+undo-redo`, `+cell-shade-toggle`, `+dot-mark`, `+region-quota` (n = 4), `+no-2x2-check` (Nurikabe), `+global-connectivity`, `+irregular-regions` (sudoku-variants).
- **Нема** → пропозиції карток:
  - `+shape-identity-check` «Канонічна форма поліоміно; однакові не сусідять» · game-logic/constraints · 📎 · слот {symmetry: rot|rot+mirror, scope: across-borders}.
  - `+region-polyomino-shading` «У кожному регіоні — звʼязна фігура заданого розміру» · game-logic/constraints · 🌱 · слот {size: 4}.

## Пропозиції до словників
- `+cond:same_shape` — дві групи клітинок мають однакову форму з точністю до поворотів/відбиттів (уточнення `same(a, b, prop)` для поліоміно; родич `fits(shape, cells)`).
- `+trigger:pattern(same_shape_touch)` — значення для `pattern(shape)`: однакові фігури торкаються стороною.
- `+card:shape-identity-check`, `+card:region-polyomino-shading` — див. мапу.

## Джерела
- ⭐ [Nikoli: LITS](https://www.nikoli.co.jp/en/puzzles/lits/) — 4 правила, приклад, історія назви, перша книга (листопад 2007).
- [Wikipedia: LITS](https://en.wikipedia.org/wiki/LITS) — правила, Nuruomino → LITS (№112), NP-повнота.
- [puzz.link lits.js](https://puzz.link/js/pzpr-samples/lits.js) — правила, історія vol. 104, коди `cs2x2`, `bkShadeGt4`, `bkShadeDivide`, `bsSameShape`, `csDivide`, `bkNoShade`, `bkShadeLt4`, тест вводу меж.
- [puzz.link rules](https://puzz.link/rules.html?lits) — сторінка правил (без JS порожня).
- [WPC unofficial wiki: LITS](https://wpcunofficial.miraheze.org/wiki/LITS) — автор, LITS+, Inverse LITSO, раунди WPC.
- YouTube: пошук «LITS puzzle how to solve».

## Непевне
- (?) Перша публікація: puzz.link і WPC-вікі — Nikoli vol. 104 (2004), Wikipedia — №106; Nikoli EN згадує «Puzzle Cyclopedia».
- (?) Автор Naoki Inaba — лише WPC-вікі.
- (?) Дії мишею в режимі play у puzz.link — тестів play-вводу нема; схему взято з інших зафарбовувань.
- (?) Норінорі як родич і Inverted LITS — з памʼяті / лише назва.
- (?) Підсвічування форм кольорами — ідея, не бачена в конкретному плеєрі.
