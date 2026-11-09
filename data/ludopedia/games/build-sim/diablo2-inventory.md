---
title: Diablo II (inventory)
slug: diablo2-inventory
aka: [Diablo 2, D2, Diablo II: Lord of Destruction, Diablo II: Resurrected, D2R]
family: build-sim
also: [roguelike]
klass: cursor
axes:
  field: square
  time: realtime
  opponent: none
  info: hidden
  random: runtime
  goal: none
year: 2000
platforms: [PC, Mac, PS4, PS5, Xbox One, Xbox Series, Switch]
links:
  - {kind: other, url: "https://classic.battle.net/diablo2exp/basics/", best: true, note: "Arreat Summit (офіційно, Blizzard): скриня-сховище, пояс, золото, підбирання й викидання"}
  - {kind: other, url: "https://classic.battle.net/diablo2exp/items/cube.shtml", note: "Horadric Cube: 2×2 у рюкзаку, сховище і трансмутація, рецепти"}
  - {kind: other, url: "https://classic.battle.net/diablo2exp/items/basics.shtml", note: "основи предметів: стеки, місце, якість, міцність, зникнення з землі"}
  - {kind: other, url: "https://classic.battle.net/diablo2exp/items/charms.shtml", note: "обереги діють лише з рюкзака"}
  - {kind: other, url: "https://classic.battle.net/diablo2exp/items/socketeditems.shtml", note: "гнізда: ліміти, самоцвіти, руни, рунні слова"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Diablo_II", note: "якості предметів, Horadric Cube, спільна скриня в Resurrected"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Diablo+II+inventory+management", note: "пошук; інвентар"}
stage: v1
coverage: 60
mechanics: [inventory, inventory-items, inventory-limit, multi-cell-size, drag-drop-piece, item-pickup, item-identification, timed-despawn, drop-on-death, shop-catalog, shop-buyback, shop-window, round-currency, save-game, hover-highlight, +shaped-items, +recipe-combine, +item-sockets, +passive-carry-item, +stack-inventory, +bag-in-bag, +equipment-slots, +shared-stash, +belt-columns, +item-rarity-tiers]
proposes: ["+effect:combine", "+effect:socket", "+effect:transmute", "+cond:in_backpack", "+role:container", "+window:stash-window", "+window:cube-window", "+ui:belt-slots", "+ui:paper-doll", "+card:bag-in-bag", "+card:item-sockets", "+card:belt-columns", "+feature:shared-stash"]
author: opus
date: 2026-11-09
---

# Diablo II — рюкзак-сітка з прямокутними предметами без повороту, пояс-колонки, скриня і куб-у-сітці з трансмутацією

## Суть
Екшн-RPG, де лут — головна нагорода, а місце в **сітці рюкзака** — головне обмеження: кожен предмет займає прямокутник клітин (каблучка — 1, обладунок — кілька), і гравець постійно вирішує, що нести до торговця, що в скриню, що лишити на землі. Поверх сітки — особливі зони: **пояс** (зілля в колонках з гарячими клавішами), **скриня** в місті, **Horadric Cube** — предмет 2×2, що сам є сіткою-контейнером і верстатом трансмутації, **обереги**, що діють лише з рюкзака. Відмінність від `backpack-hero` / `backpack-battles` і `re4-attache-case`: **нема повороту**, нема сусідства; зате є кілька сіток з різними правилами. Бій, рівні й класи — фон.

## Поле і час
- Кілька сіток: рюкзак (Backpack), екіпірування (слоти-ляльки), пояс (колонки × ряди), скриня (Stash) в кожному акті — та сама, внутрішність Cube, вікно торговця.
- Предмет — прямокутник клітин, орієнтація фіксована (?); розміри — у «Непевне».
- Час — реальний: інвентар **не ставить гру на паузу** в онлайні (?); предмети на землі зникають за таймером.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Рюкзак | zone | сітка W×H | приймає прямокутники без накладання |
| Слоти екіпірування | zone | голова, тіло, руки, каблучки, амулет, пояс, рукавиці, чоботи | один предмет відповідного типу; у LoD — 2 набори зброї (W) |
| Пояс | zone | 4 колонки; ряди — від типу пояса | зілля й сувої; гарячі клавіші колонок |
| Скриня (Stash) | container | сітка; ліміт золота | безпечне сховище, одне на всі акти й складності |
| Спільна скриня (D2R) | container | — | спільна між персонажами одного гравця |
| Horadric Cube | container | 2×2 у рюкзаку, своя сітка | сховище + Transmute за рецептом; куб у куб не кладеться |
| Предмет (зброя, обладунок…) | object | прямокутник, якість, міцність, гнізда | екіпірується, продається, ремонтується |
| Самоцвіт / руна / jewel | object | 1 клітина (?) | у гніздо предмета; 3 однакові в кубі → наступний рівень |
| Оберіг (charm) | object | малий/великий/grand | бонус лише в рюкзаку; у скрині й кубі — не діє |
| Зілля, ключі, стріли, болти, метальні | object | стек | однакові складаються в стек до максимуму |
| Золото | resource | ліміт на рівень персонажа | **не займає клітин**; на смерті втрачається частка |
| Предмет на курсорі | object | — | «ще одне місце»: лишається на курсорі навіть після виходу з гри |
| Предмет на землі | pickup | таймер | зникає за кілька хвилин; підняти й кинути — таймер скидається |
| Торговець | neutral | вітрина-сітка | купує/продає, ремонтує, перезаряджає |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(click, ground_item)` → ЯКЩО `fits(item, backpack_cells)` → ТО `pickup`, `place(item)` у вільне місце (?); інакше `block`, `message(no_room)` (?).
- КОЛИ `input(click, ground_potion)` → ЯКЩО `free(belt_slot)` → ТО `custom: «зілля одразу в пояс»`; інакше — у рюкзак.
- КОЛИ `input(shift_click, potion)` у рюкзаку → ЯКЩО `free(belt_column)` → ТО `move(potion, belt)`.
- КОЛИ `input(drag, item, cell)` → ЯКЩО `fits(item, cells)` → ТО `move(item, cell)`; ЯКЩО під ним рівно один предмет → `swap(item, other)` — інший переходить на курсор (?).
- КОЛИ `input(drag, item, stack)` → ЯКЩО `same(item, stack, kind)` → ТО `merge(item, stack → stack)`; надлишок — новий стек; стек не ділиться назад.
- КОЛИ `input(drag, item, equip_slot)` → ЯКЩО `custom: «тип і вимоги (сила, спритність, рівень) підходять»` → ТО `custom: «екіпірувати»`; інакше `block`.
- КОЛИ `input(drag, item, cube)` → ЯКЩО `fits(item, cube_cells)` and `custom: «item не куб»` → ТО `move(item, cube)`.
- КОЛИ `input(transmute)` → ЯКЩО `custom: «вміст куба = рецепт»` → ТО `merge(ingredients → product)`; напр. 3 однакові самоцвіти → самоцвіт вищого рівня, 3 руни → наступна руна, 3 магічні каблучки → магічний амулет.
- КОЛИ `input(drag, gem|rune|jewel, item)` → ЯКЩО `custom: «у предмета вільне гніздо»` → ТО `custom: «вставити назавжди»` (?); ЯКЩО `custom: «руни утворили рунне слово в правильному порядку»` → ТО `custom: «додаткові властивості»`.
- Обереги: ЯКЩО `custom: «оберіг у рюкзаку (не в скрині, не в кубі)»` → ТО `custom: «пасивний бонус»`.
- КОЛИ `input(click, gold)` → ТО `currency(+n)` до ліміту `10 000 × рівень`.
- КОЛИ `timer(lifetime)` → ЯКЩО `custom: «предмет лежить на землі»` → ТО `disappear_a` (ключі/зілля/стріли — 10 хв, рідкісні/сетові/унікальні — 30 хв).
- КОЛИ `died(player)` → ТО `currency(-level%)` (≤20 %); hardcore — `custom: «предмети втрачено»`.
- КОЛИ `input(sell, item)` у `shop-window` → ТО `currency(+value)`; `input(buy, item)` → ЯКЩО `fits(item, backpack_cells)` and `has(player, gold)` → ТО `place(item)`.
- КОЛИ `input(identify, item)` → ТО `reveal(item_properties)` (сувій, Cain; предмети в кубі Cain теж ідентифікує).
- КОЛИ `input(swap_weapons)` (W, LoD) → ТО `swap(weapon_set_1, weapon_set_2)`.
- Мета шару: нема; тиск — обмежене місце проти постійного луту.

## Керування і ввід
- Миша: клік по предмету — взяти на курсор; клік по клітині — покласти; ПКМ — використати/відкрити куб.
- Shift+клік по зіллю — у пояс; цифрові клавіші — колонки пояса (?); `~` — розгорнути пояс; Alt — підсвітити предмети на землі; W — набір зброї (LoD).
- Торговець: ПКМ — купити, Shift+ПКМ по сувою/ключу — дозаповнити книгу/стек.

## Вікна, меню, HUD
- `inventory-window`: рюкзак + `+ui:paper-doll` (слоти-лялька), золото, `tooltip` предмета (якість кольором, міцність, вимоги).
- `+window:stash-window` (скриня), `+window:cube-window` (сітка куба + кнопка Transmute), `shop-window` (вітрина-сітка торговця, ремонт).
- HUD `game-screen`: `+ui:belt-slots` (4 колонки), `hp-bar`, `energy-bar` (мана), `skill-bar`, підписи предметів на землі (Alt).
- `main-menu`, `character-select`, `pause-menu` (лише одиночна гра (?)), `settings-window`.
- Переходи: game-screen ↔ inventory-window; скриня/торговець відкривають свою сітку поруч з рюкзаком; ПКМ по кубу → cube-window.

## Фічі поза полем
- `save-game` (персонаж зберігає інвентар), `mode-hardcore`, `difficulty-presets` (Normal/Nightmare/Hell — більше гнізд у Hell), мультиплеєр Battle.net і торгівля.
- D2R: `+feature:shared-stash`; простіша ідентифікація (?).

## Варіації й родичі
- Корпус: `re4-attache-case` (сітка + поворот), `backpack-hero` / `backpack-battles` (форми + сусідство), `save-room` (пакування як пазл), `wilmots-warehouse`.
- Осі «кілька сіток»: одна (RE4) / рюкзак + пояс + скриня + куб (Diablo II).
- Осі «контейнер»: нема / предмет-сітка всередині сітки (Cube; родичі — сумки Backpack Battles, рюкзаки Minecraft-модів).
- Осі «ефект з інвентаря»: лише екіпіроване діє / несене теж діє (обереги D2) / сусідство (Backpack Hero).

## Цікавинки для курсу
- Прямокутні предмети в сітці + перша вільна позиція при підбиранні — 📎.
- Обмін «покласти на інший предмет → той на курсор» — 🌱.
- Стеки з максимумом і переповненням у новий стек — 🌱.
- Куб: контейнер-сітка всередині сітки + рецепти трансмутації як таблиця даних — 🥉.
- Гнізда й рунні слова (порядок вставки має значення) — 📎.
- Обереги: бонус лише з певної зони — 🌱.

## Мапа на каталог
- Є: `inventory` + `inventory-items` + `inventory-limit` · `multi-cell-size` · `drag-drop-piece` · `item-pickup` · `item-identification` · `timed-despawn` (лут на землі) · `drop-on-death` (золото) · `shop-catalog` + `shop-buyback` + `shop-window` · `round-currency` · `save-game` · `hover-highlight`.
- **Нема** → пропозиції карток:
  - `+bag-in-bag` «Предмет-контейнер зі своєю сіткою» · entities/state · 🥉.
  - `+item-sockets` «Гнізда й вставки, порядок дає бонус» · entities/state · 📎.
  - `+belt-columns` «Пояс-колонки з гарячими клавішами й автозаповненням» · interface/input · 🌱.
  - `+equipment-slots` «Лялька-слоти за типом предмета» · entities/state · 🌱.
  - `+shared-stash` «Сховище між персонажами» · game-logic/save · 🌱.
  - `+item-rarity-tiers` «Якість предмета: normal → unique, колір назви» · entities/state · 📎.
  - Повтори: `+recipe-combine` (backpack-battles), `+passive-carry-item`, `+stack-inventory` (Dizzy), `+shaped-items`.

## Пропозиції до словників
- `+effect:combine` (повтор) — інгредієнти → продукт; `+effect:transmute` — рецепт куба (повтор з Terraria).
- `+effect:socket` — вставити самоцвіт/руну в гніздо (повтор з GemCraft).
- `+cond:in_backpack` — предмет лежить у певній зоні інвентаря (умова дії оберега).
- `+role:container` — підтверджую (Cube, Stash).
- `+window:stash-window`, `+window:cube-window` — сітки-сховища поруч з рюкзаком.
- `+ui:belt-slots`, `+ui:paper-doll` — пояс з колонками; лялька екіпірування.
- `+feature:shared-stash`; `+card:bag-in-bag`, `+card:item-sockets`, `+card:belt-columns`.

## Джерела
- ⭐ [Arreat Summit: Basics](https://classic.battle.net/diablo2exp/basics/) — скриня в кожному акті (та сама), пояс 4 слоти + ряди, автозілля в пояс, Shift+клік, золото без місця, ліміти золота, зникнення предметів.
- [Arreat Summit: Horadric Cube](https://classic.battle.net/diablo2exp/items/cube.shtml) — 2×2 у рюкзаку, сховище, Transmute, рецепти самоцвітів/рун/гнізд/перекидання.
- [Arreat Summit: Item Basics](https://classic.battle.net/diablo2exp/items/basics.shtml) — стеки, предмет на курсорі як додаткове місце, якості, міцність, таймери зникнення.
- [Arreat Summit: Charms](https://classic.battle.net/diablo2exp/items/charms.shtml) — діють лише в рюкзаку; три розміри.
- [Arreat Summit: Socketed Items](https://classic.battle.net/diablo2exp/items/socketeditems.shtml) — броня ≤4, зброя ≤6 гнізд; рунні слова.
- [Wikipedia: Diablo II](https://en.wikipedia.org/wiki/Diablo_II) — п'ять якостей, Horadric Cube, спільна скриня в Resurrected.
- YouTube: пошук «Diablo II inventory management».

## Непевне
- (?) Розмір рюкзака 10×4, скрині 6×4 (класика) / 6×8 (LoD) / більша в D2R, сітка куба 3×4 — з памʼяті; Arreat Summit розмірів не дає, WebSearch вичерпано.
- (?) Розміри предметів (каблучка 1×1, рукавиці 2×2, обладунок 2×3, древкова 2×4, оберіг 1×1/1×2/1×3) — з памʼяті.
- (?) Правило автоматичного розміщення при підбиранні (яка клітина перша) і повідомлення «нема місця».
- (?) Обмін предмета з курсором при скиданні на зайняте; відсутність повороту — з памʼяті.
- (?) Пауза: одиночна гра ставиться на паузу лише меню Esc, не інвентарем.
- (?) Незнімність вставлених самоцвітів/рун (в оригіналі; у LoD є рецепт куба — не перевірено).
