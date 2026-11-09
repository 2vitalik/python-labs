---
title: Kaggle Crawl
slug: kaggle-crawl
aka: [Crawl, Maze Crawler]
family: program-robots
also: [maze-arcade, tactics]
klass: figure
axes:
  field: square
  time: programmed
  opponent: online
  info: hidden
  random: both
  goal: survive
year: 2026
platforms: [web, local CLI]
links:
  - {kind: official, url: "https://github.com/Kaggle/kaggle-environments/tree/master/kaggle_environments/envs/crawl", best: true, note: "середовище: README з правилами, crawl.py, crawl.json, агенти, візуалізатор"}
  - {kind: other, url: "https://raw.githubusercontent.com/Kaggle/kaggle-environments/master/kaggle_environments/envs/crawl/README.md", note: "повні правила: роботи, дії, бій-розчавлення, шахти, туман, порядок фаз, конфіг"}
  - {kind: other, url: "https://raw.githubusercontent.com/Kaggle/kaggle-environments/master/kaggle_environments/envs/crawl/crawl.py", note: "алгоритм Еллера по рядках з дзеркалом, нескінченна прокрутка, рух і бій, обмін місцями"}
  - {kind: other, url: "https://raw.githubusercontent.com/Kaggle/kaggle-environments/master/kaggle_environments/envs/crawl/crawl.json", note: "опис, 2 агенти, 3 с на хід, схема дій"}
  - {kind: other, url: "https://github.com/Kaggle/kaggle-environments/commits/master/kaggle_environments/envs/crawl", note: "історія: додано 27.04.2026, зміни до 12.06.2026"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=kaggle+crawl+maze+environment", note: "пошук"}
stage: v1
coverage: 75
mechanics: [move-4dir, impassable-cells, maze-generation, infinite-field, fog-of-war, item-pickup, environment-death, round-currency, replay, state-as-data, game-loop, +auto-scroll-boundary, +edge-walls, +build-remove-walls, +crush-hierarchy, +same-type-annihilation, +swap-pass-through, +unit-becomes-building, +mine-generator, +energy-transfer, +energy-upkeep-idle, +jump-over-walls, +cooldown-per-action, +move-period-per-type, +vision-memory-split, +symmetric-map-generation, +simultaneous-hidden-orders, +turn-time-limit, +tiebreak-cascade, +local-referee]
proposes: ["+cond:greater(a, b, prop)", "+cond:cooldown_ready(a)", "+cond:visible(cell)", "+effect:transfer(a, b, res, n)", "+effect:scroll(dir)", "+effect:set_edge(cell, dir, wall)", "+trigger:scroll_step", "+window:replay-viewer"]
author: opus
date: 2026-11-09
---

# Crawl — лабіринт сам повзе на північ і зʼїдає все позаду: фабрика будує розвідників, робітників і майнерів, хто втратив фабрику — програв

## Суть
Kaggle-середовище 2026 року для двох ботів: дзеркальний лабіринт 20×20 у тумані війни, нижня межа якого щораз зсувається на північ, знищуючи роботів, шахти й кристали. Кожен гравець має фабрику з енергією 1000, що будує роботів трьох типів: швидкого розвідника, робітника, який ставить і знімає стіни, і майнера, що перетворюється на шахту на рідкісному вузлі. Роботи в одній клітині розчавлюють слабших за ієрархією Фабрика > Майнер > Робітник > Розвідник, однакові знищують один одного — навіть свої. Виживає той, чия фабрика встигає тікати від межі; якщо обидві дожили до кінця — рахують енергію.

## Поле і час
- Вікно 20×20 нескінченного лабіринту від `southBound` до `northBound`; кожен зсув додає згенерований рядок на півночі й видаляє рядок під південною межею.
- Стіни — на **ребрах** клітин: 4 біти на клітину (N=1, E=2, S=4, W=8), ребро спільне для двох сусідів.
- Генерація: алгоритм Еллера по рядках на лівій половині, потім дзеркало на праву (E↔W); центральна вісь — стіна з «дверима» з імовірністю 8 %; периметр і вісь — незмінні стіни.
- Кристали — 6 % клітин, вузли для шахт — 3 % (не на кристалах).
- Прокрутка: інтервал лінійно падає з 10 ходів до 2 за перші 450 кроків, далі кожні 2 ходи до кінця (крок 500).
- Хід: обидва боти шлють дії одночасно; 12 фаз (кулдауни → валідація → енергія → спецдії → рух і бій → кристали → шахти → генерація → прокрутка → знищення за межею → перевірка перемоги → спостереження).
- Туман: видимість — манхеттенська відстань, обʼєднана по всіх своїх роботах.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Фабрика | spawner | енергія 1000 (без максимуму), рух раз на 2 ходи, зір 4 | будує роботів (кулдаун 10), стрибає на 2 клітини крізь стіни (кулдаун 20); не розчавлюється ніким, крім ворожої фабрики |
| Розвідник (Scout) | piece | ціна 50, макс. енергія 100, рух щоходу, зір 5 | швидка розвідка |
| Робітник (Worker) | piece | ціна 200, макс. 300, рух раз на 2, зір 3 | ставить / знімає стіну на ребрі за 100 енергії |
| Майнер (Miner) | piece | ціна 300, макс. 500, рух раз на 2, зір 3 | `TRANSFORM` на вузлі → шахта (100 енергії) |
| Шахта | resource | +50 енергії за хід, запас до 1000 | свій робот на ній забирає енергію; запамʼятовується після виявлення |
| Вузол для шахти | resource | — | рідкісний; видно лише в зорі; зникає під шахтою |
| Кристал | pickup | 10–50 енергії | бере той, хто вижив у клітині; не запамʼятовується |
| Стіна | static | на ребрі | блокує рух і передачу; робітник змінює |
| Незмінна стіна | static | периметр, центральна вісь | не змінюється |
| Двері | gate | 8 % на центральній осі | прохід між половинами |
| Південна межа | hazard | `southBound` | усе нижче знищено; фабрика нижче — вибування |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start` → ТО `custom: «кожен бот повертає словник uid робота → рядок дії»`; невалідна дія → `IDLE`.
- КОЛИ `tick` → ТО `custom: «кулдауни −1»`, потім `counter(energy, −1)` кожному роботу (не нижче 0).
- КОЛИ `counter(energy, ==, 0)` → ТО `custom: «примусовий IDLE»`; робот не гине, може отримати енергію з кристала, шахти чи передачі.
- КОЛИ `input(BUILD_SCOUT | BUILD_WORKER | BUILD_MINER [_DIR])` → ЯКЩО `custom: «нема стіни в напрямку, клітина у вікні, кулдаун будівництва 0»` and `has(factory, energy ≥ ціна)` → ТО `spawn_at(robot, сусідня клітина)` (без суфікса — на північ), енергія ціни переходить роботу; кулдаун 10; новий робот стоїть до руху й бере участь у бою.
- КОЛИ `input(JUMP_DIR)` → ЯКЩО `custom: «кулдауни руху й стрибка 0»` → ТО `teleport(factory, 2 клітини в напрямку)` крізь стіни, кулдаун 20; приземлення поза вікном → `disappear(factory)`.
- КОЛИ `input(BUILD_DIR)` робітника → ЯКЩО `custom: «ребро не незмінне»` → ТО `custom: «стіна на ребрі»`, `counter(energy, −100)`; `REMOVE_DIR` — прибрати стіну за 100; плата знімається навіть без зміни.
- КОЛИ `input(TRANSFORM)` → ЯКЩО `occupied(cell, mining_node)` and `has(miner, energy ≥ 100)` → ТО `transform(miner, mine)`, решта енергії майнера — у шахту (до 1000), вузол зникає.
- КОЛИ `input(TRANSFER_DIR)` → ЯКЩО `occupied(neighbor, own_robot)` and `custom: «між ними нема стіни»` → ТО `custom: «уся енергія переходить сусіду до його максимуму»`.
- КОЛИ `input(NORTH | SOUTH | EAST | WEST)` → ЯКЩО `custom: «нема стіни на ребрі, кулдаун руху 0»` → ТО `move(robot, dir)`; стіна → `block`.
- КОЛИ `edge(robot)` (північний чи південний край вікна) → ТО `disappear(robot)`.
- КОЛИ `custom: «два роботи міняються клітинами»` → ТО `custom: «проходять крізь один одного без бою»`.
- КОЛИ `contact(a, b)` (закінчили хід в одній клітині, будь-які власники) → ЯКЩО `custom: «тип A вищий за B: Factory > Miner > Worker > Scout»` → ТО `disappear(b)`.
- КОЛИ `contact(a, b)` → ЯКЩО `same(a, b, type)` → ТО `disappear(a)`, `disappear(b)` — і для своїх; дві ворожі фабрики гинуть обидві.
- КОЛИ `contact(robot, crystal)` → ЯКЩО `custom: «робот вижив у бою клітини»` → ТО `pickup(robot, crystal)`; ніхто не вижив — кристал зникає.
- КОЛИ `enter(own_robot, mine)` → ТО `custom: «робот забирає енергію шахти до свого максимуму»`; КОЛИ `tick` → ТО `custom: «шахта +50, максимум 1000»`.
- КОЛИ `timer(interval)` (10 → 2 за 450 кроків) → ТО `custom: «обидві межі +1; новий північний рядок за Еллером із seed + step; кристали й вузли на ньому»`.
- КОЛИ `custom: «обʼєкт нижче southBound»` → ТО `disappear(obj)`; фабрика → `lose` для власника.
- КОЛИ `turn_end` → ТО `reveal(cells у зорі своїх роботів)`; стіни запамʼятовуються назавжди, шахти — в останньому баченому стані, кристали, вузли й вороги — ні.
- КОЛИ `destroyed(factory)` → ЯКЩО `custom: «фабрика суперника жива»` → ТО `lose` власнику, `win` супернику.
- КОЛИ `custom: «обидві фабрики знищено в одному ході або дожили до кроку 500»` → ТО `custom: «тайбрейк: більше сумарної енергії → більше роботів → нічия»` (`win` / `draw`).
- Перемога: фабрика суперника знищена або тайбрейк · Поразка: своя фабрика знищена (межа, край, ворожа фабрика) · Рахунок: нагорода = сумарна енергія; тайбрейк 1 / 0.5 / 0.

## Керування і ввід
- Ввід — Python-агент Kaggle; дії — рядки на uid робота: `NORTH/SOUTH/EAST/WEST`, `BUILD_SCOUT/WORKER/MINER` (+ `_NORTH/_SOUTH/_EAST/_WEST`), `BUILD_DIR`/`REMOVE_DIR` (робітник), `TRANSFORM` (майнер), `TRANSFER_DIR`, `JUMP_DIR` (фабрика), `IDLE`.
- Спостереження: `walls` (біти, −1 — не відкрито), `crystals`, `robots` `[type, col, row, energy, owner, move_cd, jump_cd, build_cd]`, `mines`, `miningNodes`, `southBound`, `northBound`.
- 3 с на хід (`actTimeout`); локально — `kaggle_environments.make("crawl")`.

## Вікна, меню, HUD
- `replay-viewer` (візуалізатор у «пергаментній» темі): лабіринт, роботи кольорами гравців, межа прокрутки, панель керування відтворенням; швидкість за замовчуванням 5× (440 мс на крок).
- HUD реплею (?): енергія роботів, номер кроку, межі вікна.
- `leaderboard` Kaggle (якщо є змагання) (?).

## Фічі поза полем
- `local-referee`: відкритий код середовища, `seed-input` (прихований seed визначає всі нові рядки).
- Конфіг з 30 параметрами (ціни, кулдауни, зір, інтервали прокрутки, щільності) — `custom-rules` для навчальних варіантів.
- Нагорода по ходу = сумарна енергія — зручно для RL.

## Варіації й родичі
- Сімʼя арен Kaggle: [kaggle-kore-fleets](kaggle-kore-fleets.md), [lux-ai](lux-ai.md), Halite у [bot-arenas](bot-arenas.md); туман і рій — [ai-challenge-ants](ai-challenge-ants.md); роботи в темних коридорах — [duskers](duskers.md).
- Прокрутка, що зʼїдає поле, — як звуження зони в [battlesnake](battlesnake.md) (Royale) і поле, що зʼїдається, у [codingame-keep-off-the-grass](codingame-keep-off-the-grass.md).
- Осі варіацій: **поле** (статичне / прокрутка з прискоренням); **стіни** (на клітинах / на ребрах, змінні робітником); **бій** (ієрархія розчавлення / HP і шкода); **економіка** (кристали / шахти / передача між роботами); **кінець** (втрата бази / тайбрейк енергією).

## Цікавинки для курсу
- Лабіринт Еллера рядок за рядком з дзеркалом і дверима — 🥉 (нескінченна генерація з seed).
- Прокрутка вікна з лінійним прискоренням і знищенням позаду — 📎.
- Стіни на ребрах (4 біти, синхронізація сусідів) + робітник, що їх змінює — 🥉.
- Одночасний рух з обміном «крізь» і розчавленням за ієрархією, однакові гинуть разом — 🥈.
- Туман з різною памʼяттю для різних типів обʼєктів — 📎.
- Бот: фабрика тікає від межі, будує майнерів до вузлів і розвідників на кристали — 🥇.

## Мапа на каталог
- Є: `move-4dir` · `impassable-cells` · `maze-generation` · `infinite-field` (нескінченний лабіринт на північ) · `fog-of-war` · `item-pickup` (кристали) · `environment-death` (межа) · `round-currency` (енергія) · `replay` · `state-as-data` · `game-loop`.
- **Нема** → пропозиції карток:
  - `+symmetric-map-generation`, `+simultaneous-hidden-orders`, `+turn-time-limit`, `+local-referee` — з [bot-arenas](bot-arenas.md); `+cooldown-per-action` — з [lux-ai](lux-ai.md).
  - `+auto-scroll-boundary` «Межа поля сама зсувається й знищує все позаду» · levels/generation · 📎.
  - `+edge-walls` «Стіни на ребрах між клітинами» · entities/legality · 🥉.
  - `+build-remove-walls` «Юніт ставить і знімає стіни за ресурс» · entities/interact · 📎.
  - `+crush-hierarchy` «У клітині сильніший тип знищує слабших» · entities/combat · 🌱.
  - `+same-type-annihilation` «Однакові в клітині гинуть разом, навіть свої» · entities/combat · 🌱.
  - `+swap-pass-through` «Зустрічні проходять крізь один одного» · entities/move · 🌱.
  - `+unit-becomes-building` «Юніт перетворюється на споруду на спецклітині» · entities/interact · 📎.
  - `+mine-generator` «Споруда накопичує ресурс, свій юніт забирає» · game-logic/economy · 🌱.
  - `+energy-transfer` «Передати енергію сусідньому своєму юніту» · entities/interact · 🌱.
  - `+energy-upkeep-idle` «Енергія −1 щоходу, на нулі — бездіяльність» · entities/state · 🌱.
  - `+jump-over-walls` «Стрибок на 2 клітини крізь стіни з кулдауном» · entities/move · 📎.
  - `+move-period-per-type` «Рух раз на N ходів за типом» · entities/state · 🌱.
  - `+vision-memory-split` «Що з туману памʼятається, а що ні — за типом» · interface/render · 📎.
  - `+tiebreak-cascade` «Тайбрейк ланцюжком критеріїв» · game-logic/win · 🌱.

## Пропозиції до словників
- `+cond:greater(a, b, prop)` — ранг типу в ієрархії розчавлення (спільне з battlesnake, kore).
- `+cond:cooldown_ready(a)` — з lux-ai, підтвердження (рух, стрибок, будівництво).
- `+cond:visible(cell)` — з bot-arenas, підтвердження (туман).
- `+effect:transfer(a, b, res, n)` — з lux-ai, підтвердження.
- `+effect:scroll(dir)` — вікно поля зсувається: новий рядок згенеровано, старий з усім вмістом знищено.
- `+effect:set_edge(cell, dir, wall)` — поставити/прибрати стіну на ребрі клітини.
- `+trigger:scroll_step` — межа поля зсунулась (для правил «знищити все нижче»).
- `+window:replay-viewer` — підтвердження.

## Джерела
- ⭐ [kaggle-environments/envs/crawl](https://github.com/Kaggle/kaggle-environments/tree/master/kaggle_environments/envs/crawl) — тека середовища.
- [README.md](https://raw.githubusercontent.com/Kaggle/kaggle-environments/master/kaggle_environments/envs/crawl/README.md) — правила цілком: таблиця роботів, дії, бій, шахти, туман, 12 фаз, нагороди, конфіг.
- [crawl.py](https://raw.githubusercontent.com/Kaggle/kaggle-environments/master/kaggle_environments/envs/crawl/crawl.py) — Еллер з дзеркалом, вікно прокрутки, формула інтервалу, рух і бій, нуль енергії.
- [crawl.json](https://raw.githubusercontent.com/Kaggle/kaggle-environments/master/kaggle_environments/envs/crawl/crawl.json) — опис, 2 агенти, схема дій.
- [Історія комітів](https://github.com/Kaggle/kaggle-environments/commits/master/kaggle_environments/envs/crawl) — дата появи й зміни (уповільнення прокрутки, напрямки спавну).

## Непевне
- (?) Чи є публічне Kaggle-змагання на цьому середовищі — сторінки не знайшов; лінка на змагання нема.
- (?) Чи можуть ворожі роботи забирати енергію з чужої шахти — README каже лише про «friendly robots».
- (?) Ціни й швидкість прокрутки мінялись комітами травня 2026 («slow maze scroll speed», «tune unit carry capacity») — числа взято з поточного README.
- (?) Вигляд HUD візуалізатора — не відкривав.
