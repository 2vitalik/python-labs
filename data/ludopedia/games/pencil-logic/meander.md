---
title: Mäander (Meander, Vabyrinth)
slug: meander
aka: [Mäander, Vabyrinth, Schlingerpfad, Меандр]
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
  - {kind: other, url: "https://www.janko.at/Raetsel/Maeander/index.htm", best: true, note: "Janko: правила DE/EN, приклад 6×6 з розвʼязком (картинки), автор Okan Özelmas, 40 пазлів, назви Schlingerpfad / Vabyrinth"}
  - {kind: other, url: "https://www.janko.at/Raetsel/Maeander/Beispiel.htm", note: "Janko: покроковий розбір прикладу (гирло «//», поворот на 90°, ширина)"}
  - {kind: play, url: "https://www.janko.at/Raetsel/Maeander/001.a.htm", note: "applet Janko (MeanderingPath.js), пазл 3×3; у коді — розвʼязок символами / і \\"}
  - {kind: other, url: "http://wiki.logic-masters.de/index.php?title=Schlingerpfad/de", note: "Puzzle-Wiki logic-masters: Vabyrinth — правила DE (одна ширина, усі риски — стіни)"}
  - {kind: other, url: "https://wiki.logic-masters.de/index.php?title=Vabyrinth/en", note: "Puzzle-Wiki: правила EN, автор Okan Özelmas (Туреччина)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=vabyrinth+puzzle", note: "пошук; відео не шукав"}
stage: v1
coverage: 50
mechanics: [markup-validity, completion-detection, satisfy-constraints, connectivity-check, cell-click, keyboard-controls, conflict-highlight, level-bank, level-rating, puzzle-select, save-game, undo-redo, replay, +outside-clues, +half-cell-triangles, +constant-width-path, +hint-reveal, +cell-coloring]
proposes: ["+cond:count_in", "+cond:width", "+cond:border_contacts(region, n)", "+ui:solved-frame", "+window:puzzle-info", "+card:constant-width-path"]
author: opus
date: 2026-11-09
---

# Mäander (Vabyrinth) — намалюй діагоналями в клітинках береги однієї річки сталої ширини від краю до краю

## Суть
Гравець ставить у деякі клітинки діагональ «/» або «\» — це шматки берега. Разом вони мають утворити одну річку (шлях), що починається й закінчується на краю поля, ніде не розгалужується і всюди однаково широка — рівно одна клітинка. Ззовні кожного рядка й стовпця дано два числа: скільки в ньому «\» і скільки «/». Незвичне: шлях не з клітинок, а з напівклітинок, і його треба вивести лише з лічильників напрямків діагоналей.

## Поле і час
- Квадратна сітка; на Janko 3×3, 4×4, 5×5, 6×6, 8×8, 10×10.
- Підказки: пара чисел біля кожного рядка (ліва — «\», права — «/») і над кожним стовпцем (верхня — «\», нижня — «/»); легенда зі значками в куті.
- У клітинці максимум одна діагональ; клітинка без лінії — цілком вода або цілком суходіл.
- Розбір розвʼязку прикладу 6×6 (мій): область між діагоналями, що торкається рамки рівно у двох одиничних ребрах, — річка; решта — суходіл.
- Там же: окремі відрізки мають воду з обох боків і висять кінцем у полі (річка обтікає їх шпилькою на 180°), а в деяких точках сходяться 3–4 відрізки (?).
- Час статичний; 40 авторських пазлів.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітинка | terrain | порожня / «/» / «\» | щонайбільше одна діагональ |
| Відрізок «\» | mark | — | шматок берега; рахується першим числом рядка й стовпця |
| Відрізок «/» | mark | — | шматок берега; рахується другим числом |
| Річка | zone | область з напівклітинок | одна, звʼязна, без розгалужень, ширина 1 клітинка |
| Гирло | zone | одиничне ребро рамки | рівно два: початок і кінець річки |
| Суходіл | zone | решта поля | не торкається річки інакше, ніж через берег |
| Пара чисел рядка / стовпця | static | (к-сть «\», к-сть «/») | лічильники діагоналей лінії |
| Хрестик | mark | — | «тут лінії точно нема» (необовʼязковий) |
| Кружок | mark | — | «тут лінія є, яка — ще невідомо» |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left_click, cell)` → ТО `set_value(cell, наступний символ: / → \ → × → ○ → порожньо)`.
- КОЛИ `input(key)` → ТО `set_value(cell, symbol)`: `\` або `,` — «/», `/` або `.` — «\», `o` — ○, `x` — ×, `-`/Del/⌫ — порожньо (так у Bedienung, див. «Непевне»).
- Лічильник: ЯКЩО `custom: «к-сть "\" у рядку = перше число, к-сть "/" = друге»` (`+cond:count_in`) → рядок задоволено; так само для стовпця.
- Річка: ЯКЩО `connected(river)` and `custom: «річка торкається рамки рівно у двох місцях»` (`+cond:border_contacts`) → є початок і кінець.
- ЯКЩО `custom: «річка не розгалужується і всюди однієї ширини»` (`+cond:width`) → форма правильна.
- ЯКЩО `custom: «кожна діагональ — стіна річки»` → лишніх ліній нема (Puzzle-Wiki: «alle Striche müssen eine Wand des Weges sein»).
- КОЛИ `input(F6)` → ТО `custom: «усі порушення — червоним»`.
- КОЛИ `input(F3)` → ТО `set_state(board, hint_mode)`; КОЛИ `input(click, cell)` → ЯКЩО `state(board, hint_mode)` → ТО `set_value(cell, solution)`.
- КОЛИ `input(F4)` → ТО `custom: «вписати розвʼязок і шлях у список ходів»`.
- КОЛИ `input(ctrl_z|page_up)` → ТО `undo(1)`; `input(pos1)` → `undo(all)`.
- КОЛИ `all_constraints_met` → ТО `win` + `custom: «зелена рамка»`.
- Дедукція «гирло»: у рядку/стовпці, де річка починається чи закінчується, мусять бути щонайменше дві однакові лінії поруч («//» або «\\») — береги гирла паралельні (Janko).
- Дедукція «поворот біля краю»: у прикладі річка не може почати в першому рядку чи останньому стовпці і мусить там повернути на 90° (Janko).
- Дедукція «ширина»: якщо в точці закінчується береговий відрізок, паралельний відрізок мусить бути в сусідній клітинці на відстані ширини річки (жовта клітинка прикладу).
- Дедукція «зсув»: групу вже відомих ліній зсувають на клітинку, доки не зійдуться лічильники рядків і стовпців (зелені клітинки прикладу).
- Перемога: одна річка від краю до краю, стала ширина, усі лінії — її береги, усі пари чисел збіглися. Поразки й рахунку нема.

## Керування і ввід
- Миша / дотик: повторний клік (тап) по клітинці — цикл «/», «\», ×, ○, порожньо.
- Клавіатура: стрілки — рамка вибору; символи клавішами (вище); наведення без кліку + клавіша.
- Символьні маркери Ctrl+Q/W/E/R/X/A/B/C/D, кольори ходів Alt+0…9.
- Папір: діагоналі олівцем, хрестики для «тут нема».

## Вікна, меню, HUD
- `game-screen`: сітка, пари чисел зліва й зверху, легенда «\» / «/» у куті, лінії, × і ○, `conflict-highlight` (F6), зелена рамка (`+ui:solved-frame`).
- `puzzle-select` — Janko: 40 пазлів за датою, розміром, складністю.
- `help-window` — «Regeln», «Bedienungsanleitung», сторінка «Beispiel» з 7 кроками розбору.
- `+window:puzzle-info` (F1) — інфо про пазл і лист вебмайстру.

## Фічі поза полем
- `auto-check` (F6) і автовизнання розвʼязку.
- `undo` / `redo` по одному й усі; `save-slots` (?) — Ctrl+S / Ctrl+L.
- `hint` (F3), `show-solution` (F4 з логічним шляхом у списку ходів).
- `puzzle-bank` — 40 пазлів, рейтинг за часом, пазли з відтворюваним шляхом виділено.
- `tutorial` — розібраний приклад крок за кроком (Beispiel).

## Варіації й родичі
- Назви: Mäander (Janko), Schlingerpfad (Rätselportal), Vabyrinth (турецький журнал Denksel / Akıl Oyunları № 77).
- Janko називає родичем Tunnel.
- У сімʼї: [Slant](slant.md) — діагональ у кожній клітинці й лічильники у вершинах; [Shakashaka](shakashaka.md) — напівклітинки-трикутники; [Masyu](masyu.md), [Country Road](country-road.md) — одна лінія-шлях; [Nonogram](nonogram.md) — лічильники ззовні.
- **Осі варіацій**: що рахують числа (кожен напрямок окремо / разом) · ширина шляху (1 / більше) · петля чи шлях від краю до краю · чи можна торкатись себе.

## Цікавинки для курсу
- Лічильники «\» і «/» по рядках і стовпцях — 🌱.
- Поділ клітинки на 4 трикутники й union-find по них: знайти області між діагоналями — 📎.
- Перевірка «одна область торкається рамки рівно у двох ребрах» — 📎.
- Перевірка сталої ширини й відсутності розгалужень для діагонального шляху — 🥈.
- Розвʼязувач: перебір 3 станів клітинки з відсіканням за лічильниками й звʼязністю — 🥇.

## Мапа на каталог
- Є: `markup-validity`, `completion-detection`, `satisfy-constraints` · `connectivity-check` ↔ річка — одна область · `cell-click`, `keyboard-controls`, `conflict-highlight` · `level-bank`, `level-rating`, `puzzle-select` · `save-game`, `undo-redo`, `replay` ↔ розвʼязок F4 у списку ходів.
- Перевикористано: `+outside-clues` (лічильники ззовні), `+half-cell-triangles` (Slant), `+hint-reveal` ↔ F3, `+cell-coloring` ↔ кольори ходів.
- **Нема** → пропозиції карток:
  - `+constant-width-path` «Шлях сталої ширини між діагональними стінами, від краю до краю» · game-logic/constraints · 🥈 · слот {width, ends: border|loop}.

## Пропозиції до словників
- `+cond:count_in` — повтор (Compass, Doppelblock): кількість у рядку/напрямку.
- `+cond:width` — повтор (Lode Runner 3D): ширина проходу.
- `+cond:border_contacts(region, n)` — область торкається рамки рівно в n місцях.
- `+ui:solved-frame`, `+window:puzzle-info` — повтори з Suraido (applet Janko).
- `+card:constant-width-path` — див. мапу.

## Джерела
- ⭐ [Janko: Mäander](https://www.janko.at/Raetsel/Maeander/index.htm) — правила DE/EN, картинки прикладу й розвʼязку 6×6 (лічильники перевірив), автор Okan Özelmas, 40 пазлів, інші назви.
- [Janko: Beispiel](https://www.janko.at/Raetsel/Maeander/Beispiel.htm) — 7 кроків розбору: гирло «//», поворот на 90°, ширина, зсув.
- [Janko: Mäander Nr. 1](https://www.janko.at/Raetsel/Maeander/001.a.htm) — дані 3×3 (розвʼязок символами), applet MeanderingPath.js.
- [Puzzle-Wiki: Schlingerpfad / Vabyrinth (DE)](http://wiki.logic-masters.de/index.php?title=Schlingerpfad/de) — «один вхід і один вихід», «без розгалужень», «стала ширина», «усі риски — стіни».
- [Puzzle-Wiki: Vabyrinth (EN)](https://wiki.logic-masters.de/index.php?title=Vabyrinth/en) — те саме англійською, автор.
- YouTube: пошук «vabyrinth puzzle».

## Непевне
- (?) Точна геометрія «ширини 1» і чи може річка торкатись себе в точці — правила не уточнюють; опис шпильок і точок з 3–4 відрізками — мій розбір однієї картинки.
- (?) Розмітка клавіш у Bedienung суперечлива (`,` і `.` призначені двом символам) — переписав як є.
- (?) Рік винаходу й номер журналу з датою — не знайшов; «Akıl Oyunları Nr. 77» — лише зі слів Janko.
- (?) Розміри пазлів 11–40 (позначка «~050» в індексі) — не зрозумів.
- (?) Чи всі пазли Janko мають два числа на лінію — бачив лише приклад.
