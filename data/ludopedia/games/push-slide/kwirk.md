---
title: Kwirk (Puzzle Boy)
slug: kwirk
family: push-slide
also: []
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 1989
platforms: [Game Boy, Famicom Disk System, PC Engine]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Kwirk", best: true, note: "режими Going Up? / Heading Out? / Vs, турнікети, блоки, дірки, перемикання персонажів, back до 8 ходів"}
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/パズルボーイ", note: "оригінал Puzzle Boy: турнікети хрестом/Т, блок у дірку свого розміру, multi-play"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=kwirk+game+boy+gameplay", note: "пошук; геймплей"}
  - {kind: other, url: "https://strategywiki.org/w/index.php?search=Kwirk", note: "пошук StrategyWiki (сторінка віддає 403 у фетчі)"}
stage: v2
coverage: 75
mechanics: [move-4dir, keyboard-controls, push-object, multi-cell-size, impassable-cells, reach-exit, cell-transform, sequential-levels, level-select, difficulty-levels, time-bonus, score-records, theme-select, +turnstile, +fill-hole, +party-switch, +all-must-exit, +undo-redo, +simultaneous-versus]
proposes: ["+trigger:input", "+cond:free", "+effect:rotate", "+effect:set_cell", "+effect:move", "+effect:counter", "+role:gate", "+role:terrain", "+axis:actors", "+axis:undo", "+ui:move-counter", "+ui:progress-meter", "+window:mode-select", "+window:difficulty-select", "+feature:view-toggle", "+card:turnstile"]
author: opus
date: 2026-11-02
---

# Kwirk — проведи помідора (і друзів) через кімнату турнікетів, блоків і дірок до сходів

## Суть
Покрокова кімнатна головоломка з видом згори: Kwirk має дійти до сходів на протилежному боці кімнати. Головні перешкоди — **турнікети** (брусок-«хрест» на осі, що обертається на 90° від поштовху), **блоки різних розмірів** і **дірки** в підлозі, які можна засипати, зіштовхнувши в них блок. У частині кімнат під керуванням кілька персонажів (Veggie Friends), перемикання — кнопкою Select, і до сходів мають дійти **усі**. Ворогів і часу на поразку нема: це чистий Sokoban-подібний пазл з обертанням.

## Поле і час
- Кімната — квадратна сітка, обнесена цегляними стінами; на вищих рівнях кімнати ширші й з більшою кількістю перешкод (JA-вікі). Розмір (~10×18?) і чи камера скролить великі кімнати — (?).
- Шари: підлога (звичайна / дірка / сходи) + обʼєкти (персонажі, блоки, крила турнікетів, осі турнікетів).
- Хід = один крок активного персонажа (можливо з поштовхом блока або поворотом турнікета); без вводу світ не змінюється (`time: turn`). У Heading Out? і Vs таймер іде, але лише для очок/перегонів.
- Дві проєкції на вибір — «діагональна» (тіні, псевдо-3D) і «Bird's Eye» (плоска згори); логіка однакова.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Kwirk | player | позиція | рух 4 напрямки; штовхає блок; повертає турнікет |
| Veggie Friends (Curly Carrot, Eddie Eggplant, Pete the Pepper, Sass the Squash) | player | активний / неактивний | рухаються як Kwirk, без особливих здібностей; неактивний — перешкода |
| Цегляна стіна | static | — | непрохідна, нерухома |
| Блок | object | розмір w×h (1×1, 1×2, 2×2, …) | зсувається на 1 цілим, якщо всі клітини попереду вільні; штовхається лише по одному |
| Дірка | terrain | — | непрохідна для персонажа; блок над діркою падає й засипає її |
| Засипана дірка | terrain | — | звичайна підлога |
| Турнікет — вісь | static | — | центр обертання, сама нерухома |
| Турнікет — крило | object | 1–4 крила (одинарний, подвійний, потрійний, хрест) | штовхнуте крило повертає весь турнікет на 90° навколо осі |
| Сходи | terrain | — | вихід; персонаж, що став, покидає кімнату |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next_cell)` → ТО `move(active, dir)`, `counter(steps, +1)`.
- КОЛИ `input(dir)` → ЯКЩО `cell(next_cell, wall|hole|axis)` або `occupied(next_cell, friend)` → ТО `block`.
- КОЛИ `contact(active, block)` → ЯКЩО `free(all_cells_ahead_of_block)` → ТО `push`, `move(active, dir)`; інакше `block` (два блоки підряд не штовхаються).
- Над діркою: КОЛИ `enter(block, hole)` → ЯКЩО `custom: «увесь блок лежить над дірковими клітинами»` → ТО `disappear_a`, `set_cell(covered_cells, floor)`; дірка того ж розміру зникає повністю, частково заповнена лишає решту дірок (?).
- КОЛИ `contact(active, wing)` → ЯКЩО `custom: «клітини, які замітають крила при повороті на 90°, вільні»` → ТО `rotate(turnstile, ±90)` (напрям — залежно від того, з якого боку штовхнули крило), `move(active, dir)` (персонаж проходить у звільнену клітину) (?); інакше `block`.
- Турнікет не обертається, якщо будь-яке крило вперлося в стіну, блок, персонажа чи іншу вісь (саме тому одинарний турнікет працює як «двері в один бік»).
- КОЛИ `input(select)` → ТО `custom: «перемкнути активного персонажа»` (лише в кімнатах з кількома).
- КОЛИ `enter(char, stairs)` → ТО `disappear_a` (персонаж вийшов).
- КОЛИ `all_gone(player)` (усі персонажі вийшли сходами) → ТО `win`, `next_level`.
- КОЛИ `input(back)` → ТО `custom: «скасувати хід»` — до 8 разів (Going Up?).
- КОЛИ `input(redo)` (меню) → ТО `restart` кімнати.
- Перемога: усі персонажі на сходах. · Поразка: формально нема; глухий кут → Back або Redo. · Рахунок: Going Up? — за часом і кількістю кроків; Heading Out? — бонус кімнати стартує з 2000, спадає з часом і скидається на кожній новій кімнаті, сума → таблиця топ-4.

## Керування і ввід
- D-pad — крок активного персонажа (з поштовхом/поворотом).
- Select — перемкнути персонажа; A — меню кімнати: Redo (рестарт), End (у меню), Back (undo до 8 разів).
- Призначення Start і B — (?).
- Vs: два Game Boy через Link Cable, кожен проходить свою послідовність кімнат.

## Вікна, меню, HUD
- `splash-screen` — титул.
- `mode-select` (custom-window): Going Up? · Heading Out? · Vs. Mode.
- `difficulty-select`: Easy / Average / Hard (Going Up? — по 10 поверхів на складність).
- `settings-window` (?): вибір вигляду — Diagonal / Bird's Eye.
- Heading Out?: `custom-window` налаштування забігу — кількість кімнат (усього 99) (?), складність.
- `game-screen`: кімната; HUD — `level-number` (поверх/кімната), `timer-elapsed` або бонус, що спадає (Heading Out?), `move-counter` (?).
- `pause-menu` (кнопка A): Redo · End · Back.
- `end-screen`: результат поверху (час, кроки) / підсумок забігу; `leaderboard` топ-4 (Heading Out?).
- Vs: `game-screen` + `progress-meter` прогресу обох гравців; вибір матчу — одна гра або best of 3/5/7/9, гандикап різною кількістю кімнат.
- Переходи: splash → mode-select → difficulty-select → game-screen → (усі вийшли) end-screen/наступна кімната → … → leaderboard.

## Фічі поза полем
- `difficulty-presets` (Easy/Average/Hard), `levels-sequential` (Going Up?: 3×10 поверхів) + `mode-time-attack` (Heading Out?: обрана кількість з 99 кімнат на час).
- `undo` обмежений 8 ходами + `restart-level` (Redo).
- `leaderboard-local` топ-4 очок Heading Out?.
- `mode-versus` через Link Cable з гандикапом і серіями best-of.
- `theme-select`-подібне перемикання проєкції (Diagonal / Bird's Eye) — той самий стан, інший рендер.
- Нема редактора, паролів (?), збереження.

## Варіації й родичі
- Puzzle Boy (JP, герой — картоплина Potelin / ポテりん; в EN-вікі — Spud) → Kwirk (US, помідор); порти FDS (1990) і PC Engine (1991), лише Японія; Windows (2006, на основі PC Engine); Amazing Tater / Puzzle Boy II (1991 JP, 1992 US) — та сама механіка; Spud's Adventure (1991) — екшн-відгалуження. JA-режими: Puzzle (вибір поверху, мінімум ходів і часу) / Trial (серія на швидкість) / Versus.
- Осі варіацій:
  - **обертання**: нема (Sokoban) / турнікет 1–4 крила навколо осі (Kwirk) / обертання цілого поля (інші ігри);
  - **розмір блоків**: 1×1 / прямокутні w×h (Kwirk, Rush Hour) / довільні поліоміно;
  - **що робить блок у дірці**: зникає й засипає (Kwirk) / стає мостом (Chip's Challenge — блок у воду → земля) / застрягає;
  - **кількість аватарів**: один / кілька з перемиканням, усі мають вийти (Kwirk, XOR, The Lost Vikings);
  - **undo**: нема / 8 ходів (Kwirk) / ∞ (сучасні).
- Родичі: Sokoban, Chip's Challenge (блоки у воду), Adventures of Lolo, Boxxle; сучасні thinky з поворотними брусками (Stephen's Sausage Roll — обертання, Tametsi ні).

## Цікавинки для курсу
- Турнікет: перевірка «чи вільні клітини, які замітає кожне крило при повороті на 90°» + оновлення позицій крил — 🥉 (геометрія повороту на сітці навколо точки).
- Блоки w×h: штовхання з перевіркою цілого фронту блока — 📎 (картка `multi-cell-size` дорожча, бо там рух уздовж осі).
- Дірка, що засипається блоком, з частковим заповненням — 📎.
- Кілька аватарів, Select-перемикання, «вийти мають усі», неактивні — перешкоди — 🥉.
- Undo з обмеженою глибиною (кільцевий буфер на 8 станів) — 🌱.
- Розвʼязувач для кімнат із турнікетами (BFS по станах: позиції персонажів + орієнтації турнікетів + блоки + засипані дірки) — 🥇.
- Режим перегонів двох гравців на тій самій послідовності кімнат з progress-meter — 🥉.

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls` ↔ D-pad; `push-object` ↔ блоки; `multi-cell-size` ↔ блоки w×h; `impassable-cells` ↔ цегла й осі; `reach-exit` ↔ сходи; `cell-transform` ↔ дірка → підлога; `sequential-levels` + `level-select` ↔ поверхи/вибір кімнат; `difficulty-levels` ↔ Easy/Average/Hard; `time-bonus` ↔ спадний бонус Heading Out?; `score-records` ↔ топ-4; `theme-select` ↔ Diagonal/Bird's Eye.
- **Нема** → пропозиції карток:
  - `+turnstile` «Турнікет: обертання навколо осі від поштовху» · entities/interact · 🥉 · слот {wings: 1..4}.
  - `+fill-hole` «Блок засипає дірку» · entities/interact · 📎 · слот {partial: bool} — родич `cell-transform`, але зі зникненням блока.
  - `+party-switch` (вже пропонована XOR) — кілька аватарів, перемикання кнопкою.
  - `+all-must-exit` «Вийти мають усі аватари» · game-logic/win · 🌱.
  - `+undo-redo` (Sokoban) · слот depth = 8.
  - `+simultaneous-versus` (Snake/Tron) — дві консолі, однакові кімнати, хто швидше.

## Пропозиції до словників
- `+trigger:input` — крок і Select.
- `+cond:free` — вільні всі клітини фронту блока / клітини, які замітає крило.
- `+effect:rotate` — поворот турнікета на 90°; `+effect:set_cell` — дірка → підлога; `+effect:move` — крок; `+effect:counter` — кроки.
- `+role:gate` — турнікет як «двері, що пропускають лише в один бік»; `+role:terrain` — дірка, сходи.
- `+axis:actors` — `party`: кілька підконтрольних по черзі; `+axis:undo` — `limited` (8).
- `+ui:move-counter`; `+ui:progress-meter` — смуга прогресу кожного гравця в перегонах.
- `+window:mode-select`, `+window:difficulty-select` — окремі екрани вибору.
- `+feature:view-toggle` — перемикання проєкції (згори / псевдо-3D) без зміни логіки.
- `+card:turnstile` — механіка, якої в каталозі нема зовсім.

## Джерела
- ⭐ [Wikipedia: Kwirk](https://en.wikipedia.org/wiki/Kwirk) — режими й їхні правила, меню на A (Redo/End/Back до 8 разів), перешкоди (цегла, турнікети 1–4, блоки, дірки), Veggie Friends і Select, складності, вигляди, бонус 2000, порти й сиквели.
- [Wikipedia JA: パズルボーイ](https://ja.wikipedia.org/wiki/パズルボーイ) — турнікети хрестом/Т, блоки по одному, дірка засипається каменем того ж розміру, multi-play, режими Puzzle/Trial/Versus, ширші поверхи на вищих рівнях.
- [StrategyWiki: пошук](https://strategywiki.org/w/index.php?search=Kwirk) — проходження (сторінка гри віддає 403 у фетчі).
- YouTube: пошук «kwirk game boy gameplay».

## Непевне
- (?) Чи персонаж проходить у клітину разом із поворотом турнікета, чи лише повертає його й лишається — з памʼяті (проходить); JA-вікі цього не каже.
- (?) Що робить блок, більший/менший за дірку: JA-вікі каже лише «камінь того ж розміру → підлога»; часткове заповнення — припущення.
- (?) Розмір кімнати в клітинах і чи великі кімнати скролять, наявність лічильника кроків у HUD, призначення Start/B — не перевірено.
- (?) Чи є окремий екран налаштувань для вигляду, чи вибір вигляду — частина меню режиму.
