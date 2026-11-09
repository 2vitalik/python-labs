---
title: Rocket Mania!
slug: rocket-mania
aka: [Rocket Mania Deluxe]
family: connect-rotate
also: [falling-match]
klass: cursor
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: score
year: 2003
platforms: [Windows, Windows Mobile, Palm OS]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Rocket_Mania", best: true, note: "правила, предмети, три режими, рахунок"}
  - {kind: other, url: "https://www.oocities.org/tstodden.geo/GameReviews/PC/Rocket_Mania_Deluxe.html", note: "огляд Deluxe: підсвітка зʼєднань, кліки, режими"}
  - {kind: other, url: "https://www.esrb.org/ratings/9612/rocket-mania-deluxe/", note: "рейтинг Deluxe (лише бачив у пошуку)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Rocket+Mania+PopCap+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [tile-rotate, pipe-connectors, cell-click, drag-drop-piece, gravity-fall, explode-area, item-pickup, collect-quota, time-out, event-points, highlights, mode-select, difficulty-levels, sequential-levels, game-screen, end-screen, main-menu, +edge-to-edge-path, +burn-path-clear, +refill-from-top, +branching-multi-launch, +multi-launch-bonus, +upgrade-by-coins, +timer-freeze-pickup, +limited-ignitions, +expiring-pickup, +falling-tile-steer, +rank-title]
proposes: ["+effect:ignite", "+ui:connection-tint", "+ui:lantern-timer", "+card:edge-to-edge-path", "+card:burn-path-clear", "+card:limited-ignitions"]
author: opus
date: 2026-11-09
---

# Rocket Mania! — крути плитки-ґноти, щоб вогонь від сірників зліва дійшов до ракет справа; згорілий шлях зникає, згори падають нові плитки

## Суть
Поле — сітка плиток-ґнотів; уздовж лівого краю горять сірники, уздовж правого стоять феєрверкові ракети. Гравець крутить плитки, щоб скласти неперервний ґніт від лівого краю до правого; зʼєднаний ґніт загоряється, ракети злітають, згорілі плитки зникають, верхні падають, згори сиплються нові. Ядро — гібрид Infinity Loop і match-3: обертання для звʼязності + гравітаційне поповнення, а розгалуження (Т і хрест) дають кілька запусків разом і бонус.

## Поле і час
- Квадратна сітка; лівий край — сірники (джерела), правий — ракети (приймачі) по рядах. Розмір — (?)
- Гравітація лише для плиток: після згоряння стовпці осідають, порожні клітини згори заповнюють нові випадкові плитки.
- Real-time з різним тиском за режимом: Classic — таймер рівня (ряд ліхтариків), Arcade — плитки падають по одній у порожню сітку, Strategy — без таймера, обмежений запас сірників.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Плитка-ґніт | conduit | тип: пряма, кут (?), Т (3 виходи), хрест (4 виходи); орієнтація | крутиться кліком; проводить вогонь між сусідніми портами |
| Сірник | source | ряд на лівому краї | підпалює зʼєднаний з ним ґніт |
| Ракета | sink | рівень 1–10 | злітає, коли вогонь доходить; вищий рівень — більше очок |
| Монета | pickup | — | 5 монет → ракета +1 рівень; Classic — падають на поле після кількох запусків разом |
| Годинник | pickup | — | ненадовго заморожує таймер (Classic) |
| Самоцвіт | pickup | — | бонусні очки |
| Бомба | pickup | радіус | знищує сусідні плитки й предмети |
| Сірник-предмет | pickup | живе 3 запуски | +1 сірник у запас (Strategy); зʼявляється після запуску 3+ ракет |
| Ряд ліхтариків | mark | час рівня | таймер Classic |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(click_left, tile)` → ТО `rotate(tile, 90)`; КОЛИ `input(click_right, tile)` → ТО `rotate(tile, -90)`.
- КОЛИ `input(rotate, tile)` → ЯКЩО `path_exists(match, tile)` → ТО `custom: «плитка жовта»`; ЯКЩО `path_exists(tile, rocket)` → ТО `custom: «плитка червона»`; інакше `custom: «плитка біла»`.
- КОЛИ `input(rotate, tile)` → ЯКЩО `path_exists(match, rocket)` → ТО `custom: «ґніт загоряється від сірника»`.
- КОЛИ `custom: «вогонь дійшов до розгалуження»` → ТО `custom: «вогонь іде всіма гілками одночасно»`.
- КОЛИ `custom: «вогонь дійшов до ракети»` → ТО `custom: «ракета злітає»`, `score(+value(rocket.level))`, `counter(rockets, +1)`.
- КОЛИ `custom: «згоріла плитка з предметом»` → ТО `pickup(player, item)`.
- КОЛИ `picked(player, coin)` → ТО `counter(coins, +1)`; КОЛИ `counter(coins, ==, 5)` → ТО `custom: «ракета +1 рівень, до 10»`, `counter(coins, -5)`.
- КОЛИ `picked(player, clock)` → ТО `timer(stop, short)`.
- КОЛИ `picked(player, gem)` → ТО `score(+n)`.
- КОЛИ `picked(player, bomb)` → ТО `explode(radius, n)`.
- КОЛИ `custom: «ґніт догорів»` → ТО `disappear(burned_tiles)`, `fall(tiles_above)`, `spawn_at(random_tile, top)`.
- КОЛИ `counter(launched_at_once, >=, 5)` → ТО `score(+bonus)`.
- Classic: КОЛИ `counter(launched_at_once, >=, 2)` → ТО `spawn_at(coin, field)` (?).
- Classic: КОЛИ `counter(time_left, ==, 0)` → ЯКЩО `counter(rockets, >=, quota)` → ТО `score(+unused_coins)`, `next_level` (нова сітка); інакше `game_over`.
- Classic: КОЛИ `counter(coins, >, 0)` → ЯКЩО `custom: «усі ракети вже рівня 10»` → ТО `score(+bonus)`.
- Arcade: КОЛИ `timer(drop)` → ТО `spawn_at(tile, top)`, `fall(tile)`; поки падає — `move(tile, left|right)` або `rotate(tile, 90)`.
- Arcade: КОЛИ `custom: «стовпець заповнено до верху»` → ЯКЩО `custom: «місця не звільнити»` → ТО `game_over`.
- Strategy: КОЛИ `custom: «ґніт загоряється»` → ТО `counter(matches, -1)` за кожен шлях зліва направо.
- Strategy: КОЛИ `counter(launched_at_once, >=, 3)` → ТО `spawn_at(match_item, field)`, `set_state(match_item, expires, 3)`; не зібраний за 3 запуски — `disappear(match_item)`.
- Strategy: КОЛИ `counter(matches, ==, 0)` → ТО `game_over`.
- Перемога: Classic — квота ракет за час, рівень за рівнем; Arcade і Strategy — нескінченні на рахунок. Поразка: час вийшов без квоти / стовпець переповнено / сірники скінчились. Рахунок: за ракету (за її рівнем), бонус за 5+ разом, невитрачені монети; звання піротехніка за сумою очок.

## Керування і ввід
- Миша: лівий клік — повернути плитку за годинниковою, правий — проти.
- Arcade: затиснути кнопку й перетягнути плитку, що падає, вліво-вправо.
- Ніякого «підпалу» вручну: вогонь іде сам, щойно шлях зʼєднано.

## Вікна, меню, HUD
- `main-menu` → `mode-select` (Classic, Arcade, Strategy) → `difficulty-select` (три рівні складності на кожен режим).
- `game-screen`: сітка, сірники зліва, ракети справа з рівнем, `timer-countdown` рядом ліхтариків (Classic, `lantern-timer`), лічильник монет, `score`, `progress-bar` квоти ракет (?), підсвітка зʼєднань: жовтий — від сірника, червоний — до ракети, білий — ніде (`connection-tint`).
- `end-screen`: кінець рівня / гри з рахунком і званням (?).
- `leaderboard` (?); Deluxe — онлайн-гра лише в Classic.

## Фічі поза полем
- `mode-classic` (рівні з квотою), `mode-endless`-подібні Arcade і Strategy; `difficulty-presets` ×3 на режим.
- `rank-tiers` — звання піротехніка за очками (у Wikipedia — «rank based on score»).
- Deluxe: онлайн-гра лише в Classic; китайський дракон-маскот підбадьорює.

## Варіації й родичі
- Rocket Mania Deluxe (2006 (?)) — розширене видання; мобільні Windows Mobile / Palm OS; пізніше Rocket Mania Frenzy для iOS (?).
- Корпус: [Infinity Loop](infinity-loop.md) і [Plumber / Pipes](plumber-pipe-rotation.md) (обертання плиток до звʼязності) · [Pipe Mania](pipe-mania.md) (потік по трубах) · [Bejeweled](../falling-match/bejeweled.md) і [Zoo Keeper](../falling-match/zoo-keeper.md) (зникнення + падіння + поповнення).
- Осі варіацій: **що зникає** — шлях цілком (Rocket Mania) / лінія однакових (match-3) · **джерело тиску** — таймер / падіння плиток / ліміт підпалів · **розгалуження** — лише лінійні / Т і хрест дають мульти-запуск.

## Цікавинки для курсу
- Шлях від лівого до правого краю через порти плиток (BFS від усіх сірників) + підсвітка «звідки / куди дістає» — 🥉.
- Згоряння шляху → гравітація → поповнення згори: каскад як у match-3, але за звʼязністю — 🥉.
- Розгалуження: вогонь по всіх гілках одночасно, кілька ракет за раз і бонус 5+ — 📎.
- Три режими на одному ядрі (таймер / падіння по одній з керуванням / ліміт підпалів) — 📎 за режим.
- Монети → апгрейд ракети 1–10; годинник заморожує таймер; предмет, що зникає за 3 запуски, — 🌱 за кожен.

## Мапа на каталог
- Є: `tile-rotate` · `pipe-connectors` · `cell-click` · `drag-drop-piece` (Arcade) · `gravity-fall` · `explode-area` (бомба) · `item-pickup` · `collect-quota` (квота ракет) · `time-out` · `event-points` · `highlights` (жовтий/червоний/білий) · `mode-select` · `difficulty-levels` · `sequential-levels` · `game-screen` · `end-screen` · `main-menu`.
- **Нема** → пропозиції карток:
  - `+edge-to-edge-path` «Шлях від краю до краю через порти» · game-logic/win · 🥉.
  - `+burn-path-clear` «Зʼєднаний шлях зникає цілком» · entities/interact · 📎.
  - `+refill-from-top` «Поповнення поля згори випадковими плитками» · entities/spawn · 🌱.
  - `+branching-multi-launch` «Розгалуження → кілька цілей одним потоком» · game-logic · 📎.
  - `+multi-launch-bonus` «Бонус за N цілей одним ходом» · game-logic/score · 🌱.
  - `+upgrade-by-coins` «N монет → апгрейд цілі» · game-logic/economy · 🌱.
  - `+timer-freeze-pickup` «Предмет зупиняє таймер» · entities/state · 🌱.
  - `+limited-ignitions` «Обмежений запас запусків» · game-logic/lose · 🌱.
  - `+expiring-pickup` «Предмет зникає за N ходів» · entities/death · 🌱.
  - `+falling-tile-steer` «Падаюча плитка з керуванням» · entities/move · 📎.
  - `+rank-title` «Звання за рахунком» · game-logic/score · 🌱.

## Пропозиції до словників
- `+effect:ignite(path)` — підпалити зʼєднаний ланцюг від джерела; вогонь іде по ньому й знищує (Rocket Mania).
- `+ui:connection-tint` — колір плитки за досяжністю: від джерела / до приймача / ніде.
- `+ui:lantern-timer` — таймер-ряд символів, що гаснуть один за одним.
- `+card:edge-to-edge-path`, `+card:burn-path-clear`, `+card:limited-ignitions` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Rocket Mania](https://en.wikipedia.org/wiki/Rocket_Mania) — сітка ґнотів, сірники й ракети, зникнення й падіння, розгалуження, бомби, самоцвіти, годинники, монети, сірники, режими Classic/Arcade/Strategy, рахунок, Nuclide Games / PopCap 2003.
- [Огляд Rocket Mania Deluxe (oocities)](https://www.oocities.org/tstodden.geo/GameReviews/PC/Rocket_Mania_Deluxe.html) — підсвітка жовтим/червоним/білим, лівий/правий клік, перетягування в Arcade, онлайн лише Classic.
- [ESRB: Rocket Mania Deluxe](https://www.esrb.org/ratings/9612/rocket-mania-deluxe/) — бачив у пошуку.
- YouTube: пошук «Rocket Mania PopCap gameplay».

## Непевне
- (?) Набір типів плиток: Т і хрест — за Wikipedia; пряма й кут — очевидні з геймплею, але в джерелах не названі; чи є глухі кінці — не перевірено.
- (?) Розмір сітки, кількість сірників і ракет, тривалість таймера, очки за ракету — чисел у джерелах нема.
- (?) Classic: рівень закінчується за квотою чи лише коли гаснуть ліхтарики; скільки ракет разом дає монети.
- (?) Рік Deluxe: 2006 за одним джерелом, «Windows 2003» за іншим; Rocket Mania Frenzy (iOS) — лише в результатах пошуку.
- (?) Чи є екран рекордів, довідка, налаштування — у джерелах не описано.
