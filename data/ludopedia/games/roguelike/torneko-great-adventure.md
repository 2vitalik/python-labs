---
title: "Torneko's Great Adventure: Mystery Dungeon"
slug: torneko-great-adventure
aka: ["Torneko no Daibōken: Fushigi no Dungeon", トルネコの大冒険, "Taloon's Great Adventure", Torneko 1]
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
year: 1993
platforms: [SNES (Super Famicom), Switch, Switch 2, PS5, PC, Xbox Series]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Torneko_no_Daib%C5%8Dken:_Fushigi_no_Dungeon", best: true, note: "перший Mystery Dungeon: магазин Торнеко як мета-прогрес, землетрус, прозора мапа, смерть, відмінності від Rogue, ремастер 2026"}
  - {kind: fandom, url: "https://mysterydungeonwiki.com/wiki/Meta:Torneko%27s_Great_Adventure:_Mystery_Dungeon", note: "Mystery Dungeon Wiki: огляд гри, підземелля, категорії предметів, штраф смерті"}
  - {kind: fandom, url: "https://mysterydungeonwiki.com/wiki/Torneko_1:Shop", note: "10 стадій магазину, банк Нене, склад, скільки речей можна взяти в похід"}
  - {kind: fandom, url: "https://mysterydungeonwiki.com/wiki/Torneko_1:Turn", note: "порядок ходів, землетруси 1534/1574/1614 дій, голод, регенерація, спавн кожні 64 ходи"}
  - {kind: fandom, url: "https://mysterydungeonwiki.com/wiki/Torneko_1:Magic_Dungeon", note: "99 поверхів, Joy Chest з 27-го, підйом назад, Safe"}
  - {kind: fandom, url: "https://mysterydungeonwiki.com/wiki/Torneko_1:Trial_Dungeon", note: "10 поверхів туди + підйом, петля 9↔10"}
  - {kind: fandom, url: "https://mysterydungeonwiki.com/wiki/Torneko_1:Unidentified_Item", note: "що невідоме за категоріями"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=torneko+no+daibouken+fushigi+no+dungeon+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [move-8dir, dungeon-generation, stairs-levels, hp-damage, hunger-clock, item-identification, inventory-items, item-pickup, round-currency, shop-between-levels, player-death, time-out, spawn-schedule, speed-per-type, +floor-turn-limit, +monster-house, +return-trip, +meta-shop-stages, +item-storage, +throw-item]
proposes: ["+trigger:earthquake", "+effect:drop_floor", "+feature:item-storage", "+feature:meta-shop-stages", "+window:storage-window"]
author: opus
date: 2026-11-09
---

# Torneko's Great Adventure — перший Mystery Dungeon: Rogue для консолі, де купець несе лут додому розширювати крамницю

## Суть
Chunsoft 1993, Super Famicom, лише Японія (ремастер Classic HD — 2026, світовий). Торнеко — купець з Dragon Quest IV — ходить у випадкові підземелля по лут і продає його у своїй крамниці; гроші розширюють крамницю (10 стадій), а з нею — склад і кількість речей, які можна взяти в похід. Повний опис формату серії — у [mystery-dungeon.md](mystery-dungeon.md); тут лише **відмінності першої гри**: землетрус замість вітру, обовʼязковий **підйом назад зі скарбом**, втрата половини грошей замість усього.

## Поле і час
- Як у [mystery-dungeon.md](mystery-dungeon.md): квадратна сітка, кімнати + коридори, 8 напрямків, прозора мапа поверху з точками (гравець, предмети, пастки, монстри) — нововведення порівняно з Rogue.
- Порядок ходу: Торнеко першим при вході на поверх, далі монстри в порядку появи; подвійна швидкість — бонусна дія перед звичайною; сповільнений монстр діє лише через хід.
- **Землетрус** рахується **діями**, не ходами: 1534 → 1574 → на 1614-й дії Торнеко провалюється на поверх нижче.
- Новий монстр зʼявляється кожні 64 ходи.
- Підземелля: Trial Dungeon (10 поверхів, один раз), Magic Dungeon (99 поверхів), More Magical Dungeon (пост-гейм, більше невідомих предметів).

## Сутності
Спільні з серією (монстри, крамар, пастки, зброя/щит, посохи, сувої, трава, будинки монстрів, гроші) — див. [mystery-dungeon.md](mystery-dungeon.md). Відмінні:

| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Торнеко | player | Lv, HP, сила, Belly %, атака/захист | скидається до Lv 1 у кожному поході |
| Joy Chest / Jewel Chest | pickup | ціль підземелля | Joy — з 27-го поверху Magic Dungeon; Jewel — на 10-му Trial; з ним треба **піднятися** нагору |
| Сейф (Safe) | pickup | з 10-го поверху | у сумці при смерті — гроші не діляться навпіл |
| Сувій виходу (Outside Scroll) | pickup | — | вихід з підземелля зі всім; заблокований, якщо несеш Joy Chest |
| Сувій покриття (Plating) | pickup | — | робить щит «нержавним» (зірочка в назві) |
| Нене і банк | neutral | баланс, поріг стадії | приймає гроші, продає непотрібне, веде склад (з 5-ї стадії) |
| Склад (Vault) | container | 10 / 20 / 40 / 60 місць за стадією | речі переживають поразку |
| Кільце | pickup | +N невідомий | пасивний ефект; Strength Ring ±3 |

## Правила (КОЛИ → ЯКЩО → ТО)
Тут — лише відмінності; базові правила ходу, кидання, ідентифікації — у [mystery-dungeon.md](mystery-dungeon.md).
- КОЛИ `counter(actions, ==, 1534)` або `1574` → ТО `custom: «попереджувальний поштовх»`; КОЛИ `counter(actions, ==, 1614)` → ТО `custom: «землетрус: провал на поверх нижче»` (на останньому поверсі Trial — той самий поверх, нова генерація).
- КОЛИ `timer(every 10 дій)` → ТО `counter(belly, −1)`; КОЛИ `counter(belly, ==, 0)` → ТО `hp(torneko, −1)` за кожну дію.
- КОЛИ `tick` → ТО `heal(torneko, maxHP × 0.02 ÷ 3)`.
- КОЛИ `timer(every 64 ходи)` → ТО `spawn_at(monster, random)`.
- КОЛИ `picked(torneko, joy_chest)` → ТО `custom: «сходи ведуть угору, Outside Scroll не діє»`; КОЛИ `reach(torneko, floor_1)` з скринею → ТО `win` (підземелля пройдене).
- КОЛИ `enter(torneko, pit_trap)` → ТО `next_level` навіть зі скринею — пастка відкидає назад.
- КОЛИ `custom: «Jewel Chest не знайдено на 10-му»` → ТО `custom: «петля 9 ↔ 10 до знахідки або поразки»`.
- КОЛИ `hp_zero(torneko)` → ЯКЩО `has(torneko, safe)` → ТО `custom: «гроші цілі»`; інакше `currency(−50 %)`; і `custom: «усі речі з собою втрачено, Lv 1, повернення додому»`.
- КОЛИ `input(read, outside_scroll)` або вихід з підземелля → ТО `custom: «усе зібране лишається»`, Нене пропонує склад, решта — на продаж.
- КОЛИ `counter(bank, >=, threshold)` (500 / 1000 / 3000 / 5000 / 10 000 / 20 000 / 50 000) → ТО `custom: «крамниця росте на стадію»`, `unlock(vault_slots, carry_in)`.
- КОЛИ `input(use, item)` → ЯКЩО `custom: «трава або сувій поза More Magical Dungeon»` → ТО `custom: «назва вже відома»` — невідомі лише кільця, посохи (заряди) та +N/прокляття зброї й щитів.
- Перемога: Joy Chest на поверхню (сюжет) · далі More Magical Dungeon. Поразка: HP = 0 (м'яка — штраф, не кінець гри). Рахунок: розмір крамниці.

## Керування і ввід
- Як у [mystery-dungeon.md](mystery-dungeon.md): хрестовина з 8 напрямками, кнопка удару, меню предметів (Use/Throw/Put/Equip/Name).
- Ідентифікований тип можна перейменувати з меню (крім мечів і щитів).

## Вікна, меню, HUD
- `game-screen`: поле, рядок статусу (поверх, Lv, HP, гроші), прозора `map-overlay` з точками, `message-log`.
- Хаб «замок / село / дім»: `custom-window` крамниці — записка Нене на ліжку показує баланс і скільки бракує до стадії; `storage-window` — склад.
- `inventory-window` — невідомі предмети жовтим, без опису.
- `end-screen` — непритомність, повернення додому.

## Фічі поза полем
- `meta-shop-stages`: 10 стадій крамниці як мета-прогрес (9-та — за Joy Chest, 10-та — за Mystery Box з More Magical Dungeon).
- `item-storage`: склад з 5-ї стадії; скільки речей узяти в похід (1–4) — теж за стадією.
- Невдачі в Trial Dungeon: після 21+ поразок король дає Metabble Sword і Shield — «м'яка» допомога.
- Сиквели: Torneko: The Last Hope (1999, PS1/GBA) — тимчасовий сейв у підземеллі, що стирається при продовженні; Torneko's Great Adventure 3 (2002, PS2/GBA).

## Варіації й родичі
- [Mystery Dungeon](mystery-dungeon.md) — уся серія (Shiren, PMD); Torneko — її прабатько. [Rogue](rogue.md) — джерело (Famitsu назвав гру «копією Rogue», але з голодом, землетрусом, мапою й музикою).
- Відмінності від Shiren: **таймер поверху** землетрус (провал униз — навіть корисно) vs вітер (винос = поразка); **штраф смерті** половина грошей і речі з собою vs усе; **ціль** скриня з підйомом назад vs дійти до кінця; **мета-прогрес** стадії крамниці vs склад села.

## Цікавинки для курсу
- Землетрус за лічильником **дій** з двома попередженнями — 🌱 (і чим «таймер униз» відрізняється від «таймера назовні»).
- Підйом зі скарбом: після підбору цілі сходи міняють напрямок, вихід-сувій блокується — 📎 (зміна правил рівня від стану інвентаря).
- Стадії крамниці за порогами банку, що відкривають склад і «ручну поклажу» — 🌱.
- Сейф у сумці скасовує штраф смерті — 🌱 (предмет-модифікатор правила поразки).

## Мапа на каталог
- Є: `move-8dir` · `dungeon-generation` · `stairs-levels` · `hp-damage` · `hunger-clock` · `item-identification` · `inventory-items` · `item-pickup` · `round-currency` · `shop-between-levels` (продаж через Нене) · `player-death` · `time-out` (землетрус) · `spawn-schedule` (кожні 64 ходи) · `speed-per-type`.
- **Нема** → пропозиції карток: `+floor-turn-limit` і `+monster-house`, `+throw-item` — уже з mystery-dungeon.md; нові:
  - `+return-trip` «Після цілі рівні треба пройти назад угору» · levels/progression · 📎.
  - `+meta-shop-stages` «Мета-прогрес стадіями за накопичені гроші» · game-logic/economy · 🌱 · слоти {thresholds, unlocks}.
  - `+item-storage` «Склад, що переживає поразку» · game-logic/save · 🌱.

## Пропозиції до словників
- `+trigger:earthquake` — лічильник дій поверху вичерпано (дитина `counter`).
- `+effect:drop_floor` — примусовий перехід на поверх нижче (протилежність `blown_out` з mystery-dungeon.md).
- `+feature:item-storage` (уже з mystery-dungeon.md — підтверджую) · `+feature:meta-shop-stages` · `+window:storage-window` (підтверджую).

## Джерела
- ⭐ [Wikipedia: Torneko no Daibōken](https://en.wikipedia.org/wiki/Torneko_no_Daib%C5%8Dken:_Fushigi_no_Dungeon) — магазин, голод, землетрус, мапа, смерть, відмінності від Rogue, сиквели, ремастер 2026.
- [MD Wiki: огляд гри](https://mysterydungeonwiki.com/wiki/Meta:Torneko%27s_Great_Adventure:_Mystery_Dungeon) — підземелля, категорії, штраф смерті.
- [MD Wiki: Shop](https://mysterydungeonwiki.com/wiki/Torneko_1:Shop) — стадії, пороги, склад, Сейф.
- [MD Wiki: Turn](https://mysterydungeonwiki.com/wiki/Torneko_1:Turn) — порядок ходів, землетруси, голод, регенерація, спавн.
- [MD Wiki: Magic Dungeon](https://mysterydungeonwiki.com/wiki/Torneko_1:Magic_Dungeon) · [Trial Dungeon](https://mysterydungeonwiki.com/wiki/Torneko_1:Trial_Dungeon) · [Unidentified Item](https://mysterydungeonwiki.com/wiki/Torneko_1:Unidentified_Item).
- [Wikipedia: Torneko: The Last Hope](https://en.wikipedia.org/wiki/Torneko:_The_Last_Hope) — сиквел.
- YouTube: [пошук](https://www.youtube.com/results?search_query=torneko+no+daibouken+fushigi+no+dungeon+gameplay).

## Непевне
- (?) Таблиця стадій на MD Wiki пошкоджена: місткість складу 10/20/40/60 і «1–4 речі в похід» — прочитання сторінки; MD Wiki: Magic Dungeon підтверджує «до 4 речей».
- (?) Штраф смерті: Wikipedia — «повертаєшся до останнього підземелля»; MD Wiki огляд — «гроші й речі втрачено»; сторінка Shop — «гроші навпіл без Сейфа». Записав комбінацію: речі з собою — втрачено, гроші — навпіл.
- (?) Попередження перед землетрусами — чи 1534/1574 саме поштовхи-попередження, сторінка прямо не каже.
- (?) Кидання предметів у першій грі — є (серійна механіка), але окремо не підтверджено.
