---
title: Takuzu (Binairo, Unruly, Tic-Tac-Logic)
slug: takuzu
aka: [Binairo, Binero, Unruly, Tic-Tac-Logic, Tohu wa Vohu, Binary Puzzle, Binoxxo, Binox, Zernero, Eins und Zwei, Sudoku Binary, Tango, Бінарний пазл]
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
year: 2009
platforms: [paper, web, mobile, PC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Takuzu", best: true, note: "три правила, усі назви, автори Binairo й Tohu wa Vohu, техніки, варіанти, розміри"}
  - {kind: official, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/unruly.html", note: "Tatham Unruly: правила, ввід мишею/клавіатурою, параметри Custom, опція «Unique rows and columns»"}
  - {kind: play, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/unruly.html", note: "Unruly у браузері; меню Game/Type"}
  - {kind: other, url: "https://www.conceptispuzzles.com/index.aspx?uri=puzzle/tic-tac-logic", note: "Conceptis Tic-Tac-Logic: X/O, рядки й стовпці різні; підсторінки rules/techniques/history"}
  - {kind: other, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/common.html", note: "спільні дії Tatham: undo/redo, solve, game ID"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=takuzu+binairo+how+to+solve", note: "пошук; розвʼязання"}
stage: v1
coverage: 70
mechanics: [markup-validity, completion-detection, satisfy-constraints, cell-click, keyboard-controls, unique-puzzle-generation, difficulty-levels, level-solver, field-size-picker, game-settings, rule-variants, undo-redo, seed-share, import-open-formats, +cell-shade-toggle, +solve-into-undo, +balanced-lines, +no-triple-run, +distinct-lines]
proposes: ["+cond:balanced", "+cond:lines_distinct", "+window:params-dialog", "+window:game-id-dialog", "+card:balanced-lines", "+card:no-triple-run", "+card:distinct-lines"]
author: opus
date: 2026-11-09
---

# Takuzu (Binairo) — заповни сітку двома символами: порівну в рядку, без трійок, без однакових рядків

## Суть
Прямокутна сітка; частина клітинок задана символом одного з двох видів (0/1, X/O, чорне/біле). Гравець заповнює решту так, щоб у кожному рядку й стовпці було порівну обох символів, ніде не стояло трьох однакових підряд і (у класиці) жодні два рядки чи два стовпці не збігались. Це «бінарне судоку»: замість «цифра без повтору» — баланс і заборона серії. Незвичне: три обмеження різної природи — локальне (трійка), лічильне (баланс) і глобальне (унікальність рядків).

## Поле і час
- Прямокутна сітка, зазвичай квадратна, парні розміри (Tatham Unruly вимагає парних Width і Height); Wikipedia: типово від 4×4 до 20×20, бувають і 30×40.
- Шари клітинки: задане значення (незмінне) · стан гравця: порожньо / символ A / символ B.
- Дім (house) — рядок або стовпець; блоків, як у судоку, нема.
- Час статичний; хід = поставити/змінити/стерти символ.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Порожня клітинка | mark | стан empty / A / B | приймає один із двох символів |
| Задана клітинка | static | символ A або B | незмінна підказка |
| Символ A (чорне, 1, X) | mark | — | рахується в баланс свого рядка й стовпця |
| Символ B (біле, 0, O) | mark | — | те саме для другого виду |
| Рядок / стовпець | zone | довжина L (парна) | рівно L/2 кожного символу; без трьох однакових поспіль |
| Пара рядків / пара стовпців | zone | — | у класиці — не можуть збігатися повністю |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left_click, cell)` → ЯКЩО `not state(cell, given)` → ТО `mark(cell, A)`; повторні кліки циклять empty → A → B → empty (Tatham).
- КОЛИ `input(right_click, cell)` → ЯКЩО `not state(cell, given)` → ТО `mark(cell, B)`; повтор — цикл тих самих трьох станів.
- КОЛИ `input(middle_click, cell)` → ТО `unmark(cell)` (Tatham; клавіша Backspace — те саме).
- КОЛИ `input(key, cell)` → ТО Return = `mark(cell, A)`, Space = `mark(cell, B)` (Tatham, курсор стрілками).
- КОЛИ `pattern(line(3))` → ЯКЩО `same(cells, symbol)` → ТО `custom: «порушено правило "без трійок" у рядку чи стовпці»`.
- КОЛИ `constraint_broken(balance)` → ЯКЩО `custom: «у рядку/стовпці одного символу більше за L/2»` (`+cond:balanced`) → ТО `custom: «рядок/стовпець конфліктний»`.
- КОЛИ `constraint_broken(unique_lines)` → ЯКЩО `custom: «два повністю заповнені рядки (або стовпці) однакові»` (`+cond:lines_distinct`) → ТО `custom: «конфлікт унікальності»`; у Tatham — лише з опцією «Unique rows and columns», рядок і стовпець між собою можуть збігатися.
- КОЛИ `all_constraints_met` → ТО `win`.
- Дедукція «пара»: дві однакові поруч → ЯКЩО `free(cell)` з обох кінців → ТО там протилежний символ (Wikipedia: Triples).
- Дедукція «щілина»: `A _ A` → ТО середина протилежна.
- Дедукція «квота»: ЯКЩО `count(A, ==, L/2)` у рядку → ТО решта клітинок рядка = B (Wikipedia: Counting).
- Дедукція «унікальність»: ЯКЩО рядку лишилось дві клітинки і один варіант дублює вже заповнений рядок → ТО обрати інший (Wikipedia: Uniqueness).
- Дедукція «від супротивного»: пробна постановка, що веде до трійки чи дисбалансу, — відкинути (Wikipedia: Elimination).
- Перемога: усі клітинки заповнені, три правила виконані. Поразки й рахунку нема.

## Керування і ввід
- Tatham Unruly: ліва кнопка — чорне, права — біле; повторний клік тієї ж кнопки циклює три стани; середня — очистити.
- Клавіатура Tatham: стрілки — курсор; Return — чорне, Space — біле (повтор циклює); Backspace — очистити.
- Спільні дії Tatham: New, Restart, Undo, Redo, Solve; Enter game ID / random seed; Download/Upload save file.
- Conceptis Tic-Tac-Logic: символи X і O замість кольорів; є інтерактивна версія на сайті (деталі вводу не відкривав).

## Вікна, меню, HUD
- `game-screen`: сітка з двома кольорами/символами, курсор, `conflict-highlight` (?).
- Tatham: меню Game (Enter game ID…, Enter random seed…, Download save file…, Upload save file…, Preferences…) · Type (пресети + Custom…) · кнопки New game, Restart game, Undo move, Redo move, Solve game.
- `+window:params-dialog` (Custom…): Width, Height (обидва парні), Difficulty, Unique rows and columns.
- `+window:game-id-dialog` — ID або seed пазла; на сторінці — посилання «by game ID» / «by random seed».
- `settings-window` (Preferences) — вміст для Unruly не перевіряв (?).
- `help-window` — правила (Tatham doc, Conceptis rules).
- Переходи: Type → Custom → params-dialog → генерація → game-screen; розвʼязано → New game.

## Фічі поза полем
- `undo` / `redo` без ліміту; `auto-solve` (Solve) — у історії undo (Tatham common).
- `seed-input`, `share-code` (game ID), збереження/завантаження у файл.
- `custom-difficulty`: розмір, складність; `custom-rules`: перемикач «унікальні рядки».
- `puzzle-bank` / газетні пазли: Binairo, Binero, LinkedIn Tango — щоденні (Wikipedia згадує Tango) (?).

## Варіації й родичі
- Варіанти (Wikipedia): без правила унікальності рядків; **Odd Binairo** — непарна сітка, у кожному рядку й стовпці на одну «1» більше; символи 0/1, X/O, 1/2, T/V, фігури.
- Tic-Tac-Logic (Conceptis) — назва-жарт: замість «три в ряд» — заборона трьох у ряд.
- LinkedIn Tango — бінарна сітка з додатковими знаками між клітинками (?).
- Родичі: [Yin-Yang](yin-yang.md) (два кольори, але звʼязність), [Hitori](hitori.md) (зафарбування без сусідства), [Sudoku](sudoku.md) (Latin-подібна «без повтору»), [Tatham Collection](tatham-collection.md) (Unruly як частина збірки), [Nonogram](nonogram.md) (рядкові обмеження на бінарній сітці).
- **Осі варіацій**: чи обовʼязкова унікальність рядків · довжина забороненої серії (3 / k) · баланс (порівну / +1 / задані квоти) · символи · додаткові підказки між клітинками.

## Цікавинки для курсу
- Перевірка «нема трьох однакових поспіль» у рядках і стовпцях — 🌱 (ковзне вікно на 3).
- Баланс рядка/стовпця — 🌱 (лічильник; помилка рано, коли одного вже > L/2).
- Унікальність рядків через множину кортежів — 🌱; з урахуванням лише повністю заповнених — 📎.
- Розвʼязувач пропагацією трьох дедукцій (пара, щілина, квота) до нерухомої точки — 🥉.
- Зведення до SAT / системи рівнянь над GF(2), як згадує Wikipedia, — 🥇.
- Генератор з єдиним розвʼязком і перемикачем «унікальні рядки» — 👑.

## Мапа на каталог
- Є: `markup-validity` ↔ три правила · `completion-detection`, `satisfy-constraints` · `cell-click`, `keyboard-controls` · `unique-puzzle-generation`, `level-solver`, `difficulty-levels`, `field-size-picker`, `game-settings` ↔ Custom · `rule-variants` ↔ «Unique rows and columns» · `undo-redo`, `seed-share` · `import-open-formats` ↔ game ID.
- Перевикористано: `+cell-shade-toggle` (цикл станів кліком), `+solve-into-undo`.
- **Нема** → пропозиції карток:
  - `+balanced-lines` «Порівну кожного символу в рядку/стовпці» · game-logic/constraints · 🌱 · слот {quota: half|half+1|given}.
  - `+no-triple-run` «Заборона k однакових підряд» · game-logic/constraints · 🌱 · слот {k: 3}.
  - `+distinct-lines` «Усі рядки (стовпці) різні» · game-logic/constraints · 🌱 · слот {scope: rows|cols|both}.

## Пропозиції до словників
- `+cond:balanced` — у лінії/групі кожного символу рівно задана квота (Takuzu, Odd Binairo).
- `+cond:lines_distinct` — жодні два заповнені рядки (стовпці) не однакові (Takuzu, Tic-Tac-Logic).
- `+window:params-dialog` — форма Custom Tatham (повтор із Light Up, Hitori, для правила трьох).
- `+window:game-id-dialog` — ввід ID / seed (повтор із Hitori).
- `+card:balanced-lines`, `+card:no-triple-run`, `+card:distinct-lines` — див. мапу.

## Джерела
- ⭐ [Wikipedia: Takuzu](https://en.wikipedia.org/wiki/Takuzu) — правила, 10+ назв, Binairo (Peter De Schepper і Frank Coussement, 2009), Tohu wa Vohu (Adolfo Zanellati), техніки, варіанти, розміри.
- [Tatham: Unruly](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/unruly.html) — правила, ввід, Custom (Width, Height, Difficulty, Unique rows and columns); автор порту — Lennard Sprong.
- [Unruly у браузері](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/unruly.html) — меню й кнопки.
- [Conceptis: Tic-Tac-Logic](https://www.conceptispuzzles.com/index.aspx?uri=puzzle/tic-tac-logic) — X/O, «no more than two adjacent», рядки й стовпці різні.
- [Tatham: common actions](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/common.html) — спільні дії збірки.
- YouTube: пошук «takuzu binairo how to solve».

## Непевне
- (?) Як саме Tatham Unruly підсвічує помилки (трійки, дисбаланс) — сторінка документації цього не описує.
- (?) Назви рівнів складності й пресети Type у Unruly — на сторінці не перелічені.
- (?) Порядок циклу станів для правої кнопки (empty → white → black чи інакше).
- (?) LinkedIn Tango: які саме знаки між клітинками (= / ×) — Wikipedia лише згадує назву.
- (?) Рік: 2009 — для Binairo; Tohu wa Vohu Zanellati, за Wikipedia, «приблизно того ж часу», точного року нема.
