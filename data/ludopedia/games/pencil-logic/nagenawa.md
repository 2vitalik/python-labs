---
title: Nagenawa
slug: nagenawa
aka: [なげなわ, Lasso, Ласо, Ring-ring, リングリング]
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
  - {kind: play, url: "https://puzz.link/rules.html?nagenawa", best: true, note: "puzz.link: правила з картинками й плеєр (сторінка рендериться JS)"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/nagenawa.js", note: "правила EN/JA, «Nikoli vol. 123», коди помилок"}
  - {kind: other, url: "https://www.janko.at/Raetsel/Nagewawa/index.htm", note: "Janko: правила DE/EN, значення назви «ласо»"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/master/src/variety/nagenawa.js", note: "pzprjs: ввід, перевірка прямокутності, Ring-ring і Orbital"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/ringring.js", note: "Ring-ring: прямокутні петлі покривають усі білі клітинки, «Nikoli vol. 135»"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/master/src/res/failcode.en.json", note: "тексти bkLineGt / bkLineLt / lnNotRect / cuNoLine .nagenawa"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=nagenawa+puzzle", note: "пошук; розвʼязання"}
stage: v1
coverage: 60
mechanics: [markup-validity, completion-detection, satisfy-constraints, conflict-highlight, selection-highlight, path-drawing, path-cut, edge-marking, dot-mark, impassable-cells, undo-redo, in-game-editor, import-open-formats, +irregular-regions, +region-quota, +crossing-detection, +bridge-cell, +rect-shape-check, +rectangle-loops]
proposes: ["+cond:is_rectangle(loop)", "+cond:degree(cell, n)", "+cond:region_has(room, line_cell, n)", "+effect:draw", "+card:rectangle-loops"]
author: opus
date: 2026-11-09
---

# Nagenawa — намалюй кілька прямокутних петель-«ласо», що можуть перетинатись навхрест; число кімнати = скільки її клітинок зайнято петлями

## Суть
Поле поділене на кімнати, у частині — числа. Гравець малює кілька замкнених петель через центри клітинок; кожна петля — прямокутник або квадрат. Петлі можуть перетинатися (прямо, як міст), але не мають спільних відрізків і не діляться кутом. Число в кімнаті каже, скільки її клітинок проходить хоч одна петля; петлі не мусять покрити все поле. Незвичне: кількість петель не задана, а форма кожної — жорсткий прямокутник.

## Поле і час
- Прямокутна сітка з нерегулярними кімнатами (товсті межі); числа в частині кімнат.
- Петлі по ортогоналі між центрами клітинок; у клітинці 0, 2 сегменти або 4 (перетин двох петель прямо).
- Шари: межі й числа (незмінні) · сегменти, хрестики на ребрах, кружки й хрестики в клітинках (нотатки гравця).
- Час статичний; хід = провести / стерти сегмент. Назва なげなわ — «ласо» (nage — кидати, nawa — мотузка; Janko).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітинка | terrain | — | порожня, на петлі або перетин двох петель |
| Кімната | zone | клітинки, межа | — |
| Число кімнати | mark | N | рівно N клітинок кімнати зайняті петлями; перетин рахується раз |
| Петля-ласо | zone | прямокутник | замкнена; 4 кути; без спільних відрізків з іншими |
| Перетин | mark | клітинка з 4 сегментами | дві петлі йдуть прямо навхрест |
| Сегмент | mark | ребро | частина петлі |
| Хрестик на ребрі | mark | ребро | нотатка «тут лінії нема» |
| Кружок / хрестик у клітинці | mark | — | нотатки «на петлі» / «порожньо» |
| Зафарбована клітинка (Ring-ring) | static | — | петлі не заходять |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag, cells)` → ТО `custom: «намалювати сегменти вздовж шляху»` (+effect:draw).
- КОЛИ `input(click, edge)` → ТО `mark(edge, cross)`; правий drag — теж хрестики.
- КОЛИ `input(click, cell)` → ЯКЩО `mode(subcircle)` → ТО `mark(cell, circle)`.
- КОЛИ `input(click, cell)` → ЯКЩО `mode(subcross)` → ТО `mark(cell, cross)`.
- КОЛИ `input(info_line, cell)` → ТО `custom: «підсвітити петлю, що проходить клітинкою»`.
- КОЛИ `custom: «у клітинці чотири сегменти»` → ТО `custom: «це перетин двох петель: обидві йдуть прямо»`.
- КОЛИ `constraint_broken(no_line)` → ЯКЩО `count(segment, ==, 0)` → ТО `message(«на полі нема жодної лінії»)` — brNoLine.
- КОЛИ `constraint_broken(too_many)` → ЯКЩО `custom: «клітинок з лінією в кімнаті більше за N»` → ТО `message(«The number of the cells that is passed any line in the room and the number written in the room is different»)` · `flash(room)` — bkLineGt.
- КОЛИ `constraint_broken(branch)` → ЯКЩО `custom: «клітинка з трьома сегментами»` → ТО `message(«There is a branch line»)` · `flash(cell)` — lnBranch.
- КОЛИ `constraint_broken(dead_end)` → ЯКЩО `custom: «лінія обривається»` → ТО `message(«There is a dead-end line»)` — lnDeadEnd.
- КОЛИ `constraint_broken(too_few)` → ЯКЩО `custom: «клітинок з лінією в кімнаті менше за N»` → ТО `message(«…the number written in the room is different»)` · `flash(room)` — bkLineLt.
- КОЛИ `constraint_broken(not_rect)` → ЯКЩО `not custom: «компонента лінії — периметр свого обмежувального прямокутника»` → ТО `message(«There is a non-rectangle loop»)` · `flash(loop)` — lnNotRect.
- КОЛИ `all_constraints_met` → ТО `win`.
- Порядок перевірок у pzprjs: brNoLine → bkLineGt → lnBranch → lnDeadEnd → bkLineLt → lnNotRect.
- Спільний кут двох петель окремо не перевіряється: клітинка з 4 сегментами завжди читається як прямий перетин, тож «спільний кут» склеює петлі в непрямокутну компоненту й ловиться lnNotRect.
- Перемога: усі лінії — прямокутні петлі, перетини лише прямі, числа кімнат виконані. Поразки й рахунку нема.
- [Ring-ring] КОЛИ `constraint_broken(uncovered)` → ЯКЩО `not cover_all(loop)` → ТО `message(«There is no line on the unshaded cell»)` — cuNoLine; зафарбовані клітинки — без ліній.
- Дедукція «нуль»: кімната з 0 — жодна її клітинка не на петлі; петлі обходять її повністю.
- Дедукція «повна кімната»: N = розмір кімнати — кожна клітинка на петлі.
- Дедукція «кут»: кут прямокутника не може стояти в клітинці, де вже є інша лінія; дві замкнені петлі перетинаються парну кількість разів.

## Керування і ввід
- puzz.link (play): лівий drag — лінія; клік по ребру або правий drag — хрестик на ребрі; режими subcircle / subcross — нотатки в клітинках; info-line — підсвітка петлі.
- puzz.link (edit): drag по ребрах — межі кімнат; клік — число кімнати (до розміру кімнати); Ring-ring — клік зафарбовує клітинку.
- Папір: петлі олівцем; кути зручно позначати першими.

## Вікна, меню, HUD
- `game-screen` (puzz.link): сітка з кімнатами, числа, петлі, хрестики, кружки; `check-button`, `undo-button`, `redo-button`; `conflict-highlight` — кімната чи петля з помилкою.
- `selection-highlight` — info-line: підсвітка однієї петлі.
- `editor-window` (puzz.link edit) — межі, числа, експорт у URL.
- `help-window` — правила (puzz.link, Janko).
- `puzzle-select` (Janko) — архів пазлів за датою й складністю.
- Переходи: список Janko → пазл → `game-screen` → перевірка.

## Фічі поза полем
- `auto-check` за кнопкою; `undo` / `redo`.
- `level-editor` + `share-code` (URL puzz.link).
- Нотатки двох рівнів: на ребрах (хрестики) і в клітинках (кружок / хрестик).

## Варіації й родичі
- **Ring-ring** (リングリング, Nikoli vol. 135): ті самі прямокутні петлі, але чисел нема — є зафарбовані клітинки, а петлі мусять покрити кожну білу.
- **Orbital** (オービタル) — у тому самому модулі pzprjs: кола, через які проходять петлі, і числа-«центри орбіт» (кількість кіл усередині петлі); сторінки правил не бачив.
- Janko ставить Nagenawa поруч із «лініями через клітинки», зокрема [Country Road](country-road.md) (число = клітинки петлі в кімнаті).
- У корпусі: прямокутники як області — [Shikaku](shikaku.md); перетини петлі — [Pipelink](pipelink.md), [Reflect Link](reflect-link.md); кімнати з числами — [Heyawake](heyawake.md).
- **Осі варіацій**: форма петлі (прямокутник / будь-яка) · кількість петель (одна / кілька) · підказки (числа кімнат / зафарбовані / кола-орбіти) · покриття (не обовʼязкове / усі білі — Ring-ring).

## Цікавинки для курсу
- Перевірка «петля — прямокутник»: обмежувальний прямокутник компоненти і число сегментів = периметр — 🌱.
- Лінійний граф із перетинами: у клітинці з 4 сегментами розʼєднати горизонталь і вертикаль, потім рахувати компоненти — 📎.
- Лічба клітинок з лінією по кімнатах (перетин — один раз) — 🌱.
- Розвʼязувач: перебір прямокутників-кандидатів (кути, сторони) з обмеженнями кімнат — 🥈.
- Генератор з єдиним розвʼязком — 👑.

## Мапа на каталог
- Є: `markup-validity`, `completion-detection`, `satisfy-constraints` · `conflict-highlight`, `selection-highlight` ↔ info-line · `path-drawing`, `path-cut`, `edge-marking` ↔ ввід ліній · `dot-mark` ↔ кружки й хрестики в клітинках · `impassable-cells` ↔ зафарбовані Ring-ring · `undo-redo` · `in-game-editor`, `import-open-formats`.
- **Нема** → пропозиції карток:
  - `+irregular-regions`, `+region-quota`, `+crossing-detection`, `+bridge-cell`, `+rect-shape-check` — уже пропоновані в корпусі.
  - `+rectangle-loops` «Кілька петель, кожна — прямокутник; можуть перетинатись прямо» · game-logic/constraints · 📎.

## Пропозиції до словників
- `+cond:is_rectangle(loop)` — компонента має форму прямокутника (повтор із Shikaku).
- `+cond:degree(cell, n)` — скільки сегментів у клітинці (повтор).
- `+cond:region_has(room, line_cell, n)` — у кімнаті N клітинок з лінією (повтор).
- `+effect:draw` — гравець малює сегмент лінії (повтор).
- `+card:rectangle-loops` — див. мапу.

## Джерела
- ⭐ [puzz.link: Nagenawa](https://puzz.link/rules.html?nagenawa) — правила з картинками й плеєр (рендериться JS; текст узято з pzpr-samples).
- [puzz.link nagenawa.js](https://puzz.link/js/pzpr-samples/nagenawa.js) — правила EN/JA (прямокутні петлі, перетин як міст, без спільних відрізків і кутів, число = клітинки з лінією), «Nikoli vol. 123», коди помилок.
- [Janko: Nagenawa](https://www.janko.at/Raetsel/Nagewawa/index.htm) — правила DE/EN, «петлі не мусять пройти всі клітинки», значення назви.
- [pzprjs nagenawa.js](https://raw.githubusercontent.com/robx/pzprjs/master/src/variety/nagenawa.js) — режими вводу, алгоритм lnNotRect, Ring-ring, Orbital.
- [puzz.link ringring.js](https://puzz.link/js/pzpr-samples/ringring.js) — правила Ring-ring, «Nikoli vol. 135».
- [pzprjs failcode.en.json](https://raw.githubusercontent.com/robx/pzprjs/master/src/res/failcode.en.json) — тексти bkLineGt / bkLineLt / lnNotRect / cuNoLine.

## Непевне
- (?) Рік першої публікації: відомо лише «Nikoli vol. 123»; Janko пише, що джерело не певне.
- (?) Текст brNoLine не бачив — у `message` переказ.
- (?) Правила Orbital прочитані лише з коду pzprjs.
- (?) У URL Janko назва з одруківкою «Nagewawa» — сторінка відкривається саме за нею.
- (?) Дедукції «нуль», «повна кімната», «кут» — загальна логіка, не з джерела.
