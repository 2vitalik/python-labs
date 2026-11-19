---
title: Tenner Grid (Zehnergitter, Числобус)
slug: tenner-grid
aka: [Zehnergitter, Tenner, Grid Ten, From 1 to 10, Числобус]
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
  - {kind: other, url: "https://www.janko.at/Raetsel/Zehnergitter/index.htm", best: true, note: "Janko: 4 правила DE/EN, Lexikon (автор невідомий, приклад зі старого номера Logisch), 400 пазлів, сортування за датою, розміром, складністю"}
  - {kind: play, url: "https://www.janko.at/Raetsel/Zehnergitter/001.a.htm", note: "аплет Janko, пазл №1 (Otto Janko, перша публікація)"}
  - {kind: other, url: "https://www.janko.at/Raetsel/Zehnergitter/Bedienung.htm", note: "керування аплетом: цифри, Enter/Space = +1, кандидати F7, кольори Alt+0…9, F6 перевірка, F4 розвʼязок, зелена рамка"}
  - {kind: other, url: "https://www.janko.at/Raetsel/Bedienung.htm", note: "загальна інструкція аплетів Janko: undo/redo, підказка F3, 9 слотів збереження, час брутто/нетто"}
  - {kind: other, url: "https://www.mathinenglish.com/puzzlestenner.php", note: "правила EN («Sudoku + Kakuro»), назви From 1 to 10 і Grid Ten, розміри 10×3…10×7, три рівні, друк"}
  - {kind: other, url: "https://crossword.nalench.com/en/tenner-gird/54207-chislobus-10x6-5-legkij.html", note: "«Числобус» 10×6 з відповіддю, правила EN з діагональною забороною"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=tenner+grid+puzzle", note: "пошук; розвʼязання"}
stage: v1
coverage: 75
mechanics: [satisfy-constraints, markup-validity, completion-detection, cell-click, keyboard-controls, pencil-marks, conflict-highlight, selection-highlight, line-sum-clue, undo-redo, level-solver, unique-puzzle-generation, difficulty-rating, level-bank, level-rating, puzzle-select, save-multi-slot, help-window, +full-set-once, +no-touch-8, +hint-reveal, +trial-mode, +solution-path-replay]
proposes: ["+card:solution-path-replay", "+ui:value-popup-menu", "+feature:net-time"]
author: opus
date: 2026-11-19
---

# Tenner Grid — у кожному рядку цифри 0–9 по разу, однакові не торкаються навіть кутом, стовпці дають задані суми

## Суть
Сітка шириною 10 клітинок і кількох рядків; під нею — рядок сум для кожного стовпця, частина цифр задана. Гравець дописує цифри так, щоб кожен рядок містив 0–9 рівно по разу, однакові цифри не стояли поруч ні по стороні, ні по діагоналі, а сума кожного стовпця дорівнювала підказці. Ядро — схрещення двох «дімів»: рядок як перестановка (судоку-правило), стовпець як сума з дозволеними повторами (какуро-правило; так його й описує mathinenglish).

## Поле і час
- Прямокутник 10 × R: ширина дорівнює розміру алфавіту 0–9; висота R — у mathinenglish 3…7 рядків (10×3, 10×4, 10×5, 10×6, 10×7), «Числобус» — 10×6; розміри банку Janko на сторінці не названі.
- Окремий рядок під сіткою — суми стовпців; він не заповнюється.
- Сусідство для заборони — 8 клітинок (король). Усередині рядка вона нічого не додає (цифри й так різні), тож реально працює між сусідніми рядками.
- Повтори в стовпці дозволені (mathinenglish: «Numbers may be repeated in columns»), але не в сусідніх рядках.
- Час статичний; хід — вписати, змінити чи стерти цифру.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Порожня клітинка | mark | 0–9 або порожньо | приймає одну цифру |
| Задана цифра | static | 0–9 | незмінна підказка |
| Рядок | zone | 10 клітинок | кожна цифра 0–9 рівно раз (сума рядка завжди 45) |
| Стовпець | zone | R клітинок | сума цифр = підказка; повтори лише не в сусідніх рядках |
| Підказка-сума | static | S під стовпцем | ціль суми свого стовпця |
| Кандидати | mark | множина ⊆ {0…9} | нотатка гравця (Janko F7) |
| Кольорова позначка ходу | mark | колір 0–9 | мітка групи ходів-гіпотези; група приймається чи скидається разом (Janko) |
| Символьна позначка | mark | 1 з 9 символів | нотатка в клітинці (Janko Ctrl+літера) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(digit, cell)` → ЯКЩО `not state(cell, given)` → ТО `set_value(cell, digit)`; задана клітинка — `block`.
- КОЛИ `input(enter, cell)` → ТО `custom: «значення +1 по колу»` (Janko: Enter, Space, Insert — «Wert = Wert+1»).
- КОЛИ `input(delete, cell)` → ТО `unmark(cell)` (Delete, Backspace).
- КОЛИ `input(left_click, cell)` → ТО `custom: «меню вибору значень»` (`+ui:value-popup-menu`); правий клік — меню кольору чи символу.
- КОЛИ `constraint_broken(row)` → ЯКЩО `not unique(row)` → ТО `custom: «дубль у рядку — червоним»` (Janko F6 «markiert alle Fehler … rot»).
- КОЛИ `adjacent8(a, b)` → ЯКЩО `same(a, b, digit)` → ТО `custom: «конфлікт: однакові цифри торкаються»`.
- КОЛИ `constraint_broken(column)` → ЯКЩО `count(empty_in_column, ==, 0)` and `not sum(column, S)` → ТО `custom: «стовпець з хибною сумою»`.
- КОЛИ `input(hint, cell)` → ЯКЩО `mode(hint)` → ТО `reveal(cell)` (Janko F3: правильне значення обраної клітинки).
- КОЛИ `input(solve)` → ТО `custom: «вписати розвʼязок; повторно — шлях розвʼязання у список ходів (поточні ходи зникають)»` (Janko F4).
- КОЛИ `input(accept_color)` → ТО `custom: «прийняти всі значення поточного кольору»` (F8).
- КОЛИ `input(drop_color)` → ТО `custom: «стерти всі значення поточного кольору»` (F9).
- КОЛИ `all_constraints_met` → ТО `win`, `custom: «зелена рамка навколо діаграми»` (Janko).
- Наслідок: сума всіх підказок = 45 · R — швидка перевірка умови.
- Дедукція «остання клітинка»: у стовпці лишилась одна порожня → цифра = S − сума решти.
- Дедукція «сусідній рядок»: цифра d у (r, c) виключає d з (r±1, c−1…c+1) — у сусідньому рядку d стоїть щонайменше за 2 стовпці.
- Дедукція «прихована одиниця»: цифра d у рядку можлива лише в одній клітинці → вона там.
- Дедукція «межі суми»: решта стовпця має вміститись між мінімумом і максимумом допустимих цифр, з урахуванням що сусіди по вертикалі різні.
- Перемога: усі клітинки заповнені, три обмеження виконані. Поразки й рахунку нема (Janko лише показує час).

## Керування і ввід
- Janko, клавіатура: стрілки — рамка вибору; цифрові клавіші — пряме введення; Enter / Space / Insert — значення +1; Delete / Backspace — стерти.
- Janko, миша й тач: лівий клік / тап — меню значень; правий клік / утримання — попап кольору або символу.
- Кандидати: F7 або значок перемикає режим; повторне введення цифри прибирає її зі списку.
- Позначки: Ctrl + Q W E R X A B C D — один із 9 символів у клітинці; Alt+0…9 — колір наступних ходів.
- Історія: PgUp / Ctrl+Z — крок назад, Home — усе; PgDn — крок уперед, End — усе (redo лише одразу після undo).
- Папір (mathinenglish, «Числобус»): друкована сітка, цифри ручкою.

## Вікна, меню, HUD
- `game-screen` (Janko): діаграма 10×R з рядком сум, рамка вибору (`selection-highlight`), `pencil-marks`, `conflict-highlight` (червоне за F6), зелена рамка при розвʼязку; панель значків: кандидати, перевірка, підказка, розвʼязок, undo/redo, збереження, завантаження, info.
- `+ui:value-popup-menu` — меню вибору цифри по кліку.
- `help-window`: на сторінці пазла згортні розділи «Regeln», «Bedienungsanleitung», «Quelle und Copyright».
- `custom-window` info (F1): час брутто (від відкриття) і нетто (оцінка без пауз).
- `save-slots` (Ctrl+S / Ctrl+L): 1 серверний слот на 10 днів (з cookie) + 8 локальних до закриття вікна.
- `puzzle-select` (сторінка жанру): 400 пазлів, сортування за датою / розміром / складністю; кольором — пазли з відтворюваним логічним шляхом.
- Переходи: сторінка жанру → пазл NNN → F6 / зелена рамка → «Weiter» (наступний).

## Фічі поза полем
- `undo` / `redo` (крок або все), `hint` (F3), `show-solution` + шлях розвʼязання у список ходів (F4), `auto-check` за кнопкою (F6).
- Колірні гіпотези: ходи одного кольору приймаються (F8) або стираються (F9) разом — аналог trial-режиму puzz.link.
- `save-slots` (сервер + локальні), час брутто/нетто (`+feature:net-time`).
- `puzzle-bank` з рейтингом складності за часом розвʼязування (leicht 1–3, 4–8, schwer), незалежно від розміру.
- Друк: Janko — «interaktiv/online … oder ausgedruckt»; mathinenglish — друковані добірки Easier / Challenging / Harder для кожного розміру.

## Варіації й родичі
- [Kakuro](kakuro.md) — суми прогонів без повторів; [Sudoku](sudoku.md) — «дім» без повторів.
- [Survo](survo-puzzle.md) — суми рядків і стовпців, але числа 1…m·n по разу на все поле.
- [Star Battle](star-battle.md), [Battleship Sudoku](battleship-sudoku.md) — та сама заборона дотику в 8-сусідстві.
- [Magic and Latin squares](magic-latin-squares.md) — предки: перестановки в лініях і суми ліній.
- [Sumplete](../word-number/sumplete.md) — суми рядків і стовпців, але викреслюванням.
- **Осі варіацій**: що унікальне (рядок — Tenner / усе поле — Survo / прогін — Kakuro) · де суми (стовпці / рядки й стовпці / прогони) · заборона сусідства (8 / 4 / нема) · алфавіт (0–9 / 1–9 / 1…m·n).

## Цікавинки для курсу
- Перевірка рядка-перестановки 0–9 (множина з 10 значень) — 🌱.
- Заборона дотику однакових у 8-сусідстві; фактично порівняння двох сусідніх рядків — 🌱.
- Суми стовпців з ранньою перевіркою «вже перебір / вже не добрати» — 📎.
- Розвʼязувач рядок за рядком: 10! = 3 628 800 перестановок на рядок, тож без обрізання за сусідством і частковими сумами не обійтись — 🥈.
- Генератор з єдиним розвʼязком: рядки-перестановки з умовою «не торкаються» → суми → прибирати задані з перевіркою єдиності — 👑 (`unique-puzzle-generation`).
- Колірні групи ходів-гіпотез (позначити кольором, потім прийняти чи скинути групу) — 📎.

## Мапа на каталог
- Є: `satisfy-constraints` · `markup-validity` · `completion-detection` · `cell-click` · `keyboard-controls` · `pencil-marks` · `conflict-highlight` · `selection-highlight` · `line-sum-clue` ↔ суми стовпців · `undo-redo` · `level-solver` · `unique-puzzle-generation` · `difficulty-rating` ↔ складність за часом · `level-bank`, `level-rating`, `puzzle-select` ↔ банк Janko · `save-multi-slot` ↔ 9 слотів · `help-window`.
- Перевикористано: `+full-set-once` ↔ рядок = 0–9 рівно раз · `+no-touch-8` (Star Battle, Tents) ↔ однакові не торкаються кутом · `+hint-reveal` ↔ F3 · `+trial-mode` (puzz.link) ↔ колірні групи F8/F9.
- **Нема** → пропозиції карток:
  - `+solution-path-replay` «Логічний шлях розвʼязання як список ходів, який можна програти» · interface/hud · 📎 — Janko F4 і позначка в банку.

## Пропозиції до словників
- `+card:solution-path-replay` — шлях розвʼязання програється кроками зі списку ходів (Janko, усі жанри).
- `+ui:value-popup-menu` — меню значень по кліку на клітинку (повтор з Arofuro, Sukoro, Karakiri).
- `+feature:net-time` — «чистий» час розвʼязування без пауз, поруч із загальним (Janko info: брутто / нетто).

## Джерела
- ⭐ [Janko: Zehnergitter](https://www.janko.at/Raetsel/Zehnergitter/index.htm) — 4 правила DE/EN, автор і місце першої публікації невідомі, приклад зі старого номера журналу Logisch, 400 пазлів, складність за часом, позначка відтворюваного шляху.
- [Janko: пазл №1](https://www.janko.at/Raetsel/Zehnergitter/001.a.htm) — аплет; автор Otto Janko, перша публікація, CC BY-NC-SA 3.0.
- [Janko: керування Zehnergitter](https://www.janko.at/Raetsel/Zehnergitter/Bedienung.htm) — клавіші, кандидати, кольори, символи, F6, F4, зелена рамка.
- [Janko: загальна інструкція](https://www.janko.at/Raetsel/Bedienung.htm) — undo/redo, F3, збереження, F8/F9, час брутто/нетто.
- [Math in English: Tenner](https://www.mathinenglish.com/puzzlestenner.php) — правила EN, назви From 1 to 10 і Grid Ten, розміри 10×3…10×7, три рівні.
- [«Числобус» 10×6](https://crossword.nalench.com/en/tenner-gird/54207-chislobus-10x6-5-legkij.html) — правила EN, діагональна заборона, приклад з відповіддю.
- YouTube: [пошук «tenner grid puzzle»](https://www.youtube.com/results?search_query=tenner+grid+puzzle).

## Непевне
- (?) Хто і коли придумав жанр — невідомо навіть Janko; рік лишаю порожнім.
- (?) Розміри сіток у банку Janko — на сторінці жанру не названі; заголовок «~100» у сортуванні за розміром не пояснено.
- (?) У шаблоні керування Janko клавіша 0 значиться серед «стерти»; як тоді вводиться цифра 0 — не перевірено.
- (?) Варіанти з неповними сумами чи з сумами рядків — у джерелах не бачив.
- (?) Чи підсвічує Janko порушення дотику й суми окремо від дублів у рядку — сказано лише «усі помилки червоним».
