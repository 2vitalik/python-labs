---
title: Sudoku (Судоку, Number Place)
slug: sudoku
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
year: 1979
platforms: [paper, web, mobile, PC, Switch]
links:
  - {kind: play, url: "https://sudoku.com/", best: true, note: "масовий цифровий плеєр: нотатки, підказки, 3 помилки, daily, рівні складності"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Sudoku", note: "правила, історія, 17 підказок, NP-повнота"}
  - {kind: official, url: "https://www.nikoli.co.jp/en/puzzles/sudoku/", note: "Nikoli: правила, симетрія підказок з 1986"}
  - {kind: play, url: "https://sudokupad.app/", note: "SudokuPad: Digit/Corner/Centre/Colour, мультивиділення, гарячі клавіші"}
  - {kind: official, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/solo.html", note: "Tatham Solo: генератор, рівні за техніками, X/Jigsaw/Killer"}
  - {kind: official, url: "https://www.sudokuwiki.org/Strategy_Families", note: "техніки розвʼязання за рівнями Basic/Tough/Diabolical/Extreme"}
  - {kind: steam, url: "https://store.steampowered.com/app/1188330/Classic_Sudoku/", note: "Cracking the Cryptic: Classic Sudoku"}
  - {kind: youtube, url: "https://www.youtube.com/c/CrackingTheCryptic", note: "канал Cracking the Cryptic — розвʼязання вголос"}
stage: v1
coverage: 75
mechanics: [markup-validity, completion-detection, satisfy-constraints, pencil-marks, cell-click, hover-highlight, keyboard-controls, difficulty-levels, difficulty-rating, unique-puzzle-generation, level-solver, daily-puzzle, level-bank, import-open-formats, wrong-mark-lose, score-records, profile-stats, save-autosave, end-screen, +digit-highlight, +auto-candidates, +technique-hint, +multi-select, +cell-coloring]
proposes: ["+ui:number-pad", "+ui:digit-highlight", "+ui:peer-highlight", "+ui:color-palette", "+feature:auto-candidates", "+feature:technique-hints", "+feature:second-chance", "+effect:clear_notes", "+card:multi-select"]
author: opus
date: 2026-11-02
---

# Sudoku — 9×9 цифр 1–9 без повторів у рядку, стовпці й блоці; база всієї сімʼї

## Суть
Гравець заповнює порожні клітинки сітки 9×9 цифрами 1–9 так, щоб кожен рядок, стовпець і блок 3×3 містив кожну цифру рівно раз. Частину цифр дано (givens); коректний пазл має **рівно один** розвʼязок, тож усе виводиться логікою без вгадування. Цифровий плеєр додає до паперу те, що й робить судоку «грою»: олівцеві нотатки двох видів, підсвітку, перевірку конфліктів, ліміт помилок, підказки з поясненням техніки, таймер і банк/daily.

## Поле і час
- Поле 9×9 = 81 клітинка, 27 «домів» (house): 9 рядків, 9 стовпців, 9 блоків 3×3. Розміри-варіанти: 4×4 (блоки 2×2), 6×6 (2×3), 16×16, 25×25 (Wikipedia).
- Шари клітинки: given (незмінна, інший колір) · цифра гравця · нотатки (кути / центр) · колір клітинки · підсвітка.
- Час статичний: нема тіків, хід = одна розмітка. Таймер — лише метрика (`timer-elapsed`), не впливає на правила.
- Мінімум підказок для єдиного розвʼязку — 17; класичних сіток ≈6.67×10²¹, суттєво різних — 5 472 730 538.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітинка | mark | значення ∅ або 1–9 | приймає цифру гравця; конфліктує з однаковими в своїх домах |
| Given (дана цифра) | static | 1–9 | незмінна; задає пазл; зазвичай симетрична (Nikoli, з 1986) |
| Цифра гравця | mark | 1–9, `correct?` | ставиться/стирається; у sudoku.com одразу звіряється з розвʼязком |
| Кутова нотатка (corner) | mark | набір цифр | «ця цифра — в одній з цих клітинок дому» (Snyder notation); у перевірці не бере участі |
| Центральна нотатка (centre) | mark | набір цифр | «кандидати цієї клітинки»; у перевірці не бере участі |
| Колір клітинки | mark | палітра 9+ | довільна розмітка гравця (ланцюги, парність); SudokuPad Colour mode |
| Рядок / стовпець | zone | 9 клітинок | 1–9 по разу |
| Блок 3×3 | zone | 9 клітинок | 1–9 по разу; у Jigsaw — нерегулярна форма |
| Виділення | mark | одна/багато клітинок | на нього діє ввід; мультивиділення ставить нотатку в усі клітинки разом |
| Конфлікт | mark | пара клітинок | підсвічується, коли два однакові числа бачать одне одне |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(digit d)` → ЯКЩО `cell(sel, empty|player)` → ТО `mark(sel, d)`; для given — `block`.
- КОЛИ `input(digit d)` у режимі Corner/Centre → ТО `mark(sel, note d)` (toggle: повтор знімає); заповнена клітинка нотаток не має (Tatham Solo).
- КОЛИ `input(erase)` → ТО `unmark(sel)`.
- КОЛИ `constraint_broken(unique_in_row|col|box)` → ТО `custom: «conflict-highlight обох клітинок»` (SudokuPad — лише за кнопкою Check / налаштуванням (?); GNOME/Sudoku.com — одразу).
- КОЛИ `input(digit d)` → ЯКЩО `mode(check_vs_solution)` and `custom: «d ≠ розвʼязок клітинки»` → ТО `counter(mistakes, +1)`, `flash`; цифра лишається червоною (sudoku.com).
- КОЛИ `counter(mistakes, >=, 3)` → ТО `lose`, `window(game-over-continue)` («Second Chance» за рекламу).
- КОЛИ `input(digit d)` → ЯКЩО `custom: «авто-видалення нотаток»` → ТО `custom: «стерти нотатку d у всіх клітинках, що бачать sel»` (?).
- КОЛИ `input(select cell)` → ТО `custom: «підсвітити всі клітинки з тією ж цифрою + рядок/стовпець/блок вибраної»`.
- КОЛИ `input(hint)` → ТО `custom: «знайти найпростіший крок за ієрархією технік, підсвітити клітинки й пояснити»`, `mark(cell, d)` після підтвердження.
- КОЛИ `input(check)` → ТО `custom: «звірити розмітку з правилами»`, `message(«ok» | «є помилки»)` (SudokuPad Check перевіряє лише базові правила судоку).
- КОЛИ `all_constraints_met` (усі 81 заповнені, без конфліктів) → ТО `win`, `timer(stop)`, `window(end-screen)`.
- Генерація: КОЛИ `level_start` → ТО `custom: «повна сітка → прибирати підказки, доки розвʼязок єдиний і рівень = заданому»`.
- Перемога: усі клітинки заповнені й жодного конфлікту. Поразка: лише в режимі з лімітом помилок (3) або з таймером. Рахунок: час; у sudoku.com — очки за рівень/швидкість (?) і кубок у турнірах.

## Керування і ввід
- Клік/тап по клітинці → вибір; цифра з клавіатури або екранної `number-pad`. Стрілки рухають виділення (Tatham, SudokuPad).
- **Режими вводу** (`mode-toggle`): Digit (Z) · Corner (X) · Centre (C) · Colour (V) у SudokuPad; Space/PgDn — наступний режим. Модифікатори: Shift+цифра = кутова, Ctrl+цифра = центральна, Ctrl+Shift+цифра = колір.
- **Мультивиділення**: drag або Ctrl+клік додає клітинки; Ctrl+A — усе, Ctrl+I — інвертувати. Подвійний тап — «виділити всі з цією цифрою» (tool-sensitive selection).
- Tatham Solo: правий клік + цифра = pencil mark; Enter перемикає ручку/олівець; Space або 0 — стерти.
- Sudoku.com: кнопки Undo · Erase · Notes (on/off) · Hint під полем.
- Undo Ctrl+Z, Redo Ctrl+Y.

## Вікна, меню, HUD
- `main-menu` (sudoku.com): Нова гра → `difficulty-select` (Easy/Medium/Hard/Expert/Master/Extreme); Daily Challenges → `daily-window`; Statistics → `stats-window`; Settings → `settings-window`.
- `game-screen`: поле 9×9 + `timer-elapsed` + `mistake-counter` «Mistakes 0/3» + назва рівня + `pause-button` + `number-pad` (лічильник лишку на кожній цифрі (?)) + `undo-button` · erase · `mode-toggle` Notes · `hint-button`.
- HUD-підсвітки: `selection-highlight`, `+ui:peer-highlight` (рядок/стовпець/блок вибраної), `+ui:digit-highlight` (усі такі ж цифри), `conflict-highlight`, `pencil-marks`, `hint-marker`.
- `pause-menu` — поле ховається, щоб не думати на паузі (?).
- `game-over-continue` — після 3 помилок: «Second Chance» / New Game.
- `end-screen` — час, рівень, рекорд, «Нова гра».
- `daily-window` — календар місяця з позначками розвʼязаних днів, нагороди-трофеї за місяць.
- `hints-window` (sudoku.com) — пояснення техніки кроку текстом поверх поля.
- `help-window` — правила (`/sudoku-rules/`) і поради (`/how-to-play/`).
- SudokuPad: `settings-window` (тема, перевірка конфліктів, приховати таймер (?)), `custom-window` «Rules» — текст правил пазла.
- Переходи: main-menu → difficulty-select → game-screen → (3 помилки) game-over-continue / (розвʼязано) end-screen → main-menu.

## Фічі поза полем
- `difficulty-presets` за технікою (а не за кількістю підказок): Tatham — Trivial/Basic/Intermediate/Advanced/Extreme/Unreasonable; sudoku.com — 6 рівнів.
- `hint` з поясненням техніки (`+feature:technique-hints`), `auto-check` проти розвʼязку, `mistake-limit` 3, `undo`/`redo`, `+feature:auto-candidates` (заповнити всі нотатки) (?).
- `daily-puzzle` + `streaks` + нагороди за місяць; `stats` по рівнях (найкращий/середній час, % без помилок).
- `puzzle-bank` (класика CtC — ручні пазли сетерів), `seed-input`/`share-code` (Tatham Game ID, SudokuPad — лінк на пазл).
- `autosave` незавершеної партії; `theme-select` (темна тема); `custom-difficulty` у Tatham — розмір блоків, симетрія, X/Jigsaw/Killer.

## Варіації й родичі
- Розмір: 4×4, 6×6, 16×16, 25×25; нерегулярні блоки (Jigsaw); діагоналі (Sudoku-X); мульти-сітки (Samurai/Gattai-5).
- Додаткові обмеження — окремий файл [sudoku-variants](sudoku-variants.md) (Killer, Thermo, Arrow, Kropki…).
- Родичі: латинський квадрат (без блоків), KenKen, Kakuro, Futoshiki — та сама «цифра без повтору в домі» + інша підказка.
- **Осі варіацій**: геометрія доменів (рядок/стовпець/блок/діагональ/нерегулярні) · джерело підказок (givens / суми / нерівності / зовнішні) · що перевіряє плеєр (нічого / правила / розвʼязок) · ціна помилки (нічого / лічильник / програш / штраф часу).

## Цікавинки для курсу
- Перевірка валідності: конфлікти в 27 домах + підсвітка — 🌱 (картка `markup-validity` є).
- Два види нотаток (кут/центр) + мультивиділення + режими вводу — 🥉 (стан клітинки з трьох шарів, UX режимів).
- Підсвітка «peer»-клітинок і однакових цифр — 📎.
- Розвʼязувач backtracking / Dancing Links — 🥈; розвʼязувач **людськими техніками** (single → pairs → pointing → X-wing) з поясненням кроку = кнопка hint — 🥇.
- Генерація з єдиним розвʼязком + оцінка складності за найважчою потрібною технікою — 👑 (`unique-puzzle-generation` + `difficulty-rating`).
- Ліміт 3 помилки + звірка з розвʼязком + daily з календарем — 📎.

## Мапа на каталог
- Є: `markup-validity` ↔ конфлікти рядка/стовпця/блока · `completion-detection` + `satisfy-constraints` ↔ перемога · `pencil-marks` ↔ кутові/центральні нотатки · `cell-click`, `hover-highlight`, `keyboard-controls` ↔ ввід · `difficulty-levels` + `difficulty-rating` ↔ рівні за технікою · `unique-puzzle-generation` ↔ генератор · `level-solver` ↔ hint/solve · `daily-puzzle`, `level-bank` ↔ daily/банк · `import-open-formats` ↔ рядок з 81 символу, Tatham Game ID · `wrong-mark-lose` ↔ 3 помилки · `score-records`, `profile-stats` ↔ статистика · `save-autosave` ↔ продовжити · `end-screen`.
- **Нема** → пропозиції карток:
  - `+digit-highlight` «Підсвітка однакових цифр і peer-клітинок» · interface/input · 📎.
  - `+auto-candidates` «Автозаповнення нотаток і авто-видалення» · interface/input · 🥉.
  - `+technique-hint` «Підказка з назвою техніки» · levels/solvability · 🥇 · слот {techniques: list}.
  - `+multi-select` «Мультивиділення клітинок» · interface/input · 📎.
  - `+cell-coloring` «Кольорова розмітка клітинок» · interface/input · 🌱.

## Пропозиції до словників
- `+ui:number-pad` — екранна панель цифр 1–9 (часто з лічильником, скільки лишилось поставити).
- `+ui:digit-highlight` — підсвітка всіх клітинок з тією ж цифрою; `+ui:peer-highlight` — підсвітка дому вибраної клітинки.
- `+ui:color-palette` — палітра кольорів для розмітки клітинок (SudokuPad Colour).
- `+feature:auto-candidates` — автонотатки й авто-видалення кандидатів після ходу.
- `+feature:technique-hints` — підказка, що називає й пояснює техніку.
- `+feature:second-chance` — продовжити після програшу (за рекламу) — родич `game-over-continue`.
- `+effect:clear_notes` — стерти нотатку цифри в peer-клітинках після вводу.
- `+card:multi-select` — дія над набором клітинок (див. мапу).

## Джерела
- ⭐ [Sudoku.com](https://sudoku.com/) — живий плеєр: 6 рівнів, Mistakes 0/3, Notes, Hint з поясненням, Undo/Erase, Daily Challenges; правила `/sudoku-rules/`.
- [Wikipedia: Sudoku](https://en.wikipedia.org/wiki/Sudoku) — правила, Number Place 1979, Nikoli 1984/1986, мінімум 17 підказок, NP-повнота, варіанти розмірів.
- [Nikoli: Sudoku](https://www.nikoli.co.jp/en/puzzles/sudoku/) — офіційні правила, симетрія підказок, торгова марка.
- [SudokuPad](https://sudokupad.app/) — режими Digit/Corner/Centre/Colour, гарячі клавіші, мультивиділення, Check.
- [Tatham Solo](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/solo.html) — керування pencil marks, рівні складності за технікою, X/Jigsaw/Killer.
- [SudokuWiki: Strategy Families](https://www.sudokuwiki.org/Strategy_Families) — ієрархія технік (Basic → Tough → Diabolical → Extreme) = порядок, у якому їх пробує розвʼязувач.
- [GM Puzzles: Sudoku rules](https://www.gmpuzzles.com/blog/sudoku-rules-and-info/) — канонічне формулювання правил.
- [Steam: Classic Sudoku (CtC)](https://store.steampowered.com/app/1188330/Classic_Sudoku/) — ручні пазли з підказками-поясненнями.
- [YouTube: Cracking the Cryptic](https://www.youtube.com/c/CrackingTheCryptic) — розвʼязання вголос у SudokuPad.

## Непевне
- (?) Авто-видалення нотаток, лічильник лишку на цифрах `number-pad`, приховування поля на паузі — бачив у плеєрах, у джерелах сесії не підтверджено.
- (?) Набір налаштувань SudokuPad (перевірка конфліктів одразу чи лише за Check, приховати таймер) — сторінка показує тільки гарячі клавіші.
- (?) Як sudoku.com рахує очки — сторінка показує лише кубок/рахунок без формули.
- (?) Naked/hidden single як нижній рівень — у SudokuWiki в меню не названі, але це стандартні «синґли» (Tatham Basic: «завжди є клітинка з однією цифрою»).
