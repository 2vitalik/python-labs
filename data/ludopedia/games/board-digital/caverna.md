---
title: "Caverna: The Cave Farmers (Каверна)"
slug: caverna
aka: [Каверна, Caverna The Cave Farmers, Caverna Cave vs Cave]
family: board-digital
also: [build-sim]
klass: cursor
axes:
  field: square
  time: turn
  opponent: hotseat
  info: full
  random: setup
  goal: score
year: 2013
platforms: [board, PC]
links:
  - {kind: other, url: "https://www.ultraboardgames.com/caverna/actions.php", best: true, note: "дії й викладання на домашню дошку: подвійні тайли ліс/гора, одинарні за рубіни, пасовища, стайні, собаки, шахти, облаштування печер, ріст родини, сівба, кування"}
  - {kind: other, url: "https://www.ultraboardgames.com/caverna/game-rules.php", note: "базові правила: дошка ліс + гора, 12 раундів, урожаї й маркери, годування, жебрацтво, конверсія в їжу, зброя, рахунок і −1 за порожню клітину"}
  - {kind: other, url: "https://www.ultraboardgames.com/caverna/expeditions.php", note: "експедиції: рівні 1–4, мінімальна сила зброї для здобичі, +1 сила після кожної"}
  - {kind: other, url: "https://www.ultraboardgames.com/caverna/index.php", note: "огляд: 2013, Uwe Rosenberg, 1–7 гравців, собаки й осли"}
  - {kind: steam, url: "https://store.steampowered.com/app/3216750/Caverna/", note: "цифрова версія DIGIDICED (2025): AI, онлайн і асинхронна гра, 1–7 гравців"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Caverna+how+to+play", note: "пошук; як грати"}
stage: v1
coverage: 55
mechanics: [cell-click, drag-drop-piece, hover-highlight, legal-move-highlight, connectivity-check, inventory-limit, event-points, leftover-penalty, turn-enforcement, hot-seat, ai-opponent, online-multiplayer, async-multiplayer, match-setup, end-screen, help-window, save-game, multi-cell-size, +worker-placement, +domino-tile, +two-zone-board, +orthogonal-growth, +pasture-capacity, +stable-doubles-capacity, +one-type-per-pasture, +animal-breeding, +feeding-phase, +begging-penalty, +unused-cell-penalty, +missing-category-penalty, +furnishing-on-cell, +weapon-strength-order, +loot-by-strength, +harvest-schedule, +accumulating-action-space, +premium-currency-single-tile]
proposes: ["+trigger:harvest", "+cond:capacity(region, op, n)", "+cond:orth_adjacent(cell, kind)", "+cond:zone(cell, forest|mountain)", "+effect:breed(kind)", "+effect:feed(n)", "+effect:forge(strength)", "+role:pasture", "+role:worker", "+ui:capacity-badge", "+window:harvest-summary", "+window:expedition-loot", "+card:domino-tile-zoned", "+card:loot-by-strength"]
author: opus
date: 2026-11-09
---

# Caverna — особиста дошка з двох половин: ліс розчищають подвійними тайлами під поля й пасовища, гору прокопують під печери, шахти й житла

## Суть
Сестра Agricola від того самого автора: робітники-гноми займають спільні поля дій, а результат лягає на особисту дошку. Дошка поділена на **ліс** (поля, луки → пасовища, стайні) і **гору** (печери, тунелі → шахти); основний будівельний блок — подвійний тайл на дві сусідні клітини, як доміно. Печери облаштовують тайлами-меблями (житла, склади, кімнати з бонусами), а озброєний гном ходить в експедиції за здобиччю за таблицею сили зброї. Карт у руці нема — уся інформація відкрита.

## Поле і час
- Особиста дошка — прямокутна сітка з двох зон: ліс (ліворуч) і гора (праворуч); у горі вхід до печери і дві надруковані печери (житло на 2 гноми + порожня).
- Шари: клітина зони (порожній ліс / гора) → тайл (поле, лука, пасовище, печера, тунель, глибокий тунель, шахта) → облаштування печери або стайня → тварини й урожай.
- Час: 12 раундів (на двох — 11); раунд: нове поле дії → поповнення накопичувальних полів → робота (гноми по одному, за годинниковою стрілкою) → повернення → (не завжди) урожай.
- Урожаї: раунд 3 — так, 4 — лише 1 їжа за гнома, з 5-го — за маркерами урожаю, розкладеними горілиць-донизу на раундах 6–12.
- Випадковість: лише порядок появи нових полів дій і маркерів урожаю.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітина лісу | terrain | зона forest | під поле, луку, стайню |
| Клітина гори | terrain | зона mountain | під печеру, тунель |
| Подвійний тайл Лука/Поле | tile | 2 клітини лісу | перший — перед входом до печери; далі — дотик до поля, луки чи пасовища |
| Подвійний тайл Печера/Тунель | tile | 2 клітини гори | прилягає до наявної печерної системи |
| Подвійний тайл Печера/Печера | tile | 2 клітини гори | лише дією Excavation |
| Одинарні тайли | tile | ціна в рубінах | поле/лука 1, тунель 1, печера 2 рубіни |
| Поле | terrain | засіяне / порожнє | зерно 1+2, овоч 1+1; урожай знімає 1 |
| Лука → Пасовище | zone | мале (1 клітина, 2 дерева) / велике (2 клітини, 4 дерева) | тримає тварин одного виду; назавжди |
| Стайня | static | ≤3, 1 камінь | ліс/лука/пасовище, не поле й не гора; подвоює ємність огородженої луки |
| Печера | static | порожня / облаштована | лише сюди кладеться облаштування |
| Тунель / глибокий тунель | terrain | — | під шахти |
| Рудна шахта | static | 2 звичайні тунелі | +2 руди за дію видобутку; 3 очки; 1 осел |
| Рубінова шахта | static | 1 тунель | +1 рубін, якщо на глибокому тунелі; 4 очки; 1 осел |
| Житло | container | 1–2 гноми | ліміт родини; звичайне — 4 дерева + 3 камені |
| Облаштування | static | ціна, очки | кожне в одному екземплярі (крім звичайного житла) |
| Гном | player | зброя 0–14 | займає поле дії; озброєні ходять після неозброєних за зростанням сили |
| Тварини: вівця, осел, кабан, корова | object | вид | ≥2 одного виду → +1 приплід, якщо є місце |
| Собака | neutral | — | не тварина ферми; пасе лише овець |
| Поле дії | zone | 1 гном | спільне; накопичувальні поля ростуть щораунду |
| Маркер жебрацтва | hazard | −3 очки | за кожну нестачу їжі |

## Правила (КОЛИ → ЯКЩО → ТО)
- Робота: КОЛИ `input(place(dwarf, action_space))` → ЯКЩО `free(action_space)` and `turn_of(p)` → ТО `place(dwarf)` + `custom: «виконати дію поля»`.
- Порядок озброєних: ЯКЩО `custom: «у гравця є неозброєні гноми»` → ТО озброєний `block`; озброєні — за зростанням сили; `take(p, ruby)` дозволяє порушити порядок для одного гнома.
- Подвійний тайл у горі: КОЛИ `input(place(cavern_tunnel, 2 cells))` → ЯКЩО `custom: «обидві клітини — порожня гора, сусідні між собою»` and `custom: «прилягає до наявної печерної системи»` → ТО `place(tile)`.
- Подвійний тайл у лісі: КОЛИ `input(place(meadow_field, 2 cells))` → ЯКЩО `custom: «дві сусідні клітини лісу (можна зі стайнею)»` and (`custom: «перед входом до печери — для першого»` or `custom: «дотик до поля/луки/пасовища»`) → ТО `place(tile)`.
- Нема місця: ЯКЩО `custom: «нема легальних двох клітин»` → ТО `block`; замінити подвійний тайл одинарним не можна.
- Одинарний тайл: КОЛИ `input(custom: «купити тайл за рубіни»)` → ЯКЩО `has(p, ruby)` → ТО `take(p, ruby)` + `place(tile)` з тими самими вимогами суміжності.
- Пасовище: КОЛИ `input(custom: «огородити»)` → ЯКЩО `cell(x, meadow)` and `has(p, 2|4 wood)` → ТО `transform(meadow, pasture)`; за дію — ≤1 мале і ≤1 велике; поле, ліс і гору огородити не можна.
- Стайня: КОЛИ `input(place(stable, cell))` → ЯКЩО `counter(stables, <, 3)` and `not cell(x, field)` and `not cell(x, mountain)` and `has(p, 1 stone)` → ТО `place(stable)`; ≤1 на клітину, на великому пасовищі ≤2.
- Ємність: ЯКЩО `custom: «огороджена лука зі стайнею»` → ТО `custom: «ємність ×2»`; ЯКЩО `occupied(pasture, dog)` → ТО лише вівці.
- Облаштування: КОЛИ `input(place(furnishing, cell))` → ЯКЩО `cell(x, empty_cavern)` and `has(p, cost)` → ТО `place(furnishing)`; не на тунель, шахту чи порожню гору; назавжди.
- Ріст родини: КОЛИ `input(custom: «ріст родини»)` → ЯКЩО `custom: «є вільне місце в житлах»` and `counter(dwarfs, <, 5)` → ТО `spawn(dwarf)`; новий не діє цього раунду.
- Рудна шахта: КОЛИ `input(place(ore_mine, 2 tunnels))` → ЯКЩО `custom: «два сусідні звичайні тунелі, не глибокі»` → ТО `place(mine)` + `give(p, 3 ore)`.
- Рубінова шахта: КОЛИ `input(place(ruby_mine, tunnel))` → ЯКЩО `cell(x, deep_tunnel)` → ТО `give(p, ruby)`.
- Видобуток: КОЛИ `input(custom: «ore mining»)` → ТО `give(p, accumulated)` + `custom: «+2 руди за кожну рудну шахту»`.
- Кування: КОЛИ `input(custom: «кувати»)` → ЯКЩО `custom: «гном неозброєний»` and `has(p, 1..8 ore)` → ТО `custom: «сила зброї = витрачена руда»`.
- Експедиція: КОЛИ `input(custom: «експедиція рівня L»)` → ЯКЩО `custom: «гном озброєний»` → ТО `choose(L loot)` з таблиці, ЯКЩО `custom: «мінімальна сила предмета ≤ сили зброї»`; кожен предмет ≤1 раз; потім `custom: «сила +1, максимум 14»`.
- Урожай — поля: КОЛИ `custom: «фаза полів урожаю»` → ТО `take(field, 1 grain|vegetable)`.
- Урожай — годування: ТО `custom: «2 їжі на гнома, новонароджений — 1»`; ЯКЩО `custom: «їжі бракує»` → ТО `give(p, begging)` за кожну одиницю; звільнити гнома не можна.
- Урожай — приплід: ЯКЩО `count(animal_kind, >=, 2)` and `custom: «є місце»` → ТО `spawn(animal)`; ≤1 на вид; новонароджених і батьків одразу не зʼїсти.
- Маркер урожаю: ЯКЩО `custom: «перший червоний ?»` → ТО урожаю нема; `custom: «другий»` → 1 їжа за гнома; `custom: «третій»` → кожен обирає поля або приплід, годування завжди.
- Їжа: ТО `custom: «конверсія: вівця 1, кабан 2, корова 3, осел 1 (двоє — 3), зерно 1, овоч 2, рубін 2; золото — на 1 більше за їжу»`.
- Рахунок: `score(1)` за тварину ферми й собаку · `score(−2)` за кожен відсутній вид (вівця, осел, кабан, корова) · зерно ÷ 2 вгору · `score(1)` за овоч, рубін, гнома · пасовище мале 2 / велике 4 · рудна шахта 3 / рубінова 4 · облаштування — надруковане + бонуси · золото · `score(−3)` за жебрацтво.
- Порожнеча: КОЛИ `game_over` → ТО `score(−1)` за кожну клітину без тайла й стайні; надруковані й необлаштовані печери — зайняті.
- Перемога: найбільше очок; можливі кілька переможців.

## Керування і ввід
- Цифрова версія: клік по вільному полю дії ставить гнома; далі — режим дошки для цієї дії.
- Подвійний тайл: drag з поворотом на дві сусідні клітини потрібної зони (`multi-cell-size`), підсвітка легальних пар.
- Огородження, стайні, облаштування — клік по клітині з підсвіткою; тварини — перетягування між пасовищами, стайнями й житлами.
- Експедиція — вікно вибору здобичі з недоступними (за силою) предметами сірим.

## Вікна, меню, HUD
(цифрова версія; Steam DIGIDICED 2025 — деталі екранів не бачив)
- `main-menu`: Нова гра → `match-setup` · Онлайн · Правила → `help-window`.
- `match-setup`: 1–7 гравців, люди/AI, соло-режим.
- `game-screen`: поле дій (раунд, наступний урожай), дошка гравця з двома зонами, ринок облаштувань, запас ресурсів, `turn-indicator`, `capacity-badge` (кандидат), сила зброї гномів.
- `opponent-boards` — дошки суперників.
- `expedition-loot` (кандидат): таблиця здобичі з порогами сили.
- `harvest-summary` (кандидат): поля → годування → приплід.
- `end-screen`: таблиця категорій × гравці.
- Переходи: main-menu → match-setup → game-screen ⇄ expedition-loot / harvest-summary → end-screen.

## Фічі поза полем
- `hotseat` 1–7; `online-multiplayer` і асинхронна гра (Steam); `ai-opponent-levels` (?).
- Соло-режим (окрема сторінка правил).
- `custom-rules`: розмір додаткових дошок дій за кількістю гравців; на двох — 11 раундів.

## Варіації й родичі
- Прямий предок: [agricola-farm-grid](agricola-farm-grid.md) — паркани на ребрах замість подвійних тайлів, картки занять і поліпшень у руці (тут їх нема).
- Того самого автора: [a-feast-for-odin-polyomino](a-feast-for-odin-polyomino.md), [patchwork](patchwork.md), [cottage-garden](cottage-garden.md).
- Доміно-тайли на особистій сітці: [kingdomino](kingdomino.md); облаштування кімнат з бонусами — [castles-of-mad-king-ludwig](castles-of-mad-king-ludwig.md).
- Caverna: Cave vs Cave — спрощена версія на двох (?).
- **Осі варіацій**: межі областей (паркани на ребрах / подвійні тайли) · зони дошки (одна / ліс + гора) · житло (кімнати ростуть / печери облаштовують) · приховане (картки в руці / усе відкрите) · бойова гілка (нема / зброя + експедиції).

## Цікавинки для курсу
- Подвійний тайл на дві сусідні клітини однієї зони з правилом суміжності до своєї системи — 📎.
- Дві зони дошки з різними допустимими тайлами й «вхід до печери» як точка старту лісу — 🌱.
- Ємність пасовищ і стаєнь, собаки лише з вівцями, розміщення тварин як задача пакування — 🥉.
- Експедиції: вибір N предметів з таблиці за порогом сили, кожен раз, +1 сила — 🌱.
- Порядок ходу озброєних гномів за силою зброї (з винятком за рубін) — 🌱.
- Фінальний рахунок із −2 за відсутній вид і −1 за порожню клітину — 🌱.
- AI для Caverna — 👑.

## Мапа на каталог
- Є: `cell-click` · `drag-drop-piece` · `hover-highlight` · `legal-move-highlight` · `connectivity-check` (печерна система) · `inventory-limit` (ємність) · `event-points` · `leftover-penalty` · `turn-enforcement` · `hot-seat` · `ai-opponent` · `online-multiplayer` · `async-multiplayer` · `match-setup` · `end-screen` · `help-window` · `save-game` · `multi-cell-size` (подвійний тайл).
- Уже в корпусі: `+worker-placement`, `+pasture-capacity`, `+stable-doubles-capacity`, `+one-type-per-pasture`, `+animal-breeding`, `+feeding-phase`, `+begging-penalty`, `+unused-cell-penalty`, `+orthogonal-growth`, `+harvest-schedule` (Agricola); `+domino-tile` (Kingdomino).
- **Нема** → пропозиції карток:
  - `+two-zone-board` «Особиста дошка з зонами, що приймають різні тайли» · entities/legality · 🌱.
  - `+missing-category-penalty` «Мінус за кожну відсутню категорію» · game-logic/score · 🌱.
  - `+furnishing-on-cell` «Поліпшення кладеться лише на клітину певного типу» · entities/legality · 🌱.
  - `+weapon-strength-order` «Черговість робітників за параметром» · game-logic/turns · 🌱.
  - `+loot-by-strength` «Вибір N нагород з таблиці за порогом сили» · game-logic/economy · 🌱.
  - `+accumulating-action-space` «Поле дії накопичує ресурс, доки не взяли» · game-logic/economy · 🌱.
  - `+premium-currency-single-tile` «Рідкісна валюта знімає обмеження форми (одинарний тайл замість подвійного)» · game-logic/economy · 🌱.

## Пропозиції до словників
- `+trigger:harvest` — подія за розкладом раундів (як в Agricola).
- `+cond:capacity(region, op, n)` · `+cond:orth_adjacent(cell, kind)` — як в Agricola.
- `+cond:zone(cell, forest|mountain)` — клітина належить зоні дошки.
- `+effect:breed(kind)` · `+effect:feed(n)` · `+effect:forge(strength)`.
- `+role:pasture` · `+role:worker`.
- `+ui:capacity-badge`.
- `+window:harvest-summary` · `+window:expedition-loot`.
- `+card:domino-tile-zoned` — доміно, обидві половини якого мусять лягти в одну зону; `+card:loot-by-strength`.

## Джерела
- ⭐ [UBG: Caverna Actions](https://www.ultraboardgames.com/caverna/actions.php) — подвійні й одинарні тайли, суміжність, пасовища (2/4 дерева), стайні (≤3, 1 камінь), собаки й вівці, шахти, облаштування, ріст родини, сівба, видобуток, кування 1–8 руди.
- [UBG: Basic Game Rules](https://www.ultraboardgames.com/caverna/game-rules.php) — дошка ліс + гора, сетап, 12 раундів, маркери урожаю, годування, жебрацтво, конверсія в їжу, рахунок.
- [UBG: Expeditions](https://www.ultraboardgames.com/caverna/expeditions.php) — рівні 1–4, пороги сили, максимум 14, порядок озброєних.
- [UBG: Overview](https://www.ultraboardgames.com/caverna/index.php) — 2013, Uwe Rosenberg, 1–7 гравців.
- [Steam: Caverna](https://store.steampowered.com/app/3216750/Caverna/) — DIGIDICED, 28.04.2025, AI, онлайн, асинхрон, 1–7.

## Непевне
- (?) Розмір домашньої дошки (кількість клітин у кожній зоні) — сторінки UBG не наводять.
- (?) Базова ємність пасовища й стайні без паркану — UBG каже лише «стайня подвоює», приклади: стайня в лісі — до 3 кабанів (?), велике пасовище зі стайнею — 8.
- (?) Повна таблиця здобичі експедицій і пороги — лише на картці-огляді (зображення).
- (?) Що таке глибокий тунель і як він зʼявляється на дошці — UBG згадує лише в правилі рубінової шахти.
- (?) Cave vs Cave як окрема гра на двох — з памʼяті.
- (?) Раніша цифрова версія (до Steam 2025) — не перевіряв.
