---
title: Lux AI Challenge
slug: lux-ai
aka: [Lux AI, Lux AI Season 1, Lux AI 2021, Lux AI S2, Lux AI S3]
family: program-robots
also: [build-sim, tactics]
klass: figure
axes:
  field: square
  time: programmed
  opponent: online
  info: full
  random: setup
  goal: score
year: 2021
platforms: [web, local CLI]
links:
  - {kind: other, url: "https://raw.githubusercontent.com/Lux-AI-Challenge/Lux-Design-S1/master/specs.md", best: true, note: "повні правила Season 1: ресурси й дослідження, робітник/візок, міста й нічне паливо, cooldown і дороги, 8 фаз ходу, 360 ходів"}
  - {kind: official, url: "https://github.com/Lux-AI-Challenge/Lux-Design-S1", note: "рушій, стартові набори 7 мов, візуалізатор, Kaggle-змагання до 06.12.2021"}
  - {kind: official, url: "https://github.com/Lux-AI-Challenge/Lux-Design-S2", note: "Season 2 (NeurIPS 2023): Jax-рушій, асиметричні карти, більші поля"}
  - {kind: official, url: "https://github.com/Lux-AI-Challenge/Lux-Design-S3", note: "Season 3: туман, best-of-5, приховані випадкові параметри"}
  - {kind: other, url: "https://raw.githubusercontent.com/Lux-AI-Challenge/Lux-Design-S3/main/docs/specs.md", note: "правила S3: 24×24, реліквії з прихованою маскою 5×5, sap, туманність, астероїди"}
  - {kind: official, url: "https://www.lux-ai.org/", note: "сайт змагання (рендериться JS)"}
  - {kind: other, url: "https://www.kaggle.com/c/lux-ai-2021", note: "Kaggle-змагання Season 1"}
  - {kind: other, url: "https://2021vis.lux-ai.org/", note: "візуалізатор реплеїв S1"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=lux+ai+challenge+kaggle", note: "пошук; реплеї й розбори"}
stage: v1
coverage: 70
mechanics: [move-4dir, impassable-cells, round-currency, inventory-limit, spawn-points, piece-capture, fog-of-war, replay, leaderboard, state-as-data, game-loop, +text-io-protocol, +turn-time-limit, +simultaneous-hidden-orders, +day-night-cycle, +upkeep-or-die, +adjacency-discount, +research-unlocks-resource, +cooldown-per-action, +road-speedup, +resource-regrowth, +unit-cap-by-buildings, +move-conflict-cancel, +adjacent-harvest, +hidden-random-params, +best-of-series, +energy-tiebreak-combat, +symmetric-map-generation, +local-referee, +time-bank]
proposes: ["+trigger:night_start", "+trigger:out_of_fuel(a)", "+cond:cooldown_ready(a)", "+cond:researched(resource)", "+cond:cargo_full(a)", "+effect:transfer(a, b, res, n)", "+effect:build_city(cell)", "+effect:pillage(cell)", "+effect:research(+1)", "+effect:sap(cell, n)", "+effect:eliminate(bot)", "+window:replay-viewer", "+ui:frame-scrubber", "+feature:bot-upload", "+feature:time-bank", "+feature:hidden-params"]
author: opus
date: 2026-11-09
---

# Lux AI — боти на Kaggle збирають ресурси вдень і палять їх уночі: місто без палива зникає разом з усіма клітинами

## Суть
Щорічне Kaggle-змагання ботів 1v1 (Season 1 — 2021). Робітники рубають дерево, добувають вугілля й уран із сусідніх клітин, везуть вантаж у місто й будують нові клітини-міста; кожні 40 ходів настає 10-ходова ніч, і кожна клітина міста й кожен юніт поза містом мусить спалити паливо — інакше зникає. Сусідні клітини міста палять менше, тож вигідно будувати купно, але одне голодне місто гине цілком. Виграє той, у кого більше клітин-міст після 360 ходів. Season 2 і 3 змінили правила повністю (див. «Варіації»).

## Поле і час
- Квадратна карта 12, 16, 24 або 32 клітини; (0,0) — лівий верхній кут, y вниз; карта симетрична відображенням по вертикалі чи горизонталі.
- Клітина: ресурс (дерево / вугілля / уран, кількість), дорога (рівень 0–6), клітина міста (власник), юніти.
- Хід = обидва боти дають накази, рушій застосовує їх одночасно за 8 фазами; 3 с на хід + спільний банк 60 с на перевищення.
- Цикл 40 ходів: 30 день + 10 ніч; матч — 360 ходів (9 циклів).
- Інформація повна (S1); туман зʼявився лише в S3.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Робітник (worker) | piece | вантаж ≤ 100, cooldown 2, ніч −4 палива/хід поза містом | рух 5 напрямків (N/E/S/W/центр); видобуток із сусідів; будує місто; грабує дорогу |
| Візок (cart) | piece | вантаж ≤ 2000, cooldown 3, ніч −10 палива/хід | возить вантаж; лишає дорогу (+0.75 рівня) |
| Клітина міста (CityTile) | spawner | власник, паливо, cooldown 10 | будує робітника/візок, дає +1 дослідження; уночі палить 23 − 5·(сусідні свої клітини) |
| Місто (City) | zone | спільне паливо звʼязних клітин | гине цілком, якщо паливо скінчилось |
| Дерево | resource | кількість, 1 паливо/од., 20 од./хід | без дослідження; відростає на 2.5 % (вгору), якщо < 500 і не вичерпане |
| Вугілля | resource | 10 палива/од., 5 од./хід | доступне після 50 очок дослідження |
| Уран | resource | 40 палива/од., 2 од./хід | доступний після 200 очок дослідження |
| Дорога | terrain | рівень 0–6 | зменшує cooldown юніта на клітині; на місті завжди 6 |
| Очки дослідження | resource | спільні на команду | відкривають вугілля й уран |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start` → ТО `custom: «рушій шле боту повний стан: ресурси, юніти, міста, дороги, номер ходу»`.
- КОЛИ `phase_start(city_actions)` → ЯКЩО `custom: «cooldown клітини < 1»` → ТО одна дія: `spawn_at(worker|cart, city_tile)` (ЯКЩО `count(units, <, city_tiles)`) або `counter(research, +1)`; cooldown += 10.
- КОЛИ `phase_start(unit_actions)` → ЯКЩО `custom: «cooldown юніта < 1»` → ТО одна дія: `move(a, dir)`, `custom: «transfer ресурсу сусідньому юніту до його вільного місця»`, `custom: «build city»` або `custom: «pillage»`; cooldown += базовий (уночі ×2).
- КОЛИ `exec(build_city)` → ЯКЩО `custom: «робітник із повним вантажем 100 на порожній клітині»` → ТО `set_cell(cell, city_tile)`, вантаж витрачено; сусідня своя клітина → `attach` до міста.
- КОЛИ `exec(move)` → ЯКЩО `custom: «двоє юнітів ідуть в одну не-міську клітину»` → ТО `block` для обох; ЯКЩО `occupied(target, enemy_city)` → ТО `block`; свої юніти можуть стояти купою на своєму місті й мінятися місцями з сусідом (`swap`).
- КОЛИ `exec(pillage)` → ТО `custom: «рівень дороги під робітником −0.5»`.
- КОЛИ `phase_start(roads)` → ЯКЩО `occupied(cell, cart)` → ТО `custom: «дорога +0.75, max 6»`.
- КОЛИ `phase_start(collect)` → ЯКЩО `custom: «ресурс у своїй або 4 сусідніх клітинах юніта/клітини міста»` and `has(team, research ≥ поріг)` → ТО `pickup` за порядком уран → вугілля → дерево; робітник на місті не добуває — добуває саме місто й одразу перетворює на паливо.
- КОЛИ `enter(unit, own_city)` → ТО `custom: «вантаж перетворюється на паливо міста»`.
- КОЛИ `phase_start(night)` → ЯКЩО `custom: «хід 31–40 циклу»` → ТО юніти поза містом палять вантаж (спершу найменш ефективний ресурс, лише цілими одиницями), міста — паливо.
- КОЛИ `custom: «юніту не вистачило палива вночі»` → ТО `disappear_a`.
- КОЛИ `custom: «місту не вистачило палива вночі»` → ТО `disappear_a` для всіх його клітин, дороги під ними → 0.
- КОЛИ `phase_start(regrow)` → ЯКЩО `cell(x, wood)` and `custom: «< 500 і не вичерпано»` → ТО `counter(wood, +2.5 %)`.
- КОЛИ `phase_start(cooldown)` → ТО `custom: «cooldown −(1 + рівень дороги), не нижче 0»`.
- КОЛИ `custom: «у команди 0 юнітів і 0 клітин міст»` → ТО `lose` негайно.
- КОЛИ `counter(turn, ==, 360)` → ТО `game_over`: більше клітин міст → `win`; рівно — більше юнітів; рівно — `draw`.
- КОЛИ `custom: «бот перевищив 3 с, і банк 60 с вичерпано»` → ТО `custom: «бот заморожений — накази більше не приймаються»`.
- Перемога: більше CityTile на 360-му ході · Поразка: усе втрачено · Рахунок: кількість клітин міст, потім юнітів.

## Керування і ввід
- Ввід — програма-агент (Python, JS, Rust, C++, Java, TypeScript, Kotlin — стартові набори в `kits/`); локально — CLI-рушій, онлайн — Kaggle submissions.
- Кожен хід агент отримує стан і повертає список наказів: рух `m id dir`, `bcity id`, `p id`, `t src dst res n`, `bw x y` / `bc x y`, `r x y` (?) — точні рядки протоколу в специфікації не дивився.
- Багато команд RL/ML: агент — нейромережа над тензором карти; або правила + пошук.

## Вікна, меню, HUD
- `replay-viewer` (2021vis.lux-ai.org): поле по кадрах, ресурси, міста з паливом, юніти з вантажем, `frame-scrubber`, індикатор дня/ночі (?).
- `leaderboard` Kaggle з рейтингом (скіл за матчами (?)), сторінка сабмішнів з реплеями.
- Discord і форум Kaggle — поза грою.

## Фічі поза полем
- `bot-upload` (Kaggle submission), автоматичні матчі, `leaderboard-online`.
- `local-referee`: відкритий рушій, стартові набори 7 мов, `replay` у JSON.
- `time-bank`: 3 с на хід без накопичення + спільні 60 с на перевищення.
- S2: датасет минулих епізодів для навчання; S3: Jax-середовище для GPU/TPU.

## Варіації й родичі
- **Season 2** (NeurIPS 2023): фабрики, легкі/важкі роботи, лід/руда, вода, лишайник, енергія; Jax-рушій, асиметричні карти — правил не дивився, лише README.
- **Season 3** (2024 (?)): 24×24, best-of-5 матчів по 100 кроків на тій самій випадковій карті; туман за радіусом сенсора; реліквії з **прихованою маскою 5×5** клітин-очок (+1 за клітину за крок); дія `sap` (30–50 енергії в цілі, частка — у 8 сусідів); туманності (−зір, −енергія), астероїди (непрохідні, дрейфують); зіткнення — виживає сторона з більшою сумарною енергією; більшість параметрів випадкові й **приховані** — їх треба вивчати між матчами серії.
- Родичі: Halite (Two Sigma, Kaggle 2020) і AI Challenge Ants — у [bot-arenas](bot-arenas.md); [codingame-keep-off-the-grass](codingame-keep-off-the-grass.md) — поле, що зʼїдається видобутком; [screeps](screeps.md).
- Осі варіацій: **ритм** (день/ніч / без циклу); **економіка** (паливо-утримання / енергія юнітів / очки за присутність); **інформація** (повна S1 / туман S3); **параметри** (відомі / приховані випадкові); **формат** (один матч / серія best-of-5 з навчанням між матчами).

## Цікавинки для курсу
- Симулятор S1 за 8 фазами з cooldown, дорогами й нічним спалюванням — 🥈.
- «Місто гине цілком»: звʼязні компоненти клітин, спільне паливо, знижка за сусідів — 🥉.
- Нічне спалювання «спершу найменш ефективне, лише цілими одиницями» — 📎 (пастка на округлення).
- Конфлікт ходів: двоє в одну клітину — обидва стоять, обмін місцями дозволено — 🥉.
- Бот з плануванням «встигнути до ночі»: BFS до ресурсу, підрахунок палива на ніч, де ставити нову клітину — 🥇.
- S3: виведення прихованої маски реліквії з приростів очок (дедукція з шуму) — 👑.
- Серія best-of-5 з навчанням параметрів між матчами — 🥇.

## Мапа на каталог
- Є: `move-4dir` · `impassable-cells` (чужі міста, астероїди S3) · `round-currency` (паливо) · `inventory-limit` (вантаж 100/2000) · `spawn-points` (клітини міст) · `piece-capture` (зіткнення S3) · `fog-of-war` (S3) · `replay` · `leaderboard` · `state-as-data` · `game-loop`.
- **Нема** → пропозиції карток:
  - `+text-io-protocol`, `+turn-time-limit`, `+simultaneous-hidden-orders`, `+symmetric-map-generation`, `+local-referee` — з [bot-arenas](bot-arenas.md).
  - `+day-night-cycle` «Цикл день/ніч з різними правилами фаз» · game-logic · 📎.
  - `+upkeep-or-die` «Утримання паливом щоходу, нестача — загибель» · game-logic/economy · 📎.
  - `+adjacency-discount` «Знижка утримання за сусідів свого типу» · game-logic/economy · 🌱.
  - `+research-unlocks-resource` «Очки дослідження відкривають ресурси» · game-logic/economy · 🌱.
  - `+cooldown-per-action` «Кожна дія додає cooldown; діяти можна при < 1» · entities/state · 📎.
  - `+road-speedup` «Клітина з рівнем, що прискорює юнітів» · entities/move · 📎.
  - `+resource-regrowth` «Ресурс відростає на % від залишку» · game-logic/economy · 🌱.
  - `+unit-cap-by-buildings` «Ліміт юнітів = кількість будівель» · game-logic/economy · 🌱.
  - `+move-conflict-cancel` «Двоє в одну клітину — обидва ходи скасовано» · entities/legality · 📎.
  - `+adjacent-harvest` «Видобуток із сусідніх клітин і своєї» · game-logic/economy · 🌱.
  - `+hidden-random-params` «Правила з прихованими випадковими параметрами» · game-logic · 🥈.
  - `+best-of-series` «Серія матчів на тій самій карті» · game-logic/win · 📎.
  - `+energy-tiebreak-combat` «У клітині виживає сторона з більшою сумою енергії» · entities/combat · 📎.
  - `+time-bank` «Ліміт на хід + спільний банк перевищень» · game-logic/opponent · 📎.

## Пропозиції до словників
- `+trigger:night_start` — початок нічної фази циклу; `+trigger:out_of_fuel(a)` — паливо вичерпано.
- `+cond:cooldown_ready(a)` — cooldown < 1; `+cond:researched(resource)`; `+cond:cargo_full(a)`.
- `+effect:transfer(a, b, res, n)` — передача ресурсу сусідньому юніту; `+effect:build_city(cell)`; `+effect:pillage(cell)`; `+effect:research(+1)`; `+effect:sap(cell, n)` — шкода енергією в ціль і сусідів (S3); `+effect:eliminate(bot)` — підтвердження.
- `+window:replay-viewer`, `+ui:frame-scrubber` — підтвердження з bot-arenas.
- `+feature:bot-upload` — підтвердження; `+feature:time-bank`; `+feature:hidden-params`.
- Осі (вже є в `classes.md`, не пропоную): `turn-structure` = `simultaneous`, `actors` = `swarm`, `control` = `programmed`.

## Джерела
- ⭐ [Lux-Design-S1 specs.md](https://raw.githubusercontent.com/Lux-AI-Challenge/Lux-Design-S1/master/specs.md) — таблиця ресурсів, юніти, CityTile 23 − 5·сусіди, cooldown і дороги, 30+10 ходів, 360 ходів, 8 фаз, 3 с + 60 с, тайбрейки.
- [GitHub: Lux-Design-S1](https://github.com/Lux-AI-Challenge/Lux-Design-S1) — README, `kits/`, Kaggle, візуалізатор.
- [GitHub: Lux-Design-S2](https://github.com/Lux-AI-Challenge/Lux-Design-S2) — NeurIPS 2023, Jax, асиметричні карти.
- [GitHub: Lux-Design-S3](https://github.com/Lux-AI-Challenge/Lux-Design-S3) і [S3 specs.md](https://raw.githubusercontent.com/Lux-AI-Challenge/Lux-Design-S3/main/docs/specs.md) — best-of-5, 24×24, реліквії, sap, туман, приховані параметри.
- [lux-ai.org](https://www.lux-ai.org/) — сайт (JS, вміст не прочитано); [Kaggle S1](https://www.kaggle.com/c/lux-ai-2021); [візуалізатор](https://2021vis.lux-ai.org/) — лінки з README.

## Непевне
- (?) Рядковий формат наказів S1 (`m`, `bcity`, `p`, `t`, `bw`, `bc`, `r`) — з памʼяті; специфікацію протоколу не відкривав.
- (?) Правила S2 (фабрики, лишайник, енергія, вода) — лише за README, деталей не бачив.
- (?) Рік S3 (2024) і рейтингова система Kaggle — з памʼяті.
- (?) Візуалізатор: вигляд HUD і індикатор дня/ночі — не відкривав.
