---
title: "Passant: A Chess Roguelike"
slug: passant
aka: [Passant, «Balatro для шахів»]
family: chess-abstract
also: [roguelike]
klass: figure
axes:
  field: square
  time: turn
  opponent: ai
  info: full
  random: both
  goal: state
year: 2025
platforms: [PC]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/3353100", best: true, note: "фігури з особливими правилами, предмети, бейджі-зміни правил; серія матчів → фінальний бос; 4 рівні AI; демо"}
  - {kind: other, url: "https://www.gamegrin.com/reviews/passant-a-chess-roguelike-review", note: "огляд: 2 раунди → бос, сетапи Standard/Challenging, free pack замість раунду, 4 складності, 3 умови перемоги, Endless, sandbox"}
  - {kind: other, url: "https://rogueliker.com/passant-review/", note: "огляд: бос кожен 3-й раунд (два королі), взяти всіх = перемога, до 3 undo, наведення показує наслідки"}
  - {kind: other, url: "https://steamcommunity.com/app/3353100/discussions/0/604146775975003760", note: "форум: Petrify Chess, Camel, Princess, Buffalo, реролли, бос тасує дошку, відповіді розробника"}
  - {kind: other, url: "https://vaporlens.app/app/3353100/passant_a_chess_roguelike.md", note: "зведення відгуків: заморозка товарів у магазині, Duck, перемога очками, критика AI"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Passant+A+Chess+Roguelike+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [piece-move-patterns, piece-capture, pawn-promotion, check-stalemate, checkmate, no-move-into-check, rule-variants, run-relics, shop-between-levels, shop-catalog, round-currency, in-round-upgrades, undo-step, explode-area, status-effects, ai-opponent, difficulty-levels, sequential-levels, keep-playing-after-win, event-points, destroy-all-enemies, hover-highlight, drag-drop-piece, in-game-editor, game-screen, main-menu, shop-window, end-screen, difficulty-select, mode-select, placement-screen, +rule-badges, +consumable-items, +boss-rule-modifier, +shop-freeze-reroll, +skip-round-reward, +army-setup-board]
proposes: ["+effect:demote(a)", "+effect:petrify(a)", "+trigger:boss_round", "+cond:badge(name)", "+ui:badge-slots", "+ui:coin-slots", "+feature:shop-freeze", "+feature:shop-reroll", "+window:pack-open", "+card:rule-badges", "+card:boss-rule-modifier", "+card:shop-freeze-reroll"]
author: opus
date: 2026-11-09
---

# Passant — шахи як Balatro: між партіями купуєш фігури, монети й бейджі, що ламають правила, і йдеш до боса

## Суть
Шаховий роглайк Marc Makes Games (2025): забіг — серія шахових матчів проти AI зростаючої складності з босом кожен третій раунд. Між матчами в магазині купуєш нові фігури (Archbishop, Camel, Duck, Dragon King…), **монети** — витратні ефекти (заморозити фігуру, розжалувати ворожу в пішака, підвищити свою до ферзя) — і **бейджі**, що змінюють самі правила: Atomic Chess, Reflecting Bishops, Zombie Pawns, Petrify Chess. Сила гри — у стосі модифікаторів, як джокери в Balatro.

## Поле і час
- Шахова дошка 8×8 (?) у 3D; перед раундом свою армію розставляєш на «дошці розстановки» (Camel — лише на першому ряду).
- Матч — звичайна покрокова партія проти AI; до 3 undo на раунд.
- Забіг: раунд, раунд, бос → … → фінальний бос; далі — Endless.
- Інформація повна; випадковість — асортимент магазину, паки, боси, що тасують розстановку.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Класичні фігури | piece | — | ходи шахів; пішак перетворюється |
| Archbishop | piece | — | слон + кінь (?) |
| Princess | piece | — | король + слон (форум) |
| Camel | piece | лише 1-й ряд | стрибок (?); сильний на швидкий мат |
| Duck | piece | — | «може бути будь-де на дошці» — блокує клітину (?) |
| Dragon Knight / Dragon King | piece | — | підсилені фігури (у сьогі Dragon King = тура + король) (?) |
| Courtesan, Buffalo, Vampire, Franz Ferdinand | piece | з бейджів | особливі фігури, що їх дає бейдж |
| Amazonian | enemy | — | ворожа фігура (ферзь + кінь?) |
| Король-ворог | piece | 2 у боса | бос може виставити двох королів |
| Бейдж | — | слот | постійна зміна правил або нова фігура на забіг |
| Монета | pickup | слот, витратна | разовий ефект у матчі |
| Пак | container | — | безкоштовна нагорода замість раунду |
| Бос | boss | ефект | раунд з «унікальним і неприємним» правилом |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(move, piece, to)` → ЯКЩО `turn_of(player)` і `legal(move)` → ТО `move(piece, to)`, `end_turn`.
- КОЛИ `input(move, piece, to)` → ЯКЩО `occupied(to, enemy)` → ТО `disappear_b`, `score(вартість)` (?).
- КОЛИ `no_moves(enemy)` → ЯКЩО `in_check(enemy_king)` → ТО `win` матчу.
- КОЛИ `all_gone(enemy_non_king)` → ТО `win` (часто простіше за мат).
- КОЛИ `counter(points, >=, target)` → ЯКЩО `timer(<=, n_turns)` → ТО `win` (набрати очки за кілька ходів; поріг не названо).
- Бейдж Atomic Chess: КОЛИ `custom: «взяття»` → ЯКЩО `badge(atomic)` (`+cond:badge`) → ТО `explode(3x3)` (?).
- Бейдж Petrify Chess: КОЛИ `custom: «фігура взяла»` → ЯКЩО `custom: «це не король»` → ТО `custom: «фігура скам'яніла й більше не ходить»` (`+effect:petrify`).
- Бейдж Reflecting Bishops: КОЛИ `edge(bishop)` → ТО `bounce(bishop)` (?).
- Бейдж Zombie Pawns: `custom: «пішаки-зомбі»` — механіка не описана (?).
- Монета: КОЛИ `input(use, coin_freeze, piece)` → ТО `freeze(piece, n)`.
- Монета: КОЛИ `input(use, coin_demote, enemy_piece)` → ТО `transform(enemy_piece, pawn)` (`+effect:demote`).
- Монета: КОЛИ `input(use, coin_promote, own_piece)` → ТО `transform(own_piece, queen)`.
- Особливі фігури з бейджів: відроджуються після взяття або отримують апгрейд від фігури, яку взяли (rogueliker).
- КОЛИ `input(undo)` → ЯКЩО `counter(undos, >, 0)` → ТО `undo(1)`, `counter(undos, -1)` (до 3 на раунд).
- КОЛИ `level_end` → ЯКЩО `custom: «матч виграно»` → ТО `currency(+n)` (сума залежить від обраного сетапу Standard / Challenging), `window(shop-window)`.
- КОЛИ `input(skip_round)` → ТО `give(player, pack)`; магазину й грошей за цей раунд нема.
- КОЛИ `custom: «кожен третій раунд»` (`+trigger:boss_round`) → ТО `custom: «правило боса: два королі / перетасована розстановка / …»`.
- Режим «Pieces lost when captured»: КОЛИ `died(own_piece)` → ТО `take(army, piece)` назавжди.
- КОЛИ `custom: «переможено фінального боса»` → ТО `win` забігу → далі `mode-endless`.
- КОЛИ `no_moves(player)` і `in_check(king)` → ТО `lose` забігу (?) · Рахунок: вищі складності й challenge-рівні.

## Керування і ввід
- Миша: перетягнути або клік фігура → клітина у 3D-сцені (гравці скаржаться на незручне керування 3D).
- Наведення на фігуру — показ її ходів і наслідків найближчих дій.
- Магазин: клік купити, заморозити товар, реролл за гроші; дошка розстановки — drag фігур.
- Кнопки undo (лічильник), використання монет зі слотів.

## Вікна, меню, HUD
- `main-menu`: Новий забіг → `mode-select` (сетап Standard / Challenging, challenge-рівні) → `difficulty-select` (Beginner, Normal, Challenging, Grandmaster); спецсценарії; власна дошка (sandbox).
- `placement-screen`: дошка розстановки своєї армії перед раундом.
- `game-screen`: 3D-дошка, слоти бейджів (`+ui:badge-slots`) і монет (`+ui:coin-slots`), бічні інфоколонки з тактичними деталями, `undo-button` з лічильником, індикатори взяття, очки.
- `shop-window`: фігури, бейджі, монети; заморозка товару, реролл; окремий слот пішака за $1 (обіцяно розробником).
- `+window:pack-open` — відкриття безкоштовного пака при пропуску раунду.
- `end-screen`: перемога/поразка матчу й забігу; перехід в Endless.
- Переходи: main-menu → placement-screen → game-screen → shop-window → placement-screen → … бос → end-screen.

## Фічі поза полем
- `difficulty-presets` (4 рівні AI: що вище — то менше помилок, довше думає), challenge-рівні «tier two» стосують умови попередніх (як ставки Balatro).
- `mode-endless` після фінального боса; `mode-puzzle` — спецсценарії з обмеженнями; `mode-sandbox` / `level-editor` — власна дошка з усіх розблокованих фігур, бейджів і монет.
- `unlockables`: нові варіанти фігур на основі класичних; `achievements`, `cloud-save`, демо, `localization` (8 мов).
- `undo` (3 на раунд), `feature:shop-freeze`, `feature:shop-reroll`.

## Варіації й родичі
- Rule twists беруть ідеї відомих варіантів: Atomic chess, Duck chess, казкові фігури (Archbishop, Camel, Amazon, Dragon King із сьогі) — у корпусі `lichess-variants.md`, `chess-rule-twists.md`, `capablanca-chess.md`, `large-shogi-variants.md`.
- Роглайк-сусіди: `shotgun-king.md` (пари карт тобі+ворогу), `ouroboros-king.md` (казкова армія, рівні фігур, мапа вузлів), `chess-survivors.md`, `roguelike/pawnbarian.md`.
- **Відмінність від Ouroboros King**: тут головний важіль — бейджі, що змінюють **правила гри** для всієї дошки, і економіка магазину в стилі Balatro (реролл, заморозка, пак замість раунду), а не ріст окремих фігур.
- Осі варіацій: **що модифікується** (фігура / правило / ворог) · **як перемогти** (мат / усіх / очки за N ходів) · **ціна пропуску** (пак без магазину) · **втрата фігур** (лише в матчі / назавжди).

## Цікавинки для курсу
- Бейджі як модифікатори генератора ходів і обробника взяття (Atomic, Petrify, Reflecting) — правило як підключаваний обʼєкт — 🥈.
- Три умови перемоги матчу (мат / усі не-королі / очки за N ходів) одночасно — 📎.
- Магазин Balatro-типу: асортимент, реролл, заморозка товару, пак замість раунду — 🥉.
- AI, що не ламається від змінених правил (форум: AI міняє цінні фігури на пішаків під Petrify) — оцінка позиції через реальні правила — 🥇.
- Undo з лімітом на раунд — 🌱.
- Бос з модифікатором (два королі, перетасована розстановка) — 📎.

## Мапа на каталог
- Є в каталозі: `piece-move-patterns`, `piece-capture`, `pawn-promotion`, `check-stalemate`, `checkmate`, `no-move-into-check` · `rule-variants` ↔ бейджі-правила · `run-relics` ↔ бейджі · `shop-between-levels`, `shop-catalog`, `round-currency` · `in-round-upgrades` ↔ монети · `undo-step` ↔ 3 undo · `explode-area` ↔ Atomic · `status-effects` ↔ заморозка/камінь · `ai-opponent`, `difficulty-levels` · `sequential-levels`, `keep-playing-after-win` ↔ Endless · `event-points` ↔ перемога очками · `destroy-all-enemies` ↔ «взяти всіх» · `hover-highlight`, `drag-drop-piece` · `in-game-editor` ↔ sandbox · `game-screen`, `main-menu`, `shop-window`, `end-screen`, `difficulty-select`, `mode-select`, `placement-screen`.
- **Нема** → пропозиції карток:
  - `+rule-badges` «Бейджі: модифікатори правил на забіг» · game-logic/rules · 🥈 · слоти {slots, stack}.
  - `+consumable-items` «Витратні монети-ефекти в матчі» · game-logic/economy · 📎.
  - `+boss-rule-modifier` «Бос-раунд з особливим правилом» · game-logic/opponent · 📎.
  - `+shop-freeze-reroll` «Заморозка товару й реролл асортименту» · game-logic/economy · 📎.
  - `+skip-round-reward` «Пропустити раунд за пак без магазину» · game-logic/economy · 🌱.
  - `+army-setup-board` «Розстановка своєї армії перед раундом» · interface/input · 📎.

## Пропозиції до словників
- `+effect:demote(a)` — фігура понижується до базової (до пішака).
- `+effect:petrify(a)` — сутність назавжди втрачає здатність ходити, лишаючись на полі (окремий випадок `set_state`).
- `+trigger:boss_round` — настав бос-раунд (кожен N-й).
- `+cond:badge(name)` — у забігу активний модифікатор правил.
- `+ui:badge-slots` · `+ui:coin-slots` — слоти постійних і витратних модифікаторів.
- `+feature:shop-freeze` — зберегти товар магазину на наступний візит; `+feature:shop-reroll` — оновити асортимент за гроші.
- `+window:pack-open` — відкриття пака-нагороди.
- `+card:rule-badges`, `+card:boss-rule-modifier`, `+card:shop-freeze-reroll` — див. «Мапа на каталог».

## Джерела
- ⭐ [Steam: Passant](https://store.steampowered.com/app/3353100) — фігури Archbishop/Dragon Knight/Dragon King, правила Atomic/Reflecting Bishops/Zombie Pawns, монети (заморозити, розжалувати, підвищити), серія матчів → бос, рівні AI, challenge-режими, реліз 11.08.2025.
- [GameGrin: огляд](https://www.gamegrin.com/reviews/passant-a-chess-roguelike-review) — 2 раунди перед босом, сетапи Standard/Challenging визначають гроші, free pack замість раунду, 4 складності, 3 умови перемоги, Endless, спецсценарії, sandbox, Duck.
- [Rogueliker: огляд](https://rogueliker.com/passant-review/) — бос кожен 3-й раунд (два королі), взяти всіх = перемога, магазин і переставлення армії, відродження/апгрейд від взятої фігури, до 3 undo, наведення з наслідками.
- [Steam-форум](https://steamcommunity.com/app/3353100/discussions/0/604146775975003760) — Petrify Chess, Buffalo Buffalo, Franz Ferdinand, The Vampire, Camel (лише 1-й ряд), Princess (король + слон), Amazonian, реролли, режим «pieces lost when captured», бос тасує дошку.
- [Vaporlens: зведення відгуків](https://vaporlens.app/app/3353100/passant_a_chess_roguelike.md) — заморозка товарів, Duck, перемога очками / «dead points», 3 undo, критика AI й 3D-керування.

## Непевне
- (?) Розмір дошки (вважаю 8×8) і стартова армія сетапів Standard / Challenging.
- (?) Точні ходи Archbishop, Camel, Duck, Dragon Knight/King, Amazonian, Courtesan у грі (тут — за класичними казковими шахами).
- (?) Що саме роблять Reflecting Bishops (відбиття від краю?) і Zombie Pawns; радіус Atomic.
- (?) Поріг очок і кількість ходів для перемоги очками; що таке «dead points».
- (?) Скільки босів у забігу, чи поразка в одному матчі завершує забіг; заявлена в черзі цифра «100+ модифікаторів» у відкритих джерелах не підтверджена.
- (?) Розбіжність: GameGrin — «два раунди, потім бос», Rogueliker — «бос кожен третій раунд» (те саме, якщо бос — 3-й раунд).
