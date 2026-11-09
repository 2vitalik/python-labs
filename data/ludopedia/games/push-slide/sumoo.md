---
title: SUMOO
slug: sumoo
aka: []
family: push-slide
also: [falling-match, word-number]
klass: cursor
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2026
platforms: [PC, Mac, Linux]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/5108270/", best: true, note: "опис: числа ковзають і додаються, точне число на цілі; камені, ями, портали, множники; 100 рівнів / 10 глав; є демо"}
  - {kind: other, url: "https://steamcommunity.com/stats/5108270/achievements", note: "досягнення = назви глав: Sums, Minus, Stones, Pits, Anchors, Gates, Portals, Multiply, Divide, Cracks"}
  - {kind: other, url: "https://steamcommunity.com/app/5108270/reviews/?browsefilter=toprated&filterLanguage=all", note: "відгуки: усі плитки рухаються разом, від'ємні числа, камінь у яму, підказки"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=SUMOO+puzzle+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [swipe-all-shift, inertia-slide, keyboard-controls, impassable-cells, tile-merge, fill-hole, teleport, one-way-cell, destructible-blocks, undo-unlimited, restart-level, level-select, level-unlock, +move-all-with-player, +value-goal, +sum-merge, +negative-values, +anchored-tile, +value-modifier-cell, +solve-hint]
proposes: ["+cond:sum_eq", "+effect:add_value", "+effect:crack", "+ui:target-number", "+feature:hint", "+card:sum-merge", "+card:anchored-tile", "+card:value-modifier-cell"]
author: opus
date: 2026-11-09
---

# SUMOO — один натиск, і всі числа ковзають до упору; зіткнулись — додались; доведи на ціль рівно потрібне число

## Суть
Мінімалістичний сітковий пазл: напрямок вводу зсуває **всі** числові плитки до упору (стіна або інша плитка), а плитки, що зіткнулись, **додаються** в одну. Мета — привести на клітину-ціль плитку з точно заданим значенням. Кожна з 10 глав вводить один елемент: відʼємні числа, камені, ями, якорі, односторонні ворота, портали, ×2, ½, тріснуті стіни. Порівняння з 2048 очевидне, але тут поле — лабіринт зі стінами, а мета — точна арифметика, а не максимум.

## Поле і час
- Квадратна сітка: білі клітини — підлога, чорні — стіни; спецклітини (ціль, яма, портал, ×2, ½, ворота).
- Хід = один ввід напрямку; усі плитки ковзають одночасно до упору, далі злиття (`time: turn`); без ліміту часу й ходів.
- 100 рівнів: 10 глав по 10, у межах глави відкриті рівні можна проходити в будь-якому порядку.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Числова плитка | tile | значення (може бути відʼємним) | ковзає з усіма до упору; зіткнувшись з іншою, зливається в суму |
| Ціль (вихід) | terrain | цільове число | рівень пройдено, коли на ній плитка з точно цим значенням |
| Стіна (чорна) | static | — | зупиняє ковзання; у загороджені кути «паркують» зайві плитки |
| Камінь | object | — | рухається разом із плитками, але не зливається; блокує шлях; закриває яму |
| Яма | hazard | — | ковтає числову плитку; камінь у ямі → підлога |
| Якір / закріплена плитка | tile | значення | не рухається; інші плитки зливаються в неї |
| Одностороння брама | gate | напрямок | пропускає плитку лише в один бік |
| Портал | terrain | пара | переносить плитку посеред ковзання, рух триває з виходу |
| Клітина ×2 | terrain | — | подвоює значення плитки, що в неї вʼїхала |
| Клітина ½ | terrain | — | ділить значення навпіл |
| Тріснута стіна | static | — | можна проломити (умова — (?)) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ТО `slide(all_tiles, dir)` разом із каменями — кожна до упору.
- КОЛИ `contact(moving_tile, tile)` → ТО `merge(moving_tile, tile → tile(sum))` (слово — `+effect:add_value`); камінь і стіна → `block`.
- КОЛИ `contact(moving_tile, anchored_tile)` → ТО `merge` у якір; якір лишається на місці.
- КОЛИ `custom: «злиття дало 0»` → ТО `custom: «плитка з нулем»` — поведінка (зникає?) — (?).
- КОЛИ `enter(tile, pit)` → ТО `disappear(tile)`; КОЛИ `enter(stone, pit)` → ТО `disappear(stone)`, `set_cell(pit, floor)`.
- КОЛИ `enter(tile, portal)` → ТО `teleport(tile, pair_portal)`, ковзання триває.
- КОЛИ `enter(tile, one_way_gate)` → ЯКЩО `not moving(tile, gate_dir)` → ТО `block`.
- КОЛИ `enter(tile, x2_cell)` → ТО `set_value(tile, value×2)`; КОЛИ `enter(tile, half_cell)` → ТО `set_value(tile, value/2)`.
- КОЛИ `contact(tile, cracked_wall)` → ЯКЩО `custom: «умова пролому»` (?) → ТО `set_cell(cracked_wall, floor)` (слово — `+effect:crack`).
- КОЛИ `turn_end` → ЯКЩО `occupied(goal, tile)` і `custom: «значення = цільовому»` (слово — `+cond:sum_eq`) → ТО `win`, `unlock(next_level)`.
- КОЛИ `input(undo)` → ТО `undo(1)` (без ліміту); КОЛИ `input(restart)` → ТО `restart`.
- Перемога: точне число на цілі. · Поразка: нема; перебір або плитка в ямі → undo/рестарт. · Рахунок: нема.

## Керування і ввід
- Напрямок (стрілки/WASD?) — зсув усього поля; undo — по кроку, без ліміту; миттєвий рестарт.
- Підказка — кнопка: показує напрямок розвʼязку або проходить рівень за тебе.

## Вікна, меню, HUD
- `level-select` (`puzzle-select`) — 10 пакетів × 10 рівнів, у пакеті відкриті рівні — у будь-якому порядку.
- `game-screen` — поле; HUD: `target-number` на цілі (число в клітині), кнопки undo/рестарт/підказка (?).
- `hints-window` — підказка або автопроходження рівня (без ліміту).
- `settings-window` — мова (30 мов) (?).

## Фічі поза полем
- `undo` (∞, покроково), `restart-level`, `hint` (∞, аж до `auto-solve`); ні таймера, ні ліміту ходів.
- `level-unlock` по главах; глава = одна нова механіка.
- `achievements` (24, 2 приховані): по главі + дії («злий до нуля», «виріс до 20+», «пройди без undo», «закрий яму каменем»); `cloud-save`, `localization` (30 мов), демо.

## Варіації й родичі
- Родичі: `2048` і `threes` (усі плитки зсуваються, злиття), `ice-sliding-puzzles` (ковзання до упору), `tomb-of-the-mask`, `block-in-the-lock` (усі блоки одним вводом).
- Осі варіацій:
  - **правило злиття**: однакові → подвоєння (`2048`) / 1+2, далі рівні (`threes`) / **будь-які → сума, зокрема відʼємні** (SUMOO);
  - **мета**: максимум / вижити / **точне значення в точці**;
  - **модифікатори клітин**: нема / ×2, ½, портал, яма, брама (SUMOO);
  - **поле**: порожній квадрат (`2048`) / **лабіринт зі стінами й кишенями**.

## Цікавинки для курсу
- Зсув усіх плиток до упору з порядком обробки від переднього краю — 📎 (як `2048`, але зі стінами).
- Злиття в суму з відʼємними й нулем + точна ціль — 🌱.
- Модифікатори на клітинах (×2, ½) і портал посеред ковзання — 📎.
- Яма, яку закриває камінь, що рухається з плитками — 📎.
- Якір: нерухома плитка-приймач — 🌱.
- Розвʼязувач/підказка: BFS по станах поля з 4 ходами — 🥉 (стан малий, але значення ростуть — потрібна межа).

## Мапа на каталог
- Є: `swipe-all-shift` ↔ один ввід зсуває всі; `inertia-slide` ↔ до упору; `keyboard-controls`; `impassable-cells` ↔ чорні стіни; `tile-merge` ↔ зіткнення → сума; `fill-hole` ↔ камінь у яму; `teleport` ↔ портали; `one-way-cell` ↔ брами; `destructible-blocks` ↔ тріснуті стіни; `undo-unlimited` + `restart-level`; `level-select` + `level-unlock` ↔ пакети.
- **Нема** → пропозиції карток:
  - `+move-all-with-player` (вже пропонована) · слот {mode: slide}.
  - `+value-goal` (вже пропонована) — точне число на цілі.
  - `+sum-merge` «Зіткнення плиток дає суму значень (і відʼємні)» · entities/legality · 🌱 — дитина `tile-merge`.
  - `+negative-values` «Відʼємні значення плиток» · entities/state · 🌱.
  - `+anchored-tile` «Нерухома плитка-приймач злиття» · entities/legality · 🌱.
  - `+value-modifier-cell` «Клітина змінює значення плитки (×2, ½)» · entities/interact · 📎 · слот {op}.
  - `+solve-hint` «Підказка напряму / автопроходження» · game-logic/difficulty · 🥉.

## Пропозиції до словників
- `+cond:sum_eq` — значення дорівнює цільовому (вже пропонована).
- `+effect:add_value` — зіткнення додає значення (×2 і ½ лягають у наявний `set_value`; `multiplier` у словнику — множник очок, не значення плитки).
- `+effect:crack` — пролом тріснутої стіни.
- `+ui:target-number` — цільове число, намальоване на клітині-цілі.
- `+feature:hint` — підказка без ліміту, аж до автопроходження.
- `+card:sum-merge`, `+card:anchored-tile`, `+card:value-modifier-cell` — див. «Мапа на каталог».

## Джерела
- ⭐ [Steam: SUMOO](https://store.steampowered.com/app/5108270/) — «числа ковзають, зустрічаються й додаються», до стіни чи плитки, точне число на цілі, камені, ями, портали, множники, 100 рівнів / 10 глав, undo без ліміту, миттєвий рестарт; Duck Tile / Mindlabor, 26.10.2026.
- [Steam API appdetails](https://store.steampowered.com/api/appdetails?appids=5108270) — той самий опис, 24 досягнення, демо.
- [Steam: досягнення](https://steamcommunity.com/stats/5108270/achievements) — глави Sums…Cracks, «Merge into an anchored block», «one-way gate», «×2 tile», «half tile», «cracked wall», «exactly zero», «20 or beyond».
- [Steam: відгуки](https://steamcommunity.com/app/5108270/reviews/?browsefilter=toprated&filterLanguage=all) — плитки рухаються разом, відʼємні з 2-ї глави, камінь з 3-ї, ями з 4-ї, підказки без ліміту, порядок у пакеті вільний.
- YouTube: пошук «SUMOO puzzle gameplay».

## Непевне
- (?) Порядок глав після 4-ї (Anchors, Gates, Portals, Multiply, Divide, Cracks) — за порядком досягнень; підтверджено лише 1–4.
- (?) Що стається з плиткою «0» і з перебором на цілі; чи злиття в ланцюжку відбувається кілька разів за хід.
- (?) Що треба, щоб проломити тріснуту стіну (значення плитки? удар?); що таке «блоки-знищувачі» з китайського відгуку — може, ями.
- (?) Клавіші керування й наявність миші/свайпа — не бачив.
- Рік 2026 збігається з датою релізу 26.10.2026; гра свіжа (9 відгуків на момент запису).
