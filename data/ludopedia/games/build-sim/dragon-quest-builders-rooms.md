---
title: Dragon Quest Builders (rooms)
slug: dragon-quest-builders-rooms
aka: [DQB, DQB2, ドラゴンクエストビルダーズ, Dragon Quest Builders 2]
family: build-sim
also: []
klass: avatar
axes:
  field: 3d
  time: realtime
  opponent: none
  info: full
  random: setup
  goal: state
year: 2016
platforms: [PS3, PS4, Vita, Switch, iOS, Android, PC]
links:
  - {kind: fandom, url: "https://dragon-quest.org/wiki/Room_Recipes_(Dragon_Quest_Builders)", best: true, note: "Dragon Quest Wiki: усі 82 рецепти кімнат DQB — предмети, очки, ефекти; загальні вимоги (стіни 2 блоки, двері, світло)"}
  - {kind: fandom, url: "https://dragon-quest.org/wiki/List_of_room_recipes_in_Dragon_Quest_Builders_2", note: "DQB2: кімната 4–150 клітин, кімната / площа / поле, сусідні кімнати → готель, ресторан"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Dragon_Quest_Builders", note: "блоки, кімнати додають до рівня бази, день/ніч, голод, дати й платформи"}
  - {kind: fandom, url: "https://dragon-quest.org/wiki/Dragon_Quest_Builders", note: "рівень бази не падає, нічні монстри, набіги з босом, 4 розділи, Terra Incognita"}
  - {kind: fandom, url: "https://dragon-quest.org/wiki/Banner_of_Hope", note: "прапор робить довкола базу, точка збереження"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Dragon+Quest+Builders+room+recipes", note: "пошук; рецепти кімнат"}
stage: v1
coverage: 60
mechanics: [destructible-blocks, cursor-place, coverage-area, hp-damage, hunger-clock, inventory, enemy-waves, sequential-levels, save-game, connectivity-check, +place-wall-floor, +sector-flood-fill, +room-requirements, +room-recipe-catalog, +room-grading, +adjacent-room-upgrade, +base-level-points, +resident-auto-craft, +day-night-cycle, +ratchet-level, +room-effect-no-stack]
proposes: ["+cond:enclosed", "+cond:wall_height", "+trigger:room_changed", "+effect:set_room_type", "+role:resident", "+window:room-recipe-book", "+window:base-level", "+ui:room-found-banner", "+feature:free-build", "+window:crafting-window", "+card:room-recipe-catalog", "+card:adjacent-room-upgrade", "+card:base-level-points"]
author: opus
date: 2026-11-09
---

# Dragon Quest Builders (кімнати) — кімната = замкнений периметр стін ≥ 2 блоки + двері + світло, а набір меблів усередині обирає один з 82 типів

## Суть
Блоковий «Minecraft з сюжетом»: Будівник ставить і ламає блоки, відроджує місто довкола Прапора надії, жителі приходять, працюють і захищають базу від нічних монстрів і набігів. Тут описано лише **шар кімнат-рецептів**: гра сама розпізнає замкнений простір (стіни 2 блоки заввишки, хоча б одні двері, джерело світла) і за **набором меблів** присвоює йому тип — спальня, кухня, майстерня, лазня, музей тощо; кожна кімната додає **очки до рівня бази** і часто дає ефект (жителі готують у скриню, +HP, голод не падає). Відмінність від `rimworld-rooms` і `prison-architect-rooms`: тип визначається **рецептом з таблиці** (точні предмети й кількості), а не роллю, призначеною гравцем. Бій, крафт і сюжет розділів — фон.

## Поле і час
- Воксельна 3D-сітка блоків; кімната — область підлоги, обнесена стінами висотою 2 блоки (будь-які блоки), з дверима (будь-які).
- DQB2: площа кімнати 4–150 клітин; «кімната» — стіни 2 блоки + будь-які двері **або** 1 блок + хвіртка / двері салуну; «площа» — 1–2 блоки з килимком замість дверей; «поле» — кімната чи площа з опудалом.
- Час — real-time з циклом день/ніч; уночі сильніші монстри; набіги з босом періодично.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Будівник | player | HP, голод, спорядження | ставить і ламає блоки, крафтить; рівня не має |
| Блок (земля, камінь, цегла…) | static | матеріал | стіна кімнати; монстри можуть зламати |
| Двері / хвіртка / двері салуну / килимок | gate | — | обовʼязкові для кімнати; вид визначає кімнату / площу (DQB2) |
| Джерело світла (смолоскип, свічник, жаровня…) | object | вид | обовʼязкове; деякі рецепти вимагають певне |
| Меблі-інгредієнти (ліжко, багаття, скриня, верстат, стіл, стілець, вітрина, статуя, гарячі блоки води…) | object | вид, кількість | разом утворюють рецепт |
| Кімната | zone | тип з 82, очки, ефект | розпізнається автоматично; дає ефект і очки |
| Прапор надії (Banner of Hope) | static | колір розділу | перетворює довкола на базу; точка збереження; притягує людей |
| База | zone | рівень | рівень за кімнатами й будівлями; не знижується |
| Житель (resident) | ally | приватна кімната, роль | готує, крафтить, збирає врожай у скриню за типом кімнати; бʼється |
| Скриня | container | — | склад, куди жителі кладуть зроблене |
| Монстр | enemy | день/ніч | шкодить будівлям і Будівнику; набіг з босом |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `custom: «поставлено або знято блок/меблі»` → ЯКЩО `custom: «підлога обнесена стінами висотою ≥ 2 блоки»` and `has(enclosure, door)` and `has(enclosure, light_source)` → ТО `custom: «це кімната»`.
- КОЛИ `custom: «розпізнано кімнату»` → ЯКЩО `count(straw_mattress, >=, 2)` and `count(light_source, >=, 1)` → ТО `set_state(room, basic_bedroom)`, `custom: «жителі +10 % макс. HP»`.
- КОЛИ `custom: «розпізнано кімнату»` → ЯКЩО `count(fancy_bed, >=, 2)` and `count(light_source, >=, 1)` → ТО `set_state(room, fancy_bedroom)` (+15 % HP).
- КОЛИ `custom: «розпізнано кімнату»` → ЯКЩО `count(cookfire, >=, 1)` and `count(chest, >=, 1)` → ТО `set_state(room, crude_kitchen)`; жителі готують і кладуть у скриню.
- КОЛИ `custom: «розпізнано кімнату»` → ЯКЩО `custom: «багаття, скриня, 2 столи, 4 стільці, 1 декоративна їжа»` → ТО `set_state(room, cookfire_cafe)`, `custom: «голод у базі не падає»`.
- КОЛИ `custom: «розпізнано кімнату»` → ЯКЩО `custom: «верстат муляра/теслі + скриня + світло»` → ТО `set_state(room, workshop)`; жителі крафтять меблі й матеріали в скриню.
- КОЛИ `custom: «розпізнано кімнату»` → ЯКЩО `count(crop, >=, 10)` and `count(chest, >=, 1)` and `count(light_source, >=, 1)` → ТО `set_state(room, indoor_allotment)`; жителі збирають урожай.
- КОЛИ `custom: «розпізнано кімнату»` → ЯКЩО `count(hot_water_block, >=, 12)` and `count(light_source, >=, 1)` → ТО `set_state(room, public_baths)` (без ефекту).
- КОЛИ `custom: «розпізнано кімнату»` → ЯКЩО `custom: «лава + 4 вітрини + світло»` → ТО `set_state(room, museum)`, `custom: «+1 автовідновлення HP»`.
- КОЛИ `custom: «розпізнано кімнату»` → ЯКЩО `custom: «табличка жителя + горщик + ліжко + світло»` → ТО `set_state(room, private_bedroom)`; призначається конкретному жителю.
- КОЛИ `custom: «кімнату визнано»` → ТО `counter(base_points, +room_points)` (Телепортаріум — 100, Спальня принцеси — 500, Сад Кантліна — 3000).
- КОЛИ `counter(base_points, >=, next_level)` → ТО `custom: «рівень бази +1: більше жителів, кращі предмети»`; рівень бази ніколи не знижується.
- КОЛИ `custom: «два ефекти кімнат однакового виду»` → ТО `custom: «не сумуються»` (за вікі — «імовірно»).
- КОЛИ `contact(monster, block)` → ТО `damage(block, n)`, `custom: «досвід міста падає, але рівень бази — ні»`.
- КОЛИ `custom: «стіну кімнати зламано»` → ЯКЩО `not custom: «периметр замкнений»` → ТО `custom: «кімната перестає діяти»` (?).
- КОЛИ `custom: «ніч»` → ТО `spawn(stronger_monsters)`; КОЛИ `schedule(raid)` → ТО `spawn_at(horde_with_boss, base_edge)`.
- КОЛИ `tick` → ТО `counter(hunger, -1)` (?); ЯКЩО `state(room, cookfire_cafe)` and `custom: «Будівник у базі»` → ТО `block` спаду.
- DQB2: КОЛИ `custom: «розпізнано кімнату»` → ЯКЩО `custom: «площа поза межами 4–150 клітин»` → ТО `custom: «не кімната»`.
- DQB2: КОЛИ `adjacent(basic_bedroom, reception_room)` → ТО `set_state(room, hotel)`; КОЛИ `adjacent(simple_kitchen, dining_room)` → ТО `set_state(room, restaurant)`.
- DQB2: КОЛИ `custom: «у кімнаті чи площі є опудало»` → ТО `set_state(room, field)`; фермери обробляють і садять.
- DQB2: КОЛИ `custom: «стіни 1 блок + хвіртка чи двері салуну»` → ТО `custom: «теж кімната»`; КОЛИ `custom: «килимок замість дверей»` → ТО `set_state(room, plaza)`.
- Перемога: цілі розділу (бос) · Поразка: смерть Будівника — повернення до прапора (?) · Рахунок: рівень бази.

## Керування і ввід
- Від третьої особи: Будівник ставить блок чи меблі на клітину перед собою / під прицілом, ламає зброєю чи інструментом.
- Крафт на верстатах; рецепти кімнат з'являються в книзі, коли їх відкрито (?).
- Повідомлення про розпізнану кімнату (назва типу) — у момент, коли рецепт виконано (?).

## Вікна, меню, HUD
- `game-screen`: 3D-світ, HUD — `hp-bar`, `hunger-bar`, `inventory-bar` (швидкі предмети), `+ui:room-found-banner` (?).
- `+window:room-recipe-book` — перелік знайдених рецептів кімнат з інгредієнтами (?); `+window:base-level` — рівень бази й прогрес (?).
- `inventory-window`, крафт-вікно верстата (`+window:crafting-window` — повтор), `map-window`.
- `main-menu` → `chapter-select` (4 розділи) / Terra Incognita → `game-screen`; збереження — біля Прапора надії.

## Фічі поза полем
- `levels-sequential` (4 розділи, кожен з нуля), `save-game` у Прапора, `+feature:free-build` (Terra Incognita: острови, Banner of Freedom, обмін рецептами з розділів; на мобільних/PC — нескінченні матеріали, Builder Mode).
- DQB2: онлайн-кооператив і острови-розділи (?).

## Варіації й родичі
- **Dragon Quest Builders 2** (2018 (?)): межі площі 4–150, площа / поле, сусідні кімнати апгрейдять тип (готель, ресторан), рецепти з «будь-який із» (3 багаття або 1 цегляний мангал).
- Корпус: `rimworld-rooms` (кімната як flood fill + оцінка), `prison-architect-rooms` (вимоги до кімнат), `theme-hospital` / `two-point-hospital` (кімната за обладнанням), `minecraft-redstone` (блоковий світ), `core-keeper`.
- Осі: **хто визначає тип** — гравець малює зону (Prison Architect) / роль за вмістом (RimWorld) / **точний рецепт з таблиці** (DQB) · **периметр** — стіни + дах / стіни + двері + світло / також висота й площа (DQB2) · **сусідство кімнат** — нема (DQB) / апгрейд типу (DQB2).

## Цікавинки для курсу
- Розпізнавання кімнати: flood fill підлоги до стін висотою ≥ 2 + перевірка дверей і світла — 🥉.
- Рецепт як мультимножина предметів → тип; кілька рецептів збігаються — вибір пріоритетного — 📎.
- Очки кімнат → рівень бази з порогами, що не падає — 🌱.
- Ефект кімнати на жителів (готують у скриню, крафтять) — 📎.
- DQB2: сусідні кімнати перетворюють тип (спальня + рецепція = готель) — 📎.
- Площа замість кімнати за видом входу (двері / килимок) — 🌱.

## Мапа на каталог
- Є: `destructible-blocks` (монстри, Будівник) · `cursor-place` · `coverage-area` (база довкола прапора) · `hp-damage` · `hunger-clock` · `inventory` · `enemy-waves` (набіги з босом) · `sequential-levels` (розділи) · `save-game` · `connectivity-check` (замкненість периметра).
- **Нема** → пропозиції карток:
  - `+room-recipe-catalog` «Тип кімнати за рецептом з таблиці предметів» · entities/state · 📎.
  - `+adjacent-room-upgrade` «Сусідні кімнати апгрейдять тип» · entities/state · 🌱.
  - `+base-level-points` «Рівень бази за очками кімнат» · game-logic/score · 🌱.
  - `+resident-auto-craft` «Жителі виробляють у скриню за типом кімнати» · entities/spawn · 📎.
  - `+day-night-cycle` «День/ніч міняє спавн» · entities/spawn · 🌱.
  - `+ratchet-level` «Рівень, що не знижується» · game-logic/score · 🌱.
  - `+room-effect-no-stack` «Ефекти одного виду не сумуються» · entities/state · 🌱.
  - Повтори: `+place-wall-floor` (`core-keeper`), `+sector-flood-fill`, `+room-grading` (`rimworld-rooms`), `+room-requirements` (`prison-architect-rooms`).

## Пропозиції до словників
- `+cond:enclosed` (повтор з `rimworld-rooms`, `theme-hospital`, `space-haven`) — область обнесена стінами.
- `+cond:wall_height` — стіни периметра не нижчі за N блоків.
- `+trigger:room_changed` (повтор з `rimworld-rooms`) — змінився вміст або периметр кімнати.
- `+effect:set_room_type` — присвоїти кімнаті тип за рецептом (замість `set_state(room, …)`).
- `+role:resident` (повтор з `tiny-tower-simtower`) — житель бази з роботою за кімнатою.
- `+window:room-recipe-book`, `+window:base-level`, `+window:crafting-window` (повтор з `core-keeper`), `+ui:room-found-banner`.
- `+feature:free-build` — вільний режим з відкритими рецептами (родич `mode-sandbox`, але з прогресією).
- `+card:room-recipe-catalog`, `+card:adjacent-room-upgrade`, `+card:base-level-points`.

## Джерела
- ⭐ [Dragon Quest Wiki: Room Recipes (DQB)](https://dragon-quest.org/wiki/Room_Recipes_(Dragon_Quest_Builders)) — «All rooms require walls 2 blocks high and at least 1 door», світло обовʼязкове; рецепти з кількостями, очки, ефекти; 82 типи; ефекти не сумуються.
- [Dragon Quest Wiki: room recipes DQB2](https://dragon-quest.org/wiki/List_of_room_recipes_in_Dragon_Quest_Builders_2) — 4–150 клітин; кімната / площа / поле; готель і ресторан від сусідства; рецепти «будь-який із».
- [Wikipedia: Dragon Quest Builders](https://en.wikipedia.org/wiki/Dragon_Quest_Builders) — кімнати додають до рівня бази, день/ніч, голод; дати релізів і платформи.
- [Dragon Quest Wiki: Dragon Quest Builders](https://dragon-quest.org/wiki/Dragon_Quest_Builders) — рівень бази не падає, монстри шкодять будівлям, набіги з босом, розділи, Terra Incognita.
- [Dragon Quest Wiki: Banner of Hope](https://dragon-quest.org/wiki/Banner_of_Hope) — база довкола прапора, збереження, Banner of Freedom.
- YouTube: пошук «Dragon Quest Builders room recipes».

## Непевне
- (?) Межі площі кімнати в DQB1 (у DQB2 — 4–150) і чи потрібен дах — джерело не каже.
- (?) Що вибирає гра, коли збігаються кілька рецептів (пріоритет «кращого»), — не сказано; у вікі лише, що ефекти не сумуються.
- (?) Пороги рівнів бази в очках — не знайдено.
- (?) Кімната перестає діяти після пролому стіни; повідомлення про розпізнану кімнату й книга рецептів — з памʼяті.
- (?) Спад голоду за тіком, смерть Будівника → повернення до прапора, кооператив DQB2 — з памʼяті.
- (?) Вікі описує світло як обовʼязкове, але для кількох рецептів (Cookfire café, Holy hostel) світла в таблиці нема.
