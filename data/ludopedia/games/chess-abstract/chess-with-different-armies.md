---
title: Chess with Different Armies (шахи різних армій, Betza)
slug: chess-with-different-armies
aka: [Шахи з різними арміями, Betza's Chess, Equal Armies, CwDA]
family: chess-abstract
also: []
klass: figure
axes:
  field: square
  time: turn
  opponent: hotseat
  info: full
  random: setup
  goal: state
year: 1979
platforms: [board, PC, web]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Chess_with_different_armies", best: true, note: "чотири офіційні армії з ходами й Betza-нотацією, перетворення, рокіровка Clobberers, тести балансу Fairy-Max, неофіційні армії"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Fairy_chess_piece", note: "атоми фігур (ферзь, альфіл, вазир, дабаба) і нотація (лінк зі статті)"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Ralph_Betza", note: "автор (лінк зі статті)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=chess+with+different+armies", note: "пошук; огляди армій"}
stage: v1
coverage: 60
mechanics: [piece-move-patterns, piece-capture, legal-move-highlight, no-move-into-check, check-stalemate, checkmate, castling, en-passant, pawn-promotion, repetition-draw, move-notation, hot-seat, ai-opponent, ai-minimax, drag-drop-piece, cell-click, character-select, match-setup, rule-variants, codex-window, game-screen, end-screen, help-window, +army-select, +compound-piece, +asymmetric-armies, +piece-notation-dsl, +colorbound-piece, +self-play-balance]
proposes: ["+cond:reachable_by", "+cond:in_army", "+effect:choose_promotion", "+window:army-select", "+ui:move-diagram", "+feature:army-randomizer", "+axis:symmetry", "+card:asymmetric-armies", "+card:piece-notation-dsl", "+card:colorbound-piece", "+card:self-play-balance"]
author: opus
date: 2026-11-09
---

# Chess with Different Armies — шахи, де в кожної сторони свій набір феї-фігур, рівний за силою, але інший за характером

## Суть
Ральф Бетца (1979) замінив чотири типи фігур — тур, коней, слонів і ферзя — на чотири різні «армії» з феї-фігурами; король і пішаки скрізь стандартні. Сторони обирають армію навмання або таємно, і партія FIDE проти Nutty Knights — це гра двох різних наборів патернів за спільними правилами шахів. Баланс задано не симетрією, а оцінкою цінності фігур (тестували майстри, згодом — рушій Fairy-Max). Для курсу це вправа «патерн ходу як дані» і питання «як виміряти силу асиметричних сторін».

## Поле і час
- Дошка 8×8, розстановка як у шахах: кожна нова фігура стоїть на місці тієї, яку замінює (тура / кінь / слон / ферзь).
- Хід — як у шахах; шах, мат, пат, рокіровка, en passant.
- Асиметрія — лише в наборах фігур; дзеркальна партія (обидві однакові армії) теж можлива (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Король, пішаки | piece | у всіх арміях | як у шахах |
| **Fabulous FIDEs** | piece | тура, кінь, слон, ферзь | стандартні фігури |
| **Colorbound Clobberers**: Bede (BD) | piece | на місці тури | як слон або дабаба (стрибок на 2 ортогонально) |
| Clobberers: Waffle (WA) | piece | на місці коня | вазир (1 ортогонально) або альфіл (стрибок на 2 по діагоналі); усі ходи — стрибки |
| Clobberers: FAD | piece | на місці слона | ферзь-крок (1 по діагоналі), альфіл або дабаба; усі ходи — стрибки |
| Clobberers: Cardinal (NB) | piece | на місці ферзя | слон або кінь |
| **Nutty Knights**: Charging Rook (frlRrlbK) | piece | на місці тури | уперед і вбік як тура, назад як король |
| Nutty: Fibnif (fbNF) | piece | на місці коня | ферзь-крок або два «найдовших вертикальних» ходи коня вперед і назад |
| Nutty: Charging Knight (fhNrlbK) | piece | на місці слона | уперед як кінь, назад і вбік як король |
| Nutty: Colonel (fhNfrlRK) | piece | на місці ферзя | як король, уперед і вбік як тура, уперед як кінь |
| **Remarkable Rookies**: Short Rook (W4) | piece | на місці тури | як тура, до 4 клітин |
| Rookies: Woody Rook (WD) | piece | на місці коня | вазир або дабаба; стрибки |
| Rookies: Half Duck (HFD) | piece | на місці слона | трильопер (стрибок на 3 ортогонально), дабаба або ферзь-крок; стрибки |
| Rookies: Chancellor (RN) | piece | на місці ферзя | тура або кінь |
| Армія | zone | 4 офіційні + неофіційні | набір із 4 типів, що замінює R N B Q однієї сторони |

## Правила (КОЛИ → ЯКЩО → ТО)
Старт:
- КОЛИ `game_start` → ТО `choose(army)` кожною стороною: випадково або таємно обома (турнірне правило) (кандидат `+feature:army-randomizer`).
- КОЛИ `game_start` → ТО `custom: «R N B Q кожної сторони замінити фігурами її армії на тих самих полях»`.

Рух і взяття:
- КОЛИ `input(move(p, to))` → ЯКЩО `custom: «to досяжна за Betza-патерном p»` (кандидат `+cond:reachable_by`) and `legal(move)` → ТО `move(p, to)`, `end_turn`.
- Стрибкові складові (D, A, H, N) не блокуються; ковзні (R, B, W4) — блокуються, як у шахах.
- Асиметричні (f/b/l/r) патерни Nutty Knights орієнтовані відносно своєї сторони: «вперед» у білих і чорних різне.
- КОЛИ `contact(p, enemy)` → ТО `disappear_b`.

Перетворення і рокіровка:
- КОЛИ `reach(pawn, last_rank)` → ТО `choose(options)` → ЯКЩО `custom: «вибрана фігура — з армії однієї зі сторін, що були на дошці на старті»` (кандидат `+cond:in_army`) → ТО `transform(вибране)`.
- КОЛИ `input(castle(long))` → ЯКЩО `custom: «армія Clobberers (заміна тури колорбаунд)»` → ТО `move(king, b1)`, `move(rook_replacement, c1)` — щоб фігура не змінила колір полів; інакше рокіровка як у шахах.

Кінець — як у шахах:
- КОЛИ `no_moves(side)` → ЯКЩО `in_check(side)` → ТО `lose`; ЯКЩО `not in_check(side)` → ТО `draw`.
- КОЛИ `repetition` → ТО `draw`.
- Перемога: мат · Нічия: пат, повторення.

Баланс (дані, а не правило):
- Задум: армії рівні за силою з різними властивостями; оцінка — ігри майстрів.
- 2010, H. G. Muller (Fairy-Max): Nutty Knights ≈ на пішака сильніші за FIDE; Clobberers — трохи менше ніж на пішака.
- 2015, 400 партій: Rookies +62 %, Nutters +19 %, Clobberers −11 %, FIDE −71 % (похибка ≈2 %) — FIDE найслабша.
- Неофіційні правки «ослабити сильну армію»: Drunken Night (fhNrlWbF), Busy Beaver (BzB2), Prime Minister, Short Rook W2.

Нотація Бетци (Betza funny notation) — спосіб записати фігуру рядком:
- Атоми-стрибуни: `W` вазир (1 ортогонально) · `F` ферзь-крок (1 по діагоналі) · `D` дабаба (2 ортогонально, стрибок) · `A` альфіл (2 по діагоналі) · `N` кінь · `H` трильопер (3 ортогонально).
- Ковзні: `R` = W без обмеження, `B` = F без обмеження; число — ліміт (`W4` = тура до 4).
- Префікси напрямку: `f` уперед · `b` назад · `l`/`r` ліворуч/праворуч; складена фігура — конкатенація (`RN` = тура або кінь) (?).

## Керування і ввід
- Як у шахах: drag/клік фігури на легальну клітину (цифрова версія); підсвітка легальних ходів тут необхідна — патерни незнайомі.
- Вибір армії перед партією: обидва гравці наосліп (паперовий конверт / одночасний клік) або генератор випадку.
- Перетворення: вибір із фігур обох армій партії.

## Вікна, меню, HUD
- `army-select` (цифрова версія; `character-select`): 4 армії з мініатюрами фігур, режим «випадково» / «наосліп обома».
- `match-setup`: суперник (людина / AI), контроль часу, дозволені армії (офіційні + неофіційні).
- `game-screen`: дошка, дві різні армії, `legal-move-highlight`, `move-diagram` — діаграма ходу фігури під курсором, `move-list`, `player-clock`.
- `codex-window` — довідник фігур з Betza-рядками й діаграмами.
- `custom-window` — вибір фігури при перетворенні (до 8 варіантів з обох армій).
- `end-screen` — мат/пат/нічия, армії сторін.
- Переходи: main-menu → match-setup → army-select → game-screen → end-screen.

## Фічі поза полем
- `custom-rules` — набір армій як параметр; редактор своєї армії з Betza-рядка (Fairy-Max, Zillions) (?).
- `ai-opponent-levels` — Fairy-Max / XBoard грає CwDA (?).
- `stats` — статистика перемог за парами армій (основа балансу).
- `export-import` — PGN з тегом армій (?).

## Варіації й родичі
- [chess-2-sequel.md](chess-2-sequel.md) — шість асиметричних армій Sirlin (нащадок ідеї).
- [capablanca-chess.md](capablanca-chess.md) — складені фігури (канцлер = Chancellor Rookies, архієпископ = Cardinal Clobberers).
- [really-bad-chess.md](really-bad-chess.md) — випадковий склад армії замість збалансованого.
- [large-shogi-variants.md](large-shogi-variants.md) — десятки феї-фігур, Betza як мова опису.
- [chess-rule-twists.md](chess-rule-twists.md), [lichess-variants.md](lichess-variants.md) — змінюють правила, не фігури.
- Ранній задум Бетци — 8 армій з нестандартними королями й пішаками Berolina; лишилось 4.
- **Осі варіацій**:
  - **Симетрія сторін**: дзеркальні армії · різні армії рівної сили · випадкові (Really Bad Chess).
  - **Вибір армії**: випадково · таємно обома · відкрито по черзі · програвший змінює (Chess 2).
  - **Тип фігур**: стрибуни · ковзні · обмежені ковзні (W4) · напрямлені (f/b) · колорбаунд.
  - **Перетворення**: у свої · у фігури обох армій партії.

## Цікавинки для курсу
- Парсер нотації Бетци → генератор ходів (атоми, модифікатори, ліміт) — 🥈.
- Колорбаунд-фігура: перевірка «ходить лише по полях одного кольору» і поправка рокіровки — 📎.
- Напрямлені патерни (f/b) з дзеркаленням для чорних — 🌱.
- Вікно вибору армії наосліп для двох — 📎.
- Самогра AI проти AI на сотнях партій і таблиця «армія × армія» з % перемог — 🥇 (оцінка балансу, довірчий інтервал).
- Оцінка цінності фігури за мобільністю (середня кількість ходів з усіх клітин) — 🥉.

## Мапа на каталог
- Є: `piece-move-patterns` ↔ 16 нових патернів · `piece-capture` · `legal-move-highlight` · `no-move-into-check` · `check-stalemate` · `checkmate` · `castling` ↔ поправка Clobberers · `en-passant` · `pawn-promotion` ↔ у фігури обох армій · `repetition-draw` · `move-notation` · `hot-seat` · `ai-opponent` / `ai-minimax` · `drag-drop-piece` · `cell-click` · `character-select` ↔ вибір армії · `match-setup` · `rule-variants` · `codex-window` ↔ довідник фігур · `game-screen` · `end-screen` · `help-window`.
- **Нема** → пропозиції карток:
  - `+asymmetric-armies` «Сторони з різними наборами фігур рівної сили» · entities/legality · 📎 · слоти {armies: [FIDE, Clobberers, Nutty, Rookies], pick: random|blind}.
  - `+piece-notation-dsl` «Фігура з рядка нотації (Betza)» · code/architecture · 🥈 · слоти {atoms: W F D A N H, mods: f b l r, limit}.
  - `+colorbound-piece` «Фігура лише на полях одного кольору» · entities/legality · 🌱.
  - `+self-play-balance` «Баланс сторін самогрою AI» · game-logic/opponent · 🥇 · слоти {games, engine}.
  - `+army-select`, `+compound-piece` — див. [chess-2-sequel.md](chess-2-sequel.md), [capablanca-chess.md](capablanca-chess.md).

## Пропозиції до словників
- `+cond:reachable_by(p, to)` — підтверджую ([capablanca-chess.md](capablanca-chess.md)); тут — з Betza-рядка.
- `+cond:in_army(kind, armies)` — тип фігури належить одній з армій партії (обмеження перетворення).
- `+effect:choose_promotion` — підтверджую з [chess.md](chess.md).
- `+window:army-select` — підтверджую з [chess-2-sequel.md](chess-2-sequel.md).
- `+ui:move-diagram` — підтверджую з [large-shogi-variants.md](large-shogi-variants.md).
- `+feature:army-randomizer` — випадковий / сліпий вибір армій перед партією.
- `+axis:symmetry` — `mirror` · `asymmetric-balanced` · `asymmetric-random` (симетрія сторін як вісь опису гри).
- `+card:asymmetric-armies` · `+card:piece-notation-dsl` · `+card:colorbound-piece` · `+card:self-play-balance` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Chess with different armies](https://en.wikipedia.org/wiki/Chess_with_different_armies) — автор і рік (1979), чотири армії з Betza-рядками, вибір армій, перетворення в фігури обох армій, рокіровка Clobberers, тести 2010 і 2015, ослаблені версії; неофіційні армії (стаття довга, дочитав до половини).
- [Wikipedia: Fairy chess piece](https://en.wikipedia.org/wiki/Fairy_chess_piece) · [Ralph Betza](https://en.wikipedia.org/wiki/Ralph_Betza) — лінки зі статті, не відкривав.
- YouTube: пошук «chess with different armies».

## Непевне
- (?) Рік: у черзі 1996, Wikipedia — 1979; узяв 1979 (публікації на Chess Variant Pages могли бути 1996).
- (?) Чи дозволені дзеркальні пари (FIDE проти FIDE) у турнірному правилі.
- (?) Betza-модифікатор `h` у fhN і точна семантика `rlb`/`fb` у Nutty Knights — переказ статті, власним розбором не перевірено.
- (?) Неофіційні армії 3.4–3.15 (Forward FIDEs, Knishop, Bishight…) — бачив лише початок списку.
- (?) Цифрові реалізації (Fairy-Max, Zillions, сайти) і їхні вікна — з памʼяті.
