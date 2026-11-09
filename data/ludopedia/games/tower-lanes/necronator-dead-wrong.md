---
title: "Necronator: Dead Wrong"
slug: necronator-dead-wrong
aka: [Necronator]
family: tower-lanes
also: [roguelike]
klass: cursor
axes:
  field: graph
  time: realtime
  opponent: ai
  info: partial
  random: both
  goal: state
year: 2020
platforms: [PC]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1144970/Necronator_Dead_Wrong/", best: true, note: "офіційний опис: декбілдер + roguelite micro-RTS, нежить і закляття картами, розгортання по смугах на замки, підкріплення ворога, 200+ карт, 20+ реліквій, командири"}
  - {kind: other, url: "https://worthplaying.com/article/2020/9/17/reviews/121866-pc-review-necronator-dead-wrong/", note: "огляд: дороговкази перемикають маршрут, мана відновлюється, захоплені твердині прискорюють ману, типи карт, перебір руки, вузли мапи, HP між боями"}
  - {kind: other, url: "https://digitalnewsasia.com/personal-tech/play-sea-necronator-dead-wrong-gets-fun-right", note: "огляд: смуги, міста-оборонці, захоплення й «привиднення» міст, мана росте з містами, Soulspawn Crystal, перемога — знищити або протриматись"}
  - {kind: other, url: "https://entertainium.co/2020/08/25/necronator-dead-wrong-review/", note: "огляд: юніти/закляття/споруди, HP замку, табори (лікування або апгрейд), крамниці за фіолетові монети, Necronomnomicon"}
  - {kind: other, url: "https://indiecator.org/2021/06/02/indietail-necronator-dead-wrong/", note: "огляд: портал генерує ману, вежі ворога, апгрейди з двома гілками, перебір за ману з перезарядкою, три командири, ворог теж набирає реліквії, Ascension, Endless"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Necronator+Dead+Wrong+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [move-auto, spawn-schedule, spawn-points, enemy-reached-base, hp-damage, melee-vs-ranged, round-currency, shop-catalog, shop-between-levels, run-relics, world-map, map-window, character-select, codex-window, save-multi-slot, achievements-window, difficulty-levels, +reverse-td, +deck-draw, +deck-builder, +junction-toggle, +capture-income, +paid-redraw, +mana-regen-realtime, +card-upgrade-branch, +card-remove, +base-hp-carryover, +enemy-relics, +run-meta-carry, +ascension-levels, +summon-creature, +boss-fight]
proposes: ["+trigger:card_played", "+effect:draw_card", "+effect:discard", "+effect:redraw_hand", "+role:card", "+role:base", "+role:tower", "+role:waypoint", "+ui:mana-bar", "+ui:redraw-button", "+window:choice-window", "+window:deck-builder", "+window:run-setup", "+window:camp-window", "+feature:run-map", "+card:paid-redraw", "+card:capture-income", "+axis:session"]
author: opus
date: 2026-11-09
---

# Necronator: Dead Wrong — реверс-TD-декбілдер: карти нежиті спавнять юнітів, що самі йдуть дорогами на замки живих

## Суть
Гравець — нежить-командир: у реальному часі він грає карти з руки за ману, і кожна карта-юніт породжує загін біля його порталу, який **сам марширує дорогою** до ворожих міст, веж і замку. Живі весь час шлють свої загони назустріч, тож бій вирішується тим, які юніти, на яку дорогу (дороговкази на розвилках перемикаються кліком) і коли кинути, плюс закляття-бафи. Між боями — карта забігу в дусі Slay the Spire: нові карти, апгрейди з двома гілками, реліквії, табори, крамниці, бос.

## Поле і час
- Поле — ізометрична мапа з **мережею доріг** (`field: graph`): від порталу гравця до ворожого замку (Soulspawn Crystal), з розвилками й дороговказами; на дорогах стоять ворожі міста й вежі.
- Ворог випускає загони випадковими дорогами; міста обороняють дороги, на яких стоять.
- Real-time: мана відновлюється з часом (спершу повільно), бій триває кілька хвилин; пауза й швидкість — не перевірено.
- Забіг: гілляста мапа вузлів, ділянки закінчуються босом; HP порталу/кристала переноситься між боями.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Портал / база гравця | static (`+role:base`) | HP (переноситься між боями) | генерує ману; звідси виходять юніти; HP 0 — кінець забігу |
| Ворожий замок (Soulspawn Crystal) | static (`+role:base`) | HP | ціль бою; знищений — перемога |
| Ворожа вежа | static (`+role:tower`) | HP, атака | бʼє юнітів поруч; знищена — мана тече швидше |
| Ворожа твердиня / місто | spawner | HP | обороняє дорогу, випускає загони; захоплене — служить гравцю |
| Дорога | terrain | граф | юніти йдуть нею самі |
| Дороговказ | switch (`+role:waypoint`) | напрям | на розвилці направляє юнітів; клік — перемкнути |
| Юніт нежиті (скелет, скелет-лучник, орк, троль…) | ally | HP, атака, швидкість, ближній/дальній | марширує дорогою, бʼє все вороже на шляху |
| Ворожий загін живих | enemy | HP, атака | іде дорогами до порталу гравця |
| Карта-юніт | object (`+role:card`) | ціна мани | породжує загін біля порталу |
| Карта-закляття | object (`+role:card`) | ціна | шкода по ворогах або баф/захист своїх |
| Карта-утиліта | object (`+role:card`) | ціна | пасивне посилення руки чи юнітів |
| Споруда / турель (Mirabella) | ally | — | стоїть на мапі, бʼє чи випускає своїх юнітів |
| Мана | resource | швидкість відновлення | платить за карти й перебір руки |
| Реліквія | pickup | пасив | бонус гравцю; ворог теж отримує реліквії глибше в забігу |
| Фіолетові монети | resource | — | валюта крамниць |
| Командир (Number 7, Mirabella, Luavira Heartwing) | — | стартова колода, пул карт | визначає стиль: повна рука щоразу / закляття й споруди / жертва HP порталу |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `timer(regen)` → ТО `counter(mana, +1)`; ЯКЩО `count(captured_towns, >, 0)` → ТО регенерація швидша.
- КОЛИ `input(play, unit_card)` → ЯКЩО `counter(mana, >=, cost)` → ТО `spawn_at(squad, own_portal)`, `counter(mana, -cost)`, `custom: «карта йде у скид»`.
- КОЛИ `spawned(unit)` → ТО `custom: «марширує дорогою сам»`: `move(unit, road)` щотік.
- КОЛИ `enter(unit, signpost)` → ТО `move(unit, signpost_dir)`; КОЛИ `input(click, signpost)` → ТО `rotate(signpost)` — інша гілка.
- КОЛИ `in_range(unit, enemy, range)` → ТО `damage(enemy, atk)`; ближні зупиняються й бʼються, дальні стріляють.
- КОЛИ `timer(enemy_spawn)` → ТО `spawn_at(enemy_squad, enemy_castle | town)` на випадкову дорогу.
- КОЛИ `hp_zero(enemy_town)` → ТО `set_side(town, player)` — місто «привиднене»: б'ється за гравця, мана тече швидше.
- КОЛИ `destroyed(enemy_tower)` → ТО `custom: «+швидкість мани»`.
- КОЛИ `reach(enemy, own_portal)` → ТО `damage(portal, atk)`; КОЛИ `hp_zero(portal)` → ТО `lose`, `custom: «забіг і реліквії втрачено»`.
- КОЛИ `hp_zero(enemy_castle)` → ТО `win`, `choose(card_reward)`, `currency(+coins)`.
- КОЛИ `custom: «час бою вичерпано»` → ЯКЩО `mode(survive)` → ТО `win`; у боях з босом — ЯКЩО `died(boss)` → ТО `win`.
- КОЛИ `input(redraw)` → ЯКЩО `counter(mana, >=, cost)` and `not state(redraw, cooldown)` → ТО `custom: «скинути руку й набрати нову»`, `set_state(redraw, cooldown)`.
- КОЛИ `custom: «рука вичерпана»` → ТО `custom: «набрати нову руку»`; Number 7 — завжди до повної руки, Mirabella — рука сама не поновлюється.
- КОЛИ `input(cast, spell, target)` → ТО `damage(area, n)` або `set_state(units, buff)` або `heal(units, n)`.
- КОЛИ `input(play, structure_card, cell)` → ТО `place(player, turret)` — турель чи «будинок», що випускає юнітів.
- КОЛИ `timer(n)` → ЯКЩО `custom: «юніт Mirabella простояв на полі досить довго»` → ТО `transform(unit, stronger)`.
- КОЛИ `input(sacrifice)` → ЯКЩО `custom: «командир Luavira»` → ТО `damage(portal, n)`, `set_state(units, buff)` або `damage(enemies, n)`; також `custom: «краде ману ворога на свої виклики»`.
- КОЛИ `enter(player, camp)` → ТО `choose(лікувати портал | апгрейд карти | видалити карту)`.
- КОЛИ `input(upgrade, card)` → ЯКЩО `not state(card, upgraded)` → ТО `choose(2 випадкові спеціалізації)`, `set_state(card, upgraded)`.
- КОЛИ `enter(player, shop)` → ЯКЩО `counter(coins, >=, price)` → ТО `give(deck, card)` або `custom: «видалити карту»`.
- КОЛИ `custom: «перемога над елітою»` → ТО `choose(relic | skip)`.
- КОЛИ `custom: «нова ділянка забігу»` → ТО `custom: «ворог отримує реліквії»`.
- Перемога: знищити замок / протриматись / вбити боса; забіг — пройти всіх босів · Поразка: HP порталу 0 · Рахунок: —.

## Керування і ввід
- Миша: клік/перетяг карти з руки — виклик загону біля порталу або закляття в точку мапи; клік по дороговказу — змінити маршрут.
- Кнопка перебору руки (за ману, з перезарядкою).
- На карті забігу — клік по вузлу маршруту; у таборі/крамниці — вибір карти.

## Вікна, меню, HUD
- `main-menu` → `character-select` (командир і стартова колода) → `+window:run-setup` (Ascension, Endless — обираються до старту) (?); `save-slots` — три слоти.
- `map-window` — гілляста карта забігу: бій, еліта, крамниця, подія, табір, бос.
- `game-screen`: ізометрична мапа, рука карт, `+ui:mana-bar`, `+ui:redraw-button` з перезарядкою, `hp-bar` порталу і ворожого замку, дороговкази.
- `+window:choice-window` — нагорода після бою (карта, реліквія); `shop-window`; `+window:camp-window` — лікування / апгрейд / видалення; `dialogue-window` — події (тексти Chandler Groover).
- `codex-window` — «Necronomnomicon» з відкритим вмістом; `settings-window` (телеметрія вимикається тут); `end-screen`.

## Фічі поза полем
- `meta-progression`: рівень командира відкриває карти, реліквії, юнітів і колоди (без бонусів до статів).
- `difficulty-presets` через Ascension; `mode-endless` (обирається до забігу).
- `save-slots` ×3, `achievements`, Steam Workshop і `level-editor` (згадано в огляді) (?).

## Варіації й родичі
- Родичі в корпусі: [the-battle-cats](the-battle-cats.md) і [age-of-war-stick-war](age-of-war-stick-war.md) (юніти самі йдуть смугою на базу ворога), [clash-royale](clash-royale.md) (карти-юніти за еліксир у реальному часі, вежі), [monster-train](monster-train.md) (декбілдер-забіг з призовом захисників), [ratropolis](ratropolis.md) (декбілдер + оборона в реальному часі).
- Поза корпусом: Slay the Spire (каркас забігу), Plants vs. Zombies навиворіт — гравець атакує.
- **Осі варіацій**: напрям — оборона / наступ (реверс-TD) · смуги — фіксовані / граф з дороговказами · ресурс — за хід / тече в реальному часі й прискорюється захопленням · рука — авто-поновлення / перебір за ману.

## Цікавинки для курсу
- Граф доріг з дороговказами-перемикачами: юніт іде сам, гравець змінює лише стрілку на розвилці — 📎.
- Захоплення точки змінює власника і прискорює дохід мани — 🌱.
- Карти в реальному часі: мана тече, рука, перебір за ману з перезарядкою — 🥉.
- Апгрейд карти з вибором однієї з двох випадкових гілок, лише раз — 📎.
- HP бази, що переноситься між боями забігу, і табір «лікувати або покращити» — 🌱.
- Ворог теж збирає реліквії з глибиною забігу — 🌱.

## Мапа на каталог
- Є: `move-auto` ↔ марш дорогою · `spawn-schedule`, `spawn-points` ↔ підкріплення ворога · `enemy-reached-base` ↔ ворог у порталі · `hp-damage` · `melee-vs-ranged` · `round-currency` ↔ мана · `shop-catalog`, `shop-between-levels` · `run-relics` · `world-map`, `map-window` ↔ карта забігу · `character-select` · `codex-window` ↔ Necronomnomicon · `save-multi-slot` · `achievements-window` · `difficulty-levels` ↔ Ascension.
- **Нема** → пропозиції карток:
  - `+reverse-td`, `+deck-draw`, `+deck-builder`, `+junction-toggle`, `+capture-income`, `+run-meta-carry`, `+summon-creature`, `+boss-fight` — уже в корпусі.
  - `+paid-redraw` «Перебір руки за ресурс з перезарядкою» · game-logic/economy · 🌱.
  - `+mana-regen-realtime` «Ресурс тече в реальному часі, швидкість росте від захоплень» · game-logic/economy · 📎.
  - `+card-upgrade-branch` «Апгрейд карти — вибір однієї з двох гілок» · game-logic/economy · 📎.
  - `+card-remove` «Видалити карту з колоди» · game-logic/economy · 🌱.
  - `+base-hp-carryover` «HP бази переноситься між боями забігу» · game-logic/lose · 🌱.
  - `+enemy-relics` «Ворог отримує пасиви з глибиною забігу» · game-logic/difficulty · 🌱.
  - `+ascension-levels` «Рівні складності, що відкриваються перемогами» · game-logic/difficulty · 🌱.

## Пропозиції до словників
- `+trigger:card_played` — повтор (зіграно карту).
- `+effect:draw_card` — повтор; `+effect:discard` — повтор; `+effect:redraw_hand` — скинути руку й набрати нову.
- `+role:card` · `+role:base` · `+role:tower` · `+role:waypoint` — повтори (дороговказ як точка маршруту).
- `+ui:mana-bar` — шкала ресурсу, що наповнюється в реальному часі; `+ui:redraw-button` — кнопка перебору з перезарядкою.
- `+window:choice-window`, `+window:deck-builder` — повтори; `+window:run-setup` — вибір складності/режиму перед забігом; `+window:camp-window` — табір з вибором дії.
- `+feature:run-map` — повтор.
- `+card:paid-redraw`, `+card:capture-income`; `+axis:session` — `run`.

## Джерела
- ⭐ [Steam: Necronator: Dead Wrong](https://store.steampowered.com/app/1144970/Necronator_Dead_Wrong/) — декбілдер + roguelite micro-RTS, смуги й замки, підкріплення ворога, 200+ карт, 20+ реліквій, командири; Toge Productions / Modern Wolf, ранній доступ 13.02.2020, реліз 30.07.2020.
- [WorthPlaying: огляд](https://worthplaying.com/article/2020/9/17/reviews/121866-pc-review-necronator-dead-wrong/) — автоматичний рух, дороговкази, знищити базу / вижити / вбити боса, мана й твердині, типи карт, перебір, командири, вузли мапи, HP між боями.
- [Digital News Asia: огляд](https://digitalnewsasia.com/personal-tech/play-sea-necronator-dead-wrong-gets-fun-right) — смуги, міста-оборонці, захоплення й «привиднення», Soulspawn Crystal, мана росте з містами, нова рука, інни лікують кристал.
- [Entertainium: огляд](https://entertainium.co/2020/08/25/necronator-dead-wrong-review/) — замок з HP, споруди, табори, крамниці, апгрейд з двома шляхами, Necronomnomicon.
- [Indiecator: огляд](https://indiecator.org/2021/06/02/indietail-necronator-dead-wrong/) — портал генерує ману, вежі ворога, перебір за ману з перезарядкою, три командири, ворожі реліквії, Ascension, Endless, три слоти.
- YouTube: пошук «Necronator Dead Wrong gameplay».

## Непевне
- (?) Розмір руки, ліміт мани, точна швидкість регенерації — джерела не дають чисел.
- (?) Пауза й прискорення в бою — не згадано.
- (?) Чи дороговказ має два чи більше станів; чи перемикає він і ворожий потік.
- (?) Чи знищена вежа і захоплене місто — одне й те саме (у різних оглядах «towers», «strongholds», «towns»).
- (?) Редактор рівнів — згадка в одному огляді; Steam показує лише Workshop.
- (?) Вікно налаштування забігу (Ascension/Endless) — з опису «обирається перед забігом».
