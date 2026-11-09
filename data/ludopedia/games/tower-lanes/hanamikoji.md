---
title: Hanamikoji
slug: hanamikoji
aka: []
family: tower-lanes
also: [board-digital]
klass: cursor
axes:
  field: 1d
  time: turn
  opponent: hotseat
  info: hidden
  random: runtime
  goal: territory
year: 2013
platforms: [board]
links:
  - {kind: other, url: "https://rulespal.com/hanamikoji/rulebook", best: true, note: "повні правила: 7 гейш, 21 карта предметів, 4 одноразові дії, роздача, підрахунок прихильності, перемога 4 гейші або 11 чарівності, тайбрейк"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Hanamikoji+how+to+play", note: "пошук; як грати"}
stage: v1
coverage: 70
mechanics: [hot-seat, turn-enforcement, pocket, pass-device, end-screen, help-window, +lane-grid, +deck-draw, +hidden-hand-cards, +area-majority, +alt-win-conditions, +multi-round-match, +i-split-you-choose, +one-use-actions, +hidden-removed-card, +sticky-majority-markers, +secret-reserve-card, +rotating-first-player]
proposes: ["+role:card", "+effect:draw_card", "+effect:discard", "+trigger:round_start", "+trigger:round_end", "+cond:majority", "+window:choice-window", "+window:round-summary", "+ui:action-tokens", "+card:i-split-you-choose", "+card:one-use-actions"]
author: opus
date: 2026-11-09
---

# Hanamikoji — сім гейш у ряд: чотири одноразові дії ділять карти між тобою й суперником, а більшість карт біля гейші приносить її прихильність

## Суть
Карткова дуель на двох (Kota Nakayama, 2013 — див. «Непевне»). Між гравцями ряд із 7 гейш; кожна має чарівність 2–5, рівну кількості карт її предмета в колоді з 21 карти. За раунд кожен робить рівно 4 ходи, і кожен хід — одна з чотирьох **одноразових дій**: сховати карту (Secret), скинути дві (Trade-off), запропонувати три, з яких суперник бере одну (Gift), або дві пари, з яких суперник бере пару (Competition). Ядро — «ділю я, обираєш ти»: дві з чотирьох дій віддають супернику частину твоїх карт.

## Поле і час
- Поле — 7 карт-гейш в один ряд (`field: 1d`); у кожної дві сторони: карти предметів кожен кладе зі свого боку біля відповідної гейші. Суміжність гейш значення не має — це 7 незалежних «смуг» більшості.
- На кожній гейші — маркер прихильності: у центрі (нічия) або на боці гравця; між раундами маркер **лишається**.
- Раунд: роздача → 8 ходів (по 4 кожному) → підрахунок; раундів скільки завгодно, до виконання умови перемоги.
- Інформація: рука, Secret-карта, скинуті й вилучена карта — закриті; карти біля гейш відкриті.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гейша ×7 | zone (`+role:lane`) | чарівність = кількість її предметів | смуга більшості: хто має більше її карт, той забирає маркер |
| Карта предмета | piece (`+role:card`) | тип = гейша; 21 карта | кладеться біля гейші свого типу на один з боків |
| Маркер прихильності ×7 | mark | центр / сторона | рухається до переможця гейші; при нічиї стоїть |
| Маркер дії ×4 на гравця | switch | Secret, Trade-off, Gift, Competition; кольоровий / перевернутий | одна дія — раз за раунд |
| Колода | supply | 8 карт після роздачі | добір 1 карти на початку ходу |
| Рука | supply | 6 на старті раунду | джерело для всіх дій |
| Вилучена карта | supply | 1 закрита | у раунді не грає — дірка в інформації |
| Secret-карта | supply | 1 закрита під маркером | відкривається й рахується в кінці раунду |
| Trade-off-карти | supply | 2 закриті | не рахуються в цьому раунді |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `custom: «round_start»` → ТО `custom: «перемішати всі 21 карту»`, `custom: «1 карта вбік закрито»`, `give(each, 6 cards)`, `custom: «решта 8 — колода»`, `clear_state(action_markers, used)`.
- КОЛИ `turn_start(side)` → ТО `custom: «draw_card ×1 з колоди»`.
- КОЛИ `input(action, marker)` → ЯКЩО `turn_of(side)` and `not state(marker, used)` → ТО виконати дію, `set_state(marker, used)`, `end_turn`; інакше `block`.
- КОЛИ `input(secret, card)` → ТО `custom: «карта закрито під маркер Secret»` — свою можна переглядати будь-коли.
- КОЛИ `input(trade_off, card×2)` → ТО `custom: «discard 2 закрито під маркер Trade-off — у раунді не рахуються»`.
- КОЛИ `input(gift, card×3)` → ТО `reveal(card×3)`, `choose(суперник бере 1)`, `place(opponent, chosen)` біля гейші її типу, `place(player, other×2)`.
- КОЛИ `input(competition, card×4)` → ТО `reveal(card×4)`, `custom: «гравець ділить на 2 пари»`, `choose(суперник бере пару)`, `place(opponent, pair)`, `place(player, other_pair)`.
- КОЛИ `custom: «обидва зробили по 4 ходи»` → ТО `reveal(secret_cards)`, `place(each, secret)` біля своїх гейш.
- КОЛИ `custom: «round_end: для кожної гейші»` → ЯКЩО `custom: «на моєму боці її карт більше, ніж на чужому»` → ТО `set_side(favor_marker, player)`.
- КОЛИ `custom: «round_end»` → ЯКЩО `custom: «карт порівну або нема в обох»` → ТО `custom: «маркер не рухається»`.
- КОЛИ `custom: «підрахунок»` → ЯКЩО `counter(geishas[side], >=, 4)` or `counter(charm[side], >=, 11)` → ТО `win`.
- КОЛИ `custom: «підрахунок»` → ЯКЩО `custom: «в одного 4 гейші, а в іншого 11+ чарівності»` → ТО `win` того, у кого 11+.
- КОЛИ `custom: «умову не виконано»` → ТО `custom: «зібрати всі карти; маркери прихильності лишаються; маркери дій — кольором догори»`, `custom: «стартовим стає другий гравець»`.
- Перемога: 4 гейші або 11+ чарівності на маркерах · Поразка: суперник виконав умову першим · Рахунок: сума чарівності гейш з маркером на твоєму боці.

## Керування і ввід
- Хід: добрати 1 карту → обрати невикористаний маркер дії → обрати карти з руки (1 / 2 / 3 / 4 і поділ на пари).
- Відповідь суперника на Gift/Competition — вибір 1 з 3 карт або 1 з 2 пар; це єдиний момент, коли гравець діє не в свій хід.
- Порядок дій вільний; пропустити дію не можна.

## Вікна, меню, HUD
- `game-screen` (цифрова версія): ряд 7 гейш з маркерами прихильності, карти обох сторін біля гейш, `pocket` (рука), `+ui:action-tokens` (4 маркери: доступні / використані), лічильники гейш і чарівності, `remaining-counter` колоди.
- `+window:choice-window` (цифрова версія) — суперник обирає карту або пару з пропозиції.
- `pass-device` (цифрова версія) — завіса між ходами в hot-seat, бо руки закриті.
- `+window:round-summary` — відкриття Secret, переміщення маркерів, поточні 4/11.
- `end-screen`, `help-window`.

## Фічі поза полем
- Багатораундова партія без ліміту раундів; стартовий гравець чергується.
- Варіантів у правилах RulesPal нема.

## Варіації й родичі
- Родичі в корпусі: [schotten-totten](schotten-totten.md) (ряд «каменів», більшість за кожен), [air-land-and-sea](air-land-and-sea.md) (3 театри, контроль більшості), [riftforce](riftforce.md), [queens-blood](queens-blood.md) (ряд забирає більший); [arboretum](../board-digital/arboretum.md) згадує Hanamikoji як родича «рука — і ресурс, і право».
- **Осі варіацій**: розподіл — сам кладеш / «ділю я, обираєш ти» (1 з 3, пара з 2) · дії — довільні / кожна раз за раунд · маркер більшості — скидається щораунд / лишається · перемога — одна умова / дві паралельні з пріоритетом.

## Цікавинки для курсу
- «Ділю я, обираєш ти» як ігрова дія: 1 з 3 і пара з 2 пар — 🌱 логіка, 📎 з AI, що оцінює поділ.
- Чотири одноразові маркери дій на раунд: стан «використано» + блок повтору — 🌱.
- Вилучена закрита карта: підрахунок «скільки ще може бути карт типу X» — 📎.
- Маркери більшості, що не скидаються між раундами, і дві умови перемоги з пріоритетом 11 > 4 — 🌱.
- AI для двох рішень (свій хід і вибір з пропозиції) з неповною інформацією — 🥈.

## Мапа на каталог
- Є: `hot-seat`, `turn-enforcement`, `pocket` ↔ рука · `pass-device` ↔ закриті руки · `end-screen`, `help-window`.
- **Нема** → пропозиції карток:
  - `+lane-grid`, `+deck-draw`, `+hidden-hand-cards`, `+area-majority`, `+alt-win-conditions`, `+multi-round-match` — уже в корпусі.
  - `+i-split-you-choose` «Гравець ділить набір, суперник обирає частину» · game-logic/opponent · 📎.
  - `+one-use-actions` «Набір дій, кожна раз за раунд» · game-logic/opponent · 🌱.
  - `+hidden-removed-card` «Карта, вилучена закрито на раунд» · game-logic/constraints · 🌱.
  - `+sticky-majority-markers` «Маркер більшості лишається між раундами» · game-logic/score · 🌱.
  - `+secret-reserve-card` «Закрита карта, що рахується лише в кінці» · game-logic/score · 🌱.
  - `+rotating-first-player` «Стартовий гравець чергується щораунд» · game-logic/opponent · 🌱.

## Пропозиції до словників
- `+role:card`, `+effect:draw_card`, `+effect:discard` — повтори з корпусу.
- `+trigger:round_start`, `+trigger:round_end` — повтори.
- `+cond:majority` — на моєму боці смуги/зони більше одиниць, ніж на чужому.
- `+window:choice-window`, `+window:round-summary` — повтори.
- `+ui:action-tokens` — ряд одноразових маркерів дій зі станом.
- `+card:i-split-you-choose`, `+card:one-use-actions`.

## Джерела
- ⭐ [RulesPal: Hanamikoji rulebook](https://rulespal.com/hanamikoji/rulebook) — компоненти, роздача (1 карта вилучена, по 6, колода 8), 4 дії, підрахунок, оновлення, перемога 4 / 11 і пріоритет 11.
- YouTube: пошук «Hanamikoji how to play».

## Непевне
- (?) Автор (Kota Nakayama) і видавець (EmperorS4) — з памʼяті, RulesPal не називає; рік 2013 — з черги.
- (?) Розподіл чарівності 2/2/2/3/3/4/5 між гейшами: RulesPal каже лише «чарівність = кількість карт її предмета» і 21 карта.
- (?) Що буде, якщо обидва виконали умову в одному підрахунку (обидва 11+ або обидва по 4 гейші) — правила мовчать.
- (?) Офіційні цифрові версії (застосунок, BGA) — не перевірено.
