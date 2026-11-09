---
title: Islands of Insight
slug: islands-of-insight
aka: [IoI]
family: thinky
also: [pencil-logic]
klass: hybrid
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: setup
  goal: constraints
year: 2024
platforms: [PC]
links:
  - {kind: other, url: "https://freethoughtblogs.com/atrivialknot/2024/03/18/islands-of-insight-teaches-logic-puzzles", best: true, note: "розбір логічних сіток: лише чорне/біле, ~12 правил з Nurikabe/Numberlink/Yajilin/Galaxies/Kuromasu, «недопідказана» сітка"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Islands_of_Insight", note: "розробник Lunarch, видавець Behaviour, реліз 13.02.2024, shared-world, порівняння з The Witness"}
  - {kind: steam, url: "https://store.steampowered.com/app/2071500/Islands_of_Insight/", note: "10 000+ пазлів у 24 типах, 5 біомів, планер, 20+ Enclaves, оновлення пазлів, mastery, sparks, daily quests"}
  - {kind: other, url: "https://www.digitaltrends.com/gaming/islands-of-insight-pc-review/", note: "рецензія: перелік нелогічних типів (приховані предмети, арки, перспектива, кільця, музика), Mirabilis, дерево вмінь, кооп"}
  - {kind: other, url: "https://media.gdcvault.com/gdc2025/Slides/Grant_Elyot_Designing+10%2C000+Puzzles.pdf", note: "GDC 2025: 6 символів і 7 правил логічних сіток (+пост-реліз), Pattern / Music / Memory grid (бачено лише в результатах пошуку)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Islands+of+Insight+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [cell-click, satisfy-constraints, completion-detection, markup-validity, connectivity-check, line-sum-clue, unique-puzzle-generation, difficulty-rating, codex-window, map-window, player-camera, save-progress, background-music, +underclued-grid, +rule-discovery, +open-world-puzzles, +puzzle-refresh, +glide-traversal, +skill-tree, +memory-grid, +music-grid, +perspective-alignment, +symmetry-regions]
proposes: ["+cond:true_in_all_solutions", "+cond:symmetric", "+cond:visible_count", "+feature:puzzle-refresh", "+feature:skill-tree", "+feature:daily-quests", "+window:rules-tab", "+card:underclued-grid", "+card:rule-discovery", "+axis:session"]
author: opus
date: 2026-11-09
---

# Islands of Insight — відкритий світ, усипаний тисячами процедурних чорно-білих сіток і пазлів середовища

## Суть
Пазл-пригода від Lunarch Studios у «спільному світі»: гравець-«Шукач» мандрує островом і розвʼязує понад 10 000 пазлів 24 типів. Ядро — **логічні сітки**: клітини фарбуються лише в чорне або біле, а символи на сітці задають обмеження, запозичені з Nurikabe, Numberlink, Yajilin, Galaxies, Kuromasu. Правила не пояснюються текстом: перші сітки мають одне-два правила, і гравець виводить зміст символу сам («невидимий туторіал»). Решта типів — пазли середовища: перспектива, приховані предмети, арки, музика, перегони по сферах.

## Поле і час
- Дві площини: 3D-світ (5 біомів, вертикальність, політ на планері) і плоскі квадратні сітки-панелі в ньому — розміри від 3×3 до великих (?).
- Сітка: клітина = 2 стани (чорна/біла) + символи-підказки, вписані в частину клітин.
- Час статичний: сітка чекає; таймер є лише в перегонах по сферах (traversal).
- Пазли генеруються процедурно й з часом оновлюються — на тому самому місці зʼявляється новий пазл.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Шукач | player | вміння (планер, спринт) | ходить і літає світом, відкриває панелі |
| Клітина сітки | mark | black / white | гравець фарбує; перевіряється правилами |
| Число острова (Area Number) | mark | n | біла область з цим числом має рівно n клітин (Nurikabe) |
| «Море» | zone | чорні клітини | мають бути звʼязні й без квадрата 2×2 (Nurikabe-правило) |
| Літери | mark | буква | пари однакових літер зʼєднуються однією областю (з Numberlink) (?) |
| Дротики (Darts) | mark | напрям, n | рахують клітини в напрямку стрілки (з Yajilin) (?) |
| Лотос / Галактика | mark | центр симетрії | область навколо символу центрально-симетрична (з Galaxies) |
| Число огляду (Viewpoint) | mark | n | скільки клітин свого кольору видно з клітини в 4 боки (Kuromasu, Bag) |
| Недопідказана сітка | zone | кілька розвʼязків | фарбувати можна лише те, що однакове в усіх розвʼязках |
| Pattern / Music / Memory grid | zone | варіант сітки | шаблон, звукова доріжка, правила з памʼяті — інші типи сіток (GDC) |
| Пазли середовища | object | тип | приховані предмети, лінія погляду між символами, невидимі арки, вирівнювання перспективи, перетини кілець, музичний пад, сфери на час |
| Enclave | zone | набір пазлів | кураторське «підземелля», відкриває нові типи пазлів і зони кампанії |
| Mirabilis | pickup | — | збираються з викликів і Enclave-ів; відкривають нові частини острова |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(click, cell)` → ТО `mark(cell, black|white)` (ліва/права кнопка або перемикання (?)).
- КОЛИ `all_constraints_met` → ТО `win`, `custom: «пазл зараховано, нарахування досвіду mastery»`.
- КОЛИ `constraint_broken(c)` → ТО `custom: «сітка не приймається»`; підсвічування помилок — (?).
- Area Number: ЯКЩО `region_size(white_region, n)` для кожної області з числом n — обмеження виконано.
- Острови: ЯКЩО `custom: «кожна біла область містить рівно одне число»` (у класичному Nurikabe; в IoI — не завжди (?)).
- Море: ЯКЩО `connected(black)` and `no_2x2(black)` — виконано.
- Galaxies/Lotus: ЯКЩО `custom: «область навколо символу центрально-симетрична відносно нього»`.
- Viewpoint: ЯКЩО `custom: «кількість видимих клітин свого кольору в 4 напрямках = число»`.
- Letters: ЯКЩО `custom: «однакові літери в одній області, різні — в різних»` (?).
- Underclued: КОЛИ `input(click, cell)` → ЯКЩО `custom: «клітина не має однакового кольору в усіх розвʼязках»` → ТО `custom: «хід вважається помилкою»` (?).
- КОЛИ `custom: «зібрано достатньо Mirabilis»` → ТО `unlock(area)`.
- КОЛИ `custom: «пройдено Enclave»` → ТО `unlock(puzzle_type)`, `unlock(area)`.
- КОЛИ `counter(sparks, >=, cost)` → ТО `choose(skill)` — нове вміння (рух, бонуси до типу пазлів).
- КОЛИ `timer(period)` → ТО `custom: «розвʼязані процедурні пазли замінюються новими»`.
- КОЛИ `contact(seeker, orb)` у перегонах → ЯКЩО `timer(>, 0)` → ТО `counter(orbs, +1)`; усі сфери вчасно → `win`.
- Перемога: розвʼязати пазл · Поразки нема · Рахунок: досвід mastery по типах, Mirabilis, sparks.

## Керування і ввід
- Від третьої особи: рух, стрибок, спринт, планер (відкривається прогресією) (?).
- Логічна сітка: клік по клітині фарбує її (лише чорне/біле — без чисел, ліній, меж).
- Пазли середовища: стати в точку огляду (перспектива), клацнути предмет або перетин кілець, пройти арку.

## Вікна, меню, HUD
- `game-screen`: світ, панель-сітка в фокусі; HUD — індикатори mastery, квести дня (?).
- `map-window`: карта острова з позначками пазлів; окрема вкладка — словник усіх правил усіх типів (`+window:rules-tab`, близько до `codex-window`).
- `+feature:skill-tree` — вікно дерева вмінь за sparks (`upgrade-window`).
- `character-select` / кастомізація персонажа (косметика за рівні).
- `settings-window`, `pause-menu`, `main-menu` — (?).
- Переходи: світ ↔ сітка (підійти й почати); світ → мапа → вкладка правил.

## Фічі поза полем
- Прогресія: рівні mastery за типами пазлів, sparks → дерево вмінь, Mirabilis → нові зони, 20+ Enclave-ів відкривають типи пазлів.
- `+feature:puzzle-refresh` — процедурні пазли регулярно оновлюються; `+feature:daily-quests` — щоденні завдання.
- `unlockables` — косметика персонажа; `save-progress`.
- Спільний світ: інші гравці поруч; рецензія Digital Trends описує кооп із друзями, Steam позначає «single-player» (?).

## Варіації й родичі
- The Witness і Taiji — правила на панелях, які треба вивести самому; IoI бере ту саму ідею, але з процедурними сітками й MMO-обгорткою.
- Джерела правил: Nurikabe, Numberlink, Yajilin, Galaxies, Kuromasu, Bag; поруч — Tatham's Puzzles (процедурні, але кожна з одним правилом).
- Осі варіацій **логічної сітки**: що вводить гравець — колір / число / лінію; правила — пояснені / виводяться з прикладів; розвʼязок — єдиний / кілька, зараховується лише спільне (underclued); пазл — ручний / процедурний з оновленням.

## Цікавинки для курсу
- Двоколірна сітка з набором підключуваних правил-перевірок (область, звʼязність, без 2×2, симетрія, огляд) — 🥈.
- Перевірка «клітина однакова в усіх розвʼязках» (underclued) — 🥇: потрібен перебір розвʼязків або SAT.
- Генератор процедурних сіток з контролем складності й оновленням — 👑.
- Правило симетрії Galaxies для області — 🥉.
- Словник правил, що поповнюється, коли гравець їх зустрічає — 📎.
- Дерево вмінь за валюту — 📎.

## Мапа на каталог
- Є: `cell-click` ↔ фарбування; `satisfy-constraints`, `completion-detection`, `markup-validity`; `connectivity-check` ↔ море Nurikabe; `line-sum-clue` ↔ Viewpoint-числа (лічба по лініях); `unique-puzzle-generation` + `difficulty-rating` ↔ процедурні пазли; `codex-window` ↔ вкладка правил; `map-window`; `player-camera`; `save-progress`; `background-music`.
- **Нема** → пропозиції карток:
  - `+underclued-grid` «Кілька розвʼязків: зараховується лише спільне» · game-logic/constraints · 🥇.
  - `+rule-discovery` «Правило не пояснено — виводиться з простих прикладів» · levels/progression · 📎.
  - `+open-world-puzzles` «Пазли розкидані у відкритому світі» · levels/progression · 🥉.
  - `+puzzle-refresh` «Розвʼязані пазли періодично замінюються новими» · levels/generation · 🥉.
  - `+glide-traversal` «Планер/вміння руху як ключ до нових місць» · entities/move · 🥉.
  - `+skill-tree` «Дерево вмінь за валюту» · game-logic/economy · 📎.
  - `+memory-grid`, `+music-grid` — варіанти сітки: правила з памʼяті / звукова доріжка · 🥉.
  - `+perspective-alignment` «Стати в точку, з якої малюнок складається» · 🥈 (3D-камера).
  - `+symmetry-regions` «Область симетрична відносно центру» (Galaxies) · game-logic/constraints · 🥉.

## Пропозиції до словників
- `+cond:true_in_all_solutions` — клітина однакова в усіх розвʼязках (underclued).
- `+cond:symmetric` — область центрально-симетрична відносно символу.
- `+cond:visible_count` — кількість видимих клітин у 4 напрямках (Kuromasu, Viewpoint).
- `+feature:puzzle-refresh`, `+feature:skill-tree`, `+feature:daily-quests`.
- `+window:rules-tab` — вкладка мапи зі словником усіх побачених правил.
- `+card:underclued-grid`, `+card:rule-discovery` — як вище.
- `+axis:session` — `endless` (пазли оновлюються без кінця) поруч із кураторськими Enclave-ами.

## Джерела
- ⭐ [A Trivial Knot: Islands of Insight teaches logic puzzles](https://freethoughtblogs.com/atrivialknot/2024/03/18/islands-of-insight-teaches-logic-puzzles) — лише чорне/біле, ~12 правил і їхні прототипи, Nurikabe-правила моря, underclued-сітки, «невидимий туторіал».
- [Wikipedia](https://en.wikipedia.org/wiki/Islands_of_Insight) — розробник, видавець, дата, shared-world, рецепція.
- [Steam](https://store.steampowered.com/app/2071500/Islands_of_Insight/) — 10 000+ пазлів, 24 типи, біоми, планер, Enclaves, оновлення пазлів, mastery, sparks, daily quests.
- [Digital Trends: review](https://www.digitaltrends.com/gaming/islands-of-insight-pc-review/) — типи нелогічних пазлів, Mirabilis, дерево вмінь, кооп, критика повторюваності.
- [GDC 2025, Grant Elyot: Designing 10,000 Puzzles](https://media.gdcvault.com/gdc2025/Slides/Grant_Elyot_Designing+10%2C000+Puzzles.pdf) — числа символів/правил і три додаткові типи сіток (PDF завеликий для фетча; дані з анотації пошуку).
- YouTube: пошук «Islands of Insight gameplay».

## Непевне
- (?) Точні формулювання правил Letters і Darts в IoI (тут — за прототипами з Numberlink і Yajilin); чи обовʼязкове «одне число на острів».
- (?) Як карається хибний хід в underclued-сітці (помилка одразу чи перевірка в кінці).
- (?) Повний список 24 типів (назви з фан-вікі не відкрились — fandom 402, wiki.gg 401); розміри сіток.
- (?) Кооп: Steam — single-player, рецензія — гра з друзями; спільний світ показує інших гравців.
- (?) Керування мишею для сітки (ліва/права кнопка), наявність підсвічування помилок і undo на сітці.
