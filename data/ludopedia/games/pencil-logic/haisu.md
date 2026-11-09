---
title: Haisu
slug: haisu
aka: [House, Хайсу]
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
  - {kind: other, url: "https://puzz.link/rules.html?haisu", best: true, note: "puzz.link: правила EN/JA і плеєр (сторінка рендериться JS)"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/haisu.js", note: "puzz.link: текст правил, автор William Hu, тестові поля з кодами помилок"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/master/src/variety/haisu.js", note: "pzprjs: обхід шляху haisuWalk з лічильником візитів; спільний файл з Kaisu і Building Walk"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/master/src/res/failcode.en.json", note: "pzprjs: тексти haisuSG / haisuError і загальних помилок лінії"}
  - {kind: other, url: "https://www.janko.at/Raetsel/Haisu/index.htm", note: "Janko: правила DE/EN/JA + маленькі числа = загальна кількість візитів області"}
  - {kind: other, url: "https://dj-puzzles.blogspot.com/2025/03/genre-spotlight-17-haisu-puzzles-251.html", note: "DJ Puzzles: огляд жанру, вік ~8 років (2025), рідко на змаганнях"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=haisu+puzzle", note: "пошук; розвʼязання"}
stage: v1
coverage: 70
mechanics: [markup-validity, completion-detection, satisfy-constraints, path-drawing, edge-marking, conflict-highlight, in-game-editor, import-open-formats, undo-redo, +irregular-regions, +hamiltonian-path-check, +start-goal-path, +crossing-detection, +region-visit-index]
proposes: ["+cond:visited", "+trigger:pattern(loop_branch)", "+ui:direction-aux-mark", "+card:region-visit-index"]
author: opus
date: 2026-11-09
---

# Haisu — проведи один шлях від S до G через усі клітинки так, щоб клітинку з числом N він проходив під час N-го заходу в її область

## Суть
Поле поділене жирними межами на області; у ньому є старт S, ціль G і числа в частині клітинок. Гравець малює один шлях S→G через центри **всіх** клітинок, без розгалужень і самоперетинів. Шлях може заходити в область і виходити з неї скільки завгодно разів; число N у клітинці означає: шлях проходить цю клітинку саме під час N-го візиту своєї області. Незвичне: підказка — не про геометрію, а про **час** — порядковий номер заходу в регіон уздовж шляху.

## Поле і час
- Прямокутна сітка, ортогональне сусідство; області — довільні, задані пазлом; Janko має категорії 6×6, 8×8, 10×10.
- Шари: межі областей · S і G · числа · лінія гравця між центрами клітинок · хрестики на ребрах · допоміжні стрілки напрямку.
- Час статичний; хід = провести / стерти сегмент лінії.
- Візит області — безперервний відрізок шляху всередині неї; область зі S уже на старті має візит 1 (pzprjs: `oldRoom.visit = 1`).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітинка | mark | сегменти лінії 0–2 | кожну проходить шлях |
| Сегмент лінії | mark | ребро між центрами | ставить гравець |
| Хрестик на ребрі | mark | — | «тут лінії нема»; на перевірку не впливає |
| S (старт) | static | клітинка | кінець шляху, рівно 1 сегмент |
| G (ціль) | static | клітинка | інший кінець шляху, рівно 1 сегмент |
| Область | zone | клітинки, лічильник візитів | рахує заходи шляху |
| Число N | static | 1…розмір області | клітинку проходять на N-му візиті області |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag, cells)` → ТО `custom: «провести сегменти лінії між центрами клітинок»`; drag по наявній лінії — стерти (?).
- КОЛИ `input(right_click, edge)` → ТО `mark(edge, cross)` (режим `peke`) (?).
- КОЛИ `input(right_drag, edges)` → ТО `mark(edge, direction_arrow)` (режим `diraux`, `+ui:direction-aux-mark`) (?).
- КОЛИ `pattern(loop_branch)` → ЯКЩО `custom: «клітинка має 3+ сегменти»` → ТО `set_state(cell, error)` (`lnBranch`: «There is a branch line»).
- КОЛИ `constraint_broken(cross)` → ЯКЩО `custom: «лінія перетинає себе в клітинці»` → ТО `set_state(cell, error)` (`lnCross`).
- КОЛИ `constraint_broken(sg)` → ЯКЩО `custom: «S або G має 2 сегменти»` → ТО `set_state(cell, error)` (`haisuSG`: «The line goes through S/G»).
- КОЛИ `custom: «обхід лінії від S»` → ТО `counter(visits[room(S)], 1)` — старт уже рахується першим візитом.
- КОЛИ `enter(path, region)` → ЯКЩО `custom: «перехід через жирну межу»` → ТО `counter(visits[region], +1)`.
- КОЛИ `enter(path, numbered_cell)` → ЯКЩО `not counter(visits[region], ==, N)` (`+cond:visited`) → ТО `set_state(cell, error)` (`haisuError`: «A number is not passed on the right visit»).
- КОЛИ `constraint_broken(dead_end)` → ЯКЩО `custom: «кінець лінії не в S і не в G»` → ТО `set_state(cell, error)` (`lnDeadEnd`).
- КОЛИ `constraint_broken(empty)` → ЯКЩО `not cover_all(path)` → ТО `set_state(cell, error)` (`ceNoLine`: «There is an empty cell»).
- КОЛИ `constraint_broken(many_lines)` → ЯКЩО `not connected(path)` → ТО `set_state(board, error)` (`lnPlLine`: «There are multiple lines»).
- Janko-варіант: ЯКЩО `custom: «маленьке число n у лівому верхньому куті області»` → ТО `custom: «загальна кількість візитів області = n»`.
- КОЛИ `all_constraints_met` → ТО `win`.
- Обмеження редактора: число N ≤ розміру області (`maxnum = room.clist.length`) — кожен візит займає щонайменше одну клітинку.
- Дедукція «рахунок візитів»: область із числом N мусить мати ≥ N візитів, тобто ≥ N входів через межу (для області S — ≥ N−1).
- Дедукція «кути»: клітинка в куті має рівно два можливі сегменти, тож обидва обовʼязкові (якщо це не S/G).
- Дедукція «перший візит»: 1 в області S — клітинку пройдено ще до першого виходу з неї; 1 в іншій області — на першому ж заході, тож шлях не може зайти в область і вийти, оминувши цю клітинку.
- Перемога: один шлях S→G через усі клітинки, без розгалужень і перетинів, усі числа на своєму візиті. Поразки й рахунку нема.

## Керування і ввід
- Папір: лінія через центри клітинок, хрестики на закритих ребрах.
- puzz.link play: лівий drag — лінія (`line`); правий — хрестик (`peke`) або допоміжна стрілка напрямку (`diraux`); клік без руху — `clickdiraux` (?); `info-line` — підсвітити лінію.
- puzz.link edit: drag по ребрах — межі областей; клік по клітинці під курсором — число з клавіатури; S і G перетягуються мишею (`draggingSG`).

## Вікна, меню, HUD
- `game-screen`: сітка з жирними областями, S, G, числа, лінія, хрестики, стрілки; `conflict-highlight` — клітинка з числом не на своєму візиті, S/G з двома сегментами.
- `editor-window` (puzz.link edit): межі, числа, S/G; експорт URL (зразок `5/5/1551688s120mg2n1g2g3n1g`).
- `help-window` — правила (puzz.link, Janko).
- `puzzle-select` — Janko (за розміром 6×6 / 8×8 / 10×10; список за датою — «Noch keine»).
- Решта — оболонка [puzz.link](puzz-link.md): Check, Undo/Redo, Trial, URL, таймер.

## Фічі поза полем
- `auto-check` за кнопкою з текстом першої помилки; `undo` / `redo`; trial-режим оболонки.
- `level-editor` + `share-code` (URL puzz.link); `export-import` (файл pzprv3).
- Банку з прогресом не бачив; генератора й розвʼязувача в puzz.link нема.

## Варіації й родичі
- **Kaisu** (той самий файл pzprjs): кола замість чисел — на N-му візиті області лінія проходить рівно N кіл або жодного.
- [Building Walk](building-walk.md) (Nikoli vol.174, той самий файл pzprjs): шлях S→G зі станом «поверх», ліфти міняють поверх, числа — поверх у клітинці.
- [Country Road](country-road.md) — петля, кожна область рівно один візит; [Nuri-Maze](nuri-maze.md) — S→G у дереві білих; [Hidato](hidato.md) — номер клітинки на шляху; [N-Queens / Knight's Tour](n-queens-knights-tour.md) — гамільтонів шлях.
- Janko додає маленькі числа загальної кількості візитів (у pzprjs такого коду не бачив).
- **Осі варіацій**: що рахує підказка (номер візиту / кількість візитів / кількість символів на візиті) · шлях чи петля · через усі клітинки чи лише через символи · один стан (візит) чи кілька (поверх).

## Цікавинки для курсу
- Валідатор шляху: ступінь клітинок, один компонент, кінці лише S/G — 🌱.
- Обхід шляху від S з лічильником візитів на межах (`haisuWalk`) — 📎: стан на областях, а не на клітинках.
- Гамільтонів шлях з обмеженнями — розвʼязувач бектрекінгом з відсіканням за візитами — 🥇.
- Порівняти три правила одного файла (Haisu / Kaisu / Building Walk) як «той самий обхід, різний стан» — 🥉.

## Мапа на каталог
- Є: `markup-validity`, `completion-detection`, `satisfy-constraints` · `path-drawing` ↔ drag лінії · `edge-marking` ↔ хрестики · `conflict-highlight` · `in-game-editor`, `import-open-formats` · `undo-redo`.
- Перевикористано: `+irregular-regions`, `+hamiltonian-path-check` (Knight's tour), `+start-goal-path` (Building Walk), `+crossing-detection`.
- **Нема** → пропозиції карток:
  - `+region-visit-index` «Номер заходу шляху в область: клітинка N — на N-му візиті» · game-logic/constraints · 📎 · слот {count: index|total|symbols-per-visit} — Haisu, Kaisu, Janko-маленькі числа.

## Пропозиції до словників
- `+cond:visited` — повтор (Building Walk, Knight's tour): тут — номер поточного візиту області дорівнює N.
- `+trigger:pattern(loop_branch)` — повтор з Yajilin: лінія розгалужується.
- `+ui:direction-aux-mark` — допоміжна стрілка напрямку руху на лінії (puzz.link `diraux`), не перевіряється.
- `+card:region-visit-index` — див. мапу.

## Джерела
- ⭐ [puzz.link: Haisu](https://puzz.link/rules.html?haisu) — правила і плеєр; текст — у pzpr-samples.
- [pzpr-samples haisu.js](https://puzz.link/js/pzpr-samples/haisu.js) — «Draw a path from S to G that goes through all cells», «A number N indicates that the path must go through that cell on the region's Nth visit», «invented by William Hu».
- [pzprjs haisu.js](https://raw.githubusercontent.com/robx/pzprjs/master/src/variety/haisu.js) — checklist, `haisuWalk`, `haisuPassThroughSG`, режими вводу, `maxnum`, спільний код Kaisu / Building Walk.
- [pzprjs failcode.en.json](https://raw.githubusercontent.com/robx/pzprjs/master/src/res/failcode.en.json) — тексти помилок.
- [Janko: Haisu](https://www.janko.at/Raetsel/Haisu/index.htm) — правила трьома мовами, маленькі числа = загальна кількість візитів.
- [DJ Puzzles: Genre spotlight Haisu](https://dj-puzzles.blogspot.com/2025/03/genre-spotlight-17-haisu-puzzles-251.html) — «about eight years old», є puzz.link, кілька появ на 24HPC.

## Непевне
- (?) Рік: за DJ Puzzles (березень 2025) жанру «близько восьми років» — тобто ~2017; першої публікації не знайшов, тож `year: null`.
- (?) Janko EN «Haisu ("House")» — значення назви не підтверджене іншим джерелом.
- (?) Чи є в Janko справжні пазли Haisu: список за датою порожній, категорії розмірів без номерів.
- (?) Призначення кнопок миші в play-режимі (лінія / хрестик / стрілка) — з коду, у плеєрі не перевіряв.
- (?) Чи може S чи G мати число — у тестових полях не бачив.
