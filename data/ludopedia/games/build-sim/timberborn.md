---
title: Timberborn
slug: timberborn
aka: [Тімберборн, «бобровий ситібілдер»]
family: build-sim
also: [dig-gravity]
klass: cursor
axes:
  field: 3d
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: survive
year: 2021
platforms: [PC, macOS]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Timberborn", best: true, note: "суть, фракції, вода/посухи/badwater, історія оновлень (3D-вода в Update 6)"}
  - {kind: fandom, url: "https://timberborn.wiki.gg/wiki/Fluids", note: "wiki.gg: модель течії, висота води від витрати, тиск, випаровування, колеса, помпи, баки"}
  - {kind: fandom, url: "https://timberborn.wiki.gg/wiki/Droughts", note: "сезони: помірний / посуха / badtide, тривалості за складністю, шанси серій"}
  - {kind: fandom, url: "https://timberborn.wiki.gg/wiki/Irrigation", note: "зрошення: −6 клітин радіуса за +1 висоти, поріг забруднення 50 %"}
  - {kind: fandom, url: "https://timberborn.wiki.gg/wiki/Floodgates", note: "шлюзи 1/2/3 рівні, крок 0.05, синхронізація сусідів"}
  - {kind: fandom, url: "https://timberborn.wiki.gg/wiki/Dam", note: "дамба 1×1 тримає воду до 0.65 блока, перелив зверху"}
  - {kind: fandom, url: "https://timberborn.wiki.gg/wiki/Beavers", note: "потреби, вік, робочі години, споживання їжі й води"}
  - {kind: steam, url: "https://store.steampowered.com/app/1062090", note: "сторінка гри (з черги, не відкривав)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=timberborn+water+dam+drought+gameplay", note: "пошук; дамби й посухи"}
stage: v1
coverage: 55
mechanics: [cursor-place, cell-click, hover-highlight, impassable-cells, height-levels, coverage-area, multi-cell-size, game-loop, game-pause, state-as-data, save-game, save-autosave, difficulty-levels, game-settings, field-scaling, status-panel, objective-text, mode-select, difficulty-select, tutorial-window, +fluid-network, +water-level-cell, +season-cycle, +irrigation-spread, +evaporation, +contamination-spread, +flow-power, +adjustable-gate, +vertical-stack, +terraform, +worker-assignment, +needs-wellbeing, +tech-tree, +overlay-view, +district-logistics, +faction-select]
proposes: ["+effect:flow", "+effect:spread", "+trigger:season_change", "+cond:height_diff", "+cond:powered", "+role:source", "+role:sink", "+ui:weather-forecast", "+ui:water-depth-overlay", "+window:faction-select", "+card:water-level-cell", "+card:season-cycle", "+card:irrigation-spread", "+card:adjustable-gate"]
author: opus
date: 2026-11-09
---

# Timberborn — бобровий ситібілдер, де головний ресурс — вода як рівень у кожній клітині, а ворог — сезон посухи

## Суть
Гравець веде колонію бобрів у світі після людей: ставить будівлі на сітці, рубає ліс, вирощує їжу й розподіляє роботу. Ядро — **вода як симульований рівень у клітинах 3D-сітки**: річка тече з джерел, дамби, дамби-вали (levee) й шлюзи тримають її, бо в посуху джерела замовкають. Вода зрошує землю навколо (зелень = можна садити), крутить водяні колеса й поїть бобрів. Пізніше — badwater (отруйна вода) і badtide, коли навіть чисті джерела дають отруту.

## Поле і час
- Мапа — 3D-сітка блоків: земля з висотами, будівлі ставляться на клітини і **одна на одну** (вертикальні шари: платформи, мости, акведуки, будівлі на дахах).
- Вода і земля з Update 6 (2024) / Update 7 (2025) — повноцінні 3D-симуляції (раніше 2D-висоти).
- Вода тече в **ортогональних** сусідів, де її менше або де нижче — гравітація плюс тиск; макс. непресована течія через блок ≈ 6.6 м³/с; симуляція йде на 0.5×: 1 м³/с наповнює блок за 2 с.
- Висота води на виході каналу ≈ 0.3 м на кожен м³/с витрати на клітину; угору за течією зростає ще ≈ 0.0015 м/(м³/с) на клітину — тому довгий канал переливається через стінку.
- Час — real-time з днями й годинами: бобри мають робочі години (16 за замовчуванням, 0–24), старіють щосвітанку.
- Цикл = помірний сезон + небезпечний (посуха або badtide); нова гра завжди починається з помірного.
- Камера вільна (обертання, зум); висотні шари можна «зрізати» для огляду (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Бобер (дорослий) | ally | вік, голод, спрага, сон, well-being | ходить 2.67 клітини/с; працює на призначеній роботі; гине без їжі/води |
| Кіт (бобреня) | ally | вік | не працює; дорослішає |
| Бот | ally | — | працює замість бобра; не заражається badwater |
| Джерело води | source | сила за сезоном | у помірний сезон дає чисту воду; у посуху мовчить; у badtide дає badwater |
| Джерело badwater | source | — | дає badwater, поки не закрите спецбудівлею (Iron Teeth) |
| Вода в клітині | terrain | глибина, витрата, забруднення % | тече до нижчих/менш повних сусідів; випаровується |
| Земля | terrain | висота, зрошена/суха/заражена | зрошена (зелена) — можна садити; заражена — рослини гинуть |
| Дамба | static | 1×1, тримає до 0.65 блока; 20 колод | блокує течію до своєї висоти, надлишок — через переливник зверху; по ній ходять |
| Вал (levee) | static | 1 блок | повністю блокує воду; з них будують канали й акведуки |
| Шлюз (floodgate) | gate | одинарний/подвійний/потрійний: 2/3/4 блоки висоти, хід 1/2/3 | висоту відсічки ставить гравець з кроком 0.05; сусідні шлюзи синхронізуються |
| Клапан (Fill / Throttling Valve) | gate | — | автоматично доливає резервуар / дроселює потік (пізня технологія) |
| Непроникна підлога | static | — | блокує вертикальну течію (дно акведука) |
| Помпа | sink | 3 од./год; −0.031 м³/с з потоку | качає воду з клітини поруч у сховище |
| Великий бак | container | 30 / 300 / 1200 од. (малий/середній/великий) | зберігає воду без випаровування |
| Водяне колесо | object | 270 к.с. на м³/с (велике — 540) | дає енергію пропорційно течії під віссю |
| Рослина / дерево | resource | стадія росту | росте лише на зрошеній землі; на зараженій живе 0.2–0.3 дня |
| Будівля виробництва | object | робочі місця, рецепт | перетворює ресурси; потребує бобрів і часто енергії |
| Житло | object | місткість | дає сон/дах |
| Склад | container | вид товару | тримає товари району |
| Перехід району (District Crossing) | gate | — | обмін товарами між районами |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ЯКЩО `custom: «сусід ортогонально нижчий або з меншим рівнем води»` → ТО `custom: «частина води перетікає в сусіда»` (пропозиція `+effect:flow`).
- КОЛИ `tick` → ЯКЩО `occupied(cell, levee)` → ТО `block`.
- КОЛИ `tick` → ЯКЩО `occupied(cell, dam)` and `custom: «рівень води < 0.65 блока»` → ТО `block`; інакше `custom: «надлишок переливається через верх»`.
- КОЛИ `input(set_height, floodgate)` → ТО `set_value(floodgate, height)`; КОЛИ `tick` → ЯКЩО `custom: «рівень води нижче висоти шлюзу»` → ТО `block`.
- КОЛИ `tick` → ЯКЩО `occupied(cell, impermeable_floor)` → ТО `custom: «вода не тече вертикально крізь клітину»`.
- КОЛИ `tick` → ЯКЩО `custom: «клітина з водою відкрита»` → ТО `custom: «випаровування; вузькі (1–2) канали втрачають більше»`; ЯКЩО `occupied(cell, tank)` → ТО ні.
- КОЛИ `custom: «джерело повністю замкнене»` → ТО `custom: «тиск росте з часом, ніколи не лопається»`; пресована вода піднімається трубою як у сполучених посудинах.
- КОЛИ `tick` → ЯКЩО `in_range(water, soil, n)` and `custom: «забруднення води < 50 %»` → ТО `set_cell(soil, irrigated)`; кожен +1 висоти на шляху зменшує радіус на 6 клітин, спуск — ні (пропозиція `+cond:height_diff`).
- КОЛИ `tick` → ЯКЩО `not custom: «клітина зрошена»` → ТО `custom: «рослини сохнуть і гинуть»`.
- КОЛИ `custom: «зміна сезону»` → ЯКЩО `state(season, drought)` → ТО `set_state(source, off)` (пропозиція `+trigger:season_change`).
- КОЛИ `custom: «зміна сезону»` → ЯКЩО `state(season, badtide)` → ТО `transform(source, badwater_source)`; забруднення 50 % → 100 % за 12 год, за 12 год до кінця падає до 50 %, у помірний — одразу 0 %.
- КОЛИ `contact(badwater, water)` → ТО `set_value(water, contamination↑)`; КОЛИ `counter(contamination, >, 50)` → ТО `set_cell(soil, contaminated)` і `custom: «рослини на ній гинуть за 0.2–0.3 дня»`.
- КОЛИ `enter(beaver, badwater)` → ЯКЩО `prob(p)` → ТО `set_state(beaver, contaminated)`; лікує Antidote (Folktails) / Extract (Iron Teeth); боти імунні.
- КОЛИ `tick` → ЯКЩО `in_range(water_wheel, flow, 0)` → ТО `custom: «енергія = 270 к.с. × витрата на клітину під віссю»`; звуження русла шлюзом/валом підвищує течію й енергію.
- КОЛИ `tick` → ЯКЩО `occupied(cell, pump)` and `cell(adjacent, water)` → ТО `counter(water_stock, +3/год)` і `custom: «з річки зникає 0.031 м³/с»`.
- КОЛИ `tick` → ЯКЩО `custom: «будівля потребує енергії»` and `not custom: «підключена до колеса/батареї»` → ТО `custom: «стоїть»` (пропозиція `+cond:powered`).
- КОЛИ `counter(hunger, <=, 0)` або `counter(thirst, <=, 0)` надто довго → ТО `disappear(beaver)` (смерть).
- КОЛИ `custom: «світанок»` → ТО `counter(age, +1)`; КОЛИ `counter(age, >=, 50±10%)` → ТО `disappear(beaver)` (смерть від старості).
- КОЛИ `state_on(beaver, need_met)` → ТО `counter(wellbeing, +n)`; КОЛИ `counter(wellbeing, >=, threshold)` → ТО `custom: «бонус до характеристик (швидкість, довголіття…)»`.
- КОЛИ `input(place, building)` → ЯКЩО `free(cell)` and `custom: «є опора знизу»` → ТО `place(player, building_site)`; бобри-будівельники носять матеріали й зводять.
- КОЛИ `input(dismantle, building)` → ТО `disappear(building)` і `custom: «частина ресурсів повертається»`.
- КОЛИ `counter(science, >=, cost)` and `input(research, tech)` → ТО `custom: «будівля/апгрейд розблоковано»`.
- КОЛИ `custom: «оголошено наступний небезпечний сезон»` → ТО `custom: «прогноз погоди показує попередження»`.
- Рахунок сезону: перша посуха/badtide за складністю — Easy 1/1, Normal 2–3/1, Hard 3–6/6–12 (дні); далі тривалість росте з випадковістю; серії однакових подій зсувають шанс (40 % badtide → 70 % після 5 посух поспіль → 100 % після 7).
- Перемога: нема (виживання й розвиток; кінцеві «Wonders»). Поразка: `custom: «загинули всі бобри»` (?).

## Керування і ввід
- Мишею: панель будівель за категоріями → клік/drag ставить привид будівлі на клітини; рядами — дороги, вали, дамби.
- Вибір будівлі → панель: кількість працівників, пріоритет, пауза, рецепт; у шлюзу — повзунок висоти.
- Терраформінг і знесення — окремими інструментами; рослини/дерева — інструментом позначення ділянки посадки чи рубки.
- Камера: обертання, зум, рух; шари висоти для огляду всередині споруд (?).
- Глобальні налаштування колонії: робочі години (0–24), розподіл районів, автоперерозподіл товарів.

## Вікна, меню, HUD
- `main-menu`: Нова гра → `custom-window` вибору мапи + `custom-window` фракції (Folktails / Iron Teeth) + `difficulty-select` (Easy/Normal/Hard або власні налаштування режиму) → `game-screen`; Продовжити / Завантажити (`save-slots`); `settings-window`; редактор мап (?).
- `game-screen`: 3D-поле; HUD — запаси товарів району (`status-panel`), населення/безробітні, `custom: «прогноз погоди»` (сезон + попередження), день/година, швидкість гри, кнопки категорій будівель.
- `custom-window` панель будівлі: працівники, стан, рецепт, витрата/енергія; у шлюзу — висота.
- Оверлеї (`custom-window`/режим поля): зрошення, глибина/течія води, енергомережа, райони (?).
- `custom-window` дерево досліджень (Science); `custom-window` well-being / потреби бобрів.
- `pause-menu`, `confirm-dialog` (знесення, вихід).

## Фічі поза полем
- `difficulty-presets` + `custom-difficulty` (тривалості й шанси посух/badtide за режимом гри).
- Дві фракції з різними будівлями: Folktails (зиплайни, Antidote) і Iron Teeth (тубвеї, розмноження в Breeding Pod, Extract, Badwater Pressurizer).
- `autosave`, `save-slots`; кілька районів/поселень на мапі з власними складами (Districts).
- Дослідження (Science) — дерево технологій; Wonders — дорогі кінцеві споруди.
- `mod-support` (офіційна підтримка модів з Update 6); 12 мап (Update 5 переробив усі).

## Варіації й родичі
- **Осі варіацій:** модель води (рівень у 2D-клітині → повний 3D-обʼєм з тиском) · джерело ворожості (сезон, а не вороги) · вода як ресурс-поле (зрошення радіусом) і як енергія (течія під колесом) · керування потоком (статичні дамби / регульовані шлюзи / автоматичні клапани).
- Родичі в корпусі: [oxygen-not-included-cells](oxygen-not-included-cells.md) (клітинні рідини з масою, бокова проєкція), [frostpunk](frostpunk.md) (виживання проти клімату), [stardew-farm](stardew-farm.md) (поливання клітин, сезони), [factorio-belts](factorio-belts.md) (рідинні мережі), [minecraft-redstone](minecraft-redstone.md) (вода, що розтікається на N блоків), [populous](populous.md) (терраформінг), [caesar-3](caesar-3.md) (водопостачання колодязями).
- Сусіди поза корпусом: Dwarf Fortress (рівень води 1–7 у клітині), From Dust, Banished.

## Цікавинки для курсу
- Вода як число 0..N у клітині + перетікання до нижчого сусіда (2D-висотна карта) — 🥉 (класичний «water level CA»; рівноважність і стабільність).
- Дамба/шлюз як клітина-поріг: тримає до висоти h, надлишок переливається — 📎 (одна умова поверх перетікання).
- Зрошення як BFS від води з вартістю підйому (радіус −6 за +1 висоти) — 🥉 (Дейкстра з вагою підйому; спуск безкоштовний).
- Сезонний цикл з випадковою тривалістю і «серіями», що зсувають шанс (40 → 70 → 100 %) — 📎.
- Забруднення як друге поле поверх води (змішування, поріг 50 %) — 🥈 (два зв'язані поля, наслідки на землю й рослини).
- Енергія з течії: колесо = k × витрата; звуження русла підвищує течію — 🥈 (потрібна модель витрати, не лише рівня).
- Повна 3D-рідина з тиском і сполученими посудинами — 👑.

## Мапа на каталог
- Є: `cursor-place` + `multi-cell-size` (будівлі на кількох клітинах) · `impassable-cells` (вали) · `height-levels` (висота рельєфу і «будівлі на будівлях») · `coverage-area` (радіус зрошення) · `game-loop` · `game-pause` · `save-game`/`save-autosave` · `difficulty-levels` + `difficulty-select` · `status-panel` (запаси) · `tutorial-window` · `field-scaling`.
- **Нема** → пропозиції карток:
  - `+water-level-cell` «Рівень рідини в клітині + перетікання до нижчого сусіда» · game-logic · 🥉 · слоти {max_level, flow_rate}.
  - `+season-cycle` «Сезони з випадковою тривалістю й попередженням» · game-logic/waves · 📎 · слоти {seasons, duration_range}.
  - `+irrigation-spread` «Зона дії від клітин-джерел з вартістю підйому» · entities/state · 🥉 · слоти {radius, climb_cost}.
  - `+adjustable-gate` «Регульований поріг (шлюз), який задає гравець» · entities/interact · 📎 · слоти {height_step}.
  - Перевикористано: `+fluid-network`, `+evaporation`, `+contamination-spread`, `+flow-power`, `+vertical-stack`, `+terraform`, `+worker-assignment`, `+needs-wellbeing`, `+tech-tree`, `+overlay-view`, `+district-logistics`, `+faction-select`.

## Пропозиції до словників
- `+effect:flow` — рідина перетікає в сусідню клітину (Timberborn, ONI, Minecraft-вода).
- `+effect:spread` — властивість поширюється на сусідні клітини (зрошення, забруднення).
- `+trigger:season_change` — зміна сезону/погоди.
- `+cond:height_diff` — різниця висот клітин (ціна підйому, перелив).
- `+cond:powered` — будівля отримує енергію.
- `+role:source` / `+role:sink` — джерело й споживач потоку (джерело води, помпа).
- `+ui:weather-forecast` — поточний сезон і попередження про наступний.
- `+ui:water-depth-overlay` — оверлей глибини/течії води.
- `+window:faction-select` — вибір фракції перед грою.
- `+card:water-level-cell`, `+card:season-cycle`, `+card:irrigation-spread`, `+card:adjustable-gate` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Timberborn](https://en.wikipedia.org/wiki/Timberborn) — розробник Mechanistry, фракції, дамби/зрошення/колеса, посухи й badwater, історія оновлень (3D-вода, 3D-земля), дати (EA 15.09.2021, 1.0 12.03.2026).
- [wiki.gg: Fluids](https://timberborn.wiki.gg/wiki/Fluids) — правило течії, формула висоти каналу, тиск, випаровування, помпи, баки, колеса.
- [wiki.gg: Droughts](https://timberborn.wiki.gg/wiki/Droughts) — сезони, тривалості за складністю, шанси серій, забруднення в badtide.
- [wiki.gg: Irrigation](https://timberborn.wiki.gg/wiki/Irrigation) — радіус і штраф висоти, поріг 50 %.
- [wiki.gg: Floodgates](https://timberborn.wiki.gg/wiki/Floodgates) · [Dam](https://timberborn.wiki.gg/wiki/Dam) · [Beavers](https://timberborn.wiki.gg/wiki/Beavers) — параметри споруд і бобрів.
- [wiki.gg: Water](https://timberborn.wiki.gg/wiki/Water) — вода як товар, 1 блок = 5 од.
- YouTube: пошук «timberborn water dam drought».

## Непевне
- (?) Умова поразки «загинули всі бобри» — у відкритих сторінках не описана.
- (?) Базовий радіус зрошення в клітинах — wiki дає лише штраф −6 за +1 висоти.
- (?) Механіка «зрізу» висотних шарів камери, набір оверлеїв і наявність редактора мап — з памʼяті, не перевірено.
- (?) Ймовірність зараження бобра в badwater — числа не бачив.
- (?) Одиниця тривалостей у таблиці складності (дні) — у джерелі одиниця не підписана явно.
- (?) Steam-лінк узято з черги, сторінку не відкривав.
