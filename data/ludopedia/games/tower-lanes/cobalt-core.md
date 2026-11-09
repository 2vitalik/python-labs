---
title: Cobalt Core
slug: cobalt-core
aka: []
family: tower-lanes
also: [roguelike]
klass: avatar
axes:
  field: 1d
  time: turn
  opponent: ai
  info: partial
  random: both
  goal: state
year: 2023
platforms: [PC, Mac, Switch]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/2179850/Cobalt_Core", best: true, note: "суть: бій на одній осі, ухилення, щити, вирівнювання гармат, 3 члени екіпажу"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Cobalt_Core", note: "5 карт у руці, 3 очки дії, телеграфовані наміри, зсув корабля"}
  - {kind: other, url: "https://cobaltcore.wiki.gg/wiki/Midrow_Objects", note: "wiki.gg: обʼєкти середнього ряду, дрон-хід, ракети"}
  - {kind: other, url: "https://cobaltcore.wiki.gg/wiki/Ship_Parts", note: "wiki.gg: типи частин корабля, Empty"}
  - {kind: other, url: "https://cobaltcore.wiki.gg/wiki/Evade", note: "wiki.gg: статуси руху й щитів"}
  - {kind: other, url: "https://cobaltcore.wiki.gg/wiki/Part_Traits", note: "wiki.gg: Weak, Brittle, Armored, Concussable"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=cobalt+core+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [hp-damage, telegraphed-intents, telegraph-marker, status-effects, run-relics, projectile-shot, projectile-collision, shoot-forward, ai-opponent, round-currency, shop-catalog, map-window, character-select, difficulty-select, daily-puzzle, leaderboard, achievements-window, permadeath, +deck-draw, +lane-grid, +ship-lane-shift, +ship-part-grid, +midrow-objects, +shield-and-temp-shield, +card-upgrade-branch, +exhaust-card, +heat-overload, +crew-deck-mix, +time-loop-unlocks]
proposes: ["+role:card", "+role:part", "+role:lane", "+trigger:drone_phase", "+effect:draw_cards", "+effect:discard_hand", "+effect:exhaust", "+cond:lane_has", "+ui:energy-pips", "+ui:status-row", "+window:choice-window", "+window:deck-window", "+feature:run-map", "+axis:session"]
author: opus
date: 2026-11-09
---

# Cobalt Core — бій кораблів на одній осі: зсувай корабель картами, щоб гармата влучила, а ворожа — ні

## Суть
Роглайк-декбілдер: гравець з колоди трьох членів екіпажу грає карти, що стріляють, ставлять щити, запускають дрони й **зсувають корабель уліво-вправо**. Обидва кораблі стоять один навпроти одного, кожна частина корабля займає колонку; постріл бʼє лише ту колонку, де стоїть гармата. Ворог телеграфує наміри (підсвічує червоним колонки, куди вдарить), тож хід — це пазл «ухилитися + вирівняти свою гармату під слабку частину ворога». Між кораблями — **середній ряд** обʼєктів (ракети, дрони, астероїди), що блокують постріли й діють самі.

## Поле і час
- Три ряди над однією віссю колонок: ворожий корабель (верх) · midrow (обʼєкти) · корабель гравця (низ). Кожен корабель — ряд частин шириною кілька колонок (Artemis — 5).
- Рух — лише по осі X: корабель зсувається цілим на N колонок; частини всередині корабля не переставляються.
- Покроково: хід гравця (3 енергії, 5 карт) → **дрон-хід** (дрони й ракети середнього ряду діють зліва направо) → хід ворога (виконує телеграфовані наміри) → новий хід.
- Забіг: 3 сектори (Lazuli Nebula, Sapphire Cluster, Void's Cradle) з вузлами-бійками, подіями, крамницями й босом у кінці сектора.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Корабель гравця | player | hull (Artemis 12), max shield (Artemis 4), ширина в колонках | зсувається вліво-вправо; отримує шкоду в частину, що в колонці удару |
| Ворожий корабель | enemy | hull, shield, частини з намірами | кожна частина має намір на наступний хід (атака, щит, запуск, рух) |
| Бос сектора | boss | — | сильний ворог у кінці сектора; дає артефакт |
| Кокпіт | object (`+role:part`) | на Hard — Weak, на Hardest — Brittle | частина корабля; є майже в усіх кораблях |
| Гармата | object (`+role:part`) | активна / неактивна (Ares, Gemini — дві) | стріляє в те, що прямо навпроти: обʼєкт midrow або частину ворога |
| Ракетна шахта (Missile Bay) | spawner (`+role:part`) | — | запускає обʼєкт midrow у свою колонку (деякі карти — зі зсувом) |
| Comms (Jupiter) | object (`+role:part`) | завжди Weak | без власних ефектів |
| Крила | object (`+role:part`) | — | без ефекту; з артефактом Hunter Wings стають Empty |
| Порожня частина (Empty) | zone | — | атаки й ракети пролітають «наче нічого нема» |
| Астероїд | object | — | блокує постріл; руйнується будь-якою атакою |
| Космічна міна | hazard | 2 (Big — 3) | шкода тому, хто її знищив |
| Ремкомплект | pickup | +2 hull | лікує того, хто його знищив |
| Жеода | pickup | +1 Shard | дає ресурс тому, хто знищив |
| Атакуючий дрон | ally | 1 шкоди (Mk2 — 2) | у дрон-хід стріляє у свою колонку |
| Щит-дрон · енергодрон | ally | +1 shield · +1 energy | у дрон-хід дає ресурс кораблю |
| Jupiter-дрон | ally | — | додаткова «гармата»: копіює ефекти Attack |
| Ракета | projectile | 2 (heavy 3, seeker 2, acid → Corrode) | у дрон-хід жертвує собою й бʼє свою колонку; seeker — найближчу не-Empty частину |
| Футбольний мʼяч | object | незнищенний | від удару зсувається на стільки колонок, скільки шкоди |
| Bubble Shield | zone | 1 удар | на обʼєкті midrow поглинає першу атаку |
| Карта | supply (`+role:card`) | ціна в енергії, рідкість, апгрейд A/B | ефект: атака, щит, рух, запуск, статус |
| Сміттєва карта (Trash) | supply | Debris, Fear, Oxygen Leak… | вороги підкидають у колоду; заважає |
| Член екіпажу | neutral | 3 з 8 | додає свої карти в колоду; може «зникнути» статусом Character Is Missing |
| Артефакт | pickup | — | пасивне правило на весь забіг або підсилення карт одного персонажа |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(player)` → ТО `counter(energy, 3)` (невитрачена не переноситься), `custom: «взяти 5 карт»`, `clear_state(ship, temp_shield)`.
- КОЛИ `input(play, card)` → ЯКЩО `has(energy, cost)` → ТО `counter(energy, -cost)` + ефект карти; інакше `block`.
- КОЛИ `input(play, move_card)` → ТО `move(ship, dir, n)`; ЯКЩО `state(ship, engine_lock)` → `block`; ЯКЩО `state(ship, engine_stall)` → рух не вдається, `counter(engine_stall, -1)`.
- КОЛИ `input(spend, evade)` → ЯКЩО `has(evade, 1)` → ТО `move(ship, ±1)`, `counter(evade, -1)` (можна будь-коли за свій хід).
- КОЛИ `input(play, attack)` → ТО для кожної активної гармати зліва направо: `custom: «перша сутність у колонці гармати»` — ЯКЩО `occupied(column, midrow_object)` → `disappear_b` (будь-яка атака, навіть 0); інакше ЯКЩО `occupied(column, part)` and `not state(part, empty)` → `damage(n)`; інакше — промах.
- КОЛИ `custom: «корабель отримує шкоду n»` → ТО спершу `custom: «гасить temp shield, потім shield, решта — hull»`; модифікатори частини: Weak `+1` за удар, Brittle `×2`, Armored `−1` (не для пробивних).
- КОЛИ `contact(attack, part)` → ЯКЩО `state(part, concussable)` → ТО `custom: «скасувати намір частини»`; Stun-атаки → `stun(part)` (намір скасовано).
- КОЛИ `input(play, launch)` → ТО `spawn_at(object, column(missile_bay) + offset)`; ЯКЩО `occupied(cell, midrow_object)` → `damage` обом; Bubble Shield рятує власника.
- КОЛИ `custom: «trigger drone_phase»` → ТО дрони й ракети зліва направо: ракета — `damage(column)` + `disappear_a`; атакуючий дрон — `damage(1)`; щит-дрон — `custom: «+1 shield»`.
- КОЛИ `turn_end(player)` → ТО `custom: «скинути руку»`; карти з Exhaust — `custom: «вилучити до кінця бою»`.
- КОЛИ `turn_end(side)` → ЯКЩО `counter(heat, >=, 3)` → ТО `hp(ship, -1)`, `counter(heat, 0)` (перегрів).
- КОЛИ `turn_end(side)` → ТО `counter(overdrive, -1)` (Overdrive: +X до кожної атаки; Powerdrive не спадає); Corrode → `hp(ship, -X)`.
- КОЛИ `turn_start(enemy)` → ТО `custom: «кожна частина виконує показаний намір»`; гармати ворога стріляють у підсвічені колонки зліва направо.
- КОЛИ `custom: «ворог атакує колонку»` → ЯКЩО `state(ship, autododge)` → ТО `move(ship, away)`, `counter(autododge, -1)` (не від ракет).
- КОЛИ `contact(midrow_object, attack)` → ЯКЩО `same(object, football)` → ТО `shift(object, dir, damage)`; ЯКЩО міна → `damage(attacker, 2)`; ремкомплект → `heal(attacker, 2)`.
- КОЛИ `input(play, droneshift)` → ТО `shift(midrow, dir)` — зсуває всі обʼєкти середнього ряду, чиї б вони не були.
- КОЛИ `hp_zero(enemy)` → ТО `choose(card_rewards)` (з A/B-апгрейдами), бос → `give(artifact)`; `custom: «далі — вузол мапи»`.
- КОЛИ `hp_zero(ship)` → ТО `lose` (забіг з початку; петля часу відкриває нові спогади й варіанти).
- Перемога: дійти до кінця 3-го сектора · Поразка: hull = 0 · Рахунок: вихід з петлі, Daily — таблиця.

## Керування і ввід
- Миша/геймпад: клік по карті в руці — зіграти; кнопки Evade «ліворуч/праворуч»; кнопка кінця ходу.
- Наведення на частину ворога — показ наміру (`tooltip`); на карту — превʼю ефекту (куди влучить, куди зсунеться корабель).
- Ares/Gemini — карти перемикання активної гармати; Jupiter стріляє лише дронами.

## Вікна, меню, HUD
- `main-menu`: новий забіг, продовжити, Daily, налаштування, вихід.
- `character-select` — вибір 3 з 8 членів екіпажу і корабля з 5, складність (`difficulty-select`: Hard/Harder/Hardest).
- `game-screen`: ворожий корабель з `telegraph-marker` (червоні колонки), midrow, свій корабель, `hp-bar` hull + сегменти shield/temp shield, `+ui:energy-pips` (3), рука карт, `+ui:status-row` (Evade, Overdrive, Heat…), колода/скид, `end-turn-button`, `tooltip`.
- `map-window` — сектор з вузлами (бій, подія, крамниця, бос).
- `+window:choice-window` — нагорода: 1 з кількох карт; апгрейд карти — вибір гілки A або B.
- `shop-window` — крамниці-події («Grandma's Bakery and Weapons Market»).
- `+window:deck-window` — перегляд колоди/скиду; `dialogue-window` — сюжетні розмови екіпажу.
- `end-screen` — загибель/вихід з петлі; `achievements-window`; `settings-window`.

## Фічі поза полем
- `meta-progression`: петля часу розблоковує персонажів, кораблі, «спогади» (сюжет), стартові варіанти.
- `mode-daily` — Daily Challenge з модифікаторами й `leaderboard-online`.
- `difficulty-presets` — Hard/Harder/Hardest (кокпіт стає Weak/Brittle).
- `autosave`, `achievements`, `localization` (10 мов), `mod-support` (wiki: Modding).

## Варіації й родичі
- Родичі в сімʼї: [inscryption](inscryption.md) (колонки й удар навпроти), [wildfrost](wildfrost.md) (смуги + карти), [plants-vs-zombies](plants-vs-zombies.md) (смуга = ряд удару); поза сімʼєю — Slay the Spire (каркас декбілдера), FTL (бій кораблів частинами), Into the Breach (телеграф намірів).
- **Осі варіацій**: позиція — фіксована (StS) / зсув уздовж осі (Cobalt Core) / сітка (Into the Breach) · ціль удару — вибір гравця / геометрія колонки · захист — блок / ухилення рухом / щит + тимчасовий щит.

## Цікавинки для курсу
- Бій на одній осі: два ряди частин, постріл у колонку, зсув корабля — 🥉 (простий стан, багато рішень).
- Середній ряд: обʼєкти блокують постріли, дрон-фаза зліва направо, футбол зсувається на шкоду — 🥉.
- Телеграф: кожна частина ворога має намір, підсвітка колонок, Concussable скасовує — 📎.
- Модифікатори частин Weak/Brittle/Armored, багатоударні атаки — 🌱.
- Колода: рука 5, енергія 3, Exhaust, сміттєві карти — 🥉.
- Апгрейд карти з двома гілками A/B — 📎.

## Мапа на каталог
- Є: `hp-damage` ↔ hull/shield · `telegraphed-intents` + `telegraph-marker` ↔ червоні колонки · `status-effects` ↔ Evade/Heat/Overdrive · `run-relics` ↔ артефакти · `projectile-shot` + `projectile-collision` ↔ ракети в midrow · `shoot-forward` ↔ гармата бʼє навпроти · `map-window` · `character-select` · `difficulty-select` · `daily-puzzle` ↔ Daily · `leaderboard` · `permadeath` ↔ забіг з нуля.
- **Нема** → пропозиції карток:
  - `+ship-lane-shift` «Зсув цілого корабля по осі» · entities/move · 🌱.
  - `+ship-part-grid` «Корабель із частин-колонок, шкода по частині» · entities/state · 🥉.
  - `+midrow-objects` «Нейтральний ряд між сторонами: блок і дрон-фаза» · entities/combat · 🥉.
  - `+shield-and-temp-shield` «Щит до максимуму + тимчасовий, що згорає» · entities/state · 🌱.
  - `+card-upgrade-branch` «Апгрейд карти: гілка A або B» · game-logic/economy · 📎.
  - `+exhaust-card` «Карта зникає до кінця бою» · entities/state · 🌱.
  - `+heat-overload` «Лічильник перегріву з порогом» · entities/state · 🌱.
  - `+crew-deck-mix` «Колода зі стартових наборів трьох персонажів» · game-logic/economy · 📎.

## Пропозиції до словників
- `+role:card` — карта в руці/колоді; `+role:part` — частина багатоклітинної сутності з власним станом; `+role:lane` — колонка-смуга удару.
- `+trigger:drone_phase` — окрема фаза ходу для автономних обʼєктів (між ходами сторін).
- `+effect:draw_cards` — взяти N карт (не плутати з `draw` = нічия); `+effect:discard_hand` — скинути руку; `+effect:exhaust` — вилучити карту до кінця бою.
- `+cond:lane_has` — у колонці/смузі є сутність виду.
- `+ui:energy-pips` — очки енергії кружечками; `+ui:status-row` — ряд іконок статусів зі стеками.
- `+window:choice-window` — вибір 1 з N нагород; `+window:deck-window` — перегляд колоди/скиду.
- `+feature:run-map` — розгалужена мапа забігу (роглайт); `+axis:session` — значення `run`.

## Джерела
- ⭐ [Steam: Cobalt Core](https://store.steampowered.com/app/2179850/Cobalt_Core) — «single-axis combat», ухилення, щити, вирівнювання гармат, 3 члени екіпажу, Daily з таблицями, 10 мов, реліз 8.11.2023.
- [Wikipedia: Cobalt Core](https://en.wikipedia.org/wiki/Cobalt_Core) — 3 з 8 персонажів, 5 карт, 3 очки дії, зсув вліво-вправо, телеграф намірів, артефакти з босів; Rocket Rat Games / Brace Yourself Games; Switch, Windows, macOS (2025).
- [Cobalt Core Wiki: Midrow Objects](https://cobaltcore.wiki.gg/wiki/Midrow_Objects) — астероїд, міна, жеода, ремкомплект, дрони, ракети, футбол, Bubble Shield, дрон-хід.
- [Cobalt Core Wiki: Ship Parts](https://cobaltcore.wiki.gg/wiki/Ship_Parts) — кокпіт, гармата, шахта, Comms, крила, Empty; ворожі гармати підсвічують колонку.
- [Cobalt Core Wiki: Evade](https://cobaltcore.wiki.gg/wiki/Evade) — Evade, Hermes Boots, Engine Stall/Lock, Autododge, Autopilot, Corrode, Temp Shield.
- [Cobalt Core Wiki: Part Traits](https://cobaltcore.wiki.gg/wiki/Part_Traits) — Weak, Brittle, Armored, Concussable.
- [Cobalt Core Wiki: Heat](https://cobaltcore.wiki.gg/wiki/Heat) — перегрів ≥3 → 1 шкоди; Overdrive/Powerdrive; повний список статусів.
- [Cobalt Core Wiki: Energy](https://cobaltcore.wiki.gg/wiki/Energy) — 3 енергії на хід, не переноситься.
- [Cobalt Core Wiki: Artemis](https://cobaltcore.wiki.gg/wiki/Artemis) — 5 колонок, центральна гармата, hull 12, shield 4.

## Непевне
- (?) Точний порядок поглинання шкоди (temp shield → shield → hull) — з памʼяті, у відкритих сторінках не описаний.
- (?) Retain / Recycle / Temporary — трейти карт, сторінку Card Traits не відкривав.
- (?) Кількість вузлів у секторі й типи подій; Shard як ресурс окремих персонажів.
- (?) Чи атакує ворог «у колонку» чи «в частину» при зсуві корабля після телеграфу — за логікою гри колонка (саме тому ухилення працює).
