---
title: Shannon switching game / Bridg-It (+ Untangle)
slug: shannon-switching
family: connect-rotate
also: [chess-abstract, pencil-logic]
klass: cursor
axes:
  field: graph
  time: turn
  opponent: hotseat
  info: full
  random: none
  goal: state
year: 1951
platforms: [board, web, PC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Shannon_switching_game", best: true, note: "правила Short/Cut на графі, розвʼязок Lehman 1964, Gale/Bridg-It, складність"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Bridg-It", note: "Game of Gale: дві зсунуті сітки точок 5×6, перший гравець виграє, варіант з 10 мостами"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Connection_game", note: "місце серед ігор зʼєднання: Hex, TwixT, Bridg-It"}
  - {kind: other, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/untangle.html", note: "Untangle (Tatham): правила, керування мишею й клавіатурою, параметр — кількість точок"}
  - {kind: play, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/untangle.html", note: "грати Untangle в браузері"}
  - {kind: other, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/common.html", note: "спільні дії колекції Tatham: undo/redo, solve, game ID, seed, save/load"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Planarity", note: "Planarity (Tantalo, 2005) — предок Untangle; генерація з випадкових прямих, NP-повнота мінімуму ходів"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Bridg-It+Gale+game+strategy", note: "пошук; Bridg-It і стратегія"}
stage: v1
coverage: 70
mechanics: [hot-seat, turn-enforcement, ai-opponent, ai-greedy, cell-click, drag-drop-piece, hover-highlight, game-screen, end-screen, completion-detection, satisfy-constraints, unique-puzzle-generation, level-solver, game-settings, field-size-picker, save-game, sequential-levels, +connectivity-check, +edge-claim, +edge-delete, +spanning-tree-strategy, +crossing-detection, +vertex-drag, +graph-generation-planar, +seed-and-game-id, +undo-redo, +auto-solve]
proposes: ["+role:terminal", "+role:node", "+role:link", "+trigger:pattern(connected(a, b))", "+trigger:pattern(cut(a, b))", "+trigger:all_constraints_met", "+cond:connected", "+cond:path_exists", "+cond:crosses(e1, e2)", "+effect:claim_edge", "+effect:delete_edge", "+effect:move(vertex, xy)", "+ui:crossing-highlight", "+feature:seed-input", "+feature:auto-solve", "+axis:field=graph", "+card:edge-claim", "+card:spanning-tree-strategy", "+card:crossing-detection", "+card:vertex-drag"]
author: opus
date: 2026-11-02
---

# Shannon switching game / Bridg-It (+ Untangle) — ігри на графі: зʼєднай термінали або розріж; розплутай ребра

## Суть
Граф із двома виділеними вершинами A і B. Двоє ходять по черзі: **Short** фарбує (закріплює) одне незафарбоване ребро, **Cut** видаляє одне незафарбоване ребро. Short виграє, якщо зафарбовані ребра зʼєднали A з B; Cut — якщо всі шляхи між A і B зруйновано; нічиєї не буває. Bridg-It (David Gale, 1958) — та сама гра на двох зсунутих сітках точок, де кожен водночас і будує свій міст, і блокує чужий. Гра **повністю розвʼязана** (Lehman, 1964): переможець визначається двома ребро-неперетинними кістяковими деревами — рідкісний випадок, коли «секретна» виграшна стратегія — це чистий алгоритм на графах. Untangle (Tatham, за Planarity) — одиночна графова головоломка: перетягуй вершини, доки ребра не перестануть перетинатися.

## Поле і час
- Shannon: довільний граф (поле `graph`), ребра мають 3 стани: вільне / зафарбоване Short / видалене Cut. Хто ходить першим — домовленість (результат залежить від цього).
- Bridg-It: дві вкладені сітки точок 5×6 (жовта і червона, зсунуті на півклітини); міст зʼєднує дві сусідні ортогонально точки свого кольору і перекриває чужий потенційний міст, що його перетинає. Жовтий зʼєднує верх із низом, червоний — лівий край із правим. На дошці 1960 року — 20 мостів кожного кольору.
- Покроково, без часу. Партія завершується гарантовано: кожен хід зменшує кількість вільних ребер.
- Untangle: вільні координати на площині (вершини — точки, ребра — відрізки), час статичний; розмір — кількість точок.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Термінал A, B (Shannon) | terminal (custom) | 2 вершини | Short хоче звʼязати, Cut — розʼєднати |
| Вершина | node (custom) | координати (Untangle) | у Shannon нерухома; в Untangle — тягнеться мишею |
| Ребро вільне | link (custom) | — | Short може зафарбувати, Cut — видалити |
| Ребро зафарбоване | mark | власник Short | недоторканне; частина шляху A–B |
| Ребро видалене | mark | — | зникає з графа |
| Точка-стовпчик Bridg-It | node (custom) | колір: жовтий / червоний | кінці мостів одного кольору |
| Міст Bridg-It | piece | колір; горизонтальний або вертикальний | зʼєднує 2 сусідні точки свого кольору; блокує перехресний чужий |
| Край-ціль Bridg-It | zone | верх/низ або ліво/право | звʼязати свої протилежні краї — перемога |
| Ребро Untangle | link (custom) | пара вершин | прямий відрізок; перетин з іншим — порушення |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(click, edge)` → ЯКЩО `turn_of(short)` and `state(edge, free)` → ТО `claim_edge(edge)`, `pass_turn`.
- КОЛИ `input(click, edge)` → ЯКЩО `turn_of(cut)` and `state(edge, free)` → ТО `delete_edge(edge)`, `pass_turn`.
- КОЛИ `turn_end` → ЯКЩО `connected(A, B, claimed_edges)` → ТО `win(short)`.
- КОЛИ `turn_end` → ЯКЩО `not path_exists(A, B, claimed ∪ free)` → ТО `win(cut)`.
- Bridg-It: КОЛИ `input(place_bridge, p, q)` → ЯКЩО `same(p, q, color)` and `custom: «p, q сусідні ортогонально»` and `free(crossing_slot)` → ТО `place(bridge)` — займає і свій зʼєднувач, і чужий, що його перетинає (= Short для себе і Cut для суперника одночасно).
- Bridg-It: КОЛИ `turn_end` → ЯКЩО `custom: «мости кольору c звʼязали свої протилежні краї»` → ТО `win(c)`; нічия неможлива (топологія сітки, як у Hex).
- Bridg-It, варіант «10 мостів»: КОЛИ `custom: «мости скінчились»` → ТО хід = `move` одного свого моста на нове місце.
- Стратегія Short (теорема Lehman): ЯКЩО граф (на множині вершин з A і B) має два ребро-неперетинні кістякові дерева T1, T2 → Short виграє навіть другим: Cut видаляє e з T1 → Short фарбує ребро f з T2, яке знову зʼєднує дві частини T1−e, і вважає f спільним для обох дерев — інваріант зберігається.
- Стратегія Bridg-It: першому гравцю виграш гарантовано; явна стратегія — парування (Oliver Gross, Gardner 1961) (?) або через кістякові дерева.
- Untangle: КОЛИ `input(drag, vertex, xy)` → ТО `move(vertex, xy)`.
- Untangle: КОЛИ `after(move)` → ЯКЩО `not exists crosses(e1, e2)` для всіх пар ребер → ТО `win` (`all_constraints_met`), `flash` (?).
- Перемога: Short — шлях A–B, Cut — розріз · Bridg-It — свої краї звʼязано · Untangle — нуль перетинів · Рахунку нема.

## Керування і ввід
- Shannon/Bridg-It (цифрова версія): клік по ребру (або по парі сусідніх точок) — зафарбувати/видалити; `hover-highlight` ребра під курсором, `turn-indicator`.
- Untangle: ЛКМ на точку й тягнути; клавіатура: стрілки — вибір точки, Enter — почати/закінчити тягнути, Tab/Space — перебір усіх точок.
- Спільні дії Tatham: N — нова гра, U/Ctrl+Z — undo, R/Ctrl+R — redo, Restart, Solve.

## Вікна, меню, HUD
- (цифрова версія Shannon/Bridg-It) `main-menu` → `match-setup` (хто Short/Cut, хто ходить першим, людина/AI, розмір сітки 5×6 чи інший) → `game-screen` (граф, `turn-indicator`, лічильник ходів) → `end-screen` з підсвіченим шляхом або розрізом.
- Untangle (Tatham): `game-screen` — полотно з точками і лініями; кнопки New game, Restart game, Undo move, Redo move, Solve game.
- Меню Game: Enter game ID, Enter random seed, Download/Upload save file, Preferences (`settings-window`); меню Type: розміри + Custom… (`custom-window`: «Number of points»).
- Переходи Untangle: game-screen → (Solve) розвʼязаний стан → (Undo) назад; New game → новий граф.

## Фічі поза полем
- Untangle: `seed-input` / `share-code` (game ID відтворює ту саму гру), `save-slots` через файл, `undo`/`redo` без обмежень, `auto-solve` (Solve, відкочується undo), `custom-difficulty` (кількість точок).
- Planarity: `levels-sequential` — рівень n будується з n+3 випадкових прямих; gPlanarity — перетягування кількох вершин разом.
- Shannon/Bridg-It: `hotseat`, `ai-opponent-levels` — ідеальний AI реалізовний за поліноміальний час (на відміну від Hex); `custom-rules` (розмір сітки, обмежений запас мостів із перестановкою).

## Варіації й родичі
- Hex (вершини замість ребер; PSPACE-важка), TwixT (мости-конем), Bridg-It (сітка Gale), Shannon-варіанти на орієнтованих графах і матроїдах (лише теоретичні).
- Untangle ↔ Planarity (Tantalo, 2005; ідея Mary Radcliffe) ↔ gPlanarity (Chris Montgomery).
- Осі варіацій: **що займають: ребра / вершини (Hex)** · **ролі: асиметричні Short/Cut / симетричні (Bridg-It)** · **поле: довільний граф / сітка / площина з координатами** · **гравців: 2 / 1 (Untangle)** · **мета: звʼязність / площинність**.

## Цікавинки для курсу
- Перевірка «A і B звʼязані зафарбованими» і «чи ще існує шлях через вільні» — два BFS/DSU після кожного ходу — 📎.
- Bridg-It на сітці: модель «міст займає свій слот і блокує перехресний» (дві сітки, одна множина слотів) — 🥉.
- Непереможний AI для Short за теоремою Lehman: знайти два ребро-неперетинні кістякові дерева і відповідати на кожен розріз — 👑 (матроїди; для Bridg-It-сітки дерева можна задати вручну — 🥇).
- Untangle: перевірка перетину двох відрізків (векторний добуток) і підрахунок усіх перетинів — 📎; підсвітка ребер, що перетинаються — 🌱.
- Генерація розвʼязного Untangle: випадкові прямі → вершини в перетинах → ребра між сусідніми перетинами → перемішати вершини по колу — 🥉.
- Game ID / seed для відтворення партії — 📎.

## Мапа на каталог
- Є: `hot-seat` · `turn-enforcement` · `ai-opponent` / `ai-greedy` · `cell-click` (клік по ребру) · `drag-drop-piece` (тягнути вершину) · `hover-highlight` · `game-screen` · `end-screen` · `completion-detection` · `satisfy-constraints` (Untangle) · `unique-puzzle-generation` (генерація гарантовано площинного графа — не унікальність, а розвʼязність) · `level-solver` (Solve) · `game-settings` · `field-size-picker` (кількість точок) · `save-game` · `sequential-levels` (Planarity).
- **Нема** → пропозиції карток:
  - `+connectivity-check` «Звʼязність мережі» · game-logic/constraints · 🥉 · слот {goal: terminals_connected|cut}.
  - `+edge-claim` «Захоплення ребра графа» · entities/legality · 📎.
  - `+edge-delete` «Видалення ребра суперником» · entities/legality · 🌱.
  - `+spanning-tree-strategy` «Ідеальна стратегія через два кістякові дерева» · game-logic/opponent · 👑.
  - `+crossing-detection` «Перетини відрізків» · game-logic/constraints · 📎.
  - `+vertex-drag` «Перетягування вершини з вільними координатами» · interface/input · 📎.
  - `+graph-generation-planar` «Генерація площинного графа і перемішування» · levels/generation · 🥉.
  - `+seed-and-game-id` «Game ID / seed для відтворення» · levels/format · 📎.
  - `+undo-redo` «Undo/redo ходів гравця» · game-logic · 📎.
  - `+auto-solve` «Показати розвʼязок (Solve), відкочується undo» · game-logic/difficulty · 🌱.

## Пропозиції до словників
- `+role:terminal` — фіксовані кінці (A, B; з Flow Free); `+role:node` / `+role:link` — вершина і ребро графа як сутності поля `graph`.
- `+trigger:pattern(connected(a, b))` / `+trigger:pattern(cut(a, b))` — нові значення шаблону: термінали звʼязані / розʼєднані назавжди.
- `+trigger:all_constraints_met` ⏳ підтверджується (Untangle).
- `+cond:connected` / `+cond:path_exists` (×4 у корпусі — підтвердження); `+cond:crosses(e1, e2)` — два відрізки перетинаються.
- `+effect:claim_edge` / `+effect:delete_edge` — зафарбувати / видалити ребро; `+effect:move(vertex, xy)` — `move` у вільні координати.
- `+ui:crossing-highlight` — підсвітка ребер, що перетинаються (?).
- `+feature:seed-input` ⏳, `+feature:auto-solve` ⏳ — підтвердження.
- `+axis:field=graph` — підтвердження значення.

## Джерела
- ⭐ [Wikipedia: Shannon switching game](https://en.wikipedia.org/wiki/Shannon_switching_game) — правила Short/Cut, дуальність, розвʼязок Lehman (матроїди), Gale 1958, Bridg-It 1960, звʼязок із Hex, поліноміальна складність.
- [Wikipedia: Bridg-It](https://en.wikipedia.org/wiki/Bridg-It) — дві зсунуті сітки 5×6, 20 мостів кольору, перший виграє, варіант з 10 мостами й перестановкою, Ludii.
- [Wikipedia: Connection game](https://en.wikipedia.org/wiki/Connection_game) — класи ігор зʼєднання, Hex, TwixT.
- [Tatham: Untangle — довідка](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/untangle.html) — правила, миша/клавіатура, параметр «Number of points», Planarity як джерело.
- [Tatham: Untangle — грати](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/untangle.html) — меню Game/Type, кнопки New/Restart/Undo/Redo/Solve.
- [Tatham: спільні дії](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/common.html) — гарячі клавіші, Specific/Random seed, Save/Load.
- [Wikipedia: Planarity](https://en.wikipedia.org/wiki/Planarity) — Tantalo 2005, генерація з прямих, gPlanarity, NP-повнота мінімуму ходів.

## Непевне
- (?) Рік: Shannon придумав гру «десь до 1951»; поставлено 1951.
- (?) Явна парувальна стратегія Bridg-It (Oliver Gross, колонка Gardner 1961) — з памʼяті; Wikipedia лише посилається на демо стратегії червоного.
- (?) Як саме Tatham генерує граф Untangle (не як Planarity з прямих, а випадкові точки + ребра без перетинів?) і чи підсвічує перетини — довідка не каже; «спалах» при розвʼязанні — з памʼяті.
- (?) Цифрових версій Shannon/Bridg-It з меню не перевіряв (Ludii згадано у Wikipedia); вікна — «(цифрова версія)».
- (?) Хто ходить першим у класичному Shannon — Wikipedia не уточнює.
