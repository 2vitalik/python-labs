---
title: Dungeons of Dredmor
slug: dungeons-of-dredmor
aka: [Dredmor, DoD]
family: roguelike
also: []
klass: avatar
axes:
  field: square
  time: turn
  opponent: ai
  info: hidden
  random: both
  goal: state
year: 2011
platforms: [PC, macOS, Linux]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Dungeons_of_Dredmor", best: true, note: "ядро: 7 навичок на старті, крамниці на кожному поверсі, артефакти, Lutefisk God, статуї Inconsequentia, складності, permadeath-перемикач, DLC"}
  - {kind: steam, url: "https://store.steampowered.com/app/98800/", note: "Steam: крафт («товкти злитки в алюмінієвий порошок»), Lutefisk, Workshop, permadeath"}
  - {kind: other, url: "https://www.roguebasin.com/index.php/Dungeons_of_Dredmor", note: "RogueBasin: Diggles, Swarmies, пастки гравця, point-and-click, магії Necronomiconomics і Viking Runes"}
  - {kind: other, url: "https://en.wikipedia.org/wiki/List_of_roguelikes", note: "рядок у списку роглайків: Gaslamp Games, 2011"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=dungeons+of+dredmor+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [move-by-input, cell-click, dungeon-generation, stairs-levels, hp-damage, unit-xp-skills, inventory, inventory-items, item-pickup, melee-vs-ranged, projectile-shot, status-effects, shop-catalog, round-currency, thief, permadeath, difficulty-levels, player-death, message-log, fog-of-war, save-game, +skill-loadout, +crafting-recipes, +sacrifice-altar, +side-quest-giver, +player-traps, +artifact-random-names, +monster-house]
proposes: ["+feature:skill-loadout", "+feature:crafting", "+feature:permadeath-toggle", "+feature:short-floors", "+window:skill-select", "+window:crafting-window", "+window:skill-tree-window", "+effect:craft(recipe)", "+effect:sacrifice(item)", "+effect:quest(kind)", "+role:altar"]
author: opus
date: 2026-11-09
---

# Dungeons of Dredmor — роглайк-пародія: зібрав 7 абсурдних навичок, крафтиш з мотлоху й ідеш убивати Лорда Дредмора

## Суть
Класичний покроковий данжен-кроулер (Gaslamp Games, 2011): спуск поверхами процедурного підземелля до Лорда Дредмора. Головне рішення — на старті: гравець **сам складає «клас» із 7 навичок** зі списку (бойові, злодійські, магічні, ремісничі), і кожна росте з рівнями. Друга опора — **крафт** інструментами з набору предметів (кування, алхімія, «тинкерінг»). Усе загорнуто в гумор: Lutefisk God, богиня безглуздих квестів, монстри Diggles і зброя з беконом.

## Поле і час
- Квадратна сітка, вид згори; поверхи — випадкові лабіринти кімнат, звʼязаних коридорами, з монстрами, пастками, лутом і обʼєктами (Wikipedia).
- Час: 1 дія гравця = 1 хід (крок, удар, взяти/кинути/використати предмет, взаємодія з обʼєктом); монстри відповідають своїми діями.
- Поверхи йдуть униз зі зростанням складності; режим «No Time To Grind?» робить поверхи меншими, але з тим самим досвідом.
- Видимість — розвідана частина поверху, решта в тумані; кімнати відкриваються при вході.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой (з бровами) | player | HP, мана, 7 обраних навичок, рівень, характеристики | крок / удар / магія / предмет за хід |
| Монстр (Diggle, Swarmy, Thrusty, «цегляний демон з вусами»…) | enemy | HP, тип шкоди, опори | помітивши, переслідує; деякі будують гнізда (Diggles) |
| Кімната-зоопарк монстрів | zone | (?) | кімната, набита монстрами й лутом |
| Крамар | neutral | асортимент поверху | купівля/продаж; крадіжка → натовп сильних ворогів |
| Статуя Inconsequentia | neutral | — | видає квест: вбити загін / знайти артефакт / доставити артефакт |
| Статуя Lutefisk God | static | лічильник пожертв (?) | приймає лютефіск; винагорода — артефакт |
| Ковадло Крона (Anvil of Krong) | static | — | дає артефакт (?) за використання |
| Сходи вниз | static | — | наступний поверх |
| Пастка (підземелля) | hazard | тип; прихована | спрацьовує при вході |
| Пастка гравця | object | з навички/крафту | ставить гравець; спрацьовує на ворогові |
| Зброя / броня | pickup | тип шкоди, бонуси | екіпірування |
| Артефакт | pickup | випадкова назва, дод. атрибути | виглядає як звичайна річ, але з бонусами й типами шкоди |
| Їжа / напої / зілля | pickup | — | відновлення HP/мани, ефекти |
| Лютефіск | pickup | «неїстівний» | валюта для Lutefisk God |
| Матеріали для крафту (злитки, порошки, деталі) | pickup / resource | рецепти | інгредієнти рецептів |
| Zorkmids | pickup | купка | валюта |
| Скрині, бочки, важелі | container / switch | — | лут; важіль змінює щось на поверсі (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
Хід і бій:
- КОЛИ `input(dir)` → ЯКЩО `free(cell)` → ТО `move(hero, dir)`; ЯКЩО `occupied(cell, enemy)` → ТО `damage(n)` (мілі).
- КОЛИ `input(skill, target)` → ЯКЩО `has(hero, mana)` → ТО ефект навички (`damage`, `set_state`, `spawn`), `counter(mana, −n)`; інакше `block`.
- КОЛИ `turn_end(hero)` → ТО монстри роблять свої ходи.
- КОЛИ `hp_zero(enemy)` → ТО `counter(xp, +n)`; ЯКЩО `counter(xp, >=, threshold)` → ТО `custom: «новий рівень, очко в одне з дерев навичок»`.
- КОЛИ `hp_zero(hero)` → ЯКЩО `mode(permadeath)` → ТО `lose` (персонаж зникає); інакше `custom: «завантаження сейву»`.

Предмети й крафт:
- КОЛИ `contact(hero, item)` → ТО `pickup`.
- КОЛИ `input(craft, tool, recipe)` → ЯКЩО `has(hero, ingredients)` and `custom: «рівень ремісничої навички ≥ вимоги рецепта»` → ТО `take(hero, ingredients)`, `give(hero, product)`.
- КОЛИ `input(equip, artifact)` → ТО `custom: «бонуси артефакту, часто з додатковим типом шкоди»`.

Боги, квести, крамниці:
- КОЛИ `input(use, lutefisk_statue)` → ЯКЩО `has(hero, lutefisk)` → ТО `take(hero, lutefisk)`; ЯКЩО `counter(lutefisk_given, >=, n)` → ТО `give(hero, artifact)`.
- КОЛИ `input(use, inconsequentia_statue)` → ТО `custom: «квест: вбити загін / принести артефакт / доставити артефакт у точку»`; КОЛИ `custom: «квест виконано»` → ТО `give(hero, artifact)`.
- КОЛИ `input(buy, item)` → ЯКЩО `has(hero, zorkmids >= price)` → ТО `currency(−price)`, `give(hero, item)`.
- КОЛИ `custom: «гравець виносить неоплачене»` → ТО `spawn_at(powerful_enemies, around)` — кара за крадіжку.
- КОЛИ `enter(hero, monster_zoo)` → ТО `custom: «уся кімната атакує»` (?).

Пастки:
- КОЛИ `enter(hero, trap)` → ТО `reveal(trap)` + ефект пастки.
- КОЛИ `enter(enemy, player_trap)` → ТО ефект пастки на ворогові.

Перемога / поразка / рахунок:
- КОЛИ `died(lord_dredmor)` → ТО `win`.
- Поразка — смерть героя (з permadeath — остаточна). Рахунок як такого нема; мірило — глибина й кількість убитого (?).

## Керування і ввід
- Мишка: клік по клітині — крок/удар/взаємодія; клік по ворогу з вибраною навичкою — застосувати. Клавіатура — рух і гарячі клавіші навичок.
- Перетягування предметів між сумкою, слотами спорядження й панеллю швидкого доступу (рецензенти лаяли інвентар, Wikipedia).
- RogueBasin пише «без діагонального руху»; у грі — повернута (ізометрична на вигляд) плитка (?).

## Вікна, меню, HUD
- `main-menu` → `difficulty-select` (Elvishly Easy / Dwarven Moderation / Going Rogue) + перемикачі «permadeath» і «No Time To Grind?» → `skill-select` (вибір 7 навичок з сітки іконок) → `game-screen`.
- `game-screen`: поле, `hp-bar`, мана, `skill-bar` з іконками навичок і cooldown, `inventory-bar` (швидкі слоти), `message-log`.
- `inventory-window` + `equipment-slots` (спорядження на ляльці героя).
- `skill-tree-window` — дерева 7 навичок, куди витрачати очки рівня.
- `crafting-window` — вибір інструмента, список відомих рецептів, інгредієнти.
- `shop-window` — купити/продати у крамаря.
- `map-window` (?) — карта поверху.
- `end-screen` — смерть: епітафія, глибина, убите (?).
- `pause-menu`, `settings-window`, `confirm-dialog` на вихід.

## Фічі поза полем
- `difficulty-presets` (3 рівні), `permadeath-toggle` при створенні героя, `short-floors` («No Time To Grind?»).
- `mod-support`: XML-моди, Steam Workshop (нові навички, монстри, предмети).
- DLC: Realm of the Diggle Gods (2011), You Have To Name The Expansion Pack (2012), Conquest of the Wizardlands (2012) — нові навички, поверхи, вороги.
- `save-game` (у режимі permadeath сейв — лише продовження поточного забігу (?)).

## Варіації й родичі
- Родичі в корпусі: [Rogue](rogue.md) (джерело формату), [NetHack](nethack.md) (Zorkmid-гумор, крадіжка в крамаря), [Dungeon Crawl Stone Soup](dungeon-crawl-stone-soup.md) (навички замість класів), [Pixel Dungeon](pixel-dungeon.md) (мобільний аналог), [Tangledeep](tangledeep.md) (класи-«джоби» з комбінуванням).
- Осі варіацій: **клас** (фіксований / збірка з N навичок — Dredmor / вільна прокачка — DCSS); **крафт** (нема / інструменти з рецептами / алхімія-горщик — Pixel Dungeon); **смерть** (permadeath / перемикач на старті); **розмір поверху** (повний / «без гринду»).

## Цікавинки для курсу
- Вибір 7 навичок з N як «конструктор класу»: дерева з порогами за рівнем — 🥉 (дані навичок як таблиця + валідація вибору).
- Крафт: інструмент + рецепт + інгредієнти + рівень навички → продукт — 🥉 (база рецептів, пошук доступних).
- Lutefisk God: лічильник пожертв із порогом нагороди — 🌱.
- Квест-статуя з трьома шаблонами завдань — 📎 (генерація цілі та перевірка виконання).
- Крадіжка в крамаря → виклик натовпу ворогів — 📎.
- Артефакти з процедурними назвами й бонусами — 📎 (генератор назв + таблиця бонусів).

## Мапа на каталог
- Є: `move-by-input` · `cell-click` · `dungeon-generation` · `stairs-levels` · `hp-damage` · `unit-xp-skills` (рівні й очки навичок) · `inventory` + `inventory-items` · `item-pickup` · `melee-vs-ranged` · `projectile-shot` · `status-effects` · `shop-catalog` · `round-currency` (zorkmids) · `thief` (кара за крадіжку — навпаки, гравець-злодій) · `permadeath` · `difficulty-levels` · `player-death` · `message-log` · `fog-of-war` · `save-game`.
- **Нема** → пропозиції карток:
  - `+skill-loadout` «Клас як набір N навичок зі списку» · entities/state · 🥉 · слоти {n_slots, pool}.
  - `+crafting-recipes` «Крафт інструментом за рецептом» · entities/interact · 🥉 · слоти {tools, recipes}.
  - `+sacrifice-altar` «Вівтар: пожертви до порога → нагорода» · entities/interact · 🌱.
  - `+side-quest-giver` «Обʼєкт видає побічний квест із шаблонів» · game-logic/win · 📎.
  - `+player-traps` «Пастки, які ставить гравець» · entities/combat · 📎.
  - `+artifact-random-names` «Процедурні артефакти з назвою і бонусами» · entities/state · 📎.
  - `+monster-house` — уже пропоновано в Mystery Dungeon.

## Пропозиції до словників
- `+feature:skill-loadout` — збірка класу з N навичок на старті.
- `+feature:crafting` — система крафту поза полем (вікно рецептів).
- `+feature:permadeath-toggle` — permadeath вмикається при створенні героя.
- `+feature:short-floors` — режим менших поверхів без втрати прогресу (No Time To Grind).
- `+window:skill-select` — сітка навичок для вибору N на старті.
- `+window:crafting-window` — інструмент + рецепти + інгредієнти.
- `+window:skill-tree-window` — дерева навичок для очок рівня.
- `+effect:craft(recipe)` — забрати інгредієнти, видати продукт.
- `+effect:sacrifice(item)` — пожертвувати предмет обʼєкту-божеству.
- `+effect:quest(kind)` — видати побічне завдання.
- `+role:altar` — статуя/вівтар, що приймає предмети й дає нагороди.

## Джерела
- ⭐ [Wikipedia: Dungeons of Dredmor](https://en.wikipedia.org/wiki/Dungeons_of_Dredmor) — 7 навичок, хід, крамниці й крадіжка, артефакти, Lutefisk God, Inconsequentia, 3 складності, No Time To Grind, permadeath, DLC.
- [Steam](https://store.steampowered.com/app/98800/) — крафт, Lutefisk, Workshop, permadeath.
- [RogueBasin](https://www.roguebasin.com/index.php/Dungeons_of_Dredmor) — Diggles/Swarmies/Thrusties, пастки гравця, школи магії, point-and-click, «без діагоналей».
- [Wikipedia: List of roguelikes](https://en.wikipedia.org/wiki/List_of_roguelikes) — рік, платформи, розробник.
- YouTube: [пошук «dungeons of dredmor gameplay»](https://www.youtube.com/results?search_query=dungeons+of+dredmor+gameplay).

## Непевне
- (?) Кількість поверхів (10 у базі?), кількість навичок у пулі (~30+ з DLC більше) і їхня поділка на воїн/злодій/маг — з памʼяті; фан-вікі (fandom 402, wiki.gg 401, StrategyWiki 403) не відкрились.
- (?) Характеристики Burliness / Sagacity / Nimbleness + похідні (Caddishness, Stubbornness, Savvy) — з памʼяті.
- (?) Ремісничі навички (Smithing, Alchemy, Tinkering, Wand Lore) і їхні інструменти — з памʼяті; джерела кажуть лише «складний крафт».
- (?) Кімнати-зоопарки монстрів, ковадло Крона як «спосіб отримати артефакт», важелі — Wikipedia згадує ковадло, решта з памʼяті.
- (?) Діагональний рух: RogueBasin — «нема», памʼять — є через клік; не перевірено.
- (?) Як саме працює сейв при permadeath і що показує екран смерті.
