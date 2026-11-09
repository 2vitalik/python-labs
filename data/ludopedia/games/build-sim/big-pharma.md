---
title: Big Pharma
slug: big-pharma
aka: [«Велика фарма»]
family: build-sim
also: []
klass: cursor
axes:
  field: iso
  time: realtime
  opponent: ai
  info: partial
  random: runtime
  goal: score
year: 2015
platforms: [PC (Windows, macOS, Linux), Xbox One, Switch, PS4]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Big_Pharma_(video_game)", best: true, note: "концентрація 0–20, ефекти в діапазонах, обладнання, ринок, дослідження, сценарії, DLC"}
  - {kind: steam, url: "https://store.steampowered.com/app/344850", note: "35 челенджів у 7 сценаріях, Custom і Freebuild, моди, DLC Marketing and Malpractice"}
  - {kind: other, url: "https://gameplayinside.com/reviews/big-pharma-review-a-puzzle-and-business-simulator", note: "огляд з прикладом: діапазони ефектів, Dissolver/Ioniser, тири ліків, рейтинг продукту, працівники"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=big+pharma+game+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [row-conveyor, multi-cell-size, cell-click, hover-highlight, status-panel, game-pause, round-currency, ai-opponent, difficulty-levels, mode-select, save-game, level-unlock, +item-state-value, +active-range-effect, +effect-slot-swap, +machine-op-cost, +market-saturation, +product-grade, +research-tree, +ingredient-expedition, +field-expansion, +loan-interest]
proposes: ["+cond:value_in_range(item, prop, lo, hi)", "+effect:add_value(item, prop, n)", "+role:staff", "+window:market-window", "+window:product-naming", "+window:research-window", "+ui:concentration-gauge", "+card:item-state-value", "+card:active-range-effect", "+card:market-saturation"]
author: opus
date: 2026-11-09
---

# Big Pharma — фабрика ліків: машини зсувають «концентрацію» інгредієнта, щоб увімкнути ліки й вимкнути побічні ефекти

## Суть
Пазл-конструктор і бізнес-сим (Twice Circled, дизайнер Тім Вікстід, видавець Positech). Інгредієнт їде конвеєром, і головний стан предмета — **концентрація** 0–20: кожен ефект (лікувальний чи побічний) активний лише у своєму діапазоні концентрації. Гравець ставить на ізометричну підлогу машини, що піднімають чи знижують концентрацію, змішують, міняють ефекти місцями й пакують у пігулки, щоб корисне було біля піку, а побічне — поза діапазоном. Готові ліки продаються на ринку з попитом, сезонами й конкурентами.

## Поле і час
- Ізометричний план фабрики-сітки; вхідні й вихідні порти — на краях; додаткову площу можна купити.
- Машини мають різні форми й сторони входів/виходів; конвеєри зʼєднують їх.
- Real-time з паузою: лінію можна переставити на паузі; кожна одиниця матеріалу відстежується, продуктом стає лише на виході.
- Поза полем — «стратегічний» шар: ринок, дослідження, експедиції, фінанси (роки сценарію).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Інгредієнт | resource | концентрація 0–20, 1+ ефектів | заходить через вхідний порт з власною концентрацією (Satagene Extract — 17) |
| Ефект (лікувальний) | mark | діапазон і пік (wart removal: 11–16, пік 14) | активний лише в діапазоні; сила максимальна в піку |
| Побічний ефект | mark | діапазон (blood pressure increase: 8–16) | активується так само — разом з корисним |
| Каталізатор | resource | свої ефекти | потрібен для фіолетового тиру ліків; приносить власні побічні |
| Вхідний порт | source | інгредієнт, ціна | постачає матеріал на лінію |
| Вихідний порт | sink | — | готова пігулка → продаж |
| Конвеєр | terrain | напрям | везе матеріал між машинами |
| Evaporator | object | +1 | підвищує концентрацію на 1 |
| Dissolver | object | −1 | знижує концентрацію на 1 |
| Agglomerator | object | +3 | підвищує концентрацію на 3 |
| Ioniser | object | −3, дорожчий у роботі | знижує на 3; може «апгрейдити» активний ефект в інші ліки (засіб від бородавок → контрацептив) |
| Sequencer | object | 2 / 10 / 18 | встановлює концентрацію у фіксоване значення |
| Centrifuge | object | 2 входи, налаштування слотів | міняє місцями слоти ефектів між двома входами; може дати «ліки» лише з побічних (відходи) |
| Multimixer | object | 2 входи | зливає два препарати в один; так додають каталізатор |
| Analyser | object | — | показує концентрацію макс. сили ефектів; знищує відходи |
| Autoclave · Cryogenic Condenser | object | (?) | базові машини (функцію не перевірено) |
| Pill Printer · Syringe Injector | object | «Makers» | пакують готовий препарат у фінальну форму |
| Конкурент | enemy | ліки на ринку | випускає конкурентні препарати, насичує ринок |
| Науковець · Дослідник | ally | без завдання → бали | науковець відкриває/покращує машини (простій → Research Points); дослідник шукає інгредієнти (простій → Ingredient Upgrade Points) |
| Executive (DLC) | ally | — | маркетинг ліків, маніпуляція ринком |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `enter(drug, evaporator)` → ТО `counter(concentration, +1)`; `dissolver` → `counter(concentration, -1)`; `agglomerator` → `+3`; `ioniser` → `-3`.
- КОЛИ `enter(drug, sequencer)` → ТО `set_value(concentration, 2 | 10 | 18)` (за налаштуванням).
- КОЛИ `tick` → ЯКЩО `custom: «concentration у діапазоні ефекту»` → ТО `set_state(effect, active)`; інакше `clear_state(effect, active)`.
- КОЛИ `enter(drug, machine)` → ЯКЩО `state(effect, active)` and `custom: «машина — процес апгрейда цього ефекту»` → ТО `transform(effect, next_tier_cure)` (синій тир; фіолетовий — лише з каталізатором).
- Побічний ефект: КОЛИ `enter(drug, machine)` → ЯКЩО `custom: «концентрація в потрібній точці для процесу видалення»` → ТО `custom: «побічний ефект прибрано»`.
- КОЛИ `enter(a, centrifuge)` and `enter(b, centrifuge)` → ТО `swap(slot_i(a), slot_j(b))` за налаштуванням.
- КОЛИ `enter(a, multimixer)` and `enter(b, multimixer)` → ТО `merge(a, b → drug)` (ефекти обох; каталізатор так само).
- КОЛИ `enter(drug, analyser)` → ТО `reveal(peak_concentrations)`; ЯКЩО `custom: «лише побічні ефекти»` → ТО `disappear_a`.
- КОЛИ `enter(drug, any_machine)` → ТО `currency(-op_cost)`.
- КОЛИ `enter(drug, maker)` → ТО `transform(drug, pill)`.
- КОЛИ `enter(pill, output_port)` → ЯКЩО `first_time` → ТО `window(product-naming)`; далі `currency(+price)`.
- Ціна: `custom: «ефективність × відсутність побічних × попит; насичення ринку знижує ціну»`; рейтинг продукту починається з C, A — +20 %, D− — −10 %.
- КОЛИ `schedule(season)` / `rng(event)` → ТО `custom: «попит на хворобу змінюється»`; конкуренти випускають ліки → насичення.
- КОЛИ `input(research)` → ЯКЩО `has(scientist_free)` → ТО `unlock(machine | upgrade)`; КОЛИ `input(expedition)` → ТО `unlock(ingredient)`.
- КОЛИ `input(place, machine)` → ЯКЩО `free(all_cells)` → ТО `place`, `currency(-price)`; КОЛИ `input(buy_space)` → ТО `custom: «розширити підлогу»`.
- КОЛИ `input(loan)` → ТО `currency(+n)`, `custom: «відсотки щоперіоду»`.
- Перемога сценарію: `counter(money, >=, target)` за N років (приклад з Wikipedia); поразка — `timer` сценарію вичерпано без цілі (?).

## Керування і ввід
- Мишею: вибрати машину з каталогу, поставити на підлогу, тягнути конвеєри; налаштувати машину (центрифуга, секвенсер) кліком.
- Клік по машині чи матеріалу — показати поточний стан (концентрацію, ефекти) — інструмент налагодження лінії.
- Пауза для перестановки; прискорення часу (?).
- Інтерфейс панелями й вкладками: ліки, ринок, дослідження, персонал.

## Вікна, меню, HUD
- `main-menu`: сценарії, Custom game, Freebuild, моди (?).
- `mode-select` / `level-select` сценаріїв з рівнями складності.
- `game-screen`: ізометрична фабрика; `coins` (баланс), дата/сезон, `concentration-gauge` на предметі при наведенні (`tooltip`).
- `market-window` (`custom-window`): хвороби, попит, ціни, конкуренти.
- `codex-window` «Cures» — список ліків і як їх отримати.
- `research-window` (`custom-window`): дерево досліджень машин; експедиції дослідників.
- `product-naming` — назвати ліки після першої пігулки.
- `end-screen` сценарію (ціль досягнута / ні), `settings-window`, `pause-menu`.
- Переходи: game-screen ↔ market / research / cures; перша пігулка → product-naming → game-screen.

## Фічі поза полем
- Сценарії з рівнями складності (Steam: 35 челенджів у 7 сценаріях) + `tutorial`.
- Custom game і Freebuild (`mode-sandbox` без обмежень).
- `mod-support`; DLC Marketing and Malpractice (2016) — Executives, маркетинг.
- Позики з відсотками; купівля площі.

## Варіації й родичі
- **Осі варіацій:** стан предмета — тип (Factorio) / структура (shapez: чверті) / **число** (Big Pharma: концентрація) · ефект предмета — постійний / активний у діапазоні значення · продаж — фіксована ціна / ринок з насиченням.
- Наступник за духом: Production Line (Positech, інший жанр — збирання авто).
- Родичі в корпусі: [shapez](shapez.md) (машини змінюють структуру предмета), [factorio-belts](factorio-belts.md), [mindustry](mindustry.md), [prison-architect-rooms](prison-architect-rooms.md) (менеджмент поверх сітки).

## Цікавинки для курсу
- Предмет з числовим станом і машини ±1/±3/«встановити 2/10/18» — 🌱 (одне поле + конвеєр).
- Ефекти з діапазонами активності й піком: обчислити, які ефекти увімкнені й з якою силою — 📎.
- Пошук найкоротшого ланцюга машин від концентрації X до Y, що оминає діапазони побічних — 🥉 (BFS по станах).
- Центрифуга: обмін слотами ефектів між двома предметами — 📎.
- Ринок з попитом, сезонами й насиченням (ціна падає з пропозицією) — 🥈 (економічна модель).
- Рейтинг продукту за результатами (C → A/D−) з множником ціни — 📎.

## Мапа на каталог
- Є: `row-conveyor` · `multi-cell-size` (машини різних форм) · `cell-click` + `hover-highlight` + `status-panel` (стан матеріалу) · `game-pause` · `round-currency` · `ai-opponent` (конкуренти) · `difficulty-levels` + `mode-select` (сценарії/Freebuild) · `save-game` · `level-unlock`.
- Перевикористано: `+field-expansion` (купівля площі).
- **Нема** → пропозиції карток:
  - `+item-state-value` «Предмет несе число, машини його змінюють» · entities/state · 🌱 · слоти {min, max, ops}.
  - `+active-range-effect` «Ефект активний лише в діапазоні значення» · entities/state · 📎 · слоти {lo, hi, peak}.
  - `+effect-slot-swap` «Обмін слотами властивостей між двома предметами» · entities/interact · 📎.
  - `+machine-op-cost` «Кожна обробка коштує гроші» · game-logic/economy · 🌱.
  - `+market-saturation` «Попит, сезони, ціна падає з пропозицією» · game-logic/economy · 🥈.
  - `+product-grade` «Буквений рейтинг продукту як множник ціни» · game-logic/score · 📎.
  - `+research-tree` «Дерево досліджень відкриває будівлі» · levels/progression · 🥉.
  - `+ingredient-expedition` «Експедиція відкриває нову сировину» · game-logic/economy · 📎.
  - `+loan-interest` «Позика з відсотками» · game-logic/economy · 🌱.

## Пропозиції до словників
- `+cond:value_in_range(item, prop, lo, hi)` — властивість предмета в діапазоні (ефект активний).
- `+effect:add_value(item, prop, n)` — змінити числову властивість предмета (зараз пишу через `counter`, але це не лічильник гри).
- `+role:staff` — працівник поза полем (науковець, дослідник, executive): дає дію/бали, не ходить полем.
- `+window:market-window` — ринок: попит, ціни, конкуренти; `+window:product-naming` — назвати новий продукт; `+window:research-window` — дерево досліджень.
- `+ui:concentration-gauge` — шкала 0–20 з діапазонами ефектів.
- `+card:…` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Big Pharma](https://en.wikipedia.org/wiki/Big_Pharma_(video_game)) — концентрація 0–20, діапазони ефектів, каталізатори, ізометрична підлога з портами, real-time з паузою, назва продукту, рейтинг, ринок, дослідження, експедиції, сценарії, DLC, дати релізу.
- [Steam](https://store.steampowered.com/app/344850) — 35 челенджів у 7 сценаріях, Custom/Freebuild, моди, сезони попиту.
- [gameplayinside: огляд](https://gameplayinside.com/reviews/big-pharma-review-a-puzzle-and-business-simulator) — приклад Satagene Extract, Dissolver −1, Ioniser −3, тири ліків, 11 категорій хвороб, рейтинг C/A/D−, працівники, позики.
- Big Pharma Wiki (fandom) — віддає 402; з результатів пошуку: Evaporator +1, Agglomerator +3, Ioniser −3, Sequencer 2/10/18, Centrifuge, Multimixer, Analyser.
- YouTube: пошук «big pharma game gameplay».

## Непевне
- (?) Agglomerator +3 і Evaporator +1 — з уривків вікі в пошуку (сторінка не відкрилась); Dissolver −1 — з огляду.
- (?) Функції Autoclave і Cryogenic Condenser, точний механізм видалення побічних ефектів — не перевірено.
- (?) Кількість сценаріїв: Steam — 35 челенджів у 7 сценаріях, огляд — «7 груп по 6 місій, 48 разом» (арифметика не сходиться).
- (?) Умова поразки сценарію і прискорення часу — з памʼяті.
- (?) Пункти головного меню — узагальнення.
