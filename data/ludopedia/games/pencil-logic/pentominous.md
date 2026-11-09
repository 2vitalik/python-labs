---
title: Pentominous («Пентамінус»)
slug: pentominous
aka: [Polyominous, Pentomino Fillomino]
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
year: 2013
platforms: [paper, web]
links:
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/pentominous.js", best: true, note: "puzz.link: правила, коди помилок, тести вводу літер і перешкод"}
  - {kind: official, url: "https://www.gmpuzzles.com/blog/pentominous-rules-info/", note: "GM Puzzles: правила, автор Grant Fikes, 2013, приклад і рядок відповіді"}
  - {kind: other, url: "https://gmpuzzles.com/blog/tag/pentominous/page/7", note: "GM Puzzles: архів пазлів, варіант Pentominous (Borders)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=pentominous+puzzle", note: "пошук; розвʼязання"}
stage: v1
coverage: 70
mechanics: [satisfy-constraints, markup-validity, completion-detection, cell-click, keyboard-controls, edge-marking, conflict-highlight, connectivity-check, piece-rotate-flip, in-game-editor, level-bank, undo-redo, +shape-identity-check, +letter-shape-clue, +equal-size-partition, +obstacle-cells]
proposes: ["+cond:same_shape(a, b)", "+cond:shape_is(region, letter)", "+role:obstacle", "+card:shape-identity-check", "+card:letter-shape-clue", "+card:equal-size-partition", "+card:obstacle-cells"]
author: opus
date: 2026-11-09
---

# Pentominous — поріж сітку на пентаміно; дві однакові фігури не торкаються стороною

## Суть
Сітка з літерами F, I, L, N, P, T, U, V, W, X, Y, Z у деяких клітинках. Гравець ділить усю сітку на пентаміно (області з 5 клітинок). Дві сусідні по стороні пентаміно не можуть мати однакову форму (з урахуванням поворотів і відбиттів); літера в клітинці каже, якою фігурою є пентаміно, що її містить. Незвичне: перевірка — **тотожність форм** сусідів, а не значення; суміш Fillomino (поділ без меж) і класичних 12 пентаміно. Автор — Grant Fikes, 2013, GM Puzzles.

## Поле і час
- Прямокутна сітка; GM Puzzles радить для авторів ≥ 10×10 і співвідношення сторін ≤ 2:1.
- Розвʼязок — розбиття: межі по ребрах або літера в кожній клітинці (рядок відповіді GM — літери фігур у рядках).
- puzz.link: окремі клітинки-перешкоди — не належать жодній фігурі.
- Сусідство ортогональне; дотик кутами однакових фігур дозволений.
- Час статичний; хід = межа на ребрі або літера в клітинці.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітинка з літерою | static | одна з 12 літер | належить пентаміно саме цієї форми |
| Порожня клітинка | mark | належність / літера-відповідь | входить рівно в одну пентаміно |
| Перешкода (puzz.link) | static | — | не входить у жодну фігуру; літеру не приймає |
| Ребро | mark | невідомо / межа / «не межа» | межі відокремлюють фігури |
| Пентаміно | zone | форма з 12, з точністю до поворотів і відбиттів | рівно 5 клітинок; може містити кілька однакових літер |
| Інвентар форм | static | 12 фігур (GM — під пазлом) | довідка; не всі форми мусять бути, форма може повторюватись |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag, edge)` → ТО `mark(edge, border)`; повтор → `unmark(edge)` (?).
- КОЛИ `input(key_letter, cell)` (play) → ЯКЩО `not occupied(cell, obstacle)` → ТО `set_value(cell, letter)` (тест «Type F to enter answer, except on obstacle»).
- КОЛИ `input(key_letter, cell)` (edit) → ТО `set_value(cell, clue_letter)`; `q` → `set_cell(cell, obstacle)`.
- КОЛИ `constraint_broken(size)` → ЯКЩО `region_size(region, > 5)` → ТО конфлікт (`bkSizeGt`); `< 5` → `bkSizeLt`.
- КОЛИ `constraint_broken(letter)` → ЯКЩО `custom: «форма області ≠ літера в ній»` → ТО конфлікт (`nmShapeNe`).
- КОЛИ `adjacent(region_a, region_b)` → ЯКЩО `same(region_a, region_b, shape)` (повороти й відбиття = одна форма) → ТО `constraint_broken(same_shape_touch)` (`bsSameShape`).
- КОЛИ `constraint_broken(border)` → ЯКЩО `custom: «зайва межа всередині фігури»` → ТО конфлікт (`bdUnused`) (?).
- КОЛИ `all_constraints_met` → ТО `win`.
- Наслідки: дві сусідні клітинки з різними літерами — між ними межа; однакові літери поруч можуть бути в одній фігурі, а якщо в різних — це заборонено (однакові форми торкались би).
- Дедукції: клітинка, затиснута так, що в неї входить лише одна пентаміно-форма, отримує цю літеру; X і I мають мало розміщень — з них починають; однакові літери, що не вміщаються в одну фігуру, — різні фігури, тож вони не можуть сусідити.
- Перемога: уся сітка (крім перешкод) — пентаміно, літери збігаються з формами, сусіди різні. Поразки й рахунку нема.

## Керування і ввід
- puzz.link play: межі drag-ом по ребрах, права кнопка — «не межа»; клавіші F/I/L/N/P/T/U/V/W/X/Y/Z — літера-відповідь у клітинці (альтернатива межам) (?).
- puzz.link edit: літери-підказки клавішами; `q` — перешкода.
- Папір (GM): лінії меж олівцем; відповідь — літери в позначених рядках через кому.

## Вікна, меню, HUD
- `game-screen` (цифрова версія, puzz.link): сітка, літери, межі, `conflict-highlight` за Check (код помилки текстом).
- Панель кнопок puzz.link: Check · Undo · Redo · Erase answer; перемикач Edit / Play (див. puzz-link).
- `help-window` — правила; GM Puzzles: сторінка правил з прикладом і інвентарем 12 фігур під пазлом.
- `puzzle-select` — архів GM за тегом, книга «Plenty o' Pentominous» (цифрова версія — банк пазлів).
- `end-screen` — «розвʼязано» після Check.

## Фічі поза полем
- `undo`/`redo`, `auto-check` за кнопкою (puzz.link).
- `level-editor` + `share-code` — пазл кодується URL (puzz.link).
- `puzzle-bank` — архів GM Puzzles з рівнями складності за класами (easy → Grandmaster) (?).

## Варіації й родичі
- **Pentominous (Borders)** — частина меж уже намальована (GM).
- Варіант з фіксованою кількістю фігур (напр. 20 пентаміно) — за результатами пошуку (?).
- **Fillomino** — предок: поділ на поліоміно за числами; **Polyominous** — назва Fillomino в блозі Grant Fikes.
- **LITS** — та сама заборона однакових сусідніх фігур, але для тетроміно і з фарбуванням; **Palisade/Five Cells** — теж поділ на 5, але з підказкою-периметром.
- **Pentomino** (board-digital) — гра-викладання тих самих 12 фігур.
- **Осі варіацій**: розмір фігури (тетро / пента / вільний) · що задає підказка (форма / розмір / периметр) · заборона однакових сусідів (стороною / і кутом) · чи дано частину меж.

## Цікавинки для курсу
- Канонізація форми: нормалізувати 5 клітинок за 8 симетріями (повороти × відбиття) і порівняти — 🥉.
- Розпізнавання літери (F…Z) за канонічною формою — 📎.
- Перевірка «сусідні фігури різні» по графу суміжності областей — 📎.
- Два способи відповіді (межі або літери в клітинках) з одним валідатором — 🥉.
- Генератор з єдиністю розвʼязку і мінімальними літерами — 🥇.

## Мапа на каталог
- Є: `satisfy-constraints` · `markup-validity` · `completion-detection` · `cell-click` · `keyboard-controls` · `edge-marking` · `conflict-highlight` · `connectivity-check` (фігура звʼязна) · `piece-rotate-flip` (форма з точністю до поворотів/відбиттів) · `in-game-editor` · `level-bank` · `undo-redo`.
- **Нема** → пропозиції карток:
  - `+shape-identity-check` (пропоновано в LITS) — тут на пентаміно, 8 симетрій.
  - `+letter-shape-clue` «Літера-підказка = форма фігури» · game-logic/constraints · 📎.
  - `+equal-size-partition` (пропоновано в Palisade) — тут K = 5.
  - `+obstacle-cells` «Клітинки поза розбиттям» · entities/legality · 🌱.

## Пропозиції до словників
- `+cond:same_shape(a, b)` — однакова форма з точністю до поворотів і відбиттів (Pentominous, LITS, Double Choco).
- `+cond:shape_is(region, letter)` — область має задану форму.
- `+role:obstacle` — клітинка поза грою пазла (не належить жодній області).

## Джерела
- ⭐ [puzz.link pentominous.js](https://puzz.link/js/pzpr-samples/pentominous.js) — правила (форма може повторюватись чи не зʼявлятись; фігура може містити кілька однакових літер), коди `bkSizeGt`, `bkSizeLt`, `nmShapeNe`, `bsSameShape`, `bdUnused`, тести вводу.
- [GM Puzzles: Pentominous Rules and Info](https://www.gmpuzzles.com/blog/pentominous-rules-info/) — правила, Grant Fikes 2013, формат відповіді, поради авторам.
- [GM Puzzles: архів Pentominous](https://gmpuzzles.com/blog/tag/pentominous/page/7) — у результатах пошуку, зокрема Pentominous (Borders).
- YouTube: [пошук](https://www.youtube.com/results?search_query=pentominous+puzzle).

## Непевне
- (?) `bdUnused` — значення коду не розшифроване джерелом; припущення: межа, що не розділяє дві різні фігури.
- (?) Керування мишею для пентаміно-жанру в puzz.link — за загальною схемою, не перевірено тестами.
- (?) Варіант з фіксованою кількістю фігур — лише в підсумку пошуку, сторінку не відкривав.
- (?) Рівні складності архіву GM — з загальних знань про сайт.
- (?) Сторінка з черги `pentominous-rules-and-info` віддала 404; робоча адреса — `pentominous-rules-info`.
