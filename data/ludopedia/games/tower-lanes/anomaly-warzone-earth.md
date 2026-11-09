---
title: "Anomaly: Warzone Earth"
slug: anomaly-warzone-earth
aka: [Anomaly, AWE]
family: tower-lanes
also: [tactics]
klass: hybrid
axes:
  field: graph
  time: realtime
  opponent: ai
  info: full
  random: none
  goal: state
year: 2011
platforms: [PC, Mac, iOS, Android, Xbox 360, PS3, BlackBerry 10]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Anomaly:_Warzone_Earth", best: true, note: "reverse TD: маршрут конвою вулицями, юніти, Commander з power-up-ами, платформи й дати"}
  - {kind: steam, url: "https://store.steampowered.com/app/91200/", note: "опис: маршрут, вибір юнітів, ресурси в бою, кампанія + 2 режими Squad Assault"}
  - {kind: other, url: "https://mogelpower.de/cheats/loesung.php?id=39998", note: "гайд: ціни/HP юнітів, апгрейди ×2, 4 здібності, 6 типів веж, продаж"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Tower_defense", note: "Anomaly як перша «reverse tower defense»"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=anomaly+warzone+earth+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [enemy-waves, hp-damage, projectile-shot, shoot-cooldown, tower-range, threat-range, explode-area, beam-tracing, status-effects, melee-vs-ranged, speed-per-type, in-round-upgrades, shop-buyback, round-currency, item-pickup, respawn, temporary-modes, coverage-area, path-preview, map-window, sequential-levels, leaderboard, achievements-window, mode-select, difficulty-select, +reverse-td, +route-planning, +convoy-order, +support-abilities, +target-priority, +tower-revive]
proposes: ["+trigger:junction", "+cond:target_priority", "+effect:set_route", "+effect:reorder", "+effect:revive", "+effect:drain_shield", "+effect:sell", "+role:convoy-unit", "+role:commander", "+ui:route-line", "+ui:ability-gauge", "+ui:convoy-panel", "+window:tactical-map", "+axis:control", "+card:route-planning", "+card:convoy-order", "+card:support-abilities", "+card:target-priority"]
author: opus
date: 2026-11-09
---

# Anomaly: Warzone Earth — «tower defense навпаки»: прокладаєш маршрут конвою вулицями міста повз ворожі вежі й підтримуєш його здібностями

## Суть
Ролі TD перевернуто: вежі — у ворога (інопланетні турелі), а гравець веде **конвой** броньованих машин вулицями міста до цілі. Машинами напряму не керують: на тактичній карті гравець задає маршрут — куди звертати на перехрестях, — а конвой їде сам, і його юніти автоматично стріляють по вежах у радіусі. Гравець купує й апгрейдить юніти, міняє їх порядок у колоні й керує піхотинцем **Commander**, який підбирає й ставить здібності (ремонт, дим, приманка, авіаудар). Клас — гібрид: `cursor` (маршрут і склад конвою) + `avatar` (Commander на ПК/консолях).

## Поле і час
- Карта — квартали міста (Багдад, Токіо, …); дороги утворюють граф перехресть, конвой рухається лише ними, по одній колоні з фіксованою швидкістю.
- Вежі стоять уздовж вулиць і мають радіус; конвой проїжджає крізь їх зони — гра про **вибір маршруту**, де бій буде вигідним.
- Тактична карта — окремий шар/екран огляду: усі вулиці, вежі, цілі; на ній малюється маршрут (?).
- Commander (ПК, XBLA, PSN) ходить вільно по місту поруч із конвоєм; на iOS/Android його нема — здібності ставлять тачем прямо на карту.
- Real-time; камера стежить за конвоєм/Commander (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Commander | player | HP, регенерація | ходить вільно; підбирає й ставить здібності; гине → повертається за час |
| APC | ally | $100; HP 120→300; атака 60→96 | дешевий «губка шкоди», коротка дальність |
| Crawler | ally | $125; HP 70→112; атака 85→280 | найбільша шкода й дальність, повільна стрільба |
| Shield Generator | ally | $150; HP 125; щит 40→80 | без атаки; щит собі й сусіднім у колоні |
| Tank | ally | $200; HP 140→308; атака 75→165 | повільніше стріляє, сильніше бʼє, багато HP |
| Dragon | ally | $250; HP 120→220; атака 65→123 | два вогнемети: бʼє 2 цілі, підпалює |
| Supply Truck | ally | $175; HP 120 | без атаки; наповнює шкалу здібностей Commander |
| Blaster | enemy | мало HP, середня дальність | швидко повертається й стріляє, слабка шкода |
| Scorcher | enemy | багато HP, дуже велика дальність | плазмовий промінь, **не повертається** — підходити збоку |
| Behemoth | enemy | дуже багато HP | повільно повертається, площинна шкода (AOE) |
| Storm Ray | enemy | середнє HP | знімає щити, сповільнює Commander, бʼє другу ціль поруч |
| Hacker | enemy | дуже багато HP, без шкоди | AOE: змушує юнітів стріляти по Commander; ігнорує дим |
| Energizer | enemy | мало HP | нейтралізує здібності; **воскрешає** знищені вежі за ~3 с |
| Ремонт (Repair) | zone | малий радіус, коротко | лікує юнітів у зоні: % від макс. HP за час у зоні |
| Дим (Smoke) | zone | радіус | вежі, що стріляють у зону, часто мажуть |
| Приманка (Decoy) | object | своє HP і таймер | вежі в радіусі бʼють її першою |
| Авіаудар (Airstrike) | zone | ~2 сусідні вежі | шкода вежам, не своїм |
| Здібність на дорозі | pickup | тип | Commander підбирає → у запас |
| Ціль місії | static | — | дійти / знищити / дослідити аномалію |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(click, junction)` (на тактичній карті) → ТО `custom: «set_route: на цьому перехресті конвой звертає сюди; маршрут — ланцюг вулиць»`.
- КОЛИ `tick` → ТО `move(convoy, next_on_route)`; колона їде одна за одною з фіксованою швидкістю.
- КОЛИ `input(buy, unit)` → ЯКЩО `has(money, cost)` → ТО `custom: «додати юніт у колону»`, `currency(-cost)`.
- КОЛИ `input(upgrade, unit)` → ЯКЩО `has(money, cost)` and `custom: «рівень < 3»` → ТО `transform(unit_tier+1)`, `currency(-cost)`; ціна кожного апгрейда — ×2 від попереднього.
- КОЛИ `input(sell, unit)` → ТО `currency(+value × hp/max_hp)`, `disappear_b` (апгрейди повертаються повністю, але пропорційно HP).
- КОЛИ `input(reorder, unit, pos)` → ТО `custom: «reorder: змінити позицію юніта в колоні»` (далекобійні — назад, міцні — вперед).
- КОЛИ `in_range(unit, tower, r)` → ЯКЩО `custom: «перезаряд готовий»` → ТО `spawn(projectile)` / `damage(n)` (автоматично).
- КОЛИ `in_range(tower, target, r)` → ЯКЩО `custom: «повернута до цілі»` → ТО `damage(n)`; пріоритет: Decoy > юніти > Commander.
- КОЛИ `hp_zero(tower)` → ТО `disappear_a`, `currency(+bounty)`.
- КОЛИ `died(tower)` → ЯКЩО `in_range(energizer, tower, r)` and `timer(<, 3)` → ТО `custom: «revive: вежа відновлюється»`.
- КОЛИ `contact(storm_ray_shot, unit)` → ТО `custom: «drain_shield»`, `speed(commander, ×k)`.
- КОЛИ `in_range(hacker, unit, r)` → ТО `custom: «юніти перемикають ціль на Commander»`.
- КОЛИ `counter(kills, ≥, ability_cost)` (шкала Supply Truck) → ТО `spawn_at(ability_pickup, near(commander))`; апгрейд Truck змінює наступну здібність по колу: Repair → Smoke → Decoy → Airstrike.
- КОЛИ `contact(commander, ability_pickup)` → ТО `pickup`.
- КОЛИ `input(use, ability, cell)` → ЯКЩО `has(commander, ability)` and `custom: «cooldown минув»` → ТО `spawn_at(zone, cell)`.
- КОЛИ `enter(unit, repair_zone)` → ТО `heal(unit, % max_hp)` щотік; КОЛИ `enter(unit, smoke_zone)` → ТО `set_state(unit, hard_to_hit)`.
- КОЛИ `hp_zero(unit)` → ТО `disappear_a`; КОЛИ `hp_zero(commander)` → ТО `respawn(commander, convoy)` за час, без підтримки в цей час.
- КОЛИ `all_gone(convoy_unit)` → ТО `lose`.
- КОЛИ `reach(convoy, objective)` / `custom: «ціль місії виконано»` → ТО `win`, `next_level`.
- Перемога: виконати ціль місії (дійти, знищити ключові вежі) · Поразка: конвой знищено · Рахунок: очки місії для таблиць рекордів (?).

## Керування і ввід
- Миша/клавіатура (ПК): Commander — рух (WASD або клік (?)); здібності — гарячі клавіші/кнопки; тактична карта — клавіша-перемикач, клік по перехрестях = маршрут.
- Тач (iOS/Android): без Commander; здібності кладуться пальцем на карту, маршрут — тапом по перехрестях.
- Панель конвою: купити / апгрейд / продати / переставити юніт; на ПК — підтримка тачскрину Windows 7.

## Вікна, меню, HUD
- `main-menu` → Campaign / Squad Assault (2 режими) / налаштування; `mode-select`, `difficulty-select` (?).
- `map-window` «тактична карта» (`+window:tactical-map`): місто згори, вежі, маршрут лінією (`+ui:route-line`), ціль місії.
- `game-screen`: конвой і Commander, `hp-bar` над юнітами, `ability-buttons` з кількістю здібностей, `+ui:ability-gauge` (шкала Supply Truck), `coins` (гроші), `objective-text`, `minimap` (?).
- `shop-window` / `+ui:convoy-panel` — склад колони, ціни, апгрейди, порядок.
- `pause-menu`, `end-screen` з очками, `leaderboard` (Steam), `achievements-window`, `settings-window`.

## Фічі поза полем
- Кампанія з місій (`levels-sequential`, Багдад → Токіо; Токіо нема в мобільних версіях); 2 режими Squad Assault.
- `in-round-upgrades`: гроші з веж — нові юніти й апгрейди прямо в місії; продаж юнітів.
- `leaderboard-online`, `achievements`, `cloud-save`, Steam Trading Cards.
- Мобільна версія — інша схема вводу (без аватара): той самий двіжок, інший шар керування.

## Варіації й родичі
- Сиквели: Anomaly: Korea (2012, нові юніти й здібності), Anomaly 2 (2013: юніти-трансформери, режим мультиплеєра «вежі проти конвою» (?)).
- Реверс-TD у корпусі: [pvz-puzzle-modes](pvz-puzzle-modes.md) (I, Zombie), [mechabellum](mechabellum.md) (обидві армії атакують); класичні TD — [plants-vs-zombies](plants-vs-zombies.md), [fieldrunners](fieldrunners.md).
- Інші tower offense: Kingdom Rush-подібні «навпаки», Tower Offense-флеш-ігри (?).
- **Осі варіацій**: роль — оборона / напад · керування юнітами — пряме / маршрут на графі / жодного (I, Zombie) · підтримка — аватар зі здібностями / курсор · порядок колони — фіксований / переставний · ворожа оборона — статична / з воскресінням (Energizer).

## Цікавинки для курсу
- Маршрут на графі вулиць кліками по перехрестях, конвой їде сам — 🥉 (граф доріг + рух по шляху).
- Колона з порядком: щит покриває сусідів, далекобійні ззаду, переставляння як тактика — 📎.
- Вежі з кутом повороту (Scorcher не повертається, Behemoth повільно) — заходити збоку — 🥈 (орієнтація + швидкість повороту).
- Пріоритет цілей веж: Decoy > юніти > Commander; Hacker перемикає пріоритет — 📎.
- Energizer воскрешає вежі за 3 с, якщо не вбити його першим — 📎.
- Шкала здібностей за вбивства з циклом типів Repair→Smoke→Decoy→Airstrike — 🌱.
- Продаж юніта з поверненням, пропорційним HP — 🌱.

## Мапа на каталог
- Є: `enemy-waves` (наближено — тут статичні вежі) · `hp-damage` · `projectile-shot` + `shoot-cooldown` · `tower-range` + `threat-range` ↔ радіуси веж · `explode-area` ↔ Behemoth, авіаудар · `beam-tracing` ↔ промінь Scorcher (наближено) · `status-effects` ↔ дим, сповільнення, підпал · `melee-vs-ranged` · `speed-per-type` · `in-round-upgrades` · `shop-buyback` ↔ продаж юніта · `round-currency` ↔ гроші з веж · `item-pickup` ↔ здібності · `respawn` ↔ Commander · `temporary-modes` + `coverage-area` ↔ зони здібностей · `path-preview` ↔ лінія маршруту · `map-window` ↔ тактична карта · `sequential-levels` · `leaderboard` · `achievements-window` · `mode-select` · `difficulty-select`.
- **Нема** → пропозиції карток:
  - `+reverse-td` — див. pvz-puzzle-modes.
  - `+route-planning` «Маршрут кліками по вузлах графа доріг» · entities/move · 🥉 · слот {graph: streets}.
  - `+convoy-order` «Колона з порядком і ефектами сусідства» · entities/move · 📎.
  - `+support-abilities` «Здібності-зони підтримки (ремонт, дим, приманка, удар)» · entities/combat · 🥉 · слот {radius, duration}.
  - `+target-priority` «Пріоритет цілей ворога» · game-logic/opponent · 📎 · слот {order}.
  - `+tower-revive` «Воскресіння знищених сутностей сусідом» · entities/death · 📎 · слот {delay}.

## Пропозиції до словників
- `+trigger:junction` — сутність досягла вузла графа доріг (перехрестя) — тут вирішується поворот.
- `+cond:target_priority` — ціль обирається за пріоритетом типів (приманка > юніти > аватар).
- `+effect:set_route` — задати маршрут як послідовність вузлів графа.
- `+effect:reorder` — змінити позицію сутності в колоні/черзі.
- `+effect:revive` — повернути знищену сутність (Energizer).
- `+effect:drain_shield` — зняти щит без шкоди HP.
- `+effect:sell` — продати свою сутність з поверненням (повтор із dungeon-warfare).
- `+role:convoy-unit` — юніт гравця, що рухається маршрутом без прямого керування; `+role:commander` — аватар підтримки поряд із юнітами.
- `+ui:route-line` — лінія запланованого маршруту на карті; `+ui:ability-gauge` — шкала накопичення здібності; `+ui:convoy-panel` — склад колони з купівлею/апгрейдом/порядком.
- `+window:tactical-map` — тактична карта, на якій планують маршрут (не просто `map-window` для огляду).
- `+axis:control` — `indirect` (маршрут) + `direct` (Commander) в одній грі.
- `+card:route-planning`, `+card:convoy-order`, `+card:support-abilities`, `+card:target-priority` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Anomaly: Warzone Earth](https://en.wikipedia.org/wiki/Anomaly:_Warzone_Earth) — «reverse tower defense / tower offense», машинами не керують, маршрут вулицями, power-up-и (decoy, smoke), купівля юнітів, Commander лише на ПК/консолях, мобільні без Токіо; 11 bit studios, дати релізів, сиквели.
- [Steam: Anomaly: Warzone Earth](https://store.steampowered.com/app/91200/) — планування маршруту, вибір юнітів, ресурси в бою, кампанія + 2 Squad Assault, таблиці рекордів, тачскрин.
- [Mogelpower: Anomaly – Warzone Earth (e)](https://mogelpower.de/cheats/loesung.php?id=39998) — неофіційний англомовний гайд: 6 юнітів з цінами/HP/атакою, апгрейди ×2, Supply Truck і цикл здібностей, 6 типів веж, пріоритет цілей, продаж пропорційно HP.
- [Wikipedia: Tower defense](https://en.wikipedia.org/wiki/Tower_defense) — Anomaly як перша «reverse tower defense».
- YouTube: пошук «anomaly warzone earth gameplay».

## Непевне
- (?) Чи тактична карта ставить гру на паузу/сповільнює; як саме малюється маршрут (клік по перехрестях — з памʼяті).
- (?) Числа юнітів і веж — з неофіційного гайду (2011), версія гри не вказана; назва «Tank» (у грі, можливо, Heavy Tank).
- (?) Чи здібності також випадають з веж/лежать на картах, окрім шкали Supply Truck (Wikipedia: «drop power-ups»).
- (?) Назви й правила двох режимів Squad Assault; рівні складності; рахунок місії.
- (?) Мультиплеєр Anomaly 2 (вежі проти конвою) — з памʼяті.
- (?) `field: graph` — вулиці як граф; Commander при цьому ходить вільно (`free`).
