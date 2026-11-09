---
title: Titanium Court
slug: titanium-court
aka: []
family: falling-match
also: [tower-lanes, roguelike]
klass: hybrid
axes:
  field: square
  time: turn
  opponent: ai
  info: full
  random: both
  goal: state
year: 2026
platforms: [PC, macOS, Switch, Switch 2, PS5, iOS, Android]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Titanium_Court", best: true, note: "жанрова суміш, фази High Tide / Low Tide, солдати й фермери, гори біля Двору, премія IGF 2026"}
  - {kind: other, url: "https://aftermath.site/titanium-court-demo/", note: "огляд демо: тайли вода/пагорби/поля, ресурси їжа/камінь/дерево, будівлі на сітці, катапульти, роглайк-мапа"}
  - {kind: steam, url: "https://store.steampowered.com/app/2364580/Titanium_Court/", note: "Steam: опис, теги (Match 3, Tower Defense, Roguelite, Auto Battler), демо"}
  - {kind: official, url: "https://www.fellowtraveller.games/titanium-court", note: "видавець Fellow Traveller: бої-пазли, війська не керуються"}
  - {kind: other, url: "https://www.pcgamer.com/games/roguelike/titanium-court-review/", note: "огляд PC Gamer (74/100) — бачено у Wikipedia, текст не відкрився"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=titanium+court+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [line-match-clear, gravity-fall, swap-on-contact, round-currency, move-auto, enemy-reached-base, hp-damage, tower-placement, impassable-cells, floor-types, map-window, world-map, run-relics, in-round-upgrades, shop-window, dungeon-generation, permadeath, save-autosave, +match-3-swap, +two-phase-turn, +match-yields-resource, +extra-turn-on-big-match, +terrain-as-defense, +preserve-tile-to-use, +auto-battle-units, +harvest-leftover-tiles, +card-draft-upgrades]
proposes: ["+trigger:phase_start(high_tide|low_tide)", "+effect:deploy(unit, from)", "+effect:harvest(tile)", "+cond:unmatched(tile)", "+role:court", "+ui:tide-indicator", "+ui:battle-tower", "+feature:card-draft", "+axis:phases"]
author: opus
date: 2026-11-09
---

# Titanium Court — match-3 як будівник рельєфу: збіги дають ресурси й перекроюють поле, по якому потім воюють автономні війська

## Суть
Бій іде на клітинному полі з тайлів рельєфу (вода, пагорби, поля) і двох фортець — твого Двору й ворожих. Хід ділиться на дві фази: **High Tide** — ти складаєш тайли рельєфу в лінії по 3, отримуючи ресурси й змінюючи ландшафт; **Low Tide** — витрачаєш ресурси, висаджуючи солдатів і фермерів, які б'ються самі. Тобто match-3 тут — не спосіб набрати очки, а інструмент і економіки, і tower defense: що лишилось на полі після збігів — це перешкоди для ворогів, урожай для фермерів і будівлі для вжитку. Між боями — роглайк-мапа з драфтом карток-апгрейдів і сюрреалістичний текстовий наратив. Клас `hybrid`: `cursor` (match-3) + автобатлер/TD.

## Поле і час
- Квадратна сітка тайлів; Двір гравця — одна клітина-фортеця, вороги намагаються до неї дійти.
- Покроково по фазах: High Tide (матчинг, кілька ходів; серія збігів дає більше ходів у фазі) → Low Tide (розстановка і автобій) → знову High Tide.
- Бій у Low Tide спостерігається, не керується; прогрес битви показано «вежами Дженги».
- Поза боями — роглайк-мапа: твій Двір рухається нею до виходу.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Двір (Court) гравця | static | HP (?) | клітина-фортеця; ворог, що дійшов, шкодить (?) |
| Ворожий Двір / твердиня | enemy | HP (?) | ціль твоїх солдатів; породжує ворогів (?) |
| Тайл «вода» | terrain | ресурс (?) | збіг 3 → ресурс; лишений — перешкода для ворожих військ |
| Тайл «пагорби» / гори | terrain | камінь | збіг → камінь; лишений біля Двору — уповільнює ворогів, захищає від катапульт |
| Тайл «поля» | terrain | їжа | збіг → їжа; лишений — урожай для фермерів |
| Ліс (?) | terrain | дерево | збіг → дерево |
| Будівля на сітці | static | тип | працює в Low Tide, лише якщо не була зматчена в High Tide |
| Госпіталь | static | — | лікує (війська/Двір?) |
| Крамниця | static | — | продає предмети |
| Дзеркало | static | — | поряд із Двором — війська «два за ціною одного» |
| Солдат | ally | ціна | атакує ворожі твердині або захищає Двір; рухається сам |
| Фермер | ally | ціна | збирає ресурси з лишених на полі тайлів під час бою |
| Ворожі війська | enemy | тип | ідуть до Двору; рельєф їх уповільнює/блокує |
| Катапульта | enemy | дальність (?) | б'є здалеку; контра — пагорби навколо Двору |
| Літаючий ворог | enemy | — | ігнорує рельєф (?) |
| Карта-апгрейд | pickup | ефект | драфт між боями; змінює правила до кінця забігу |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `phase_start(high_tide)` → ТО `custom: «гравець отримує ходи матчингу»`.
- КОЛИ `input(swap(a, b))` → ЯКЩО `adjacent(a, b)` → ТО `swap(a, b)`.
- КОЛИ `pattern(match(terrain, 3))` → ТО `clear(line)`, `counter(resource[terrain], +n)` (їжа / камінь / дерево).
- КОЛИ `pattern(match(...))` → ЯКЩО `chain(2+)` → ТО `extra_move` — серія збігів дає ще ходи у фазі.
- КОЛИ `after(clear)` → ТО `fall(tiles_above)` (?), `spawn_at(random_terrain, top)` (?).
- КОЛИ `pattern(match(building))` → ТО `clear`; `custom: «будівля втрачена для Low Tide»`.
- КОЛИ `phase_start(low_tide)` → ТО `custom: «deploy — гравець витрачає ресурси на солдатів або фермерів»`: `input(place(unit))` → ЯКЩО `has(resource, cost)` → ТО `take(resource)`, `place(unit)`.
- КОЛИ `custom: «бій Low Tide»` → ТО `move(units, auto)` — солдати йдуть на ворожі твердині або назустріч ворогам; керування нема.
- КОЛИ `enter(enemy, hills|mountain)` → ТО `speed(enemy, −)` — рельєф уповільнює.
- КОЛИ `contact(soldier, enemy)` → ТО `damage(n)` обом (?); результат видно на «вежах».
- КОЛИ `enter(farmer, resource_tile)` → ТО `custom: «harvest — ресурс без матчингу»`; ЯКЩО `count(resource_tiles, ==, 0)` → ТО фермер марний.
- КОЛИ `custom: «солдат біля будівлі»` → ЯКЩО `occupied(cell, hospital)` → ТО `heal(unit, n)` (?); `shop` → `window(shop-window)`.
- КОЛИ `place(unit)` → ЯКЩО `custom: «дзеркало поряд із Двором»` → ТО `clone(unit)`.
- КОЛИ `in_range(catapult, court, n)` → ЯКЩО `not custom: «Двір оточено пагорбами»` → ТО `damage(court, n)`.
- КОЛИ `reach(enemy, court)` → ТО `damage(court, n)` (?); КОЛИ `hp_zero(court)` → ТО `lose` — кінець забігу (?).
- КОЛИ `hp_zero(enemy_court)` → ТО `win` бою (?), `choose(card_draft)`.
- КОЛИ `custom: «вузол мапи пройдено»` → ТО `move(court, next_node)`; КОЛИ `reach(court, exit)` → ТО `next_level` (?).
- Перемога: знищити ворожий Двір/твердині (?) і дійти мапою до виходу. Поразка: впав власний Двір (?). Рахунок: нема — прогрес забігу.

## Керування і ввід
- Миша / дотик: свап сусідніх тайлів у High Tide; вибір юніта й клітини розстановки у Low Tide; натиск «бій» — і спостереження.
- Поза боями — point-and-click по сценах (наратив, предмети, «інтерактивний душ»), вибір карток із драфту, вибір вузла мапи.

## Вікна, меню, HUD
- `game-screen` бою: сітка тайлів, Двори, лічильники ресурсів (їжа, камінь, дерево), `custom: «tide-indicator»` (поточна фаза), лічильник ходів фази, `custom: «battle-tower»` — вежі-стоси, що показують хід битви.
- `map-window` — роглайк-мапа (за оглядом — «заплутана, і гра це визнає»).
- `shop-window` (будівля-крамниця), `custom: «card-draft»` — вибір карти-апгрейда після бою (`upgrade-window`).
- `dialogue-window` — текстові сцени Двору (багато читання), `main-menu`, `settings-window`, `end-screen` забігу.

## Фічі поза полем
- Роглайт: `run-relics`/картки-апгрейди драфтом, нова мапа кожен забіг (?), `meta-progression` — секрети, що назавжди змінюють персонажа (?).
- `achievements` (Steam), `cloud-save`.
- Наратив: point-and-click квест пошуку зниклих речей; «кар'єри» (Warlord, Arsonist, Celebrity, Insurance Fraudster) — розблоковуються грою (?).

## Варіації й родичі
- Родичі в корпусі: [puzzle-quest](puzzle-quest.md) і [gems-of-war](gems-of-war.md) (match-3 → бій), [10000000](10000000.md) (match-3 рухає героя), [dungeon-raid](dungeon-raid.md) (збіги як роглайк-ресурс), [triple-town](triple-town.md) (поле як будівництво), [clash-of-heroes](clash-of-heroes.md). З tower-lanes — лабіринтування рельєфом як у Fieldrunners; автобій — як auto chess.
- **Осі варіацій**: що дає збіг (очки / ману / ресурс + зміну рельєфу) · що робить лишене на полі (нічого / перешкода / урожай / будівля) · хто воює (гравець / автономні юніти) · фази ходу (одна / дві — High/Low Tide).

## Цікавинки для курсу
- Двофазний хід: match-3 фаза → фаза розстановки → автобій — 🥉 (стан-машина фаз, спільне поле).
- Лишені тайли як рельєф для шляху ворогів (pathfinding по полю, яке перекроїв match-3) — 🥈.
- Будівля працює, лише якщо її НЕ зматчили — збіг як вибір «знищити/зберегти» — 🌱.
- Фермер збирає з того, що ти лишив, — компроміс «ресурс зараз (матч) чи потім (урожай)» — 📎.
- Автобій юнітів з простою поведінкою «йти до цілі, бити сусіда» — 🥉.
- Серія збігів дає додаткові ходи фази — 🌱.

## Мапа на каталог
- Є: `line-match-clear` · `gravity-fall` (?) · `swap-on-contact` (найближча до свапу) · `round-currency` (їжа/камінь/дерево) · `move-auto` (юніти) · `enemy-reached-base` · `hp-damage` · `tower-placement` (розстановка юнітів; найближча) · `impassable-cells` · `floor-types` (рельєф) · `map-window` · `world-map` · `run-relics` · `in-round-upgrades` · `shop-window` · `dungeon-generation` (роглайк-мапа) · `permadeath` (забіг) · `save-autosave`.
- **Нема** → пропозиції карток:
  - `+match-3-swap` (спільна з Bejeweled) · entities/interact · 📎.
  - `+two-phase-turn` «Хід із двох фаз з різним вводом» · game-logic/opponent · 🥉.
  - `+match-yields-resource` «Збіг типу → ресурс цього типу» · game-logic/economy · 🌱.
  - `+extra-turn-on-big-match` (спільна з PQ; тут за серію) · game-logic/opponent · 🌱.
  - `+terrain-as-defense` «Тайли поля — рельєф для шляху ворогів» · entities/move · 🥈.
  - `+preserve-tile-to-use` «Плитка працює, лише якщо її не зматчили» · entities/interact · 🌱.
  - `+auto-battle-units` «Юніти воюють самі, гравець лише ставить» · game-logic/opponent · 🥉.
  - `+harvest-leftover-tiles` «Юніт збирає ресурс з плиток на полі» · game-logic/economy · 📎.
  - `+card-draft-upgrades` «Вибір 1 з N карток після бою» · game-logic/economy · 📎.

## Пропозиції до словників
- `+trigger:phase_start(high_tide|low_tide)` — підтверджую `phase_start` з аргументом фази ходу (не тіку).
- `+effect:deploy(unit, from)` — висадити юніт за ресурси з Двору (ширше за `place`: з ціною й точкою виходу).
- `+effect:harvest(tile)` — юніт забирає ресурс клітини.
- `+cond:unmatched(tile)` — плитка пережила фазу матчингу (будівлі).
- `+role:court` — фортеця-база сторони (ціль і точка висадки).
- `+ui:tide-indicator` — поточна фаза ходу; `+ui:battle-tower` — стос-індикатор переваги в бою.
- `+feature:card-draft` — вибір карт-апгрейдів між боями.
- `+axis:phases` — `single` · `two-phase` (матч → бій).

## Джерела
- ⭐ [Wikipedia: Titanium Court](https://en.wikipedia.org/wiki/Titanium_Court) — жанри, High Tide/Low Tide, солдати й фермери, гори біля Двору, рецензії, IGF 2026 (Seumas McNally Grand Prize, Excellence in Design).
- [Aftermath: демо](https://aftermath.site/titanium-court-demo/) — тайли вода/пагорби/поля, ресурси, ходи за серію збігів, будівлі (госпіталь, крамниця, дзеркало), катапульти, літаючі, «вежі Дженги», роглайк-мапа.
- [Steam](https://store.steampowered.com/app/2364580/Titanium_Court/) — «match-3 tower-defense roguelike», драфт карт («не зовсім декбілдер»), теги, дата 23.04.2026.
- [Fellow Traveller](https://www.fellowtraveller.games/titanium-court) — війська не керуються, рельєф «падає на твою користь», платформи.

## Непевне
- (?) Чи тайли падають/поповнюються після збігу, чи поле лише перекроюється — у Steam «terrain so it falls in your favor», механіку не описано.
- (?) Умови перемоги/поразки, HP Дворів, ціни юнітів — джерела не дають.
- (?) Який тайл дає дерево (ліс?) і що дає вода; чи є інші типи тайлів.
- (?) Як саме рухаються й б'ються юніти; що робить літаючий ворог.
- (?) «Дуель Дворів» у черзі — у джерелах лише «battles against rival Courts».
- Огляди PC Gamer, The Verge, Rock Paper Shotgun не відкрились (скорочено/блок); WebSearch на гру не вдався — ліміт вичерпано.
