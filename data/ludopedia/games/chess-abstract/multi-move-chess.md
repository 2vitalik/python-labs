---
title: Шахи з серіями ходів (Marseillais, Progressive)
slug: multi-move-chess
aka: [Marseillais chess, Double-move chess, Марсельські шахи, Progressive chess, Прогресивні шахи, Scotch progressive chess, Italian progressive chess, English progressive chess]
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
year: 1925
platforms: [board, web]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Marseillais_chess", best: true, note: "два ходи за хід, шах першим ходом обриває серію, en passant, збалансована версія Bruce 1963"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Progressive_chess", note: "серії 1, 2, 3…; Scottish / Italian / English правила шаху; пат, правило 10 ходів"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=marseillais+chess", note: "пошук; Marseillais"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=progressive+chess+explained", note: "пошук; Progressive"}
stage: v1
coverage: 60
mechanics: [piece-move-patterns, piece-capture, no-move-into-check, check-stalemate, checkmate, castling, en-passant, pawn-promotion, repetition-draw, turn-enforcement, hot-seat, ai-opponent, ai-minimax, async-multiplayer, drag-drop-piece, legal-move-highlight, last-move-highlight, move-notation, move-counter, rule-variants, match-setup, game-screen, end-screen, help-window, +multi-move-turn, +check-ends-series, +move-count-draw, +one-move-per-piece, +capture-all-win]
proposes: ["+cond:series_last", "+cond:moved_this_turn", "+trigger:series_end", "+ui:series-counter", "+axis:turn-structure:multi-move", "+card:multi-move-turn", "+card:check-ends-series", "+card:one-move-per-piece"]
author: opus
date: 2026-11-09
---

# Шахи з серіями ходів — за один хід робиш кілька шахових ходів, а шах обриває серію

## Суть
Звичайні шахові фігури й дошка, але хід сторони — **серія** ходів. Marseillais (1925): серія завжди з двох ходів. Progressive: серія росте — білі 1, чорні 2, білі 3, чорні 4… Уся глибина — у правилах шаху всередині серії: шах першим ходом обриває серію (Marseillais, Scottish), або шах дозволено лише останнім ходом серії (Italian). Родич Avalanche/Duck з [chess-rule-twists.md](chess-rule-twists.md): там друга дія ходу — інша сутність, тут — та сама шахова.

## Поле і час
- Дошка 8×8, фігури й розстановка — як у [chess.md](chess.md).
- Хід = серія з N одиничних ходів однієї сторони; одиничний хід — звичайний шаховий.
- Marseillais: N = 2 (у збалансованій версії перший хід білих — N = 1: Б, Ч Ч, Б Б, Ч Ч…).
- Progressive: N = номер ходу партії (1, 2, 3, 4…); партії короткі — за кілька серій армія розгорнута.
- Кожен одиничний хід серії легальний окремо: після нього свій король не під шахом.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Король, ферзь, тура, слон, кінь, пішак | piece | як у шахах | патерни без змін; одна фігура може ходити в серії кілька разів (крім English) |
| Пішак після подвійного кроку | piece | позначка «пройшов 2 клітини в минулій серії» | ціль en passant — лише першим ходом наступної серії суперника |
| Лічильник серії | — | `moves_left`, N | скільки одиничних ходів лишилось у поточній серії |
| Лічильник тихих серій (Progressive) | — | серії без взяття й ходу пішака | 10 поспіль → нічия |

## Правила (КОЛИ → ЯКЩО → ТО)
Загальний цикл серії:
- КОЛИ `turn_start(side)` → ЯКЩО `mode(marseillais)` → ТО `counter(moves_left, 2)`; ЯКЩО `mode(progressive)` → ТО `counter(moves_left, custom: «номер ходу партії»)`.
- КОЛИ `game_start` → ЯКЩО `mode(marseillais_balanced)` → ТО `counter(moves_left(white), 1)` (правило Bruce, 1963).
- КОЛИ `input(move(p, to))` → ЯКЩО `turn_of(side)` and `legal(move)` → ТО `move(p, to)`, `counter(moves_left, -1)`; інакше `block`.
- КОЛИ `counter(moves_left, =, 0)` → ТО `end_turn`.
- Рокіровка = один одиничний хід серії (Marseillais).

Шах усередині серії:
- КОЛИ `turn_start(side)` → ЯКЩО `in_check(side)` → ТО `custom: «перший хід серії мусить зняти шах»`; не можна зняти — мат, `lose`.
- КОЛИ `input(move)` → ЯКЩО `custom: «після цього ходу свій король під шахом»` → ТО `block` (у Marseillais не можна стати під шах першим ходом і втекти другим).
- КОЛИ `check(enemy)` → ЯКЩО `mode(marseillais)` or `mode(scottish)` or `mode(english)` → ТО `end_turn` (решта серії згоряє; суперник отримує свою звичайну серію).
- КОЛИ `input(move)` → ЯКЩО `mode(italian)` and `custom: «хід дає шах»` and `custom: «хід не останній у серії»` (кандидат `+cond:series_last`) → ТО `block` (шах — лише останнім ходом повної серії).
- КОЛИ `turn_start(side)` → ЯКЩО `mode(italian)` and `in_check(side)` and `custom: «єдиний вихід — дати шах першим, не останнім ходом»` → ТО `lose` («progressive checkmate»).

En passant:
- КОЛИ `input(en_passant(p, q))` → ЯКЩО `custom: «q зробив подвійний крок у минулій серії суперника (Progressive: не далі після нього)»` and `custom: «це перший хід серії»` → ТО `move(p, to)`, `disappear_b`.
- Marseillais: брати на проході можна й пішака, що ходив першим ходом серії суперника; два пішаки на проході — обидва в одній серії.
- English progressive: en passant нема.

Кінець партії:
- КОЛИ `no_moves(side)` → ЯКЩО `in_check(side)` → ТО `lose`; ЯКЩО `not in_check(side)` → ТО `draw` («progressive stalemate»: можна врятуватися, запатувавши себе).
- КОЛИ `counter(quiet_series, >=, 10)` → ЯКЩО `custom: «ніхто не має форсованого мату»` → ТО `draw` (Progressive, аналог правила 50 ходів).

Підваріанти Progressive:
- English: КОЛИ `input(move(p))` → ЯКЩО `custom: «p уже ходив у цій серії»` (кандидат `+cond:moved_this_turn`) and `custom: «є інша фігура з легальним ходом, що ще не ходила стільки ж разів»` → ТО `block`; обмеження скидається з новою серією.
- Take-All: КОЛИ `all_gone(enemy_pieces)` → ТО `win`; пішак може перетворитися на короля — `transform(king)`.
- Logical (Byway, 1995): рокіровки й подвійного кроку пішака нема → нема й en passant.

- Перемога: мат (з поправкою Italian) · взяття всіх (Take-All) · Нічия: пат, 10 тихих серій (Progressive).

## Керування і ввід
- Як у шахах: drag/клік фігури на легальну клітину; серія — послідовність таких дій без передачі ходу.
- Клієнт сам передає хід, коли `moves_left = 0` або шах обірвав серію; кнопки «кінець ходу» правила не передбачають (?).
- За дошкою — ручний підрахунок; у Progressive серії довгі, тому популярна гра поштою (стаття Wikipedia).

## Вікна, меню, HUD
- `match-setup` (цифрова версія): варіант (Marseillais / balanced / Progressive Scottish / Italian / English / Take-All).
- `game-screen`: дошка; `series-counter` («хід 2 з 5»); `turn-indicator`; `last-move-highlight` — підсвітити **усю** серію суперника, не лише останній хід; `move-list` з нотацією серій (номер ходу = номер серії); `legal-move-highlight`.
- `help-window`: правило шаху обраного підваріанта.
- `end-screen`: мат / progressive checkmate / пат / нічия 10 серій.
- Переходи: main-menu → match-setup → game-screen → end-screen.

## Фічі поза полем
- `custom-rules` — підваріант правила шаху як перемикач партії.
- `ai-opponent-levels` — пошук за серіями: гілок на хід ∝ (ходів)^N, наївний minimax не тягне (?).
- `online-multiplayer` / гра поштою (`async-multiplayer`) — партії короткі за кількістю ходів.
- `replay` по серіях.

## Варіації й родичі
- [chess-rule-twists.md](chess-rule-twists.md): Avalanche (друга фаза — штовхнути ворожого пішака), Duck (друга фаза — качка), Kung-Fu (без черги взагалі).
- Monster chess (білі — король і 4 пішаки, по два ходи) — у списку multimove-варіантів Wikipedia; Circe chess зазвичай грають прогресивно.
- Arimaa ([arimaa.md](arimaa.md)) — 4 кроки за хід, але кроки не шахові; Hive/Onitama — один хід.
- **Осі варіацій**:
  - **Довжина серії**: 1 (шахи) · 2 (Marseillais) · 1 на перший хід, далі 2 (balanced) · зростає 1, 2, 3… (Progressive).
  - **Шах у серії**: обриває серію (Marseillais, Scottish, English) · лише останнім ходом (Italian).
  - **Хто ходить у серії**: будь-яка фігура будь-скільки · по колу, поки всі не сходили (English).
  - **En passant**: першим ходом серії · нема (English, Logical).
  - **Ціль**: мат · взяти все (Take-All).

## Цікавинки для курсу
- Серія з N ходів поверх шахового рушія + передача ходу за лічильником — 📎 (лічильник + стан «чия серія»).
- Обрив серії шахом (Scottish/Marseillais) — 🌱 поверх готового `in_check`.
- Italian: «шах лише останнім ходом» і progressive checkmate — 🥉 (треба перебрати, чи існує вихід із шаху, що не дає шаху).
- English: обмеження «кожна фігура по разу, потім по два» — 📎.
- En passant крізь серію (мітка живе одну серію суперника, бити лише першим ходом) — 📎.
- AI для Progressive: пошук мату в серії з N ходів (дерево (ходів)^N) — 🥇.
- Задачі «мат за одну серію» як банк пазлів — 🥈 (генерація й розвʼязувач).

## Мапа на каталог
- Є: `piece-move-patterns` · `piece-capture` · `no-move-into-check` ↔ кожен хід серії окремо · `check-stalemate` · `checkmate` · `castling` · `en-passant` ↔ з поправкою на серію · `pawn-promotion` · `repetition-draw` ↔ правило 10 тихих серій · `turn-enforcement` · `hot-seat` · `ai-opponent` / `ai-minimax` · `async-multiplayer` ↔ гра поштою · `move-notation` · `last-move-highlight` ↔ уся серія · `move-counter` ↔ лічильник серії · `rule-variants` · `match-setup`.
- **Нема** → пропозиції карток:
  - `+multi-move-turn` «Серія ходів за хід» · game-logic/opponent · 📎 · слоти {series: fixed(2) | progressive(1,2,3…), first_turn_short} — Marseillais, Progressive, Monster.
  - `+check-ends-series` «Шах обриває / дозволений лише в кінці серії» · game-logic/constraints · 🥉 · слоти {check_rule: ends | last-only}.
  - `+one-move-per-piece` «Кожна фігура по разу до повтору в серії» · entities/legality · 📎 — English progressive.
  - `+capture-all-win` «Перемога взяттям усіх фігур» · game-logic/win · 🌱 — Progressive Take-All (родич `destroy-all-enemies`).
  - `+move-count-draw` — див. [chess.md](chess.md).

## Пропозиції до словників
- `+cond:series_last` — поточний одиничний хід останній у серії (Italian; також Arimaa-кроки).
- `+cond:moved_this_turn(p)` — фігура вже ходила в цій серії (English; відмінне від `+cond:moved` з chess.md — «ходила за партію»).
- `+trigger:series_end(side)` — серія сторони завершилась (за лічильником або обривом).
- `+ui:series-counter` — «хід k з N» у серії.
- `+axis:turn-structure:multi-move` — нове значення осі `turn-structure`: серія з кількох одиничних ходів.
- `+card:multi-move-turn` · `+card:check-ends-series` · `+card:one-move-per-piece` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Marseillais chess](https://en.wikipedia.org/wiki/Marseillais_chess) — Le Soleil 1925, популярність кінця 1930-х (Alekhine, Réti, Znosko-Borovsky, Chéron), шах першим ходом, en passant, balanced rule Bruce 1963, список multimove-варіантів.
- [Wikipedia: Progressive chess](https://en.wikipedia.org/wiki/Progressive_chess) — серії 1, 2, 3…; Scottish / Italian / English; пат; правило 10 серій; Take-All; Logical (Byway 1995); дослідження Beasley (416 матів, 158 italian progressive checkmates).
- Chess Variant Pages (Marseillais) — 403, не відкрилась.
- YouTube: пошуки «marseillais chess», «progressive chess explained».

## Непевне
- (?) Автор Marseillais — у статті не названий; відома лише публікація в Le Soleil 1925.
- (?) Автор і рік Progressive — у статті нема; Wikipedia посилається на книги Pritchard.
- (?) Рокіровка в Progressive як один хід серії — стаття явно не пише.
- (?) Italian: що буде, коли гравець не може зробити всіх N ходів серії, — не перевірено.
- (?) Marseillais: мат і пат окремо не описані; узято шахові.
- (?) Кнопка «кінець ходу» / дострокове завершення серії — правилами не передбачене, з памʼяті.
