---
title: Terraria — рідини
slug: terraria-liquids
aka: [Террарія]
family: build-sim
also: [dig-gravity]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: partial
  random: setup
  goal: none
year: 2011
platforms: [PC, macOS, Linux, PS4, Xbox One, Switch, iOS, Android]
links:
  - {kind: fandom, url: "https://terraria.wiki.gg/wiki/Liquids", best: true, note: "офіційна вікі: 4 рідини, течія, змішування, відра, помпи, дублювання"}
  - {kind: fandom, url: "https://terraria.wiki.gg/wiki/Water", note: "вода: випаровування в Underworld, гасіння On Fire!, дихання"}
  - {kind: fandom, url: "https://terraria.wiki.gg/wiki/Lava", note: "лава: 80 шкоди, On Fire!, знищення предметів, випаровування після 50 тайлів"}
  - {kind: fandom, url: "https://terraria.wiki.gg/wiki/Honey", note: "мед: уповільнення, баф Honey +1 HP/с, не випаровується"}
  - {kind: fandom, url: "https://terraria.wiki.gg/wiki/Shimmer", note: "мерехтіння: трансмутація предметів, прохід крізь блоки"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Terraria", note: "огляд: Re-Logic, 2011, платформи"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=Terraria", note: "пошук; точну сторінку не відкривав"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=terraria+liquid+mechanics", note: "пошук; течія і змішування"}
stage: v1
coverage: 60
mechanics: [floor-types, environment-death, hp-damage, status-effects, temporary-modes, cell-transform, gravity-fall, interaction-table, inventory-items, item-pickup, speed-per-type, +liquid-flow, +liquid-mixing, +liquid-volume, +breath-meter, +liquid-pump, +bucket-scoop, +evaporation, +item-transmute, +liquid-layer-behind-block]
proposes: ["+role:liquid", "+effect:flow", "+effect:evaporate", "+cond:volume", "+trigger:signal_rise", "+trigger:world_load", "+cond:submerged", "+effect:transmute", "+ui:breath-meter", "+feature:liquid-dynamics-setting", "+card:liquid-flow", "+card:liquid-mixing"]
author: opus
date: 2026-11-09
---

# Terraria (рідини) — вода, лава, мед і мерехтіння течуть між тайлами, а зустрівшись, твердіють у новий блок

## Суть
Описано **лише рідинний шар** 2D-пісочниці Terraria. Кожна клітина світу може містити рідину одного з чотирьох видів (вода, лава, мед, мерехтіння) з частковим рівнем; рідина падає вниз, розтікається вбік і вирівнюється. Дві різні рідини при контакті витрачаються й утворюють твердий блок (обсидіан, медовий блок…), тож рідини — і загроза, і будматеріал. Гравець носить рідини відрами й помпами, будує пастки, ферми, фонтани.

## Поле і час
- Сітка тайлів 2D-світу (вид збоку, гравітація вниз). Рідина — **окремий шар** клітини: не може займати клітину з блоком, але стоїть «позаду» поставленого в неї блоку й чекає, доки блок приберуть.
- Рівень рідини в клітині — частковий (відро бачить поріг 100/255 тайла ⇒ рівень зберігається як 0–255 (?)). Тонко розтеклася рідина зникає.
- Real-time; швидкість течії залежить від рідини: вода й мерехтіння найшвидші, лава повільніша, мед найповільніший. З Desktop 1.3.4 «динамічність» рідин — налаштування.
- При завантаженні світу рідини «осідають» (екран «Settling liquids»); рідина, замкнена між блоками, після однієї спроби осідання видаляється.
- Видимість: лава непрозора (ховає предмети й ворогів), мед сильно зменшує видимість, вода тонує колір за біомом.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець | player | HP, дихання, стани | ходить, стрибає; у рідині сповільнюється; може тонути |
| Вода | terrain | рівень, колір біому | швидко тече; гасить On Fire!; у Underworld випаровується |
| Лава | hazard | рівень | повільно тече; 80 шкоди + On Fire!; знищує дешеві предмети; випаровується після 50 тайлів течії |
| Мед | terrain | рівень | найповільніший; сильно сповільнює; дає баф Honey; не випаровується в Underworld |
| Мерехтіння (Shimmer) | terrain | рівень | швидко тече; трансмутує предмети; гравця проводить крізь блоки; відром не береться |
| Блок (земля, камінь…) | static | — | рідина не входить; замикає рідину, якщо поставлений у неї |
| Обсидіан | static | — | продукт вода + лава |
| Медовий блок | static | — | продукт вода + мед |
| Хрусткий медовий блок | static | — | продукт лава + мед |
| Блок етерію (Aetherium) | static | — | продукт мерехтіння + будь-яка рідина |
| Решітка (Grate) | gate | вкл/викл дротом | пропускає рідину, тримає сутності |
| Бульбашка (Bubble) | static | — | тримає рідину, пропускає сутності |
| Порожнє відро | pickup | — | черпає рідину з 3×3, якщо там ≥ 0.39 тайла |
| Повне відро (вода/лава/мед) | pickup | стек до 9999 | виливає рівно 1 повний тайл |
| Бездонне відро | pickup | — | нескінченне джерело рідини свого виду |
| Губка (Super / Lava / Honey / Ultra Absorbent) | pickup | — | прибирає рідину |
| Вхідна помпа (Inlet) | object | дріт | за сигналом забирає рідину |
| Вихідна помпа (Outlet) | object | дріт | за сигналом виливає забране, до 4 тайлів за сигнал |
| Рідинні бомби/ракети (Wet / Lava / Honey) | projectile | — | створюють рідину у місці вибуху |
| Dry Bomb / Dry Rocket, Freeze Bomb | projectile | — | прибирають рідину; Freeze — вода → лід |
| Предмет на землі | object | рідкість | у лаві: сірі й більшість білих згорають; у мерехтінні — трансмутують |
| Ворог / NPC | enemy | — | у лаві 50 шкоди; більшість босів імунні |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ЯКЩО `free(below)` → ТО `fall(liquid)`.
- КОЛИ `tick` → ЯКЩО `not free(below)` → ТО `custom: «рідина розтікається вбік, вирівнюючи рівні сусідніх клітин»`.
- КОЛИ `tick` → ЯКЩО `custom: «рівень у клітині надто тонкий»` → ТО `disappear(liquid)`.
- КОЛИ `contact(water, lava)` → ТО `set_cell(cell, obsidian)`, `custom: «витрачається до 1 тайла кожної рідини»`.
- КОЛИ `contact(water, honey)` → ТО `set_cell(cell, honey_block)`.
- КОЛИ `contact(lava, honey)` → ТО `set_cell(cell, crispy_honey_block)`.
- КОЛИ `contact(shimmer, water|lava|honey)` → ТО `set_cell(cell, aetherium_block)`.
- Пріоритет реакції: `custom: «вода < мерехтіння < мед < лава — визначає, чия клітина реагує»`; меблі, актуовані блоки можуть блокувати реакцію.
- КОЛИ `enter(water, underworld)` → ТО `disappear(water)` (випаровування); мед і лава — ні.
- КОЛИ `custom: «лава протекла 50 тайлів в одному напрямку»` → ТО `disappear(lava)`.
- КОЛИ `contact(player, lava)` → ЯКЩО `not has(player, obsidian_skin)` → ТО `damage(player, 80)`, `set_state(player, on_fire, 7s)` (Expert 14 с, Master 17.5 с).
- КОЛИ `contact(enemy, lava)` → ТО `damage(enemy, 50)`, `set_state(enemy, on_fire, 7s)`.
- КОЛИ `enter(item, lava)` → ЯКЩО `custom: «сіра або біла рідкість і занурений за середину спрайта»` → ТО `disappear(item)`.
- КОЛИ `enter(player, water|honey)` → ТО `clear_state(player, on_fire)`.
- КОЛИ `enter(player, liquid)` → ТО `speed(player, ×k)` (найповільніше — мед, далі лава, вода) і `custom: «скасовує шкоду від падіння»`.
- КОЛИ `tick` → ЯКЩО `custom: «голова під водою або медом»` and `not has(player, gills)` → ТО `counter(breath, -1)`.
- КОЛИ `counter(breath, ==, 0)` → ТО `damage(player, ~17/с)`.
- КОЛИ `enter(player, honey)` → ЯКЩО `custom: «басейн ≥ 2 тайли завширшки й ≥ 5/8 тайла завглибшки»` → ТО `set_state(player, honey, 30s)`, `custom: «+1 HP/с регенерації»`.
- КОЛИ `enter(item, shimmer)` → ТО `transform(item, into)` (розкрафт у матеріали або особливий предмет); нетрансмутовні — `fall(item)`.
- КОЛИ `custom: «голова гравця в мерехтінні»` → ТО `set_state(player, shimmering)` — повільне падіння крізь блоки до відкритого простору.
- КОЛИ `input(use, empty_bucket)` → ЯКЩО `custom: «у 3×3 навколо курсора ≥ 100/255 тайла»` → ТО `give(player, full_bucket)`, `custom: «знімає до 1 тайла»`.
- КОЛИ `input(use, full_bucket)` → ТО `place(player, liquid)` — рівно 1 повний тайл (розрив «забрати менше — вилити повний» = дублювання).
- КОЛИ `custom: «сигнал дроту на парі помп»` → ТО `custom: «inlet забирає до 4 тайлів, outlet виливає їх»`.
- КОЛИ `input(place, block)` → ЯКЩО `not cell(target, lava)` → ТО `place(player, block)`; рідина лишається замкненою за блоком.
- КОЛИ `custom: «сигнал дроту на решітці»` → ТО `set_state(grate, toggle)`.
- КОЛИ `input(use, sponge)` → ТО `custom: «прибирає рідину зі своєї області»`.
- КОЛИ `level_start` → ТО `custom: «settling liquids: рідини осідають; замкнена рідина після однієї спроби видаляється»`.
- Перемога/поразка/рахунок: шар без власної мети; смерть гравця (лава, утоплення) — звичайний респаун гри.

## Керування і ввід
- Клавіатура + миша: рух/стрибок — клавіші; використання предмета (відро, губка, блок) — клік у клітину під курсором у межах досяжності.
- Відро — «курсорний» ввід поверх аватара: обирається з хотбару, клік черпає або виливає.
- Помпи й решітки — через дроти й перемикачі (окремий шар Wiring), таймери дають ритм.

## Вікна, меню, HUD
- `game-screen`: світ збоку, HUD `hp-bar`, `inventory-bar` (хотбар з відрами), `breath-meter` (бульбашки над гравцем під водою), іконки бафів/дебафів (On Fire!, Honey, Shimmering) з `tooltip`.
- `loading-screen`: «Settling liquids» при завантаженні світу.
- `inventory-window` — інвентар (відра стеком).
- `settings-window` — серед іншого «динамічність» рідин (з 1.3.4).
- `main-menu` → вибір персонажа (`character-select`) → вибір світу (`save-slots`) → `game-screen`.

## Фічі поза полем
- `settings-window`: рівень динамічності рідин (Desktop 1.3.4+) — `+feature:liquid-dynamics-setting`.
- Збереження світу (`save-slots`), осідання рідин при завантаженні.
- Рідини як міні-станції крафту: стояти поруч з водою/лавою/медом — рецепти; фонтани й раковини — нескінченна вода для рецептів.
- Платформенні відмінності: Aetherium, бездонні відра, губки — лише Desktop/Console/Mobile; дублювання помпами — лише old-gen і 3DS.

## Варіації й родичі
- Родичі в корпусі: `oxygen-not-included-cells` (одна рідина на клітину з масою, шари за густиною, тепло), `timberborn` (вода як рівень у клітині), `minecraft-redstone` (поряд — течія води в Minecraft з рівнями 1–7), `the-powder-toy`, `sandspiel`, `noita` (клітинні автомати піску й рідин), `wheres-my-water` (труби й змішування рідин як пазл).
- Осі «рідина в клітині»: булева (Minecraft-джерело/течія) / рівень 0–N (Terraria, Timberborn) / маса з тиском (ONI).
- Осі «змішування»: нічого / твердне в блок (Terraria, Minecraft: обсидіан, бруківка) / реакція з продуктом-газом (Noita, ONI).
- Осі «зникнення»: тонкий шар / дистанція течії (лава 50) / біом (Underworld) / ніколи.

## Цікавинки для курсу
- Рідина з рівнем у клітині: падіння вниз + вирівнювання вбік — 🥈 (порядок обходу, «пульсація», збереження обʼєму).
- Таблиця змішувань пар рідин з пріоритетом — 📎 (`interaction-table` для шару рідин).
- Відро з порогом черпання і повним виливом — 🌱; помітити, що різниця дає дублювання — 📎 (урок про інваріант обʼєму).
- Помпи за сигналом: перенос рідини на відстань — 🥉 (звʼязок із шаром дротів).
- Лічильник дихання під водою + шкода при нулі — 🌱 (`hunger-clock`-подібно).
- Трансмутація предметів у рідині — 📎 (таблиця «предмет → продукт» як дані).
- Осідання рідин при завантаженні + видалення замкненої — 🥉 (симуляція до стабілізації, `settled`).

## Мапа на каталог
- Є: `floor-types` (вода/лава/мед як підлога з властивістю) · `environment-death` (лава, утоплення) · `hp-damage` · `status-effects` (On Fire!, Honey, Shimmering) · `temporary-modes` · `cell-transform` (змішування → блок) · `gravity-fall` (рідина падає) · `interaction-table` (пари рідин) · `inventory-items` + `item-pickup` (відра, губки) · `speed-per-type` (уповільнення за рідиною).
- **Нема** → пропозиції карток:
  - `+liquid-flow` «Рідина з рівнем: падає й розтікається» · entities/move · 🥈 · слоти {speed, min_level}.
  - `+liquid-mixing` «Дві рідини → блок» · entities/interact · 📎 · слот {pairs}.
  - `+liquid-volume` «Частковий рівень у клітині» · entities/state · 🥉.
  - `+breath-meter` «Дихання під водою» · entities/state · 🌱.
  - `+liquid-pump` «Помпа за сигналом» · entities/interact · 🥉.
  - `+bucket-scoop` «Черпати й виливати відром» · interface/input · 🌱 · слот {threshold}.
  - `+evaporation` «Рідина зникає за умовою» · entities/death · 🌱 · слот {where|distance}.
  - `+item-transmute` «Предмет у рідині стає іншим» · entities/interact · 📎.
  - `+liquid-layer-behind-block` «Рідина як шар під блоком» · entities/state · 📎.

## Пропозиції до словників
- `+role:liquid` — рідина як шар клітини з рівнем (не `terrain`: тече й змінює обʼєм).
- `+effect:flow` — розтектися на сусідні клітини, вирівнюючи рівні; `+effect:evaporate` — рідина зникає (біом, дистанція); `+effect:transmute` — предмет у рідині стає іншим за таблицею.
- `+cond:volume` — рівень рідини в клітині порівняно з порогом (відро 100/255, тонкий шар зникає); `+cond:submerged` — сутність (голова) під рідиною.
- `+trigger:signal_rise` — сигнал дроту (помпи, решітки); `+trigger:world_load` — завантаження світу (осідання рідин).
- `+ui:breath-meter` — бульбашки дихання над аватаром.
- `+feature:liquid-dynamics-setting` — налаштування «наскільки динамічні рідини».
- `+card:liquid-flow`, `+card:liquid-mixing` — див. вище.

## Джерела
- ⭐ [Terraria Wiki: Liquids](https://terraria.wiki.gg/wiki/Liquids) — чотири рідини, течія й осідання, змішування з пріоритетом, відра (поріг 100/255), помпи (4 тайли), дублювання.
- [Terraria Wiki: Water](https://terraria.wiki.gg/wiki/Water) — випаровування в Underworld, гасіння вогню, дихання, кольори біомів.
- [Terraria Wiki: Lava](https://terraria.wiki.gg/wiki/Lava) — 80/50 шкоди, On Fire! 7/14/17.5 с, знищення предметів, 50 тайлів до випаровування.
- [Terraria Wiki: Honey](https://terraria.wiki.gg/wiki/Honey) — баф Honey (+1 HP/с, 30 с, басейн ≥ 2 × 5/8).
- [Terraria Wiki: Shimmer](https://terraria.wiki.gg/wiki/Shimmer) — трансмутація, Shimmering, Aetherium, відром не береться.
- [Wikipedia](https://en.wikipedia.org/wiki/Terraria) — Re-Logic, 16.05.2011, платформи.
- YouTube: пошук «terraria liquid mechanics».

## Непевне
- (?) Внутрішнє зберігання рівня як 0–255 — висновок із порогу відра 100/255; алгоритм вирівнювання (порядок обходу клітин) вікі не описує.
- (?) Мінімальний рівень, нижче якого рідина зникає, — вікі не дає числа.
- (?) «~17 HP/с» при утопленні — з вікі Liquids, «about»; точний тік не перевірено.
- (?) Області дії губок і бомб — вікі не дає чисел.
- (?) Список платформ — скорочено; Stadia (знято) й старі консолі пропущені.
