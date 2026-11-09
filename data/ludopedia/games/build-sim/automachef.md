---
title: Automachef
slug: automachef
aka: []
family: build-sim
also: [program-robots]
klass: cursor
axes:
  field: square
  time: programmed
  opponent: none
  info: full
  random: none
  goal: collect
year: 2019
platforms: [PC, Switch]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/984800/Automachef/", best: true, note: "опис: автоматизовані ресторани, кампанія, контракти, тестова кухня, Workshop-рецепти"}
  - {kind: official, url: "https://www.rhombicogames.com/game/automachef", note: "Rhombico Games: режими, пожежі на кухні, платформи"}
  - {kind: other, url: "https://kettlecomplication.pages.dev/posts/automachef-a-beginner-s-guide1256146", note: "гайд новачка: руки dumb/smart, напрям руки, швидкості конвеєра 1–5, режими машин, order reader, блекаут"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Automachef+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [row-conveyor, orientation-state, impassable-cells, multi-cell-size, cell-click, drag-drop-piece, hover-highlight, round-currency, collect-quota, time-out, sequential-levels, level-unlock, level-select, objective-text, status-panel, highlights, game-pause, save-progress, interaction-table, cell-transform, +item-transfer-grabber, +filter-by-sample, +recipe-combine, +order-reader-routing, +machine-power-mode, +power-budget-blackout, +build-budget, +optional-level-targets, +simulate-order, +test-kitchen-blueprints]
proposes: ["+effect:combine", "+cond:configured", "+trigger:order_expired", "+ui:unconfigured-warning", "+ui:power-meter", "+feature:test-kitchen", "+feature:simulate-order", "+card:order-reader-routing", "+card:power-budget-blackout"]
author: opus
date: 2026-11-09
---

# Automachef — кухня без кухарів: машини на сітці, рецепт = маршрут інгредієнтів від диспенсера до ресторану

## Суть
Гравець проєктує автоматизовану кухню на порожній клітинній ділянці: диспенсери видають інгредієнти, конвеєри й роботизовані руки везуть їх до гриля, фритюра, асемблера — і готова страва їде в ресторан. Після розстановки кухня запускається й працює сама; гравець лише перевіряє, чи виконано квоту замовлень у межах бюджету й енергії. Головне для корпусу — **рецепт як граф маршрутів** і **order reader**, який «програмує» диспенсери видавати рівно стільки, скільки треба на одне замовлення. `time: programmed` — фаза побудови без часу, потім симуляція.

## Поле і час
- Кухня — квадратна сітка зі стінами й фіксованою точкою видачі в ресторан; поле й набір дозволених машин задає рівень (сценарій).
- Машина займає клітину (частина — кілька клітин (?)), має орієнтацію входу/виходу.
- Дві фази: **побудова** (час стоїть, ставиш і налаштовуєш машини) → **запуск** (real-time симуляція, замовлення надходять і мають термін).
- Темп машин налаштовний: конвеєр швидкість 1–5; гриль/фритюр/асемблер — режими standard / fast / power-saving.
- Камера згори-збоку, вся кухня видна.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Диспенсер інгредієнта | source | інгредієнт, привʼязка до order reader | видає інгредієнт на клітину виходу (за сигналом order reader) |
| Конвеєр | conduit | напрям, швидкість 1–5 | везе предмет у сусідню клітину; швидше = більше енергії |
| Рука (dumb) | object | напрям: прямо / ліворуч / праворуч | бере будь-який предмет перед собою й кладе на вихід; може «повернути за ріг» |
| Розумна рука (smart) | object | навчений предмет, напрям | як рука, але бере лише заданий предмет (зазвичай уже приготований) |
| Гриль | object | режим standard / fast / power-saving | сире → підсмажене за час; швидше = більше енергії |
| Фритюр | object | режим | як гриль, для смаженого у фритюрі |
| Кухонний комбайн (food processor) | object | — | переробляє інгредієнт (нарізка (?)); рука може брати прямо з нього |
| Асемблер | object | рецепт (обовʼязково задати), режим | збирає страву з потрібних частин рецепта |
| Order reader | switch | рецепт, звʼязані машини, кількість кожного інгредієнта на 1 замовлення | на кожне замовлення дає сигнал диспенсерам видати порцію |
| Точка видачі в ресторан | sink | — | приймає готову страву; зараховує замовлення |
| Замовлення | neutral | страва, термін | приходить під час симуляції; згорає, якщо не доставлено вчасно |
| Інгредієнт / напівфабрикат / страва | resource | стан: сирий → приготований | рухається між машинами |
| Стіна, зайняті клітини | static | — | машину не поставити |
| Пожежа | hazard | — | кухня може загорітись (?) — механіка не розкрита в джерелах |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(place, machine)` → ЯКЩО `free(cell)` and `custom: «лишилось бюджету на машину»` → ТО `place(player, machine)`, `currency(-cost)`.
- КОЛИ `input(delete, machine)` → ТО `disappear(machine)`, `currency(+cost)` (?).
- КОЛИ `input(rotate, machine)` → ТО `rotate(machine, 90)`.
- КОЛИ `input(configure, arm)` → ТО `face(arm, straight|left|right)` — стрілка на основі руки.
- КОЛИ `input(configure, conveyor)` → ТО `speed(conveyor, 1..5)`.
- КОЛИ `input(start)` → ЯКЩО `custom: «є неналаштовані машини»` → ТО `custom: «червоний трикутник над машиною»`; машина не працює.
- КОЛИ `schedule(orders)` → ТО `spawn_at(order, restaurant)`, `trigger(order_reader)`.
- КОЛИ `custom: «нове замовлення рецепта R»` → ЯКЩО `same(order, reader, recipe)` → ТО `custom: «кожен звʼязаний диспенсер видає задану кількість інгредієнта»`.
- КОЛИ `tick` → ЯКЩО `occupied(conveyor, item)` and `free(cell_ahead)` → ТО `move(item, facing)`; інакше `block`.
- КОЛИ `tick` → ЯКЩО `occupied(cell_front, item)` and `free(arm_output)` → ТО `custom: «dumb-рука переносить предмет на вихід»`.
- КОЛИ `tick` → ЯКЩО `same(item, arm_sample, kind)` → ТО `custom: «smart-рука переносить лише заданий предмет»`.
- КОЛИ `enter(raw_item, grill)` → ТО `timer(start, cook_time)`; КОЛИ `timer(cook_time)` → ТО `transform(raw_item, cooked)`, `custom: «вихід машини»`.
- КОЛИ `enter(item, assembler)` → ЯКЩО `custom: «зібрано всі частини рецепта»` → ТО `custom: «частини стають стравою»` (`+effect:combine`).
- КОЛИ `enter(item, assembler)` → ЯКЩО `custom: «рецепт не задано»` → ТО `block`.
- КОЛИ `enter(dish, restaurant)` → ЯКЩО `same(dish, order, recipe)` and `timer(>, 0)` → ТО `counter(orders_done, +1)`, `disappear(order)`.
- КОЛИ `custom: «термін замовлення вийшов»` → ТО `counter(orders_failed, +1)` (`+trigger:order_expired`).
- КОЛИ `tick` → ТО `counter(power, -usage)` — енергію їдять конвеєри (за швидкістю) і машини (за режимом).
- КОЛИ `counter(power, >, limit)` → ЯКЩО `level(op, n)` (пізні рівні) → ТО `custom: «блекаут: кухня зупиняється»` (?).
- КОЛИ `counter(orders_done, >=, quota)` → ТО `win`; оцінка за опційними цілями (енергія, інгредієнти).
- КОЛИ `input(simulate_order, recipe)` → ТО `custom: «пробне замовлення для перевірки лінії»`.
- Перемога: виконати обовʼязкову квоту замовлень · Поразка: замовлення не встигають / бюджет (?) · Рахунок: опційні цілі — енергія й витрата інгредієнтів у межах.

## Керування і ввід
- Мишка: вибір машини з панелі, клік по клітині — поставити; конвеєр — протягуванням (?); правий клік по руці — перемкнути напрям (прямо / ліворуч / праворуч).
- Панель машини: рецепт асемблера, режим швидкості, навчений предмет smart-руки, швидкість конвеєра.
- Order reader: обрати рецепт → клікнути звʼязані машини → задати кількість кожного інгредієнта на одне замовлення.
- Кнопки запуску симуляції й «Simulate Order» під кожним рецептом.

## Вікна, меню, HUD
- `game-screen` (побудова): сітка кухні, палітра машин (`tool-palette`), бюджет (`coins`), список цілей рівня (`objective-text`), червоні трикутники над неналаштованими машинами (`+ui:unconfigured-warning`).
- `game-screen` (запуск): ті самі машини в русі, лічильник виконаних замовлень (`progress-bar`), споживання енергії (`+ui:power-meter`), черга замовлень з таймерами (`timer-countdown`).
- `custom-window` налаштування машини (рецепт, режим, напрям) і order reader.
- `end-screen`: квота виконана / ні, опційні цілі.
- `main-menu` → кампанія (`level-select`) / контракти (`mode-select`) / тестова кухня; `pause-menu`, `settings-window`.

## Фічі поза полем
- Режими: кампанія (сценарії зі зростанням набору машин), контракти («шлях бізнес-світом»), `mode-sandbox` — тестова кухня.
- Тестова кухня: зібрати набір машин і зберегти блюпринтом для кампанії (`+feature:test-kitchen`); у рівні блюпринт обмежений грошима й місцем.
- `mod-support`: Steam Workshop — свої інгредієнти, рецепти, сценарії.
- `localization` 7 мов, озвучка; гумористичний сюжет про Robert Person.

## Варіації й родичі
- У корпусі: `plateup` (та сама кухня з граберами, але кухар-аватар і real-time сервіс), `factorio-belts` (конвеєр + маніпулятор, джерело руки), `shapez` (збирання з частин), `big-pharma` (машина змінює стан предмета на конвеєрі), `production-line` (станції-слоти авто).
- Родичі поза корпусом: Opus Magnum (рука-маніпулятор як програма), Infinifactory.
- Осі «хто керує подачею»: диспенсер видає безперервно / за сигналом order reader / гравець руками.
- Осі «транспорт»: конвеєр (штовхає) / рука (бере і кладе, з поворотом) / рука-фільтр.

## Цікавинки для курсу
- Order reader → диспенсери: подія замовлення запускає видачу рівно потрібної порції — 🥉 (подієва маршрутизація, а не безперервний потік).
- Рука з напрямом прямо/ліворуч/праворуч і фільтром — 📎.
- Асемблер, що чекає на повний набір частин рецепта — 📎 (мультимножина на вході).
- Енергетичний бюджет: швидкість конвеєра й режим машини ↔ споживання, блекаут — 🥉.
- Фаза побудови + запуск симуляції з «пробним замовленням» — 🥉.
- Перевірка конфігурації перед запуском (червоні трикутники) — 🌱.
- Оцінка рівня: обовʼязкова квота + опційні цілі — 🌱.

## Мапа на каталог
- Є: `row-conveyor` (конвеєр) · `orientation-state` (напрям руки/машини) · `impassable-cells` · `multi-cell-size` (?) · `cell-click` / `drag-drop-piece` / `hover-highlight` · `round-currency` (бюджет) · `collect-quota` (квота замовлень) · `time-out` (термін замовлення) · `sequential-levels` / `level-unlock` / `level-select` · `objective-text` · `status-panel` · `highlights` (трикутники) · `game-pause` · `save-progress` · `interaction-table` (машина × інгредієнт) · `cell-transform` (сире → готове).
- **Нема** → пропозиції карток:
  - `+order-reader-routing` «Замовлення запускає видачу порції» · game-logic/program · 🥉 · слоти {recipe, amounts}.
  - `+power-budget-blackout` «Енергія від швидкості машин, блекаут» · game-logic/economy · 🥉.
  - `+machine-power-mode` «Режим машини: швидко / звичайно / економно» · entities/state · 🌱.
  - `+build-budget` «Бюджет на побудову рівня» · game-logic/economy · 🌱.
  - `+optional-level-targets` «Обовʼязкова ціль + опційні» · game-logic/win · 🌱.
  - `+simulate-order` «Пробний запуск однієї події» · game-logic/history · 📎.
  - `+test-kitchen-blueprints` «Пісочниця → блюпринт у кампанію» · levels/editor · 🥉.
  - `+item-transfer-grabber`, `+filter-by-sample`, `+recipe-combine` — як у `plateup`.

## Пропозиції до словників
- `+effect:combine` — частини стають стравою за рецептом (як у `plateup`).
- `+cond:configured` — машина налаштована (рецепт/зразок/звʼязки задано).
- `+trigger:order_expired` — у замовлення вийшов термін.
- `+ui:unconfigured-warning` — значок над неналаштованим обʼєктом; `+ui:power-meter` — споживання енергії проти ліміту.
- `+feature:test-kitchen` — пісочниця з експортом блюпринтів; `+feature:simulate-order` — пробна подія.
- `+card:order-reader-routing`, `+card:power-budget-blackout` — див. вище.

## Джерела
- ⭐ [Steam: Automachef](https://store.steampowered.com/app/984800/Automachef/) — «проєктуй і програмуй автоматизовані ресторани»; кампанія, контракти, тестова кухня, Workshop; реліз 23.07.2019, Rhombico Games / Team17.
- [Rhombico Games: Automachef](https://www.rhombicogames.com/game/automachef) — режими, «кухні горять», Switch і Windows.
- [Гайд новачка](https://kettlecomplication.pages.dev/posts/automachef-a-beginner-s-guide1256146) — машини (диспенсер, конвеєр, гриль, фритюр, асемблер, рука, order reader, food processor), dumb/smart-рука, напрям руки правим кліком, швидкість конвеєра 1–5, режими машин, енергетичні цілі й блекаут, бюджет, термін замовлень, червоні трикутники, Simulate Order, блюпринти тестової кухні.
- YouTube: пошук «Automachef gameplay».

## Непевне
- (?) Повний список машин (сміттєвий бак, розгалужувач, холодильник, «комп'ютер»/логіка) — Steam має тег Programming, але логічних блоків у відкритих джерелах не бачив.
- (?) Чи займають якісь машини кілька клітин і чи конвеєр тягнеться drag-ом.
- (?) Поразка: точна умова (кількість прострочених замовлень, вичерпаний бюджет) і чи замовлення випадкові.
- (?) Блекаут — «пізні рівні мають ризик»; поріг і наслідок не описано.
- (?) Пожежа на кухні — лише згадка на офіційному сайті.
- (?) «Понад 40 сценаріїв» — з огляду в пошуковій видачі, сторінку не відкрито.
- (?) Повернення грошей при видаленні машини.
