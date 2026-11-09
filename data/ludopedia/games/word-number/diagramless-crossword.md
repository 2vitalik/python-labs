---
title: Diagramless crossword (Кросворд без сітки)
slug: diagramless-crossword
aka: [Diagramless, Carte Blanche, Skeleton crossword, Кросворд-скелет, Кросворд без схеми]
family: word-number
also: [pencil-logic]
klass: puzzle
axes:
  field: square
  time: static
  opponent: none
  info: hidden
  random: none
  goal: constraints
year: 1924
platforms: [paper, web, mobile]
links:
  - {kind: other, url: "https://content.puzzazz.com/how-to/diagramless-crosswords", best: true, note: "Puzzazz: що дано, правила (нема 2-літерних слів, усі літери перевірені), дедукція з нумерації, стратегія, Block-клавіша, автосиметрія, Shade Starting Cell"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Crossword", note: "розділ варіантів: дано лише розміри, назви diagramless / skeleton / carte blanche, типи симетрії, NYT вимагає 17×17"}
  - {kind: other, url: "https://www.puzzles.wiki/wiki/Diagramless_Crossword", note: "історія 1924 (Hartswick відтворив загублену сітку), фігурні сітки, хант-варіанти, прийоми"}
  - {kind: other, url: "https://www.puzzler.com/media/puzzles/instructions/SkeletonCrossword.pdf", note: "Puzzler (UK): вісім типів симетрії сітки skeleton crossword"}
  - {kind: other, url: "https://clarity-media.co.uk/puzzleblog/skeleton-crossword-solving-tips", note: "skeleton crossword: дано частину чорних клітин і номерів, довжини невідомі, поради"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=how+to+solve+diagramless+crossword", note: "пошук; розвʼязування"}
stage: v1
coverage: 60
mechanics: [cell-click, keyboard-controls, selection-highlight, completion-detection, satisfy-constraints, markup-validity, conflict-highlight, daily-puzzle, level-bank, game-screen, help-window, settings-window, +across-down-entry, +clue-list, +hidden-grid-layout, +numbering-deduction, +symmetry-rule, +block-placement, +start-cell-hint, +reveal-letter, +shift-row-col, +clue-done-mark, +shaped-grid]
proposes: ["+cond:symmetric", "+cond:numbering_consistent", "+cond:all_checked", "+feature:grid-symmetry", "+feature:start-cell-hint", "+ui:block-key", "+ui:clue-list", "+card:numbering-deduction"]
author: opus
date: 2026-11-09
---

# Diagramless crossword — кросворд, де дано лише розмір і підказки: де чорні клітини і де стоять номери, розвʼязувач виводить сам

## Суть
Звичайний американський кросворд із номерованими підказками Across і Down, але сітка порожня: невідомо, які клітини чорні, де стоять номери і якої довжини відповіді. Розвʼязувач паралельно вгадує слова й **будує каркас**: з нумерації (номери йдуть рядками зліва направо) виводить довжини і позиції, ставить блоки, дзеркалить їх за симетрією. Шматки відповідей зростаються в «кластери», а ті — у цілу сітку. Перший diagramless зʼявився в 1924 році: редактори загубили сітку, і F. Gregory Hartswick відтворив її з самих підказок.

## Поле і час
- Квадратна сітка R×C, дано лише розмір (NYT вимагає 17×17); у частині видань ще позиція 1-Across (іноді й 1-Down) і тип симетрії.
- Фігура з білих клітин торкається всіх чотирьох країв сітки; сітка звʼязна, ізольованих клітин нема.
- Симетрія: найчастіше 180° обертальна; також дзеркальна ліво-право, вища симетрія або обриси предметів (фігурні сітки). Puzzler (UK) розрізняє 8 типів: full, central (180°), biaxial, vertical, horizontal, NE-діагональ, NW-діагональ, asymmetry.
- Шари: клітина (невідома / біла з літерою / чорна), номер, підказки поза полем.
- Часу нема; у застосунках — секундомір (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітина | tile | стан: невідома / біла / чорна; літера | розвʼязувач вирішує, біла вона чи чорна, і вписує літеру |
| Блок (чорна клітина) | static | позиція | ставиться розвʼязувачем; за симетрією тягне за собою парні блоки |
| Номер | mark | 1…N | стоїть у клітині, де починається Across або Down; виводиться, а не дається |
| Відповідь Across / Down | zone | номер, напрям; довжина невідома | ланцюг білих клітин між блоками/краями |
| Підказка | static | номер, текст | у списках Across і Down; довжину не показує |
| Стартова клітина | mark | позиція 1-Across | дається у вступі або хінтом Shade Starting Cell |
| Кластер | zone | набір вписаних слів | частково зібраний шматок сітки, ще не привʼязаний до координат |

## Правила (КОЛИ → ЯКЩО → ТО)
Конвенції сітки (обмеження, якими користується розвʼязувач):
- КОЛИ `custom: «біла клітина»` → ЯКЩО `custom: «зліва блок або край, а справа біла»` or `custom: «зверху блок або край, а знизу біла»` → ТО `custom: «клітина має номер; номери зростають рядками зліва направо»`.
- КОЛИ `constraint_broken(двобуквене слово)` → ТО `custom: «хибний каркас»` (мінімальна довжина відповіді — 3).
- КОЛИ `constraint_broken(літера лише в одному слові)` → ТО `custom: «хибний каркас»` — кожна літера входить і в Across, і в Down.
- КОЛИ `constraint_broken(ізольована порожня клітина)` → ТО `set_cell(cell, block)`.
- КОЛИ `custom: «перевірка сітки»` → ЯКЩО not `connected(white cells)` → ТО `custom: «хибний каркас»`.
- КОЛИ `input(place block)` → ЯКЩО `mode(symmetry known)` → ТО `custom: «поставити парні блоки за типом симетрії»`.
- КОЛИ `all_constraints_met` → ЯКЩО `custom: «літери й блоки = авторському розвʼязку»` → ТО `win`.

Дедукція з нумерації (прийоми Puzzazz і puzzles.wiki):
- КОЛИ `level_start` → ТО `custom: «1-Across лежить у верхньому ряду, останнє Across — у нижньому»`.
- КОЛИ `custom: «1-Across у верхньому ряду»` → ТО `custom: «довжина 1-Across = номер другого Across − 1»` (кожна літера верхнього ряду починає Down і отримує свій номер).
- КОЛИ `custom: «два ранні Across розділяє менше трьох номерів»` → ТО `custom: «вони не в одному (верхньому) ряду»`.
- КОЛИ `custom: «номер є і в Across, і в Down»` → ТО `custom: «його клітина — кут (зліва і зверху блок або край)»`.
- КОЛИ `custom: «симетрія 180°»` → ТО `custom: «перше і останнє Across однакової довжини; кожен блок має пару»`.
- Стратегія: починати з 1-Across (довжина відома), далі Down-слова за їхніми першими літерами, потім ранні Across, що перетинають 2–3 ряд; рух згори вниз, бо слово легше вгадати з перших літер.

Ввід (цифрова версія, Puzzazz):
- КОЛИ `input(type letter)` → ЯКЩО `state(cell, selected)` → ТО `set_value(cell, letter)`.
- КОЛИ `input(Block key)` → ТО `set_cell(cell, block)`; ЯКЩО `mode(Grid Symmetry)` → ТО `custom: «симетричні блоки додаються/знімаються разом»`.
- КОЛИ `input(move row/col)` → ТО `shift(row|col, dir)` без переходу через край (якщо кластер вписано не туди).
- КОЛИ `input(Shade Starting Cell)` → ЯКЩО `custom: «у пазлі є розвʼязок»` → ТО `custom: «підсвітити клітину 1-Across»`.
- КОЛИ `input(hint)` → ТО `reveal(cell)` або `custom: «прибрати помилки»`.
- КОЛИ `input(Mark Clue Solved)` → ТО `mark(clue, solved)`.
- Перемога: сітка = розвʼязок · Поразки нема · Рахунок: час (?).

## Керування і ввід
- Папір: розвʼязувачі малюють на міліметрівці, вписують перші Across, поки не стане ясно, де старт; певні слова — великими літерами, сумнівні — інакше; блоки затушовують, стежачи, щоб не «випасти» за край.
- (цифрова версія, Puzzazz) клік по клітині, набір літер, клавіша Block з обох кінців відповіді, зсув цілого рядка/стовпця, натиснути й утримати підказку → Clue Options (нотатки, Mark Clue Solved).

## Вікна, меню, HUD
- (цифрова версія) `game-screen`: порожня сітка R×C, `clue-list` Across/Down (розвʼязані позначені), `selection-highlight`, клавіатура з `block-key`, кнопка хінтів.
- (цифрова версія) `settings-window`: Grid Symmetry (вибір типу; правильний позначений `*`, якщо симетрію дано).
- (цифрова версія) `hints-window`: Shade Starting Cell, reveal клітини, очистити помилки.
- (цифрова версія) `help-window`: вступ пазла (розмір, 1-Across, симетрія), довідка.
- (цифрова версія) `end-screen`: «розвʼязано» (?).
- (цифрова версія) `puzzle-select`: архів пазлів видання (?).

## Фічі поза полем
- `hint` (стартова клітина, reveal), `auto-check` (очистити помилки), `puzzle-bank` — у застосунках.
- Автосиметрія блоків (`grid-symmetry`) і зсув кластера — фічі саме diagramless-редактора.
- Нотатки на підказці (Clue Options).
- Видання: NYT (17×17), Dell; skeleton crossword у UK-журналах (Puzzler).

## Варіації й родичі
- **Skeleton crossword / Carte Blanche (UK)** — дано частину чорних клітин і часто частину номерів; довжини невідомі; решту блоків виводять симетрією (вісім типів у Puzzler).
- **Фігурні diagramless** — каркас у формі предмета (напр. обрис Каліфорнії, Stan Kurzban); тема підказує форму.
- **Хант-варіанти**: The Island of the Cyclopes (Mark Halpin — з відповідей прибрано I, сітка у формі ока), Diagramless Crossmusic (MITMH 2013, підказки — аудіо), World's Longest Diagramless (MITMH 2016, підказки майже за абеткою).
- Fill-In (`fill-in.md`) — теж має diagramless-варіант (сітку виводять зі списку слів); Codeword (`codeword.md`) — сітка дана, приховані літери; Cryptic (`cryptic-crossword.md`), Arrowword (`arrowword.md`) — сітка дана.
- **Осі варіацій:** що дано (лише розмір / + старт 1-Across / + частина блоків і номерів) · симетрія (180° / дзеркало / 8 типів / нема / фігура) · підказки (означення / криптичні / аудіо) · нумерація (повна / частково / нема).

## Цікавинки для курсу
- Автонумерація сітки з розставлених блоків (стандартне правило «починає Across або Down») — 🌱.
- Валідатор каркаса: нема 2-літерних слів, усі літери перевірені, звʼязність (BFS), симетрія заданого типу — 📎.
- Автосиметрія блоків для 8 типів симетрії (відображення координат) — 📎.
- Зсув рядка/стовпця без wrap, щоб пересунути кластер — 🌱.
- Розвʼязувач каркаса: за списком номерів Across/Down знайти всі розстановки блоків, що дають саме таку нумерацію (backtracking рядками) — 🥇.
- Помічник «де старт»: довжина 1-Across з номера другого Across, кути за спільними номерами — 🥉.

## Мапа на каталог
- Є: `cell-click` + `keyboard-controls` ↔ ввід; `selection-highlight`; `markup-validity` + `conflict-highlight` ↔ перевірка каркаса; `completion-detection` + `satisfy-constraints`; `daily-puzzle` + `level-bank` ↔ газетні випуски й архів; `game-screen`, `help-window`, `settings-window` ↔ Grid Symmetry.
- **Нема** → пропозиції карток:
  - `+hidden-grid-layout` «Каркас сітки прихований, розвʼязувач ставить блоки» · game-logic/constraints · 🥉.
  - `+numbering-deduction` «Вивід позицій із номерів підказок» · game-logic/constraints · 🥈.
  - `+symmetry-rule` «Симетрія сітки як обмеження й автодзеркалення» · game-logic/constraints · 📎 · слот {type: 180 / mirror / 8 типів}.
  - `+block-placement` «Розстановка блоків клавішею» · interface/input · 🌱.
  - `+start-cell-hint` «Хінт: підсвітити стартову клітину» · game-logic/history · 🌱.
  - `+shift-row-col` «Зсунути рядок/стовпець без wrap» · interface/input · 🌱.
  - `+shaped-grid` «Фігурна сітка за обрисом» · levels/format · 📎.
  - `+across-down-entry`, `+clue-list`, `+reveal-letter`, `+clue-done-mark` — уже пропоновані іншими файлами.

## Пропозиції до словників
- `+cond:symmetric` — розстановка блоків симетрична за типом (180°, дзеркало, діагональ).
- `+cond:numbering_consistent` — номери в клітинах збігаються з тими, що дає правило «починає Across/Down».
- `+cond:all_checked` — кожна біла клітина входить і в Across, і в Down.
- `+feature:grid-symmetry` — автодзеркалення поставлених блоків.
- `+feature:start-cell-hint` — хінт стартової клітини.
- `+ui:block-key` — окрема клавіша «блок» на екранній клавіатурі.
- `+ui:clue-list` — списки Across/Down з позначкою «розвʼязано».
- `+card:numbering-deduction` — механіка виводу каркаса з нумерації.

## Джерела
- ⭐ [Puzzazz: Diagramless Crosswords](https://content.puzzazz.com/how-to/diagramless-crosswords) — що дано, правила (нема 2-літерних слів, ізольованих клітин, кожна літера в обох словах), дедукція (1-Across = номер другого Across − 1, кути, верхній/нижній ряд), стратегія, Block, Grid Symmetry, Shade Starting Cell, зсув рядків.
- [Wikipedia: Crossword](https://en.wikipedia.org/wiki/Crossword) — розділ варіантів: дано розміри, назви, симетрії; NYT — 17×17; правило нумерації.
- [puzzles.wiki: Diagramless Crossword](https://www.puzzles.wiki/wiki/Diagramless_Crossword) — історія 1924, фігурні сітки, хант-варіанти, прийоми.
- [Puzzler: Skeleton Crossword (PDF)](https://www.puzzler.com/media/puzzles/instructions/SkeletonCrossword.pdf) — вісім типів симетрії з правилами дзеркалення.
- [Clarity Media: Skeleton crossword tips](https://clarity-media.co.uk/puzzleblog/skeleton-crossword-solving-tips) — що дано в skeleton, поради.
- YouTube: пошук «how to solve diagramless crossword».

## Непевне
- (?) Чи є в цифрових версіях таймер, екран завершення, архів — не бачив; Puzzazz описує лише ввід і хінти.
- (?) «Нема 2-літерних слів» і «усі літери перевірені» — американські конвенції (Puzzazz); у UK skeleton крос-перевірка може бути неповною.
- (?) Dell як постійний видавець diagramless — з памʼяті, у відкритих джерелах не названий.
- (?) Рік 1924 — за puzzles.wiki (анекдот про загублену сітку), Wikipedia історії не дає.
