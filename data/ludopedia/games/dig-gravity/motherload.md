---
title: Motherload
slug: motherload
aka: [MotherLoad, Motherload Goldium Edition, Super Motherload]
family: dig-gravity
also: [build-sim]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: partial
  random: both
  goal: state
year: 2004
platforms: [web (Flash), PS4, PS3, PC (Super Motherload, 2013–2014)]
links:
  - {kind: other, url: "https://www.cyberly.org/game-cheats/pc-walkthroughs/motherload.html", best: true, note: "повний гайд: магазини, мінерали з цінами й глибинами, 6 гілок апгрейдів, предмети, небезпеки, боси"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Super_Motherload", note: "сиквел 2013: підземні бази-чекпоінти, сплави з послідовностей мінералів, бомбові пазли"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/XGen_Studios", note: "студія; Motherload — Flash 2004"}
  - {kind: steam, url: "https://store.steampowered.com/app/269110/Super_Motherload/", note: "Super Motherload: процедурний світ, кооп 1–4 локально, 150+ вибухових пазлів"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Motherload+XGen+gameplay", note: "пошук; геймплей Flash-версії"}
stage: v1
coverage: 70
mechanics: [move-by-input, gravity-fall, dig-terrain, impassable-cells, hp-damage, environment-death, player-death, item-pickup, inventory-limit, inventory-items, explode-area, teleport-one-way, round-currency, shop-between-levels, shop-catalog, in-round-upgrades, hunger-clock, event-points, save-game, player-camera, status-panel, leaderboard, +fuel-tank, +sell-cargo, +depth-tiered-ore, +fall-damage, +hidden-hazard-cell, +surface-quake, +upgrade-tiers, +flight-thrust]
proposes: ["+trigger:land", "+effect:sell", "+effect:refuel", "+ui:fuel-gauge", "+ui:depth-meter", "+ui:cargo-meter", "+card:fuel-tank", "+card:sell-cargo", "+card:depth-tiered-ore", "+card:hidden-hazard-cell", "+card:surface-quake", "+card:upgrade-tiers", "+card:flight-thrust"]
author: opus
date: 2026-11-09
---

# Motherload — копання як економіка: паливо і корпус проти глибини й цін руди

## Суть
Гравець керує бурильною капсулою на Марсі: риє вниз і вбік, набирає руду в трюм і повертається на поверхню продати її, заправитись і полагодитись. Гроші йдуть на апгрейди шести вузлів (бур, корпус, двигун, бак, радіатор, трюм), що дають змогу лізти глибше, де руда дорожча, а небезпеки — лава, газ, валуни — сильніші. Ядро — петля «рейс униз → повернення до палива» з двома ресурсами-таймерами (паливо, корпус) і обмеженим трюмом. Глибоко внизу — сюжетні боси.

## Поле і час
- Вертикальний розріз ґрунту під поверхнею; на поверхні вряд стоять будівлі-магазини. Поле — сітка квадратів ґрунту; висотомір у футах від 0 (поверхня) вниз.
- Камера слідує за капсулою; видно лише околицю (`info: partial`); газові кишені маскуються під звичайний ґрунт.
- Real-time; капсула має фізику польоту: тяга вгору проти гравітації, інерція, удар при падінні.
- Розкладка руди залежить від глибини (смуги появи); землетруси на поверхні переставляють ґрунт (`random: runtime`).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Капсула (pod) | player | корпус (HP), паливо, трюм, бур, двигун, радіатор | їздить, літає тягою, бурить ліворуч/праворуч/вниз; угору не бурить |
| Ґрунт | terrain | — | буриться → порожнеча; швидкість за буром |
| Порожнеча / тунель | terrain | — | капсула падає або летить |
| Мінерал ×10 | resource | ціна $30…$500 000; глибина появи | буриться → у трюм, якщо є місце |
| Скарб ×4 | pickup | $1 000…$50 000 | одразу гроші, не займає трюм (?) |
| Валун | static | — | не буриться; лише вибухівка |
| Лавова кишеня | hazard | з ~3100 ft | при бурінні шкода корпусу; радіатор зменшує |
| Газова кишеня | hazard | з ~4700 ft; схожа на ґрунт | при бурінні вибух: клітина зникає, шкода корпусу; радіатор не допомагає |
| Fuel Depot | static | $5/$10/$25/$50/Fill | заправка |
| Mineral Depot | static | SELL ALL | продає весь трюм |
| Junk Shop | static | 6 гілок × до 7 рівнів | апгрейди |
| Repair Station | static | ремонт $50…full; предмети | ремонт корпусу, продаж витратних |
| Save Pod | static | — | збереження (тунелі не зберігаються) |
| Динаміт | pickup | $2 000; радіус 1 | вибух, руйнує валуни |
| Пластична вибухівка | pickup | $5 000; радіус 2 | більший вибух |
| Reserve Fuel Tank | pickup | $2 000; +25 л | заправка під землею |
| Hull Repair Nanobots | pickup | $7 500; +30 HP | ремонт під землею |
| Quantum Teleporter | pickup | $2 000 | на поверхню, може пошкодити корпус |
| Matter Transmitter | pickup | $10 000 | безпечно до Fuel Depot |
| Mr. Natas | boss | 1000 HP; ~7300 ft | замахи посохом, лазер монокля |
| Фінальний бос | boss | 2000 HP | рука-механізм, вогняна куля |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left|right|down)` → ЯКЩО `cell(target, soil)` → ТО `custom: «бурить клітину за час, що залежить від бура»`, `set_cell(target, tunnel)`, `move(pod, dir)`.
- КОЛИ `input(up)` → ЯКЩО `cell(above, soil)` → ТО `block` (угору не бурить).
- КОЛИ `input(up)` → ЯКЩО `free(above)` → ТО `custom: «тяга вгору проти гравітації, витрачає паливо»`.
- КОЛИ `tick` → ЯКЩО `free(below)` and `custom: «нема тяги»` → ТО `fall(pod)`.
- КОЛИ `custom: «приземлення з великої швидкості»` → ТО `damage(pod, n ~ швидкість)`.
- КОЛИ `tick` → ТО `counter(fuel, -n)` (у русі й бурінні більше, ?).
- КОЛИ `counter(fuel, ==, 0)` → ТО `lose` (капсула вибухає).
- КОЛИ `hp_zero(pod)` → ТО `lose`.
- КОЛИ `custom: «пробурено мінерал»` → ЯКЩО `counter(cargo, <, capacity)` → ТО `pickup(pod, mineral)`, `counter(cargo, +1)`; інакше `custom: «мінерал втрачено»` (?).
- КОЛИ `custom: «пробурено скарб»` → ТО `currency(+value)`, `score(+)`.
- КОЛИ `contact(pod, boulder)` → ТО `block`.
- КОЛИ `custom: «пробурено лаву»` → ТО `damage(pod, n × (1 − radiator%))`.
- КОЛИ `custom: «пробурено газ»` → ТО `explode(cell, 1)`, `damage(pod, n)`.
- КОЛИ `input(item_key)` → ЯКЩО `has(pod, dynamite)` → ТО `take(pod, dynamite)`, `explode(square, 1)`; пластична — `explode(square, 2)`; вибух руйнує й валуни.
- КОЛИ `input(item_key)` → ЯКЩО `has(pod, reserve_fuel)` → ТО `take`, `counter(fuel, +25)`; нанороботи → `heal(pod, 30)`.
- КОЛИ `input(item_key)` → ЯКЩО `has(pod, quantum_teleporter)` → ТО `teleport(pod, surface)`, `damage(pod, rng)` (?); matter transmitter → `teleport(pod, fuel_depot)`.
- КОЛИ `enter(pod, mineral_depot)` → ТО `window(custom-window)`; «SELL ALL» → `currency(+Σ cargo)`, `counter(cargo, =0)`.
- КОЛИ `enter(pod, fuel_depot)` → ТО `window(shop-window)`; покупка → `currency(-price)`, `counter(fuel, +litres)`.
- КОЛИ `enter(pod, junk_shop)` → ТО `window(shop-window)`; покупка рівня вузла → `currency(-price)`, `set_value(pod.part, next_tier)`.
- КОЛИ `enter(pod, repair_station)` → ТО `window(shop-window)`: `heal(pod, n)` за гроші або `give(pod, item)`.
- КОЛИ `leave(pod, shop)` → ЯКЩО `prob(p)` → ТО `custom: «землетрус переставляє ґрунт біля поверхні, ламає тунель»`.
- КОЛИ `reach(pod, 3500|6200|7000 ft)` → ТО `message(попередження Mr. Natas)`.
- КОЛИ `hp_zero(boss)` → ТО `currency(+reward)`, фінал → `win`, підсумок очок за грошима.
- Перемога: перемогти фінального боса. Поразка: паливо 0 або корпус 0. Рахунок: росте за мінерали й дії; при повторі гри ціни руди ×½, очки ×.

## Керування і ввід
- Стрілки або WASD: їзда ліворуч/праворуч, рух у ґрунт = буріння; вгору = тяга (політ).
- Клавіші предметів: вибухівка, запасне паливо, нанороботи, телепорти.
- Магазини — вʼїхати в будівлю на поверхні; далі клік по кнопках вітрини.
- Тактика: розрахувати паливо на дорогу назад; не падати з висоти; глибше 4500 ft — лише з міцним корпусом через газ.

## Вікна, меню, HUD
- `main-menu` / титул: нова гра, продовжити (?).
- `game-screen`: розріз ґрунту; HUD — `hp-bar` корпусу (червоний циліндр), `fuel-gauge` (коричневий циліндр), висотомір (`depth-meter`, з 5812 ft «глючить»), `coins` (гроші), `score`.
- `shop-window` ×4: Fuel Depot (суми заправки), Junk Shop (6 вкладок апгрейдів з цінами й характеристиками), Repair Station (ремонт + предмети), Mineral Depot (`custom-window` зі списком трюму й SELL ALL).
- `save-slots` / Save Pod — збереження; онлайн-версія скидає рахунок при збереженні й шле рекорд у `leaderboard`.
- `dialogue-window` — повідомлення Mr. Natas.
- `end-screen` — підсумок виплат і рахунку після боса.
- Переходи: game-screen → (вʼїзд у будівлю) shop-window → game-screen; паливо/корпус 0 → end-screen.

## Фічі поза полем
- Прогресія — `upgrade-tiers`: 6 вузлів × до 7 рівнів (бур 28→120 ft/s, корпус 10→180, бак 10→150 л, трюм ≤15→120, радіатор 0→80 %, двигун ≤160→210 HP), ціни $750…$500 000.
- `save-slots`, `leaderboard-online` (онлайн), New Game+ з половинними цінами.
- Goldium Edition: стартові $0, Multi-Drill для валунів, збереження без скидання рахунку.
- Super Motherload (2013): процедурний світ щоразу інший, підземні бази-чекпоінти, сплави за послідовністю зібраних мінералів, 150+ бомбових пазлів, кооп 1–4 локально, розгалужений сюжет.

## Варіації й родичі
- У сімʼї: SteamWorld Dig (та сама петля «вниз → продати → апгрейд», але платформер з драбинами й світлом), Dig Dug / Mr. Driller (копання без економіки), Dome Keeper (копання між хвилями оборони).
- Super Motherload — сплави: порядок збору як «рецепт» (дитина `pattern`); бомбові пазли.
- **Осі варіацій**: повернення — «на поверхню / до підземної бази / телепортом»; таймер рейсу — «паливо / повітря / світло / голод»; трюм — «кількість одиниць / вага»; небезпека — «видима (лава) / замаскована (газ)».

## Цікавинки для курсу
- Два ресурси-таймери (паливо й корпус) + трюм: кожен рейс — задача планування маршруту туди-назад — 🥉.
- Смуги руди за глибиною й ціни, що ростуть експоненційно, — генерація з таблицею ймовірностей за рядом — 📎.
- Магазин апгрейдів з 6 гілками й рівнями, що міняють фізику капсули — 🥉 (дані + застосування).
- Замаскована небезпека (газ = ґрунт) — 🌱.
- Шкода від падіння за швидкістю приземлення — 📎.
- Землетрус, що переставляє клітини біля поверхні після виходу з магазину — 📎.
- Сплави Super Motherload: послідовність зібраного як рецепт — 🥉.

## Мапа на каталог
- Є: `move-by-input` · `gravity-fall` · `dig-terrain` · `impassable-cells` ↔ валуни · `hp-damage` ↔ корпус · `environment-death` ↔ лава, газ · `player-death` · `item-pickup` · `inventory-limit` ↔ трюм · `inventory-items` ↔ вибухівка, телепорти · `explode-area` ↔ радіус 1/2 · `teleport-one-way` ↔ на поверхню · `round-currency` · `shop-between-levels` + `shop-catalog` · `in-round-upgrades` ↔ 6 вузлів · `hunger-clock` ↔ паливо · `event-points` · `save-game` · `player-camera` · `status-panel` · `leaderboard`.
- **Нема** → пропозиції карток:
  - `+fuel-tank` «Паливо як таймер рейсу з заправкою» · entities/state · 📎 · слоти {capacity, burn} — дитина `hunger-clock`.
  - `+sell-cargo` «Продаж зібраного на базі» · game-logic/economy · 🌱.
  - `+depth-tiered-ore` «Ресурси за глибиною» · levels/generation · 📎 · слот {table}.
  - `+fall-damage` «Шкода від падіння» · entities/death · 📎 (повтор зі SteamWorld Dig).
  - `+hidden-hazard-cell` «Небезпека під виглядом звичайної клітини» · entities/legality · 🌱.
  - `+surface-quake` «Подія перебудовує частину поля» · levels/generation · 📎.
  - `+upgrade-tiers` «Гілки апгрейдів з рівнями» · game-logic/economy · 🥉 · слот {branches, tiers}.
  - `+flight-thrust` «Тяга проти гравітації за паливо» · entities/move · 📎.

## Пропозиції до словників
- `+trigger:land` — приземлення після падіння (шкода за швидкістю; повтор зі SteamWorld Dig).
- `+effect:sell` — обміняти вміст інвентаря на валюту (Mineral Depot; повтор).
- `+effect:refuel` — поповнити ресурс-таймер за гроші/предмет.
- `+ui:fuel-gauge` — шкала палива; `+ui:depth-meter` — висотомір/глибиномір (повтор з Mr. Driller, SteamWorld Dig); `+ui:cargo-meter` — заповнення трюму.

## Джерела
- ⭐ [Cyberly: Motherload walkthrough](https://www.cyberly.org/game-cheats/pc-walkthroughs/motherload.html) — магазини, 10 мінералів і 4 скарби з цінами й глибинами, таблиці апгрейдів, предмети, валуни/лава/газ/землетруси/падіння, боси, рахунок.
- [Wikipedia: Super Motherload](https://en.wikipedia.org/wiki/Super_Motherload) — сиквел: бази-чекпоінти, сплави, бомбові пазли, Марс.
- [Wikipedia: XGen Studios](https://en.wikipedia.org/wiki/XGen_Studios) — Motherload як Flash-гра 2004.
- [Steam: Super Motherload](https://store.steampowered.com/app/269110/Super_Motherload/) — процедурний світ, кооп 1–4, 150+ пазлів.
- YouTube: пошук «Motherload XGen gameplay».

## Непевне
- (?) Окремої статті Wikipedia про Motherload 2004 нема (⭐-лінк черги — 404); усе про оригінал — з фан-гайда Cyberly й пошукових сніпетів.
- (?) Як саме витрачається паливо (за час / за рух / за буріння) і з якою швидкістю.
- (?) Що стається з мінералом при повному трюмі; чи скарби займають трюм.
- (?) Чи розкладка руди випадкова на кожну нову гру в оригіналі (Super Motherload — так, процедурна).
- (?) Ушкодження від Quantum Teleporter — «може пошкодити», механіка невідома.
- (?) Пункти титульного меню.
