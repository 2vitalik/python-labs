---
title: Where's My Water?
slug: wheres-my-water
aka: [WMW, "Де моя вода?", "Where's My Water? 2", "Where's My Perry?"]
family: dig-gravity
also: []
klass: cursor
axes:
  field: free
  time: realtime
  opponent: none
  info: full
  random: none
  goal: collect
year: 2011
platforms: [iOS, Android, Windows Phone, Windows, macOS, Kindle Fire, Flash]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Where%27s_My_Water%3F", best: true, note: "рідини та їх реакції, умови перемоги/поразки, качки, глави, режими Cranky/Allie/Mystery Duck"}
  - {kind: wiki, url: "https://simple.wikipedia.org/wiki/Where%27s_My_Water%3F", note: "таблиця глав: який елемент де зʼявляється; що вбиває качок"}
  - {kind: other, url: "https://gameyum.com/iphone-games/125571-wheres-my-water-review-and-game-guide-for-iphone", note: "гайд: перемикачі, труби, крани, засувки, бомби, водорості, колекції, відкриття глав"}
  - {kind: other, url: "https://www.pocketgamer.com/articles/037305/r/", note: "гайд Cranky's Story (бачив у пошуку)"}
  - {kind: other, url: "https://www.mobygames.com/game/55063/", note: "MobyGames (403 при відкритті)"}
  - {kind: other, url: "https://apps.apple.com/app/id449735650", note: "App Store (бачив у пошуку)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Where%27s+My+Water+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [dig-terrain, gravity-fall, cell-transform, interaction-table, button-toggle, impassable-cells, explode-area, collect-quota, item-pickup, environment-death, sequential-levels, level-select, level-unlock, world-map, event-points, time-bonus, save-progress, swipe-gestures, +fluid-particles, +fluid-contamination, +fluid-sink-goal, +bonus-from-overflow, +triple-collectible-set, +tilt-control, +duck-gated-chapters]
proposes: ["+trigger:fluid_reach", "+cond:fluid_type", "+cond:fill", "+effect:contaminate", "+effect:erode", "+role:fluid", "+window:collectibles-shelf", "+feature:iap-unlock", "+card:fluid-contamination", "+card:fluid-sink-goal", "+axis:control-carve"]
author: opus
date: 2026-11-09
---

# Where's My Water? — прокопай землю пальцем, і рідина сама потече у ванну крокодила

## Суть
Гравець не керує водою — він **прибирає землю**: пальцем прокопує канали, а рідина під гравітацією сама тече туди, де пусто. Ціль — довести достатньо чистої води до труби над ванною Swampy. Головна цікавинка — **кілька рідин, що реагують одна з одною**: отрута заражає воду, слиз (ooze) їсть землю, пара підіймається вгору, бруд висихає в землю, водорості пʼють воду і ростуть. Три гумові качки на рівні наповнюються водою — це «зірки» гри, які відкривають нові глави.

## Поле і час
- Вертикальний 2D-рівень на один екран (?) щодо скролу; шари: земля (стирається пальцем), камінь (непрохідний, не копається), рідини, механізми.
- Земля — растрова маска, що зникає під пальцем довільної форми; рідина — безліч крапель з фізикою, не сітка клітин (`field: free`).
- Real-time: рідина тече постійно; запас — обмежена калюжа або нескінченний потік із труби.
- Рівень закінчується, коли ванна набрала потрібне (перемога) або коли рідина вичерпалась / до труби дійшла шкідлива рідина (поразка).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Земля (dirt) | terrain | — | зникає під пальцем; ховає колекційні предмети; ooze її розʼїдає; бомба руйнує |
| Камінь (rock) | static | — | непрохідний, не копається |
| Чиста вода | object | обʼєм | падає й розтікається; росте водорості; від отрути/бруду сама стає ними |
| Отрута (poison, фіолетова; «acid» у гайдах) | hazard | — | перетворює воду на отруту; прибирає водорості; вбиває качок; дійшла до ванни → поразка |
| Слиз (ooze, зелений) | hazard | — | розʼїдає землю, лопає кульки, розчиняє воду й бруд; водорості → камінь (?); дійшов до ванни → поразка |
| Пара (steam) | object | — | летить угору замість падіння; у Allie's Story — живить орган |
| Бруд (mud, червонуватий) | object | — | поступово висихає в землю; вода/пара/отрута знову розмочують; дійшов до ванни → поразка |
| Водорості (algae) | hazard | — | вбирають воду і ростуть; отрута їх прибирає |
| Труба Swampy (вхід ванни) | sink | квота води | рахує чисту воду; шкідлива рідина → поразка |
| Труба-перехідник (pipe) | conduit | — | широкий кінець приймає рідину, вузький — вистрілює її з силою |
| Кран (faucet / tap) | source | нескінченний запас | вмикається натисканням; часто — щоб влучити в перемикач |
| Перемикач рідини (switch) | switch | — | дотик води/отрути вмикає/вимикає засувки й механізми |
| Засувка (gate / slider) | gate | — | пересувається пальцем або перемикачем; тримає чи пропускає рідину |
| Бомба | hazard | радіус | вибухає від рідини: руйнує землю й обʼєкти, вбиває качок, розбризкує рідину |
| Кулька (balloon) | object | — | лопається від ooze (глава «Stretched Thin»); є парові кульки (?) |
| Вентилятор / пилосос | zone | напрям | женуть або тягнуть рідину (глава «Caution to the Wind») |
| Клапан (valve) | switch | — | перенаправляє рідини (глава «Rising Tide») |
| Конвертер рідин | conduit | з → у | перетворює тип рідини (?) щодо видів |
| Гаряче вугілля, лід | terrain | — | глава «Boiling Point» (пара ↔ вода) (?) щодо поведінки |
| Гумова качка | pickup | порція води | зарахована, коли вбере достатньо води; отрута, бруд, ooze, бомба її вбивають |
| Колекційний предмет | pickup | — | захований у землі біля «найкращого шляху»; 3 однакові → бонус-рівень |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(swipe)` → ЯКЩО `cell(x, dirt)` → ТО `set_cell(x, empty)`; ЯКЩО `cell(x, rock)` → ТО `block`.
- КОЛИ `tick` → ЯКЩО `free(below)` → ТО `fall(water|poison|ooze|mud)`; інакше `custom: «розтікання вбік»`.
- КОЛИ `tick` → ТО `custom: «пара піднімається вгору»`.
- КОЛИ `contact(water, poison)` → ТО `transform(water → poison)`.
- КОЛИ `contact(water, mud)` → ТО `transform(water → mud)` — і навпаки: вода розмочує бруд.
- КОЛИ `timer(every)` → ЯКЩО `state(mud, still)` → ТО `transform(mud → dirt)` — висихання.
- КОЛИ `contact(ooze, dirt)` → ТО `set_cell(dirt, empty)` — розʼїдання.
- КОЛИ `contact(ooze, water|mud)` → ТО `disappear_b`; КОЛИ `contact(ooze, balloon)` → ТО `disappear_b`.
- КОЛИ `contact(ooze, algae)` → ТО `transform(algae → rock)` (?) — за Wikipedia; гайд каже «вбиває».
- КОЛИ `contact(poison, ooze)` → ТО `explode(area)`.
- КОЛИ `contact(water, algae)` → ТО `disappear_a`, `grow(algae)`; КОЛИ `contact(poison, algae)` → ТО `disappear_b`.
- КОЛИ `contact(fluid, switch)` → ТО `custom: «перемкнути засувки й механізми, привʼязані до перемикача»`.
- КОЛИ `input(tap, faucet)` → ТО `custom: «кран вмикається, нескінченний потік»`.
- КОЛИ `input(drag, gate)` → ТО `move(gate)`.
- КОЛИ `enter(fluid, pipe_wide)` → ТО `teleport(fluid → pipe_narrow)`, `speed(fluid, ×k)`.
- КОЛИ `contact(fluid, bomb)` → ТО `explode(area)`: земля й обʼєкти поруч зникають, качки гинуть.
- КОЛИ `contact(water, duck)` → ЯКЩО `custom: «вбрала достатньо»` → ТО `pickup`, `counter(ducks, +1)`.
- КОЛИ `contact(poison|mud|ooze, duck)` → ТО `disappear_b` (качку втрачено).
- КОЛИ `contact(finger, collectible)` (?) → ТО `pickup` — предмет відкопано.
- КОЛИ `counter(tub, >=, quota)` → ТО `win`; рахунок: `score` за час, качки й воду понад мінімум.
- КОЛИ `enter(poison|ooze|mud, inlet)` → ТО `lose`.
- КОЛИ `custom: «уся рідина вичерпалась / стекла, а квоти нема»` → ТО `lose`.
- Режими-заміни: Cranky's Story — отрута має розчинити водорості над їжею Cranky, качки фіолетові і беруть лише бризки отрути; Allie's Story — пара живить орган, качки сині й наповнюються лише парою, втрата пари = поразка.
- Перемога: квота в трубі · Поразка: шкідлива рідина у трубі, рідина скінчилась · Рахунок: час + качки + надлишок води (на гру не впливає).

## Керування і ввід
- Палець: провести по землі — стерти її смугою; натиснути на кран — увімкнути; потягнути засувку — зсунути.
- Бонус-рівні: нахил телефона рухає воду (`tilt`).
- Рестарт рівня й пауза — кнопками (?) щодо розміщення.

## Вікна, меню, HUD
- `main-menu`: Play → вибір історії (Swampy / Cranky / Allie / Mystery Duck) → `chapter-select` → `level-select`.
- `mode-select` — історії-персонажі; Cranky і Allie після перших 5 рівнів — платні.
- `level-select` — сітка рівнів глави з трьома качками на кожному.
- `game-screen`: рівень + лічильник качок + кнопка паузи (?).
- `end-screen` — ванна повна: качки, очки за час і воду.
- `collectibles-shelf` — полиця колекційних предметів: три в ряд → бонус-рівень.
- `shop-window` — покупка історій і Locksmith Duck (відкрити главу без качок).
- `achievements-window` — Game Center (50 знищених качок, 20 разів наповнити ванну отрутою/слизом).
- `pause-menu` — продовжити / рестарт / вийти (?).
- Переходи: level-select → game-screen → end-screen → наступний рівень або level-select.

## Фічі поза полем
- `levels-sequential`: на старті 4 глави по 20 рівнів; оновлення додали глави («Change is Good», «Boiling Point», «Caution to the Wind», «Rising Tide», святкові «Lost Levels»).
- `level-unlock` за качками: наступна група рівнів — після набору качок; повний набір колекцій глави дає +6 качок.
- `collectibles` → бонус-рівні; `achievements`.
- `stars-rating`-аналог: три качки на рівень.
- Платне розблокування: Locksmith Duck, історії Cranky/Allie.
- Режим Mystery Duck: Mega Ducks (потребують багато води), Ducklings (10 маленьких), Mystery Duck рухається по рівню.

## Варіації й родичі
- Сиквели й спін-офи: Where's My Water? 2 (2013), Where's My Perry?, Where's My Mickey? (?) — той самий двіжок рідин.
- Сімʼя: [dig-dug](dig-dug.md) і [boulder-dash](boulder-dash.md) — копання як прокладання шляху, але для себе; тут — для рідини; [the-powder-toy](the-powder-toy.md), [sandboxels](sandboxels.md) — реакції рідин без мети.
- Сусіди: Cut the Rope (той самий тип тач-фізики), Fluidity, Sprinkle (?).
- **Осі варіацій**: хто рухається — «аватар копає собі (Dig Dug) / гравець прокладає шлях речовині (WMW)»; рідини — «одна / кілька з реакціями»; ціль — «квота в стоці / наповнити підзадачі (качки) / уникнути забруднення».

## Цікавинки для курсу
- Клітинна вода + стирання землі мишею: прокласти канал до стоку — 🥉 (рідина як falling-sand-клітини).
- Таблиця реакцій рідин (вода + отрута → отрута, отрута + слиз → вибух, слиз їсть землю) — 📎.
- Стік з квотою й «отруєнням» — перемога за кількістю, поразка за типом — 🌱.
- Качки як підцілі, що вбирають порцію рідини — 🌱.
- Перемикачі, що їх тисне рідина, і засувки — 📎.
- Бруд, що висихає в землю за часом спокою — 📎.
- Розблокування глав за сумою «зірок»-качок + полиця колекцій — 📎.

## Мапа на каталог
- Є: `dig-terrain` ↔ стерти землю пальцем · `gravity-fall` ↔ рідини · `cell-transform` + `interaction-table` ↔ реакції · `button-toggle` ↔ перемикачі рідини · `impassable-cells` ↔ камінь · `explode-area` ↔ бомби · `collect-quota` ↔ ванна · `item-pickup` ↔ качки, колекції · `environment-death` ↔ загибель качок · `sequential-levels` · `level-select` · `level-unlock` · `world-map` (глави) · `event-points` + `time-bonus` · `save-progress` · `swipe-gestures`.
- **Нема** → пропозиції карток:
  - `+fluid-particles` «Рідина з безлічі крапель/клітин, що тече» · entities/move · 🥉.
  - `+fluid-contamination` «Рідина перетворює іншу при дотику» · entities/interact · 📎 · слот {from, to}.
  - `+fluid-sink-goal` «Стік з квотою й забороненими типами» · game-logic/win · 🌱.
  - `+bonus-from-overflow` «Очки за надлишок понад квоту» · game-logic/score · 🌱.
  - `+triple-collectible-set` «Три однакові колекції → бонус» · levels/progression · 🌱.
  - `+duck-gated-chapters` «Глави за сумою підцілей» · levels/progression · 🌱.
  - `+tilt-control` «Нахил пристрою як ввід» · interface/input · 📎.

## Пропозиції до словників
- `+trigger:fluid_reach(type, sink)` — рідина типу дійшла до стоку (ванна, орган).
- `+cond:fluid_type(a, t)` — тип рідини (вода, отрута, слиз, бруд, пара) — замість окремих сутностей.
- `+cond:fill(a, op, n)` — наповненість качки/ванни.
- `+effect:contaminate(a → b)` — рідина заражає іншу (отрута → вода), поширюючись дотиком.
- `+effect:erode(cell)` — рідина розʼїдає клітину рельєфу (ooze → земля).
- `+role:fluid` — рідина без форми, що тече (≠ `object`).
- `+window:collectibles-shelf` — полиця колекцій з наборами.
- `+feature:iap-unlock` — платне відкриття контенту.
- `+card:fluid-contamination` · `+card:fluid-sink-goal` — див. «Мапа на каталог».
- `+axis:control-carve` — значення осі `control`: гравець змінює рельєф, а не рухає сутність.

## Джерела
- ⭐ [Wikipedia: Where's My Water?](https://en.wikipedia.org/wiki/Where%27s_My_Water%3F) — рідини й реакції, перемога/поразка, качки й колекції, глави, Cranky/Allie/Mystery Duck, рахунок, платформи.
- [Simple Wikipedia](https://simple.wikipedia.org/wiki/Where%27s_My_Water%3F) — таблиця глав (крани, слайдери, перемикачі в трубах, парові кульки, вентилятори, вугілля, лід), загибель качок.
- [Gameyum: гайд](https://gameyum.com/iphone-games/125571-wheres-my-water-review-and-game-guide-for-iphone) — перемикачі, труби, крани, засувки, бомби, колекції, відкриття глав, нахил у бонус-рівнях, досягнення.
- [Pocket Gamer: Cranky's Story](https://www.pocketgamer.com/articles/037305/r/) — гайд режиму (у пошуку).
- YouTube: пошук «Where's My Water gameplay».

## Непевне
- (?) Ooze + водорості: Wikipedia — «перетворює на камінь», гайд — «вбиває».
- (?) «Поразка, коли вся вода стекла» — Wikipedia: «all water drains away»; точна умова (таймер, повна зупинка) невідома.
- (?) Поведінка гарячого вугілля, льоду, конвертерів і парових кульок — названі, але не описані.
- (?) Чи рідина — частинки з фізикою, чи сітка клітин; `field: free` — за враженням від гри.
- (?) UA-назва «Де моя вода?» — не перевірено; Where's My Mickey? і Sprinkle — з памʼяті.
- (?) Як саме підбирається колекційний предмет — відкопати чи дати воді торкнутись.
