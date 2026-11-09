---
title: Suraido (スライド)
slug: suraido
aka: [スライド]
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
  - {kind: other, url: "https://www.janko.at/Raetsel/Suraido/index.htm", best: true, note: "Janko: правила DE/EN, приклад і розвʼязок, автор R. M. Renger Kas, 40 пазлів 9×9, рейтинг 1–8"}
  - {kind: play, url: "https://www.janko.at/Raetsel/Suraido/001.a.htm", note: "applet Janko (Kendoku.js); у коді сторінки — блок даних problem/solution/moves"}
  - {kind: other, url: "https://www.janko.at/Raetsel/Suraido/Bedienung.htm", note: "керування applet-а: меню значень, кандидати F7, помилки F6, підказка F3, розвʼязок F4"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=suraido+sudoku+puzzle", note: "пошук; розвʼязання"}
stage: v1
coverage: 65
mechanics: [markup-validity, completion-detection, satisfy-constraints, cell-click, keyboard-controls, pencil-marks, conflict-highlight, level-bank, level-rating, puzzle-select, save-game, undo-redo, replay, +latin-square, +cross-multiset-clue, +hint-reveal, +cell-coloring]
proposes: ["+cond:multiset_eq(cells, digits)", "+cond:duplicate_in_line", "+ui:value-popup-menu", "+ui:solved-frame", "+window:puzzle-info", "+card:cross-multiset-clue"]
author: opus
date: 2026-11-09
---

# Suraido — судоку, де цифри підказки треба «розсунути» на саму клітинку та її чотирьох сусідів

## Суть
Поле 9×9 з блоками 3×3, як у судоку, але готових цифр нема. У деяких клітинках дрібно записано набір цифр (напр. `25889`): ці цифри треба розподілити між самою клітинкою та її орто-сусідами, по одній на клітинку. Решту поля заповнити так, щоб у кожному рядку, стовпці й блоці кожна цифра 1–9 була рівно раз. Незвичне: підказка — **мультимножина без порядку** на хресті з 3–5 клітинок, а хрести різних підказок перекриваються. Назва — японське スライド, співзвучне англ. «slide».

## Поле і час
- Квадратна сітка 9×9, товсті лінії ділять її на 9 «Gebiete» (у прикладі — стандартні блоки 3×3).
- Клітинка-підказка: зверху дрібний рядок цифр, знизу — велика цифра, яку вписує гравець (клітинка-підказка теж частина судоку).
- Кількість цифр у підказці = 1 + кількість орто-сусідів: 4 біля краю (`5679`, `1479`), 5 усередині (`25889`).
- Цифри в підказці відсортовані й можуть повторюватись (`11389`, `25889`).
- Час статичний; пазли авторські (40 шт. на Janko), генератора нема.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітинка | mark | цифра 1–9 або порожньо | одна цифра; рядок/стовпець/блок без повторів |
| Клітинка-підказка | mark | мультимножина k цифр, k = 1 + сусіди | сама отримує одну з цих цифр |
| Хрест підказки | zone | клітинка + 2–4 орто-сусіди | мультимножина вписаних цифр = підказка |
| Рядок / стовпець | zone | 9 клітинок | кожна цифра 1–9 рівно раз |
| Блок (Gebiet) | zone | 9 клітинок, межа товстою лінією | кожна цифра 1–9 рівно раз |
| Кандидати | mark | список цифр | режим F7: редагується список можливих значень |
| Кольорова позначка | mark | колір 0–9 | фарбує наступні ходи (Alt+0…9), на перевірку не впливає |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left_click, cell)` → ТО `choose(«1…9 · • очистити»)` → `set_value(cell, d)` (Janko: «Auswahlmenü → Werte»).
- КОЛИ `input(right_click, cell)` → ТО `choose(«маркери»)` → `mark(cell, symbol)` (Janko: «Auswahlmenü → Markierungen»).
- КОЛИ `input(key_digit)` → ЯКЩО `custom: «клітинка під рамкою клавіатури або під мишею»` → ТО `set_value(cell, d)`.
- КОЛИ `input(enter|space|insert)` → ТО `custom: «значення → значення+1»` (циклічне перебирання).
- КОЛИ `input(del|backspace|x|,|/|-)` → ТО `unmark(cell)`.
- КОЛИ `input(F7)` → ТО `set_state(board, candidate_mode)`; КОЛИ `input(key_digit)` → ЯКЩО `state(board, candidate_mode)` → ТО `mark(cell, candidate d)`.
- Судоку: ЯКЩО `unique(row)` and `unique(col)` and `unique(region)` → обмеження виконано; інакше `constraint_broken(custom: «повтор цифри»)` (`+cond:duplicate_in_line`).
- Хрест: ЯКЩО `custom: «мультимножина цифр клітинки-підказки та її орто-сусідів = цифри підказки»` (`+cond:multiset_eq`) → підказка задоволена; інакше `constraint_broken(custom: «хрест не збігся»)`.
- КОЛИ `input(F6)` → ТО `custom: «усі порушення правил — червоним»` (`conflict-highlight`).
- КОЛИ `input(F3)` → ТО `set_state(board, hint_mode)`; КОЛИ `input(click, cell)` → ЯКЩО `state(board, hint_mode)` → ТО `set_value(cell, solution)` (Janko: «Tipp-Modus»).
- КОЛИ `input(F4)` → ТО `custom: «вписати розвʼязок і логічний шлях у список ходів»`.
- КОЛИ `input(ctrl_z|page_up)` → ТО `undo(1)`; `input(pos1)` → `undo(all)`; `input(ctrl_y|page_down)` → `custom: «redo»`; `input(end)` → `custom: «redo всіх»`.
- КОЛИ `all_constraints_met` → ТО `win` + `custom: «зелена рамка навколо поля»`.
- Дедукція «перетин хрестів»: спільна клітинка кількох хрестів має кандидатами перетин їхніх мультимножин. У прикладі Janko r2c2 лежить у хрестах `5679`, `1479`, `25889`, `11389` → лишається лише 9.
- Дедукція «повтор»: дві однакові цифри в підказці (`25889`) лягають лише в пару клітинок хреста, що не мають спільного рядка, стовпця чи блоку.
- Дедукція «чужа цифра»: цифра, якої нема в підказці, заборонена в усіх клітинках хреста.
- Дедукція «центр»: цифра клітинки-підказки — одна з цифр її підказки.
- Далі — звичайні техніки судоку (Janko: «Lösungstechniken wie bei Sudoku»).
- Перемога: коректне судоку + усі хрести збіглися. Поразки й рахунку нема.

## Керування і ввід
- Миша: лівий клік — меню значень (1…9, «•» — очистити); правий клік — меню маркерів і кольорів.
- Дотик: тап — меню значень; утримання — меню маркерів.
- Клавіатура: стрілки — рамка вибору; цифри — значення; Enter/Space/Insert — значення+1; Del/⌫/X/,/-// — очистити.
- Наведення без кліку + клавіша — вписати в клітинку під мишею.
- F7 — режим кандидатів; Alt+0…9 — колір наступних ходів; Ctrl+Q/W/E/R/X/A/B/C/D — символьні маркери.
- Папір: вписати цифри; кандидати олівцем.

## Вікна, меню, HUD
- `game-screen`: сітка 9×9 з товстими межами блоків; підказки дрібно вгорі клітинки; дані цифри сині, цифри гравця чорні; кандидати, кольорові позначки; `conflict-highlight` (F6, червоним); зелена рамка після розвʼязання (`+ui:solved-frame`).
- `+ui:value-popup-menu` — спливне меню значень/маркерів біля клітинки.
- `help-window` — розкривні блоки «Regeln», «Bedienungsanleitung», «Quelle und Copyright» на сторінці пазла.
- `puzzle-select` — індекс Janko: 40 пазлів за датою, розміром, складністю.
- `+window:puzzle-info` (F1) — інформація про пазл і лист вебмайстру з поточним станом і списком ходів.
- Переходи: індекс → сторінка пазла; «Zurück»/«Weiter», Ctrl+PgUp/PgDn — сусідній пазл.

## Фічі поза полем
- `auto-check` за F6; автоматичне виявлення розвʼязку (зелена рамка).
- `undo` / `redo` по одному й усі разом (Pos1 / Ende).
- `hint` — режим F3: правильне значення в обрані клітинки; `show-solution` — F4 з логічним шляхом у списку ходів (його можна «програти» redo-кроками).
- `save-slots` (?) — Ctrl+S / Ctrl+L: зберегти й завантажити стан.
- `puzzle-bank` — 40 пазлів, рейтинг 1–8 лише за часом розвʼязання; пазли з логічно відтворюваним шляхом виділено кольором.
- Масштаб поля (клік / Ctrl+стрілки), друк для паперу.

## Варіації й родичі
- У сімʼї: [Sudoku](sudoku.md) (ядро), [Sudoku variants](sudoku-variants.md), [Sudoku line/dot variants](sudoku-line-dot-variants.md) — інші накладені обмеження; [Kakuro](kakuro.md), [KenKen](kenken.md) — підказка про групу клітинок, але сума/операція, а не мультимножина.
- Janko називає родичами Sudoku, Sukaku (клітинки з наборами кандидатів) і числові пазли.
- suraido.nl — сайт автора з багатьма пазлами (не відкрився, див. «Непевне»).
- **Осі варіацій**: форма «хреста» (орто-сусіди / 8 сусідів / рядок) · що в підказці (мультимножина / сума / множина) · чи дані цифри є взагалі (тут — ні).

## Цікавинки для курсу
- Перевірка «мультимножина хреста = підказка» через `Counter` — 🌱.
- Рендер клітинки з двома шарами: дрібна підказка + велика цифра — 🌱.
- Кандидати з перетину хрестів + латинські виключення — 📎.
- Розвʼязувач: судоку-backtracking з обмеженням хрестів (виключення «чужих» цифр) — 🥉.
- Генератор: заповнене судоку → обрати клітинки-підказки → прибрати все інше з перевіркою єдиності — 🥇.
- Список ходів «логічного шляху», який гравець програє кроками redo — 📎.

## Мапа на каталог
- Є: `markup-validity`, `completion-detection`, `satisfy-constraints` · `cell-click`, `keyboard-controls`, `pencil-marks`, `conflict-highlight` · `level-bank`, `level-rating`, `puzzle-select` · `save-game` ↔ Ctrl+S/L · `undo-redo` · `replay` ↔ розвʼязок F4 як список ходів.
- Перевикористано: `+latin-square` (рядки/стовпці), `+hint-reveal` ↔ F3, `+cell-coloring` ↔ кольорові позначки.
- **Нема** → пропозиції карток:
  - `+cross-multiset-clue` «Підказка = мультимножина цифр клітинки та її сусідів, без порядку» · game-logic/constraints · 🌱 · слот {shape: cross|ring8|line}.

## Пропозиції до словників
- `+cond:multiset_eq(cells, digits)` — мультимножина значень групи клітинок дорівнює заданій.
- `+cond:duplicate_in_line` — повтор (KenKen, Skyscrapers, Futoshiki).
- `+ui:value-popup-menu` — спливне меню значень біля клітинки (Janko-applet).
- `+ui:solved-frame` — рамка навколо поля як сигнал розвʼязку.
- `+window:puzzle-info` — повтор: вікно інформації про пазл.
- `+card:cross-multiset-clue` — див. мапу.

## Джерела
- ⭐ [Janko: Suraido](https://www.janko.at/Raetsel/Suraido/index.htm) — правила DE/EN, приклад і розвʼязок (картинки Regeln-01/02), автор R. M. Renger Kas, 40 пазлів 9×9, рейтинг 1–8, етимологія スライド.
- [Janko: Suraido Nr. 1](https://www.janko.at/Raetsel/Suraido/001.a.htm) — блок даних: підказки `5679`, `25889`…, розвʼязок і список ходів; перевірив хрести вручну.
- [Janko: Bedienung](https://www.janko.at/Raetsel/Suraido/Bedienung.htm) — меню значень, F7/F6/F3/F4/F1, undo/redo, Ctrl+S/L, зелена рамка.
- YouTube: пошук «suraido sudoku puzzle».

## Непевне
- (?) Рік винаходу і першої публікації — не вказано; suraido.nl не відкрився (самопідписаний сертифікат).
- (?) Чи бувають Suraido з нерегулярними «Gebiete» або іншими розмірами — на Janko лише 9×9 зі стандартними блоками.
- (?) Чи може підказка стояти в куті (3 цифри) — у прикладі таких нема; правило це дозволяє.
- (?) `save-slots`: Ctrl+S/L — один слот чи кілька, не описано.
- (?) Поле `unit 40` у даних пазла — сенс не зрозумів.
