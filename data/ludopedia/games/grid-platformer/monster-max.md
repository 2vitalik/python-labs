---
title: Monster Max
slug: monster-max
aka: []
family: grid-platformer
also: [thinky]
klass: avatar
axes:
  field: iso
  time: realtime
  opponent: none
  info: partial
  random: none
  goal: collect
year: 1994
platforms: [Game Boy]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Monster_Max", best: true, note: "поверхи-академія, 2–3 місії на поверх (2 обовʼязкові), золото → ліфт, термінали місій, кишені на 2 предмети, сумка на 1 блок, бонуси, зброя, паролі, відмінності від Head over Heels"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Monster+Max+Game+Boy+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [push-object, gravity-fall, item-pickup, inventory-items, inventory-limit, temporary-modes, projectile-shot, touch-death, player-death, destroy-all-enemies, collect-quota, round-currency, level-password, map-window, pause-menu, objective-text, game-screen, +carry-in-room, +carry-one-block, +floor-missions-elevator, +mission-terminal, +choose-n-of-m-levels, +button-mapped-slots, +shield-blocks-actions, +crouch-squeeze]
proposes: ["+card:floor-missions-elevator", "+card:mission-terminal", "+card:choose-n-of-m-levels", "+card:button-mapped-slots", "+card:shield-blocks-actions", "+card:crouch-squeeze", "+feature:mission-select"]
author: opus
date: 2026-11-09
---

# Monster Max — спадкоємець Head over Heels на Game Boy: один герой, місії по поверхах академії, порядок дій і переставляння блоків у кімнатах

## Суть
Ізометрична пригода-головоломка від Джона Рітмана й Берні Драммонда (авторів [head-over-heels](head-over-heels.md)); тут — **лише відмінності**. Замість двох героїв, що зливаються, — один Макс, і акцент зміщено з «хто що вміє» на **правильний порядок дій** у кімнаті: куди переставити блоки, коли вимкнути котли й електрику. Гра поділена на поверхи-місії: виконав завдання — отримав золото — купив поїздку ліфтом на наступний поверх.

## Поле і час
- Як у HoH: кімнати — ізометричні коробки з блоків; real-time; гравітація.
- Структура: 9 поверхів академії + 10-й з королем Krond; на поверсі 3 рівні (набори кімнат), обовʼязкові лише 2.
- Кімнати більші, ніж у HoH; кожен поверх має свою тему.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Макс | player | 4 життя на старті, 2 кишені | ходить, з бонусами — біжить, присідає, стрибає; несе 1 блок у сумці |
| Сумка | pickup | місткість 1 блок | взяти/покласти блок; між кімнатами не несе |
| Переставний блок | object | — | платформа/перешкода; переставляється сумкою |
| Котел, електрика | hazard | вкл/викл | треба вимкнути у правильний момент (?) |
| Термінал | static | — | показує завдання наступної кімнати |
| Блискавка | pickup | — | швидша хода |
| Качка | pickup | — | присісти й пролізти в низькі місця |
| Чоботи | pickup | — | дають стрибати |
| Меч | pickup | — | зброя ближнього бою (?) |
| Міни | pickup | — | знищують ворогів і блоки |
| Супер-заклинання | pickup | — | стріляє кулею |
| Зірки | pickup | тривалість | тимчасовий захист від ворогів |
| Енергетичне поле | pickup | тривалість | захист, але не можна ходити й стріляти |
| Додаткове життя | pickup | +1 | — |
| Предмети місії (журнали, сейфи, корони, факели) | pickup | квота | зібрати для виконання завдання |
| Вороги (папуги, роботи, мумії) | enemy | — | дотик шкодить; частину треба знищити за завданням |
| Ліфт | gate | ціна в золоті | веде на наступний поверх |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(slot_a|slot_b)` → ЯКЩО `has(max, item_in_slot)` → ТО `use(max, item)` — кожна з 2 кишень привʼязана до кнопки Game Boy; нижче `input(slot)` = це натискання.
- КОЛИ `contact(max, pickup)` → ЯКЩО `custom: «кишені повні»` → ТО `custom: «вибір, що лишити»` (?); інакше `pickup`.
- КОЛИ `input(bag)` → ЯКЩО `occupied(cell_front, block)` і `not has(max, block)` → ТО `pickup`; повторно → `place(max, block)`.
- КОЛИ `leave(max, room)` → ЯКЩО `has(max, block)` → ТО `custom: «блок лишається в кімнаті»`.
- КОЛИ `input(slot)` → ЯКЩО `has(max, lightning)` → ТО `speed(max, +n)`; ЯКЩО `has(max, duck)` → ТО `set_state(max, crouch)` — проходить низькі проходи; ЯКЩО `has(max, boots)` → ТО `set_state(max, can_jump)`.
- КОЛИ `input(slot)` → ЯКЩО `has(max, mine)` → ТО `place(max, mine)`, `custom: «вибух знищує ворогів і блоки поруч»`; ЯКЩО `has(max, super_spell)` → ТО `spawn(ball)`.
- КОЛИ `input(slot)` → ЯКЩО `has(max, stars)` → ТО `set_state(max, invulnerable, n)`; ЯКЩО `has(max, energy_field)` → ТО `set_state(max, shielded, n)` і `custom: «ходити й стріляти не можна»`.
- КОЛИ `contact(max, enemy)` → ЯКЩО `not state(max, invulnerable)` → ТО `lives(-1)` (?); КОЛИ `counter(lives, =, 0)` → ТО `game_over`.
- КОЛИ `contact(max, terminal)` → ТО `message(next_room_task)`.
- КОЛИ `custom: «завдання виконано»` (знищити ворогів / зібрати N предметів) → ТО `currency(+gold)`.
- КОЛИ `enter(max, lift)` → ЯКЩО `custom: «золота вистачає»` → ТО `currency(-price)`, `next_level` (поверх).
- КОЛИ `custom: «виконано 2 з 3 рівнів поверху»` → ТО ліфт доступний (?).
- 10-й поверх: КОЛИ `counter(objects, =, 4)` → ТО фінальна битва з Krond; перемога → `win`.
- Перемога: скинути Krond. Поразка: життя скінчились. Рахунок: золото (?).

## Керування і ввід
- Хрестовина — 4 ізометричні напрямки; A і B — два предмети в кишенях (саме тому кишень 2).
- Select/Start — пауза з поточною місією, описом предметів і мапою (?).

## Вікна, меню, HUD
- `pause-menu`: поточна місія (`objective-text`), пояснення функцій предметів у кишенях, мапа (`map-window`: де ти й прогрес).
- `level-password`: вийти з місії й продовжити пізніше за паролем.
- `game-screen`: кімната + HUD (кишені A/B, життя, золото (?)).
- `custom-window` «термінал»: завдання наступної кімнати.
- Тренувальний рівень Play Pen на першому поверсі (`tutorial-window`).

## Фічі поза полем
- Паролі замість відсутнього в HoH збереження.
- Вибір 2 з 3 рівнів на поверсі — гравець сам обирає, що пропустити.
- Вбудована мапа (у HoH її не було).

## Варіації й родичі
- Предок: [head-over-heels](head-over-heels.md) (два герої, злиття, сумка без перенесення між кімнатами); ідея кишені — з Batman (1986).
- Родичі ізометричних пазл-пригод: [knight-lore](knight-lore.md), [solstice](solstice.md).
- Осі: **кількість героїв** (два зі злиттям / один з бонусами); **структура** (вільна мапа / поверхи з місіями й ліфтом); **інвентар** (сумка / 2 кишені за кнопками); **збереження** (риба-checkpoint / паролі).

## Цікавинки для курсу
- Кишені, привʼязані до кнопок (інвентар = розкладка вводу) — 🌱.
- Поверхи-місії з валютою за виконання й «ліфтом за золото» — 📎.
- Вибір N з M рівнів поверху для доступу далі — 🌱.
- Щит, що блокує власні дії гравця (поле: захищений, але нерухомий) — 🌱.
- Кімнати-пазли «порядок дій»: переставити блоки, вимкнути котел, потім пройти — 🥉 (дизайн + перевірка прохідності).

## Мапа на каталог
- Є: `push-object` (?) · `gravity-fall` · `item-pickup` · `inventory-items` · `inventory-limit` (2 кишені, 1 блок) · `temporary-modes` (зірки, поле) · `projectile-shot` (супер-заклинання) · `touch-death` · `player-death` · `destroy-all-enemies` · `collect-quota` · `round-currency` (золото) · `level-password` · `map-window` · `pause-menu` · `objective-text` · `game-screen`.
- Уже в корпусі з `+`: `+carry-in-room` (HoH) · `+carry-one-block`.
- **Нема** → пропозиції карток:
  - `+floor-missions-elevator` «Поверх = місії → валюта → перехід за ціну» · levels/progression · 📎.
  - `+mission-terminal` «Термінал показує завдання наступної кімнати» · interface/hud · 🌱.
  - `+choose-n-of-m-levels` «Пройти N з M рівнів» · levels/progression · 🌱.
  - `+button-mapped-slots` «Слоти інвентарю за кнопками» · entities/state · 🌱.
  - `+shield-blocks-actions` «Щит знерухомлює власника» · entities/state · 🌱.
  - `+crouch-squeeze` «Присісти й пролізти в низький прохід» · entities/move · 🌱.

## Пропозиції до словників
- `+feature:mission-select` — гравець обирає, які місії поверху виконати (2 з 3).
- `+card:floor-missions-elevator`, `+card:mission-terminal`, `+card:choose-n-of-m-levels`, `+card:button-mapped-slots`, `+card:shield-blocks-actions`, `+card:crouch-squeeze` — див. вище.

## Джерела
- ⭐ [Wikipedia: Monster Max](https://en.wikipedia.org/wiki/Monster_Max) — поверхи, місії, золото й ліфт, термінали, кишені на 2, сумка на 1 блок, бонуси, зброя, вороги, паролі, відмінності від HoH, автори.
- YouTube: пошук «Monster Max Game Boy gameplay».

## Непевне
- (?) Чи блоки штовхаються, чи лише переносяться сумкою (Wikipedia: «блоки, які можна переставляти»).
- (?) Чи дотик ворога забирає життя одразу чи енергію.
- (?) Що стається при підборі третього предмета, коли кишені повні.
- (?) Склад HUD і як відкривається мапа; що саме дає золото, крім ліфта.
- (?) Як вимикаються котли й електрика (кнопки? блоки?) — джерело згадує лише «вимкнути».
