---
title: Infinity Loop + Net (Tatham)
slug: infinity-loop
family: connect-rotate
also: [pencil-logic]
klass: puzzle
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: setup
  goal: constraints
year: 2015
platforms: [iOS, Android, web, PC]
links:
  - {kind: play, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/net.html", best: true, note: "Net у браузері; правила на 5 рядків під полем"}
  - {kind: official, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/net.html", note: "мануал Net: керування, обгортання, барʼєри, унікальність"}
  - {kind: official, url: "https://apps.apple.com/la/app/infinity-loop-anxiety-relief/id977028266", note: "App Store: опис Infinity Loop, Dark mode, нескінченні рівні"}
  - {kind: official, url: "https://play.google.com/store/apps/details?id=com.balysv.loop", note: "Google Play"}
  - {kind: play, url: "https://poki.com/en/g/infinity-loop-hex", note: "Infinity Loop: Hex у браузері"}
  - {kind: play, url: "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/netslide.html", note: "Netslide — та сама мережа, хід зсувом ряду"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Infinity+Loop+puzzle+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [cell-click, hover-highlight, completion-detection, satisfy-constraints, unique-puzzle-generation, difficulty-levels, field-size-picker, game-settings, level-solver, game-screen, help-window, +tile-rotate, +pipe-connectors, +connectivity-check, +loop-detection, +lock-cell, +wrap-edges, +edge-barrier, +lit-from-source, +inverse-goal-mode, +undo-redo, +endless-levels, +jumble]
proposes: ["+role:conduit", "+role:source", "+trigger:all_constraints_met", "+cond:ports_match", "+cond:connected", "+effect:rotate", "+effect:lock", "+ui:lit-tiles", "+ui:lock-marker", "+feature:mode-zen", "+feature:mode-inverse", "+card:tile-rotate", "+card:connectivity-check", "+card:edge-barrier"]
author: opus
date: 2026-11-02
---

# Infinity Loop і Net — поверни кожну плитку так, щоб усі зʼєднання зійшлися

## Суть
На полі — плитки з відрізками ліній до сторін (1–4 «конектори»); гравець лише обертає їх на місці. **Infinity Loop** (мобільна, 2015): мета — щоб кожен конектор стикувався з конектором сусіда, утворивши замкнені фігури; ніякого часу, нескінченні рівні, «дзен». **Net** (Simon Tatham): та сама плитка-механіка, але мета суворіша — одна звʼязна мережа **без циклів** (дерево) від центральної плитки-джерела, з варіантом обгортання країв і барʼєрами. Ядро — локальні обмеження портів, що складаються в глобальну властивість графа.

## Поле і час
- Квадратна сітка W×H (Net — довільний розмір у налаштуваннях); Infinity Loop: Hex — гексагональна (6 сторін, поворот на 60°). Один шар: плитки; Net додає барʼєри на ребрах між клітинами.
- Net «Walls wrap around»: поле — тор, конектор на лівому краю стикується з правим краєм.
- Час статичний: хід = поворот однієї плитки; таймера нема (Infinity Loop прямо подає «без тиску часу»).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Кінцівка (1 конектор) | conduit (custom) | орієнтація 0–3 | у Net — «лампочка»-термінал; обертається на 90° |
| Пряма (2 протилежні) | conduit | 2 орієнтації (різні) | обертання на 180° її не змінює |
| Коліно (2 сусідні) | conduit | 4 орієнтації | — |
| Трійник (3) | conduit | 4 орієнтації | — |
| Хрест (4) | conduit | 1 орієнтація | обертання нічого не змінює (у Net хрестів нема — дерево (?)) |
| Порожня клітина | static | — | без конекторів (Infinity Loop) |
| Центральна плитка-джерело | source (custom) | позиція (Ctrl+стрілки) | у Net від неї «світяться» підключені плитки |
| Барʼєр | static | ребро між двома клітинами | забороняє зʼєднання через це ребро; працює як підказка |
| Замок (lock) | mark | на плитці | заблокована плитка не обертається (Net) |
| Гекс-плитки | conduit | 6 сторін | Infinity Loop: Hex |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(tap, tile)` → ЯКЩО `not state(tile, locked)` → ТО `rotate(tile, 90)` (Infinity Loop — за годинниковою; Net: ЛКМ — проти, ПКМ — за, F — на 180°).
- КОЛИ `input(lock, tile)` → ТО `set_state(tile, locked, toggle)` (Net).
- КОЛИ `after(rotate)` → ТО `custom: «перерахувати, які плитки звʼязані з джерелом»` → `mark(lit)` на них (Net).
- Infinity Loop, перемога: КОЛИ `all_constraints_met` = для кожного конектора `ports_match(tile, neighbour)` (жодного «висячого» кінця) → ТО `win`, `next_level`; кількість фігур не важлива, кожна — замкнена.
- Net, перемога: КОЛИ `count(lit, ==, all_tiles)` and `not pattern(loop_closed)` → ТО `win` (звʼязна мережа без циклів, кожен конектор має пару).
- КОЛИ `pattern(loop_closed)` → ТО `custom: «цикл підсвічується як помилка»` (налаштування: завжди / лише якщо всі плитки циклу заблоковані — щоб не підказувати).
- КОЛИ `contact(connector, barrier)` → ТО `custom: «стик через барʼєр неможливий»` — такий конектор лишається висячим.
- КОЛИ `edge(connector)` → ЯКЩО `mode(wrap)` → ТО `wrap` (стикується з протилежним краєм); інакше — висячий.
- Dark mode (Infinity Loop): КОЛИ `custom: «жоден конектор не стикується з жодним»` → ТО `win` — інверсія мети.
- Неоднозначність: Infinity Loop приймає будь-яке розвʼязання, що задовольняє стики (перевірка локальна); Net за замовчуванням генерує пазл з **єдиним** розвʼязком («Ensure unique solution»), вимкнувши — отримаєш неоднозначні пазли.
- Поразки нема; рахунку нема (Net рахує ходи (?)).

## Керування і ввід
- Infinity Loop: тап по плитці = поворот на 90°; нічого більше.
- Net: ЛКМ/`A` — проти годинникової, ПКМ/`D` — за, `F` — 180°; середня кнопка / Shift+клік / `S` — замок; стрілки — курсор; Shift+стрілки — зсунути все поле (на торі — переносить «початок координат»); Ctrl+стрілки — пересунути джерело; `J` — перемішати всі незаблоковані плитки.
- Плюс спільне Tatham: `U`/`R` — undo/redo, `N` — новий пазл, Solve, Restart.

## Вікна, меню, HUD
- `game-screen` (Infinity Loop): лише поле; після розвʼязання плитки «зливаються» в картинку й можна зробити фото, далі — наступний рівень (номер рівня вгорі).
- `settings-window` (Infinity Loop): кнопка внизу геймплею — звук, перехід у Dark mode, звʼязок прогресу з акаунтом.
- `custom-window` Playground (з 2019) і `daily-window` Daily Challenges з трофеями (з 2020).
- `game-screen` (Net): поле зі `lit-tiles` (підсвічені звʼязані з джерелом), `lock-marker`, `conflict-highlight` для циклів, статус-рядок (?).
- Меню Net: Game (New, Restart, Undo, Redo, Solve, Specific/Random seed, Preferences) · Type (пресети розмірів, з обгортанням, Custom… → `settings-window`: Width, Height, Walls wrap around, Barrier probability 0.0–1.0, Ensure unique solution) · Help.
- Переходи: розвʼязання → анімація завершення → новий пазл (Infinity Loop автоматично; Net — по `N`).

## Фічі поза полем
- `mode-endless` / `mode-zen` (Infinity Loop: «нескінченні» рівні, складність навмисно не росте; без таймера).
- `mode-daily`, `achievements` (трофеї), `cloud-save` (прогрес через акаунт), платне «Remove Ads & Unlock Dark mode».
- Net: `custom-difficulty` (розмір, щільність барʼєрів, тор), `seed-input`/`seed-display` (ідентифікатор гри), `undo`/`redo` ∞, `show-solution`, `restart-level`, `jumble`.
- Барʼєри генеруються незалежно від решти: той самий seed з іншою ймовірністю барʼєрів — та сама мережа, інші підказки.

## Варіації й родичі
- Infinity Loop: Hex, Infinity Loop: Energy (?), Blueprints (?); численні мобільні «Loop/Energy/Plumber».
- Tatham Netslide — та сама мережа, хід — тороїдальний зсув ряду замість обертання; Twiddle — обертання блоку k×k.
- Pipe Mania — плитки не обертаються, а приходять із черги.
- Осі варіацій: **мета: усі стики замкнені / одне дерево / одна мережа з джерелом / жодного стику (Dark)** · **сітка: квадрат / гекс / тор** · **хід: обертання / зсув ряду / обмін** · **підказки: барʼєри / заблоковані плитки / нічого**.

## Цікавинки для курсу
- Плитка як 4-бітна маска портів, поворот = циклічний зсув бітів, перевірка стику з сусідом — 🌱.
- Перевірка «усі конектори мають пару» (локальна) — 🌱; «одна мережа без циклів» (BFS/DFS від джерела + пошук циклу) — 🥉.
- Підсвітка звʼязаних з джерелом після кожного ходу — 📎 (flood fill на графі портів).
- Генерація: випадкове кістякове дерево на сітці (Prim/DFS) → розкласти плитки → перемішати поворотами — 🥈; з гарантією **єдиного** розвʼязку — 👑 (картка `unique-puzzle-generation`).
- Тор + барʼєри як налаштування того самого генератора — 📎.
- Інверсний режим (Dark mode) — та сама перевірка з протилежним знаком — 🌱.
- Автосолвер обертань (propagation обмежень портів) — 🥇.

## Мапа на каталог
- Є: `cell-click` · `hover-highlight` · `completion-detection` · `satisfy-constraints` · `unique-puzzle-generation` (Net) · `difficulty-levels` / `field-size-picker` / `game-settings` (Custom-налаштування Net) · `level-solver` (Solve) · `game-screen` · `help-window`.
- **Нема** → пропозиції карток:
  - `+tile-rotate` «Обертання плитки на місці» · entities/state · 🌱 · слоти {step: 90|60, dir: cw|ccw|both}.
  - `+pipe-connectors` «Плитка-зʼєднувач з портами» · entities/state · 🌱.
  - `+connectivity-check` «Звʼязність мережі» · game-logic/constraints · 🥉 · слоти {goal: all_matched|single_tree|from_source}.
  - `+loop-detection` «Виявлення циклу» · game-logic/constraints · 📎.
  - `+lit-from-source` «Підсвітка підключених до джерела» · interface/hud · 📎.
  - `+lock-cell` «Замок на клітині» · interface/input · 🌱.
  - `+wrap-edges` «Обгортання країв (тор)» · entities/move · 📎.
  - `+edge-barrier` «Барʼєр на ребрі між клітинами» · entities/legality · 🌱.
  - `+inverse-goal-mode` «Інверсна мета» · game-logic/win · 🌱.
  - `+undo-redo` «Undo/redo ходів гравця» · game-logic · 📎 (у каталозі є лише `editor-undo`).
  - `+endless-levels` «Нескінченні згенеровані рівні» · levels/generation · 🥉.
  - `+jumble` «Перемішати незаблоковані» · interface/input · 🌱.

## Пропозиції до словників
- `+role:conduit` — плитка, що проводить зʼєднання (труба, лінія); `+role:source` — джерело, від якого рахується звʼязність.
- `+trigger:all_constraints_met` уже ⏳ — тут ядро перемоги.
- `+cond:ports_match(a, b)` — конектори сусідів стикуються; `+cond:connected(a, source)` — плитка в компоненті джерела.
- `+effect:rotate` уже ⏳ (зустрівся знову: Infinity Loop, Net, Deflektor); `+effect:lock` — заборонити зміну клітини гравцем.
- `+ui:lit-tiles` — підсвітка підключених; `+ui:lock-marker` — позначка заблокованої плитки.
- `+feature:mode-zen` ⏳ підтверджується; `+feature:mode-inverse` — режим з протилежною метою (Dark mode).
- `+card:tile-rotate`, `+card:connectivity-check`, `+card:edge-barrier` — див. вище.

## Джерела
- ⭐ [Net у браузері (Tatham)](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/net.html) — грати одразу; правила, керування, варіант з обгортанням.
- [Мануал Net](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/doc/net.html) — повне керування (lock, jumble, Shift/Ctrl+стрілки), параметри: Walls wrap around, Barrier probability, Ensure unique solution, налаштування підсвітки циклів.
- [App Store: Infinity Loop](https://apps.apple.com/la/app/infinity-loop-anxiety-relief/id977028266) — опис мети, Dark mode, «нескінченні» рівні, Playground (2019), Daily Challenges (2020), автори.
- [Google Play: Infinity Loop](https://play.google.com/store/apps/details?id=com.balysv.loop) — Android-версія.
- [Infinity Loop: Hex на Poki](https://poki.com/en/g/infinity-loop-hex) — гекс-варіант у браузері.
- [Netslide](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/netslide.html) — родич зі зсувом рядів.

## Непевне
- (?) Рік Infinity Loop 2015 — з черги куратора; App Store показує історію лише з 2017.
- (?) Напрям повороту в Infinity Loop (за годинниковою) — з памʼяті.
- (?) Чи генерує Net хрести (4 конектори) — у дереві можливі, але за памʼяттю рідкісні/відсутні.
- (?) Статус-рядок Net з лічильником активних плиток / ходів — не перевірено.
- (?) Infinity Loop: Energy і Blueprints — назви з памʼяті й черги, механіку не перевірено (Energy — «живлення від джерела до лампочок»).
