---
title: Emeraldia
slug: emeraldia
aka: [エメラルディア, "Arcade Archives EMERALDIA"]
family: falling-match
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: hotseat
  info: full
  random: runtime
  goal: collect
year: 1993
platforms: [arcade (Namco NA-1), mobile (2006), Wii Virtual Console Arcade, PS4, Switch]
links:
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/エメラルディア", best: true, note: "JA: L-фігура з 3 кубиків, тріщина/розбиття, шкода на однокольорових сусідів з діагоналями, червона лінія і кочення, режими, предмети Adventure"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Emeraldia", note: "Adventure: порятунок істот, предмети, бос Jamir, Escape Stage"}
  - {kind: other, url: "https://store.playstation.com/en-gb/concept/10010050", note: "Arcade Archives: опис правила, режими, онлайн-рекорди"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Emeraldia+arcade+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [gravity-fall, multi-cell-size, piece-rotate-flip, hp-damage, chain-reaction, inventory-items, skip-level, sequential-levels, difficulty-levels, progress-acceleration, simultaneous-versus, garbage-attack, game-over-continue, leaderboard, game-settings, mode-select, end-screen, +landing-hit-crack, +damage-spread-same-color, +overflow-roll, +deliver-to-bottom, +color-clear-special, +gauge-item-block, +garbage-adjacent-clear, +garbage-collide-clear, +possessed-block-boss, +lose-only-if-unplayable]
proposes: ["+effect:clear_color", "+card:landing-hit-crack", "+card:damage-spread-same-color", "+card:overflow-roll", "+card:deliver-to-bottom", "+card:garbage-collide-clear", "+card:possessed-block-boss", "+card:lose-only-if-unplayable"]
author: opus
date: 2026-11-09
---

# Emeraldia — кубик, упавши на свій колір, тріскає його; другий удар розбиває, і шкода розтікається на однокольорових сусідів

## Суть
Аркадна головоломка Namco: падають L-фігури з трьох кольорових кубиків. Кубики не зникають від «трьох у ряд»: кожен кубик, що впав на кубик **того самого кольору**, завдає йому удару — перший тріскає, другий розбиває. Удар передається всім однокольоровим кубикам, що торкаються сторонами або кутами, тож велика тріснута пляма розлітається разом, а падіння зверху запускає ланцюги. В Adventure мета — розбити стартову кладку так, щоб морські істоти, замкнені в ній, опустились на дно.

## Поле і час
- Колодязь із червоною лінією вгорі; розмір у джерелах не названо (?).
- Real-time падіння; «drop level» — темп, що росте з кількістю скидань (Beginner в аркаді закінчується на drop level 20).
- Adventure: кожна стадія починається з заданою кладкою кубиків і істотами в ній; Normal — з порожнього поля, без кінця; Versus — два поля.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| L-фігура | player | 3 кубики, кольори | зсув, поворот, падіння |
| Кубик | tile | колір; ціле → тріснуте → розбите (2 удари) | падіння на однокольоровий = удар по ньому; удар розтікається на однокольорових сусідів (4 сторони + діагоналі) |
| Чорний блок | hazard | — | не отримує шкоди від «Люті восьминога»; інша поведінка в джерелах не описана |
| Морська істота | object | у стартовій кладці | опускається разом зі стеком; на дні — врятована |
| Червона лінія | zone | верх поля | частина фігури понад лінією відламується й котиться вбік |
| Зірка | pickup | Normal — коли повна шкала; Versus — кожні N скидань | лягла → стирає всі кубики кольору, на який упала |
| Кубик-перешкода з обличчям | hazard | Versus | зникає, якщо поруч розбито звичайний кубик, або від зіткнення з іншим кубиком-перешкодою |
| Джамір | boss | 6 тріщин | вселяється в кубик; тріснув → переходить в інший |
| Дельфіни (7 рожевих, 1 синій) | object | Escape Stage | теж треба опустити на дно |
| Предмет Adventure | pickup | одноразовий, діє лише в наступному океані | див. перелік нижче |

Предмети: Священне серце Мінт (з рулетки continue) — зникають усі кубики · Сяюча луска — усі, крім двох нижніх рядів · Дрімота риби-місяця — кладка повертається до старту, але вся тріснута · Лють восьминога — 1 удар усім, крім чорних · Задум краба — пропуск двох стадій · Сльози черепахи — усі кубики одного кольору · Щирість пінгвіна — на час усі кубики падають уже тріснутими · Перше кохання вудильника — на час падає по одному кубику.

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ЯКЩО `free(cells_below)` → ТО `move(piece, down)`; `input(shift|rotate)` → ЯКЩО `free(target)` → ТО `move` / `rotate(piece, 90)`.
- КОЛИ `locked(piece)` → ЯКЩО `occupied(cell_below, cube)` і `same(cube, cube_below, color)` → ТО `damage(cube_below, 1)`.
- КОЛИ `after(damage)` → ТО `damage(same_color_group8, 1)` — удар отримують усі однокольорові кубики, що торкаються сторонами або діагоналлю.
- КОЛИ `custom: «перший удар»` → ТО `set_state(cube, cracked)`; КОЛИ `hp_zero(cube)` (другий удар) → ТО `disappear(cube)`, `fall(cubes_above)`.
- КОЛИ `after(fall)` → ЯКЩО кубик упав на однокольоровий → ТО новий удар, `combo(+1)` — ланцюг.
- КОЛИ `locked(piece)` → ЯКЩО `custom: «частина фігури вище червоної лінії»` → ТО `custom: «частина відламується»`, `roll(part, left|right)`.
- КОЛИ `input(change_roll)` → ЯКЩО `first_time` → ТО `custom: «напрям кочення змінюється — один раз»`.
- КОЛИ `spawned(next)` → ЯКЩО `not free(spawn)` і `custom: «наступна фігура не звільнить місця»` → ТО `lose`; повне поле саме по собі не програш.
- КОЛИ `counter(gauge, ==, full)` → ЯКЩО `mode(normal)` → ТО `spawn_at(star, next)`; КОЛИ `counter(drops, ==, n)` → ЯКЩО `mode(versus)` → ТО теж зірка.
- КОЛИ `locked(star)` → ТО `custom: «clear_color — з поля зникають усі кубики кольору, на який упала зірка»`.
- КОЛИ `reach(creature, bottom)` → ТО `custom: «істоту врятовано»`; КОЛИ `all_gone(creature)` → ТО `win`, `next_level`.
- КОЛИ `level_end` (океан пройдено або continue) → ТО `give(player, item)`; КОЛИ `input(up + button)` → ЯКЩО `has(player, item)` → ТО `use(item)`.
- КОЛИ `custom: «розбито багато кубиків за раз»` → ЯКЩО `mode(versus)` → ТО `send_garbage(cubes)` — кубики, серед них кубики-перешкоди.
- КОЛИ `custom: «поруч розбито звичайний кубик»` → ТО `disappear(obstacle_cube)`; КОЛИ `contact(obstacle_cube, obstacle_cube)` → ТО `disappear_both`.
- КОЛИ `custom: «тріснув кубик Джаміра»` → ТО `counter(jamir, -1)`, `teleport(jamir, other_cube)`; КОЛИ `counter(jamir, ==, 0)` → ТО `win`.
- Перемога: усі істоти на дні (Adventure), бос Джамір після 6 тріщин · Поразка: нема місця для наступної фігури · Рахунок: очки за розбиті кубики й ланцюги (формулу не знайдено).

## Керування і ввід
- Важіль — зсув і прискорення; кнопка — поворот фігури.
- Важіль угору + кнопка — застосувати предмет Adventure.
- Під час кочення відламаної частини можна один раз змінити напрям — це часто вирішує, чи виживеш.

## Вікна, меню, HUD
- `splash-screen` / `attract-demo` → `mode-select`: Adventure · Normal · Versus (другий гравець).
- `game-screen`: поле з червоною лінією, `next-piece-preview` зі шкалою зірки (Normal), `score`, рівень темпу; в Adventure — лічильник істот (?).
- `map-window` (?) — вибір/показ океану між стадіями; 7 океанів, фінальний — Mystic Ocean.
- `game-over-continue` з рулеткою (може дати Священне серце Мінт).
- `end-screen` стадії / гри; `leaderboard` (Arcade Archives — світові рекорди).
- `settings-window` (Arcade Archives): складність, вигляд аркадного екрана, межа лічильника очок (counter stop) до десятків мільйонів; мануал шістьма мовами.

## Фічі поза полем
- `mode-classic` → Adventure: 40 стадій у 7 океанах (мобільна — 42), предмет за кожен океан · `mode-endless` → Normal · `mode-versus`.
- `difficulty-presets` (Beginner обмежений drop level 20) · `skip-level` (Задум краба) · `continue` з рулеткою.
- Arcade Archives (2024): `leaderboard-online`, `operator-settings`, оригінальна й закордонні версії.

## Варіації й родичі
- Порти: мобільний (2006, Windream, 42 стадії), Wii VC Arcade (2009), Arcade Archives PS4/Switch (2024, Hamster).
- Та сама плата NA-1, що й у Cosmo Gang the Puzzle (окремий файл сімʼї).
- Родичі: [columns](columns.md) (трійка кольорів, але збіг лінією), [puyo-puyo](puyo-puyo.md) (звʼязана група), [dr-mario](dr-mario.md) (стартова кладка, яку треба розібрати).
- **Осі варіацій**: що руйнує (збіг N / удар падінням) · міцність (1 удар / 2) · поширення (лише та клітина / група 4 / група 8) · переповнення (програш / відламати й котити).

## Цікавинки для курсу
- Удар падінням: перевірка «під кубиком той самий колір» після кожного приземлення — 🌱.
- Поширення шкоди на однокольорову групу з 8-сусідством, 2 HP на клітину — 📎 (flood fill + стани тріщини).
- Ланцюг «розбито → падіння → новий удар» — 🥉 (каскад до стабілізації).
- Переповнення як подія, а не програш: частина фігури відламується й котиться, напрям можна змінити один раз — 📎.
- Adventure-мета «опусти істот на дно» замість «прибери все» — 🌱; бос, що перестрибує між кубиками, — 📎.
- Предмети з різними глобальними ефектами (скинути поле, удар усім, тріснуті кубики на час) — 🥉 (система модифікаторів).

## Мапа на каталог
- Є: `gravity-fall` · `multi-cell-size` (L з 3 кубиків) · `piece-rotate-flip` · `hp-damage` (2 удари) · `chain-reaction` · `inventory-items` (предмети Adventure) · `skip-level` · `sequential-levels` · `difficulty-levels` · `progress-acceleration` (drop level) · `simultaneous-versus` + `garbage-attack` · `game-over-continue` · `leaderboard` · `game-settings` · `mode-select` · `end-screen`.
- **Нема** → пропозиції карток:
  - `+landing-hit-crack` «Падіння на свій колір — удар» · entities/interact · 🌱 · слоти {hits: 2}.
  - `+damage-spread-same-color` «Шкода розтікається на однокольорову групу» · entities/interact · 📎 · слоти {adjacency: 4|8}.
  - `+overflow-roll` «Частина фігури понад лінією відламується й котиться» · entities/move · 📎.
  - `+deliver-to-bottom` «Опустити обʼєкти на дно поля» · game-logic/win · 🌱 — істоти, дельфіни.
  - `+color-clear-special` «Спецблок стирає колір» · entities/interact · 🌱 — зірка.
  - `+gauge-item-block` «Шкала скидань дає предмет у NEXT» · game-logic/economy · 📎.
  - `+garbage-adjacent-clear` / `+garbage-collide-clear` «Сміття зникає від сусіднього розбиття / від зіткнення сміття зі сміттям» · entities/interact · 🌱.
  - `+possessed-block-boss` «Бос вселяється в клітину й перестрибує» · entities/state · 📎.
  - `+lose-only-if-unplayable` «Повне поле — не програш, якщо наступна фігура звільнить місце» · game-logic/lose · 🌱.

## Пропозиції до словників
- `+effect:clear_color` — прибрати всі кубики одного кольору (зірка, Сльози черепахи); підтверджую 🔥.
- `+card:landing-hit-crack` · `+card:damage-spread-same-color` · `+card:overflow-roll` · `+card:deliver-to-bottom` · `+card:garbage-collide-clear` · `+card:possessed-block-boss` · `+card:lose-only-if-unplayable` — див. «Мапа на каталог».

## Джерела
- ⭐ [JA Wikipedia: エメラルディア](https://ja.wikipedia.org/wiki/エメラルディア) — L з 3 кубиків, 1 удар = тріщина, 2 = розбиття, поширення на однокольорових по сторонах і діагоналях, червона лінія й кочення, умова поразки, Adventure (океани, предмети), Normal (зірка, drop level 20), Versus (кубики-перешкоди), порти.
- [EN Wikipedia: Emeraldia](https://en.wikipedia.org/wiki/Emeraldia) — режими, порятунок істот, предмети на наступний океан, бос Jamir (6 тріщин), Escape Stage.
- [PlayStation Store: Arcade Archives EMERALDIA](https://store.playstation.com/en-gb/concept/10010050) — «crashed by dropping them twice with the same color», три режими, світові рекорди, налаштування.
- YouTube: пошук «Emeraldia arcade gameplay».

## Непевне
- (?) EN Wikipedia описує інакше: «три кубики одного кольору вертикально тріскаються, четвертий розбиває всіх» — JA каже «кожне падіння на свій колір = удар»; беру JA, бо збігається з описом Arcade Archives.
- (?) Чи розпадається L-фігура після приземлення на окремі кубики — не сказано.
- (?) Розмір поля, кількість кольорів, формула очок, куди саме надходять кубики-сміття у Versus (зверху чи знизу).
- (?) Арифметика Adventure: «7 океанів по 5 стадій = 40, Південний Тихий — 3, фінальний — 7» у JA не сходиться; показ карти океанів не підтверджено.
- (?) Поведінка чорних блоків поза взаємодією з предметом.
