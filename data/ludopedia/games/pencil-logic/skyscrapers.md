---
title: Skyscrapers (Towers, Хмарочоси)
slug: skyscrapers
aka: [Towers, Building Puzzle, Skyscraper, Хмарочоси, Вежі, ビルディング]
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
year: 1992
platforms: [paper, web, mobile, PC]
links:
  - {kind: official, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/towers.html", best: true, note: "Tatham Towers: правила, pencil marks, M, сірі підказки, Custom 3–9, Unreasonable, 2D-вигляд у Preferences"}
  - {kind: play, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/towers.html", note: "Towers у браузері; меню Game/Type, кнопки New/Restart/Undo/Redo/Solve"}
  - {kind: other, url: "https://www.conceptispuzzles.com/index.aspx?uri=puzzle/skyscrapers", note: "Conceptis: правила, розміри 4×4–6×6 за складністю"}
  - {kind: other, url: "https://www.conceptispuzzles.com/index.aspx?uri=puzzle/skyscrapers/techniques", note: "Conceptis: 15 технік розвʼязання (підказки 1, N, 2; перебір кандидатів)"}
  - {kind: other, url: "https://www.gmpuzzles.com/blog/?p=541", note: "GM Puzzles: правила й історія (японський жанр, WPC 1992), розміри 5–9"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/skyscrapers.js", note: "puzz.link: правила EN/JP, коди помилок nmDupRow / nmSightNe / ceNoNum"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=skyscrapers+puzzle+how+to+solve", note: "пошук; розвʼязання"}
stage: v1
coverage: 70
mechanics: [markup-validity, completion-detection, satisfy-constraints, line-sum-clue, cell-click, keyboard-controls, pencil-marks, hover-highlight, unique-puzzle-generation, difficulty-levels, level-solver, field-size-picker, game-settings, undo-redo, seed-share, import-open-formats, gui-render, +latin-square, +visibility-count-clue, +auto-candidates, +solve-into-undo, +clue-done-mark, +view-2d-3d]
proposes: ["+cond:view_count", "+cond:duplicate_in_line", "+ui:clue-done-mark", "+feature:view-2d-3d", "+window:params-dialog", "+window:game-id-dialog", "+card:clue-done-mark"]
author: opus
date: 2026-11-09
---

# Skyscrapers (Towers) — латинський квадрат висот, де підказка ззовні рахує, скільки веж видно

## Суть
Сітка N×N — квартал; у кожну клітинку ставиш вежу висотою 1…N так, щоб у кожному рядку й стовпці кожна висота була рівно раз (латинський квадрат). Числа на краях кажуть, скільки веж видно, якщо дивитися в рядок/стовпець з цього боку: вища вежа ховає всі нижчі за нею. Незвичне: підказка не про значення клітинки, а про **профіль послідовності** — кількість «рекордів» (префіксних максимумів) у перестановці.

## Поле і час
- Квадратна сітка N×N; Tatham — N від 3 до 9 (більше — незручно вводити цифри); GM Puzzles радить 5×5…9×9; Conceptis — 4×4…6×6 у безкоштовних зразках.
- Підказки — у рамці навколо поля: до 4N чисел (зверху, знизу, ліворуч, праворуч); у складніших пазлах частина підказок відсутня, а частина висот дана всередині (Tatham, GM Puzzles).
- Шари: підказки рамки й дані висоти (незмінні) · висота гравця · pencil marks · «сірі» (опрацьовані) підказки.
- Tatham малює вежі тривимірними блоками; у Preferences — плаский 2D-вигляд із цифрами.
- Час статичний; хід = вписати/стерти висоту чи кандидата.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітинка | mark | висота 1…N або порожньо; кандидати | одна висота або набір олівцевих кандидатів |
| Вежа (висота) | mark | h ∈ 1…N | рахується в рядку й стовпці; ховає нижчі за собою в лінії погляду |
| Дана висота | static | h | незмінна підказка всередині поля |
| Кандидат (pencil mark) | mark | набір висот | ігнорується перевіркою (Tatham) |
| Підказка рамки | static | число v, сторона, ряд/стовпець | видимих веж з цього боку = v |
| Сіра підказка | mark | — | гравець позначив як опрацьовану; на перевірку не впливає |
| Рядок / стовпець | zone | N клітинок | кожна висота 1…N рівно раз |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left_click, cell)` + `input(key_digit)` → ТО `set_value(cell, h)`; Space → `unmark(cell)` (Tatham).
- КОЛИ `input(right_click, cell)` + `input(key_digit)` → ЯКЩО `not custom: «у клітинці вже стоїть вежа»` → ТО `mark(cell, candidate h)`; повтор тієї ж цифри → `unmark(cell)` для цього кандидата (Tatham).
- КОЛИ `input(key_M)` → ТО `custom: «кожна клітинка без вежі отримує повний набір кандидатів 1…N»` (Tatham).
- КОЛИ `after(set_value)` → ТО `custom: «кандидати клітинки стираються»` (вежа й кандидати не співіснують, Tatham).
- КОЛИ `input(left_click, clue)` → ТО `mark(clue, done)` (сірий); повторний клік → `unmark(clue)` (Tatham).
- КОЛИ `input(ctrl_or_shift + arrow)` → ТО `custom: «позначити сірими підказки з боку стрілки»` (Tatham).
- Видимість: вежа на позиції i видна з краю, ЯКЩО `custom: «вона вища за всі вежі між нею і краєм»`; перша від краю видна завжди.
- КОЛИ `constraint_broken(latin)` → ЯКЩО `custom: «висота повторюється в рядку чи стовпці»` (`+cond:duplicate_in_line`) → ТО конфлікт (puzz.link `nmDupRow`).
- КОЛИ `constraint_broken(view)` → ЯКЩО `custom: «кількість видимих веж ≠ підказці»` (`+cond:view_count`) → ТО конфлікт (puzz.link `nmSightNe`).
- КОЛИ `constraint_broken(fill)` → ЯКЩО `custom: «є порожня клітинка»` → ТО не розвʼязано (puzz.link `ceNoNum`).
- КОЛИ `all_constraints_met` → ТО `win`.
- Дедукція «підказка 1»: найвища вежа N стоїть впритул до підказки (Conceptis).
- Дедукція «підказка N»: висоти з цього боку 1, 2, …, N по зростанню (Conceptis).
- Дедукція «вежа N далі від підказки v»: N не може стояти ближче ніж на позиції v (між краєм і нею має вміститися v−1 видимих) — звужує кандидатів (Conceptis «High skyscrapers»).
- Дедукція «підказка 2»: якщо N — не друга, а далі, то впритул до підказки стоїть N−1 (Conceptis); якщо 1 впритул до 2 — N у наступній клітинці; N−1 не може стояти другою від підказки 2 (Conceptis).
- Дедукція «єдина послідовність»: коли лишилося кілька висот, а підказці відповідає лише одна їхня перестановка — заповнити (Conceptis).
- Дедукція «пробний хід»: поставити кандидата, якщо він веде до суперечності з підказкою чи повтору — викреслити (Conceptis advanced).
- Перемога: латинський квадрат + усі підказки рамки виконано. Поразки й рахунку нема.

## Керування і ввід
- Tatham: лівий клік + цифра — вежа; лівий клік + Space або Undo — стерти.
- Pencil: правий клік + цифра — додати/прибрати кандидата; правий клік + Space або лівий клік + цифра/Space — очистити кандидатів.
- Клавіатура: стрілки — курсор; цифра — вписати; Return — перемикач режиму «олівець»; M — усі кандидати скрізь.
- Підказки: лівий клік — сіра/звичайна; Ctrl/Shift + стрілка — позначити підказки з того боку.
- Спільні дії Tatham: New, Restart, Undo, Redo, Solve; Enter game ID / random seed; Download/Upload save file; Preferences.
- Conceptis і puzz.link — клік по клітинці й цифра; деталі вводу не перевіряв (?).

## Вікна, меню, HUD
- `game-screen`: сітка з 3D-вежами (або цифрами в 2D), підказки рамки, `pencil-marks`, курсор, сірі підказки (`+ui:clue-done-mark`).
- Tatham: меню Game (Enter game ID…, Enter random seed…, Download save file…, Upload save file…, Preferences…) · Type (пресети + Custom…) · кнопки New game, Restart game, Undo move, Redo move, Solve game.
- `+window:params-dialog` (Custom…): Grid size 3–9, Difficulty (найвища — Unreasonable).
- `+window:game-id-dialog` — ID/seed; «Link to this puzzle: by game ID / by random seed».
- `settings-window` (Preferences) — 2D/3D вигляд (`+feature:view-2d-3d`).
- `help-window` — «Full instructions».
- Переходи: Type → Custom → params-dialog → генерація → game-screen; Solve → розвʼязок у стеку undo.

## Фічі поза полем
- `undo` / `redo` без ліміту; `auto-solve` (Solve).
- `seed-input`, `share-code`, збереження/завантаження файла.
- `custom-difficulty`: розмір і складність; легші рівні — без перебору, Unreasonable може вимагати backtracking, розвʼязок єдиний (Tatham).
- `theme-select`-подібне: 2D/3D вигляд (Preferences).
- Conceptis — банк пазлів за розміром і складністю; puzz.link — редактор і URL пазла.

## Варіації й родичі
- Родичі: [KenKen](kenken.md) (латинський квадрат + арифметичні клітки), [Sudoku](sudoku.md) (латинський квадрат + блоки), Skyscraper-обмеження всередині [Sudoku variants](sudoku-variants.md), [Kuromasu](kuromasu.md) (число = скільки клітинок видно), колекція [Tatham](tatham-collection.md) (Towers поряд з Keen, Unequal, Solo).
- GM Puzzles: дані висоти всередині — рідко, якщо тема цікава; є окрема збірка «variations on Skyscrapers» (не відкривав).
- Варіанти з власних знань (?): з порожніми клітинками/парками, Sum Skyscrapers (підказка = сума видимих висот), діагональні підказки.
- **Осі варіацій**: що рахує підказка (кількість видимих / сума видимих) · підказки повні / неповні · дані висоти всередині (так / ні) · латинський квадрат / з порожніми клітинками.

## Цікавинки для курсу
- Перевірка латинського квадрата — 🌱.
- Підрахунок видимих веж (кількість префіксних максимумів) з чотирьох боків — 🌱.
- 2D-рендер vs псевдо-3D вежі з тим самим станом (перемикач у налаштуваннях) — 📎.
- Помічник кандидатів: M + викреслення за рядком/стовпцем + «підказка 1 / N» — 🥉.
- Розвʼязувач: для кожного рядка перелічити перестановки, сумісні з двома підказками й кандидатами, перетнути з колонками; далі backtracking — 🥇.
- Генератор з неповними підказками й єдиним розвʼязком (видаляти підказки, доки розвʼязок єдиний) — 👑.

## Мапа на каталог
- Є: `markup-validity` ↔ повтори · `completion-detection`, `satisfy-constraints` · `line-sum-clue` ↔ підказка рамки (картка прямо згадує Skyscrapers) · `cell-click`, `keyboard-controls`, `hover-highlight` · `pencil-marks` · `unique-puzzle-generation`, `difficulty-levels`, `level-solver` · `field-size-picker`, `game-settings` ↔ Custom · `undo-redo`, `seed-share`, `import-open-formats` ↔ game ID · `gui-render` ↔ 3D-вежі.
- Перевикористано: `+latin-square` (з KenKen), `+visibility-count-clue` (з Kuromasu; слот counts: towers), `+auto-candidates`, `+solve-into-undo`.
- **Нема** → пропозиції карток:
  - `+clue-done-mark` «Позначити підказку опрацьованою» · interface/input · 🌱 — сірі підказки Towers, Undead; лічильники Undead сіріють самі.
  - `+view-2d-3d` «Перемикач плаского / обʼємного вигляду того самого стану» · interface/render · 📎.

## Пропозиції до словників
- `+cond:view_count` — кількість видимих з точки сутностей = N (повтор з Kuromasu; тут — вежі, вища ховає нижчу).
- `+cond:duplicate_in_line` — повтор значення в рядку/стовпці (повтор з KenKen).
- `+ui:clue-done-mark` — підказка, позначена гравцем як опрацьована (сіра).
- `+feature:view-2d-3d` — вибір 2D/3D вигляду в налаштуваннях.
- `+window:params-dialog`, `+window:game-id-dialog` — повтор Tatham-вікон.
- `+card:clue-done-mark` — див. мапу.

## Джерела
- ⭐ [Tatham: Towers](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/towers.html) — правила, керування, M, сірі підказки, Ctrl/Shift+стрілка, Custom 3–9, Unreasonable, 2D у Preferences.
- [Towers у браузері](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/towers.html) — меню й кнопки.
- [Conceptis: Skyscrapers](https://www.conceptispuzzles.com/index.aspx?uri=puzzle/skyscrapers) — правила, розміри зразків.
- [Conceptis: техніки](https://www.conceptispuzzles.com/index.aspx?uri=puzzle/skyscrapers/techniques) — підказки 1, N, 2; «high skyscrapers»; пробні ходи.
- [GM Puzzles: Skyscrapers Rules and Info](https://www.gmpuzzles.com/blog/?p=541) — японський жанр, перша широка публікація — Puzzler (Sekai Bunka-sha) на 1-му WPC, Нью-Йорк, 1992.
- [puzz.link: skyscrapers.js](https://puzz.link/js/pzpr-samples/skyscrapers.js) — правила EN/JP, коди помилок.
- YouTube: пошук «skyscrapers puzzle how to solve».

## Непевне
- (?) Автор і перша публікація жанру невідомі — GM Puzzles сам просить читачів підказати; `year: 1992` — перша широка поява, не винахід.
- (?) Як Tatham Towers підсвічує помилки (дублікати, невиконані підказки) — у документації не описано.
- (?) Назви нижчих рівнів складності Towers — сторінка називає лише Unreasonable.
- (?) Властивість «a + b ≤ N + 1 для протилежних підказок» — з власних знань, у відкритих джерелах не бачив.
- (?) Sum Skyscrapers і варіанти з парками — з власних знань.
