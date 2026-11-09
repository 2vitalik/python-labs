---
title: Pipelink
slug: pipelink
aka: [パイプリンク, Pipe Link, Pipelink Returns, 帰ってきたパイプリンク, Loop Special, 環状線スペシャル]
family: pencil-logic
also: [connect-rotate]
klass: puzzle
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: none
  goal: constraints
year: 1993
platforms: [paper, web]
links:
  - {kind: play, url: "https://puzz.link/rules.html?pipelink", best: true, note: "puzz.link: правила з картинками й плеєр (сторінка рендериться JS)"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/pipelink.js", note: "правила EN/JA, «Nikoli vol. 45», коди помилок"}
  - {kind: other, url: "https://www.janko.at/Raetsel/Pipelink/index.htm", note: "Janko: правила DE/EN, Nikoli №45 (жовтень 1993), 200 пазлів, родинні жанри"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/master/src/variety/pipelink.js", note: "pzprjs: форми труб, ввід, чек-листи Pipelink / Returns / Loop Special"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/pipelinkr.js", note: "Pipelink Returns: перетин лише в колах, «Nikoli vol. 110»"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/loopsp.js", note: "Loop Special: кілька петель за числами, «Nikoli vol. 57»"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/master/src/res/failcode.en.json", note: "тексти помилок .pipelink"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=pipelink+puzzle+nikoli", note: "пошук; розвʼязання"}
stage: v1
coverage: 60
mechanics: [markup-validity, completion-detection, satisfy-constraints, conflict-highlight, single-loop-check, path-drawing, path-cut, edge-marking, pipe-connectors, keyboard-controls, undo-redo, in-game-editor, import-open-formats, level-bank, +crossing-detection, +bridge-cell, +fill-all-cells, +given-segments, +numbered-loops]
proposes: ["+cond:degree(cell, n)", "+cond:crosses", "+effect:draw", "+trigger:pattern(loop_branch)", "+card:given-segments", "+card:numbered-loops"]
author: opus
date: 2026-11-09
---

# Pipelink — одна петля крізь усі клітинки, яка може перетинати себе прямо, як труба над трубою; частину труб уже прокладено

## Суть
Гравець малює одну замкнену петлю через центри всіх клітинок поля. Лінія може перетнути себе в будь-якій клітинці, але лише навхрест і прямо (міст, «立体交差»); повертати на перехресті чи зливатись не можна. Частина клітинок містить дані шматки труб — прямі, кути, хрести; до них нічого не додається. Незвичне: перетин — дозволений інструмент, тож клітинка-хрест «вміщує» петлю двічі.

## Поле і час
- Прямокутна сітка без регіонів; дані шматки труб у клітинках.
- Петля по ортогоналі між центрами сусідніх клітинок; у клітинці 2 сегменти (прохід) або 4 (перехрестя, лінії прямо).
- Шари: дані труби (незмінні) · сегменти й хрестики гравця.
- Час статичний; хід = провести / стерти сегмент.
- Перша публікація — Nikoli №45, жовтень 1993 (Janko).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітинка | terrain | — | петля мусить пройти |
| Дана труба | static | форма: пряма ─/│, кут ×4, хрест ┼ | частина петлі; лінії до клітинки не додаються |
| Перехрестя | mark | клітинка з 4 сегментами | дві гілки петлі йдуть прямо, не повʼязані |
| Петля | zone | одна | через усі клітинки; перетини лише прямі |
| Сегмент | mark | ребро | частина петлі |
| Хрестик | mark | ребро | нотатка «тут лінії нема» |
| Коло (Returns) | static | — | лише тут можна перетинатись; повертати не можна |
| Коло з числом (Loop Special) | mark | N або порожнє | визначає, якій петлі належить клітинка |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag, cells)` → ТО `custom: «намалювати сегменти вздовж шляху»` (+effect:draw).
- КОЛИ `input(click, edge)` → ЯКЩО `free(edge)` → ТО `mark(edge, cross)`; правий drag — теж хрестики.
- КОЛИ `adjacent(pipe_a, pipe_b)` → ЯКЩО `custom: «виходи обох даних труб дивляться на спільне ребро»` → ТО `custom: «ребро автоматично стає лінією»`.
- КОЛИ `custom: «у клітинці чотири сегменти»` → ТО `custom: «це перехрестя: дві незалежні прямі гілки петлі»`.
- КОЛИ `constraint_broken(add_line)` → ЯКЩО `occupied(cell, pipe)` і `custom: «лінії клітинки не збігаються з формою даної труби»` → ТО `message(«до клітинки з трубою додано лінію»)` · `flash(cell)` — ceAddLine.
- КОЛИ `constraint_broken(branch)` → ЯКЩО `custom: «клітинка з трьома сегментами»` → ТО `message(«There is a branch line»)` · `flash(cell)` — lnBranch.
- КОЛИ `constraint_broken(many_loops)` → ЯКЩО `not single_loop` → ТО `message(«There are multiple loops»)` — lnPlLoop.
- КОЛИ `constraint_broken(cross_mark)` → ЯКЩО `custom: «дана хрест-труба не перетнута лінією»` → ТО `message(«перетин на хресті не виконано»)` — lnNotCrossMk (?).
- КОЛИ `constraint_broken(no_line)` → ЯКЩО `not cover_all(loop)` → ТО `message(«клітинка без лінії»)` · `flash(cell)` — ceNoLine.
- КОЛИ `constraint_broken(dead_end)` → ЯКЩО `custom: «лінія обривається»` → ТО `message(«There is a dead-end line»)` — lnDeadEnd.
- КОЛИ `all_constraints_met` → ТО `win`.
- Порядок перевірок Pipelink у pzprjs: ceAddLine → lnBranch → lnPlLoop → lnNotCrossMk → ceNoLine → lnDeadEnd.
- [Returns] КОЛИ `constraint_broken(cross_outside)` → ЯКЩО `custom: «перетин у клітинці без кола і без даного хреста»` → ТО `message(«There is a crossing line out of circles»)` — lnCrossExCir.
- [Returns] КОЛИ `constraint_broken(turn_on_circle)` → ЯКЩО `occupied(cell, circle)` і `custom: «лінія в колі повертає»` → ТО `message(«A line turns on a circle»)` — lnCurveOnCir.
- [Loop Special] КОЛИ `constraint_broken(cross_on_number)` → ЯКЩО `occupied(cell, number)` і `custom: «у клітинці з числом перетин»` → ТО `message(«Lines are crossed on a number»)` — lnCrossOnNum.
- [Loop Special] КОЛИ `constraint_broken(mixed_numbers)` → ЯКЩО `not same(circle_a, circle_b, number)` і `custom: «обидва кола на одній петлі»` → ТО `message(«A loop has multiple kinds of number»)` — lpPlNum.
- [Loop Special] КОЛИ `constraint_broken(split_number)` → ЯКЩО `same(circle_a, circle_b, number)` і `custom: «кола на різних петлях»` → ТО `message(«A kind of number is in different loops»)` — lpSepNum.
- [Loop Special] КОЛИ `constraint_broken(loop_without_number)` → ЯКЩО `custom: «петля не проходить жодного кола»` → ТО `message(«A loop has no numbers»)` — lpNoNum.
- Перемога: одна петля (Loop Special — кілька петель за числами) через усі клітинки, з усіма даними трубами, з перетинами лише прямо. Поразки й рахунку нема.
- Дедукція «кут поля»: у кутовій клітинці петля може лише повернути; на краю поля перехрестя неможливе (потрібні 4 виходи).
- Дедукція «дана труба»: її виходи продовжуються в сусідні клітинки; сусід, у який труба не дивиться, не може мати лінію через спільне ребро.

## Керування і ввід
- puzz.link (play): лівий drag — лінія; клік без руху по ребру без лінії — хрестик; правий drag — хрестики.
- puzz.link (edit): клік по клітинці перебирає форми труби; клавіші q / w / e / a / s / d / f — сім форм (хрест, дві прямі, чотири кути), r або пробіл — стерти; у Returns клавіша 1 — коло; у Loop Special — цифри для чисел у колах.
- Папір: лінія олівцем, перехрестя малюють як пряме перетинання.

## Вікна, меню, HUD
- `game-screen` (puzz.link): сітка, дані труби, кола (Returns, Loop Special), лінія, хрестики; `check-button`, `undo-button`, `redo-button`; `conflict-highlight` — клітинка чи петля з помилкою.
- `editor-window` (puzz.link edit) — розмір, труби, кола, числа, експорт у URL.
- `help-window` — правила (puzz.link, Janko).
- `puzzle-select` (Janko): 200 пазлів за номером, розміром, складністю.
- Переходи: список Janko → пазл → `game-screen` → перевірка.

## Фічі поза полем
- `auto-check` за кнопкою; `undo` / `redo`.
- `level-editor` з клавіатурним вводом форм труб + `share-code` (URL puzz.link).
- `puzzle-bank` — Janko: 200 пазлів, переважно 10×10, є 5×5 … 18×10 і кілька великих (~250–1000 клітинок).

## Варіації й родичі
### Pipelink Returns (帰ってきたパイプリンク, Nikoli vol. 110)
- На полі є білі кола; перетинатися можна лише в колі, а повертати в колі не можна (коло = прямий прохід або перехрестя).

### Loop Special (環状線スペシャル, Nikoli vol. 57)
- Петель кілька; кожна клітинка — на якійсь петлі; у кожній петлі — хоч одне коло; кола з однаковим числом — на одній петлі, з різними — на різних; у колі з числом перетин заборонений.

### Родичі
- Janko: Reflexion (петля не мусить пройти всі клітинки, перетин лише в заданих місцях), Barns (на сірих не повертає, деякі стіни), Aisuban / Aisurom (шлях, не петля, через сірі зони).
- У корпусі: [Reflect Link](reflect-link.md) (перетини й відбивачі), [Icebarn](icebarn.md) (лід — без поворотів), [Tracks](tracks.md) (рейки з даними шматками), [Masyu](masyu.md); поза сімʼєю — труби в [connect-rotate](../../taxonomy/families.md).
- **Осі варіацій**: де можна перетинатись (будь-де / лише в колах / лише на даних хрестах) · кількість петель (одна / кілька за числами) · покриття (усі клітинки / ні) · дані шматки (труби / лише кола).

## Цікавинки для курсу
- Модель клітинки з портами (4 біти виходів) і автозʼєднання сусідніх даних труб — 🌱.
- Розрізнення перехрестя і розгалуження за степенем клітинки (2 / 4 — норма, 3 — помилка) — 🌱.
- Обхід петлі з перехрестями: у клітинці-хресті йти прямо, рахувати компоненти — 📎.
- Loop Special: розфарбування петель за числами й перевірка «одне число на петлю, одна петля на число» — 📎.
- Розвʼязувач (кожна клітинка — одна з 7 форм, локальна узгодженість портів + одна петля) — 🥇.

## Мапа на каталог
- Є: `single-loop-check` ↔ одна петля · `pipe-connectors` ↔ дані труби з портами · `path-drawing`, `path-cut`, `edge-marking` ↔ ввід ліній · `keyboard-controls` ↔ клавіші форм у редакторі · `markup-validity`, `conflict-highlight`, `completion-detection`, `satisfy-constraints` · `undo-redo` · `in-game-editor`, `import-open-formats` · `level-bank` ↔ Janko.
- **Нема** → пропозиції карток:
  - `+crossing-detection`, `+bridge-cell`, `+fill-all-cells` — уже пропоновані в корпусі.
  - `+given-segments` «Частина лінії дана наперед; до таких клітинок нічого не додається» · game-logic/constraints · 🌱.
  - `+numbered-loops` «Кілька петель; числа визначають, які точки на одній петлі» · game-logic/constraints · 📎.

## Пропозиції до словників
- `+cond:degree(cell, n)` — скільки сегментів у клітинці (повтор).
- `+cond:crosses` — лінія перетинає себе в клітинці (повтор).
- `+effect:draw` — гравець малює сегмент лінії (повтор).
- `+trigger:pattern(loop_branch)` — розгалуження лінії (повтор).
- `+card:given-segments`, `+card:numbered-loops` — див. мапу.

## Джерела
- ⭐ [puzz.link: Pipelink](https://puzz.link/rules.html?pipelink) — правила з картинками й плеєр (рендериться JS; текст узято з pzpr-samples).
- [puzz.link pipelink.js](https://puzz.link/js/pzpr-samples/pipelink.js) — правила EN/JA (перехрестя прямо, дані сегменти), «Nikoli vol. 45», коди ceAddLine / lnBranch / lnPlLoop / lnNotCrossMk / ceNoLine / lnDeadEnd.
- [Janko: Pipelink](https://www.janko.at/Raetsel/Pipelink/index.htm) — правила DE/EN, Nikoli №45 жовтень 1993, 200 пазлів, Reflexion / Barns / Aisuban / Aisurom.
- [pzprjs pipelink.js](https://raw.githubusercontent.com/robx/pzprjs/master/src/variety/pipelink.js) — форми труб, клавіші, автозʼєднання, чек-листи трьох жанрів.
- [puzz.link pipelinkr.js](https://puzz.link/js/pzpr-samples/pipelinkr.js) і [loopsp.js](https://puzz.link/js/pzpr-samples/loopsp.js) — правила Returns (vol. 110) і Loop Special (vol. 57).
- [pzprjs failcode.en.json](https://raw.githubusercontent.com/robx/pzprjs/master/src/res/failcode.en.json) — тексти lnCrossExCir / lnCurveOnCir / lnCrossOnNum / lpPlNum / lpSepNum / lpNoNum.

## Непевне
- (?) Точні тексти ceAddLine, lnNotCrossMk і ceNoLine для Pipelink не бачив — у `message` переказ; зміст lnNotCrossMk («даний хрест мусить бути перетином») — з назви перевірки checkNotCrossOnMark.
- (?) Маркер «?» (ques −2) у редакторі Pipelink є в коді, але його правило в коді не описане.
- (?) Автор жанру не названий ні в Janko, ні в pzpr-samples.
- (?) Дедукції «кут поля» і «дана труба» — загальна логіка, не з джерела.
