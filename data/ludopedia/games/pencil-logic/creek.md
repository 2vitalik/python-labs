---
title: Creek (クリーク)
slug: creek
aka: [クリーク, Струмок, Крік]
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
  - {kind: other, url: "https://www.janko.at/Raetsel/Creek/index.htm", best: true, note: "Janko: правила DE/EN/JA з прикладом, ≈460 пазлів у браузері, варіанти Toroidal, Knapp daneben, Coded, Treasure Hunt"}
  - {kind: official, url: "https://www.nikoli.co.jp/ja/puzzles/creek/", note: "Nikoli (JA): 3 правила, приклад → проміжний стан → відповідь"}
  - {kind: play, url: "https://puzz.link/rules.html?creek", note: "puzz.link: правила EN/JA і вхід у плеєр/редактор (сторінка рендериться JS)"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/creek.js", note: "правила EN/JA, «first appeared in Puzzle Communication Nikoli vol. 110», приклад 6×6, тест-дошки й сценарії вводу"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/main/src/variety/creek.js", note: "код pzprjs: числа 0–4 на вершинах, лічба клітинок навколо вершини, checklist"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Creek+nikoli+puzzle", note: "пошук"}
stage: v1
coverage: 75
mechanics: [cell-click, dot-mark, neighbor-count-clue, connectivity-check, satisfy-constraints, markup-validity, completion-detection, conflict-highlight, keyboard-controls, in-game-editor, editor-window, import-open-formats, undo-redo, help-window, level-bank, fixture-level-tests, level-solver, +cell-shade-toggle, +vertex-clue, +wildcard-clue, +trial-mode]
proposes: ["+cond:count_in", "+card:vertex-clue"]
author: opus
date: 2026-11-19
---

# Creek — зафарбуй клітинки так, щоб число на кожному перехресті дорівнювало кількості чорних навколо нього, а білі лишились одним «струмком»

## Суть
На перетинах ліній сітки стоять кружечки з числами 0–4. Гравець зафарбовує клітинки так, щоб кожне число дорівнювало кількості чорних серед (до чотирьох) клітинок, що торкаються його перехрестя. Друге й останнє правило: усі білі клітинки утворюють одну ортогонально звʼязну область. Незвичне: підказка стоїть **на вершині**, а не в клітинці, тож кожна клітинка — під впливом до чотирьох підказок, а самі чорні нічим не обмежені.

## Поле і час
- Квадратна сітка; у Janko — від 9×9 до 19×19 і 18×10, найчастіше 10×10; приклад puzz.link — 6×6.
- Підказки — на вершинах, включно з краєм поля: вершина всередині торкається 4 клітинок, на краю — 2, у куті — 1 (puzz.link малює поле з запасом пів клітинки, щоб кружки на краю влізли).
- Шари: числа на вершинах (умова) · стан клітинки гравця: невідомо / чорна / крапка «біле».
- Час статичний; хід = змінити стан клітинки.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Кружечок з числом | static | N = 0…4, на вершині | рівно N чорних серед клітинок, що торкаються вершини |
| Кружечок «?» | static | — | вершина-підказка без числа, перевірок не додає |
| Клітинка | mark | невідомо / чорна / крапка | клік змінює стан |
| Біла область | zone | кількість компонент | усі білі — одна 4-звʼязна компонента |
| Чорні клітинки | mark | — | можуть стояти поруч і утворювати будь-які групи |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left_click, cell)` → ТО `mark(cell, shaded)`; повтор → `unmark(cell)` (схема puzz.link для зафарбовувань).
- КОЛИ `input(right_click, cell)` → ТО `mark(cell, dot)` — позначка «біле».
- КОЛИ `constraint_broken(no_shade)` → ЯКЩО `count(shaded, ==, 0)` → ТО `message(«There are no shaded cells on the board.»)` (код brNoShade).
- КОЛИ `constraint_broken(too_many)` → ЯКЩО `custom: «чорних серед клітинок навколо вершини > N»` (`+cond:count_in`) → ТО `set_state(clue, error)`, `message(«The number of shaded cells overlapping a number is too high.»)` (crShadeGt).
- КОЛИ `constraint_broken(white_divided)` → ЯКЩО `not connected(white)` → ТО `set_state(white_component, error)`, `message(«The unshaded cells are divided.»)` (cuDivide).
- КОЛИ `constraint_broken(too_few)` → ЯКЩО `custom: «чорних навколо вершини < N»` (`+cond:count_in`) → ТО `set_state(clue, error)`, `message(«The number of shaded cells overlapping a number is too low.»)` (crShadeLt).
- КОЛИ `all_constraints_met` → ТО `win`.
- Порядок перевірок puzz.link: є хоч одна чорна → не забагато → білі звʼязні → не замало → усі клітинки визначені (лише статус «не завершено», без помилки).
- Перемога: кожне число дорівнює кількості чорних навколо своєї вершини, білі — одна звʼязна область. · Поразки й рахунку нема.
- Наслідки правил (дедукції): «4» — усі чотири клітинки чорні; «0» — усі білі; «1» у куті поля — кутова клітинка чорна; «2» на краю — обидві клітинки чорні; біла клітинка не може опинитися замкненою чорними (якщо білих більше однієї).

## Керування і ввід
- puzz.link play: ліва кнопка з протяжкою — фарба, права — крапка «біле»; режими `shade` / `unshade`.
- puzz.link edit: курсор ходить по вершинах; цифри 0–4 і `-` («?») з клавіатури; клік мишею по вершині перебирає значення «? → 0 → 1 → 2 → 3 → 4», права кнопка — у зворотний бік (тест вводу); режим `clear`.
- Janko: інтерактивна сітка — клік фарбує сірі клітинки в чорний або білий.
- Папір: числа в кружечках на перетинах ліній, чорнити олівцем.

## Вікна, меню, HUD
- `game-screen` (puzz.link): сітка з полем навколо, кружечки з числами на вершинах, темно-сірі чорні клітинки, крапки; кнопки Check · Undo · Redo · Erase answer · Erase marks · Trial (оболонка — [puzz.link](puzz-link.md)); `conflict-highlight` — вершина з хибним числом, розірвані білі.
- `editor-window` — той самий екран у режимі Edit: number · clear, вивід URL.
- `help-window` — rules.html?creek; Nikoli — 例題 / 途中経過 / 答え (приклад, проміжний стан, відповідь).
- `puzzle-select` (Janko) — ≈460 пазлів, сортування за датою, розміром і складністю.
- Переходи: Janko список → пазл → перевірка; puzz.link rules → плеєр за URL → Check → «розвʼязано» або перша помилка.

## Фічі поза полем
- `auto-check` і Check з текстом першої помилки; `undo` ∞ / `redo`; `+feature:trial-mode` (puzz.link).
- `level-editor` + `share-code` (URL `p?creek/6/6/…`; код читає і новий, і старий формат URL), файли pzprv3.
- `puzzle-bank`: Janko — ≈460 пазлів від різних авторів; журнал Nikoli.
- Нема генератора, підказок, рекордів.

## Варіації й родичі
- Варіанти Janko: Toroidal — поле-тор, краї зшиті; Knapp daneben — кожне число хибне рівно на ±1; Cipher / Coded — числа замінено літерами (однакові літери — однакові числа); Treasure Hunt (Palmer Mebane) — в одній клітинці захований скарб, місце не дано.
- [Slant](slant.md), [Kuralin](kuralin.md) — теж підказки на вершинах (`+vertex-clue`): у Slant число — скільки діагоналей сходиться у вершині.
- [Fill-a-Pix](fill-a-pix.md) — та сама лічба чорних, але квадрат 3×3 з центром у клітинці; [Tapa](tapa.md) — серії чорних у кільці з 8 сусідів.
- [Heyawake](heyawake.md), [Hitori](hitori.md), [Kuromasu](kuromasu.md) — теж «усі білі звʼязні».
- Janko називає схожими Tasukuea, Kurotto, Lampions, Spotlight.
- **Осі варіацій**: де стоїть підказка (клітинка — Fill-a-Pix / вершина — Creek) · окіл (2×2 навколо вершини / 3×3 / кільце) · глобальна умова (білі звʼязні / чорні звʼязні / нема) · правдивість чисел (точні / ±1 — Knapp daneben) · топологія (площина / тор).

## Цікавинки для курсу
- Відображення «вершина ↔ до 4 клітинок» (вершин (W+1)×(H+1); на краю 2, у куті 1) — 🌱.
- Лічба чорних навколо вершини з окремими кодами «забагато» й «замало» — 🌱.
- Звʼязність білих: BFS чи union-find — 📎 (картка `connectivity-check`).
- Швидка перевірка «чи не відріже ця чорна білих» — точки зчленування в графі білих — 🥈.
- Розвʼязувач: локальні виводи (0, 4, кути, краї) + пошук із відсіканням за звʼязністю — 🥇.
- Варіанти як перемикачі: тор (зшиті краї для лічби й звʼязності), числа ±1 — 📎 кожен.

## Мапа на каталог
- Є: `cell-click`, `dot-mark` ↔ фарба / крапка · `neighbor-count-clue` ↔ число = кількість чорних серед клітинок навколо вершини · `connectivity-check` ↔ білі звʼязні · `satisfy-constraints`, `markup-validity`, `completion-detection`, `conflict-highlight` ↔ Check з кодами · `keyboard-controls`, `in-game-editor`, `editor-window`, `import-open-formats` ↔ редактор і URL · `undo-redo` · `help-window` · `level-bank` ↔ Janko · `fixture-level-tests` ↔ тест-дошки на кожен код · `level-solver`.
- Перевикористано: `+cell-shade-toggle` · `+vertex-clue` (Slant, Kuralin) · `+wildcard-clue` («?») · `+trial-mode`.
- **Нема** → нових карток не треба.

## Пропозиції до словників
- `+cond:count_in` — повтор: кількість чорних серед клітинок, що торкаються вершини.
- `+card:vertex-clue` — повтор (Slant): підказки на вершинах сітки.

## Джерела
- ⭐ [Janko: Creek](https://www.janko.at/Raetsel/Creek/index.htm) — правила («A number in a circle indicates how many of the 4 adjacent cells must be blackened», «All white cells must form a single orthogonally-connected area»), ≈460 пазлів, варіанти, схожі жанри, назва — «струмок».
- [Nikoli: クリーク](https://www.nikoli.co.jp/ja/puzzles/creek/) — офіційні правила («数字がまたがる最大４マス» — до 4 клітинок, на яких стоїть число), приклад і відповідь.
- [puzz.link: Creek](https://puzz.link/rules.html?creek) — правила й плеєр (рендериться JS).
- [pzpr-samples/creek.js](https://puzz.link/js/pzpr-samples/creek.js) — правила EN/JA, «Puzzle Communication Nikoli vol. 110», тести brNoShade · crShadeGt · cuDivide · crShadeLt, сценарії вводу чисел з клавіатури й мишею.
- [pzprjs creek.js](https://raw.githubusercontent.com/robx/pzprjs/main/src/variety/creek.js) — `Cross: maxnum 4, minnum 0`, `checkQnumCross` (лічба `cellinside` навколо вершини), checklist.
- [JA-Вікіпедія: パズル通信ニコリ](https://ja.wikipedia.org/wiki/パズル通信ニコリ) — дати випусків журналу (для оцінки року).
- YouTube: [пошук «Creek nikoli puzzle»](https://www.youtube.com/results?search_query=Creek+nikoli+puzzle).

## Непевне
- (?) Рік: Nikoli vol.110 (puzz.link); за JA-Вікі vol.113 вийшов 10.12.2005 при щоквартальному виході, тож vol.110 ≈ березень 2005; прямої дати не бачив, `year: null`. Автор жанру невідомий (Janko лишив поле порожнім).
- (?) Правила Treasure Hunt (Palmer Mebane, №405 у Janko) — бачив лише перше речення.
- (?) Перевірка «усі клітинки визначені» у puzz.link лише ставить статус «не завершено» — імовірно, для режиму автоперевірки guarded.
- (?) Дії мишею в play — загальна схема pzpr для зафарбовувань (`use`); у тестах жанру — лише ввід чисел.
