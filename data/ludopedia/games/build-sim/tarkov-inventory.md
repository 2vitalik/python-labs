---
title: Escape from Tarkov (inventory)
slug: tarkov-inventory
aka: [EFT, Tarkov, Побег из Таркова]
family: build-sim
also: []
klass: cursor
axes:
  field: square
  time: realtime
  opponent: online
  info: hidden
  random: runtime
  goal: state
year: 2017
platforms: [PC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Escape_from_Tarkov", best: true, note: "сітковий інвентар, форма залежить від розгрузки й рюкзака; захищений контейнер; втрата всього при смерті; страхування; схрон, барахолка, евакуація"}
  - {kind: other, url: "https://wikiwiki.jp/eft/%E5%88%9D%E5%BF%83%E8%80%85%E3%82%AC%E3%82%A4%E3%83%89", note: "EFT JPN Wiki, гайд новачка: слоти, що не губляться, сортувальний стіл, сумка-в-сумці ≤7, складання зброї"}
  - {kind: other, url: "https://wikiwiki.jp/eft/%E3%83%9D%E3%83%BC%E3%83%81", note: "захищені контейнери: Alpha 2×2 … Kappa 3×4, заборонені предмети"}
  - {kind: other, url: "https://wikiwiki.jp/eft/%E3%83%90%E3%83%83%E3%82%AF%E3%83%91%E3%83%83%E3%82%AF", note: "рюкзаки: місткість, «стиснення», вкладеність"}
  - {kind: other, url: "https://wikiwiki.jp/eft/%E3%82%BF%E3%82%AF%E3%83%86%E3%82%A3%E3%82%AB%E3%83%AB%E3%83%AA%E3%82%B0", note: "розгрузки: швидкі слоти, перезарядка з розгрузки, броньовані розгрузки"}
  - {kind: other, url: "https://wikiwiki.jp/eft/Item%20case", note: "Item case: 4×4 зовні, 8×8 всередині, чорний список кейсів"}
  - {kind: other, url: "https://wikiwiki.jp/eft/%E6%93%8D%E4%BD%9C%E3%81%AE%E8%AA%AC%E6%98%8E", note: "керування: R поворот, Ctrl/Alt/Shift-клік, поділ стеку, складання приклада, огляд, Del"}
  - {kind: other, url: "https://www.gamepressure.com/escape-from-tarkov/10-best-starting-tips/zfcf2d", note: "поради: захищений контейнер, страхування, Scav без втрат"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Escape+from+Tarkov+inventory+tetris", note: "пошук; inventory tetris"}
stage: v1
coverage: 60
mechanics: [inventory, inventory-items, inventory-limit, multi-cell-size, piece-rotate-flip, drag-drop-piece, item-pickup, item-identification, drop-on-death, shop-catalog, shop-window, round-currency, hover-highlight, online-multiplayer, save-game, +equipment-slots, +grid-from-equipment, +sub-grid-layout, +bag-in-bag, +bigger-inside, +container-whitelist, +secure-container, +typed-slots, +insurance-return, +attachment-resize, +stack-inventory, +sorting-table, +auto-sort-pin, +weight-encumbrance, +quick-slots, +reload-from-rig, +found-in-raid-tag, +extraction-zone, +stash-upgrade, +player-market]
proposes: ["+cond:in_backpack", "+cond:allowed_in", "+effect:discard", "+effect:fold", "+effect:insure", "+trigger:extracted", "+window:stash-window", "+window:loot-window", "+window:flea-market", "+window:insurance-window", "+ui:paper-doll", "+ui:weight-readout", "+ui:quick-slots", "+feature:progress-wipe", "+card:grid-from-equipment", "+card:bigger-inside", "+card:secure-container", "+card:attachment-resize", "+card:sorting-table"]
author: opus
date: 2026-11-09
---

# Escape from Tarkov (інвентар) — сітку несеш на собі: її форму дають розгрузка й рюкзак, кейси «більші всередині», а смерть забирає все, крім захищеного контейнера

## Суть
Шутер-«екстракшн»: гравець іде в рейд зі спорядженням, збирає лут і мусить дійти до зони евакуації в межах часу; загинув — втратив усе, що ніс. Тут описано лише **сітковий шар**: інвентар складається з кількох сіток, і їхню форму задає саме спорядження — розгрузка дає набір дрібних осередків, рюкзак — блоки клітин, а кейси й рюкзаки в схроні мають **внутрішню сітку більшу за зовнішній розмір**. Відмінність від `diablo2-inventory` і `re4-attache-case`: сітка **не дана грою, а надягнута** (зняв рюкзак — зникла частина інвентаря), предмет **змінює розмір** від обвісу й складеного приклада, а **захищений контейнер** — єдина сітка, що переживає смерть. Стрілянина, карти й квести — фон.

## Поле і час
- Інвентар персонажа = слоти екіпірування + сітки: кишені, розгрузка (tactical rig), рюкзак, захищений контейнер (pouch), спецслоти (3).
- Сітка кожного контейнера — набір прямокутних підсіток (форма — у даних предмета); предмет займає прямокутник W×H і повертається на 90°.
- Схрон (stash) — велика прямокутна сітка поза рейдом; росте апгрейдами в Хованці; стартовий розмір залежить від видання, кінцевий — однаковий.
- Час: у рейді інвентар **не ставить гру на паузу** (вагу й шум перевіряє світ); у схроні — поза часом.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Слоти екіпірування | zone | голова, обличчя, навушники, броня, розгрузка, рюкзак, контейнер, пов'язка, ніж, зброя | один предмет відповідного типу |
| Кишені | zone | малі осередки (?) | завжди є; гранати й магазини для швидкого доступу |
| Розгрузка (rig) | container | зовнішній розмір, підсітки | сітка з'являється, коли надягнута; швидкі слоти й перезарядка звідси |
| Броньована розгрузка | container | клас броні, підсітки | займає слот розгрузки й не сумісна з бронежилетом |
| Рюкзак | container | місткість, підсітки, штраф руху | надягнутий — нова сітка; порожній можна покласти в інший |
| Захищений контейнер | container | Alpha 2×2 · Beta 3×2 · Epsilon 4×2 · Gamma 3×3 · Theta 4×2+1×2 · Kappa 3×4 | вміст не губиться при смерті; у рейді не знімається; не продається |
| Спецслот ×3 | zone | лише [SPEC] (+ сигнальні ракети, паракорд, хірургічні набори) | не губиться при смерті |
| Кейс (Item case, Junk box, Weapon case, magazine case…) | container | зовнішній 4×4 → внутрішній 8×8 (Item case); Junk box — 14×14 | «більший всередині»; білий/чорний список вмісту |
| Предмет | object | W×H, вага, ціна, FIR-мітка | займає прямокутник; повертається; продається |
| Зброя | object | розмір від обвісу | приклад, глушник, магазин міняють розмір; приклад складається |
| Стек (набої, гроші) | object | кількість | ділиться й зливається |
| Невідомий предмет | object | силует | до огляду показано лише силует |
| Тіло / контейнер на рівні | container | сітка | відкривається поруч з інвентарем для обшуку |
| Сортувальний стіл | zone | без ліміту | тимчасовий буфер схрону |
| Схрон | container | сітка за виданням + апгрейди | постійне сховище між рейдами |
| Торговець / Барахолка | neutral | асортимент, рівень лояльності | купує/продає; барахолка — між гравцями |
| Страховик | neutral | ціна | повертає застраховане, якщо ніхто не виніс |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag, item, cell)` → ЯКЩО `fits(item, cells)` → ТО `move(item, cell)`; інакше `block`.
- КОЛИ `input(rotate, item)` під час drag → ЯКЩО `fits(item_rotated, cells)` → ТО `rotate(item, 90)`.
- КОЛИ `input(ctrl_click, item)` → ЯКЩО `custom: «є вільне місце в іншій відкритій сітці (схрон / обшук / інвентар)»` → ТО `move(item, first_free)`.
- КОЛИ `input(alt_click, item)` → ЯКЩО `free(equip_slot)` → ТО `custom: «екіпірувати»`.
- КОЛИ `custom: «рюкзак/розгрузку надягнуто»` → ТО `custom: «додається сітка з підсітками цього предмета»`; знято → його сітка їде разом із вмістом як один предмет.
- КОЛИ `input(drag, backpack, other_backpack)` → ЯКЩО `custom: «вкладений не більший; ланцюг ≤ 7 сумок у схроні»` → ТО `move(backpack, inside)`; у рейді сумки від 30 клітин (Tri-Zip і більші) в надягнуту не кладуться.
- КОЛИ `input(drag, item, case)` → ЯКЩО `custom: «предмет дозволений списком кейса»` → ТО `move(item, case_grid)`; Item case приймає все, крім інших кейсів.
- КОЛИ `input(drag, item, secure_container)` → ЯКЩО `not custom: «зброя, магазини, гранати, набої, шоломи, ПНБ, більшість кейсів, рюкзаки з контейнерами»` → ТО `move(item, secure_container)`; інакше `block`.
- КОЛИ `input(drag, item, special_slot)` → ЯКЩО `custom: «предмет з міткою [SPEC] або винятки»` → ТО `move(item, special_slot)`; інакше `block`.
- КОЛИ `input(fold, stock)` → ТО `custom: «зброя коротшає на клітину»`; КОЛИ `input(detach, part)` → ТО `custom: «розмір зброї зменшується, частина стає окремим предметом»`.
- КОЛИ `input(ctrl_drag, stack)` → ТО `split(stack)`; КОЛИ `input(drag, stack, same_stack)` → ЯКЩО `same(a, b, kind)` → ТО `merge(a, b → stack)`.
- КОЛИ `input(drag, ammo|magazine, weapon)` → ТО `custom: «зарядити»`; у руках — зі звуком, за спиною — тихо.
- КОЛИ `input(reload)` → ЯКЩО `custom: «у розгрузці/кишенях є магазин і місце для знятого»` → ТО `swap(mag_in_weapon, mag_in_rig)`; нема місця → `custom: «знятий магазин падає на землю»`; осліплений — падає завжди.
- КОЛИ `input(middle_click, unknown_item)` → ТО `custom: «огляд за час»`, `reveal(item)`.
- КОЛИ `input(del, item)` → ЯКЩО `mode(raid)` → ТО `custom: «викинути на землю»`; ЯКЩО `mode(stash)` → ТО `disappear` назавжди.
- КОЛИ `tick` → ЯКЩО `counter(weight, >, limit)` → ТО `speed(player, -k)`, `custom: «витрата витривалості росте; на межі — не бігти»`.
- КОЛИ `reach(player, extraction_zone)` → ЯКЩО `timer(<, raid_limit)` → ТО `custom: «усе несене переходить у схрон»`, `custom: «зібране в рейді отримує мітку FIR»`.
- КОЛИ `died(player)` → ТО `custom: «усе, крім контейнера, спецслотів, пов'язки й ножа, лишається на тілі»`; вміст контейнера повертається без FIR.
- КОЛИ `custom: «рейд закінчено»` → ЯКЩО `state(item, insured)` and `custom: «ніхто не виніс предмет із рейду; статус не MIA»` → ТО `give(player, item)` (через страховика).
- КОЛИ `custom: «таймер рейду вийшов (MIA)»` → ТО `custom: «як смерть; страховка не повертає»`.
- КОЛИ `input(shift_click, item)` у схроні → ТО `move(item, sorting_table)`; КОЛИ `input(close, sorting_table)` → ЯКЩО `not fits(items, stash)` → ТО `block`.
- КОЛИ `input(auto_sort, stash)` → ТО `custom: «переставити все, крім закріплених (P)»`.
- КОЛИ `input(sell, item)` → ЯКЩО `custom: «торговець приймає; на барахолку — лише FIR»` → ТО `currency(+price)`, `disappear`.
- Мета шару: вивезти з рейду більше цінності на клітину, ніж приніс; поразка — смерть або MIA (втрата спорядження).

## Керування і ввід
- Tab — інвентар; drag-and-drop, R під час перетягування — поворот; подвійний клік — подробиці предмета.
- Ctrl+клік — швидке перенесення між відкритими сітками; Alt+клік — надягнути; Shift+клік — на сортувальний стіл; Ctrl+drag — поділ стеку.
- Середня кнопка — огляд невідомого; L+Alt — скласти/розкласти приклад; Del — викинути.
- 4–0 — швидкі слоти з розгрузки/кишень/спецслотів; утримання слота аптечки + колесо — вибір частини тіла.

## Вікна, меню, HUD
- `inventory-window`: `+ui:paper-doll` (слоти) + сітки кишень, розгрузки, рюкзака, контейнера; `tooltip` (розмір, вага, ціна, FIR); `+ui:weight-readout`.
- `+window:loot-window` — обшук тіла чи контейнера рівня поруч з інвентарем; предмети відкриваються поступово (`hidden` до пошуку (?)).
- `+window:stash-window` — схрон + сортувальний стіл, кнопка автосортування, закріплення предметів.
- `shop-window` (торговці), `+window:flea-market` (оголошення гравців), `+window:insurance-window`, вікна кейсів (сітка всередині сітки).
- HUD рейду: `+ui:quick-slots` (4–0), `hp-bar` частин тіла, витривалість.
- Переходи: `main-menu` → схрон/торговці/Хованка → вибір карти → `game-screen` рейду ↔ `inventory-window` → `end-screen` (вижив / загинув / MIA) → схрон.

## Фічі поза полем
- `save-game` (схрон і прогрес на сервері), `online-multiplayer`, `+feature:progress-wipe` (періодичне скидання прогресу; стартовий розмір схрону і контейнер — за виданням).
- Хованка: апгрейди схрону, крафт (крафтоване — FIR).
- Режим PvE та Scav-рейди (Scav — чуже спорядження, без втрат) (?).

## Варіації й родичі
- Корпус: `diablo2-inventory` (кілька сіток, без повороту), `re4-attache-case` (сітка + поворот, апгрейд місткості), `backpack-hero` / `backpack-battles` (сусідство), `dredge` (типізовані слоти), `save-room` / `wilmots-warehouse` (пакування).
- Осі «звідки сітка»: дана грою (RE4) / купується апгрейдом (RE4, Diablo-скриня) / **надягається предметом** (Tarkov) .
- Осі «контейнер»: нема / предмет-сітка (Horadric Cube) / **більший усередині + білий/чорний список** (Tarkov-кейси).
- Осі «смерть»: нічого не губиш / губиш золото (Diablo II) / **губиш усе, крім захищеної сітки** (Tarkov).
- Родичі-«екстракшн»: Arena Breakout, Dark and Darker, Marathon (?) — та сама схема контейнера.

## Цікавинки для курсу
- Сітка з підсіток, що з'являється при екіпіруванні предмета — 🥉.
- Кейс «більший усередині» + білий/чорний список вмісту + ліміт вкладеності — 🥉.
- Захищений контейнер: одна сітка переживає смерть, решта — на тіло — 📎.
- Розмір предмета від складових (приклад, обвіс) — 🥉.
- Сортувальний стіл як безлімітний буфер, що не закривається, поки нема місця — 🌱.
- Автосортування з закріпленими предметами (bin packing з фіксованими клітинами) — 🥇.
- Страховка: повернення, якщо інший гравець не виніс предмет — 📎.

## Мапа на каталог
- Є: `inventory` + `inventory-items` + `inventory-limit` · `multi-cell-size` · `piece-rotate-flip` (R) · `drag-drop-piece` · `item-pickup` · `item-identification` (силует до огляду) · `drop-on-death` (усе лишається на тілі) · `shop-catalog` + `shop-window` · `round-currency` (рублі) · `hover-highlight` · `online-multiplayer` · `save-game`.
- **Нема** → пропозиції карток:
  - `+grid-from-equipment` «Сітка інвентаря дається надягнутим предметом» · entities/state · 🥉.
  - `+sub-grid-layout` «Сітка контейнера з окремих підсіток» · entities/state · 📎.
  - `+bigger-inside` «Внутрішня сітка більша за зовнішній розмір» · entities/state · 📎.
  - `+container-whitelist` «Контейнер приймає лише дозволене» · entities/legality · 🌱.
  - `+secure-container` «Сітка, що переживає смерть» · entities/death · 🌱.
  - `+insurance-return` «Повернення застрахованого, якщо не винесли» · game-logic/economy · 📎.
  - `+attachment-resize` «Розмір предмета від складових» · entities/state · 🥉.
  - `+sorting-table` «Безлімітний тимчасовий буфер» · interface/input · 🌱.
  - `+auto-sort-pin` «Автосортування із закріпленими предметами» · interface/input · 🥇.
  - `+weight-encumbrance` «Вага сповільнює» · entities/state · 🌱.
  - `+quick-slots` «Швидкі слоти 4–0 з певних контейнерів» · interface/input · 🌱.
  - `+reload-from-rig` «Перезарядка лише з певних сіток» · entities/state · 📎.
  - `+found-in-raid-tag` «Мітка походження предмета» · entities/state · 🌱.
  - `+extraction-zone` «Вийти через зону евакуації до таймера» · game-logic/win · 🌱.
  - `+stash-upgrade` «Схрон росте апгрейдами» · game-logic/economy · 🌱.
  - `+player-market` «Барахолка між гравцями» · game-logic/economy · 🥈.
  - Повтори: `+equipment-slots`, `+bag-in-bag`, `+typed-slots`, `+stack-inventory`.

## Пропозиції до словників
- `+cond:in_backpack` (повтор з `diablo2-inventory`) — предмет у певній зоні інвентаря; тут — у захищеному контейнері/спецслоті, тому не губиться.
- `+cond:allowed_in` — предмет дозволений у цьому контейнері (білий/чорний список).
- `+effect:discard` (повтор) — викинути: у рейді на землю, у схроні — знищити.
- `+effect:fold` — змінити розмір предмета (складений приклад).
- `+effect:insure` — позначити предмет застрахованим.
- `+trigger:extracted` — гравець вийшов через зону евакуації (кінець рейду з перемогою).
- `+window:stash-window` (повтор), `+window:loot-window`, `+window:flea-market`, `+window:insurance-window`.
- `+ui:paper-doll` (повтор), `+ui:weight-readout`, `+ui:quick-slots`.
- `+feature:progress-wipe` — періодичне скидання прогресу всіх гравців.
- `+card:grid-from-equipment`, `+card:bigger-inside`, `+card:secure-container`, `+card:attachment-resize`, `+card:sorting-table`.

## Джерела
- ⭐ [Wikipedia: Escape from Tarkov](https://en.wikipedia.org/wiki/Escape_from_Tarkov) — інвентар «grid-based», розмір і форма від розгрузок і рюкзаків; вага → швидкість і витривалість; захищений контейнер; втрата всього при смерті; страхування; схрон, торговці, барахолка; евакуація в межах часу; beta 2017, 1.0 — 15.11.2025.
- [EFT JPN Wiki: гайд новачка](https://wikiwiki.jp/eft/%E5%88%9D%E5%BF%83%E8%80%85%E3%82%AC%E3%82%A4%E3%83%89) — слоти, що не губляться, спецслоти, FIR, страхування й MIA, сортувальний стіл, автосортування з P, сумка-в-сумці ≤7, розбирання зброї до висоти 1.
- [EFT JPN Wiki: Pouch](https://wikiwiki.jp/eft/%E3%83%9D%E3%83%BC%E3%83%81) — розміри контейнерів, заборонені предмети, не знімається в рейді.
- [EFT JPN Wiki: Backpack](https://wikiwiki.jp/eft/%E3%83%90%E3%83%83%E3%82%AF%E3%83%91%E3%83%83%E3%82%AF) — місткість і «стиснення», ліміт 7 у схроні, 30+ клітин у рейді.
- [EFT JPN Wiki: Tactical rig](https://wikiwiki.jp/eft/%E3%82%BF%E3%82%AF%E3%83%86%E3%82%A3%E3%82%AB%E3%83%AB%E3%83%AA%E3%82%B0) — швидкі слоти, перезарядка з розгрузки, падіння магазина.
- [EFT JPN Wiki: Item case](https://wikiwiki.jp/eft/Item%20case) — 4×4 → 8×8, чорний список кейсів.
- [EFT JPN Wiki: керування](https://wikiwiki.jp/eft/%E6%93%8D%E4%BD%9C%E3%81%AE%E8%AA%AC%E6%98%8E) — R, Ctrl/Alt/Shift-клік, поділ стеку, приклад, огляд, Del, швидкі слоти.
- [Gamepressure: 10 tips](https://www.gamepressure.com/escape-from-tarkov/10-best-starting-tips/zfcf2d) — контейнер, страхування, Scav не втрачає нічого.
- YouTube: пошук «Escape from Tarkov inventory tetris».

## Непевне
- (?) Розмір кишень (4 осередки 1×1) — лише з пошукового резюме старого гайда.
- (?) Розміри схрону за виданнями й апгрейдами — не відкрито.
- (?) Точні підсітки розгрузок і рюкзаків — у вікі лише картинками; Junk box 14×14 і T H I C C case — з пошукових резюме.
- (?) Поступове «пошукове» відкриття вмісту контейнерів і тіл — з памʼяті.
- (?) Набір дозволених у контейнері предметів змінювався між версіями (ліки дозволили після релізу; у PvE — інакше).
- (?) Родичі Arena Breakout, Dark and Darker, Marathon — з памʼяті, не перевірено.
- Черга: рік «2017 / 2025» коректний — закрита бета 28.07.2017, 1.0 і Steam — 15.11.2025.
