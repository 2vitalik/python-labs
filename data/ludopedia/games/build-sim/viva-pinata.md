---
title: Viva Piñata
slug: viva-pinata
aka: [Viva Pinata, Віва Піньята]
family: build-sim
also: []
klass: cursor
axes:
  field: free
  time: realtime
  opponent: none
  info: partial
  random: runtime
  goal: collect
year: 2006
platforms: [Xbox 360, PC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Viva_Pi%C3%B1ata_(video_game)", best: true, note: "сад, інструменти, контур → мешканець, романс і лабіринт, кислі піньяти, бурʼяни, хижаки, смерть"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Viva_Pi%C3%B1ata", note: "франшиза: Rare, 2006, сиквели Trouble in Paradise і Pocket Paradise"}
  - {kind: other, url: "https://www.gamepressure.com/vivapinata/taffly-twingersnap-whirlm/z5894", note: "Gamepressure: вимоги появи/візиту/мешканця/романсу, варіанти кольору, ціни"}
  - {kind: other, url: "https://www.gamepressure.com/vivapinata/uninvited-guests/z4875", note: "Gamepressure: кислі, рафіани, Dastardos і хвороба, Ivor, Captain Cutlass"}
  - {kind: other, url: "https://www.gamepressure.com/vivapinata/game-guide/z48c45", note: "Gamepressure: зміст гайду (сад, помічники, рослини, гроші)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Viva+Pinata+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [cell-transform, floor-types, cursor-place, interaction-table, chase-player, random-walk, item-pickup, round-currency, shop-catalog, shop-window, inventory, codex-window, objective-text, popup-text, save-game, online-multiplayer, achievements-window, +species-requirement-ladder, +terrain-area-share, +attract-visitors, +food-variant-color, +breed-same-species, +predator-prey, +sour-visitor, +weed-spread, +sickness-timer, +helper-npc, +house-required]
proposes: ["+cond:area_share(type, op, pct)", "+cond:has_eaten(a, item, n)", "+trigger:requirements_met(stage)", "+effect:breed(a, b)", "+role:visitor", "+window:journal", "+ui:requirement-checklist", "+card:species-requirement-ladder", "+card:terrain-area-share"]
author: opus
date: 2026-11-09
---

# Viva Piñata — сад-екосистема: склад ґрунту, рослин і інших тварин відкриває сходинки «зʼявився → завітав → оселився → романс»

## Суть
Гравець лопатою й лійкою перетворює занедбану ділянку: трава, ґрунт, ставки, рослини, будиночки. Тварини-піньяти (60 видів) приходять самі, коли сад задовольняє їхні вимоги, що йдуть сходинками: контур → гість → мешканець → пара для романсу. Вимоги — від **частки площі** певного покриву («10 кв. піньометрів ґрунту або трави, 1 %») до «зʼїв конкретну квітку» чи «має 2 мешканців-Whirlm» — тобто кожен новий вид залежить від стану всього саду, включно з іншими видами. Головне для корпусу — **предикати над складом поля** і **харчові ланцюги**, де хижак має зʼїсти здобич, щоб оселитись.

## Поле і час
- Сад — ділянка з вільними координатами (3D, не сітка); покрив малюється лопатою й насінням по площі; площу міряють у «квадратних піньометрах» і частках саду.
- Шари: покрив (ґрунт / трава / вода) → рослини (квіти, овочі, дерева) → будиночки, паркани, стежки, декор → тварини.
- Real-time з днем і ніччю (?); рослини ростуть за часом і поливом (?).
- Камера над садом, курсор-рука; рівень саду зростає з досвідом і відкриває інструменти й розширення (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Ґрунт | terrain | площа | основа; лопатою зорати / утрамбувати (?) |
| Трава | terrain | площа | насіння трави; частина вимог (напр. Whirlm) |
| Вода (ставок) | terrain | площа | копається лопатою; вимога водних видів (Newtgat) |
| Рослина (квітка, овоч, дерево) | object | вид, стадія росту, полив | росте; дає плоди/насіння; її їдять піньяти (вимоги «зʼїв N») |
| Бурʼян | hazard | — | проростає й поширюється; руйнує ряди овочів, якщо не прибрати |
| Піньята-контур | neutral | вид | чорно-білий силует біля саду, коли виконано вимогу появи |
| Піньята-гість | neutral | вид | заходить у сад; оселиться, якщо виконано вимогу мешканця |
| Піньята-мешканець | ally | вид, колір-варіант, вартість, щастя (?) | живе в саду, їсть, може битись з не-здобиччю, романсувати |
| Хижак (піньятавор) | ally | здобич | має зʼїсти здобич, щоб оселитись чи романсувати; мешканців не їсть без наказу |
| Кисла піньята | enemy | вид (8) | їсть насіння, кидає отруйні цукерки, ламає обʼєкти; приручається парканом навколо |
| Рафіани (Professor Pester) | enemy | — | на пізніх рівнях: великі руйнування (засипають ставок) |
| Dastardos | enemy | — | приходить до хворої піньяти; якщо лікар не встиг — розбиває її |
| Будиночок виду | static | вид, ціна | обовʼязковий для романсу свого виду |
| Паркан | static | — | обгородити кислу піньяту — приручити; ділити сад |
| Помічник (Watchling тощо) | ally | робота | поливає, збирає плоди, вартує; будиночок і стежки — працює швидше |
| Яйце | container | вид | після романсу приносить лелека; можна висиджувати чи відправити іншому гравцю |
| Шоколадні монети | resource | — | валюта: продаж піньят і рослин, покупки в крамницях |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(shovel, ground)` → ТО `set_cell(area, soil)`; повторно на ґрунті — `set_cell(area, water)` (ставок) (?).
- КОЛИ `input(sow, grass_seed)` → ЯКЩО `cell(area, soil)` → ТО `set_cell(area, grass)`.
- КОЛИ `input(plant, seed)` → ТО `place(player, plant)`, `set_state(plant, growing)`.
- КОЛИ `input(water, plant)` → ТО `custom: «рослина росте швидше / не сохне»` (?).
- КОЛИ `rng(p)` → ТО `spawn_at(weed, random)`; КОЛИ `timer(every)` → ЯКЩО `adjacent_count(weed_area, vegetable, >, 0)` → ТО `custom: «бурʼян поширюється й руйнує ряд»`.
- КОЛИ `custom: «перевірка вимог виду»` → ЯКЩО `custom: «покрив типу ≥ N кв. піньометрів»` (`+cond:area_share`) → ТО `spawn_at(silhouette, garden_edge)` — стадія «зʼявився».
- КОЛИ `custom: «виконано вимогу візиту»` → ТО `move(pinata, into_garden)`, `set_state(pinata, visitor)`.
- КОЛИ `custom: «виконано вимогу мешканця»` → ЯКЩО `state(pinata, visitor)` → ТО `set_state(pinata, resident)`, `custom: «повний колір, ім'я»`.
- Приклад Whirlm: усі сходинки — «≥ 10 кв. піньометрів ґрунту або трави (1 %)»; романс — те саме + будиночок Whirlm.
- Приклад Taffly: поява — будь-яка квітка; візит — 2 квітки; мешканець — `custom: «зʼїв 1 квітку»`; романс — зʼїв 1 мак + будиночок.
- КОЛИ `contact(predator, prey)` → ЯКЩО `custom: «вимога хижака — зʼїсти здобич»` → ТО `disappear(prey)`, `counter(eaten, +1)`.
- КОЛИ `custom: «два мешканці без звʼязку хижак-здобич зустрілись»` → ТО `custom: «бійка»` (?).
- КОЛИ `input(romance, a, b)` → ЯКЩО `same(a, b, species)` and `custom: «виконано вимогу романсу»` and `count(species_house, >=, 1)` → ТО `custom: «танець → міні-гра лабіринт»`.
- КОЛИ `custom: «лабіринт пройдено»` → ТО `spawn_at(egg, garden)` (приносить лелека).
- КОЛИ `after(first_romance(species))` → ТО `unlock(romance_sweet)` — цукерка пропускає вимоги романсу для виду.
- КОЛИ `input(feed, pinata, item)` → ЯКЩО `custom: «предмет-варіант виду»` → ТО `custom: «змінює колір (варіант)»` (Whirlm: ріпа → фіолетовий).
- КОЛИ `rng(p)` → ТО `spawn_at(sour_pinata, garden_edge)`; КОЛИ `custom: «кисла поряд із насінням / обʼєктом»` → ТО `custom: «зʼїдає / ламає / кидає отруйну цукерку»`.
- КОЛИ `custom: «кислу обгороджено парканом»` → ТО `transform(sour_pinata, tame)`.
- КОЛИ `contact(pinata, poison_candy)` → ТО `set_state(pinata, sick)`; КОЛИ `state_on(pinata, sick)` → ТО `spawn_at(dastardos, garden_edge)`.
- КОЛИ `timer(illness_time)` → ЯКЩО `state(pinata, sick)` and `not custom: «лікар вилікував»` → ТО `custom: «Dastardos розбиває піньяту»`, `disappear(pinata)`.
- КОЛИ `in_range(dastardos, tame_crowla_or_sherbat, n)` → ТО `custom: «Dastardos тікає»`.
- КОЛИ `input(shovel, pinata)` → ТО `custom: «піньята розбивається: цукерки, втрачає аксесуари»`, `disappear(pinata)`.
- КОЛИ `input(sell, pinata_or_plant)` → ТО `currency(+value)`.
- КОЛИ `input(give, ivor, 1000_coins)` → ТО `unlock(ivor_shop)`.
- Перемога: нема фінальної (колекція видів, «майстер» виду після романсу) · Поразка: нема (втрати піньят) · Рахунок: рівень саду, досвід, вартість саду (?).

## Керування і ввід
- Курсор-рука на геймпаді / мишці; поточний інструмент з колеса чи панелі: лопата, лійка, насіння, пакети з магазину (?).
- Лопата: копати / розбивати; лійка: полив; клік по піньяті — інфо і дії (годувати, романс, назвати).
- Романс — окрема міні-гра: провести піньяту лабіринтом до пари.
- Розміщення будиночків, парканів, стежок — курсором по вільному місцю.

## Вікна, меню, HUD
- `game-screen`: сад, курсор-рука, монети (`coins`), рівень саду (`progress-bar`), значки над піньятами.
- `+window:journal` / `codex-window`: енциклопедія видів з вимогами сходинок (`+ui:requirement-checklist`), що відкриваються поступово.
- `shop-window`: крамниці села (насіння, будиночки, ліки, помічники; Ivor після 1000 монет).
- `custom-window` міні-гра лабіринту романсу.
- `achievements-window`: досягнення, ранги.
- `main-menu`, `save-slots`, `settings-window`, `pause-menu`.

## Фічі поза полем
- Помічники: найм, будиночки й стежки прискорюють їх.
- Обмін піньятами та яйцями через Xbox Live (`online-multiplayer`; сервер згодом закрили).
- `achievements`, ранги; відкриття крамниць і предметів з рівнем саду.
- Сиквели: Trouble in Paradise (2008, змінені вимоги видів), Pocket Paradise (DS, 2008); збірка Rare Replay (2015).

## Варіації й родичі
- У корпусі: `acnh-flowers` (селекція за сусідством), `stardew-farm` / `harvest-moon` (вирощування), `terra-nil` (екологічне відновлення ділянки), `simant` (екосистема), `game-of-life` (стан клітини від сусідів).
- Осі «вимога виду»: площа покриву / наявність обʼєкта / кількість мешканців іншого виду / «зʼїв N» / будиночок.
- Осі «сходинок»: одна умова появи / ланцюг контур → гість → мешканець → романс.

## Цікавинки для курсу
- Сходинки вимог виду як автомат станів (контур → гість → мешканець → пара) — 📎.
- Предикат «частка площі покриву ≥ p %» по всьому полю — 🌱 (агрегат над сіткою).
- Вимога «має N мешканців іншого виду» → граф залежностей видів; знайти порядок, щоб відкрити всіх — 🥉 (топосорт).
- Харчовий ланцюг: хижак оселяється, лише зʼївши здобич — 📎.
- Кисла піньята, що приручається огорожею навколо — 📎 (перевірка замкненого контуру).
- Хвороба з таймером і «ворог-кат», якого відлякують певні мешканці — 📎.
- Колір-варіант від їжі — 🌱.

## Мапа на каталог
- Є: `cell-transform` / `floor-types` (покрив) · `cursor-place` (рослини, будиночки) · `interaction-table` (хто кого їсть) · `chase-player` / `random-walk` (рух піньят) (?) · `item-pickup` · `round-currency` · `shop-catalog` / `shop-window` · `inventory` · `codex-window` (журнал) · `objective-text` · `popup-text` · `save-game` · `online-multiplayer` · `achievements-window`.
- **Нема** → пропозиції карток:
  - `+species-requirement-ladder` «Сходинки вимог для появи виду» · entities/spawn · 📎 · слоти {appear, visit, resident, romance}.
  - `+terrain-area-share` «Умова на частку площі покриву» · game-logic/constraints · 🌱.
  - `+attract-visitors` «Сутності приходять самі, коли поле відповідає умові» · entities/spawn · 🥉.
  - `+food-variant-color` «Їжа змінює варіант сутності» · entities/state · 🌱.
  - `+breed-same-species` «Пара одного виду → яйце» · entities/spawn · 📎.
  - `+predator-prey` «Хижак мусить зʼїсти здобич» · entities/interact · 📎.
  - `+sour-visitor` «Шкідник, що приручається огорожею» · entities/interact · 📎.
  - `+weed-spread`, `+sickness-timer`, `+helper-npc`, `+house-required` — 🌱 кожна.

## Пропозиції до словників
- `+cond:area_share(type, op, pct)` — частка/площа покриву типу на полі.
- `+cond:has_eaten(a, item, n)` — A зʼїв N предметів виду (історія сутності).
- `+trigger:requirements_met(stage)` — виконано набір вимог сходинки.
- `+effect:breed(a, b)` — пара дає нащадка (яйце).
- `+role:visitor` — сутність, що приходить сама, якщо поле відповідає умові.
- `+window:journal` — журнал видів з вимогами; `+ui:requirement-checklist` — список вимог з галочками.
- `+card:species-requirement-ladder`, `+card:terrain-area-share` — див. вище.

## Джерела
- ⭐ [Wikipedia: Viva Piñata (гра)](https://en.wikipedia.org/wiki/Viva_Pi%C3%B1ata_(video_game)) — лопата й лійка, оранка, ставки; контур → мешканець; романс-танець, лабіринт, яйце лелекою; цукерка після першого романсу; Pester, рафіани, кислі (паркан приручає); бурʼяни; 60 видів, піньятавори; смерть від лопати, хижака, хвороби; Xbox 360 9.11.2006, Windows 2007.
- [Wikipedia: франшиза](https://en.wikipedia.org/wiki/Viva_Pi%C3%B1ata) — розробники, сиквели, Rare Replay.
- [Gamepressure: Taffly, Twingersnap, Whirlm](https://www.gamepressure.com/vivapinata/taffly-twingersnap-whirlm/z5894) — точні вимоги чотирьох сходинок, варіанти від їжі, ціни (Whirlm 100 / будиночок 55; Taffly 300 / 165; Twingersnap 1500 / 825).
- [Gamepressure: Uninvited guests](https://www.gamepressure.com/vivapinata/uninvited-guests/z4875) — 8 кислих видів, рафіани й Captain Cutlass, Dastardos і лікар, Crowla/Sherbat, Ivor за 1000 монет, Watchling.
- [Gamepressure: Game guide](https://www.gamepressure.com/vivapinata/game-guide/z48c45) — розділи: стежки й паркани, помічники, рослини, гроші, ранги.
- YouTube: пошук «Viva Pinata gameplay».

## Непевне
- (?) Типи покриву понад ґрунт/траву/воду (пісок, довга трава) і як лопата робить ставок.
- (?) Полив і швидкість росту рослин, добовий цикл.
- (?) Sparrowmint: поява — 1 мешканець Whirlm, візит — 2; мешканець і романс (зʼїсти Whirlm, будиночок) — з пошукової видачі, сторінку не відкрито.
- (?) Бійки мешканців: коли саме і чим закінчуються.
- (?) Рівень саду: що його підвищує і що відкриває (розширення ділянки, крамниці).
- (?) Щастя піньяти й вплив на вартість — у змісті гайду є розділ, не відкривав.
- Fandom і StrategyWiki віддали 402/403 — у шапку не взято.
