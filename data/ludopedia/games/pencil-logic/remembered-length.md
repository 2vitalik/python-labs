---
title: Remembered Length
slug: remembered-length
aka: [remlen]
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
  - {kind: play, url: "https://puzz.link/rules.html?remlen", best: true, note: "puzz.link: правила з картинкою й плеєр (сторінка рендериться JS)"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/remlen.js", note: "правила EN/JA, автор Palmer Mebane, коди помилок"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/master/src/variety/country.js", note: "pzprjs: модуль регіональних петель; перевірка blRemLength в обох напрямках"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/master/src/res/failcode.en.json", note: "текст помилки blRemLength"}
  - {kind: other, url: "https://arxiv.org/html/2510.21938v2", note: "arXiv 2025: NP-повнота All or Nothing, Water Walk і Remembered Length (T-metacell)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=remembered+length+puzzle", note: "пошук; розвʼязання"}
stage: v1
coverage: 55
mechanics: [markup-validity, completion-detection, satisfy-constraints, conflict-highlight, single-loop-check, path-drawing, path-cut, edge-marking, impassable-cells, undo-redo, in-game-editor, import-open-formats, +irregular-regions, +crossing-detection, +directed-loop, +hamiltonian-path-check, +next-region-length-clue]
proposes: ["+cond:degree(cell, n)", "+cond:crosses", "+cond:line_length(visit, op, n)", "+ui:direction-arrows", "+card:next-region-length-clue"]
author: opus
date: 2026-11-09
---

# Remembered Length — спрямована петля крізь усі клітинки; число регіону «запамʼятовується» і задає довжину наступного візиту в сусідній регіон

## Суть
Поле поділене на регіони, частина з них має число. Гравець малює одну замкнену петлю через усі білі клітинки, без розгалужень і перетинів, і обирає їй напрям обходу. Щоразу, коли петля виходить із регіону з числом N, її наступна ділянка — суцільний візит у сусідньому регіоні — має бути рівно N клітинок. Незвичне: число говорить не про свій регіон, а про той, куди петля піде далі, тож напрям обходу — частина розвʼязку.

## Поле і час
- Прямокутна сітка, розбита на нерегулярні регіони; можуть бути зафарбовані клітинки (петля їх оминає).
- Петля йде по ортогоналі між центрами клітинок; кожна біла клітинка має степінь 2.
- «Візит» — максимальна суцільна ділянка петлі в одному регіоні; регіон можна відвідувати скільки завгодно разів, кожен вихід з числового регіону перевіряється окремо.
- Шари: межі регіонів, числа, зафарбовані (незмінні) · сегменти, хрестики, стрілки напрямку гравця.
- Час статичний; хід = провести / стерти сегмент.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітинка | terrain | — | біла: петля мусить пройти |
| Зафарбована клітинка | static | — | петля не заходить |
| Регіон | zone | клітинки, межа | відвідується будь-скільки разів |
| Число регіону | mark | N | після кожного виходу з регіону наступний візит має N клітинок |
| Візит | zone | довжина | суцільна ділянка петлі в одному регіоні |
| Петля | zone | напрям обходу | одна, замкнена, через усі білі; без розгалужень і перетинів |
| Сегмент | mark | ребро | частина петлі |
| Хрестик | mark | ребро | нотатка «тут лінії нема» |
| Стрілка напрямку | mark | ребро, напрям | нотатка гравця; перевірка її не читає |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag, cells)` → ТО `custom: «намалювати сегменти вздовж шляху»` (+effect:draw).
- КОЛИ `input(left_click, edge)` → ТО `mark(edge, arrow)` — стрілка напрямку (режим diraux), не впливає на перевірку.
- КОЛИ `input(right_drag, edge)` → ТО `mark(edge, cross)` або стрілка — залежно від того, з чого почато drag (pzprjs).
- КОЛИ `constraint_broken(branch)` → ЯКЩО `custom: «клітинка з трьома або більше сегментами»` → ТО `message(«There is a branch line»)` · `flash(cell)` — lnBranch.
- КОЛИ `constraint_broken(cross)` → ЯКЩО `custom: «лінія перетинає себе в клітинці»` → ТО `message(«There is a crossing line»)` · `flash(cell)` — lnCross.
- КОЛИ `constraint_broken(remembered_length)` → ЯКЩО `custom: «в обох напрямках обходу є вихід з регіону N, після якого наступний візит не має N клітинок»` → ТО `message(«A number does not indicate the length of the visit in the next room»)` · `flash(visits)` — blRemLength.
- КОЛИ `constraint_broken(dead_end)` → ЯКЩО `custom: «лінія обривається»` → ТО `message(«There is a dead-end line»)` — lnDeadEnd.
- КОЛИ `constraint_broken(many_loops)` → ЯКЩО `not single_loop` → ТО `message(«There are multiple loops»)` — lnPlLoop.
- КОЛИ `constraint_broken(no_line)` → ЯКЩО `not cover_all(loop)` → ТО `message(«клітинка без лінії»)` · `flash(cell)` — ceNoLine.
- КОЛИ `all_constraints_met` → ТО `win`.
- Порядок перевірок у pzprjs: lnBranch → lnCross → blRemLength → lnDeadEnd → lnPlLoop → ceNoLine.
- Напрям: перевірка проходить петлю в обидва боки й приймає розвʼязок, якщо хоч один напрям виконує всі числа; помилку підсвічує в напрямку з меншою кількістю порушень.
- Перемога: одна петля через усі білі клітинки і напрям обходу, за якого кожен вихід з числового регіону веде у візит потрібної довжини. Поразки й рахунку нема.
- Дедукція «замалий сусід»: петля не може вийти з регіону N прямо в сусідній регіон, менший за N клітинок, — ця межа закрита в цьому напрямку.
- Дедукція «одиничка»: після регіону з 1 петля заходить у наступний регіон рівно на одну клітинку й одразу виходить.
- Дедукція «напрям»: якщо в одному напрямку якесь число неможливе, напрям обходу визначено для всієї петлі.

## Керування і ввід
- puzz.link (play): лівий drag — лінія; лівий клік по ребру — стрілка напрямку; правий drag — хрестики або стрілки (?); режими line / peke / diraux / clear / info-line.
- puzz.link (edit): drag по ребрах — межі регіонів; клік — число регіону; режим empty — зафарбована клітинка; «?» вимкнено.
- Папір: лінія олівцем; напрям зручно позначати стрілками на лінії.

## Вікна, меню, HUD
- `game-screen` (puzz.link): сітка з межами регіонів, числа, зафарбовані клітинки, лінія, хрестики, стрілки; `check-button`, `undo-button`, `redo-button`; `conflict-highlight` — візити з помилкою.
- `editor-window` (puzz.link edit) — межі, числа, зафарбовані, експорт у URL.
- `help-window` — правила (puzz.link).
- Переходи: URL пазла → `game-screen` → перевірка.

## Фічі поза полем
- `auto-check` за кнопкою; `undo` / `redo`.
- `level-editor` + `share-code` (URL puzz.link).
- Нотатки напрямку (стрілки на ребрах) — допоміжний шар, перевірка їх ігнорує.

## Варіації й родичі
- Автор жанру — Palmer Mebane (puzz.link, arXiv).
- У модулі pzprjs «country» — ціла родина регіональних петель: Country Road, Detour, Dotchi-Loop, Double Back, Maxi Loop, Moon or Sun, All or Nothing, Onsen-meguri, Ovotovata, Rassi Silai, Wataridori.
- Складність: у тій самій статті arXiv доведено NP-повноту All or Nothing (Inaba Naoki) і Water Walk (Martin Ender).
- У корпусі: [Country Road](country-road.md) (число = клітинки петлі у своєму регіоні), [Moon or Sun](moon-or-sun.md), [Nagareru Loop](nagareru-loop.md) (спрямована петля), [Masyu](masyu.md).
- **Осі варіацій**: що рахує число (свій регіон / наступний візит / найдовший візит) · спрямованість (нема / вибирає гравець / задана стрілками) · покриття (усі клітинки / ні) · кількість візитів у регіон (рівно 1 / будь-скільки).

## Цікавинки для курсу
- Розбиття циклу на візити: пройти петлю й склеїти сусідні клітинки одного регіону в ділянки (run-length по регіонах) — 📎.
- Перевірка в обидва боки обходу з вибором кращого напрямку для підсвітки — 🌱.
- Шар стрілок-нотаток на ребрах, який не бере участі в перевірці — 🌱.
- Гамільтонова петля по всіх білих клітинках (степені 2 + одна компонента) — 🥉.
- Розвʼязувач: петля + обмеження на довжини візитів — 🥇; доведення NP-повноти гаджетами (arXiv) — 👑 як матеріал для читання.

## Мапа на каталог
- Є: `single-loop-check` ↔ одна петля · `path-drawing`, `path-cut`, `edge-marking` ↔ ввід ліній · `impassable-cells` ↔ зафарбовані · `markup-validity`, `conflict-highlight`, `completion-detection`, `satisfy-constraints` · `undo-redo` · `in-game-editor`, `import-open-formats`.
- **Нема** → пропозиції карток:
  - `+irregular-regions`, `+crossing-detection`, `+directed-loop`, `+hamiltonian-path-check` — уже пропоновані в корпусі.
  - `+next-region-length-clue` «Число регіону задає довжину наступного візиту петлі в інший регіон» · game-logic/constraints · 📎.

## Пропозиції до словників
- `+cond:degree(cell, n)` — скільки сегментів лінії в клітинці (повтор).
- `+cond:crosses` — лінія перетинає себе (повтор).
- `+cond:line_length(visit, op, n)` — довжина ділянки лінії (повтор; тут — візит у регіон).
- `+ui:direction-arrows` — стрілки напрямку на лінії як нотатка (повтор).
- `+card:next-region-length-clue` — див. мапу.

## Джерела
- ⭐ [puzz.link: Remembered Length](https://puzz.link/rules.html?remlen) — правила з картинкою й плеєр (рендериться JS; текст узято з pzpr-samples).
- [puzz.link remlen.js](https://puzz.link/js/pzpr-samples/remlen.js) — правила EN/JA (спрямована петля через усі білі, «наступний регіон» з урахуванням повторних візитів), автор Palmer Mebane, коди ceNoLine / lnBranch / lnCross / lnPlLoop / blRemLength.
- [pzprjs country.js](https://raw.githubusercontent.com/robx/pzprjs/master/src/variety/country.js) — режими вводу, зафарбовані (empty), алгоритм перевірки в обидва напрямки, порядок перевірок.
- [pzprjs failcode.en.json](https://raw.githubusercontent.com/robx/pzprjs/master/src/res/failcode.en.json) — текст blRemLength і загальні тексти lnBranch / lnCross / lnDeadEnd / lnPlLoop.
- [arXiv 2510.21938](https://arxiv.org/html/2510.21938v2) — формальні правила, автор Palmer Mebane, NP-повнота.

## Непевне
- (?) Рік і місце першої публікації: відомо лише автора (Palmer Mebane).
- (?) Тексту помилки ceNoLine для цього жанру не бачив — у `message` переказ.
- (?) Розкладка правої кнопки (хрестик чи стрілка) — з опису коду, не перевірена в плеєрі.
- (?) Дедукції «замалий сусід», «одиничка», «напрям» — загальна логіка, не з джерела.
