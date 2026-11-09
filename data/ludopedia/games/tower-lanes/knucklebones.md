---
title: Knucklebones (Cult of the Lamb)
slug: knucklebones
aka: []
family: tower-lanes
also: [word-number]
klass: cursor
axes:
  field: square
  time: turn
  opponent: ai
  info: full
  random: runtime
  goal: score
year: 2022
platforms: [PC, macOS, PS4, PS5, Xbox One, Xbox Series X/S, Switch]
links:
  - {kind: other, url: "https://www.gamepressure.com/cult-of-the-lamb/knucklebones-rules-and-how-to-play/z6102ab", best: true, note: "правила Cult of the Lamb: 3 стовпці по 3, пара ×2, трійка ×9, збіг у стовпці навпроти знищує чужі кубики, кінець — повне поле; суперники й ставки"}
  - {kind: other, url: "https://rulespal.com/knucklebones/rulebook", note: "настільна адаптація: 9 кубиків, ряди замість стовпців, знищені кубики вертаються в руку; приклади підрахунку"}
  - {kind: steam, url: "https://store.steampowered.com/app/1313140/", note: "Cult of the Lamb; доповнення Unholy Alliance — кнукльбоунс на двох"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Cult+of+the+Lamb+Knucklebones+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 75
mechanics: [cell-click, ai-opponent, difficulty-levels, end-screen, round-currency, +lane-grid, +single-die-roll, +same-value-multiplier, +opposite-column-clear, +board-full-end, +wager-coins, +opponent-ladder, +local-versus]
proposes: ["+effect:roll_die", "+trigger:board_full", "+cond:same_in_column", "+role:die", "+ui:column-score", "+ui:wager-picker", "+window:opponent-select", "+card:same-value-multiplier", "+card:opposite-column-clear"]
author: opus
date: 2026-11-09
---

# Knucklebones (Cult of the Lamb) — кидай кубик у один із трьох стовпців: однакові множать очки, однакове навпроти — знищує чужі

## Суть
Кубикова міні-гра з Cult of the Lamb: у кожного гравця поле 3×3 — три стовпці по три місця, стовпці стоять навпроти стовпців суперника, як смуги. Щоходу кидаєш один d6 і ставиш у свій стовпець; однакові значення в стовпці **множаться**, а поставлене значення **знищує всі такі самі кубики** в стовпці суперника навпроти. Партія закінчується, щойно чиєсь поле заповнене; більше очок — перемога.

## Поле і час
- Два поля 3×3: стовпець *i* гравця стоїть навпроти стовпця *i* суперника — пара стовпців = смуга бою.
- Хід почерговий: кидок → вибір стовпця з вільним місцем → підрахунок.
- Повна інформація про поле; випадковість — лише в кидку.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Кубик | tile (`+role:die`) | значення 1–6 | ставиться у вільне місце свого стовпця; дає очки |
| Стовпець ×3 | zone (`+role:lane`) | ≤ 3 кубики, очки стовпця | рахує очки з множниками; навпроти — стовпець суперника |
| Поле гравця | zone | 9 місць | повне — кінець партії |
| Суперник | — | складність 1–4, максимальна ставка | Ratau, Flinky, Klunko і Bop, Shrumy |
| Ставка | resource | монети, до максимуму суперника | виграш/програш монет |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(side)` → ТО `custom: «roll_die: d6»`.
- КОЛИ `input(column)` → ЯКЩО `count(dice_in_column, <, 3)` → ТО `place(player, die)`; інакше `block`.
- КОЛИ `spawned(die)` → ЯКЩО `occupied(opposite_column, same_value_die)` → ТО `disappear(all_same_value_dice_in_opposite_column)`.
- КОЛИ `spawned(die)` → ТО `custom: «очки стовпця = Σ по значеннях v × n × n, де n — скільки кубиків зі значенням v»` (пара шісток = 24, три пʼятірки = 45).
- КОЛИ `custom: «очки гравця»` → ТО `score(сума трьох стовпців)`.
- КОЛИ `custom: «поле гравця заповнене (9 кубиків)»` → ТО `game_over`.
- КОЛИ `game_over` → ЯКЩО `custom: «твої очки більші»` → ТО `win`, `currency(+ставка)`; інакше `lose`, `currency(-ставка)`.
- КОЛИ `custom: «вибір суперника»` → ЯКЩО `custom: «ставка ≤ максимуму суперника»` → ТО `custom: «партія на монети»`.
- Перемога: більше очок, коли чиєсь поле заповнене · Поразка: менше · Рахунок: Σ стовпців з множником v × n².

## Керування і ввід
- Після автоматичного кидка — вибір одного з трьох своїх стовпців (курсор/стрілки, клік).
- Перед партією — вибір ставки.

## Вікна, меню, HUD
- `+window:opponent-select` — Lonely Shack (Ратау) і зустрічі в регіонах: Ratau (Darkwood), Flinky (Anura), Klunko і Bop (Anchordeep), Shrumy (Silk Cradle).
- `+ui:wager-picker` — ставка до 10 / 15 / 20 / 50 монет відповідно.
- `game-screen`: два поля 3×3 одне навпроти одного, кубик, що котиться, `+ui:column-score` над кожним стовпцем, загальні очки обох.
- `end-screen` — переможець, виграні/програні монети.

## Фічі поза полем
- `difficulty-presets` за суперником: 1 → 4 (Ratau → Shrumy); суперники відкриваються зустрічами в регіонах (`+opponent-ladder`).
- `+wager-coins`: монети Cult of the Lamb як ставка.
- Unholy Alliance: кнукльбоунс на двох (`+local-versus`, `mode-versus`).

## Варіації й родичі
- **Настільна адаптація (RulesPal)**: 9 кубиків у руці, ряди замість стовпців, знищені кубики вертаються в руку власника, кінець — коли в когось скінчились кубики; множник той самий (пара — кожен ×2, трійка — кожен ×3).
- Родичі в корпусі: [queens-blood](queens-blood.md) (3 ряди, суми по смугах), [gwent](gwent.md), [marvel-snap](marvel-snap.md) (більше в смузі), [inscryption](inscryption.md) (колонки навпроти).
- **Осі варіацій**: взаємодія смуг — нема / знищення однакових навпроти / атака · множник — без / пара і трійка / v × n² · кінець — повне поле / порожня рука / N ходів.

## Цікавинки для курсу
- Очки стовпця v × n² для груп однакових значень — 🌱.
- Знищення однакових кубиків у стовпці навпроти — 🌱; разом із множником — дилема «будувати комбо чи бити чуже» — 📎.
- AI-суперник: жадібний за очікуваними очками (кидок відомий, вибір з 3 стовпців) — 📎; expectimax на кілька ходів — 🥇.
- Повне поле як кінець партії — 🌱.

## Мапа на каталог
- Є: `cell-click` ↔ вибір стовпця · `ai-opponent` · `difficulty-levels` ↔ 4 суперники · `end-screen` · `round-currency` ≈ ставка монет.
- **Нема** → пропозиції карток:
  - `+lane-grid`, `+opponent-ladder` — уже в корпусі.
  - `+single-die-roll` «Хід — кидок одного кубика» · game-logic/random · 🌱.
  - `+same-value-multiplier` «Однакові значення в стовпці множать очки (v × n²)» · game-logic/score · 🌱.
  - `+opposite-column-clear` «Поставлене значення знищує такі самі в стовпці навпроти» · entities/combat · 🌱.
  - `+board-full-end` «Партія закінчується, коли поле одного гравця повне» · game-logic/win · 🌱.
  - `+wager-coins` «Ставка валюти гри на партію» · game-logic/economy · 🌱; `+local-versus` · 📎.

## Пропозиції до словників
- `+effect:roll_die` — кинути кубик (значення відоме перед вибором).
- `+trigger:board_full` — поле гравця заповнене.
- `+cond:same_in_column` — у стовпці / стовпці навпроти є кубик того ж значення.
- `+role:die` — кубик як сутність поля; `+role:lane` — повтор.
- `+ui:column-score` — очки над стовпцем; `+ui:wager-picker`.
- `+window:opponent-select` — вибір суперника зі ставкою.
- `+card:same-value-multiplier`, `+card:opposite-column-clear`.

## Джерела
- ⭐ [gamepressure: Knucklebones rules](https://www.gamepressure.com/cult-of-the-lamb/knucklebones-rules-and-how-to-play/z6102ab) — 3 стовпці по 3, значення = очки, пара множить суму на 2, трійка ×9, знищення однакових навпроти, кінець при повному полі, таблиця суперників (регіон, ставка, складність).
- [RulesPal: Knucklebones](https://rulespal.com/knucklebones/rulebook) — настільна версія: 9 кубиків, ряди, повернення в руку, приклади «2 шістки = 24», «3 пʼятірки = 45».
- [Steam: Cult of the Lamb](https://store.steampowered.com/app/1313140/) — гра-носій (Massive Monster, 11.08.2022), Unholy Alliance з кнукльбоунсом на двох.
- YouTube: пошук «Cult of the Lamb Knucklebones gameplay».

## Непевне
- (?) Чи гравець обирає місце в стовпці, чи кубик стає в наступне вільне (gamepressure пише «column and position»).
- (?) Чи зсуваються решта кубиків стовпця після знищення.
- (?) Нічия за очками.
- (?) Хто ходить першим і як працює ставка при нічиїй.
- (?) Формат гри на двох в Unholy Alliance (за одним екраном чи онлайн).
