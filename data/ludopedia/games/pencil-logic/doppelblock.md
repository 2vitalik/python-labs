---
title: Doppelblock (Double Block)
slug: doppelblock
aka: [Double Block, Doplo, Дубль-блок]
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
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/doppelblock.js", best: true, note: "puzz.link: правила EN/JP, автор жанру Inaba Naoki, коди ceNoNum / nmDupRow / ceTooManyBlocks / nmSum"}
  - {kind: other, url: "https://www.janko.at/Raetsel/Doppelblock/index.htm", note: "Janko: правила DE/EN/JP, назви Double Block / Doplo, 250 пазлів 5×5–8×8"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/master/src/res/failcode.en.json", note: "тексти помилок pzprjs"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=doppelblock+puzzle+how+to+solve", note: "пошук; розвʼязання"}
stage: v1
coverage: 70
mechanics: [markup-validity, completion-detection, satisfy-constraints, line-sum-clue, cell-click, keyboard-controls, pencil-marks, conflict-highlight, level-bank, level-rating, import-open-formats, in-game-editor, +latin-square, +empty-cells-in-latin, +cell-shade-toggle, +sum-between-clue, +undo-redo, +seed-share]
proposes: ["+cond:sum_between", "+cond:count_in", "+cond:duplicate_in_line", "+card:sum-between-clue"]
author: opus
date: 2026-11-09
---

# Doppelblock — у кожному рядку й стовпці дві чорні клітинки, решта 1…N−2; ззовні — сума між чорними

## Суть
Сітка N×N: у кожному рядку й стовпці зафарбовуєш рівно дві клітинки, а в N−2 білих вписуєш числа 1…N−2 по одному разу. Число за краєм рядка/стовпця — сума чисел, що стоять **між** двома чорними клітинками цієї лінії. Незвичне: підказка задає не значення, а **проміжок** — гравець шукає водночас позиції «дужок» і перестановку всередині; сума 0 означає, що чорні стоять поруч.

## Поле і час
- Квадратна сітка N×N; Janko — 5×5 (66 пазлів), 6×6 (102), 7×7 (80), 8×8 (2).
- Числа в білих клітинках ∈ 1…N−2 (N = ширина поля).
- Підказки — праворуч/ліворуч і зверху/знизу (одна на лінію) (?); не всі лінії мають підказку.
- Шари: підказки рамки · чорні клітинки · числа гравця · кандидати/позначки (цифрова версія).
- Час статичний; хід = зафарбувати / вписати / стерти.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітинка | mark | чорна / число / порожньо | або блок, або одне число |
| Блок (чорна) | mark | — | рівно 2 у рядку й стовпці; межі «проміжку» |
| Число | mark | 1…N−2 | рівно раз у рядку й стовпці |
| Підказка рамки | static | сума s | сума чисел між двома блоками лінії = s; 0 — блоки поруч (JP-правила) |
| Рядок / стовпець | zone | N клітинок | 2 блоки + перестановка 1…N−2 |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(click, cell)` → ТО `mark(cell, block)`; повтор → `unmark(cell)` (?).
- КОЛИ `input(key_digit, cell)` → ТО `set_value(cell, n)`.
- КОЛИ `constraint_broken(blocks)` → ЯКЩО `custom: «у лінії більше двох блоків»` (`+cond:count_in`) → ТО конфлікт: «There are more than two blocks in a row or column» (ceTooManyBlocks).
- КОЛИ `constraint_broken(latin)` → ЯКЩО `custom: «число повторюється в рядку чи стовпці»` (`+cond:duplicate_in_line`) → ТО конфлікт (nmDupRow).
- КОЛИ `constraint_broken(clue)` → ЯКЩО `not custom: «сума між двома блоками = підказка»` (`+cond:sum_between`) → ТО конфлікт: «The sum of the numbers between the two blocks is wrong» (nmSum).
- КОЛИ `constraint_broken(fill)` → ЯКЩО `custom: «біла клітинка без числа»` → ТО конфлікт (ceNoNum).
- КОЛИ `all_constraints_met` → ТО `win`.
- Перемога: 2 блоки й повна перестановка в кожній лінії, усі суми виконані · Поразка: — · Рахунок: —.

## Керування і ввід
- puzz.link play: клік — блок / позначка; цифри — клавіатурою; права кнопка — допоміжна позначка «точно біла» (?).
- puzz.link edit: розмір і підказки рамки.
- Папір: зафарбувати, вписати числа, кандидати олівцем; типовий прийом — таблиця можливих сум для пари блоків (мін 0, макс сума всіх N−2).

## Вікна, меню, HUD
- `game-screen`: сітка, рамка з сумами, `conflict-highlight` для лінії з помилкою.
- puzz.link: перемикач play/edit, кнопка перевірки з першою помилкою, `settings-window`.
- `puzzle-select` — архів Janko (250), сортування за датою/розміром/складністю.
- `help-window` — правила DE/EN/JP.

## Фічі поза полем
- `auto-check` за кнопкою з кодами pzpr; `undo` / `redo`.
- `level-editor` + `share-code` (URL puzz.link).
- `puzzle-bank` Janko з рейтингом 1–8 (за часом розвʼязання); пазли з покроковим логічним шляхом — кольором.

## Варіації й родичі
- Назви: Double Block (EN), Doplo (швейцарський журнал Rätselverlag Küng); Janko вперше бачили на Croco Puzzle.
- Родичі: [Easy as ABC](easy-as-abc.md) (латинський квадрат з дірками + підказка рамки), [Kakuro](kakuro.md) (сума в проміжку), [Skyscrapers](skyscrapers.md), [Sudoku](sudoku.md).
- **Осі варіацій**: кількість блоків у лінії (2 / більше) · що міряє підказка (сума між / кількість між / сума зовні) · дані числа всередині (так / ні).

## Цікавинки для курсу
- Перевірка лінії: рівно 2 блоки, перестановка решти, сума між — 🌱.
- Генерація всіх розкладів лінії для суми s (позиції блоків × підмножини чисел) — 📎.
- Розвʼязувач: перетин кандидатів рядків і стовпців + backtracking — 🥇.
- Генератор з єдиним розвʼязком і частиною підказок — 👑.

## Мапа на каталог
- Є: `markup-validity`, `completion-detection`, `satisfy-constraints` · `line-sum-clue` ↔ сума на лінії · `cell-click`, `keyboard-controls`, `pencil-marks`, `conflict-highlight` · `level-bank`, `level-rating` · `import-open-formats`, `in-game-editor`.
- Перевикористано: `+latin-square`, `+empty-cells-in-latin` (з Easy as ABC), `+cell-shade-toggle`, `+undo-redo`, `+seed-share`.
- **Нема** → пропозиції карток:
  - `+sum-between-clue` «Сума між двома блоками лінії» · game-logic/constraints · 🌱 — Doppelblock; сестра `line-sum-clue`.

## Пропозиції до словників
- `+cond:sum_between` — сума значень між двома маркерами лінії = N.
- `+cond:count_in` — кількість сутностей виду в лінії/регіоні = N (повтор з інших пазлів).
- `+cond:duplicate_in_line` — повтор значення в рядку/стовпці.
- `+card:sum-between-clue` — див. мапу.

## Джерела
- ⭐ [puzz.link: doppelblock.js](https://puzz.link/js/pzpr-samples/doppelblock.js) — 4 правила EN, «invented by Inaba Naoki», коди помилок.
- [Janko: Doppelblock](https://www.janko.at/Raetsel/Doppelblock/index.htm) — правила DE/EN/JP (JP: сума 0, якщо між блоками нічого), назви, 250 пазлів за розмірами, рейтинг.
- [pzprjs failcode.en.json](https://raw.githubusercontent.com/robx/pzprjs/master/src/res/failcode.en.json) — тексти ceTooManyBlocks / nmSum.
- YouTube: пошук «doppelblock puzzle how to solve».

## Непевне
- (?) Рік і перша публікація невідомі: puzz.link називає автора Inaba Naoki, Janko — «невідомо».
- (?) Підказки з одного чи з обох боків лінії — у правилах не уточнено.
- (?) Схема миші puzz.link — не перевіряв на живій сторінці.
