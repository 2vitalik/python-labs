---
title: Capablanca chess (шахи Капабланки) і сімʼя 10×8
slug: capablanca-chess
aka: [Шахи Капабланки, Knighted chess, Gothic chess, Trice's chess, Embassy chess, Capablanca Random Chess, CRC]
family: chess-abstract
also: []
klass: figure
axes:
  field: square
  time: turn
  opponent: hotseat
  info: full
  random: none
  goal: state
year: 1926
platforms: [board, web, PC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Capablanca_Chess", best: true, note: "10×8, архієпископ і канцлер, розстановка, рокіровка на 3, перетворення, історія сімʼї knighted chess (Carrera 1617 … Gothic, Embassy, CRC, Seirawan)"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Gothic_chess", note: "Gothic chess — переадресація на статтю про Capablanca chess (розділ варіантів)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=capablanca+chess", note: "пошук; огляди й партії"}
stage: v1
coverage: 65
mechanics: [piece-move-patterns, piece-capture, legal-move-highlight, no-move-into-check, check-stalemate, checkmate, castling, en-passant, pawn-promotion, repetition-draw, move-notation, hot-seat, ai-opponent, ai-minimax, drag-drop-piece, cell-click, field-size-picker, rule-variants, match-setup, pocket, game-screen, end-screen, help-window, +compound-piece, +random-setup, +piece-gating, +setup-constraints, +move-count-draw]
proposes: ["+cond:reachable_by", "+cond:attacked", "+cond:moved", "+effect:choose_promotion", "+effect:gate", "+feature:board-size-variant", "+card:compound-piece", "+card:piece-gating", "+card:setup-constraints"]
author: opus
date: 2026-11-09
---

# Capablanca chess — шахи на дошці 10×8 з двома складеними фігурами: архієпископ (слон + кінь) і канцлер (тура + кінь)

## Суть
Капабланка пропонував у 1920-х розширити шахи: дошка 10×8 і дві нові фігури, кожна — **обʼєднання** двох наявних патернів. Решта — шахи: мат, рокіровка (король іде на 3), перетворення пішака (тепер і в нові фігури). Файл описує і сімʼю 10×8: Gothic (інша розстановка), Embassy, Capablanca Random (960-підхід), а також родичів Grand Chess (10×10) і Seirawan (8×8 з «вводом» фігур з руки).

## Поле і час
- Дошка 10×8 (файли a–j, ряди 1–8); Капабланка спершу пробував 10×10, але після тестів з Edward Lasker обрав 10×8 — бій починається раніше.
- Розстановка першого ряду (фінальна версія): R N **A** B Q K B **C** N R — архієпископ на c1/c8, канцлер на h1/h8; 10 пішаків на другому/сьомому ряду.
- Король стартує на полі свого кольору (у шахах — ферзь); пішаки на i-файлі в цій розстановці не захищені — головна критика.
- Покроково, як шахи.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Король | piece | — | як у шахах; при рокіровці йде на 3 поля |
| Ферзь | piece | тура + слон | як у шахах |
| Тура, слон, кінь | piece | — | як у шахах |
| Архієпископ (Archbishop, princess; Gothic — Archbishop, Janus — janus) | piece | слон + кінь | хід як слон **або** як кінь |
| Канцлер (Chancellor, empress, marshall) | piece | тура + кінь | хід як тура **або** як кінь |
| Пішак | piece | 10 на сторону | як у шахах; перетворюється також в архієпископа чи канцлера |
| Рука (Seirawan) | supply | яструб (A) + слон-elephant (C) | фігури поза дошкою, вводяться на звільнене поле |

## Правила (КОЛИ → ЯКЩО → ТО)
Складені фігури:
- КОЛИ `input(move(archbishop, to))` → ЯКЩО `custom: «to досяжна ходом слона або ходом коня»` (кандидат `+cond:reachable_by`) and `legal(move)` → ТО `move(archbishop, to)`, `end_turn`.
- КОЛИ `input(move(chancellor, to))` → ЯКЩО `custom: «to досяжна ходом тури або ходом коня»` and `legal(move)` → ТО `move(chancellor, to)`, `end_turn`.
- КОЛИ `contact(p, enemy)` → ТО `disappear_b` (взяття як у шахах для всіх фігур).
- Кінська складова стрибає (не блокується), лінійна — блокується як у слона/тури.

Рокіровка і перетворення:
- КОЛИ `input(castle(side))` → ЯКЩО `custom: «король і тура не ходили, між ними порожньо, король не під шахом і не проходить битих полів»` → ТО `move(king, 3 поля до тури)`, `move(rook, поле поруч з королем з іншого боку)` (?).
- КОЛИ `reach(pawn, last_rank)` → ТО `choose({Q, R, B, N, A, C})`, `transform(вибране)`.
- En passant і подвійний крок пішака — як у шахах (?).

Кінець:
- КОЛИ `no_moves(side)` → ЯКЩО `in_check(side)` → ТО `lose`; ЯКЩО `not in_check(side)` → ТО `draw`.
- КОЛИ `repetition` → ТО `draw` (як у шахах).

Сімʼя 10×8 і родичі (дельти):
- **Gothic** (Ed Trice, 2000–2002, патент 2002, пізніше Trice's chess): 10×8, ті самі фігури, інша розстановка (?).
- **Embassy** (Kevin Hill, 2005): 10×8, розстановка Grand Chess — усі пішаки захищені.
- **Capablanca Random** (Reinhard Scharnagl, 2004): КОЛИ `game_start` → ТО `custom: «випадкова розстановка першого ряду, дзеркальна для обох»` → ЯКЩО `custom: «усі пішаки захищені; слони на різних кольорах; ферзь і архієпископ на різних кольорах»` — 12 118 позицій.
- **Grand Chess** (Christian Freeling, 1984): 10×10, усі фігури, крім тур, стартують на ряд ближче; рокіровки нема.
- **Seirawan** (Yasser Seirawan і Bruce Harper): 8×8, класична розстановка + яструб і слон у руці. КОЛИ `input(move(p))` → ЯКЩО `custom: «p вперше сходить з поля першого ряду»` and `has(hand, hawk|elephant)` → ТО `place(x, звільнене поле)` (опційно); після рокіровки — на поле короля або тури.
- **Janus** (Werner Schöndorf, 1978): 10×8, дві фігури janus (слон + кінь).
- Предки: Carrera (1617, 8×10, centaur + champion), Bird (1874, 8×10, equerry + guard), Foster (1887, 9×9, chancellor).

- Перемога: мат · Нічия: пат, повторення.

## Керування і ввід
- Як у шахах: drag/клік фігури на легальну клітину; вікно вибору фігури при перетворенні (6 варіантів).
- Seirawan: після ходу фігурою першого ряду — запит «ввести яструба/слона на звільнене поле?» (цифрова версія).

## Вікна, меню, HUD
- `match-setup` (цифрова версія): варіант (Capablanca / Gothic / Embassy / CRC / Grand / Seirawan) → розмір дошки, розстановка.
- `game-screen`: дошка 10×8 з координатами a–j, `legal-move-highlight`, `move-list`, `player-clock`; Seirawan — `pocket` з рукою.
- `custom-window` — вибір фігури при перетворенні (+A, +C).
- `help-window` — патерни нових фігур; `end-screen` — мат/пат/нічия.
- Переходи: main-menu → match-setup → game-screen → end-screen.

## Фічі поза полем
- `custom-rules` — варіант як параметр партії; `seed-input` / номер позиції для CRC (?).
- `board-size-variant` — розмір дошки як частина варіанта (10×8, 10×10, 8×8).
- `ai-opponent-levels`, `online-multiplayer` — на сайтах варіантів (?).
- `export-import` — нотація для 10 файлів (a–j).

## Варіації й родичі
- [chess.md](chess.md) — база; [lichess-variants.md](lichess-variants.md) — Chess960 (CRC — його аналог для 10×8).
- [chess-rule-twists.md](chess-rule-twists.md) — інші правила при тих самих фігурах; тут навпаки — ті самі правила, нові фігури.
- [shogi.md](shogi.md) / Crazyhouse — дроп з руки; Seirawan — «ввід» з руки лише на звільнене поле.
- [glinski-hex-chess.md](glinski-hex-chess.md), [5d-chess.md](5d-chess.md) — інша геометрія замість нових фігур.
- **Осі варіацій**:
  - **Розмір дошки**: 8×8 (Seirawan) · 9×9 (Foster) · 10×8 (Capablanca, Gothic, Embassy, Janus) · 10×10 (Grand, рання версія Капабланки) · 10×14 (Rutland).
  - **Нові фігури**: A + C · лише A ×2 (Janus) · + amazon Q+N (Hyderabad, Kaiserspiel).
  - **Розстановка**: фіксована · захищені пішаки (Embassy, Grand) · випадкова з обмеженнями (CRC).
  - **Вхід нових фігур**: з початку на дошці · з руки на звільнене поле (Seirawan).

## Цікавинки для курсу
- Складена фігура як обʼєднання патернів (union з двох генераторів ходів) — 🌱 поверх шахового рушія з даними-патернами.
- Параметризована дошка W×H (10×8 / 10×10) і нотація a–j — 📎.
- Розстановка CRC з обмеженнями (захищені пішаки, кольори) — генерація з перевіркою — 📎; підрахунок 12 118 позицій — 🥉.
- Рокіровка з параметром «на скільки йде король» — 🌱.
- Seirawan-ввід фігури на звільнене поле — 📎.
- Оцінка цінності нових фігур для AI (A проти C проти Q) — 🥈.

## Мапа на каталог
- Є: `piece-move-patterns` ↔ складені патерни · `piece-capture` · `legal-move-highlight` · `no-move-into-check` · `check-stalemate` · `checkmate` · `castling` ↔ король на 3 · `en-passant` · `pawn-promotion` ↔ +A, +C · `repetition-draw` · `move-notation` · `hot-seat` · `ai-opponent` / `ai-minimax` · `field-size-picker` ↔ 10×8 / 10×10 · `rule-variants` · `match-setup` · `pocket` ↔ рука Seirawan.
- **Нема** → пропозиції карток:
  - `+compound-piece` «Складена фігура = обʼєднання патернів» · entities/legality · 🌱 · слоти {components: [bishop, knight] | [rook, knight] | [queen, knight]}.
  - `+piece-gating` «Ввід фігури з руки на звільнене поле» · entities/legality · 📎 — Seirawan.
  - `+setup-constraints` «Випадкова розстановка з обмеженнями» · levels/generation · 📎 · слоти {pawns_protected, bishops_opposite, Q_A_opposite} — CRC (родич `+random-setup`).
  - `+random-setup`, `+move-count-draw` — див. [lichess-variants.md](lichess-variants.md), [chess.md](chess.md).

## Пропозиції до словників
- `+cond:reachable_by(p, to, pattern)` — клітина досяжна за патерном (основа складених фігур і шахових умов загалом).
- `+cond:attacked` · `+cond:moved` · `+effect:choose_promotion` — підтверджую з [chess.md](chess.md) (рокіровка, перетворення в 6 фігур).
- `+effect:gate(x, cell)` — ввести фігуру з руки на щойно звільнене поле (Seirawan; відмінне від `place` — лише в момент ходу іншої фігури).
- `+feature:board-size-variant` — розмір дошки як частина варіанта, а не налаштування складності.
- `+card:compound-piece` · `+card:piece-gating` · `+card:setup-constraints` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Capablanca chess](https://en.wikipedia.org/wiki/Capablanca_Chess) — Revista Bimestre Cubana 1926, Lasker і 10×8, розстановка, король на 3 при рокіровці, перетворення в A/C, критика (Winter, Euwe, Tarrasch), Carrera 1617, Hyderabad, Tressau 1840, Bird 1874, Foster 1887, CRC 2004 (12 118), Gothic 2000–2002, Embassy 2005, Grand 1984, Seirawan, Janus 1978.
- [Wikipedia: Gothic chess](https://en.wikipedia.org/wiki/Gothic_chess) — відкрилась як стаття про Capablanca chess.
- YouTube: пошук «capablanca chess».

## Непевне
- (?) Куди стає тура при рокіровці (поруч із королем з іншого боку) — стаття каже лише «король на 3 поля».
- (?) Подвійний крок пішака й en passant у фінальній версії — стаття окремо не описує; у ранній 10×10 пішак міг іти до 3 полів.
- (?) Розстановка Gothic (R N B Q C K A B N R?) — точну не бачив.
- (?) CRC: «слони не на сусідніх полях» чи «на різних кольорах» — переказ інструмента неоднозначний; узяв «на різних кольорах».
- (?) Seirawan: яструб = A, слон-elephant = C — за статтею; деталі вводу після рокіровки спрощено.
- (?) Рік: перша згадка 1926; самі пропозиції — «1920-ті».
