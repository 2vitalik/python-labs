---
title: Hook
slug: hook
aka: [Hook 2]
family: connect-rotate
also: [thinky]
klass: cursor
axes:
  field: graph
  time: static
  opponent: none
  info: full
  random: none
  goal: state
year: 2015
platforms: [PC, Mac, Linux, iOS, Android, web]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/367580/Hook/", best: true, note: "Steam: Maciej Targoni, 25.01.2015, мета — зняти всі гачки, без таймера й очок"}
  - {kind: steam, url: "https://store.steampowered.com/app/1871310/Hook_2/", note: "Hook 2 (2022): ті самі задачі в 3D, що обертається"}
  - {kind: other, url: "https://plannedallalong.blogspot.com/2019/11/quick-review-hook.html?m=1", note: "огляд: контур від гачка до котушки, перемикні перехрестя, звʼязані гачки, 3 життя в кінці"}
  - {kind: other, url: "https://indiegamereviewer.com/?p=25231", note: "огляд: кнопка тягне лінії, порядок зняття, обертні колеса, бездротові передавачі, 50 рівнів"}
  - {kind: other, url: "https://apps.apple.com/us/app/id956794130", note: "App Store"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Hook+puzzle+game+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [cell-click, completion-detection, collect-all, player-death, restart-level, sequential-levels, level-unlock, save-progress, game-screen, level-select, achievements-window, theme-select, +pull-order-dependency, +signal-circuit, +rotary-junction, +linked-retract, +wireless-link]
proposes: ["+cond:not_covered", "+cond:circuit_closed", "+effect:retract", "+card:pull-order-dependency", "+card:signal-circuit", "+card:rotary-junction"]
author: opus
date: 2026-11-09
---

# Hook — натисни кнопку, і гачок змотається, але лише якщо його лінію нічого не перекриває: знайди правильний порядок

## Суть
Мінімалістичний пазл «Мікадо на схемі»: на полі лінії-ліски з гачками на кінцях, кожна тягнеться до кнопки-котушки. Натиск кнопки змотує повʼязану лінію; якщо її перетинає інша лінія зверху, гачок застрягає — помилка, рівень спочатку. Треба зняти всі гачки, отже — вивести порядок залежностей «хто на кому лежить». Згодом зʼявляються дроти-контури від кнопки до гачка, перемикні перехрестя, обертні колеса, бездротові передавачі й звʼязані гачки.

## Поле і час
- Поле — схема з відрізків під 90° і 45° (?) між вузлами; клітин як таких нема, тому `graph`.
- Шари: лінії лежать одна над одною — перетин означає «верхня блокує нижню».
- Статичний пазл: дія — натиск, змотування анімоване, таймера нема.
- Hook 2: те саме у 3D, поле обертається камерою.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гачок | object | на кінці лінії | змотується разом з лінією; зник — гачок знято |
| Лінія (ліска) | conduit | траєкторія; що лежить над/під нею | при змотуванні проходить усім маршрутом; блокується, якщо щось на ній |
| Кнопка-котушка | switch | — | натиск змотує лінії, повʼязані з нею контуром |
| Дріт-контур | conduit | — | несе «сигнал» від кнопки до гачка; має бути замкнений (?) |
| Перемикне перехрестя | switch | положення | натиск змінює, які гілки контуру зʼєднані |
| Обертне колесо | switch | поворот | обертається й по-новому зʼєднує/розʼєднує лінії |
| Бездротовий передавач | conduit | пара | зʼєднує лінії без фізичного дроту |
| Звʼязані гачки | object | група | змотуються одночасно, тож блокуватись не має жоден |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(click, button)` → ЯКЩО `custom: «контур від кнопки до гачка замкнений»` (+cond:circuit_closed) → ТО `custom: «сигнал іде до гачка»`.
- КОЛИ `custom: «сигнал дійшов до гачка»` → ЯКЩО `custom: «жодна лінія не лежить зверху»` (+cond:not_covered) → ТО `custom: «лінія змотується»` (+effect:retract), `disappear_a`.
- КОЛИ `custom: «сигнал дійшов до гачка»` → ЯКЩО `not custom: «лінія вільна»` → ТО `lose` (ранні рівні: одразу рестарт) / `lives(-1)` (останні рівні: 3 життя).
- КОЛИ `input(click, junction)` → ТО `set_state(junction, next)` — інший варіант зʼєднання гілок.
- КОЛИ `input(click, wheel)` → ТО `rotate(wheel, step)` — колесо по-новому зʼєднує лінії.
- КОЛИ `custom: «сигнал на бездротовому передавачі»` → ТО `custom: «сигнал зʼявляється на парному передавачі»`.
- КОЛИ `custom: «звʼязані гачки змотуються»` → ЯКЩО `custom: «вільні всі»` → ТО `disappear_a` для всіх; інакше `lose`.
- КОЛИ `lives(0)` → ТО `restart`.
- КОЛИ `all_gone(hook)` → ТО `win`, `next_level`.
- Перемога: знято всі гачки · Поразка: спроба змотати перекриту лінію · Рахунок: нема.

## Керування і ввід
- Клік/дотик по кнопці (котушці), перехрестю або колесу; більше нічого.
- Тексту в грі нема, механіки вводяться простими рівнями.

## Вікна, меню, HUD
- `game-screen`: схема рівня, номер рівня (?); у пізніх рівнях — індикатор 3 життів (?).
- `level-select`: сітка рівнів (?).
- `settings-window`: темний режим (`theme-select`), звук (?).
- `achievements-window`: досягнення Steam.
- Переходи: game-screen → наступний рівень одразу після останнього гачка (?).

## Фічі поза полем
- `levels-sequential`: 50–60 рівнів у Hook 1.
- `cloud-save` (Steam Cloud), `achievements`, `theme-select` (темний режим), локалізація інтерфейсу без тексту.
- Без таймерів, очок і реклами.
- Hook 2 (2022): 3D-поле з обертанням камери, «Points Shop» Steam.

## Варіації й родичі
- Предок — Мікадо / Jack-straws (зняти, не зачепивши інших).
- Того ж автора: oO, Klocki, Up Left Out (?).
- У корпусі: [lyne](lyne.md) і [infinity-loop](infinity-loop.md) (зʼєднання як мета), [electric-box](electric-box.md) (сигнал по контуру).
- Осі варіацій: **блокування: верхня лінія / будь-який перетин** · **активація: кнопка тягне свою лінію / сигнал через контур** · **помилка: рестарт / життя** · **поле: 2D / 3D з обертанням**.

## Цікавинки для курсу
- Граф «лінія A лежить над B» і топологічне сортування — порядок зняття — 📎.
- Перевірка перекриття: перетин відрізків з ознакою шару — 📎.
- Сигнал від кнопки через контур і перемикачі (обхід графа зі станами вузлів) — 🥉.
- Звʼязані гачки = зняття групи, коли вільні всі — 🌱.
- Генерація рівня без циклів у графі перекриттів (гарантовано розвʼязного) — 🥈.

## Мапа на каталог
- Є: `cell-click` (клік по кнопці) · `completion-detection` / `collect-all` (зняти всі гачки) · `player-death` (3 життя) · `restart-level` · `sequential-levels` · `level-unlock` · `save-progress` · `game-screen` · `level-select` · `achievements-window` · `theme-select`.
- **Нема** → пропозиції карток:
  - `+pull-order-dependency` «Зняти лише непокритий: порядок за перекриттям» · entities/legality · 📎.
  - `+signal-circuit` «Сигнал від кнопки по контуру до цілі» · entities/interact · 🥉.
  - `+rotary-junction` «Обертне перехрестя/колесо перемикає звʼязки» · entities/state · 📎.
  - `+linked-retract` «Група обʼєктів знімається одночасно» · entities/interact · 🌱.
  - `+wireless-link` «Парні передавачі сигналу» · entities/interact · 🌱 (як `teleport-pair` для сигналу).

## Пропозиції до словників
- `+cond:not_covered(a)` — на сутності не лежить інша (шари перекриття).
- `+cond:circuit_closed(a, b)` — є замкнений контур від A до B.
- `+effect:retract(a)` — змотати лінію до котушки.

## Джерела
- ⭐ [Steam: Hook](https://store.steampowered.com/app/367580/Hook/) — автор, дата, мета «зняти всі гачки», без таймера/очок, темний режим, хмарні збереження.
- [Steam: Hook 2](https://store.steampowered.com/app/1871310/Hook_2/) — 3D-сиквел 2022.
- [Planned All Along: quick review](https://plannedallalong.blogspot.com/2019/11/quick-review-hook.html?m=1) — контур гачок–котушка, перехрестя, звʼязані гачки, 3 життя.
- [Indie Game Reviewer](https://indiegamereviewer.com/?p=25231) — кнопка і лінії, обертні колеса, бездротові передавачі, 50 рівнів, Kongregate.
- [App Store](https://apps.apple.com/us/app/id956794130).

## Непевне
- (?) Кількість рівнів: Steam — 60, огляди — близько 50.
- (?) Кути ліній (90°/45°) — за памʼяттю.
- (?) Чи перехрестя перемикається кліком, чи обертається, — огляд не уточнює.
- (?) Інтерфейс (вибір рівнів, налаштування, індикатор життів) — не бачив.
- (?) Інші ігри автора крім oO — за памʼяттю.
