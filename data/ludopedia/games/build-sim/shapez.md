---
title: shapez
slug: shapez
aka: [shapez.io, Шейпз]
family: build-sim
also: [program-robots]
klass: cursor
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: setup
  goal: collect
year: 2020
platforms: [PC (Windows, macOS, Linux), web]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1318690", best: true, note: "опис гри, демо, Puzzle DLC"}
  - {kind: official, url: "https://raw.githubusercontent.com/tobspr-games/shapez.io/master/translations/base-en.yaml", note: "відкритий код: тексти всіх будівель, меню, налаштувань, Puzzle-режиму"}
  - {kind: other, url: "https://raw.githubusercontent.com/tobspr-games/shapez.io/master/src/js/game/shape_definition.js", note: "код форми: рядок-ключ, порядок чвертей, операції різання/повороту/стека"}
  - {kind: other, url: "https://raw.githubusercontent.com/tobspr-games/shapez.io/master/src/js/game/colors.js", note: "8 кольорів і таблиця змішування (бітове OR RGB)"}
  - {kind: other, url: "https://raw.githubusercontent.com/tobspr-games/shapez.io/master/src/js/game/modes/levels.js", note: "26 рівнів: форма, кількість, нагорода"}
  - {kind: other, url: "https://gigazine.net/gsc_news/en/20201103-game-shapez", note: "огляд перших рівнів: екстрактор, конвеєр, різак, смітник, апгрейди"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=shapez+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 75
mechanics: [row-conveyor, multi-cell-size, orientation-state, path-drawing, cell-click, hover-highlight, teleport-pair, button-toggle, impassable-cells, collect-quota, sequential-levels, level-unlock, in-round-upgrades, round-currency, save-game, save-autosave, field-scaling, game-settings, in-game-editor, level-exchange, state-as-data, game-loop, +entity-rotate, +underground-link, +splitter-balance, +overflow-gate, +item-filter-sort, +color-mixing, +blueprint-ghost, +logic-circuit-wiring, +overlay-view, +drag-build-line, +shape-code-string, +quadrant-shape-ops, +layer-stack-drop, +throughput-goal, +clog-on-full-output]
proposes: ["+effect:paint_item(item, color)", "+effect:cut(item, parts)", "+trigger:delivered(item, sink)", "+cond:truthy(signal)", "+window:markers-window", "+ui:pinned-goals", "+ui:building-toolbar", "+ui:layer-toggle", "+feature:puzzle-share", "+card:shape-code-string", "+card:quadrant-shape-ops", "+card:layer-stack-drop", "+card:throughput-goal", "+card:clog-on-full-output"]
author: opus
date: 2026-11-09
---

# shapez — фабрика фігур: ріж, крути, фарбуй і складай чверті, щоб здати HUB-у потрібну форму

## Суть
Factorio без бою, руди й крафтових дерев: будівлі безкоштовні, ресурс — геометрична **форма** з 4 чвертей і до 4 шарів, кожна чверть має тип (коло, квадрат, зірка, вітряк) і колір. Гравець ставить екстрактори на родовища форм і фарб, тягне конвеєри й будує лінії з різаків, поворотників, стекерів, фарбувальників і змішувачів, щоб HUB отримав задану форму в потрібній кількості. Кожен рівень відкриває нову будівлю; з рівня 20 — шар дротів з логікою, з 25 — віртуальні процесори, з 26 — фріплей. Ядро — **форма як рядок-код** і чисті операції над ним (cut / rotate / stack / paint).

## Поле і час
- Нескінченна квадратна карта, HUB у центрі; родовища форм і кольорів розкидані світом (генерація — `random: setup`).
- Два **шари**: звичайний (будівлі, конвеєри, предмети) і шар дротів (сигнали); перемикаються, видно один поверх іншого.
- Будівлі мають напрям, вхідні й вихідні сторони; машини з двома входами/виходами ширші за одну клітину (розмір — у «Непевне»).
- Real-time: предмети їдуть конвеєром, машини мають час обробки; швидкість визначають апгрейди.
- Камера: пан і зум від окремих клітин до огляду всієї фабрики.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| HUB | sink | ціль рівня: форма × кількість | приймає будь-які форми з усіх боків; рахує доставку цілі, решта йде в запас для апгрейдів |
| Родовище форми / кольору | resource | форма або колір | невичерпне джерело під екстрактором |
| Форма (предмет) | object | 1–4 шари × 4 чверті; чверть = тип (C/R/S/W) + колір | їде конвеєром; змінюється машинами |
| Фарба (предмет) | object | колір: r g b y p c w (+ u — без кольору) | їде конвеєром у фарбувальник/змішувач |
| Екстрактор / екстрактор-ланцюг | source | на родовищі | видобуває форму/колір у вихід; ланцюговий передає вперед через сусідні екстрактори |
| Конвеєр | terrain | напрям | везе предмети; «тягни — ставиш ряд» |
| Балансир | object | 2 входи / 2 виходи | рівномірно розподіляє всі входи на всі виходи |
| Злиття / розгалуження (compact) | object | 2→1 / 1→2 | компактні варіанти балансира |
| Тунель I / II | terrain | пара вхід–вихід, II — більша дальність | переносить предмети під будівлями й конвеєрами; рівні II і I можна змішувати |
| Різак | object | 2 виходи | ріже форму згори донизу на дві половини; невикористану половину треба знищити, інакше забивається |
| Різак (quad) | object | 4 виходи | ріже на 4 чверті; те саме правило засмічення |
| Поворотник CW / CCW / 180° | object | — | повертає форму на 90° за год., 90° проти год., 180° |
| Стекер | object | лівий + правий вхід | обʼєднує в одному шарі, якщо можна; інакше правий кладе поверх лівого |
| Змішувач кольорів | object | 2 входи фарби | адитивне змішування (r+g = y, r+b = p, g+b = c, всі три = w) |
| Фарбувальник / дзеркальний | object | форма зліва, фарба згори (дзеркальний — знизу) | фарбує всю форму в колір |
| Фарбувальник (double) | object | 2 форми + 1 фарба | фарбує дві форми одним кольором |
| Фарбувальник (quad) | object | форма + 4 фарби + сигнали | фарбує кожну чверть окремо, лише ті слоти, де сигнал дроту truthy |
| Смітник | sink | — | приймає з усіх боків і знищує |
| Склад (storage) | container | місткість | тримає надлишок; віддає з пріоритетом лівого виходу — працює як overflow-gate |
| Дріт / перехрестя | conduit | колір дроту | передає сигнал (форма, колір або 0/1); дроти різних кольорів не зʼєднуються; перехрестя — без контакту |
| Постійний сигнал / важіль | switch | значення | видає форму, колір або 0/1; важіль перемикає 0/1 |
| AND / OR / XOR / NOT, транзистор | object | входи-сигнали | булева логіка; транзистор пропускає нижній вхід, якщо бічний truthy |
| Фільтр | object | предмет або сигнал | збіг — вгору, решта — праворуч |
| Дисплей · зчитувач конвеєра · аналізатор форми · компаратор | object | — | показує сигнал · міряє пропускну здатність і видає останній предмет · повертає форму й колір верхньої правої чверті нижнього шару · 1, якщо сигнали рівні |
| Віртуальні процесори (cutter, rotator, unstacker, stacker, painter) | object | лише шар дротів | ті самі операції над формою-сигналом без предметів |
| Постійний виробник · приймач цілі · блок (Puzzle) | source / sink / static | — | у пазл-режимі: дає задану форму · запамʼятовує доставлену форму як ціль · непрохідна клітина |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ЯКЩО `free(next_cell_on_belt)` → ТО `move(item, belt_dir)`; інакше `block` (затор біжить назад лінією).
- КОЛИ ставиться екстрактор → ЯКЩО `cell(x, deposit)` → ТО видобуває; КОЛИ `timer(extract_period)` → ЯКЩО `free(output)` → ТО `spawn_at(item_of_deposit, output)`.
- КОЛИ `enter(shape, cutter)` → ЯКЩО `free(out_left)` and `free(out_right)` → ТО `custom: «ліва половина (чверті TL, BL) → один вихід, права (TR, BR) → інший»`; інакше `block` — різак «забивається», доки зайву половину не знищено.
- КОЛИ `enter(shape, quad_cutter)` → ТО `custom: «4 чверті в 4 виходи»`, кожен вихід має бути `free`.
- КОЛИ `enter(shape, rotator)` → ТО `rotate(shape, 90 | -90 | 180)` — зсув масиву чвертей кожного шару на 1 / −1 / 2.
- КОЛИ `enter(a, stacker_left)` and `enter(b, stacker_right)` → ТО `merge(a, b → c)`: `custom: «b падає на a, доки в найближчій по вертикалі чверті не опиниться на 1 шар вище; вище 4-го шару — відкидається»`.
- КОЛИ `enter(color_a, mixer)` and `enter(color_b, mixer)` → ТО `merge(color_a, color_b → color_a OR color_b)` (r=001, g=010, b=100; u — нейтральний; w поглинає все).
- КОЛИ `enter(shape, painter)` and `has(painter, color)` → ТО `custom: «усі непорожні чверті форми → color»`.
- КОЛИ `enter(shape, quad_painter)` → ЯКЩО `custom: «сигнал слота k truthy»` → ТО чверть k → колір k; інші лишаються.
- КОЛИ `enter(item, trash)` → ТО `disappear_a`.
- КОЛИ `enter(item, tunnel_entry)` → ТО `teleport(item, paired_exit)`; пара — вихід у напрямку тунелю в межах дальності свого рівня.
- КОЛИ `enter(item, balancer)` → ТО `custom: «чергувати виходи; якщо один зайнятий — у вільний»`.
- КОЛИ `enter(item, storage)` → ТО `give(storage, item)`; КОЛИ `tick` → ЯКЩО `free(left_out)` → туди; інакше праворуч; заповнений склад → `block`.
- КОЛИ `enter(item, filter)` → ЯКЩО `same(item, filter_value)` → ТО вгору; інакше праворуч.
- КОЛИ `contact(shape, hub)` → ТО `pickup`, `counter(stored[shape], +1)`; ЯКЩО `same(shape, level_goal)` → ТО `counter(delivered, +1)`.
- КОЛИ `counter(delivered, >=, goal_amount)` → ТО `unlock(reward_building)`, `next_level`, `window(level_complete)`.
- Рівень 14: КОЛИ `counter(goal_shape_per_second, >=, 8)` → ТО перемога рівня (ціль на **пропускну здатність**, не кількість).
- КОЛИ `input(upgrade, category)` → ЯКЩО `has(hub, required_shapes)` → ТО `take(hub, required_shapes)`, `speed(category, +improvement)` (категорії: конвеєри/розподільники/тунелі · видобуток · різання/поворот/стек · змішування й фарбування).
- КОЛИ `input(paste_blueprint)` → ЯКЩО `has(hub, blueprint_shape, cost)` → ТО `take(...)`, `place(buildings)`; інакше `block`.
- КОЛИ `input(place, building)` → ЯКЩО `free(all_cells)` → ТО `place`; КОЛИ `input(delete)` → ТО `custom: «будівля зникає безкоштовно»` (будівлі нічого не коштують).
- КОЛИ `input(toggle, lever)` → ТО `set_state(lever, flip)`; КОЛИ `tick` → гейти рахують вихід з входів (`custom: «булева функція»`).
- Puzzle-режим: КОЛИ `contact(shape, goal_acceptor)` → ЯКЩО `same(shape, stored_goal)` → ТО прогрес; КОЛИ `all_constraints_met` (усі приймачі задоволені) → ТО `win`.
- Поразки нема. «Рахунок» — номер рівня, кількість доставленого, рівні апгрейдів.

## Керування і ввід
- Тулбар будівель (цифрові гарячі клавіші (?)), клік — поставити, drag — ряд конвеєрів або будівель; поворот будівлі перед розміщенням (клавіша R (?)); варіанти будівлі перемикаються (T (?)).
- ПКМ — видалити; рамка ПКМ/drag — масове видалення (?).
- Ctrl-drag — виділення, C — копіювати в креслення, вставка коштує форми-креслення (розблоковано на рівні 12).
- Перемикач шару дротів (клавіша E (?)); піпетка — взяти будівлю з поля (Q (?)).
- Пан і зум камери (WASD / колесо (?)); маркери: ЛКМ — стрибнути, ПКМ — видалити.
- Шпилька біля форми апгрейда — закріпити її на екрані; клік по закріпленій — відкріпити.

## Вікна, меню, HUD
- `main-menu`: Play / Continue, New Game, Import, Puzzle Mode, Changelog, Reddit; список збережень.
- `game-screen`: поле, `building-toolbar` (будівлі й варіанти), ціль рівня біля HUB («Deliver … to unlock …»), `pinned-goals` зліва, `layer-toggle`, `zoom-control`.
- `upgrade-window` («Upgrades»): 4 категорії, «Tier N», потрібні форми з кількістю, кнопка Upgrade, «MAXIMUM LEVEL».
- `stats-window`: джерела Stored (у HUB), Produced (вироблено), Delivered (доставлено); порожньо — «No shapes have been produced so far».
- `markers-window` («Markers»): HUB і власні маркери; «Marker has been created».
- `end-screen`-модал рівня: нова будівля, кнопка далі; демо — «End of Demo».
- `settings-window`: General, User Interface, Advanced, Performance (зокрема режим для дальтоніків).
- Puzzle: `puzzle-select` (Play, Edit, Create Puzzle, Load, Review & Publish) → `editor-window` (Zone: Width/Height/Trim, Clear Items, Clear Buildings, Reset Puzzle, Share, Report).
- `pause-menu` — повернутись / налаштування / вихід у меню (?).
- Переходи: main-menu → game-screen (збереження) · game-screen ↔ upgrade-window / stats-window / markers-window · рівень → модал → game-screen · main-menu → Puzzle Mode → puzzle-select ↔ editor-window.

## Фічі поза полем
- `levels-sequential` (26 рівнів) + `level-unlock` будівель + `mode-sandbox` (фріплей після 26; Item Producer — лише sandbox).
- `meta-progression` у межах сейву — апгрейди за форми (ціни ростуть з кроком ×2.5).
- Креслення (blueprints) — copy/paste ділянки фабрики за ресурс.
- `autosave` + `save-slots` + Import сейву; `colorblind-palette`.
- Puzzle DLC: `level-editor` пазлів, `level-sharing` (Share / Review & Publish), `user-levels-browser`, Report.
- Демо-версії: 8 рівнів + «кінець демо».

## Варіації й родичі
- **Осі варіацій:** ресурс — предмет-тип (Factorio) / предмет-структура (shapez: форма-код) / предмет-число (Big Pharma: концентрація) · будівлі коштують / безкоштовні · логіка окремим шаром / у тому ж шарі.
- shapez 2 (2024): 3D-поверхи, модульні острови, форми до 4 шарів × 4 чверті — у черзі окремо.
- Родичі в корпусі: [factorio-belts](factorio-belts.md) (доріжки, сайдлоад, маніпулятори), [mindustry](mindustry.md) (логістика + оборона), [big-pharma](big-pharma.md) (стан предмета змінюється машинами), [opus-magnum](../program-robots/opus-magnum.md) (вихід — задана молекула), [wilmots-warehouse](wilmots-warehouse.md).
- Puzzle DLC — перехід у `thinky`: обмежене поле, задані джерела, ціль — точна форма.

## Цікавинки для курсу
- Рядок-код форми (`CuCuCuCu`, `RbRb----`, шари через `:`) + парсер/валідатор (1–4 шари, ≥1 непорожня чверть на шар) — 🌱.
- Операції над формою як чисті функції: cut / rotate CW / CCW / 180 / paint / paint-quad — 📎 (масив 4 чвертей × шари; ідеально під unit-тести).
- Стекер з «падінням» верхньої форми до найближчої чверті і обрізанням до 4 шарів — 🥉 (нетривіальний мінімум розриву по чвертях).
- Змішування кольорів як бітове OR над RGB — 🌱 (таблиця 8×8 з однієї операції).
- Конвеєр + засмічення: машина з двома виходами стоїть, якщо будь-який вихід зайнятий; затор біжить назад — 🥉.
- Ціль рівня по кількості та по пропускній здатності (предмети/с за вікном часу) — 📎.
- Шар дротів: сигнали-значення (форма/колір/0-1), гейти, фільтр, віртуальні процесори — 🥈.
- Розвʼязувач «яка послідовність операцій дає цільову форму з родовищ» — 🥇 (пошук у просторі форм).

## Мапа на каталог
- Є: `row-conveyor` · `multi-cell-size` (машини ширші за клітину) · `orientation-state` (напрям будівлі) · `path-drawing` (drag конвеєра) · `cell-click` + `hover-highlight` · `teleport-pair` (тунель) · `button-toggle` (важіль) · `impassable-cells` (блок у пазлі) · `collect-quota` (ціль HUB) · `sequential-levels` + `level-unlock` · `in-round-upgrades` + `round-currency` (форми = валюта апгрейдів) · `save-game` + `save-autosave` · `field-scaling` · `game-settings` · `in-game-editor` + `level-exchange` (Puzzle DLC) · `state-as-data` · `game-loop`.
- Перевикористано: `+entity-rotate`, `+underground-link`, `+splitter-balance`, `+overflow-gate` (склад), `+item-filter-sort`, `+color-mixing`, `+blueprint-ghost`, `+logic-circuit-wiring`, `+overlay-view` (шар дротів), `+drag-build-line`.
- **Нема** → пропозиції карток:
  - `+shape-code-string` «Предмет як рядок-код структури» · code/architecture · 🌱 · слоти {alphabet, layers}.
  - `+quadrant-shape-ops` «Операції над формою з чвертей: різати, крутити, фарбувати» · entities/state · 📎.
  - `+layer-stack-drop` «Складання шарів з падінням до опори» · entities/state · 🥉.
  - `+throughput-goal` «Ціль — N предметів за секунду» · game-logic/win · 📎.
  - `+clog-on-full-output` «Машина стоїть, якщо вихід зайнятий» · entities/interact · 📎.

## Пропозиції до словників
- `+effect:paint_item(item, color)` — фарбування предмета (не клітини: `paint` у словнику — для клітин).
- `+effect:cut(item, parts)` — розрізати предмет на частини з виходами (різак, quad-різак).
- `+trigger:delivered(item, sink)` — предмет здано приймачу (HUB, вихідний порт у Big Pharma).
- `+cond:truthy(signal)` — сигнал дроту не 0/порожній (quad-фарбувальник, транзистор).
- `+window:markers-window` — список маркерів-закладок на карті.
- `+ui:pinned-goals` — закріплені на екрані форми з лічильником; `+ui:building-toolbar` — тулбар будівель з варіантами; `+ui:layer-toggle` — перемикач шарів поля.
- `+feature:puzzle-share` — публікація пазла з рецензуванням (Review & Publish, Report).
- `+card:…` — див. «Мапа на каталог».

## Джерела
- ⭐ [Steam: shapez](https://store.steampowered.com/app/1318690) — суть, Early Access 24.05.2020, реліз 07.06.2020, Puzzle DLC, демо.
- [base-en.yaml](https://raw.githubusercontent.com/tobspr-games/shapez.io/master/translations/base-en.yaml) — описи всіх будівель і варіантів, меню, налаштування, статистика, маркери, креслення, Puzzle-редактор.
- [shape_definition.js](https://raw.githubusercontent.com/tobspr-games/shapez.io/master/src/js/game/shape_definition.js) — формат ключа, порядок чвертей TR→BR→BL→TL, максимум 4 шари, алгоритм стекера.
- [colors.js](https://raw.githubusercontent.com/tobspr-games/shapez.io/master/src/js/game/colors.js) — 8 кольорів і таблиця змішування.
- [levels.js](https://raw.githubusercontent.com/tobspr-games/shapez.io/master/src/js/game/modes/levels.js) — 26 рівнів, нагороди, рівень 14 на пропускну здатність (8/с).
- [GIGAZINE](https://gigazine.net/gsc_news/en/20201103-game-shapez) — перші рівні (30 кіл → різак і смітник), апгрейди, режим для дальтоніків.
- YouTube: пошук «shapez gameplay».

## Непевне
- (?) Гарячі клавіші R / T / E / Q і цифри тулбара — з памʼяті; підтверджено лише Ctrl-drag + C для креслень і ЛКМ/ПКМ для маркерів.
- (?) Розміри HUB і машин (2×1) і дальність тунелів — числа не бачив у відкритих джерелах.
- (?) Наявність web-версії (shapez.io у браузері) — підказує назва репозиторію; у відкритих джерелах прямо не сказано.
- (?) Як саме генеруються родовища на нескінченній карті (сид, віддаленість від HUB) — не перевірено.
- (?) Пункти `pause-menu` — не бачив у перекладах.
