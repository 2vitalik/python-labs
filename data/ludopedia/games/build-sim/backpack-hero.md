---
title: Backpack Hero
slug: backpack-hero
family: build-sim
also: [roguelike, tactics]
klass: hybrid
axes:
  field: square
  time: turn
  opponent: ai
  info: partial
  random: both
  goal: survive
year: 2023
platforms: [PC, macOS, Linux, Switch, PS4, PS5, Xbox One, Xbox Series]
links:
  - {kind: fandom, url: "https://backpackhero.wiki.gg/wiki/Backpack_Hero_Wiki", best: true, note: "офіційна вікі: персонажі, статуси, підземелля, атлас предметів"}
  - {kind: steam, url: "https://store.steampowered.com/app/1970580/Backpack_Hero/", note: "опис: 800+ предметів, 100+ ворогів, 5 героїв, місто Haversack Hill"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Backpack_Hero", note: "дати, платформи, жанр «inventory management roguelike»"}
  - {kind: fandom, url: "https://backpackhero.wiki.gg/wiki/Status_Effects", note: "16 статусів зі стеками"}
  - {kind: fandom, url: "https://backpackhero.wiki.gg/wiki/CR-8", note: "заряди енергії, що біжать рюкзаком"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=backpack+hero+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [inventory, inventory-items, inventory-limit, multi-cell-size, orientation-state, drag-drop-piece, hover-highlight, hp-damage, temporary-modes, telegraphed-intents, ai-opponent, shop-between-levels, shop-catalog, shop-buyback, shop-window, dungeon-generation, sequential-levels, +shaped-items, +adjacency-buff, +bag-expansion, +energy-per-turn, +status-stacks, +charge-routing, +deck-in-grid, +town-builder]
proposes: ["+trigger:turn_start", "+trigger:turn_end", "+trigger:adjacent", "+trigger:hp_zero", "+cond:adjacent_count", "+cond:has", "+cond:state", "+effect:rotate", "+effect:damage", "+effect:set_state", "+effect:hp", "+effect:heal", "+effect:counter", "+effect:choose", "+effect:set_side", "+effect:end_turn", "+role:container", "+role:ally", "+role:boss", "+role:zone", "+ui:energy-bar", "+ui:hp-bar", "+ui:telegraph-marker", "+ui:end-turn-button", "+ui:tooltip", "+ui:adjacency-overlay", "+window:inventory-window", "+window:upgrade-window", "+window:map-window", "+window:character-select", "+feature:meta-progression", "+card:adjacency-buff"]
author: opus
date: 2026-11-02
---

# Backpack Hero — рюкзак-сітка і є бойова система: форма, поворот і сусідство предметів вирішують бій

## Суть
Роглайт, де інвентар — головне поле гри: предмети різних форм (поліміно) треба вмістити в сітку рюкзака, і **позиція визначає силу** — багато предметів підсилюють сусідів у позначених клітинах. У покроковому бою гравець витрачає енергію, клікаючи по предметах у рюкзаку (меч бʼє, щит дає блок), а вороги заздалегідь показують наміри. Між боями — підземелля з кімнатами, лут, крамниці, рівні з розширенням рюкзака. Клас `hybrid`: `cursor` (перекладання предметів) + `avatar` (герой іде мапою підземелля).

## Поле і час
- **Головне поле — рюкзак**: квадратна сітка клітин, що росте з рівнями (Pochette — 5×7; Satchel розширює в межах 5×11). Клітини рюкзака бувають розірвані — окремі «кишені» (Satchel рахує їх як окремі pockets).
- Поза рюкзаком — «підлога» з лутом: предмети, що лишились поза сіткою, при виході з кімнати втрачаються (?).
- Друге поле — **мапа поверху**: сітка кімнат, яку герой досліджує кліком (туман недосліджених — `info: partial`); унизу — сайд-вʼю бою.
- Час — покроковий: хід гравця (енергія) → хід ворогів (виконання намірів). Статуси тікають на початку/кінці ходу.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой (Purse, Satchel, Tote, CR-8, Pochette) | player | HP, енергія/хід (Pochette — 2; базово 3 (?)), рівень | використовує предмети з рюкзака; кожен має унікальний механізм |
| Клітина рюкзака | zone | — | місце, куди можна покласти предмет; додається при рівні |
| Предмет-зброя (меч, сокира, лук) | object | форма, енергія, шкода, клітини-цілі ★ | клік → шкода цілі; підсилюється сусідами |
| Броня/щит | object | форма, енергія, блок | клік (або пасивно на початку ходу (?)) → блок |
| Предмет-підсилювач | object | діаграма клітин | дає бонус предметам у позначених клітинах (+шкода, +блок, −енергія) |
| Манакамінь + жезл/посох | object | мана | жезли витрачають ману з каменів (?) |
| Золото | pickup | займає місце | валюта, але теж лежить у рюкзаку |
| Прокляття (Cursed Item) | object | займає місце | шкідливий предмет-лут від статусу Curse |
| Споживане (зілля, їжа) | pickup | заряди | одноразовий ефект |
| Ворог | enemy | HP, намір на наступний хід | показує намір (атака N, блок, бафф, статус); виконує в хід ворогів |
| Бос | boss | фази (?) | у кінці акту; після нього — вибір наступної зони |
| Скриня / Chest crab | container / enemy | — | лут; мімік-краб нападає |
| Торговці (Dungeon Shop, Healer, Master Smith, Chester…) | neutral | — | купівля/продаж, лікування, кування, обмін «рівного розміру» |
| Ядро CR-8 | object | 3 енергії на заряд | створює заряд, що біжить рюкзаком по прямій |
| Компонент CR-8 | object | — | повертає заряд, додає енергію, породжує заряди |
| Різьблення Tote (Carving) | object | ціна виклику/застосування | карта з колоди: тягнеться (до 5), кладеться в рюкзак, скидається в кінці ходу |
| Улюбленець Pochette | ally | HP, енергія, статуси | викликається з рюкзака, стоїть перед героїнею, ворог бʼє передню |
| Бонусний предмет Purse | pickup | до 3 за бій | зʼявляється ліворуч; не вмістила до кінця ходу — зникає |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag, item, cell)` → ЯКЩО `custom: «усі клітини форми предмета лягають на вільні клітини рюкзака»` → ТО розміщення; інакше предмет лишається поза рюкзаком.
- КОЛИ `input(rotate, item)` → ТО `rotate(item, 90)` — форма і діаграма сусідства обертаються разом.
- КОЛИ `turn_start(player)` → ТО `counter(energy, =base)`; `custom: «предмети з ефектом Each Turn / Start of Turn спрацьовують»`.
- КОЛИ `input(click, item)` → ЯКЩО `counter(energy, >=, cost)` → ТО `counter(energy, -cost)`, ефект предмета (`damage(n)` у ціль, `custom: «+block n»`, статус).
- Бонус сусідства: ЯКЩО `custom: «предмет B лежить у ★-клітині діаграми предмета A»` and `custom: «тип B підходить (зброя/броня/за тегом)»` → ТО B отримує модифікатор (+шкода/+блок/−вартість).
- КОЛИ `input(end_turn)` → ТО `end_turn`; вороги виконують показані наміри; блок гравця поглинає шкоду.
- КОЛИ `turn_start(enemy)` → ТО ворог показує **наступний** намір (`telegraph-marker`).
- Статуси: стеки, більшість −1 за хід. Haste/Slow ±блок предметів; Rage/Weak ±шкода предметів; Poison — шкода в кінці ходу крізь блок і ухил (стеків > HP ворога → пропускає хід); Burn — шкода на початку ходу; Spikes — шкода атакуючому; Freeze — +вхідна шкода; Dodge — скасовує N атак; Regen — лікування на старті; Sleep — пропуск ходу; Charm — стеків ≥ HP → `set_side(enemy, player)`; Curse — після бою один предмет луту стає проклятим; Exhaust — −1 енергія.
- КОЛИ `hp_zero(enemy)` для всіх → ТО `custom: «XP + лут»`, `window(loot)`; ЯКЩО XP ≥ поріг → `choose(new_bag_cells)` (Purse — окремі клітини; Satchel і CR-8 — тетроміно).
- КОЛИ `hp_zero(player)` → ТО `lose` (кінець забігу, повернення в місто/меню).
- КОЛИ `custom: «покидаєш кімнату з предметами поза рюкзаком»` → ТО `disappear` (?).
- CR-8: КОЛИ ядро використано → ТО `spawn(charge, energy 3)`; заряд `move` по прямій, використовує кожен предмет, через який проходить, і платить його вартість; енергія 0 → `disappear`, далі інші заряди; усі зникли → `end_turn`. Перекладання під час бою зазвичай пропускає хід.
- Tote: КОЛИ `turn_start` → `custom: «тягнути до 5 різьблень з колоди»`; невикористані — у скид наприкінці ходу; колода порожня → скид перемішується. Kin — бонус поруч; Sap — ефект у групі ≥3; Toss (1 енергія) — скинути все з рюкзака, 1 шкода за кожне.
- Pochette: виклик улюбленця коштує енергію; ворог атакує найпереднього (улюбленця або Pochette); Recall (1 енергія) повертає в рюкзак, знімає статуси; мертвий оживає після бою з 1 HP.
- Purse: Scratch (1 енергія, 3 шкоди) — базова атака; бонусні предмети зʼявляються ліворуч (≤3 за бій).
- Перемога: пройти фінальний бос акту 3 (Magma Core або Frozen Heart) (?) · Поразка: HP героя = 0 · Рахунку нема (прогрес — місто і розблокування).

## Керування і ввід
- Миша: drag предмета між рюкзаком і підлогою, ПКМ/R/колесо — поворот під час перетягування (?), клік по предмету — використати, кнопка End Turn.
- Клік по ворогу — вибір цілі (?); наведення — тултип предмета з діаграмою сусідства й ефектом.
- Мапа поверху: клік по кімнаті — герой іде туди.
- Геймпад: курсор + кнопки повороту (консолі).

## Вікна, меню, HUD
- `game-screen` (бій): рюкзак-сітка в центрі, підлога з лутом поруч, внизу — сайд-вʼю героя і ворогів з `telegraph-marker` (іконка + число намірів), `hp-bar` і статуси над кожним, `energy-bar` героя, `end-turn-button`, `tooltip` предмета, `adjacency-overlay` (підсвітка ★-клітин при перетягуванні) (?).
- `map-window` поверху: сітка кімнат, туман, іконки подій/крамниць/сходів.
- Лут після бою (`custom-window`) — предмети викладаються на підлогу; рівень → вибір нових клітин рюкзака (`upgrade-window`).
- `shop-window` (Dungeon Shop, Alchemist, Apprentice Mage — жезли); Master Smith — кування; Chester — обмін предметів однакового розміру; Healer.
- Вибір зони після боса (`choose`): The Crypt/The Bramble → Deep Cave/Enchanted Swamp → Magma Core/Frozen Heart.
- `character-select` (5 героїв, вбрання), Story Mode → місто Haversack Hill (`custom-window`: будування, мешканці, дослідження, квести).
- `main-menu`, `settings-window`, `pause-menu`, `end-screen` забігу.
- Переходи: main-menu → (Story) місто → вхід у підземелля → character-select → map-window ↔ бій/подія/крамниця → бос → вибір зони → … → end-screen.

## Фічі поза полем
- `meta-progression`: місто Haversack Hill — ресурси з підземелля → будівлі, мешканці, дослідження, розблокування героїв, викликів і квестів; окремо — standalone-забіги.
- `unlockables` (герої, вбрання, предмети), `achievements`, `save-game` (продовжити забіг), `difficulty-presets`/виклики (?).
- `codex` — атлас предметів у грі (?); `tutorial`.
- Процедурні поверхи й лут (`random: both`).

## Варіації й родичі
- Backpack Battles (2024, PvP-автобатлер рюкзаків — бій автоматичний, синергії «поруч»), Resident Evil 4 (кейс-сітка без бою), Slay the Spire (енергія + наміри ворогів — пряме джерело бойової частини), Loop Hero (тайли обслуговують бій), Luck be a Landlord (сітка слотів із сусідством), Peglin, Dicey Dungeons (слоти кубиків).
- Осі «сітка-інвентар»: лише місткість (RE4) / сусідство дає бонуси (BH) / форма = і місце, і ефект (CR-8 — шлях заряду).
- Осі «розширення»: окремі клітини / тетроміно / сумки-предмети з клітинами (Backpack Battles).
- Осі «використання»: клік з енергією (BH) / автоматичний cooldown (BB) / карта з колоди, що кладеться в сітку (Tote).

## Цікавинки для курсу
- Предмети-поліміно в сітці: розміщення, поворот на 90°, колізії — 📎 (основа: як Tetris без падіння).
- Діаграма сусідства ★ (предмет підсилює клітини навколо себе, обертається разом із ним) — 🥉.
- Покроковий бій з енергією і телеграфованими намірами ворогів — 🥉.
- Статуси-стеки з тіком на початку/кінці ходу (16 видів з різними правилами) — 🥉 за сімʼю.
- Розширення рюкзака при рівні вибором клітин/тетроміно — 📎.
- CR-8: заряд енергії біжить рюкзаком по прямій, компоненти повертають його — 🥈 (рюкзак як «плата» з маршрутом, близько до Factorio-конвеєра).
- Tote: колода карт, що кладуться в сітку, з синергіями груп ≥3 — 🥇 (дві системи разом: deckbuilder + полімінальне поле).

## Мапа на каталог
- Є: `inventory` + `inventory-items` + `inventory-limit` (рюкзак) · `multi-cell-size` (форми) · `orientation-state` (поворот) · `drag-drop-piece` + `hover-highlight` · `hp-damage` · `temporary-modes` (статуси) · `telegraphed-intents` · `ai-opponent` · `shop-between-levels` + `shop-catalog` + `shop-buyback` + `shop-window` · `dungeon-generation` · `sequential-levels` (поверхи) · `save-game` · `item-pickup`.
- **Нема** → пропозиції карток:
  - `+shaped-items` «Предмети-фігури в сітці інвентаря» · entities/state · 📎 · слоти {shapes, rotate} — дитина `inventory`.
  - `+adjacency-buff` «Бонус за сусідство в сітці» · entities/interact · 🥉 · слоти {pattern, filter} — Backpack Hero/Battles, Luck be a Landlord.
  - `+bag-expansion` «Розширення поля клітинами/фігурами» · levels/progression · 📎.
  - `+energy-per-turn` «Енергія на хід» · game-logic/economy · 🌱.
  - `+status-stacks` «Статуси зі стеками й тіком» · entities/state · 🥉.
  - `+charge-routing` «Заряд іде полем по прямій і активує клітини» · entities/move · 🥈 (CR-8).
  - `+deck-in-grid` «Карти з колоди кладуться в сітку» · game-logic · 🥇 (Tote).
  - `+town-builder` «Мета-місто між забігами» · levels/progression · 🥈.

## Пропозиції до словників
- `+trigger:turn_start`, `+trigger:turn_end` (статуси, енергія), `+trigger:adjacent` (сусідство в рюкзаку), `+trigger:hp_zero`.
- `+cond:adjacent_count` (Sap ≥3), `+cond:has`, `+cond:state`.
- `+effect:rotate`, `+effect:damage`, `+effect:set_state`, `+effect:hp`, `+effect:heal`, `+effect:counter` (енергія), `+effect:choose` (нові клітини, зона, лут), `+effect:set_side` (Charm), `+effect:end_turn`.
- `+role:container` (скриня/рюкзак), `+role:ally` (улюбленці), `+role:boss`, `+role:zone` (клітини рюкзака, кишені).
- `+ui:energy-bar`, `+ui:hp-bar`, `+ui:telegraph-marker`, `+ui:end-turn-button`, `+ui:tooltip`; новий `+ui:adjacency-overlay` — підсвітка клітин, які предмет підсилює, під час перетягування.
- `+window:inventory-window` (тут він же `game-screen`), `+window:upgrade-window` (вибір клітин рюкзака), `+window:map-window`, `+window:character-select`.
- `+feature:meta-progression`.
- `+card:adjacency-buff` — див. вище.

## Джерела
- ⭐ [Backpack Hero Wiki (wiki.gg)](https://backpackhero.wiki.gg/wiki/Backpack_Hero_Wiki) — вхід у вікі: персонажі, атлас предметів, статуси, підземелля.
- [Status Effects](https://backpackhero.wiki.gg/wiki/Status_Effects) — 16 статусів зі стеками й правилами.
- [CR-8](https://backpackhero.wiki.gg/wiki/CR-8) · [Tote](https://backpackhero.wiki.gg/wiki/Tote) · [Satchel](https://backpackhero.wiki.gg/wiki/Satchel) · [Pochette](https://backpackhero.wiki.gg/wiki/Pochette) · [Purse](https://backpackhero.wiki.gg/wiki/Purse) — унікальні механіки героїв.
- [Dungeon](https://backpackhero.wiki.gg/wiki/Dungeon) — зони актів, події, торговці.
- [Steam](https://store.steampowered.com/app/1970580/Backpack_Hero/) — 800+ предметів, 100+ ворогів, місто.
- [Wikipedia](https://en.wikipedia.org/wiki/Backpack_Hero) — дати (EA 2022, реліз 14.11.2023), платформи, порівняння з кейсом RE4.
- YouTube: пошук «backpack hero gameplay».

## Непевне
- (?) Базова енергія 3/хід (підтверджено лише 2 для Pochette); чи броня діє пасивно; мана-камені й жезли.
- (?) Втрата предметів поза рюкзаком при виході з кімнати; поворот клавішею R/ПКМ; вибір цілі кліком.
- (?) Кількість поверхів у зоні, боси з фазами, фінальна умова перемоги; кількість клітин за рівень у Purse.
- (?) Наявність `adjacency-overlay` і внутрішнього атласу — з памʼяті.
- WebSearch вичерпано; загальні сторінки механік (енергія, рівні) на вікі не знайдено.
