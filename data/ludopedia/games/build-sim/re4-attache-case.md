---
title: Resident Evil 4 (attaché case)
slug: re4-attache-case
aka: [RE4, Biohazard 4, Resident Evil 4 Remake, кейс Леона]
family: build-sim
also: []
klass: cursor
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: none
  goal: constraints
year: 2005
platforms: [GameCube, PS2, PC, Wii, PS3, Xbox 360, PS4, Xbox One, Switch, iOS, Android, Quest 2]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Resident_Evil_4", best: true, note: "сітка кейса, апгрейди місткості, ключові предмети й скарби окремо, торговець"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Resident_Evil_4_(2023_video_game)", note: "рімейк 2023: той самий кейс, крафт, торговець, міцність ножа"}
  - {kind: other, url: "https://www.gfinityesports.com/guides/resident-evil-4-remake-inventory-system", note: "рімейк: предмети горизонтально/вертикально, вкладки Keys і Treasures, гнізда скарбів"}
  - {kind: other, url: "https://gamertagmythras.com/blog/resident-evil-4/resident-evil-4-remake-attache-case-guide", note: "рімейк: розміри 7×12 → 9×13, обереги, кейси з бонусами"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Resident+Evil+4+attache+case+inventory", note: "пошук; кейс"}
stage: v1
coverage: 60
mechanics: [inventory, inventory-items, inventory-limit, multi-cell-size, piece-rotate-flip, polyomino-placement, drag-drop-piece, item-pickup, shop-catalog, shop-buyback, shop-window, round-currency, in-round-upgrades, hp-damage, +shaped-items, +bag-expansion, +item-combine, +attache-case-packing, +pickup-overflow-choice, +off-grid-tabs, +gem-socket-value, +case-charms]
proposes: ["+effect:discard", "+effect:combine", "+effect:socket", "+cond:fits", "+window:case-upgrade", "+ui:footprint-ghost", "+card:pickup-overflow-choice", "+card:off-grid-tabs", "+feature:auto-sort"]
author: opus
date: 2026-11-09
---

# Resident Evil 4 — кейс-сітка: прямокутні предмети, поворот на 90°, місткість купується в торговця — прообраз «inventory tetris»

## Суть
Шутер від третьої особи, у якому інвентар — **сітка attaché case**: зброя, патрони, гранати й ліки займають прямокутники клітин, їх можна переставляти й повертати. Місце — головний ресурс: щоб підібрати новий предмет, інколи треба переставити, використати чи викинути інший; місткість кейса купується в торговця. Відмінність від `backpack-hero` і `backpack-battles`: **сітка — лише сховище**, без сусідства, без бою всередині, без форм-поліміно (лише прямокутники (?)); бій, торговець і рівні — зовнішній шар, тут описаний одним абзацом.

## Поле і час
- Поле — прямокутна сітка кейса; розмір росте з апгрейдами (у рімейку — 7×12, 8×12, 8×13, 9×13 = 117 клітин). Розміри оригіналу — в «Непевне».
- Окремо від сітки — вкладки **ключових предметів** і **скарбів** (місця не займають).
- Час: у меню кейса гра на паузі (?) — `time: static` для цього шару; сама гра — real-time.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Кейс | zone | W×H | приймає предмети без накладання |
| Зброя (пістолет, дробовик, гвинтівка…) | object | прямокутник клітин, апгрейди | займає місце; рушниця — більше, ніж коробка патронів |
| Патрони | object | тип, кількість | займають малий прямокутник; стек одного типу (?) |
| Граната | object | вид | займає клітини |
| Трава (зелена, червона, жовта) | object | колір | змішується в лікувальну суміш |
| Спрей першої допомоги | object | — | лікує |
| Ключовий предмет | mark | — | вкладка Keys, місця не займає; у рімейку можна продати, коли непотрібний |
| Скарб | pickup | ціна | вкладка Treasures; продається; деякі мають гнізда під камені |
| Самоцвіт | pickup | колір/форма | вставляється в скарб → ціна вища |
| Торговець | neutral | асортимент | продає/купує, апгрейдить зброю, продає більший кейс |
| Ресурси і порох (рімейк) | object | вид | крафт патронів і предметів |
| Оберіг (рімейк) | mark | бонус | до трьох на кейс; пасивні бонуси |
| Варіант кейса (рімейк) | zone | бонус | змінює шанси дропу (порох, ресурси); сітку не змінює |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(pickup, item)` → ЯКЩО `fits(item, case_cells)` → ТО `place(item)` у вільне місце.
- КОЛИ `input(pickup, item)` → ЯКЩО `not fits(item, case_cells)` → ТО `window(inventory-window)`, `custom: «переставити, використати, викинути щось або лишити предмет»` (?).
- КОЛИ `input(drag, item, cell)` → ЯКЩО `fits(item, cells)` → ТО `move(item, cell)`; інакше `block`.
- КОЛИ `input(rotate, item)` → ТО `rotate(item, 90)` — горизонтально ↔ вертикально.
- КОЛИ `input(combine, herb_a, herb_b)` → ЯКЩО `custom: «пара є в таблиці сумішей»` → ТО `merge(herb_a, herb_b → mix)`; клітини звільняються.
- КОЛИ `input(use, healing)` → ТО `heal(player, n)`, `disappear_a`.
- КОЛИ `input(discard, item)` → ТО `custom: «предмет зникає з кейса»`.
- КОЛИ `contact(player, ammo)` → ЯКЩО `same(ammo, case_ammo, type)` → ТО `custom: «дозаповнити наявну коробку до максимуму»` (?).
- КОЛИ `input(buy, item)` у `shop-window` → ЯКЩО `has(player, pesetas)` and `fits(item, case_cells)` (?) → ТО `currency(-price)`, `place(item)`.
- КОЛИ `input(sell, item|treasure)` → ТО `currency(+value)`, `disappear_a`.
- КОЛИ `input(buy, case_upgrade)` → ЯКЩО `has(player, pesetas)` → ТО `currency(-price)`, `custom: «сітка кейса збільшується; предмети лишаються»`.
- КОЛИ `input(combine, treasure, gem)` → ЯКЩО `custom: «у скарбі є вільне гніздо під камінь»` → ТО `custom: «камінь у гніздо, ціна скарбу зростає»`.
- КОЛИ `input(craft, recipe)` (рімейк) → ЯКЩО `has(player, gunpowder|resources)` → ТО `take(player, ingredients)`, `give(player, product)`.
- Оберіг (рімейк): ЯКЩО `custom: «оберіг у слоті кейса»` → ТО `custom: «пасивний бонус»` (напр. Cute Bear — −1 порох у кожному крафті).
- Перемога/поразка — не в цьому шарі · Ціль шару: вмістити потрібне.

## Керування і ввід
- Меню кейса: курсор по сітці, схопити предмет → тягнути → кнопка повороту → покласти.
- Вибраний предмет: використати, поєднати з іншим, екіпірувати, викинути.
- У торговця — купити/продати/апгрейд, купівля більшого кейса.

## Вікна, меню, HUD
- `inventory-window` (кейс): сітка, `drag-ghost` / `+ui:footprint-ghost` (рамка місця), опис предмета, вкладки Keys і Treasures.
- `shop-window` (торговець): Buy · Sell · Tune Up · у рімейку — Trade (спінелі); `+window:case-upgrade`.
- Рімейк: Craft (вкладка кейса), Customize Case біля друкарської машинки — вибір кейса й оберегів (`custom-window`).
- `game-screen` — бій (HUD: `hp-bar`, патрони); `pause-menu`, `settings-window`, `save-slots` (друкарська машинка).
- Переходи: game-screen ↔ inventory-window · торговець → shop-window → inventory-window (куди покласти купуване).

## Фічі поза полем
- `save-slots` біля друкарських машинок; `difficulty-presets`; New Game+ (?).
- Рімейк: крафт, обереги з тиру, кілька кейсів з бонусами; `auto-sort` (?).

## Варіації й родичі
- Корпус: `save-room` (чистий пазл на цій механіці), `backpack-hero` / `backpack-battles` (сітка + сусідство + бій), `diablo2-inventory` (старіший прямокутний інвентар без повороту), `wilmots-warehouse` (склад-сітка).
- Осі «повороту»: нема (Diablo II) / 90° (RE4) / 90° + поліміно (Backpack Hero).
- Осі «місткості»: фіксована / купується (RE4) / росте за рівнем (Backpack Hero).
- Осі «поза сіткою»: усе в сітці / ключі й скарби у вкладках (RE4) / окремий пояс (Diablo II).

## Цікавинки для курсу
- Прямокутні предмети в сітці з поворотом на 90° і перевіркою накладання — 📎.
- Діалог переповнення: що робити, коли новий предмет не влазить — 🌱.
- Апгрейд сітки зі збереженням розкладки — 🌱.
- Суміші трав за таблицею (G+G, G+R, G+Y, G+R+Y (?)) — 🌱.
- Автосортування кейса (щільне пакування прямокутників) — 🥇 (bin packing).

## Мапа на каталог
- Є: `inventory` + `inventory-items` + `inventory-limit` · `multi-cell-size` · `piece-rotate-flip` (поворот 90°) · `polyomino-placement` (прямокутники як окремий випадок) · `drag-drop-piece` · `item-pickup` · `shop-catalog` + `shop-buyback` + `shop-window` · `round-currency` (песети) · `in-round-upgrades` (тюнінг зброї) · `hp-damage`.
- **Нема** → пропозиції карток:
  - `+pickup-overflow-choice` «Нема місця — обери, що викинути/використати» · entities/interact · 🌱.
  - `+off-grid-tabs` «Предмети поза сіткою (ключі, скарби)» · entities/state · 🌱.
  - `+gem-socket-value` «Камінь у гніздо скарбу підвищує ціну» · game-logic/economy · 🌱.
  - `+case-charms` «Пасивні бонуси-обереги, слоти на кейсі» · entities/state · 📎.
  - Повтори: `+shaped-items`, `+bag-expansion` (backpack-*), `+item-combine`, `+attache-case-packing` (save-room).

## Пропозиції до словників
- `+effect:discard` — викинути предмет з інвентаря (повтор з index/proposals).
- `+effect:combine` — два предмети стають третім за рецептом (повтор).
- `+effect:socket` — вставити камінь у гніздо предмета (повтор з GemCraft).
- `+cond:fits` — предмет вміщається у вільні клітини (у 🔥 як `fits(shape, cells)`; підтверджую).
- `+window:case-upgrade` — купівля більшої сітки інвентаря в торговця.
- `+ui:footprint-ghost` — рамка клітин, які займе предмет при відпусканні.
- `+feature:auto-sort` — автоматично переукласти інвентар.
- `+card:pickup-overflow-choice`, `+card:off-grid-tabs` — див. вище.

## Джерела
- ⭐ [Wikipedia: Resident Evil 4](https://en.wikipedia.org/wiki/Resident_Evil_4) — сітка кейса, апгрейди місця, ключі й скарби в окремому меню, торговець (продає, купує скарби, апгрейдить зброю).
- [Wikipedia: Resident Evil 4 (2023)](https://en.wikipedia.org/wiki/Resident_Evil_4_(2023_video_game)) — кейс як в оригіналі, крафт, торговець, міцність ножа.
- [Gfinity: RE4 Remake inventory](https://www.gfinityesports.com/guides/resident-evil-4-remake-inventory-system) — горизонтально/вертикально, «Tetris», вкладки Keys/Treasures, гнізда скарбів.
- [Gamer Tag Mythras: Attaché Case guide](https://gamertagmythras.com/blog/resident-evil-4/resident-evil-4-remake-attache-case-guide) — 7×12, 8×12, 8×13, 9×13 (117 клітин, 64 000 песет), 3 слоти оберегів, кейси з бонусами дропу.
- YouTube: пошук «Resident Evil 4 attache case inventory».

## Непевне
- (?) Розміри кейса в оригіналі 2005: за пошуковою видачею Resident Evil Wiki — мала 60 клітин, середня 7×11 (77), велика 8×12 (96), XL 8×15 (120); сама вікі віддала 402.
- (?) Що відбувається при підбиранні без місця (вибір «переставити/використати/лишити»); чи пауза в меню кейса.
- (?) Стеки патронів і дозаповнення коробок; чи купівля в торговця вимагає місця в кейсі.
- (?) Таблиця сумішей трав (з памʼяті); автосортування в рімейку.
- (?) Чи всі предмети — прямокутники (за джерелами — «горизонтально або вертикально»).
