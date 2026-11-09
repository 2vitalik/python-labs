---
title: Z.H.P. Unlosing Ranger VS Darkdeath Evilman
slug: zhp-unlosing-ranger
aka: [ZHP, Z.H.P., 絶対ヒーロー改造計画, Absolute Hero Modding Project]
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
year: 2010
platforms: [PSP, Switch, Windows]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Z.H.P._Unlosing_Ranger_VS_Darkdeath_Evilman", best: true, note: "рівень з 1-го в кожному підземеллі + Total Level, кидання ворогів, хаб, Body Modification, боси й зміна стилю, перевидання 2022"}
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/絶対ヒーロー改造計画", note: "人体改造 (сітка-тіло в «Темній клініці»), 5 слотів спорядження, травма, «спів» технік, знос і коваль, пресети спорядження"}
  - {kind: other, url: "https://www.taptap.cn/app/767813/all-info", note: "опис Windows-версії: покроковий роглайк, Total Level, сітка Body Modification"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=ZHP+Unlosing+Ranger+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 40
mechanics: [dungeon-generation, stairs-levels, hp-damage, inventory, inventory-limit, item-pickup, player-death, teleport-random-exit, +throw-enemy, +throw-item, +carry-object, +level-reset-on-entry, +total-level-meta, +run-meta-carry, +trauma-weakness, +body-mod-grid, +equipment-slots, +equipment-appearance, +equipment-durability, +enemy-trait-parts, +chant-charge, +combo-technique, +equip-loadout, +bag-expansion, +town-hub]
proposes: ["+effect:bank_level(a, total)", "+effect:add_weakness(a, cause)", "+effect:charge(technique)", "+window:body-mod-grid", "+feature:loadout-presets"]
author: opus
date: 2026-11-09
---

# Z.H.P. Unlosing Ranger VS Darkdeath Evilman — роглайк, де кожен забіг, навіть програний, додає рівні до «Total Level»

## Суть
Пародійна токусацу-гра Nippon Ichi (PSP, 2010): випадковий перехожий отримує костюм непереможного рейнджера й мусить підготуватись до реваншу з Darkdeath Evilman. Підземелля — покроковий «Mystery Dungeon»: при вході **рівень падає до 1**, а коли підземелля пройдено **або програно**, досягнутий рівень **додається до Total Level**, який піднімає базові стати. Тому поразка теж прогрес; поразка ще й залишає **травму** — слабкість до того, що тебе вбило. Другий сітковий шар — **Body Modification**: у клініці гравець вставляє частини спорядження в панелі сітки у формі людського тіла.

## Поле і час
- Квадратна сітка поверхів, підземелля багаторівневі й генеруються щоразу; типи — завод, море тощо, у кожного свої трюки (гармати, що вистрілюють героя у випадкову клітину поверху).
- Покроково: дія героя = хід. Кінець розділу — бос у покроковому RPG-бою на окремому екрані, стиль графіки якого «старіє» сюжетом від раннього Dragon Quest до Super Robot Wars.
- Поза підземеллям — хаб на «Зворотній Землі»; поверх сітки підземелля — друга сітка, тіло героя для модифікацій.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой (Unlosing Ranger) | player | рівень забігу (з 1), Total Level → базові стати, 5 слотів (голова, ліва й права руки, ноги, опція), травми | ходить, бʼється, піднімає й кидає ворогів і предмети, «співає» техніки |
| Ворог | enemy | вид, атаки | бʼється; частину не можна підняти |
| Частина спорядження | pickup | слот, здатність, знос; риси ворога, з якого випала | змінює вигляд і здатності; зношується від ужитку |
| Підсилювальна частина | pickup | — | ставиться на заповнену панель сітки тіла: + місткість сумки, + ефект спорядження |
| Панель сітки тіла | mark | порожня / заповнена | приймає частину; заповнена — основа для підсилювача |
| Гармата (трюк підземелля) | terrain | — | вистрілює героя у випадкову клітину поверху |
| Скриня | container | — | частини, предмети |
| Бос розділу | boss | фази (?) | окремий покроковий бій |
| Хаб: дім, коваль, космічна поліція, COSPATIO | zone | будівлі, змінні NPC | склад, ремонт і злиття, пресети спорядження, костюми |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `level_start` (вхід у підземелля) → ТО `custom: «рівень героя = 1»`.
- КОЛИ `level_end` (пройдено) або `hp_zero(hero)` → ТО `custom: «поточний рівень додається до Total Level»` → `custom: «базові стати ростуть»`.
- КОЛИ `hp_zero(hero)` → ТО `custom: «втрата всього, що ніс»` + `custom: «причина смерті стає травмою: наступного забігу слабший до цієї атаки»`; подолав травму → сильніший.
- КОЛИ `input(lift)` → ЯКЩО `in_range(hero, enemy|item, 1)` and `custom: «ціль можна підняти»` → ТО `carry(target)` (1 хід); з ношею можна ходити, але не бити звичайно.
- КОЛИ `input(throw, dir)` → ЯКЩО `state(hero, carrying)` → ТО `throw(target, dir)` на відстань.
- КОЛИ `died(enemy)` або `input(open, chest)` → ТО `custom: «може випасти частина»`; частина з ворога зберігає його риси.
- КОЛИ `custom: «спорядження вжито»` → ТО `custom: «знос»`; ремонт — у коваля.
- КОЛИ `input(chant, technique)` → ТО `custom: «1 хід на «спів», далі техніку можна застосувати будь-коли»`; деякі частини співають кілька технік разом → комбо-атака.
- КОЛИ `enter(hero, cannon)` → ТО `teleport(hero, random_cell)`.
- КОЛИ `input(install, part, panel)` у Темній клініці → ЯКЩО `free(panel)` → ТО `place(part)` + `custom: «базові стати ростуть»`.
- КОЛИ `input(install, booster, panel)` → ЯКЩО `occupied(panel, part)` → ТО `custom: «+місткість сумки / +ефект спорядження»`.
- КОЛИ `input(preset)` у підземеллі → ЯКЩО `custom: «відкрито космічну поліцію»` → ТО `custom: «миттєво змінити набір спорядження на збережений»`.
- КОЛИ `input(lunch)` у підземеллі → ЯКЩО `custom: «дім має обід»` → ТО `custom: «обід доставляють»` (?).
- Перемога: пройти сюжетні підземелля й перемогти Darkdeath Evilman. Поразка в підземеллі — не кінець гри, а повернення в хаб.

## Керування і ввід
- Кнопки PSP / геймпад: крок по сітці, удар, підняти/кинути, меню предметів і технік; техніки «співаються» заздалегідь, щоб застосувати в потрібний момент.
- У клініці — курсор по сітці-тілу: обрати панель → вставити частину / підсилювач.

## Вікна, меню, HUD
- `game-screen` підземелля: сітка поверху, рівень забігу, HP.
- `body-mod-grid` (Темна клініка) — сітка панелей у формі тіла, стати до/після.
- `inventory-window` + екран спорядження з 5 слотами; вигляд героя змінюється від частин.
- Хаб: дім (`custom-window` склад-скриня), коваль (ремонт, перефарбування, злиття однотипних), космічна поліція (пресети), COSPATIO (костюми).
- Окремий екран бою з босом (покроковий RPG-бій зі змінним графічним стилем).
- Переходи: хаб → підземелля → (кінець або смерть) → хаб з новим Total Level.

## Фічі поза полем
- `meta-progression`: Total Level + травми + сітка тіла + склад; «RPG, у яку можна зіграти 40 мільйонів разів».
- Будівлі хабу налаштовуються, кожна дає механіку, доступну в підземеллі; NPC-керівників можна міняти; склад розширюється, якщо давати дружині гроші на життя.
- Тема пісні змінює мелодію й слова залежно від поєднання вдягнених частин.
- Перевидання 2022: Switch (у збірці Prinny Presents NIS Classics Volume 2 з Makai Kingdom) і Windows.

## Варіації й родичі
- [mystery-dungeon](mystery-dungeon.md) — пряма основа формату підземелля; [azure-dreams](azure-dreams.md) — рівень героя теж скидається, але прогрес живе у фамільярах, а не в сумі рівнів.
- Кидання ворогів — фірмове для Nippon Ichi (Disgaea).
- Осі варіацій: **що дає програний забіг** (нічого / частину луту / рівні в загальну суму / слабкість-травму); **модифікація героя** (слоти / сітка-тіло з підсилювачами).

## Цікавинки для курсу
- Total Level: рівень кожного забігу, і програного, сумується в постійний бонус — 🌱.
- Травма від причини смерті: тег атаки → слабкість у наступному забігу — 📎.
- Підняти й кинути ворога (1 хід, з ношею не бʼєш) — 📎.
- Сітка-тіло: частини в панелі, підсилювачі лише на заповнені — 🥉 (якщо частини мають форму — 🥈).
- «Спів» техніки: заряд на хід, застосування пізніше, комбо з кількох — 📎.

## Мапа на каталог
- Є: `dungeon-generation` · `stairs-levels` · `hp-damage` · `inventory` + `inventory-limit` (місткість росте) · `item-pickup` · `player-death` · `teleport-random-exit` (гармата).
- **Нема** → пропозиції карток:
  - `+level-reset-on-entry` + `+total-level-meta` «Рівень з 1-го, сума рівнів забігів — постійний бонус» · entities/state · 🌱.
  - `+trauma-weakness` «Причина смерті → слабкість наступного забігу» · entities/state · 📎.
  - `+throw-enemy` + `+carry-object` «Підняти сусіда й кинути» · entities/interact · 📎.
  - `+body-mod-grid` «Сітка-тіло для частин і підсилювачів» · entities/state · 🥉.
  - `+equipment-slots` + `+equipment-appearance` + `+equipment-durability` + `+enemy-trait-parts` · entities/state · 📎.
  - `+chant-charge` + `+combo-technique` «Зарядити техніку на хід, застосувати пізніше» · entities/combat · 📎.
  - `+equip-loadout` · `+bag-expansion` · `+town-hub` — хабові.

## Пропозиції до словників
- `+effect:bank_level(a, total)` — перенести рівень забігу в постійну суму.
- `+effect:add_weakness(a, cause)` — додати слабкість до типу атаки, що вбила.
- `+effect:charge(technique)` — витратити хід на підготовку дії, яку можна виконати пізніше.
- `+window:body-mod-grid` — вікно сітки модифікації тіла.
- `+feature:loadout-presets` — збережені набори спорядження з миттєвою зміною.

## Джерела
- ⭐ [Wikipedia: Z.H.P.](https://en.wikipedia.org/wiki/Z.H.P._Unlosing_Ranger_VS_Darkdeath_Evilman) — підземелля як у Mystery Dungeon, гармати, кидання, рівень з 1-го + Total Level, хаб, Body Modification, боси, платформи.
- [Wikipedia JA](https://ja.wikipedia.org/wiki/絶対ヒーロー改造計画) — 人体改造 (панелі у формі тіла, підсилювачі), 5 слотів, частини з рисами ворогів, знос, травма, 詠唱, будівлі хабу, «40 мільйонів разів».
- [TapTap: опис Windows-версії](https://www.taptap.cn/app/767813/all-info) — «turn-based rogue-like dungeon crawler», Total Level, grid-based Body Modification.
- YouTube: [пошук «ZHP Unlosing Ranger gameplay»](https://www.youtube.com/results?search_query=ZHP+Unlosing+Ranger+gameplay).

## Непевне
- (?) Форма частин у сітці тіла (одна клітина чи поліоміно), правила сусідства й розмір сітки — у джерелах нема; файл описує лише «панель порожня / заповнена».
- (?) Енергія костюма, перетворення й лічильник кроків — памʼятаю як частину гри, але жодне відкрите джерело цього не підтверджує; не описано.
- (?) Доставка обіду в підземелля — що саме дає (HP? ситість?) — не сказано.
- (?) Чи травма знімається одразу після першої перемоги над тією атакою — сформульовано загально («подолав — сильніший»).
