---
title: Changes
slug: changes
aka: [Changes (Et Al Games)]
family: thinky
also: [push-slide, build-sim]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2021
platforms: [PC (Windows)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1654920/Changes/", best: true, note: "штовхаєш клітини, поле живе за трьома правилами (народження / смерть / виживання за кількістю живих сусідів) і змінюється з кожним ходом; undo, 100+ рівнів, 8 експозицій, без замкнених рівнів; Et Al Games, 12.10.2021"}
  - {kind: official, url: "https://etalgames.com/changes.html", note: "сторінка автора: «interactive version of Conway's Game of Life», експозиції, вірші й коментарі, динамічний саундтрек; назви скріншотів (overworld, glider gun, blinker kill…)"}
  - {kind: itch, url: "https://etalgames.itch.io/changes", note: "та сама гра: 100+ рівнів у 8 світах, усе відкрито від старту, Windows"}
  - {kind: other, url: "https://steamcommunity.com/app/1654920/discussions/0/4477133359550459235/", note: "обговорення Steam: рівень = стартова і цільова розстановка; клітина гравця не жива, не рахується сусідом, лише штовхає"}
  - {kind: other, url: "https://steamcommunity.com/app/1654920/discussions/0/4477133359562479522/", note: "відповідь розробника: стандартний Conway's Life + імунна клітина гравця + одне додаткове правило в пізніх рівнях"}
  - {kind: youtube, url: "https://www.youtube.com/watch?v=E505zmvaJKM", note: "«Changes: Indie Dev Postmortem» — доповідь автора (зміст не переглянуто)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Changes+Et+Al+Games+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [move-4dir, move-by-input, keyboard-controls, push-object, undo-redo, world-map, background-music, sound-effects, game-screen, +cellular-automaton-rule, +goal-state-check, +immune-avatar, +reactive-music, +hub-world, +open-progression]
proposes: ["+card:immune-avatar", "+card:reactive-music", "+feature:open-progression", "+ui:goal-overlay"]
author: opus
date: 2026-11-09
---

# Changes — Sokoban на полі Conway's Life: штовхнув клітину, і все поле прожило ще одне покоління

## Суть
Рівень — сітка з живими клітинами («living stones»), яка після **кожного ходу** гравця робить один крок стандартного Conway's Game of Life. Гравець — окрема клітина, імунна до правил: вона не жива, не рахується сусідом і вміє лише штовхати живі клітини. Мета рівня — довести поле від стартової розстановки до заданої цільової. Ядро — передбачити, як один зсув однієї клітини розгойдає всю колонію (ланцюгові реакції, «вибухи» невдалих спроб); 100+ рівнів у 8 експозиціях-«музеї» з віршами, історією Life і коментарями автора.

## Поле і час
- Квадратна сітка клітин, сусідство — 8 клітин довкола (Moore, стандарт Conway's Life).
- Хід = крок гравця (з поштовхом або без) → один крок покоління для всього поля; без вводу поле стоїть (`time: turn`).
- Оновлення синхронне: усі клітини рахують сусідів за станом до кроку (класичний Life).
- Світ — overworld з експозиціями, у які заходиш як у зали музею (скріншот «overworld») (?).
- Розміри рівнів, межі (стіна / край / тор) — (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітина гравця | player | не жива, імунна | крок 4 напрямки; штовхає живу клітину; не входить у підрахунок сусідів |
| Жива клітина («living stone») | object | стан alive | штовхається; після кожного ходу виживає / вмирає за кількістю живих сусідів |
| Порожня клітина | terrain | стан dead | оживає, якщо поруч рівно 3 живі |
| Цільова розстановка | zone | набір клітин | рівень пройдено, коли поле з нею збіглося; як показана — (?) |
| Тексти світу (вірші, історія, коментарі) | static | текст | супровід кожного пазла: історія Life, відомі патерни (glider) |
| «Додаткове правило» пізніх рівнів | — | — | одне нове правило понад Life; суть не розкрито (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next_cell)` → ТО `move(player, dir)`.
- КОЛИ `contact(player, live_cell)` → ЯКЩО `free(cell_behind)` → ТО `push(live_cell)`, `move(player, dir)`; інакше `block` (чи штовхається ланцюг клітин — (?)).
- КОЛИ `turn_end(player)` → ЯКЩО `not occupied(cell, live)` and `adjacent_count(cell, live, ==, 3)` → ТО `spawn(live, cell)` — народження.
- КОЛИ `turn_end(player)` → ЯКЩО `occupied(cell, live)` and `adjacent_count(cell, live, <, 2)` → ТО `disappear(live)` — самотність.
- КОЛИ `turn_end(player)` → ЯКЩО `occupied(cell, live)` and `adjacent_count(cell, live, >, 3)` → ТО `disappear(live)` — перенаселення; 2–3 сусіди — клітина лишається.
- Підрахунок: `custom: «клітина гравця не рахується живим сусідом і сама не вмирає»` (розробник: «a cell that is immune to the rules»).
- КОЛИ `turn_end(player)` → ТО `custom: «усі клітини оновлюються одночасно за станом до кроку»`.
- КОЛИ `pattern(goal_arrangement)` → ТО `win` (поле збіглося з цільовою розстановкою).
- КОЛИ `spawned(live)` / `died(live)` → ТО `sound(note)`; КОЛИ `input(dir)` → ТО `sound(note)` — музика з руху й народжень/смертей.
- КОЛИ `input(undo)` → ТО `undo(1)` — відмотати хід, щоб виправити помилку або переграти ланцюгову реакцію.
- Пізні рівні: `custom: «одне додаткове правило понад Life»` (?).
- Перемога: цільова розстановка · Поразка: нема (колонія може «вибухнути» — тоді undo) · Рахунок: нема.

## Керування і ввід
- Клавіатура: крок клітини гравця на 1 у 4 напрямки (тег Steam Grid-Based Movement); поштовх — крок у бік живої клітини.
- Undo — окрема клавіша (яка — (?)).
- Тег Controller на Steam; рівень підтримки геймпада не вказано (?).

## Вікна, меню, HUD
- `main-menu` (?).
- `map-window`-подібний overworld: зали-експозиції з вхідними точками рівнів, вірші й коментарі в просторі (?).
- `game-screen`: поле клітин, клітина гравця; тексти-супровід пазла (історія Life, патерни); ціль — `+ui:goal-overlay` (як саме показана, гравці питали в обговоренні) (?).
- `settings-window` (?).
- Переходи: overworld → рівень → (ціль) → назад в експозицію (?).

## Фічі поза полем
- `undo` (rewind ходів), `+feature:open-progression` — жодних замкнених зон і схованих рівнів, експозиції відкриті від старту (Steam, itch); сторінка автора каже «each exhibit unlocks» — розбіжність (?).
- `world-map` / хаб-«музей»: 8 експозицій на теми ідентичності, конфлікту, жертви.
- Динамічна музика: ноти від руху гравця й народжень/смертей клітин; у фазі роздумів — тихий дрон (відгук).
- Тексти: вірші, фрагменти історії Life, коментарі розробника.

## Варіації й родичі
- Conway's Game of Life — `build-sim/game-of-life` (правила B3/S23 без гравця); Cell Machine — `build-sim/cell-machine` (штовхання клітин з власними правилами, але без Life-кроку).
- Thinky-родичі: Baba Is You (правила як обʼєкти) — `thinky/baba-is-you`; Sokobond (клітини зчіплюються після поштовху) — `thinky/sokobond`.
- **Осі варіацій**: аватар у CA — імунний штовхач (Changes) / сам живий і рахується / ставить клітини курсором · крок автомата — після кожного ходу / за таймером / вручну кнопкою · мета — цільова розстановка / дійти до виходу / вижити N поколінь · правило — фіксоване Conway / змінне B/S.

## Цікавинки для курсу
- Крок Life B3/S23 з подвійним буфером на квадратній сітці — 🌱 (класика).
- Імунна клітина гравця в Life-кроці (не сусід, не вмирає, займає клітину) і поштовх живої клітини — 📎.
- Undo, що зберігає повний знімок поля на кожен хід: Life незворотний, назад не обчислити — 📎.
- Перевірка «поле = цільова розстановка» — 🌱.
- Музика з подій поля (ноти на народження/смерть, квантування) — 🥉.
- Розвʼязувач: BFS по ходах гравця з Life-динамікою, стан = поле + позиція — 🥇 (хаос: малий зсув → інший результат).

## Мапа на каталог
- Є: `move-4dir` + `move-by-input` + `keyboard-controls` ↔ крок клітини гравця; `push-object` ↔ поштовх живої клітини; `undo-redo` ↔ rewind ходів; `world-map` ↔ overworld з експозиціями; `background-music` + `sound-effects` ↔ динамічна музика; `game-screen`.
- **Нема** → пропозиції карток:
  - `+cellular-automaton-rule` (вже в корпусі) — тут крок автомата прив'язаний до ходу гравця.
  - `+goal-state-check` (Karel, 7 Billion Humans) — поле проти цільової розстановки.
  - `+immune-avatar` «Аватар усередині клітинного автомата, імунний до його правил» · entities/state · 📎.
  - `+reactive-music` «Музика з подій поля» · interface/sound · 🥉.
  - `+hub-world` (Starseed Pilgrim) — музей-хаб.
  - `+open-progression` «Усі рівні відкриті від старту» · levels/progression · 🌱.

## Пропозиції до словників
- `+card:immune-avatar`, `+card:reactive-music` — див. «Мапа на каталог».
- `+feature:open-progression` — жодних замків на рівнях (протилежність `level-unlock`).
- `+ui:goal-overlay` — цільова розстановка поверх поля / поруч із ним.

## Джерела
- ⭐ [Steam: Changes](https://store.steampowered.com/app/1654920/Changes/) — короткий опис («living stones that evolve every time you move»), три правила, undo, 100+ рівнів, 8 експозицій, музика, вірші, теги.
- [Et Al Games: Changes](https://etalgames.com/changes.html) — «interactive version of Conway's Game of Life», експозиції, саундтрек, назви скріншотів.
- [itch.io: Changes](https://etalgames.itch.io/changes) — 100+ рівнів у 8 світах, без замків.
- [Steam: «What's the game about?»](https://steamcommunity.com/app/1654920/discussions/0/4477133359550459235/) — стартова й цільова розстановка, імунна клітина гравця, текст-супровід про історію Life і глайдер.
- [Steam: «Game of life?»](https://steamcommunity.com/app/1654920/discussions/0/4477133359562479522/) — розробник: стандартний Conway's Life, імунна клітина, одне додаткове правило.
- [Steam: відгуки](https://steamcommunity.com/app/1654920/reviews/?browsefilter=toprated&l=english) — ланцюгові реакції, «вибух» невдалих спроб, музей-експозиції, ноти від дій.
- [YouTube: Changes: Indie Dev Postmortem](https://www.youtube.com/watch?v=E505zmvaJKM) — доповідь автора (зміст не переглянуто).

## Непевне
- (?) Числа B3/S23 прямо ніде не написано: розробник каже «standard Conway's Game of Life», а це саме B3/S23 у сусідстві Мура.
- (?) Як показана цільова розстановка, чи треба точний збіг усього поля чи лише позначених клітин — гравець у Steam питав і відповіді не отримав.
- (?) Чи штовхається ряд клітин ланцюгом, чи може клітина народитись на клітині гравця, межі поля (стіни / край / тор).
- (?) Яке саме «додаткове правило» з'являється пізніше; назви скріншотів «river gold», «sudden death», «snake wall», «pond» натякають на тип клітин або цілі, але це лише назви.
- (?) Рух гравця по overworld і як заходять у рівень; клавіші undo; підтримка геймпада.
- Розбіжність: Steam/itch — «no gated areas», сайт автора — «each exhibit unlocks».
