---
title: Two Point Hospital
slug: two-point-hospital
aka: [TPH, Лікарня Two Point]
family: build-sim
also: []
klass: cursor
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: constraints
year: 2018
platforms: [PC, macOS, Linux, PS4, Xbox One, Switch]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Two_Point_Hospital", best: true, note: "престиж кімнати від розміру й оздоблення, Kudosh, кваліфікації персоналу, привиди, епідемії й вакцини, зірки лікарень, DLC"}
  - {kind: steam, url: "https://store.steampowered.com/app/535930/Two_Point_Hospital/", note: "предмети підвищують престиж, кілька будівель, хвороби з власними машинами, дослідження"}
  - {kind: other, url: "https://steamcommunity.com/sharedfiles/filedetails/?id=1509294663", note: "гайд: бусти предметів додаються, золоті сертифікати → престиж, ~10 % діагнозу за прийом, щастя >80 % → +10 % до навичок"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Two+Point+Hospital+gameplay+room+prestige", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [multi-cell-size, impassable-cells, cell-click, drag-drop-piece, hover-highlight, chase-bfs, round-currency, spawn-schedule, game-pause, save-game, save-multi-slot, objective-text, status-panel, sequential-levels, level-unlock, world-map, leaderboard, +room-requirements, +room-blueprint, +room-grading, +diagnosis-pipeline, +queue-line, +agent-needs, +additive-room-buffs, +staff-qualifications, +meta-currency-unlocks, +multi-plot-expansion]
proposes: ["+role:visitor", "+effect:queue_join", "+ui:thought-bubble", "+window:research-window", "+window:staff-hire", "+window:training-window", "+feature:year-end-awards", "+card:additive-room-buffs", "+card:staff-qualifications", "+card:meta-currency-unlocks", "+card:multi-plot-expansion", "+card:room-grading"]
author: opus
date: 2026-11-09
---

# Two Point Hospital — Theme Hospital на новий лад: кімната з креслення, але її престиж і сила росте від розміру й кожного поставленого предмета

## Суть
Духовний наступник Theme Hospital від частини тієї ж команди: гравець креслить кімнати з обовʼязковими предметами, наймає й навчає персонал, проводить пацієнтів через GP → діагностику → лікування. Відмінності від `theme-hospital` і `prison-architect-rooms`: **престиж кімнати** — число від розміру й оздоблення, кожен предмет додає свій буст **адитивно**; діагностичні предмети (шафи з ліками, полиці) підсилюють силу діагнозу в кімнаті; **кваліфікації** для всіх працівників (включно з прибиральниками — «ловля привидів»); валюта **Kudosh** за виклики відкриває нові предмети; лікарня розростається на **кілька ділянок-будівель**; рівні — **1–3 зірки**, одна відкриває наступну лікарню.

## Поле і час
- Квадратна сітка всередині будівель ділянки; 3D-камера (?). Лікарня = кілька будівель, нові ділянки докуповуються.
- Шари клітини: підлога/стіна будівлі · кімната (прямокутник з дверима) · предмет N×M з поворотом · коридорний предмет · тепло від батарей (?).
- Real-time, календар місяцями; кінець року — церемонія нагород. Пауза, швидкості (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Кімната (креслення) | zone | тип, прямокутник ≥ мін., двері, престиж | діє з обовʼязковими предметами; престиж = розмір + оздоблення |
| Обовʼязковий предмет (стіл, ліжко, машина) | object | розмір, поворот | без нього кімната не відкривається |
| Буст-предмет (шафа з ліками, полиця-енциклопедія, анатомічна модель) | object | +n % (діагноз / навчання / престиж) | бусти одного виду додаються |
| Декор (рослина, постер, золотий сертифікат) | object | +престиж | сертифікат з нагород дає престиж |
| Предмети для персоналу (кавомашина, санітайзер, автомат солодощів) | object | — | закривають потреби персоналу в кімнаті |
| Коридорний предмет (лави, автомати, туалети, аркада) | object | — | закривають потреби пацієнтів у черзі |
| Машина лікування | object | міцність | одна хвороба — свій тип машини; зношується, ремонтує прибиральник |
| Пацієнт | neutral | хвороба, певність діагнозу, потреби, гроші | GP → діагностика до порогу → лікування; виходить з черги за потребою |
| Лікар / медсестра / асистент / прибиральник | ally | рівень, кваліфікації (слоти), риси, щастя | працює в кімнаті; щастя >80 % → +10 % до всіх навичок |
| Привид | enemy | — | лишається після смерті пацієнта; прибирає лише прибиральник з «Ghost Capture» |
| Ділянка-будівля | zone | ціна | докуповується, розширює лікарню |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag_room, type, rect)` → ЯКЩО `fits(rect, min_size)` і `free(rect)` → ТО `place(blueprint)`; інакше `block`.
- КОЛИ `input(confirm_room)` → ЯКЩО `has(room, required_objects)` → ТО `set_state(room, open)`, `currency(-cost)`.
- КОЛИ `input(place, item, room)` → ЯКЩО `fits(item, cells)` → ТО `place(item)`, `custom: «престиж кімнати += престиж предмета»`.
- КОЛИ `custom: «зміна розміру або оздоблення»` → ТО `custom: «перерахунок престижу: розмір + сума предметів»`.
- КОЛИ `tick` → ЯКЩО `custom: «престиж кімнати високий»` → ТО `custom: «щастя персоналу в кімнаті +»`; нещасні звільняються.
- КОЛИ `custom: «прийом у діагностичній кімнаті»` → ТО `counter(patient.certainty, +n)`; `custom: «n = база + сума бустів шаф/полиць у кімнаті»`.
- КОЛИ `counter(patient.certainty, >=, threshold)` → ТО `custom: «направлення на лікування»`; інакше — у наступну діагностику.
- КОЛИ `reach(patient, room)` → ТО `custom: «стати в чергу»`; ЯКЩО `custom: «голод/спрага/туалет/нудьга»` → ТО `custom: «вийти з черги й затримати кімнату»`.
- КОЛИ `custom: «лікування»` → ЯКЩО `prob(cure_chance)` → ТО `currency(+fee)`; інакше `custom: «пацієнт помирає»`, `spawn_at(ghost, room)`.
- КОЛИ `contact(janitor, ghost)` → ЯКЩО `has(janitor, ghost_capture)` → ТО `disappear_b`.
- КОЛИ `input(train, worker, qualification)` → ЯКЩО `custom: «є кімната навчання й вільний слот»` → ТО `custom: «кваліфікацію додано за N днів»`; кваліфікація посилює роботу у своєму відділенні (GP → кабінет GP).
- КОЛИ `custom: «виконано виклик»` → ТО `counter(kudosh, +n)`.
- КОЛИ `input(buy, item, kudosh)` → ТО `unlock(item)`.
- КОЛИ `input(buy_plot)` → ТО `custom: «нова будівля-ділянка доступна для забудови»`.
- КОЛИ `rng(p)` → ТО `custom: «епідемія»` → `give(player, vaccines: n)`; КОЛИ `custom: «усіх заражених щеплено»` → ТО нагорода; інакше −репутація.
- КОЛИ `schedule(emergency)` → ТО `spawn_at(patients, entrance)`, `timer(start)`; вилікувано >½ вчасно → бонус і +репутація.
- КОЛИ `timer(year)` → ТО `window(custom: «церемонія нагород»)` → золоті сертифікати (престиж кімнат).
- КОЛИ `counter(stars, >=, 1)` → ТО `unlock(next_hospital)`; 2–3 зірки — додаткові цілі. Рівень лікарні росте з кількістю кімнат і персоналу → більше пацієнтів і сильніші кандидати.

## Керування і ввід
- Миша: Build Room → категорія → drag прямокутника → двері → предмети (обовʼязкові відмічено) → Confirm; кімнату можна перемістити/розширити.
- Коридорні предмети — з каталогу; Hire → кандидати з рівнем і рисами → кинути на клітину.
- Клік по людині/кімнаті — вікно стану; навчання — вибрати працівника й кваліфікацію; ціни лікування, кредити.

## Вікна, меню, HUD
- `main-menu`: кампанія → `world-map` (лікарні як вузли зі зірками) · пісочниця · виклики/мультиплеєр · налаштування.
- `game-screen`: поле, нижня панель кнопок, гроші, дата, репутація; `objective-text` з цілями зірок.
- Вікно кімнати (`custom-window`): престиж, черга, персонал, бусти.
- Вікно людини: пацієнт — хвороба, певність, потреби (`+ui:thought-bubble`); працівник — рівень, кваліфікації, щастя.
- `+window:staff-hire`, `+window:training-window` (кваліфікації), `+window:research-window`, `shop-window` за Kudosh (?), `stats-window` (статистика й інформаційні екрани), `leaderboard` (асинхронні таблиці).
- `+feature:year-end-awards` — вікно церемонії.

## Фічі поза полем
- `levels-sequential` + `level-unlock` + `stars-rating` (1 зірка відкриває наступну, повернутись можна будь-коли), `world-map`.
- `mode-sandbox` (оновлення жовтня 2018); асинхронні online-таблиці й кооп/змагальні виклики; Superbug Initiative — спільнотні цілі.
- Steam Workshop: картини, стіни, підлоги. DLC з новими лікарнями й хворобами (Bigfoot, Pebberley Island, Close Encounters, Off the Grid, Culture Shock, A Stitch in Time).
- `save-slots`, `pause`.

## Варіації й родичі
- У корпусі: `theme-hospital` (база: креслення, GP → діагностика → лікування, вибух машин, тепло по тайлах), `prison-architect-rooms` (позначка зони, розклад), `rimworld-rooms` (якість кімнати за формулою).
- Two Point Campus (2022), Two Point Museum (2025) — та сама рамка (?).
- **Осі варіацій «якість кімнати»**: нема (Theme Hospital) / адитивна сума предметів + розмір (Two Point) / формула з мінімумом і ролями (RimWorld) · **«сила кімнати»**: фіксована / підсилюється предметами-бустами · **«персонал»**: навичка числом / слоти кваліфікацій з навчанням.

## Цікавинки для курсу
- Престиж кімнати = розмір + сума внесків предметів, оновлення при кожній зміні — 🌱.
- Бусти предметів в кімнаті, що додаються до сили дії (діагноз +n %) — 🌱.
- Конвеєр діагнозу з певністю й порогом направлення — 📎 (як у `theme-hospital`).
- Слоти кваліфікацій і навчання за дні — 📎.
- Метавалюта за виклики відкриває каталог предметів — 🌱.
- Черга, з якої агент виходить через потребу й блокує кімнату — 📎.

## Мапа на каталог
- Є: `multi-cell-size` · `impassable-cells` · `cell-click` + `drag-drop-piece` + `hover-highlight` · `chase-bfs` · `round-currency` · `spawn-schedule` (екстрені пацієнти) · `game-pause` · `save-game` + `save-multi-slot` · `objective-text` + `status-panel` · `sequential-levels` + `level-unlock` + `world-map` · `leaderboard`.
- **Нема** → пропозиції карток:
  - `+additive-room-buffs` «Предмети в зоні додають бусти до її дії» · entities/state · 🌱 · слоти {stat, per_item}.
  - `+staff-qualifications` «Слоти кваліфікацій агента + навчання» · game-logic · 📎.
  - `+meta-currency-unlocks` «Окрема валюта за виклики відкриває предмети» · game-logic/economy · 🌱.
  - `+multi-plot-expansion` «Докуповувані ділянки розширюють поле» · levels · 🌱.
  - `+room-grading` (престиж), `+room-requirements`, `+room-blueprint`, `+diagnosis-pipeline`, `+queue-line`, `+agent-needs` — пропоновані раніше, підтвердження.

## Пропозиції до словників
- `+role:visitor` — пацієнт як автономний клієнт (повторно).
- `+effect:queue_join` — стати в чергу (повторно, Theme Hospital, RCT).
- `+ui:thought-bubble` — потреба/думка над агентом.
- `+window:staff-hire`, `+window:training-window`, `+window:research-window`.
- `+feature:year-end-awards` — річна церемонія з сертифікатами, що дають престиж.
- `+card:additive-room-buffs`, `+card:staff-qualifications`, `+card:meta-currency-unlocks`, `+card:multi-plot-expansion`, `+card:room-grading` — див. вище.

## Джерела
- ⭐ [Wikipedia: Two Point Hospital](https://en.wikipedia.org/wiki/Two_Point_Hospital) — престиж від розміру й оздоблення, Kudosh, кваліфікації для всіх, привиди й Ghost Capture, епідемії з вакцинами, зірки й рівень лікарні, нагороди, пісочниця, DLC, таблиці.
- [Steam](https://store.steampowered.com/app/535930/Two_Point_Hospital/) — предмети → престиж, кілька будівель, машина на хворобу, дослідження, ціни лікування, кредити.
- [ADVANCED Hospital Guide](https://steamcommunity.com/sharedfiles/filedetails/?id=1509294663) — бусти додаються, сертифікати → престиж, ~10 % діагнозу за прийом, поріг 70–75 %, щастя >80 % → +10 %, навчання 10–15 днів, черги й потреби.

## Непевне
- (?) Мінімальні розміри кімнат і таблиця обовʼязкових предметів — не бачив у відкритих джерелах.
- (?) Шкала престижу (рівні, максимум) і чи впливає він на пацієнтів, а не лише на персонал — Wikipedia каже про персонал.
- (?) Поріг автоматичного направлення на лікування — налаштування політики (за Theme Hospital) чи фіксований.
- (?) Як саме тратиться Kudosh (окремий магазин чи каталог) і тепло/батареї — з памʼяті.
- (?) Консольні платформи (2020) — з памʼяті; гайд Steam позначено «removed».
