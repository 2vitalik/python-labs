---
title: Nonogram (Японський кросворд, Picross, Griddlers, Hanjie)
slug: nonogram
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
year: 1987
platforms: [paper, web, mobile, Game Boy, Nintendo DS, 3DS, Switch]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Nonogram", best: true, note: "правила, історія, техніки по рядку, варіанти, NP-повнота"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Mario%27s_Picross", note: "30 хв, штрафи 2/4/8 хв за помилку, hint-рулетка"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Picross_DS", note: "Normal vs Free mode, Daily Picross, My Picross"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Picross_S", note: "серія Switch з 2017 (S…S9, S+ 2024, ліцензійні випуски до 2026): Clip (S2), Color (S3), Extra (S4)"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Picross_e", note: "серія 3DS: e (2011) … e9 (2018)"}
  - {kind: official, url: "https://www.nintendo.com/us/store/products/picross-s-switch/", note: "Picross S (Jupiter, 28.09.2017): Picross + Mega Picross, 300 пазлів, 2 гравці одночасно, тач, assist"}
  - {kind: official, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/pattern.html", note: "Tatham Pattern: керування мишею й клавіатурою, drag лінією, Custom: ширина/висота"}
  - {kind: official, url: "https://www.conceptispuzzles.com/index.aspx?uri=puzzle/pic-a-pix", note: "Conceptis Pic-a-Pix: ч/б і кольорові правила (різнокольорові блоки можуть торкатись)"}
  - {kind: play, url: "https://puzz.link/rules.html?nonogram", note: "puzz.link: плеєр і редактор"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=picross+s+gameplay", note: "пошук; геймплей Picross S"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=picross", note: "пошук Steam: Picross-подібні"}
stage: v2
coverage: 75
mechanics: [markup-validity, completion-detection, satisfy-constraints, cell-click, wrong-mark-lose, time-out, difficulty-levels, level-bank, level-select, unique-puzzle-generation, level-solver, in-game-editor, level-exchange, daily-puzzle, score-records, +run-length-clues, +cross-mark, +drag-paint-line, +clue-greying, +auto-cross-line, +mistake-time-penalty, +picture-reveal, +mega-clue, +color-runs, +clip-composite]
proposes: ["+role:clue-outside", "+cond:line_runs", "+effect:timer(-n)", "+ui:clue-greyed", "+ui:row-column-guide", "+feature:time-penalty", "+feature:try-it-out", "+feature:picture-reveal", "+window:picture-gallery"]
author: opus
date: 2026-11-02
---

# Nonogram — зафарбуй клітинки за довжинами серій у рядках і стовпцях, отримай малюнок

## Суть
Над кожним стовпцем і зліва від кожного рядка — список чисел: довжини послідовних серій зафарбованих клітинок у цьому ряду, по порядку. Гравець фарбує клітинки й ставить хрестики («точно порожньо»), розвʼязуючи ряд за рядом; результат — піксельний малюнок. Цифрові версії (Nintendo Picross із 1995) додали те, чого нема на папері: миттєву перевірку помилок зі штрафом часу, hint-рулетку, кольорові й «мега» підказки, складені з кількох пазлів картини.

## Поле і час
- Прямокутна сітка: Mario's Picross 5×5 / 10×10 / 15×15; Picross S Extra — 30×30 і 40×30; Tatham — довільна ширина/висота.
- Зовнішнє кільце підказок: ліворуч від рядків і над стовпцями; кожна підказка — послідовність чисел (або `0`/порожньо — ряд пустий).
- Стан клітинки: unknown / filled / cross. Сітка ділиться жирними лініями кожні 5 клітинок (у пізніх S — чергування кольорів смуг по 5 (?)).
- Час статичний, але в Nintendo-режимах є таймер: ліміт 30 хв (Mario's Picross) або лічильник часу з рейтингом.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітинка | mark | unknown / filled / cross | фарбується, хреститься, очищується |
| Підказка ряду | static | список довжин [a, b, …] | серії filled у ряду точно відповідають списку за порядком; між серіями ≥1 порожня |
| Підказка числа (одиничне) | static | n | сіріє, коли відповідна серія однозначно стоїть (у частині плеєрів) |
| Кольорова підказка | static | (довжина, колір) | Color Picross / Color Pic-a-Pix: серії різних кольорів можуть торкатись, однакових — ≥1 порожня між ними |
| Мега-підказка | static | n на 2 ряди | Mega Picross: число охоплює два рядки/стовпці — звʼязна фігура з n клітинок у цій парі (?) |
| Хрестик | mark | — | «точно порожньо»; у перевірці = порожньо |
| Малюнок | zone | вся сітка | зʼявляється анімацією й назвою після розвʼязання |
| Clip-фрагмент | zone | маленький пазл | Clip Picross: кожен пазл — шматок великої картини |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(fill, cell)` → ТО `mark(cell, filled)`; повтор → `unmark(cell)`.
- КОЛИ `input(cross, cell)` → ТО `mark(cell, cross)`.
- КОЛИ `input(drag, cells)` → ТО `mark(cells, state_of_first)` — протяжка по рядку/стовпцю (Tatham: ліва drag — лінія чорних, права — лінія білих, вертикально чи горизонтально; середня/Shift-drag — прямокутник unknown).
- КОЛИ `input(fill, cell)` → ЯКЩО `mode(normal)` and `custom: «клітинка в розвʼязку порожня»` → ТО `block`, `mark(cell, cross_red)`, `counter(mistakes, +1)`, `timer(-penalty)`: 2 хв → 4 хв → 8 хв і далі по 8 (Mario's Picross, Picross DS Normal).
- КОЛИ `counter(time_left, ==, 0)` → ТО `lose` (Mario's Picross: Маріо падає, гра закінчена).
- КОЛИ `input(fill, cell)` → ЯКЩО `mode(free)` → ТО `mark(cell, filled)` без перевірки (Picross DS Free: помилки не показуються).
- КОЛИ `input(fill, cell)` → ЯКЩО `mode(like_paper)` and `custom: «помилка»` → ТО `lose` (картка `wrong-mark-lose`) / `lives(-1)` у мобільних (?).
- КОЛИ `constraint_broken(line_runs)` — ряд заповнено, а серії ≠ підказці → ТО `custom: «підказка ряду червоніє»` (?).
- КОЛИ `custom: «серії ряду вже відповідають підказці»` → ТО `custom: «підказки сіріють»`; ЯКЩО `mode(auto_cross)` → ТО `mark(rest_of_line, cross)` (?).
- КОЛИ `level_start` → ЯКЩО `mode(hint)` → ТО `custom: «рулетка по рядках і стовпцях»`, `reveal(row, col)` — гравець напівактивно зупиняє рулетку (Mario's Picross); що час позначається «з підказкою» — (?). Picross DS: hint відкриває випадковий рядок і стовпець без впливу на час (крім Daily й Online).
- КОЛИ `all_constraints_met` → ТО `win`, `timer(stop)`, `custom: «показати малюнок і назву»`, `window(end-screen)`.
- КОЛИ `win` → ЯКЩО `custom: «кожен 5-й/10-й/15-й пазл сторінки»` → ТО `unlock(clip_set)` (Clip Picross, S2).
- Перемога: усі ряди відповідають підказкам (у Nintendo — збіг з єдиним задуманим малюнком). Поразка: час вичерпано (Mario's Picross) або помилка в «паперовому» режимі. Рахунок: час; Daily Picross DS — оцінка кожного челенджу від A, +5 с за помилку; п'ять A → загальна S.

## Керування і ввід
- Курсор + дві кнопки: A — «долото» (fill), B — хрестик; утримання й рух — протяжка по рядку (Nintendo (?)). Picross S — також тач.
- Мишка (Tatham): ліва — чорна, права — біла (хрестик), середня або Shift+клік — повернути unknown; drag заповнює лінію; клавіатура: стрілки, Enter/Space циклюють стан (у протилежних напрямках), Ctrl — фарбує пройдене чорним, Shift — білим, обидва — сірим.
- Picross DS Free: «Try it Out» — тимчасовий шар припущень, який можна застосувати або стерти.
- Picross S: двоє гравців одночасно на одній консолі (з S8 — до 4).

## Вікна, меню, HUD
- `main-menu` (Picross S): Picross · Mega Picross · Clip Picross · Color Picross · Extra · Tutorial · Options (?).
- `puzzle-select` — сітка пазлів сторінками з позначками «розвʼязано» й найкращим часом; Clip — макет великої картини з дірками.
- `game-screen`: сітка + підказки зліва/зверху + `timer-elapsed`/`timer-countdown` + `+ui:row-column-guide` (підсвітка рядка/стовпця курсора) + `+ui:clue-greyed` + кнопки fill/cross + `undo-button`.
- `end-screen` — анімований малюнок, назва, час.
- `tutorial-window` — навчальний пазл (Picross S).
- `editor-window` — My Picross (DS): створити й надіслати друзям (локально чи онлайн), автоматична оцінка складності 1–4 зірки; Classic-паки з Wi-Fi (до 10).
- `daily-window` — Daily Picross (DS): 5 челенджів 7×7 (Nonstop Time Attack, No X Marks, Error Search, Memory, Secret), відкриваються на 0/3/7/12/20-й день гри.
- Переходи: main-menu → режим → puzzle-select → game-screen → end-screen → puzzle-select.

## Фічі поза полем
- `mistake-limit` у вигляді штрафу часу (`+feature:time-penalty`), `hint` (рулетка), `assist-mode` (S-серія: «Assist functions» — підсвітки й навігація (?)).
- `difficulty-presets` = розмір поля (Picross DS: 5×5 … 25×20, по 15 пазлів на рівень); `level-select`/`puzzle-bank` з сотнями пазлів (Picross S — 300).
- `daily-puzzle` + оцінки; `stats` найкращих часів; `autosave`.
- `level-editor` + `level-sharing` (My Picross, puzz.link edit, Tatham Game ID).
- `+feature:picture-reveal` — малюнок як нагорода; галерея пройдених (?).
- Tatham Pattern: генерація випадкових пазлів (без малюнка), Custom — лише ширина й висота; `seed-input`, Solve (?).

## Варіації й родичі
- Nintendo/Jupiter: Mario's Picross (Game Boy, 1995) → Picross DS (2007) → Picross 3D → Picross e (3DS, 2011–2018) → Picross S (Switch, з 2017: S…S9, S+ 2024, ліцензійні S-випуски — до 2026).
- Режими S-серії: Mega Picross (мега-підказки на 2 ряди) · Clip Picross (S2: пазли-шматки великої картини) · Color Picross (S3: кольорові серії) · Extra (S4: два 30×30 + 40×30 за кожну попередню S у бібліотеці) · мультиплеєр до 4 (S8).
- Conceptis Pic-a-Pix (ч/б і кольорові, Mega 100×60), Triddlers (трикутники), Link-a-Pix, Fill-a-Pix, Maze-a-Pix, Tile Paint, pentomino paint-by-numbers.
- **Осі варіацій**: ціна помилки (нічого / штраф часу / програш / нічого не видно) · колір (1 / кілька) · геометрія підказки (1 ряд / 2 ряди — Mega) · розмірність (2D / 3D куб) · композиція (один пазл / мозаїка з Clip-пазлів).

## Цікавинки для курсу
- Перевірка ряду за списком серій (run-length encoding) — 🌱; підсвітка виконаних підказок — 📎.
- Протяжка drag по рядку з фіксацією напрямку й стану першої клітинки — 📎.
- Режими помилок: штраф 2/4/8 хв + таймер / без перевірки / «паперовий» програш — 🥉 як налаштування гри.
- Лінійний розвʼязувач (перетин усіх розміщень серій у ряду, ітерація рядки↔стовпці) — 🥈; повний з перебором — 🥇.
- Картинка → пазл: генерація підказок з піксель-арту + перевірка унікальності — 👑.
- Color Picross (сусідні серії різного кольору без пропуску) — 🥉; Mega-підказки — 🥇.

## Мапа на каталог
- Є: `markup-validity` ↔ ряд ≠ підказці · `completion-detection`, `satisfy-constraints` · `cell-click` · `wrong-mark-lose` ↔ «like paper» · `time-out` ↔ 30 хв · `difficulty-levels` ↔ розмір · `level-bank`, `level-select` · `unique-puzzle-generation`, `level-solver` · `in-game-editor`, `level-exchange` ↔ My Picross · `daily-puzzle` ↔ Daily Picross · `score-records` ↔ найкращий час.
- **Нема** → пропозиції карток:
  - `+run-length-clues` «Підказки довжин серій» · game-logic/constraints · 🌱.
  - `+cross-mark` «Хрестик "точно порожньо"» · interface/input · 🌱.
  - `+drag-paint-line` «Протяжка станом по рядку/стовпцю» · interface/input · 📎.
  - `+clue-greying` «Виконані підказки сіріють» · interface/hud · 📎.
  - `+auto-cross-line` «Автохрестики в завершеному ряду» · interface/input · 📎.
  - `+mistake-time-penalty` «Штраф часу, що зростає з помилками» · game-logic/lose · 📎 · слот {penalties: [2,4,8]}.
  - `+picture-reveal` «Малюнок-нагорода після розвʼязання» · interface/graphics · 🌱.
  - `+mega-clue` «Підказка на два ряди» · game-logic/constraints · 🥇.
  - `+color-runs` «Кольорові серії» · game-logic/constraints · 🥉.
  - `+clip-composite` «Велика картина з малих пазлів» · levels/progression · 📎.

## Пропозиції до словників
- `+role:clue-outside` — підказка поза полем, привʼязана до ряду (спільна з sudoku-variants).
- `+cond:line_runs` — серії ряду відповідають підказці.
- `+effect:timer(-n)` — значення для `timer(...)`: відняти час як штраф.
- `+ui:clue-greyed` — виконана підказка сіріє; `+ui:row-column-guide` — підсвітка рядка й стовпця під курсором.
- `+feature:time-penalty` — помилка коштує час, а не життя; `+feature:try-it-out` — тимчасовий шар припущень (Picross DS); `+feature:picture-reveal` — малюнок-нагорода.
- `+window:picture-gallery` — галерея розвʼязаних малюнків / макет Clip-картини (?).

## Джерела
- ⭐ [Wikipedia: Nonogram](https://en.wikipedia.org/wiki/Nonogram) — правила, Non Ishida (1987) і незалежно Tetsuya Nishio, назви, техніки по рядку, варіанти, NP-повнота.
- [Wikipedia: Mario's Picross](https://en.wikipedia.org/wiki/Mario%27s_Picross) — 30 хв, штрафи 2/4/8 хв, hint-рулетка, долото й хрестик.
- [Wikipedia: Picross DS](https://en.wikipedia.org/wiki/Picross_DS) — Normal/Free, Try it Out, hint, Daily (5 челенджів, +5 с, A → S), My Picross, розміри до 25×20.
- [Wikipedia: Picross S](https://en.wikipedia.org/wiki/Picross_S) — серія з 2017, Clip (S2), Color (S3), Extra (S4), мультиплеєр (S8).
- [Wikipedia: Picross e](https://en.wikipedia.org/wiki/Picross_e) — серія 3DS, e (2011) … e9 (2018).
- [Nintendo: Picross S](https://www.nintendo.com/us/store/products/picross-s-switch/) — Jupiter, 28.09.2017: Picross + Mega Picross, 300 пазлів, 2 гравці одночасно, тач, assist.
- [Tatham Pattern](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/pattern.html) — керування мишею/клавіатурою, генерація.
- [Conceptis Pic-a-Pix](https://www.conceptispuzzles.com/index.aspx?uri=puzzle/pic-a-pix) — правила ч/б і кольорових (однакові кольори — з проміжком, різні — можуть торкатись).
- [puzz.link](https://puzz.link/rules.html?nonogram) — правила (сторінка рендериться JS; вміст через WebFetch не прочитано).
- YouTube: пошук «picross s gameplay»; Steam: пошук «picross».

## Непевне
- (?) Точне правило Mega Picross (мега-число = звʼязна фігура в парі рядків) і перша поява (Picross e3, 2013) — з памʼяті; Wikipedia (Picross e, Picross S) і Nintendo лише називають режим.
- (?) Чергування кольорів смуг по 5 у пізніх S і чи позначається час «з підказкою» в Mario's Picross — з памʼяті.
- (?) Набір Assist у Picross S (підсвітка рядків, автохрестики, показ помилок) — сторінка Nintendo лише каже «assist functions».
- (?) Автохрестики й сірі підказки — поведінка багатьох мобільних плеєрів, у відкритих джерелах не підтверджено.
- (?) «Like paper» як програш з першої помилки — формулювання картки каталогу; у мобільних частіше 3 життя.
- (?) Кнопки A/B і утримання для протяжки на Nintendo-консолях.
