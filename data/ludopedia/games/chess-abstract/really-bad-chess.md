---
title: Really Bad Chess
slug: really-bad-chess
aka: [RBC, «Дуже погані шахи»]
family: chess-abstract
also: []
klass: figure
axes:
  field: square
  time: turn
  opponent: ai
  info: full
  random: setup
  goal: state
year: 2016
platforms: [iOS, Android, web]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Really_Bad_Chess", best: true, note: "випадкові армії за рівнем гравця, пат = поразка, нічиїх нема, Puzzmo 2023"}
  - {kind: official, url: "https://noodlecake.com/games/really-bad-chess/", note: "режими: Ranked, Daily, Weekly, Freeplay, Versus (IAP)"}
  - {kind: other, url: "https://gamedeveloper.com/design/how-zach-gage-breaks-all-of-the-rules-in-i-really-bad-chess-i-", note: "дизайн: цінності фігур, ранг 15/50/100, до 10 000 кандидатів дошки, ферзь не в першому ряду"}
  - {kind: other, url: "https://www.pocketgamer.com/really-bad-chess/app-army-assemble-really-bad-chess-just-how-bad-is-it", note: "огляд: ранг 0–100, AI не розумнішає, кращають його фігури"}
  - {kind: other, url: "https://apps.apple.com/app/really-bad-chess/id1109751921", note: "App Store"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=really+bad+chess+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [piece-move-patterns, piece-capture, no-move-into-check, check-stalemate, checkmate, legal-move-highlight, cell-click, ai-opponent, hot-seat, daily-puzzle, difficulty-levels, weighted-spawn, main-menu, mode-select, game-screen, end-screen, shop-window, theme-select, pocket, +random-army, +rank-scaled-handicap, +stalemate-loss, +no-draws, +weekly-challenge]
proposes: ["+effect:generate_army", "+cond:value_ge", "+ui:rank-badge", "+feature:rank-handicap", "+feature:weekly-challenge", "+card:random-army", "+card:rank-scaled-handicap", "+card:stalemate-loss"]
author: opus
date: 2026-11-09
---

# Really Bad Chess — шахи з випадковими арміями, сила яких підлаштовується під твій ранг

## Суть
Звичайна дошка 8×8 і звичайні ходи фігур, але склад і розстановка армій випадкові: можна отримати 8 коней і 3 пішаки проти 9 слонів. Баланс тримає **ранг** гравця: на низькому ранзі твоя армія сильніша за армію AI, на 50 — рівні, на 100 — AI сильніший. Дебютна теорія не працює, тому гра — «шахи для тих, хто не вчив дебютів» (Zach Gage). Нічиїх нема: пат — поразка запатованого.

## Поле і час
- Дошка 8×8, рух фігур — як у [chess.md](chess.md); покроково, проти AI або hot-seat.
- Перед партією генератор будує армії: кожна сторона — король і 15 випадкових фігур (Wikipedia), фігури можуть стояти й у передньому ряду (слони попереду), але ферзь — ніколи в передньому ряду.
- Сила сторони = сума цінностей фігур (ферзь 9, тура 5, пішак 1); генератор перебирає до 10 000 кандидатів, щоб різниця сил відповідала рангу.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Король | piece | — | як у шахах; мат — кінець партії |
| Ферзь | piece | цінність 9 | як у шахах; не стартує в передньому ряду |
| Тура | piece | цінність 5 | як у шахах |
| Слон, кінь | piece | цінність (?) | як у шахах; кількість будь-яка |
| Пішак | piece | цінність 1 | як у шахах |
| Армія | — | склад, розстановка, сума цінностей | генерується під ранг |
| Ранг гравця | — | 0–100, старт 15 | росте з перемогами → армія AI кращає |

## Правила (КОЛИ → ЯКЩО → ТО)
Генерація партії:
- КОЛИ `game_start` → ТО `custom: «згенерувати армії обох сторін: до 10 000 випадкових дошок, взяти ту, де різниця сум цінностей відповідає рангу»` (слово-кандидат `+effect:generate_army`).
- КОЛИ `custom: «генератор ставить ферзя»` → ЯКЩО `custom: «клітина в передньому ряду»` → ТО `block`.
- КОЛИ `game_start` → ЯКЩО `custom: «ранг 50»` → ТО `custom: «суми цінностей армій рівні»`; ЯКЩО `custom: «ранг < 50»` → армія гравця сильніша; ЯКЩО `custom: «ранг > 50»` → сильніша армія AI (кандидат `+cond:value_ge`).

Хід:
- КОЛИ `input(move(p, to))` → ЯКЩО `turn_of(player)` and `legal(move)` → ТО `move(p, to)`, `end_turn`.
- КОЛИ `contact(p, enemy)` → ТО `disappear_b`.
- КОЛИ `input(move)` → ЯКЩО `custom: «після ходу свій король під шахом»` → ТО `block`.

Кінець партії:
- КОЛИ `no_moves(side)` → ЯКЩО `in_check(side)` → ТО `lose` (мат).
- КОЛИ `no_moves(side)` → ЯКЩО `not in_check(side)` → ТО `lose` (пат = поразка запатованого).
- КОЛИ `repetition` → ТО `custom: «нічиєї нема — грають далі»`.
- КОЛИ `custom: «на дошці лише два королі»` → ТО `custom: «партія триває»` (нестачі матеріалу як нічиєї нема).
- КОЛИ `win` → ЯКЩО `mode(ranked)` → ТО `counter(rank, +n)` (?).

- Перемога: мат або пат суперника · Поразка: мат або пат собі · Нічия: нема.

## Керування і ввід
- Тач: тап фігури → підсвічені легальні клітини → тап цілі (мобільна гра).
- Versus: hot-seat на одному пристрої (IAP).
- Армії не обирають і не розставляють — їх дає генератор.

## Вікна, меню, HUD
- `main-menu` = `mode-select`: Ranked → `game-screen`; Daily Challenge; Weekly Challenge; Freeplay (практика); Versus (локально, IAP).
- `game-screen`: дошка, `rank-badge` (поточний ранг), `legal-move-highlight`; `pocket` — показ узятих фігур (IAP).
- `end-screen`: перемога/поразка, зміна рангу (?).
- `shop-window` — одна покупка: Versus, без реклами, узяті фігури, палітри.
- `settings-window` → `theme-select` (альтернативні палітри кольорів, IAP).

## Фічі поза полем
- `rank-handicap` — ранг 0–100: перемоги піднімають ранг, і генератор дає AI сильнішу армію; AI як «розум» не посилюється (Pocket Gamer).
- `mode-daily` / `weekly-challenge` — дошка дня й тижня проти AI; з 2023 — щоденна гра на порталі Puzzmo.
- `mode-practice` — Freeplay.
- `hotseat` — Versus.
- `theme-select` — палітри.

## Варіації й родичі
- [lichess-variants.md](lichess-variants.md): Chess960 — випадкова лише розстановка, склад стандартний; тут випадковий і склад.
- [chess-2-sequel.md](chess-2-sequel.md) — вибір асиметричної армії замість випадкової; [shotgun-king.md](shotgun-king.md) — асиметрія «один король проти армії».
- Пат = поразка — дзеркало Duck chess (пат = перемога запатованого) з [chess-rule-twists.md](chess-rule-twists.md).
- **Осі варіацій**:
  - **Склад армії**: стандарт · стандарт, випадкова розстановка (960) · випадковий склад під бюджет (RBC) · вибір гравця (Chess 2).
  - **Баланс**: симетрія · гандикап від рангу.
  - **Пат**: нічия · поразка (RBC) · перемога (Duck).

## Цікавинки для курсу
- Генератор армії під бюджет цінності з перебором кандидатів — 📎 (сума цінностей + rejection sampling).
- Обмеження розстановки (ферзь не в передньому ряду, слони де завгодно) як фільтр генератора — 🌱.
- Ранг як динамічна складність: перемога → сильніша армія AI — 🌱 поверх генератора.
- Пат = поразка, нема нічиєї повторенням і нестачею матеріалу — 🌱 (прибрати правила з рушія).
- Daily / weekly дошка з фіксованим seed — 📎.
- Оцінка «справедливості» випадкової дошки не лише сумою цінностей (мобільність, безпека короля) — 🥇.

## Мапа на каталог
- Є: `piece-move-patterns` · `piece-capture` · `no-move-into-check` · `check-stalemate` · `checkmate` · `legal-move-highlight` · `cell-click` · `ai-opponent` · `hot-seat` ↔ Versus · `daily-puzzle` ↔ Daily Challenge (фіксований seed) · `difficulty-levels` ↔ ранг · `weighted-spawn` ↔ випадковий вибір фігур (?) · `mode-select` · `shop-window` · `theme-select` · `pocket` ↔ узяті фігури.
- **Нема** → пропозиції карток:
  - `+random-army` «Випадкова армія під бюджет цінності» · levels/generation · 📎 · слоти {values: Q9 R5 P1…, slots, tries: 10000, banned: queen@front}.
  - `+rank-scaled-handicap` «Гандикап сторін від рангу гравця» · game-logic/difficulty · 🌱 · слоти {rank: 0–100, even: 50}.
  - `+stalemate-loss` «Пат = поразка запатованого» · game-logic/lose · 🌱 (родич `+stalemate-win` з chess-rule-twists).
  - `+no-draws` «Без нічиїх (повторення, нестача матеріалу)» · game-logic/win · 🌱.
  - `+weekly-challenge` «Задача тижня» · levels/bank · 📎 — родич `daily-puzzle`.

## Пропозиції до словників
- `+effect:generate_army(side, budget)` — згенерувати склад і розстановку армії під бюджет (RBC; родич `random-setup` Chess960).
- `+cond:value_ge(a, b)` — порівняння цінності (тут — сум армій; уже пропонувався в chess-rule-twists, підтверджую).
- `+ui:rank-badge` — ранг гравця на екрані (підтверджую).
- `+feature:rank-handicap` — ранг керує гандикапом сторін, а не силою AI.
- `+feature:weekly-challenge` — задача тижня (поруч із `mode-daily`).
- `+card:random-army` · `+card:rank-scaled-handicap` · `+card:stalemate-loss` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Really Bad Chess](https://en.wikipedia.org/wiki/Really_Bad_Chess) — Zach Gage, iOS 13.10.2016, Android 18.05.2017 (Noodlecake), король + 15 випадкових фігур за рівнем, пат = поразка, нема нічиїх, гра триває з голими королями, Puzzmo 2023.
- [Noodlecake: Really Bad Chess](https://noodlecake.com/games/really-bad-chess/) — режими й склад IAP.
- [Game Developer: How Zach Gage breaks all of the rules](https://gamedeveloper.com/design/how-zach-gage-breaks-all-of-the-rules-in-i-really-bad-chess-i-) — цінності, ранг 15/50/100, 10 000 кандидатів, ферзь не в передньому ряду.
- [Pocket Gamer: App Army](https://www.pocketgamer.com/really-bad-chess/app-army-assemble-really-bad-chess-just-how-bad-is-it) — ранг 0–100; AI не розумнішає (бачив лише в пошуковій видачі).
- reallybadchess.com — сертифікат прострочений, не відкрився.

## Непевне
- (?) Склад: Wikipedia — «один король + 15 фігур», Game Developer — приклад «чотири королі»; чи буває кілька королів і як тоді мат — не перевірено.
- (?) Цінності слона й коня (3?) — у джерелах названі лише Q9 R5 P1.
- (?) Перетворення пішака: чи є і на що — джерела мовчать.
- (?) На скільки змінюється ранг за перемогу/поразку, чи падає за поразку.
- (?) Чи Daily/Weekly — однакова для всіх дошка (seed) — не перевірено.
- (?) Правило «пат = поразка» з Wikipedia; чи діє воно й у Versus — не перевірено.
- `weighted-spawn` як відповідник генератора — натяжка.
