---
title: Air, Land & Sea
slug: air-land-and-sea
aka: [Air Land and Sea]
family: tower-lanes
also: [board-digital]
klass: cursor
axes:
  field: 1d
  time: turn
  opponent: hotseat
  info: hidden
  random: both
  goal: score
year: 2019
platforms: [board]
links:
  - {kind: other, url: "https://rulespal.com/air-land-and-sea/rulebook", best: true, note: "правила текстом: дії Deploy/Improvise/Withdraw, накриті карти, Instant/Ongoing, контроль театру, бої до 12 ПО, 9 карт з текстом"}
  - {kind: official, url: "https://www.arcanewonders.com/game/air-land-sea/", note: "сторінка видавця Arcane Wonders: суть гри, лінк на рулбук"}
  - {kind: other, url: "https://www.arcanewonders.com/wp-content/uploads/2021/05/Air_Land_and_Sea_Rulebook_2026.pdf", note: "офіційний рулбук (видання 2026, сторінки-картинки): компоненти, таблиці відступу обох командувачів, ротація театрів, ключові терміни"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Air+Land+and+Sea+how+to+play", note: "пошук; як грати"}
stage: v1
coverage: 70
mechanics: [hot-seat, turn-enforcement, pocket, pass-device, event-points, end-screen, help-window, match-setup, +lane-grid, +row-power-sum, +majority-of-lanes, +hidden-hand-cards, +retreat-concede, +second-player-compensation, +multi-round-match, +splash-adjacent-lanes, +face-down-wild-play, +flip-any-card, +covered-card-stack, +instant-vs-ongoing, +first-player-wins-ties, +withdraw-value-chart, +lane-rotation, +fixed-hand-no-draw]
proposes: ["+role:card", "+role:lane", "+effect:flip", "+effect:withdraw", "+effect:destroy_card", "+trigger:card_played", "+trigger:battle_start", "+cond:face_up", "+cond:uncovered", "+cond:matching_theater", "+ui:flipped-card", "+ui:withdraw-chart", "+ui:row-power", "+window:round-summary", "+card:withdraw-value-chart", "+card:instant-vs-ongoing"]
author: opus
date: 2026-11-09
---

# Air, Land & Sea — три театри-стовпці: відкрита карта — лише у свій театр і зі здібністю, закрита — будь-куди з силою 2, а вчасний відступ віддає супернику менше очок

## Суть
Карткова дуель Джона Перрі (Arcane Wonders, 2019) на 18 карт. Між гравцями лежать три театри — Повітря, Земля, Море; за бій кожен має 6 карт і не добирає. Хід — одна дія: **Deploy** (карта відкрито у свій театр, спрацьовує здібність), **Improvise** (закрито в будь-який театр, сила 2, без здібності) або **Withdraw** (відступ: бій програно, але суперник отримує тим менше очок, чим раніше відступив). Хто контролює більше театрів після останньої карти — виграє бій і 6 ПО; партія — до 12 ПО.

## Поле і час
- Поле — 3 театри в ряд (`field: 1d`): кожен театр — стовпець між гравцями, у кожного своя сторона. Суміжні — лише сусідні в ряду: крайні театри не суміжні.
- На своїй стороні театру карти лягають внахлест: нова **накриває** попередні (видно лише верх). Накрита карта рахує силу, але багато здібностей діють тільки на ненакриті.
- Порядок театрів випадковий на старті; після кожного бою ротація: Повітря → місце Землі, Земля → місце Моря, Море → місце Повітря.
- Покроково: ходи по черзі, починає 1-й гравець; бій закінчується відступом або коли обидва зіграли всі карти. Партія — серія боїв до 12 ПО (довга — 18).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Театр ×3 (Air, Land, Sea) | zone (`+role:lane`) | тип, позиція в ряду | контролює той, у кого більша сума сили на своєму боці |
| Карта бою | piece (`+role:card`) | тип театру, сила 1–6, здібність Instant ⚡ або Ongoing ∞ | 6 карт на тип; сила і здібність лише відкритою |
| Закрита карта | piece | сила 2 | «дика»: будь-який театр; здібності нема |
| Командувач 1st Player | static | червоний; виграє нічиї | таблиця відступу: у руці 4+ → 2 ПО, 2–3 → 3, 1 → 4, 0 → 6 |
| Командувач 2nd Player | static | синій; програє нічиї | таблиця відступу: 5+ → 2, 3–4 → 3, 2 → 4, 0–1 → 6 |
| Жетони ПО | mark | 6 / 3 / 1 | рахунок партії |
| Рука | supply | 6 карт на бій | добору нема, якщо здібність не каже |
| Колода | supply | решта 6 карт, закрита | ціль Reinforce і знищених карт (під низ) |
| Support (Air 1) ∞ | piece | — | (?) +3 сили в кожному суміжному театрі |
| Air Drop (Air 2) ⚡ | piece | — | наступного ходу можна зіграти карту в невідповідний театр |
| Maneuver (Air/Land/Sea 3) ⚡ | piece | — | перевернути ненакриту карту в суміжному театрі |
| Aerodrome (Air 4) ∞ | piece | — | (?) карти сили ≤ 3 можна грати відкрито в будь-який театр |
| Containment (Air 5) ∞ | piece | — | будь-яку карту, зіграну закрито (будь-ким), знищити |
| Heavy Bombers · Heavy Tanks · Super Battleship (6) | piece | — | без здібності, найбільша сила |
| Reinforce (Land 1) ⚡ | piece | — | подивитися верхню карту колоди; можна зіграти її закрито в суміжний театр |
| Ambush (Land 2) ⚡ | piece | — | (?) перевернути карту |
| Cover Fire (Land 4) ∞ | piece | — | усі карти, накриті нею, мають силу 4 |
| Disrupt (Land 5) ⚡ | piece | — | суперник перевертає 1 свою карту, потім ти — 1 свою |
| Transport (Sea 1) ⚡ | piece | — | можна перемістити 1 свою карту в інший театр |
| Escalation (Sea 2) ∞ | piece | — | усі твої закриті карти мають силу 4 |
| Redeploy (Sea 4) ⚡ | piece | — | повернути 1 свою закриту карту в руку; якщо так — зіграти карту |
| Blockade (Sea 5) ∞ | piece | — | карту, зіграну в суміжний театр, де вже ≥ 3 карт (обох гравців), знищити |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `custom: «battle_start»` → ТО `custom: «перемішати 18 карт»`, `give(each, 6 cards)`, `custom: «решта — закрита колода»`; 1-й гравець — власник червоного командувача.
- КОЛИ `input(deploy, card, theater)` → ЯКЩО `turn_of(side)` and `custom: «matching_theater: тип карти = тип театру»` → ТО `place(player, card)` відкрито поверх своїх карт, `custom: «спрацьовує здібність»`, `end_turn`; інакше `block`.
- КОЛИ `input(improvise, card, theater)` → ЯКЩО `turn_of(side)` → ТО `place(player, card)` закрито, `set_value(card, 2)`, `end_turn`.
- КОЛИ `input(withdraw)` → ТО `custom: «бій виграє суперник»`, `score(opponent, chart(cards_left))` за таблицею командувача **того, хто відступив**.
- КОЛИ `custom: «карту зіграно відкритою або перевернуто відкритою»` → ЯКЩО `custom: «здібність Instant»` → ТО `custom: «виконати одразу й повністю, навіть якщо карту перевернуть посеред»`; кілька Instant — у порядку виникнення.
- КОЛИ `custom: «здібність Ongoing»` → ЯКЩО `custom: «face_up: карта відкрита»` → ТО ефект діє; закрита → ефект зникає.
- КОЛИ `custom: «здібність без слова may»` → ЯКЩО `custom: «виконати неможливо»` → ТО `custom: «ігнорується»`; інакше — обовʼязково.
- КОЛИ `custom: «flip(card)»` → ТО `custom: «відкрита ↔ закрита»` — будь-яку карту, свою чи чужу, якщо не сказано інше.
- КОЛИ `custom: «move(card)»` → ТО `move(card, other_theater)` — лишається на боці власника, кладеться поверх; переміщення — не «розіграш» (Blockade/Containment не діють).
- КОЛИ `custom: «destroy(card)»` → ТО `custom: «карта закрито під низ колоди»`; знищена одразу після розіграшу здібності не виконує.
- КОЛИ `custom: «зіграно Maneuver»` → ТО `custom: «flip ненакритої карти в суміжному театрі»`.
- КОЛИ `custom: «зіграно закриту карту»` → ЯКЩО `custom: «відкритий Containment у грі»` → ТО `custom: «destroy цієї карти»`.
- КОЛИ `custom: «зіграно карту в театр, суміжний з відкритим Blockade»` → ЯКЩО `count(cards_in_theater, >=, 3)` → ТО `custom: «destroy цієї карти»`.
- КОЛИ `custom: «зіграно Redeploy»` → ЯКЩО `custom: «є своя закрита карта»` → ТО `custom: «повернути її в руку»`, `extra_move`.
- КОЛИ `custom: «зіграно Disrupt»` → ТО `custom: «суперник перевертає 1 свою карту, потім ти — 1 свою»`.
- КОЛИ `custom: «зіграно Reinforce»` → ТО `custom: «переглянути верх колоди»`, `custom: «можна зіграти її закрито в суміжний театр»`.
- КОЛИ `custom: «battle_end: обидва зіграли всі карти»` → ТО `custom: «для кожного театру: більша сума сили → контроль; рівність або порожньо → 1-й гравець»`.
- КОЛИ `custom: «контроль підраховано»` → ТО `custom: «більше театрів — перемога в бою»`, `score(winner, 6)`.
- КОЛИ `counter(vp, >=, 12)` → ТО `win`.
- КОЛИ `custom: «наступний бій»` → ТО `rotate(theaters, 1)` (Air → Land → Sea → Air), `swap(commander_cards)`, `custom: «нова роздача по 6»`.
- Перемога: першим 12 ПО (довга партія — 18) · Поразка: суперник першим · Рахунок: 6 ПО за повний бій або за таблицею відступу 2–6. Режим новачка: бій = 1 ПО, гра до 3, таблиці ігноруються.

## Керування і ввід
- Хід: обрати карту з руки → обрати дію (відкрито у свій театр / закрито будь-куди) або оголосити відступ.
- Здібності інколи вимагають вибору цілі: яку карту перевернути, яку перемістити, куди зіграти верх колоди.
- Свої закриті карти можна переглядати будь-коли, чужі — ні.

## Вікна, меню, HUD
- `game-screen` (цифрова версія): 3 театри в ряд з картами внахлест з обох боків, суми сили на кожному боці (`+ui:row-power` у корпусі), `pocket` (рука), `+ui:flipped-card` (закриті карти із силою 2), `+ui:withdraw-chart` (скільки ПО віддаси, якщо відступиш зараз), кнопка Withdraw, `turn-indicator`.
- `match-setup` (цифрова версія): мета 12 / 18 ПО, режим новачка.
- `pass-device` (цифрова версія) — закриті руки в hot-seat.
- `+window:round-summary` — контроль театрів, ПО за бій; `end-screen` — переможець партії; `help-window` — довідка з текстами всіх 18 карт.

## Фічі поза полем
- Серія боїв з ротацією театрів і обміном ролей 1-й/2-й гравець; довжина партії налаштовується (12 / 18 ПО).
- Режим новачка — спрощений рахунок для вивчення здібностей.

## Варіації й родичі
- Сиквел-окрема гра: Air, Land & Sea: Spies, Lies & Supply Lines (?).
- Родичі в корпусі: [schotten-totten](schotten-totten.md) (смуги-«камені», більшість), [hanamikoji](hanamikoji.md), [riftforce](riftforce.md) (локації в ряд, суміжність), [marvel-snap](marvel-snap.md) (3 локації, відступ з меншою втратою), [gwent](gwent.md) і [queens-blood](queens-blood.md) (сума сили ряду).
- **Осі варіацій**: хто забирає смугу — більша сума / покерна комбінація / присутність · нічия — 1-му гравцю / нікому · відступ — нема / фіксований штраф / таблиця від кількості карт у руці · закрита карта — блеф без сили / «дика» з силою 2.

## Цікавинки для курсу
- Дві форми карти: відкрита (свій театр + здібність) і закрита (будь-куди, сила 2) — 🌱.
- Instant проти Ongoing: одноразова дія проти стану, що зникає, коли карту перевернули, і перерахунок сил — 📎.
- Стек карт внахлест: «накрита/ненакрита» як ціль, Cover Fire змінює силу лише накритих — 📎.
- Таблиця відступу від кількості карт у руці й асиметрія 1-го/2-го гравця — 🌱, але цікава задача AI: коли відступати (очікувана вартість) — 🥈.
- Ротація театрів між боями й обмін ролей — 🌱.

## Мапа на каталог
- Є: `hot-seat`, `turn-enforcement`, `pocket` ↔ рука · `pass-device` · `event-points` ↔ ПО · `match-setup` ↔ 12/18, новачок · `end-screen`, `help-window`.
- **Нема** → пропозиції карток:
  - `+lane-grid`, `+row-power-sum`, `+majority-of-lanes`, `+hidden-hand-cards`, `+retreat-concede`, `+second-player-compensation`, `+multi-round-match`, `+splash-adjacent-lanes` — уже в корпусі.
  - `+face-down-wild-play` «Закрита карта — будь-куди з фіксованою силою» · entities/legality · 🌱.
  - `+flip-any-card` «Перевернути карту на полі: вмикає/вимикає здібність» · entities/state · 📎.
  - `+covered-card-stack` «Карти внахлест: ціль — накрита / ненакрита» · entities/state · 📎.
  - `+instant-vs-ongoing` «Одноразові й постійні здібності» · entities/state · 📎.
  - `+first-player-wins-ties` «Нічия на смузі — 1-му гравцю» · game-logic/score · 🌱.
  - `+withdraw-value-chart` «Відступ коштує ПО за таблицею від залишку руки» · game-logic/lose · 🌱.
  - `+lane-rotation` «Смуги міняються місцями між раундами» · game-logic/waves · 🌱.
  - `+fixed-hand-no-draw` «Рука на весь раунд без добору» · game-logic/constraints · 🌱.

## Пропозиції до словників
- `+role:card`, `+role:lane`, `+effect:flip`, `+effect:withdraw`, `+trigger:card_played` — повтори з корпусу.
- `+effect:destroy_card` — карта йде закрито під низ колоди (не `disappear`: повертається в гру наступного бою).
- `+trigger:battle_start` — повтор.
- `+cond:face_up` — карта відкрита; `+cond:uncovered` — карта не накрита іншою; `+cond:matching_theater` — тип карти збігається з типом театру.
- `+ui:flipped-card`, `+ui:row-power` — повтори; `+ui:withdraw-chart` — таблиця ціни відступу.
- `+window:round-summary` — повтор.
- `+card:withdraw-value-chart`, `+card:instant-vs-ongoing`.

## Джерела
- ⭐ [RulesPal: Air, Land & Sea rulebook](https://rulespal.com/air-land-and-sea/rulebook) — повні правила текстом, режим новачка, ротація, тексти 9 карт (Reinforce, Transport, Air Drop, Escalation, Cover Fire, Redeploy, Blockade, Disrupt, Containment).
- [Arcane Wonders: сторінка гри](https://www.arcanewonders.com/game/air-land-sea/) — суть, 6 карт на бій, 12 ПО, лінк на рулбук.
- [Офіційний рулбук 2026 (PDF)](https://www.arcanewonders.com/wp-content/uploads/2021/05/Air_Land_and_Sea_Rulebook_2026.pdf) — компоненти (6 карт на театр, 2 командувачі, жетони 6/3/1), обидві таблиці відступу, «1st Player wins tied theaters», суміжність, ключові терміни Flip/Move/Destroy/Occupied, ротація, автор Jon Perry; тексти Transport, Escalation, Redeploy, Containment, Maneuver на ілюстраціях.
- YouTube: пошук «Air Land and Sea how to play».

## Непевне
- (?) Тексти Support, Ambush, Aerodrome — назви й сила видно на ілюстраціях рулбука, текст не прочитано; подані з памʼяті.
- (?) Redeploy: у рулбуку 2026 — «поверни закриту карту в руку; якщо так — зіграй карту», RulesPal — «отримай додатковий хід»; ефект той самий, формулювання різне.
- (?) Blockade і Containment: RulesPal — «скинути», рулбук 2026 — «знищити» (під низ колоди).
- (?) Maneuver у всіх трьох театрах — по одній «3» видно в кожному кольорі, текст прочитано лише для Air/Sea.
- (?) Сиквел Spies, Lies & Supply Lines і цифрові версії — не перевірено.
