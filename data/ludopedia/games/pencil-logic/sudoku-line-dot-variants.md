---
title: Sudoku line & dot variants (Thermo, Arrow, Kropki, German Whispers)
slug: sudoku-line-dot-variants
aka: [Термометр-судоку, Thermo-Sudoku, Стрілкове судоку, Arrow Sudoku, Kropki Sudoku, Kropki Pairs, Consecutive Pairs Sudoku, Крапки, German Whispers, Німецькі шепоти, Dutch Whispers, Renban, Ренбан, Renban Sudoku]
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
year: 2019
platforms: [paper, web, mobile, PC]
links:
  - {kind: other, url: "https://artisanalsudoku.substack.com/p/the-basics-of-popular-sudoku-variants", best: true, note: "Whispers, Kropki, Arrow — правила й перші висновки (нема 5 на whisper, пари чорної крапки, мінімуми стрілок)"}
  - {kind: official, url: "https://www.gmpuzzles.com/blog/category/sudoku/thermo-sudoku/", note: "GM Puzzles: Thermo, Slow Thermo, Anti-King Thermo, Thermo-Kropki Pairs — тексти правил"}
  - {kind: official, url: "https://www.gmpuzzles.com/blog/category/sudoku/arrow-sudoku/", note: "GM Puzzles: Arrow, двоцифрова капсула, Overflowing, ≤, Alternating Parity"}
  - {kind: official, url: "https://www.gmpuzzles.com/blog/category/sudoku/consecutive-pairs-sudoku/", note: "GM Puzzles: білі кружки «різниця 1», без кружка — будь-що"}
  - {kind: official, url: "https://www.gmpuzzles.com/blog/category/sudoku/consecutive-sudoku/", note: "GM Puzzles: Consecutive (риска; без риски — не послідовні) і Nonconsecutive"}
  - {kind: official, url: "https://www.gmpuzzles.com/blog/?p=35009", note: "Philip Newman, German/Dutch Whispers: зелена ≥5, помаранчева ≥4"}
  - {kind: official, url: "https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000557", note: "LMG: German Whispers — «новинка WSC 2019 у Німеччині»"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/kropki.js", note: "puzz.link Kropki: латинський квадрат N×N, усі крапки дано, коди помилок"}
  - {kind: play, url: "https://sudokupad.app/", note: "SudokuPad: режими Digit/Corner/Centre/Colour, приклад Arrow Sudoku (Eric Fox)"}
  - {kind: official, url: "https://puzzles.mit.edu/sudokuopen/2024/variants-i.pdf", note: "MIT Sudoku Open 2024: турнірне формулювання Renban (і Antiknight, Consecutive Pairs, Kropki Lines)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=german+whispers+sudoku+cracking+the+cryptic", note: "пошук; розвʼязання CtC"}
stage: v1
coverage: 60
mechanics: [markup-validity, completion-detection, satisfy-constraints, conflict-highlight, pencil-marks, cell-click, keyboard-controls, line-sum-clue, level-bank, level-solver, import-open-formats, in-game-editor, +undo-redo, +line-constraints, +dot-constraints, +constraint-overlay, +multi-select, +cell-coloring, +negative-constraint, +latin-square]
proposes: ["+cond:increasing", "+cond:diff", "+cond:ratio", "+role:line", "+role:edge-clue", "+card:negative-constraint", "+card:latin-square", "+axis:clue-completeness", "+cond:consecutive_set"]
author: opus
date: 2026-11-09
---

# Sudoku line & dot variants — термометри, стрілки, крапки й «шепоти» поверх класичної сітки

## Суть
Чотири найпоширеніші модулі-обмеження сучасного варіантного судоку, описані разом, бо всі вони — **відношення між сусідніми цифрами**, намальоване лінією чи крапкою: Thermo (строго зростає від колби), Arrow (сума на стрілці = цифра в кружку), Kropki (біла крапка — різниця 1, чорна — відношення 1:2), German Whispers (сусіди на лінії різняться ≥ 5). Базові правила — [sudoku](sudoku.md); каталог модулів — [sudoku-variants](sudoku-variants.md). Цей файл додає те, чого там нема: підваріанти кожного модуля, позитивні/негативні формулювання, ключові висновки-«break-in» і окрему таблицю обмежень.

## Поле і час
- Сітка 9×9 з рядками, стовпцями й блоками 3×3 (GM Puzzles); puzz.link Kropki — латинський квадрат N×N без блоків, цифри 1…N.
- Лінії (термометр, стрілка, whisper) — послідовності ортогонально чи діагонально сусідніх клітинок поверх сітки; крапка (Kropki) — на ребрі між двома ортогональними сусідами.
- Час статичний; хід = вписати цифру / олівцеву позначку / колір.

### Таблиця обмежень по варіантах
| Варіант | Елемент | Обмеження | Повтори на елементі | Без елемента | Ключовий висновок |
|---|---|---|---|---|---|
| Thermo | колба + лінія | строго зростає від колби до плаского кінця | неможливі | — | на термометрі довжини L: колба ≤ 10−L, i-та клітинка ∈ [i, 9−L+i] |
| Slow Thermo | те саме | зростає або стоїть (приклад GM: 233577888) | можливі | — | слабше: лише нижня/верхня межі без зсуву |
| Arrow | кружок + стрілка | сума цифр на стрілці = цифра в кружку | можливі, якщо дозволяє судоку | — | стрілка в межах одного блоку з k клітинок ≥ 1+2+…+k; на багатоклітинній стрілці нема 9 |
| Arrow (капсула) | 2-клітинна «пігулка» | сума = двоцифрове число зліва направо | можливі | — | капсула 1x → стрілка дає 10–19 |
| Overflowing Arrow | кружок + стрілка | сума всіх, крім однієї клітинки, = кружок | можливі | — | гравець шукає «зайву» клітинку |
| ≤ Arrow | кружок + стрілка | сума ≤ кружка | можливі | — | лише верхня межа |
| Alternating Parity Arrow | кружок + стрілка | парність чергується вздовж стрілки разом з кружком | — | — | немає суми, лише парність |
| Kropki (puzz.link) | біла / чорна крапка | біла — різниця 1; чорна — одна цифра вдвічі більша | — | **негативне**: сусіди без крапки не послідовні й не 1:2 | латинський квадрат, усі крапки дано |
| Kropki Pairs / Consecutive Pairs (GM) | білий (і чорний) кружок | біла — різниця 1; чорна — відношення 2 | — | будь-що | чорна: лише 1-2, 2-4, 3-6, 4-8; 5, 7, 9 — ніколи на чорній |
| Consecutive (GM) | риска | різниця 1 | — | **негативне**: без риски — не послідовні | біла крапка = одна парна + одна непарна |
| Nonconsecutive (GM) | — | жодні ортогональні сусіди не послідовні | — | — | глобальна версія того самого |
| German Whispers | зелена лінія | сусіди на лінії різняться ≥ 5 | можливі, якщо дозволяє судоку | — | нема 5; низькі 1–4 і високі 6–9 чергуються; 4 лише поруч з 9, 6 — з 1 |
| Dutch Whispers | помаранчева лінія (Newman) | різниця ≥ 4 | можливі | — | 5 можлива (поруч з 1 або 9) |
| Renban | фіолетова (MIT — сіра) лінія | набір різних послідовних цифр у будь-якому порядку | неможливі | — | лінія довжини L ≥ 5 завжди містить 10−L…L; див. підрозділ «Renban» |

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Цифрова клітинка | mark | 1–9 (або 1–N) · олівці · колір | приймає цифру; належить рядку, стовпцю, блоку |
| Рядок / стовпець / блок | zone | 9 клітинок | без повторів (базове судоку) |
| Колба термометра | mark | початок лінії | найменша цифра термометра |
| Тіло термометра | zone | упорядкована лінія | цифри строго зростають від колби (Slow — неспадають) |
| Кружок стрілки | mark | 1 клітинка або 2-клітинна капсула | значення = сума на стрілці (капсула — двоцифрове число) |
| Тіло стрілки | zone | упорядкована лінія від кружка | цифри сумуються; повтори дозволені |
| Біла крапка Kropki | mark | ребро між 2 сусідами | цифри послідовні |
| Чорна крапка Kropki | mark | ребро між 2 сусідами | одна цифра = 2 × інша |
| Риска Consecutive | mark | ребро | цифри послідовні; у Consecutive відсутність риски — заборона |
| Лінія German Whispers | zone | зелена лінія | сусіди на лінії різняться ≥ 5 |
| Лінія Dutch Whispers | zone | помаранчева лінія | сусіди різняться ≥ 4 |

## Правила (КОЛИ → ЯКЩО → ТО)
- Завжди: КОЛИ `input(digit)` → ЯКЩО `not unique(row|col|box)` → ТО `constraint_broken(sudoku)` (базові правила; у puzz.link Kropki — лише рядок/стовпець, `nmDupRow`).
- Thermo: КОЛИ `input(digit)` на термометрі → ЯКЩО `not custom: «строго більша за попередню від колби»` (`+cond:increasing`) → ТО `constraint_broken(thermo)`.
- Slow Thermo: те саме, але ЯКЩО `custom: «менша за попередню»` → ТО `constraint_broken(slow_thermo)`; рівність дозволена.
- Arrow: КОЛИ `custom: «стрілка повна»` → ЯКЩО `not sum(arrow, circle)` → ТО `constraint_broken(arrow)`.
- Arrow-капсула: ЯКЩО `not sum(arrow, custom: «число з цифр капсули зліва направо»)` → ТО `constraint_broken(arrow_pill)`.
- Overflowing Arrow: ЯКЩО `custom: «нема клітинки, без якої сума = кружок»` → ТО `constraint_broken(overflow_arrow)`.
- ≤ Arrow: ЯКЩО `custom: «сума стрілки > кружка»` → ТО `constraint_broken(arrow_le)`.
- Alternating Parity Arrow: ЯКЩО `same(neighbor_a, neighbor_b, parity)` на стрілці з кружком → ТО `constraint_broken(parity_arrow)`.
- Kropki біла: КОЛИ `input(digit)` біля білої крапки → ЯКЩО `not custom: «|a−b| = 1»` (`+cond:diff`) → ТО `constraint_broken(white)` (`nmSubNe1`).
- Kropki чорна: ЯКЩО `not custom: «a = 2b або b = 2a»` (`+cond:ratio`) → ТО `constraint_broken(black)` (`nmDivNe2`).
- Kropki негативне: ЯКЩО `mode(all_dots_given)` and `custom: «нема крапки»` and `custom: «|a−b| = 1»` → ТО `constraint_broken(missing_white)` (`nmSubEq1`); те саме для 1:2 → `nmDivEq2`.
- Consecutive: ЯКЩО `custom: «нема риски»` and `custom: «|a−b| = 1»` → ТО `constraint_broken(consecutive)`; Nonconsecutive — для всіх ортогональних пар.
- German Whispers: КОЛИ `input(digit)` на лінії → ЯКЩО `custom: «|a−b| < 5 для сусідів на лінії»` → ТО `constraint_broken(whisper)`.
- Dutch Whispers: те саме з порогом 4.
- КОЛИ `constraint_broken(*)` → ТО `custom: «підсвітити елемент (лінію/крапку) і клітинки»` (`conflict-highlight`).
- КОЛИ `custom: «є порожня клітинка»` при перевірці → ТО `constraint_broken(empty)` (`ceNoNum`).
- КОЛИ `all_constraints_met` → ТО `win`.
- Висновки-«break-in» (не правила гри, але суть розвʼязання):
  - Whisper: 5 на лінії неможлива; дві сусідні клітинки лінії — одна з 1–4, друга з 6–9; 4 у середині лінії потребує двох 9 — у одному блоці неможливо, тож 4 і 6 тяжіють до кінців.
  - Kropki: два чорні поспіль без повтору — 1-2-4 або 2-4-8, середина — 2 або 4; біла пара — завжди парна + непарна.
  - Arrow: різні цифри на стрілці з k клітинок дають суму ≥ k(k+1)/2; дві кружки зі стрілками сумарно ≥ 15 можуть змусити пару 7-8.
  - Thermo: термометр довжини 9 фіксує 1…9; довгий термометр звужує кожну клітинку до вікна ширини 10−L.
- Перемога: усі клітинки заповнені, базові й модульні обмеження виконані. Поразки нема; рахунок — час (застосунки) (?).

## Керування і ввід
- SudokuPad: режими Digit (Z) · Corner (X) · Centre (C) · Colour (V), перемикання Space/PgDown; Shift/Ctrl/Ctrl+Shift — ввід у режим без перемикання; мультивиділення мишею/дотиком/клавіатурою, select all, invert selection; undo/redo.
- Колір — основний інструмент для whispers (низькі/високі) і Kropki (парність).
- puzz.link Kropki: ввід цифр у клітинку клавіатурою/кліком; у редакторі — крапки на ребрах (?).
- Папір (GM Puzzles): PDF-пазл, ручка й олівець.

## Вікна, меню, HUD
- `game-screen` (SudokuPad): поле з шарами — термометри сірими лініями з колбою, стрілки з кружками, крапки на ребрах, кольорові лінії whispers; `+ui:rules-panel` (правила пазла); `pencil-marks` (corner/centre); `undo-button`/`redo-button`; `check-button` — перевіряє лише базові правила судоку (SudokuPad help).
- `game-screen` (puzz.link Kropki): сітка, крапки, кнопка перевірки з кодом першої помилки.
- `help-window`: SudokuPad — довідка гарячих клавіш і приклади пазлів; GM Puzzles — сторінка правил категорії.
- `puzzle-select` (цифрова версія): GM — стрічка блогу за категоріями (Thermo, Arrow, Consecutive Pairs…), SudokuPad — список прикладів.
- `editor-window` (цифрова версія): f-puzzles / SudokuPad maker — палітра «лінія термометра / стрілка / крапка / whisper» (?).

## Фічі поза полем
- `custom-rules` як суть: кожен пазл декларує свій набір модулів текстом (GM: «Standard Sudoku rules» + абзац модуля); комбінації — Thermo-Kropki Pairs, Anti-King Thermo, Arrow Consecutive Pairs, Consecutive Pairs Killer, German/Dutch Whispers в одному пазлі.
- `auto-check` за кнопкою (puzz.link — код помилки; SudokuPad — лише базові правила).
- `undo`/`redo`, `level-sharing` через короткий URL (SudokuPad, puzz.link).
- `puzzle-bank`: GM Puzzles — регулярні пазли з бонусною «складнішою версією» (Sumbeams → Partly Summy).

## Варіації й родичі
- **Осі варіацій**:
  - тип відношення: порядок (Thermo) · сума (Arrow) · різниця = 1 (Kropki біла, Consecutive) · відношення 1:2 (Kropki чорна) · різниця ≥ k (Whispers: German 5, Dutch 4);
  - строгість: строго / нестрого (Slow Thermo) · рівно / ≤ (Arrow) · усі / усі крім однієї (Overflowing);
  - повнота підказок: «дано не всі» (Kropki Pairs, Consecutive Pairs) / «дано всі — відсутність теж підказка» (puzz.link Kropki, Consecutive) / глобально без підказок (Nonconsecutive);
  - кодування числа: одна клітинка / капсула-двоцифрове (Arrow).
- Родичі: [kakuro](kakuro.md) і Killer — суми без лінії; Futoshiki — порядок на ребрі (знаки < >); Greater Than Sudoku (Wikipedia) — 12 знаків між сусідами в блоці; [sudoku-variants](sudoku-variants.md) — Renban, Palindrome, Region Sum, Between — інші лінії того ж класу; [takuzu](takuzu.md) — бінарний аналог латинського квадрата.
- German Whispers — наймолодший із чотирьох: LMG називає перший такий пазл «новинкою WSC 2019 у Німеччині».

### Renban — лінія з набором послідовних цифр у будь-якому порядку
- Правило (MIT Sudoku Open 2024, Renban Sudoku): «Gray lines must contain a set of distinct, consecutive digits in any order». Цифри на лінії різні навіть між різними блоками й разом утворюють відрізок натурального ряду; колір — сірий у MIT, фіолетовий в Artisanal Sudoku.
- Відмінність від решти ліній файла: Renban — предикат над **множиною** цифр лінії, а не над сусідніми парами, тож порядок на лінії не важить і лінія може бути будь-якої форми.
- КОЛИ `input(digit)` на лінії → ЯКЩО `not unique(line)` → ТО `constraint_broken(renban)`.
- КОЛИ `input(digit)` на лінії → ЯКЩО `custom: «max − min > L − 1»` (`+cond:consecutive_set`) → ТО `constraint_broken(renban)` — конфлікт видно ще до заповнення лінії; на повній лінії без повторів умова `max − min = L − 1` рівносильна всьому правилу.
- Висновки-«break-in» (Artisanal Sudoku): 2-клітинна ортогональна лінія = біла крапка Kropki (парна + непарна); 4-клітинна лінія з 1 — рівно 1–4; лінія довжини L ≥ 5 завжди містить середні цифри 10−L…L (5 → 5; 6 → 4, 5, 6; 7 → 3–7; 8 → усе, крім 1 або 9) — те саме «вікно», що в термометра, але без порядку.
- Цікавинка: перевірка через множину (`len(set) = L` і `max − min = L − 1`) — 🌱; звуження кандидатів «вікном» на неповній лінії — 📎.
- Родичі: Kropki біла крапка й Consecutive — та сама «послідовність» для пари; [sudoku-variants](sudoku-variants.md) — Renban у загальному каталозі модулів; Nabner — протилежний модуль у черзі (?).

## Цікавинки для курсу
- Лінія як упорядкований список клітинок + предикат над сусідніми парами (`increasing`, `diff ≥ k`) — 🌱 на модуль, 📎 як спільний клас «pairwise-line».
- Крапки на ребрах: зберігання (між клітинками) і рендер — 📎; негативне обмеження «усі дано» — 🌱 прапорець, але тест на всі пари без крапки цікавий.
- Arrow з капсулою (двоцифрове число з двох клітинок) — 🌱; Overflowing («усі, крім однієї») — 📎.
- Звуження кандидатів за модулями (вікно термометра, «нема 5 на whisper», пари чорної крапки) у розвʼязувачі-пропагаторі — 🥉.
- Повний розвʼязувач судоку з модулями як плагінами `check(grid)` + `prune(candidates)` — 🥇.
- Генератор варіантного пазла з мінімумом givens і єдиним розвʼязком — 👑.

## Мапа на каталог
- Є: `markup-validity`, `conflict-highlight` ↔ порушені лінії/крапки · `completion-detection`, `satisfy-constraints` · `pencil-marks`, `cell-click`, `keyboard-controls` ↔ SudokuPad · `line-sum-clue` ↔ сума на стрілці · `level-bank` ↔ GM/SudokuPad · `level-solver`, `in-game-editor`, `import-open-formats` ↔ URL пазлів.
- Перевикористано з [sudoku-variants](sudoku-variants.md): `+line-constraints`, `+dot-constraints`, `+constraint-overlay`, `+multi-select`, `+cell-coloring`.
- **Нема** → пропозиції карток:
  - `+negative-constraint` «Відсутність підказки — теж підказка» · game-logic/constraints · 🌱 · слот {all_given: bool} — Kropki, Consecutive, XV.
  - `+latin-square` «Латинський квадрат N×N без блоків» · game-logic/constraints · 🌱 — puzz.link Kropki, KenKen, Futoshiki.

## Пропозиції до словників
- `+cond:increasing` — значення на упорядкованій лінії строго (або нестрого, слот `strict`) зростають.
- `+cond:diff` — |a − b| порівняно з N (`= 1` Kropki, `≥ 5` German Whispers, `≥ 4` Dutch).
- `+cond:ratio` — a = k·b або b = k·a (Kropki чорна, k = 2).
- `+role:line` — упорядкована лінія клітинок (повтор із sudoku-variants і herugolf).
- `+role:edge-clue` — підказка на ребрі між двома клітинками (крапка, риска, знак <).
- `+card:negative-constraint`, `+card:latin-square` — див. мапу.
- `+axis:clue-completeness` — `partial` (дано не всі) / `complete` (відсутність = заборона) / `global` (правило без підказок).
- `+cond:consecutive_set` — значення на лінії/в групі різні й утворюють відрізок натурального ряду (Renban).

## Джерела
- ⭐ [Artisanal Sudoku: basics of popular variants](https://artisanalsudoku.substack.com/p/the-basics-of-popular-sudoku-variants) — Whispers (нема 5, чергування, 4↔9, 6↔1), Kropki (4 пари чорної, 5/7/9), Arrow (мінімуми, 7-8 з двох кружків).
- [GM Puzzles: Thermo-Sudoku](https://www.gmpuzzles.com/blog/category/sudoku/thermo-sudoku/) — правило «strictly increasing from the round bulb to the flat end», Slow Thermo (233577888), Anti-King Thermo, Thermo-Kropki Pairs.
- [GM Puzzles: Arrow Sudoku](https://www.gmpuzzles.com/blog/category/sudoku/arrow-sudoku/) — повтори на стрілці, капсула, Overflowing, ≤, Alternating Parity.
- [GM Puzzles: Consecutive Pairs](https://www.gmpuzzles.com/blog/category/sudoku/consecutive-pairs-sudoku/) — білий кружок = різниця 1, без кружка — будь-що; старіше формулювання «not all gray circles are given».
- [GM Puzzles: Consecutive Sudoku](https://www.gmpuzzles.com/blog/category/sudoku/consecutive-sudoku/) — риска / без риски не послідовні; Nonconsecutive.
- [GM Puzzles: German/Dutch Whispers (Newman, 2026-02-10)](https://www.gmpuzzles.com/blog/?p=35009) — зелена ≥ 5, помаранчева ≥ 4.
- [LMG: DSM Qualitraining 2021: German Whispers](https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000557) — правило німецькою; перший German Whispers — новинка WSC 2019.
- [puzz.link kropki.js](https://puzz.link/js/pzpr-samples/kropki.js) — латинський квадрат, усі крапки дано, коди `nmDupRow nmSubNe1 nmSubEq1 nmDivNe2 nmDivEq2 ceNoNum`.
- [SudokuPad](https://sudokupad.app/) — режими вводу, Check лише базових правил, приклад Arrow Sudoku (Eric Fox).
- [Wikipedia: Sudoku](https://en.wikipedia.org/wiki/Sudoku) — розділ варіантів: лише Greater Than Sudoku; Thermo/Arrow/Kropki/Whispers не згадані.
- [MIT Sudoku Open 2024 Variants I](https://puzzles.mit.edu/sudokuopen/2024/variants-i.pdf) — правило Renban Sudoku (сірі лінії, «distinct, consecutive digits in any order»).

## Непевне
- (?) `year: 2019` — рік German Whispers (LMG); дати появи Thermo, Arrow і Kropki не знайшов (Wikipedia їх не описує).
- (?) Як puzz.link/Kropki-судоку трактують пару 1-2 під негативним правилом (обидві крапки можливі — яку малювати): правило в kropki.js цього не уточнює.
- (?) Значення кодів puzz.link виведені з назв і тестів.
- (?) Хто автор German Whispers і звідки назва — LMG лише «новинка WSC 2019»; атрибуцію Axel Gebhardt (сторонній сайт) не підтвердив.
- (?) Колір Dutch Whispers «помаранчевий» — лише в одному пазлі Newman; конвенції нема.
- (?) Рахунок часу й редактори f-puzzles для цих модулів — з памʼяті, сторінок не відкривав.
- (?) Renban: автора й рік появи не знайшов; Nabner («жодні дві цифри на лінії не послідовні») — лише назва в черзі, правило з памʼяті; формула «середні цифри 10−L…L» для L = 9 у джерелі не названа, виведена.
