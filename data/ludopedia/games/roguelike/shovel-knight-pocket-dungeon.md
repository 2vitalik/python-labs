---
title: Shovel Knight Pocket Dungeon
slug: shovel-knight-pocket-dungeon
aka: [SKPD, Pocket Dungeon]
family: roguelike
also: [falling-match]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: full
  random: runtime
  goal: survive
year: 2021
platforms: [PC (Windows, macOS), Switch, PS4, iOS, Android]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Shovel_Knight_Pocket_Dungeon", best: true, note: "8×8, падіння ворогів, bump-атака, ланцюг однотипних, переповнення = програш, versus, герої"}
  - {kind: steam, url: "https://store.steampowered.com/app/1184760/Shovel_Knight_Pocket_Dungeon/", note: "режими Adventure / Versus / Daily Challenge, 10+ героїв, DLC Puzzler Pack і Paradox Pack, мод-підтримка"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=shovel+knight+pocket+dungeon+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [move-4dir, hp-damage, gravity-fall, spawn-schedule, item-pickup, inventory-items, run-relics, shop-between-levels, shop-catalog, round-currency, player-death, character-select, simultaneous-versus, garbage-attack, daily-puzzle, cheat-codes, progress-acceleration, combo-multiplier, status-effects, key-and-door, sequential-levels, +bump-attack, +group-damage, +board-overflow, +kill-blow-free, +idle-drift, +gem-meter-decay, +meta-currency-keep]
proposes: ["+trigger:board_full", "+effect:group_damage(group, n)", "+effect:drift(all, down)", "+cond:killing_blow", "+feature:infinite-lives", "+card:bump-attack", "+card:group-damage", "+card:board-overflow", "+card:idle-drift"]
author: opus
date: 2026-11-09
---

# Shovel Knight Pocket Dungeon — роглайк у колодязі 8×8: вороги сиплються згори, як тетраміно

## Суть
Герой стоїть у полі 8×8, куди згори безперервно падають вороги, предмети й блоки. Кожен хід (крок або удар) зсуває все вниз; навіть якщо стояти, поле повільно осідає. Атака — «bump»: ступити в клітину ворога; кожен неостаточний удар коштує герою HP, а **добивальний — безкоштовний**, і шкода передається всій звʼязній групі однакових ворогів. Програш — HP = 0 **або поле повністю заповнилось** (Tetris-переповнення). Між рівнями — крамниці реліквій, боси відкривають нових героїв.

## Поле і час
- Квадратна сітка 8×8, уся видима (`info: full`); вхід нових сутностей — з верхнього краю.
- Гібридний час: кожна дія гравця — тік, після якого поле зсувається; без дій поле теж дрейфує вниз, але повільніше → фактично `realtime` з прискоренням від дій.
- Сутності падають, доки під ними є вільне; стоять стовпчиками, як у колодязі «падаючих блоків».
- Випадковий потік появи (`random: runtime`); рівні з різними ворогами й босом (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой | player | HP, атака, реліквії | рух 4 напрямки; вхід у ворога = удар |
| Ворог (тип X) | enemy | HP, атака, тип | падає згори; при ударі відповідає шкодою; групи однакових сусідів ділять шкоду |
| Бос | boss | HP, поведінка | кінець рівня (?); перемога відкриває нового героя |
| Зілля | pickup | +HP | зʼявляється серед потоку; взяти — лікування |
| Ключ / фрагмент ключа | pickup | — | ключ відкриває Tower of Fate; 4 фрагменти — справжня кінцівка |
| Самоцвіти | resource | — | падають з ворогів; валюта крамниць і частково мета-валюта |
| Реліквія | pickup | ефект | пасивний бонус до кінця забігу (напр., +HP); купується або знаходиться |
| Блок каменю/землі | object | — | займає місце в колодязі (?) |
| Крамниця | static | товари | між рівнями: реліквії за самоцвіти |
| Самоцвітний лічильник | — | шкала | наповнюється вбивствами, повільно спадає; повна — дедалі більше самоцвітів |

Герої (вибірка): Shovel Knight (базовий) · Specter Knight — лікується вбивствами · Prism Knight — телепортується по полю · Plague Knight — удар отруює · Puzzle Knight (DLC) · The Enchantress, Chester (DLC Paradox Pack).

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(move dir)` → ЯКЩО `free(target)` → ТО `move(hero, dir)`, далі `fall(all)`.
- КОЛИ `input(move dir)` → ЯКЩО `occupied(target, enemy)` → ТО `damage(enemy, atk)`, `fall(all)`.
- КОЛИ `contact(hero, enemy)` → ЯКЩО `not custom: «удар добиває»` → ТО `hp(hero, −enemy.atk)`; ЯКЩО добиває → шкоди герою нема.
- КОЛИ `contact(hero, enemy)` → ЯКЩО `connected(group of same type)` → ТО `custom: «уся звʼязна група однакових отримує ту саму шкоду»` (ланцюгова атака).
- КОЛИ `hp_zero(enemy)` → ТО `disappear_b`, `currency(+gems)`, `counter(gem_meter, +)`.
- КОЛИ `counter(gem_meter, >=, full)` → ТО `currency(+bonus gems)` (з кожним наповненням більше).
- КОЛИ `tick` → ТО `counter(gem_meter, −decay)`; `custom: «повільне осідання поля без дій»`.
- КОЛИ `timer(spawn)` або `after(player action)` → ТО `spawn_at(enemy|potion|item, top row)`.
- КОЛИ `contact(hero, potion)` → ТО `pickup`, `heal(hero, n)`.
- КОЛИ `contact(hero, key)` → ТО `pickup` → відкриває Tower of Fate; 4 фрагменти → справжня кінцівка.
- КОЛИ `custom: «усі 64 клітини зайняті»` → ТО `lose`.
- КОЛИ `hp_zero(hero)` → ЯКЩО `mode(infinite lives)` → ТО `respawn(hero)` повільно, поле далі заповнюється; інакше `lose`, `custom: «частина самоцвітів лишається для мета-розблокувань»`.
- КОЛИ `died(boss)` → ТО `unlock(hero)`, `next_level`.
- КОЛИ `input(shop buy)` → ЯКЩО `count(gems, >=, price)` → ТО `give(hero, relic)`.
- Здібності героїв: Specter — КОЛИ `died(enemy)` → ТО `heal(hero, n)`; Plague — КОЛИ `contact(hero, enemy)` → ТО `set_state(enemy, poisoned)`; Prism — `teleport(hero)`.
- Versus: КОЛИ `died(enemy)` у гравця A → ТО `speed(spawn of B, +)` — поле суперника заповнюється швидше.
- Перемога: пройти рівні до фіналу. Поразка: HP = 0 або поле переповнене. Рахунок: самоцвіти, прогрес, рекорди Daily (?).

## Керування і ввід
- 4 напрямки (геймпад/клавіатура/свайп на мобільних (?)); рух і атака — одна дія.
- Перемикання предметів/спорядження «на льоту» (Steam).
- Спецздібність героя — окрема кнопка (?).

## Вікна, меню, HUD
- `game-screen`: колодязь 8×8, `hp-bar` героя, HP на ворогах, `combo-meter` (самоцвітна шкала, що спадає), `coins` (самоцвіти), слоти реліквій, `progress-bar` рівня (?).
- `character-select` — вибір героя (розблоковані босами).
- `shop-window` — крамниця реліквій; Mr Hat's Fancy Shop (DLC).
- `map-window` / вибір рівня-локації (?); `mode-select`: Adventure · Versus · Daily Challenge.
- `settings-window` з доступністю: HP і атака героя, «нескінченні життя».
- `end-screen` — смерть: самоцвіти, що лишаються.
- Переходи: `main-menu` → `mode-select` → `character-select` → рівні з крамницями між ними → `end-screen`.

## Фічі поза полем
- `meta-progression` — частина самоцвітів після смерті → розблокування реліквій.
- `assist-mode` / `infinite-lives` — нескінченні життя, змінні HP й атака.
- `mode-versus` (2 гравці, split-screen), `mode-daily` (Daily Challenge), `unlockables` (герої), `achievements`, `cloud-save`, `mod-support` (Paradox Pack), `cheat-codes` (Paradox Pack), квести (Puzzler Pack).

## Варіації й родичі
- Родичі: [desktop-dungeons](desktop-dungeons.md) і [magic-tower](magic-tower.md) — детермінований bump-бій; [868-hack](868-hack.md); Dungeon Raid, 10000000, Puzzle Quest — match-3 + RPG; Tetris/Puyo — переповнення колодязя (сімʼя `falling-match`).
- Осі варіацій: **що падає** (вороги-«плитки» / лише блоки) · **шкода групі** (однаковий тип-сусід / колір / нема) · **темп** (лише дії / дрейф без дій / суто real-time) · **програш** (HP / переповнення / обидва).

## Цікавинки для курсу
- Поле 8×8 з падінням «плиток-ворогів» після кожної дії — `fall` стовпчиками — 📎.
- Bump-атака з правилом «добивальний удар безкоштовний» — 🌱 (чиста умова в бою).
- Шкода звʼязній групі однакових сусідів — flood fill по типу — 📎.
- Подвійна поразка: HP = 0 або колодязь повний — 🌱.
- Дрейф без дій (тік таймера) поверх покрокового руху — 📎 (два джерела тіку).
- Versus із «прискоренням» поля суперника за вбивства — 🥉.

## Мапа на каталог
- Є: `move-4dir` · `hp-damage` · `gravity-fall` ↔ осідання · `spawn-schedule` ↔ потік згори · `item-pickup`/`inventory-items` · `run-relics` · `shop-between-levels`/`shop-catalog` · `round-currency` (самоцвіти) · `player-death` · `character-select` · `simultaneous-versus` + `garbage-attack` (≈ прискорення суперника) · `daily-puzzle` · `cheat-codes` · `progress-acceleration` · `combo-multiplier` (≈ шкала самоцвітів) · `status-effects` (отрута Plague Knight) · `key-and-door` (ключ до Tower of Fate) · `sequential-levels`.
- **Нема** → пропозиції карток:
  - `+bump-attack` «Атака = крок у клітину ворога» · entities/combat · 🌱.
  - `+group-damage` «Шкода передається звʼязній групі однакових» · entities/combat · 📎.
  - `+board-overflow` «Поле заповнилось — програш» · game-logic/lose · 🌱.
  - `+kill-blow-free` «Добивальний удар не коштує HP» · entities/combat · 🌱.
  - `+idle-drift` «Поле зсувається і без дій, повільніше» · entities/move · 📎.
  - `+gem-meter-decay` «Шкала комбо, що спадає з часом» · game-logic/score · 🌱.
  - `+meta-currency-keep` «Частина валюти лишається після смерті» · game-logic/economy · 🌱.

## Пропозиції до словників
- `+trigger:board_full` — усі клітини поля зайняті (переповнення колодязя).
- `+effect:group_damage(group, n)` — шкода всій звʼязній групі; `+effect:drift(all, down)` — зсув усього поля без дії гравця.
- `+cond:killing_blow` — удар добиває ціль.
- `+feature:infinite-lives` — смерть без кінця гри, лише затримка.
- `+card:bump-attack` · `+card:group-damage` · `+card:board-overflow` · `+card:idle-drift`.

## Джерела
- ⭐ [Wikipedia: Shovel Knight Pocket Dungeon](https://en.wikipedia.org/wiki/Shovel_Knight_Pocket_Dungeon) — поле 8×8, падіння й дрейф, bump, безкоштовний добивальний удар, шкода групі, переповнення, самоцвіти й реліквії, герої, versus, Tower of Fate.
- [Steam](https://store.steampowered.com/app/1184760/Shovel_Knight_Pocket_Dungeon/) — режими, 10+ героїв, DLC (Puzzler Pack, Paradox Pack), мод-підтримка, чіт-коди.

## Непевне
- (?) Скрині, що відкриваються ключами, блоки землі/каменю, бомби, вихід-двері, що відкривається після прогресу рівня, — з памʼяті, у відкритих джерелах не описано.
- (?) Кількість рівнів/локацій, шкала прогресу рівня, бос наприкінці кожної локації.
- (?) Як саме реліквії перемикаються «на льоту» і скільки слотів.
- (?) Чи падіння на гравця шкодить/виштовхує героя — не знайшов.
- (?) Daily Challenge: спільний seed і таблиця — за аналогією, не перевірено.
