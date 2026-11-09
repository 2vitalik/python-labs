---
title: Fill-a-Pix (Mosaic)
slug: fill-a-pix
aka: [Mosaic, Nurie-Puzzle, ArtMosaico, Magipic, Mosaico, Fill-a-Pix Minesweeper, Мозаїка]
family: pencil-logic
also: [hidden-deduction]
klass: puzzle
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: setup
  goal: constraints
year: 2003
platforms: [paper, web, mobile, PC]
links:
  - {kind: official, url: "https://www.conceptispuzzles.com/index.aspx?uri=puzzle/fill-a-pix", best: true, note: "Conceptis: що це, розміри 10×10…35×35 і Mega 100×65, Basic/Advanced, інтерактив"}
  - {kind: official, url: "https://www.conceptispuzzles.com/index.aspx?uri=puzzle/fill-a-pix/rules", note: "правила: число = зафарбовані в 3×3 разом із клітинкою підказки; Basic проти Advanced"}
  - {kind: official, url: "https://www.conceptispuzzles.com/index.aspx?uri=puzzle/fill-a-pix/history", note: "історія: Trevor Truran, Game of Life, анонс Conceptis 02.2003, Nurie-Puzzle (G-mode, NTT DoCoMo)"}
  - {kind: official, url: "https://www.conceptispuzzles.com/index.aspx?uri=puzzle/fill-a-pix/techniques", note: "техніки розвʼязання"}
  - {kind: official, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/mosaic.html", note: "Tatham Mosaic: правила, миша/клавіатура, Custom з Aggressive generation, інші назви"}
  - {kind: play, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/mosaic.html", note: "Tatham Mosaic у браузері, нескінченна генерація"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=fill-a-pix+puzzle", note: "пошук; розвʼязання"}
stage: v1
coverage: 80
mechanics: [satisfy-constraints, markup-validity, completion-detection, conflict-highlight, cell-click, keyboard-controls, neighbor-count-clue, dot-mark, unique-puzzle-generation, no-guess-generation, difficulty-levels, difficulty-rating, field-size-picker, level-bank, undo-redo, seed-share, +picture-reveal, +cell-shade-toggle, +self-inclusive-neighborhood, +drag-paint-line, +clue-done-mark]
proposes: ["+cond:count_in_area", "+card:self-inclusive-neighborhood"]
author: opus
date: 2026-11-09
---

# Fill-a-Pix — зафарбуй клітинки так, щоб кожне число дорівнювало кількості чорних у його квадраті 3×3, і проявиться малюнок

## Суть
Сітка з числами 0–9 у частині клітинок. Число каже, скільки клітинок зафарбовано в квадраті 3×3 з центром у ньому — **разом із самою клітинкою підказки**. Гравець фарбує й позначає «точно біле», доки не проявиться піксельний малюнок. Це «сапер без ризику»: та сама лічба сусідів, але все поле видно, і помилка не вибухає; від нонограми — малюнок-нагорода, але підказки локальні, а не по рядку.

## Поле і час
- Прямокутна сітка: Conceptis — 10×10 … 35×35 і Mega 100×65; Tatham — довільні ширина й висота.
- Окіл підказки — 3×3 (8 сусідів + сама клітинка); на краю/в куті — 6 чи 4 клітинки, тож макс. число менше (кутова 4, крайова 6).
- Шари: числа (дані) · стан гравця unknown / black / white.
- Час статичний; хід = зміна стану однієї клітинки (або протяжкою — кількох).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітинка | mark | unknown / black / white | клік циклює стани; у розвʼязку — чорна або біла |
| Підказка | static | 0–9 | у квадраті 3×3 навколо (включно з собою) рівно n чорних; сама клітинка може бути і чорною, і білою |
| Окіл 3×3 | zone | 9 / 6 / 4 клітинки | спільні клітинки сусідніх околів — основа «просунутих» дедукцій |
| Малюнок | zone | уся сітка | проявляється після розвʼязання (Conceptis); у Tatham — без задуму, випадковий |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left_click, cell)` → ТО `paint(cell, black)`; повтор → по колу black → white → empty (Tatham).
- КОЛИ `input(right_click, cell)` → ТО `mark(cell, white)`; повтор — по колу в іншому порядку.
- КОЛИ `input(drag, cells)` → ТО `custom: «той самий стан на всі пройдені клітинки»` (Tatham: «click and drag to colour several squares at once»).
- КОЛИ `constraint_broken(clue)` → ЯКЩО `custom: «чорних в окрузі 3×3 більше за n або білих більше за 9 − n (для краю — за розміром околу)»` (`+cond:count_in_area`) → ТО конфлікт, підказка червоніє (?).
- КОЛИ `custom: «в окрузі вже рівно n чорних і решта білі»` → ТО `custom: «підказка позначається виконаною»` (Tatham (?)).
- КОЛИ `all_constraints_met` → ТО `win`, `custom: «показати малюнок»` (Conceptis), `flash(completion)` (Tatham).
- Дедукція 0 → весь окіл білий; 9 → весь окіл чорний (разом із клітинкою); кутова 4 / крайова 6 → теж усе чорне.
- Дедукція «повний / порожній»: якщо невідомих в окрузі = n − чорні → усі чорні; якщо чорних уже n → решта білі.
- Дедукція «дві підказки» (Advanced Logic): околи сусідніх чисел перетинаються; різниця чисел обмежує клітинки поза перетином (напр., 7 і 4 поруч по горизонталі: у спільних 6 клітинках ≤ 4 чорних → 3 клітинки лише околу 7 усі чорні, спільні — рівно 4, 3 клітинки лише околу 4 — білі).
- Перемога: кожна підказка виконана; у Conceptis розвʼязок єдиний і досягається логікою. Поразки й рахунку нема.

## Керування і ввід
- Tatham Mosaic: ліва — чорна, права — біла, повтор циклює три стани (black / white / empty); drag — фарбує кілька клітинок одразу.
- Клавіатура (Tatham): стрілки — курсор, Return — чорна, Space — біла, Backspace — порожньо; повтор циклює стани.
- Conceptis-застосунки: тап / режим фарби й «точки» (?).

## Вікна, меню, HUD
- `game-screen`: сітка з числами, `conflict-highlight` переповнених підказок, позначка виконаних, `undo-button`.
- Tatham: оболонка колекції — Game / Type меню, Custom → `+window:params-dialog` (ширина, висота, Aggressive generation) — див. [tatham-collection](tatham-collection.md).
- Conceptis: `puzzle-select` за розміром і рівнем (Basic Logic / Advanced Logic / Mega), `end-screen` з малюнком.
- `help-window` — правила й техніки.
- Переходи: puzzle-select / Type → game-screen → розвʼязано → end-screen (малюнок).

## Фічі поза полем
- `difficulty-presets`: Basic Logic (вистачає однієї підказки за раз) / Advanced Logic (дві підказки впливають одна на одну) / Mega — розмір.
- Tatham: `custom-difficulty` (W×H), «Aggressive generation» — генератор старанніше прибирає зайві підказки (повільно, не радять для > ~30×30); `seed-input`, `share-code`, undo ∞, Solve.
- `puzzle-bank` Conceptis (журнали, застосунки); у Японії — Nurie-Puzzle для мобільних NTT DoCoMo (березень 2003); журнал «Mozaic» (Puzzler Media, UK, з 2004).
- `+feature:picture-reveal` (є в nonogram) — малюнок як нагорода.

## Варіації й родичі
- [Minesweeper](../hidden-deduction/minesweeper.md) — той самий лічильник сусідів, але без самої клітинки в окрузі й з прихованим полем; тут «відкрите» поле і самовключний окіл.
- [Nonogram](nonogram.md) — малюнок-нагорода, підказки по рядку; Conceptis-родина: Pic-a-Pix, Link-a-Pix, Maze-a-Pix.
- [Tatham Collection](tatham-collection.md) — Mosaic (Didi Kohen, кольори Michal Shomer; за проєктом mordechaim/Mosaic).
- [Light Up](light-up.md), [Tapa](tapa.md) — інші «числа про сусідів».
- Корінь ідеї — Game of Life Конвея (окіл 3×3): Trevor Truran.
- **Осі варіацій**: окіл (3×3 з собою / 8 сусідів / 4 сусіди / хрест) · видимість (усе / приховано, як сапер) · мета (малюнок / випадкова сітка) · кількість кольорів (1 / кілька (?)).

## Цікавинки для курсу
- Підрахунок чорних в околі 3×3 з урахуванням краю — 🌱.
- Конфлікт підказки: чорних > n або білих > розмір околу − n — 🌱.
- Розвʼязувач правилом «повний/порожній» до нерухомої точки — 📎; пари перетинних околів (Advanced) — 🥉.
- Генератор з малюнка: підказки з бітмапу, прибирати зайві, доки розвʼязок єдиний (Aggressive generation) — 🥇.
- Анімація-проявлення малюнка після розвʼязання — 🌱.

## Мапа на каталог
- Є: `satisfy-constraints`, `markup-validity`, `completion-detection`, `conflict-highlight` · `cell-click`, `keyboard-controls` · `neighbor-count-clue` ↔ число околу (з варіантом «включно з собою») · `dot-mark` ↔ біла · `unique-puzzle-generation`, `no-guess-generation` ↔ «using logic alone» · `difficulty-levels`, `difficulty-rating` ↔ Basic / Advanced · `field-size-picker` (Tatham Custom) · `level-bank` (Conceptis) · `undo-redo`, `seed-share` (Tatham).
- Перевикористано: `+picture-reveal`, `+drag-paint-line` (з nonogram), `+cell-shade-toggle` (з nurikabe), `+clue-done-mark`.
- **Нема** → пропозиції карток:
  - `+self-inclusive-neighborhood` «Окіл підказки включно з її клітинкою» · game-logic/constraints · 🌱 · слот {shape: 3x3|plus|8-neighbors, include_self} — параметр до `neighbor-count-clue`.

## Пропозиції до словників
- `+cond:count_in_area` — кількість клітинок стану в заданому околі (3×3, хрест) порівняно з n; відрізняється від `adjacent_count` тим, що включає саму клітинку.
- `+card:self-inclusive-neighborhood` — див. мапу.

## Джерела
- ⭐ [Conceptis: Fill-a-Pix](https://www.conceptispuzzles.com/index.aspx?uri=puzzle/fill-a-pix) — опис, розміри, Basic / Advanced / Mega.
- [Conceptis: правила](https://www.conceptispuzzles.com/index.aspx?uri=puzzle/fill-a-pix/rules) — «including the square with the clue»; приклади 0, 2, 9; Advanced — дві підказки одночасно.
- [Conceptis: історія](https://www.conceptispuzzles.com/index.aspx?uri=puzzle/fill-a-pix/history) — Trevor Truran (Games & Puzzles, кінець 1970-х), прототипи наприкінці 2001, анонс 02.2003, Nurie-Puzzle 03.2003, Mozaic 03.2004.
- [Conceptis: техніки](https://www.conceptispuzzles.com/index.aspx?uri=puzzle/fill-a-pix/techniques).
- [Tatham: Mosaic](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/mosaic.html) — правила, миша й клавіатура, Custom, автори, інші назви; [грати](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/mosaic.html).
- YouTube: пошук «fill-a-pix puzzle».

## Непевне
- (?) Як саме Tatham і Conceptis підсвічують переповнену чи виконану підказку — сторінки цього не описують.
- (?) Кольорові Fill-a-Pix — у Conceptis бачив лише ч/б, тож вісь «кілька кольорів» лишаю гіпотезою.
- (?) Керування в застосунках Conceptis (режими тапу) — не перевіряв.
- (?) Хто придумав назву «Fill-a-Pix» — сторінка історії не каже.
