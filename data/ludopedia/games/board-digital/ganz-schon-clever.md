---
title: Ganz Schön Clever (That's Pretty Clever)
slug: ganz-schon-clever
aka: [That's Pretty Clever!, Ganz schön clever, «Дуже розумно», GSC]
family: board-digital
also: [word-number]
klass: cursor
axes:
  field: square
  time: turn
  opponent: hotseat
  info: full
  random: runtime
  goal: score
year: 2018
platforms: [board]
links:
  - {kind: other, url: "https://www.ultraboardgames.com/thats-pretty-clever/game-rules.php", best: true, note: "повні правила: 3 кидки, срібна таця, пасивні гравці, 5 областей аркуша, білий кубик-джокер, бонуси, дії reroll/+1, лиси, рахунок"}
  - {kind: bgg, url: "https://boardgamegeek.com/geeksearch.php?action=search&q=Ganz+Schon+Clever", note: "пошук BGG; сиквели Doppelt so clever, Clever hoch drei"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=Clever", note: "пошук цифрової версії"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Ganz+Schon+Clever+how+to+play", note: "пошук; пояснення правил"}
stage: v1
coverage: 60
mechanics: [cell-click, hover-highlight, legal-move-highlight, selection-highlight, turn-enforcement, hot-seat, simultaneous-versus, event-points, chain-reaction, completion-detection, game-settings, match-setup, game-screen, end-screen, help-window, score-records, +dice-roll-pool, +roll-and-write, +sub-lower-dice-tray, +passive-player-pick, +multi-area-sheet, +ascending-sequence-rule, +threshold-track, +multiplier-cells, +sum-of-two-dice, +wild-die, +bonus-chain-cascade, +action-tokens-reroll, +extra-die-action, +min-color-score, +escalating-track-score, +row-column-bonus, +round-start-bonus, +tiebreak-chain]
proposes: ["+effect:roll", "+effect:cross_box", "+effect:to_tray", "+cond:value_at_least", "+cond:ascending", "+trigger:box_filled", "+role:die", "+role:sheet-area", "+ui:dice-pool", "+ui:silver-tray", "+ui:score-sheet", "+card:sub-lower-dice-tray", "+card:passive-player-pick", "+card:bonus-chain-cascade", "+card:wild-die"]
author: opus
date: 2026-11-09
---

# Ganz Schön Clever — три кидки шести кубиків: узяв великий — менші йдуть суперникам на тацю, а кожен хрестик може ланцюжком запустити ще кілька

## Суть
Roll-and-write: активний гравець кидає 6 кольорових кубиків тричі, щоразу бере один і записує його значення в область аркуша свого кольору. Усі кубики з меншим значенням ідуть на «срібну тацю» — з неї потім вибирають пасивні гравці, а активний втрачає їх для наступних кидків. Аркуш має 5 областей із різними правилами запису; заповнені клітинки дають бонуси (хрестик в іншій області, дію reroll чи «+1 кубик», лиса), які ланцюжаться. Ядро — розплата за жадібність: великий кубик зараз = менше кидків і щедра таця суперникам.

## Поле і час
- **Аркуш гравця** (особистий): 5 областей — жовта (сітка чисел 4×4 з діагоналлю (?)), синя (сітка сум), зелена, помаранчева, фіолетова (рядки-доріжки зліва направо); плюс трек раундів і дві смуги дій (reroll, +1).
- **Спільне**: 6 кубиків (білий, жовтий, синій, зелений, помаранчевий, фіолетовий); 3 клітинки для обраних кубиків; срібна таця.
- Раунди: 4 гравці — 4, 3 гравці — 5, 1–2 гравці — 6; у кожному раунді кожен гравець раз активний.
- Хід активного = до 3 кидків + фаза пасивних (одночасно).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Кубик кольору | object | колір, значення 1–6 | записується в область свого кольору |
| Білий кубик | object | джокер | у жовту/зелену/помаранчеву/фіолетову як будь-який колір; у синій — у сумі з синім |
| Клітинка для кубика | supply | 3 | обраний кубик ставиться сюди, не кидається далі |
| Срібна таця | supply | — | менші за обраний кубики; пасивні беруть звідси (кілька гравців — той самий кубик) |
| Жовта область | zone | числа, кожне двічі | закреслити число, будь-який порядок; повний стовпець → обведене число-очки |
| Синя область | zone | суми синій + білий | закреслити суму; очки за кількість хрестиків за шкалою (4 → 7, 9 → 37) |
| Зелена область | zone | доріжка з порогами ≥ N | зліва направо без пропусків; значення ≥ порогу клітинки; очки — за останньою клітинкою |
| Помаранчева область | zone | доріжка, клітинки ×2, ×3 | зліва направо, будь-яке значення (з множником); очки — сума |
| Фіолетова область | zone | доріжка | зліва направо; кожне > попереднього, крім після 6; очки — сума |
| Бонус клітинки | pickup | хрестик кольору / число / дія / лис | спрацьовує одразу при заповненні; може запустити інший бонус |
| Дія reroll | resource | смуга на аркуші | лише активний: перекинути всі кубики не на таці й не в клітинках |
| Дія «+1 кубик» | resource | смуга на аркуші | у кінці будь-чийого ходу: взяти будь-який з 6 кубиків, навіть використаний |
| Лис | mark | — | наприкінці = найменший рахунок серед 5 областей |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `phase_start(round)` → ЯКЩО `level(<=, 4)` → ТО `custom: «бонус раунду з треку; у 4-му — вибір з двох»`.
- Кидок: КОЛИ `turn_start(active)` → ТО `custom: «кинути всі кубики, що не на таці і не в клітинках»`.
- Вибір: КОЛИ `input(choose(die))` → ТО `move(die, slot)`, `custom: «записати значення в область кольору кубика»`; кожен кубик = рівно один запис.
- КОЛИ `after(choose)` → ТО `custom: «кожен кубик зі значенням < обраного — на срібну тацю»`.
- КОЛИ `custom: «3 кубики обрано або нема чого кидати»` → ТО `custom: «решта кубиків — на тацю»`; фаза пасивних.
- Пасивні: КОЛИ `custom: «фаза пасивних»` → ТО `choose(tray_die)` кожен одночасно; ЯКЩО `not custom: «на таці є придатний кубик»` → ТО можна взяти кубик з клітинок активного.
- Жовта: КОЛИ `input(record(yellow, v))` → ЯКЩО `custom: «невикреслене v є в жовтій»` → ТО `mark(cell, X)`.
- Синя: КОЛИ `input(record(blue|white))` → ТО `custom: «записується лише сума синього + білого»` → `mark(cell_with_sum, X)`.
- Зелена: КОЛИ `input(record(green, v))` → ЯКЩО `custom: «v ≥ порогу наступної клітинки»` → ТО `mark(next_cell, X)`; інакше `block`.
- Помаранчева: КОЛИ `input(record(orange, v))` → ТО `mark(next_cell, v × множник клітинки)`.
- Фіолетова: КОЛИ `input(record(purple, v))` → ЯКЩО `first_time` or `custom: «v > попереднього або попереднє = 6»` → ТО `mark(next_cell, v)`; інакше `block`.
- Бонуси: КОЛИ `custom: «заповнено клітинку з бонусом / повний ряд чи стовпець»` → ТО одразу `custom: «хрестик у вказаній області / число / дія / лис»`; КОЛИ `after(bonus)` → ЯКЩО `custom: «бонус заповнив клітинку з бонусом»` → ТО `trigger(bonus)` — ланцюг.
- Reroll: КОЛИ `input(reroll)` → ЯКЩО `turn_of(player)` and `has(player, reroll_action)` → ТО `custom: «перекинути всі доступні кубики»` (не частину).
- +1: КОЛИ `turn_end(active)` → ЯКЩО `has(player, plus_one_action)` → ТО `choose(any_die)`; кожен кубик — раз за хід, але можна кілька дій.
- КОЛИ `custom: «останній хід останнього раунду + пасивні»` → ТО можна використати +1, решта дій згорає; `game_over`.
- Рахунок: жовта — сума обведених · синя — за шкалою кількості · зелена — число над останньою клітинкою · помаранчева і фіолетова — суми · кожен лис `score(+min(областей))`; будь-яка область 0 → лиси = 0.
- Тай-брейк: найкраща окрема область → спільна перемога.

## Керування і ввід
- Активний: «кинути» → клік по кубику → клік по клітинці області (підсвічені легальні) → бонуси застосовуються по черзі з вибором цілі.
- Кнопки reroll і «+1» з лічильником доступних дій.
- Пасивні: одночасний вибір кубика з таці (у цифровій версії — кожен на своєму пристрої або по черзі).

## Вікна, меню, HUD
(цифрова версія)
- `match-setup`: 1–4 гравці, AI, соло.
- `game-screen`: `dice-pool` (6 кубиків), 3 клітинки обраних, `silver-tray`; `score-sheet` гравця з 5 областями і `legal-move-highlight`; смуги дій; трек раундів; `opponent-boards` (мініатюри аркушів); `turn-indicator`; `popup-text` для ланцюгів бонусів.
- `end-screen`: розклад очок за областями, лиси.
- `help-window`: правила кожної області й бонусів.

## Фічі поза полем
- Соло-режим (?) — правила на окремій сторінці, не читав.
- `hotseat`, одночасна фаза пасивних — `simultaneous-versus`.
- `score-records` — рекорд аркуша.

## Варіації й родичі
- Сиквели (BGG-родина «Ganz Schön Clever»): Doppelt so clever, Clever hoch drei (Clever Cubed), Clever 4ever (?) — інші області, та сама основа «менші — на тацю».
- Сусіди по теці: `welcome-to` (flip-and-write), `railroad-ink` (roll-and-write на сітці), `sagrada` (кубики як фігури).
- **Осі варіацій**: доступ пасивних (нема / таця менших / будь-який) · правило області (будь-який порядок / зростання / поріг / множник / сума двох) · бонуси (нема / одиночні / ланцюгові).

## Цікавинки для курсу
- «Менші за обраний — на тацю»: компроміс жадібності в 3 рядки коду — 🌱.
- 5 областей = 5 валідаторів запису (порядок, поріг, зростання з reset після 6, множник, сума двох кубиків) — 📎 разом.
- Ланцюг бонусів: заповнення клітинки → подія → інша клітинка → … (черга подій, захист від циклу) — 🥉.
- Лис = мінімум областей: штовхає до балансу — 🌱.
- Одночасний вибір пасивних з однієї таці (кубик не зникає) — 🌱.
- AI-оцінка «який кубик узяти» з урахуванням таці й ланцюгів — 🥇.

## Мапа на каталог
- Є: `cell-click` · `legal-move-highlight` · `selection-highlight` · `turn-enforcement` · `hot-seat` · `simultaneous-versus` (пасивні) · `event-points` · `chain-reaction` (ланцюг бонусів) · `completion-detection` (повні ряди/стовпці) · `score-records` · стандартні вікна.
- **Нема** → пропозиції карток:
  - `+sub-lower-dice-tray` «Кубики менші за обраний відходять іншим» · game-logic/opponent · 🌱.
  - `+passive-player-pick` «Пасивні гравці теж ходять з залишку активного» · game-logic/opponent · 🌱.
  - `+bonus-chain-cascade` «Бонус клітинки заповнює іншу клітинку з бонусом» · game-logic/score · 🥉.
  - `+wild-die` «Кубик-джокер для будь-якого кольору» · entities/state · 🌱.
  - `+multi-area-sheet` «Аркуш з кількома областями з різними правилами» · entities/legality · 📎.
  - `+threshold-track` «Доріжка з порогами ≥ N» · entities/legality · 🌱 · `+multiplier-cells` · `+sum-of-two-dice` · `+action-tokens-reroll` · `+extra-die-action` · `+round-start-bonus` · `+row-column-bonus`.
  - `+dice-roll-pool` · `+roll-and-write` · `+ascending-sequence-rule` · `+min-color-score` · `+escalating-track-score` · `+tiebreak-chain` — як у сусідах по теці.

## Пропозиції до словників
- `+effect:roll` — кинути кубики (Sagrada; тут — лише «не на таці»).
- `+effect:cross_box` — закреслити клітинку аркуша (Welcome To).
- `+effect:to_tray` — перемістити кубик у спільний запас для інших.
- `+cond:value_at_least` — значення ≥ порогу клітинки.
- `+cond:ascending` — значення більше попереднього в доріжці (тут з reset після 6).
- `+trigger:box_filled` — заповнено клітинку з бонусом (запуск ланцюга).
- `+role:die` · `+role:sheet-area` — область аркуша зі своїм правилом запису.
- `+ui:dice-pool` · `+ui:silver-tray` · `+ui:score-sheet`.

## Джерела
- ⭐ [UltraBoardGames: That's Pretty Clever rules](https://www.ultraboardgames.com/thats-pretty-clever/game-rules.php) — компоненти, раунди за кількістю гравців, послідовність кидків, таця, пасивні, правила 5 областей, бонуси, дії, рахунок, тай-брейк.
- BGG: пошук «Ganz Schon Clever»; Steam: пошук; YouTube: пошук «how to play».

## Непевне
- (?) Точна геометрія жовтої (4×4 з діагоналлю) і синьої областей, кількість клітинок у доріжках, повна шкала синьої — з памʼяті / лише два приклади у джерелі.
- (?) Соло-правила — на окремій сторінці, не відкривав.
- (?) Офіційний застосунок (мобільний) — памʼятаю, що існує, не перевірено; вікна — гіпотетичні.
- (?) Clever 4ever як четверта гра серії — з памʼяті.
- (?) Сторінка UltraBoardGames за посиланням ganz-schon-clever віддала чужий зміст; правила взято зі сторінки thats-pretty-clever. Wikipedia-статті нема (404).
