---
title: Tiny Tower / SimTower
slug: tiny-tower-simtower
aka: [The Tower, SimTower: The Vertical Empire, Yoot Tower, The Tower II, Tiny Death Star, Tiny Tower Vegas]
family: build-sim
also: []
klass: cursor
axes:
  field: 1d
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: score
year: 1994
platforms: [PC, Mac, Saturn, 3DO, mobile]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Tiny_Tower", best: true, note: "Tiny Tower: житлові й 5 типів комерційних поверхів, біцизени й ліфт, мрії, VIP, coins і Tower Bux"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/SimTower", note: "SimTower: розріз хмарочоса, стрес мешканців, ліфти (стандартний ≤30 поверхів, експрес), зірки, 100+9 поверхів, події"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=SimTower+gameplay", note: "пошук; SimTower"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Tiny+Tower+gameplay", note: "пошук; Tiny Tower"}
stage: v1
coverage: 60
mechanics: [cell-click, drag-drop-piece, multi-cell-size, round-currency, spawn-random-cell, weighted-spawn, level-unlock, status-panel, objective-text, popup-text, save-game, save-autosave, game-pause, game-settings, shop-window, event-effects, progress-acceleration, +vertical-stack, +elevator-dispatch, +elevator-range-limit, +transfer-lobby, +rider-request, +tenant-stress, +star-rating-threshold, +timed-build, +restock-timer, +worker-assignment, +skill-match, +dream-job-match, +premium-currency-skip, +offline-progress, +day-schedule, +cost-scaling, +random-event]
proposes: ["+trigger:day_start", "+trigger:arrive", "+cond:reachable_by", "+cond:wait_time", "+effect:assign", "+effect:ride", "+effect:restock", "+role:resident", "+ui:floor-list", "+ui:speech-bubble", "+ui:stress-color", "+ui:star-meter", "+ui:clock-calendar", "+window:floor-detail", "+window:bitbook", "+axis:field=1d-stack", "+card:elevator-dispatch", "+card:tenant-stress", "+card:rider-request"]
author: opus
date: 2026-11-09
---

# Tiny Tower / SimTower — хмарочос як одновимірний стос поверхів, де ліфт — вузьке місце всієї економіки

## Суть
Гравець будує вежу в розрізі: поверх за поверхом заселяє житлом, офісами, магазинами, а люди мусять між ними пересуватись. **SimTower** (1994, Yoot Saito) — симуляція ліфтів: мешканці самі ходять за розкладом, і якщо ліфти не встигають, у них росте стрес і вони зʼїжджають; рейтинг зірок відкриває нові типи приміщень. **Tiny Tower** (2011, NimbleBit) — спрощена мобільна версія: поверх = одна клітина стосу, кожного мешканця («біцизена») гравець **сам** везе ліфтом на потрібний поверх, а економіка тримається на таймерах складу й продажу. Один файл — бо обидві ігри ставлять ту саму задачу на `1d`-полі.

## Поле і час
- **Поле — вертикальний стос**. SimTower: 100 поверхів над землею і 9 під, кожен поверх — горизонтальна смуга клітин, приміщення різної ширини (2D-розріз, але логіка руху — вертикальна лінія ліфтів). Tiny Tower: поверх = одна комірка, вежа росте лише вгору від лобі; горизонталі нема.
- **Транспорт — шахти**: стандартний ліфт SimTower охоплює до 30 поверхів, експрес — усю висоту; в Tiny Tower один ліфт уздовж усієї вежі.
- **Час**: real-time. SimTower — доба з робочими днями і вихідними, квартали (рента, події); Tiny Tower — реальні хвилини/години, прогрес іде, коли гра закрита.
- Камера: вертикальний скрол (Tiny Tower — свайп угору-вниз, швидкий перехід до поверху).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Поверх / приміщення | zone | тип, ширина (SimTower), рівень, місткість | дає дохід або житло; SimTower — вимоги (тиша, паркінг, сервіс) |
| Лобі | static | поверх 1; у SimTower ще пересадкові лобі (?) | вхід у вежу, тут зʼявляються відвідувачі |
| Ліфт (SimTower) | conduit | тип (стандарт / експрес / сервісний (?)), діапазон поверхів, кабіни | возить людей між поверхами своєї шахти; черги на зупинках |
| Сходи, ескалатор (SimTower) | conduit | 1 поверх (?) | короткий перехід без очікування |
| Ліфт (Tiny Tower) | conduit | швидкість (апгрейд) | везе одного пасажира, коли гравець тримає/тапає |
| Мешканець / офісний працівник (SimTower) | neutral | стрес, розклад, місце роботи/житла | ходить за розкладом; стрес росте від черг і поганих сусідів; високий — зʼїжджає |
| Біцизен (Tiny Tower) | neutral | 5 навичок 0–9 за категоріями, мрія-робота, житло | зʼявляється в ліфті з бульбашкою поверху; працює на комерційному поверсі |
| Відвідувач-пасажир (Tiny Tower) | neutral | бажаний поверх | після доставки дає coins або Tower Bux |
| Товар комерційного поверху (Tiny Tower) | resource | до 3 на поверх, один на працівника | склад поповнюється за час, продається сам |
| VIP (Tiny Tower) | neutral | тип (Big Spender, Celebrity, Construction Worker, Delivery Man, Real Estate) | разовий бонус; можна зберегти до 5 у лобі |
| Coins / Tower Bux | resource | — | coins — будівництво й склад; Bux — пришвидшення таймерів |
| Подія SimTower | hazard | бомба, пожежа (?), VIP-візит, золото під землею | випадкова; бомбу має знайти охорона, інакше шкода |
| Собор (SimTower) | static | верх 5-зіркової вежі | умова рейтингу «Tower» |

## Правила (КОЛИ → ЯКЩО → ТО)
Спільне:
- КОЛИ `input(build(floor_type))` → ЯКЩО `has(player, coins >= cost)` and `custom: «новий поверх ставиться згори стосу (Tiny Tower) / на вільну смугу поруч із транспортом (SimTower)»` → ТО `place(floor)`, `currency(-cost)`; ціна росте з висотою вежі.
- КОЛИ `custom: «поверх збудовано»` → ЯКЩО `custom: «таймер будівництва минув»` → ТО `set_state(floor, open)`; час будівництва росте з висотою (Tiny Tower).

SimTower:
- КОЛИ `custom: «мешканцю треба на інший поверх»` → ЯКЩО `custom: «є ліфт, що охоплює обидва поверхи»` → ТО `custom: «стати в чергу на зупинці»`; інакше `custom: «пересадка через поверх, де перетинаються шахти»` або `custom: «піти сходами, якщо 1 поверх»` (?).
- КОЛИ `custom: «довге очікування ліфта або погане сусідство»` → ТО `counter(stress, +n)` мешканця.
- КОЛИ `counter(stress, >=, high)` → ТО `custom: «орендар зʼїжджає, приміщення порожніє»`.
- КОЛИ `custom: «бракує сервісу (медцентр, паркінг, переробка, прибирання готелю)»` → ТО `counter(stress, +n)` у відповідних орендарів.
- КОЛИ `counter(population, >=, threshold)` → ЯКЩО `custom: «виконано вимоги рівня (напр., VIP-візит з добрим відгуком)»` → ТО `custom: «+1 зірка»`, `unlock(facility_types)`.
- КОЛИ `custom: «5 зірок і собор на вершині, усі поверхи над землею забудовано»` → ТО `custom: «рейтинг Tower»`.
- КОЛИ `rng(p)` → ТО `custom: «дзвінок про бомбу з викупом»`; ЯКЩО `custom: «відмовився платити»` and `not custom: «охорона знайшла бомбу вчасно»` → ТО `custom: «приміщення навколо вибуху зруйновано»`.
- КОЛИ `custom: «будівництво під землею»` → ЯКЩО `prob(p)` → ТО `currency(+big)` (знайдене золото).
- КОЛИ `custom: «кінець кварталу»` → ТО `currency(+rent)` від орендарів; кондо продається один раз.

Tiny Tower:
- КОЛИ `timer(every)` → ЯКЩО `custom: «у лобі нема пасажира»` → ТО `spawn_at(bitizen, elevator)` з бульбашкою цільового поверху.
- КОЛИ `input(ride(elevator))` → ТО `move(elevator, dir)`.
- КОЛИ `reach(bitizen, target_floor)` → ТО `custom: «пасажир виходить»`: на житловому з місцем — заселяється; на поверсі, що будується або поповнює склад, — `timer(-1 min)`; інакше — `currency(+tip)`.
- КОЛИ `input(assign(bitizen, floor))` → ЯКЩО `custom: «на поверсі < 3 працівників»` → ТО `custom: «працює; відкриває 1 товар»`; ЯКЩО `custom: «поверх = мрія біцизена»` → ТО `currency(+5 Bux)`.
- КОЛИ `input(restock(product))` → ЯКЩО `has(player, coins >= stock_cost)` → ТО `timer(start)`; по завершенні `counter(stock, +n)`.
- КОЛИ `tick` → ЯКЩО `counter(stock, >, 0)` → ТО `counter(stock, -1)`, `currency(+price)`; продаж іде й офлайн.
- КОЛИ `rng(p)` → ТО `spawn_at(vip, elevator)`; КОЛИ `input(use(vip))` → ТО ефект VIP (викупити склад / зробити роботу мрією / −3 год будівництва / заповнити склад / заселити поверх).
- КОЛИ `input(spend_bux(timer))` → ТО `custom: «таймер завершується одразу»`.
- КОЛИ `custom: «завдання (знайти біцизена/предмет)»` → ЯКЩО `input(tap(target_floor))` правильний → ТО `currency(+Bux)`.
- Перемога: нема (SimTower — рейтинг Tower як мета) · Поразка: нема (банкрутство в SimTower (?)) · Рахунок: гроші, населення, зірки.

## Керування і ввід
- SimTower (миша): вибрати інструмент приміщення → клік/drag по смузі поверху; ліфт — тягнути шахту вгору/вниз, додавати кабіни й налаштовувати зупинки (?); інспектор — клік по людині/приміщенню показує стрес і стан; швидкість часу.
- Tiny Tower (тач): тап «Up» везе ліфт (утримання — швидше) (?), свайп — скрол вежі, тап поверху — меню (склад, працівники, апгрейд), drag біцизена між поверхами.
- Обидві: будівництво з меню типів; підтвердження ціни.

## Вікна, меню, HUD
- `main-menu` (SimTower): Нова вежа · Завантажити · Налаштування.
- `game-screen`: розріз вежі; HUD — гроші як `coins`, населення, `star-meter`, `clock-calendar` (SimTower); Tiny Tower — coins, Bux, рівень вежі, кнопка ліфта, `speech-bubble` з цільовим поверхом.
- `tool-palette` (SimTower): типи приміщень, ліфти, сходи, знесення, інспектор.
- `floor-detail` (Tiny Tower): товари з таймерами, слоти працівників з навичками, кнопка апгрейду.
- `floor-list` / пошук біцизенів (Tiny Tower) · `bitbook` — стрічка повідомлень біцизенів.
- `shop-window`: Tower Bux, VIP, костюми (Tiny Tower).
- `stats-window` (SimTower): фінанси, населення, вимоги до наступної зірки (?).
- `settings-window` · `save-slots` (SimTower) / `autosave` (Tiny Tower).
- Переходи: game-screen ⇄ floor-detail / tool-palette / shop-window; події — модальні `message`.

## Фічі поза полем
- `autosave` і офлайн-прогрес (Tiny Tower), `save-slots` (SimTower).
- `speed-control` (SimTower: пауза і швидкості) · `pause`.
- Прогресія: зірки відкривають типи приміщень (`level-unlock`); Tiny Tower — нові поверхи з ростом вежі, костюми, VIP.
- Монетизація Tiny Tower: Tower Bux за реальні гроші як пропуск таймерів.
- Завдання/місії (Tiny Tower), події року (Санта в SimTower — без ефекту).

## Варіації й родичі
- Родичі в корпусі: [fallout-shelter.md](fallout-shelter.md) (сітка поверхів, ліфти, мешканці за навичками — найближчий нащадок), [prison-architect-rooms.md](prison-architect-rooms.md) (приміщення з вимогами), [theme-hospital.md](theme-hospital.md) (агенти між кімнатами). [tiny-towns.md](../board-digital/tiny-towns.md) — лише назва, не родич.
- Нащадки й клони: Yoot Tower / The Tower II (1998), The Tower DS, Project Highrise (2016), Tiny Death Star, Tiny Tower Vegas (казино й фішки), Lego Tower (2019).
- **Осі варіацій**: хто везе людей (симуляція ліфтів / гравець вручну) · ширина поверху (1 клітина / смуга) · ліфти (один на всю висоту / шахти з діапазоном і пересадками) · прогрес (таймери з пропуском за валюту / ігровий час) · мета (рейтинг / нескінченна).

## Цікавинки для курсу
- Tiny Tower-ліфт: стос поверхів як масив, пасажир з бульбашкою, доставка вручну — 🌱.
- Таймери складу й продажу з офлайн-прогресом (рахувати «скільки минуло» при запуску) — 📎.
- Призначення працівників за навичками 0–9 і бонус «мрія» — жадібний матчинг — 📎; оптимальний (угорський алгоритм) — 🥈.
- Симуляція ліфтів SimTower: черги на зупинках, алгоритм кабіни (SCAN/«ліфтовий»), стрес від очікування — 🥇.
- Маршрут з пересадками між шахтами з різним діапазоном (граф шахт, BFS) — 🥉.
- Пороги населення → зірки → відкриття типів приміщень — 🌱.

## Мапа на каталог
- Є: `cell-click` · `drag-drop-piece` · `multi-cell-size` (приміщення різної ширини) · `round-currency` · `spawn-random-cell` / `weighted-spawn` (біцизени, VIP) · `level-unlock` (зірки) · `status-panel` · `objective-text` (вимоги до зірки) · `popup-text` (+coins) · `save-game` / `save-autosave` · `game-pause` · `game-settings` · `shop-window` · `event-effects` · `progress-acceleration` (пропуск таймерів).
- **Нема** → пропозиції карток:
  - `+elevator-dispatch` «Кабіна обслуговує виклики за алгоритмом, черги на поверхах» · simulation/agents · 🥇 · слоти {кабін, діапазон, алгоритм}.
  - `+elevator-range-limit` / `+transfer-lobby` — шахта охоплює ≤ N поверхів, пересадки на лобі.
  - `+rider-request` «Пасажир з бажаним поверхом, гравець везе його сам» · entities/interaction · 🌱.
  - `+tenant-stress` «Стрес агента росте від очікування, при порозі — виїзд» · game-logic/agents · 🥉.
  - `+star-rating-threshold` «Пороги населення відкривають рівні» · progression · 🌱.
  - `+timed-build` · `+restock-timer` · `+offline-progress` · `+premium-currency-skip` — таймерна економіка мобільних ігор (родич `mobile-farm-timers`).
  - `+worker-assignment` · `+skill-match` · `+dream-job-match` — як у Fallout Shelter, + бонус «мрія».
  - `+vertical-stack` · `+day-schedule` · `+cost-scaling` · `+random-event`.

## Пропозиції до словників
- `+trigger:day_start` — початок доби/робочого дня (розклад мешканців) — уже пропонував Stardew; тут ще `+trigger:arrive` — агент прибув на ціль.
- `+cond:reachable_by` — поверх досяжний шахтою ліфта · `+cond:wait_time` — агент чекає довше за N.
- `+effect:assign` — призначити агента на роботу/житло · `+effect:ride` — везти ліфтом · `+effect:restock` — поповнити склад з таймером.
- `+role:resident` — агент-мешканець з потребами (не `neutral`, бо має стрес і виїжджає).
- `+ui:floor-list` · `+ui:speech-bubble` (бажання агента над головою) · `+ui:stress-color` · `+ui:star-meter` · `+ui:clock-calendar`.
- `+window:floor-detail` · `+window:bitbook` (внутрішньоігрова стрічка).
- `+axis:field=1d-stack` — стос поверхів (1d по вертикалі з шириною поверху).
- `+card:elevator-dispatch` · `+card:tenant-stress` · `+card:rider-request`.

## Джерела
- ⭐ [Wikipedia: Tiny Tower](https://en.wikipedia.org/wiki/Tiny_Tower) — поверхи (житлові + Food/Retail/Service/Recreation/Creative), біцизени з навичками 0–9 і мрією, ручний ліфт, VIP і їхні ефекти, coins/Tower Bux, спіноффи.
- [Wikipedia: SimTower](https://en.wikipedia.org/wiki/SimTower) — ліфти (стандарт ≤30 поверхів, експрес на всю висоту), стрес і сервіси, зірки, собор → Tower, 100+9 поверхів, бомба, золото, VIP, Санта, Yoot Tower.
- StrategyWiki (403) і fandom (402) не відкрились; YouTube — пошукові лінки.

## Непевне
- (?) Пороги населення для зірок SimTower, ширина приміщень, діапазон сервісного ліфта, сходи/ескалатори, пересадкові лобі кожні 15 поверхів — з памʼяті; Wikipedia не наводить.
- (?) Пожежі й таргани в SimTower — лише згадка з рецензії.
- (?) Місткість житлового поверху Tiny Tower, ріст ціни й часу будівництва, керування ліфтом утриманням — не перевірено.
- (?) Банкрутство як поразка в SimTower — не перевірено.
- (?) Перезапуск вежі (rebuild) і дах у Tiny Tower 2016 — Wikipedia не описує.
