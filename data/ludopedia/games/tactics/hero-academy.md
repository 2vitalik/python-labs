---
title: Hero Academy
slug: hero-academy
aka: []
family: tactics
also: []
klass: figure
axes:
  field: square
  time: turn
  opponent: online
  info: partial
  random: runtime
  goal: state
year: 2012
platforms: [iOS, Windows, macOS, Android]
links:
  - {kind: other, url: "https://destructoid.com/?p=122360", best: true, note: "гайд Destructoid: поле 9×5, 5 дій, колода й рука, бонус-клітини, трупи, усі юніти й предмети Ради з числами"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Hero_Academy", note: "умови перемоги, 5 ходів, рука з юнітів/заклять/зілля/спорядження, команди, платформи, закриття 2019"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Hero+Academy+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [hp-damage, melee-vs-ranged, push-object, explode-area, inventory-items, pocket, async-multiplayer, online-multiplayer, turn-enforcement, shop-window, game-screen, end-screen, +action-points, +hand-of-tiles, +deck-draw, +card-replace, +bonus-tile-cells, +crystal-objective, +corpse-revive-window, +stomp-corpse, +chain-lightning, +swap-ability, +damage-type-resist, +equipment-no-stack, +turn-reset-before-submit, +cross-platform-play, +faction-teams]
proposes: ["+effect:revive", "+effect:knockback", "+effect:draw_card", "+effect:discard", "+effect:equip", "+trigger:attacked", "+role:objective", "+role:card", "+ui:deck-counter", "+ui:action-pips", "+ui:submit-button", "+window:match-list", "+window:faction-select", "+feature:turn-reset"]
author: opus
date: 2026-11-09
---

# Hero Academy — асинхронна дуель на полі 9×5: п'ять дій на хід, юніти й предмети з руки, мета — розбити кристали суперника

## Суть
Двоє гравців по черзі мають по **5 дій** на хід і витрачають їх як завгодно: виставити юніта з руки, походити, атакувати, надягти предмет, скинути плитку. Рука — випадкові плитки з колоди команди (юніти, закляття, зілля, спорядження) і добирається після ходу. Мета — зруйнувати кристал(и) суперника або знищити всі його доступні юніти. Партії асинхронні: хід відправляють, а суперник відповідає коли зможе — партія триває від пів дня до тижня.

## Поле і час
- Поле 9×5 клітин; на ньому кристали обох сторін і особливі клітини (меч, щит, кристал-штурм).
- Хід = 5 дій одного гравця; до відправлення хід можна скинути й переграти; відправлений хід не повертається.
- Партія асинхронна, крос-платформна (iOS, PC, Mac, Android).
- Інформація часткова: рука й колода суперника приховані, видно лише лічильник колоди.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Кристал | objective | HP (?) | зруйновано всі кристали гравця — він програв |
| Лицар (Рада) | piece | 1200 HP; рух 2; дальність 1; 200 фізичної; опір фізичній 20 % | удар відкидає ціль на 1 клітину |
| Лучниця | piece | 800 HP; рух 2; дальність 3; 300 фізичної | впритул — лише 50 % шкоди |
| Чарівник | piece | 800 HP; рух 2; дальність 2; 200 магічної | ланцюгова блискавка: наступні цілі 75 % і 50 % |
| Клірик | piece | 800 HP; рух 2; дальність 2; 200 магічної | лікує й воскрешає в радіусі 2 |
| Ніндзя (суперюніт) | piece | 800 HP; рух 3; дальність 2; 200 фізичної | міняється місцями з будь-яким юнітом; подвійна шкода впритул |
| Труп (вибитий юніт) | object | — | лежить до кінця наступного ходу власника; можна воскресити; юніт, ставши на нього, прибирає (1 дія) |
| Клітина «Меч» | terrain | +100 шкоди | бонус, доки юніт стоїть на ній |
| Клітина «Щит» | terrain | +20 % фізичного захисту | бонус, доки стоїть |
| Клітина «Кристал» (штурм) | terrain | +300 шкоди по кристалу | бонус до атаки кристала |
| Рунний меч | pickup | +50 % сили | надягається на юніта |
| Луска дракона (щит) | pickup | +20 % фізичного опору | надягається |
| Сяйний шолом | pickup | +20 % магічного опору, +10 % макс. HP | надягається; однакові типи не складаються |
| Зілля відродження | pickup | лікує 1000 HP або воскрешає | разове |
| Суперзаряд (сувій) | pickup | ×3 шкоди | на одну атаку |
| Пекло (Inferno) | pickup | 350 магічної, 3×3 | шкода площею й прибирає трупи в ній |
| Рука | supply | — | плитки для виставлення/застосування |
| Колода («двері») | supply | лічильник | звідси добирається рука; плитку можна скинути в двері за нову |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(player)` → ТО `counter(actions, =5)`.
- КОЛИ `input(deploy, unit_tile, cell)` → ЯКЩО `counter(actions, >=, 1)` і `free(cell)` → ТО `place(player, unit)`, `counter(actions, -1)`.
- КОЛИ `input(move, unit, cell)` → ЯКЩО `in_range(unit, cell, move)` і `free(cell)` → ТО `move(unit, cell)`, `counter(actions, -1)`.
- КОЛИ `input(attack, unit, target)` → ЯКЩО `in_range(unit, target, range)` → ТО `damage(target, power × (1 − resist_of_type))`, `counter(actions, -1)`; фізична шкода зменшується фізичним опором, магічна — магічним.
- КОЛИ `input(attack, knight, target)` → ЯКЩО `free(cell_behind_target)` → ТО `push(target)` на 1 клітину.
- КОЛИ `input(attack, archer, target)` → ЯКЩО `in_range(archer, target, 1)` → ТО `custom: «шкода ×0.5»`.
- КОЛИ `input(attack, ninja, target)` → ЯКЩО `in_range(ninja, target, 1)` → ТО `custom: «шкода ×2»`.
- КОЛИ `input(attack, wizard, target)` → ТО `damage(target, n)`, `custom: «блискавка перескакує на наступну ціль: 75 %, далі 50 %»`.
- КОЛИ `input(swap, ninja, unit)` → ТО `swap(ninja, unit)` (будь-який юніт на полі), `counter(actions, -1)`.
- КОЛИ `input(heal, cleric, ally)` → ЯКЩО `in_range(cleric, ally, 2)` → ТО `heal(ally, n)`; ЯКЩО `state(ally, knocked_out)` → ТО `custom: «revive»`.
- КОЛИ `input(equip, item, unit)` → ЯКЩО `not has(unit, same_item_type)` → ТО `give(unit, item)`, `counter(actions, -1)` — бонуси до сили/опору/HP.
- КОЛИ `input(use, supercharge, unit)` → ТО `set_state(unit, supercharged)`; КОЛИ `after(attack)` → ЯКЩО `state(unit, supercharged)` → ТО `custom: «шкода ×3»`, `clear_state(unit, supercharged)`.
- КОЛИ `input(use, inferno, cell)` → ТО `explode(3x3, 350)`, `disappear(corpses_in_area)`.
- КОЛИ `input(use, revive_potion, unit)` → ТО `heal(unit, 1000)` або `custom: «revive»`.
- КОЛИ `enter(unit, sword_cell)` → ТО `set_state(unit, power_boost)`; КОЛИ `leave(unit, sword_cell)` → ТО `clear_state(unit, power_boost)`; так само «Щит» і «Кристал».
- КОЛИ `hp_zero(unit)` → ТО `transform(unit, corpse)`.
- КОЛИ `enter(unit, corpse)` → ТО `disappear(corpse)`, `counter(actions, -1)` (воскресити його вже не можна).
- КОЛИ `turn_end(owner)` → ЯКЩО `custom: «труп пролежав до кінця наступного ходу власника»` → ТО `disappear(corpse)`.
- КОЛИ `input(discard, tile)` → ЯКЩО `counter(actions, >=, 1)` → ТО `custom: «плитка в колоду, взамін нова»`, `counter(actions, -1)`.
- КОЛИ `turn_end(player)` → ТО `custom: «рука добирається з колоди»`.
- КОЛИ `input(reset)` → ЯКЩО `custom: «хід ще не відправлено»` → ТО `undo(all)`, `counter(actions, =5)`.
- КОЛИ `input(submit)` → ТО `end_turn`.
- КОЛИ `all_gone(enemy_crystal)` → ТО `win`.
- КОЛИ `custom: «у суперника нема юнітів ні на полі, ні в руці й колоді»` → ТО `win`.
- Перемога: зруйнувати всі кристали або всі доступні юніти суперника · Поразка: дзеркально · Рахунок: —.

## Керування і ввід
- Тач/миша: drag плитки з руки на клітину — виставити юніта чи застосувати предмет; тап юніта → тап клітини (рух) або ворога (атака).
- Плитку перетягнути на «двері» — обміняти на нову з колоди.
- Кнопки «скинути хід» і «відправити хід»; дії до відправки — пробні.

## Вікна, меню, HUD
- `+window:match-list` — список поточних асинхронних партій («чий хід»), запрошення, реванш.
- `+window:faction-select` — вибір команди для нової партії (Рада за замовчуванням; Темні ельфи, Гноми, Плем'я, Team Fortress 2, Шаолінь — доповнення).
- `shop-window` — купівля команд.
- `game-screen`: поле 9×5; `pocket` (рука плиток); `+ui:deck-counter` на дверях; `+ui:action-pips` (5 дій); кнопки reset і `+ui:submit-button`; `hp-bar` юнітів; HP кристалів.
- `end-screen` — перемога/поразка, реванш.
- Переходи: match-list → game-screen (хід) → submit → match-list; нова партія → faction-select → game-screen.

## Фічі поза полем
- Асинхронний онлайн з крос-платформою; кілька партій одночасно.
- Команди-доповнення з власними юнітами й предметами; команда TF2 — ексклюзив Steam, але грається на всіх платформах.
- Скидання ходу до відправки (`undo` у межах ходу).
- Сервери закрито 8.04.2019 (разом з Hero Academy 2).

## Варіації й родичі
- Hero Academy 2 (2017–2019) — сиквел; закрився разом з першою.
- Команди: Темні ельфи (використовують трупи, темна магія), Гноми (вибухові атаки, бонуси на спецклітинах), Плем'я (агресія), Шаолінь (навернення ворогів, комбінаційні атаки), TF2.
- Родичі: [Duelyst](duelyst.md) (карти-юніти на сітці 9×5, генерал замість кристала), [Faeria](faeria.md), [Summoner Wars](summoner-wars.md) (настільна дуель призивачів), [Dofus](dofus.md) (бюджет дій на хід).
- **Осі варіацій**: бюджет ходу — одна дія на юніта (шахи, FE) / спільний пул дій на всіх (Hero Academy: 5) / ОД кожного юніта (XCOM, Dofus) · ціль — король/генерал / кристали / знищити всіх · смерть юніта — миттєва / труп з вікном воскресіння.

## Цікавинки для курсу
- Спільний пул 5 дій на будь-яких юнітів і будь-які дії (виставити, рух, атака, предмет, скинути) — 📎.
- Труп з вікном воскресіння до кінця наступного ходу + «затоптати» його дією — 🥉 (стан із таймером у ходах власника).
- Бонус-клітини, що діють, лише доки юніт на них стоїть — 📎.
- Ланцюгова блискавка 100 → 75 → 50 % по сусідніх цілях — 🥉 (пошук наступної цілі).
- Фізична/магічна шкода проти двох опорів, предмети одного типу не складаються — 📎.
- Асинхронна партія: хід як пакет дій, «скинути до відправки», список партій — 🥈 (серверний стан, пробний локальний хід).

## Мапа на каталог
- Є: `hp-damage` · `melee-vs-ranged` (лучниця впритул 50 %) · `push-object` (відкидання лицарем) · `explode-area` (Пекло 3×3) · `inventory-items` (спорядження на юніті) · `pocket` (рука) · `async-multiplayer` · `online-multiplayer` · `turn-enforcement` · `shop-window` · вікна.
- **Нема** → пропозиції карток:
  - `+action-points` «Пул дій на хід» · game-logic/opponent · 🌱 · слот {n: 5}.
  - `+hand-of-tiles` + `+deck-draw` «Рука з колоди, добір після ходу» · game-logic/economy · 📎.
  - `+card-replace` «Скинути плитку за нову» · game-logic/economy · 🌱.
  - `+bonus-tile-cells` «Клітини-бонуси, поки стоїш» · entities/state · 📎.
  - `+crystal-objective` «Знищити обʼєкт-ціль суперника» · game-logic/win · 🌱.
  - `+corpse-revive-window` «Труп з вікном воскресіння» · entities/state · 🥉.
  - `+chain-lightning` «Ланцюгова атака зі спаданням» · entities/combat · 🥉 · слот {falloff}.
  - `+turn-reset-before-submit` «Скинути хід до відправки» · game-logic/history · 📎.

## Пропозиції до словників
- `+effect:revive` — повернути вибитого юніта з трупа; `+effect:knockback` — удар відкидає ціль (лицар).
- `+effect:draw_card` — добрати плитку з колоди (у словнику `draw` = нічия); `+effect:discard` — скинути плитку; `+effect:equip` — надягти предмет на юніта (≠ `give`: діє як модифікатор характеристик).
- `+trigger:attacked` — юніт отримав атаку (точка для відкидання й ланцюга).
- `+role:objective` — кристал: ціль атаки без власної поведінки; `+role:card` — плитка руки.
- `+ui:deck-counter` — «двері» з кількістю плиток; `+ui:action-pips` — 5 дій; `+ui:submit-button` — відправити хід.
- `+window:match-list` — список асинхронних партій; `+window:faction-select` — вибір команди.
- `+feature:turn-reset` — скинути всі дії до відправки ходу.

## Джерела
- ⭐ [Destructoid: гайд для початківців](https://destructoid.com/?p=122360) — поле 9×5, 5 дій, двері-колода, бонус-клітини, трупи, фізична/магічна шкода, усі юніти й предмети Ради з числами.
- [Wikipedia: Hero Academy](https://en.wikipedia.org/wiki/Hero_Academy) — умови перемоги, рука, команди, платформи й дати, сиквел, закриття.
- YouTube: пошук «Hero Academy gameplay».

## Непевне
- (?) HP кристала і чи є в команди кілька кристалів за замовчуванням — у гайді не сказано (Wikipedia: «one or more crystals»).
- (?) Клітини розгортання: чи можна виставляти юніта будь-куди, чи лише на спецклітини біля своїх кристалів — гайд мовчить.
- (?) Розмір руки й колоди, чи добір — до повної руки.
- (?) Хто може «затоптати» труп — гайд каже лише, що юніт, ставши на труп, прибирає його за 1 дію; чи це роблять і свої, і ворожі юніти — не уточнено.
- (?) Рік у черзі 2012 — збігається з iOS-релізом 11.01.2012; PC — 10.08.2012.
