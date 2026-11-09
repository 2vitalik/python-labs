---
title: Mini Metro
slug: mini-metro
aka: [Mind the Gap, «Міні-метро»]
family: connect-rotate
also: [build-sim]
klass: cursor
axes:
  field: free
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: survive
year: 2015
platforms: [PC, macOS, Linux, iOS, Android, Switch, PS4]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Mini_Metro_(video_game)", best: true, note: "станції-форми, пасажири-форми, лінії й поїзди, тунелі/мости, щотижневі активи, переповнення (типово 6), режими Normal/Extreme/Endless/Creative, 34 міста"}
  - {kind: official, url: "https://dinopoloclub.com/games/mini-metro/", note: "сайт Dinosaur Polo Club: «Draw lines between stations…», оновлення міст"}
  - {kind: steam, url: "https://store.steampowered.com/app/287980/Mini_Metro/", note: "режими, Creative, понад два десятки міст, дальтонізм і нічний режим, музика Disasterpeace, Workshop"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Mini+Metro+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [path-drawing, drag-drop-piece, spawn-random-cell, spawn-schedule, progress-acceleration, move-auto, inventory, inventory-limit, impassable-cells, game-pause, mode-select, level-select, level-unlock, end-screen, score-records, leaderboard, theme-select, background-music, game-settings, field-scaling, +overflow-timer, +choose-upgrade, +route-network, +shape-matched-delivery, +line-edit-live, +procedural-music]
proposes: ["+trigger:week_end", "+cond:overcrowded", "+effect:board", "+effect:alight", "+effect:reroute", "+role:passenger", "+ui:overflow-ring", "+ui:week-clock", "+ui:asset-tray", "+feature:mode-extreme", "+feature:mode-creative", "+card:overflow-timer", "+card:choose-upgrade", "+card:route-network", "+card:shape-matched-delivery"]
author: opus
date: 2026-11-09
---

# Mini Metro — малюй лінії метро між станціями-фігурами, поки місто росте, а пасажири самі шукають маршрут

## Суть
На абстрактній мапі міста зʼявляються станції-фігури (коло, трикутник, квадрат, рідкісні унікальні форми). Біля станцій виникають пасажири — маленькі фігури, яким треба на будь-яку станцію своєї форми. Гравець тягне кольорові лінії через станції, на кожній лінії їздять поїзди; пасажири самі обирають, на який поїзд сісти і де пересісти. Ядро — **перебудова мережі в реальному часі** за обмеженого набору ресурсів (лінії, поїзди, вагони, тунелі): станцій дедалі більше, і рано чи пізно одна переповниться — кінець.

## Поле і час
- Поле `free`: станції мають координати на мапі, лінії — ламані під кути 45°/90° у стилі схеми Гаррі Бека (?); річки й вода — перешкода, яку лінія перетинає лише тунелем/мостом.
- Мапа реального міста (34 міста станом на 2023): своя палітра, вода, темп появи станцій.
- Час — безперервний; є пауза (під час неї можна перебудовувати лінії) і прискорення (?). Ігровий тиждень — одиниця прогресу.
- Камера віддаляється в міру росту міста (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Станція | sink (custom) | форма; місткість (типово 6); таймер переповнення | зʼявляється випадково; породжує пасажирів; переповнена → таймер, що добігає → кінець гри |
| Унікальна станція (зірка, діамант, хрест…) | sink (custom) | рідкісна форма | одна-дві на мапі; пасажирів до неї мало, але їхати далеко (?) |
| Пасажир | neutral | форма-ціль | чекає на станції; сідає в поїзд, якщо лінія веде (з пересадками) до станції його форми; виходить там / на пересадці |
| Лінія | conduit (custom) | колір; послідовність станцій; петля чи відкрита | малюється drag-ом; її можна подовжити з кінця, вставити станцію, видалити |
| Поїзд (локомотив) | object | місткість (?); лінія | їздить лінією туди-назад (або по петлі); зупиняється на станціях, вантажить/вивантажує |
| Вагон | object | +місткість | чіпляється до поїзда |
| Тунель / міст | resource | кількість | дозволяє лінії перетнути воду; витрачається на кожен перетин |
| Пересадочний вузол (interchange) | static | +місткість, швидше посадка | ставиться на станцію з запасу |
| Нова лінія | resource | — | дає ще один колір лінії |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag, station_a→station_b)` → ЯКЩО `has(player, free_line)` → ТО `custom: «нова лінія між станціями»`, на ній зʼявляється поїзд.
- КОЛИ `input(drag, line_end→station)` → ТО `custom: «подовжити лінію»`; drag з середини сегмента → `custom: «вставити станцію в лінію»`.
- КОЛИ `input(drag, line→water)` → ЯКЩО `has(player, tunnel)` → ТО `take(player, tunnel)`; інакше `block`.
- КОЛИ `input(drag, line_end→off)` → ТО `custom: «вкоротити / видалити лінію»`, ресурси повертаються в запас після того, як поїзд доїде (?).
- КОЛИ `input(drag, asset→line|station)` → ТО `place(asset)` (поїзд, вагон, interchange) — `take(player, asset)`.
- КОЛИ `timer(spawn)` → ТО `spawn_at(station, random_free_point)`; темп росте (`progress-acceleration`).
- КОЛИ `rng(p)` на станції → ТО `spawn_at(passenger, station)` з формою ≠ форми станції.
- КОЛИ `contact(train, station)` → ЯКЩО `same(passenger, station, shape)` → ТО `custom: «пасажир виходить»`, `disappear_a`, `score(1)`.
- КОЛИ `contact(train, station)` → ЯКЩО `path_exists(train.line → shape)` and `not state(train, full)` → ТО `custom: «пасажир сідає в поїзд»`; пересадка — `custom: «вийти на станції, звідки маршрут коротший»` (?).
- КОЛИ `input(edit_line)` → ТО `custom: «усі пасажири перераховують маршрут»`.
- КОЛИ `count(passengers@station, >, capacity)` → ТО `set_state(station, overcrowded)`, `timer(start)`; ЯКЩО спадає ≤ capacity → `timer(stop)` і таймер повільно відкочується (?).
- КОЛИ `timer(overcrowded, ==, full)` → ЯКЩО `mode(normal|extreme)` → ТО `lose`, `window(end-screen)`; ЯКЩО `mode(endless)` → переповнення не буває.
- КОЛИ `custom: «кінець тижня»` → ТО `give(player, locomotive)` + `choose(options: line | carriage | tunnel | interchange)`.
- КОЛИ `mode(extreme)` → ТО `custom: «лінії й активи після розміщення не можна змінити»`.
- КОЛИ `mode(creative)` → ТО `custom: «вільно ставити станції, без програшу»`.
- Перемога: нема (гра на виживання) · Поразка: станція переповнена довше за таймер · Рахунок: кількість перевезених пасажирів (ridership).

## Керування і ввід
- Мишею/пальцем: drag від станції до станції — нова лінія; drag кінця лінії — подовження/вкорочення; drag сегмента на станцію — вставити.
- Drag поїзда/вагона з запасу на лінію; drag interchange на станцію; поїзд можна перенести на іншу лінію.
- Пауза (пробіл, ?) — перебудова без поспіху; Extreme забороняє правки.

## Вікна, меню, HUD
- `main-menu` (мінімальний, сам виглядає як схема метро): Play → `level-select` (міста лінією-маршрутом, відкриваються по черзі) → вибір режиму (`mode-select`: Normal / Extreme / Endless / Creative).
- `game-screen`: мапа, `score` (пасажири), `week-clock` (день тижня), `asset-tray` (запас ліній-кольорів, поїздів, вагонів, тунелів), `overflow-ring` над переповненою станцією, кнопки паузи/швидкості (?).
- `choose-upgrade` (`custom-window`): щонеділі — локомотив + вибір одного з двох активів.
- `end-screen`: «Station overcrowded», кількість пасажирів, рекорд, можна поділитись / зберегти карту (?).
- `settings-window`: дальтонізм, нічний режим, звук.
- `leaderboard` / рекорди по місту; щоденний челендж (?).
- Переходи: main-menu → level-select → game-screen ⇄ choose-upgrade → end-screen → level-select.

## Фічі поза полем
- `level-unlock`: місто відкривається за результат у попередньому; Extreme-режим міста — за виконання умови з обмеженням.
- `mode-endless`, `mode-sandbox` (Creative, 2018), `mode-extreme` (+feature).
- `colorblind-palette`, `theme-select` (нічний режим).
- Процедурна музика від мережі (Disasterpeace): кожна лінія/поїзд — свій звук.
- Steam Workshop — мапи гравців; історичні мапи Лондона 1960, Парижа 1937, Нью-Йорка 1972.

## Варіації й родичі
- Наступник — Mini Motorways (дороги по квадратній сітці замість ліній; `build-sim`).
- Родичі: Trainyard, Railbound (колії до станцій, але статичний пазл), Train Valley (колії real-time), Pipe Mania (тиск часу), OpenTTD (сигнали й економіка).
- **Осі варіацій:** мережа — лінії-маршрути / вільний граф / колії по сітці · агенти — пасажири з власним маршрутом / потоки / поїзди з ціллю · правки — будь-коли / лише на паузі / заборонені (Extreme) · ресурс — тиждень / дохід / розмір поля.

## Цікавинки для курсу
- Маршрутизація пасажира: BFS по графу ліній до будь-якої станції потрібної форми, з пересадками — 🥉.
- Перерахунок маршрутів при зміні мережі + пасажири вже у поїзді — 🥈.
- Таймер переповнення з накопиченням і відкатом — 📎.
- Лінія як ламана 45°/90° між вільними точками + перетин з водою (тунель) — 🥈.
- Поїзд туди-назад / по петлі з посадкою-висадкою на зупинках — 🥉.
- Щотижневий вибір з двох активів — 🌱.

## Мапа на каталог
- Є: `path-drawing` ↔ лінії · `drag-drop-piece` ↔ поїзди/вагони · `spawn-random-cell` ↔ станції · `spawn-schedule` ↔ пасажири · `progress-acceleration` · `move-auto` ↔ поїзди · `inventory` + `inventory-limit` ↔ запас активів · `impassable-cells` ↔ вода без тунелю · `game-pause` · `mode-select` · `level-select` · `level-unlock` · `end-screen` · `score-records` · `leaderboard` · `theme-select` · `background-music` · `game-settings` · `field-scaling`.
- **Нема** → пропозиції карток:
  - `+overflow-timer` «Таймер переповнення сутності» · game-logic/lose · 📎 (вже пропонувала Mini Motorways).
  - `+choose-upgrade` «Вибір 1 з N активів за період» · game-logic/economy · 🌱.
  - `+route-network` «Агенти маршрутизуються по мережі ліній з пересадками» · entities/move · 🥈.
  - `+shape-matched-delivery` «Доставка до будь-якої цілі своєї форми» · game-logic/score · 🌱.
  - `+line-edit-live` «Правка мережі під час руху, ресурси повертаються після звільнення» · interface/input · 🥉.
  - `+procedural-music` «Музика з подій гри» · interface/sound · 🥈.

## Пропозиції до словників
- `+trigger:week_end` — кінець ігрового тижня (підтвердження з Mini Motorways).
- `+cond:overcrowded` — кількість на станції > місткості (можна виразити `count`, але це стан з таймером).
- `+effect:board` / `+effect:alight` — агент сідає в транспорт / виходить.
- `+effect:reroute` — усі агенти перераховують маршрут після зміни мережі.
- `+role:passenger` — агент з ціллю, що їздить чужим транспортом (Mini Metro, Cosmic Express).
- `+ui:overflow-ring` (з Mini Motorways), `+ui:week-clock`, `+ui:asset-tray` — запас ліній/поїздів/тунелів.
- `+feature:mode-extreme` — правки заборонені після розміщення; `+feature:mode-creative` — пісочниця.
- `+card:*` — див. «Мапа на каталог».

## Джерела
- ⭐ [Mini Metro — Wikipedia](https://en.wikipedia.org/wiki/Mini_Metro_(video_game)) — станції/пасажири-форми, лінії й поїзди, тунелі/мости, щотижневі активи (лінії, interchange), місткість «typically six», режими, 34 міста, історичні мапи, Ludum Dare 26 («Mind the Gap»), дати релізів.
- [Steam](https://store.steampowered.com/app/287980/Mini_Metro/) — Normal/Endless/Extreme/Creative, випадковий ріст міста, стиль Гаррі Бека, музика Disasterpeace, дальтонізм і нічний режим, Workshop.
- [Dinosaur Polo Club](https://dinopoloclub.com/games/mini-metro/) — «Draw lines between stations and start your trains running», нові міста (Nanjing, Boston).

## Непевне
- (?) Кути 45°/90° для ліній, місткість поїзда (6?) і вагона, «вибір з двох» щотижня — з памʼяті; Wikipedia каже лише «щотижня активи».
- (?) Деталі маршрутизації (як пасажир обирає пересадку) і відкат таймера переповнення — з памʼяті.
- (?) Перелік унікальних форм, прискорення часу, щоденний челендж, поділитися картою — не звірено.
- (?) PS4: інфобокс 20.09.2019, текст — 10.09.2019.
- Тека `connect-rotate` (як призначено: ядро — малювання ліній між станціями); наступник Mini Motorways лежить у `build-sim`, тож межа спірна.
