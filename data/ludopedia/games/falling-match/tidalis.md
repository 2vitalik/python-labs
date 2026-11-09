---
title: Tidalis
slug: tidalis
aka: []
family: falling-match
also: [connect-rotate]
klass: cursor
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: survive
year: 2010
platforms: [PC, Mac, Linux]
links:
  - {kind: other, url: "https://psillustrated.com/gamevortex/soft_rev.php/5097", best: true, note: "огляд GameVortex: правий drag повертає стрілки однокольорових блоків уздовж шляху, лівий клік — запуск хвилі, подвійні стрілки ділять хвилю, падіння запускає нові хвилі, режими"}
  - {kind: steam, url: "https://store.steampowered.com/app/40420/Tidalis/", note: "опис: блоки з кольором і стрілкою падають, стос вище поля = поразка, 20 режимів, 115 рівнів пригоди, редактор, кооп і versus"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Tidalis", note: "лише інфобокс: Arcen Games, 2010, Unity"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=tidalis+arcen+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [beam-tracing, tile-rotate, path-drawing, gravity-fall, chain-reaction, spawn-random-cell, combo-multiplier, move-limit, in-game-editor, level-exchange, editor-window, mode-select, online-multiplayer, rule-variants, game-settings, sequential-levels, game-screen, +arrow-stream-match, +stream-split, +wildcard-tile, +fixed-arrow-tile, +overflow-top-lose]
proposes: ["+effect:emit_stream(a)", "+effect:orient_along(path)", "+trigger:stream_end"]
author: opus
date: 2026-11-09
---

# Tidalis — падаючі блоки зі стрілками: запусти хвилю, вона біжить за стрілками й забирає однокольорові

## Суть
Згори падають блоки, кожен має колір і стрілку. Гравець правим drag-ом малює шлях — однокольорові блоки на шляху повертають стрілки за ним; лівим кліком запускає з блока хвилю, що біжить за стрілками і «підхоплює» блоки свого кольору. Коли хвиля скінчилась, підхоплені блоки зникають, верхні падають — і їхнє падіння запускає нові хвилі (комбо). Незвичне: збіг — не сусідство, а **маршрут** по стрілках, який ти будуєш поворотами.

## Поле і час
- Прямокутна дошка-колодязь; блоки падають, поки ти плануєш (GameVortex: «tiles keep falling while you plan»).
- Реальний час, крім режиму головоломок (brainteaser) — там ліміт ходів, а не таймер.
- Хвиля переходить на блок, що не далі ніж за 2 клітини від попереднього (GameVortex) — тобто може перестрибнути одну.
- Поразка — стос вище висоти поля (Steam).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Блок | tile | колір, напрям стрілки | падає; повертається drag-ом; підхоплюється хвилею свого кольору |
| Блок з подвійною стрілкою | conduit | колір, 2 напрями | хвиля ділиться й іде в обидва боки |
| Wildcard-блок | tile | — | збігається з будь-яким кольором (?) |
| Неповоротний блок | tile | колір, стрілка | стрілку не змінити (пізні рівні) |
| Хвиля (stream) | projectile | колір, напрям | біжить від блока за стрілками; блоки інших кольорів не чіпає (?) |
| Power-up | pickup | тип | змінює правила/поле; деталей у джерелах нема (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `timer(spawn)` → ТО `spawn_at(block(random_color, random_dir), top)`, `fall(block)`.
- КОЛИ `input(right_drag(path))` → ЯКЩО `same(block, start_block, color)` → ТО `custom: «orient_along — стрілки однокольорових блоків на шляху повертаються вздовж шляху»`.
- КОЛИ `input(left_click(block))` → ТО `custom: «emit_stream — з блока виходить хвиля його кольору за стрілкою»`.
- КОЛИ `custom: «хвиля дійшла до блока»` → ЯКЩО `same(stream, block, color)` і `in_range(prev_block, block, 2)` → ТО `set_state(block, activated)`, `face(stream, block.dir)`.
- КОЛИ `custom: «хвиля на блоці іншого кольору»` → ТО `custom: «проходить без ефекту»` (?).
- КОЛИ `custom: «хвиля на подвійній стрілці»` → ТО `clone(stream)`, обидві йдуть своїми напрямками.
- КОЛИ `custom: «stream_end — далі нема блока свого кольору»` → ЯКЩО `count(activated, ≥, 3)` (?) → ТО `clear(activated)`, `score(n)`.
- КОЛИ `after(clear)` → ТО `fall(blocks_above)`; КОЛИ `settled` → ЯКЩО `custom: «блок, що впав, утворив маршрут»` → ТО `custom: «нова хвиля»`, `combo(+1)`.
- КОЛИ `input(right_drag)` → ЯКЩО `state(block, fixed_arrow)` → ТО `block`.
- КОЛИ `counter(stack_height, >, board_height)` → ТО `lose`.
- КОЛИ `input(any)` → ЯКЩО `mode(brainteaser)` → ТО `counter(moves, −1)`; КОЛИ `counter(moves, =, 0)` → ЯКЩО `count(blocks, >, 0)` → ТО `lose`.
- КОЛИ `all_gone(block)` → ЯКЩО `mode(brainteaser)` → ТО `win`.
- Перемога: виконати ціль рівня / очистити головоломку · Поразка: стос переповнив поле або скінчились ходи · Рахунок: довші ланцюги й комбо — більше очок.

## Керування і ввід
- Миша: правий drag — малювати шлях і повертати стрілки; лівий клік — запустити хвилю (GameVortex; Steam формулює «right-click and drag paths through the arrows»).
- Повороти плануються на льоту, поки блоки падають; одна хвиля може зачепити кілька маршрутів.

## Вікна, меню, HUD
- `main-menu`: Adventure · Quick Play (налаштовувані правила) · Brainteasers · Multiplayer · Editor · Options (?).
- `mode-select` — 20 режимів: «action-oriented» і «timer-less brainteasers» (Steam).
- `game-screen`: колодязь, `score`, `move-counter` (brainteaser), `path-preview` хвилі (?).
- `editor-window` — редактор тем, рівнів і пригод.
- `lobby-window` — мережева гра з пошуком друзів (GameVortex).
- `settings-window` — доступність: палітра для дальтоніків, менше світла й руху, слабкі ПК (Steam).

## Фічі поза полем
- Пригода: 115 рівнів з оповіддю, складність росте (Steam, GameVortex).
- `mode-puzzle` (brainteasers) — розчистити дошку за задану кількість ходів.
- `custom-rules` — Quick Play / custom games з налаштуванням правил.
- `level-editor` + `level-sharing`: створювати й ділитися темами, рівнями, пригодами.
- `mode-coop` і `mode-versus` — локально й по мережі.
- `colorblind-palette`, `animation-toggle` (менше руху/світла).

## Варіації й родичі
- Родичі: [puzzle-and-dragons](puzzle-and-dragons.md) (збіг маршрутом), [magical-drop](magical-drop.md), [lumines](lumines.md); стрілки й промені — сімʼя `connect-rotate` (Deflektor, Khet); [panel-de-pon](panel-de-pon.md) — каскади від падіння.
- **Осі варіацій**: що таке збіг (сусідство / лінія / маршрут за стрілками) · хто задає маршрут (гравець поворотами / фіксовані стрілки) · розгалуження (нема / подвійна стрілка) · крок хвилі (лише сусід / до 2 клітин).

## Цікавинки для курсу
- Хвиля по стрілках з підхопленням свого кольору — трасування з умовою — 📎.
- Поворот стрілок уздовж намальованого шляху (drag → орієнтація) — 📎.
- Розгалуження хвилі на подвійній стрілці (BFS замість одного шляху) — 🥉.
- Падіння після зникнення запускає нові хвилі — каскад — 🥉.
- Ліміт ходів у головоломках поверх реального часу (два режими одних правил) — 🌱.

## Мапа на каталог
- Є: `beam-tracing` (хвиля за стрілками) · `tile-rotate` · `path-drawing` (правий drag) · `gravity-fall` · `chain-reaction` · `spawn-random-cell` · `combo-multiplier` · `move-limit` (brainteasers) · `in-game-editor`/`editor-window`/`level-exchange` · `mode-select` · `online-multiplayer` · `rule-variants` (Quick Play) · `game-settings` · `sequential-levels`.
- **Нема** → пропозиції карток:
  - `+arrow-stream-match` «Збіг маршрутом по стрілках клітин» · entities/interact · 📎.
  - `+stream-split` «Хвиля ділиться на подвійній стрілці» · entities/interact · 🥉.
  - `+wildcard-tile` «Плитка під будь-який колір» · entities/interact · 🌱.
  - `+fixed-arrow-tile` «Неповоротна плитка» · entities/state · 🌱.
  - `+overflow-top-lose` «Стос вище поля = поразка» · game-logic/lose · 🌱.

## Пропозиції до словників
- `+effect:emit_stream(a)` — з сутності виходить хвиля, що йде за стрілками клітин.
- `+effect:orient_along(path)` — стрілки сутностей на шляху повертаються вздовж намальованого шляху.
- `+trigger:stream_end` — хвиля/промінь більше не має куди йти.

## Джерела
- ⭐ [GameVortex: огляд](https://psillustrated.com/gamevortex/soft_rev.php/5097) — правий drag, лівий клік, ≤2 клітини, подвійні стрілки, падіння → нові хвилі, неповоротні блоки, brainteasers з лімітом ходів, мережа.
- [Steam](https://store.steampowered.com/app/40420/Tidalis/) — падіння, поразка за висотою, 20 режимів, 115 рівнів, редактор, кооп/versus, доступність.
- [Wikipedia](https://en.wikipedia.org/wiki/Tidalis) — лише інфобокс.

## Непевне
- (?) Мінімальна довжина ланцюга — 3 (зі сніпета пошуку, не з першого джерела).
- (?) Хвиля проходить крізь блоки іншого кольору без ефекту — зі сніпета пошуку.
- (?) Wildcard-блок і власне список спецблоків і power-up-ів («dozens» за Steam) — без деталей.
- (?) Чи хвиля перестрибує саме одну порожню/чужу клітину і чи йде лише по прямій стрілки.
- (?) Пункти головного меню; чи є versus проти AI.
- (?) Цілі рівнів пригоди (очки / ланцюги / виживання) — `goal: survive` як найближче.
