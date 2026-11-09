---
title: Triple Triad
slug: triple-triad
aka: [トリプルトライアド, TT]
family: board-digital
also: [chess-abstract]
klass: cursor
axes:
  field: square
  time: turn
  opponent: ai
  info: hidden
  random: setup
  goal: territory
year: 1999
platforms: [PlayStation, PC, PC/PS (FF XIV), mobile, board]
links:
  - {kind: official, url: "https://na.finalfantasyxiv.com/lodestone/playguide/contentsguide/goldsaucer/tripletriad/", best: true, note: "FF XIV: 3×3, 5 карт, базове захоплення, 15 правил матчу, таймер 90 с, обмеження колоди за зірками, нагороди"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Triple_Triad", note: "історія, елементи клітин, версії: FF VIII, фізичний набір Bandai, FF XIV, Final Fantasy Portal App"}
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/ファイナルファンタジーVIII", note: "розділ 2.10 Triple Triad: ранги 1–10 (A), Same, Plus, Wall Same, Elemental, правила обміну One/Diff/Direct/Full/Null"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Triple+Triad+rules", note: "пошук; пояснення правил"}
stage: v1
coverage: 70
mechanics: [cursor-place, cell-click, pocket, ai-opponent, online-multiplayer, move-timer, rule-variants, chain-reaction, match-setup, game-screen, end-screen, +edge-rank-capture, +same-plus-capture, +wall-as-rank, +combo-capture-chain, +majority-win, +elemental-field-bonus, +hidden-hand-cards, +card-collection, +win-card-reward, +trade-rule-stakes, +regional-rules, +reverse-compare, +type-count-modifier, +sudden-death-replay, +deck-rarity-limit, +forced-card-order]
proposes: ["+cond:greater", "+cond:pair_sum", "+trigger:board_full", "+ui:card-hand", "+ui:score-tally", "+window:deck-builder", "+window:rules-banner", "+feature:card-collection", "+feature:regional-rules", "+card:edge-rank-capture", "+card:same-plus-capture", "+card:trade-rule-stakes"]
author: opus
date: 2026-11-09
---

# Triple Triad — карти з чотирма числами-ребрами на полі 3×3 перефарбовують слабших сусідів

## Суть
Картярка всередині Final Fantasy VIII (1999), пізніше окрема гра у FF XIV і мобільному Final Fantasy Portal App. Двоє по черзі кладуть карти з руки (5 карт) на поле 3×3; кожна карта має чотири ранги — по одному на ребро. Покладена карта порівнює свої ребра з дотичними ребрами сусідніх карт суперника й захоплює (перефарбовує) ті, де її число більше. Наприкінці виграє той, хто контролює більше карт; переможець забирає карту(и) суперника — колекція росте від партій.

## Поле і час
- Поле — 3×3, 9 клітин; сусідство ортогональне: карта має до 4 сусідів, кутова — 2, центральна — 4.
- Шари: клітина (у FF VIII може мати елемент) + карта з власником (колір рамки).
- Хід = покласти одну карту на вільну клітину; карти на полі не рухаються, змінюється лише власник. Перший гравець — випадково (FF XIV).
- Партія — рівно 9 ходів: перший кладе 5 карт, другий — 4, а його 10-та карта лишається в руці й теж іде в рахунок (FF XIV).
- Інформація: руки закриті, якщо не діє Open; поле відкрите. FF XIV: 90 с на матч на гравця, кожен хід починається з 5 с «на роздуми», коли годинник стоїть.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Карта | piece | 4 ранги (верх, право, низ, ліво) 1–A, A = 10; власник; елемент (FF VIII) або тип (FF XIV) | кладеться з руки на вільну клітину; бʼє дотичні ребра сусідів; захоплена — міняє колір, може бути відвойована |
| Клітина поля | terrain | 9 клітин | вільна / зайнята |
| Елементна клітина | terrain | елемент (вогонь, лід, …) | під Elemental: карта того ж елементу +1 до всіх рангів, іншого або без елементу −1 |
| Край поля | static | ранг A під Same Wall | бере участь у Same як «сусід» з A |
| Рука | supply | 5 карт | джерело ходів; під Open — відкрита; невикладена карта рахується |
| Колекція / колода | supply | FF XIV: 5 слотів колод по 5 карт | з неї збирають руку; поповнюється виграними картами |
| Рідкість карти | — | 1–5 зірок (FF XIV) | ★5 — максимум 1 у колоді; ★4 — до 2, або 1, якщо є ★5 |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `game_start` → ТО `custom: «першого гравця обирає випадок»`; ЯКЩО `mode(random)` → ТО `custom: «рука = 5 випадкових карт з колекції»`.
- КОЛИ `input(place(card, cell))` → ЯКЩО `turn_of(player)` і `free(cell)` → ТО `place(player, card)`, `end_turn`; інакше `block`.
- Базове захоплення: КОЛИ `input(place(card, cell))` → ЯКЩО `occupied(neighbor, enemy_card)` і `custom: «ранг нової карти на ребрі до сусіда більший за ранг сусіда на дотичному ребрі»` (`+cond:greater`) → ТО `set_side(neighbor, player)` — для кожного з ≤4 сусідів окремо.
- Elemental: КОЛИ `input(place(card, cell))` → ЯКЩО `mode(elemental)` і `cell(cell, element)` і `same(card, cell, element)` → ТО `custom: «+1 до всіх 4 рангів на час порівнянь»`; ЯКЩО `not same(card, cell, element)` → ТО `custom: «−1 до всіх рангів»`.
- Same: КОЛИ `input(place(card, cell))` → ЯКЩО `mode(same)` і `same(card_edge, neighbor_edge, rank)` для ≥2 сусідів → ТО `set_side(enemy_neighbors_of_these_pairs, player)`; елементні +1/−1 тут не діють.
- Same Wall: ЯКЩО `mode(same)` і `mode(same_wall)` → ТО `custom: «край поля поруч з ребром = сусід з рангом A, рахується в пари Same»`; без Same — ігнорується.
- Plus: КОЛИ `input(place(card, cell))` → ЯКЩО `mode(plus)` і `custom: «≥2 сусіди дають однакову суму "ребро нової + дотичне ребро сусіда"»` (`+cond:pair_sum`) → ТО `set_side(enemy_neighbors_of_these_pairs, player)`.
- Combo: КОЛИ `after(set_side)` (захоплення через Same/Plus) → ТО `trigger(basic_capture)` від імені захопленої карти — вона бʼє своїх слабших сусідів, ланцюг триває, доки є нові захоплення.
- Reverse (FF XIV): ЯКЩО `mode(reverse)` → ТО `custom: «у базовому захопленні менший ранг бʼє більший»`.
- Fallen Ace (FF XIV): ЯКЩО `mode(fallen_ace)` → ТО `custom: «1 бʼє A»`; разом з Reverse — `custom: «A бʼє 1»`.
- Ascension (FF XIV): КОЛИ `input(place(card, cell))` → ЯКЩО `mode(ascension)` і `custom: «у карти є тип»` → ТО `custom: «ранги всіх карт цього типу +1 за кожну карту типу на полі; ≥11 = A»`; Descension — −1, ≤0 = 1.
- All Open: КОЛИ `game_start` → ЯКЩО `mode(all_open)` → ТО `reveal(hands)`; Three Open — `reveal(3 random cards of each hand)`.
- Order: КОЛИ `turn_start(player)` → ЯКЩО `mode(order)` → ТО `custom: «грати лише наступну карту в порядку колоди»`; Chaos — `custom: «карту на хід обирає випадок»`.
- Swap: КОЛИ `game_start` → ЯКЩО `mode(swap)` → ТО `swap(random_card_mine, random_card_theirs)`; після матчу карти повертаються.
- Таймер (FF XIV): КОЛИ `custom: «годинник гравця вичерпано»` → ТО `custom: «карту кладе автомат; далі — лише в межах 5 с на хід»`.
- Кінець: КОЛИ `custom: «на полі 9 карт»` (`+trigger:board_full`) → ТО `custom: «рахунок = карти свого кольору на полі + карта в руці»`; більше — `win`, рівно — `draw`.
- Sudden Death: КОЛИ `custom: «партія закінчилась нічиєю»` → ЯКЩО `mode(sudden_death)` → ТО `restart` з картами, якими кожен володів наприкінці; FF XIV — після ще 5 нічиїх поспіль `draw` остаточно.
- Обмін (FF VIII): КОЛИ `game_over` → ЯКЩО `mode(one)` → ТО `choose(одна карта переможеного)`, `give(winner, card)`.
- КОЛИ `game_over` → ЯКЩО `mode(diff)` → ТО `custom: «переможець бере стільки карт, яка різниця рахунку»`; `mode(direct)` → `custom: «кожен забирає карти свого кольору на полі — навіть переможець може втратити свої»`; `mode(full)` → `custom: «переможець бере всі 5 карт руки суперника»`; `mode(null)` → нічого.
- Перемога: більше карт свого кольору (поле + рука) · Поразка: менше · Рахунок: 5:5 — нічия; ставка — за правилом обміну.

## Керування і ввід
- FF VIII (PS): вибір карти в руці стрілками, потім клітини, підтвердження; виклик NPC на гру — діалог «зіграти в карти?» (?).
- FF XIV: миша/геймпад — клік по карті руки, клік по клітині; годинник матчу внизу (?).
- Перед матчем: вибір колоди (FF XIV) або 5 карт з колекції (FF VIII); під Random рука збирається сама.

## Вікна, меню, HUD
- `match-setup` (`+window:rules-banner`): перелік правил регіону/матчу (до 2 правил у FF XIV, Roulette — випадкові) і правило обміну.
- `custom-window` вибору руки (`+window:deck-builder`): колекція карт сторінками, рідкість, ліміт зірок (FF XIV — 5 колод по 5 карт).
- `game-screen`: поле 3×3 у центрі, руки двох гравців з боків (`+ui:card-hand`, `pocket`), колір рамки = власник, `popup-text` «Same!» / «Plus!» / «Combo» (?), рахунок кожної сторони (`+ui:score-tally`), `turn-indicator`, `player-clock` (FF XIV), іконки елементів на клітинах (FF VIII).
- `end-screen`: перемога / поразка / нічия; далі вибір карти суперника за правилом One (FF VIII) або нагорода MGP і карта (FF XIV).
- `codex-window`-подібне меню колекції карт (Card у меню FF VIII, Triple Triad Card list у FF XIV) (?).
- Переходи: діалог NPC → match-setup → вибір руки → game-screen → end-screen → обмін → назад у світ.

## Фічі поза полем
- `custom-rules` / регіональні правила: кожен регіон FF VIII має свою комбінацію правил, правила поширюються між регіонами разом з гравцем; Card Queen за плату додає правила. FF XIV — регіональні правила оновлюються щодня, до 2 одночасно.
- `card-collection` (`+feature:card-collection`): виграні карти; FF VIII — Card Mod (G.F. Quezacotl) переробляє непотрібні карти на предмети, рідкісні — на рідкісні.
- `ai-opponent-levels`: NPC з різними колодами; FF XIV — турніри (open/invitational), PvP з денним бонусом за 5 перемог.
- `turn-timer` (FF XIV), `custom-rules` для турнірів, Draft (колода з випадкової пропозиції).
- Фізична версія Bandai (1999): 110 карт Triple Triad, 72 художні, ігровий килимок; фан-версії Triple Triad PSP (2007), Triple Triad Advance (браузер); Final Fantasy Portal App (2015) — freemium з енергією, закрито в листопаді 2024.

## Варіації й родичі
- Tetra Master (FF IX) — наступник того ж автора (Хіроюкі Іто): інша сітка і стрілки замість ребер (?); у корпусі нема.
- Queen's Blood (`tower-lanes/queens-blood.md`) — пізніша картярка серії на смугах; Eye of Judgment (`tower-lanes/eye-of-judgment.md`) — 3×3 з елементами клітин і сторонами карти.
- Reversi (`chess-abstract/reversi.md`) і Ataxx (`chess-abstract/ataxx.md`) — та сама ідея «перефарбувати сусіда», але без чисел.
- **Осі варіацій**: порівняння (більше / менше — Reverse / 1 бʼє A) · комбо (нема / Same / Plus / Same Wall / Combo-ланцюг) · видимість (закрито / Three Open / All Open) · вибір руки (своя / Random / Order / Chaos / Draft / Swap) · модифікатор клітини (нема / елемент / тип у полі) · ставка (One / Diff / Direct / Full / Null).

## Цікавинки для курсу
- Базове захоплення: 4 порівняння ребер з урахуванням сторони — 🌱 (ідеальне перше завдання про сусідство).
- Same / Plus / Same Wall: пошук пар серед ≤4 сусідів (рівні ранги або рівні суми) + край як A — 📎.
- Combo-ланцюг: черга захоплених карт, кожна бʼє далі (BFS по полю 3×3) — 📎.
- Перемикачі правил матчу (до 2 з 15, Roulette) як дані — 🥉: одна функція порівняння з модифікаторами Reverse/Fallen Ace/Ascension.
- Колекція + правила обміну One/Diff/Direct/Full — 📎: ставка як окремий шар поверх партії.
- AI з відкритими руками: повний перебір дерева 9 ходів з альфа-бета і memo — 🥇 (дерево ~10⁹ листків без відсікань).

## Мапа на каталог
- Є: `cursor-place` + `cell-click` ↔ карту на вільну клітину · `pocket` ↔ рука · `ai-opponent` ↔ NPC (`ai-minimax` — для завдання-розвʼязника) · `online-multiplayer` ↔ PvP FF XIV · `move-timer` ↔ 90 с + 5 с · `rule-variants` ↔ правила матчу · `chain-reaction` ↔ Combo · `match-setup` · `game-screen` · `end-screen`.
- **Нема** → пропозиції карток:
  - `+edge-rank-capture` «Захоплення сусіда числом на ребрі» · entities/combat · 🌱 · слоти {compare: greater|less, ace_rule}.
  - `+same-plus-capture` «Захоплення парами: рівні ранги або рівні суми» · entities/combat · 📎 · слоти {min_pairs: 2, wall_rank: A}.
  - `+wall-as-rank` · `+combo-capture-chain` — підкартки до попередньої.
  - `+trade-rule-stakes` «Ставка партії: що переможець забирає» · game-logic/economy · 📎 · слот {one|diff|direct|full|null}.
  - `+regional-rules` «Набір правил залежить від місця й поширюється» · game-logic/constraints · 🥉.
  - `+type-count-modifier` «Ранги ростуть/падають від кількості карт типу на полі» · entities/state · 🌱.
  - `+sudden-death-replay` «Нічия → переграш тими картами, що в кого лишились» · game-logic/opponent · 🌱.
  - `+deck-rarity-limit` «Ліміт рідкісних карт у колоді» · game-logic/economy · 🌱.
  - `+forced-card-order` «Order / Chaos: карту на хід задає порядок або випадок» · game-logic/opponent · 🌱.
  - `+majority-win` · `+elemental-field-bonus` · `+hidden-hand-cards` · `+card-collection` · `+win-card-reward` · `+reverse-compare` — уже в корпусі або очевидні.

## Пропозиції до словників
- `+cond:greater` — число A більше за число B на дотичних ребрах (базове захоплення TT, Queen's Blood).
- `+cond:pair_sum` — у ≥2 пар сусідів однакова сума (Plus); не плутати з `sum` (обмеження пазла).
- `+trigger:board_full` — усі клітини поля зайняті → кінець партії.
- `+ui:card-hand` — рука карт гравця на екрані (відкрита / закрита).
- `+ui:score-tally` — живий рахунок «скільки карт мого кольору» з обох боків поля.
- `+window:deck-builder` — збирання руки/колоди з колекції з обмеженнями.
- `+window:rules-banner` — екран-банер з правилами цього матчу перед стартом.
- `+feature:card-collection` — колекція карт між партіями, поповнюється виграшами.
- `+feature:regional-rules` — правила партії залежать від локації світу гри.
- `+card:edge-rank-capture` · `+card:same-plus-capture` · `+card:trade-rule-stakes` — див. «Мапа на каталог».

## Джерела
- ⭐ [FF XIV Lodestone: Triple Triad](https://na.finalfantasyxiv.com/lodestone/playguide/contentsguide/goldsaucer/tripletriad/) — поле, 9 ходів і 10-та карта, захоплення «більше», рідкість і ліміти колоди, 15 правил матчу з описами, таймер, нагороди.
- [Wikipedia EN: Triple Triad](https://en.wikipedia.org/wiki/Triple_Triad) — 3×3, 5 карт, елементи ±1, кінець при повному полі, версії й історія.
- [Wikipedia JA: Final Fantasy VIII, розділ 2.10](https://ja.wikipedia.org/wiki/ファイナルファンタジーVIII) — ранги 1–10 (A), Open, Plus, Same, Wall Same, ланцюг після Same/Plus, Elemental, Random Hand, Sudden Death, обмін One/Diff/Direct/Full/Null, регіональні правила, Card Queen, Card Mod.
- YouTube: пошук «Triple Triad rules».

## Непевне
- (?) EN-Wikipedia пише «matching or exceeding» для базового захоплення; FF XIV і JA-Wikipedia — строго «більше». У файлі — «більше»; рівність захоплює лише через Same.
- (?) Механізм поширення й скасування регіональних правил у FF VIII (як правило «переноситься» з гравцем і як його позбутись) — у джерелах лише згадано.
- (?) Хто ходить першим у FF VIII; чи Same/Plus зараховують пару, де сусід — своя карта (за JA — так, захоплюються лише чужі з пар).
- (?) Точні назви й порядок пунктів меню FF VIII і HUD FF XIV — з памʼяті; `popup-text` «Same!/Plus!/Combo» — з памʼяті.
- (?) Кількість карт у FF VIII і поділ на рівні; у FF XIV — 80 видів станом на патч 2.51, тепер більше.
