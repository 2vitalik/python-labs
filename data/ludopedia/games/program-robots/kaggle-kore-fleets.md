---
title: Kaggle Kore 2022 (Kore Fleets)
slug: kaggle-kore-fleets
aka: [Kore 2022, Kore Fleets, Kore]
family: program-robots
also: [build-sim]
klass: figure
axes:
  field: square
  time: programmed
  opponent: online
  info: full
  random: setup
  goal: score
year: 2022
platforms: [web, local CLI]
links:
  - {kind: official, url: "https://github.com/Kaggle/kaggle-environments/tree/master/kaggle_environments/envs/kore_fleets", best: true, note: "середовище: helpers.py, kore_fleets.py, json-конфіг, ноутбук, стартові боти, візуалізатор"}
  - {kind: other, url: "https://raw.githubusercontent.com/Kaggle/kaggle-environments/master/kaggle_environments/envs/kore_fleets/helpers.py", note: "дії верфей, план польоту, злиття, бої флотів, верф проти флоту, збір і відростання kore"}
  - {kind: other, url: "https://raw.githubusercontent.com/Kaggle/kaggle-environments/master/kaggle_environments/envs/kore_fleets/kore_fleets.py", note: "симетрична генерація kore, старти, вибування, нагорода"}
  - {kind: other, url: "https://raw.githubusercontent.com/Kaggle/kaggle-environments/master/kaggle_environments/envs/kore_fleets/kore_fleets.json", note: "400 кроків, 21×21, spawnCost 10, convertCost 50, regenRate 0.02, maxRegenCellKore 500, 3 с на хід"}
  - {kind: other, url: "https://www.kaggle.com/competitions/kore-2022", note: "сторінка змагання (рендериться JS; прочитав лише заголовок)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=kaggle+kore+2022", note: "пошук; реплеї"}
stage: v1
coverage: 70
mechanics: [move-4dir, wrap-edges, command-program, round-currency, spawn-points, piece-capture, replay, leaderboard, state-as-data, game-loop, ai-greedy, +flight-plan-string, +plan-length-by-size, +simultaneous-hidden-orders, +turn-time-limit, +time-bank, +merge-same-owner, +larger-fleet-wins, +adjacent-fleet-damage, +shipyard-capture, +spawn-cap-by-age, +harvest-rate-by-size, +resource-regrowth, +convert-to-base, +symmetric-map-generation, +local-referee]
proposes: ["+cond:greater(a, b, prop)", "+effect:launch(a, n, plan)", "+effect:harvest(a, cell, rate)", "+effect:regrow(cell, k, cap)", "+trigger:plan_step(a, cmd)", "+effect:eliminate(bot)", "+window:replay-viewer", "+feature:time-bank"]
author: opus
date: 2026-11-09
---

# Kore Fleets — флот летить за рядком-програмою на кшталт «N2E…C», збирає kore з клітин тора і зливається, бʼється чи захоплює верфі

## Суть
Kaggle-змагання ботів 2022 року (1, 2 або 4 гравці). Єдиний «будинок» — верф: вона купує кораблі за kore і відправляє флоти, кожен з **планом польоту** — рядком команд напрямку й кількості кроків, довжина якого обмежена логарифмом розміру флоту. Флот, пролітаючи клітиною, забирає частку kore (більший флот — більшу частку), повертається у свою верф із вантажем або перетворюється на нову верф командою `C`. Зіткнення флотів вирішує кількість кораблів, сусідні ворожі флоти бʼють один одного, а верф можна захопити. Після 400 кроків виграє той, у кого найбільше kore в банку.

## Поле і час
- Квадратне поле 21×21 — **тор**: усі координати беруться за модулем розміру.
- Клітина: кількість kore (дробова, 3 знаки), можливо верф, можливо флот. Позиція кодується як `row · size + column`.
- Старт: одна верф на гравця з 0 кораблів; стартовий kore 2750 розкидано випадково, але дзеркально в чотири квадранти (і симетрично відносно діагоналі); kore у стартових клітинах обнулено.
- Крок: усі гравці подають дії одночасно → рушій для кожного гравця застосовує дії верфей, рухає флоти, зливає свої → бої флотів → флоти на верфях → бій сусідів → збір kore → відростання.
- Партія — 400 кроків; 3 с на хід + запас `remainingOverageTime` 60 с.
- Інформація повна: видно всі флоти, їхні плани, вантаж і верфі суперника.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Верф (shipyard) | spawner | власник, кораблі, `turns_controlled` | купує кораблі (`SPAWN_n`) або випускає флот (`LAUNCH_n_plan`) — одна дія за хід |
| Флот (fleet) | piece | власник, кораблі, напрямок, вантаж kore, план польоту | щоходу рухається на 1 за планом; без плану — летить прямо |
| Kore у клітині | resource | 0…≈500+ | флот забирає частку; порожня клітина відростає на 2 % |
| Банк kore гравця | resource | старт — див. «Непевне» | платить за кораблі (10 за штуку); рахунок перемоги |
| План польоту | — (програма) | рядок `N/E/S/W`, числа, `C` | літера — напрямок, число — ще стільки кроків, `C` — стати верфю |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start` → ТО `custom: «бот повертає словник uid верфі → SPAWN_n або LAUNCH_n_plan»`.
- КОЛИ `input(SPAWN_n)` → ЯКЩО `custom: «n ≤ max_spawn верфі»` and `has(player, kore ≥ 10·n)` → ТО `counter(ships, +n)` у верфі, `currency(−10·n)`.
- КОЛИ `input(LAUNCH_n_plan)` → ЯКЩО `has(shipyard, ships ≥ n)` → ТО `spawn_at(fleet(n, plan), shipyard)` — флот рухається вже цього кроку; план довший за `⌊2·ln n⌋ + 1` символів обрізається.
- КОЛИ `exec(digit 0)` на початку плану → ТО `custom: «нулі відкидаються»`.
- КОЛИ `exec(C)` → ЯКЩО `has(fleet, ships ≥ 50)` and `not occupied(cell, shipyard)` → ТО `transform(fleet, shipyard)`: 50 кораблів витрачено, решта в новій верфі, вантаж — у банк, kore клітини → 0; інакше `C` пропускається.
- КОЛИ `exec(letter)` → ТО `face(fleet, dir)`; КОЛИ `exec(number d)` → ТО `custom: «ще d кроків цим напрямком; число зменшується на 1 щокроку»` (`E3` = 4 кроки на схід).
- КОЛИ `tick` → ТО `move(fleet, dir)`, `wrap(fleet)`; порожній план — `custom: «летить поточним напрямком далі»`.
- КОЛИ `contact(fleet, own_fleet)` → ТО `merge(a, b, fleet)`: найбільший (кораблі → kore → напрямок) поглинає інших разом із вантажем, лишає свій план.
- КОЛИ `contact(fleet, enemy_fleet)` → ЯКЩО `custom: «у флоту найбільше кораблів»` → ТО `disappear(others)`, `damage(winner, кораблі найбільшого з переможених)`, `pickup(winner, їхній kore)`; рівність лідерів → гинуть усі, kore — власнику верфі на клітині або на клітину.
- КОЛИ `enter(fleet, enemy_shipyard)` → ЯКЩО `custom: «кораблів флоту більше, ніж у верфі»` → ТО `set_side(shipyard, attacker)`, кораблі = різниця, `turns_controlled = 1`, вантаж — у банк нападника; інакше `damage(shipyard, кораблі флоту)`, `disappear(fleet)`, вантаж — захиснику.
- КОЛИ `enter(fleet, own_shipyard)` → ТО `custom: «кораблі — у верф, вантаж — у банк»`, `disappear(fleet)`.
- КОЛИ `adjacent(fleet, enemy_fleet)` (4 сусіди) → ТО `damage(enemy_fleet, кораблі атакувальника)` — сума від усіх сусідів; знищений → половина вантажу на клітину, половина — атакувальникам пропорційно шкоді.
- КОЛИ `phase_start(collect)` → ТО `pickup(fleet, kore)`: `custom: «забрати kore_клітини × min(ln(кораблі) / 20, 0.99)»`; клітина втрачає стільки ж.
- КОЛИ `phase_start(regen)` → ЯКЩО `not occupied(cell, fleet)` and `not occupied(cell, shipyard)` and `custom: «kore < 500»` → ТО `custom: «kore × 1.02»`.
- КОЛИ `turn_end` → ТО `counter(turns_controlled, +1)`; `max_spawn` = 1, 2, …, 10 за порогами 2, 7, 17, 34, 60, 97, 147, 212, 294 ходів володіння.
- КОЛИ `custom: «у гравця нема ні верфей, ні флотів»` → ТО `lose`; нагорода = крок вибування − 401.
- КОЛИ `custom: «активних гравців < 2»` (на 2–4) → ТО `game_over`.
- КОЛИ `counter(step, ==, 400)` → ТО `game_over`: більше kore в банку → `win`.
- Перемога: найбільший банк kore після 400 кроків або останній живий · Поразка: втратив усі верфі й флоти · Рахунок: kore в банку.

## Керування і ввід
- Ввід — Python-агент `agent(obs, config)` (Kaggle-формат); бібліотека `helpers`: `Board`, `ShipyardAction.spawn_ships(n)`, `ShipyardAction.launch_fleet_with_flight_plan(n, plan)`, `Direction`, `to_char()`.
- Дії лише для верфей; флоти не керуються після запуску — уся «програма» в рядку плану.
- Локально — `kaggle_environments.make("kore_fleets")`, `env.run([agent1, agent2])`, рендер реплею в ноутбуці.

## Вікна, меню, HUD
- `replay-viewer` (візуалізатор середовища): поле-тор з інтенсивністю kore, верфі й флоти кольорами гравців, номер кроку, банки (?).
- `leaderboard` Kaggle, сторінка сабмішнів з епізодами (?).
- Ноутбук `kore_fleets.ipynb` — інтерактивний вхід: правила, приклади, запуск.

## Фічі поза полем
- `bot-upload` (Kaggle submission), автоматичні матчі, `leaderboard-online`.
- `local-referee`: відкрите середовище `kaggle-environments`, `seed-input` (`randomSeed`), 1/2/4 агенти.
- `time-bank`: 3 с на хід + 60 с запасу на перевищення (старий `agentTimeout` — застарілий).
- Стартові боти в `starter_bots`.

## Варіації й родичі
- Halite I/III (Two Sigma, Kaggle Halite 2020) — збір ресурсу кораблями на торі — у [bot-arenas](bot-arenas.md); [lux-ai](lux-ai.md) — наступні Kaggle-арени ресурсів; [screeps](screeps.md).
- Програма-рядок замість покрокових наказів — як у [cargo-bot](cargo-bot.md) чи [robozzle](robozzle.md), але виконується без нагляду і без умов.
- Осі варіацій: **керування юнітом** (план на запуску / наказ щоходу); **довжина програми** (обмежена розміром загону / вільна); **бій** (більший виграє з втратами / шкода сусідам / захоплення бази); **збір** (частка за розміром / фіксована швидкість); **поле** (тор / прямокутник).

## Цікавинки для курсу
- Парсер і виконавець плану `N2E10S…C` з обрізанням довжини `⌊2·ln n⌋ + 1` — 📎.
- Повний крок Kore: злиття, бої в клітині, бій сусідів, захоплення верфі, збір, відростання — 🥈 (порядок фаз вирішує все).
- Генерація kore: випадковий квадрант → 4 дзеркальні копії → нормування до 2750 — 🌱.
- Планувальник маршрутів-петель: перебір коротких планів з поверненням у верф і оцінкою зібраного kore — 🥇.
- Захист верфі: передбачити ворожий флот за його відкритим планом — 🥈.
- `max_spawn` за віком верфі — компроміс «нова верф vs стара» — 🌱.

## Мапа на каталог
- Є: `move-4dir` · `wrap-edges` (тор) · `command-program` (план польоту виконується сам) · `round-currency` (kore) · `spawn-points` (верфі) · `piece-capture` (захоплення верфі) · `replay` · `leaderboard` · `state-as-data` · `game-loop` · `ai-greedy` (стартові боти).
- **Нема** → пропозиції карток:
  - `+simultaneous-hidden-orders`, `+turn-time-limit`, `+merge-same-owner`, `+symmetric-map-generation`, `+local-referee` — з [bot-arenas](bot-arenas.md); `+time-bank`, `+resource-regrowth` — з [lux-ai](lux-ai.md).
  - `+flight-plan-string` «Програма руху — рядок напрямків і чисел» · game-logic/program · 📎.
  - `+plan-length-by-size` «Довжина програми залежить від розміру загону» · game-logic/program · 🌱.
  - `+larger-fleet-wins` «Більший загін у клітині виграє, втрачає стільки, скільки мав суперник» · entities/combat · 🌱.
  - `+adjacent-fleet-damage` «Сусідні ворожі загони бʼють один одного» · entities/combat · 🥉.
  - `+shipyard-capture` «База переходить до сильнішого нападника» · entities/combat · 📎.
  - `+spawn-cap-by-age` «Ліміт спавну росте з часом володіння» · game-logic/economy · 🌱.
  - `+harvest-rate-by-size` «Частка зібраного = f(розмір загону)» · game-logic/economy · 🌱.
  - `+convert-to-base` «Загін стає новою базою за ціну частини себе» · entities/interact · 📎.

## Пропозиції до словників
- `+cond:greater(a, b, prop)` — спільне з battlesnake (кораблі флоту).
- `+effect:launch(a, n, plan)` — випустити загін з програмою руху.
- `+effect:harvest(a, cell, rate)` — забрати частку ресурсу клітини.
- `+effect:regrow(cell, k, cap)` — ресурс клітини росте на k, доки нижче cap.
- `+trigger:plan_step(a, cmd)` — загін виконав чергову команду свого плану (поруч із 🔥 `exec(cmd)`, але для автономного юніта).
- `+effect:eliminate(bot)` · `+window:replay-viewer` · `+feature:time-bank` — підтвердження.

## Джерела
- ⭐ [kaggle-environments/envs/kore_fleets](https://github.com/Kaggle/kaggle-environments/tree/master/kaggle_environments/envs/kore_fleets) — тека середовища: код, конфіг, ноутбук, стартові боти, візуалізатор.
- [helpers.py](https://raw.githubusercontent.com/Kaggle/kaggle-environments/master/kaggle_environments/envs/kore_fleets/helpers.py) — уся механіка кроку, формули плану й збору, пороги `max_spawn`.
- [kore_fleets.py](https://raw.githubusercontent.com/Kaggle/kaggle-environments/master/kaggle_environments/envs/kore_fleets/kore_fleets.py) — генерація, старти, вибування, нагорода.
- [kore_fleets.json](https://raw.githubusercontent.com/Kaggle/kaggle-environments/master/kaggle_environments/envs/kore_fleets/kore_fleets.json) — конфіг і схеми спостереження/дії.
- [Kaggle: Kore 2022](https://www.kaggle.com/competitions/kore-2022) — сторінка змагання (вміст рендериться JS).

## Непевне
- (?) Стартовий банк гравця: у json «reward default 500» — схоже на стартовий kore гравця, але не перевірено в коді.
- (?) Docstring збору каже `ln(n) / 10`, код — `ln(n) / 20`; описано за кодом.
- (?) Друга умова вибування («нема кораблів, флотів і не можна купити») у коді не спрацьовує через порівняння списку з 0.
- (?) Верф, що впала до 0 кораблів, не знищується — описано за переказом коду.
- (?) Дати змагання, призи, рейтинг Kaggle і вигляд візуалізатора — сторінки не прочитано.
