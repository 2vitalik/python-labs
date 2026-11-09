---
title: Sudoku variants (варіанти судоку, Cracking the Cryptic / SudokuPad)
slug: sudoku-variants
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
year: 2005
platforms: [paper, web, mobile, PC]
links:
  - {kind: official, url: "https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000OGK", best: true, note: "LMG «Confined Constraints» (Burak Alver, 2025): класика + 8 модулів з точними правилами + лінк SudokuPad"}
  - {kind: play, url: "https://sudokupad.app/plzx2drps0", note: "той самий пазл у SudokuPad — як рендеряться лінії, клітки, крапки, X/V, стрілки"}
  - {kind: official, url: "https://crackingthecryptic.com/apps", note: "застосунки CtC: Sandwich, Chess, Thermo, Miracle, Killer, Arrow, Domino, Lines, Fog of War"}
  - {kind: official, url: "https://www.crackingthecryptic.com/sudoku?id=2865", note: "Fog of War + Little Killer, X-Sums, Renban, Whisper, Region Sum"}
  - {kind: play, url: "https://sudokupad.app/hvtrbv1n24", note: "Fog of War у SudokuPad"}
  - {kind: official, url: "https://logic-masters.de/Raetselportal/", note: "Logic Masters Germany: 37 359 пазлів (2026-11), теги варіантів, складність 1–5"}
  - {kind: official, url: "https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000LRL", note: "Skyscraper Fog: туман сходить по лініях видимості"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Killer_sudoku", note: "Killer: історія (Nishio, The Times 2005), сума 45 у регіоні, innies/outies"}
  - {kind: official, url: "https://puzzles.mit.edu/sudokuopen/2024/variants-i.pdf", note: "MIT Sudoku Open: точні тексти правил Antiknight, Kropki lines, Odd/Even, Renban, X-Sums"}
  - {kind: official, url: "https://puzzles.mit.edu/sudokuopen/2023/variants-i.pdf", note: "MIT 2023: Palindrome, Little Killer, Sandwich, Quadruples, Thermo, Arrow"}
  - {kind: steam, url: "https://store.steampowered.com/app/3165770/Cracking_the_Cryptic__Fog_of_War_1/", note: "CtC Fog of War 1"}
  - {kind: youtube, url: "https://www.youtube.com/c/CrackingTheCryptic", note: "канал — варіанти в SudokuPad щодня"}
  - {kind: steam, url: "https://store.steampowered.com/app/1117310/Sandwich_Sudoku/", note: "CtC Sandwich Sudoku (2019): правило «сума між 1 і 9», 40→100 рівнів"}
  - {kind: steam, url: "https://store.steampowered.com/app/1377260/Miracle_Sudoku/", note: "CtC Miracle Sudoku (2020): Non-Consecutive, Miracle, NC Thermo, NC Sandwich"}
  - {kind: steam, url: "https://store.steampowered.com/app/1250560/Chess_Sudoku/", note: "CtC Chess Sudoku (2020): Knight, King, Queen — тексти правил"}
  - {kind: other, url: "https://ethmcc.github.io/miracle-sudoku", note: "On Miracle Sudoku: правила, 72 повні сітки, 174 816 пар даних з єдиним розвʼязком"}
stage: v2
coverage: 55
mechanics: [markup-validity, completion-detection, satisfy-constraints, pencil-marks, cell-click, keyboard-controls, level-bank, level-rating, import-open-formats, in-game-editor, level-exchange, level-solver, +constraint-overlay, +killer-cage, +line-constraints, +dot-constraints, +outside-clues, +chess-move-constraint, +fog-reveal, +irregular-regions, +multi-select, +cell-coloring]
proposes: ["+role:line", "+role:clue-outside", "+trigger:reveal_by_correct", "+effect:reveal", "+ui:rules-panel", "+feature:custom-rules", "+axis:rule-composition", "+cond:sum_between", "+cond:knight_move"]
author: opus
date: 2026-11-02
---

# Sudoku variants — класична сітка 9×9 + модулі-обмеження, намальовані поверх

## Суть
Варіант = класичне судоку (рядок/стовпець/блок без повторів) **плюс** один або кілька графічних елементів-обмежень: клітки з сумою, лінії, крапки між клітинками, підказки ззовні, шахові заборони, туман. Givens часто майже нема — інформацію несуть обмеження, і пазл «розкривається» через «break-in» (перший неочевидний висновок). Цифрова сцена (Cracking the Cryptic, SudokuPad, f-puzzles, Logic Masters Germany) перетворила це на конструктор: сетер комбінує модулі, плеєр малює їх шарами й перевіряє розвʼязок.

## Поле і час
- Поле — сітка 9×9 (іноді 6×6, 8×8) з доменами судоку; Jigsaw замінює блоки нерегулярними регіонами.
- **Шари рендеру** (SudokuPad): фон клітинок (сірі/кольорові, туман) → лінії (thermo, whispers, renban…) → межі кліток (пунктир) → крапки/X/V на ребрах → кружки й стрілки → цифри/нотатки → підказки поза сіткою (рамка навколо поля).
- Поле поза сіткою: зовнішнє кільце для Sandwich, X-Sums, Skyscrapers, Little Killer (стрілка по діагоналі).
- Час статичний. Fog of War — єдиний «динамічний» модуль: правильна цифра відкриває частину поля (стан поля залежить від історії вводу).

## Сутності
| Сутність (обмеження) | Роль | Параметри | Поведінка (правило) |
|---|---|---|---|
| Killer-клітка | zone | сума у верхньому лівому куті | цифри не повторюються в клітці й дають суму; рендер — пунктирна рамка |
| Термометр | zone | колба + лінія | цифри строго зростають від колби; рендер — сіра товста лінія з кругом |
| Стрілка (Arrow) | zone | кружок + лінія зі стрілкою | сума цифр на стрілці = цифра в кружку; повтори можливі, якщо судоку дозволяє |
| Kropki біла крапка | mark | між 2 сусідами | цифри послідовні (різниця 1) |
| Kropki чорна крапка | mark | між 2 сусідами | відношення 1:2; «не всі крапки дано» — негативне обмеження |
| XV | mark | X або V на ребрі | X — сума 10, V — сума 5; часто «не всі дано» |
| German Whispers | zone | зелена лінія | сусіди на лінії різняться ≥ 5 (5 на лінії неможлива, low/high чергуються) |
| Renban | zone | фіолетова лінія | набір різних послідовних цифр у будь-якому порядку |
| Palindrome | zone | сіра лінія | цифри однакові з обох кінців (читається однаково) |
| Region Sum line | zone | синя лінія | сегменти лінії, розрізані межами блоків, мають рівні суми |
| Between line | zone | лінія між двома кружками | цифри на лінії строго між значеннями в кружках (?) |
| Odd / Even | mark | кружок / квадрат у клітинці | непарна / парна цифра |
| Little Killer | mark | число + діагональна стрілка ззовні | сума діагоналі = число; повтори на діагоналі можливі |
| Sandwich | mark | число ззовні рядка/стовпця | сума цифр між 1 і 9 у цьому ряду |
| X-Sums | mark | число ззовні | сума перших N цифр від краю, де N — перша цифра |
| Skyscraper | mark | число ззовні | скільки «будинків» видно від краю; вища цифра ховає нижчі |
| Anti-knight | zone | глобальне | однакові цифри не на відстані ходу коня |
| Anti-king | zone | глобальне | однакові цифри не на відстані ходу короля (по суті — діагональні сусіди) |
| Jigsaw (Irregular) | zone | нерегулярні регіони | замість блоків 3×3 — 9 фігур по 9 клітинок |
| Extra region | zone | сірі клітинки | ще один дім 1–9 |
| Quadruple | mark | кружок на перетині 4 клітинок | перелічені цифри є серед 4 клітинок |
| Туман (Fog of War) | mark | закриті клітинки | правильна цифра розвіює туман навколо / по лініях видимості / де задумав сетер |

## Правила (КОЛИ → ЯКЩО → ТО)
- Базові правила [sudoku](sudoku.md) (`unique_in_row|col|box`) діють завжди; кожен модуль — ще одна функція перевірки над набором клітинок.
- КОЛИ `constraint_broken(cage_sum|cage_unique)` → ТО `custom: «conflict-highlight клітки»`.
- КОЛИ `constraint_broken(thermo_increasing)` → ТО конфлікт: `custom: «сусіди на термометрі не зростають»`.
- КОЛИ `constraint_broken(arrow_sum)` / `(whisper_diff≥5)` / `(renban_consecutive)` / `(palindrome)` / `(region_sum_equal)` / `(between)` → ТО `custom: «conflict-highlight лінії»`.
- КОЛИ `constraint_broken(kropki_white|kropki_black|x|v)` → ТО `custom: «conflict-highlight ребра»`; ЯКЩО `mode(negative_constraint)` («усі крапки дано») → ТО й відсутня крапка між послідовними — порушення.
- КОЛИ `constraint_broken(sandwich|x_sum|skyscraper|little_killer)` → ТО `custom: «conflict-highlight підказки ззовні»` — перевіряється лише коли ряд повний (?).
- КОЛИ `constraint_broken(anti_knight|anti_king)` → ТО `custom: «дві однакові цифри на відстані ходу фігури»`.
- КОЛИ `input(digit d)` → ЯКЩО `mode(fog)` and `custom: «d = розвʼязок»` → ТО `reveal(cells_by_rule)` — 8 сусідів, або лінії видимості в 4 напрямках (Skyscraper Fog), або визначені сетером клітинки; givens під туманом відкриваються й не перезаписуються.
- КОЛИ `input(check)` → ТО SudokuPad Check перевіряє лише базові правила судоку, а повна перевірка — порівнянням із вбудованим розвʼязком, якщо сетер його дав (?).
- КОЛИ `all_constraints_met` → ТО `win`, `message(«solved»)`, `timer(stop)`; на LMG — ввести «solution code» (напр. цифри стовпця 3) для зарахування.
- Комбінування: глобальний модуль «кожен тип обмеження без повторів у всьому пазлі» (CtC id 2865: жодна цифра не повторюється на всіх renban-лініях разом) — правило над **класом** елементів, а не над одним.
- Перемога: розвʼязок єдиний, усі модулі виконані. Поразки нема; рахунок — час; на LMG — лічильник «gelöst» біля пазла.

## Керування і ввід
- Ті самі режими, що в класиці: Digit / Corner / Centre / Colour + мультивиділення drag/Ctrl (SudokuPad).
- Колір — головний інструмент варіантів: розфарбування парності/low-high на whispers, «двох світів» у ланцюгах.
- У Fog of War правильність цифри видна одразу (туман сходить або ні) — інформаційний канал, якого нема в класиці; у LMG «Cartography» автор радить стирати вже поставлені цифри, щоб перевіряти, що вони «бачать» (туман сходить лише при вводі).
- Редактори (f-puzzles, SudokuPad maker, Penpa+): палітра елементів — клітка, лінія, крапка, текст ззовні; експорт у коротке посилання.

## Вікна, меню, HUD
- `game-screen` SudokuPad: поле з шарами + `+ui:rules-panel` (текст правил і автор поруч з полем) + `timer-elapsed` + `number-pad` з перемикачами режимів + `undo-button`/`redo-button` + `check-button` + `restart-button`.
- `fog-overlay` — сірий шар над клітинками з туманом.
- `settings-window` — тема, підсвітка конфліктів, обмеження «показувати пазл як…» (?).
- `end-screen` — «You solved it» з часом, коментар автора (якщо є) (?).
- `puzzle-select` — каталог CtC `/sudokus`, LMG пошук з тегами (Kropki, Killer, Renban…) і рейтингом 1–5; застосунки CtC — банк по паках з розблокуванням.
- `editor-window` — f-puzzles / SudokuPad maker / Penpa+: інструменти-обмеження.
- Переходи: LMG сторінка пазла → лінк SudokuPad → game-screen → solved → назад на LMG ввести solution code.

## Фічі поза полем
- `custom-rules` як суть жанру: правила пазла — частина файла пазла (текст + набір модулів).
- `level-sharing` через короткі лінки (`sudokupad.app/<id>`), `level-editor`, `user-levels-browser` + `level-rating` (LMG: складність 1–5, «найгарніші», лічильник «gelöst», коментарі).
- `puzzle-bank` у застосунках CtC (Thermo, Killer, Arrow, Miracle, Sandwich, Chess, Fog of War, Domino, Lines…) з `level-unlock` (?).
- `undo`/`redo`, `autosave` прогресу в браузері (?).

## Варіації й родичі
- Сімʼї модулів: **суми** (Killer, Arrow, Little Killer, Sandwich, X-Sums, XV, Region Sum) · **порядок** (Thermo, Between, Skyscraper) · **різниці/відношення** (Kropki, Whispers, Renban) · **симетрія** (Palindrome) · **парність** (Odd/Even) · **геометрія** (Jigsaw, Extra regions, Anti-knight/king) · **інформація** (Fog of War).
- Miracle Sudoku (Mitchell Lee, CtC 2020): anti-king + anti-knight + ортогональні сусіди не послідовні; дано лише 2 цифри (1 і 2).
- Осі варіацій: «одне обмеження / мікс» · «позитивне (дано) / негативне (не дано = заборонено)» · «локальне (лінія) / глобальне (anti-knight)» · «над елементом / над класом елементів» · «повне поле / туман».
- Родичі: Kakuro (Killer без сітки судоку), Futoshiki (Thermo-нерівності на ребрах), Skyscrapers/Towers (Tatham) — самостійні жанри.

### Sandwich Sudoku — сума «начинки» між 1 і 9
- Правило (Steam «Sandwich Sudoku», CtC): числа ззовні біля рядків і стовпців — «the SUM of cells sandwiched between the 1 and the 9 in that row/column»; 1 і 9 — «скибки», самі в суму не входять. На 6×6 (MIT 2023, Sandwich Sums) — сума між 1 і 6.
- КОЛИ `custom: «у ряду з підказкою стоять 1 і 9»` → ЯКЩО `not sum(between_1_9, clue)` (`+cond:sum_between`) → ТО `constraint_broken(sandwich)`.
- Висновки (виведено з правила): 0 — 1 і 9 поруч; 35 — 1 і 9 на кінцях ряду (2+…+8); суми 1 і 34 неможливі. Начинка з k клітинок дає від 2+…+(k+1) до (9−k)+…+8: k=1 → 2–8, k=2 → 5–15, k=3 → 9–21, k=4 → 14–26, k=5 → 20–30, k=6 → 27–33, k=7 → 35. Тож сума 2–4 — одна клітинка, 31–33 — рівно шість, а відстань між скибками в рядку й стовпці звʼязує позиції 1 і 9 по всьому полю.
- Історія: CtC зробили варіант вірусним (Guardian, 6 травня 2019, «Sandwich sudoku – a new puzzle goes viral» — за Wikipedia «Cracking the Cryptic»); застосунок «Sandwich Sudoku» (Steam, 19.08.2019): 40 рівнів на старті + 5 щомісяця до 100, підказки від Simon і Mark, теми.
- Родичі: [doppelblock](doppelblock.md) — сума між двома чорними клітинками (картка `+sum-between-clue`); X-Sums і Skyscraper — інші зовнішні підказки (таблиця сутностей); Non-Consecutive Sandwich — у застосунку Miracle Sudoku.
- Цікавинка: перевірка ряду (індекси 1 і 9, сума між ними) — 🌱; таблиця «сума → можливі набори начинки» для розвʼязувача — 📎.

### Miracle Sudoku — anti-knight + anti-king + non-consecutive і дві дані цифри
- Правила (ethmcc «On Miracle Sudoku», 11.05.2020): класичне судоку + однакові цифри не на відстані ходу коня + не на відстані ходу короля + ортогональні сусіди не послідовні (по діагоналі — можна). Chess Sudoku CtC формулює King як «a digit must not be a single diagonal move away from itself» — ортогональних сусідів і так покривають рядок і стовпець.
- Автор — Mitchell Lee; в оригіналі дано лише дві цифри — 1 і 2 (ethmcc). Відео CtC з ним стало вірусним (Guardian, 22.05.2020 — за Wikipedia «Cracking the Cryptic»).
- КОЛИ `input(digit)` → ЯКЩО `custom: «та сама цифра на ході коня»` (`+cond:knight_move`) → ТО `constraint_broken(anti_knight)`.
- КОЛИ `input(digit)` → ЯКЩО `custom: «та сама цифра в діагональному сусіді»` → ТО `constraint_broken(anti_king)`.
- КОЛИ `input(digit)` → ЯКЩО `custom: «ортогональний сусід = d ± 1»` → ТО `constraint_broken(non_consecutive)` — глобальна форма Nonconsecutive з [sudoku-line-dot-variants](sudoku-line-dot-variants.md).
- Чому «диво» (ethmcc): повних сіток рівно 72 — 9 з точністю до 8 симетрій квадрата (по одній на центральну цифру), 5 з урахуванням заміни d ↔ 10−d; жоден пазл з однією даною не має єдиного розвʼязку; 174 816 розстановок двох даних дають єдиний розвʼязок (21 852 з точністю до симетрій), випадкова пара різних даних — майже у 75 %. Без non-consecutive шахові правила не розрізняють цифр (перестановка значень зберігає розвʼязок), тож треба ≥ 8 даних.
- Застосунки CtC: «Chess Sudoku» (Steam, 02.03.2020) — Knight, King і Queen («кожна 9 — ферзь»); «Miracle Sudoku» (Steam, 13.08.2020) — 40 пазлів на старті, 100 за перший рік, 4 варіанти: Non-Consecutive, Miracle, Non-Consecutive Thermo, Non-Consecutive Sandwich; підказки Simon і Mark, зірки за розвʼязання відкривають нові пазли.
- Цікавинки: перелічити всі 72 Miracle-сітки перебором або exact cover (ethmcc — Algorithm X, dancing links) — 🥉; знайти всі пари даних з єдиним розвʼязком — 🥇.
- Родичі: Miracle на торі — [sudoku-topology](sudoku-topology.md); [n-queens-knights-tour](n-queens-knights-tour.md) — ті самі шахові відстані без цифр.

## Цікавинки для курсу
- Модуль-обмеження як обʼєкт з методом `check(grid) → conflicts`; варіант = список модулів — 🥉 (архітектура plugin-правил).
- Рендер шарів поверх сітки: лінії, пунктир кліток, крапки на ребрах, зовнішнє кільце — 🥈 (консоль: ASCII-лінії — окремий виклик).
- Killer з комбінаціями сум і правилом 45 у розвʼязувачі — 🥇.
- Fog of War: розкриття за правильністю цифри — 🥉 (потрібно мати розвʼязок і правило розкриття).
- Негативні обмеження («усі крапки дано») — 📎 як прапорець над модулем, але тест цікавий.
- Пазл як файл з правилами (JSON: сітка + модулі + розвʼязок) і короткий лінк — 🥈.

## Мапа на каталог
- Є: `markup-validity` ↔ конфлікти модулів · `completion-detection`, `satisfy-constraints` · `pencil-marks`, `cell-click`, `keyboard-controls` · `level-bank`, `level-rating` ↔ LMG/CtC · `import-open-formats` ↔ f-puzzles/SudokuPad лінки · `in-game-editor`, `level-exchange` ↔ редактори · `level-solver`.
- **Нема** → пропозиції карток:
  - `+constraint-overlay` «Шари обмежень поверх сітки» · interface/render · 🥈.
  - `+killer-cage` «Клітка з сумою» · game-logic/constraints · 🥉 · слот {sum, unique}.
  - `+line-constraints` «Лінії-обмеження (thermo/whisper/renban/palindrome/region-sum/between)» · game-logic/constraints · 🥉 за сімʼю, 📎 кожна.
  - `+dot-constraints` «Обмеження на ребрі (Kropki, XV)» · game-logic/constraints · 📎 · слот {negative: bool}.
  - `+outside-clues` «Підказки ззовні (Sandwich, X-Sums, Skyscraper, Little Killer)» · game-logic/constraints · 🥉.
  - `+chess-move-constraint` «Anti-knight / anti-king» · game-logic/constraints · 🌱 · слот {piece}.
  - `+fog-reveal` «Туман, що сходить від правильної цифри» · game-logic/constraints · 🥉 · слот {reveal: neighbours|sightlines|scripted}.
  - `+irregular-regions` «Нерегулярні регіони (Jigsaw)» · levels/format · 📎.

## Пропозиції до словників
- `+role:line` — послідовність клітинок з порядком (термометр, стрілка, whisper): `zone` не передає порядок.
- `+role:clue-outside` — підказка поза полем, привʼязана до ряду/діагоналі.
- `+trigger:reveal_by_correct` — правильний ввід як подія (Fog of War); поки — `input` + `custom`.
- `+effect:reveal` — уже ⏳, тут ще одне вживання (туман).
- `+ui:rules-panel` — текст правил конкретного пазла поруч з полем (`fog-overlay` уже ⏳ — тут ще одне вживання).
- `+feature:custom-rules` — правила як частина рівня (вже ⏳; ще одне вживання).
- `+axis:rule-composition` — `fixed` (одне правило) / `modular` (рівень = набір модулів-обмежень).
- `+cond:sum_between` — сума значень між двома позначеними клітинками ряду (Sandwich; повтор з Doppelblock).
- `+cond:knight_move` — клітинки на відстані ходу коня (anti-knight, Miracle; повтор з N-Queens).

## Джерела
- ⭐ [LMG: Confined Constraints](https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000OGK) — класика + 8 модулів (Thermo, Killer, Whisper, Renban, Kropki, XV, Arrow, Odd) з точними правилами + лінк у SudokuPad; solution code — стовпець 3.
- [SudokuPad: Confined Constraints](https://sudokupad.app/plzx2drps0) — як усе це рендериться шарами.
- [CtC: Unique Under The Fog 6.0](https://www.crackingthecryptic.com/sudoku?id=2865) — Fog of War, Region Sum, правило «без повторів у класі обмежень»; [SudokuPad](https://sudokupad.app/hvtrbv1n24).
- [LMG: Cartography](https://logic-masters.de/Raetselportal/Raetsel/zeigen.php?id=000LRL) — Skyscraper Fog: туман сходить у клітинці й по 4 ортогональних лініях видимості; висота поставленої цифри не важить.
- [CtC Apps](https://crackingthecryptic.com/apps) — застосунки-варіанти (Steam/iOS/Android).
- [Logic Masters Germany](https://logic-masters.de/Raetselportal/) — портал: 37 359 пазлів, теги варіантів, складність 1–5, лічильник «gelöst».
- [Wikipedia: Killer sudoku](https://en.wikipedia.org/wiki/Killer_sudoku) — Nishio (ідея Miyuki Nisawa), The Times 2005, сума 45 у регіоні, innies/outies.
- [MIT Sudoku Open 2024 Variants I](https://puzzles.mit.edu/sudokuopen/2024/variants-i.pdf) і [2023](https://puzzles.mit.edu/sudokuopen/2023/variants-i.pdf) — турнірні формулювання правил.
- [Artisanal Sudoku: basics](https://artisanalsudoku.substack.com/p/the-basics-of-popular-sudoku-variants) — Kropki, Whispers, Renban, Arrow з наслідками (whisper без 5).
- [Steam: CtC Fog of War 1](https://store.steampowered.com/app/3165770/Cracking_the_Cryptic__Fog_of_War_1/).
- [YouTube: Cracking the Cryptic](https://www.youtube.com/c/CrackingTheCryptic).
- [Steam: Sandwich Sudoku](https://store.steampowered.com/app/1117310/Sandwich_Sudoku/) — правило, 40 рівнів + 5 на місяць до 100, 19.08.2019.
- [Steam: Miracle Sudoku](https://store.steampowered.com/app/1377260/Miracle_Sudoku/) — 4 варіанти з non-consecutive, 13.08.2020.
- [Steam: Chess Sudoku](https://store.steampowered.com/app/1250560/Chess_Sudoku/) — тексти правил Knight, King, Queen, 02.03.2020.
- [On Miracle Sudoku (ethmcc)](https://ethmcc.github.io/miracle-sudoku) — правила, Mitchell Lee, дві дані 1 і 2, 72 сітки, 174 816 пар даних.
- [Wikipedia: Cracking the Cryptic](https://en.wikipedia.org/wiki/Cracking_the_Cryptic) — посилання на статті Guardian про Sandwich (2019) і Miracle (2020), перелік застосунків.
- [The Takeout: Sandwich Sudoku](https://thetakeout.com/sandwich-sudoku-puzzles-how-to-play-1834591096) — правило і атрибуція ідеї (див. «Непевне»).

## Непевне
- (?) Between line, Skyscraper-sudoku, «повтори на діагоналі Little Killer можливі» — з памʼяті (стандартні формулювання), сторінок з їхнім текстом не відкрив.
- (?) Як SudokuPad перевіряє варіанти: Check — лише базові правила; повна перевірка — через вбудований розвʼязок (з памʼяті).
- (?) Кольори ліній (зелений whisper, фіолетовий renban, синій region sum) — конвенція, а не стандарт; Palindrome «сірий» бачив лише в MIT 2023 («shaded lines»).
- (?) Рік 2005 у шапці умовний: Killer у The Times — 2005, CtC — 2017 (обидва за Wikipedia); старші варіанти (Sudoku-X, Jigsaw) — дат не перевіряв.
- (?) Автор Sandwich: The Takeout пише про ідею Isaac Resnikoff, Guardian (джерело Wikipedia) агенту недоступний — атрибуцію не підтверджено; чи підказки дано біля всіх рядків, правило Steam не уточнює.
- (?) Miracle: де саме стоять дані 1 і 2 в оригіналі, ethmcc не каже; дату відео CtC (травень 2020) знаю лише з дати статті Guardian і результатів пошуку.
