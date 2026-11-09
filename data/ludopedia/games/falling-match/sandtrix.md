---
title: Sandtrix (Sandtrix+)
slug: sandtrix
aka: [Sandtrix+, Sand Tetris, Setris]
family: falling-match
also: [dig-gravity]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: score
year: 2023
platforms: [Windows, macOS, Linux, Steam Deck, web, mobile web]
links:
  - {kind: itch, url: "https://msky-dev.itch.io/sandtrix", best: true, note: "опис «Blocks turn into sand», порівняння Sandtrix / Sandtrix+, коментарі про правило зникнення, завантаження"}
  - {kind: other, url: "https://msky-dev.itch.io/sandtrix/devlog", note: "31 запис changelog: режими, комбометр, мішок кольорів, Custom, Stacks, налаштування"}
  - {kind: play, url: "https://www.crazygames.com/game/sandtrix", note: "грати в браузері; розкладка клавіш, 3 режими, 3 складності, очки за піксель, комбо до x10"}
  - {kind: official, url: "https://sandtrix.net", note: "сайт автора: версії, таблиця 3/6 режимів, 1/5 колірних режимів, 1/16 тем, 0/14 ефектів"}
  - {kind: steam, url: "https://store.steampowered.com/app/2546310/Sandtrix/", note: "Sandtrix+ (31.08.2023); безкоштовний Sandtrix на Steam з 26.01.2024"}
  - {kind: other, url: "https://phaser.io/news/2024/10/setris", note: "Setris (Rosebud AI + Phaser, 2024) — окремий клон із тим самим правилом «колір від краю до краю»"}
  - {kind: play, url: "https://play.rosebud.ai/games/ed0d3974-3d9b-4af5-a634-a7f75506e7b9", note: "грати в Setris (лінк зі статті Phaser)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=sandtrix+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [gravity-fall, cell-transform, connectivity-check, combo-multiplier, event-points, progress-acceleration, time-out, difficulty-levels, difficulty-select, mode-select, next-queue, popup-text, score-records, game-pause, pause-menu, end-screen, main-menu, settings-window, volume-control, background-music, theme-select, field-scaling, keyboard-controls, swipe-gestures, save-progress, +falling-sand-cell, +piece-to-sand, +edge-to-edge-path-clear, +bag-randomizer, +combo-timer-meter, +colorblind-palette, +custom-game-mode, +star-unlocks]
proposes: ["+effect:crumble", "+cond:spans_edges", "+feature:effects-unlock", "+window:custom-game-setup"]
author: opus
date: 2026-11-09
---

# Sandtrix — тетроміно падає і розсипається піском; зникає одноколірна пляма, що зʼєднала ліву стінку з правою

## Суть
Падаюча фігура керується як у Tetris (зсув, поворот, прискорене падіння), але щойно вона приземлилась, то **розсипається на піщинки** — окремі пікселі свого кольору, що далі сиплються й осідають купою. Повних рядів нема: зникає **звʼязна область піску одного кольору, що торкається і лівого, і правого краю поля** («connecting the same color across the screen»). Очки — по 1 за кожен стертий піксель, множник комбо до x10, якщо зчищення йдуть одне за одним. Гра вільна (Sandtrix), розширена версія — платна (Sandtrix+); Setris (2024) — окремий браузерний клон з тим самим правилом.

## Поле і час
- Вертикальний колодязь: стек — піксельна сітка піску (одна піщинка = одна клітина), активна фігура — тетроміно, кожна клітина якого складена з багатьох пікселів (масштаб — (?)).
- Шари: пісок (колір кожної піщинки) + активна фігура + рамка зі стінками (ліва/права — «краї» для правила зникнення) + фон теми (анімація фону вимикається з 3.1).
- Real-time: фігура падає з темпом складності; пісок симулюється щокадру; після приземлення — дуже коротка затримка, потім розсипання (слова автора: «That delay exists but it is very short»).
- Складність Easy — повне поле, нормальна швидкість; Medium і Hard — швидше **і вужче поле** (менше пікселів до протилежної стінки).
- Endless — швидкість росте з часом.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Активна фігура | player | форма-тетроміно, один колір, поворот | падає; ввід зсуває, обертає, прискорює; приземлилась → розсипається |
| Піщинка | tile | колір | падає вниз; осідає купою; частина звʼязної одноколірної області |
| Одноколірна область | zone | множина звʼязних піщинок одного кольору | торкнулась обох стінок → зникає цілком |
| Стінка ліва / права | static | — | межа поля; дві «цілі» для правила звʼязності |
| Верх поля | static | лінія | пісок / фігура досягли — кінець гри |
| Мішок кольорів | spawner | набір кольорів | роздає колір наступній фігурі без довгих серій невдач (з 1.1) |
| Next-превʼю | — (ui `next-piece-preview`) | наступна фігура | показує форму й колір наступної (збільшена з 1.1) |
| Комбометр | — (ui `combo-meter`) | множник x1…x10, таймер «стека» | кожне зчищення в межах таймера підвищує множник |
| Stack (Sandtrix+, режим Stacks) | object | — | знімається зчищенням: звичайне — 1, комбо — кілька (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left|right)` → ЯКЩО `free(cells_beside)` → ТО `move(piece, dir)`; інакше `block`.
- КОЛИ `input(rotate)` → ЯКЩО `free(rotated_cells)` → ТО `rotate(piece, 90)`; напрям і кіки — (?).
- КОЛИ `input(drop)` → ТО `custom: «прискорене падіння фігури (soft чи hard — не підтверджено)»`.
- КОЛИ `timer(fall_rate)` → ЯКЩО `free(below_piece)` → ТО `move(piece, down)`.
- КОЛИ `blocked(piece)` (сіла на пісок або дно) → ТО `custom: «crumble — після короткої затримки фігура стає множиною піщинок свого кольору»`, `spawn_at(next_piece, top)`.
- КОЛИ `tick` → ЯКЩО `free(below)` → ТО `fall(grain)`; інакше ЯКЩО `free(below_diag)` → ТО `move(grain, diag)` — пісок осідає схилом (класичне falling sand; точна поведінка — (?)).
- КОЛИ `tick` → ЯКЩО `connected(same_color_grains)` and `custom: «область торкається лівої і правої стінки»` → ТО `clear(region)`, `score(+1 × pixels × combo)`.
- КОЛИ `after(clear)` → ТО `fall(grains_above)` — пісок «зісковзує на місце» (Setris), може скласти нову перетинку → нове зчищення.
- КОЛИ `after(clear)` → ЯКЩО `timer(combo_window, >, 0)` → ТО `combo(+1)` (максимум x10), `timer(combo_window, start)`; на x10 нові очки додаються до наявного стека x10 (3.0).
- КОЛИ `timer(combo_window, ==, 0)` → ТО `reset_combo`; що вища швидкість гри, то швидше спливає вікно (2.0).
- КОЛИ `custom: «спавн фігури»` → ТО `custom: «колір береться з мішка кольорів»` (форма — випадкова (?)).
- КОЛИ `reach(grain|piece, top)` → ТО `game_over`, `window(end-screen)` з Retry / Menu (з 2.6).
- Endless: КОЛИ `timer(every)` → ТО `speed(piece, +n)`; гра до заповнення поля.
- High Score: КОЛИ `timer(3 min, ==, 0)` → ТО `game_over`; правила інакше як Endless.
- Clear 40: КОЛИ `counter(clears, ≥, 40)` → ТО `win`; часу нема, виклик — не програти.
- КОЛИ `level_start` → ЯКЩО `difficulty(medium|hard)` → ТО `speed(piece, +n)`, `custom: «поле вужче»`.
- Sandtrix+: КОЛИ `game_over` → ЯКЩО `counter(score, ≥, star_threshold)` → ТО `custom: «зірка»`; зірки відкривають теми й ефекти (до 60 зірок з 2.4) (?).
- Перемога: лише Clear 40 · Поразка: пісок дійшов до верху · Рахунок: 1 очко за піксель × комбо.

## Керування і ввід
- Клавіатура: A/D або ←/→ — зсув; W або ↑ — поворот; S або ↓ — падіння; P або Esc — пауза; Enter / ЛКМ — підтвердження в меню.
- Тач (веб, мобільний браузер): тап — поворот, свайп ліворуч/праворуч — зсув.
- Геймпад — будь-який; плечові кнопки підтримуються з 2.7 (?: призначення — поворот).
- Стратегія незвична для Tetris: важливо не «закрити ряд», а **протягнути одноколірну смугу** від стінки до стінки, керуючи, куди сиплеться пісок.

## Вікна, меню, HUD
- `main-menu`: Play → `mode-select` (Endless · High Score · Clear 40; у Sandtrix+ ще Custom, Stacks і ще один (?)) → `difficulty-select` (Easy · Medium · Hard) → `game-screen`.
- `game-screen`: колодязь з піском, активна фігура, `next-piece-preview`, `score`, `combo-meter` (показує час, що лишився поточному стеку очок), `popup-text` очок на зчищенні, `timer-countdown` (High Score), лічильник зчищень (Clear 40).
- `pause-menu` (P / Esc).
- `end-screen`: результат + Retry / Menu; `leaderboard` — локальні рекорди (топ-5 (?)).
- `settings-window`: `volume-sliders`, режим екрана Pixel-Perfect / Fit / Stretch, колірний режим для дальтоніків, вимкнути трясіння екрана, вимкнути спалах фігури, вимкнути анімацію фону, вибір музики (3 треки).
- `skin-select` — окреме вікно вибору теми (Sandtrix+, з 1.8 / 1.2).
- Custom (Sandtrix+): екран налаштування партії — швидкість кроком 10 %, «legacy» чи «fluid» поведінка піску, увімкнути прискорення.

## Фічі поза полем
- Режими: `mode-endless`, `custom: «High Score — 3 хвилини»` (як Ultra), `custom: «Clear 40»` (як Sprint), Sandtrix+ — Custom (`custom-rules`), Stacks.
- `difficulty-presets` (3 рівні; до 1.3 їх було 5).
- Sandtrix+: 5 колірних режимів (зокрема шестиколірний), 16 тем, 14 ефектів, зірки як валюта розблокування (`unlockables`).
- `colorblind-palette` (з 1.4), `screen-shake-toggle`, `animation-toggle`, `music-toggle` / вибір треку, `volume-sliders`, `fullscreen`-подібні режими масштабу.
- Збереження налаштувань і рекордів у портативній теці (`autosave`, 1.5); гра офлайн, без DRM.
- JVM-опції для досвідчених: `-DskipMenu` (одразу в гру), лог партії в CSV, бенчмарк (2.4).

## Варіації й родичі
- Sandtrix (06.2023, itch, HTML5) → Sandtrix+ (31.08.2023, Steam/itch, платна) → безкоштовний Sandtrix на Steam (01.2024) → 3.x (2024–2026). Рушій — libGDX + власний PixelUIEngine автора.
- Setris (2024, Rosebud AI + Phaser) — окремий клон «Sand Tetris»: блоки при посадці «crumble to pieces», зникає «solid stretch of color» від боку до боку, пісок зверху зісковзує.
- Родичі за правилом зникнення: [gunpey.md](gunpey.md) (траса від лівої стінки до правої), Hex (`chess-abstract`: перемога — зʼєднати протилежні краї), [puyo-puyo.md](puyo-puyo.md) (одноколірні звʼязні групи, але за розміром ≥4).
- Родичі за фізикою: falling sand у `dig-gravity` — Sandspiel, Sandboxels, Noita; [tetris.md](tetris.md) — керування фігурою.
- **Осі варіацій**: що лишає фігура (жорсткі клітини — Tetris / окремі блоки, що падають — Puyo / пісок — Sandtrix) · умова зникнення (повний ряд / група ≥N / одноколірна перетинка край–край) · фізика піску (вертикально / схилом / «fluid» з розтіканням) · ширина поля як складність.

## Цікавинки для курсу
- Falling sand на сітці пікселів: падіння вниз, інакше по діагоналі; порядок обходу знизу вгору й випадковий бік — 📎.
- Розсипання фігури: тетроміно → множина піщинок (кожна клітина фігури = k×k пікселів) — 🌱.
- Перевірка «одноколірна область торкається обох стінок»: BFS/flood fill від пікселів лівої стінки по кольору, щокадру — 🥉 (варто union-find або перевірка лише після змін).
- Комбо-вікно з таймером, що швидшає зі швидкістю гри, і стелею x10 — 🌱.
- Мішок кольорів замість чистого random (як 7-bag Tetris) — 🌱.
- Складність як «вужче поле + швидше» — 🌱; Custom-режим з параметрами симуляції — 📎.

## Мапа на каталог
- Є: `gravity-fall` ↔ пісок і фігура · `cell-transform` (найближча: фігура → пісок) · `connectivity-check` ↔ одноколірна звʼязна область · `combo-multiplier` ↔ комбометр x10 · `event-points` ↔ 1 за піксель · `progress-acceleration` ↔ Endless · `time-out` ↔ High Score 3 хв · `difficulty-levels` + `difficulty-select` · `mode-select` · `next-queue` ↔ next-превʼю · `popup-text` ↔ індикатор очок · `score-records` · `game-pause` + `pause-menu` · `end-screen` (Retry/Menu) · `main-menu` · `settings-window` + `volume-control` + `background-music` · `theme-select` (16 тем) · `field-scaling` (Pixel-Perfect/Fit/Stretch) · `keyboard-controls` · `swipe-gestures` · `save-progress`.
- **Нема** → пропозиції карток:
  - `+falling-sand-cell` (повтор TPT/Sandspiel) — пісок як клітина з правилом падіння.
  - `+piece-to-sand` «Фігура розсипається на частинки після посадки» · entities/state · 📎.
  - `+edge-to-edge-path-clear` (повтор Gunpey) — тут не траса, а одноколірна пляма.
  - `+bag-randomizer` (повтор Tetris) — мішок кольорів.
  - `+combo-timer-meter` «Комбо триває, поки не спливло вікно» · game-logic/score · 🌱.
  - `+colorblind-palette` · interface/settings · 🌱 · `+custom-game-mode` «Партія з власними параметрами» · interface/settings · 📎 · `+star-unlocks` «Зірки за рекорди відкривають теми й ефекти» · levels/progression · 🌱.

## Пропозиції до словників
- `+effect:crumble` — сутність розпадається на окремі клітини-частинки, які далі живуть самі (Sandtrix; близько до розпаду пари Puyo) — не `transform`, бо з однієї сутності стає багато.
- `+cond:spans_edges` — звʼязна множина торкається двох протилежних меж поля (Sandtrix, Gunpey, Hex) — уточнення ⏳ `connected`.
- `+feature:effects-unlock` — розблоковувані візуальні ефекти поля окремо від тем (Sandtrix+: 14 ефектів).
- `+window:custom-game-setup` — екран параметрів власної партії: швидкість, фізика, прискорення (Sandtrix+ Custom; ширше за `match-setup`).

## Джерела
- ⭐ [itch.io: Sandtrix](https://msky-dev.itch.io/sandtrix) — опис, порівняння версій, коментарі (правило «колір від краю до краю», затримка перед розсипанням, Custom для повільної гри).
- [itch.io: devlog Sandtrix](https://msky-dev.itch.io/sandtrix/devlog) — версії 1.0–3.1: мішок кольорів і next (1.1), 3 складності й прискорення Endless (1.3), колірний режим (1.4), налаштування (1.5), Custom і шестиколірний (1.8), fluid-пісок і комбо-таймер (2.0), Stacks і зірки (2.4–2.5), Retry (2.6), комбометр x10 (3.0).
- [CrazyGames: Sandtrix](https://www.crazygames.com/game/sandtrix) — керування, режими Endless / High Score / Clear 40, складності, 1 очко за піксель, комбо до 10x, кінець гри.
- [sandtrix.net](https://sandtrix.net) — версії й таблиця вмісту, платформи, рушій.
- [Steam: Sandtrix+](https://store.steampowered.com/app/2546310/Sandtrix/) — дата, опис, офлайн/DRM-free.
- [Phaser News: Setris](https://phaser.io/news/2024/10/setris) — клон: правило «solid stretch of color touch from side to side».

## Непевне
- (?) Звʼязність піщинок — 4- чи 8-сусідство; чи достатньо торкнутися стінки будь-яким пікселем.
- (?) Поведінка піску: лише вниз/діагональ чи з розтіканням («fluid» — опція Custom, «legacy» — стара); розмір піщинки відносно клітини фігури.
- (?) «Drop» на S/↓ — soft чи hard; напрям повороту, кіки, hold — у джерелах нема.
- (?) Кількість кольорів у базовому режимі (ймовірно 4) і скільки фігур у next.
- (?) Як саме працюють «стеки» очок у комбометрі і правила режиму Stacks; шостий режим Sandtrix+ не названо.
- (?) Пороги зірок і що саме вони відкривають; топ-5 рекордів — з changelog «fixed 5th high score not counting».
- (?) Чи може осідання після зчищення дати каскад (ланцюг) з окремими очками — логічно так, джерела не кажуть.
