---
title: Harvest Moon (SNES)
slug: harvest-moon
aka: [Bokujō Monogatari, 牧場物語, Story of Seasons]
family: build-sim
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: state
year: 1996
platforms: [SNES, Satellaview]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Harvest_Moon_(video_game)", best: true, note: "огляд петлі: полив щодня, тварини, нестача поливу зупиняє ріст"}
  - {kind: other, url: "https://fogu.com/hm/snes/crops.php", note: "FoGu: культури, 3×3 посадка, дні росту, регроу, ціни"}
  - {kind: other, url: "https://fogu.com/hm/snes/tools.php", note: "FoGu: інструменти і золоті версії, спринклер 3×3"}
  - {kind: other, url: "https://fogu.com/hm/snes/pberries.php", note: "FoGu: витривалість 100, пороги, 10 power berries"}
  - {kind: other, url: "https://fogu.com/hm/snes/yourfarm.php", note: "FoGu: будівлі ферми, ящик відвантаження о 17:00, 2 інструменти в руках"}
  - {kind: other, url: "https://fogu.com/hm/snes/ending.php", note: "FoGu: 7 кінцівок і їхні умови"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=harvest+moon+snes+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [move-4dir, impassable-cells, floor-types, cell-transform, coverage-area, destructible-blocks, inventory-items, inventory-limit, item-pickup, round-currency, shop-catalog, save-game, hunger-clock, event-points, +day-tick, +growth-stages, +tool-area-charge, +energy-cost, +area-seed-plant, +season-crop-rule, +animal-care, +ending-evaluation, +deadline-years]
proposes: ["+trigger:day_start", "+trigger:season_change", "+ui:clock-calendar", "+ui:stamina-face", "+window:diary-save", "+window:ending-scenes", "+feature:ending-evaluation", "+card:area-seed-plant"]
author: opus
date: 2026-11-09
---

# Harvest Moon (SNES) — первинна фермерська петля: зорати 3×3, посіяти з центру, поливати щодня, відвантажити до 17:00

## Суть
Гравець успадковує занедбану ферму й має **2.5 роки**, щоб її відродити: розчистити поле від каміння, пеньків і бурʼяну, орати, сіяти, поливати, продавати врожай, тримати корів і курей, одружитись. Порівняно з `stardew-farm` тут **первинна** версія петлі: насіння сіється мішком одразу на квадрат 3×3, полив щодня обовʼязковий (без нього культура не росте, але й не гине), восени культур нема. Наприкінці батько оцінює ферму — кінцівки за досягнутими станами.

## Поле і час
- Ферма — квадратна сітка клітин поля з будівлями (дім, корівник, курник, силос, сарай з інструментами, дровітня, ставки-водойми, ящик відвантаження).
- Шари клітини поля: ґрунт (дикий / зораний / политий) + обʼєкт (камінь малий/великий, пеньок, бурʼян, культура, трава-пасовище).
- Час: ігровий годинник дня; **день** — тік росту; о 17:00 скупник забирає ящик відвантаження. Сезони: весна, літо, осінь, зима. Ліміт гри — 2.5 роки.
- Погода (дощ, буря, сніг) змінює день; у бурю кури надворі гинуть (?) — див. Непевне.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Фермер | player | витривалість 100, 2 інструменти в руках | ходить 4 напрямки, бʼє інструментом у клітину попереду |
| Дика клітина поля | terrain | — | мотика → зораний ґрунт |
| Зораний ґрунт | terrain | сухий/политий | приймає насіння; полив — до наступного дня |
| Малий камінь | static | 1 удар | молот розбиває; можна кинути у водойму |
| Великий камінь | static | 6 ударів (золотий — 1) | молот |
| Пеньок | static | 6 ударів (золота сокира — 1) | сокира → деревина в дровітню |
| Бурʼян | static | — | серп зрізає (золотий — 3×3) |
| Культура (картопля, ріпа, кукурудза, томат) | object | сезон, днів росту, регроу | щодня +1 стадія, якщо полита; доросла — збір |
| Трава-пасовище | object | 9 днів, регроу 7 | серп → корм у силос; узимку спить |
| Насіння | pickup | сезон | сіється мішком на 3×3 навколо фермера |
| Лійка | pickup | — | поливає 1 клітину; поповнюється у водоймі |
| Спринклер | pickup | 3×3 | поливає 9 клітин; продається 20 літа за 2000 G |
| Мотика / Золота мотика | pickup | 1 / 6 клітин у ряд | оре |
| Ящик відвантаження | sink | — | о 17:00 перетворює вміст на гроші |
| Силос | container | корм | тримає зрізану траву для тварин |
| Корова | neutral | здоровʼя, вік | їсть щодня, треба розмовляти, чесати, доїти; не годована → хворіє |
| Курка | neutral | — | їсть щодня; яйця; надворі — ризик бурі й диких собак |
| Дикий собака | enemy | — | може зʼїсти курку надворі |
| Їжа (торт, риба, гриби, ягоди) | pickup | +10 / +50 витривалості | відновлює витривалість; отруйний гриб −10 |
| Power Berry | pickup | 10 на гру | збільшує щоденну витривалість |
| Гаряче джерело | terrain | — | 5–6 занурень → витривалість 100 |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(hoe, cell)` → ЯКЩО `cell(target, field)` → ТО `set_cell(target, tilled)`; золота мотика — 6 клітин у ряд.
- КОЛИ `input(seed_bag)` → ЯКЩО `custom: «фермер у центрі 3×3 зораних клітин»` → ТО `custom: «насіння лягає на всі 9 клітин»`.
- КОЛИ `input(watering_can, cell)` → ЯКЩО `has(farmer, water)` → ТО `set_state(cell, watered, 1 day)`.
- КОЛИ `contact(watering_can, water_hole)` → ТО `custom: «лійка поповнюється»`.
- КОЛИ `day_start` → ЯКЩО `state(cell, watered)` → ТО `counter(crop_stage, +1)`; інакше `custom: «культура не росте, але й не гине»`.
- КОЛИ `day_start` → ТО `clear_state(cell, watered)`; спринклер `custom: «поливає 3×3 навколо себе»`.
- КОЛИ `counter(crop_stage, ==, days_to_grow)` → ТО `set_state(crop, ripe)`.
- КОЛИ `input(harvest, crop)` → ЯКЩО `state(crop, ripe)` → ТО `pickup(farmer, produce)`; регроу-культура `custom: «знову дозріває через 3 дні»`, інакше `set_cell(target, tilled)`.
- КОЛИ `input(hammer, rock)` → ТО `counter(rock_hits, +1)`; КОЛИ `counter(rock_hits, ==, 6)` → ТО `disappear(rock)` (малий — з 1 удару, золотий молот — завжди 1).
- КОЛИ `input(axe, stump)` → ТО `counter(stump_hits, +1)`; КОЛИ `counter(stump_hits, ==, 6)` → ТО `disappear(stump)`, `give(farmer, lumber)` (золота сокира — з 1 удару).
- КОЛИ `input(sickle, weed)` → ТО `disappear(weed)`; золотий серп — `clear(square3)`.
- КОЛИ `input(sickle, grass)` → ЯКЩО `state(grass, grown)` → ТО `counter(fodder, +1)` у силос.
- КОЛИ `input(tool)` → ТО `counter(stamina, -k)` (?).
- КОЛИ `counter(stamina, <=, 50)` → ТО `custom: «фермер пітніє»`; `<= 25` → `custom: «важко дихає»`; `== 0` → `custom: «падає без сил»`.
- КОЛИ `input(eat, food)` → ТО `counter(stamina, +n)`.
- КОЛИ `picked(farmer, power_berry)` → ТО `custom: «щоденна витривалість зростає»`.
- КОЛИ `schedule(17:00)` → ТО `currency(+sum(shipped))`, `clear(shipping_bin)`.
- КОЛИ `day_start` → ЯКЩО `not state(cow, fed)` → ТО `set_state(cow, sick)`; затяжне нехтування → `died(cow)`.
- КОЛИ `custom: «буря або дикий собак»` → ЯКЩО `custom: «курка надворі»` → ТО `disappear(chicken)`.
- КОЛИ `season_change` → ЯКЩО `mode(winter)` → ТО `set_state(grass, dormant)`; восени культури не сіються (у продажу нема насіння).
- КОЛИ `custom: «минуло 2.5 роки»` → ТО `window(ending)` — батько оцінює: 200 штук одного врожаю, 4 курки, 4 дорослі корови, шлюб, дитина, «Ladies Man», «Reckless Abandonment».
- Перемога: сцени-кінцівки за досягнутими станами · Поразка: нема, «найгірша» кінцівка — без грошей, тварин і врожаю · Рахунок: гроші як ресурс.

## Керування і ввід
- D-pad — рух; кнопка — застосувати інструмент у клітину попереду; інша — підняти/кинути предмет (камінь у водойму, врожай у ящик).
- У руках лише 2 інструменти; решта — в сараї (обмін на місці).
- Дзвоник кличе корів до фермера.

## Вікна, меню, HUD
- `game-screen`: ферма/село, HUD — годинник і дата/сезон (`+ui:clock-calendar`), поточний інструмент; витривалість подається анімацією фермера (піт, задишка), а не смугою (`+ui:stamina-face`).
- `+window:diary-save` — збереження через щоденник у домі.
- `dialogue-window` — розмови з селянами й нареченими; щоденники дівчат із сердечками (`stats-window`-подібно).
- `shop-window` — квіткова крамниця (насіння), сарай з інструментами, тварини.
- `+window:ending-scenes` — фінальна оцінка й сцени кінцівок.
- `splash-screen` → `main-menu` (новий / продовжити з щоденника) → `game-screen`.

## Фічі поза полем
- `save-slots` через щоденник; `levels-sequential` нема — один безперервний світ.
- Ліміт часу гри (2.5 роки) + оцінка — `+feature:ending-evaluation`.
- Золоті інструменти як прогресія (секрети: богиня ставка, феї, тесля).
- Фестивалі (окремі дні), шлюб і дитина — соціальний шар поза полем.
- Satellaview-версія: 4 епізоди-трансляції 1996 р.

## Варіації й родичі
- Нащадки: серія Harvest Moon / Story of Seasons, Rune Factory, `stardew-farm` (пряма спадкоємиця), `acnh-flowers` (полив сусідніх квітів).
- Відмінності від Stardew: посадка мішком 3×3 з центру, а не по клітині; витривалість 100 і пороги-анімації; восени нема культур; гра має кінець (2.5 роки), а не нескінченна; спринклер один, 3×3.
- Осі «посадка»: по клітині / шаблоном 3×3 / рядом (золота мотика 6).
- Осі «пропущений полив»: стоп росту (HM) / стоп росту + висихання (Stardew) / загибель.

## Цікавинки для курсу
- Клітина поля як автомат станів (дика → зорана → посаджено → стадії → дозріло) із щоденним тіком — 📎.
- Посадка шаблоном 3×3 навколо аватара — 🌱 (одна дія → 9 клітин; що робити з незораними).
- Багатоударні перешкоди (6 ударів, золотий інструмент — 1) — 🌱.
- Витривалість із порогами, що змінюють анімацію, а не числом на екрані — 🌱.
- Ящик відвантаження: продаж наприкінці дня, а не одразу — 🌱.
- Обмежена гра (2.5 роки) з кількома кінцівками за досягнутими станами — 📎.
- Тварини з потребами «щодня» і станами здоровий/хворий/мертвий — 📎.

## Мапа на каталог
- Є: `move-4dir` · `impassable-cells` (каміння, пеньки, будівлі) · `floor-types` (ґрунт, вода) · `cell-transform` (оранка) · `coverage-area` (спринклер 3×3) · `destructible-blocks` (каміння/пеньки/бурʼян) · `inventory-items` + `inventory-limit` (2 інструменти) · `item-pickup` · `round-currency` · `shop-catalog` · `save-game` · `hunger-clock` (витривалість, їжа) · `event-points` (ціни продажу).
- **Нема** → пропозиції карток:
  - `+day-tick` «Денний тік» — та сама, що в `stardew-farm`.
  - `+growth-stages` «Стадії росту за днями» — та сама.
  - `+tool-area-charge` / `+energy-cost` — як у `stardew-farm`; тут — золоті інструменти замість заряду.
  - `+area-seed-plant` «Посадка шаблоном навколо аватара» · entities/interact · 🌱 · слот {shape: 3x3}.
  - `+season-crop-rule` «Сезон дозволяє/забороняє культуру» · game-logic · 🌱.
  - `+animal-care` «Тварина з щоденними потребами» · entities/state · 📎.
  - `+ending-evaluation` «Оцінка в кінці терміну, кілька кінцівок» · game-logic/win · 📎.
  - `+deadline-years` «Ліміт ігрового часу (роки)» · game-logic/lose · 🌱.

## Пропозиції до словників
- `+trigger:day_start`, `+trigger:season_change` — ті самі, що в `stardew-farm` (лічба підтримки).
- `+ui:clock-calendar` — годинник + дата + сезон; `+ui:stamina-face` — стан витривалості анімацією персонажа.
- `+window:diary-save` — збереження «щоденником» у світі гри; `+window:ending-scenes` — серія сцен-кінцівок.
- `+feature:ending-evaluation` — оцінка гравця після ліміту часу.
- `+card:area-seed-plant` — див. вище.

## Джерела
- ⭐ [Wikipedia: Harvest Moon (video game)](https://en.wikipedia.org/wiki/Harvest_Moon_(video_game)) — петля дня, полив щодня (без нього ріст стоїть), тварини, бурі й собаки, Satellaview.
- [FoGu: Crops](https://fogu.com/hm/snes/crops.php) — 3×3 посадка з центру, таблиця культур (дні, регроу, ціни), восени культур нема, трава і силос.
- [FoGu: Tools](https://fogu.com/hm/snes/tools.php) — 6 ударів/золоті інструменти, спринклер 3×3 за 2000 G.
- [FoGu: Power Berries & Stamina](https://fogu.com/hm/snes/pberries.php) — 100 очок, пороги 50/25/0, їжа, джерело, 10 ягід.
- [FoGu: Your Farm](https://fogu.com/hm/snes/yourfarm.php) — будівлі, ящик о 17:00, 2 інструменти в руках, камінь у водойму.
- [FoGu: The End](https://fogu.com/hm/snes/ending.php) — 7 кінцівок і умови.
- YouTube: пошук «harvest moon snes gameplay».

## Непевне
- (?) Чи зміна сезону вбиває культури, що ростуть, — черга так пише, але в джерелах не бачив (FoGu: лише «восени культур нема»).
- (?) Довжина сезону (30 днів) — з памʼяті, не перевірено.
- (?) Скільки витривалості коштує кожен інструмент і на скільки підіймає її ягода — джерела не дають.
- (?) Курку надворі губить саме буря/собаки — за Wikipedia; механіку шансу не бачив.
- (?) Рік виходу: Японія 1996, Північна Америка 1997 (з памʼяті); fandom-вікі віддала 402.
- (?) Розмір поля ферми — не знайдено.
