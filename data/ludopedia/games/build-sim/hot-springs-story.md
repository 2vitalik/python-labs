---
title: Hot Springs Story
slug: hot-springs-story
aka: [ゆけむり温泉郷, Yukemuri Onsenkyo]
family: build-sim
also: []
klass: cursor
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: score
year: 2009
platforms: [feature phone, iOS, Android, Switch, PC, PS4, Xbox]
links:
  - {kind: other, url: "https://www.pocketgamer.com/articles/027950/r/", best: true, note: "огляд Pocket Gamer (2011): кімнати й зручності, типи гостей, рейтинг путівників кожні пів року, бонус «Compat» за сусідство"}
  - {kind: official, url: "https://kairosoft.net/game/appli/onsen.html", note: "офіційна сторінка (JA): вид із кімнат, сад, сезонні рослини, ефекти джерел від довколишніх рослин і крамниць"}
  - {kind: steam, url: "https://store.steampowered.com/app/1823710/Hot_Springs_Story/", note: "Steam-версія 2022: кімнати, ресторани, аркади, купальні; японський сад; VIP-гості"}
  - {kind: other, url: "https://steamcommunity.com/sharedfiles/filedetails/?id=3689706743", note: "Steam-гайд (KO): зона впливу 5×5, сумісності, пейзаж, розміри, ефекти джерел, календар"}
  - {kind: other, url: "https://steamcommunity.com/sharedfiles/filedetails/?id=3334347328", note: "Steam-гайд (ZH): таблиця сумісностей, пейзаж за ціною, путівники, 49 типів гостей, предмети"}
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/カイロソフト", note: "список ігор Kairosoft: ゆけむり温泉郷 — 30.10.2009, платформи"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Hot+Springs+Story+Kairosoft+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [cursor-place, multi-cell-size, cell-click, hover-highlight, coverage-area, round-currency, shop-catalog, shop-window, in-round-upgrades, level-unlock, popup-text, status-panel, save-game, save-autosave, game-pause, +adjacency-score, +radius-scoring, +adjacency-buff, +compat-pairs, +seasonal-modifier, +recipe-unlock-by-neighbors, +guest-segments, +periodic-ranking, +investment-unlock, +type-wide-upgrade, +agent-needs, +monthly-upkeep, +calendar-events, +new-game-plus]
proposes: ["+cond:in_zone_5x5", "+effect:appeal", "+trigger:month_start", "+role:visitor", "+window:guidebook-ranking", "+window:investment-window", "+window:build-catalog", "+ui:scenery-value", "+ui:clock-calendar", "+feature:new-game-plus", "+card:compat-pairs", "+card:seasonal-modifier", "+card:recipe-unlock-by-neighbors", "+card:periodic-ranking"]
author: opus
date: 2026-11-09
---

# Hot Springs Story — онсен на клітинах: будівлі впливають одна на одну в квадраті 5×5, сусіди дають «Compat»-бонус або штраф, сад підіймає вид, а джерело відкриває ефект від того, що стоїть поруч

## Суть
Менеджмент Kairosoft: гравець ставить на ділянці-сітці номери, купальні, крамниці й сад і чекає гостей, що платять, голосують і приводять друзів. Головне рішення — **розташування**: кожна будівля впливає на інші в зоні 5×5 навколо себе, певні пари мають **сумісність** (кімната біля торгового автомата ↑, біля аркади ↓), рослини й ліхтарі піднімають **вид** сусідніх номерів, а гаряче джерело відкриває новий **ефект**, коли поруч назбирався потрібний набір будівель і декору. Двічі на рік путівники публікують рейтинг за голосами гостей — мета зійти на перше місце.

## Поле і час
- Квадратна сітка ділянки; будівлі 1×1 і більші (купальня 2×1, велика лазня 3×2, рецепція 2×2, кіоск 1×2, пінг-понг 2×1, ставок 2×1); ділянка росте купівлею прав на землю.
- Зона впливу будівлі — квадрат 5×5 з центром у ній (2 клітини в кожен бік, з діагоналями); джерела й лазні «бачать» ширше.
- Час — календар (місяці, роки, день/ніч); сезони змінюють вид рослин; швидкий режим ×2 — пізніше.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Японський / західний / VIP-номер | static | популярність, ціна, вид, утримання | гість живе тут; оцінює вид і сусідів |
| Купальня (чоловіча/жіноча) | static | 2×1; популярність, ціна, вид | має ефект; відкриває новий ефект від набору поруч |
| Велика лазня | static | 3×2 | як купальня, ширша зона |
| Рецепція | static | 2×2 | вхід гостей |
| Торговий автомат, масажне крісло, чайна | static | ціна, популярність | зручність поруч із номером |
| Крамниці: ресторан, кіоск, аркада, читальня, «доросла» аркада, салон краси, караоке, кафе, ворожка, пінг-понг | static | популярність, ціна, вид, сегмент | гість ходить у найближчі до свого номера; кожна має «свої» сегменти гостей |
| Пейзаж: сосна, гортензія, камінь, азалія, ліхтар, бамбук, клен, слива, ставок | terrain | ціна, вид (+6 … +26), сезонний бонус | додає вид будівлям у зоні; ліхтар — уночі +3 |
| Гість | neutral | сегмент, гроші, задоволення | приходить, платить за послуги, голосує в путівнику |
| Особливий гість (перукар, архітектор, бармен, майстер чаю, Kairobot…) | neutral | умова інвестиції | відкриває будівлі, тайли, ефекти |
| Предмет (насіння популярності, насіння ціни, молоко, чай, мед…) | pickup | ефект на тип | діє на **всі** будівлі одного типу |
| Путівник | zone | наклад, кількість закладів, нагорода | рейтинг за голосами гостей; нагорода G і відкриття |
| Право на землю (Land Deed) | pickup | ціна, дата | розширює ділянку |
| Гроші (G) | resource | — | будівництво, утримання, інвестиції |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(place, building)` → ЯКЩО `fits(building, cells)` and `has(player, gold)` → ТО `place(building)`, `currency(-cost)`, `custom: «перерахувати вплив у квадратах 5×5»`.
- КОЛИ `in_range(guest_room, vending_machine, 2)` → ТО `custom: «популярність і ціна номера ↑ для всіх сегментів»`.
- КОЛИ `in_range(guest_room, arcade, 2)` → ТО `custom: «↓ для всіх»` (шумні будівлі біля номерів і читальні знижують показники).
- КОЛИ `in_range(guest_room, massage_chair, 2)` → ТО `custom: «↑ для середнього віку й літніх»`.
- КОЛИ `in_range(japanese_room, japanese_room, 2)` → ТО `custom: «↑ для всіх»`; `in_range(western_room, restaurant, 2)` → ТО `custom: «↑ для всіх»`.
- КОЛИ `in_range(tea_room, reading_room, 2)` → ТО `custom: «взаємно ↑ для всіх»`; `in_range(reading_room, karaoke, 2)` → ТО `custom: «взаємно ↓ для всіх»`.
- КОЛИ `in_range(kiosk, western_room, 2)` → ТО `custom: «взаємно: молоді ↑, решта ↓»`; `in_range(beauty_room, fortune_teller, 2)` → ТО `custom: «жінки ↑»`; `in_range(arcade, game_room, 2)` → ТО `custom: «чоловіки ↑»`.
- КОЛИ `in_range(building, scenery, 2)` → ТО `counter(view, +scenery_value)` (сосна +6, камінь +10, азалія +12, ліхтар +13, бамбук +16, клен/слива +18, ставок +26).
- КОЛИ `custom: «змінився сезон або день/ніч»` → ТО `custom: «сезонний бонус: гортензія літо +2, азалія весна +3, ліхтар ніч +3, клен осінь +4, слива весна +6 / літо +2»`.
- КОЛИ `custom: «купальня перерахувала зону»` → ЯКЩО `count(vending_machine, >=, 1)` and `count(natural_stone, >=, 2)` → ТО `custom: «ефект Warm — до літніх гостей»`.
- КОЛИ `custom: «купальня перерахувала зону»` → ЯКЩО `count(karaoke, >=, 2)` and `count(table_tennis, >=, 1)` and `count(azalea, >=, 1)` → ТО `custom: «ефект Friendly — до груп»`; аналогічно ще 5 ефектів (Cozy, Soft, Popular, Rejuvenating, Intoxicating).
- КОЛИ `input(use, milk, women_bath)` → ТО `custom: «одразу ефект Soft»`.
- КОЛИ `custom: «гість обирає, куди піти»` → ТО `custom: «найближчі до його номера зручності й крамниці»`, `currency(+charge)`.
- КОЛИ `input(use, item, building_type)` → ТО `custom: «показник усіх будівель цього типу ↑ (велике / мале / ледь / нема — за таблицею)»`.
- КОЛИ `custom: «задоволення цільового сегмента > 30»` → ТО `spawn(guest_group)` нового типу; одночасно — до трьох цільових сегментів.
- КОЛИ `input(invest, special_guest)` → ЯКЩО `custom: «умова: напр. задоволення жінок ≥ 200 — перукар; популярність чайної ≥ 40 — майстер чаю»` → ТО `unlock(special_guest)`, `custom: «нові будівлі / тайли»`.
- КОЛИ `input(buy, land_deed)` → ЯКЩО `custom: «дата не раніше вказаної; попереднє право куплено»` → ТО `custom: «ділянка ширша»`.
- КОЛИ `schedule(march)` → ТО `custom: «рейтинг путівника за голосами гостей»`; ЯКЩО `custom: «заклад у рейтингу»` → ТО `currency(+reward)`, `unlock(next_guidebook)`.
- КОЛИ `schedule(may)` → ТО `custom: «Golden Week: гостей більше»`; `schedule(july_august)` → ТО `custom: «більше студентів і родин»`.
- КОЛИ `custom: «кінець місяця»` → ТО `currency(-upkeep)` за кожну будівлю.
- КОЛИ `custom: «перше місце в загальному путівнику»` → ТО `unlock(chimp_guest)`; популярність ≥ 90 в усіх сегментах → `unlock(kairobot)`.
- КОЛИ `level_end` → ТО `custom: «частина даних переходить у наступне проходження»`.
- Перемога: №1 у путівниках · Поразка: нема явної (?) · Рахунок: гроші, популярність, місце в рейтингу.

## Керування і ввід
- Тап/клік по клітині з каталогом будівництва → привид → поставити; переставити й знести будівлю.
- Тап по будівлі — показники (популярність, ціна, вид) і предмети; тап по гостю — його стан.
- Меню: будувати · предмети · інвестиції · реклама · путівники · статистика; швидкість ×2.

## Вікна, меню, HUD
- `game-screen`: ділянка зверху, гості ходять; HUD — `coins` (G), `+ui:clock-calendar`, популярність, `popup-text` над будівлями (гроші, «Compat»).
- `+window:build-catalog` — список будівель і пейзажу з ціною й розміром.
- `+window:investment-window` — особливі гості й відкриття; `shop-window` — предмети.
- `+window:guidebook-ranking` — рейтинги путівників; `stats-window` — сегменти гостей і задоволення.
- `+ui:scenery-value` — вид будівлі як число в картці; `tooltip` сумісності (?).
- `main-menu` → `game-screen`; `end-screen` (фінал/рахунок) → нове проходження з перенесеними даними; `settings-window`.

## Фічі поза полем
- `save-game` / `autosave`, `speed-control` (×2 пізніше), `+feature:new-game-plus` (частина даних переходить у нове проходження).
- Реклама (кампанії для приваблення сегментів) (?).
- Перевидання на Switch, Steam, PS4, Xbox; на Steam — досягнення.

## Варіації й родичі
- **Hot Springs Story 2** (31.08.2020; Switch, Steam, мобільні): той самий «温泉旅館経営SLG»; відмінності механік не перевірено (?).
- Kairosoft-сімʼя з комбо-сусідством: Dream Town Story, Pocket Academy, Mega Mall Story, Venture Towns (?).
- Корпус: `islanders` (очки за сусідів у радіусі), `tiny-tower-simtower`, `theme-hospital` / `two-point-hospital` (кімнати й гості), `kingdoms-and-castles`, `urbek-city-builder` (сусідство тайлів).
- Осі: **радіус впливу** — лише сусіди (Islanders, Backpack Hero) / квадрат 5×5 (Kairosoft) / дорожня мережа (Factory Town) · **знак** — лише бонус / бонус і штраф · **кому** — всім / за сегментами гостей.

## Цікавинки для курсу
- Зона впливу 5×5 і таблиця пар «будівля × будівля → ±для сегментів» — 📎.
- Вид як сума значень пейзажу в зоні із сезонним модифікатором — 🌱.
- Ефект джерела як «рецепт сусідства»: набір будівель у зоні відкриває нову властивість — 📎.
- Гість іде в найближчі заклади до свого номера — 📎 (BFS/відстань).
- Предмет діє на весь тип будівель — 🌱.
- Періодичний рейтинг за голосами + розблокування за порогами — 🥉.

## Мапа на каталог
- Є: `cursor-place` · `multi-cell-size` · `cell-click` · `hover-highlight` · `coverage-area` (зона 5×5) · `round-currency` · `shop-catalog` + `shop-window` · `in-round-upgrades` (насіння) · `level-unlock` · `popup-text` · `status-panel` · `save-game` + `save-autosave` · `game-pause`.
- **Нема** → пропозиції карток:
  - `+compat-pairs` «Таблиця сумісності пар будівель у зоні: ±для сегментів» · entities/state · 📎.
  - `+seasonal-modifier` «Значення тайла залежить від сезону/часу доби» · entities/state · 🌱.
  - `+recipe-unlock-by-neighbors` «Набір сусідів відкриває властивість» · entities/state · 📎.
  - `+guest-segments` «Гості за сегментами з окремим задоволенням» · game-logic/economy · 🥉.
  - `+periodic-ranking` «Рейтинг за голосами за розкладом» · game-logic/score · 📎.
  - `+investment-unlock` «Інвестиція з умовою відкриває контент» · game-logic/economy · 🌱.
  - `+type-wide-upgrade` «Апгрейд діє на всі будівлі типу» · game-logic/economy · 🌱.
  - `+monthly-upkeep` «Утримання за будівлю щомісяця» · game-logic/economy · 🌱.
  - `+calendar-events` «Події календаря змінюють потік гостей» · game-logic/waves · 🌱.
  - `+new-game-plus` «Перенесення частини прогресу в нове проходження» · game-logic/save · 🌱.
  - Повтори: `+adjacency-score`, `+radius-scoring` (Islanders), `+adjacency-buff` (Backpack Hero), `+agent-needs`.

## Пропозиції до словників
- `+cond:in_zone_5x5` — ціль у квадратній зоні впливу (Чебишовська відстань ≤ 2); загальніше — `in_range` з метрикою.
- `+effect:appeal` — змінити популярність/ціну будівлі для сегмента (замість `custom` у правилах сумісності).
- `+trigger:month_start` — початок місяця календаря (утримання, події).
- `+role:visitor` (повтор з `theme-hospital`) — гість-клієнт із власними потребами.
- `+window:guidebook-ranking`, `+window:investment-window`, `+window:build-catalog`.
- `+ui:scenery-value`, `+ui:clock-calendar` (повтор з `tiny-tower-simtower`).
- `+feature:new-game-plus`.
- `+card:compat-pairs`, `+card:seasonal-modifier`, `+card:recipe-unlock-by-neighbors`, `+card:periodic-ranking`.

## Джерела
- ⭐ [Pocket Gamer: Hot Springs Story review](https://www.pocketgamer.com/articles/027950/r/) — номери й зручності, типи гостей зі своїми вподобаннями, рейтинг путівників кожні пів року, «Compat» за сусідство, магазин апгрейдів, реклама.
- [Kairosoft: ゆけむり温泉郷](https://kairosoft.net/game/appli/onsen.html) — вид із номерів, сад, сезонні рослини, ефекти джерел від довколишніх рослин і крамниць, VIP, перенесення даних після фіналу.
- [Steam: Hot Springs Story](https://store.steampowered.com/app/1823710/Hot_Springs_Story/) — кімнати, ресторани, аркади, купальні, японський сад, VIP.
- [Steam-гайд (KO)](https://steamcommunity.com/sharedfiles/filedetails/?id=3689706743) — «범위 5x5 (가로세로대각선 2칸)», сумісності, пейзаж і сезонні бонуси, розміри, ефекти джерел, особливі гості, календар.
- [Steam-гайд (ZH)](https://steamcommunity.com/sharedfiles/filedetails/?id=3334347328) — 11 пар сумісності, пейзаж із цінами, путівники з нагородами, 49 типів гостей, предмети.
- [Wikipedia JA: カイロソフト](https://ja.wikipedia.org/wiki/カイロソフト) — дата 30.10.2009, платформи.
- YouTube: пошук «Hot Springs Story Kairosoft gameplay».

## Непевне
- (?) «Спад впливу з відстанню» (з рядка черги) — у жодному відкритому джерелі нема; лише зона 5×5.
- (?) Гайди писані для Steam-перевидання 2022 — мобільна версія 2010–2011 могла мати інші числа.
- (?) Персонал (найм, навчання) — у гайдах не згадано; у грі є, судячи з жанру Kairosoft.
- (?) Явної поразки (банкрутство) не знайдено.
- (?) Механіки Hot Springs Story 2 і родичі Kairosoft з комбо — з памʼяті.
- Черга: рік «2010 (?)» — оригінал 30.10.2009 (JA, мобільні телефони); англійська мобільна — 2010–2011 (Pocket Gamer, 03.2011; Play Store, 15.04.2011 за EN Wikipedia «Kairosoft»).
