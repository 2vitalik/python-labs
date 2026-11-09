---
title: Six Match
slug: six-match
aka: []
family: falling-match
also: []
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: runtime
  goal: score
year: 2017
platforms: [Android, iOS, PC, macOS]
links:
  - {kind: itch, url: "https://st33d.itch.io/six-match", best: true, note: "правила від автора: аватар міняється з монетами, збіг за 6 ходів, Survival/Puzzle, Help, керування"}
  - {kind: other, url: "https://apps.apple.com/app/six-match/id1327790148", note: "App Store: wild-монети, карти й бонус, діаманти внизу, клітки штовхають лінії, кубики, історія версій"}
  - {kind: other, url: "https://st33d.itch.io/six-match/devlog", note: "devlog 2017–2023: блок-штамп, кубики, Help → бомба, cash-in, glass, розміри поля"}
  - {kind: other, url: "https://st33d.itch.io/six-match/devlog/11236/block-party", note: "монета кінця туру → блок, що штампує фішки; кубики до номера туру"}
  - {kind: other, url: "https://st33d.itch.io/six-match/devlog/10101/help-for-hints", note: "нема шляху до збігу → сусідня монета стає бомбою"}
  - {kind: other, url: "https://st33d.itch.io/six-match/devlog/11914/cash-in", note: "Help скінчились → знищити всі монети на очки й завершити"}
  - {kind: other, url: "https://st33d.itch.io/six-match/devlog/45095/pc", note: "PC 7×7 замість мобільних 6×8, клавіатура й геймпад"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=six+match+st33d+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [move-4dir, keyboard-controls, swipe-gestures, swap-on-contact, line-match-clear, move-limit, gravity-fall, push-object, explode-area, unsolvable-states, level-solver, progress-acceleration, event-points, score-records, leaderboard, save-autosave, undo-redo, mode-select, main-menu, pause-menu, confirm-dialog, game-screen, end-screen, +edge-spawn, +wildcard-tile, +ingredient-drop, +poker-hand-bonus, +stamp-block, +dice-coin, +self-matching-tile, +help-charges, +cash-out, +death-rewind, +move-during-cascade, +clear-board-goal]
proposes: ["+card:poker-hand-bonus", "+card:stamp-block", "+card:dice-coin", "+card:self-matching-tile", "+card:help-charges", "+card:death-rewind", "+card:move-during-cascade", "+card:clear-board-goal", "+feature:help-charges"]
author: opus
date: 2026-11-09
---

# Six Match — match-3, де ти аватар: крок у монету міняє вас місцями, а збіг треба зробити за 6 ходів

## Суть
Mr Swap-With-Coins стоїть на полі монет: кожен крок у сусідню клітину міняє його місцями з монетою, тобто аватар «протягує» монету за собою, як порожня клітина в п'ятнашках. Мета — за 6 кроків чи менше скласти лінію з 3 однакових; збіг зникає, монети падають, лічильник ходів знову повний. Автор називає це гібридом «sliding tile puzzle» і match-3. Кожен збіг дає карту — покерні комбінації з карт дають бонус; згодом додаються кубики, діаманти, блоки-штампи, клітки, скло, бомби.

## Поле і час
- Квадратна сітка: мобільна версія 6×8, PC — 7×7 (devlog «PC»).
- Покроково: хід = крок аватара; падіння й досипання анімуються, але рухатися можна й під час падіння («ninja matching», каже автор).
- Гравітація вниз, нові монети — згори (?).
- «Тур» — цикл гри, наприкінці якого падає особлива монета чи блок; з турами росте складність (devlog).
- Survival триває тижнями: автосейв.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Mr Swap-With-Coins | player | 6 ходів до збігу | крок у монету — обмін місцями |
| Монета | tile | тип/колір | 3 в лінію однакових — зникає; падає без опори |
| Wild-монета | tile | — | за збіг з 4 або перехрестя; підходить до будь-якого типу; може стати бомбою |
| Бомба | object | — | вибухає й чистить ряд або стовпець (?) |
| Діамант (gem) | pickup | — | не збігається; збирається, коли доходить до нижнього ряду |
| Кубик-монета | tile | значення 1–6 | замінила черепи; значення росте з номером туру; знімається «з умінням» (?) |
| Клітка | object | — | штовхає цілу лінію монет |
| Блок-штамп | object | — | падає наприкінці туру; кожна клітина, де він зупинився, отримує фішку |
| Фішка (chip) | mark | 1 очко | збір збігом поверх неї (як «желе» Candy Crush) |
| Кольоровий незнищенний блок | static | по одному на колір | падає перед блоками-штампами (v1.2) |
| Скло (glass) | tile | — | «монета, що збігається сама» (?) |
| Карта | pickup | тип монети | дається за збіг; набір карт — покерна рука |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `occupied(next_cell, coin)` → ТО `swap(player, coin)`, `counter(moves_left, -1)`.
- КОЛИ `input(dir)` → ЯКЩО `custom: «край поля або незнищенний блок»` → ТО `block`.
- КОЛИ `contact(player, cage)` → ТО `push` — клітка зсуває всю лінію монет (?).
- КОЛИ `pattern(line(3))` → ЯКЩО `same(coins, type)` → ТО `clear(line)`, `give(player, card)`, `set_value(moves_left, 6)`.
- КОЛИ `pattern(line(4))` or `custom: «збіг-перехрестя»` → ТО `spawn(wild_coin)`.
- КОЛИ `after(clear)` → ТО `fall(unsupported)`, `spawn_at(coin, top)`.
- КОЛИ `custom: «карти в руці утворили покерну комбінацію»` → ТО `score(n)` — флеш дає 50 (devlog «Transitions»).
- КОЛИ `reach(gem, bottom_row)` → ТО `pickup`, `score(n)`.
- КОЛИ `custom: «кінець туру»` → ТО `spawn_at(stamp_block, top)`; КОЛИ `custom: «блок зупинився на клітині»` → ТО `mark(cell, chip)`.
- КОЛИ `custom: «збіг поверх фішки»` → ТО `unmark(cell)`, `score(1)`.
- КОЛИ `spawned(dice_coin)` → ТО `set_value(dice, random(1..min(tour, 6)))`; кубик у збігу дає 6 (devlog).
- КОЛИ `counter(moves_left, ==, 0)` → ТО `lose` (?) → `confirm-dialog`: витратити Help, щоб відмотатися до автосейва (v1.3).
- КОЛИ `input(help)` → ЯКЩО `path_exists(player, match)` → ТО `custom: «привид показує ходи до збігу»`; інакше `transform(neighbour_coin, bomb)`.
- КОЛИ `input(help)` → ТО `counter(help, -1)`: 3 безкоштовні підказки + 6 Help за гру.
- КОЛИ `counter(help, ==, 0)` → ТО `choose(cash_in)`: `clear(all_coins)`, `score(n)`, `game_over`.
- КОЛИ `all_gone(coins)` → ЯКЩО `mode(puzzle)` → ТО `win`.
- КОЛИ `input(undo)` → ЯКЩО `mode(puzzle)` → ТО `undo(1)`; `input(redo)` — повторити.
- Рахунок Survival: очки за збіги, фішки, діаманти, покерні руки, кубики; рекорд на титульному екрані.

## Керування і ввід
- PC: WASD / стрілки — крок; Space або Z — Help (Survival) / Undo (Puzzle); X — Redo; Esc — меню. Геймпад, перепризначення клавіш у стартовому діалозі.
- Мобільні: свайпи (у коментарях — скарги на випадкові свайпи); «мертва зона» згори й знизу екрана (v1.2).
- Fast-move вимкнено за замовчуванням (v1.2).

## Вікна, меню, HUD
- `main-menu` — Survival · Puzzle; `hi-score` на титулі; відмова від аналітики (v1.3).
- `game-screen`: поле, `score`, `move-counter` (лишилось ходів із 6), `hint-button` «Help» з лічильником безкоштовних підказок, `pocket` — зібрані карти (?); у Puzzle — `undo-button`, `redo-button`.
- `pause-menu` (Esc) → Quit → `confirm-dialog`.
- `end-screen` — game over з найкращим рахунком (закривається пробілом).
- `custom-window` — пропозиція cash-in, коли Help скінчились; діалог «відмотатися за Help» після смерті.
- `puzzle-select` (?) — список коротких пазлів.

## Фічі поза полем
- `mode-classic` (Survival) · `mode-puzzle` (Puzzle: очистити поле від монет, з undo/redo).
- `autosave` — одна партія Survival може тривати тижнями.
- `hint` з лімітом: привид показує шлях; ШІ підказок вичерпно перевіряє, чи є збіг у межах 6 ходів.
- `leaderboard-online` / `achievements` — Game Center у «Supports» (?), хоча v1.0 «прибрала соціальні функції».
- Без реклами, таймерів і pay-to-win після v1.0.

## Варіації й родичі
- Еволюція за devlog: черепи → кубики-монети; «мертва монета» кінця туру → блок-штамп; таймерні підказки → кнопка Help; бомба як вихід з глухого кута; cash-in; скло (iOS, 2018); Puzzle-режим (2022).
- Родичі: `bejeweled` / `candy-crush` (свап сусідніх; фішки = желе, діаманти = інгредієнти), `poker-smash` (покер + збіги), п'ятнашки (обмін з «порожнечею»). Рецензенти згадують Swap Sword (?) як схожу ідею з монстрами.
- **Осі варіацій**: хто міняє плитки (курсор / **аватар, що крокує крізь них**) · ліміт (нема / ходи на рівень / **ходи до наступного збігу**) · глухий кут (перемішування / **бомба з підказки** / cash-in).

## Цікавинки для курсу
- Аватар-«дірка»: крок = swap з монетою — 🌱.
- Ліміт «збіг за 6 ходів», що скидається після кожного збігу, — 🌱.
- Вичерпний пошук «чи є збіг за ≤6 кроків» (BFS по станах аватара й поля) для підказки і виявлення глухого кута — 🥇.
- Покерна рука з карт за збіги — окрема оцінка комбінацій — 📎.
- Блок-штамп, що лишає фішки, і діаманти, які треба довести до низу, — 📎.
- Cash-in: добровільне завершення з конвертацією поля в очки — 🌱.

## Мапа на каталог
- Є: `move-4dir` · `keyboard-controls` · `swipe-gestures` · `swap-on-contact` ↔ крок = обмін · `line-match-clear` · `move-limit` ↔ 6 ходів · `gravity-fall` · `push-object` ↔ клітка · `explode-area` ↔ бомба · `unsolvable-states` + `level-solver` ↔ ШІ підказок · `progress-acceleration` ↔ тури · `event-points` · `score-records` · `leaderboard` · `save-autosave` · `undo-redo` (Puzzle) · `mode-select` · `main-menu` · `pause-menu` · `confirm-dialog` · `game-screen` · `end-screen`.
- **Нема** → пропозиції карток:
  - `+edge-spawn`, `+wildcard-tile`, `+ingredient-drop`, `+cash-out` — підтверджую (уже пропоновані: 2048/Threes, Triple Town, Candy Crush).
  - `+poker-hand-bonus` «Збіг дає карту, комбінація карт — бонус» · game-logic/score · 📎.
  - `+stamp-block` «Блок лишає фішки на клітинах, де зупинився» · entities/interact · 🌱.
  - `+dice-coin` «Плитка-кубик зі значенням, що росте з туром» · entities/state · 🌱.
  - `+self-matching-tile` «Плитка, що зникає без пари» · entities/interact · 🌱.
  - `+help-charges` «Обмежені підказки; без шляху — рятівний бонус» · game-logic/assist · 📎.
  - `+death-rewind` «Після смерті — відкат до автосейва за ресурс» · game-logic/death · 🌱.
  - `+move-during-cascade` «Хід під час падіння (ninja matching)» · entities/move · 📎.
  - `+clear-board-goal` «Мета — очистити поле» · game-logic/win · 🌱.

## Пропозиції до словників
- `+card:poker-hand-bonus` — кожен збіг кладе карту в руку; покерна комбінація карт дає очки (Six Match).
- `+card:stamp-block` — падаючий блок «штампує» фішки, які збираються збігами поверх.
- `+card:dice-coin` — плитка-кубик, чиє випадкове значення обмежене номером туру.
- `+card:self-matching-tile` — плитка, що зникає сама («glass»), без пари.
- `+card:help-charges` — лічильник підказок; коли шляху до збігу нема, підказка створює бомбу.
- `+card:death-rewind` — після смерті запропонувати відкат до автосейва за ресурс.
- `+card:move-during-cascade` — гравець ходить, поки поле ще осідає.
- `+card:clear-board-goal` — пазл-режим: прибрати всі плитки.
- `+feature:help-charges` — обмежена кількість підказок за партію з видимим лічильником.

## Джерела
- ⭐ [itch.io: Six Match](https://st33d.itch.io/six-match) — опис від автора (st33d / Aaron Steed): обмін з монетами, збіг за 6 ходів, Survival (покерні руки, діаманти внизу, Help, бомба, автосейв), Puzzle, керування.
- [App Store](https://apps.apple.com/app/six-match/id1327790148) — wild-монети за 4/перехрестя, карти й бонус, клітки штовхають лінії, кубики-монети, історія версій 1.0–1.3 (12.01.2018 — 05.01.2023).
- [Devlog](https://st33d.itch.io/six-match/devlog) — 21 пост з вересня 2017: підказки-привид, кубики, Help → бомба, тури, покерні нагороди, cash-in, Android (12.2017), iOS + glass (01.2018), PC 7×7 (08.2018), Puzzle-режим (12.2022).
- [Block Party](https://st33d.itch.io/six-match/devlog/11236/block-party) · [Help for Hints](https://st33d.itch.io/six-match/devlog/10101/help-for-hints) · [Cash-In](https://st33d.itch.io/six-match/devlog/11914/cash-in) · [PC](https://st33d.itch.io/six-match/devlog/45095/pc) — окремі механіки.

## Непевне
- (?) Що саме стається, коли 6 ходів минули без збігу: з контексту («prompt on death», коментарі) — смерть і кінець партії.
- (?) Бомба чистить ряд чи стовпець — лише з пошукового сніпета огляду AppUnwrapper (сторінка 403).
- (?) Як саме клітка «штовхає лінію» і як знімаються кубики (у devlog: кубики поводились як стіни, потім — як клітки, які можна штовхати).
- (?) Що таке «тур» точно (скільки збігів чи ходів) і як працює скло.
- (?) Чи відбуваються каскадні збіги після падіння і чи є множник.
- (?) Рік: черга каже 2018; devlog і Android-реліз — 2017 (iOS — січень 2018, PC — серпень 2018).
