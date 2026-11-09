---
title: Hearthstone Battlegrounds
slug: hearthstone-battlegrounds
aka: [HSBG, Battlegrounds, Поля битв]
family: tower-lanes
also: []
klass: cursor
axes:
  field: 1d
  time: turn
  opponent: online
  info: partial
  random: runtime
  goal: survive
year: 2019
platforms: [PC, Mac, iOS, Android]
links:
  - {kind: fandom, url: "https://hearthstone.wiki.gg/wiki/Battlegrounds", best: true, note: "wiki.gg: таверна, тири й ціни, золото 3→10, freeze, 7 місць, трійки, порядок атаки, шкода герою, таймери, Kel'Thuzad, Duos"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Hearthstone", note: "розділ Game modes: 8 гравців, автобій, топ-4 = перемога"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=hearthstone+battlegrounds+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [round-currency, shop-catalog, shop-buyback, shop-preview, tile-merge, drag-drop-piece, hp-damage, online-multiplayer, move-timer, chain-reaction, status-effects, mode-select, character-select, leaderboard, end-screen, popup-text, +auto-battle, +shop-reroll, +shop-freeze, +star-up-merge, +shared-unit-pool, +tier-upgrade-discount, +ability-triggers, +attack-order-left-right, +taunt-targeting, +damage-by-survivors, +ghost-opponent, +no-repeat-pairing, +placement-rating, +hero-power, +tribe-pool-rotation, +duo-pass-cards]
proposes: ["+role:unit", "+role:hero", "+trigger:battle_start", "+trigger:faint", "+trigger:bought", "+trigger:sold", "+trigger:card_played", "+effect:reroll", "+effect:sell", "+effect:freeze_slot", "+effect:summon", "+effect:discover", "+effect:upgrade_tier", "+cond:position", "+cond:has_keyword", "+ui:tavern-tier", "+ui:shop-bar", "+ui:player-list", "+ui:phase-timer", "+feature:mode-duos", "+axis:time"]
author: opus
date: 2026-11-09
---

# Hearthstone Battlegrounds — автобатлер на 8: таверна, ряд із 7 міньйонів і порядок «зліва направо»

## Суть
Вісім героїв у лобі; кожен раунд — фаза найму в таверні Боба (купити, продати, оновити, заморозити, підвищити тир) і фаза автоматичного бою з випадковим суперником. Твоя армія — **ряд до 7 міньйонів**, порядок задаєш сам: атакують по черзі зліва направо, і від позиції залежить, хто бʼє першим, кого прикриває Taunt і на кого спрацює ефект сусіда. Програвши бій, герой втрачає здоровʼя; останній живий перемагає, топ-4 вважається виграшем.

## Поле і час
- Поле — 1D-ряд до 7 слотів на сторону; у бою два ряди один навпроти одного, ціль атаки — будь-який ворожий міньйон (випадково), не лише передній.
- Хід = раунд: **Recruit Phase** (таймер 60 с у 1-му раунді, +15 с щораунду, кап 120 с) → **Combat Phase** (без власної тривалості, автоматичний).
- Таймер найму стартує з початком бою: коротший бій → більше часу на наступний найм.
- Суперник раунду — випадковий з живих; при непарній кількості — «привид» Kel'Thuzad з копією дошки останнього вибулого.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой | player (`+role:hero`) | 30 HP (Patchwerk 60), броня за силою героя, hero power | отримує шкоду за програні бої; 0 HP — вибув |
| Hero power | switch | ціна в золоті | активна/пасивна здібність героя у фазі найму; частина спрацьовує перед боєм |
| Таверна Боба | spawner | тир 1–6 (часом 7), 3 слоти +1 на тирах 2, 4, 6 | пропонує міньйонів свого тиру й нижчих зі спільного пулу |
| Міньйон | ally (`+role:unit`) | атака, HP, тир, тип (tribe), ключові слова | стоїть у слоті; у бою атакує в свою чергу; тригерні здібності |
| Золотий міньйон (Triple) | ally | подвоєні стати, часто сильніша здібність | злиття 3 копій; при розіграші дає винагороду Discover |
| Слот ряду | zone | 7 | порядок = порядок атаки |
| Рука | zone | — (?) | куплене спершу в руці; з дошки в руку не повернути |
| Tavern spell | pickup | ціна, тир | заклинання з таверни (баф, золото, ефект) |
| Токен | ally | тир 1 для шкоди | призваний ефектами; займає слот, якщо є місце |
| Золото (Coins) | resource | 3 на старті, +1 щораунду, макс. 10 | не переноситься між раундами |
| Спільний пул | zone | копій на тир: 15/15/13/11/9/7/5 | купив ти — менше шансів у суперника |
| Kel'Thuzad | enemy | 0 HP | копія дошки й тиру щойно вибулого; суперник «зайвого» гравця |
| Типи (tribes) | zone | Beast, Demon, Dragon, Elemental, Mech, Murloc, Naga, Pirate, Quilboar, Undead… | синергії між міньйонами одного типу |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(player)` → ТО `currency(set: min(3 + round − 1, 10))`, `custom: «таверна оновлюється, крім замороженого»`, `custom: «ціна апгрейду таверни −1, якщо тир не мінявся»`.
- КОЛИ `input(buy, minion)` → ЯКЩО `has(gold, 3)` → ТО `currency(-3)`, `give(player, minion)` (у руку); ціна однакова для всіх тирів.
- КОЛИ `input(play, minion, slot)` → ЯКЩО `count(board, <, 7)` → ТО `place(minion, slot)`, `custom: «Battlecry, якщо є»`.
- КОЛИ `input(sell, minion)` → ТО `currency(+1)` (якщо ефект не змінює ціну), `disappear_a`, `custom: «копія повертається у спільний пул»`.
- КОЛИ `input(refresh)` → ЯКЩО `has(gold, 1)` → ТО `currency(-1)`, `custom: «нові пропозиції з пулу»`.
- КОЛИ `input(freeze)` → ЯКЩО `counter(freeze_toggles, <, 5)` → ТО `set_state(shop, frozen)` (безкоштовно; пропозиції переживають раунд).
- КОЛИ `input(upgrade_tavern)` → ЯКЩО `has(gold, cost)` → ТО `currency(-cost)`, `counter(tier, +1)`; базові ціни: тир 2 — 5, 3 — 7, 4 — 8, 5 — 11, 6 — 11.
- КОЛИ `input(drag, minion, slot)` → ТО `swap(a, b)` або `move(a, slot)` — переставити порядок.
- КОЛИ `counter(copies_of_minion, ==, 3)` → ТО `merge(a, b, golden)` (з руки й дошки разом; зачарування зберігаються).
- КОЛИ `input(play, golden)` → ТО `give(player, triple_reward)`; КОЛИ `input(play, triple_reward)` → ТО `choose(3 minions of tier+1)` (з тиру 6 — тир 6).
- КОЛИ `input(hero_power)` → ЯКЩО `has(gold, cost)` → ТО `custom: «ефект героя»`.
- КОЛИ `phase_start(combat)` → ТО `custom: «першим атакує той, у кого більше міньйонів; порівну — випадково»`.
- КОЛИ `custom: «черга атаки сторони»` → ТО `custom: «наступний зліва міньйон б'є випадкову ворожу ціль»`; ЯКЩО `custom: «у ворога є Taunt»` → ТО ціль — випадковий з Taunt.
- КОЛИ `contact(attacker, target)` → ТО `damage(atk)` обом одночасно (атакувальник отримує атаку цілі).
- КОЛИ `hp_zero(minion)` → ТО `disappear_a`, `custom: «Deathrattle, якщо є»`; КОЛИ `custom: «Reborn»` → ТО `respawn(minion, slot)` з 1 HP (?).
- КОЛИ `custom: «ефект призиває міньйона»` → ЯКЩО `count(board, <, 7)` → ТО `spawn_at(token, slot)`, `custom: «новий входить у чергу атаки зліва направо»`; інакше `block`.
- КОЛИ `custom: «Divine Shield»` and `contact(attacker, minion)` → ТО `clear_state(minion, divine_shield)` замість шкоди (?).
- КОЛИ `custom: «Windfury»` → ТО `extra_move` (дві атаки за свою чергу).
- КОЛИ `all_gone(minions, side)` → ЯКЩО `custom: «в іншої сторони хтось вижив»` → ТО `damage(loser_hero, tavern_tier + Σ tiers of survivors)` (токен = тир 1); інакше `draw` (без шкоди).
- КОЛИ `hp_zero(hero)` → ТО `custom: «гравець вибуває, місце = кількість живих + 1»`.
- КОЛИ `count(heroes_alive, ==, 1)` → ТО `win`; місця 1–4 — `custom: «рейтинг росте»`, 5–8 — падає.
- КОЛИ `custom: «підбір суперника»` → ЯКЩО `custom: «живих гравців > 2»` → ТО `custom: «не той самий суперник чи Kel'Thuzad частіше, ніж раз на 3 раунди»`.
- Перемога: останній живий; «виграш» для рейтингу — топ-4 · Поразка: HP героя = 0 · Рахунок: місце 1–8 → MMR (прихований) і Visual Rating.

## Керування і ввід
- Миша/тач: drag міньйона з таверни в руку (купити), з руки на дошку (зіграти), з дошки на Боба (продати), між слотами (переставити).
- Кнопки: Refresh (1 золото), Freeze (перемикач), Upgrade Tavern (ціна на кнопці), hero power; у бою — лише спостереження.
- На старті — вибір з 2 героїв (4 із Season Pass), кожен слот героя можна перекинути раз за токен.

## Вікна, меню, HUD
- `mode-select` — Battlegrounds Solo / Duos у меню Hearthstone.
- `character-select` — 2–4 картки героїв з hero power, кнопка reroll.
- `game-screen` найму: Боб і `+ui:shop-bar` (3–6 пропозицій), `+ui:tavern-tier` і ціна апгрейду, `coins` (x/10), кнопки Refresh/Freeze/Upgrade, рука, ряд з 7 слотів, `+ui:phase-timer`, `+ui:player-list` (8 героїв за HP, тип і тир останнього суперника), `tooltip` міньйона.
- `game-screen` бою: два ряди, `popup-text` шкоди, анімація атак; після бою — шкода герою.
- `end-screen` — місце 1–8 і зміна рейтингу; `leaderboard` — рейтингова таблиця (?).

## Фічі поза полем
- `online-multiplayer` на 8, матчмейкінг за MMR; `+feature:mode-duos` — 4 команди по 2: спільне здоровʼя, передача карт напарнику.
- Ротація контенту: герої (123 станом на сторінку) і типи міньйонів міняються між сезонами (?), сезонні механіки — buddies, квести, anomalies, trinkets (лише згадані на сторінці).
- Season Pass — більше героїв на вибір і безкоштовний reroll.

## Варіації й родичі
- У сімʼї: [super-auto-pets](super-auto-pets.md) (той самий ряд і тригери, але бій передніми й асинхронний), [dota-auto-chess](dota-auto-chess.md) і [teamfight-tactics](teamfight-tactics.md) (2D-дошка, спільний пул, зірки з трьох копій), [inscryption](inscryption.md) (ряд карт навпроти).
- **Осі варіацій**: ціль атаки — передній (SAP) / випадковий з Taunt-пріоритетом (HSBG) / найближчий на дошці (TFT) · економіка — +1 золото за раунд до 10 / фіксовано 10 / відсотки · апгрейд магазину — купується з дешевшанням / росте з ходом · суперник — живий синхронний / записаний / привид вибулого.

## Цікавинки для курсу
- Порядок атаки зліва направо з чергуванням сторін і вставкою призваних у чергу — 📎.
- Шкода герою = тир таверни + сума тирів тих, хто вижив — 🌱.
- Спільний обмежений пул копій (купив ти — менше в інших) — 🥉.
- Апгрейд таверни, що дешевшає на 1 щораунду, поки чекаєш — 🌱 (вибір «зараз чи потім»).
- Трійка → золотий + Discover з наступного тиру — 📎.
- Підбір пар без повторів частіше ніж раз на 3 раунди + привид при непарних — 🥈.

## Мапа на каталог
- Є: `round-currency` ↔ золото 3→10 · `shop-catalog` + `shop-preview` ↔ таверна · `shop-buyback` ↔ продаж за 1 · `tile-merge` ↔ трійка · `drag-drop-piece` · `hp-damage` · `online-multiplayer` · `move-timer` ↔ таймер найму · `chain-reaction` ↔ ланцюги Deathrattle/призову · `status-effects` ↔ Divine Shield, Reborn, Poisonous · `mode-select` · `character-select` ↔ вибір героя · `leaderboard` · `end-screen` · `popup-text`.
- **Нема** → пропозиції карток:
  - `+attack-order-left-right` «Авто-атака по черзі зліва направо з чергуванням сторін» · entities/combat · 📎.
  - `+taunt-targeting` «Випадкова ціль із пріоритетом провокації» · entities/combat · 🌱.
  - `+damage-by-survivors` «Шкода гравцю за силою тих, хто вижив» · game-logic/score · 🌱.
  - `+tier-upgrade-discount` «Апгрейд дешевшає з кожним раундом очікування» · game-logic/economy · 🌱.
  - `+ghost-opponent` «Привид вибулого як суперник при непарних» · game-logic/opponent · 📎.
  - `+no-repeat-pairing` «Пари без повтору N раундів» · game-logic/opponent · 🥉.
  - `+placement-rating` «Рейтинг за місцем 1–N, топ-половина = виграш» · game-logic/score · 📎.
  - `+hero-power` «Здібність персонажа з ціною на хід» · entities/state · 🌱.
  - `+tribe-pool-rotation` «Набір типів міньйонів змінюється між партіями» · game-logic/setup · 🌱.
  - `+duo-pass-cards` «Пара гравців зі спільним HP і передачею карт» · game-logic/opponent · 🥈.

## Пропозиції до словників
- `+role:unit` · `+role:hero` — аватар-«життя» гравця поза полем бою.
- `+trigger:battle_start` · `+trigger:faint` (Deathrattle) · `+trigger:bought` · `+trigger:sold` · `+trigger:card_played` (Battlecry).
- `+effect:reroll` · `+effect:sell` · `+effect:freeze_slot` · `+effect:summon` · `+effect:discover` (вибір 1 з 3 випадкових за фільтром) · `+effect:upgrade_tier`.
- `+cond:position` (місце в ряду) · `+cond:has_keyword(a, k)` (Taunt, Divine Shield).
- `+ui:tavern-tier` · `+ui:shop-bar` · `+ui:player-list` · `+ui:phase-timer`.
- `+feature:mode-duos`.
- `+axis:time` — значення `phased` (найм → бій).

## Джерела
- ⭐ [Hearthstone Wiki: Battlegrounds](https://hearthstone.wiki.gg/wiki/Battlegrounds) — 8 гравців, 2/4 героїв і reroll, 30 HP, тири 1–6(7), пропозиції 3 (+1 на 2/4/6), пул копій за тирами, 3 золота +1 до 10, ціни 3/1/1, апгрейд 5/7/8/11/11 і −1 за раунд, freeze 5 разів, 7 місць, трійки й Discover, таймер 60 +15 до 120, порядок атаки, Taunt, шкода = тир + тири тих, хто вижив, Kel'Thuzad, пари раз на 3 раунди, топ-4, Duos.
- [Wikipedia: Hearthstone](https://en.wikipedia.org/wiki/Hearthstone) — режим з листопада 2019, 8 гравців, автобій, топ-4 = виграш.
- [YouTube: пошук](https://www.youtube.com/results?search_query=hearthstone+battlegrounds+gameplay) — геймплей.

## Непевне
- (?) Ліміт руки (10?) — на сторінці не вказано.
- (?) Divine Shield (поглинає першу шкоду), Reborn (повертається з 1 HP), Poisonous/Venomous — сторінка лише перелічує ключові слова, пояснення з памʼяті.
- (?) Чи є кап шкоди герою (на сторінці — лише «20+ у пізній грі»); винятки з атакувальником (Cleave, атака без отримання шкоди) не перевірені.
- (?) Скільки типів міньйонів виключається в партії — сторінка не каже.
- (?) Порядок спрацювання «на початку бою» між гравцями.
