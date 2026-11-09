---
title: Urbek City Builder
slug: urbek-city-builder
aka: [Urbek]
family: build-sim
also: [thinky]
klass: cursor
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: state
year: 2022
platforms: [PC]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1411740/Urbek_City_Builder/", best: true, note: "без грошей, 30+ ресурсів, органічний ріст будівель від оточення, умови розміщення (ринок біля ферм, університет ← ліцей ← школа), освіта відкриває будівлі"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Urbek_City_Builder", note: "пазл-ситібілдер без грошей і катастроф; апгрейд в інший тип за розміщенням; забруднення шкодить житлу; зони; first-person"}
  - {kind: other, url: "https://worive.gitbook.io/urbek-modding/in-depth-knowledge/structure-attributes/placement.md", note: "документація модингу: buildingsNeeded / resourcesNeeded / localVariablesNeeded у радіусі, distanceToRoad, біоми, coastal, line/zone"}
  - {kind: other, url: "https://worive.gitbook.io/urbek-modding/in-depth-knowledge/structure-attributes/upgrades-and-abandon", note: "модинг: список updates у порядку пріоритету, updatesFrom, fastAbandon"}
  - {kind: other, url: "https://worive.gitbook.io/urbek-modding/in-depth-knowledge/in-game-data-names/building-names/map-0-temperate.md", note: "188 будівель мапи Temperate: ланцюги житла, нетрі, бунтарі, вілла → маєток"}
  - {kind: other, url: "https://www.thegamer.com/urbek-city-builder-best-layouts-farms-mining-fishing-mansions-villas-wind-orchards/", note: "відстані в клітинах: шахтарські й рибальські доми, вілли, Path of Wealth / Leisure"}
  - {kind: other, url: "https://ladiesgamers.com/urbek-city-builder-review/", note: "огляд: хатина → сільський дім, забруднення → дім бунтарів, апгрейд кварталу одним кліком"}
  - {kind: other, url: "https://www.keengamer.com/articles/reviews/pc-reviews/urbek-city-builder-review-a-beginners-guide-to-city-planning/", note: "огляд: зони впливу, нетрі біля фабрик, біоми забороняють ріллю"}
  - {kind: other, url: "https://www.gog.com/game/urbek_city_builder", note: "GOG: опис, 5 мап-біомів і «шляхи» цілей (з відгуків)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Urbek+City+Builder+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [cursor-place, hover-highlight, coverage-area, multi-cell-size, cell-transform, chain-reaction, impassable-cells, tutorial-window, save-game, +house-evolution, +influence-map, +labor-pool, +zone-paint, +drag-build-line, +context-tile-rules, +placement-requirement, +first-person-view, +mod-support, +radius-requirement, +upgrade-priority-list, +context-specialization, +downgrade-abandon, +resource-threshold-unlock, +policy-choice, +path-goals, +no-money-economy]
proposes: ["+cond:count_in_radius", "+cond:local_var_in_radius", "+ui:range-rings", "+window:policy-window", "+card:radius-requirement", "+card:upgrade-priority-list", "+card:context-specialization", "+card:downgrade-abandon"]
author: opus
date: 2026-11-09
---

# Urbek City Builder — без грошей: кожна будівля сама стає іншою, коли оточення виконує її умови в радіусі N клітин

## Суть
Ситібілдер-пазл на квадратній сітці з вокселями, де **нема грошей і катастроф**: будують за ресурси (деревина, їжа, вугілля, праця різної кваліфікації — понад 30 видів). Ядро — **умовні перетворення**: хатина, біля якої зʼявились парк і крамниця, стає сільським домом; дім біля фабрики — нетрями, а без поліції — домом бунтарів; дім біля доку й води — рибальським. Одна поставлена будівля може запустити ланцюг апгрейдів цілого кварталу й раптом виснажити ресурси й працю. Пазл — у вимогах сусідства, кількості й відстанях між будівлями.

## Поле і час
- Квадратна сітка тайлів; відстані й радіуси — у клітинах (`radio` у файлах будівель). Будівлі бувають 1×1 і більші (2×2, 3×3 у форматі моделі `Name,TileSize,TileSize`).
- Мапа = біом: файли гри мають 5 мап (Temperate, Desert, Archipel, Forest, Ruins) і 24 типи біомних клітин (пустеля, степ, луг, ліс, сніг, хвойний ліс, заплава, камінь, тропіки, пустища, руїни міста й полів…).
- Шари клітини: біом → вода (море / ріка / лагуна) → будівля або дорога → **локальні змінні** (28: забруднення, зелені зони, освіта, комерція, нічне життя, щільність…), які будівлі виробляють і споживають навколо себе.
- Камера вільна над мапою; режим вулиці від першої особи — лише для огляду, на гру не впливає.
- Час: виробництво й апгрейди відбуваються з часом (?) — апгрейд «має шанс» статися, коли умови виконано.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітина біому | terrain | biome id | дозволяє/забороняє типи будівель (`biomeAble` / `biomeUnable`); пустеля й тундра не дають ріллі |
| Вода (море, ріка, лагуна) | terrain | — | `coastal`-будівлі лише поруч; док, рибальські доми, міст |
| Рудна клітина (залізо) | resource | — | залізна шахта — щонайменше 1 рудна клітина в радіусі 5 |
| Ліс | resource | — | лісоруби збирають деревину в радіусі (`resourceExtraction`); природні ресурси вичерпуються |
| Дорога (сільська, міська, комерційна, промислова, «гарна») | conduit | ставиться лінією | більшості будівель треба дорога в межах 3 клітин; сама апгрейдиться за оточенням; вигляд — за типом перехрестя |
| Деревʼяна хатина | piece | рівень 0 | дає некваліфіковану працю; з парками й крамницями → сільський дім |
| Сільський дім → заможний → передмістя → заможне передмістя → downtown | piece | рівень | росте, коли поруч сервіси й ресурси; downtown просить школи й зупинки |
| Багатоповерхівки (blocks, 5 і 12 поверхів, HLM, змішані) | piece | щільність | густа забудова з базовими сервісами |
| Нетрі (shanty house) | piece | — | житло біля забруднення або без сервісів |
| Дім бунтарів | piece | — | нетрі без поліції |
| Вілла → маєток | piece | ділянка 4×4 | жодного житла в радіусі 5; вистачає 1 парку поруч; маєток — апгрейд вілли |
| Рибальський дім | piece | — | дім біля води в радіусі 6 від доку: їжа + праця; не апгрейдиться; забруднення → нетрі |
| Шахтарський дім | piece | — | дім біля дороги в радіусі 5 від шахти: дає ресурс шахти; не зважає на забруднення |
| Тематичний квартал (митців, релігійний, нічного життя, анархістська комуна) | zone | — | бари, парки, бібліотеки + низька щільність поруч → богемний квартал |
| Сервіси (школа, ліцей, університет, клініка, лікарня, поліція, зупинка) | static | радіус дії | виробляють локальні змінні; вимоги ланцюгом (університет ← ліцей ← школа) |
| Парк, сквер | static | — | зелені зони; піднімають ціну житла |
| Ферма, сад | zone | ставиться зоною | їжа; працює до 5 клітин від дороги; не на пустелі/снігу |
| Ринок, мінімаркет | static | — | ринок — біля ферм; мінімаркет — впритул до дороги |
| Фабрика, ТЕС, металургія | static | − якість життя | більше ресурсів, але знецінює житло поруч |
| Шахта (вугілля, залізо) | static | — | вугільна — будь-де; залізна — біля руди |
| Склад, силос | container | місткість | зберігає ресурси (`storage`) |
| Покинута будівля | object | — | результат деградації (`abandonedModel`) |
| Глобальна змінна (кваліфікована / наукова праця) | resource | поріг q | відкриває нові будівлі (`unblock`) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(place, building)` → ЯКЩО `has(city, cost)` and `custom: «біом клітини дозволений»` and `custom: «дорога не далі за distanceToRoad»` and `custom: «усі buildingsNeeded виконано»` → ТО `place(player, building)`, `take(city, cost)`; інакше `block`.
- Умова сусідства: `custom: «у радіусі r щонайменше / щонайбільше q будівель типу X»`; q = 0 і «щонайбільше» — заборона (вілла: 0 житла в радіусі 5).
- Те саме для ресурсів (`resourcesNeeded`) і локальних змінних (`localVariablesNeeded`: сума в радіусі вище/нижче порогу).
- КОЛИ `input(drag, road)` → ТО `custom: «ставиться лінією»`; ферми й житло — `custom: «зоною»`.
- КОЛИ `tick` → ЯКЩО `custom: «виконано умови типу зі списку updates»` and `prob(p)` → ТО `transform(building, next)` — перший за порядком списку тип, чиї умови виконано (список updates = пріоритет).
- КОЛИ `after(transform)` → ТО `custom: «сусіди перевіряють свої умови знову»` — каскад: один парк чи ринок апгрейдить цілий квартал.
- КОЛИ `tick` → ЯКЩО `custom: «умови поточного рівня більше не виконано»` → ТО `transform(building, lower_or_abandoned)`; з fastAbandon — швидше.
- КОЛИ `tick` → ЯКЩО `in_range(hut, factory, r)` or `custom: «бракує сервісів»` → ТО `transform(hut, shanty)`.
- КОЛИ `tick` → ЯКЩО `state(house, shanty)` and `not in_range(house, police, r)` → ТО `transform(house, rebel_house)`.
- КОЛИ `tick` → ЯКЩО `cell(house, coast)` and `in_range(house, dock, 6)` → ТО `transform(house, fisherman_house)`; далі `counter(food, +n)`, `counter(unskilled_work, +n)`.
- КОЛИ `tick` → ЯКЩО `state(house, fisherman)` and `in_range(house, pollution, r)` → ТО `transform(house, shanty)` — їжа зупиняється.
- КОЛИ `tick` → ЯКЩО `custom: «дім біля дороги»` and `in_range(house, mine, 5)` → ТО `transform(house, miner_house)` — дає ресурс шахти; на забруднення не зважає.
- КОЛИ `input(place, iron_mine)` → ЯКЩО `custom: «≥ 1 рудна клітина в радіусі 5»` → ТО `place(player, iron_mine)`; вугільна — без умови.
- КОЛИ `input(place, villa)` → ЯКЩО `custom: «0 житла в радіусі 5»` → ТО `place(player, villa)`.
- КОЛИ `tick` → ЯКЩО `adjacent_count(villa, park, >=, 1)` and `custom: «населення й щастя достатні»` → ТО `transform(villa, mansion)`.
- КОЛИ `tick` → ТО `custom: «кожна будівля додає produces (мінус = споживання) і локальні змінні у свій радіус»`; без byBuilding — на кожну клітину (3×3 дає 9×).
- КОЛИ `tick` → ЯКЩО `custom: «resourceExtraction: ресурс є в межах distance»` → ТО `counter(wood, +n)`; ліс вичерпується (?).
- КОЛИ `tick` → ЯКЩО `custom: «некваліфікованої праці менше, ніж споживають будівлі»` → ТО `custom: «нестача праці гальмує виробництво»`; працю дають доми.
- КОЛИ `counter(qualified_work, >=, q)` → ТО `unlock(advanced_buildings)` (unblock: глобальна змінна ≥ q або N будівель типу).
- КОЛИ `custom: «збудовано ратушу рівня k»` → ТО `choose(policies)` — політики з плюсом і мінусом (сільські школи, …); повторно не сумуються.
- КОЛИ `tick` → ЯКЩО `custom: «жителі нещасні довго»` → ТО `custom: «перестають працювати й виїжджають»`.
- Гроші: нема — `currency` не вживається; ресурси й праця — єдина економіка.
- Перемога (?) — завершити цілі «шляху» мапи (Wealth: 4 вілли; Leisure: 2 вілли; 20+ парків до вілл → шлях Leisure) · Поразка: нема, лише виснаження ресурсів · Рахунок: нема.

## Керування і ввід
- Миша й клавіатура, без геймпада (на старті).
- Обрати будівлю в меню категорій → навести (жовте й синє кола радіусів `drawRange`, `drawRange2`) → клік; дороги й мости — протягнути лінією; ферми й житло — зоною.
- Знести будівлю — інструмент (?); дорога-інструмент ставить і поверх наявного, якщо будівля має `replaces` (зупинка — поверх дороги).
- Перемикач камери на рівень вулиці.

## Вікна, меню, HUD
- `game-screen`: воксельне місто; верхня смуга ресурсів і праці (`status-panel`); при виборі будівлі — `+ui:range-rings` (жовтий і синій радіуси), `tooltip` з вимогами.
- `tutorial-window`: текстові діалоги в правому нижньому куті, механіки відкриваються поступово.
- `+window:policy-window` — вибір політик із плюсами й мінусами, рівні 0–3 від ратуші.
- `main-menu` → вибір мапи-біому й розміру (`match-setup`) → `game-screen`; `settings-window`; `save-slots`.
- Режим першої особи — окремий вид того самого `game-screen`.

## Фічі поза полем
- `mod-support`: JSON-файли будівель (умови, апгрейди, ресурси, моделі), власні 3D-моделі.
- `autosave` / `cloud-save` (GOG: хмарні збереження).
- `tutorial` і `onboarding-hints` у перших кроках.
- 5 мап-біомів з різними ресурсами (Archipel — рибальство й туризм; Ruins — мародерство їжі й заліза; Desert — водна мережа).

## Варіації й родичі
- **Осі варіацій «сусідство як умова»:** очки за сусідів у момент розміщення ([islanders](islanders.md)) · бонус виробництва від сусідніх гексів ([civ6-districts](civ6-districts.md), [before-we-leave](before-we-leave.md)) · **будівля стає іншою будівлею** (Urbek, [loop-hero](loop-hero.md)) · житло росте від покриття сервісами ([caesar-3](caesar-3.md), [pharaoh](pharaoh.md)).
- **Осі «перевірка умови»:** кількість будівель типу в радіусі (≥ / ≤) · сума локальної змінної в радіусі · сусідство впритул · відстань до дороги.
- **Осі «деградація»:** лишається як є · нетрі / бунтарі / покинута (Urbek) · зникає.
- Родичі: [cities-skylines-zoning](cities-skylines-zoning.md) (зони ростуть самі), [simcity-1989](simcity-1989.md) (забруднення знецінює землю), [townscaper](townscaper.md) (вигляд від сусідів — тут ще й функція), [anno-1800-service-roads](anno-1800-service-roads.md); Concrete Jungle — порівняння з оглядом RPS (за Wikipedia); Urbek City Builder 2 — заявлений сиквел (?).

## Цікавинки для курсу
- Перевірка `buildingsNeeded`: «≥/≤ q будівель типу X у радіусі r» по сітці — 🌱; той самий двіжок для ресурсів і локальних змінних — 📎.
- Апгрейд за списком пріоритетів: перший тип зі списку, чиї умови виконано, — 📎 (дані в JSON, без `if` на кожну будівлю).
- Каскад апгрейдів: черга «перевір сусідів після перетворення» до стабілізації — 🥉.
- Локальні змінні як поля над сіткою: кожна будівля додає ±значення в радіус, клітина бачить суму — 🥉 (оверлей забруднення в подарунок).
- Спеціалізація за контекстом: дім → рибальський / шахтарський / нетрі за тим, що поруч, — 📎.
- Розблокування за порогом глобальної змінної й «шляхи» цілей мапи — 🌱.
- Повний пазл «досягти маєтку з мінімумом ресурсів» з розвʼязувачем перебором — 🥇.

## Мапа на каталог
- Є: `cursor-place` · `hover-highlight` (радіуси при наведенні) · `coverage-area` (радіус дії будівлі) · `multi-cell-size` (2×2, 3×3) · `cell-transform` (будівля → інша будівля) · `chain-reaction` (каскад апгрейдів кварталу) · `impassable-cells` (заборонені біоми) · `tutorial-window` · `save-game`.
- Перевикористано з корпусу: `+house-evolution`, `+influence-map` (локальні змінні), `+labor-pool`, `+zone-paint`, `+drag-build-line`, `+context-tile-rules` (вигляд дороги за перехрестям), `+placement-requirement`, `+first-person-view`, `+mod-support`.
- **Нема** → пропозиції карток:
  - `+radius-requirement` «Будівля вимагає ≥/≤ q будівель типу в радіусі r» · entities/legality · 🌱 · слоти {type, radius, q, op}.
  - `+upgrade-priority-list` «Апгрейд у перший тип зі списку, чиї умови виконано» · game-logic · 📎 · слоти {targets[]}.
  - `+context-specialization` «Та сама будівля стає різними типами за оточенням» · entities/state · 📎.
  - `+downgrade-abandon` «Будівля без умов деградує / стає покинутою» · entities/state · 🌱.
  - `+resource-threshold-unlock` «Нові будівлі за порогом глобальної змінної» · game-logic/economy · 🌱.
  - `+policy-choice` «Політики з плюсом і мінусом» · game-logic · 🌱 · `+path-goals` «Цілі мапи гілками-шляхами» · game-logic/win · 📎 · `+no-money-economy` «Економіка лише ресурсів і праці» · game-logic/economy · 🌱.

## Пропозиції до словників
- `+cond:count_in_radius` — кількість будівель виду в радіусі (≥ / ≤); уже просили Islanders — тут ядро всієї гри.
- `+cond:local_var_in_radius` — сума локальної змінної (забруднення, зелені зони) в радіусі порівняно з порогом.
- `+ui:range-rings` — два кольорові радіуси дії при розміщенні/виборі.
- `+window:policy-window` — вибір політик міста (Urbek; Frostpunk має книгу законів).
- `+card:radius-requirement`, `+card:upgrade-priority-list`, `+card:context-specialization`, `+card:downgrade-abandon` — див. «Мапа на каталог».

## Джерела
- ⭐ [Steam: Urbek City Builder](https://store.steampowered.com/app/1411740/Urbek_City_Builder/) — без грошей, 30+ ресурсів, органічний ріст (2+ поверхи там, де густо й є базові сервіси), ринок біля ферм, університет ← ліцей ← школа, освіта відкриває будівлі, компроміси «промисловість ↔ якість життя», вигляд з вулиці; 13.07.2022, Windows.
- [Wikipedia: Urbek City Builder](https://en.wikipedia.org/wiki/Urbek_City_Builder) — без випадкових подій; апгрейд в інший тип за розміщенням; забруднення шкодить житлу; зони; пазл з кількості й відстаней; туторіал діалогами; Estudios Kremlinois / RockGame.
- [Urbek Modding: Placement](https://worive.gitbook.io/urbek-modding/in-depth-knowledge/structure-attributes/placement.md), [Upgrades & Abandon](https://worive.gitbook.io/urbek-modding/in-depth-knowledge/structure-attributes/upgrades-and-abandon), [Resources](https://worive.gitbook.io/urbek-modding/in-depth-knowledge/structure-attributes/resources.md), [Local Variables](https://worive.gitbook.io/urbek-modding/in-depth-knowledge/in-game-data-names/local-variables.md), [Biomes](https://worive.gitbook.io/urbek-modding/in-depth-knowledge/in-game-data-names/biomes.md), [Building names: Temperate](https://worive.gitbook.io/urbek-modding/in-depth-knowledge/in-game-data-names/building-names/map-0-temperate.md), [Availability & Unblock](https://worive.gitbook.io/urbek-modding/in-depth-knowledge/structure-attributes/availability-and-unblock.md), [Policy](https://worive.gitbook.io/urbek-modding/in-depth-knowledge/structure-attributes/policy.md), [Appearance](https://worive.gitbook.io/urbek-modding/in-depth-knowledge/structure-attributes/appearance.md) — формат даних будівлі: умови в радіусі, пріоритет апгрейдів, виробництво на клітину, 28 локальних змінних, 24 біоми, 188 будівель, розблокування, рівні політик, радіуси на екрані.
- [TheGamer: best layouts](https://www.thegamer.com/urbek-city-builder-best-layouts-farms-mining-fishing-mansions-villas-wind-orchards/) — відстані в клітинах для шахтарів, рибалок, вілл, ферм, доріг; шляхи Wealth / Leisure.
- [Ladies Gamers](https://ladiesgamers.com/urbek-city-builder-review/), [KeenGamer](https://www.keengamer.com/articles/reviews/pc-reviews/urbek-city-builder-review-a-beginners-guide-to-city-planning/), [Kotaku](https://kotaku.com/new-city-building-game-is-all-about-the-voxels-1849325917) — огляди: хатина → сільський дім, нетрі й бунтарі, каскад кварталу, «кілька будинків разом — вілла, парк посередині — кондо».
- [GOG](https://www.gog.com/game/urbek_city_builder) — опис; з відгуків: 5 мап-біомів, «шлях» цілей, шанс апгрейду.

## Непевне
- (?) Модель часу: чи є пауза і прискорення, як часто перевіряються апгрейди — у джерелах лише «має шанс автоматично апгрейднутись».
- (?) Чи вичерпуються ліси й руда фізично (клітина зникає) чи лише запас — Steam каже «не виснажте природні ресурси», механізм не описано.
- (?) Перемога: «шляхи» Wealth / Leisure / Productivity і їх завершення — з відгуку на GOG і гайду TheGamer, офіційного опису нема.
- (?) Розробник: Wikipedia і GOG — Estudios Kremlinois, у моїй вибірці Steam — Fridus; платформи — Windows; версія для Switch (згадка в TouchArcade) не перевірена.
- (?) Інструмент знесення й радіуси сервісів у клітинах — не бачив у джерелах.
- (?) Сиквел Urbek City Builder 2 — лише назва в результатах пошуку.
