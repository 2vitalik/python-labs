---
title: Kickle Cubicle (迷宮島)
slug: kickle-cubicle
family: grid-platformer
also: [push-slide, maze-arcade]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: none
  goal: collect
year: 1988
platforms: [arcade (1988), NES/Famicom (1990)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Kickle_Cubicle", best: true, note: "морозне дихання, вороги → лід, лід у воду → суходіл, крижаний стовп, Dream Bags, 4 землі + special"}
  - {kind: other, url: "https://ja.wikipedia.org/wiki/迷宮島", note: "JP: 3 мішки на рівень, причини втрати життя (ворог, ковзний лід, час), 4 землі по 16–17 рівнів, боси, 20 special"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=kickle+cubicle+nes+gameplay", note: "пошук; геймплей NES"}
stage: v1
coverage: 60
mechanics: [move-4dir, inertia-slide, push-object, collect-all, touch-death, player-death, time-out, enemy-patrol, chase-player, spawn-points, cell-transform, sequential-levels, level-select, status-panel, goal-counter, game-screen, end-screen, +freeze-into-block, +bomb-kick, +crush-by-slide, +create-destroy-block, +fill-hole-with-block, +boss-fight, +kick-in-place]
proposes: ["+effect:slide", "+effect:set_cell", "+effect:freeze", "+effect:place", "+trigger:enter", "+trigger:after", "+role:terrain", "+role:hazard", "+role:spawner", "+role:boss", "+ui:lives", "+ui:timer-countdown", "+card:fill-hole-with-block", "+card:freeze-into-block"]
author: opus
date: 2026-11-02
---

# Kickle Cubicle — заморожуй ворогів у кубики, копай ними і засипай море, щоб дійти до мішків

## Суть
Зверху видно крижаний острівець серед моря; Кікл має зібрати 3 Dream Bags. Морозним диханням він перетворює ворогів на крижані кубики, а копняком пускає кубик ковзати до упору: ковзний кубик збиває ворогів на шляху, а впавши в море — **стає новою клітиною суходолу**. Ще Кікл ставить перед собою крижаний стовп як тимчасовий блок. Ядро — пазл «звідки заморозити, куди штовхнути, щоб і розчистити шлях, і добудувати міст», під тиском часу й рухомих ворогів.

## Поле і час
- Один екран, вид зверху, квадратна сітка (≈ 10×? клітин (?)); острів — суходіл, навколо й усередині — вода.
- Real-time: вороги ходять, рівень має таймер; пазл детермінований (?), але вимагає точних дій.
- Шари: вода/суходіл (terrain, змінюється), нерухомі камені/стовпи (static), рухомі (вороги, кубики), мішки (pickup).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Кікл | player | життя, таймер | рух 4 напрямки; дихання; копняк; ставить/прибирає крижаний стовп |
| Dream Bag | pickup | 3 на рівень | взяти всі → рівень пройдено |
| Вода (море) | terrain | — | непрохідна для Кікла; кубик, що впав, → суходіл |
| Суходіл/лід-підлога | terrain | — | ходять Кікл і вороги |
| Крижаний кубик | object | — | з замороженого ворога; копняк → `slide` до упору; збиває ворогів; у воду → суходіл |
| Крижаний стовп | object | один за раз (?) | Кікл ставить перед собою як блок; ще раз — прибирає (?) |
| Камінь (base rock) | static | — | нерухомий блок; зупиняє кубики (?) |
| Пружина/відбивач | static | — | змінює напрямок ковзного кубика (?) |
| Молоток | static | — | відбиває кубик назад (?) |
| Noggle | enemy | — | ходить островом; заморожується в кубик |
| Незаморожувані вороги (Sparky, Rocky …) | enemy | — | дихання не діє; гинуть від ковзного кубика (?) |
| Генератор ворогів | spawner | — | випускає нових (?) |
| Бос землі | boss | фази атак | атакує предметами; Кікл кидає їх назад копняком |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next)` і `not cell(next, water)` → ТО `move(kickle, dir)`; інакше `block`.
- КОЛИ `input(breath)` → ТО `custom: «хмара холоду летить уперед»`; КОЛИ `contact(breath, freezable_enemy)` → ТО `transform(enemy → ice_cube)`.
- КОЛИ `input(kick)` → ЯКЩО `facing(kickle, ice_cube)` → ТО `slide(cube, dir)` до упору (Кікл лишається на місці).
- КОЛИ `contact(sliding_cube, enemy)` → ТО `disappear_b`, `score(+n)` (?).
- КОЛИ `enter(sliding_cube, water)` → ТО `disappear_a`, `set_cell(water → land)`.
- КОЛИ `blocked(sliding_cube)` → ТО `custom: «стоп; на пружині/молотку — розворот»` (?).
- КОЛИ `input(pillar)` → ЯКЩО `free(cell_ahead)` → ТО `spawn_at(ice_pillar, cell_ahead)`; на наявному стовпі → `disappear_b` (?).
- КОЛИ `contact(enemy, kickle)` → ТО `lose` (life −1, рестарт рівня).
- КОЛИ `contact(sliding_cube, kickle)` → ТО `lose` (JP wiki).
- КОЛИ `counter(time, ==, 0)` → ТО `lose`.
- КОЛИ `custom: «заморожений ворог відтає за N тіків»` → ТО `transform(cube → enemy)` (?).
- КОЛИ `contact(kickle, bag)` → ТО `pickup`, `counter(bags_left, -1)`; КОЛИ `counter(bags_left, ==, 0)` → ТО `win`, `next_level`.
- КОЛИ `custom: «усі рівні землі пройдено»` → ТО `window(boss_stage)` — бій з босом.
- Перемога: 3 мішки. Поразка: ворог, ковзний лід, час; життя скінчились → `game_over`. Рахунок: очки за ворогів і мішки (?).

## Керування і ввід
- Хрестовина — рух; B — морозне дихання (?); A — копняк / крижаний стовп (?) — розкладка не перевірена.
- Start — пауза.

## Вікна, меню, HUD
- `splash-screen` → `main-menu`: 1 Player / 2 Players (почергово (?)).
- `custom-window` «мапа землі»: острови-рівні (у JP-версії рівні землі в будь-якому порядку, у NA/EU — фіксований порядок).
- `game-screen`: острів; HUD — `lives`, `timer-countdown`, `remaining-counter` мішків (?), `score` (?).
- `end-screen` рівня; `end-screen` game over; бос-екран землі.
- Переходи: main-menu → мапа землі → game-screen → (3 мішки) → мапа; (усі рівні землі) → бос → наступна земля; (життя 0) → game over.

## Фічі поза полем
- 4 землі (Vegetable 17, Fruit 17, Sweets 16, Toy 17 за JP wiki) + бос у кожній; після всіх — Special Game (20 за JP / 30 за EN wiki) складніших рівнів.
- `level-select` у межах землі (лише JP-версія — довільний порядок).
- Життя, таймер, рахунок; паролі/збереження — (?).
- Аркада 1988 і NES 1990 відрізняються складом рівнів (JP — більше ворогів).

## Варіації й родичі
- Pengo (штовхнути лід, розчавити ворога), Adventures of Lolo (вороги, перетворені на яйце-блок, можна штовхати й топити у воді), Fire 'n Ice / Solomon's Key 2 (вогонь і лід), Toki Tori (Freeze-O-Matic: ворог → блок), Chip's Challenge (блок у воду → земля).
- Осі: **що стає блоком** (стіна / ворог / предмет); **рух блока після удару** (на 1 / до упору); **що робить блок у воді** (тоне / стає землею / пливе); **хто гине від ковзного блока** (ворог / гравець / обидва).

## Цікавинки для курсу
- Ворог → кубик → ковзання → суходіл: ланцюг із 3 трансформацій однієї сутності — 🥉.
- Кубик засипає воду (`set_cell`) — рельєф, що будується гравцем — 📎.
- Ковзний кубик як снаряд: збиває ворогів і гравця на шляху — 📎 (родич `+crush-by-slide`).
- Крижаний стовп «поставити/прибрати перед собою» — 🌱.
- Розвертання ковзного кубика пружинами — 📎 (сімʼя `+turn-when-blocked`).
- Перевірка «рівень ще розвʼязний» (не вистачає ворогів-кубиків на міст) — 🥇.

## Мапа на каталог
- Є: `move-4dir` · `inertia-slide` (кубик) · `push-object` (копняк) · `collect-all` (мішки) · `touch-death` · `player-death` · `time-out` · `enemy-patrol` / `chase-player` (?) · `spawn-points` (?) · `cell-transform` (вода → суходіл) · `sequential-levels` · `level-select` · `status-panel` · `goal-counter` · `game-screen` · `end-screen`.
- **Нема** → пропозиції карток:
  - `+freeze-into-block` «Ворог → блок» · entities/interact · 🥉 (є з Toki Tori).
  - `+bomb-kick` «Штовхнути ногою, ковзає до упору» · entities/legality · 📎 — тут для кубика.
  - `+kick-in-place` «Поштовх без кроку» · entities/legality · 🌱.
  - `+crush-by-slide` «Розчавити ковзним обʼєктом» · entities/combat · 📎.
  - `+create-destroy-block` «Створити/прибрати блок перед собою» · entities/interact · 📎 — крижаний стовп.
  - `+fill-hole-with-block` «Блок засипає воду/яму» · entities/interact · 📎 — Kickle, Chip's Challenge, Sokoban-варіанти.
  - `+boss-fight` «Бій з босом у кінці світу» · game-logic/waves · 🥉.

## Пропозиції до словників
- `+effect:slide` — кубик до упору; `+effect:set_cell` — вода → суходіл; `+effect:freeze` (уточнення `transform` для «ворог → блок» з можливим відтаванням); `+effect:place` — крижаний стовп.
- `+trigger:enter` — кубик заходить у воду; `+trigger:after` — після `slide` перевірка напрямку.
- `+role:terrain` (вода/суходіл), `+role:hazard` (ковзний кубик для гравця), `+role:spawner`, `+role:boss`.
- `+ui:lives`, `+ui:timer-countdown`.
- `+card:fill-hole-with-block`, `+card:freeze-into-block`.

## Джерела
- ⭐ [Wikipedia: Kickle Cubicle](https://en.wikipedia.org/wiki/Kickle_Cubicle) — дихання, заморожені вороги як доріжки над водою і зброя, крижаний стовп-блок, 4 землі з босами, Special Game, регіональні відмінності.
- [ja.wikipedia: 迷宮島](https://ja.wikipedia.org/wiki/迷宮島) — 3 мішки, причини смерті (ворог, ковзний лід, час), кількість рівнів по землях, боси, 20 special, аркада 1988 / Famicom 1990.
- YouTube: пошук «kickle cubicle nes gameplay».

## Непевне
- (?) Імена й поведінка ворогів (Noggle, Sparky, Rocky, Hoople, Max тощо) — з брифу куратора і памʼяті; жодне джерело в доступі їх не описує.
- (?) Пружини, молотки, base rocks — чи є і як саме відбивають кубик; «стовпи, які можна штовхати» з брифу не підтверджено.
- (?) Розкладка A/B, відтавання кубиків, генератори ворогів, ліміт крижаних стовпів, рахунок.
- (?) Розбіжність Special Game: 20 (JP) vs 30 (EN) рівнів.
- WebSearch вичерпано; StrategyWiki (403), HG101 (обслуговування), fandom (402) недоступні.
