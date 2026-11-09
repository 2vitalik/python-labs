---
title: Nuri-Maze (Nurimeizu, ぬりめいず)
slug: nuri-maze
aka: [Nurimeizu, Nurimaze, ぬりめいず, Нурі-Мейз, Зафарбуй лабіринт]
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
  - {kind: official, url: "https://www.nikoli.co.jp/en/puzzles/nurimeizu/", best: true, note: "Nikoli: 5 правил — кімнати фарбуються цілком, білі звʼязні без петель, ○ на шляху S→G, △ — ні, без 2×2"}
  - {kind: play, url: "https://puzz.link/rules.html?nurimaze", note: "puzz.link: плеєр з автоперевіркою (сторінка рендериться JS)"}
  - {kind: other, url: "https://puzz.link/js/pzpr-samples/nurimaze.js", note: "правила EN, «Puzzle Communication Nikoli vol. 145», коди помилок"}
  - {kind: other, url: "https://raw.githubusercontent.com/robx/pzprjs/master/src/variety/nurimaze.js", note: "реалізація: S/G, ○/△, фарбування кімнати цілком, DFS-маршрут, checklist"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=nurimeizu+puzzle", note: "пошук; розвʼязання"}
stage: v1
coverage: 80
mechanics: [satisfy-constraints, markup-validity, completion-detection, conflict-highlight, cell-click, dot-mark, connectivity-check, reachability-check, maze-generation, level-solver, in-game-editor, import-open-formats, undo-redo, +irregular-regions, +no-2x2-check, +room-fill-click, +acyclic-check, +route-checkpoints]
proposes: ["+cond:acyclic", "+cond:on_path", "+card:acyclic-check", "+card:route-checkpoints"]
author: opus
date: 2026-11-09
---

# Nuri-Maze — зафарбуй цілі кімнати так, щоб білі клітинки стали деревом-лабіринтом, де шлях S→G проходить усі кола й оминає трикутники

## Суть
Сітка поділена жирними лініями на кімнати; у деяких клітинках — S (старт), G (ціль), кола ○ і трикутники △. Гравець зафарбовує кімнати **цілком** (стіни) або лишає білими (коридори). Білі клітинки мають бути звʼязні, без петель і без білих чи чорних квадратів 2×2 — тобто білі утворюють «дерево», і шлях S→G у ньому єдиний. Усі ○ мають лежати на цьому шляху, усі △ — поза ним (у глухих кутах). Незвичне: гравець **будує лабіринт**, а не проходить його — генерація лабіринту стає пазлом.

## Поле і час
- Прямокутна сітка, ортогональне сусідство; кімнати — довільні звʼязні групи клітинок (часто 1–3 клітинки (?)).
- Шари: межі кімнат і символи S/G/○/△ (дані) · стан кімнати гравця: невідомо / чорна / біла.
- Час статичний; хід = зафарбувати чи позначити білою кімнату (в puzz.link — вся кімната одним кліком).
- Маршрут не малюється: він випливає з білих клітинок (шлях у дереві між S і G).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітинка | mark | unknown / shaded / unshaded | стан однаковий у всій кімнаті |
| Кімната | zone | клітинки між межами | фарбується цілком або лишається білою |
| S (старт) | static | клітинка | кімната з S не фарбується; початок маршруту |
| G (ціль) | static | клітинка | кімната з G не фарбується; кінець маршруту |
| Коло ○ | static | клітинка | кімната не фарбується; клітинка — на шляху S→G |
| Трикутник △ | static | клітинка | кімната не фарбується; клітинка — поза шляхом S→G (тупик) |
| Білі клітинки (лабіринт) | zone | компонента | одна звʼязна, без петель (дерево), без 2×2 |
| Чорні клітинки (стіни) | zone | — | без 2×2; звʼязність не вимагається |
| Маршрут S→G | zone | клітинки | єдиний шлях у дереві білих = найкоротший |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left_click, cell)` → ЯКЩО `not custom: «у кімнаті S, G, ○ або △»` → ТО `paint(room, shaded)` — уся кімната; інакше `mark(room, unshaded)` (puzz.link).
- КОЛИ `input(right_click, cell)` → ТО `mark(room, unshaded)` — кімната позначена білою (фон) (?).
- КОЛИ `constraint_broken(room)` → ЯКЩО `custom: «кімната частково чорна, частково біла»` → ТО конфлікт `bkMixed`.
- КОЛИ `constraint_broken(object)` → ЯКЩО `custom: «S, G, ○ або △ на чорній клітинці»` → ТО конфлікт `objShaded`.
- КОЛИ `constraint_broken(white)` → ЯКЩО `not connected(unshaded)` → ТО конфлікт `cuDivide`.
- КОЛИ `pattern(block2x2)` → ЯКЩО `custom: «усі чотири білі»` → ТО конфлікт `cu2x2`; ЯКЩО `custom: «усі чотири чорні»` → ТО конфлікт `cs2x2`.
- КОЛИ `pattern(loop_closed)` → ЯКЩО `custom: «петля з білих клітинок»` (`+cond:acyclic`) → ТО конфлікт `cuLoop`.
- КОЛИ `constraint_broken(route)` → ЯКЩО `custom: «○ не на шляху S→G»` (`+cond:on_path`) → ТО конфлікт `routeIgnoreCP`.
- КОЛИ `constraint_broken(route)` → ЯКЩО `custom: «△ на шляху S→G»` → ТО конфлікт `routePassDeadEnd`.
- КОЛИ `all_constraints_met` → ТО `win`.
- Маршрут: `custom: «DFS від S по білих до G; клітинки шляху — onroute, решта білих — outroute»` (puzz.link `getMazeRouteInfo`); через відсутність петель шлях єдиний, тож «найкоротший» Nikoli = «єдиний».
- Дедукція: кімнати з S, G, ○, △ — білі одразу; дві білі кімнати, що замкнули б петлю, — одна з них чорна; білий 2×2 → щонайменше одна кімната в ньому чорна.
- Дедукція △: трикутник — у тупиковій гілці; клітинка, що зʼєднала б △ із шляхом «напряму», мусить бути відгалуженням, а не частиною S→G.
- Перемога: кімнати одноколірні, білі — звʼязне дерево, без 2×2 обох кольорів, ○ на шляху, △ поза ним. Поразки й рахунку нема.

## Керування і ввід
- puzz.link: клік по клітинці фарбує всю кімнату (кімнату з символом — лише позначає білою); режими `shade` / `unshade`; drag — кілька кімнат (?).
- Редактор puzz.link: межі drag-ом, ○ і △ — режими `mark-circle` / `mark-triangle` або клавіші `1`/`q` і `2`/`w`; S і G — переносні (за замовчуванням лівий верхній і правий нижній кут).
- Info-режим `info-line` / `info-road` — підсвітити звʼязний коридор (?).

## Вікна, меню, HUD
- `game-screen`: сітка з жирними кімнатами, S/G/○/△, чорні кімнати, `conflict-highlight` (кімната / 2×2 / петля / символ), кнопка перевірки.
- `help-window` — правила (Nikoli, puzz.link).
- `editor-window` — puzz.link edit: межі, символи, S/G; експорт URL.
- Решта — оболонка [puzz-link](puzz-link.md) (Undo/Redo, Trial, URL, таймер).
- Переходи: edit → play → Check → повідомлення з кодом помилки.

## Фічі поза полем
- `auto-check` (puzz.link, коди помилок), `undo` / `redo`, `level-editor` + `share-code` (URL).
- Банк — журнал Puzzle Communication Nikoli (жанр — з vol. 145); генератора не бачив.

## Варіації й родичі
- Перша поява — Puzzle Communication Nikoli vol. 145 (puzz.link).
- Родичі «зафарбуй кімнату цілком»: [Heyawake](heyawake.md), [LITS](lits.md) (тетраміно в кімнаті), Norinori; «білі звʼязні + без 2×2»: [Nurikabe](nurikabe.md) (там чорні звʼязні), [Yin-Yang](yin-yang.md) (обидва кольори звʼязні, без 2×2).
- Чекпоінти на шляху: [Masyu](masyu.md) (перлини на петлі), [Icebarn](icebarn.md) (стрілки на шляху).
- Генерація лабіринтів (`maze-generation`: DFS/Прим дають саме дерево — «perfect maze»).
- **Осі варіацій**: одиниця фарбування (клітинка / кімната) · форма білих (дерево / звʼязні з петлями) · обмеження маршруту (чекпоінти ○ / заборонені △ / довжина) · заборона 2×2 (обох / одного кольору).

## Цікавинки для курсу
- Фарбування кімнати одним кліком (клік → room id → усі клітинки) — 🌱.
- Звʼязність і ациклічність білих: BFS + перевірка «ребер = вершин − 1» або union-find з виявленням циклу — 📎.
- Шлях у дереві S→G (DFS з батьками) і перевірка ○ на шляху / △ поза ним — 📎.
- Заборона 2×2 для обох кольорів — 🌱.
- Розвʼязувач: бінарний стан на кімнату + пропагація (символи → біле, петлі, 2×2) + перебір — 🥉.
- Генератор: випадкове остовне дерево (perfect maze) → кімнати навколо стін → символи на шляху/тупиках → перевірка єдиності — 🥇.

## Мапа на каталог
- Є: `satisfy-constraints`, `markup-validity`, `completion-detection`, `conflict-highlight` · `cell-click`, `dot-mark` (біла кімната) · `connectivity-check` ↔ білі звʼязні · `reachability-check` ↔ шлях S→G · `maze-generation` ↔ розвʼязок = «досконалий» лабіринт · `level-solver` · `in-game-editor`, `import-open-formats`, `undo-redo` (puzz.link).
- Перевикористано: `+irregular-regions`, `+no-2x2-check` (nurikabe).
- **Нема** → пропозиції карток:
  - `+room-fill-click` «Клік фарбує всю кімнату» · interface/input · 🌱.
  - `+acyclic-check` «Білі без петель (дерево)» · game-logic/constraints · 📎.
  - `+route-checkpoints` «Обовʼязкові й заборонені точки на шляху» · game-logic/constraints · 📎 · слот {must: ○, must_not: △}.

## Пропозиції до словників
- `+cond:acyclic` — множина клітинок не містить циклу (дерево); пара до `connected`.
- `+cond:on_path` — клітинка лежить на шляху між двома точками.
- `+card:acyclic-check`, `+card:route-checkpoints` — див. мапу.

## Джерела
- ⭐ [Nikoli: Nurimeizu](https://www.nikoli.co.jp/en/puzzles/nurimeizu/) — 5 правил: лабіринт S→G по білих; кімнати цілком; білі не розірвані й без петель; кімнати з S, G, ○, △ білі, ○ на найкоротшому шляху, △ — ні; без 2×2 обох кольорів.
- [puzz.link: nurimaze.js (samples)](https://puzz.link/js/pzpr-samples/nurimaze.js) — правила EN, vol. 145, коди `bkMixed`, `objShaded`, `cuDivide`, `cu2x2`, `cs2x2`, `cuLoop`, `routeIgnoreCP`, `routePassDeadEnd`.
- [src/variety/nurimaze.js](https://raw.githubusercontent.com/robx/pzprjs/master/src/variety/nurimaze.js) — S/G за замовчуванням у кутах, ○/△ (`ques` 41/42), фарбування кімнати, DFS-маршрут, checklist.
- [puzz.link: Nurimaze](https://puzz.link/rules.html?nurimaze) — плеєр.
- YouTube: пошук «nurimeizu puzzle».

## Непевне
- (?) Рік vol. 145 — номер бачив, рік — ні.
- (?) Права кнопка й drag у puzz.link для цього жанру — з загальної поведінки плеєра.
- (?) Типовий розмір кімнат і полів Nikoli — з памʼяті.
- (?) Чи `info-road` підсвічує маршрут саме в цьому жанрі.
