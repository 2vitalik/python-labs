---
title: BattleTech
slug: battletech
aka: [BattleTech (2018), HBS BattleTech, BattleTech (настолка 1984), BattleDroids]
family: tactics
also: []
klass: figure
axes:
  field: hex
  time: turn
  opponent: ai
  info: hidden
  random: both
  goal: state
year: 2018
platforms: [PC, macOS, Linux, board (1984)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/BattleTech_(video_game)", best: true, note: "ланс із 4 мехів, шасі/зброя/броня/актуатори, навички пілотів, показ шансу, DLC Flashpoint/Urban Warfare/Heavy Metal"}
  - {kind: wiki, url: "https://www.sarna.net/wiki/BattleTech_(Video_Game)", note: "Sarna: ускладнення місій, найманецька компанія, переговори про гроші/салвідж, Career mode 1200 днів"}
  - {kind: other, url: "https://leetguides.blogspot.com/2018/05/battletech-general-gameplay-tactics.html", note: "гайд механік: ініціатива за вагою, резерв, нагрів, перенос шкоди по частинах, evasion, stability, brace, guarded, jump у тил"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=BattleTech", note: "пошук Steam"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=BattleTech+2018+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [hp-damage, melee-vs-ranged, line-of-sight-attack, orientation-state, height-levels, floor-types, destructible-blocks, status-effects, unit-xp-skills, inventory, inventory-limit, interaction-table, reinforcements, fog-of-war, reachable-highlight, path-preview, threat-range, destroy-all-enemies, ai-opponent, online-multiplayer, shop-catalog, round-currency, save-multi-slot, map-window, placement-screen, character-select, +initiative-by-weight, +heat-system, +hit-locations, +damage-transfer, +facing-arcs, +evasion-pips, +stability-knockdown, +called-shot, +hit-chance, +salvage, +unit-loadout-editor, +morale-abilities, +sensor-lock]
proposes: ["+trigger:attacked", "+trigger:overheat", "+cond:facing_arc", "+cond:heat", "+effect:knockdown", "+effect:shutdown", "+effect:transfer_damage", "+effect:reserve", "+effect:vent_heat", "+ui:heat-bar", "+ui:paper-doll", "+ui:hit-chance", "+ui:evasion-pips", "+ui:stability-bar", "+ui:initiative-tracker", "+window:mech-lab", "+window:contract-negotiation", "+window:salvage-select", "+window:starmap", "+role:location", "+feature:career-mode"]
author: opus
date: 2026-11-09
---

# BattleTech — гігантські мехи на гексах: кожна частина корпусу має свою броню, а кожен постріл гріє

## Суть
Гравець веде **ланс** із чотирьох бойових мехів пілотів-найманців. Мех — не одна смужка HP, а набір **частин** (голова, торси, руки, ноги) зі своєю бронею й структурою; втрата руки забирає зброю на ній, втрата ноги валить меха. Кожен постріл додає **нагріву**: перегрів шкодить і може вимкнути меха, тому залп «усім» — рішення, а не дефолт. Між боями — найманецька компанія: контракти, переговори про гроші/салвідж, ремонт і збірка мехів у мехлабі.

## Поле і час
- Гексова сітка на 3D-карті з висотами; кожен мех займає гекс, має **напрям** (фронт / бік / тил) і може повертати торс.
- Ландшафт: ліс/укриття (зменшення шкоди), вода (кращий тепловідвід), висота (бонус точності), зруйновані будівлі (Urban Warfare блокує огляд).
- Раунд розбитий на **фази ініціативи** за ваговим класом: легкі мехи діють раніше, штурмові й турелі — в останній фазі (1); у межах фази гравець і ШІ чергуються (?).
- Видимість: сенсори й лінія огляду; ворог поза зором — маркер-«блип» (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Мех (light/medium/heavy/assault) | piece | тоннаж, клас ініціативи, рух, jump jets, тепловідвід | рухається, стріляє, бʼє в ближньому; має частини й нагрів |
| Частина меха (Head, CT, LT, RT, LA, RA, LL, RL) | piece | броня + внутрішня структура, слоти | приймає влучання; знищена → шкода переходить далі, зброя на ній втрачена |
| Пілот (MechWarrior) | ally | Gunnery, Piloting, Guts, Tactics, HP | навички дають точність, стабільність, поріг нагріву, ініціативу, вміння |
| Зброя: балістика / енергетика / ракети / підтримка | object | шкода, нагрів, дальність, набої, стабільна шкода | балістика й ракети — набої (вибухають у знищеній частині (?)); енергетика — більше нагріву |
| Heat sink | object | тепловідвід | знижує нагрів щоходу |
| Ворожий мех / техніка / турель | enemy | — | ті самі правила; техніка й турелі — простіші цілі |
| Укриття / ліс | terrain | −25 % шкоди | шкода менша, рух дорожчий |
| Вода | terrain | + ефективність охолодження | краще тепловідвід |
| Будівля | object | HP | руйнується, блокує огляд |
| Артобстріл | hazard | зона | місії з артилерією: небезпечні зони |
| Точка висадки / мета місії | zone | — | старт лансу; захоплення/оборона/евакуація |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `phase_start(n)` → ТО `custom: «діють юніти з ініціативою n; у межах фази гравець і ШІ по черзі»`; фази від вищого числа до 1.
- Резерв: КОЛИ `input(reserve, mech)` → ТО `custom: «мех переходить у пізнішу фазу»`, `custom: «зберігає evasion/guarded з минулого ходу; −1 поділка стабільної шкоди»`.
- Рух: КОЛИ `input(move|sprint|jump, mech, hex)` → ТО `move`, `custom: «evasion +k за пройдену відстань»`; sprint — без пострілу і без brace; jump ігнорує ландшафт і поворот, дає нагрів.
- КОЛИ `input(fire, mech, target, weapons)` → ЯКЩО `line_of_sight(mech, target)` і `in_range(mech, target, range)` → ТО `counter(heat, +Σ нагріву зброї)` і для кожної зброї: ЯКЩО `prob(hit)` → ТО `damage(location, n)`.
- Шанс влучання: `custom: «база від Gunnery − evasion цілі (кожен пип) ± висота ± укриття ± пошкодження сенсорів»`; КОЛИ атака по цілі → ТО `counter(evasion, −1)` незалежно від влучання.
- Локація: КОЛИ влучання → ТО `custom: «частина обирається за таблицею, залежною від дуги атаки (фронт/бік/тил)»`; з тилу — по задній броні центру/боків торса.
- КОЛИ `custom: «броню частини вичерпано»` → ТО `custom: «шкода йде в структуру»`; КОЛИ структура = 0 → ТО `disappear(location)` і втрата зброї на ній; далі `custom: «перенос: рука/нога → бічний торс → центральний торс»`.
- КОЛИ `destroyed(head|center_torso)` або `custom: «обидві ноги знищено»` → ТО `custom: «мех знищено»`; КОЛИ `custom: «пілот загинув»` → ТО те саме.
- Нагрів: КОЛИ `turn_end(mech)` → ТО `counter(heat, −heat_sinks)`; ЯКЩО `custom: «мех у воді»` → ТО охолодження більше.
- КОЛИ `counter(heat, >, overheat)` → ТО `damage(internal, n)` (?); КОЛИ `counter(heat, ≥, max)` → ТО `set_state(mech, shutdown)` — мех вимикається, лежить відкритим для прицільних пострілів.
- Стабільність: КОЛИ `custom: «влучання зі стабільною шкодою»` (ракети, ближній бій) → ТО `counter(stability, +n)`; ЯКЩО `counter(stability, ≥, unsteady)` → ТО `set_state(mech, unsteady)`, `custom: «втрачає всі evasion»`; далі → `custom: «knockdown»`.
- КОЛИ `destroyed(leg)` → ТО `custom: «гарантований knockdown»`; лежачий мех переходить пізніше в ініціативі й підводиться лише на своїй активації.
- Brace: КОЛИ `input(brace, mech)` → ТО `clear_state(mech, stability)`, `set_state(mech, guarded)` (−50 % шкоди) і `set_state(mech, entrenched)` (−50 % стабільної шкоди); не можна після sprint.
- Прицільний постріл: КОЛИ `input(called_shot, location)` → ЯКЩО `state(target, knocked_down|shutdown)` або `custom: «морал-вміння Precision Shot»` → ТО `custom: «вибір частини замість таблиці»`.
- Ближній бій: КОЛИ `input(melee, mech, target)` → ЯКЩО `adjacent(mech, target)` → ТО `damage`, `counter(evasion(target), −1)`; ігнорує evasion і guarded (?) у шансі.
- Sensor lock: КОЛИ `input(sensor_lock, mech, target)` → ТО `counter(evasion(target), −2)`, `reveal(target)`; замість пострілу.
- Мораль: КОЛИ `counter(morale, ≥, cost)` → ТО `custom: «Precision Shot (+20 % шансу) або Vigilance (як brace + тимчасово +1 ініціатива)»`.
- КОЛИ `custom: «боєприпаси в знищеній частині»` → ТО `explode(location)` (?).
- Місія: КОЛИ `custom: «мета контракту»` (знищити, захистити, евакуювати, захопити зону) → ТО `win`; КОЛИ `custom: «весь ланс знищено або відступ»` → ТО `lose`.
- Після бою: КОЛИ `win` → ТО `currency(+оплата)`, `choose(salvage)` за домовленою часткою; поранені пілоти лікуються днями.
- Кампанія: КОЛИ `custom: «день минає»` → ТО `currency(−утримання)`; Career mode — рахунок за 1200 днів.
- Перемога: виконати мету контракту · Поразка: загибель лансу, банкрутство (?) · Рахунок: Career mode — мехи, контракти, C-bills, апгрейди Argo, рівні пілотів.

## Керування і ввід
- Мишею: вибрати меха на його фазі → кнопки дій: Move · Sprint · Jump · Fire · Melee · Brace · Reserve · Sensor Lock · Morale.
- При русі — підсвітка досяжних гексів і вибір кінцевого напрямку (стрілка).
- Fire: список зброї з галочками (вмикати/вимикати окремі) і показ шансу на кожну; превʼю нагріву від залпу.
- Між місіями — клік по зоряній мапі (переліт), контракти (повзунки переговорів), мехлаб (drag зброї/броні в слоти).

## Вікна, меню, HUD
- `main-menu`: Campaign · Career · Skirmish · Multiplayer · Settings.
- `map-window` «Starmap» — системи, переліт, контракти на планетах.
- `custom-window` «Contract negotiation» — оплата ↔ салвідж ↔ репутація фракції.
- `placement-screen` / `character-select` «Lance configuration» — 4 мехи + пілоти, ліміт тоннажу місії.
- `custom-window` «MechLab» — паперова лялька меха: слоти, тоннаж, броня по частинах, тепловідвід.
- `custom-window` «Barracks» — пілоти, навички, найм.
- `game-screen`: поле; `turn-indicator` фаз ініціативи; панель меха (паперова лялька з бронею частин, шкала нагріву, стабільності, evasion-пипи); шанс влучання; `threat-range`; `fog-overlay` (?); `objective-text`.
- `end-screen` + `custom-window` «Salvage» — вибір частин/мехів трофеєм; `custom-window` «Travel event» — подія з виборами.
- Переходи: main-menu → Argo (корабель-хаб) → starmap → contract → lance config → бій → salvage → Argo.

## Фічі поза полем
- Режими: кампанія (Restoration, сюжетні + процедурні місії) · `+feature:career-mode` (1200 днів, рахунок) · Skirmish · `online-multiplayer`.
- Економіка: утримання, ремонт, переговори, салвідж; репутація з фракціями; апгрейди корабля Argo.
- Прогресія пілотів: дерево навичок (Gunnery, Piloting, Guts, Tactics) і вміння.
- DLC: Flashpoint (ланцюжки місій без ремонту між ними) · Urban Warfare (міста, руйнування, техніка) · Heavy Metal (нова зброя й мехи); моди (`mod-support`).
- `save-slots`, `difficulty-presets` (налаштування Career: ліміт часу, ironman (?)).

## Варіації й родичі
- Настолка BattleTech (FASA, 1984, BattleDroids): та сама модель — гекси, нагрів, таблиці влучань по частинах; ініціатива кидком кубиків, фаза руху → фаза стрільби (?).
- Родичі: MechWarrior (екшн-сим), MechCommander (RTS), [xcom](xcom.md) (шанс влучання, укриття), [jagged-alliance-2](jagged-alliance-2.md) (найманці й економіка), [battle-brothers](battle-brothers.md) (компанія між боями).
- **Осі варіацій**: HP — одна смужка / частини з бронею / броня + структура · ресурс залпу — AP / набої / нагрів · порядок — фази сторін / ініціатива за класом / таймлайн · напрям — нема / бік удару / торс окремо від ніг.

## Цікавинки для курсу
- Ініціатива за ваговим класом + резерв (відкласти себе в пізнішу фазу) — 📎.
- Нагрів як спільний ресурс зброї: тепловідвід щоходу, пороги перегріву й вимкнення — 🥉.
- Мех як набір частин з бронею і структурою, перенос шкоди по графу частин — 🥉 (граф як дані).
- Таблиця локацій за дугою атаки (фронт/бік/тил) — 🥉 (кут між гексами → дуга).
- Evasion-пипи від руху, що зриваються кожною атакою — 📎.
- Стабільна шкода → unsteady → knockdown → прицільні постріли — 🥉.
- Салвідж і переговори «гроші ↔ трофеї» — 📎.

## Мапа на каталог
- Є: `hp-damage` · `melee-vs-ranged` · `line-of-sight-attack` · `orientation-state` (напрям меха і торса) · `height-levels` · `floor-types` (ліс, вода) · `destructible-blocks` (Urban Warfare) · `status-effects` (shutdown, unsteady, guarded) · `unit-xp-skills` · `inventory` + `inventory-limit` (слоти й тоннаж мехлабу) · `interaction-table` (таблиця локацій) · `reinforcements` · `fog-of-war` · `reachable-highlight` · `path-preview` · `threat-range` · `destroy-all-enemies` · `ai-opponent` · `online-multiplayer` · `shop-catalog` (ринки систем) · `round-currency` · `save-multi-slot` · `map-window` · `placement-screen` · `character-select`.
- **Нема** → пропозиції карток:
  - `+initiative-by-weight` «Ініціатива за класом юніта + резерв» · game-logic/turns · 📎.
  - `+heat-system` «Нагрів від дій, тепловідвід, перегрів» · entities/state · 🥉 · слоти {поріг, max}.
  - `+hit-locations` «Частини юніта з окремою бронею» · entities/combat · 🥉.
  - `+damage-transfer` «Перенос шкоди по графу частин» · entities/combat · 📎.
  - `+facing-arcs` «Дуга атаки: фронт/бік/тил» · entities/combat · 🥉.
  - `+evasion-pips` «Ухилення від руху, що зривається атаками» · entities/state · 📎.
  - `+stability-knockdown` «Стабільна шкода і падіння» · entities/state · 📎.
  - `+called-shot` «Прицільний постріл по частині» · entities/combat · 🌱.
  - `+hit-chance` — спільна з XCOM.
  - `+salvage` «Трофеї після бою за часткою» · progression/economy · 📎.
  - `+unit-loadout-editor` «Збірка юніта в слоти з лімітом ваги» · progression · 🥉.
  - `+morale-abilities` «Спільна шкала моралі на вміння» · game-logic/economy · 🌱.
  - `+sensor-lock` «Підсвітити ціль без лінії огляду» · entities/combat · 🌱.

## Пропозиції до словників
- `+trigger:attacked` — ціль атакували (зрив evasion) — повтор із корпусу tactics.
- `+trigger:overheat` — нагрів перетнув поріг.
- `+cond:facing_arc` — атака з дуги (фронт/бік/тил) відносно напрямку цілі.
- `+cond:heat` — рівень нагріву порівняно з порогом.
- `+effect:knockdown` · `+effect:shutdown` · `+effect:transfer_damage` · `+effect:reserve` (відкласти себе на пізнішу фазу) · `+effect:vent_heat`.
- `+role:location` — частина складеної сутності зі своїм HP.
- `+ui:heat-bar` · `+ui:paper-doll` (схема частин з бронею) · `+ui:hit-chance` · `+ui:evasion-pips` · `+ui:stability-bar` · `+ui:initiative-tracker`.
- `+window:mech-lab` · `+window:contract-negotiation` · `+window:salvage-select` · `+window:starmap`.
- `+feature:career-mode` — кампанія з лімітом днів і підсумковим рахунком.

## Джерела
- ⭐ [Wikipedia: BattleTech (video game)](https://en.wikipedia.org/wiki/BattleTech_(video_game)) — ланс, кастомізація мехів, пілоти, показ шансу, DLC, дати.
- [Sarna: BattleTech (Video Game)](https://www.sarna.net/wiki/BattleTech_(Video_Game)) — ускладнення місій, компанія, переговори, Career mode 1200 днів, рахунок.
- [Leet Guides: general gameplay tactics](https://leetguides.blogspot.com/2018/05/battletech-general-gameplay-tactics.html) — ініціатива, резерв, нагрів і Guts, перенос шкоди, evasion, sensor lock, unsteady, brace/guarded/entrenched (50 %), укриття 25 %, jump у тил, Precision Shot +20 %, Vigilance.
- YouTube: пошук «BattleTech 2018 gameplay».

## Непевне
- (?) Номери фаз за класом (light 4 … assault 1) і чергування гравець/ШІ всередині фази — з пошукового зведення і памʼяті.
- (?) Пошкодження структури від перегріву, точні пороги нагріву, вибух набоїв у знищеній частині — з памʼяті.
- (?) Чи ближній бій справді ігнорує evasion у шансі — так каже гайд, перевірити в грі.
- (?) Поле справді гексове (видно гекси при русі) — з памʼяті; Wikipedia про сітку мовчить.
- (?) Ворог поза зором як «блип», ironman у Career, банкрутство як поразка — з памʼяті.
- (?) Настолка: порядок фаз (рух → стрільба → фізичні атаки → нагрів) — з памʼяті.
