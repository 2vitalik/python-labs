---
title: "Archaica: The Path of Light"
slug: archaica-the-path-of-light
aka: [Archaica]
family: connect-rotate
also: []
klass: cursor
axes:
  field: iso
  time: static
  opponent: none
  info: full
  random: none
  goal: state
year: 2017
platforms: [PC (Windows), Xbox One, Switch]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/550590/Archaica_The_Path_of_Light/", best: true, note: "Two Mammoths, 08.09.2017: дзеркала й кольорове скло, засвітити всі кристали, ієрогліфи, ачівки, хмара"}
  - {kind: other, url: "https://www.thexboxhub.com/archaica-the-path-of-light-review/", note: "огляд Xbox: конвертер, дільник, змішування кольорів, сенсор-перемикачі, 50+ рівнів у 5 зонах, підказки-кристали, Альманах"}
  - {kind: other, url: "https://www.xboxtavern.com/archaica-the-path-of-light-review/", note: "огляд: телепорти, Stone Keys → бонус-рівні, плінт підказок на 5 клітин, курсор із прилипанням"}
  - {kind: other, url: "https://purenintendo.com/review-archaica-nintendo-switch/", note: "огляд Switch: кольорові кристали, Lightwell, багатоетапні рівні з платформами, cells і cryptoglyphs"}
  - {kind: other, url: "https://mygamer.com/archaica-the-path-of-light-xbox-one-review", note: "огляд: подовжувачі світла, розміщення лише на окремих плитках, поворот плечовими, камера"}
  - {kind: other, url: "https://opencritic.com/game/4830/archaica-the-path-of-light", note: "зведення оглядів"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Archaica+Path+of+Light+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [beam-tracing, mirror-reflect, tile-rotate, cursor-place, teleport-pair, button-toggle, hidden-under-block, completion-detection, sequential-levels, level-unlock, level-select, world-map, achievements-window, codex-window, game-screen, main-menu, player-camera, +beam-color-mix, +beam-splitter, +color-converter, +multi-beam-target, +allowed-place-cells, +piece-limited-placement, +multi-stage-level, +hint-from-collectibles, +hint-placement-only, +bonus-levels-by-key]
proposes: ["+trigger:beam_hit", "+effect:emit_beam", "+effect:reflect", "+effect:split_beam", "+effect:recolor_beam", "+ui:hint-plinth", "+feature:hint-from-collectibles", "+card:allowed-place-cells", "+card:multi-stage-level", "+card:hint-from-collectibles"]
author: opus
date: 2026-11-09
---

# Archaica: The Path of Light — розстав дзеркала на ізометричній сітці, щоб засвітити всі кристали

## Суть
Класичний пазл «промінь + дзеркала» в ізометричних храмах: з джерела йде промінь світла, гравець переставляє й крутить дзеркала та пристрої, щоб промені потрібних кольорів засвітили всі кристали рівня. Тоді вмикається Lightwell — вихід на наступний рівень. Від Deflektor відрізняється відсутністю часу й ворогів, від Chromatron — тим, що дзеркала стоять лише на дозволених плитках і переміщуються по клітинці, а від обох — пригодницькою оболонкою: збираються підказки, ієрогліфи, ключі до бонус-рівнів.

## Поле і час
- Ізометрична сітка (камеру можна обертати стіками); частина плиток дозволена для розміщення, решта — декорація/перешкоди.
- Деякі рівні багатоетапні: ті самі джерела й дзеркала, але платформи зсуваються, коли відкривається наступна секція.
- Час статичний: промінь перераховується після кожної зміни; ні таймера, ні лічильника ходів.
- 50+ рівнів у п'яти зонах (пустеля, болота, джунглі…).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Джерело світла | source | колір, напрям | випускає промінь |
| Промінь | projectile | колір | іде прямо до перешкоди |
| Дзеркало (кілька видів) | conduit | кут відбиття | відбиває під своїм кутом; пізніше — «кутові» дзеркала з іншим кутом |
| Подовжувач світла (light extender) | conduit | — | продовжує/переносить промінь (?) |
| Конвертер | conduit | колір | змінює колір променя (?) |
| Дільник (divider) | conduit | — | розщеплює промінь на кілька напрямків (?) |
| Телепорт | conduit | пара | промінь входить в один і виходить з іншого |
| Кольоровий кристал | sink | колір | засвічується променем; змішування кольорів має дати потрібний (?) |
| Lightwell | gate | — | вмикається, коли засвічено всі кристали; перехід далі |
| Сенсор-перемикач | switch | — | спрацьовує лише від світла на сенсорі; знімає замок з каменя |
| Камінь із замком / Stone Key | gate | — | відкриває прихований/бонусний набір рівнів |
| Дозволена плитка | terrain | — | лише сюди можна ставити обʼєкти |
| Платформа етапу | terrain | — | зсувається, коли відкрито наступну секцію рівня |
| Білий кристал-підказка (cell) | pickup | 2–3 на рівень | зібрав усі → доступна підказка |
| Ієрогліф / cryptoglyph | pickup | — | відкриває запис в Альманаху (історія світу) |
| Тотем | static | — | показує ачівки; відкриває інфо про новий елемент |
| Курсор | player | — | вибирає обʼєкт, рухає його по клітині, крутить |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `after(move)` або `after(rotate)` → ТО `custom: «перетрасувати всі промені від джерел: дзеркало — відбиття за кутом, телепорт — вихід з пари, дільник — кілька променів, конвертер — новий колір»`.
- КОЛИ `input(select, piece)` → ТО `set_state(piece, selected)`.
- КОЛИ `input(dir, piece)` → ЯКЩО `state(piece, selected) and cell(target, allowed) and free(target)` → ТО `move(piece, dir)`; інакше `block`.
- КОЛИ `input(shoulder, piece)` → ЯКЩО `state(piece, selected)` → ТО `rotate(piece, step)`.
- КОЛИ `custom: «промінь входить у телепорт»` → ТО `teleport(beam, pair)`.
- КОЛИ `custom: «два промені сходяться»` → ТО `custom: «кольори змішуються»` (?).
- КОЛИ `custom: «промінь влучив у кристал»` → ЯКЩО `same(beam, crystal, color)` → ТО `set_state(crystal, lit)`.
- КОЛИ `counter(lit_crystals, ==, all)` → ТО `set_state(lightwell, on)`, `win`, `next_level`.
- КОЛИ `custom: «промінь влучив у сенсор»` → ТО `set_state(lock, open)`, `unlock(hidden_levels)`.
- КОЛИ `custom: «секцію рівня розвʼязано»` → ЯКЩО `count(stages_left, >, 0)` → ТО `custom: «платформи зсуваються, відкривається наступний етап»`.
- КОЛИ `input(click, white_crystal)` → ТО `pickup(cursor, white_crystal)`, `counter(hint_cells, +1)`.
- КОЛИ `counter(hint_cells, ==, all)` → ТО `set_state(hint_plinth, active)`.
- КОЛИ `input(hint)` → ЯКЩО `state(hint_plinth, active) and counter(hint_charges, >, 0)` → ТО `mark(cells_5, mirror_here)`, `counter(hint_charges, -1)`; `custom: «заряди повільно відновлюються»`.
- КОЛИ `input(click, glyph)` → ТО `pickup(cursor, glyph)`, `custom: «запис в Альманаху»`.
- Перемога рівня: усі кристали засвічено → Lightwell · Поразки нема · Рахунку нема (ні таймера, ні лічильника ходів).

## Керування і ввід
- Геймпад (Xbox/Switch): лівий стік — курсор, що прилипає до найближчого обʼєкта; A — вибрати; після вибору стік рухає обʼєкт на одну клітину; плечові кнопки — поворот; обидва стіки — кут камери.
- ПК: мишка (?).
- Курсор потрібен і для збирання білих кристалів та ієрогліфів, захованих у декораціях.

## Вікна, меню, HUD
- `main-menu` → `map-window`/`level-select` по зонах; не показує, чи зібрано кристали-підказки рівня.
- `game-screen`: ізометричний храм, обʼєкти без підсвітки (огляди скаржаться), `hint-plinth` з підсвіткою 5 клітин.
- `codex-window` — Альманах: тексти ієрогліфів (переглянути пізніше не можна — за оглядом).
- `achievements-window` — Тотем: 12 досягнень.
- Переходи: level-select → game-screen → (Lightwell) → наступний рівень; сенсор/ключ → прихований набір рівнів.

## Фічі поза полем
- `levels-sequential` + `level-unlock`: наступний рівень лише після попереднього; 5 зон.
- `collectibles`: білі кристали (підказки), ієрогліфи (історія), Stone Keys (поодинці або парами) → бонусні важчі рівні; частина тем відкривається лише після найважчих рівнів.
- `hint` за зібране: плінт підсвічує 5 клітин, де має стояти дзеркало, але не яке; 3 заряди, далі повільне відновлення.
- Steam: `achievements`, `cloud-save`, 8 мов з озвучкою.

## Варіації й родичі
- У сімʼї: `deflektor.md`, `chromatron.md` (кольори, дільник, змішування), `laser-tank.md`, `khet.md`, `solas-128.md` (імпульси в такт, звʼязані кімнати).
- Ізометричні «light puzzle» з оболонкою храму — популярна мобільна ніша (?).
- **Осі варіацій:** де стоять дзеркала — будь-де / лише дозволені плитки · хід — переставити миттєво / зсунути на клітину · ціль — один приймач / усі кристали / кольорові кристали · підказка — повний розвʼязок / «де» без «що» / заробити збиранням.

## Цікавинки для курсу
- Трасування з телепортами, дільником і конвертером кольору одним циклом (черга променів) — 🥉.
- Маска дозволених клітин як окремий шар рівня (як вежі TD) — 🌱.
- Багатоетапний рівень: розвʼязок секції змінює поле наступної, обʼєкти лишаються — 📎.
- Підказка, яку треба заробити збиранням, з зарядами, що відновлюються — 📎.
- Ізометричний рендер квадратної сітки + обертання камери (перерахунок порядку малювання) — 🥈.
- Курсор, що прилипає до найближчого обʼєкта (і чому це заважає) — 🌱.

## Мапа на каталог
- Є: `beam-tracing` · `mirror-reflect` · `tile-rotate` · `cursor-place` · `teleport-pair` · `button-toggle` (сенсор) · `hidden-under-block` (приховані збиранки) · `completion-detection` · `sequential-levels` · `level-unlock` · `level-select` · `world-map` (5 зон) · `achievements-window` · `codex-window` (Альманах) · `game-screen` · `main-menu` · `player-camera`.
- **Нема** → пропозиції карток:
  - `+allowed-place-cells` «Ставити лише на дозволені плитки» · entities/legality · 🌱.
  - `+piece-limited-placement` «Обʼєкт рухається по клітині, не стрибає» · interface/input · 🌱.
  - `+multi-stage-level` «Рівень з етапами» · levels/progression · 📎.
  - `+hint-from-collectibles` «Підказка за зібрані предмети» · game-logic/difficulty · 📎.
  - `+hint-placement-only` «Підказка: де, а не що» · 📎 (як у SOLAS 128).
  - `+bonus-levels-by-key` «Бонус-рівні за ключі» · levels/progression · 🌱.
  - `+color-converter` «Пристрій змінює колір променя» · entities/interact · 🌱; `+beam-splitter`, `+beam-color-mix`, `+multi-beam-target` — як у Chromatron.

## Пропозиції до словників
- `+trigger:beam_hit(a)` — промінь влучив у кристал/сенсор (Deflektor, Chromatron, SOLAS 128).
- `+effect:emit_beam`, `+effect:reflect`, `+effect:split_beam`, `+effect:recolor_beam` — трасування, відбиття, розщеплення, зміна кольору.
- `+ui:hint-plinth` — підказка-зона з N підсвіченими клітинами.
- `+feature:hint-from-collectibles` — підказки купуються збиранням на рівні.

## Джерела
- ⭐ [Steam: Archaica](https://store.steampowered.com/app/550590/Archaica_The_Path_of_Light/) — Two Mammoths, 08.09.2017; дзеркала й кольорове скло, засвітити всі кристали, ієрогліфи, ачівки, хмара, мови.
- [TheXboxHub](https://www.thexboxhub.com/archaica-the-path-of-light-review/) — конвертер, дільник, змішування, сенсор-перемикачі, 50+ рівнів у 5 зонах, підказка на 5 клітин, Альманах, 12 ачівок.
- [Xbox Tavern](https://www.xboxtavern.com/archaica-the-path-of-light-review/) — телепорти, Stone Keys, плінт підказок із зарядами, керування.
- [Pure Nintendo](https://purenintendo.com/review-archaica-nintendo-switch/) — кольорові кристали, Lightwell, етапи з платформами, cells і cryptoglyphs.
- [MyGamer](https://mygamer.com/archaica-the-path-of-light-xbox-one-review) — подовжувачі світла, дозволені плитки, поворот плечовими, камера.
- [OpenCritic](https://opencritic.com/game/4830/archaica-the-path-of-light) · YouTube: пошук «Archaica Path of Light gameplay».

## Непевне
- (?) Поведінка конвертера, дільника й «light extender» — названі в оглядах без пояснень.
- (?) Модель змішування кольорів і чи кристал вимагає точного кольору.
- (?) «Power boosters» з одного огляду (сніпет пошуку) — сторінку не відкрито.
- (?) Кількість положень дзеркала при повороті (90° чи 45°).
- (?) Керування мишею на ПК; дати виходу Xbox One і Switch.
- (?) Огляди розходяться щодо підказок: «таргетовані й практичні» (Steam) проти «дрібний некорисний текст» (MyGamer) — можливо, різні системи.
