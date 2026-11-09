---
title: Futoshiki (Unequal, Нерівності)
slug: futoshiki
aka: [Unequal, More or Less, Hutosiki, 不等式, Adjacent, Нерівності]
family: pencil-logic
also: []
klass: puzzle
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: setup
  goal: constraints
year: 2001
platforms: [paper, PC, web, mobile]
links:
  - {kind: other, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/unequal.html", best: true, note: "мануал Tatham Unequal: правила, режими Unequal/Adjacent, pencil marks, M/H, позначення підказок, рівні Trivial…Recursive"}
  - {kind: play, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/unequal.html", note: "грати в браузері (WASM), коротка інструкція"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Futoshiki", note: "Tamaki Seto 2001, газети UK, техніки розвʼязання"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=futoshiki+how+to+solve", note: "пошук; розвʼязання"}
stage: v1
coverage: 70
mechanics: [markup-validity, completion-detection, satisfy-constraints, cell-click, keyboard-controls, pencil-marks, unique-puzzle-generation, difficulty-levels, difficulty-rating, level-solver, field-size-picker, game-settings, rule-variants, seed-share, save-game, undo-redo, import-open-formats, +latin-square, +auto-candidates, +clue-done-mark, +solve-into-undo, +edge-inequality-clue, +absent-clue-is-info]
proposes: ["+cond:less_than(a, b)", "+cond:differ_by(a, b, 1)", "+cond:duplicate_in_line", "+card:edge-inequality-clue", "+card:absent-clue-is-info", "+ui:clue-done-mark", "+window:params-dialog", "+window:game-id-dialog"]
author: opus
date: 2026-11-09
---

# Futoshiki (Unequal) — латинський квадрат, де знаки «<» між сусідніми клітинками задають порядок

## Суть
Квадратна сітка s×s; гравець вписує цифри 1…s так, щоб у кожному рядку й стовпці кожна цифра була рівно раз. Між деякими сусідніми клітинками стоять знаки «<» / «>» — нерівність має виконатись; кілька цифр можуть бути дані наперед. Незвичне: підказки — **на ребрах між клітинками** і задають лише порядок, а не значення. У Tatham є другий режим — Adjacent: риска на ребрі означає «числа відрізняються на 1», а відсутність риски — що **не** відрізняються.

## Поле і час
- Квадратна сітка s×s; розмір задається в Custom (Tatham), Wikipedia показує 5×5.
- Підказки: на ребрах між сусідами (знак або риска) і подекуди дані цифри в клітинках.
- Шари: підказки на ребрах (незмінні, але гравець може їх «згасити») · цифри гравця · pencil marks.
- Час статичний; хід = вписати/стерти цифру чи кандидата. Пазл генерується (`random: setup`).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітинка | mark | цифра 1…s або порожньо; кандидати | одна цифра або набір кандидатів, не разом |
| Дана цифра | mark | d | закріплена |
| Кандидат (pencil mark) | mark | набір цифр | не впливає на перевірку |
| Знак нерівності | mark | напрямок «<» | гострий кінець — менша цифра |
| Риска Adjacent | mark | — | сусіди відрізняються рівно на 1 |
| Ребро без риски (Adjacent) | mark | — | сусіди **не** відрізняються на 1 (усі риски показані завжди) |
| Рядок / стовпець | zone | s | кожна цифра 1…s рівно раз |
| Згашена підказка | mark | стан grey | позначка гравця «вже використав» |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left_click, cell)` + `input(key_digit)` → ТО `set_value(cell, d)`; Space або 0 → `unmark(cell)` (Tatham).
- КОЛИ `input(right_click, cell)` + `input(key_digit)` → ТО `mark(cell, candidate d)`; та сама цифра вдруге — зняти кандидата (Tatham).
- КОЛИ `after(set_value)` → ЯКЩО `custom: «у клітинці були кандидати»` → ТО `custom: «кандидати стираються»` (Tatham: цифра і кандидати не співіснують).
- КОЛИ `input(key_M)` → ТО `custom: «вписати в усі клітинки повні набори кандидатів»` (Tatham).
- КОЛИ `input(key_H)` → ТО `custom: «як M, і ще прибрати всі очевидно неможливі кандидати»` (Tatham).
- КОЛИ `input(left_click, clue)` → ТО `set_state(clue, grey)`; повторно → `clear_state(clue, grey)` (Tatham).
- КОЛИ `input(ctrl_or_shift + arrow)` → ТО `set_state(clue_in_dir, grey)` — згасити підказку біля курсора (Tatham).
- Латинський квадрат: ЯКЩО `unique(row)` and `unique(col)` → рядки й стовпці задоволені; інакше `constraint_broken(custom: «повтор цифри в рядку/стовпці»)` (`+cond:duplicate_in_line`).
- Режим Unequal: ЯКЩО `custom: «a < b для кожного знака a < b»` (`+cond:less_than`) → підказка задоволена.
- Режим Adjacent: ЯКЩО `custom: «|a − b| = 1 там, де риска, і ≠ 1, де риски нема»` (`+cond:differ_by`) → ребро задоволене.
- Unequal на вищих рівнях: ЯКЩО `difficulty(high)` → ТО `custom: «не всі знаки показані»` (Tatham).
- КОЛИ `all_constraints_met` → ТО `win`.
- Дедукція «кінці ланцюга»: клітинка, більша за k інших у ланцюгу знаків, ≥ k+1; менша — ≤ s−k (Wikipedia: ланцюги нерівностей).
- Дедукція «AB elimination»: підмножина клітинок рядка з відомим набором значень звільняє ці значення з решти рядка (Wikipedia).
- Дедукція «до суперечності»: пройти значенням по ланцюгу нерівностей, поки не виникне суперечність (Wikipedia).
- Перемога: латинський квадрат і всі нерівності/риски виконані. Поразки й рахунку нема.

## Керування і ввід
- Лівий клік + цифра (або літера для s > 9) — вписати; Space/0 — стерти; Backspace у веб-інструкції.
- Правий клік + цифра — кандидат; правий клік + Space або лівий клік + цифра/Space — очистити кандидатів.
- Лівий клік по знаку — згасити/відновити підказку; Ctrl/Shift + стрілка — те саме з клавіатури.
- Клавіатура: стрілки — курсор; Return — перемикач «цифра / олівець».
- M — усі кандидати; H — усі кандидати мінус очевидні.
- Спільні дії Tatham: New, Restart, Undo, Redo, Solve; Enter game ID / random seed; Download / Upload save file; Preferences.

## Вікна, меню, HUD
- `game-screen`: сітка s×s, знаки «<» або риски на ребрах, цифри, `pencil-marks`, курсор, згашені підказки (`+ui:clue-done-mark`), `conflict-highlight` (?).
- Меню Game: Enter game ID… · Enter random seed… · Download save file… · Upload save file… · Preferences…; кнопки New game · Restart game · Undo move · Redo move · Solve game.
- Type → Custom… → `params-dialog`: Mode (Unequal / Adjacent), Size (s×s), Difficulty (Trivial … Recursive).
- `game-id-dialog`, `help-window`.

## Фічі поза полем
- Складність Tatham: **Trivial** (лише Custom) — знаків нема, чистий латинський квадрат; проміжні — дедалі складніші дедукції без перебору; **Recursive** (лише Custom) — потрібен backtracking, розвʼязок єдиний.
- `custom-rules`: режим Adjacent — інший тип підказок на тому самому полі.
- `undo` ∞ + `redo`, `auto-solve`, `seed-input`, `share-code`, збереження у файл.
- `auto-candidates` (M) і напівавтоматичне прибирання (H) — асистент розвʼязання.
- Газети UK: The Daily Telegraph, The Guardian (суботи), The Times, Dundee Courier, i (Wikipedia); Tatham: «зʼявляється в Guardian під назвою Futoshiki».

## Варіації й родичі
- **Adjacent** (Tatham) — риски «різниця 1»; відсутність риски — теж інформація.
- Родичі в сімʼї: [Sudoku](sudoku.md) (латинський квадрат + блоки), [KenKen](kenken.md) (латинський квадрат + арифметичні клітки), [Skyscrapers](skyscrapers.md) (латинський квадрат + видимість з краю), [Sudoku line/dot variants](sudoku-line-dot-variants.md) (Kropki-крапки «різниця 1 / удвічі»), Greater Than Sudoku у [Sudoku variants](sudoku-variants.md), [Tatham collection](tatham-collection.md) (оболонка).
- **Осі варіацій**: тип підказки на ребрі (порядок / різниця 1 / відношення ×2) · чи важлива відсутність підказки (Unequal — ні; Adjacent — так) · частка видимих знаків · дані цифри (є / нема).

## Цікавинки для курсу
- Рендер підказок на ребрах між клітинками з напрямком знака — 📎.
- Перевірка латинського квадрата + нерівностей — 🌱.
- Згашування підказок кліком як особиста розмітка гравця — 🌱.
- Кандидати M і «прибрати очевидні» H (рядок/стовпець + сусідні знаки) — 📎.
- Розвʼязувач: пропагація меж (min/max) по ланцюгах знаків + латинські виключення + backtracking на Recursive — 🥇.
- Генератор: випадковий латинський квадрат → знаки на всіх ребрах → прибирання з перевіркою єдиності і рейтингом за дедукціями — 👑.

## Мапа на каталог
- Є: `markup-validity`, `completion-detection`, `satisfy-constraints` · `cell-click`, `keyboard-controls`, `pencil-marks` · `unique-puzzle-generation`, `difficulty-levels`, `difficulty-rating` ↔ рівні за дедукціями, `level-solver` · `field-size-picker`, `game-settings`, `rule-variants` ↔ Mode Unequal/Adjacent · `seed-share`, `save-game`, `undo-redo`, `import-open-formats`.
- Перевикористано: `+latin-square` (KenKen) · `+auto-candidates` ↔ M · `+clue-done-mark` ↔ згашування знаків · `+solve-into-undo`.
- **Нема** → пропозиції карток:
  - `+edge-inequality-clue` «Підказка на ребрі між сусідами: порядок або різниця» · game-logic/constraints · 📎 · слот {kind: less|diff1|double} — Futoshiki, Adjacent, Kropki.
  - `+absent-clue-is-info` «Усі підказки показані, тож відсутність — теж обмеження» · game-logic/constraints · 🌱 — Adjacent, Kropki з негативним обмеженням.

## Пропозиції до словників
- `+cond:less_than(a, b)` — значення A менше за B.
- `+cond:differ_by(a, b, n)` — значення відрізняються рівно на n.
- `+cond:duplicate_in_line` — повтор з інших файлів (KenKen, Skyscrapers).
- `+ui:clue-done-mark` — повтор: згашена/використана підказка.
- `+card:edge-inequality-clue`, `+card:absent-clue-is-info` — див. мапу.
- `+window:params-dialog`, `+window:game-id-dialog` — повтор Tatham-вікон.

## Джерела
- ⭐ [Tatham: Unequal](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/unequal.html) — правила, режими Unequal/Adjacent («all clues are always visible»), керування (pencil marks, Return, M, H, Ctrl/Shift+стрілка, клік по підказці), Custom (Mode, Size, Difficulty: Trivial…Recursive), James Harvey, «Futoshiki» у Guardian.
- [Tatham: Unequal (грати)](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/unequal.html) — меню, кнопки, «pointed end smaller», Backspace.
- [Wikipedia: Futoshiki](https://en.wikipedia.org/wiki/Futoshiki) — Tamaki Seto 2001, «More or Less», газети UK, техніки (кандидати, AB elimination, ланцюги нерівностей).
- YouTube: пошук «futoshiki how to solve».

## Непевне
- (?) Назви проміжних рівнів Tatham Unequal (між Trivial і Recursive) — сторінка їх не перелічує.
- (?) Чи підсвічує Tatham дублікати й порушені знаки — не описано на сторінці.
- (?) Вміст Preferences у Unequal.
- (?) Типові розміри газетних Futoshiki (5×5…7×7) — бачив лише приклад 5×5.
- (?) Назва Renzoku для режиму Adjacent — з памʼяті, у джерелах не бачив.
- (?) Дедукція «кінці ланцюга з k» — узагальнення з Wikipedia-тексту про ланцюги, сформульоване мною.
