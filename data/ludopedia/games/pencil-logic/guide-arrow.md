---
title: Guide Arrow (ガイドアロー)
slug: guide-arrow
aka: [ガイドアロー, Gaidoaro, guidearrow, Стрілка-провідник]
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
  - {kind: other, url: "https://puzz.link/rules.html?guidearrow", best: true, note: "puzz.link: правила EN/JA і плеєр (сторінка рендериться JS)"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/guidearrow.js", note: "puzz.link: текст правил, автор Inaba Naoki, тестові поля з кодами помилок"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/master/src/variety/guidearrow.js", note: "pzprjs: buildGoalDirections — обчислення справжніх напрямків до зірки обрізанням листків"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/master/src/res/failcode.en.json", note: "pzprjs: тексти csAdjacent / cuLoop / ceDirection .guidearrow"}
  - {kind: other, url: "https://www.janko.at/Raetsel/Guide-Arrow/index.htm", note: "Janko (як Gaidoaro): правила DE/EN/JA, клітинка, куди вказує стрілка, теж біла; 20 пазлів"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=guide+arrow+puzzle", note: "пошук; розвʼязання"}
stage: v1
coverage: 70
mechanics: [markup-validity, completion-detection, satisfy-constraints, cell-click, keyboard-controls, connectivity-check, conflict-highlight, in-game-editor, import-open-formats, level-bank, undo-redo, +cell-shade-toggle, +no-adjacent-check, +acyclic-check, +goal-direction-arrow]
proposes: ["+cond:acyclic", "+cond:on_path", "+card:goal-direction-arrow"]
author: opus
date: 2026-11-09
---

# Guide Arrow — зафарбуй клітинки так, щоб білі стали деревом, а кожна стрілка показувала єдиний перший крок до зірки

## Суть
На сітці — одна зірка ★ і кілька стрілок. Гравець зафарбовує клітинки: чорні не торкаються сторонами, білі утворюють одну звʼязну область **без петель** (заборонено й білий квадрат 2×2 — це теж петля). Отже білі клітинки — дерево, і від будь-якої білої клітинки до ★ веде рівно один шлях. Стрілка показує напрямок першого кроку цього шляху: з клітинки-стрілки до зірки можна вирушити лише туди, куди вона дивиться, не проходячи чорних клітинок і не повертаючись назад.

## Поле і час
- Прямокутна сітка, ортогональне сусідство; редактор pzprjs за замовчуванням 8×8; Janko — 20 пазлів.
- Шари: ★ і стрілки (дані, завжди білі) · зафарбування гравця · позначки «біле» (фон / хрестик).
- Одна ★ на поле (`goalpos` — один обʼєкт дошки).
- Час статичний; хід = зафарбувати / позначити / стерти клітинку.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітинка | mark | невідома / чорна / біла (позначка) | гравець перемикає |
| Зірка ★ | static | одна | корінь дерева білих; не фарбується |
| Стрілка | static | ↑ → ↓ ← | не фарбується; перший крок шляху до ★ іде за стрілкою |
| Клітинка «?» | static | — | підказка без напрямку: лише не фарбується (?) |
| Чорні клітинки | zone | — | жодні дві не сусідять сторонами |
| Білі клітинки | zone | одна компонента | звʼязні, без петель і без 2×2 — дерево з коренем у ★ |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left_click, cell)` → ЯКЩО `custom: «клітинка без стрілки й без ★»` → ТО `mark(cell, shaded)`; інакше `block` (pzprjs `allowShade`).
- КОЛИ `input(right_click, cell)` → ТО `mark(cell, unshaded)` — позначка «біле» (режими `unshade` / `peke`) (?).
- КОЛИ `constraint_broken(adjacent)` → ЯКЩО `not no_adjacent(shaded)` → ТО `set_state(cells, error)` (`csAdjacent`: «Some shaded cells are adjacent»).
- КОЛИ `constraint_broken(clue)` → ЯКЩО `custom: «стрілка або ★ зафарбована»` → ТО `set_state(cell, error)` (`csOnArrow`: «A cell with a clue is shaded»).
- КОЛИ `constraint_broken(divided)` → ЯКЩО `not connected(unshaded)` → ТО `set_state(board, error)` (`cuDivideRB`: «The unshaded cells are divided»).
- КОЛИ `pattern(loop_closed)` → ЯКЩО `custom: «петля з білих клітинок, зокрема 2×2»` (`+cond:acyclic`) → ТО `set_state(loop, error)` (`cuLoop`: «There is a loop of unshaded cells»).
- КОЛИ `constraint_broken(direction)` → ЯКЩО `custom: «перший крок шляху від стрілки до ★ не в напрямку стрілки»` (`+cond:on_path`) → ТО `set_state(arrow, error)` (`ceDirection`: «A cell does not follow the indicated direction towards the goal»).
- Справжній напрямок (pzprjs `buildGoalDirections`): `custom: «доки є біла клітинка з рівно одним ще не визначеним білим сусідом (або ★) — її напрямок = на цього сусіда»`; листки дерева «обрізаються» до кореня ★, клітинки в петлях напрямку не отримують.
- Перерахунок: КОЛИ `custom: «змінено зафарбування»` → ТО `set_state(board, stale)` — напрямки перебудовуються ліниво при перевірці.
- КОЛИ `all_constraints_met` → ТО `win`.
- Порядок перевірки pzprjs: сусідні чорні → зафарбована підказка → розрив білих → напрямок стрілок → петлі.
- Дедукція Janko: клітинка, на яку вказує стрілка, — біла (інакше першого кроку нема).
- Дедукція «інші три боки»: шлях від стрілки до ★ через бічного сусіда неможливий, тож кожен білий бічний сусід стрілки веде в гілку без ★.
- Дедукція «2×2»: у кожному квадраті 2×2 щонайменше одна чорна; разом із «чорні не сусідять» — або одна, або дві по діагоналі.
- Дедукція «зірка»: стрілка, сусідня з ★, мусить дивитися на ★ — ребро між двома білими сусідами в дереві і є єдиний шлях.
- Перемога: чорні не сусідять, білі — одне дерево, підказки білі, усі стрілки збігаються з першим кроком до ★. Поразки й рахунку нема.

## Керування і ввід
- Папір: зафарбувати клітинку, крапкою позначити білу.
- puzz.link play: клік — чорна; права кнопка / режим `unshade` — позначка білої; режими `shade`, `unshade`, `peke`, `info-blk` (підсвітити групу чорних) (?).
- puzz.link edit: drag у клітинці малює стрілку в напрямку руху (повторний — знімає); клавіші `1`/`w`/`Shift+↑` — ↑, `2`/`s` — →, `3`/`z` — ↓, `4`/`a` — ←, `5`/`q`/пробіл — очистити; `g` — поставити ★ під курсор; ★ перетягується мишею.

## Вікна, меню, HUD
- `game-screen`: сітка, ★, стрілки з обводкою, «?», чорні клітинки, позначки білих, `conflict-highlight` (сусідні чорні, петля, неправильна стрілка); перетягувана ★ підсвічується червоним.
- `editor-window` (puzz.link edit): стрілки, ★, розмір; експорт URL (зразок `4/4/33i3ele`).
- `help-window` — правила (puzz.link, Janko).
- `puzzle-select` — Janko: 20 пазлів.
- Решта — оболонка [puzz.link](puzz-link.md): Check, Undo/Redo, Trial, URL, таймер.

## Фічі поза полем
- `auto-check` за кнопкою з текстом першої помилки; `undo` / `redo`; trial-режим оболонки.
- `level-editor` + `share-code` (URL puzz.link: позиція ★ кодується першими двома символами); `export-import` (файл pzprv3).
- `puzzle-bank` — Janko 20 пазлів; генератора не бачив.

## Варіації й родичі
- «Чорні не сусідять + білі звʼязні»: [Hitori](hitori.md), [Heyawake](heyawake.md), [Kuromasu](kuromasu.md).
- Дерево білих і маршрут до цілі: [Nuri-Maze](nuri-maze.md) (кімнати, S→G через ○); стрілки-напрямки: [Signpost](signpost.md), [Yajilin](yajilin.md) (стрілка рахує чорні).
- Janko зве жанр «Gaidoaro»; автор і перша публікація там невідомі, pzprjs — Inaba Naoki.
- **Осі варіацій**: що каже стрілка (перший крок / відстань / кількість гілок) · одна ★ чи кілька · чи обовʼязкове дерево (без петель) · чи заборонене сусідство чорних.

## Цікавинки для курсу
- «Чорні не сусідять» + BFS-звʼязність білих — 🌱.
- Пошук циклу в ґратці білих (2×2 — найменший цикл) — 📎.
- Обрізання листків дерева до кореня ★ (`buildGoalDirections`) — 📎: топологічний обхід замість BFS від цілі.
- Те саме через BFS від ★ з батьківськими вказівниками — 🌱; порівняти два підходи — 📎.
- Розвʼязувач: зафарбування з пропагацією «стрілка ⇒ сусід білий» і перевіркою дерева — 🥈.

## Мапа на каталог
- Є: `markup-validity`, `completion-detection`, `satisfy-constraints` · `cell-click`, `keyboard-controls` (edit) · `connectivity-check` ↔ білі звʼязні · `conflict-highlight` · `in-game-editor`, `import-open-formats` · `level-bank` (Janko) · `undo-redo`.
- Перевикористано: `+cell-shade-toggle`, `+no-adjacent-check` (Kuromasu), `+acyclic-check` (Nuri-Maze).
- **Нема** → пропозиції карток:
  - `+goal-direction-arrow` «Стрілка = перший крок єдиного шляху до цілі в дереві» · game-logic/constraints · 📎 · слот {graph: tree|shortest-path} — Guide Arrow; родич `+route-checkpoints` (Nuri-Maze).

## Пропозиції до словників
- `+cond:acyclic` — повтор (Nuri-Maze): білі клітинки без петель.
- `+cond:on_path` — повтор (Nuri-Maze): клітинка (сусід за стрілкою) лежить на шляху до ★.
- `+card:goal-direction-arrow` — див. мапу.

## Джерела
- ⭐ [puzz.link: Guide Arrow](https://puzz.link/rules.html?guidearrow) — правила і плеєр; текст — у pzpr-samples.
- [pzpr-samples guidearrow.js](https://puzz.link/js/pzpr-samples/guidearrow.js) — 5 правил: «Shaded cells cannot be horizontally or vertically adjacent», «cannot form a loop. This includes 2x2 squares», «An arrow indicates the only direction…»; «invented by Inaba Naoki».
- [pzprjs guidearrow.js](https://raw.githubusercontent.com/robx/pzprjs/master/src/variety/guidearrow.js) — `buildGoalDirections`, checklist, `allowShade`, клавіші, режими вводу.
- [pzprjs failcode.en.json](https://raw.githubusercontent.com/robx/pzprjs/master/src/res/failcode.en.json) — тексти помилок.
- [Janko: Gaidoaro](https://www.janko.at/Raetsel/Guide-Arrow/index.htm) — правила DE/EN/JA, «Felder, auf die ein Pfeil zeigt» не фарбуються, 20 пазлів.

## Непевне
- (?) Рік і перша публікація: pzprjs називає автора Inaba Naoki, Janko — «невідомо»; `year: null`.
- (?) Клітинка «?» (pzprjs малює `drawHatenas`) — у текстах правил її нема; поведінку виведено з коду.
- (?) Призначення кнопок миші в play-режимі (`autoplay_func: cellpeke`) — з коду, у плеєрі не перевіряв.
- (?) UA-назва «Стрілка-провідник» — описовий переклад, усталеної нема.
