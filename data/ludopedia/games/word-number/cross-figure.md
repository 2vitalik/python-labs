---
title: Cross-figure (Crossnumber)
slug: cross-figure
aka: [Crossnumber, Cross number puzzle, Figure Logic, Figure Logics, Числовий кросворд, Кросчисло]
family: word-number
also: [pencil-logic]
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
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Cross-figure", best: true, note: "будова, 8 типів підказок, неявні правила (без нуля попереду, без однакових відповідей, «;»), прийом звуження цифр, Dell Figure Logics"}
  - {kind: other, url: "http://jig.joelpomerantz.com/fun/dogsmead.html", note: "Little Pigley Farm / Dog's Mead (W. T. Williams, 1935): підказки-історія, одна цифра на клітину, одиниці виміру; Singmaster — кросчисла з 1926"}
  - {kind: other, url: "http://www.krazydad.com/crossfigures/", note: "дві PDF-книжки по 100 пазлів (Classic за Horsefield і Dvir, Modern за Typke), шпаргалка простих, квадратів, кубів, трикутних, Фібоначчі"}
  - {kind: other, url: "https://www.yaddlezap.com/number-crosswords", note: "друковані числові кросворди"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=crossnumber+puzzle+how+to+solve", note: "пошук; розвʼязування"}
stage: v1
coverage: 60
mechanics: [cell-click, keyboard-controls, selection-highlight, pencil-marks, satisfy-constraints, completion-detection, markup-validity, conflict-highlight, unique-puzzle-generation, level-solver, difficulty-levels, level-bank, game-screen, help-window, +across-down-entry, +clue-list, +arithmetic-clue, +cross-reference-clue, +set-membership-clue, +no-leading-zero, +distinct-answers, +story-clues, +print-version]
proposes: ["+cond:crossings_agree", "+cond:no_leading_zero", "+cond:clue_relation", "+ui:clue-list", "+ui:math-reference-sheet", "+feature:reference-tables", "+card:cross-reference-clue", "+card:no-leading-zero"]
author: opus
date: 2026-11-09
---

# Cross-figure — кросворд з цифр: кожна клітина — одна цифра, підказки — арифметика, властивості чисел і посилання на інші відповіді

## Суть
Сітка кросворду, де відповіді «по горизонталі» й «по вертикалі» — числа, а в кожній білій клітині стоїть одна цифра. Підказки бувають прямі («27 × 79», «сьоме просте»), відносні («кратне 24↓»), невизначені («просте число») й такі, що спираються на інші відповіді («9↓ − 3→»). Розвʼязування йде не відповідь за відповіддю, а звуженням можливих цифр у клітинах через перетини — ближче до логічного пазла, ніж до словесного кросворду. Класика жанру — «Little Pigley Farm» (1935), де підказки — сюжет про ферму, площі й віки.

## Поле і час
- Квадратна сітка з чорними клітинами (як у кросворді); білі клітини групуються в записи по горизонталі й вертикалі, номер стоїть у першій клітині запису.
- Шари: сітка (біла / чорна) + номер запису + вписана цифра; у цифровій версії — кандидати-цифри олівцем.
- Довжина запису — кількість його клітин; відповідь має рівно стільки цифр.
- Часу нема (`static`): хід = вписати / стерти цифру.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Біла клітина | mark | цифра 0–9 або порожньо, кандидати | одна цифра; належить одному чи двом записам |
| Чорна клітина | static | — | розділяє записи |
| Запис (entry) | zone | номер, напрям →/↓, довжина | число з цифр своїх клітин |
| Підказка | zone | тип: пряма / застосована / невизначена / відносна / групова / алгебраїчна / сюжетна / без підказки | обмеження на число запису |
| Невідома-літера (алгебраїчний варіант) | mark | літера, значення | змінна, через яку виражено підказки («A − 2B») |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(type digit, cell)` → ТО `mark(cell, digit)` — рівно одна цифра на клітину.
- КОЛИ `input(erase, cell)` → ТО `unmark(cell)`.
- КОЛИ `input(pencil digit, cell)` (цифрова версія) → ТО `mark(cell, candidate)` — кандидати для звуження.
- Обмеження перетину: `custom: «цифра клітини однакова для горизонтального і вертикального запису»` — вписується одна, тож виконується автоматично.
- Пряма підказка: `custom: «число запису = значенню виразу або факту»` («27 × 79», «сьоме просте», рік битви при Гастінгсі).
- Застосована підказка: `custom: «число запису = вираз від інших записів»` («9↓ − 3→»).
- Невизначена підказка: `custom: «число належить множині»` (просте, квадрат, паліндром).
- Відносна підказка: `custom: «число повʼязане з іншим записом без однозначності»` («кратне 24↓»).
- Групова підказка: `custom: «одна умова на кілька записів»` (наприклад, які цифри вони разом містять).
- Алгебраїчна підказка: `custom: «літери позначають невідомі цілі числа»` («A − 2B»).
- Сюжетна підказка: `custom: «величини з історії»` (площа поля, вік доньки фермера, ціна в фунтах).
- Запис без підказки: `custom: «визначається лише перетинами або посиланнями інших підказок»`.
- Неявне правило 1: `custom: «перша цифра запису не 0»` (деякі пазли явно дозволяють).
- Неявне правило 2: `unique(entries)` — дві відповіді не збігаються.
- Конвенція «;»: `custom: «1234;5678 означає склеєне число 12345678»`.
- КОЛИ `all_constraints_met` (усі клітини заповнено, кожна підказка виконана) → ТО `win`.
- Укладач: `custom: «розвʼязок має бути єдиним»` — перевіряється розвʼязанням (програма може допомогти, але складності не покаже).
- Перемога: усі записи узгоджені · Поразка: нема · Рахунок: нема.

## Керування і ввід
- Папір: вписування цифр, кандидати дрібно в кутку клітини, допоміжні обчислення на полях.
- (цифрова версія) клік по клітині + клавіша цифри, перемикач олівець / ручка, стрілки й Tab між записами, клік по підказці виділяє запис.
- Прийом (Wikipedia): 12→ і 7↓ — тризначні, підказка 12→ = «7↓ × 2» ⇒ перша цифра 7↓ не більша за 4, остання цифра 12→ парна — звужуєш клітини, а не вгадуєш відповіді.

## Вікна, меню, HUD
- (цифрова версія) `game-screen`: сітка, `clue-list` (горизонталь / вертикаль), `selection-highlight` запису й поточної підказки, `pencil-marks`, `conflict-highlight` (порушено неявні правила або перевірку).
- (цифрова версія) `puzzle-select` за складністю (Dell: від easy до «challenger»); `end-screen` з часом (?).
- (цифрова версія) `help-window`: правила, типи підказок і `math-reference-sheet` — таблиця простих, квадратів, кубів, трикутних і чисел Фібоначчі (як шпаргалка KrazyDad).
- Друкована версія: PDF-книжки (KrazyDad, Yaddlezap).

## Фічі поза полем
- `difficulty-presets` за типами підказок і кількістю перехресних посилань; `puzzle-bank` (Dell Math & Logic Problems — 18 Figure Logics у номері).
- `reference-tables` — довідник числових послідовностей як допомога.
- (цифрова версія) `auto-check`, `show-solution`, `undo`.
- Освітнє застосування: прямі підказки (арифметика) — для уроків; ентузіасти вважають, що в «справжніх» пазлах їх майже не має бути.

## Варіації й родичі
- Історія: Singmaster («Sources in Recreational Mathematics») веде кросчисла з 1926 року (перший відомий приклад, непідтверджено); «Little Pigley Farm» / «Dog's Mead» — W. T. Williams, The Strand Problems Book, 1935; передруки під іменами «Dog Days», «Little Pigley», «Pilgrims' Plot».
- Сучасні лінії: Classic (L. G. Horsefield, Y. Dvir) і Modern (Rainer Typke) у KrazyDad; Dell Figure Logics.
- **Осі варіацій:** тип підказок (прямі / відносні / застосовані / алгебраїчні / сюжетні) · нуль попереду (заборонено / дозволено) · основа числення (десяткова / інша (?)) · записи без підказок (є / нема) · штучні прийоми («;», паліндроми, репюніти — є / уникаються).
- Родичі в корпусі: [crossmath.md](crossmath.md) (сітка рівностей з лотком чисел — сучасний нащадок), [mathler.md](mathler.md) і [nerdle.md](nerdle.md) (числові вирази), [codeword.md](codeword.md) (кросворд без словесних підказок); у `pencil-logic` — Kakuro (сума в записі, без повторів цифр).

## Цікавинки для курсу
- Модель: сітка → автоматичний пошук записів (горизонталь / вертикаль, номери в першій клітині) — 🌱 (той самий код, що для кросворду).
- Підказки як дані: дерево виразу з посиланнями на інші записи (`9↓ − 3→`), обчислення лише коли всі посилання відомі — 📎.
- Перевірка розвʼязку: перетини, неявні правила (нуль, дублікати), кожна підказка — 🌱.
- Розвʼязувач: звуження доменів цифр (CSP з поширенням обмежень + пошук з поверненням), підказки «кратне», «просте» як фільтри множин — 🥇.
- Генератор з гарантією єдиного розвʼязку й оцінкою складності за кількістю кроків поширення — 👑.
- Сюжетна підказка (Little Pigley Farm) — текст-задача, що перекладається в рівняння; цікава як «рівень» для ручного розвʼязання, не для коду — 📎.

## Мапа на каталог
- Є: `cell-click` + `keyboard-controls` ↔ вписування цифр · `selection-highlight` · `pencil-marks` ↔ кандидати · `satisfy-constraints` + `completion-detection` · `markup-validity` + `conflict-highlight` ↔ неявні правила · `unique-puzzle-generation` + `level-solver` · `difficulty-levels` + `level-bank` · `game-screen`, `help-window`.
- **Нема** → пропозиції карток:
  - `+across-down-entry`, `+clue-list` (вже пропоновані cryptic-crossword) — записи двох напрямів і список підказок.
  - `+arithmetic-clue` «Підказка — арифметичний вираз або числовий факт» · game-logic/constraints · 🌱.
  - `+cross-reference-clue` «Підказка посилається на інший запис» · game-logic/constraints · 📎 — граф залежностей між відповідями.
  - `+set-membership-clue` «Підказка задає множину: просте, квадрат, паліндром» · game-logic/constraints · 🌱.
  - `+no-leading-zero` «Число не починається з нуля» · game-logic/constraints · 🌱.
  - `+distinct-answers` «Усі відповіді різні» · game-logic/constraints · 🌱.
  - `+story-clues` «Підказки — текстова задача» · levels/format · 📎.
  - `+print-version` (codeword) — PDF-книжки.

## Пропозиції до словників
- `+cond:crossings_agree` (уже пропонована cryptic-crossword) — цифри / літери на перетині записів однакові.
- `+cond:no_leading_zero` — перша цифра запису не 0.
- `+cond:clue_relation` — число запису задовольняє вираз або відношення з іншими записами («кратне 24↓», «9↓ − 3→»).
- `+ui:clue-list` (cryptic-crossword); `+ui:math-reference-sheet` — таблиця простих, квадратів, кубів поруч із сіткою.
- `+feature:reference-tables` — довідник числових послідовностей як вбудована допомога.
- `+card:cross-reference-clue`, `+card:no-leading-zero` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Cross-figure](https://en.wikipedia.org/wiki/Cross-figure) — визначення, 8 типів підказок з прикладами, неявні правила, «;», прийом звуження, вимога єдиного розвʼязку, Dell Figure Logics.
- [Joel Pomerantz: Dog's Mead / Little Pigley Farm](http://jig.joelpomerantz.com/fun/dogsmead.html) — історія класичного пазла, підказки-сюжет, «не більше однієї цифри в клітині», Singmaster і 1926 рік.
- [KrazyDad: Cross-figures](http://www.krazydad.com/crossfigures/) — Classic / Modern книжки, шпаргалка числових послідовностей.
- [Yaddlezap: Number crosswords](https://www.yaddlezap.com/number-crosswords) — друковані приклади.
- YouTube: пошук «crossnumber puzzle how to solve».

## Непевне
- (?) Рік виникнення: Singmaster — з 1926, але це «перший відомий приклад», не підтверджений; `year: null`.
- (?) Інтерфейс цифрових версій (олівець, перевірка, архів, таймер) — описано як було б у цифровій версії; інтерактивного застосунку не відкривав.
- (?) Типові розміри сітки й чи бувають кросчисла в інших системах числення — у джерелах не знайдено.
- (?) Чи завжди сітка симетрична, як у словесному кросворді, — джерела мовчать.
