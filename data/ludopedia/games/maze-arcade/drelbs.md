---
title: Drelbs
slug: drelbs
aka: []
family: maze-arcade
also: [connect-rotate]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: full
  random: runtime
  goal: state
year: 1983
platforms: [Atari 8-bit, Apple II, Commodore 64 (1984)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Drelbs", best: true, note: "ворота повертаються на 90°, коробки, trollaboars, screwhead-танки, dark corridor, mystery lady, 8 раундів, 3 складності"}
  - {kind: other, url: "https://archive.org/details/drelbs-synapse/", note: "скан мануалу Synapse (PDF + OCR-текст): серця, діаманти, gorgolytes, бонус 250 × коробки, 5 життів, клавіші"}
  - {kind: other, url: "http://www.atarimagazines.com/rom/issue6/product_reviews.php", note: "огляд ROM Magazine: рахунок тане без вікна, 2 танки з другого рівня, gorgolyte розбирає коробки"}
  - {kind: other, url: "https://256colors.wordpress.com/2009/05/28/review-drelbs-c64-by-kelly-jones-miriam-nathan-william-mandel-published-by-synapse-software/", note: "огляд C64: вікно завжди далеко від гравця, у коридорі прохід рядом звільняє весь ряд"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Drelbs+Atari+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [move-4dir, chase-player, enemy-patrol, projectile-shot, touch-death, player-death, temporary-modes, event-points, sequential-levels, progress-acceleration, difficulty-levels, difficulty-select, game-pause, game-screen, +grid-line-field, +turnstile-gate, +close-box-cells, +trap-escape-timer, +ricochet-shot, +box-destroyer-enemy, +timed-portal, +score-drain, +captive-rescue, +bonus-stage]
proposes: ["+window:bonus-round", "+card:close-box-cells", "+card:box-destroyer-enemy", "+card:timed-portal", "+card:score-drain", "+card:captive-rescue"]
author: opus
date: 2026-11-09
---

# Drelbs — крути ворота-стінки решітки, замикай із них коробки, поки квадратні вороги крутять їх назад

## Суть
Дрелб — ходяче око — бігає по «атомній фліп-решітці» з воріт: стінок на шарнірах, що повертаються на 90°, коли в них вбігти. Мета — повертанням воріт замкнути якомога більше коробок (клітин, закритих з чотирьох боків), а коли закрито все, що можна, — вскочити у вікно-портал до темного коридору й визволити там полонених дрелбів. Переслідувачі trollaboars теж крутять ворота, але замкнути коробку не можуть; по порожній рамці навколо решітки їздять танки, чиї кулі рикошетять від воріт.

## Поле і час
- Решітка воріт (як у Lady Bug): кожні ворота — відрізок стіни на центральному шарнірі; положення горизонтальне / вертикальне. Між воротами — коридори; «коробка» — клітина, всі чотири сторони якої закрито воротами.
- Навколо решітки — порожня смуга-рамка, де патрулюють танки.
- Два екрани: решітка (основний) і темний коридор (окремий екран-раунд з полоненими).
- Real-time; 8 раундів, названих самоцвітами, плюс бонус-екран після кожного.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Дрелб | player | 5 життів | біг 4 напрямки; вбігши у ворота, повертає їх на 90° |
| Ворота | gate | орієнтація ━/┃, шарнір | повертаються на 90° від поштовху дрелба або trollaboar |
| Коробка (замкнена) | zone | пульсує | клітина, закрита з 4 боків; дає очки; пастка для trollaboar |
| Trollaboar | enemy | квадратний | переслідує дрелба; крутить ворота, але не замикає коробок |
| Screwhead-танк | enemy | 1, з наступного рівня 2 | патрулює рамку, стріляє |
| Куля танка | projectile | — | рикошетить від воріт; влучання — смерть |
| Серце | pickup | у коридорах решітки | заморожує trollaboars на 5 с |
| Діамант | pickup | зʼявляється ненадовго | відкриває вікно до коридору раніше, ніж закрито всі коробки |
| Gorgolyte | enemy | у коробках після повного закриття | руйнує коробку, у якій зʼявився; на решітці дрелбу не шкодить |
| Drelbish window | gate | ненадовго; на дальньому від гравця боці | портал у темний коридор |
| Mystery lady | neutral | зʼявляється випадково в коробці gorgolyte | поцілунок → бонус-екран |
| Полонений дрелб | pickup | сітка в коридорі | дотик звільняє |
| Gorgolyte коридору | enemy | — | полює і стріляє; спійманий дрелб повертається на решітку |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(cell_in_dir)` → ТО `move(drelb, dir)`.
- КОЛИ `contact(drelb, gate)` → ТО `rotate(gate, 90)`.
- КОЛИ `contact(trollaboar, gate)` → ТО `rotate(gate, 90)`; ЯКЩО `custom: «поворот замкнув би коробку»` → ТО `custom: «коробка не зараховується»` (замикає лише дрелб).
- КОЛИ `pattern(region_closed)` → ЯКЩО `custom: «останні ворота повернув дрелб»` → ТО `transform(cell, closed_box)`, `score(n)`.
- КОЛИ `pattern(region_closed)` → ЯКЩО `occupied(cell, trollaboar)` → ТО `stun(trollaboar, n)` — ненадовго знерухомлений, потім вибирається.
- КОЛИ `contact(drelb, heart)` → ТО `pickup`, `freeze(trollaboars, 5s)`.
- КОЛИ `timer(tank_fire)` → ТО `spawn(bullet)`; КОЛИ `blocked(bullet)` → ЯКЩО `custom: «перешкода — ворота»` → ТО `bounce(bullet)`.
- КОЛИ `contact(drelb, bullet|tank)` → ТО `lose` (−1 життя).
- КОЛИ `custom: «закрито всі можливі коробки»` → ТО `spawn_at(gorgolyte, boxes)`, `spawn_at(window, far_box)`.
- КОЛИ `spawned(gorgolyte)` → ТО `custom: «руйнує свою коробку»` — коробка знову відкрита.
- КОЛИ `contact(drelb, diamond)` → ТО `pickup`, `spawn_at(window, box)` достроково.
- КОЛИ `enter(drelb, window)` → ТО `window(custom-window)` «dark corridor».
- КОЛИ `timer(window_life)` → ЯКЩО `custom: «дрелб не встиг»` → ТО `disappear(window)`, `custom: «рахунок швидко тане, доки не закрито нових коробок»`.
- КОЛИ `rng(p)` → ТО `spawn_at(mystery_lady, gorgolyte_box)`; КОЛИ `contact(drelb, mystery_lady)` → ТО `window(bonus-round)`, `score(250 × closed_boxes)`.
- Коридор: КОЛИ `contact(drelb, captive)` → ТО `disappear_b`; `custom: «пробіг рядом/стовпцем звільняє весь ряд»`.
- Коридор: КОЛИ `contact(drelb, gorgolyte|shot)` → ТО `custom: «назад на решітку»` (життя не втрачається).
- Коридор: КОЛИ `all_gone(captive)` → ТО `window(bonus-round)`, `score(250 × closed_boxes)`, `next_level`.
- КОЛИ `level_start` → ЯКЩО `level(>=, 2)` → ТО `custom: «два танки замість одного»`.
- КОЛИ `counter(lives, ==, 0)` → ТО `game_over`.
- Перемога: пройти 8 раундів. · Поразка: 5 життів втрачено. · Рахунок: закриті коробки, бонус 250 × коробки (через леді або коридор), рахунок тане без вікна.

## Керування і ввід
- Джойстик — біг; вбігання у ворота повертає їх (окремої кнопки нема (?)).
- Atari: START — гра, OPTION — складність Novice / Tough / Super, SELECT — старт з вищого рівня, пробіл — пауза (рух джойстика — продовжити), R — рестарт.

## Вікна, меню, HUD
- `splash-screen` — титул; `difficulty-select` через OPTION (Novice / Tough / Super); вибір стартового рівня через SELECT.
- `game-screen` — решітка в рамці з танками; HUD: `score`, `lives`, назва раунду (`level-number`) (?).
- `custom-window` «Dark corridor» — сітка полонених, gorgolytes.
- `custom-window` бонус-екран (`+window:bonus-round`) — 250 × коробки, далі наступний раунд.
- `pause-menu` — пауза пробілом, без меню.
- Переходи: титул → решітка → (усі коробки / діамант) вікно → коридор → (усі визволені) бонус → решітка наступного раунду; решітка → (леді) бонус → наступний раунд; коридор → (спіймали) решітка.

## Фічі поза полем
- `levels-sequential` — 8 раундів-самоцвітів (у мануалі названо 7: Sapphire, Ruby, Emerald, Topaz, Peridot, Agate, Amethyst).
- `difficulty-presets` (Novice / Tough / Super) + старт з вищого рівня (SELECT).
- `pause`, `restart-level` (R перезапускає гру).
- Нема збережень, рекордів (?), 2P (?).

## Варіації й родичі
- Портовано на Apple II і C64 (1984, U.S. Gold у Британії). Автор — Kelly Jones (Synapse).
- Родичі: Lady Bug (турнікети, що крутить лише гравець), Dots and Boxes (замкнути клітинку четвертою стороною), Amidar (фарбування замкнених прямокутників), Kwirk (турнікети в головоломці).
- Осі варіацій:
  - **хто крутить ворота**: лише гравець (Lady Bug) / усі, але зараховує лише гравець (Drelbs);
  - **навіщо замикати**: відрізати переслідувачів (Lady Bug) / коробки — ціль і очки (Drelbs, Amidar);
  - **що руйнує зроблене**: нічого / ворог, що вселяється в коробку (gorgolyte).

## Цікавинки для курсу
- Решітка воріт на шарнірах: поворот 90° від поштовху, оновлення стін обох сусідніх клітин — 📎.
- Детектор «клітину закрито з 4 боків» після кожного повороту + хто зробив останній поворот — 🌱 логіка, 📎 з анімацією пульсації.
- Ворог, який крутить ті самі ворота, — переслідувач, що змінює поле під собою (перерахунок шляху) — 🥉.
- Кулі, що рикошетять від воріт, — відбиття на сітці зі змінними стінами — 📎.
- Вікно-портал на дальньому боці + рахунок, що тане, поки ти не встиг, — 🌱.
- Другий екран-режим (коридор) зі своїми правилами і поверненням на решітку при невдачі — 📎.

## Мапа на каталог
- Є: `move-4dir`; `chase-player` ↔ trollaboars; `enemy-patrol` ↔ танки по рамці; `projectile-shot` ↔ кулі; `touch-death` · `player-death` ↔ 5 життів; `temporary-modes` ↔ серце; `event-points`; `sequential-levels` ↔ 8 раундів; `progress-acceleration` ↔ 2 танки; `difficulty-levels` + `difficulty-select` ↔ Novice/Tough/Super; `game-pause` ↔ пробіл; `game-screen`.
- **Нема** → пропозиції карток:
  - `+grid-line-field` (Amidar) — ворота на ребрах, коробки — грані.
  - `+turnstile-gate` (Lady Bug) · слот {who: all} — тут крутять і вороги.
  - `+close-box-cells` «Замкнути клітинку чотирма стінками» · game-logic/score · 📎 · слот {who_counts: player}.
  - `+trap-escape-timer` (Heiankyo Alien) — trollaboar у замкненій коробці.
  - `+ricochet-shot` — кулі від воріт.
  - `+box-destroyer-enemy` «Ворог руйнує зроблене гравцем» · entities/interact · 🌱.
  - `+timed-portal` «Тимчасовий портал на інший екран» · levels/transition · 📎 · слот {far_side: bool}.
  - `+score-drain` «Рахунок тане, доки не діяти» · game-logic/score · 🌱.
  - `+captive-rescue` «Визволити полонених дотиком (рядом)» · game-logic/win · 🌱.
  - `+bonus-stage` (Clu Clu Land).

## Пропозиції до словників
- `+window:bonus-round` — бонус-екран після раунду (250 × коробки).
- `+card:close-box-cells`, `+card:box-destroyer-enemy`, `+card:timed-portal`, `+card:score-drain`, `+card:captive-rescue` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Drelbs](https://en.wikipedia.org/wiki/Drelbs) — ворота на 90°, коробки, trollaboars крутять, але не замикають, танки по рамці, dark corridor, mystery lady, 8 раундів-самоцвітів, 3 складності, автори портів.
- [Скан мануалу Synapse (archive.org)](https://archive.org/details/drelbs-synapse/) — atomic flip grid, серця на 5 с, діаманти, gorgolytes руйнують коробки, вікно, коридор, бонус 250 × коробки, 5 життів, клавіші START/OPTION/SELECT/пробіл/R.
- [ROM Magazine #6, огляд](http://www.atarimagazines.com/rom/issue6/product_reviews.php) — рахунок тане без вікна, зелений gorgolyte розбирає коробки, 2 танки на наступному рівні, кулі в коридорі.
- [256 Colors: огляд C64](https://256colors.wordpress.com/2009/05/28/review-drelbs-c64-by-kelly-jones-miriam-nathan-william-mandel-published-by-synapse-software/) — ворота навколо центрального шарніру, вікно завжди далеко від гравця, прохід рядом у коридорі звільняє ряд.
- YouTube: пошук «Drelbs Atari gameplay».

## Непевне
- (?) Чи вбиває дотик trollaboar — мануал лише радить триматися подалі; ROM-огляд теж не каже.
- (?) Які саме ворота повертаються при «hop» (ті, у які вбіг, чи сусідні) і в який бік — за годинниковою чи від напрямку руху.
- (?) Очки за коробку, за визволеного дрелба; чи є таймер у коридорі — у джерелах лише бонус 250 × коробки.
- (?) 8 раундів за Wikipedia, але мануал (OCR) називає 7 самоцвітів.
- (?) Чи є 2P і таблиця рекордів.
