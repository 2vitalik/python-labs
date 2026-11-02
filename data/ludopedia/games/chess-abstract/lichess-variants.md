---
title: Lichess variants (варіанти шахів Lichess)
slug: lichess-variants
family: chess-abstract
also: []
klass: figure
axes:
  field: square
  time: turn
  opponent: online
  info: full
  random: setup
  goal: state
year: 2014
platforms: [web, mobile]
links:
  - {kind: official, url: "https://lichess.org/variant", best: true, note: "список 8 варіантів з короткими правилами, звідти — сторінка кожного"}
  - {kind: official, url: "https://lichess.org/variant/chess960", note: "Chess960: обмеження розстановки, рокіровка «король на туру»"}
  - {kind: official, url: "https://lichess.org/variant/crazyhouse", note: "дропи взятих фігур"}
  - {kind: official, url: "https://lichess.org/variant/atomic", note: "вибух 3×3, звʼязані королі"}
  - {kind: official, url: "https://lichess.org/variant/antichess", note: "обовʼязкове взяття, король не королівський"}
  - {kind: official, url: "https://lichess.org/variant/horde", note: "36 пішаків проти армії"}
  - {kind: official, url: "https://lichess.org/variant/kingOfTheHill", note: "король у центр d4/d5/e4/e5"}
  - {kind: official, url: "https://lichess.org/variant/racingKings", note: "перегони королів до 8-го ряду"}
  - {kind: official, url: "https://lichess.org/variant/threeCheck", note: "три шахи — перемога"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=lichess+variants+explained", note: "пошук; огляди варіантів"}
stage: v1
coverage: 60
mechanics: [piece-move-patterns, piece-capture, no-move-into-check, check-stalemate, checkmate, reach-exit, destroy-all-enemies, blast-wave, move-timer, ai-opponent, legal-move-highlight, drag-drop-piece, game-settings, +castling, +pawn-promotion, +piece-drop, +forced-capture, +explosion-capture, +random-setup, +rule-variants, +check-counter]
proposes: ["+trigger:check", "+cond:in_check", "+effect:place", "+effect:explode", "+role:zone", "+ui:pocket", "+ui:check-counter", "+window:variant-select", "+feature:custom-rules", "+axis:win-condition"]
author: opus
date: 2026-11-02
---

# Варіанти Lichess — одна шахова «фізика», вісім різних правил перемоги й взяття

## Суть
Парасолька над 8 варіантами шахів на Lichess: кожен змінює рівно одну-дві осі стандартних правил — стартову розстановку, долю взятої фігури, умову перемоги або королівський статус короля. Рух фігур скрізь як у шахах ([chess.md](chess.md)); це робить набір ідеальною вправою «правила як параметри одного рушія». Окремий рейтинг на кожен варіант, свої лідерборди й турніри.

## Поле і час
- Дошка 8×8, хід = як у шахах. Контроль часу — як у стандарті (інкремент, кореспонденція).
- Відмінності поля: у Crazyhouse зʼявляються дві «кишені» (зона поза дошкою з взятими фігурами); у Three-check — лічильник шахів у стані; у Chess960 — стартова позиція з 960 варіантів (випадкова на старті партії).
- Стан позиції розширюється: кишені (Crazyhouse), лічильники шахів (Three-check), «звʼязані королі» (Atomic) — обчислюється з розстановки.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Фігури шахів (K Q R B N P) | piece | як у стандарті | патерни ходів без змін у всіх варіантах |
| Chess960 | — | 960 стартових позицій | тилові фігури випадково, симетрично; слони на різних кольорах; король між турами; рокіровка — король ходить «на туру», опиняється на c/g |
| Crazyhouse | — | кишеня на сторону | взята фігура міняє колір і йде в кишеню взявшого; хід = рух **або** дроп з кишені на порожню клітину; пішака не можна ставити на 1/8 ряд; перетворений пішак після взяття → пішак у кишеню; дроп із шахом і матом дозволено |
| Antichess | — | король не королівський | взяття обовʼязкове (вибір серед взяттів вільний); шаху нема, рокіровки нема; перетворення і в короля; перемога — втратити всі фігури або отримати пат |
| Atomic | — | радіус 1 | кожне взяття — вибух: зникають фігура, що бʼє, взята і всі не-пішаки в 8 сусідніх клітинах; король не може бити; не можна підірвати свого короля; королі поруч — «звʼязані», шахи не діють |
| Horde | — | білі: 36 пішаків, без короля | пішаки на 1-му ряду теж мають подвійний крок (але en passant по такому не можна); чорні виграють, знищивши всіх пішаків (включно з перетвореними), білі — матом |
| King of the Hill | zone | d4, d5, e4, e5 | легальний хід короля в центр = перемога; мат теж виграє |
| Racing Kings | — | без пішаків | обидві армії на 1–2 рядах; давати шах і ходити під шах заборонено; перший король на 8-му ряду виграє; якщо чорні відповідають тим самим одразу — нічия |
| Three-check | — | лічильник 0–3 на сторону | третій легальний шах = перемога; подвійний шах = 1; мат теж виграє |
| Кишеня (Crazyhouse) | zone | фігури з кількістю | джерело дропів, видна обом |
| Центр (KotH) | zone | 4 клітини | ціль-фініш для короля |

## Правила (КОЛИ → ЯКЩО → ТО)
- Базово: усі правила [chess.md](chess.md) діють, крім явно змінених нижче.
- **Chess960** — КОЛИ `game_start` → ТО `custom: «випадкова тилова розстановка з 960 з обмеженнями»`; КОЛИ `input(king onto own rook)` → ЯКЩО умови рокіровки → ТО `move(king, c|g)`, `move(rook, d|f)`.
- **Crazyhouse** — КОЛИ `contact(piece, enemy_piece)` → ТО `disappear_b`, `give(capturer, pocket, unpromoted(b))`, `set_side(b, capturer)`.
- **Crazyhouse** — КОЛИ `input(drop(kind, cell))` → ЯКЩО `has(side, kind)` and `free(cell)` and `not (kind == P and rank in {1,8})` and `legal(move)` → ТО `place(kind, cell)`, `take(side, kind)`, `end_turn`.
- **Antichess** — КОЛИ `turn_start(side)` → ЯКЩО `custom: «є хоч одне взяття»` → ТО легальні лише взяття; КОЛИ `count(own_pieces, ==, 0)` or `no_moves(side)` → ТО `win(side)`.
- **Atomic** — КОЛИ `contact(piece, enemy_piece)` → ТО `explode(cell, r=1, spare=pawns)`: `disappear_both` + усі не-пішаки в 3×3; ЯКЩО `custom: «вибух зачепив свого короля»` → хід нелегальний; ЯКЩО вибух зачепив ворожого короля → ТО `win` (пріоритетніше за будь-який шах).
- **Atomic** — КОЛИ `adjacent8(king_w, king_b)` → ТО `custom: «шахи не діють»` (жоден король не може «вибухнути» поруч).
- **Horde** — КОЛИ `count(white_pawns_and_promoted, ==, 0)` → ТО `win(black)`; білий мат → `win(white)`.
- **King of the Hill** — КОЛИ `enter(own_king, center)` → ЯКЩО `legal(move)` → ТО `win`.
- **Racing Kings** — КОЛИ `input(move)` → ЯКЩО `custom: «хід дає шах будь-якому королю»` → ТО `block`; КОЛИ `reach(white_king, rank8)` → ЯКЩО чорний король може дійти на 8-й наступним ходом і доходить → ТО `draw`; інакше `win(white)`; `reach(black_king, rank8)` першим → `win(black)`.
- **Three-check** — КОЛИ `check(side)` → ТО `counter(checks[attacker], +1)`; КОЛИ `counter(checks, ==, 3)` → ТО `win`.
- Перемога: залежить від варіанта (мат / вибух короля / усі фігури втрачено / усі пішаки знищено / центр / 8-й ряд / 3 шахи). Нічия: як у шахах + Racing-Kings «обидва на 8-му». Рахунок: 1/½/0, окремий рейтинг Glicko-2 на варіант.

## Керування і ввід
- Як у шахах: drag або клік-клік, premove, takeback-запит.
- Crazyhouse: drag фігури з кишені на дошку (або клік по фігурі в кишені → клік по клітині); Lichess також дає «drop-premove» (?).
- Chess960: рокіровка — перетягнути короля на свою туру.
- Antichess: при перетворенні завжди відкривається вибір (і король у списку), навіть з увімкненим auto-queen.

## Вікна, меню, HUD
- `variant-select` (модал «Create a game»): випадне меню Variant (Standard, Crazyhouse, Chess960, King of the Hill, Three-check, Antichess, Atomic, Horde, Racing Kings, From Position) + час, режим rated/casual, колір.
- `game-screen`: як у шахах + `pocket` (Crazyhouse — фігури з лічильниками біля годинника кожної сторони), `check-counter` (Three-check — «+2» біля імені), назва варіанта над дошкою з посиланням на правила.
- `help-window`: сторінка `/variant/<name>` з правилами й прикладами-діаграмами.
- `leaderboard`: топ гравців кожного варіанта; `profile-window` — рейтинг за кожним варіантом окремо.
- `analysis-board` з варіантом (рушій Fairy-Stockfish/мультиваріантний (?)).
- Переходи: main-menu → Create a game → variant-select → lobby/пошук → game-screen → end-screen.

## Фічі поза полем
- `custom-rules`: варіант — параметр гри при створенні виклику; окремий рейтинг, окремі турніри-арени для кожного.
- `seed-display` неявно: номер стартової позиції Chess960 (0–959) (?) і FEN.
- Решта — як у шахах: `online-multiplayer`, `ai-opponent-levels`, `puzzle-bank` (задачі здебільшого для стандарту), `replay`, `export-import` PGN з тегом `[Variant]`.

## Варіації й родичі
- Шогі — «Crazyhouse з японським набором» (дропи — канон); Bughouse — Crazyhouse на двох дошках парами (на Lichess нема).
- Сайти-конструктори правил: pychess.org (десятки варіантів), chessvariants.com (енциклопедія). Fairy-Stockfish — рушій для довільних правил.
- **Осі варіацій** (для студента — параметри рушія):
  - **Умова перемоги**: мат · вибух короля · втратити все · знищити всі пішаки · король у зону · король на ряд · N шахів.
  - **Пул фігур/старт**: стандарт · випадковий тил (960) · асиметричний (36 пішаків) · без пішаків (Racing Kings).
  - **Доля взятої фігури**: зникає · у кишеню суперника (дроп) · вибух радіусом.
  - **Легальність**: звичайна · взяття обовʼязкове · шах заборонений · шах не діє (звʼязані королі).
  - **Статус короля**: королівський · звичайна фігура (Antichess) · відсутній (Horde-білі).

## Цікавинки для курсу
- Варіант = набір параметрів одного шахового рушія (умова перемоги, доля взяття, обовʼязковість, старт) — 🥇: архітектурне завдання «правила як стратегії».
- Chess960: генерація стартової позиції з обмеженнями + узагальнена рокіровка — 🥉.
- Crazyhouse-дропи: кишеня, зміна кольору, заборони на ряд — 🥈.
- Atomic-вибух 3×3 з винятком для пішаків і перевіркою «не підірви свого короля» — 🥈.
- Antichess: обовʼязкове взяття — фільтр легальних ходів — 🥉.
- King of the Hill / Racing Kings / Three-check — нова умова перемоги поверх шахів — 🌱/📎 кожна.

## Мапа на каталог
- Є: `piece-move-patterns` · `piece-capture` · `no-move-into-check` · `check-stalemate` · `checkmate` · `reach-exit` ↔ King of the Hill / Racing Kings · `destroy-all-enemies` ↔ Horde-чорні · `blast-wave` ↔ Atomic (лише частково: тут 3×3, не хрест) · `move-timer` · `ai-opponent` · `legal-move-highlight` · `drag-drop-piece` · `game-settings` ↔ вибір варіанта.
- **Нема** → пропозиції карток:
  - `+piece-drop` «Дроп взятої фігури» · entities/legality · 🥈 · слоти {restrictions} — Crazyhouse, шогі.
  - `+forced-capture` «Обовʼязкове взяття» · entities/legality · 📎 — Antichess, шашки.
  - `+explosion-capture` «Взяття-вибух» · entities/combat · 🥉 · слоти {radius, spare} — Atomic.
  - `+random-setup` «Випадкова стартова позиція з обмеженнями» · levels/generation · 🥉 — Chess960.
  - `+rule-variants` «Варіанти правил як параметр» · game-logic/constraints · 🥇 — набір умов перемоги/взяття за перемикачем.
  - `+check-counter` «Лічильник шахів» · game-logic/win · 🌱 — Three-check.
  - (`+castling`, `+pawn-promotion` — див. chess.md.)

## Пропозиції до словників
- `+trigger:check` · `+cond:in_check` — як у chess.md (Three-check рахує шахи, Racing Kings їх забороняє).
- `+effect:place` — поставити фігуру/камінь з резерву на клітину (дроп Crazyhouse; також го, шогі, Hive).
- `+effect:explode` — зняти все в радіусі з винятками (Atomic); узагальнення `blast-wave` на 8-сусідство.
- `+role:zone` — кишеня і центр KotH (уже ⏳, підтверджую вживання).
- `+ui:pocket` — резерв фігур біля дошки з лічильниками (Crazyhouse, шогі-комадай); `+ui:check-counter`.
- `+window:variant-select` — вибір набору правил перед партією (≠ `mode-select`: змінює правила, а не формат).
- `+feature:custom-rules` (⏳ є) — підтверджую.
- `+axis:win-condition` — значення: checkmate · royal-capture · lose-all · zone · race · n-checks; корисна для всіх абстрактних ігор.

## Джерела
- ⭐ [Lichess: variants](https://lichess.org/variant) — список 8 варіантів з однорядковими правилами.
- [Chess960](https://lichess.org/variant/chess960) — обмеження розстановки, рокіровка ходом короля на туру.
- [Crazyhouse](https://lichess.org/variant/crazyhouse) — кишеня, дропи, заборона пішака на 1/8 ряд, перетворений → пішак.
- [Atomic](https://lichess.org/variant/atomic) — вибух, пішаки не вибухають, звʼязані королі, пріоритет вибуху над шахом.
- [Antichess](https://lichess.org/variant/antichess) — обовʼязкове взяття, перетворення в короля, пат = перемога.
- [Horde](https://lichess.org/variant/horde) — 36 пішаків, подвійний крок з 1-го ряду, умови перемоги.
- [King of the Hill](https://lichess.org/variant/kingOfTheHill) — центр d4/d5/e4/e5.
- [Racing Kings](https://lichess.org/variant/racingKings) — заборона шахів, нічия при відповіді чорних.
- [Three-check](https://lichess.org/variant/threeCheck) — третій шах, подвійний = один.
- YouTube: пошук «lichess variants explained».

## Непевне
- (?) Точні стартові позиції Horde (32 пішаки на 1–4 рядах + 4 на 5-му) і Racing Kings (обидві армії на рядах 1–2) — з памʼяті FEN, на сторінках лише картинки.
- (?) Drop-premove у Crazyhouse, номер позиції 960 в інтерфейсі, рушій аналізу варіантів — з памʼяті.
- (?) Як Lichess обробляє пат у Horde/Racing Kings — не перевірено.
- `year: 2014` — умовно (варіанти на Lichess зʼявлялися поступово з 2014-го (?)).
