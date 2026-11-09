---
title: Detektivschach (Detective Chess)
slug: detective-chess
aka: [Detektivschach, Детективні шахи]
family: pencil-logic
also: [chess-abstract, hidden-deduction]
klass: puzzle
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: none
  goal: constraints
year: null
platforms: [paper, web, PC]
links:
  - {kind: other, url: "https://www.janko.at/Raetsel/Detektivschach/index.htm", best: true, note: "Janko: правила DE/EN, приклад з розвʼязком, 240 пазлів 6×6/8×8/10×10, Gardner → Jaime Poniachik"}
  - {kind: play, url: "https://www.janko.at/Raetsel/Detektivschach/001.a.htm", note: "applet Janko (ChessPlace.js); у коді сторінки — дані: розмір, набір фігур, поле, розвʼязок"}
  - {kind: other, url: "https://www.janko.at/Raetsel/Detektivschach/Bedienung.htm", note: "керування: цикл кліками, меню K/Q/R/B/N, клавіші k d t l s, F3/F4/F6"}
  - {kind: other, url: "http://runamok.tech/cpuzzle.html", note: "Mark Joerger, CPUZZLE (1991, QuickBasic): гра-запитання за Gardner, режими, VOZ Gerry Quinn"}
  - {kind: wiki, url: "https://es.wikipedia.org/wiki/Jaime_Poniachik", note: "автор ідеї: уругвайський укладач головоломок (1943–2011)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=detective+chess+logic+puzzle", note: "пошук; розвʼязання"}
stage: v1
coverage: 65
mechanics: [piece-move-patterns, cursor-place, markup-validity, completion-detection, satisfy-constraints, cell-click, keyboard-controls, conflict-highlight, level-bank, level-rating, puzzle-select, save-game, undo-redo, replay, +attack-count-clue, +piece-set-placement, +hint-reveal, +cell-coloring]
proposes: ["+cond:attacked(cell, by)", "+cond:attack_count(cell, n)", "+cond:knight_move(a, b)", "+ui:value-popup-menu", "+ui:solved-frame", "+window:puzzle-info", "+card:attack-count-clue", "+card:piece-set-placement"]
author: opus
date: 2026-11-09
---

# Detektivschach (Detective Chess) — розстав заданий набір шахових фігур так, щоб числа показували, скільки фігур бʼє клітинку

## Суть
На шаховій дошці частина клітинок позначена рамкою, частина містить числа. Гравець ставить заданий набір фігур (напр. 1 король, 1 ферзь, 2 тури, 2 слони, 2 коні) на позначені клітинки так, щоб кожне число дорівнювало кількості фігур, які могли б піти на цю клітинку. Незвичне: підказки — «тиск» фігур, а фігури перекривають лінії одна одній, тож кожна розстановка змінює дію інших. Оригінал (Martin Gardner, ідея Jaime Poniachik) — гра-запитання: фігури сховані, гравець питає «скільки фігур бʼє цю клітинку?».

## Поле і час
- Квадратна дошка 6×6, 8×8 або 10×10 з шаховим затіненням (Janko).
- Шари: позначені клітинки (рамка) · числові клітинки · фігури гравця · кольорові маркери.
- Кількість позначених клітинок = кількість фігур у наборі (перевірив у 6 пазлах), тож кожна позначена отримує рівно одну фігуру.
- Набір пишеться над полем: приклад `(1K,1D,2T,2L,2S)`; у даних 10×10 — `k2 q2 r2 b2 n2` (два королі допустимі).
- Час статичний; пазли Janko (автор у даних — Otto Janko).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Позначена клітинка | zone | рамка | сюди й лише сюди ставлять фігуру |
| Числова клітинка | static | n ≥ 0 | n = кількість фігур, що бʼють; фігуру не ставлять; лінію атаки не перекриває |
| Порожня клітинка | terrain | — | прозора для ліній атаки |
| Король (König) | piece | 1 крок, 8 напрямків | бʼє 8 сусідів |
| Ферзь (Dame) | piece | лінії, 8 напрямків | бʼє до першої фігури включно з порожніми й числовими |
| Тура (Turm) | piece | 4 ортогоналі | як ферзь, лише по рядку/стовпцю |
| Слон (Läufer) | piece | 4 діагоналі | як ферзь, лише по діагоналях |
| Кінь (Springer) | piece | стрибок (1, 2) | бʼє 8 клітинок, перешкод не знає |
| Набір фігур | supply | кількість кожного виду | усе має бути розставлено |
| Кольорова позначка | mark | колір 0–9 | особиста розмітка гравця |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left_click, cell)` → ТО `set_value(cell, наступний символ: король → ферзь → тура → слон → кінь → порожньо)`.
- КОЛИ `input(right_click, cell)` → ТО `choose(K|Q|R|B|N|•)` → `place(player, piece)` або `unmark(cell)`.
- КОЛИ `input(key k|d,q|t,r|l,b|s,n)` → ТО `place(player, piece)`; `-`, `/`, Del, ⌫ → `unmark(cell)`.
- КОЛИ `input(enter|space)` → ТО `custom: «наступний символ циклу в клітинці під рамкою»`.
- Розстановка: ЯКЩО `custom: «фігура стоїть не на позначеній клітинці»` → `constraint_broken(custom: «не та клітинка»)`.
- Набір: ЯКЩО `count(piece_kind, eq, n_kind)` для кожного виду → набір використано повністю.
- Число: ЯКЩО `custom: «кількість фігур, що могли б піти на клітинку, = n»` (`+cond:attack_count`, `+cond:attacked`) → підказка задоволена.
- Король: ЯКЩО `in_range(king, cell, 1)` (8 сусідів) → клітинка під ударом.
- Кінь: ЯКЩО `custom: «клітинка на ході коня»` (`+cond:knight_move`) → під ударом; фігури між ними не важать.
- Тура / слон / ферзь: ЯКЩО `line_of_sight(piece, cell)` у своїх напрямках → під ударом.
- Перекриття фігурою: ЯКЩО `occupied(cell_between, piece)` → лінію обірвано (приклад Janko: слон не бʼє «2», бо між ними кінь; інакше було б 3).
- Числові клітинки прозорі: ЯКЩО `custom: «між фігурою і ціллю лише числові або порожні клітинки»` → лінія діє (пазл 001: тура бʼє «1» крізь клітинку «3»).
- Фігура не бʼє клітинку, на якій стоїть (Joerger за Gardner).
- КОЛИ `input(F6)` → ТО `custom: «усі порушення — червоним»`.
- КОЛИ `input(F3)` → ТО `set_state(board, hint_mode)`; КОЛИ `input(click, cell)` → ЯКЩО `state(board, hint_mode)` → ТО `place(player, correct_piece)`.
- КОЛИ `input(F4)` → ТО `custom: «вписати розвʼязок і шлях у список ходів»`.
- КОЛИ `input(ctrl_z|page_up)` → ТО `undo(1)`; `input(pos1)` → `undo(all)`.
- КОЛИ `all_constraints_met` → ТО `win` + `custom: «зелена рамка навколо дошки»`.
- Дедукція «нуль поруч»: позначена клітинка, орто-сусідня з «0», — не король, не ферзь, не тура; діагонально-сусідня — не король, не ферзь, не слон.
- Дедукція «нуль на стрибку»: позначена клітинка на ході коня від «0» — не кінь.
- Дедукція «максимум»: якщо число дорівнює кількості позначених клітинок, які взагалі можуть його бити, усі вони мусять бити.
- Дедукція «щит»: поставлена фігура обриває лінії інших, тож вплив кожної розстановки нелокальний — типовий хід розвʼязку «спершу коні та король, потім лінійні».
- Перемога: усі фігури набору на позначених клітинках, усі числа збіглися. Поразки й рахунку нема.

## Керування і ввід
- Миша: лівий клік по клітинці — цикл фігур; правий клік — меню «K / Q / R / B / N / •».
- Дотик: тап — цикл; утримання — меню.
- Клавіатура: стрілки — рамка; `k` король, `d`/`q` ферзь, `t`/`r` тура, `l`/`b` слон, `s`/`n` кінь; Enter/Space — цикл; `-`, `/`, Del, ⌫ — очистити.
- Наведення без кліку + клавіша — у клітинку під мишею.
- Символьні маркери Ctrl+Q/W/E/R/X/A/B/C/D, кольори Alt+0…9.
- Гра Gardner (CPUZZLE): текстовий запит «Square or Piece» — клітинка (C3) дає кількість атакувальників, буква фігури + клітинка — так/ні; X — вихід, Z — пропустити дошку зі штрафом.

## Вікна, меню, HUD
- `game-screen`: шахова дошка, позначені клітинки рамкою, числа, іконки фігур (чорні), набір фігур у підписі, `conflict-highlight` (F6), зелена рамка після розвʼязання (`+ui:solved-frame`).
- `+ui:value-popup-menu` — спливне меню фігур біля клітинки.
- `puzzle-select` — Janko: 240 пазлів за датою, розміром (6×6 / 8×8 / 10×10), складністю.
- `help-window` — «Regeln», «Bedienungsanleitung», сторінка «Beispiel» (розбір позначено «wird ergänzt»).
- `+window:puzzle-info` (F1) — інфо про пазл і лист вебмайстру зі станом і ходами.
- CPUZZLE (цифрова версія Gardner): `match-setup` — номер гри 1–9999 або Random, «Show Pieces (Y/n)»; набір із 5 дошок, після пʼятої — сума запитань (`end-screen`).

## Фічі поза полем
- `auto-check` (F6) і автовизнання розвʼязку.
- `undo` / `redo` по одному й усі (Pos1 / Ende); `save-slots` (?) — Ctrl+S / Ctrl+L.
- `hint` — F3 ставить правильну фігуру; `show-solution` — F4 з логічним шляхом у списку ходів.
- `puzzle-bank` — 240 пазлів, рейтинг 1–8 за часом; пазли з відтворюваним шляхом — кольором.
- CPUZZLE: `seed-input` (номер гри, щоб порівняти результат з іншими), режим без зірочок (`difficulty-presets`), пропуск дошки зі штрафом (`skip-level`).
- VOZ Gerry Quinn (за Joerger): казкові фігури (`custom-rules`), розмір дошки, опція «мінімум інформації», миша.

## Варіації й родичі
- **Gardner / Poniachik (гра-запитання)**: 5 схованих чорних фігур K, Q, B, N, R на 8×8; гравець питає кількість атак на клітинку або «чи стоїть фігура P на X»; виграє той, хто знайде всі за найменше запитань. Позначені зірочкою клітинки — полегшений режим; без зірочок — складніше й з удачею.
- **Detektivschach Janko** — статичний пазл: усі «відповіді» вже дані числами.
- Gerry Quinn, Detective Chess / VOZ — генератор з казковими фігурами; Janko: не всі згенеровані пазли мають єдиний розвʼязок.
- У сімʼї: [N-Queens / Knight's Tour](n-queens-knights-tour.md) (розстановка за атаками), [Battleship Sudoku](battleship-sudoku.md) та [Star Battle](star-battle.md) (розстановка з підказками-лічильниками), [Undead](undead.md) (лічильники видимості).
- Поза сімʼєю: шахи (`chess-abstract`) — патерни ходів; Minesweeper / Battleship (`hidden-deduction`) — гра-запитання Gardner.
- **Осі варіацій**: набір фігур (класичні / казкові / два королі) · хто перекриває лінії (фігури / усе / ніщо) · позначені клітинки (дані / ні) · формат (статичні числа / запитання з лічильником).

## Цікавинки для курсу
- Підрахунок атак з перекриттям ліній (ray-cast у 8 напрямках + стрибки коня) — 🌱.
- Цикл фігур кліком і меню правою кнопкою — 🌱.
- Перевірка «набір використано повністю» + «усі числа збіглися» — 🌱.
- Гра-запитання Gardner: сховати фігури, рахувати запитання, режим без зірочок — 📎.
- Розвʼязувач: перестановки набору по позначених клітинках з відсіканням за числами — 🥉.
- Генератор з єдиним розвʼязком (Gerry Quinn не завжди вдавалося) — 🥇.

## Мапа на каталог
- Є: `piece-move-patterns` ↔ король/ферзь/тура/слон/кінь · `cursor-place` ↔ фігура на позначену клітинку · `markup-validity`, `completion-detection`, `satisfy-constraints` · `cell-click`, `keyboard-controls`, `conflict-highlight` · `level-bank`, `level-rating`, `puzzle-select` · `save-game`, `undo-redo`, `replay` ↔ розвʼязок F4 у списку ходів.
- Перевикористано: `+hint-reveal` ↔ F3, `+cell-coloring` ↔ кольорові маркери.
- **Нема** → пропозиції карток:
  - `+attack-count-clue` «Число = скільки фігур бʼє клітинку, з перекриттям ліній» · game-logic/constraints · 📎 · слот {pieces, blockers: pieces|all|none, mode: given|query}.
  - `+piece-set-placement` «Розставити заданий набір фігур на позначені клітинки» · entities/legality · 🌱 · слот {set, slots: marked|free}.

## Пропозиції до словників
- `+cond:attacked(cell, by)` — повтор (Chess, N-Queens).
- `+cond:attack_count(cell, n)` — клітинку бʼє рівно n фігур.
- `+cond:knight_move(a, b)` — повтор (N-Queens).
- `+ui:value-popup-menu`, `+ui:solved-frame`, `+window:puzzle-info` — повтори з Suraido (той самий applet Janko).
- `+card:attack-count-clue`, `+card:piece-set-placement` — див. мапу.

## Джерела
- ⭐ [Janko: Detektivschach](https://www.janko.at/Raetsel/Detektivschach/index.htm) — правила DE/EN, приклад `(1K,1D,2T,2L,2S)` з картинкою розвʼязку (перевірив блокування вручну), 240 пазлів, Gardner/Poniachik, посилання на Joerger і Gerry Quinn.
- [Janko: Detektivschach Nr. 1](https://www.janko.at/Raetsel/Detektivschach/001.a.htm) — дані пазла (6×6, `pieces k q r b n`, клітинки `x`, розвʼязок); також бачив 050/120/180/230/240 (10×10, `k2 q2 r2 b2 n2`).
- [Janko: Bedienung](https://www.janko.at/Raetsel/Detektivschach/Bedienung.htm) — цикл, меню, клавіші, F1/F3/F4/F6, undo, зелена рамка.
- [Mark Joerger: Chess Puzzle](http://runamok.tech/cpuzzle.html) — правила гри Gardner, режими «зірочки / без», CPUZZLE 1991, VOZ Gerry Quinn.
- [Wikipedia ES: Jaime Poniachik](https://es.wikipedia.org/wiki/Jaime_Poniachik) — біографія (про цей пазл не згадує).
- YouTube: пошук «detective chess logic puzzle».

## Непевне
- (?) Рік книги Gardner «Puzzles from Other Worlds»: Janko пише 1981, Joerger — 1984; рік винаходу Poniachik — невідомо.
- (?) Правила не кажуть явно, що числові клітинки прозорі, а фігури перекривають, — висновок з ручної перевірки прикладу й пазла 001.
- (?) Чи завжди кількість позначених = кількість фігур — бачив 6 пазлів, у всіх так.
- (?) Заголовок сторінки Janko «Detektivschach • Solitaire Chess» — не плутати з ThinkFun Solitaire Chess (там фігури бʼють одна одну); як aka не ставив.
- (?) Пішак (Bauer) є в легенді Bedienung, але не в меню й не в баченому наборі.
- (?) Сторінка Gerry Quinn (indigo.ie) не відкрилась.
