---
title: Desktop Tower Defense
slug: desktop-tower-defense
family: tower-lanes
also: []
klass: cursor
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: none
  goal: survive
year: 2007
platforms: [web (Flash), Nintendo DS]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Desktop_Tower_Defense", best: true, note: "вільний лабіринт із веж, типи кріпів, режими The 100 / 3K Fixed"}
  - {kind: play, url: "https://www.kongregate.com/games/preecep/desktop-tower-defense", note: "сторінка гри на Kongregate (Flash), гарячі клавіші"}
  - {kind: official, url: "https://www.handdrawngames.com/DesktopTD/", note: "сайт автора (HandDrawnGames)"}
  - {kind: other, url: "https://www.handdrawngames.com/DesktopTD/Instructions.asp", note: "гайд: вежі, жонглювання, челенджі 3K/10K/15 Towers"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=desktop+tower+defense+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [enemy-waves, spawn-schedule, spawn-points, enemy-reached-base, player-death, chase-bfs, reachability-check, round-currency, in-round-upgrades, shop-buyback, shop-catalog, projectile-shot, shoot-cooldown, blast-wave, temporary-modes, hp-damage, speed-per-type, multi-cell-size, difficulty-levels, game-pause, hover-highlight, cell-click, keyboard-controls, leaderboard, status-panel, +tower-placement, +maze-by-towers, +path-recompute, +tower-range, +flying-ignores-maze, +call-wave-early, +path-juggling, +aura-buff, +split-on-death, +challenge-modes]
proposes: ["+trigger:path_changed", "+cond:path_exists", "+effect:recompute_path", "+effect:sell", "+effect:upgrade", "+effect:buff", "+role:tower", "+ui:range-circle", "+ui:tower-panel", "+ui:next-wave-button", "+window:mode-select", "+feature:challenge-modes", "+feature:score-submit", "+axis:session"]
author: opus
date: 2026-11-02
---

# Desktop Tower Defense — офісний стіл-сітка, де вежі самі стають лабіринтом

## Суть
Порожнє поле, схоже на робочий стіл; кріпи заходять з краю і біжать до протилежного краю найкоротшим шляхом. Гравець ставить вежі будь-де, і кожна вежа — водночас стіна: шлях вигинається, кріпи довше під вогнем («mazing»). Повністю закрити вихід не можна. Гра популяризувала «лабіринт з веж» і трюк **жонглювання** — продажем/посадкою вежі розвертати натовп туди-сюди.

## Поле і час
- Прямокутна сітка без доріг; вежа займає квадрат 2×2 клітини (?), кріпи рухаються по клітинах з вільними координатами між ними.
- Два входи і два виходи: зліва → направо і згори → вниз (?) — два потоки ділять одне поле, лабіринт мусить працювати для обох.
- Real-time: хвилі (levels) йдуть за таймером; кнопкою можна викликати наступну раніше. Пауза пробілом — будувати можна і на паузі (?).
- Камера: усе поле на екрані, інформація повна; нема туману.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Вхід | spawner | 2 (ліво, верх) | хвиля виходить тут |
| Вихід | static | протилежний край | кріп дійшов → −1 життя |
| Межа поля / кути | static | — | непрохідні, будувати не можна |
| Pellet Tower | tower | найдешевша, 2×2 | слабкі постріли по одній цілі; дешева «цеглина» лабіринту |
| Squirt Tower | tower | швидка стрільба | одна ціль, бʼє і наземних, і повітряних |
| Dart Tower | tower | сплеск | дротики зі шкодою по області, лише наземні (?) |
| Swarm Tower | tower | лише повітря | ракети по літаючих, дуже сильна після апгрейдів |
| Frost Tower | tower | сповільнення | зменшує швидкість наземних у радіусі/цілі |
| Bash Tower | tower | удар по площі | приглушує (stun) наземних поруч з шансом (?) |
| Boost Tower | tower | без атаки | підсилює шкоду сусідніх веж (аура) |
| Звичайний кріп | enemy | HP | біжить найкоротшим шляхом |
| Швидкий (fast) | enemy | швидкість ×k | той самий шлях, швидше |
| Групи (group) | enemy | багато дрібних | натовп, вигідний для сплеску |
| Імунний (immune) | enemy | — | не зазнає ефекту окремих веж (сповільнення/оглушення) |
| Spawn | enemy | — | при смерті розпадається на дрібніших |
| Літаючий (flying) | enemy | — | летить прямо над вежами, ігнорує лабіринт |
| Бос | boss | 1–2 великі, багато HP | кілька разів за гру; деякі літають |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(place, tower, cell)` → ЯКЩО `has(gold, cost)` and `free(cells_2x2)` and `custom: «cond path_exists: обидва входи досягають своїх виходів»` → ТО `spawn(tower)`, `currency(-cost)`, `custom: «effect recompute_path для всіх наземних»`; інакше `block`.
- КОЛИ `custom: «trigger path_changed»` → ТО кожен наземний кріп `custom: «новий найкоротший шлях від своєї поточної позиції»` — він може розвернутися назад.
- КОЛИ `tick` → наземний кріп `move(a, next_on_path)`; літаючий — `move(a, straight_to_exit)`.
- КОЛИ `in_range(tower, creep, r)` → ЯКЩО `custom: «тип цілі дозволений (наземна/повітряна)»` → ТО `spawn(projectile)` з періодом `shoot-cooldown`.
- КОЛИ `contact(projectile, creep)` → ТО `damage(n)`; Dart — `damage` по радіусу; Frost — `speed(creep, ×k, duration)`; Bash — `stun(creep, n)` з `prob(p)` (?).
- КОЛИ `custom: «Boost поруч»` → ТО `custom: «effect buff: +% шкоди сусіднім вежам»`.
- КОЛИ `state(creep, immune)` → ТО ефекти сповільнення/оглушення `block` (?).
- КОЛИ `hp_zero(creep)` → ТО `disappear_a`, `currency(+bounty)`, `score(+n)`; Spawn — `spawn(smaller ×k)` на місці.
- КОЛИ `reach(creep, exit)` → ТО `lives(-1)`, `disappear_a`.
- КОЛИ `counter(lives, ==, 0)` → ТО `lose`.
- КОЛИ `input(upgrade)` на вежі → ЯКЩО `has(gold, price)` → ТО `custom: «effect upgrade: шкода, дальність, темп»`.
- КОЛИ `input(sell)` → ТО `custom: «effect sell: повернути частину вартості»`, `disappear_a`, `custom: «path_changed»`.
- КОЛИ `schedule(levels)` або `input(next_wave)` → ТО `wave_start`, `spawn_at(creeps, entrances)`; раніше викликана хвиля дає бонус-очки.
- Жонглювання (емерджентне правило): `input(sell|place)` в мить, коли натовп близько до виходу, → `path_changed` → натовп розвертається на довший шлях; повтор → кріпи бігають туди-сюди під вогнем.
- Перемога: пережити всі хвилі (50 у звичайній, 100 у The 100) · Поразка: життя = 0 · Рахунок: очки за кріпів + бонус за ранні хвилі; прохід кріпа знижує рахунок (?).

## Керування і ввід
- Миша: клік по іконці вежі → «привид» над полем (зелений — можна, червоний — ні) з колом дальності → клік ставить.
- Клік по вежі → панель: рівень, характеристики, Upgrade, Sell.
- Клавіші: `1–6` — вибір типу вежі, `0` — зняти вибір, `U` — апгрейд, `S` — продаж, утримання `Shift` — ставити кілька підряд, `Space` — пауза.
- Кнопка Start / Next level — запустити (наступну) хвилю раніше.

## Вікна, меню, HUD
- `main-menu` / `mode-select` (⏳): вибір складності (Easy / Medium / Hard) і режиму (звичайний, The 100, челенджі «fun»-режимів).
- `game-screen`: поле-стіл, справа панель веж з цінами (сірі — не вистачає золота), `coins` (золото), `lives`, `score`, `level-number`/`wave-counter`, `next-wave-preview` (тип наступної хвилі), кнопка старту хвилі.
- `+ui:tower-panel` — характеристики вибраної вежі, кнопки Upgrade/Sell; `+ui:range-circle` — затемнене коло дальності.
- `end-screen` — перемога/поразка з рахунком і пропозицією надіслати його.
- `leaderboard` — таблиця рекордів (введення імені; голосова підказка з «Ivor the Engine»).
- Переходи: main-menu → (режим/складність) → game-screen → end-screen → leaderboard → main-menu.

## Фічі поза полем
- `difficulty-presets`: Easy / Medium / Hard.
- `+feature:challenge-modes`: The 100 (100 рівнів), 3K Fixed (фіксований набір веж з апгрейдами за 3000 золота), 10K, 15 Towers (лише 15 веж), Splash Only та інші «fun»-режими з обмеженнями.
- `leaderboard-online` — надсилання рахунку на сайт/Kongregate (`+feature:score-submit`).
- `pause`, швидкий виклик хвиль (`+call-wave-early`).
- Версії: 1.0 → 1.5 (нові вежі й режими), Desktop TD Pro (?), DS-версія 2009, Desktop Defender (Facebook, 2010).

## Варіації й родичі
- Попередник ідеї — кастомні карти Warcraft III / StarCraft («maze TD»); наступники — Fieldrunners (2008), Defense Grid, Gemcraft, Bloons (фіксований шлях), Emberward (лабіринт з тетроміно).
- **Осі варіацій**: шлях — фіксований / лабіринт з веж / з окремих блоків · кількість потоків — 1 / 2 перехресні · блокування — заборонено / дозволено (вороги ламають) · вежа як стіна — так / ні (вежі на узбіччі).
- Челенджі як «правила-обмеження» на тому самому двіжку: ліміт золота, ліміт кількості веж, лише сплеш-вежі.

## Цікавинки для курсу
- Лабіринт з веж + заборона перекриття: BFS від обох входів перед кожною посадкою — 🥇 (`reachability-check` у живому часі для двох пар вхід/вихід).
- Перерахунок шляху для кожного кріпа з його поточної клітини (кріп розвертається) — 🥈.
- Жонглювання: емерджентна поведінка з двох простих правил (продаж + перерахунок шляху) — 🥈, гарний приклад «механіка, яку не проєктували».
- Boost-аура: вежа без атаки, що модифікує сусідів — 🥉 (сусідство на сітці + модифікатори параметрів).
- Кріп, що розпадається при смерті (Spawn) — 📎.
- Челенджі як конфіг обмежень до тих самих правил — 📎.

## Мапа на каталог
- Є: `enemy-waves` + `spawn-schedule` + `spawn-points` · `enemy-reached-base` + `player-death` (життя) · `chase-bfs` ↔ найкоротший шлях · `reachability-check` ↔ заборона перекриття · `round-currency` ↔ золото · `in-round-upgrades` ↔ апгрейд веж · `shop-buyback` ↔ продаж · `shop-catalog` ↔ панель веж · `projectile-shot` + `shoot-cooldown` · `blast-wave` ↔ сплеск Dart/Bash · `temporary-modes` ↔ сповільнення/оглушення · `hp-damage` · `speed-per-type` · `multi-cell-size` ↔ вежа 2×2 · `difficulty-levels` · `game-pause` · `hover-highlight` + `cell-click` · `keyboard-controls` (гарячі клавіші) · `leaderboard` · `status-panel`.
- **Нема** → пропозиції карток:
  - `+tower-placement`, `+tower-range`, `+maze-by-towers`, `+path-recompute`, `+flying-ignores-maze`, `+call-wave-early` — див. fieldrunners.
  - `+path-juggling` «Жонглювання шляхом» · entities/move · 🥈 — посадка/продаж вежі розвертає натовп; тест на коректний перерахунок шляху з середини.
  - `+aura-buff` «Аура-підсилення сусідів» · entities/state · 🥉 · слот {radius, bonus}.
  - `+split-on-death` «Розпад при смерті» · entities/spawn · 📎 · слот {children}.
  - `+challenge-modes` «Режими-обмеження» · game-logic/difficulty · 📎 · слоти {gold_cap, tower_cap, allowed_towers}.

## Пропозиції до словників
- `+trigger:path_changed`, `+cond:path_exists`, `+effect:recompute_path`, `+effect:sell`, `+effect:upgrade`, `+role:tower` — підтвердження з fieldrunners.
- `+effect:buff` — тимчасово/постійно змінити параметр іншої сутності (Boost Tower).
- `+ui:range-circle`, `+ui:tower-panel`, `+ui:next-wave-button` — підтвердження.
- `+window:mode-select` — уже ⏳; тут складність + челенджі.
- `+feature:challenge-modes` — набір режимів з обмеженнями ресурсу/кількості.
- `+feature:score-submit` — надіслати рахунок на онлайн-таблицю з кінцевого екрана.
- `+axis:session` — `match` (50/100 рівнів).

## Джерела
- ⭐ [Wikipedia: Desktop Tower Defense](https://en.wikipedia.org/wiki/Desktop_Tower_Defense) — шлях будують вежі, вихід не можна закрити, типи кріпів (літаючі, spawn, імунні, швидкі, боси), життя, The 100, 3K Fixed, DS і Facebook-версії.
- [Kongregate](https://www.kongregate.com/games/preecep/desktop-tower-defense) — опис і гарячі клавіші (1–6, 0, U, S, Shift, Space).
- [HandDrawnGames: Instructions](https://www.handdrawngames.com/DesktopTD/Instructions.asp) — гайд: вежі Bash/Frost/Squirt/Swarm/Boost, жонглювання, режими 3K/10K/15 Towers/Splash Only, ранні хвилі за бонус.
- [HandDrawnGames](https://www.handdrawngames.com/DesktopTD/) — сайт автора (Paul Preece).
- YouTube: пошук «desktop tower defense gameplay».

## Непевне
- (?) Розмір вежі (2×2) і поля в клітинах, точні координати двох входів/виходів.
- (?) Вежі по версіях: у 1.0 лише Pellet/Squirt/Dart/Frost/Swarm (?), Bash/Boost — 1.5; сайт автора і гайд згадують також Storm/Snap/Ink — ймовірно інші версії (Pro/DS).
- (?) Чи є відсотки (interest) на золото, стартове число життів (20?), частка повернення при продажу.
- (?) Хто з кріпів імунний до чого саме; чи бʼє Dart повітряних.
- (?) Формула рахунку і чи знижує його прохід кріпа.
