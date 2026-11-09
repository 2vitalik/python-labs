---
title: Flash Element TD
slug: flash-element-td
aka: [FETD, Flash Element Tower Defense]
family: tower-lanes
also: []
klass: cursor
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: none
  goal: survive
year: 2007
platforms: [web (Flash), web (Go/Ebitengine ремейк)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Flash_Element_TD", best: true, note: "історія: Flash-спрощення WC3-мапи Element TD, версії 1 і 2"}
  - {kind: play, url: "https://enbiggen.itch.io/flash-element-td", note: "ремейк v1.5 від автора: правила дерева, стихій, відсотків, гарячі клавіші"}
  - {kind: other, url: "https://gigazine.net/gsc_news/en/20070112_flash_element_td", note: "огляд 2007: базові вежі Arrow/Cannon/Air, наземні й повітряні, дерево кожні 7 рівнів"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Tower_defense", note: "FETD як приклад «ворогів, що біжать лабіринтом»"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=flash+element+td+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [enemy-waves, spawn-schedule, spawn-points, enemy-reached-base, player-death, tower-placement, tower-range, round-currency, in-round-upgrades, shop-buyback, shop-catalog, projectile-shot, shoot-cooldown, blast-wave, temporary-modes, hp-damage, speed-per-type, game-pause, keyboard-controls, cell-click, drag-drop-piece, status-panel, +interest-economy, +call-wave-early, +second-currency, +element-unlock, +element-combo-tower, +immune-enemy, +target-air-ground]
proposes: ["+effect:sell", "+effect:upgrade", "+effect:interest", "+role:tower", "+ui:range-circle", "+ui:next-wave-button", "+ui:wood-counter", "+trigger:boss_wave"]
author: opus
date: 2026-11-09
---

# Flash Element TD — браузерна класика: вежі на траві вздовж дороги, деревина за боса відкриває стихії

## Суть
Кріпи йдуть звивистою дорогою від входу до виходу; гравець ставить вежі на траву обабіч і за золото їх апгрейдить. Друга валюта — **деревина** (wood), що падає за босові хвилі: нею відкривають стихійні вежі (вода, вогонь, земля), купують ставку відсотків або додаткові життя. Відкрито всі три стихії — доступна ракетна вежа. Відмінність від Desktop TD: шлях фіксований (вежі не стають лабіринтом), а головне рішення — **на що витратити рідкісну деревину**: силу, економіку чи запас життів.

## Поле і час
- Одна мапа-сітка: дорога (непрохідна для будування) і трава (будувати можна); вежі не перекривають шлях.
- Real-time: хвилі (levels) йдуть одна за одною; кнопкою/пробілом викликають наступну раніше; є пауза й прискорення (F перемикає швидкості в ремейку).
- Видно все поле; туману нема.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Вхід | spawner | — | хвиля виходить сюди |
| Вихід | static | — | кріп дійшов → −1 життя |
| Дорога | terrain | фіксована | кріпи йдуть по ній; будувати не можна |
| Трава | terrain | — | місце для веж |
| Arrow | tower | 3 апгрейди | мала шкода, швидкий темп; бʼє наземних і повітряних |
| Cannon | tower | 3 апгрейди | повільно, але сильно; лише наземні; апгрейд — шкода по площі навколо цілі (?) |
| Air | tower | 3 апгрейди | лише повітряні; шкода + темп + дальність |
| Water | tower | за деревину | сповільнює кріпів |
| Fire | tower | за деревину | додаткова шкода імунним кріпам |
| Earth | tower | за деревину | повністю прокачана — шанс оглушити |
| Rocket | tower | усі 3 стихії | відкривається лише після трьох стихій |
| Наземний кріп | enemy | HP | іде дорогою |
| Повітряний кріп | enemy | HP | летить; бʼють лише Arrow/Air (і ті, що вміють) |
| Швидкий кріп | enemy | швидкість | частина хвиль бігає швидше |
| Імунний кріп | enemy | — | вода не сповільнює, вогонь бʼє сильніше |
| Бос | boss | багато HP | босова хвиля; дає 1 деревину |
| Бонус-рівень | enemy | величезна зграя | після рівня 30 (за оглядом 2007) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(place, tower, cell)` → ЯКЩО `cell(cell, grass)` and `free(cell)` and `has(player, gold)` → ТО `place(player, tower)`, `currency(-cost)`; інакше `block`.
- КОЛИ `schedule(levels)` або `input(send_wave)` → ТО `spawn_at(creeps, entrance)`, `counter(level, +1)`.
- КОЛИ `tick` → кріп `move(a, next_on_road)`.
- КОЛИ `in_range(tower, creep, r)` → ЯКЩО `custom: «тип цілі дозволений: Arrow — обидва, Cannon — наземні, Air — повітряні»` → ТО `spawn(projectile)` з періодом `shoot-cooldown`.
- КОЛИ `contact(projectile, creep)` → ТО `damage(n)`; апгрейджений Cannon — `damage` по площі навколо цілі (?).
- КОЛИ `contact(water_shot, creep)` → ЯКЩО `not state(creep, immune)` → ТО `speed(creep, ×k)`.
- КОЛИ `contact(fire_shot, creep)` → ЯКЩО `state(creep, immune)` → ТО `damage(n × bonus)`.
- КОЛИ `contact(earth_shot, creep)` → ЯКЩО `custom: «вежа Earth на максимальному рівні»` and `prob(p)` → ТО `stun(creep, n)`.
- КОЛИ `hp_zero(creep)` → ТО `disappear(creep)`, `currency(+bounty)`, `score(+n)`.
- КОЛИ `hp_zero(boss)` → ТО `counter(wood, +1)`.
- КОЛИ `input(spend_wood, element)` → ЯКЩО `counter(wood, >=, 1)` → ТО `counter(wood, -1)`, `unlock(element_tower)`.
- КОЛИ `input(spend_wood, interest)` → ТО `counter(wood, -1)`, `custom: «ставка відсотків зростає»`.
- КОЛИ `input(spend_wood, lives)` → ТО `counter(wood, -1)`, `lives(+n)`.
- КОЛИ `custom: «відкрито water, fire і earth»` → ТО `unlock(rocket_tower)`.
- КОЛИ `wave_cleared` → ТО `custom: «effect interest: +% від невитраченого золота до доходу»`.
- КОЛИ `reach(creep, exit)` → ТО `lives(-1)`, `disappear(creep)`.
- КОЛИ `counter(lives, ==, 0)` → ТО `lose`.
- КОЛИ `input(upgrade, tower)` → ЯКЩО `has(player, gold)` → ТО `custom: «effect upgrade: шкода, у частини веж — дальність або площа»` (3 рівні).
- КОЛИ `input(sell, tower)` → ТО `custom: «effect sell: повернути частину ціни»`, `disappear(tower)`.
- Перемога: пройти всі рівні (?) · Поразка: життя = 0 · Рахунок: очки за кріпів.

## Керування і ввід
- Миша: клік по кнопці вежі → клік по траві; на телефоні (ремейк) — тягнути вежу з нижнього меню.
- Клік по вежі → Upgrade / Sell.
- Клавіші (ремейк v1.5): `Space` — надіслати хвилю, `1–3` — три базові вежі, `U` — апгрейд, `S` — продаж, `Esc` — скасувати, `F` — швидкість, `P` — пауза, `O` — повноекранний, `R` — скинути гру.

## Вікна, меню, HUD
- `game-screen`: мапа з дорогою, панель веж з цінами, `coins` (золото), `+ui:wood-counter`, `lives`, `score`, `level-number`, `next-wave-preview` (?), `+ui:next-wave-button`, `+ui:range-circle`.
- Панель вибраної вежі: характеристики, Upgrade, Sell.
- Панель деревини: Water / Fire / Earth / Interest / Lives.
- `end-screen` — рахунок після поразки/перемоги.

## Фічі поза полем
- `pause`, `speed-control` (ремейк), `fullscreen`, `touch-controls` (ремейк).
- Версії: 1.0 (12.01.2007, щоденні оновлення до 22.01), 2 (2008), ремейк Golang/Ebitengine v1.5 з переробленими Earth і Rocket.

## Варіації й родичі
- Батько — WC3-мапа Element TD (Brian Powers, Evan Hatampour) → наступник `element-td-2` (6 стихій, комбо-вежі, мейзинг-розширення).
- Сусіди: `desktop-tower-defense` (той самий 2007 рік, але лабіринт з веж), `fieldrunners`, `gemcraft` (комбінування самоцвітів замість стихій).
- **Осі варіацій**: шлях — фіксований / лабіринт · друга валюта — нема / за боса / за час · на що йде рідкісна валюта — сила / економіка / життя · стихії — лінійні вежі / комбінації (Element TD 2) / самоцвіти (GemCraft).

## Цікавинки для курсу
- Дві валюти: золото щохвилі і деревина за боса — вибір «стихія / відсотки / життя» — 📎.
- Відсотки на невитрачене золото наприкінці хвилі (не витрачай під кінець) — 🌱.
- Розблокування вежі за набором трьох стихій — 🌱 (множина + перевірка підмножини).
- Цілі за типом (наземні/повітряні) у кожної вежі — 🌱.
- Імунітет: вода не діє, вогонь бʼє більше — 📎 (таблиця модифікаторів «стан × вежа»).

## Мапа на каталог
- Є: `enemy-waves` + `spawn-schedule` + `spawn-points` · `enemy-reached-base` + `player-death` · `tower-placement` + `tower-range` · `round-currency` · `in-round-upgrades` (3 рівні) · `shop-buyback` · `shop-catalog` · `projectile-shot` + `shoot-cooldown` · `blast-wave` ↔ площа Cannon · `temporary-modes` ↔ сповільнення/оглушення · `hp-damage` · `speed-per-type` · `game-pause` · `keyboard-controls` · `cell-click` · `drag-drop-piece` (мобільний ремейк) · `status-panel`.
- **Нема** → пропозиції карток:
  - `+second-currency` «Рідкісна друга валюта» · game-logic/economy · 📎 · слот {source}.
  - `+element-unlock` «Відкриття типів веж валютою» · game-logic/economy · 🌱.
  - `+element-combo-tower` «Вежа за набором стихій» · game-logic/economy · 🌱 · слот {requires}.
  - `+immune-enemy` «Імунітет до ефекту» · entities/state · 🌱.
  - `+target-air-ground` «Ціль за типом (земля/повітря)» · entities/combat · 🌱.
  - `+interest-economy`, `+call-wave-early` — див. родину.

## Пропозиції до словників
- `+effect:sell`, `+effect:upgrade`, `+role:tower`, `+ui:range-circle`, `+ui:next-wave-button` — підтвердження з родини.
- `+effect:interest` — % від запасу валюти (підтвердження).
- `+ui:wood-counter` — лічильник другої валюти.
- `+trigger:boss_wave` — почалась/закінчилась босова хвиля (для нагород).

## Джерела
- ⭐ [Wikipedia: Flash Element TD](https://en.wikipedia.org/wiki/Flash_Element_TD) — автор David Scott, реліз 12.01.2007, спрощення WC3-мапи Element TD, версія 2 (2008), поширення.
- [itch.io: Flash Element TD v1.5](https://enbiggen.itch.io/flash-element-td) — «towers on the grass», деревина на стихії/відсотки/життя, бос дає 1 деревину, вода сповільнює, імунні + вогонь, Earth оглушує, Rocket за 3 стихії, відсотки після хвилі, гарячі клавіші.
- [Gigazine (2007)](https://gigazine.net/gsc_news/en/20070112_flash_element_td) — старт 40 золота, Arrow/Cannon/Air і цілі, деревина кожні 7 рівнів, бонус-рівень після 30.
- [Wikipedia: Tower defense](https://en.wikipedia.org/wiki/Tower_defense) — FETD як приклад жанру.
- YouTube: пошук «flash element td gameplay».

## Непевне
- (?) Дорога в оригіналі 2007 повністю фіксована — так виходить з «towers on the grass», але черга корпусу писала «лабіринт з веж»; власне мейзинг — у WC3-оригіналі й Element TD 2.
- (?) Кількість рівнів (30 + бонус? 40?), стартові життя, ставки відсотків.
- (?) Чи мала версія 2007 вежу Air і стихії в тому самому складі, що ремейк v1.5 (автор міняв Earth і Rocket).
- (?) Чи є прев'ю наступної хвилі в HUD.
