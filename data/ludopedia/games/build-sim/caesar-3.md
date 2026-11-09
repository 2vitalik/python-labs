---
title: Caesar III
slug: caesar-3
aka: [Caesar 3, C3, Цезар III, Augustus (фан-рушій), Julius (фан-рушій)]
family: build-sim
also: []
klass: cursor
axes:
  field: iso
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: constraints
year: 1998
platforms: [PC, Mac]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Caesar_III", best: true, note: "ходоки-служби, рейтинги Culture/Prosperity/Peace/Favor, кар'єра peaceful/military, City Construction Kit, радники"}
  - {kind: other, url: "https://caesar3.heavengames.com/", note: "HeavenGames: будівлі, юніти, кварталові блоки 7×7 і 9×9"}
  - {kind: other, url: "https://caesar3.heavengames.com/units/civilians/", note: "список цивільних ходоків: префект, інженер, торговець ринку, банщик, актор, збирач податків"}
  - {kind: other, url: "https://caesar3.heavengames.com/strategy/housing/", note: "кварталові блоки під ходоків (7×7, 9×9, «одна довга дорога»)"}
  - {kind: other, url: "https://www.caesar3augustus.com/book/engineeringtransport/roads", note: "довідник Augustus: дім ≤2 клітин від дороги, ходок розвертається при перешкоді, дорога стає бруківкою з бажаністю"}
  - {kind: other, url: "https://www.alteredgamer.com/caeser-3/16884-guide-to-building-population-the-importance-of-roads-and-intersections/", note: "перехрестя і патрулі префектів/інженерів"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=Caesar+3", note: "пошук"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Caesar+III+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [cell-click, drag-drop-piece, hover-highlight, multi-cell-size, impassable-cells, round-currency, coverage-area, random-walk, chase-bfs, cell-transform, spawner-entity, enemy-waves, game-pause, save-game, save-multi-slot, map-window, minimap-radar, objective-text, status-panel, sequential-levels, difficulty-levels, in-game-editor, +walker-coverage, +house-evolution, +influence-map, +risk-meter, +labor-pool, +map-overlay, +town-builder, +drag-build-line, +ratings-goal, +god-mood]
proposes: ["+card:walker-coverage", "+card:house-evolution", "+card:risk-meter", "+card:labor-pool", "+card:ratings-goal", "+role:walker", "+window:advisor-window", "+ui:map-overlay", "+ui:rating-columns", "+trigger:month_start"]
author: opus
date: 2026-11-09
---

# Caesar III — місто живе тим, хто пройшов повз: служби розносять ходоки по дорогах, а не радіус будівлі

## Суть
Гравець-губернатор ставить на ізометричній сітці дороги, житло, водогони, ринки, храми, школи, префектури — і виконує умови провінції (населення + чотири рейтинги). Ядро — **ходоки** (walkers): будівля-служба випускає пішохода, він блукає дорогами, і кожен будинок, повз який він пройшов, отримує доступ до служби. Покриття = **пройдений шлях по графу доріг**, а не коло навколо будівлі; тому планування — це керування маршрутом блукання (мало перехресть, замкнені квартали-блоки). Будинки самі еволюціонують (намет → вілла → палац (?)) або деградують, коли доступ зникає.

## Поле і час
- Одна мапа міста (на відміну від Caesar II з мапою провінції і міста) — квадратна сітка в ізометрії; рельєф: річки, родючі землі, ліси, скелі, рудники — непрохідні або з ресурсом (`random: setup` у кар'єрі не випадковий, мапи задані).
- Шари: тайл (трава/вода/скеля/дорога) · будівля N×N (1×1 до 5×5 (?)) · ходоки на дорозі · невидимі поля: бажаність (desirability), ризик пожежі/обвалу кожної будівлі, покриття служб у кожного будинку.
- Час — real-time, ігровий календар місяцями; рейтинги й податки рахуються помісячно/щорічно (?). Регулятор швидкості гри.
- Камера — ізометрична, повороти виду (?); мінімапа й **оверлеї** (вода, пожежа, ушкодження, злочинність, освіта, здоровʼя тощо).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Дорога / бруківка | terrain | — | граф пересування ходоків; ґрунтова сама стає бруківкою з ростом бажаності поруч |
| Площа (plaza) | terrain | дорога | дорога, що піднімає бажаність навколо |
| Будинок | object | рівень, мешканці, потреби, бажаність | ≤2 клітин від дороги; росте (`transform` у вищий рівень) при виконанні потреб, деградує при втраті |
| Будівля-служба (префектура, інженерний пост, храм, школа, лікар, баня, театр, ринок…) | spawner | працівники, дорога-доступ | випускає ходока, лише якщо має працівників і торкається дороги |
| Ходок-служба, блукаючий (префект, інженер, торговець ринку, банщик, актор, жрець, учень, збирач податків) | neutral | макс. відстань (?) | іде дорогою, на перехресті обирає напрям, дійшовши межі — повертається; дає службу будинкам поруч з маршрутом |
| Ходок цільовий (візник, покупець ринку, рибальський човен) | neutral | вантаж, ціль | найкоротший шлях дорогами до цілі (склад, зерносховище, ринок) і назад |
| Найманець праці (labor seeker) (?) | neutral | — | блукає від робочої будівлі; якщо пройшов повз житло — будівля отримує доступ до робочої сили |
| Мігрант / бездомний | neutral | — | приходить з краю мапи до вільного житла; бездомний — після знесення/деградації дому шукає нове |
| Колодязь / фонтан | static | радіус | вода — **радіусом** (не ходоком); фонтан — від водогону |
| Резервуар + акведук | conduit | — | несе воду до фонтанів і бань; акведук перетинає дороги |
| Ферма, шахта, лісопилка, майстерня | object | працівники | виробляє; візник везе на склад/в майстерню |
| Зерносховище / склад | container | місткість | приймає й видає товари ходокам |
| Храм бога (5 богів) (?) | spawner | бог | задовольняє релігію; настрій бога → благословення/кари |
| Сенат / форум | spawner | — | податки, рейтинги |
| Форт, казарма, мури, ворота | object | — | військо; мури й ворота стримують загарбників |
| Загарбник, вовк, бунтар | enemy | HP | іде на місто, нищить будівлі |
| Пожежа / руїна | hazard | — | будівля з повним ризиком загоряється або обвалюється |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(build, cell)` → ЯКЩО `free(area)` and `has(city, denarii)` → ТО `place(building)`, `currency(-cost)`; інакше `block`.
- КОЛИ `input(drag_road, from, to)` → ТО `custom: «прокласти дорогу найкоротшою лінією з кутом»` (тягнеться лінією).
- КОЛИ `tick` → ЯКЩО `state(service_building, staffed)` and `custom: «торкається дороги»` → ТО `spawn_at(walker, adjacent_road)`.
- КОЛИ `tick` → ЯКЩО `state(walker, roaming)` → ТО `move(walker, road_next)`; на перехресті `custom: «обрати напрям (випадково / ще не пройдений (?))»`.
- КОЛИ `blocked(walker)` → ТО `custom: «розвернутись і йти назад»`.
- КОЛИ `counter(walker.distance, >=, max)` → ТО `custom: «повернутись до своєї будівлі»`, `disappear_a`.
- КОЛИ `in_range(walker, house, 2)` → ТО `set_state(house, has_service, decay_time)` — доступ до служби на час, доки ходок не прийде знову (?).
- КОЛИ `in_range(prefect, building, 2)` → ТО `set_value(building.fire_risk, 0)`.
- КОЛИ `in_range(engineer, building, 2)` → ТО `set_value(building.damage_risk, 0)`.
- КОЛИ `tick` → ТО `custom: «ризик пожежі й обвалу кожної будівлі зростає за її типом»`.
- КОЛИ `counter(building.fire_risk, >=, max)` → ТО `transform(building, fire)` → далі `transform(fire, ruins)`.
- КОЛИ `counter(building.damage_risk, >=, max)` → ТО `transform(building, ruins)`.
- КОЛИ `in_range(market_trader, house, 2)` → ЯКЩО `has(market, food)` → ТО `give(house, food)`; також глиняний посуд, олія, меблі, вино для вищих рівнів.
- КОЛИ `tick` → ЯКЩО `in_range(house, well|fountain, r)` → ТО `set_state(house, water)` — вода радіусом, контраст з ходоками.
- КОЛИ `tick` → ЯКЩО `custom: «виконано всі потреби наступного рівня»` and `custom: «бажаність ≥ поріг рівня»` → ТО `transform(house, next_level)`; більший дім вміщує більше мешканців.
- КОЛИ `tick` → ЯКЩО `not state(house, required_service)` → ТО `transform(house, prev_level)`; зайві мешканці стають бездомними.
- КОЛИ `transform(house, bigger)` → ЯКЩО `custom: «сусідні дома того ж рівня утворюють квадрат 2×2»` → ТО `merge(houses → 2×2 house)` (?).
- КОЛИ `timer(scan)` → ТО `custom: «бажаність клітини = сума внесків будівель у радіусі (сади, храми, статуї +; ферми, майстерні, склади −), спадає з відстанню»`.
- КОЛИ `tick` → ЯКЩО `custom: «найманець праці пройшов повз житло»` → ТО `set_state(workplace, has_labor)`; без нього будівля не працює.
- КОЛИ `input(order_goods, warehouse)` → ТО `custom: «візник везе найкоротшим шляхом до цілі»` (цільові ходоки ігнорують блукання).
- КОЛИ `timer(month)` → ТО `custom: «настрій кожного бога = f(кількість храмів, свята)»`; низький → кара (пожежа, мор, повінь (?)), високий — благословення.
- КОЛИ `timer(year)` → ТО `custom: «перерахувати рейтинги: Culture (покриття храмів/театрів/шкіл), Prosperity (зайнятість, якість житла, дохід), Peace (без шкоди від злочину/бунтів/вторгнень), Favor (вчасна данина й дари Цезарю)»`.
- КОЛИ `schedule(invasions)` → ТО `spawn_at(invaders, map_edge)` — на військових мапах.
- КОЛИ `rng(p)` → ЯКЩО `mode(peaceful)` → ТО `custom: «землетрус / пожежі — небезпеки мирних мап»`.
- КОЛИ `all_constraints_met` (населення + 4 рейтинги ≥ умов) → ТО `win` → наступна провінція кар'єри.
- КОЛИ `counter(favor, <=, 0)` (?) → ТО `custom: «Цезар надсилає легіони»` → `lose` при падінні міста.
- Рахунок: рейтинги й населення; City Construction Kit — без перемоги.

## Керування і ввід
- Миша: вибір будівлі з підменю за типами (Житло, Дороги, Вода, Здоровʼя, Релігія, Освіта, Розваги, Адміністрація, Інженерія, Безпека, Індустрія) → клік або drag для рядів (дороги, акведуки, стіни, ферми (?)).
- Інструмент знесення (clear land) рамкою; клік по будівлі — вікно з працівниками й станом; клік по ходоку — хто він і куди йде (?).
- Оверлеї вмикаються з меню: показують, які будинки мають доступ до служби/ризик.
- Регулятор швидкості гри, пауза, повороти мапи (?).

## Вікна, меню, HUD
- `main-menu`: Нова кар'єра (імʼя губернатора) · Завантажити · City Construction Kit · Вийти.
- `custom-window` вибору провінції: дві мапи-варіанти на кожному етапі — peaceful/military.
- `game-screen`: ізометричне поле + бічна панель (меню будівель, `minimap`, кнопки оверлеїв і радників) + верхній рядок: денарії, населення, дата.
- `custom-window` радників (`+window:advisor-window`): праця, військо, імперія, рейтинги, торгівля, населення, здоровʼя, освіта, розваги, релігія, фінанси, головний радник (зведення проблем).
- `map-window`: мапа Імперії — торгові шляхи, загрози вторгнень.
- Вікно будівлі (`custom-window`): працівники, запаси, стан; для дому — чого бракує до наступного рівня.
- `pause-menu`/меню файла: Зберегти · Завантажити · Налаштування · Вийти; `end-screen` провінції (перемога/звільнення).
- HUD: `coins` (денарії), `objective-text` (умови), `+ui:rating-columns` — стовпчики Culture/Prosperity/Peace/Favor з цілями; `+ui:map-overlay`; `tooltip`.

## Фічі поза полем
- `levels-sequential` + розгалуження кар'єри (peaceful/military), `difficulty-presets` (?), `save-slots`, `pause`, `speed-control`.
- `mode-sandbox` — City Construction Kit без умов перемоги.
- `level-editor` — офіційний редактор мап від Sierra (вибір загарбників, доступних будівель, рельєфу).
- Фан-рушії Augustus / Julius (відкриті реімплементації) — додають roadblock, широкий екран (?).

## Варіації й родичі
- Серія Impressions: Pharaoh (+ roadblock — блокує лише блукаючих), Zeus, Emperor; Caesar IV (3D). Augustus — фан-рушій з покращеннями.
- Родичі в корпусі: `simcity-1989` (покриття станцій — радіус і поля-карти), `prison-architect-rooms` (зони за розкладом), `mini-motorways` (дороги як граф), `factorio-belts` (зона живлення стовпа — радіус).
- **Осі варіацій «покриття службою»**: радіус від будівлі (SimCity, колодязь тут) / шлях ходока по графу (Caesar) / потік до цілі (візник) / заблоковані напрями (roadblock у Pharaoh).
- Осі «ріст житла»: поріг потреб / поріг бажаності / злиття сусідів у більший дім.

## Цікавинки для курсу
- Блукаючий ходок по графу доріг з лімітом довжини і поверненням — 📎 (BFS не потрібен, лише сусіди).
- Покриття «пройшов у межах 2 клітин» з таймером згасання — 🥉 (стан на будинку + повторні візити).
- Лічильник ризику пожежі/обвалу, який скидає патруль — 📎.
- Еволюція/деградація дому за списком потреб і полем бажаності — 🥈 (порогові рівні + гістерезис (?)).
- Поле бажаності як сума внесків з затуханням — 🥉.
- Цільовий ходок vs блукаючий (найкоротший шлях проти випадкового) і roadblock, що спиняє лише блукаючих — 🥉.

## Мапа на каталог
- Є: `coverage-area` (колодязь/фонтан — радіус) · `random-walk` (блукання ходока) · `chase-bfs` (цільовий ходок) · `cell-transform` (дім ↔ рівень, будівля → руїна) · `spawner-entity` (служба випускає ходока) · `multi-cell-size` · `impassable-cells` · `round-currency` (денарії) · `enemy-waves` · `map-window` + `minimap-radar` · `objective-text` + `status-panel` · `sequential-levels` · `in-game-editor` · `save-game`.
- **Нема** → пропозиції карток:
  - `+walker-coverage` «Служба розноситься ходоком по дорогах» · entities/move · 🥉 · слоти {max_distance, reach, decay}.
  - `+house-evolution` «Житло росте/деградує за потребами» · entities/state · 🥈 · слоти {levels, needs}.
  - `+risk-meter` «Лічильник ризику, що скидає патруль» · entities/state · 📎 · слоти {growth, reset_by}.
  - `+labor-pool` «Будівля працює, лише якщо до неї дійшла робоча сила» · game-logic/economy · 🥉.
  - `+ratings-goal` «Мета — кілька рейтингів ≥ порогів» · game-logic/score · 📎.
  - `+god-mood` «Настрій богів → благословення/кари» · game-logic · 📎.
  - `+influence-map`, `+map-overlay`, `+drag-build-line`, `+town-builder` — уже пропоновані іншими (SimCity, Factorio, Loop Hero).

## Пропозиції до словників
- `+card:walker-coverage`, `+card:house-evolution`, `+card:risk-meter`, `+card:labor-pool`, `+card:ratings-goal` — див. вище.
- `+role:walker` — сутність-посланець будівлі, що несе службу маршрутом (ходоки Impressions, жителі Mini Metro (?)).
- `+window:advisor-window` — радники: зведення стану міста за темами.
- `+ui:map-overlay` — шар-оверлей поля (як у SimCity); `+ui:rating-columns` — стовпчики рейтингів з позначкою цілі.
- `+trigger:month_start` — календарний тік (помісячні податки, настрій богів).

## Джерела
- ⭐ [Wikipedia: Caesar III](https://en.wikipedia.org/wiki/Caesar_III) — ходоки «проходять повз будівлі», рейтинги, кар'єра peaceful/military, City Construction Kit, радники, Empire map, редактор.
- [HeavenGames: Civilians](https://caesar3.heavengames.com/units/civilians/) — ролі ходоків (префект — злочин/бунти/пожежі; інженер — обвали; торговець ринку — маршрут з товарами; банщик блукає).
- [HeavenGames: Housing blocks](https://caesar3.heavengames.com/strategy/housing/) — блоки 7×7/9×9, «одна довга дорога».
- [Augustus handbook: Roads](https://www.caesar3augustus.com/book/engineeringtransport/roads) — дім ≤2 клітин від дороги, ходок при перешкоді розвертається, ґрунт → бруківка з бажаністю, площа.
- [AlteredGamer: Roads & intersections](https://www.alteredgamer.com/caeser-3/16884-guide-to-building-population-the-importance-of-roads-and-intersections/) — вибір напряму на перехресті, патрулі, візники.
- YouTube: пошук «Caesar III gameplay».

## Непевне
- (?) Правило вибору напряму на перехресті: випадково чи «ще не пройдений» — джерела розходяться (форуми кажуть «випадково», моя памʼять — пріоритет невідвіданого).
- (?) Довжина маршруту блукаючого ходока: AlteredGamer — «5 або 6 клітин» як грубе правило для патрулів; на мою памʼять — значно більше (десятки клітин).
- (?) Радіус обслуговування «2 клітини від маршруту», таймер згасання доступу, злиття домів у 2×2, кількість рівнів житла (≈20) і богів (5) — з памʼяті.
- (?) Найманці праці (labor seekers) як окремі ходоки і умова Favor → легіони — з памʼяті.
- (?) Roadblock у самому Caesar III відсутній (є в Pharaoh/Augustus); чи ворота мурів діють як roadblock — лише форумне твердження.
