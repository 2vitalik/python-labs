---
title: Land Maker (Builder's Block)
slug: land-maker
aka: [ランドメーカー, Landmaker, LandMaker, "Builder's Block"]
family: falling-match
also: []
klass: avatar
axes:
  field: iso
  time: realtime
  opponent: ai
  info: full
  random: runtime
  goal: survive
year: 1998
platforms: [arcade (Taito F3), PlayStation, PlayStation Network (Game Archives)]
links:
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/ランドメーカー", best: true, note: "JA: ромбове поле, постріл знизу, схили, перефарбування, будівлі, великі будівлі 2×2–4×4, предмети, безбарвні фігури супернику, dead line"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Land_Maker", note: "EN: персонажі й стихії, боси, режими PS, дати, Builder's Block"}
  - {kind: other, url: "https://psxdatacenter.com/games/U/B/SLUS-01086.html", note: "Builder's Block (NTSC-U): режими Puzzle / Battle / Arcade, знесення будівлі пострілом у кут"}
  - {kind: other, url: "https://nextquest.dev/games/builders-block", note: "опис: 7 курсів Puzzle-режиму, будувати задані розміри не руйнуючи"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Land+Maker+Taito+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [shoot-forward, event-points, garbage-attack, simultaneous-versus, ai-opponent, character-select, sequential-levels, mode-select, keyboard-controls, +slope-deflect, +wall-bounce-shot, +recolor-on-stick, +building-group-clear, +shape-bonus, +clear-leaves-item, +garbage-pushback, +dead-line]
proposes: ["+effect:recolor_neighbors", "+effect:deflect", "+effect:offset_garbage", "+role:building", "+card:slope-deflect", "+card:recolor-on-stick", "+card:building-group-clear", "+card:shape-bonus"]
author: opus
date: 2026-11-09
---

# Land Maker — стріляй кольоровими фігурами на ромбове поле: вони ковзають схилами, перефарбовують сусідів і складаються в будівлі

## Суть
Versus-головоломка Taito на кшталт Puzzle Bobble за виглядом, але ближча до Puyo за грою: знизу екрана гравець вистрілює кольорові фігури вгору по полю з ромбових (◇) клітин в ізометрії. Фігура, що влучила в схил, ковзає по діагоналі вгору, відбивається від краю, прилипає до першої зустрічної фігури й **перефарбовує** фігури за нею у свій колір. Однокольорові сусіди злипаються в «будівлю»; постріл того ж кольору у вершину будівлі знищує її цілком, а ромби 2×2/3×3/4×4 дають «великі будівлі» з предметом. Знищені будівлі летять супернику безбарвними фігурами зверху; хто перетне dead line — програв.

## Поле і час
- Поле — сітка ромбів (квадрати, повернуті на 45°, «◇-узор»), ізометрична проєкція; стрілок — унизу, фігури йдуть знизу вгору. Розміри поля — (?).
- Real-time; два поля поруч (гравець і CPU / другий гравець). Сміття суперника приходить згори.
- Шари: фігури на полі (колір / безбарвна) + «будівлі» як звʼязні однокольорові групи + предмети в центрі знесених великих будівель.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Стрілок (персонаж) | player | позиція внизу; персонаж (8 + 2 боси) | рухається вздовж низу, стріляє фігурою вгору |
| Фігура в польоті | projectile | колір | летить вгору; на схилі — діагонально вгору проти схилу; біля краю поля — розворот |
| Фігура на полі | tile | колір | прилипає; перефарбовується сусідньою прилиплою |
| Будівля | zone | звʼязна група одного кольору, розмір | постріл того ж кольору у вершину (верх/низ ромба) знищує її цілком; більша — більше очок |
| Велика будівля | zone | ромб 2×2 / 3×3 / 4×4 | дає очки при утворенні; знесена — лишає предмет у центрі |
| Предмет | pickup | ефект (?) | знесений/використаний — очищає фігури й будівлі або змінює кольори |
| Безбарвна фігура (сміття) | hazard | — | приходить від суперника згори, насувається; відштовхується власними зачистками |
| Dead line | zone | лінія | фігури за нею + нема куди стріляти → поразка |
| Схил | terrain | напрям | відхиляє фігуру діагонально вгору в протилежний бік |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(move)` → ТО `move(shooter, dir)` уздовж низу; КОЛИ `input(fire)` → ТО `spawn_at(piece, shooter_column)`, `move(piece, up)` щотік.
- КОЛИ `contact(piece, slope)` → ТО `custom: «deflect — фігура йде діагонально вгору в бік, протилежний схилу»`.
- КОЛИ `edge(piece)` → ТО `bounce(piece)` — розворот діагоналі біля краю поля.
- КОЛИ `contact(piece, field_piece)` (гранню) → ТО `custom: «прилипає»`, `custom: «recolor — фігури на клітину далі за точкою дотику набувають її кольору»`.
- КОЛИ `contact(piece, building)` вершиною (верх/низ ромба) → ЯКЩО `same(piece, building, color)` → ТО `clear(building)` — уся звʼязна група, `score(size)`.
- КОЛИ `pattern(group(n))` → ЯКЩО `connected(same_color)` → ТО `custom: «група стає будівлею»`.
- КОЛИ `pattern(diamond 2×2|3×3|4×4)` одного кольору → ТО `transform(building, large_building)`, `score(n)`.
- КОЛИ `destroyed(large_building)` → ТО `spawn_at(item, center)`.
- КОЛИ `destroyed(item)` / `custom: «предмет використано»` → ТО `clear(pieces_and_buildings)` або `paint(cells, color)` (?).
- КОЛИ `after(clear)` → ЯКЩО `mode(versus)` → ТО `send_garbage(colorless_pieces)` — кількість за розміром знесеного; суперникові згори.
- КОЛИ `after(clear)` → ЯКЩО `count(incoming_garbage, >, 0)` → ТО `custom: «offset — власні зачистки відштовхують безбарвні фігури назад»`.
- КОЛИ `custom: «нема куди вистрілити»` → ЯКЩО `occupied(dead_line, piece)` → ТО `lose`.
- КОЛИ `counter(wins, ==, n)` → ТО `win` матчу; 1P: 10 стадій проти CPU, далі боси Ranju → Gaira.
- Перемога: суперник перетнув dead line (раунди до N перемог) · Поразка: власні фігури за dead line · Рахунок: розмір будівлі, бонус за велику будівлю.

## Керування і ввід
- Аркада: важіль (рух стрілка) + кнопки (постріл; призначення решти — (?)).
- Гравець цілиться **колонкою пострілу й схилами**, а не кутом, як у Puzzle Bobble (?).
- 2P — одночасно на двох полях.

## Вікна, меню, HUD
- `attract-demo` / титул (аркада, (?)).
- `character-select`: 8 персонажів зі стихіями — Hiryu (вогонь), Aifa (рослини), Soumei (лід), Renki (бруд), Youen (звук), Kouko (камінь), Rinrei (мечі), Roushinshi (блискавка); персонаж змінює дизайн фігур і ефект ураження; боси Ranju і Gaira — за кодом.
- `game-screen`: два поля поруч, `danger-line` (dead line), `score`, `spawn-indicator` / лічильник сміття, що летить (?).
- `end-screen` раунду / матчу; `game-over-continue` (аркада, (?)).
- PS: `mode-select` — Arcade (точний порт) · Puzzle (7 курсів, 3D) · Battle (2P, 3D).
- Переходи: титул → (PS) mode-select → character-select → game-screen → end-screen → наступна стадія.

## Фічі поза полем
- `mode-versus` (2P), 1P проти CPU — 10 стадій + боси (`ai-opponent-levels` за стадіями (?)).
- PS: `mode-puzzle` — 7 курсів, треба збудувати будівлі заданого розміру й **не руйнувати** їх; Battle — для проходження стадії потрібно 100 монет (?).
- Builder's Block: картка памʼяті (1 блок), PocketStation, вібрація.
- `cheat-codes`: боси як персонажі.

## Варіації й родичі
- **Builder's Block** (PS, NTSC-U, Jaleco) — американська назва PS-версії; у Arcade-режимі згадано будівлі до 5×5 (?).
- Родичі: Puzzle Bobble (стрілок унизу, відбиття від стін, стеля), Puyo Puyo / Baku Baku Animal (versus зі сміттям, звʼязні групи), Hexic / Hexa Sort (нестандартна сітка), Cleopatra Fortune (форма як умова зачистки).
- **Осі варіацій**: траєкторія пострілу (кут + відбиття від стін / **колонка + відхилення схилом**) · зачистка (≥3 кулі / **постріл того ж кольору в будівлю**) · вплив пострілу на сусідів (нема / **перефарбування**) · бонус за форму (нема / **ромб 2×2–4×4**).

## Цікавинки для курсу
- Ромбова сітка (квадрат під 45°) з координатами й сусідством по гранях — 📎.
- Траєкторія: прямо вгору → схил → діагональ проти схилу → розворот біля краю → прилипання — 🥉 (кілька станів снаряда).
- Перефарбування «на клітину далі» при прилипанні: зміна звʼязності груп одним пострілом — 🥉.
- Будівля = звʼязна однокольорова компонента; знесення цілої компоненти одним влученням — 📎 (flood fill).
- Розпізнавання ромба N×N одного кольору як бонусної форми — 🥉.
- Versus із безбарвним сміттям, яке відштовхують власні зачистки — 🥉.

## Мапа на каталог
- Є: `shoot-forward` (постріл угору) · `event-points` · `garbage-attack` · `simultaneous-versus` · `ai-opponent` · `character-select` · `sequential-levels` (10 стадій) · `mode-select` (PS) · `keyboard-controls` (важіль/кнопки).
- **Нема** → пропозиції карток:
  - `+slope-deflect` «Снаряд відхиляється схилом клітини» · entities/move · 🥉 · слот {dir}.
  - `+wall-bounce-shot` (вже є з Puzzle Bobble) — розворот біля краю поля.
  - `+recolor-on-stick` «Прилиплий снаряд перефарбовує сусідів» · entities/interact · 🥉 · слот {reach: 1}.
  - `+building-group-clear` «Влучання того ж кольору знищує всю звʼязну групу» · entities/legality · 📎.
  - `+shape-bonus` «Бонус за форму групи (ромб N×N)» · game-logic/score · 🥉 · слот {sizes}.
  - `+clear-leaves-item` «Знищена велика група лишає предмет» · entities/spawn · 📎 (родич `drop-on-death`).
  - `+garbage-pushback` «Власні зачистки відштовхують сміття суперника» · game-logic/opponent · 📎.
  - `+dead-line` «Лінія поразки на полі» · game-logic/lose · 🌱.

## Пропозиції до словників
- `+effect:recolor_neighbors` — після прилипання фігури сусіди за нею набувають її кольору (відрізняється від `paint`, бо колір береться від сутності, а не задається).
- `+effect:deflect` — снаряд змінює напрям за властивістю клітини (схил), а не відбивається (`bounce`).
- `+effect:offset_garbage` — власна зачистка гасить/відштовхує сміття, що летить (вже пропонована ×2: Puyo, Tetris).
- `+role:building` — звʼязна група плиток як одна сутність із розміром (вже пропонована ×10 в іншому значенні — будівля TD; куратору розвести).
- `+card:*` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia JA: ランドメーカー](https://ja.wikipedia.org/wiki/ランドメーカー) — правила: постріл знизу по ◇-полю, зачистка дотиком вершинами, схили й розворот біля краю, перефарбування на клітину далі, будівлі, великі будівлі 2×2/3×3/4×4 з предметом, безбарвні фігури супернику, відштовхування, dead line, 1P — 10 стадій, 8 персонажів, 1998/1999.
- [Wikipedia EN: Landmaker](https://en.wikipedia.org/wiki/Land_Maker) — Taito F3, versus-орієнтована аркада, персонажі й стихії, боси Ranju/Gaira, режими PS, дати, Builder's Block.
- [PSXDataCenter: Builder's Block](https://psxdatacenter.com/games/U/B/SLUS-01086.html) — Puzzle (7 курсів), Battle (100 монет), Arcade (8 персонажів + боси), «знести будівлю пострілом у кут».
- [NextQuest: Builder's Block](https://nextquest.dev/games/builders-block) — Puzzle-режим «будуй, не руйнуй».
- YouTube: пошук «Land Maker Taito gameplay».

## Непевне
- (?) Розміри поля, кількість кольорів, що саме «на клітину далі» перефарбовується (одна фігура чи весь ряд), як прибирати безбарвні фігури.
- (?) Ефекти предметів (JA: «очищає фігури й будівлі або змінює кольори» — без переліку).
- (?) Чи є каскади/ланцюги в класичному сенсі: джерела кажуть лише про очки за розмір будівлі.
- (?) Будівлі 5×5 і умова «100 монет» — з пошукових описів PS-версії, не з первинного джерела.
- (?) Дата NA: EN-вікі — 12.07.2000, PSXDataCenter — 07.12.2000.
- (?) Призначення кнопок, наявність прицілу/кута пострілу.
