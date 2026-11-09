---
title: Chromatron (1–5)
slug: chromatron
aka: [Chromatron 2, "Chromatron 3: Geometry", "Chromatron 4: Less is Not More", Chromatron 5]
family: connect-rotate
also: []
klass: cursor
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: none
  goal: state
year: 2002
platforms: [PC (Windows), Mac OS X]
links:
  - {kind: other, url: "https://www.homeoftheunderdogs.net/game.php?id=3504", best: true, note: "огляд Chromatron 2: дзеркала, розщеплювач, що й зливає, кольорові цілі-вертушки, нові пристрої другої частини"}
  - {kind: official, url: "https://silverspaceship.com/chromatron/", note: "офіційна сторінка Sean Barrett: частини 1–4 безкоштовно, 4×50 рівнів, рестарт на r, копіювання розвʼязку як рядка"}
  - {kind: other, url: "https://alternativeto.net/software/chromatron/about", note: "коротко: дзеркала спрямовують лазери на цілі; Windows/Mac, безкоштовно"}
  - {kind: play, url: "https://hkmg.itch.io/quantum-mirrorcle", note: "PuzzleScript-демейк Chromatron: дзеркала, розщеплювач, доплер, призма, комплементор, щілина, квантовий тунель"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Chromatron+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [beam-tracing, mirror-reflect, drag-drop-piece, inventory, orientation-state, impassable-cells, completion-detection, satisfy-constraints, sequential-levels, level-unlock, level-select, puzzle-select, restart-level, state-string, save-progress, game-screen, main-menu, end-screen, +tile-rotate-45, +beam-color-mix, +beam-splitter, +color-filter, +color-complement, +entangled-pair, +fixed-vs-movable-piece, +multi-beam-target]
proposes: ["+trigger:beam_hit", "+effect:reflect", "+effect:emit_beam", "+effect:split_beam", "+effect:recolor_beam", "+cond:beam_color", "+ui:piece-tray", "+feature:solution-code", "+card:beam-color-mix", "+card:beam-splitter", "+card:multi-beam-target", "+card:fixed-vs-movable-piece"]
author: opus
date: 2026-11-09
---

# Chromatron — розстав і поверни оптику так, щоб кольорові промені склались у потрібний колір на кожній цілі

## Суть
На полі стоять нерухомі лазери й цілі-«вертушки» (pinwheels); гравець бере з лотка дзеркала, розщеплювачі, фільтри та інші пристрої, ставить їх у клітини й обертає. Промінь іде прямо, доки не вдариться в пристрій чи стіну; рівень пройдено, коли кожна ціль отримує саме той колір, якого вимагає. Новинка проти класичних лазерних пазлів (Reflections, Deflektor): **колір складається з кількох променів** за правилом основних кольорів, а частина цілей вимагає одночасно кількох променів. Автор — Sean Barrett (Silver Spaceship Software); частини 1–4 безкоштовні, по 50 рівнів.

## Поле і час
- Квадратна сітка зі стінами; промінь іде по прямих, а пристрої повертаються кроком, що дає косі напрямки (8 напрямків, ?).
- Два шари: пристрій у клітині + промені, що проходять крізь клітину (можуть перетинатись, ?).
- Час статичний: промені перераховуються миттєво після кожної зміни; таймера й рахунку нема.
- Поле вміщається на екран, камери нема.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Лазер | source | колір; напрямок | нерухомий; безперервно випускає промінь свого кольору |
| Ціль-вертушка | sink | потрібний колір; іноді кількість променів | світиться, коли сума кольорів, що в неї влучили, = вимога |
| Дзеркало | conduit | кут; кілька типів | відбиває промінь; ставиться з лотка й обертається |
| Розщеплювач | conduit | кут | промінь під кутом ділиться на два; два промені зливає в один |
| Призма | conduit | — | розкладає змішаний колір на складові (?) |
| Фільтр | conduit | колір | пропускає лише свою складову (?) |
| Мульти-фільтр (Ch2) | conduit | — | назва з огляду; поведінка не описана (?) |
| Комплементор (Ch2) | conduit | — | інвертує колір променя (за демейком, ?) |
| Твістер (Ch2) | conduit | — | назва з огляду; поведінка не описана (?) |
| Квантовий танглер | conduit | пара/група | є з першої частини, 8 рівнів Ch2; переносить промінь між повʼязаними пристроями (?) |
| Стіна | static | — | поглинає промінь, не займається пристроєм |
| Нерухомий пристрій | static | тип, кут | частина задачі: не можна взяти чи повернути (?) |
| Лоток пристроїв | supply | набір на рівень | звідки беруть пристрої; рівень видає їх обмежено (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag, piece, cell)` → ЯКЩО `free(cell)` and `not state(piece, fixed)` → ТО `place(piece, cell)`.
- КОЛИ `input(drag, piece, tray)` → ТО `custom: «пристрій повертається в лоток»`.
- КОЛИ `input(rotate, piece)` → ЯКЩО `not state(piece, fixed)` → ТО `rotate(piece, 45)` (?).
- КОЛИ `after(place|rotate)` → ТО `custom: «перерахувати всі промені від кожного лазера»` (+effect:emit_beam).
- КОЛИ `custom: «промінь влучив у дзеркало»` (+trigger:beam_hit) → ТО `custom: «відбити промінь за кутом дзеркала»` (+effect:reflect).
- КОЛИ `custom: «промінь влучив у розщеплювач під кутом»` → ТО `custom: «два промені: прямо і відбитий»` (+effect:split_beam).
- КОЛИ `custom: «два промені зустрілись на розщеплювачі»` → ТО `custom: «злити в один із сумою кольорів»`.
- КОЛИ `custom: «промінь проходить фільтр/комплементор»` → ТО `custom: «змінити колір променя»` (+effect:recolor_beam, ?).
- КОЛИ `custom: «промінь влучив у стіну»` → ТО `block`.
- КОЛИ `custom: «промінь влучив у ціль»` → ЯКЩО `custom: «сума кольорів променів = колір цілі»` (+cond:beam_color) → ТО `set_state(target, lit)`; інакше `clear_state(target, lit)`.
- КОЛИ `custom: «ціль вимагає N променів»` → ЯКЩО `count(beams_on(target), >=, n)` → ТО `set_state(target, lit)`.
- КОЛИ `all_constraints_met` (усі цілі світяться) → ТО `win`, `unlock(next_level)`.
- КОЛИ `input(key, r)` → ТО `restart`.
- Перемога: усі цілі світяться потрібним кольором · Поразка: нема · Рахунок: нема.

## Керування і ввід
- Миша: перетягнути пристрій із лотка на клітину; повернути — клік/правий клік по пристрою (?).
- Перетягнути назад у лоток — зняти пристрій.
- `r` — рестарт рівня (на офіційній сторінці названо прихованою фічею).
- Ctrl-C / Ctrl-V (Cmd на Mac, або меню Edit) — скопіювати/вставити розвʼязок рівня як текстовий рядок.

## Вікна, меню, HUD
- `game-screen`: поле, лазери й цілі, `piece-tray` (лоток пристроїв), підсвічені цілі, що вже горять.
- `level-select` / `puzzle-select`: 50 рівнів частини з позначкою розвʼязаних (?).
- `end-screen`: короткий екран «рівень пройдено» → наступний (?).
- `main-menu` мінімальний; Mac-версія має меню Edit для копіювання розвʼязку.
- HUD: `remaining-counter` цілей (?) — у грі мінімалістичний інтерфейс, лічильників ходів нема.
- Переходи: main-menu → level-select → game-screen → end-screen → наступний рівень.

## Фічі поза полем
- `levels-sequential` / `level-unlock`: 50 рівнів на частину, 200 у збірці 1–4.
- `autosave`: прогрес у файлі `chroma.dat` (Windows) або в Library/Preferences (Mac).
- `share-code`: розвʼязок рівня копіюється як рядок і вставляється назад.
- `restart-level`.
- Chromatron 5 — комерційна частина з редактором рівнів (?).

## Варіації й родичі
- Натхнення — Reflections (за словами автора); родичі — Aargon Deluxe, Laser Light, а в корпусі [deflektor](deflektor.md), [laser-tank](laser-tank.md), [khet](khet.md).
- Підсерії: 3 «Geometry», 4 «Less is Not More» — нові набори рівнів; 2 додає твістер, комплементор, мульти-фільтр.
- Демейки: Quantum Mirrorcle (PuzzleScript) — доплер, призма, комплементор, щілина, квантовий тунель.
- Осі варіацій: **промінь: один колір / адитивне змішування RGB** · **пристрої: дано на полі / лоток для розстановки** · **ціль: будь-який промінь / точний колір / N променів** · **кути: 90° / 45°**.

## Цікавинки для курсу
- Трасування променя по сітці з 8 напрямками й відбиттям за кутом дзеркала (таблиця «кут × вхідний напрям → вихідний») — 🥉.
- Колір як 3-бітна маска RGB: злиття = OR, фільтр = AND, комплементор = XOR 111 — 📎.
- Розщеплювач = промінь роздвоюється: обхід у ширину з чергою променів і захистом від нескінченних петель (visited по (клітина, напрям)) — 🥉.
- Цілі з вимогою «N променів» — лічильник влучень на ціль — 🌱.
- Розвʼязок як рядок (серіалізація розстановки пристроїв і їхніх кутів) — 📎.
- Розвʼязувач рівня перебором розстановок із лотка — 🥇.

## Мапа на каталог
- Є: `beam-tracing` (промінь) · `mirror-reflect` (дзеркала) · `drag-drop-piece` (з лотка на поле) · `inventory` (лоток) · `orientation-state` (кут пристрою) · `impassable-cells` (стіни) · `completion-detection` / `satisfy-constraints` (усі цілі горять) · `sequential-levels` · `level-unlock` · `level-select` · `puzzle-select` · `restart-level` · `state-string` (розвʼязок як рядок) · `save-progress` · `game-screen` · `main-menu` · `end-screen`.
- **Нема** → пропозиції карток:
  - `+tile-rotate-45` «Поворот кроком 45°» · entities/state · 🌱 — варіант `tile-rotate` з 8 положеннями.
  - `+beam-color-mix` «Адитивне змішування кольорів променів» · entities/interact · 📎 · слоти {colors: RGB}.
  - `+beam-splitter` «Розщеплювач: один промінь → два, два → один» · entities/interact · 🥉.
  - `+color-filter` «Фільтр кольору» · entities/interact · 🌱.
  - `+color-complement` «Інверсія кольору» · entities/interact · 🌱.
  - `+entangled-pair` «Повʼязані пристрої передають промінь» · entities/interact · 📎 (як `teleport-pair` для променя).
  - `+fixed-vs-movable-piece` «Нерухомі й розставлювані пристрої» · entities/legality · 🌱.
  - `+multi-beam-target` «Ціль потребує N променів/точного кольору» · game-logic/win · 🌱.

## Пропозиції до словників
- `+trigger:beam_hit(a)` — промінь торкнувся сутності.
- `+effect:reflect` — змінити напрям променя за кутом; `+effect:emit_beam` — перерахувати промінь від джерела; `+effect:split_beam` — роздвоїти промінь; `+effect:recolor_beam(op)` — фільтр/інверсія кольору.
- `+cond:beam_color(target, c)` — сума кольорів на цілі дорівнює c.
- `+ui:piece-tray` — лоток пристроїв рівня, з якого перетягують на поле.
- `+feature:solution-code` — копіювати/вставити розвʼязок як текст (вужче за `share-code`).

## Джерела
- ⭐ [Home of the Underdogs: Chromatron 2](https://www.homeoftheunderdogs.net/game.php?id=3504) — дзеркала, розщеплювач (ділить і зливає), цілі з кількома променями й кольором, нові пристрої Ch2, квантовий танглер, 50 рівнів, 2002.
- [Silver Spaceship Software: Chromatron](https://silverspaceship.com/chromatron/) — частини 1–4, 200 рівнів, рестарт на r, копіювання розвʼязку, збереження, натхнення Reflections.
- [AlternativeTo](https://alternativeto.net/software/chromatron/about) — опис ядра, платформи.
- [Quantum Mirrorcle (itch)](https://hkmg.itch.io/quantum-mirrorcle) — демейк із поясненнями пристроїв.

## Непевне
- (?) Точна поведінка призми, фільтра, мульти-фільтра, твістера, квантового танглера — у відкритих джерелах лише назви; опис за памʼяттю й за демейком.
- (?) Крок повороту 45° і 8 напрямків променя — за памʼяттю.
- (?) Chromatron 5: офіційна сторінка перелічує лише 1–4; існування комерційної 5-ї частини з редактором — з памʼяті, сторінку не знайдено (404).
- (?) Рік першої частини: огляд Ch2 дає 2002; дата Chromatron 1 не звірена.
- (?) Чи видає лоток обмежену кількість кожного пристрою і чи є нерухомі пристрої — за памʼяттю.
- (?) Вигляд меню й екрана перемоги не бачив.
