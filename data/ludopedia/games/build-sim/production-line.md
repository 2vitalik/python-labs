---
title: Production Line
slug: production-line
aka: [Production Line Car Factory Simulation]
family: build-sim
also: []
klass: cursor
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: score
year: 2017
platforms: [PC]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/591370/", best: true, note: "опис: слоти, що діляться дослідженнями, конвеєри, just-in-time, дослідження фіч авто; реліз 7.03.2019"}
  - {kind: official, url: "https://www.positech.co.uk/productionline/", note: "Positech: фабрика за Фордом, «кожен квадратний метр», ціна авто проти ринку"}
  - {kind: other, url: "https://mail.positech.co.uk/productionline/faq.html", note: "офіційний FAQ: меню слотів, імпорт/експорт на стінах, перетин конвеєрів, сток, дослідження, керування"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Production+Line+car+factory+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [row-conveyor, orientation-state, multi-cell-size, impassable-cells, cell-click, drag-drop-piece, hover-highlight, round-currency, status-panel, game-pause, save-game, in-round-upgrades, player-camera, field-scaling, +fixed-step-order, +slot-split-research, +wall-import-export, +resource-conveyor-feed, +research-tree, +product-naming-price, +finished-stock, +loan-interest, +conveyor-crossing-cost]
proposes: ["+trigger:exported", "+cond:feeds_next(slot)", "+effect:split_slot", "+window:research-window", "+window:product-naming", "+window:slot-order", "+ui:stock-icon", "+feature:loan", "+card:slot-split-research", "+card:wall-import-export"]
author: opus
date: 2026-11-09
---

# Production Line — автозавод за Фордом: корпус авто їде конвеєром крізь слоти-станції, а дослідження дробить кожну станцію на коротші й швидші

## Суть
Гравець планує цех: ставить слоти-станції у фіксованому порядку збирання авто, зʼєднує їх конвеєром для корпусів і підводить до кожного слота ресурсні конвеєри від імпорту на стінах. Готове авто виїжджає через експорт, отримує назву й ціну та йде на склад продажів. Головне для корпусу — **дослідження змінює граф станцій**: великий слот (напр., шасі) розпадається на кілька менших (вісь, каркас, карданний вал), лінія довшає, але пропускна здатність зростає. Гра — про пошук вузьких місць у потоці.

## Поле і час
- Цех — квадратна сітка всередині стін; по периметру — сірі місця під імпорт ресурсів і експорт авто.
- Слот займає прямокутник клітин (?) з входом і виходом; конвеєр авто — ланцюжок клітин з напрямом; ресурсні конвеєри — окремий шар, можуть перетинати конвеєр авто (дорожче).
- Real-time симуляція з паузою (?); авто проходить слот за час роботи станції.
- Камера згори з поворотом і зумом.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Слот-станція | object | крок збирання, час роботи, потрібні ресурси | бере корпус з входу, виконує крок, передає на вихід, якщо наступний конвеєр приймає |
| Під-слот | object | частина великого кроку | зʼявляється після дослідження спеціалізації; коротший крок |
| Конвеєр авто | conduit | напрям | везе корпус від слота до наступного слота; неправильний напрям — авто не виходить |
| Ресурсний конвеєр | conduit | напрям | везе компоненти від імпорту до слота; перетин з конвеєром авто дорожчий |
| Імпорт ресурсу | source | вид ресурсу | лише на сірих місцях стін; видає компоненти за just-in-time замовленням |
| Експорт | sink | — | на стіні; авто, що пройшло, стає доступним для продажу |
| Дослідний центр | object | — | ставиться будь-де; без нього нема досліджень |
| Корпус авто | resource | дизайн (набір фіч), стан збирання | їде крізь слоти у фіксованому порядку |
| Склад (stock) | container | дизайни, кількість | непродані авто чекають покупця |
| Стіни цеху | static | — | межа поля; носії імпорту/експорту |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(place, slot)` → ЯКЩО `free(cells)` and `counter(money, >=, cost)` → ТО `place(player, slot)`, `currency(-cost)`.
- КОЛИ `input(place, importer)` → ЯКЩО `cell(target, wall_import_spot)` → ТО `place(player, importer)`; інакше `block`.
- КОЛИ `input(place, exporter)` → ЯКЩО `cell(target, wall)` → ТО `place(player, exporter)`.
- КОЛИ `input(drag, resource_conveyor)` → ЯКЩО `occupied(cell, car_conveyor)` → ТО `custom: «перетин дозволено, ціна вища»`.
- КОЛИ `custom: «слот закінчив крок»` → ЯКЩО `custom: «вихідний конвеєр веде у наступний за порядком слот»` → ТО `move(car_body, facing)`; інакше `block` (авто стоїть у слоті).
- КОЛИ `enter(car_body, slot)` → ЯКЩО `has(slot, components)` → ТО `timer(start, work_time)`; інакше `custom: «чекає ресурс»`.
- КОЛИ `timer(work_time)` → ТО `set_state(car_body, step_done)`, `take(slot, components)`.
- КОЛИ `custom: «слоту бракує компонента»` → ТО `custom: «just-in-time замовлення в імпорт»`, `currency(-price)` (?).
- КОЛИ `tick` → ЯКЩО `occupied(conveyor, item)` and `free(cell_ahead)` → ТО `move(item, facing)`.
- КОЛИ `enter(car_body, exporter)` → ЯКЩО `first_time` (для цього набору фіч) → ТО `window(product-naming)`: назва дизайну і ціна.
- КОЛИ `enter(car_body, exporter)` → ТО `custom: «авто йде на склад»`, `counter(stock, +1)`.
- КОЛИ `custom: «на ринку є покупець на дизайн за цю ціну»` → ТО `counter(stock, -1)`, `currency(+price)` (?).
- КОЛИ `custom: «дослідження спеціалізації завершено»` → ЯКЩО `count(research_center, >=, 1)` → ТО `custom: «слот можна замінити під-слотами»` (`+effect:split_slot`).
- КОЛИ `custom: «досліджено фічу авто (фари, підсилювач керма, Bluetooth, голосове керування) або кузов (sedan, SUV, compact)»` → ТО `unlock(feature)`.
- КОЛИ `counter(money, <, 0)` → ЯКЩО `not custom: «є позика»` → ТО `game_over` — банкрутство.
- КОЛИ `input(take_loan)` → ТО `currency(+loan)`, `custom: «відсотки»` (?).
- Перемога: нема фіксованої (тикун-пісочниця) (?) · Поразка: банкрутство · Рахунок: прибуток, собівартість одного авто.

## Керування і ввід
- Мишка: вибрати слот / конвеєр у панелі, клік — поставити; ресурсні конвеєри — click-and-drag.
- Середня кнопка — повернути обʼєкт; правий клік — видалити; Shift+правий клік — видалити ресурсний конвеєр.
- Колесо або PageUp/PageDown — зум.
- Меню слотів (ізометрична піктограма вгорі ліворуч) показує обовʼязковий порядок кроків.

## Вікна, меню, HUD
- `game-screen`: цех, палітра будівель (`tool-palette`), гроші (`coins`), іконка складу авто вгорі ліворуч (`+ui:stock-icon`), індикатори затримок слотів (?).
- `+window:slot-order` — меню слотів: порядок кроків збирання.
- `+window:research-window` — дерево досліджень: виробничі методи (під-слоти) і фічі авто.
- `+window:product-naming` — назва й ціна нового дизайну при першому експорті.
- `custom-window` склад: непродані авто за дизайнами.
- `main-menu`, `settings-window` (роздільна здатність, віконний режим), `pause-menu` (?).

## Фічі поза полем
- Дослідження двох гілок: виробничі методи (дроблення слотів) і продуктові фічі.
- Позики як запобіжник банкрутства.
- Ринок: малотиражне «під замовлення» або масовий ринок проти великих концернів.
- DLC «Doors that go like this», «Design Variety Pack» — нові кузови/дизайни (?).
- Ранній доступ 2017 (?), повний реліз 7.03.2019.

## Варіації й родичі
- У корпусі: `big-pharma` (той самий автор Positech: машина змінює предмет на конвеєрі, ринок і дослідження), `factorio-belts` (конвеєри й постачання), `automachef` (кухня з машинами за рецептом), `shapez`.
- Осі «станція»: один великий крок / дроблення на під-кроки після дослідження / паралельні копії слота для пропускної здатності.
- Осі «постачання»: склад у слоті / just-in-time від імпорту / ручна доставка.

## Цікавинки для курсу
- Фіксований порядок кроків: авто проходить слоти лише по черзі, інакше застрягає — 🌱.
- Дослідження, що заміняє вузол лінії ланцюжком під-вузлів — 📎 (зміна графа потоку).
- Пошук вузького місця: найповільніший слот задає темп усієї лінії — 🥉 (симуляція пропускної здатності).
- Імпорт/експорт лише на стінах + ресурсні конвеєри з перетинами — 📎.
- Дизайн = набір фіч; перший експорт просить назву й ціну; склад і продаж — 🥉.
- Банкрутство з позикою — 🌱.

## Мапа на каталог
- Є: `row-conveyor` · `orientation-state` (напрям конвеєра) · `multi-cell-size` (?) · `impassable-cells` · `cell-click` / `drag-drop-piece` / `hover-highlight` · `round-currency` · `status-panel` · `game-pause` (?) · `save-game` · `in-round-upgrades` (дослідження) · `player-camera` / `field-scaling` (поворот, зум).
- **Нема** → пропозиції карток:
  - `+slot-split-research` «Дослідження дробить станцію на під-станції» · game-logic/economy · 📎.
  - `+wall-import-export` «Вхід і вихід ресурсів лише на краю поля» · entities/legality · 🌱.
  - `+fixed-step-order` «Обовʼязковий порядок станцій» · entities/legality · 🌱.
  - `+resource-conveyor-feed` «Окремий шар конвеєрів постачання» · entities/move · 📎.
  - `+product-naming-price` «Новий продукт: назва й ціна» · game-logic/economy · 🌱.
  - `+finished-stock` «Склад готової продукції й продаж» · game-logic/economy · 📎.
  - `+conveyor-crossing-cost` «Перетин ліній за доплату» · entities/legality · 🌱.
  - `+research-tree`, `+loan-interest` — як у `big-pharma`.

## Пропозиції до словників
- `+trigger:exported` — предмет вийшов через експорт (подія продукту).
- `+cond:feeds_next(slot)` — вихід веде в наступну за порядком станцію.
- `+effect:split_slot` — станція замінюється ланцюжком під-станцій.
- `+window:research-window`, `+window:product-naming` (як у `big-pharma`), `+window:slot-order` — порядок кроків.
- `+ui:stock-icon` — склад непроданої продукції.
- `+feature:loan` — позика проти банкрутства.
- `+card:slot-split-research`, `+card:wall-import-export` — див. вище.

## Джерела
- ⭐ [Steam: Production Line](https://store.steampowered.com/app/591370/) — слоти, що діляться на менші; конвеєри компонентів; just-in-time; дослідження методів і фіч (автофари, підсилювач, Bluetooth, голосове керування); Positech, 7.03.2019.
- [Positech: Production Line](https://www.positech.co.uk/productionline/) — фабрика за методом Форда, «кожен квадратний метр», собівартість авто, «під замовлення» проти масового ринку.
- [Офіційний FAQ](https://mail.positech.co.uk/productionline/faq.html) — меню слотів і порядок, шасі → вісь/каркас/кардан, імпорт лише на сірих місцях стін, експорт на стінах, назва й ціна першого дизайну, сток, дослідні центри, перетин конвеєрів дорожчий, керування мишею.
- YouTube: пошук «Production Line car factory gameplay».

## Непевне
- (?) Розмір слота в клітинах і чи слот-апгрейди (роботи, швидші версії) — окрема механіка від під-слотів.
- (?) Як ринок вирішує, чи куплять авто: очікувана ціна за фічі, попит, конкуренти.
- (?) Як саме нараховується just-in-time вартість компонентів; чи бувають склади ресурсів.
- (?) Позика: відсотки, ліміти.
- (?) Наявність сценаріїв/цілей і чи є пауза й прискорення часу.
- (?) Рік у черзі 2017 — ймовірно ранній доступ; Steam показує 7.03.2019.
- (?) Пошукова видача згадує сортування кузовів Sedan/SUV/Compact як досліджувані — сторінку з цим не відкривав.
